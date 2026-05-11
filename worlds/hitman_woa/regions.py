from BaseClasses import Region, CollectionState

from .items import base_id
from .locations import location_table

class HitmanRegion(Region):
    game: str = "HITMAN World of Assassination"
    ut_mirrored_location: str|None = None

    def can_reach(self, state: CollectionState) -> bool:
        if self.ut_mirrored_location is None or not hasattr(state.multiworld, "hitman_client_checked_locations"):
            return super().can_reach(state)

        return super().can_reach(state) or location_table[self.ut_mirrored_location].id + base_id in state.multiworld.hitman_client_checked_locations