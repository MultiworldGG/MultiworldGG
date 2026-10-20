from rule_builder.rules import NestedRule, FieldResolver, Rule, OptionFilter, True_, False_, And, Or, resolve_field
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any, Self
from typing_extensions import TypeVar, override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart

if TYPE_CHECKING:
    from . import PokemonSnapWorld
else:
    PokemonSnapWorld = TypeVar("PokemonSnapWorld")

# TODO: I copied this from 0.6.8 commits. Remove this when 0.6.8 is stable and commonly used.
class AtLeast(NestedRule[PokemonSnapWorld], game="Pokemon Snap"):
    """A rule that returns true when at least N child rules evaluate as true"""

    count: int | FieldResolver

    def __init__(
        self,
        count: int | FieldResolver,
        *children: Rule[PokemonSnapWorld],
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(*children, options=options, filtered_resolution=filtered_resolution)
        self.count = count

    @override
    def _instantiate(self, world: PokemonSnapWorld) -> Rule.Resolved:
        count = resolve_field(self.count, world, int)
        if count == 0:
            return True_().resolve(world)

        children_to_process = [c.resolve(world) for c in self.children]
        return AtLeast.from_resolved(count, world, children_to_process)

    @classmethod
    def from_resolved(cls, count: int, world: PokemonSnapWorld, children_to_process: list[Rule.Resolved]) -> Rule.Resolved:
        clauses: list[Rule.Resolved] = []

        while children_to_process:
            child = children_to_process.pop(0)
            if child.always_true:
                if count == 1:
                    return child
                count -= 1
                continue
            if child.always_false:
                # falses can be ignored
                continue

            clauses.append(child)

        if len(clauses) < count:
            return False_().resolve(world)
        if count == 1:
            # Switch to Or which has more optimized handling
            return Or.from_resolved(world, clauses)
        if count == len(clauses):
            # Switch to And which has more optimized handling
            return And.from_resolved(world, clauses)
        return AtLeast.Resolved(
            tuple(clauses),
            count=count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def to_dict(self) -> dict[str, Any]:
        output = super().to_dict()
        count = self.count
        output["count"] = count.to_dict() if isinstance(count, FieldResolver) else count
        return output

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[PokemonSnapWorld]") -> Self:
        args = cls._parse_field_resolvers(data, world_cls.game)
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        children = [world_cls.rule_from_dict(c) for c in data.get("children", ())]
        return cls(
            args.pop("count"),
            *children,
            options=options,
            filtered_resolution=data.get("filtered_resolution", False),
        )

    class Resolved(NestedRule.Resolved):
        count: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            count = self.count
            for rule in self.children:
                if rule(state):
                    if count == 1:
                        return True
                    count -= 1
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "At least "},
                    {"type": "color", "color": "cyan", "text": str(self.count)},
                    {"type": "text", "text": " of ("},
                ]
            else:
                satisfied_count = sum(1 if child(state) else 0 for child in self.children)
                messages = [
                    {"type": "text", "text": "At least "},
                    {"type": "color", "color": "cyan", "text": f"{satisfied_count}/{self.count}"},
                    {"type": "text", "text": " of ("},
                ]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": ", "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = ", ".join([c.explain_str(state) for c in self.children])
            if state is None:
                return f"At least {self.count} of ({clauses})"
            satisfied_count = sum(1 if child(state) else 0 for child in self.children)
            return f"At least {satisfied_count}/{self.count} of ({clauses})"

        @override
        def __str__(self) -> str:
            clauses = ", ".join([str(c) for c in self.children])
            return f"At least {self.count} of ({clauses})"