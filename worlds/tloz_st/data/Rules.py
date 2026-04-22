import dataclasses

from .Items import ITEMS
from .Constants import ITEM_GROUPS, tear_lookup, big_tear_lookup
from ..Options import *

from rule_builder.rules import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..__init__ import SpiritTracksWorld

has_sword = Has("Sword (Progressive)") | Has("Sword")
has_shield = Has("Shield")
has_whirlwind = Has("Whirlwind")
has_boomerang = Has("Boomerang")
has_whip = Has("Whip")
has_bow = Has("Bow (Progressive)")
has_bombs = Has("Bombs (Progressive)")
has_sand_wand = Has("Sand Wand")
has_sword_beam = has_sword & Has("Sword Beam Scroll")
has_stamp_book = Has("Stamp Book")

has_cannon = Has("Cannon")

# Songs
has_spirit_flute = Has("Spirit Flute")
has_soa = has_spirit_flute & Has("Song of Awakening")
has_soh = has_spirit_flute & Has("Song of Healing")
has_sob = has_spirit_flute & Has("Song of Birds")
has_sol = has_spirit_flute & Has("Song of Light")
has_sod = has_spirit_flute & Has("Song of Discovery")

# Keys
def has_small_keys(dungeon, count):
    return Has(f"Small Key ({dungeon})", count)

# Rabbits
has_net = Has("Rabbit Net")

def has_rabbit_items(realm, count):
    return Has(f"{realm} Rabbit", count)

def caught_rabbits(realm, count):
    return Has(f"_caught_{realm.lower()}_rabbits", count)

def has_total_rabbits(count):
    return HasFromList("Forest Rabbit", "Snow Rabbit", count=count)

rabbit_count_lookup = {r: ITEMS[r].value for r in ITEM_GROUPS["Rabbits"]}

# Tracks
has_compass = Has("Compass of Light")

def has_glyph(realm):
    return Has(f"{realm} Glyph")

def has_source(realm):
    return Has(f"{realm} Source")

def has_temple_tracks(temple):
    return Has(f"{temple} Temple Tracks")

def has_portal(portal, forward):
    option = SpiritTracksRandomizePortals
    if forward:
        return ([OptionFilter(option, 1), OptionFilter(option, 0)]
                | Has(f"Portal Unlock: {portal}", options=[OptionFilter(option, 2)]))
    return ([OptionFilter(option, 1)]
        | Has(f"Portal Unlock: {portal}", options=[OptionFilter(option, 2)]))

no_tear_items = [OptionFilter(SpiritTracksRandomizeTears, SpiritTracksRandomizeTears.option_no_tears, "ne"),
                OptionFilter(SpiritTracksRandomizeTears, SpiritTracksRandomizeTears.option_vanilla, "ne")]

progressive_shuffle = [OptionFilter(SpiritTracksShuffleToSSections, 1), OptionFilter(SpiritTracksTearGroup, 2)]
not_tower_shuffle = [OptionFilter(SpiritTracksShuffleToSSections, 0), OptionFilter(SpiritTracksTearGroup, 2)]

def has_tears(section: int, _):
    return Filtered(Or(
        Has(f"Tear of Light (ToS {section})", 3, options=[OptionFilter(SpiritTracksTearGroup, 0), OptionFilter(SpiritTracksTearSize, 0)]),
        Has(f"Big Tear of Light (ToS {section})", options=[OptionFilter(SpiritTracksTearGroup, 0), OptionFilter(SpiritTracksTearSize, 1)]),
        HasShuffledSection(f"Tear of Light (Progressive)", section), # options=progressive_shuffle + [OptionFilter(SpiritTracksTearSize, 0)]),
        Has(f"Tear of Light (Progressive)", 16, options=[OptionFilter(SpiritTracksTearGroup, 2), OptionFilter(SpiritTracksTearSize, 0)]),
        Has(f"Tear of Light (Progressive)", section * 3, options=not_tower_shuffle + [OptionFilter(SpiritTracksTearSize, 0)]),
        HasShuffledSection(f"Big Tear of Light (Progressive)", section), #, options=progressive_shuffle + [OptionFilter(SpiritTracksTearSize, 1)]),
        Has(f"Big Tear of Light (Progressive)", section, options=not_tower_shuffle + [OptionFilter(SpiritTracksTearSize, 1)]),
        Has(f"Tear of Light (All Sections)", 3, options=[OptionFilter(SpiritTracksTearGroup, 1), OptionFilter(SpiritTracksTearSize, 0)]),
        Has(f"Big Tear of Light (All Sections)", options=[OptionFilter(SpiritTracksTearGroup, 1), OptionFilter(SpiritTracksTearSize, 1)]),
    ), options=no_tear_items)

has_bow_of_light = Or(
    Has("Bow of Light") & has_bow,
    Filtered(
        Or(Has(f"Tear of Light (Progressive)", 16),
           Has(f"Big Tear of Light (Progressive)", 6),
            Has(f"Tear of Light (All Sections)", 4),
            Has(f"Big Tear of Light (All Sections)", 2)),
        options=no_tear_items))

def can_possess_phantom(floor, lookup):
    return has_bow_of_light | Has("Sword (Progressive)", 2) | (has_sword & has_tears(floor, lookup))

vanilla_tears = Filtered(has_sword, options=[OptionFilter(SpiritTracksRandomizeTears, -1)])

# Isolated options
hard_logic_filter = [OptionFilter(SpiritTracksLogic, SpiritTracksLogic.option_hard), OptionFilter(SpiritTracksLogic, SpiritTracksLogic.option_glitched)]
hard_logic = Has("_UT_Glitched_Logic") | hard_logic_filter

# Composites
has_train = has_cannon & has_glyph("Forest")
has_damage = has_bombs | has_sword | has_bow | has_whip
can_kill_bat = has_damage | has_boomerang
can_kill_bat_pit = can_kill_bat | has_whirlwind
can_kill_bubble = has_bombs | has_bow | has_whip | (has_sword & (has_boomerang | has_whirlwind))
has_range = has_bow | has_boomerang
has_range_objects = has_range | has_whirlwind  # range with
has_short_range = has_range | has_whip | has_sword_beam | has_bombs
can_ring_bell = has_sword | has_boomerang
can_rotate_repeater = has_sword | has_boomerang | has_whip
has_cuccos = has_sob | has_whirlwind
ct_cuccos = has_sob | (has_whirlwind & hard_logic)
can_kill_freezards = (has_shield | has_bow_of_light | hard_logic) & has_damage
can_kill_freezards_torch = (has_boomerang | has_shield | has_bow_of_light | hard_logic) & has_damage

can_enter_tos = (
        [OptionFilter(SpiritTracksToSBase, 0)] |
        Has("Tower of Spirits Base", options=[OptionFilter(SpiritTracksToSBase, 1)]) |
        Has("Progressive ToS Section", options=[OptionFilter(SpiritTracksToSBase, 1)])
        )

def can_enter_tos_section(section):
    sources = [None, "Forest", "Snow", "Ocean", "Fire"]
    if section == 1:
        return can_enter_tos
    return Or([OptionFilter(SpiritTracksToSSectionUnlocks, 0)] |
              Filtered(has_source(sources[section-1]), options=[OptionFilter(SpiritTracksToSSectionUnlocks, 1)]),
              Has("Progressive ToS Section", section, options=[OptionFilter(SpiritTracksToSSectionUnlocks, 2), OptionFilter(SpiritTracksToSBase, 1)]),
              Has("Progressive ToS Section", section-1, options=[OptionFilter(SpiritTracksToSSectionUnlocks, 2), OptionFilter(SpiritTracksToSBase, 0)]))

# Rupees
def has_rupees(count):
    wild_rupees = Has("_rupee_farming_spot", options=[OptionFilter(SpiritTracksExcessTreasures, 2), OptionFilter(SpiritTracksRupeeFarming, 1)])
    treasure_farming = HasAll("_rupee_farming_spot", "_can_sell_treasure", options=[OptionFilter(SpiritTracksExcessTreasures, 1), OptionFilter(SpiritTracksRupeeFarming, 1)])

    return Or(Has("_UT_Glitched_Logic"),
              wild_rupees,
              treasure_farming,
              Has("Rupees", count),
              Has("Treasure", count + 2500) & Has("_can_sell_treasure"))

def has_dungeon_rewards(count: int):
    option = SpiritTracksDarkRealmUnlock
    return ([
                OptionFilter(option, option.option_dungeons, operator="ne")]
            | Has("_dungeon_reward", count, options=[OptionFilter(option, option.option_dungeons)]))


def st_has_dungeon_rewards(state, player):
    if state.multiworld.worlds[player].options.dark_realm_access != "dungeons":
        return True
    dungeon_count = state.multiworld.worlds[player].options.dungeons_required.value
    return state.has("_dungeon_reward", player, dungeon_count)

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
