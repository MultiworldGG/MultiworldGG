import dataclasses

from .Items import ITEMS
from .Constants import ITEM_GROUPS, tear_lookup, big_tear_lookup, rabbit_realms
from ..Options import *

from rule_builder.rules import *
from rule_builder.field_resolvers import FromWorldAttr, FromOption
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..__init__ import SpiritTracksWorld

has_sword = Has("Sword (Progressive)") | Has("Sword")
has_shield = Has("Shield") | Has("Ancient Shield")
has_whirlwind = Has("Whirlwind")
has_boomerang = Has("Boomerang")
has_whip = Has("Whip")
has_bow = Has("Bow (Progressive)") | Has("Bow")
has_bombs = Has("Bombs (Progressive)") | Has("Bomb Bag")
has_sand_wand = Has("Sand Wand")
has_sword_beam = has_sword & Has("Sword Beam Scroll")
has_stamp_book = Has("Stamp Book")

has_cannon = Has("Cannon")
has_wagon = Has("Wagon")

# Songs
has_spirit_flute = Has("Spirit Flute")
has_soa = has_spirit_flute & Has("Song of Awakening")
has_soh = has_spirit_flute & Has("Song of Healing")
has_sob = has_spirit_flute & Has("Song of Birds")
has_sol = has_spirit_flute & Has("Song of Light")
has_sod = has_spirit_flute & Has("Song of Discovery")

normal_key_options = [OptionFilter(SpiritTracksShuffleDungeonRooms, 0), OptionFilter(SpiritTracksShuffleBosses, 1, "le"), OptionFilter(SpiritTracksShuffleWarps, 0)]
event_key_options = [OptionFilter(SpiritTracksShuffleDungeonRooms, 0, "gt"), OptionFilter(SpiritTracksShuffleBosses, 1, "gt"), OptionFilter(SpiritTracksShuffleWarps, 0, "gt")]

@dataclasses.dataclass
class DungeonIsRemoved(Rule["SpiritTracksWorld"], game="Spirit Tracks"):
    dungeon: str

    @override
    def _instantiate(self, world: "SpiritTracksWorld") -> Rule.Resolved:
        removed = self.dungeon in world.non_required_dungeons
        if removed:
            return True_().resolve(world)
        return False_().resolve(world)

def dungeon_is_removed(dung):
    return DungeonIsRemoved(dung) & [OptionFilter(SpiritTracksExcludeDungeons, 2)]

def option_or(rule: Rule, options: Iterable):
    """Check if any of the options are resolved"""
    res = [Filtered(rule, options=[o]) for o in options]
    return Or(*res)

# Keys
def has_small_keys_er(dungeon, count, _ool=None, er=None):
    _ool = _ool if _ool is not None else count
    er = count if er is None else er
    return Or(Has(f"Keyring ({dungeon})"),  # keyring always works
        Has(f"Small Key ({dungeon})", count, options=normal_key_options),
        ool & Has(f"Small Key ({dungeon})", _ool, options=normal_key_options),
        Has(f"Small Key ({dungeon})", er),
        option_or(Has(f"Small Key ({dungeon})", 1) & ool, event_key_options),
        dungeon_is_removed(dungeon)
              )


def has_small_keys(dungeon, count, _ool=None):
    _ool = _ool if _ool is not None else count
    return Or(Has(f"Keyring ({dungeon})"),  # keyring always works
        Has(f"Small Key ({dungeon})", count),
        ool & Has(f"Small Key ({dungeon})", _ool),
        dungeon_is_removed(dungeon)
              )

def has_single_small_key(dungeon):
    return Has(f"Keyring ({dungeon})") | Has(f"Small Key ({dungeon})") | dungeon_is_removed(dungeon)

def has_boss_key(dungeon):
    return Or(
            Has(f"Boss Key ({dungeon})"),
            Has(f"Keyring ({dungeon})", options=[OptionFilter(SpiritTracksBigKeyrings, 1)]),
            dungeon_is_removed(dungeon)
    )

# Rabbits
has_net = Has("Rabbit Net") & has_cannon

def has_rabbit_items(realm, count):
    return Has(f"{realm} Rabbit", count)

def caught_rabbits(realm, count):
    return Has(f"_caught_{realm.lower()}_rabbits", count)

def has_total_rabbits(count):
    return HasFromList("Grass Rabbit", "Snow Rabbit", "Ocean Rabbit", "Mountain Rabbit", "Sand Rabbit", count=count)

rabbit_count_lookup = {r: ITEMS[r].value for r in ITEM_GROUPS["Rabbits"]}

has_all_rabbits = And(
    Has("Grass Rabbit", 10),
    Has("Snow Rabbit", 10),
    Has("Ocean Rabbit", 10),
    Has("Mountain Rabbit", 10),
    Has("Sand Rabbit", 10)
)
has_all_rabbit_types = HasFromListUnique("Grass Rabbit", "Snow Rabbit", "Ocean Rabbit", "Mountain Rabbit", "Sand Rabbit", count=5)

# Tracks
has_compass = Has("Compass of Light") | Has("Compass of Light Shard", count=FromOption(SpiritTracksCompassShardCount))

def has_glyph(realm):
    return HasGroup(f"Tracks: {realm} Glyph") & has_train

def has_source(realm):
    return HasGroup(f"Tracks: {realm} Source") & has_train

def has_temple_tracks(temple):
    return HasGroup(f"Tracks: {temple} Temple Tracks") & has_train

def has_tracks(tracks):
    return HasGroup(f"Tracks: {tracks}") & has_train

def has_portal(portal, forward, event, _exit=False):
    not_fw = False_() if forward else True_()
    no_event = True_() if _exit else False_()
    return Or(
        (not_fw | has_cannon | [OptionFilter(SpiritTracksPortalLocations, 0)]) & [OptionFilter(SpiritTracksRandomizePortals, 1)],
        has_cannon & (Has(event) | no_event) & [OptionFilter(SpiritTracksRandomizePortals, 0)],
        Has(f"Portal Unlock: {portal}") & (not_fw | has_cannon | [OptionFilter(SpiritTracksPortalLocations, 0)]) & [OptionFilter(SpiritTracksRandomizePortals, 2)],
    )

no_tear_items = [OptionFilter(SpiritTracksRandomizeTears, SpiritTracksRandomizeTears.option_no_tears, "ne"),
                OptionFilter(SpiritTracksRandomizeTears, SpiritTracksRandomizeTears.option_vanilla, "ne")]

progressive_shuffle = [OptionFilter(SpiritTracksShuffleToSSections, 1), OptionFilter(SpiritTracksTearGroup, 2)]
not_tower_shuffle = [OptionFilter(SpiritTracksShuffleToSSections, 0), OptionFilter(SpiritTracksTearGroup, 2)]



def has_tears(section: int):
    return Filtered(
        Or(
            Has(f"Tear of Light (ToS {section})", 3, options=[OptionFilter(SpiritTracksTearGroup, 0), OptionFilter(SpiritTracksTearSize, 0)]),
            Has(f"Big Tear of Light (ToS {section})", options=[OptionFilter(SpiritTracksTearGroup, 0), OptionFilter(SpiritTracksTearSize, 1)]),
            HasShuffledSection(f"Tear of Light (Progressive)", section), # options=progressive_shuffle + [OptionFilter(SpiritTracksTearSize, 0)]),
            Has(f"Tear of Light (Progressive)", count=FromWorldAttr("tears_included_small"), options=[OptionFilter(SpiritTracksTearGroup, 2), OptionFilter(SpiritTracksTearSize, 0)]),
            Has(f"Tear of Light (Progressive)", section * 3, options=not_tower_shuffle + [OptionFilter(SpiritTracksTearSize, 0)]),
            HasShuffledSection(f"Big Tear of Light (Progressive)", section), #, options=progressive_shuffle + [OptionFilter(SpiritTracksTearSize, 1)]),
            Has(f"Big Tear of Light (Progressive)", section, options=not_tower_shuffle + [OptionFilter(SpiritTracksTearSize, 1)]),
            Has(f"Tear of Light (All Sections)", 3, options=[OptionFilter(SpiritTracksTearGroup, 1), OptionFilter(SpiritTracksTearSize, 0)]),
            Has(f"Big Tear of Light (All Sections)", options=[OptionFilter(SpiritTracksTearGroup, 1), OptionFilter(SpiritTracksTearSize, 1)]),
    ), options=no_tear_items)

has_bow_of_light = Or(
    Has("Bow of Light") & has_bow,
    Filtered(
        Or(Has(f"Tear of Light (Progressive)", count=FromWorldAttr("tears_included_small")),
           Has(f"Big Tear of Light (Progressive)", count=FromWorldAttr("tears_included_big")),
            Has(f"Tear of Light (All Sections)", 4),
            Has(f"Big Tear of Light (All Sections)", 2)),
        options=no_tear_items))

def can_possess_phantom(floor):
    return has_bow_of_light | Has("Sword (Progressive)", 2) | (has_sword & (Has("Lokomo Sword") | has_tears(floor)))

# Passengers, cargo
def has_passenger(passenger, event):
    return Has(f"Passenger: {passenger}") | Has(event)

pickup_tracks = [OptionFilter(SpiritTracksPassengerPickupRequirement, 0)]
pickup_visit = [OptionFilter(SpiritTracksPassengerPickupRequirement, 1)]

def pickup_passenger(tracks: str, event: str):
    return Filtered(has_tracks(tracks), options=pickup_tracks) | Has(event, options=pickup_visit)

def has_cargo(cargo, event):
    return has_wagon & (
            Has(f"Cargo: {cargo}") | Has(event)
    )

vanilla_tears = Filtered(has_sword, options=[OptionFilter(SpiritTracksRandomizeTears, -1)])
not_vanilla_tears = [OptionFilter(SpiritTracksRandomizeTears, -1, operator="ne")]
vanilla_boss_keys = [OptionFilter(SpiritTracksRandomizeBossKeys, 0)]
randomize_boss_keys = [OptionFilter(SpiritTracksRandomizeBossKeys, 0, "gt")]
no_passengers = [OptionFilter(SpiritTracksRandomizePassengers, 0)]
randomize_passengers = [OptionFilter(SpiritTracksRandomizePassengers, 2, operator="ge")]
no_cargo = [OptionFilter(SpiritTracksRandomizeCargo, 0)]
not_vanilla_passengers = [OptionFilter(SpiritTracksRandomizePassengers, 1, operator="ne")]
vanilla_passengers = [OptionFilter(SpiritTracksRandomizePassengers, 1)]

# Isolated options
hard_logic_filter = [OptionFilter(SpiritTracksLogic, 1, operator="ge")]
ool = Has("_UT_Glitched_Logic")
hard_logic = ool | hard_logic_filter
glitched_logic = ool | [OptionFilter(SpiritTracksLogic, SpiritTracksLogic.option_glitched)]


# Composites
has_train = has_cannon | [OptionFilter(SpiritTracksCannonLogic, 1, "gt")] | (ool & [OptionFilter(SpiritTracksCannonLogic, 0, "gt")])
has_good_damage = has_bombs | has_sword | has_bow
has_damage = has_good_damage | has_whip
can_kill_moth = has_whirlwind | has_bow | has_bombs | has_whip | (has_boomerang | has_sword) | has_sword_beam
can_kill_bat = has_damage | has_boomerang
can_kill_bat_pit = has_boomerang | has_whirlwind | has_whip | has_bow | has_sword_beam
can_kill_bubble = has_bombs | has_bow | has_whip | (has_sword & (has_boomerang | has_whirlwind))
can_kill_ice_bat = has_bombs | has_bow | has_whip | has_boomerang | (has_sword & has_whirlwind)

has_range = has_bow | has_boomerang
has_range_objects = has_range | has_whirlwind  # range with
has_short_range = has_range | has_whip | has_sword_beam | has_bombs
can_ring_bell = has_sword | has_boomerang
can_break_grass = can_ring_bell
can_rotate_repeater = has_sword | has_boomerang | has_whip
has_cuccos = has_sob | has_whirlwind
ct_cuccos = has_sob | (has_whirlwind & hard_logic)
can_kill_freezards = (has_shield | has_bow_of_light | hard_logic) & has_damage
can_kill_freezards_torch = (has_boomerang | has_shield | has_bow_of_light | hard_logic) & has_damage
hard_birds = has_whip & (has_sob | hard_logic)
can_fight_malladus = has_sword & has_bow_of_light

soft_cannon = has_cannon | ool | [OptionFilter(SpiritTracksCannonLogic, 3)]
open_warps = [OptionFilter(SpiritTracksOpenBlueWarps, 1)]

can_enter_tos = (
        [OptionFilter(SpiritTracksToSBase, 0)] |
        Has("Tower of Spirits Base", options=[OptionFilter(SpiritTracksToSBase, 1)]) |
        Has("Progressive ToS Section", options=[OptionFilter(SpiritTracksToSBase, 1)])
        )

def can_enter_tos_section(section):
    sources = [None, "Forest", "Snow", "Ocean", "Fire"]
    if section == 1:
        return can_enter_tos
    return can_enter_tos & Or(True_() & [OptionFilter(SpiritTracksToSSectionUnlocks, 0)],
              Filtered(has_source(sources[section-1]), options=[OptionFilter(SpiritTracksToSSectionUnlocks, 1)]),
              Has("Progressive ToS Section", section, options=[OptionFilter(SpiritTracksToSSectionUnlocks, 2), OptionFilter(SpiritTracksToSBase, 1)]),
              Has("Progressive ToS Section", section-1, options=[OptionFilter(SpiritTracksToSSectionUnlocks, 2), OptionFilter(SpiritTracksToSBase, 0)]))

tos_15f_glitched = Or(
    And(
        has_range | has_sword_beam,
        has_small_keys("ToS 4", 3, 2)
    ),
    And(
        glitched_logic & has_small_keys("ToS 4", 3, 1),
        Or(
            has_range, has_sword_beam,
            has_bombs & has_whirlwind
        )
    )
)
can_kill_vulcano = has_bow & Or(
            has_sword,
            has_whip,
            Has("Bombs (Progressive)", 2),
            Has("Bomb Bag") & Has("Bomb Bag Upgrade"))

mtt_center = Or(
    And(  # 2 Keys, normal
        has_small_keys("Mountain Temple", 2),
        Or(
            has_boomerang, has_bombs,
            And(  # Harder options
                hard_logic,
                has_bow | has_sword_beam | has_whip
            )
        )
    ),
    And(  # Skip Keys
        glitched_logic,
        Or(
            has_bombs,  # oob
            And(
                has_small_keys("Mountain Temple", 2, 1),  # 1 key boomerang clip
                has_boomerang
            )
        )
    )
)

# Rupees
def has_rupees(count):
    wild_rupees = Has("_rupee_farming_spot", options=[OptionFilter(SpiritTracksExcessTreasures, 2), OptionFilter(SpiritTracksRupeeFarming, 1)])
    treasure_farming = HasAll("_rupee_farming_spot", "_can_sell_treasure", options=[OptionFilter(SpiritTracksExcessTreasures, 1), OptionFilter(SpiritTracksRupeeFarming, 1)])

    return Or(ool,
              wild_rupees,
              treasure_farming,
              Has("Rupees", int(count*0.7)),
              Has("Treasure Rupees", int(count*0.7) + 2500) & Has("_can_sell_treasure"))


has_dungeon_rewards = ([
            OptionFilter(SpiritTracksDarkRealmUnlock, SpiritTracksDarkRealmUnlock.option_dungeons, operator="ne")]
            | Has("_dungeon_reward", count=FromOption(SpiritTracksDungeonCount), options=[OptionFilter(SpiritTracksDarkRealmUnlock, [1, 3], "in")]))

@dataclasses.dataclass
class HasShuffledSection(Rule["SpiritTracksWorld"], game="Spirit Tracks"):
    item_name: str
    section: int

    @override
    def _instantiate(self, world: "SpiritTracksWorld") -> Rule.Resolved:

        # print(f"Tower section lookup {world.tower_section_lookup} for section {self.section} and item {self.item_name} {self.options}")
        tower_section_lookup = {int(i): v for i, v in world.tower_section_lookup.items()}
        shuffled_section = tower_section_lookup[self.section]
        if self.item_name.startswith("Big"):
            return Has(self.item_name, shuffled_section).resolve(world)
        return Has(self.item_name, shuffled_section*3).resolve(world)

    def __str__(self):
        return "Has Progressive tears for shuffle level"


class DebugRule(Rule["SpiritTracksWorld"], game="Spirit Tracks"):
    @override
    def _instantiate(self, world: "SpiritTracksWorld") -> Rule.Resolved:
        return self.Resolved(player=world.player)

    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # print([(r, state.count(f"{r} Rabbit", self.player)) for r in rabbit_realms])
            return all([state.has(f"{r} Rabbit", self.player, 10) for r in rabbit_realms])


