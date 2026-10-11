from __future__ import annotations

from .address_maps import save_address

from typing import TYPE_CHECKING

from ..constants import Rac5Planets
from ..locations import ALL_LOCATIONS
from ..locations.observation import LocationObservation
from .locations.challenge_locations import (
    ALL_CLANK_ADDRESS_MAP,
    CHALLENGE_ADDRESS_MAP,
    CLANK_SECTION_UNLOCK_ADDRESSES,
    COUNT_BASED_CHALLENGE_ADDRS,
    DAYNI_MOON_CHALLENGE_NAMES,
    GLADIATOR_FAILSAFE,
    METALIS_CHALLENGE_NAMES,
    SKYBOARD_ADDRESS_MASK_MAP,
    ChallengeSection,
)

if TYPE_CHECKING:
    from ..pypine import Pine

_CLANK_ADDRESSES: tuple[int, ...] = tuple(ALL_CLANK_ADDRESS_MAP)


class ChallengeInventory:
    """Pine-backed live accessor for every clank-challenge completion byte."""

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self._name_to_address: dict[str, int] = {n: addr for addr, n in ALL_CLANK_ADDRESS_MAP.items()}
        self._counts: dict[str, int] = dict.fromkeys(ALL_CLANK_ADDRESS_MAP.values(), 0)
        self.completed: set[str] = set()
        self.gladiator_sent: set[str] = set()

    def _read_all(self) -> dict[int, int]:
        values = self.pine.batch_read_int8([save_address(a) for a in list(_CLANK_ADDRESSES)])
        return dict(zip(_CLANK_ADDRESSES, values, strict=True))

    def get(self, name: str) -> int:
        return self.pine.read_int8(save_address(self._name_to_address[name]))

    def set(self, name: str, value: int) -> None:
        self.pine.write_int8(save_address(self._name_to_address[name]), value)

    def delete(self, name: str) -> None:
        self.set(name, 0)

    def unlock_section(self, planet: str, section: ChallengeSection, value: int = 0x0F) -> None:
        """Unlock a single challenge section (Derby / Gadgetbot Toss / Gadgetbot) on a planet."""
        self.pine.write_int8(save_address(CLANK_SECTION_UNLOCK_ADDRESSES[planet][section]), value)

    def setup(self, all_challenges: bool = False) -> None:
        """Unlock every section on every tracked planet. Never writes individual
        challenge-completion bytes — those are the game's own save data."""
        del all_challenges
        for planet, sections in CLANK_SECTION_UNLOCK_ADDRESSES.items():
            for section in sections:
                self.unlock_section(planet, section)

    def check(self, all_challenges: bool = False, raw_by_address=None) -> list[str]:
        """Read every tracked byte and return newly completed AP location
        names for this call, including any gladiator failsafe locations."""

        if raw_by_address is None:
            raw_by_address = self._read_all()
        newly: list[str] = []
        addr_map = ALL_CLANK_ADDRESS_MAP if all_challenges else CHALLENGE_ADDRESS_MAP
        for address, name in addr_map.items():
            if name in self.completed:
                continue
            count = raw_by_address[address]
            observation = LocationObservation(challenges=raw_by_address, previous={address: self._counts.get(name, 0)})
            done = ALL_LOCATIONS[name].completed(observation)
            if address in COUNT_BASED_CHALLENGE_ADDRS:
                self._counts[name] = count
            if done:
                self.completed.add(name)
                newly.append(name)
        newly.extend(self._check_gladiator_failsafe())
        return newly

    def _check_gladiator_failsafe(self) -> list[str]:
        """Report a planet's Ultimate Gladiator skill point once every individual
        challenge on it is complete, even if its own in-game detection never fired."""
        newly: list[str] = []
        if Rac5Planets.METALIS not in self.gladiator_sent and METALIS_CHALLENGE_NAMES <= self.completed:
            self.gladiator_sent.add(Rac5Planets.METALIS)
            newly.append(GLADIATOR_FAILSAFE[Rac5Planets.METALIS])
        if Rac5Planets.DAYNI_MOON not in self.gladiator_sent and DAYNI_MOON_CHALLENGE_NAMES <= self.completed:
            self.gladiator_sent.add(Rac5Planets.DAYNI_MOON)
            newly.append(GLADIATOR_FAILSAFE[Rac5Planets.DAYNI_MOON])
        return newly

    def sync(self) -> None:
        """Baseline read: populate completed/_counts without reporting anything as newly completed."""
        raw_by_address = self._read_all()
        for address, name in ALL_CLANK_ADDRESS_MAP.items():
            count = raw_by_address[address]
            if address in COUNT_BASED_CHALLENGE_ADDRS:
                self._counts[name] = count
                if count > 0:
                    self.completed.add(name)
            elif count >= 2:
                self.completed.add(name)

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        self.completed.update(name for name in checked_locations if name in ALL_CLANK_ADDRESS_MAP.values())

    def __repr__(self) -> str:
        return f"ChallengeInventory(completed={len(self.completed)}/{len(ALL_CLANK_ADDRESS_MAP)})"


_SKYBOARD_ADDRESSES: tuple[int, ...] = tuple({address for address, _mask in SKYBOARD_ADDRESS_MASK_MAP})


class SkyboardInventory:
    """Pine-backed live accessor + completion tracking for every skyboard
    race's two-bit win counter, keyed by (address, mask)."""

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self._name_to_addr_mask: dict[str, tuple[int, int]] = {n: k for k, n in SKYBOARD_ADDRESS_MASK_MAP.items()}
        self.completed: set[str] = set()

    def _read_all(self) -> dict[int, int]:
        values = self.pine.batch_read_int8([save_address(a) for a in list(_SKYBOARD_ADDRESSES)])
        return dict(zip(_SKYBOARD_ADDRESSES, values, strict=True))

    def get(self, name: str) -> bool:
        address, mask = self._name_to_addr_mask[name]
        return bool(self.pine.read_int8(save_address(address)) & mask)

    def set(self, name: str, value: bool) -> None:
        address, mask = self._name_to_addr_mask[name]
        raw = self.pine.read_int8(save_address(address))
        # Set an uncompleted race to one win; preserve existing win counts.
        # The mask covers a two-bit counter, not two independent flags.
        if value:
            if not raw & mask:
                raw |= mask & -mask
        else:
            raw &= ~mask
        self.pine.write_int8(save_address(address), raw)

    def delete(self, name: str) -> None:
        self.set(name, False)

    def check(self, raw_by_address=None) -> list[str]:
        """Read every tracked bit and return newly completed AP location names for this call."""

        if raw_by_address is None:
            raw_by_address = self._read_all()
        newly: list[str] = []
        for (address, mask), name in SKYBOARD_ADDRESS_MASK_MAP.items():
            if name in self.completed:
                continue
            if ALL_LOCATIONS[name].completed(LocationObservation(skyboard=raw_by_address)):
                self.completed.add(name)
                newly.append(name)
        return newly

    def sync(self) -> None:
        """Baseline read: populate completed without reporting anything as newly completed."""
        raw_by_address = self._read_all()
        for (address, mask), name in SKYBOARD_ADDRESS_MASK_MAP.items():
            if raw_by_address[address] & mask:
                self.completed.add(name)

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        self.completed.update(name for name in checked_locations if name in SKYBOARD_ADDRESS_MASK_MAP.values())

    def __repr__(self) -> str:
        return f"SkyboardInventory(completed={len(self.completed)}/{len(SKYBOARD_ADDRESS_MASK_MAP)})"
