from rule_builder.field_resolvers import FromWorldAttr, FromOption
from ..Options import *
from .Constants import *
from typing import Literal
from .LogicPredicates import floor_lookup
from .RuleClasses import *

# Options
is_ut = Has("_is_ut")
is_not_ut = Has("_is_not_ut")
ut_glitched = Has("_UT_Glitched_Logic")
hard_logic = [OptionFilter(PhantomHourglassLogic, 0, "gt")] | ut_glitched
glitched_logic = [OptionFilter(PhantomHourglassLogic, 1, "gt")] | ut_glitched
normal_logic = [OptionFilter(PhantomHourglassLogic, 0)]
not_glitched_logic = [OptionFilter(PhantomHourglassLogic, 1, "le")]

keysanity = [OptionFilter(PhantomHourglassKeyRandomization, 2)]
smart_keys = is_ut & [OptionFilter(PhantomHourglassUTSmartKeys, 1)]
vanilla_keys = [OptionFilter(PhantomHourglassKeyRandomization, 0)]
keys_own_dungeon = [OptionFilter(PhantomHourglassKeyRandomization, 1, "le")]
pedestals_vanilla = [OptionFilter(PhantomHourglassRandomizePedestalItems, 0)]
pedestals_abstract_vanilla = [OptionFilter(PhantomHourglassRandomizePedestalItems, 1)]
pedestals_vanilla_any = [OptionFilter(PhantomHourglassRandomizePedestalItems, 1, "le")]
pedestals_own_dungeon = [OptionFilter(PhantomHourglassRandomizePedestalItems, 2)]
pedestals_anywhere = [OptionFilter(PhantomHourglassRandomizePedestalItems, 3)]
pedestals_not_vanilla = [OptionFilter(PhantomHourglassRandomizePedestalItems, 0, "gt")]

vanilla_caves = [OptionFilter(PhantomHourglassShuffleCaves, 0)]
vanilla_dungeons = [OptionFilter(PhantomHourglassShuffleDungeonEntrances, 0)]
vanilla_bosses = [OptionFilter(PhantomHourglassShuffleBosses, 0)]

randomize_minigames = [OptionFilter(PhantomHourglassRandomizeMinigames, 0, "gt")]

# Basic Items
has_sword = Has("Sword (Progressive)") | Has("Oshus' Sword")
has_phantom_sword = Has("Sword (Progressive)", 2) | (has_sword & Has("Phantom Sword"))
has_shield = Has("Shield")
has_shovel = Has("Shovel")
has_bow = Has("Bow (Progressive)") | Has("Bow")
has_bombs = Has("Bombs (Progressive)") | Has("Bomb Bag")
has_chus = Has("Bombchus (Progressive)") | Has("Bombchu Bag")
has_grapple = Has("Grappling Hook")
has_hammer = Has("Hammer")
has_boomerang = Has("Boomerang")

def has_spirit(spirit: Literal["Power", "Wisdom", "Courage"], count=1):
    spirit_index = SPIRITS.index(spirit) + 1
    if count > 1:
        return Or(
            Has(f"Spirit of {spirit} (Progressive)", count),
            And(
                Or(
                    Has(f"Spirit of {spirit}"),
                    Has(f"Spirit (Progressive", spirit_index)
                ),
                Or(
                    Has(f"{spirit} Upgrade", count-1),
                    Has(f"Spirit Upgrade", count-1)
                )
            )
        )
    return Or(
        Has(f"Spirit of {spirit} (Progressive)"),
        Has(f"Spirit of {spirit}"),
        Has(f"Spirit (Progressive)")
    )

def has_spirit_gems(spirit: Literal["Power", "Wisdom", "Courage"], count):
    spirit_index = SPIRITS.index(spirit)
    return Has(f"{spirit} Gem", count) & Or(*[has_spirit(s) for s in SPIRITS[spirit_index:]])

has_ph = Has("Phantom Hourglass")
has_phantom_blade = Has("Phantom Blade")
has_triforce_crest = Has("Triforce Crest") | [OptionFilter(PhantomHourglassTriforceCrestRandomization, 0)]
has_courage_crest = Has("Courage Crest")

def has_sea_chart(quadrant: Literal["NW", "NE", "SW", "SE"]):
    return Has(f"{quadrant} Sea Chart")

has_cannon = Has("Cannon")
has_salvage = Has("Salvage Arm")
has_fishing_rod = Has("Fishing Rod") | Has("Fishing Rod (Progressive)")
has_lure = Has("Big Catch Lure") | Has("Fishing Rod (Progressive)", 2)
has_swordfish_shadows = Has("Swordfish Shadows") | Has("Fishing Rod (Progressive)", 3)
can_catch_rsf = has_lure | has_swordfish_shadows
can_catch_stowfish = has_swordfish_shadows & (has_lure | ut_glitched)

def require_sea_chart(quadrant: Literal["NW", "NE", "SW", "SE"]):
    return has_sea_chart(quadrant) | [OptionFilter(PhantomHourglassBoatRequiresSeaChart, 0)]

def has_fish(fish):
    return Has(f"Fish: {fish}")


has_rsf = has_fish("Rusty Swordfish")
has_neptoona = has_fish("Legendary Neptoona")
has_stowfish = has_fish("Stowfish") & HasGroup("Normal Fish")
has_cyclone_slate = Has("Cyclone Slate")

def has_frog(glyph, quadrant):
    return has_sea_chart(quadrant) & has_cyclone_slate & (Has(f"Golden Frog Glyph {glyph}") | [OptionFilter(PhantomHourglassFrogRandomization, PhantomHourglassFrogRandomization.option_start_with)])

has_frog_x = has_frog("X", "SW")
has_frog_n = has_frog("N", "NW")
has_frog_se = has_frog("Omega", "SE") | has_frog("W", "SE")
has_frog_square = has_frog("Square", "NE")
has_frog_phi = has_frog("Phi", "SW")

def has_map(number):
    return Has(TREASURE_MAPS[number-1])

# Combined item states
has_explosives = has_bombs | has_chus
has_swordless_cave_damage = Or(has_bombs, has_bow, has_grapple, has_hammer)
has_swordless_damage = has_swordless_cave_damage | has_chus
has_cave_damage = Or(has_sword, has_swordless_cave_damage)
has_damage = has_cave_damage | has_chus
has_fire_sword = has_sword & has_spirit("Power", 2)
has_super_shield = has_spirit("Wisdom", 2) & has_shield
has_beam_sword = has_sword & has_spirit("Courage", 2)
has_stun_sword = has_sword & (has_boomerang | has_super_shield)
can_cut_bamboo = has_sword | has_explosives



clever_pots = hard_logic
clever_bombs = has_bombs | hard_logic

can_kill_bat = has_damage | has_boomerang
can_kill_dark_yook = Or(has_sword, has_bow, has_hammer, has_grapple)
can_kill_yook = can_kill_dark_yook | hard_logic
can_kill_blue_chu = has_swordless_cave_damage | has_beam_sword | has_stun_sword
can_kill_phantom_eyes = has_swordless_damage | clever_pots
can_kill_eye_brute = hard_logic | has_hammer | has_chus | (has_bow & has_sword)
can_kill_bubble = has_swordless_damage | has_stun_sword | has_fire_sword
can_steal_from_phantom = can_kill_bat | clever_pots

has_range = Or(has_boomerang, has_bow, has_grapple)
has_beam_range = has_range | has_beam_sword
has_mid_range = has_range | has_beam_sword | has_hammer
has_short_range = has_mid_range | clever_bombs
has_pot_range = has_short_range | clever_pots
cucco_dig = has_shovel & has_grapple
lazy_cuccos = has_grapple  # add option here later

can_hit_switches = can_kill_bat | clever_pots
can_hit_spin_switches = has_sword | (hard_logic & (has_explosives | has_boomerang))
can_hit_spiral_switches = has_boomerang | has_hammer | has_explosives
quick_switches = has_boomerang | (has_bow & hard_logic)
tricky_switches = has_short_range | clever_pots

hammer_glitch = has_hammer & glitched_logic
bombchu_switches = has_chus | hammer_glitch
boomerang_glitch = has_boomerang & glitched_logic
arrow_glitch = has_bow & glitched_logic
chu_glitch = has_chus & glitched_logic
sword_glitch = has_sword & glitched_logic
grapple_glitch = has_grapple & glitched_logic
sword_scroll_clip = has_sword & glitched_logic & Has("Swordsman's Scroll")

# Keys
def has_small_keys(dung_name, count=1):
    return Has(f"Small Key ({dung_name})", count) | Has(f"Keyring ({dung_name})")

def has_boss_key(dung_name):
    return Has(f"Boss Key ({dung_name})") | Has(f"Keyring ({dung_name})", options=[OptionFilter(PhantomHourglassBossKeyrings, 1)])

def has_force_gems(floor, count=3):
    return Has(f"Force Gem (B{floor})", count) | Has(f"Force Gems", 1)

def has_shape_crystals(dung_name, shape, diff=""):
    return Or(
        Has(f"{shape} Crystal ({dung_name})"),
        Has(f"{shape} Crystals"),
        Has(f"{shape} Pedestal {diff} ({dung_name})")
    )

ut_vanilla_keys = smart_keys & vanilla_keys
ut_keys_own_dungeon = smart_keys & keys_own_dungeon
boss_keys_vanilla = [OptionFilter(PhantomHourglassRandomizeBossKeys, [0, 3], "in")]
boss_keys_own_dungeon = [OptionFilter(PhantomHourglassRandomizeBossKeys, 2, "ne")]
ut_boss_keys_own_dungeon = boss_keys_own_dungeon & smart_keys

open_post_dungeon = [OptionFilter(PhantomHourglassOpenPostDungeonLocations, 1)]

# Rupees
can_farm_rupees = Or(
    And(
        Has("_has_treasure_teller"),
        Or(
            Has("_can_farm_totok") & has_phantom_sword,
            randomize_minigames & HasAny("_can_play_archery", "_can_play_cannon_game", "_can_play_goron_race")
        )
    ),
    Has("_can_play_harrow") & [OptionFilter(PhantomHourglassRandomizeHarrow, 1)]
)

shop_restocks = [OptionFilter(PhantomHourglassShopsanity, "restocks", "contains")]
shop_potions = [OptionFilter(PhantomHourglassShopsanity, "potions", "contains")]
def has_restock_rupees(base_cost, locked_cost):
    return has_rupees(base_cost) | (has_rupees(base_cost-locked_cost) & shop_restocks)

def has_rupees(count):
    return (can_farm_rupees | ut_glitched
            | Has("Rupees", count)
            | (HasFromList("Rupees", "Treasure", count=count) & Has("_has_treasure_teller")))

def shop_shield(base_cost, locked_cost):
    return And(
        Filtered(has_shield, options=[OptionFilter(PhantomHourglassShieldInPool, 1)], filtered_resolution=True),
        has_rupees(base_cost) | (has_rupees(base_cost-locked_cost) & shop_restocks & shop_potions)
        )

beedle_bronze = HasBeedlePoints(1) | has_rupees(80)


# More Options
phantom_grapple = has_grapple & (ut_glitched | [OptionFilter(PhantomHourglassPhantomCombatDifficulty, 3)])
phantom_stun = (ut_glitched | [OptionFilter(PhantomHourglassPhantomCombatDifficulty, 2, "ge")]) & Or(has_bow, has_hammer, has_fire_sword)
phantom_traps = (ut_glitched | [OptionFilter(PhantomHourglassPhantomCombatDifficulty, 1, "ge")])
can_kill_phantoms = has_phantom_sword | phantom_grapple | phantom_stun
can_kill_phantoms_traps = can_kill_phantoms | phantom_traps

can_pass_sea_monster = has_cannon | [OptionFilter(PhantomHourglassSkipOceanFights, 1)]

goal_midway = [OptionFilter(PhantomHourglassGoal, PhantomHourglassGoal.option_triforce_door)]
goal_bellumbeck = [OptionFilter(PhantomHourglassBellumAccess, 4, "ne"), OptionFilter(PhantomHourglassGoal, 0, "ne")]

bellum_access_b13 = [OptionFilter(PhantomHourglassBellumAccess, 0)]
bellum_access_staircase_plus = [OptionFilter(PhantomHourglassBellumAccess, 1, "ge")]
bellum_access_warp = [OptionFilter(PhantomHourglassBellumAccess, 2)]
bellum_access_wreck = [OptionFilter(PhantomHourglassBellumAccess, 3)]

def charted_sea_monster(quadrant):
    return can_pass_sea_monster & require_sea_chart(quadrant)

has_go_mode = is_ut & Has("_required_dungeon",  # Show go mode early in UT
                                FromOption(PhantomHourglassDungeonsRequired),
                                options=[OptionFilter(PhantomHourglassGoal, 1)])

def spirit_pool():
    HasGroup("Metals", FromWorldAttr("required_metals"), options=[OptionFilter(PhantomHourglassBossRewardPool, 0)])

has_metals = (HasGroup("Metals", FromWorldAttr("required_metals"))
              & Filtered(HasRequiredSpirits(), options=[OptionFilter(PhantomHourglassBossRewardPool, 1)], filtered_resolution=True)
              ) | has_go_mode
win_on_metals = Filtered(has_metals, options=[OptionFilter(PhantomHourglassBellumAccess, PhantomHourglassBellumAccess.option_zauz)])

# Specific locations, move to logic file?
ember_grapple_chest = has_grapple | sword_glitch
oshus_gem = (has_phantom_blade & has_ph) | Has("_beat_tow")
can_defeat_bellum = And(has_grapple, has_phantom_sword, has_bow, has_spirit("Courage"))
can_defeat_bellumbeck = has_phantom_sword & has_spirit("Courage")
bannan_scroll = Has("_wayfarer_trade") & can_pass_sea_monster
bannan_sea_monster = And(
    require_sea_chart("NW"),
    can_pass_sea_monster | ut_glitched
)
ghost_ship_access = And(
    require_sea_chart("NW"),
    [OptionFilter(PhantomHourglassFogSettings, 2)] | (
        has_spirit("Power") & has_spirit("Wisdom") & has_spirit("Courage")
    )
)
goron_chus = has_shovel & (
                has_bow | has_grapple | (has_hammer & hard_logic)
            ) | (has_hammer & glitched_logic)

ice_field = Has("_beat_toi") | (can_kill_dark_yook & has_bombs)
ruins_water = Has("_ruins_lower_water")

def savescum_keys(dung, count):
    return ut_glitched & has_small_keys(dung, count)

def simple_boss_key(dung):
    return Or(has_boss_key(dung),
              smart_keys & boss_keys_vanilla)

# Pirate Ambush
unlock_ambush = Has("_beat_ghost_ship") | open_post_dungeon

pirate_ambush_nw = Has("_beat_cubus_sisters") & Has("_beat_ghost_ship") & vanilla_dungeons & vanilla_bosses

# Mountain Passage
mp_rat = can_kill_bat | (clever_pots & vanilla_caves)
can_reach_mp2 = Or(
    has_small_keys("Mountain Passage", 2),
    Filtered(Or(
        And(
            smart_keys | is_not_ut,
            mp_rat
        ),
        Filtered(has_small_keys("Mountain Passage", 1), options=vanilla_caves)
    ), options=keys_own_dungeon),
    savescum_keys("Mountain Passage", 1)
)

mp2_top = has_small_keys("Mountain Passage", 2) | (ut_glitched & has_small_keys("Mountain Passage", 1))
mp2_bypass_fore = Or(
    has_small_keys("Mountain Passage", 3),
    savescum_keys("Mountain Passage", 2),
    And(
        Filtered(Or(), options=vanilla_caves) | keys_own_dungeon,
        has_small_keys("Mountain Passage", 2),
        is_not_ut | smart_keys
    )
)
mp2_bypass = Or(
    has_small_keys("Mountain Passage", 3),
    savescum_keys("Mountain Passage", 2),
    hard_logic
)
mp3 = Or(
    has_small_keys("Mountain Passage", 3),
    savescum_keys("Mountain Passage", 1),
    has_small_keys("Mountain Passage", 1) & ut_keys_own_dungeon,
    keys_own_dungeon & is_not_ut & mp_rat
)
mp3_back = Or(
    has_small_keys("Mountain Passage", 3),
    has_small_keys("Mountain Passage", 2) & (Filtered(Or(), options=vanilla_caves) | keys_own_dungeon),
    savescum_keys("Mountain Passage", 1)
)

# ToF
tof_maze = has_small_keys("Temple of Fire") | (ut_keys_own_dungeon & can_kill_bat)
tof_3f = And(
    has_small_keys("Temple of Fire", 2) | ut_keys_own_dungeon,
    has_boomerang | has_hammer | clever_bombs | (hard_logic & has_chus & (has_bow | has_grapple))
)
tof_key_drop = has_boomerang | (has_grapple & hard_logic)
tof_key_door = has_small_keys("Temple of Fire", 3) | (ut_keys_own_dungeon & tof_key_drop)
tof_bk = has_boss_key("Temple of Fire") | (has_boomerang & ut_boss_keys_own_dungeon)

# ToW
tow_key_ut = is_ut & has_shovel & (
    vanilla_keys | (has_bombs & keys_own_dungeon)
)
tow_key = has_small_keys("Temple of Wind") | tow_key_ut
tow_bk = has_bombs & (
    has_boss_key("Temple of Wind") | (
        ut_boss_keys_own_dungeon & tow_key_ut
    )
)

# ToC
def toc_key_doors(glitched, not_glitched, savescum=1):
    return Or(has_small_keys("Temple of Courage", glitched) & glitched_logic,
              has_small_keys("Temple of Courage", not_glitched) & not_glitched_logic,
              savescum_keys("Temple of Courage", savescum))

toc_door_1 = And(
    has_damage,
    Or(
        toc_key_doors(3, 1),
        ut_keys_own_dungeon & not_glitched_logic & (has_explosives | vanilla_keys)
    )
)
def toc_crystal(diff):
    return has_shape_crystals("Temple of Courage", "Square", diff)
def toc_crystals_state(state: CollectionState, player: int, diff: str):
    shape, dung_name = "Square", "Temple of Courage"
    return any([
        state.has(f"{shape} Crystal ({dung_name})", player),
        state.has(f"{shape} Crystals", player),
        state.has(f"{shape} Pedestal {diff} ({dung_name})", player),
    ])
toc_door_2 = Or(
    toc_key_doors(3, 3, 2),
    toc_key_doors(3, 2) & pedestals_vanilla_any,
    is_ut & Or(
        savescum_keys("Temple of Courage", 1) & has_hammer,
        not_glitched_logic & smart_keys & Or(
            keys_own_dungeon & has_explosives & has_grapple & has_bow,
            vanilla_keys & (has_explosives | (has_bow & has_grapple))
        )
    )
)
toc_all_checks_door_3 = Or(
    keys_own_dungeon & has_bow & has_explosives,
    vanilla_keys & (hammer_glitch | (has_bow & (has_grapple | has_explosives)))
)
toc_door_3 = Or(
    toc_key_doors(3, 3, 3),
    is_ut & Or(
        smart_keys & toc_all_checks_door_3,
        savescum_keys("Temple of Courage", 1) & has_hammer,
        savescum_keys("Temple of Courage", 2) & has_grapple,
    )
)

# GS
gs_barrel = has_hammer | has_boomerang | has_grapple | has_shape_crystals("Ghost Ship", "Round") | (has_bombs & hard_logic)
gs_triangle = has_shape_crystals("Ghost Ship", "Triangle") | (smart_keys & pedestals_vanilla_any)

# GT
gt_bk = has_boss_key("Goron Temple") | (ut_boss_keys_own_dungeon & has_chus)

# ToI
toi = "Temple of Ice"
def toi_key_doors(glitched, not_glitched):
    return Or(
        has_small_keys(toi, not_glitched) & not_glitched_logic,
        has_small_keys(toi, glitched) & glitched_logic
    )

toi_all_doors_ut = smart_keys & keys_own_dungeon & has_grapple & has_explosives & has_bow & quick_switches
toi_3f_boomerang = quick_switches & (has_boomerang | has_grapple)
toi_door_1 = toi_key_doors(3, 1) | (
    is_ut & Or(
        savescum_keys(toi, 1),
        smart_keys & Or(
            toi_all_doors_ut,
            And(
                toi_3f_boomerang & not_glitched_logic,  # switch key
                vanilla_keys | (
                    keys_own_dungeon & (
                        (
                            (has_explosives | has_boomerang) & hard_logic
                        ) | has_bombs  # final chest in normal logic
                    )
                )
            ),

        )
    )
)
toi_door_2 = Or(
    toi_key_doors(3, 2),
    is_ut & Or(
        Filtered(keys_own_dungeon & quick_switches, options=not_glitched_logic),
        savescum_keys(toi, 1),
    toi_all_doors_ut
    )
)
toi_b2 = has_bow & has_grapple & Or(
    quick_switches & Has("_toi_b1_switch"),
    chu_glitch & has_boomerang
)
toi_door_3 = Or(
    toi_key_doors(3, 3),
    toi_all_doors_ut,
    And(
        ut_glitched, has_small_keys("Temple of Ice", 1), has_hammer, has_grapple, has_explosives
    )
)
toi_bk = has_boss_key(toi) | (ut_boss_keys_own_dungeon & toi_all_doors_ut)
gleeok = has_grapple & (has_sword | Has("Bombs (Progressive)", 2) | has_hammer | (Has("Bomb Bag") & Has("Bomb Bag Upgrade")))


# MT
mt = "Mutoh's Temple"
def mt_keys(glitched, not_glitched):
    return Or(has_small_keys(mt, not_glitched) & not_glitched_logic,
              has_small_keys(mt, glitched) & glitched_logic,
              has_small_keys(mt, 1) & ut_glitched)
mutoh_entrance = Or(
    has_explosives,
    has_hammer & hard_logic,
    has_boomerang & (has_bow | has_sword)
)
mutoh_water = Or(
    has_explosives & has_beam_sword & glitched_logic,  # bombchu skew
    arrow_glitch,  # arrow despawn
    And(
        has_bow,
        has_boomerang | has_beam_sword,
        mt_keys(2, 1) | ut_keys_own_dungeon,
    )
)
mutoh_bk_chest = Or(
    has_small_keys(mt, 2),
    ut_keys_own_dungeon,
    savescum_keys(mt, 1)
)
mutoh_bk = has_boss_key(mt) | (ut_boss_keys_own_dungeon & mutoh_bk_chest)

# TotOK
# Time
time_logic_none = ut_glitched | [OptionFilter(PhantomHourglassTimeLogic, 5)]
time_require_ph = ut_glitched | [OptionFilter(PhantomHourglassTimeRequiresHourglass, 1)]

def has_sand(time):
    return Has("Sand", time)

def has_floor_time(room, time=0):
    floor_func = floor_lookup[room]
    return ut_glitched | HasTime(time, floor_func, room)


totok = "Temple of the Ocean King"
def totok_keys(count):
    return has_small_keys(totok, count) | (is_ut & TotOKSmallKeys(count))

def totok_deep_keys(count):
    return has_small_keys(totok, count) | (has_small_keys(totok, count-1) & has_grapple) | (is_ut & TotOKSmallKeys(count))

def totok_shape_crystals(shape, diff):
    return has_shape_crystals(totok, shape, diff)

ut_pedestals_vanilla = smart_keys & pedestals_vanilla

# Floor Logic, o is time logic option value taken from outer scope
# 1F
totok_1f = has_floor_time(0)
totok_1f_chest = has_floor_time(0, 5)

# B1
totok_b1 = has_floor_time(1) & has_spirit("Power")
totok_b1_key = Or(
    (has_explosives | has_grapple) & has_floor_time(1, 15),
    has_boomerang & has_floor_time(1, 25))
totok_b1_phantom = Or(
    has_phantom_sword & has_floor_time(1, 10),
    can_kill_phantoms & has_floor_time(1, 30))
totok_b1_bow = has_bow & has_grapple & has_floor_time(1, 12)

totok_b1_all_checks_ut = And(
    ut_keys_own_dungeon, has_spirit("Power"), totok_b1_bow, totok_b1_key, totok_b1_phantom)

totok_1f_chart = (has_floor_time(0, 15)
                               & Or(totok_keys(1), totok_b1_all_checks_ut))
# B2
totok_b2 = has_floor_time(2) & (totok_keys(2) | totok_b1_all_checks_ut)
totok_b2_key = Or(
    has_explosives & has_floor_time(2, 15),
    boomerang_glitch & has_floor_time(2, 20),
    clever_pots & has_floor_time(2, 70))
totok_b2_phantom = has_phantom_sword & (has_mid_range | has_explosives) & has_floor_time(2, 20)
totok_b2_chu = bombchu_switches & has_floor_time(2, 20)

totok_b2_all_checks_ut = And(
    totok_b1_all_checks_ut, totok_b2_phantom, totok_b2_chu, totok_b2_key)

# B3
totok_b3 = has_floor_time(3) & (totok_keys(3) | totok_b2_all_checks_ut)
totok_b3_nw = has_floor_time(3, 5)
totok_b3_se = has_floor_time(3, 10)
totok_b3_bow = has_bow & (
        (has_shovel & has_floor_time(3, 20))
        | has_floor_time(3, 25))
totok_b3_key = can_steal_from_phantom & has_floor_time(3, 5)
totok_b3_phantom = has_grapple & Or(
    has_phantom_sword & Or(
        (has_shovel & has_floor_time(3, 15)),
        has_floor_time(3, 20)),
    can_kill_phantoms_traps & has_floor_time(3, 35))
totok_b35 = has_floor_time(4)

# B4
totok_b4 = has_spirit("Wisdom") & has_floor_time(4)
totok_b4_key = Or(
    boomerang_glitch & has_floor_time(4, 6),
    bombchu_switches & Or(
        has_bow & has_floor_time(4, 12),
        has_pot_range & has_floor_time(4, 20)
    ),
    has_bombs & Or(
        has_bow & has_floor_time(4, 20),
        has_pot_range & has_floor_time(4, 40),
    )
)
totok_b4_eyes = can_kill_phantom_eyes & Or(
    has_bow & has_floor_time(4, 25),
    has_pot_range & has_floor_time(4, 40),
)
totok_b4_phantom = has_phantom_sword & Or(
    has_bow & has_floor_time(4, 15),
    has_pot_range & has_floor_time(4, 25),
)

totok_b4_all_checks_ut = And(
    totok_b2_all_checks_ut, has_spirit("Wisdom"),
    totok_b3_phantom, totok_b3_bow,
    totok_b4_phantom, totok_b4_eyes, totok_b4_key
)
totok_b3_sw = has_floor_time(3, 7) & (totok_keys(4) | totok_b4_all_checks_ut)

# B5
totok_b5 = has_floor_time(5) & (totok_deep_keys(5) | totok_b4_all_checks_ut)
totok_b5_alt = bombchu_switches & totok_b5
totok_b5_chest = can_kill_bubble & has_pot_range & has_floor_time(5, 25)
totok_b5_alt_chest = (has_shovel | has_grapple) & has_floor_time(5, 7)

# B6
totok_b6 = has_floor_time(6)
totok_b6_bow = has_bow & has_floor_time(6, 10)
totok_b6_phantom = has_phantom_sword & has_floor_time(6, 15)
totok_b6_crest = has_sea_chart("SW") & has_floor_time(6, 10)

# B7
totok_b7 = has_triforce_crest & has_floor_time(7)
totok_b7_crystal = Or(
    has_grapple & has_floor_time('7_g'),
    can_hit_switches & has_floor_time('7_e'))
totok_b7_switch_chest = has_range & (has_floor_time('7_g', 15) | has_floor_time('7_e', 30))
totok_b7_phantom = Or(
    has_phantom_sword & has_floor_time('7_e', 20),
    can_kill_phantoms & has_floor_time('7_e', 70),
)

# B8
totok_b8 = has_floor_time(8)
totok_b8_phantom = Or(
    has_phantom_sword & has_floor_time(8, 25),
    can_kill_phantoms & has_floor_time(8, 45))
totok_b8_2_crystals_chest = And(
    has_explosives | pedestals_not_vanilla,
    Or(
        ut_pedestals_vanilla,
        totok_shape_crystals("Round", "B8") & totok_shape_crystals("Triangle", "B8")
    ),
    Or(
        pedestals_not_vanilla & has_floor_time("8_2c", 15),
        pedestals_vanilla & has_floor_time("8_2c", 30)
    )
)

# B9
totok_b9 = Or(
    bombchu_switches & has_floor_time('9_1c'),
    And(
        totok_shape_crystals("Triangle", "B8") | ut_pedestals_vanilla,
        has_explosives | pedestals_not_vanilla,
        has_floor_time('9_2c'),
    ),
    And(
        totok_shape_crystals("Square", "West") & pedestals_not_vanilla,
        totok_shape_crystals("Round", "B8") | has_hammer,
        has_floor_time('8_2c', 5),
    )
)
totok_b9_abstract_triangle = totok_shape_crystals("Triangle", "B8") & pedestals_not_vanilla
def totok_b9_routes(route):
    return Or(
        has_phantom_sword & has_floor_time(route, 12),
        can_kill_phantoms_traps & Or(
            has_hammer & has_floor_time(route, 17),
            has_bow & has_boomerang & has_floor_time(route, 20))
    )
totok_b9_phantom = Or(
    (bombchu_switches | totok_b9_abstract_triangle) & totok_b9_routes(9),
    totok_b9_routes("9_1c"),
)
totok_b9_crystal = can_steal_from_phantom & has_floor_time(9, 10)
totok_b9_wizzrobes = has_floor_time("9_1c", 30) | (bombchu_switches & has_floor_time(9, 30))
def totok_b9_square_crystal(diff):
    return (can_steal_from_phantom & pedestals_vanilla) | totok_shape_crystals("Square", diff)
totok_b9_corner_chest = Or(
    (has_hammer | ut_pedestals_vanilla | totok_shape_crystals("Round", "B8") & has_floor_time("8_2c")),
    (totok_b9_square_crystal("West") | has_grapple) & (has_floor_time(9, 25) | has_floor_time("9_2c"))
)
totok_b9_all_crystals = And(
    totok_b9_square_crystal("Center"),
    totok_shape_crystals("Round", "B9"),
    totok_shape_crystals("Triangle", "B9")
)

# B10
totok_b10 = (ut_pedestals_vanilla | totok_b9_all_crystals) & has_floor_time(10)
totok_b10_key = can_steal_from_phantom & has_floor_time(10, 10)
totok_b10_phantom = has_explosives & Or(
    has_phantom_sword & has_floor_time(10, 30),
    can_kill_phantoms_traps & has_floor_time(10, 45)
)
totok_b10_eyes = has_explosives & Or(
    has_chus & has_floor_time(10, 40),
    has_floor_time(10, 45)
)
totok_b10_hammer = has_hammer & has_explosives & Or(
    has_chus & has_floor_time(10, 20),
    has_floor_time(10, 35)
)
totok_b10_all_checks_ut = And(
    totok_b4_all_checks_ut,
    has_triforce_crest,
    has_spirit("Courage"),
    has_sea_chart("SW"),
    has_hammer,
    has_explosives,
    has_shovel
)

# B11
totok_b11 = has_explosives & has_floor_time(11) & (totok_deep_keys(6) | totok_b10_all_checks_ut)
totok_b11_phantom = has_phantom_sword & has_floor_time(11, 10)
totok_b11_eyes = has_floor_time(11, 25)

# B12
def totok_b12_routes(normal=0, hammer=0):
    return has_floor_time("12_h", hammer) | has_floor_time(12, normal)
totok_b12 = totok_b12_routes()
totok_b12_nw = totok_b12_routes(12, 15)
totok_b12_ne = totok_b12_routes(35, 15)
totok_b12_phantom = has_phantom_sword & totok_b12_routes(55, 40)
totok_b12_gem = can_steal_from_phantom & totok_b12_routes(15, 5)
totok_b12_wizzrobes = Or(
    pedestals_not_vanilla & has_force_gems(12, 2) & totok_b12_routes(20, 20),
    totok_b12_routes(50, 70) & pedestals_vanilla
)
totok_b12_hammer = has_floor_time("12_h", 10)

# B13
totok_b13 = And(
    Or(
        can_steal_from_phantom & pedestals_vanilla,
        has_force_gems(12, 3)
    ),
    has_floor_time(13)
)
totok_b13_chest = has_floor_time(13, 5)
totok_b13_door = (has_phantom_sword & has_floor_time(13, 30)
                  & (bellum_access_staircase_plus | Filtered(has_metals, options=bellum_access_b13)))