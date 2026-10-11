from __future__ import annotations


class BaseState:
    """Lightweight lifecycle marker for state classes wanting enter()/exit()
    semantics. Everything reads/writes pine directly now."""

    _active: bool = False

    def enter(self) -> None:
        self._active = True
        self._register_handlers()
        self.on_enter()

    def exit(self) -> None:
        self._active = False
        self._unregister_handlers()
        self.on_exit()

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def _register_handlers(self) -> None:
        pass

    def _unregister_handlers(self) -> None:
        pass

    def sync(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(active={self._active})"
