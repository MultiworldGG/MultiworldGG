from BaseClasses import MultiWorld, Item, EntranceType, Entrance
from .data.Rules import *
from .data.Entrances import ENTRANCES
from .Subclasses import STTransition


def make_overworld_logic(player: int, origin_name: str, world):
    tower_section_lookup = world.tower_section_lookup

    def get_portal_logic(r1, pr1, r2, pr2, t1, t2, pi, event):
        return (
            [pr1, pr2, False, has_tracks(t1) & has_portal(pi, True, event)],
            [pr2, pr1, False, has_tracks(t2) & has_portal(pi, False, event)],
            [r1, pr1, False, has_portal(pi, True, event)],
            [r2, pr2, False, has_portal(pi, False, event)],
            [pr1, r1, False, has_tracks(t1) & has_portal(pi, False, event, True)],
            [pr2, r2, False, has_tracks(t2) & has_portal(pi, False, event, True)]
        )

    overworld_logic: list[list] = [

        # ====== Outset Village ==============
        # ["menu", "niko's house", False, None],
        #[region 1, region 2, two-directional, logic requirements],
        ["outset village", "outset station", False, None],
        ["outset station", "outset village", False, has_glyph("Forest")],
        ["outset station", "forest realm", True, has_train & has_glyph("Forest")],

        ["outset village", "niko's house", True, None],
        ["outset village", "mary's house", True, None],
        ["outset village", "train workshop", True, None],

        ["niko's house", "niko's stamp book", False, has_passenger("Alfonzo" ,"_picked_up_alfonzo")
         | Filtered(has_glyph("Snow"), options=[OptionFilter(SpiritTracksRandomizePassengers, 0)])],
        ["niko's stamp book", "outset 10 stamps", False, Has("Stamp", 10)],
        ["niko's stamp book", "outset 15 stamps", False, Has("Stamp", 15)],
        ["niko's stamp book", "outset 20 stamps", False, Has("Stamp", 20)],
        ["outset village", "outset stamp station", False, has_stamp_book],
        ["outset stamp station", "outset stamp event", False, has_stamp_book],
        ["outset village", "outset village trees", False, has_sod],
        ["outset village", "outset joe", False, has_source("Snow")],
        ["outset village", "outset cuccos", False, has_cargo("Cuccos", "_buy_cuccos")]
            if world.options.randomize_cargo.value in [1, 2] else
        ["outset village", "outset cuccos", False, has_wagon & (
                Has("Cargo: Cuccos (5)", 3) | (
                    Has("Cargo: Cuccos (5)", 2) & ool))],
        ["outset village", "delivered ferrus", False, has_passenger("Alfonzo", "_picked_up_alfonzo")
            & has_passenger("Ferrus", "_ferrus_1")],
        ["delivered ferrus", "outset delivered ferrus event", False, None],
        ["train workshop", "outset ferrus", None, Has("_delivered_ferrus")],
        ["outset village", "visit outset", False, None],

        # ========= Forest Realm ==========

        ["forest realm", "forest realm se portal track", True, has_tracks("Forest Realm SE Portal") & has_glyph("Forest")],
        ["forest realm", "wtt", True, has_temple_tracks("Wooded") & has_glyph("Forest")],
        ["forest realm", "forest source", True, has_source("Forest") & has_glyph("Forest")],
        ["forest realm", "w castle town tracks", True, has_tracks("W Castle Town") & has_glyph("Forest")],
        ["forest realm", "n castle town tracks", True, has_tracks("N Castle Town") & has_glyph("Forest")],
        ["wtt", "snow realm fr", True, has_temple_tracks("Wooded") & has_glyph("Snow")],
        ["wtt", "w castle town tracks", True, has_tracks("W Castle Town") & has_source("Forest")],

        ["forest realm n portal", "snow realm south portal", False, has_portal("Hyrule Castle to Anouki Village", False, "_sr_portal") & has_glyph("Forest")],
        ["snow realm south portal", "forest realm n portal", False, has_portal("Hyrule Castle to Anouki Village", True, "_sr_portal") & has_glyph("Snow")],
        ["forest realm n portal", "forest realm", False, has_portal("Hyrule Castle to Anouki Village", False, "_sr_portal", True) & has_glyph("Forest")],
        ["forest realm", "forest realm n portal", False, None],
        ["snow realm south", "snow realm south portal", False, None],
        ["snow realm", "snow realm south portal", False, None],  # Need to separate some entrances here to make cannon logic work, don't care rn
        ["snow realm south portal", "snow realm south", False, has_portal("Hyrule Castle to Anouki Village", False, "_sr_portal", True) & has_glyph("Snow")],
        ["snow realm south portal", "snow realm", False, has_portal("Hyrule Castle to Anouki Village", False, "_sr_portal", True) & has_glyph("Snow")],
        ["forest realm", "dark realm portal", True, has_compass & has_glyph("Forest")],

        # cave
        ["forest realm", "forest cave tracks", True, has_tracks("Forest Realm SW Cave") & has_glyph("Forest")],
        ["forest cave tracks", "forest cave portal loc", False, has_cannon],
        ["forest cave portal loc", "cave portal event", False, None],
        ["forest cave tracks", "w forest tracks", True, has_tracks("Forest Realm SW Cave") & has_tracks("W Forest Realm")],
        ["w forest tracks", "snow realm fr", True, has_glyph("Snow") & has_tracks("W Forest Realm")],
        ["w forest tracks", "wtt", True, has_temple_tracks("Wooded") & has_tracks("W Forest Realm")],

        # W Wooded temple
        ["wtt", "w wooded temple tracks", True, has_tracks("W Wooded Temple") & has_temple_tracks("Wooded")],
        ["w wooded temple tracks", "snow realm fr", True, has_tracks("W Wooded Temple") & has_glyph("Snow")],
        ["w wooded temple tracks north", "snow realm", True, has_tracks("W Wooded Temple") & has_glyph("Snow")],
        ["w wooded temple tracks north", "snow realm south", True, has_tracks("W Wooded Temple") & has_glyph("Snow")],
        ["w wooded temple tracks", "w wooded temple tracks north", False, has_tracks("W Wooded Temple")],
        ["w wooded temple tracks north", "w wooded temple tracks", False, has_glyph("Snow") & has_tracks("W Wooded Temple")],

        # Rabbits
        ["forest realm", "forest realm rabbits", False, has_net],
        ["ocean shortcut", "forest ocean shortcut rabbit", False, has_tracks("Forest Realm Ocean Shortcut") & has_net],
        ["e mayscore bridge", "e mayscore rabbits", False, has_tracks("E Mayscore Bridge") & has_net],
        ["forest realm se portal track", "sw trading post rabbit", False, has_net],
        ["forest realm rabbits", "sw trading post rabbit", False, has_glyph("Ocean") & hard_logic],
        ["wtt", "wt rabbit", False, has_net],
        ["forest source", "wt rabbit", False, has_net],
        ["w forest tracks", "s rabbit haven rabbits", False, has_net],
        ["snow realm fr", "nr rabbit haven rabbit", False, has_net & has_glyph("Snow")],

        # Snow bridge
        ["w castle town tracks", "snow bridge south", True, has_tracks("W Castle Town") & has_tracks("Snow Realm Bridge")],
        ["n castle town tracks", "snow bridge south", True, has_tracks("N Castle Town") & has_tracks("Snow Realm Bridge")],
        ["n castle town tracks", "n castle town tracks north", True, has_tracks("N Castle Town")],
        ["n castle town tracks north", "snow realm source", True, has_tracks("N Castle Town") & has_source("Snow") & soft_cannon],
        ["snow bridge mid", "snow bridge south", True, has_tracks("Snow Realm Bridge")],
        ["snow bridge north", "snow bridge mid", True, has_tracks("Snow Realm Bridge")],
        ["wtt", "snow bridge south", True, has_temple_tracks("Wooded") & has_tracks("Snow Realm Bridge") & soft_cannon],
        ["snow bridge north", "snow realm", True, has_glyph("Snow") & has_tracks("Snow Realm Bridge")],
        ["snow bridge north", "snow realm source", True, has_source("Snow") & has_tracks("Snow Realm Bridge")],
        ["snow bridge north", "snow bridge portal loc", False, has_cannon],
        ["snow bridge portal loc", "snow bridge portal event", False, None],

        ["wtt", "forest ferrus", False, has_passenger("Ferrus", "_ferrus_3")],
        ["forest source", "forest ferrus", False, has_passenger("Ferrus", "_ferrus_3")],

        # # ======== Castle Town =========

        ["forest realm (ct)", "castle town", False, has_glyph("Forest")],
        ["castle town", "forest realm (ct)", False, None],
        ["forest realm", "forest realm (ct)", True, has_glyph("Forest") & soft_cannon],
        ["castle town", "castle town goron", False, has_passenger("City Goron", "_city_goron")],
        ["castle town", "pick up alfonzo", False, (has_glyph("Snow") & has_glyph("Forest") & pickup_tracks) | (Has("_visit_outset") & pickup_visit)],
        ["castle town", "castle town teacher", False, ((has_glyph("Snow") | has_glyph("Ocean") | has_glyph("Fire") | has_source("Fire")) & pickup_tracks) | (HasAny("_visit_av", "_visit_papuzia", "_visit_gv") & pickup_visit)],
        ["pick up alfonzo", "alfonzo event", False, None],
        ["mona's house", "castle town mona", False, pickup_passenger("Snow Glyph", "_visit_rabbit")],
        ["castle town", "castle town fish", False, has_cargo("Fish", "_buy_fish")],
        ["castle town", "visit castle town", False, None],

        ["castle town", "castle town wall", False, has_bombs],
        ["castle town wall", "castle town stamp station", False, has_stamp_book],
        ["castle town stamp station", "castle town stamp event", False, None],
        ["castle town wall", "castle town cuccos", False, ct_cuccos],

        ["castle town", "lucia's house", True, None],
        ["castle town", "mona's house", True, None],
        ["castle town", "shitate's shop", True, None],
        ["castle town", "milo's house", True, None],
        ["castle town", "teao", True, None],

        ["teao", "teao rupees", False, has_rupees(150) | ool],
        ["teao rupees", "teao 1", False, And(
             has_sword,
             has_whirlwind,
             Or(has_source("Forest"), has_source("Ocean"), has_source("Sand")))],
        ["teao rupees", "teao 2", False, And(
            has_source("Ocean") | has_source("Sand"),
            has_sword,
            has_whirlwind,
            has_boomerang,
            has_whip)
         ],
        ["teao rupees", "teao 3", False, And(
            has_source("Sand"),
            has_sword,
            has_whirlwind,
            has_boomerang,
            has_whip,
            has_bow,
            has_sand_wand)],
        ["teao 3", "teao_event", False, None],

        # # ======== Hyrule Castle =========

        ["castle town", "hyrule castle courtyard", True, None],
        ["hyrule castle courtyard", "hyrule castle 1f", True, None],
        ["hyrule castle 1f", "hyrule castle throne room", True, None],
        ["hyrule castle 1f", "hyrule castle barracks", True, None],
        ["hyrule castle 1f", "hyrule castle infirmary", True, None],
        ["hyrule castle 1f", "hyrule castle roof left", True, None],
        ["hyrule castle 1f", "hyrule castle roof right", True, None],

        ["hyrule castle roof left", "hyrule castle roof right", True, None],
        ["hyrule castle roof right", "hyrule castle ne ledge", False, None],
        ["hyrule castle ne ledge", "hyrule castle courtyard", False, None],
        ["hyrule castle roof right", "hyrule castle 2f", True, None],

        ["hyrule castle 2f", "hyrule castle ne ledge", True, None],
        ["hyrule castle 2f", "hyrule castle nw ledge", True, None],
        ["hyrule castle throne room", "hyrule castle 2f left", True, None],
        ["hyrule castle throne room", "hyrule castle 2f", True, None],
        ["hyrule castle 2f left", "hyrule castle 2f", True, None],
        ["hyrule castle 2f", "zelda's room", True, None],
        ["hyrule castle 2f", "hyrule castle backdoor", True, None],

        ["hyrule castle barracks", "hyrule castle sword minigame", False, has_sword & has_source("Snow") & has_rupees(100)],

        # # ======== ToS Tunnel =========

        ["hyrule castle backdoor", "hyrule castle backyard", True, None],
        ["hyrule castle backyard", "tower tunnel 1f", True, None],
        ["tower tunnel 1f", "tower tunnel block chest", False, can_kill_bat_pit | has_bombs | hard_logic],
        ["tower tunnel 1f", "tower tunnel key door", True, has_single_small_key("Tunnel to ToS")],
        ["tower tunnel key door", "tower tunnel 2f", True, None],

        ["tower tunnel 2f", "tower tunnel 2f north", False, None],
        ["tower tunnel 2f north", "tower tunnel 2f", False, has_bombs],
        ["tower tunnel 2f north", "tower tunnel 2f door", False, can_kill_bat],
        # ["tower tunnel 2f door", "tower tunnel 2f north", False, None],  # depends on entrance animation?
        ["tower tunnel 2f door", "tower tunnel 3f", False, can_kill_bat],
        ["tower tunnel 3f", "tower tunnel 2f door", False, None],

        ["tower tunnel 3f", "tower tunnel 3f north", True, has_damage],
        ["tower tunnel 3f north", "tos lobby", False, None],

        # # ========== ToS ===================

        ["forest realm", "tos forest station", True, can_enter_tos & has_glyph("Forest")],
        ["forest source", "tos forest station", True, can_enter_tos & has_source("Forest")],
        ["snow realm source", "tos snow station", True, can_enter_tos & has_source("Snow") & soft_cannon],
        ["ocean realm source", "tos ocean station", True, can_enter_tos & has_source("Ocean")],
        ["fire source", "tos fire station", True, can_enter_tos & has_source("Fire")],

        ["tos forest station", "tos lobby", False, can_enter_tos & (has_glyph("Forest") | has_source("Forest"))],
        ["tos lobby", "tos forest station", False, None],
        ["tos snow station", "tos lobby", False, can_enter_tos & has_source("Snow")],
        ["tos lobby", "tos snow station", False, None],
        ["tos ocean station", "tos lobby", False, can_enter_tos & has_source("Ocean")],
        ["tos lobby", "tos ocean station", False, None],
        ["tos fire station", "tos lobby", False, can_enter_tos & has_source("Fire")],
        ["tos lobby", "tos fire station", False, None],
        ["tos lobby", "tos", True, can_enter_tos],

        ["tos", "tos 1", True, can_enter_tos_section(1)],
        ["tos", "tos 2", True, can_enter_tos_section(2)],
        ["tos", "tos 3", True, can_enter_tos_section(3)],
        ["tos", "tos 4", True, can_enter_tos_section(4)],
        ["tos", "tos 5", True, can_enter_tos_section(5)],
        ["tos 5", "tos 23f", False, None] if world.exclude_tos_5 else None,

        ["tos 1", "tos 1f", True, None],
        ["tos 1f", "tos 1f chest", False, has_range | has_sword_beam],
        ["tos 1f", "tos 1f switch", False, can_kill_bat | can_possess_phantom(1)], # Phantom can hit switch
        ["tos 1f", "tos 2f", False, can_possess_phantom(1) | vanilla_tears],
        ["tos 2f", "tos 2f raised chests", False, has_whirlwind | glitched_logic],
        ["tos 2f", "tos 2f bomb wall", False, has_bombs],
        ["tos 2f", "tos 3f rail map", False, None],
        ["tos 3f rail map", "goal_forest_glyph", False, None],
        ["tos 3f rail map", "event_3f", False, None],

        ["tos 2", "tos 4f", True, None],
        ["tos 4f", "tos 4f whirlwind", False, has_whirlwind | can_possess_phantom(2)],
        ["tos 4f", "tos 5f phantom", False, can_possess_phantom(2) | (vanilla_tears & has_whirlwind)],
        ["tos 5f phantom", "tos 5f spinnit key", False, has_whirlwind],
        ["tos 5f spinnit key", "tos 5f alt path", False, has_boomerang],
        ["tos 5f alt path", "tos 5f secret chest", False, has_bombs],
        ["tos 5f alt path", "tos 4f ne chest", False, has_bombs], # needs whirlwind and boomerang to get here
        ["tos 5f alt path", "tos 6f chests", False, None], # geozards only need sword + phantom
        ["tos 5f spinnit key", "tos 6f key", False, has_small_keys("ToS 2", 1)], # already have whirlwind
        ["tos 6f key", "tos 7f rail map", False, has_small_keys("ToS 2", 2)],
        ["tos 7f rail map", "goal_snow_glyph", False, None],
        ["tos 7f rail map", "event_7f", False, None],

        ["tos 3", "tos 8f", True, None],
        ["tos 8f", "tos 8f bombs", False, has_bombs],
        ["tos 8f", "tos 9f phantom", False, vanilla_tears | can_possess_phantom(3)], #
        ["tos 9f phantom", "tos 9f nw", False, has_whirlwind],
        ["tos 9f phantom", "tos 11f", False, has_damage & (has_boss_key("ToS 3") | vanilla_boss_keys)],
        ["tos 11f", "event_12f", False, None],
        ["tos 11f", "goal_ocean_glyph", False, None],

        ["tos 4", "tos 13f", True, None],
        ["tos 13f", "tos 13f whip", False, has_whip],
        ["tos 13f", "tos 13f boomerang", False, has_boomerang],
        ["tos 13f", "tos 14f east", False, has_small_keys("ToS 4", 3, 1) | (vanilla_tears & has_small_keys("ToS 4", 2, 1))],
        ["tos 13f", "tos 13f phantom", False, can_possess_phantom(4)
            | (vanilla_tears & has_whip & has_small_keys("ToS 4", 2, 1))],
        ["tos 13f phantom", "tos 13f phantom whip", False, has_whip],
        ["tos 13f phantom", "tos 14f west", False, has_small_keys("ToS 4", 2, 1) ],

        ["tos 14f east", "tos 14f phantom", False, can_possess_phantom(4) | (vanilla_tears & has_whip)],
        ["tos 14f west", "tos 15f", False, has_whip],
        ["tos 15f", "tos 16f", False, tos_15f_glitched],
        ["tos 16f", "tos 16f bombs", False, has_bombs],
        ["tos 16f", "event_17f", False, None],
        ["tos 16f", "goal_fire_glyph", False, None],

        ["tos 5", "tos 18f", True, None],
        ["tos 18f", "tos 18f whip", False, has_whip],
        ["tos 18f", "tos 19f", False, has_small_keys("ToS 5", 1)],
        ["tos 18f", "tos 18f phantom", False, can_possess_phantom(5)],
        ["tos 18f phantom", "tos 19f center", False, None],

        ["tos 19f", "tos 19f south", False, has_bow & (has_boomerang | (can_possess_phantom(5) & can_rotate_repeater))],
        ["tos 19f south", "tos 20f tear", False, has_boomerang | has_sword_beam | (
            hard_logic & can_rotate_repeater & (
                can_possess_phantom(5) | has_whip))],
        ["tos 19f", "tos 19f center", False, can_possess_phantom(5) | (vanilla_tears & has_bow & has_boomerang)],
        ["tos 19f center", "tos 19f center chest", False, has_bow & (has_boomerang | has_sword_beam | has_whip | hard_logic)],
        ["tos 19f center", "tos 18f phantom", False, None],
        ["tos 19f center", "tos 20f", False, has_small_keys("ToS 5", 2) | (not_vanilla_tears & has_small_keys("ToS 5", 2, 1))],

        ["tos 20f", "tos 19f center 2", False, has_bow & can_rotate_repeater],
        ["tos 20f", "tos 19f center chest", False, has_bow],
        ["tos 20f", "tos 22f", False, has_bow & can_rotate_repeater & has_whip],
        ["tos 20f", "tos 19f south", False, can_possess_phantom(5)],
        ["tos 22f", "tos 21f bombs", False, has_bombs],
        ["tos 22f", "tos 23f", False, has_boss_key("ToS 5") | (vanilla_boss_keys & (has_bow | has_sword_beam))],
        ["tos 23f", "tos staven", False, has_sword],
        ["tos staven", "tos post staven", False, None],
        ["tos post staven", "tos 23f", False, None],
        ["tos staven", "event_staven", False, None],
        ["tos staven", "goal_staven", False, None],

        ["tos post staven", "tos summit lower", True, None],
        ["tos summit lower", "tos summit", True, None],
        ["tos summit", "tos stamp station", False, has_stamp_book],
        ["tos stamp station", "tos stamp event", False, has_stamp_book],
        ["tos summit", "tos 6", False, has_bow_of_light],
        ["tos 30f", "tos 6", True, None],

        ["tos 30f", "tos 30f bomb wall", False, has_bombs],
        ["tos 30f", "tos 29f", False, can_possess_phantom(6) & has_boomerang & has_whirlwind],
        ["tos 29f", "tos 29f sand wand", False, has_sand_wand],
        ["tos 29f sand wand", "tos 29f se", False, has_bow_of_light],

        ["tos 29f se", "tos 27f", False, has_small_keys("ToS 6", 3)],
        ["tos 27f", "tos 24f", False, has_whip],
        ["tos 29f", "tos 24f", False, glitched_logic & has_bombs & has_small_keys("ToS 6", 3, 1)],
        ["tos 24f", "event_24f", False, None],
        ["tos 24f", "goal_compass", False, None],

        # # ======== Mayscore =========

        ["forest realm", "mayscore station", True, has_glyph("Forest")],
        ["mayscore station", "mayscore", False, has_glyph("Forest")],
        ["mayscore", "mayscore station", False, None],
        ["mayscore", "mayscore north", True, None],

        ["mayscore", "uriko's shop", True, None],
        ["mayscore", "morris' house", True, None],
        ["mayscore", "dovok's house", True, None],
        ["mayscore", "wood's house", True, None],

        ["mayscore north", "mayscore stamp station", False, has_stamp_book],
        ["mayscore stamp station", "mayscore stamp event", False, None],
        ["mayscore north", "mayscore whip chest", False, has_whip],
        ["mayscore whip chest", "mayscore whip game", False, has_rupees(200)],
        ["mayscore", "mayscore leaves", False, has_whirlwind],
        ["mayscore north", "mayscore leaves", False, has_whirlwind],

        ["dovok's house", "mayscore dovok", False, pickup_passenger("Ocean Glyph", "_visit_papuzia")],
        ["mayscore whip chest", "mayscore wood", False, pickup_passenger("Ocean Glyph", "_visit_papuzia")],
        ["mayscore", "mayscore steel", False, has_cargo("Goron Steel", "_buy_steel")],
        ["morris' house", "mayscore morris", False, pickup_passenger("Ocean Glyph", "_visit_papuzia")],
        ["mayscore", "mayscore quest", False, pickup_passenger("Ocean Glyph", "_visit_papuzia")],

        # # ======== Forest Sanctuary =========

        ["forest realm", "woodland sanc station", True, has_glyph("Forest")],
        ["woodland sanc station", "woodland sanc", False, has_glyph("Forest")],
        ["woodland sanc", "woodland sanc station", False, None],
        ["woodland sanc", "woodland sanc stamp station", False, has_stamp_book],
        ["woodland sanc stamp station", "woodland sanc stamp event",False, None],
        ["woodland sanc", "woodland sanc song statue", False, has_spirit_flute],
        ["woodland sanc", "woodland sanc door", False, None],
        ["woodland sanc door", "woodland sanc sanc", True, None],
        ["woodland sanc sanc", "woodland sanc duet", False, has_spirit_flute],
        ["woodland sanc", "woodland sanc chest", False, has_cuccos], 

        # # ======== Wooded Temple =========

        ["wtt", "wt station", True, has_temple_tracks("Wooded")],
        ["forest source", "wt station", True, has_source("Forest")],
        ["wt station", "wooded temple lobby", False, has_temple_tracks("Wooded") | has_source("Forest")],
        ["wooded temple lobby", "wt station", False, None],
        ["wooded temple lobby", "wt song statue", False, has_spirit_flute],
        ["wooded temple lobby", "wt 1f", True, None],

        ["wt 1f", "wt 1f switch chest", False, has_whirlwind | hard_logic],
        ["wt 1f switch chest", "wt stamp station", False, has_stamp_book],
        ["wt stamp station", "wt stamp event", False, None],
        ["wt 1f", "wt 1f right arena", False, None],
        ["wt 1f right arena", "wt 1f", False, has_damage],
        ["wt 1f right arena", "wt 1f enemy chest", False, has_damage],
        ["wt 1f right arena", "wt 1f se door", False, has_damage],
        ["wt 1f se door", "wt 2f", True, None],

        ["wt 2f", "wt 2f ne arena", False, None],
        ["wt 2f ne arena", "wt 2f", False, has_damage],
        ["wt 2f ne arena", "wt 2f enemy chest", False, has_damage],
        ["wt 2f", "wt 2f poison chest", False, has_whirlwind | hard_logic],
        ["wt 2f enemy chest", "wt 2f north", False, has_whirlwind],
        ["wt 2f ne arena", "wt 2f north", False, has_whirlwind & hard_logic],
        ["wt 2f north", "wt 1f north", True, None],
        ["wt 1f north", "wt 1f key", False, has_whirlwind | has_boomerang | has_whip],
        ["wt 1f north", "wt 1f", False, None],

        ["wt 1f", "wt 1f left", True, has_small_keys_er("Wooded Temple", 1, er=2)],
        ["wt 1f", "wt 1f keydoor", False, None],
        ["wt 1f left", "wt 1f keydoor", False, None],
        ["wt 1f left", "wt 1f left arena", False, None],
        ["wt 1f left arena", "wt 1f left", False, can_kill_bubble],
        ["wt 1f left arena", "wt 2f left", False, can_kill_bubble],
        ["wt 2f left", "wt 1f left arena", False, None],

        ["wt 2f left", "wt 3f left", True, None],
        ["wt 3f left", "wt 3f chestnut chest", False, has_range_objects | has_sword_beam],
        ["wt 2f left", "wt 2f moth", False, has_small_keys_er("Wooded Temple", 2)],
        ["wt 2f moth", "wt 2f left", False, can_kill_moth & has_small_keys_er("Wooded Temple", 2)],
        ["wt 2f moth", "wt 2f moth door", False, can_kill_moth],
        ["wt 2f moth door", "wt 3f", True, None],

        ["wt 3f", "wt 3f se chest", False, has_whirlwind | hard_logic],
        ["wt 3f", "wt 3f bk", False, has_whirlwind | (has_bombs & hard_logic)],
        ["wt 3f bk", "wt 3f boss door", False, True_() & vanilla_boss_keys],
        ["wt 3f", "wt 3f boss door", True, has_boss_key("Wooded Temple")],
        ["wt 3f boss door", "wt 4f", True, None],

        ["wt 4f", "wt blue warp", True, None],
        ["wt blue warp", "wooded temple lobby", False, None],
        ["wt blue warp", "wt warp event", False, None],
        ["wooded temple lobby", "wt blue warp", False, Has("_wt_warp") | open_warps],
        ["wt 4f", "wt pre stagnox", False, None],
        ["wt pre stagnox", "wt 4f", False, has_sword & has_whirlwind],
        ["wt pre stagnox", "wt stagnox", False, has_sword & has_whirlwind],
        ["wt stagnox", "goal_stagnox", False, None],
        ["wt stagnox", "event_stagnox", False, None]
    ]

    overworld_logic += [

        # # ============ Trading Post =============

        ["forest realm", "trading post tracks", True, has_glyph("Ocean") & soft_cannon & has_glyph("Forest")],
        ["trading post tracks", "trading post station", True, has_glyph("Ocean")],
        ["trading post station", "trading post", False, has_glyph("Ocean")],
        ["trading post", "trading post station", False, None],
        ["trading post", "visit trading post", False, None],

        ["trading post", "linebeck's shop", True, None],
        ["trading post", "trading post tunnel", True, None],
        ["trading post north", "trading post tunnel", True, None],
        ["trading post north", "trading post island", False, has_range | has_sword_beam],
        ["trading post island", "trading post north", False, has_range | has_sword_beam | has_bombs],
        ["trading post island", "trading post cave", False, has_range | has_sword_beam | has_bombs],
        ["trading post cave", "trading post island", False, None],

        ["trading post north", "trading post light song statue", False, has_spirit_flute],
        ["trading post cave", "trading post chest", False, has_sod & (has_sol | hard_logic)],
        ["trading post tunnel", "trading post stamp station", False, has_bombs & has_stamp_book],
        ["trading post stamp station", "trading post stamp event", False, None],
        ["trading post north", "trading post leaves", False, has_whirlwind],

        ["trading post", "trading post bridge worker", False, has_passenger("Kenzo", "_kenzo_1")],
        ["trading post bridge worker", "trading post bridge worker event", False, None],
        ["trading post bridge worker event", "linebeck trading", False, Has("Treasure: Regal Ring")]
            if world.options.randomize_passengers.value else
            ["trading post", "linebeck trading", False, Has("Treasure: Regal Ring")],
        ["linebeck trading", "linebeck event", False, None],
        ["trading post", "trading post pick up kenzo", False, Has("_can_sell_treasure") & pickup_passenger("Snow Glyph", "_visit_av")],
        ["trading post pick up kenzo", "trading post pick up kenzo event", False, None],
        ["linebeck's shop", "linebeck dark ore", False, Has("_can_sell_treasure") & has_cargo("Dark Ore", "_buy_ore")],

        # # ========== Rabbit Haven ========

        ["snow realm fr", "rabbit haven station", True, has_glyph("Snow")],
        ["rabbit haven station", "rabbit haven", False, has_glyph("Snow")],
        ["rabbit haven", "rabbit haven station", False, None],
        ["rabbit haven", "visit rabbit haven", False, None],

        ["rabbit haven", "rabbit haven 5 rabbits", False, has_total_rabbits(5)],
        ["rabbit haven", "rabbit haven 10 forest rabbits", False, has_rabbit_items("Grass", 10)],
        ["rabbit haven", "rabbit haven 10 snow rabbits", False, has_rabbit_items("Snow", 10)],
        ["rabbit haven", "rabbit haven 10 ocean rabbits", False, has_rabbit_items("Ocean", 10)],
        ["rabbit haven", "rabbit haven 10 mountain rabbits", False, has_rabbit_items("Mountain", 10)],
        ["rabbit haven", "rabbit haven 10 sand rabbits", False, has_rabbit_items("Sand", 10)],
        ["rabbit haven", "rabbit haven 50 rabbits", False, has_all_rabbits],
        ["rabbit haven", "rabbit haven 1 of each rabbits", False, has_all_rabbit_types],
        ["rabbit haven", "rabbit haven mona", False, has_passenger("Mona", "_mona")],

        # # ============ Snow Realm ===============

        ["snow realm s entr", "snow realm fr", True, has_glyph("Snow")],
        ["snow realm south", "snow realm s entr", True, has_glyph("Snow")],
        ["snow realm south", "snow realm", True, soft_cannon],
        ["snow realm south", "anouki portal", False, has_cannon],
        ["anouki portal", "anouki portal event", False, None],
        ["snow realm", "blizzard temple tracks", True, has_temple_tracks("Blizzard") & has_glyph("Snow")],
        ["snow realm", "snow realm rabbits", False, has_net],
        ["blizzard temple tracks", "blizzard temple tracks rabbits", False, has_net],
        ["blizzard temple tracks rabbits", "snow realm blizzard rabbits", False, has_source("Snow")],
        ["blizzard temple tracks rabbits", "snow realm early blizzard rabbits", False, has_source("Snow") | hard_logic],
        ["snow realm source", "blizzard temple tracks", True, has_source("Snow") & has_temple_tracks("Blizzard")],

        ["snowdrift tracks", "snowdrift station rabbit", False, has_net],
        ["blizzard temple tracks", "icyspring tracks", True, has_tracks("N Icy Spring") & has_temple_tracks("Blizzard")],
        ["icyspring tracks", "icyspring rabbits", False, has_net],
        ["icyspring tracks", "icyspring portal loc", False, has_cannon],
        ["icyspring portal loc", "icyspring portal event", False, None],

        ["blizzard temple tracks", "snow realm ferrus", False, 
            has_source("Snow") & has_passenger("Alfonzo", "_picked_up_alfonzo")
         & pickup_passenger("Forest Glyph", "_visit_outset")],

        *get_portal_logic("forest realm se portal track", "forest realm se portal",
                          "blizzard temple tracks", "btt e portal",
                          "Forest Realm SE Portal", "Blizzard Temple Tracks",
                          "Trading Post to E Snow Realm", "_tp_portal"),
        ["forest realm se portal track", "trading post portal", False, has_cannon],
        ["trading post portal", "trading post portal event", False, None],

        # ======== Anouki Village ========

        ["snow realm", "snow realm (av)", True, has_glyph("Snow")],
        ["snow realm (av)", "anouki village", False, has_glyph("Snow")],
        ["anouki village", "snow realm (av)", False, None],
        ["anouki village", "visit anouki village", False, None],

        ["anouki village", "honcho's house", True, None],
        ["anouki village", "bulu's house", True, None],
        ["anouki village", "kofu's house", True, None],
        ["anouki village", "noko's house", True, None],
        ["anouki village", "yefu's house", True, None],
        ["anouki village", "yeko's house", True, None],
        ["anouki village", "ice block cave", False, has_bombs],
        ["ice block cave", "anouki village", False, None],

        ["anouki village", "anouki village stamp station", False, has_stamp_book],
        ["anouki village stamp station", "anouki village stamp event", False, None],
        ["anouki village", "anouki village song statue", False, has_spirit_flute],
        ["anouki village", "anouki village lake chest", False, has_boomerang],

        ["anouki village", "av noko", False, pickup_passenger("Blizzard Temple Tracks", "_visit_icyspring")],
        ["anouki village", "av fence", False, (
                has_passenger("Kenzo", "_kenzo_2") | no_passengers
            ) & (
                has_cargo("Lumber", "_buy_lumber") | no_cargo)],
        ["anouki village", "av kenzo", False, (has_passenger("Kenzo", "_kenzo_2") | no_passengers)
        | (has_cargo("Lumber", "_buy_lumber") | no_cargo)],
        ["anouki village", "av goron", False, has_passenger("Snow Goron", "_snow_goron")],
        ["av goron", "av goron event", False, None],
        ["honcho's house", "av kofu", False, Has("_av_goron") & (((has_glyph("Fire") | has_source("Fire")) & pickup_tracks) | Has("_visit_gv", options=pickup_visit))],

        # NPC Quest events
        ["av kofu", "av kofu event", False, None],
        ["av noko", "av noko event", False, None],
        ["icyspring noko", "icyspring noko event", False, None],
        ["castle town mona", "castle town mona event", False, None],
        ["outset joe", "outset joe event", False, None],
        ["mayscore dovok", "mayscore dovok event", False, None],
        ["pv carben", "pv carben event", False, None],
        ["pirate wadatsumi", "pirate wadatsumi event", False, None],
        ["pick up snow goron", "pick up snow goron event", False, None],
        ["pick up city goron", "pick up city goron event", False, None],
        ["snow realm ferrus", "snow realm ferrus event", False, None],
        ["fire realm ferrus", "fire realm ferrus event", False, None],

        # Cargo Events
        ["icyspring ice", "icyspring ice event", False, None],
        ["mayscore lumber", "mayscore lumber event", False, None],
        ["castle town buy cuccos", "castle town buy cuccos event", False, None],
        ["papuzia buy fish", "papuzia buy fish event", False, None],
        ["wise one buy vessel", "wise one buy vessel event", False, None],
        ["goron steel", "goron steel event", False, None],
        ["dark ore mine ore", "dark ore mine ore event", False, None],

        # =========== Snow Sanctuary ==========

        ["snow realm", "snow sanc tracks", False, Has("Snow Sanctuary Cave Key") & has_cannon],
        ["snow sanc tracks", "snow realm", False, has_cannon],
        ["blizzard temple tracks", "snow sanc tracks", True, has_temple_tracks("Blizzard") & has_glyph("Snow")],
        ["snow sanc tracks", "snow sanc station", True, has_glyph("Snow")],
        ["snow sanc station", "snow sanc", False, has_glyph("Snow")],
        ["snow sanc", "snow sanc station", False, None],

        ["snow sanc", "snow sanc stamp station", False, has_stamp_book],
        ["snow sanc stamp station", "snow sanc stamp event", False, None],
        ["snow sanc", "snow sanc cave", True, None],
        ["snow sanc", "snowfall supermarket", True, None],
        ["snow sanc cave", "snow sanc sanc", True, None],
        ["snow sanc sanc", "snow sanc song", False, has_spirit_flute],
        ["snow sanc song", "steem gift", False, has_source("Snow")]
            if world.options.randomize_minigames.value else
            ["snow sanc sanc", "steem gift", False, has_source("Snow")],
        ["snow sanc", "snow sanc vessel", False, has_cargo("Vessel", "_buy_vessel")],
        ["snow sanc vessel", "snow sanc sanc", False, ool],

        ## ========== Blizzard Temple =========

        ["snow realm source", "bt station", True, has_source('Snow') & soft_cannon],
        ["blizzard temple tracks", "bt station", True, has_temple_tracks("Blizzard")],
        ["bt station", "blizzard temple lobby", False, has_temple_tracks("Blizzard") | has_source('Snow')],
        ["blizzard temple lobby", "bt station", False, None],

        ["blizzard temple lobby", "bt 1f exit", True, None],
        ["bt 1f exit", "bt 1f s", True, can_break_grass],
        ["bt 1f s", "bt 1f", True, None],

        ["bt 1f", "bt 1f e", False, Filtered(can_ring_bell, options=[OptionFilter(SpiritTracksOpenBlizzardTemple, 0)], filtered_resolution=True)],
        ["bt 1f e", "bt 1f", False, Filtered(True_(), options=[OptionFilter(SpiritTracksOpenBlizzardTemple, 1)])],
        ["bt 1f e", "bt 1f e shortcut", True, None],
        ["bt 1f e", "bt 1f se", True, None],
        ["bt 1f se", "bt 1f se door", True, has_whirlwind | has_short_range],
        ["bt 1f se door", "bt b1 se", True, None],

        ["bt b1 se", "bt b1 e", False, has_whirlwind],
        ["bt b1 e", "bt b1 ne", False, None],
        ["bt b1 ne", "bt b1 ne enemy chest", False, can_kill_ice_bat],
        ["bt b1 ne", "bt b1 ne door", False, has_short_range | has_boomerang],
        ["bt b1 ne door", "bt b1 ne", False, can_kill_bat],
        ["bt b1 ne door", "bt 1f ne", True, None],

        ["bt 1f ne", "bt 1f ne chest", False, can_kill_bat_pit],
        ["bt 1f ne", "bt 1f ne bell", False, has_boomerang],
        ["bt 1f ne bell", "bt 1f", False, None],
        ["bt 1f ne bell", "bt 1f torches", False, ool],
        ["bt 1f ne bell", "bt 1f ne bell event", False, None],

        ["bt 1f", "bt 1f sw", False, Filtered(has_boomerang & Has("_bt_bell_2"), options=[OptionFilter(SpiritTracksOpenBlizzardTemple, 0)], filtered_resolution=True)],
        ["bt 1f sw", "bt 1f", False, Filtered(Has("_bt_bell_2"), options=[OptionFilter(SpiritTracksOpenBlizzardTemple, 0)], filtered_resolution=True)],
        ["bt 1f sw", "bt 1f sw door", False, has_boomerang],
        ["bt 1f sw door", "bt 1f sw", False, can_break_grass],
        ["bt 1f sw door", "bt b1 sw", False, has_boomerang],
        ["bt b1 sw", "bt 1f sw door", False, None],

        ["bt b1 sw", "bt b1 sw chest", False, has_boomerang],
        ["bt b1 sw chest", "bt b1 w", False, has_single_small_key("Blizzard Temple") & can_kill_freezards_torch & has_whirlwind],
        ["bt b1 w", "bt b1 stamp station", False, has_stamp_book],
        ["bt b1 stamp station", "bt b1 stamp event", False, has_stamp_book],
        ["bt b1 w", "bt b1 nw", False, None],
        ["bt b1 w", "bt b1 w chest", False, can_kill_bubble | has_whirlwind],
        ["bt b1 nw", "bt 1f nw", True, None],

        ["bt 1f nw", "bt 1f w", True, None],
        ["bt 1f nw", "bt 1f nw bell", True, has_boomerang],
        ["bt 1f nw bell", "bt 1f", False, None],
        ["bt 1f nw bell", "bt 1f nw bell event", False, None],
        ["bt 1f nw bell", "bt 1f torches", False, None],

        ["bt 1f", "bt 1f n", False, Filtered(Has("_bt_bell_2") & Has("_bt_bell_3") & has_boomerang, options=[OptionFilter(SpiritTracksOpenBlizzardTemple, 0)], filtered_resolution=True)],
        ["bt 1f n", "bt 1f n chest", False, Has("_bt_torches")],
        ["bt 1f n", "bt 1f", False, [OptionFilter(SpiritTracksOpenBlizzardTemple, 1)] | Has("_bt_bell_3")],
        ["bt 1f n", "bt 1f n shortcut", True, None],
        ["bt 1f n", "bt 2f", True, None],

        ["bt 2f", "bt 2f boss door", True, has_boss_key("Blizzard Temple")],
        ["bt 2f", "bt 2f e", False, has_boomerang & has_damage],
        ["bt 2f e", "bt 2f boss key", False, has_whirlwind],
        ["bt 2f", "bt 2f boss key", False, Filtered(has_whirlwind, options=[OptionFilter(SpiritTracksRandomizeBossKeys, 0, "ne")]) & hard_logic],
        ["bt 2f boss key", "bt 2f boss door", False, True_() & vanilla_boss_keys],
        ["bt 2f boss door", "bt 3f", True, None],
        ["bt 3f", "bt pre fraaz", False, None],
        ["bt pre fraaz", "bt 3f", False, has_damage & has_boomerang],

        ["bt 3f", "bt blue warp", True, None],
        ["bt blue warp", "blizzard temple lobby", False, None],
        ["blizzard temple lobby", "bt blue warp", False, Has("_bt_warp") | open_warps],
        ["bt blue warp", "bt warp event", False, None],

        ["bt pre fraaz", "bt fraaz", False, has_damage & has_boomerang],
        ["bt fraaz", "goal_fraaz", False, None],
        ["bt fraaz", "event_fraaz", False, None],

        # ========== Icy Spring ==========

        ["blizzard temple tracks", "icyspring station", True, has_temple_tracks("Blizzard")],
        ["icyspring station", "icyspring", False, has_temple_tracks("Blizzard")],
        ["icyspring", "icyspring station", False, None],
        ["icyspring", "visit icyspring", False, None],

        ["icyspring", "ferrus' trailer", True, None],
        ["icyspring", "icyspring stamp station", False, has_stamp_book & has_boomerang],
        ["icyspring stamp station", "icyspring stamp event", False, None],
        ["icyspring", "icyspring whip chest", False, has_whip],
        ["icyspring", "icyspring noko", False, has_passenger("Noko", "_noko") | no_passengers],

        # ============ Snowdrift Station =========

        ["blizzard temple tracks", "snowdrift tracks", True, has_tracks("Snowdrift Station") & soft_cannon & has_temple_tracks("Blizzard")],
        ["snowdrift tracks", "snowdrift station", True, has_tracks("Snowdrift Station")],
        ["snowdrift station", "snowdrift", False, has_tracks("Snowdrift Station")],
        ["snowdrift", "snowdrift station", False, None],
        ["snowdrift", "snowdrift cave", True, None],
        ["snowdrift cave", "snowdrift reward", False, (has_range | (has_sword_beam & hard_logic)) & can_kill_freezards],

        ["snowdrift cave", "octive arena", True, None],
        ["snowdrift cave", "frostflame cave", True, None],
        ["snowdrift cave", "small skating", True, None],
        ["snowdrift cave", "big ice puzzle", True, None],

        # ========== Slippery Station ==========
        ["slippery tracks", "slippery station", True, has_tracks("Slippery Station")],
        ["slippery station", "slippery", False, has_tracks("Slippery Station")],
        ["slippery", "slippery station", False, None],
        ["blizzard temple tracks", "slippery tracks", True, has_tracks("Slippery Station") & has_temple_tracks("Blizzard") & soft_cannon & (has_source("Snow") | has_tracks("N Icy Spring"))],
        ["skating rink", "slippery", True, None],
        ["skating rink", "slippery amateur", False, None],
        ["skating rink", "slippery pro", False, None],
        ["skating rink", "slippery champion", False, None],

        # ========== Bridge Worker's Home =======
        ["snow realm source", "bridge workers station", True, has_source("Snow")],
        ["bridge workers station", "bridge workers", False, has_source("Snow")],
        ["bridge workers", "bridge workers station", False, None],
        ["bridge workers", "bridge workers chest", False, has_sod],
        ["bridge workers", "kenzo's house", True, None],
        ["kenzo's house", "pick up bridge worker", False, pickup_passenger("Ocean Glyph", "_visit_tp")],
        ["pick up bridge worker", "pick up bridge worker event", False, None],

        # ========== Ocean Realm =============
        ["forest realm", "e mayscore bridge", True, has_tracks("E Mayscore Bridge") & has_glyph("Forest")],
        ["e mayscore bridge", "ocean realm mid", True, has_glyph("Ocean") & has_tracks("E Mayscore Bridge")],
        ["forest realm", "ocean shortcut", True, has_tracks("Forest Realm Ocean Shortcut") & has_glyph("Forest")],
        ["forest source", "ocean shortcut", True, has_tracks("Forest Realm Ocean Shortcut") & has_source("Forest")],
        ["ocean shortcut east", "pirate hideout tracks", True, has_tracks("Forest Realm Ocean Shortcut") & has_tracks("Pirate Hideout")],
        ["e mayscore bridge", "ocean shortcut", True, has_tracks("Forest Realm Ocean Shortcut") & has_tracks("E Mayscore Bridge")],
        ["ocean shortcut east", "ocean shortcut", True, has_tracks("Forest Realm Ocean Shortcut")],

        ["trading post tracks", "ocean realm mid", True, Has("Repair Trading Post Bridge") & has_glyph("Ocean")],
        ["ocean realm mid", "ocean realm", True, has_glyph("Ocean")],
        ["ocean realm", "ocean temple tracks", True, has_temple_tracks("Marine") & has_glyph("Ocean")],
        ["ocean temple tracks", "ocean realm source", True, has_source("Ocean") & has_temple_tracks("Marine")],
        ["ocean realm", "pirate hideout tracks", True, has_tracks("Pirate Hideout") & has_glyph("Ocean")],
        ["ocean realm source", "pirate hideout tracks", True, has_source("Ocean") & has_tracks("Pirate Hideout")],
        ["ocean realm source", "ocean portal tracks", True, has_source("Ocean") & has_tracks("Ocean Portal")],
        ["ocean temple tracks", "ocean portal tracks", True, has_temple_tracks("Marine") & has_tracks("Ocean Portal")],
        ["ocean portal tracks", "sand realm", False, has_tracks("Sand Realm") & has_tracks("Ocean Portal")],
        ["ocean portal tracks", "ocean portal loc", False, has_cannon],
        ["ocean portal loc", "ocean portal event", False, None],

        ["ocean temple tracks", "undersea entrance", True, has_temple_tracks("Marine")],
        ["ocean realm source", "undersea entrance", True, has_source("Ocean")],
        ["undersea entrance", "undersea tracks", True, has_temple_tracks("Marine") | has_source("Ocean")],
        ["undersea tracks", "oct station", True, has_temple_tracks("Marine") | has_source("Ocean")],

        # Ocean Portals
        *get_portal_logic("ocean portal tracks", "ocean portal",
                          "trading post tracks", "s mayscore portal",
                          "Ocean Portal", "Ocean Glyph",
                          "Mayscore to Ocean Portal Tracks", "_ocean_portal"),
        *get_portal_logic("snow bridge north", "snow bridge portal",
                          "ocean temple tracks", "island sanc portal",
                          "Snow Realm Bridge", "Marine Temple Tracks",
                          "Snow Bridge to Island Sanctuary", "_bridge_portal"),

        # Ocean Rabbits
        ["ocean temple tracks", "ocean rabbits", False, has_net],
        ["las tracks", "las rabbit", False, has_net],
        ["ocean realm source", "ocean source rabbits", False, has_net],
        ["ocean portal tracks", "ocean portal rabbits", False, has_net],
        ["ocean shortcut east", "pirate rabbit", False, has_net & has_tracks("Forest Realm Ocean Shortcut")],

        # ========== Island Sanctuary =============
        ["ocean realm", "island sanc station", True, has_glyph("Ocean")],
        ["island sanc station", "island sanc", False, has_glyph("Ocean")],
        ["island sanc", "island sanc station", False, None],

        ["island sanc", "island sanc peninsula", False, has_sob & has_whip & hard_logic],
        ["island sanc peninsula", "island sanc shortcut", True, None],
        ["island sanc peninsula", "island sanc", False, None],
        ["island sanc peninsula", "island sanc north", True, None],
        ["island sanc", "island sanc S island chest", False, hard_birds],

        ["island sanc", "island sanc cave west", True, None],
        ["island sanc cave west", "island sanc cave east", False, has_boomerang],
        ["island sanc cave east", "island sanc cave west", False, has_bombs],
        ["island sanc cave east", "island sanc north", True, None],

        ["island sanc north", "island sanc nw chest", False, hard_birds],
        ["island sanc north", "island sanc stamp station", False, has_stamp_book & has_sob & has_whip],
        ["island sanc stamp station", "island sanc stamp event", False, None],
        ["island sanc north", "island sanc sanc", True, None],
        ["island sanc sanc", "island sanc song", False, has_spirit_flute]
            if world.options.randomize_passengers == "no_passengers" else
            ["island sanc sanc", "island sanc song", False, has_spirit_flute & Has("_deliver_carben")],
        ["island sanc", "island sanc carben", False, has_passenger("Carben", "_carben")],
        ["island sanc carben", "carben event", False, None],

        # ========== Papuzia Village =============
        ["ocean realm", "ocean realm (pv)", True, has_glyph("Ocean")],
        ["ocean realm (pv)", "papuzia village", False, has_glyph("Ocean")],
        ["papuzia village", "ocean realm (pv)", False, None],
        ["papuzia village", "papuzia village song statue", False, has_sod],
        ["papuzia village", "pv dovok", False, has_passenger("Dovok", "_dovok")],
        ["pv dovok", "orca's house", False, ool],
        ["pv wadatsumi", "orca's house", False, ool],
        ["papuzia village", "visit papuzia", False, None],

        ["papuzia village", "fuku's house", True, None],
        ["papuzia village", "wise one's house", True, None],
        ["papuzia village", "orca's house", True, None],
        ["papuzia village", "kogane's shop", True, None],

        ["papuzia village", "pv carben", False, has_sod],
        ["papuzia village", "pv wadatsumi", False, has_passenger("Wadatsumi", "_wadatsumi")],
        ["papuzia village song statue", "papuzia village south", False, hard_birds],
        ["papuzia village south", "papuzia village", False, Has("_papuzia_sob") & hard_birds],
        ["papuzia village south", "papuzia archipelago north", True, None],
        ["papuzia archipelago north", "papuzia archipelago", False, hard_birds],
        ["papuzia archipelago", "papuzia village stamp station", False, has_stamp_book & has_sob],
        ["papuzia village stamp station", "papuzia village stamp event", False, None],
        # You need a warp to start to return without bird song, patched with a dynaentrance
        # I don't like that this is locked behind song statue, but flags might not let us get there earlier

        ["papuzia village", "papuzia ice", False, has_cargo("Mega Ice", "_buy_ice")]
        if world.options.randomize_cargo.value in [1, 2] else
        ["papuzia village", "papuzia ice", False, has_wagon
             & (Has("Cargo: Mega Ice", 3) | (Has("Cargo: Mega Ice", 1) & ool))],

        # ========= Marine Temple ==================
        ["oct station", "marine temple lobby", False, has_temple_tracks("Marine") | has_source("Ocean")],
        ["marine temple lobby", "oct station", False, None],
        ["marine temple lobby", "oct song statue", False, has_spirit_flute],
        ["marine temple lobby", "oct 1f", True, None],
        ["marine temple lobby", "visit marine temple", False, None],

        ["oct 1f", "oct 1f whip", False, has_whip],
        ["oct 1f", "oct 1f right", False, hard_logic | Has("_oct_boulders")],
        ["oct 1f whip", "oct 1f right", False, None],
        ["oct 1f right", "oct 1f", False, None],

        ["oct 1f", "oct 2f", True, None],
        ["oct 2f", "oct 2f boulders", False, has_boomerang | has_bombs],
        ["oct 2f boulders", "oct 2f boulders event", False, None],
        ["oct 2f", "oct boomerang room", False, has_bombs],
        ["oct boomerang room", "oct 2f", False, None],
        ["oct boomerang room", "oct boomerang switch", False, has_boomerang & has_whip],
        ["oct boomerang switch", "oct boomerang switch event", False, has_boomerang & has_whip],
        ["oct 2f", "oct stamp room", False, has_bombs],
        ["oct stamp room", "oct 2f", False, None],
        ["oct stamp room", "oct stamp station", False, has_stamp_book & has_whip & Has("_oct_boomerang")],
        ["oct stamp station", "oct stamp event", False, None],

        ["oct 1f right", "oct 2f right", True, None],
        ["oct 2f right", "oct 2f logs", False, has_whip],
        ["oct 2f right", "oct 3f east", True, None],

        ["oct 3f east", "oct 3f arena", False, None],
        ["oct 3f arena", "oct 3f post arena", False, has_sword],
        ["oct 3f east", "oct 3f post arena", False, hard_logic & ((has_bombs & (glitched_logic | has_whirlwind)) | (has_boomerang & has_damage))],
        # you can't escape stunlock without sword, and the fight scripts you into it from the start
        ["oct 3f post arena", "oct 3f east", False, None],

        ["oct 3f post arena", "oct 3f north", False, has_whip],
        ["oct 3f north", "oct 3f arena", False, has_whip & hard_logic],
        ["oct 3f north", "oct 3f n chest", False, has_whip],
        ["oct 3f north", "oct 3f ne", True, has_small_keys_er("Marine Temple", 1, er=2)],
        ["oct 3f ne", "oct 4f north", True, None],

        ["oct 3f post arena", "oct 3f west", False, has_whip],
        ["oct 3f west", "oct 3f arena", False, has_whip & hard_logic],
        ["oct 3f west", "oct 4f west", True, None],

        ["oct 4f north", "oct 4f west", False, has_whip],
        ["oct 4f west", "oct 4f south", False, has_whip],
        ["oct 4f south", "oct 3f south", True, None],
        ["oct 3f south", "oct 3f arena", False, has_whip & hard_logic],
        ["oct 3f south", "oct 3f s chest", False, has_whip],

        ["oct 4f north", "oct 4f east", True, has_whip],
        ["oct 4f east", "oct 5f", False, has_whip | has_bombs],
        ["oct 5f", "oct 4f east", False, None],

        ["oct 5f", "oct 5f nw", False, has_whip],
        ["oct 5f", "oct 5f sw", True, has_whip],
        ["oct 5f sw", "oct 6f sw", True, None],
        ["oct 6f sw", "oct 6f sw arena", False, has_whip | has_bow | has_bombs],
        ["oct 6f sw arena", "oct 6f sw arena event",  False, None],
        ["oct 5f nw", "oct 6f nw", True, None],
        ["oct 5f", "oct 5f s", True, has_small_keys("Marine Temple", 2)],
        ["oct 5f s", "oct 5f se", False, has_whip],
        ["oct 5f se", "oct 6f se", True, None],

        ["oct 6f nw", "oct 6f", True, has_whip],
        ["oct 6f", "oct 6f w chest", False, has_whip],
        ["oct 6f w chest", "oct 6f e chest", False, Has("_oct_6f_arena")],
        ["oct 6f se", "oct 6f bk", False, has_whip],
        ["oct 6f", "oct 6f bk", False, glitched_logic & has_whirlwind & has_bombs],
        ["oct 6f bk", "oct 6f bk loc", False, None],
        ["oct 6f", "oct 6f bk loc", False, has_whirlwind],
        ["oct 6f bk", "oct 6f boss door", False, True_() & vanilla_boss_keys],
        ["oct 6f", "oct 6f boss door", True, has_boss_key("Marine Temple")],
        ["oct 6f boss door", "oct 7f south", True, None],

        ["oct 7f south", "oct 7f north", True, has_whip],
        ["oct 7f thorns", "oct 7f north", False, None],
        ["oct 7f north", "oct 7f thorns", False, has_whip],
        ["oct 7f thorns", "oct pre phytops", False, None],
        ["oct pre phytops", "oct 7f thorns", False, has_whip & has_good_damage],
        ["oct pre phytops", "oct phytops", False, has_whip & has_good_damage],
        ["oct phytops", "event_phytops", False, None],
        ["oct phytops", "goal_phytops", False, None],

        ["oct 7f north", "oct blue warp", True, None],
        ["marine temple lobby", "oct blue warp", False, Has("_oct_warp") | open_warps],
        ["oct blue warp", "marine temple lobby", False, None],
        ["oct blue warp", "oct warp event", False, None],
        ["marine temple lobby", "oct ferrus", False, has_passenger("Ferrus", "_ferrus_2")
                       & (randomize_passengers | ool | Has("_ferrus_backup"))],
        ["oct ferrus", "oct ferrus event", False, None],
        # If you fail the train journey in vanilla, make sure you have access to icyspring for backup.

        # ========= Pirate Hideout ==============
        ["pirate hideout tracks", "pirate hideout station", True, has_tracks("Pirate Hideout")],
        ["pirate hideout station", "pirate hideout", False, has_tracks("Pirate Hideout")],
        ["pirate hideout", "pirate hideout station", False, None],
        ["pirate hideout", "pirate hideout stamp station", False, has_stamp_book & has_whip & has_sob],
        ["pirate hideout stamp station", "pirate hideout stamp event", False, None],
        ["pirate hideout", "pirate hideout secret cave", False, has_bombs],
        ["pirate hideout secret cave", "pirate hideout", False, None],
        ["pirate hideout", "pirate hideout minigame", False, has_bow],
        ["pirate hideout", "pirate hangout", True, None],
        # Wadatsumi able to be reached with only tracks with minigames turned off, otherwise requires bow
        ["pirate hideout", "pirate wadatsumi", False, pickup_passenger("Ocean Glyph", "_visit_papuzia")]
            if world.options.randomize_minigames.value in [0] else
            ["pirate hideout", "pirate wadatsumi", False, has_bow & pickup_passenger("Ocean Glyph", "_visit_papuzia")],
        # First hideout minigame gives you bow automatically, and then it shows in top right, even with no items, but doesn't let you use it. With an item, it doesn't show

        # ======== Lost at Sea Station ==========
        ["ocean temple tracks", "las tracks", True, has_temple_tracks("Marine") & has_tracks("Lost at Sea Station")],
        ["las tracks", "lost at sea station", True, has_tracks("Lost at Sea Station")],
        ["lost at sea station", "lost at sea", False, has_tracks("Lost at Sea Station")],
        ["lost at sea", "lost at sea station", False, None],

        ["lost at sea", "las outside chest", False, has_sod & (has_sol | hard_logic)],
        ["lost at sea", "las cliff", False, hard_birds],
        ["las cliff", "lost at sea", False, None],
        ["las cliff", "las lobby", False, hard_logic | has_sol],
        ["las lobby", "las cliff", False, None],
        ["las 1", "las 2", False, has_boomerang],
        ["las 2", "las 1", False, None],
        ["las 2", "las 3", False, has_whirlwind],
        ["las 3", "las 2", False, None],
        ["las 3", "las 4", False, has_whip],
        ["las 4", "las 3", False, None],
        ["las 4", "las 4 door", False, has_bombs | hard_logic],
        ["las 4 door", "las 4", False, has_bombs],
        ["las 4 door", "las 5", False, has_bombs | hard_logic],
        ["las 5", "las 4 door", False, None],
        ["las 5", "las 5 door", False, has_boomerang & has_whip & (has_bombs | hard_logic)],
        ["las 5", "las 5 se", False, has_bombs | hard_logic],
        ["las 5", "las 5 sw", False, has_boomerang],
        ["las 5", "las 5 nw", False, has_whip],

        ["las 5 door", "las 6", True, None],
        ["las 6", "las event shield", False, None],
        ["las event shield", "las_event", False, None],
        ["las 6", "las loop event", False, None],

        ["las lobby", "las loop", False, has_soa],
        ["las loop", "las lobby", False, Has("_las6")],
        ["las loop", "las 1", False, None],
        ["las 6", "las loop", False, None],
        # ["las loop", "las 6", False, None],

        # ===== Fire Realm =====
        ["gorge tracks east", "fire realm", True, has_glyph("Fire") & has_tracks("Snow Realm Gorge")],
        ["blizzard temple tracks", "gorge tracks west", True, has_tracks("Snow Realm Gorge") & has_temple_tracks("Blizzard")],
        ["gorge tracks west", "gorge tracks east", True, has_tracks("Snow Realm Gorge")],

        ["blizzard temple tracks", "fire realm west", True, has_glyph("Fire") & has_temple_tracks("Blizzard")],
        ["snow realm source", "fire realm west", True, has_glyph("Fire") & has_source("Snow")],
        ["fire realm west entr", "fire realm west", True, has_glyph("Fire")],
        ["fire realm", "fire realm west entr", True, has_glyph("Fire")],

        ["fire realm", "fire source", True, has_glyph("Fire") & has_source("Fire")],
        ["mountain temple tracks", "fire source", True, has_temple_tracks("Mountain") & has_source("Fire")],
        ["mountain temple tracks", "fire realm", True, has_temple_tracks("Mountain") & has_glyph("Fire")],
        ["mountain temple tracks", "ends of the earth tracks", True, has_temple_tracks("Mountain") & has_tracks("Ends of the Earth")],
        ["mountain temple tracks", "disorientation tracks", True, has_temple_tracks("Mountain") & has_tracks("Disorientation Station")],
        ["fire realm", "disorientation tracks", True, has_glyph("Fire") & has_tracks("Disorientation Station")],
        ["fire realm", "sand connection", True, has_glyph("Fire") & has_tracks("Fire Realm Sand Portal")],
        ["mountain temple tracks", "dark ore mine tracks", True, has_temple_tracks("Mountain") & has_tracks("Dark Ore Mine")],
        ["mountain temple tracks", "snurglars", True, has_cannon],
        ["fire realm", "fire realm ferrus", False, ((has_temple_tracks("Marine") | has_source("Ocean")) & pickup_tracks) | (Has("_visit_oct") & pickup_visit)],
        ["fire realm ferrus", "icyspring", False, ool & vanilla_passengers],

        ["fire realm", "fire realm rabbits", False, has_net],
        ["mountain temple tracks", "mountain rabbits", False, has_net],
        ["fire source", "fire source rabbits", False, has_net],
        ["disorientation tracks", "disorientation rabbits", False, has_net],
        ["fire realm", "disorientation rabbits", False, has_net],
        ["ends of the earth tracks", "eote rabbits", False, has_net],
        ["fire source", "s mountain temple rabbit", False, has_net],
        ["mountain temple tracks", "s mountain temple rabbit", False, has_net],

        *get_portal_logic("forest cave tracks", "forest cave portal",
                          "fire realm", "fire realm portal",
                          "Forest Realm SW Cave", "Fire Glyph",
                          "Forest Cave to Goron Village", "_cave_portal"),
        *get_portal_logic("icyspring tracks", "icyspring portal",
                          "mountain temple tracks", "mountain temple portal",
                          "N Icy Spring", "Mountain Temple Tracks",
                          "Icy Spring to Mountain Temple", "_icyspring_portal"),

        # Goron Village
        ["fire realm", "fire realm (gv)", True, has_glyph("Fire")],
        ["goron village", "fire realm (gv)", False, None],
        ["fire realm (gv)", "goron village", False, has_glyph("Fire") | has_source("Fire")],
        ["fire source", "fire realm (gv)", True, has_source("Fire")],
        ["goron village", "visit goron village", False, None],

        ["goron village", "goron village shop", True, None],
        ["goron village", "goron village kagoron", False, Has("_visit_kagoron")],

        ["goron village", "goron field", True, None],
        ["goron field", "goron whip", False, has_whip],
        ["goron whip", "goron field north", False, None],
        ["goron field north", "mountain altar", True, None],
        ["mountain altar", "kagoron event", False, None],
        ["goron field north", "goron field", False, None],
        ["goron field north", "goron field ne", False, has_whip],
        ["goron whip", "goron field stamp station", False, has_stamp_book],
        ["goron field stamp station", "goron field stamp event", False, None],

        ["goron ice", "goron ice event", False, None],
        ["goron ice event", "pick up snow goron", False, pickup_passenger("Snow Glyph", "_visit_av")],
        ["goron ice event", "pick up city goron", False, pickup_passenger("Forest Glyph", "_visit_ct")],
        ["goron ice event", "gv kofu", False, has_passenger("Kofu", "_kofu")],
        ["goron ice event", "goron plaza", False, None],
        ["goron plaza", "goron village", False, None],

        ["goron plaza", "goron house 3 pots", True, None],
        ["goron plaza", "goron neighbour's house", True, None],
        ["goron plaza", "kofu's new house", True, None],
        ["goron plaza", "mouldy goron house", True, None],
        ["goron plaza", "goron elder's house", True, None],
        ["goron ice 2", "comfy goron's doorstep", False, None],
        ["comfy goron's doorstep", "comfy goron's house", True, None],

        ["goron elder's house", "valley sanc tunnel west", True, None],
        ["valley sanc tunnel west", "valley sanc tunnel east", False, has_whip],
        ["valley sanc tunnel east", "valley sanc tunnel west", False, None],
        ["valley sanc tunnel east", "goron village north", True, None],
        ["goron village north", "valley sanc", True, None],

        ["valley sanc", "valley sanc upper", None, has_boomerang],
        ["valley sanc upper", "valley sanc stamp station", False, has_stamp_book],
        ["valley sanc stamp station", "valley sanc stamp event", False, None],
        ["valley sanc upper", "valley sanc east", False, None],
        ["valley sanc east", "valley sanc", False, None],
        ["valley sanc east", "valley sanc door", False, has_sol],
        ["valley sanc door", "valley sanc sanc", True, None],
        ["valley sanc sanc", "valley sanc song", False, has_spirit_flute],

    ]

    if world.options.randomize_cargo == "no_cargo":
        goron_logic = [
            ["goron village", "goron ice", False, None],
            ["goron ice event", "goron ice 2", True, None]
        ]
    elif world.options.randomize_cargo.value in [1, 2]:
        goron_logic = [
            ["goron village kagoron", "goron ice", False, has_cargo("Mega Ice", "_buy_ice")],
            ["goron ice event", "goron ice 2", False, None],  # need to open from the other side still
            ["goron ice 2", "goron ice event", False, Has("_goron_ice_event")]
        ]
    else:
        goron_logic = [
            ["goron village kagoron", "goron ice", False, has_wagon & (
                Has("Cargo: Mega Ice", 2) | (
                    Has("Cargo: Mega Ice", 1) & ool))],
            ["goron ice event", "goron ice 2", False, has_wagon & (
                    Has("Cargo: Mega Ice", 3) | (
                    Has("Cargo: Mega Ice", 2) & ool))]
            ]
    overworld_logic += goron_logic
    overworld_logic += [

        # Goron Target Game
        ["fire realm", "goron target station", True, has_glyph("Fire")],
        ["goron target lobby", "gtr", False, has_cannon & Has("_goron_ice") & has_rupees(50)],
        ["goron target station", "goron target lobby", False, has_glyph("Fire")],
        ["goron target lobby", "goron target station", False, None],

        # Mountain Temple
        ["mountain temple tracks", "mountain temple door", False, None],
        ["fire source", "mountain temple door", False, None],
        ["mountain temple door", "mtt station", False, Has("Mountain Temple Snurglar Key", 3) | Has("Snurglar Keyring")],
        ["mtt station", "mountain temple lobby", False, has_temple_tracks("Mountain") | has_source("Fire")],
        ["mountain temple lobby", "mtt station", False, None],
        ["mtt station", "mountain temple tracks", False, has_temple_tracks("Mountain")],
        ["mtt station", "fire source", False, has_source("Fire")],

        ["mountain temple lobby", "mtt song statue", False, has_spirit_flute],
        ["mountain temple lobby", "mtt 1f", True, None],
        ["mtt 1f", "mtt 1f left", False, has_damage],
        ["mtt 1f left", "mtt 1f", False, None],

        ["mtt 1f left", "mtt 1f right", False, has_short_range],
        ["mtt 1f left", "mtt 2f left", True, None],
        ["mtt 1f right", "mtt 2f right", True, None],
        ["mtt 2f right", "mtt 2f chest", False, can_kill_bat],

        ["mtt 1f", "mtt 1f door puzzle", False, has_small_keys_er("Mountain Temple", 2, er=3) & Or(
            has_bombs, has_boomerang, hard_logic & (has_bow | has_sword_beam | has_whip)
        )],
        ["mtt 1f door puzzle", "mtt 1f door", False, None],
        ["mtt 1f left", "mtt 1f door", False, glitched_logic & has_boomerang & has_small_keys_er("Mountain Temple", 1, er=3)],
        ["mtt 1f left", "mtt 1f oob", False, glitched_logic & has_bombs],
        ["mtt 1f oob", "mtt 1f door", False, None],
        ["mtt 1f oob", "mtt 1f n", False, None],
        ["mtt 1f oob", "mtt 1f ne", False, None],
        ["mtt 1f door", "mtt 2f arena", True, None],

        ["mtt 2f arena", "mtt 2f post arena", False, has_good_damage],
        ["mtt 2f post arena", "mtt 2f ne", False, None],
        ["mtt 2f ne", "mtt 2f ne door", True, has_bow],
        ["mtt 2f ne door", "mtt 1f ne", True, None],
        ["mtt 1f ne", "mtt 1f n", False, has_bow & can_rotate_repeater],
        ["mtt 1f n", "mtt 1f ne", False, has_bow],
        ["mtt 1f ne", "mtt 1f n chest", False, has_bow],
        ["mtt 1f n", "mtt b1 n", True, None],

        ["mtt b1 n", "mtt b2 n", True, None],
        ["mtt b2 n", "mtt b2", False, has_bow | has_bombs | has_sword_beam | has_whip],
        ["mtt b2", "mtt b2 e", False, has_bow & has_whip],
        ["mtt b2 e", "mtt b2", False, has_whip],
        ["mtt b2 e", "mtt b2 se", False, has_boomerang],

        ["mtt b2 se", "mtt b1 arena", True, None],
        ["mtt b1 arena", "mtt b1 post arena", False, has_bow],
        ["mtt b1 post arena", "mtt b1 arena exit", False, None],
        ["mtt b1 arena exit", "mtt b2 sw", True, None],

        ["mtt b2 sw", "mtt b2 w", False, has_bow & can_rotate_repeater],
        ["mtt b2 w", "mtt b2", False, has_whip],
        ["mtt b2 w", "mtt b2 sw shortcut", False, None],
        ["mtt b2 sw shortcut", "mtt b2", False, has_whip],

        ["mtt b1 n", "mtt b1 cart", True, has_small_keys("Mountain Temple", 3, 1)],
        ["mtt b1 cart", "mtt b1 cart exit", False, has_bow],
        ["mtt b1 cart exit", "mtt b1 cart", False, None],
        ["mtt b1 cart exit", "mtt b1 stamp station", False, has_range & has_stamp_book],
        ["mtt b1 stamp station", "mtt b1 stamp event", False, None],
        ["mtt b1 cart exit", "mtt b2 s", True, None],
        ["mtt b2 s", "mtt b3", True, None],

        ["mtt b3", "mtt b3 ne", False, has_short_range],
        ["mtt b3 ne", "mtt b3 chest", False, has_whip],
        ["mtt b3 ne", "mtt b3 bk", False, has_whirlwind],
        ["mtt b3 ne", "mtt b3 n", False, None],
        ["mtt b3 n", "mtt b3 chest", False, hard_logic],
        ["mtt b3 n", "mtt b3 ne", False, has_whip],
        ["mtt b3 bk", "mtt b3 boss door", False, True_() & vanilla_boss_keys],
        ["mtt b3 boss door", "mtt b3 n", True, has_boss_key("Mountain Temple")],
        ["mtt b3 boss door", "mtt b4", True, None],

        ["mtt b4", "mtt blue warp", True, None],
        ["mtt blue warp", "mountain temple lobby", False, None],
        ["mtt blue warp", "mtt warp event", False, None],
        ["mountain temple lobby", "mtt blue warp", False, Has("_mtt_warp") | open_warps],

        ["mtt b4", "mtt pre vulcano", False, None],
        ["mtt pre vulcano", "mtt b4", False, can_kill_vulcano],
        ["mtt pre vulcano", "mtt vulcano", False, can_kill_vulcano],
        ["mtt vulcano", "event_vulcano", False, None],
        ["mtt vulcano", "goal_vulcano", False, None],

        # Disorientation Station
        ["disorientation tracks", "disorientation station station", True, has_tracks("Disorientation Station")],
        ["disorientation station", "disorientation station station", False, None],
        ["disorientation station station", "disorientation station", False, has_tracks("Disorientation Station")],
        ["disorientation station", "disorientation bird", False, hard_birds],
        ["disorientation bird", "disorientation top", False, None],
        ["disorientation top", "disorientation station", False, None],
        ["disorientation top", "disorientation gift", False, Has("_disorientation_chest")],
        ["d9", "disorientation sod", False, has_sod],
        ["disorientation sod", "disorientation event", False, None],
        ["d5", "disorientation top", True, None],

        ["d1", "d2", True, None],
        ["d3", "d2", True, None],
        ["d1", "d3", True, None],

        ["d4", "d5", True, None],
        ["d4", "d6", True, None],
        ["d6", "d5", True, None],

        ["d7", "d8", True, None],
        ["d9", "d8", True, None],
        ["d7", "d9", True, None],

        ["d1", "d4", True, None],
        ["d4", "d7", True, None],
        ["d3", "d6", True, None],
        ["d6", "d9", True, None],

        ["d2", "d5", True, None],
        ["d5", "d8", True, None],
        ["d8", "d2", True, None],

        # Ends of the Earth
        ["ends of the earth tracks", "ends of the earth station", True, has_tracks("Ends of the Earth")],
        ["ends of the earth station", "ends of the earth", False, has_tracks("Ends of the Earth")],
        ["ends of the earth", "ends of the earth station", False, None],

        ["ends of the earth", "eote 1", True, None],
        ["eote 1", "eote 2", True, None],
        ["eote 2", "eote 3", False, has_sand_wand],
        ["eote 3", "eote 2", False, None],
        ["eote 3", "eote 4", False, has_sand_wand],
        ["eote 4", "eote 3", False, None],
        ["eote 4", "eote 4 chest", False, has_sand_wand],
        ["eote 1 chest", "eote 4 chest", True, None],
        ["eote 1 chest", "eote 1", False, None],

        ["ends of the earth", "eote 5", True, None],
        ["eote 5", "eote 6", True, None],
        ["eote 6", "eote 7", False, has_sand_wand],
        ["eote 7", "eote 6", False, None],
        ["eote 7", "eote 8", False, has_sand_wand],
        ["eote 8", "eote 7", False, None],
        ["eote 8", "eote 8 chest", False, has_sand_wand],
        ["eote 5 chest", "eote 8 chest", True, None],
        ["eote 5 chest", "eote 5", False, None],

        ["ends of the earth", "eote 9", True, None],
        ["eote 9", "eote a", True, None],
        ["eote a", "eote b", False, has_sand_wand],
        ["eote b", "eote a", False, None],
        ["eote b", "eote c", False, has_sand_wand],
        ["eote c", "eote b", False, None],
        ["eote c", "eote c chest", False, has_sand_wand],
        ["eote 9 chest", "eote c chest", True, None],
        ["eote 9 chest", "eote 9", False, None],

        # ===== Sand Realm =====
        ["ocean realm source", "sand realm", True, has_source("Ocean") & has_tracks("Sand Realm")],
        ["sand realm", "sand connection south", True, has_tracks("Sand Realm") & has_tracks("Fire Realm Sand Portal")],
        ["sand connection south", "sand connection mid", True, has_tracks("Sand Realm") & has_tracks("Fire Realm Sand Portal")],
        ["sand connection", "sand connection mid", True, has_tracks("Sand Realm") & has_tracks("Fire Realm Sand Portal")],

        ["sand realm exit", "sand restoration rocktite", False, has_temple_tracks("Desert")],
        ["sand restoration rocktite", "sand realm exit", False, has_temple_tracks("Desert")],
        ["sand realm", "sand realm exit", True, has_temple_tracks("Desert") & has_tracks("Sand Realm")],
        ["sand restoration rocktite", "sand restoration", True,  has_temple_tracks("Desert") & (has_cannon | [OptionFilter(SpiritTracksShuffleTrainTransitions, 0, "ne")])],
        ["sand restoration south exit", "sand restoration south", True, has_temple_tracks("Desert")],
        ["sand restoration mid", "sand restoration south exit", True, has_temple_tracks("Desert")],
        ["sand restoration mid", "sand restoration", True, has_temple_tracks("Desert")],

        ["sand realm", "sand realm rabbits", False, has_net],
        ["sand restoration", "sand restoration rabbits", False, has_net],
        ["sand restoration south", "sand restoration south rabbits", False, has_net],
        ["sand connection", "sand connection rabbit", False, has_net],

        ["sand restoration south", "sand restoration portal", False, has_cannon],
        ["sand connection", "sand connection portal loc", False, has_cannon],
        ["sand restoration portal", "sand restoration portal event", False, None],
        ["sand connection portal loc", "sand connection portal event", False, None],

        *get_portal_logic("sand restoration south", "desert temple portal",
                          "sand realm", "sand realm portal",
                          "Desert Temple Tracks", "Sand Realm",
                          "Desert Temple to Sand Realm", "_dt_portal"),
        *get_portal_logic("sand connection", "sand connection portal",
                          "ocean temple tracks", "ocean temple portal",
                          "Fire Realm Sand Portal", "Marine Temple Tracks",
                          "Sand Valley to Marine Temple", "_sand_portal"),

        # ===== Sand Sanc =====
        ["sand realm", "sand sanc station", True, has_tracks("Sand Realm")],
        ["sand sanc station", "sand sanc", False, has_tracks("Sand Realm")],
        ["sand sanc", "sand sanc station", False, None],
        ["sand sanc sanc", "sand sanc song", False, has_spirit_flute],
        ["sand sanc cuccos", "sand sanc stamp station", False, has_stamp_book],
        ["sand sanc cuccos", "sand sanc cuccos event", False, None],
        ["sand sanc stamp station", "sand sanc stamp event", False, None],
        ["sand sanc", "sand sanc sand wand", False, has_sand_wand],
        ["sand sanc", "sand sanc tunnel", True, None],
        ["sand sanc sanc", "sand sanc tunnel", True, None],
    ]

    if world.options.randomize_cargo.value == 0:
        sand_sanc_logic = None
    elif world.options.randomize_cargo.value in [1, 2]:
        sand_sanc_logic = has_cargo("Cuccos", "_buy_cuccos")
    else:
        sand_sanc_logic = (has_wagon & (
                Has("Cargo: Cuccos (5)", 3) | (
                    Has("Cargo: Cuccos (5)", 1) & ool
                )
            )
        )
    overworld_logic.append(["sand sanc", "sand sanc cuccos", False, sand_sanc_logic])

        # ===== Desert Temple =====
    overworld_logic += [
        ["sand restoration south", "desert temple door", False, has_cannon],
        ["desert temple door", "desert temple station", False, None],
        ["desert temple station", "sand restoration south", False, has_temple_tracks("Desert")],
        ["desert temple station", "desert temple lobby", False, has_temple_tracks("Desert")],
        ["desert temple lobby", "desert temple station", False, None],

        ["desert temple lobby", "dt", True, None],
        ["dt", "dt sw", False, has_sand_wand],
        ["dt sw", "dt 1f nw", False, has_bow],
        ["dt", "dt 1f n", False, has_bow],

        ["dt sw", "dt 1f n earthquake", False, has_bow],

        ["dt", "dt 2f west", False, has_small_keys("Desert Temple", 2, 1)],
        ["dt 2f west", "dt", False, None],
        ["dt 2f west", "dt 2f", False, None],
        ["dt 2f", "dt 2f sw", False, has_sand_wand],
        ["dt 2f sw", "dt 2f west", False, None],
        ["dt 2f", "dt 3f", True, None],
        ["dt 3f", "dt 3f chest", False, has_damage],

        ["dt", "dt b1 stairs", False, has_sand_wand],
        ["dt b1 stairs", "dt", False, None],
        ["dt b1 stairs", "dt b1", False, has_small_keys("Desert Temple", 2, 1) & has_sand_wand],
        ["dt b1", "dt stamp station", False, has_stamp_book],
        ["dt stamp station", "dt stamp event", False, None],
        ["dt b1", "dt b1 s", False, has_range | has_bombs],
        ["dt b1 s", "dt b1 damage", False, has_damage],
        ["dt b1", "dt b1 boss door", False, glitched_logic & has_bombs & has_sword],
        ["dt b1 boss door", "dt b2 s", True, None],
        ["dt b1 boss door", "dt b1 mid", False, has_boss_key("Desert Temple") & has_sand_wand],
        ["dt b1 s", "dt b1 stairs", False, None],
        ["dt b1 s", "dt b1 mid", False, has_sand_wand],

        ["dt b1 damage", "dt b1 boss door", False, None]
            if world.options.randomize_boss_keys.value == 0
            else ["dt b1 s", "dt b1 boss door", False, has_boss_key("Desert Temple") & has_sand_wand],
        ["dt b2 s", "dt b2 n", False, has_sand_wand],
        ["dt b2 n", "dt b2 s", False, None],
        ["dt b2 n", "dt pre skeldritch", False, None],
        ["dt pre skeldritch", "dt b2 n", False, has_sand_wand & has_good_damage],
        ["dt pre skeldritch", "dt skeldritch", False, has_sand_wand & has_good_damage],
        # Whip is not good enough damage
        ["dt skeldritch", "skeldritch event", False, None],
        ["dt skeldritch", "skeldritch goal", False, None],

        ["dt b2 n", "dt blue warp", True, None],
        ["dt blue warp", "desert temple lobby", False, None],
        ["dt blue warp", "dt warp event", False, None],
        ["desert temple lobby", "dt blue warp", False, Has("_dt_warp") | open_warps],

        # ===== Dark ore mine =====
        ["sand restoration", "dark ore mine tracks", False, has_tracks("Dark Ore Mine") & soft_cannon],
        ["dark ore mine tracks", "sand restoration", False, has_temple_tracks("Desert") & has_cannon],
        ["dark ore mine tracks", "dark ore mine station", True, has_tracks("Dark Ore Mine")],
        ["dark ore mine station", "dark ore mine", False, has_tracks("Dark Ore Mine")],
        ["dark ore mine", "dark ore mine station", False, None],

        ["dark ore tunnels left", "dark ore mine sod", False, has_sod],
        ["dark ore mine", "dark ore tunnels left", True, None],
        ["dark ore mine", "dark ore tunnels right", True, None],
        ["dark ore mine", "dark ore tunnels mid", True, None],
        ["dark ore tunnels left", "dark ore tunnels mid", True, None],
        ["dark ore tunnels right", "dark ore tunnels mid", True, None],

        # ===== Dark Realm =====
        ["dark realm portal", "dark realm trains", False, has_dungeon_rewards],
        ["dark realm trains", "demon train", False, None],
        ["demon train", "cole fight", False, has_cannon],
        ["cole fight", "malladus 1", False, can_fight_malladus],
        ["malladus 1", "malladus 2", False, has_spirit_flute & has_sword],
        ["malladus 2", "malladus goal", False, can_fight_malladus],
        # ["dark realm portal", "malladus goal", False, None],
        ["malladus 2", "malladus event", False, can_fight_malladus],

        ["forest realm", "beedle", False, has_source("Snow")],
        ["snow realm", "beedle", False, has_source("Snow")],
        ["blizzard temple tracks", "beedle", False, has_source("Snow")],
        ["snow realm source", "beedle", False, has_source("Snow")],
        ["fire realm", "beedle", False, has_source("Snow")],
        ["mountain temple tracks", "beedle", False, has_source("Snow")],
        ["ocean realm", "beedle", False, has_source("Snow")],
        ["ocean temple tracks", "beedle", False, has_source("Snow")],
        ["sand realm", "beedle", False, has_source("Snow")],
        ["beedle", "beedle joe", False, has_passenger("Joe", "_joe")]
    ]

    if world.options.endgame_scope.value == 5:
        overworld_logic += [
            ["dark realm trains", "malladus goal", False, None],  # enter dark realm goal
            ["dark realm trains", "dark realm event", False, None]
        ]

    required_rupees = world.get_required_rupees()

    overworld_logic += [
        # Shops
        ["snowfall supermarket", "snow sanc shop", False, has_rupees(required_rupees)],

        ["beedle", "beedle shop", False, has_rupees(required_rupees)],
        ["beedle shop", "beedle shop bombs", False, has_bombs],

        ["uriko's shop", "mayscore shop", False, has_rupees(required_rupees)],
        ["shitate's shop", "castle town shop", False, has_rupees(required_rupees)],
        ["kogane's shop", "papuzia shop", False, has_rupees(required_rupees)],
        ["papuzia shop", "papuzia shop arrows", False, has_bow],
        ["papuzia shop", "papuzia shop bombs", False, has_bombs],
        ["linebeck's shop", "trading post shield", False, has_rupees(required_rupees)],
        ["goron village shop", "goron shop", False, has_rupees(required_rupees)],
        ["goron shop", "goron shop bombs", False, has_bombs],
        ["goron shop", "goron shop bow", False, has_bow],

        ["castle town", "castle town buy cuccos", False, has_wagon & has_rupees(required_rupees)],
        ["mayscore", "mayscore lumber", False, has_wagon & has_rupees(required_rupees)],
        ["icyspring noko", "icyspring ice", False, has_wagon]
            if world.options.randomize_cargo in [2, 3] else
            ["icyspring noko event", "icyspring ice", False, has_wagon & has_rupees(required_rupees)], #  You can bully noko for free ice
        ["papuzia village", "papuzia buy fish", False, has_wagon & has_rupees(required_rupees)],
        ["wise one's house", "wise one buy vessel", False, has_wagon & has_rupees(required_rupees)],
        ["goron field", "goron steel", False, has_wagon & has_rupees(required_rupees) & Has("_goron_ice")],
        ["dark ore tunnels mid", "dark ore mine ore", False, has_wagon & has_rupees(required_rupees)],

        # Total rabbits
        ["menu", "total rabbits", False, has_net],
    ]

    # Total rabbit events
    if world.is_ut and "rabbits" in world.options.extra_events.value and world.options.rabbitsanity.value in [3, 4]:
        overworld_logic += [
            ["forest realm rabbits", "forest realm rabbits event", False, None],
            ["forest ocean shortcut rabbit", "forest ocean shortcut rabbit event", False, None],
            ["e mayscore rabbits", "e mayscore rabbits event", False, None],
            ["sw trading post rabbit", "sw trading post rabbit event", False, None],
            ["forest realm rabbits", "forest realm rabbits event 2", False, None],
            ["s rabbit haven rabbits", "s rabbit haven rabbits event", False, None],
            ["wt rabbit", "wt rabbit event", False, None],
            ["nr rabbit haven rabbit", "nr rabbit haven rabbit event", False, None],
            ["e mayscore rabbits", "e mayscore rabbits event 2", False, None],
            ["s rabbit haven rabbits", "s rabbit haven rabbits event 2", False, None],

            ["fire source rabbits", "fire source rabbits event", False, None],
            ["disorientation rabbits", "disorientation rabbits event", False, None],
            ["eote rabbits", "eote rabbits event", False, None],
            ["mountain rabbits", "mountain rabbits event", False, None],
            ["mountain rabbits", "mountain rabbits event 2", False, None],
            ["mountain rabbits", "mountain rabbits event 3", False, None],
            ["s mountain temple rabbit", "s mountain temple rabbit event", False, None],
            ["mountain rabbits", "mountain rabbits event 4", False, None],
            ["fire realm rabbits", "fire realm rabbits event", False, None],
            ["fire realm rabbits", "fire realm rabbits event 2", False, None],
            ["sand restoration rabbits", "sand restoration rabbits event", False, None],
            ["sand restoration rabbits", "sand restoration rabbits event 2", False, None],
            ["sand restoration rabbits", "sand restoration rabbits event 3", False, None],
            ["sand connection rabbit", "sand connection rabbit event", False, None],

            ["las rabbit", "las rabbit event", False, None],
            ["ocean rabbits", "ocean rabbits event", False, None],
            ["ocean source rabbits", "ocean source rabbits event", False, None],
            ["pirate rabbit", "pirate rabbit event", False, None],
            ["ocean rabbits", "ocean rabbits event 2", False, None],
            ["ocean rabbits", "ocean rabbits event 3", False, None],
            ["ocean portal rabbits", "ocean portal rabbits event", False, None],
            ["ocean rabbits", "ocean rabbits event 4", False, None],
            ["ocean rabbits", "ocean rabbits event 5", False, None],
            ["ocean rabbits", "ocean rabbits event 6", False, None],
            ["sand realm rabbits", "sand realm rabbits event", False, None],
            ["sand realm rabbits", "sand realm rabbits event 2", False, None],
            ["sand realm rabbits", "sand realm rabbits event 3", False, None],
            ["sand realm rabbits", "sand realm rabbits event 4", False, None],
            ["sand restoration south rabbits", "sand restoration south rabbits event", False, None],
            ["sand restoration south rabbits", "sand restoration south rabbits event 2", False, None],

            ["snow realm early blizzard rabbits", "snow realm early blizzard rabbits event", False, None],
            ["snow realm blizzard rabbits", "snow realm blizzard rabbits event", False, None],
            ["snow realm rabbits", "snow realm rabbits event", False, None],
            ["snow realm blizzard rabbits", "snow realm blizzard rabbits event 2", False, None],
            ["blizzard temple tracks rabbits", "blizzard temple tracks rabbits event", False, None],
            ["snowdrift station rabbit", "snowdrift station rabbit event", False, None],
            ["icyspring rabbits", "icyspring rabbits event", False, None],
            ["icyspring rabbits", "icyspring rabbits event 2", False, None],
            ["snow realm early blizzard rabbits", "snow realm early blizzard rabbits event 2", False, None],
            ["snow realm early blizzard rabbits", "snow realm early blizzard rabbits event 3", False, None],
        ]

    if world.is_ut and "shortcuts" in world.options.extra_events.value:
        overworld_logic += [
            ["wt 1f","wt 1f north", False, CanReachRegion("wt 1f north")],
            ["wt 2f north", "wt 2f ne arena", False, CanReachRegion("wt 2f ne arena") & has_whirlwind],

            ["bt 1f e shortcut","bt 1f", False, CanReachRegion("bt 1f") & can_ring_bell],
            ["bt b1 e","bt b1 se", False, CanReachRegion("bt b1 se") & has_whirlwind],
            ["bt 1f", "bt 1f ne", False, CanReachRegion("bt 1f ne") & has_boomerang],
            # ["bt 1f n shortcut", "bt 1f", False, CanReachRegion("bt 1f nw bell") & has_boomerang],
            ["bt 1f", "bt 1f nw", False, CanReachRegion("bt 1f nw") & has_boomerang],

            ["oct 3f arena","oct 3f south", False, CanReachRegion("oct 3f south") & has_whip],
            ["oct 4f west","oct 4f north", False, CanReachRegion("oct 4f north") & has_whip],
            ["oct 4f south","oct 4f west", False, CanReachRegion("oct 4f west") & has_whip],
            ["oct 5f nw","oct 5f", False, CanReachRegion("oct 5f") & has_whip],
            ["oct 5f se","oct 5f s", False, CanReachRegion("oct 5f s") & has_whip],

            # ["mtt 1f right","mtt 1f", False, CanReachRegion("mtt 1f") & has_short_range],  platform does not stay after exiting dungeon
            ["mtt 1f door","mtt 1f", False, CanReachRegion("mtt 1f door puzzle")],
            ["mtt 2f ne","mtt 2f arena", False, CanReachRegion("mtt 2f post arena")],
            ["mtt b2","mtt b2 n", False, CanReachRegion("mtt b2 n") & (has_bow | has_bombs | has_sword_beam | has_whip)],
            ["mtt b2 se","mtt b2 e", False, CanReachRegion("mtt b2 e") & has_boomerang & has_whip & has_bow],
            ["mtt b2","mtt b2 sw shortcut", False, CanReachRegion("mtt b2 sw shortcut") & can_rotate_repeater & has_bow],
            ["mtt b1 arena exit", "mtt b1 arena", False, CanReachRegion("mtt b1 arena") & has_bow],

            ["dt b1 mid", "dt b1 s", False, CanReachRegion("dt b1 s")],
            ["dt b1 stairs", "dt b1 s", False, CanReachRegion("dt b1 s")],

            ["island sanc", "island sanc shortcut", False, CanReachRegion("island sanc shortcut")],
            ["tower tunnel 2f door", "tower tunnel 2f north", False, CanReachRegion("tower tunnel 2f north") & can_kill_bat],
            ["valley sanc door", "valley sanc east", False, CanReachRegion("valley sanc east") & has_sol],
        ]

    # Generate rabbit total items
    if world.options.rabbitsanity in ["on_total", "both"]:
        # print(f"Creating total rabbit logic")
        overworld_logic += [
            [f"total rabbits", f"{rabbit} Rabbit Count {i}", False, caught_rabbits(rabbit, i)
             ] for i in range(1, 11) for rabbit in ["Grass", "Snow", "Ocean", "Mountain", "Sand"]
        ]

    return overworld_logic


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name

def create_connections(world: "SpiritTracksWorld", player: int, origin_name: str, options):
    all_logic = [
        make_overworld_logic(player, origin_name, world)
    ]

    if world.is_ut:
        # from .data.Constants import region_aliases
        from .data.Regions import REGIONS
        # alias_logic = []
        # for region, aliases in region_aliases.items():
        #     for alias in aliases:
        #         alias_logic.append([region, alias, False, None])
        # all_logic.append(alias_logic)
        all_logic.append([[entr.entrance_region, entr.name, False, None] for entr in ENTRANCES.values() if entr.name not in REGIONS])


    entrance_lookup = {(e.entrance_region, e.exit_region): e for e in ENTRANCES.values()}
    world.set_completion_rule(Has("_beaten_game"))

    def create_entrance(r1, r2, rule_):
        entrance_data: "STTransition" or None = entrance_lookup.get((r1.name, r2.name), None)
        name = entrance_data.name if entrance_data else None

        entrance = r1.connect(r2, name)
        if rule_ is not None:
            # print(f"Setting rule {entrance} {rule_}")
            world.set_rule(entrance, rule_)

        if entrance_data:
            # print(f"Creating connection {r1} -> {r2} | {entrance_data.name} {rule_}")
            rando_type_bool = entrance_data.two_way
            entrance.randomization_type = EntranceType.TWO_WAY if rando_type_bool else EntranceType.ONE_WAY
            entrance.randomization_group = entrance_data.direction | entrance_data.category_group | entrance_data.island
            world.valid_entrances.append(entrance)

    # Create connections
    # print(f"Creating entrances: ")
    for logic_array in all_logic:
        for entr_data in logic_array:
            if entr_data is None:
                continue

            reg1, reg2, is_two_way, rule = entr_data

            region_1 = world.get_region(reg1)
            region_2 = world.get_region(reg2)

            create_entrance(region_1, region_2, rule)
            if is_two_way:
                create_entrance(region_2, region_1, rule)
