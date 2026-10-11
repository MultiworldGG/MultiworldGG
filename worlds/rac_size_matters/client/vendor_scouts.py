"""Scouted AP rewards keyed by the native purchase, never by its display icon."""
from dataclasses import dataclass

from ..core.vendor import WEAPON_VENDOR_IDS
from ..locations import GADGET_INTERNAL_TO_LOCATION, WEAPON_INTERNAL_TO_LOCATION, TITAN_INTERNAL_TO_LOCATION, MOD_INTERNAL_TO_LOCATION


@dataclass(frozen=True)
class VendorReward:
    location_id: int
    item_id: int
    recipient_slot: int
    item_name: str
    recipient_name: str
    flags: int

    @property
    def progression(self):
        return bool(self.flags & 1)

    @property
    def description(self):
        return f"{self.item_name}\nFor {self.recipient_name}"

    @property
    def title_color(self):
        return 2 if self.progression else 1


class VendorScouts:
    def __init__(self, location_ids):
        self.location_ids = dict(location_ids)
        self.locations = {}
        for kind, mapping in ((0, WEAPON_INTERNAL_TO_LOCATION | GADGET_INTERNAL_TO_LOCATION),
                              (2, TITAN_INTERNAL_TO_LOCATION)):
            self.locations.update({(kind, WEAPON_VENDOR_IDS[key]): location_ids[name]
                                   for key, name in mapping.items() if name in location_ids})
        self.allowed = set(self.locations.values()) | {
            location_ids[name] for name in MOD_INTERNAL_TO_LOCATION.values() if name in location_ids}
        self.rewards = {}

    def request(self, server_locations):
        return {"cmd": "LocationScouts", "locations": sorted(self.allowed & set(server_locations)),
                "create_as_hint": 0}

    def update(self, items, item_name, player_name):
        for item in items:
            if item.location in self.allowed:
                self.rewards[item.location] = VendorReward(
                    item.location, item.item, item.player,
                    item_name(item.item, item.player), player_name(item.player), item.flags)

    def for_purchase(self, kind, native_id):
        return self.rewards.get(self.locations.get((kind, native_id)))

    def for_location(self, name):
        return self.rewards.get(self.location_ids.get(name))
