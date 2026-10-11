from enum import IntFlag

from ..pypine import Pine
from .address_maps import PLANET_ADDRESSES

"""Controller Logic. Holding L1 + L2 + R1 + R2 + START force-opens the Planet
Menu (see PLANET_MENU_HOTKEY / GlobalButtonState.opens_planet_menu)."""
class PauseSelectButtons(IntFlag):
    SELECT = 0x01
    START  = 0x08
    D_PAD_UP    = 0x10
    D_PAD_DOWN  = 0x40
    D_PAD_LEFT  = 0x80
    D_PAD_RIGHT = 0x20


class ControllerButtons(IntFlag):
    L1       = 0x01
    R1       = 0x02
    L2       = 0x04
    R2       = 0x08
    TRIANGLE = 0x10
    CIRCLE   = 0x20
    CROSS    = 0x40
    SQUARE   = 0x80


PLANET_MENU_HOTKEY: tuple[PauseSelectButtons | ControllerButtons, ...] = (
    ControllerButtons.L1,
    ControllerButtons.L2,
    ControllerButtons.R1,
    ControllerButtons.R2,
    PauseSelectButtons.SELECT,
)


class GlobalButtonState:
    """Snapshot of both controller bytes, read each tick. These bytes start at 0xFF and
    are decremented while held, so a bit reads 0 when pressed — hence the inversion below."""

    def __init__(self, pause_sel: int, buttons: int) -> None:
        self.pause_sel = PauseSelectButtons(~pause_sel & 0xFF)
        self.buttons   = ControllerButtons(~buttons & 0xFF)

    @classmethod
    def read(cls, ipc: Pine, planet_id: int) -> "GlobalButtonState | None":
        """None for a planet id with no known controller address (e.g. the Kalidon
        skyboard sub-level). Callers must treat None as "nothing held"."""
        addrs = PLANET_ADDRESSES.get(planet_id)
        pause_select_addr = addrs.controller_pause_select_v2 if addrs is not None else None
        if pause_select_addr is None:
            return None
        full_addr = 0x20000000 | pause_select_addr
        return cls(
            ipc.read_int8(full_addr),
            ipc.read_int8(full_addr + 1),
        )

    def pressed(self, *flags: PauseSelectButtons | ControllerButtons) -> bool:
        """Return True if every supplied flag is currently held."""
        for f in flags:
            if isinstance(f, PauseSelectButtons):
                if not (self.pause_sel & f):
                    return False
            else:
                if not (self.buttons & f):
                    return False
        return True

    @property
    def opens_planet_menu(self) -> bool:
        """True while the Planet Menu hotkey combo is held."""
        return self.pressed(*PLANET_MENU_HOTKEY)

    def __repr__(self) -> str:
        return f"GlobalButtonState(pause_sel={self.pause_sel!r}, buttons={self.buttons!r})"
