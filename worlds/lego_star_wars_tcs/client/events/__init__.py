import inspect
import logging
from dataclasses import dataclass, field
from functools import cached_property
from typing import Callable, TypeVar, Any, ClassVar, Generic, Awaitable, overload, cast

from ..common import ClientComponent
from ..common_addresses import AREA_DATA_ID, is_actively_playing
from ..type_aliases import TCSContext


debug_logger = logging.getLogger("TCS Debug")


@dataclass
class Event:
    _subclasses: "ClassVar[dict[str, type[Event]]]" = {}
    context: TCSContext

    def __init_subclass__(cls, **kwargs):
        Event._subclasses[cls.__name__] = cls

    @staticmethod
    def get_subclass(subclass_name: str) -> "type[Event]":
        return Event._subclasses[subclass_name]


_Subscriber = TypeVar("_Subscriber")
_T = TypeVar("_T")


@dataclass
class EventManager:
    subscriptions: dict[type[Event], list[Callable[[Event], None]]] = field(default_factory=dict)
    async_subscriptions: dict[type[Event], list[Callable[[Event], Awaitable[None]]]] = field(default_factory=dict)

    def fire_event(self, event: Event):
        event_type = type(event)

        # The tick event fires too frequently for logging.
        if event_type is not OnGameWatcherTickEvent:
            debug_logger.info("Firing event %s", event)

        if event_type in self.async_subscriptions:
            # Maybe they could be run as tasks in the background instead, but avoid the extra complexity for now.
            raise RuntimeError(f"There are async subscribers of {event}, so fire_event cannot be used.")
        for subscriber in self.subscriptions.get(event_type, ()):
            subscriber(event)

    async def fire_event_async(self, event: Event):
        """Fire an event, but async, so that the loop awaits before calling each subscribed method."""
        event_type = type(event)

        # The tick event fires too frequently for logging.
        if event_type is not OnGameWatcherTickEvent:
            debug_logger.info("Firing async event %s", event)

        for async_subscriber in self.async_subscriptions.get(event_type, ()):
            await async_subscriber(event)
        # Support for mixed subscribers.
        for subscriber in self.subscriptions.get(event_type, ()):
            await self._fire_event_async(subscriber, event)

    @staticmethod
    async def _fire_event_async(subscriber: Callable[[Event], None], event: Event):
        subscriber(event)

    def subscribe_events(self, instance: _Subscriber) -> _Subscriber:
        subscriber: EventSubscriber
        members = inspect.getmembers(instance, lambda member: isinstance(member, _EventSubscriberBase))
        if members:
            debug_logger.info("Subscribing to events on %s", instance)
        for _method_name, subscriber in members:
            func = subscriber.fun
            event_type = subscriber.event_subscription
            bound_method = func.__get__(instance)
            if isinstance(subscriber, EventSubscriber):
                self.subscriptions.setdefault(event_type, []).append(bound_method)
            elif isinstance(subscriber, AsyncEventSubscriber):
                self.async_subscriptions.setdefault(event_type, []).append(bound_method)
            else:
                # Should never happen.
                raise TypeError(f"Unexpected type {subscriber}({type(subscriber)})")
            debug_logger.info("\tSubscribed to %s on %s", event_type.__name__, func.__qualname__)

        return instance

    def subscribe_method(self, method, event_type: type[Event]):
        # todo: Validate the method.
        if not issubclass(event_type, Event):
            raise ValueError("event_type should be an Event subclass")
        self.subscriptions.setdefault(event_type, []).append(method)


EVENT = TypeVar("EVENT", bound=Event)


class _EventSubscriberBase(Generic[_Subscriber, EVENT, _T]):
    event_subscription: type[EVENT]
    fun: Callable[[_Subscriber, EVENT], _T]

    def __init__(self, event_type: type[EVENT], fun: Callable[[_Subscriber, EVENT], _T]):
        self.event_subscription = event_type
        self.fun = fun

    # __set_name__ is used to check that the owner of the decorated method is a valid target for subscribing to
    # events.
    # If it worked, it would have been much simpler to set `fun.__set_name__` and then just return `fun`.
    def __set_name__(self, owner, name):
        if not issubclass(owner, ClientComponent):
            raise TypeError(
                f"{subscribe_event.__name__} can only be used in classes that inherit from ClientComponent."
                f"Use on {owner.__qualname__} is not allowed.")
        else:
            debug_logger.info("@subscribe_event{%s} usage on %s",
                              self.event_subscription.__name__, owner.__qualname__)

    def __get__(self, instance, owner):
        # noinspection PyUnresolvedReferences
        return self

    def __call__(self, other_self: _Subscriber, event: EVENT):
        # Allow direct calling if needed.
        return self.fun(other_self, event)


class EventSubscriber(_EventSubscriberBase[_Subscriber, EVENT, None]):
    def __init__(self, event_type: type[EVENT], fun: Callable[[_Subscriber, EVENT], None]):
        super().__init__(event_type, fun)


class AsyncEventSubscriber(_EventSubscriberBase[_Subscriber, EVENT, Awaitable]):
    def __init__(self, event_type: type[EVENT], fun: Callable[[_Subscriber, EVENT], Awaitable]):
        super().__init__(event_type, fun)


@overload
def subscribe_event(fun: Callable[[_Subscriber, EVENT], None]) -> EventSubscriber[_Subscriber, EVENT]: ...


@overload
def subscribe_event(fun: Callable[[_Subscriber, EVENT], Awaitable]) -> AsyncEventSubscriber[_Subscriber, EVENT]: ...


def subscribe_event(fun: Callable[[_Subscriber, EVENT], None] | Callable[[_Subscriber, EVENT], Awaitable]
                    ) -> EventSubscriber[_Subscriber, EVENT] | AsyncEventSubscriber[_Subscriber, EVENT]:
    params = inspect.signature(fun).parameters
    params_iter = iter(params.values())
    # Skip the 'self' argument.
    next(params_iter)
    event_type = next(params_iter).annotation
    if issubclass(event_type, Event):
        pass
    elif isinstance(event_type, str):
        event_type = Event.get_subclass(event_type)
    else:
        raise ValueError(f"Invalid function to subscribe to events, the second argument should have an Event type"
                         f" annotation, but got {event_type}")

    if inspect.iscoroutinefunction(fun):
        return AsyncEventSubscriber(event_type, cast(Callable[[_Subscriber, EVENT], Awaitable], fun))
    else:
        return EventSubscriber(event_type, cast(Callable[[_Subscriber, EVENT], None], fun))


@dataclass
class OnLevelChangeEvent(Event):
    """Called when the current level changes."""
    old_level_id: int
    new_level_id: int

    def __str__(self):
        return f"{type(self).__name__}({self.old_level_id} -> {self.new_level_id})"


@dataclass
class OnAreaChangeEvent(Event):
    """Called when the current area changes."""
    old_p_area_data: int
    new_p_area_data: int

    def __str__(self):
        return f"{type(self).__name__}(0x{self.old_p_area_data:x} -> 0x{self.new_p_area_data:x})"

    @cached_property
    def new_area_data_id(self) -> int:
        if not self.new_p_area_data:
            return -1
        else:
            return AREA_DATA_ID.get(self.context, self.new_p_area_data)

    @cached_property
    def old_area_data_id(self) -> int:
        if not self.old_p_area_data:
            return -1
        else:
            return AREA_DATA_ID.get(self.context, self.old_p_area_data)


@dataclass
class OnReceiveSlotDataEvent(Event):
    """Called when slot data is received."""
    slot_data: dict[str, Any]
    first_time_setup: bool
    """Whether first-time setup should be performed."""
    generator_version: tuple[int, int, int] = field(init=False)
    """The version of the Lego Star Wars: TCS apworld that generated the multiworld"""

    def __post_init__(self):
        # Setting the version is structured this way to satisfy type checking.
        major, minor, patch = self.slot_data["apworld_version"]
        assert isinstance(major, int)
        assert isinstance(minor, int)
        assert isinstance(patch, int)
        self.generator_version = (major, minor, patch)


@dataclass
class OnGameWatcherTickEvent(Event):
    """Called on each tick of the game watcher loop, while loaded into the game."""
    tick_count: int
    """
    A strictly increasing tick count of game watcher ticks while loaded into the game.
    Reset to zero upon no longer being loaded into the game.
    Use modular arithmetic to run tick event callbacks less frequently.
    """

    @cached_property
    def is_actively_playing(self) -> bool:
        """
        Get whether the player is actively playing the game (not paused/alt-tabbed/in a cutscene/in the shop/etc.).

        This property is cached the first time it is accessed.
        """
        return is_actively_playing(self.context)


@dataclass
class OnPlayerCharacterIdChangeEvent(Event):
    """Called whenever P1 or P2's character ID changes."""
    old_p1_character_id: int | None
    old_p2_character_id: int | None
    new_p1_character_id: int | None
    new_p2_character_id: int | None
