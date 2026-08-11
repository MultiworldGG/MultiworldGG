from typing import NamedTuple

class SpawnItems(NamedTuple):
    moki_hf: int  # How many health fragments are required to meet the region requirements
    gorlek_hf: int
    kii_hf: int
    require_regen: bool  # Regenerate is only required in moki and gorlek (and if regenerate_requirements is enabled)
    early_ks: int  # How many keystones to put in the early items
    items_amount: int  # How many items to spawn with


spawn_data: dict[str, SpawnItems] = {
    "MarshSpawn": SpawnItems(0, 0, 0, False, 2, 5),
    "HowlsDen": SpawnItems(0, 0, 0, False, 2, 5),
    "MarshPastOpher": SpawnItems(0, 0, 0, False, 0, 4),
    "MidnightBurrows": SpawnItems(0, 0, 0, False, 0, 4),
    "WestHollow": SpawnItems(0, 0, 0, False, 0, 4),
    "EastHollow": SpawnItems(0, 0, 0, False, 0, 4),
    "GladesTown": SpawnItems(0, 0, 0, False, 0, 4),
    "WestGlades": SpawnItems(1, 0, 0, False, 0, 4),
    "OuterWellspring": SpawnItems(1, 0, 0, False, 0, 5),
    "InnerWellspring": SpawnItems(1, 0, 0, False, 0, 5),
    "WoodsEntry": SpawnItems(2, 0, 0, True, 2, 6),
    "WoodsMain": SpawnItems(2, 0, 0, True, 4, 7),
    "LowerReach": SpawnItems(3, 0, 0, True, 0, 5),
    "UpperReach": SpawnItems(3, 0, 0, True, 0, 5),
    "UpperDepths": SpawnItems(3, 1, 1, True, 2, 5),
    "LowerDepths": SpawnItems(3, 1, 1, True, 0, 5),
    "PoolsApproach": SpawnItems(1, 0, 0, True, 0, 5),
    "EastPools": SpawnItems(1, 0, 0, True, 0, 5),
    "UpperPools": SpawnItems(1, 0, 0, True, 0, 5),
    "WestPools": SpawnItems(1, 0, 0, True, 0, 5),
    "LowerWastes": SpawnItems(5, 1, 1, True, 4, 7),
    "UpperWastes": SpawnItems(5, 1, 1, True, 2, 5),
    "WindtornRuins": SpawnItems(5, 1, 1, True, 2, 7),  # Copied from Wastes, since you usually end up there after escape
    "WeepingRidge": SpawnItems(7, 3, 3, True, 0, 6),
    "WillowsEnd": SpawnItems(7, 3, 3, True, 0, 7),
}
