from BaseClasses import MultiWorld, Item, EntranceType
from typing import TYPE_CHECKING
from .data.LogicPredicates import *
from .Options import SpiritTracksOptions
from .data.Entrances import ENTRANCES

if TYPE_CHECKING:
    from . import SpiritTracksWorld
    from .Subclasses import STTransition
    from BaseClasses import Region, Entrance


def make_overworld_logic(player: int, origin_name: str, options: SpiritTracksOptions):

    overworld_logic = [

        # ====== Outset Village ==============

        #[region 1, region 2, two-directional, logic requirements],
        ["outset village", "forest realm", False, lambda state: st_has_train(state, player)],

        ["outset village", "outset village stamp book", False, lambda state:
            st_has_passenger(state, player, "Alfonzo", "_picked_up_alfonzo") or
            (st_has_glyph(state, player, "Snow") and not options.randomize_passengers)],
        ["outset village stamp book", "outset 10 stamps", False, lambda state: state.has("Stamp", player, 10)],
        ["outset village stamp book", "outset 15 stamps", False, lambda state: state.has("Stamp", player, 15)],
        ["outset village stamp book", "outset 20 stamps", False, lambda state: state.has("Stamp", player, 20)],
        ["outset village", "outset village stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["outset village", "outset village trees", False, lambda state: st_has_discovery_song(state, player)],
        ["outset village", "outset joe", False, lambda state: st_has_source(state, player, "Snow")],
        ["outset village", "outset cuccos", False, lambda state: st_has_cargo(state, player, "Cuccos", "_buy_cuccos")]
            if options.randomize_cargo.value in [1, 2] else
        ["outset village", "outset cuccos", False, lambda state: state.has("Wagon", player)
                                                                 and (state.has("Cargo: Cuccos (5)", player, 3)
                                                                      or (state.has("Cargo: Cuccos (5)", player, 2)
                                                                          and state.has("_UT_Glitched_Logic", player)))],
        ["outset village", "outset ferrus", False, lambda state: st_has_passenger(state, player, "Alfonzo", "_picked_up_alfonzo")
                                                                 and st_has_passenger(state, player, "Ferrus", "_ferrus_1")],

        # ========= Forest Realm ==========

        ["forest realm", "forest realm se portal track", False, lambda state: st_has_misc_tracks(state, player, "Forest Realm SE Portal")],
        ["forest realm", "forest realm rabbits", False, lambda state: st_has_net(state, player)],
        ["forest realm", "wtt", False, lambda state: st_has_temple_tracks(state, player, "Wooded")],
        ["forest realm", "forest source", False, lambda state: st_has_source(state, player, "Forest")],
        ["forest realm", "w castle town tracks", False, lambda state: st_has_misc_tracks(state, player, "W Castle Town")],
        ["forest realm", "n castle town tracks", False, lambda state: st_has_misc_tracks(state, player, "N Castle Town")],
        ["wtt", "snow realm fr", True, lambda state: st_has_temple_tracks(state, player, "Wooded") and st_has_glyph(state, player, "Snow") and st_has_cannon(state, player)],
        ["forest realm", "snow realm fr portal", False, lambda state: st_has_portal(state, player, "Hyrule Castle to Anouki Village", False) and st_has_glyph(state, player, "Snow")],
        ["snow realm fr portal", "snow realm fr", False, None],
        ["snow realm fr portal", "snow realm", False, None],
        ["forest realm", "dark realm portal", True, lambda state: st_has_compass_of_light(state, player)],

        # cave
        ["forest realm", "forest cave tracks", True, lambda state: st_has_misc_tracks(state, player, "Forest Realm SW Cave")],
        ["forest cave tracks", "forest cave portal", False, lambda state: st_has_cannon(state, player)],
        ["forest cave tracks", "w forest tracks", True, lambda state: st_has_misc_tracks(state, player, "Forest Realm SW Cave") and st_has_misc_tracks(state, player,"W Forest Realm") and st_soft_cannon(state, player)],
        ["w forest tracks", "snow realm fr", True, lambda state: st_has_glyph(state, player, "Snow") and st_has_misc_tracks(state, player, "W Forest Realm")],
        ["w forest tracks", "wtt", True, lambda state: st_has_temple_tracks(state, player, "Wooded") and st_has_misc_tracks(state, player, "W Forest Realm")],

        # W Wooded temple
        ["wtt", "w wooded temple tracks", True, lambda state: st_has_misc_tracks(state, player, "W Wooded Temple") and st_has_temple_tracks(state, player, "Wooded")],
        ["w wooded temple tracks", "snow realm fr", True, lambda state: st_has_misc_tracks(state, player, "W Wooded Temple") and st_has_glyph(state, player, "Snow")],
        ["w wooded temple tracks", "snow realm", True,
         lambda state: st_has_misc_tracks(state, player, "W Wooded Temple") and st_has_glyph(state, player, "Snow")],

        # Rabbits
        ["forest realm rabbits", "forest ocean shortcut rabbit", False, lambda state: st_has_misc_tracks(state, player, "Forest Realm Ocean Shortcut")],
        ["forest realm rabbits", "e mayscore rabbits", False, lambda state: st_has_misc_tracks(state, player, "E Mayscore Bridge")],
        ["forest realm se portal track", "sw trading post rabbit", False, lambda state: st_has_net(state, player)],
        ["forest realm rabbits", "sw trading post rabbit", False, lambda state: st_has_glyph(state, player, "Ocean") and st_option_hard_logic(state, player)],
        ["wtt", "wt rabbit", False, lambda state: st_has_net(state, player)],
        ["forest source", "wt rabbit", False, lambda state: st_has_net(state, player)],
        ["w forest tracks", "s rabbit haven rabbits", False, lambda state: st_has_net(state, player)],
        ["snow realm rabbits", "nr rabbit haven rabbit", False, None],

        # Snow bridge
        ["w castle town tracks", "snow bridge", True, lambda state: st_has_misc_tracks(state, player, "W Castle Town") and st_has_misc_tracks(state, player, "Snow Realm Bridge") and st_soft_cannon(state, player)],
        ["n castle town tracks", "snow bridge", True, lambda state: st_has_misc_tracks(state, player, "N Castle Town") and st_has_misc_tracks(state, player, "Snow Realm Bridge") and st_soft_cannon(state, player)],
        ["n castle town tracks", "snow realm source", True, lambda state: st_has_misc_tracks(state, player, "N Castle Town") and st_has_source(state, player, "Snow") and st_soft_cannon(state, player)],
        ["wtt", "snow bridge", True, lambda state: st_has_temple_tracks(state, player, "Wooded") and st_has_misc_tracks(state, player,"Snow Realm Bridge") and st_soft_cannon(state, player)],
        ["snow bridge", "snow realm", True, lambda state: (
            st_has_glyph(state, player, "Snow") and
            st_has_misc_tracks(state, player,"Snow Realm Bridge"))],
        ["snow bridge", "snow realm source", True, lambda state: st_has_source(state, player, "Snow") and st_has_misc_tracks(state, player, "Snow Realm Bridge")],
        ["snow bridge", "snow bridge portal", False, lambda state: st_has_cannon(state, player)],

        ["wtt", "forest ferrus", False, lambda state: st_has_passenger(state, player, "Ferrus", "_ferrus_3")],
        ["forest source", "forest ferrus", False, lambda state: st_has_passenger(state, player, "Ferrus", "_ferrus_3")],

        # # ======== Castle Town =========

        ["forest realm", "castle town", True, None],
        ["castle town", "castle town goron", False, lambda state: st_has_passenger(state, player, "City Goron", "_goron")],
        ["castle town", "pick up alfonzo", False, lambda state: st_has_glyph(state, player, "Snow")],
        ["castle town", "castle town teacher", False, lambda state: st_has_glyph(state, player, "Snow") or st_has_glyph(state, player, "Ocean")],
        ["pick up alfonzo", "alfonzo event", False, None],
        ["pick up alfonzo", "castle town mona", False, None],
        ["castle town wall", "castle town stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["castle town", "castle town wall", False, lambda state: st_has_bombs(state, player)],
        ["castle town wall", "castle town cuccos", False, lambda state: st_castle_town_cuccos(state, player)],
        ["castle town", "castle town fish", False, lambda state: st_has_cargo(state, player, "Fish", "_buy_fish")],

        ["castle town", "teao rupees", False, lambda state: st_has_rupees(state, player, 150) or state.has("_UT_Glitched_Logic", player)],
        ["teao rupees", "teao 1", False, lambda state:
            st_has_sword(state, player) and
            st_has_whirlwind(state, player) and
            any([
                st_has_source(state, player, "Forest"),
                st_has_source(state, player, "Ocean"),
                st_has_source(state, player, "Sand")])],
        ["teao rupees", "teao 2", False, lambda state:
            (st_has_source(state, player, "Ocean") or
             st_has_source(state, player, "Sand")) and
            st_has_sword(state, player) and
            st_has_whirlwind(state, player) and
            st_has_boomerang(state, player) and
            st_has_whip(state, player)],
        ["teao rupees", "teao 3", False, lambda state:
            st_has_source(state, player, "Sand") and
            st_has_bow(state, player) and
            st_has_sand_wand(state, player) and
            st_has_sword(state, player) and
            st_has_whirlwind(state, player) and
            st_has_boomerang(state, player) and
            st_has_whip(state, player)],
        ["teao 3", "teao_event", False, None],

        # # ======== Hyrule Castle =========

        ["castle town", "hyrule castle", False, None],
        ["hyrule castle", "hyrule castle sword minigame", False, lambda state: st_has_sword(state, player) and st_has_source(state, player, "Snow") and st_has_rupees(state, player, 100)],

        # # ======== ToS Tunnel =========

        ["hyrule castle", "tower tunnel", False, None],
        ["tower tunnel", "tower tunnel block chest", False, lambda state: (st_can_kill_bat(state, player) or st_has_whirlwind(state, player) or st_option_hard_logic(state, player))],
        ["tower tunnel", "tower tunnel 2f chest", False, lambda state: st_has_small_keys(state, player, "Tunnel to ToS", 1)],

        # # ========== ToS ===================

        ["forest realm", "tos", True, lambda state: st_can_enter_tos(state, player)],
        ["snow realm source", "tos", True, lambda state: st_can_enter_tos(state, player) and st_has_source(state, player, "Snow") and st_soft_cannon(state, player)],
        ["ocean realm source", "tos", True, lambda state: st_can_enter_tos(state, player) and st_has_source(state, player, "Ocean")],
        ["fire source", "tos", True, lambda state: st_can_enter_tos(state, player) and st_has_source(state, player, "Fire")],

        ["tos", "tos 1f", True, None],
        ["tos", "tos 2", False, lambda state: st_can_enter_tos_section(state, player, 2)],
        ["tos", "tos 3", False, lambda state: st_can_enter_tos_section(state, player,3)],
        ["tos", "tos 4", False, lambda state: st_can_enter_tos_section(state, player,4)],
        ["tos", "tos 5", False, lambda state: st_can_enter_tos_section(state, player,5)],
        ["tos 5", "tos 22f", False, lambda state: state.multiworld.worlds[player].exclude_tos_5],  # bypass tos 5 if excluded

        ["tos 1f", "tos 1f chest", False, lambda state: (st_has_bow(state, player) or st_has_boomerang(state, player) or st_has_beam_sword(state, player))],
        ["tos 1f", "tos 1f switch", False, lambda state: st_can_kill_bat(state, player) or st_can_possess_phantoms(state, player, 1)],
        ["tos 1f", "tos 2f", False, lambda state: st_can_possess_phantoms(state, player, 1) or st_vanilla_tears(state, player)],
        ["tos 2f", "tos 2f raised chests", False, lambda state: st_has_whirlwind(state, player) or st_option_glitched_logic(state, player)],
        ["tos 2f", "tos 2f bomb wall", False, lambda state: st_has_bombs(state, player)],
        ["tos 2f", "tos 3f rail map", False, None],
        ["tos 3f rail map", "goal_forest_glyph", False, None],
        ["tos 3f rail map", "event_3f", False, None],

        ["tos 2", "tos 4f", True, None],
        ["tos 4f", "tos 4f whirlwind", False, lambda state: st_has_whirlwind(state, player)],
        ["tos 4f", "tos 5f phantom", False, lambda state: st_can_possess_phantoms(state, player, 2) or (st_vanilla_tears(state, player) and st_has_whirlwind(state, player))],
        ["tos 5f phantom", "tos 5f spinnit key", False, lambda state: st_has_whirlwind(state, player)],
        ["tos 5f spinnit key", "tos 5f alt path", False, lambda state: st_has_boomerang(state, player)],
        ["tos 5f alt path", "tos 5f secret chest", False, lambda state: st_has_bombs(state, player)],
        ["tos 5f alt path", "tos 4f ne chest", False, lambda state: st_has_bombs(state, player)],
        ["tos 5f alt path", "tos 6f chests", False, None],
        ["tos 5f spinnit key", "tos 6f key", False, lambda state: st_has_small_keys(state, player, "ToS 2", 1)],
        ["tos 6f key", "tos 7f rail map", False, lambda state: st_has_small_keys(state, player, "ToS 2", 2)],
        ["tos 7f rail map", "goal_snow_glyph", False, None],
        ["tos 7f rail map", "event_7f", False, None],

        ["tos 3", "tos 8f", True, None],
        ["tos 8f", "tos 8f bombs", False, lambda state: st_has_bombs(state, player)],
        ["tos 8f", "tos 9f phantom", False, lambda state: st_can_possess_phantoms(state, player, 3) or st_vanilla_tears(state, player)],
        ["tos 9f phantom", "tos 9f nw", False, lambda state: st_has_whirlwind(state, player)],
        ["tos 9f phantom", "tos 11f", False, lambda state: st_has_damage(state, player) and (st_has_boss_key(state, player, "ToS 3") or options.randomize_boss_keys == "vanilla")],
        ["tos 11f", "event_12f", False, None],
        ["tos 11f", "goal_ocean_glyph", False, None],


        ["tos 4", "tos 13f", True, None],
        ["tos 13f", "tos 13f whip", False, lambda state: st_has_whip(state, player)],
        ["tos 13f", "tos 13f boomerang", False, lambda state: st_has_boomerang(state, player)],
        ["tos 13f", "tos 14f east", False, lambda state: st_has_small_keys(state, player, "ToS 4", 3, 1) | (st_vanilla_tears(state, player) & st_has_small_keys(state, player, "ToS 4", 2, 1))],
        ["tos 13f", "tos 13f phantom", False, lambda state: any([
            st_can_possess_phantoms(state, player, 4), all([
                st_vanilla_tears(state, player),
                st_has_whip(state, player),
                st_has_small_keys(state, player, "ToS 4", 2, 1)])])],
        ["tos 13f phantom", "tos 13f phantom whip", False, lambda state: st_has_whip(state, player)],
        ["tos 13f phantom", "tos 14f west", False, lambda state: st_tos_14f_glitched(state, player)],

        ["tos 14f east", "tos 14f phantom", False, lambda state:
         st_can_possess_phantoms(state, player, 4) | (st_vanilla_tears(state, player) & st_has_whip(state, player))],
        ["tos 14f west", "tos 15f", False, lambda state: st_has_whip(state, player)],
        ["tos 15f", "tos 16f", False, lambda state: st_tos_15f_glitched(state, player)],
        ["tos 16f", "tos 16f bombs", False, lambda state: st_has_bombs(state, player)],
        ["tos 16f", "event_17f", False, None],
        ["tos 16f", "goal_fire_glyph", False, None],

        ["tos 5", "tos 18f", True, None],
        ["tos 18f", "tos 18f whip", False, lambda state: st_has_whip(state, player)],
        ["tos 18f", "tos 19f", False, lambda state: st_has_small_keys(state, player, "ToS 5", 1)],
        ["tos 18f", "tos 18f phantom", False, lambda state: st_can_possess_phantoms(state, player, 5)],
        ["tos 18f phantom", "tos 19f center", False, None],

        ["tos 19f", "tos 19f south", False, lambda state:
         st_has_bow(state, player) & (st_has_boomerang(state, player) | st_can_possess_phantoms(state, player, 5))],
        ["tos 19f south", "tos 20f tear", False,  lambda state:
            st_has_boomerang(state, player) or
            st_has_beam_sword(state, player) or
            (st_option_hard_logic(state, player) and st_can_rotate_repeater(state, player) and (
                st_can_possess_phantoms(state, player, 5) or
                st_has_whip(state, player)))
         ],
        ["tos 19f", "tos 19f center", False, lambda state:
         st_can_possess_phantoms(state, player, 5) | (st_vanilla_tears(state, player) & st_has_bow(state, player) & st_has_boomerang(state, player))],
        ["tos 19f center", "tos 19f", False, None],
        ["tos 19f center", "tos 19f center chest", False, lambda state: st_has_bow(state, player) & (st_has_boomerang(state, player) | st_has_beam_sword(state, player) | st_has_whip(state, player))],
        ["tos 19f center", "tos 18f phantom", False, None],
        ["tos 19f center", "tos 20f", False, lambda state: st_has_small_keys(state, player, "ToS 5", 2)],

        ["tos 20f", "tos 19f center 2", False, lambda state: st_has_bow(state, player) & st_can_rotate_repeater(state, player)],
        ["tos 20f", "tos 19f center chest", False, lambda state: st_has_bow(state, player)],
        ["tos 20f", "tos 22f", False, lambda state: st_has_bow(state, player) and st_can_rotate_repeater(state, player) and st_has_whip(state, player)],
        ["tos 22f", "tos 21f bombs", False, lambda state: st_has_bombs(state, player)],
        ["tos 22f", "tos staven", False, lambda state: st_has_sword(state, player) and (st_has_boss_key(state, player, "ToS 5") or options.randomize_boss_keys == "vanilla" or state.multiworld.worlds[player].exclude_tos_5)],
        ["tos staven", "event_staven", False, None],
        ["tos staven", "goal_staven", False, None],

        ["tos staven", "tos summit lower", True, None],
        ["tos summit lower", "tos summit", True, None],
        ["tos summit", "tos stamp stand", False, lambda state: st_has_stamp_book(state, player)],
        ["tos summit", "tos 6", False, lambda state: st_has_bow_of_light(state, player)],
        ["tos 30f", "tos 6", True, None],

        ["tos 30f", "tos 30f bomb wall", False, lambda state: st_has_bombs(state, player)],
        ["tos 30f", "tos 29f", False, lambda state: st_can_possess_phantoms(state, player, 6) & st_has_boomerang(state, player) & st_has_whirlwind(state, player)],
        ["tos 29f", "tos 29f sand wand", False, lambda state: st_has_sand_wand(state, player)],
        ["tos 29f sand wand", "tos 29f se", False, lambda state: st_has_bow_of_light(state, player)],

        ["tos 29f se", "tos 27f", False, lambda state: st_has_small_keys(state, player, "ToS 6", 3)],
        ["tos 27f", "tos 24f", False, lambda state: st_has_whip(state, player)],
        ["tos 29f", "tos 24f", False, lambda state: st_option_glitched_logic(state, player) and st_has_bombs(state, player) and st_has_small_keys(state, player, "ToS 6", 3, 1)],
        ["tos 24f", "event_24f", False, None],
        ["tos 24f", "goal_compass", False, None],


        # # ======== Mayscore =========

        ["forest realm", "mayscore", False, None],
        ["mayscore", "mayscore stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["mayscore", "mayscore whip chest", False, lambda state: st_has_whip(state, player)],
        ["mayscore whip chest", "mayscore whip game", False, lambda state: st_has_rupees(state, player, 200) or state.has("_UT_Glitched_Logic", player)],  # safety protecting against early rupee farming
        ["mayscore", "mayscore leaves", False, lambda state: st_has_whirlwind(state, player)],
        ["mayscore", "mayscore dovok", False, lambda state: st_has_glyph(state, player, "Ocean")],
        ["mayscore dovok", "mayscore wood", False, lambda state: st_has_whip(state, player)],
        ["mayscore", "mayscore steel", False, lambda state: st_has_cargo(state, player, "Goron Steel", "_buy_steel")],

        # # ======== Forest Sanctuary =========

        ["forest realm", "fos", False, None],
        ["fos", "fos stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["fos", "fos song statue", False, lambda state: st_has_spirit_flute(state, player)],
        ["fos", "fos chest", False, lambda state: st_has_whirlwind(state, player) or st_has_birds_song(state, player)],

        # # ======== Wooded Temple =========

        ["wtt", "wt", False, None],
        ["forest source", "wt", False, None],
        ["wt", "wt stamp station", False, lambda state: st_has_stamp_book(state, player) and (st_has_whirlwind(state, player) or st_option_hard_logic(state, player))],
        ["wt", "wt song statue", False, lambda state: st_has_spirit_flute(state, player)],
        ["wt", "wt 1f enemy chest", False, lambda state: st_has_damage(state, player)],
        ["wt 1f enemy chest", "wt 1f key", False, lambda state: st_has_whirlwind(state, player)],
        ["wt 1f enemy chest", "wt 2f enemy chest", False, None],
        ["wt 1f enemy chest", "wt 2f poison chest", False, lambda state: st_has_whirlwind(state, player) or st_option_hard_logic(state, player)],
        ["wt", "wt 1f switch chest", False, lambda state: st_has_whirlwind(state, player) or st_option_hard_logic(state, player)],
        ["wt", "wt 2f left", False, lambda state: st_can_kill_bubble(state, player) and st_has_small_keys(state, player, "Wooded Temple", 1)],
        ["wt 2f left", "wt 3f chestnut chest", False, lambda state: st_has_range(state, player) or st_has_beam_sword(state, player) or st_has_whirlwind(state, player)],
        ["wt 2f left", "wt 3f", False, lambda state: st_has_small_keys(state, player, "Wooded Temple", 2)],
        ["wt 3f", "wt 3f se chest", False, lambda state: st_has_whirlwind(state, player) or st_option_hard_logic(state, player)],
        ["wt 3f", "wt 3f bk", False, lambda state: st_has_whirlwind(state, player) or options.randomize_boss_keys == "vanilla"],
        ["wt 3f bk", "wt 4f", False, lambda state: options.randomize_boss_keys == "vanilla"],
        ["wt 3f", "wt 4f", False, lambda state: st_has_boss_key(state, player, "Wooded Temple")],
        ["wt 4f", "wt stagnox", False, lambda state: st_has_sword(state, player) and st_has_whirlwind(state, player)],
        ["wt stagnox", "goal_stagnox", False, None],
        ["wt stagnox", "event_stagnox", False, None],

        # # ============ Trading Post =============

        ["forest realm", "trading post tracks", False, lambda state: st_has_glyph(state, player, "Ocean") and st_soft_cannon(state, player)],
        ["trading post tracks", "trading post", False, None],
        ["trading post", "trading post light song statue", False, lambda state: st_has_spirit_flute(state, player)],
        ["trading post", "trading post chest", False,
         lambda state: (st_has_range(state, player) or st_has_beam_sword(state, player))
                       and st_has_discovery_song(state, player)
                       and (st_has_light_song(state, player) or st_option_hard_logic(state, player))],
        ["trading post", "trading post stamp station", False, lambda state: st_has_bombs(state, player) and st_has_stamp_book(state, player)],
        ["trading post", "trading post bridge worker", False, lambda state: st_has_passenger(state, player,"Kenzo", "_kenzo_1")],
        ["trading post bridge worker", "linebeck trading", False, lambda state: state.has("Treasure: Regal Ring", player)],
        ["trading post", "linebeck trading", False, lambda state: state.has("Treasure: Regal Ring", player) and options.randomize_passengers.value == 0],
        ["trading post", "trading post leaves", False, lambda state: st_has_whirlwind(state, player)],
        ["linebeck trading", "trading post pick up kenzo", False, lambda state: st_has_glyph(state, player, "Snow")],
        ["linebeck trading", "linebeck dark ore", False, lambda state: st_has_cargo(state, player, "Dark Ore", "_buy_ore")],
        ["linebeck trading", "linebeck event", False, None],
    ]
    overworld_logic += [
        ["snow realm fr", "rabbit haven", True, lambda state: st_has_glyph(state, player, "Snow")],
        ["rabbit haven", "rabbit haven 5 rabbits", False, lambda state: st_has_total_rabbits(state, player, 5)],
        ["rabbit haven", "rabbit haven 1 of each rabbits", False, lambda state: st_all_types_rabbits(state, player, 1)],
        ["rabbit haven", "rabbit haven 10 forest rabbits", False, lambda state: st_has_rabbit_items(state, player, "Grass")],
        ["rabbit haven", "rabbit haven 10 snow rabbits", False, lambda state: st_has_rabbit_items(state, player, "Snow")],
        ["rabbit haven", "rabbit haven 10 ocean rabbits", False, lambda state: st_has_rabbit_items(state, player, "Ocean")],
        ["rabbit haven", "rabbit haven 10 mountain rabbits", False, lambda state: st_has_rabbit_items(state, player, "Mountain")],
        ["rabbit haven", "rabbit haven 10 sand rabbits", False, lambda state: st_has_rabbit_items(state, player, "Sand")],
        ["rabbit haven", "rabbit haven 50 rabbits", False, lambda state: st_all_types_rabbits(state, player, 10)],
        ["rabbit haven", "rabbit haven mona", False, lambda state: st_has_passenger(state, player, "Mona", "_mona")],

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # # ============ Snow Realm ===============

        ["snow realm fr", "snow realm", True, lambda state: st_soft_cannon(state, player)],
        ["snow realm fr", "anouki portal", False, lambda state: st_has_cannon(state, player)],
        ["snow realm", "blizzard temple tracks", True, lambda state: st_has_temple_tracks(state, player, "Blizzard") and st_has_glyph(state, player, "Snow")],
        ["snow realm", "snow realm rabbits", False, lambda state: st_has_net(state, player)],
        ["blizzard temple tracks", "blizzard temple tracks rabbits", False, lambda state: st_has_net(state, player)],
        ["blizzard temple tracks rabbits", "snow realm blizzard rabbits", False, lambda state: st_has_source(state, player, "Snow")],
        ["blizzard temple tracks rabbits", "snow realm early blizzard rabbits", False, lambda state: st_has_source(state, player, "Snow") or st_option_hard_logic(state, player)],

        ["blizzard temple tracks rabbits", "snowdrift station rabbit", False, lambda state: st_has_misc_tracks(state, player, "Snowdrift Station")],
        ["blizzard temple tracks", "icyspring tracks", True, lambda state: st_has_misc_tracks(state, player, "N Icy Spring") and st_has_temple_tracks(state, player, "Blizzard")],
        ["icyspring tracks", "icyspring rabbits", False, lambda state: st_has_net(state, player)],
        ["icyspring tracks", "icyspring portal", False, lambda state: st_has_cannon(state, player)],

        ["blizzard temple tracks", "snow realm ferrus", False,
            lambda state: st_has_source(state, player, "Snow")
            and st_has_passenger(state, player, "Alfonzo", "_picked_up_alfonzo")],

        ["forest realm se portal track", "blizzard temple tracks", False,
         lambda state: st_has_temple_tracks(state, player, "Blizzard")
                       and st_has_portal(state, player, "Trading Post to E Snow Realm", True)],
        ["blizzard temple tracks", "forest realm se portal track", False,
         lambda state: st_has_misc_tracks(state, player, "Forest Realm SE Portal")
                       and st_has_portal(state, player, "Trading Post to E Snow Realm", False)],
        ["forest realm se portal track", "trading post portal", False, lambda state: st_has_cannon(state, player)],
        ["snow realm source", "blizzard temple tracks", True, lambda state: st_has_source(state, player, "Snow") and st_has_temple_tracks(state, player, "Blizzard")],

        # ======== Anouki Village ========

        ["snow realm", "anouki village", False, None],
        ["anouki village", "anouki village stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["anouki village", "anouki village song statue", False, lambda state: st_has_spirit_flute(state, player)],
        ["anouki village", "anouki village bomb cave chest", False, lambda state: st_has_bombs(state, player)],
        ["anouki village", "anouki village lake chest", False, lambda state: st_has_boomerang(state, player)],
        ["anouki village", "av noko", False, lambda state: st_has_temple_tracks(state, player, "Blizzard")],
        ["anouki village", "av fence", False, lambda state:
            (   st_has_passenger(state, player, "Kenzo", "_kenzo_2") or
                options.randomize_passengers == "no_passengers"
            ) and (st_has_cargo(state, player, "Lumber", "_buy_lumber") or options.randomize_cargo == "no_cargo")],
        ["anouki village", "av kenzo", False, lambda state:
            (st_has_passenger(state, player, "Kenzo", "_kenzo_2") or options.randomize_passengers == "no_passengers")
            or (st_has_cargo(state, player, "Lumber", "_buy_lumber") or options.randomize_cargo == "no_cargo")],
        ["anouki village", "av goron", False, lambda state: st_has_passenger(state, player, "Snow Goron", "_goron")],
        ["av goron", "av kofu", False, lambda state: st_has_glyph(state, player, "Fire") or st_has_source(state, player, "Fire")],

        # =========== Snow Sanctuary ==========

        ["snow realm", "ss", False, lambda state: st_has_temple_tracks(state, player, "Blizzard") or (state.has("Snowfall Sanctuary Cave Key", player) and st_has_cannon(state, player))],
        ["ss", "ss stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["ss", "ss song", False, lambda state: st_has_spirit_flute(state, player)],
        ["ss song", "steem gift", False, lambda state: st_has_source(state, player, "Snow")],
        ["ss", "steem gift", False, lambda state: st_has_source(state, player, "Snow") and options.randomize_minigames == "no_minigames"],
        ["ss", "snow sanc vessel", False, lambda state: st_has_cargo(state, player, "Vessel", "_buy_fish")],

        ## ========== Blizzard Temple =========

        ["snow realm source", "bt", True, lambda state: st_has_source(state, player, 'Snow') and st_soft_cannon(state, player)],
        ["blizzard temple tracks", "bt", True, lambda state: st_has_temple_tracks(state, player, "Blizzard")],
        ["bt", "bt b1 se", False, lambda state: st_can_ring_bell(state, player) and st_has_whirlwind(state, player)],
        ["bt b1 se", "bt b1 e enemy chest", False, None],
        ["bt b1 se", "bt b1 ne enemy chest", False, lambda state: st_can_kill_bubble(state, player)],
        ["bt b1 se", "bt 1f ne chest", False, lambda state: st_has_mid_range(state, player) or st_has_bombs(state, player)],
        ["bt 1f ne chest", "bt b1 sw chest", False, lambda state: st_has_boomerang(state, player)],
        ["bt b1 sw chest", "bt west", False, lambda state: st_has_small_keys(state, player, "Blizzard Temple", 1) and st_can_kill_freezards_torch(state, player)],
        ["bt west", "bt stamp station", False, lambda state: st_has_stamp_book(state, player)],
        ["bt west", "bt 3f", False, lambda state: st_has_boss_key(state, player, "Blizzard Temple") or options.randomize_boss_keys == "vanilla"],
        ["bt 3f", "bt fraaz", False, lambda state: st_has_sword(state, player)],
        ["bt fraaz", "goal_fraaz", False, None],
        ["bt fraaz", "event_fraaz", False, None],

        # ========== Icy Spring ==========

        ["blizzard temple tracks", "icyspring", True, lambda state: st_has_temple_tracks(state, player, "Blizzard")],
        ["icyspring", "icyspring stamp station", False, lambda state: st_has_stamp_book(state, player) and st_has_boomerang(state, player)],
        ["icyspring", "icyspring whip chest", False, lambda state: st_has_whip(state, player)],
        ["icyspring", "icyspring noko", False, lambda state: (st_has_passenger(state, player, "Noko", "_noko")
                                                              or options.randomize_passengers == "no_passengers")
                                                             and st_has_temple_tracks(state, player, "Blizzard")],  # for ferrus logic

        # ============ Snowdrift Station =========

        ["blizzard temple tracks", "snowdrift", True, lambda state: st_has_misc_tracks(state, player, "Snowdrift Station") and st_soft_cannon(state, player)],
        ["snowdrift", "snowdrift reward", False, lambda state: st_can_kill_freezards(state, player) and (
            st_has_range(state, player) or (st_has_beam_sword(state, player) and st_option_hard_logic(state, player)))],

        # ========== Slippery Station ==========
        ["blizzard temple tracks", "slippery", True,
         lambda state: st_has_misc_tracks(state, player, "Slippery Station") and st_soft_cannon(state, player)
                       and (st_has_source(state, player, 'Snow') or st_has_misc_tracks(state, player, "N Icy Spring"))],
        ["slippery", "slippery amateur", False, None],
        ["slippery", "slippery pro", False, None],
        ["slippery", "slippery champion", False, None],

        # ========== Bridge Worker's Home =======
        ["snow realm source", "bridge workers", True, lambda state: st_has_source(state, player, "Snow")],
        ["bridge workers", "bridge workers chest", False, lambda state: st_has_discovery_song(state, player)],
        ["bridge workers", "pick up bridge worker", False, lambda state: st_has_glyph(state, player, "Ocean")],

        # ========== Ocean Realm =============
        ["forest realm", "ocean realm", False, lambda state: st_has_glyph(state, player, "Ocean") and st_has_misc_tracks(state, player, "E Mayscore Bridge")],
        ["forest realm", "pirate hideout tracks", True, lambda state: st_has_misc_tracks(state, player, "Forest Realm Ocean Shortcut") and
                                                                      st_has_misc_tracks(state, player, "Pirate Hideout")],
        ["trading post tracks", "ocean realm", True, lambda state: state.has("Repair Trading Post Bridge", player)],
        ["ocean realm", "ocean temple tracks", True, lambda state: st_has_temple_tracks(state, player, "Marine")
                                                                   and st_has_glyph(state, player, "Ocean")],
        ["ocean temple tracks", "ocean realm source", True, lambda state: st_has_source(state, player, "Ocean")
                                                                          and st_has_temple_tracks(state, player, "Marine")],
        ["ocean realm", "pirate hideout tracks", True, lambda state: st_has_misc_tracks(state, player, "Pirate Hideout") and
                                                                     st_has_glyph(state, player, "Ocean")],
        ["ocean realm source", "pirate hideout tracks", True, lambda state: st_has_source(state, player, "Ocean")
                                                                            and st_has_misc_tracks(state, player, "Pirate Hideout")],
        ["ocean temple tracks", "oct", True, lambda state: st_has_temple_tracks(state, player, "Marine")],
        ["ocean realm source", "oct", True, lambda state: st_has_source(state, player, "Ocean")],
        ["ocean realm source", "ocean portal tracks", True, lambda state: st_has_source(state, player, "Ocean") and st_has_misc_tracks(state, player, "Ocean Portal")],
        ["ocean temple tracks", "ocean portal tracks", True, lambda state: (
            st_has_temple_tracks(state, player, "Marine") and
            st_has_misc_tracks(state, player, "Ocean Portal"))],
        ["ocean portal tracks", "sand realm", False, lambda state: st_has_misc_tracks(state, player, "Sand Realm") and st_has_misc_tracks(state, player, "Ocean Portal")],
        ["ocean portal tracks", "ocean portal", False, lambda state: st_has_cannon(state, player)],

        # Ocean Portals
        ["trading post tracks", "ocean portal tracks", False,
         lambda state: st_has_misc_tracks(state, player, "Ocean Portal") and st_has_portal(state, player, "Mayscore to Ocean Portal Tracks", False)],
        ["ocean portal tracks", "trading post tracks", False,
         lambda state: st_has_glyph(state, player, "Ocean")
                       and st_has_portal(state, player,"Mayscore to Ocean Portal Tracks",True)],
        ["snow bridge", "ocean temple tracks", False,
         lambda state: st_has_temple_tracks(state, player, "Marine")
                       and st_has_portal(state, player,"Snow Bridge to Island Sanctuary",True)],
        ["ocean temple tracks", "snow bridge", False,
         lambda state: st_has_misc_tracks(state, player, "Snow Realm Bridge")
                       and st_has_portal(state, player,"Snow Bridge to Island Sanctuary",False)],

        # Ocean Rabbits
        ["ocean temple tracks", "ocean rabbits", False, lambda state: st_has_net(state, player)],
        ["las tracks", "las rabbit", False, lambda state: st_has_net(state, player)],
        ["ocean realm source", "ocean source rabbits", False, lambda state: st_has_net(state, player)],
        ["ocean portal tracks", "ocean portal rabbits", False, lambda state: st_has_net(state, player)],
        ["forest ocean shortcut rabbit", "pirate rabbit", False, None],

        # ========== Island Sanctuary =============
        ["ocean realm", "ocs", False, None],
        ["ocs", "ocs north", False, lambda state: st_has_boomerang(state, player)
                                                  or (st_has_birds_song(state, player) and st_has_whip(state, player) and st_option_hard_logic(state, player))], # Spreadsheet shows Whirlwind needed too,
                                                                                  # but not sure why looking at walkthrough
                                                                                  # probably wants you to whirlwind a bomb in the cave, but you can make the throw.
        ["ocs north", "ocs stamp station", False, lambda state: st_has_stamp_book(state, player)
                                                         and st_has_birds_song(state, player) and st_has_whip(state, player)],

        ["ocs", "ocs S island chest", False, lambda state: st_hard_birds(state, player)],  # borderline if it should count as hard logic
        ["ocs north", "ocs nw chest", False, lambda state: st_hard_birds(state, player)],
        ["ocs north", "ocs song", False, lambda state: st_has_spirit_flute(state, player)]
            if options.randomize_passengers == "no_passengers" else
        ["ocs carben", "ocs song", False, lambda state: st_has_spirit_flute(state, player)
                                                        and (st_has_boomerang(state, player)
                                                             or (st_has_birds_song(state, player) and st_has_whip(state, player) and st_option_hard_logic(state, player)))],
        ["ocs", "ocs carben", False, lambda state: st_has_passenger(state, player, "Carben", "_carben")
                                                   and (options.randomize_passengers.value != 1
                                                        or st_has_sword(state, player)  # Fight off the blins
                                                        or st_has_whip(state, player)
                                                        or st_has_temple_tracks(state, player, "Marine")  # or go around
                                                        or state.has("_UT_Glitched_Logic", player))],  # or train speed past

        # ========== Papuchia Village =============
        ["ocean realm", "papuchia village", False, None],
        ["papuchia village", "papuchia village song statue", False, lambda state: st_has_discovery_song(state, player)],
        ["papuchia village", "pv dovok", False, lambda state: st_has_passenger(state, player, "Dovok", "_dovok")],
        ["papuchia village south", "papuchia village stamp station", False, lambda state: st_has_stamp_book(state, player) and st_has_birds_song(state, player)],

        ["papuchia village", "pv carben", False, lambda state: st_has_discovery_song(state, player)],
        ["papuchia village", "pv wadatsumi", False, lambda state: st_has_passenger(state, player, "Wadatsumi", "_wadatsumi")],
        ["papuchia village song statue", "papuchia village south", False, lambda state: st_hard_birds(state, player)],  # You need a warp to start to return without bird song, patched with a dynaentrance
        # I don't like that this is locked behind song statue, but flags might not let us get there earlier

        ["papuchia village", "papuzia ice", False, lambda state: st_has_cargo(state, player, "Mega Ice", "_buy_ice")]
        if options.randomize_cargo.value in [1, 2] else
        ["papuchia village", "papuzia ice", False, lambda state: state.has("Wagon", player) and (state.has("Cargo: Mega Ice", player, 3)
                                                                 or (state.has("Cargo: Mega Ice", player, 1) and state.has("_UT_Glitched_Logic", player)))],

        # ========= Marine Temple ==================
        ["oct", "oct song statue", False, lambda state: st_has_spirit_flute(state, player)],
        ["oct 2f", "oct whip chest", False, lambda state: st_has_sword(state, player)], # you can't escape stunlock without sword, and the fight scripts you into it from the start
        ["oct", "oct whip", False, lambda state: st_has_whip(state, player)],
        ["oct", "oct 2f", None, lambda state: any([
            st_has_whip(state, player),
            st_can_hit_switches(state, player),
            st_option_hard_logic(state, player)  # damageboost through the boulders
        ])],
        ["oct", "oct stamp station", False, lambda state: st_has_stamp_book(state, player) and st_has_whip(state, player) and st_has_bombs(state, player) and st_has_boomerang(state, player)],
        ["oct whip chest", "oct 3f whip", False, lambda state: st_has_whip(state, player)],
        ["oct 3f whip", "oct 6f chest", False, lambda state: st_has_small_keys(state, player, "Marine Temple", 1)],
        ["oct 6f chest", "oct bk", False, lambda state: st_has_small_keys(state, player, "Marine Temple", 2) or
         all([st_option_glitched_logic(state, player), st_has_whirlwind(state, player), st_has_bombs(state, player)])],
        ["oct 6f chest", "oct bk loc", False, lambda state: st_has_whirlwind(state, player) and options.randomize_boss_keys.value > 0 and st_option_hard_logic(state, player)],
        ["oct bk", "oct bk loc", False, None],
        ["oct bk", "oct phytops", False, lambda state: options.randomize_boss_keys == "vanilla"],
        ["oct 6f chest", "oct phytops", False, lambda state: st_has_boss_key(state, player, "Marine Temple")],
        ["oct phytops", "event_phytops", False, None],
        ["oct phytops", "goal_phytops", False, None],

        ["oct", "oct ferrus", False,
         lambda state: st_has_passenger(state, player, "Ferrus", "_ferrus_2")
                       and (options.randomize_passengers.value > 1
                            or st_option_hard_logic(state, player)
                            or state.has("_ferrus_backup", player))
         ],  # If you fail the train journey in vanilla, make sure you have access to icyspring for backup.

        # ========= Pirate Hideout ==============
        ["pirate hideout tracks", "pirate hideout", False, None],
        ["pirate hideout", "pirate hideout stamp station", False, lambda state: st_has_stamp_book(state, player)
                                                                                and st_has_whip(state, player) and st_has_birds_song(state, player)],
        ["pirate hideout", "pirate hideout secret cave", False, lambda state: st_has_bombs(state, player)],
        ["pirate hideout", "pirate hideout minigame", False, lambda state: st_has_bow(state, player)],
        # Wadatsumi able to be reached with only tracks with minigames turned off, otherwise requires bow
        ["pirate hideout", "pirate wadatsumi", False, lambda state: st_has_glyph(state, player, "Ocean")]
            if options.randomize_minigames.value in [0] else
        ["pirate hideout", "pirate wadatsumi", False, lambda state: st_has_bow(state, player) and st_has_glyph(state, player, "Ocean")],
        # First hideout minigame gives you bow automatically, and then it shows in top right, even with no items, but doesn't let you use it. With an item, it doesn't show

        # ======== Lost at Sea Station ==========
        ["ocean temple tracks", "las tracks", True, lambda state: st_has_temple_tracks(state, player, "Marine")
                                                    and st_has_misc_tracks(state, player,"Lost at Sea Station")],
        ["las tracks", "lost at sea", True, lambda state: st_has_misc_tracks(state, player, "Lost at Sea Station")],
        ["lost at sea", "las outside chest", False, lambda state: st_has_discovery_song(state, player) and (st_has_light_song(state, player) or st_option_hard_logic(state, player))],
        ["lost at sea", "las 1st room chest", False, lambda state: st_has_awakening_song(state, player) and st_hard_birds(state, player)],
        ["las 1st room chest", "las 2nd room chest", False, lambda state: st_has_boomerang(state, player)],
        ["las 2nd room chest", "las 3rd room chest", False, lambda state: st_has_whirlwind(state, player)],
        ["las 3rd room chest", "las 4th room chest", False, lambda state: st_has_whip(state, player)],
        ["las 4th room chest", "las 5th room", False, lambda state: st_has_bombs(state, player) or st_option_hard_logic(state, player)],
        ["las 5th room", "las_event", False, None],

        # ===== Fire Realm =====
        ["blizzard temple tracks", "fire realm", True, lambda state: st_has_glyph(state, player, "Fire") and st_has_temple_tracks(state, player, "Blizzard")],
        ["blizzard temple tracks", "gorge tracks", True, lambda state: st_has_misc_tracks(state, player, "Snow Realm Gorge") and st_has_temple_tracks(state, player, "Blizzard")],
        ["gorge tracks", "fire realm", True, lambda state: st_has_glyph(state, player, "Fire") and st_has_misc_tracks(state, player, "Snow Realm Gorge")],
        ["fire realm", "fire source", True, lambda state: st_has_glyph(state, player, "Fire") and st_has_source(state, player, "Fire")],
        ["mountain temple tracks", "fire source", True, lambda state: st_has_temple_tracks(state, player, "Mountain") and st_has_source(state, player, "Fire")],
        ["mountain temple tracks", "fire realm", True, lambda state: st_has_temple_tracks(state, player, "Mountain") and st_has_glyph(state, player, "Fire")],
        ["mountain temple tracks", "ends of the earth", True, lambda state: st_has_temple_tracks(state, player, "Mountain") and st_has_misc_tracks(state, player, "Ends of the Earth")],
        ["mountain temple tracks", "disorientation station", True, lambda state: st_has_temple_tracks(state, player, "Mountain") and st_has_misc_tracks(state, player,"Disorientation Station")],
        ["fire realm", "disorientation station", True, lambda state: st_has_glyph(state, player, "Fire") and st_has_misc_tracks(state, player,"Disorientation Station")],
        ["fire realm", "sand connection", True, lambda state: st_has_glyph(state, player, "Fire") and st_has_misc_tracks(state, player,"Fire Realm Sand Portal")],
        ["mountain temple tracks", "dark ore mine", True, lambda state: st_has_temple_tracks(state, player, "Mountain") and st_has_misc_tracks(state, player,"Dark Ore Mine")],
        ["mountain temple tracks", "snurglars", True, lambda state: st_has_cannon(state, player)],
        ["fire realm", "fire realm ferrus", False, lambda state: st_has_temple_tracks(state, player, "Marine")],
        ["fire realm ferrus", "icyspring", False, lambda state: options.randomize_passengers == "vanilla" and state.has("_UT_Glitched_Logic", player)],

        ["fire realm", "fire realm rabbits", False, lambda state: st_has_net(state, player)],
        ["mountain temple tracks", "mountain rabbits", False, lambda state: st_has_net(state, player)],
        ["fire source", "fire source rabbits", False, lambda state: st_has_net(state, player)],
        ["disorientation station", "disorientation rabbits", False, lambda state: st_has_net(state, player)],
        ["fire realm", "disorientation rabbits", False, lambda state: st_has_net(state, player)],
        ["ends of the earth", "eote rabbits", False, lambda state: st_has_net(state, player)],
        ["fire source", "s mountain temple rabbit", False, lambda state: st_has_net(state, player)],
        ["mountain temple tracks", "s mountain temple rabbit", False, lambda state: st_has_net(state, player)],

        ["fire realm", "forest cave tracks", False, lambda state: st_has_misc_tracks(state, player,"Forest Realm SW Cave") and st_has_portal(state, player, "Forest Cave to Goron Village", False)],
        ["forest cave tracks", "fire realm", False, lambda state: st_has_glyph(state, player, "Fire") and st_has_portal(state, player,"Forest Cave to Goron Village",True)],
        ["mountain temple tracks", "icyspring tracks", False, lambda state: st_has_misc_tracks(state, player,"N Icy Spring") and st_has_portal(state, player,"Icy Spring to Mountain Temple",False)],
        ["icyspring tracks", "mountain temple tracks", False, lambda state: st_has_temple_tracks(state, player, "Mountain") and st_has_portal(state, player,"Icy Spring to Mountain Temple",True)],

        # Goron Village
        ["fire realm", "goron village", False, None],
        ["fire source", "goron village", False, None],
        ["goron village", "goron whip", False, lambda state: st_has_whip(state, player)],
        ["goron whip", "goron village stamp", False, lambda state: st_has_stamp_book(state, player)],
        ["goron ice event", "valley sanc tunnel", False, lambda state: st_has_whip(state, player)],
        ["valley sanc tunnel", "valley sanc", False, lambda state: st_has_boomerang(state, player)],
        ["valley sanc", "valley sanc stamp", False, lambda state: st_has_stamp_book(state, player)],
        ["valley sanc", "valley sanc song", False, lambda state: st_has_light_song(state, player)],
        ["goron ice event", "pick up gorons", False, lambda state: st_has_glyph(state, player, "Snow")],
        ["goron ice event", "gv kofu", False, lambda state: st_has_passenger(state, player, "Kofu", "_kofu")],

        ["goron village", "goron ice", False, None] if options.randomize_cargo == "no_cargo" else (
            ["goron whip", "goron ice", False, lambda state: st_has_cargo(state, player, "Mega Ice", "_buy_ice")]
            if options.randomize_cargo.value in [1, 2] else
            ["goron whip", "goron ice", False, lambda state: state.has("Wagon", 1) and (
                state.has("Cargo: Mega Ice", player, 2)
                or (state.has("Cargo: Mega Ice", player, 1) and state.has("_UT_Glitched_Logic", player)))]
        ),
    ]
    # print(f"CARGO LOGIC {options.randomize_cargo.value} {overworld_logic[-1]}")
    overworld_logic += [
        ["goron ice", "goron ice event", False, None],
        ["goron ice event", "goron ice 2", False, None] if options.randomize_cargo.value in [0, 1, 2] else
        ["goron ice event", "goron ice 2", False, lambda state: state.has("Wagon", 1) and (
                state.has("Cargo: Mega Ice", player, 3) or (
                    state.has("Cargo: Mega Ice", player, 2) and state.has("_UT_Glitched_Logic", player)))],

        # Goron Target Game
        ["fire realm", "gtr", False, lambda state: st_has_cannon(state, player) and state.has("_goron_ice", player) and st_has_rupees(state, player, 50)],

        # Mountain Temple
        ["mountain temple tracks", "mountain temple door", False, None],
        ["fire source", "mountain temple door", False, None],
        ["mountain temple door", "mtt", False, lambda state: state.has("Mountain Temple Snurglar Key", player, 3) or state.has("Snurglar Keyring", player)],
        ["mtt", "mtt song statue", False, lambda state: st_has_spirit_flute(state, player)],
        ["mtt", "mtt left", False, lambda state: st_has_damage(state, player)],
        ["mtt left", "mtt right", False, lambda state: st_has_range(state, player) or st_has_bombs(state, player)],
        ["mtt left", "mtt 2f right", False, lambda state: st_has_range(state, player) or st_has_sword(state, player) or st_has_whip(state, player)],
        ["mtt", "mtt center", False, lambda state: st_mtt_center(state, player)],
        ["mtt center", "mtt heatoise", False, lambda state: st_has_good_damage(state, player)],
        ["mtt heatoise", "mtt 1f ne", False, lambda state: st_has_bow(state, player)],
        ["mtt 1f ne", "mtt b1", False, lambda state: st_can_rotate_repeater(state, player)],
        ["mtt b1", "mtt b2", False, lambda state: st_has_whip(state, player)],
        ["mtt b2", "mtt b1 arena", False, lambda state: st_has_boomerang(state, player)],
        ["mtt b1", "mtt b1 cart", False, lambda state: st_has_small_keys(state, player, "Mountain Temple", 3, 1)],
        # ["mtt b1 cart", "mtt b1 arena", False, None],  # Removed!
        ["mtt b1 cart", "mtt stamp", False, lambda state: st_has_stamp_book(state, player)],
        ["mtt b1 cart", "mtt bk", False, lambda state: st_has_whirlwind(state, player)],
        ["mtt bk", "mtt boss", False, lambda state: options.randomize_boss_keys == "vanilla"],
        ["mtt b1 cart", "mtt boss", False, lambda state: st_has_boss_key(state, player, "Mountain Temple") and any([
            st_has_sword(state, player),
            st_has_whip(state, player),
            state.has("Bombs (Progressive)", player, 2)
        ])],
        ["mtt boss", "event_vulcano", False, None],
        ["mtt boss", "goal_vulcano", False, None],

        # Disorientation Station
        ["disorientation station", "disorientation bird", False, lambda state: st_hard_birds(state, player)],
        ["disorientation bird", "disorientation sod", False, lambda state: st_has_discovery_song(state, player)],

        # Ends of the Earth
        ["ends of the earth", "eote puzzles", False, lambda state: st_has_sand_wand(state, player)],

        # ===== Sand Realm =====
        ["ocean realm source", "sand realm", True, lambda state: st_has_source(state, player, "Ocean") and st_has_misc_tracks(state, player, "Sand Realm")],
        ["sand realm", "sand restoration", False, lambda state: st_has_temple_tracks(state, player, "Desert") and st_has_misc_tracks(state, player, "Sand Realm") and st_has_cannon(state, player)],
        ["sand realm", "sand connection", True, lambda state: st_has_misc_tracks(state, player, "Sand Realm") and st_has_misc_tracks(state, player, "Fire Realm Sand Portal")],

        ["sand realm", "sand realm rabbits", False, lambda state: st_has_net(state, player)],
        ["sand restoration", "sand restoration rabbits", False, lambda state: st_has_net(state, player)],
        ["sand connection", "sand connection rabbit", False, lambda state: st_has_net(state, player)],

        ["sand restoration", "sand restoration portal", True, lambda state: st_has_cannon(state, player)],
        ["sand connection", "sand connection portal", True, lambda state: st_has_cannon(state, player)],
        ["sand realm", "sand realm portal", True, None],
        ["sand restoration", "sand realm portal", False, lambda state: st_has_portal(state, player, "Desert Temple to Sand Realm", True) and st_has_misc_tracks(state, player, "Sand Realm")],
        ["sand realm portal", "sand restoration", False, lambda state: st_has_portal(state, player, "Desert Temple to Sand Realm", False) and st_has_temple_tracks(state, player, "Desert")],
        ["sand connection", "ocean temple tracks", False, lambda state: st_has_portal(state, player, "Sand Valley to Marine Temple", True) and st_has_temple_tracks(state, player, "Marine")],
        ["ocean temple tracks", "sand connection", False, lambda state: st_has_portal(state, player, "Sand Valley to Marine Temple",False) and st_has_misc_tracks(state, player, "Fire Realm Sand Portal")],

        # ===== Sand Sanc =====
        ["sand realm", "sand sanc", False, None],
        ["sand sanc", "sand sanc song", False, lambda state: st_has_spirit_flute(state, player)],
        ["sand sanc cuccos", "sand sanc stamp stand", False, lambda state: st_has_stamp_book(state, player)],
        ["sand sanc", "sand sanc cuccos", False, None] if options.randomize_cargo.value == 0
        else (
            ["sand sanc", "sand sanc cuccos", False, lambda state: st_has_cargo(state, player, "Cuccos", "_buy_cuccos")]
            if options.randomize_cargo.value in [1, 2] else
            ["sand sanc", "sand sanc cuccos", False, lambda state: state.has("Wagon", player) and (state.has("Cargo: Cuccos (5)", player, 3)
                or (state.has("Cargo: Cuccos (5)", player, 1) and state.has("_UT_Glitched_Logic", player)))]
        ),


        # ===== Desert Temple =====
        ["sand restoration", "desert temple", False, lambda state: st_has_cannon(state, player)],
        ["desert temple", "dt sw", False, lambda state: st_has_sand_wand(state, player)],
        ["dt sw", "dt 1f nw", False, lambda state: st_has_bow(state, player)],
        ["desert temple", "dt 1f n", False, lambda state: st_has_bow(state, player)],

        ["dt sw", "dt 1f n earthquake", False, lambda state: st_has_bow(state, player)],

        ["desert temple", "dt 2f", False, lambda state: st_desert_temple_keys(state, player)],
        ["dt 2f", "dt 2f sw", False, lambda state: st_has_sand_wand(state, player)],
        ["dt 2f", "dt 3f", False, lambda state: st_has_damage(state, player)],

        ["dt sw", "dt b1", False, lambda state: st_desert_temple_keys(state, player)],
        ["dt b1", "dt stamp stand", False, lambda state: st_has_stamp_book(state, player)],
        ["dt b1", "dt b1 2", False, lambda state: st_has_range(state, player) or st_has_bombs(state, player)],
        ["dt b1 2", "dt b1 damage", False, lambda state: st_has_damage(state, player)],
        ["dt b1", "dt b2", False, lambda state: st_option_glitched_logic(state, player) and st_has_bombs(state, player) and st_has_sword(state, player)],

        # ["dt b1 2", "dt b2", False, lambda state: st_has_boss_key(state, player, "Desert Temple")],
        ["dt b1 damage", "dt b2", False, None]
            if options.randomize_boss_keys == "vanilla"
            else ["dt b1 2", "dt b2", False, lambda state: st_has_boss_key(state, player, "Desert Temple")],
        ["dt b2", "skeldritch", False, lambda state: st_has_good_damage(state, player)], # Whip is not good enough damage
        ["skeldritch", "skeldritch event", False, None],
        ["skeldritch", "skeldritch goal", False, None],

        # ===== Dark ore mine =====
        ["sand restoration", "dark ore mine", False, lambda state: st_has_misc_tracks(state, player, "Dark Ore Mine") and st_soft_cannon(state, player)],
        ["dark ore mine", "sand restoration", False, lambda state: st_has_temple_tracks(state, player, "Desert") and st_has_cannon(state, player)],
        ["dark ore mine", "dark ore mine sod", False, lambda state: st_has_discovery_song(state, player)],

        # ===== Dark Realm =====
        ["dark realm portal", "dark realm trains", False, lambda state: st_has_dungeon_rewards(state, player)],
        ["dark realm trains", "demon train", False, None],
        ["dark realm trains", "malladus goal", False, lambda state: options.endgame_scope == "enter_dark_realm"],
        ["dark realm trains", "dark realm event", False, lambda state: options.endgame_scope == "enter_dark_realm"],
        ["demon train", "cole fight", False, lambda state: st_has_cannon(state, player)],
        ["cole fight", "malladus 1", False, lambda state: st_can_fight_malladus(state, player)],
        ["malladus 1", "malladus 2", False, lambda state: st_has_spirit_flute(state, player) and st_has_sword(state, player)],
        ["malladus 2", "malladus goal", False, lambda state: st_can_fight_malladus(state, player)],
        # ["dark realm portal", "malladus goal", False, None],
        ["malladus 2", "malladus event", False, lambda state: st_can_fight_malladus(state, player)],

        ["forest realm", "beedle", False, lambda state: st_has_source(state, player, "Snow")],
        ["beedle", "beedle joe", False, lambda state: st_has_passenger(state, player, "Joe", "_joe")],
    ]

    required_rupees = 0
    if "uniques" in options.shopsanity.value: required_rupees += 4500
    if "treasure" in options.shopsanity.value: required_rupees += 2400
    if "potions" in options.shopsanity.value: required_rupees += 1400
    if "shields" in options.shopsanity.value: required_rupees += 610
    if "postcards" in options.shopsanity.value: required_rupees += 500
    if "ammo" in options.shopsanity.value: required_rupees += 500
    if options.randomize_cargo == "vanilla": required_rupees += 650
    elif options.randomize_cargo: required_rupees += 550

    overworld_logic += [
        # Shops
        ["ss", "snow sanc shop", False, lambda state: st_has_rupees(state, player, required_rupees)],

        ["beedle", "beedle shop", False, lambda state: st_has_rupees(state, player, required_rupees)],
        ["beedle shop", "beedle shop bombs", False, lambda state: st_has_bombs(state, player)],

        ["mayscore", "mayscore shop", False, lambda state: st_has_rupees(state, player, required_rupees)],
        ["castle town", "castle town shop", False, lambda state: st_has_rupees(state, player, required_rupees)],
        ["papuchia village", "papuzia shop", False, lambda state: st_has_rupees(state, player, required_rupees)],
        ["papuzia shop", "papuzia shop arrows", False, lambda state: st_has_bow(state, player)],
        ["papuzia shop", "papuzia shop bombs", False, lambda state: st_has_bombs(state, player)],
        ["trading post", "trading post shield", False, lambda state: st_has_rupees(state, player, required_rupees)],
        ["goron village", "goron shop", False, lambda state: st_has_rupees(state, player, required_rupees)],
        ["goron shop", "goron shop bombs", False, lambda state: st_has_bombs(state, player)],
        ["goron shop", "goron shop bow", False, lambda state: st_has_bow(state, player)],

        ["castle town", "castle town buy cuccos", False, lambda state: st_has_wagon(state, player) and st_has_rupees(state, player, required_rupees)],
        ["mayscore", "mayscore lumber", False, lambda state: st_has_wagon(state, player) and st_has_rupees(state, player, required_rupees)],
        ["icyspring noko", "icyspring ice", False, lambda state: st_has_wagon(state, player)]
            if options.randomize_cargo in [2, 3] else
        ["icyspring noko", "icyspring ice", False, lambda state: st_has_wagon(state, player) and st_has_rupees(state, player, required_rupees)], #  You can bully noko for free ice
        ["papuchia village", "papuzia buy cargo", False, lambda state: st_has_wagon(state, player) and st_has_rupees(state, player, required_rupees)],
        ["goron ice event", "goron steel", False, lambda state: st_has_wagon(state, player) and st_has_rupees(state, player, required_rupees)],
        ["dark ore mine", "dark ore mine ore", False, lambda state: st_has_wagon(state, player) and st_has_rupees(state, player, required_rupees)],
    ]

    # Generate rabbit total items
    if options.rabbitsanity in ["on_total", "both"]:
        # print(f"Creating total rabbit logic")
        # overworld_logic += [  silly lambda instancing
        #     [f"{realm.lower()} realm rabbits", f"{realm} Rabbit Count {i}", False,
        #      lambda state: st_caught_rabbits(state, player, realm, i)] for i in range(1, 11)
        #     for realm in ["Forest", "Snow"]
        # ]
        overworld_logic += [
            ["forest realm rabbits", "Grass Rabbit Count 1", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 1)],
            ["forest realm rabbits", "Grass Rabbit Count 2", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 2)],
            ["forest realm rabbits", "Grass Rabbit Count 3", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 3)],
            ["forest realm rabbits", "Grass Rabbit Count 4", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 4)],
            ["forest realm rabbits", "Grass Rabbit Count 5", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 5)],
            ["forest realm rabbits", "Grass Rabbit Count 6", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 6)],
            ["forest realm rabbits", "Grass Rabbit Count 7", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 7)],
            ["forest realm rabbits", "Grass Rabbit Count 8", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 8)],
            ["forest realm rabbits", "Grass Rabbit Count 9", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 9)],
            ["forest realm rabbits", "Grass Rabbit Count 10", False,
             lambda state: st_caught_rabbits(state, player, "Grass", 10)],

            ["forest realm rabbits", "Snow Rabbit Count 1", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 1)],
            ["forest realm rabbits", "Snow Rabbit Count 2", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 2)],
            ["forest realm rabbits", "Snow Rabbit Count 3", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 3)],
            ["forest realm rabbits", "Snow Rabbit Count 4", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 4)],
            ["forest realm rabbits", "Snow Rabbit Count 5", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 5)],
            ["forest realm rabbits", "Snow Rabbit Count 6", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 6)],
            ["forest realm rabbits", "Snow Rabbit Count 7", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 7)],
            ["forest realm rabbits", "Snow Rabbit Count 8", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 8)],
            ["forest realm rabbits", "Snow Rabbit Count 9", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 9)],
            ["forest realm rabbits", "Snow Rabbit Count 10", False,
             lambda state: st_caught_rabbits(state, player, "Snow", 10)],

            ["forest realm rabbits", "Ocean Rabbit Count 1", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 1)],
            ["forest realm rabbits", "Ocean Rabbit Count 2", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 2)],
            ["forest realm rabbits", "Ocean Rabbit Count 3", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 3)],
            ["forest realm rabbits", "Ocean Rabbit Count 4", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 4)],
            ["forest realm rabbits", "Ocean Rabbit Count 5", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 5)],
            ["forest realm rabbits", "Ocean Rabbit Count 6", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 6)],
            ["forest realm rabbits", "Ocean Rabbit Count 7", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 7)],
            ["forest realm rabbits", "Ocean Rabbit Count 8", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 8)],
            ["forest realm rabbits", "Ocean Rabbit Count 9", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 9)],
            ["forest realm rabbits", "Ocean Rabbit Count 10", False,
             lambda state: st_caught_rabbits(state, player, "Ocean", 10)],

            ["forest realm rabbits", "Mountain Rabbit Count 1", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 1)],
            ["forest realm rabbits", "Mountain Rabbit Count 2", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 2)],
            ["forest realm rabbits", "Mountain Rabbit Count 3", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 3)],
            ["forest realm rabbits", "Mountain Rabbit Count 4", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 4)],
            ["forest realm rabbits", "Mountain Rabbit Count 5", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 5)],
            ["forest realm rabbits", "Mountain Rabbit Count 6", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 6)],
            ["forest realm rabbits", "Mountain Rabbit Count 7", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 7)],
            ["forest realm rabbits", "Mountain Rabbit Count 8", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 8)],
            ["forest realm rabbits", "Mountain Rabbit Count 9", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 9)],
            ["forest realm rabbits", "Mountain Rabbit Count 10", False,
             lambda state: st_caught_rabbits(state, player, "Mountain", 10)],

            ["forest realm rabbits", "Sand Rabbit Count 1", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 1)],
            ["forest realm rabbits", "Sand Rabbit Count 2", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 2)],
            ["forest realm rabbits", "Sand Rabbit Count 3", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 3)],
            ["forest realm rabbits", "Sand Rabbit Count 4", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 4)],
            ["forest realm rabbits", "Sand Rabbit Count 5", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 5)],
            ["forest realm rabbits", "Sand Rabbit Count 6", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 6)],
            ["forest realm rabbits", "Sand Rabbit Count 7", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 7)],
            ["forest realm rabbits", "Sand Rabbit Count 8", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 8)],
            ["forest realm rabbits", "Sand Rabbit Count 9", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 9)],
            ["forest realm rabbits", "Sand Rabbit Count 10", False,
             lambda state: st_caught_rabbits(state, player, "Sand", 10)],
        ]

    return overworld_logic


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name

def create_connections(world: "SpiritTracksWorld", player: int, origin_name: str, options):
    all_logic = [
        make_overworld_logic(player, origin_name, options)
    ]
    entrance_lookup = {(e.entrance_region, e.exit_region): e for e in ENTRANCES.values()}
    world.multiworld.completion_condition[player] = lambda state: state.has("_beaten_game", player)

    def create_entrance(r1: "Region", r2: "Region", rule_):
        entrance_data: "STTransition" or None = entrance_lookup.get((r1.name, r2.name), None)
        name = entrance_data.name if entrance_data else None

        if rule_ is not None:
            entrance = r1.connect(r2, name, rule_)
        else:
            entrance = r1.connect(r2, name)
            # print(f"Setting rule {rule_}")
            # world.set_rule(entrance, rule_)

        if entrance_data:
            # print(f"Creating connection {r1} -> {r2} | {entrance_data.name}")
            rando_type_bool = entrance_data.two_way
            entrance.randomization_type = EntranceType.TWO_WAY if rando_type_bool else EntranceType.ONE_WAY
            entrance.randomization_group = entrance_data.direction | entrance_data.category_group | entrance_data.island
            world.valid_entrances.append(entrance)

    # Create connections
    for logic_array in all_logic:
        for reg1, reg2, is_two_way, rule in logic_array:
            region_1 = world.get_region(reg1)
            region_2 = world.get_region(reg2)

            create_entrance(region_1, region_2, rule)
            if is_two_way:
                create_entrance(region_2, region_1, rule)
