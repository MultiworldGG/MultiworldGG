from BaseClasses import MultiWorld, Item, EntranceType, Entrance
from .data.Rules import *
from .data.Entrances import ENTRANCES
from .Subclasses import STTransition


def make_overworld_logic(player: int, origin_name: str, world):
    tower_section_lookup = world.tower_section_lookup
    overworld_logic = [

        # ====== Outset Village ==============

        #[region 1, region 2, two-directional, logic requirements],
        ["outset village", "outset village stamp book", False, Has("_picked_up_alfonzo")],
        ["outset village", "outset village stamp station", False, has_stamp_book],
        ["outset village", "outset village trees", False, has_sod],
        ["outset village", "forest realm", False, has_train],

        # ========= Forest Realm ==========

        ["forest realm", "forest realm se portal track", False, Has("Forest Realm SE Portal Tracks")],
        ["forest realm", "forest realm rabbits", False, has_net],
        ["forest realm", "wtt", False, has_temple_tracks("Wooded")],
        ["forest realm", "forest source", False, has_source("Forest")],
        ["forest realm", "w castle town tracks", False, Has("W Castle Town Tracks")],
        ["forest realm", "n castle town tracks", False, Has("N Castle Town Tracks")],
        ["wtt", "snow realm", True, has_temple_tracks("Wooded") & has_glyph("Snow")],
        ["forest realm", "snow realm", False, has_portal("Hyrule Castle to Anouki Village", False) & has_glyph("Snow")],
        ["forest realm", "dark realm portal", True, has_compass],

        # cave
        ["forest realm", "forest cave tracks", True, Has("Forest Realm SW Cave Tracks")],
        ["forest cave tracks", "w forest tracks", True, Has("Forest Realm SW Cave Tracks") & Has("W Forest Realm Tracks")],
        ["w forest tracks", "snow realm", True, has_glyph("Snow") & Has("W Forest Realm Tracks")],
        ["w forest tracks", "wtt", True, has_temple_tracks("Wooded") & Has("W Forest Realm Tracks")],

        # Rabbits
        ["forest realm rabbits", "forest ocean shortcut rabbit", False, Has("Forest Realm Ocean Shortcut Tracks")],
        ["forest realm rabbits", "e mayscore rabbits", False, Has("E Mayscore Bridge Tracks")],
        ["forest realm se portal track", "sw trading post rabbit", False, has_net],
        ["forest realm rabbits", "sw trading post rabbit", False, has_glyph("Ocean") & hard_logic],
        ["wtt", "wt rabbit", False, has_net],
        ["forest source", "wt rabbit", False, has_net],
        ["w forest tracks", "s rabbit haven rabbits", False, has_net],
        ["snow realm rabbits", "nr rabbit haven rabbit", False, None],

        # Snow bridge
        ["w castle town tracks", "snow bridge", True, Has("W Castle Town Tracks") & Has("Snow Realm Bridge Tracks")],
        ["n castle town tracks", "snow bridge", True, Has("N Castle Town Tracks") & Has("Snow Realm Bridge Tracks")],
        ["wtt", "snow bridge", True, has_temple_tracks("Wooded") & Has("Snow Realm Bridge Tracks")],
        ["snow bridge", "snow realm", True, has_glyph("Snow") & Has("Snow Realm Bridge Tracks")],
        ["snow bridge", "snow realm source", True, has_source("Snow") & Has("Snow Realm Bridge Tracks")],

        # # ======== Castle Town =========

        ["forest realm", "castle town", True, None],
        ["castle town", "pick up alfonzo", False, has_glyph("Snow")],
        ["pick up alfonzo", "alfonzo event", False, None],
        ["castle town", "castle town wall", False, has_bombs],
        ["castle town wall", "castle town stamp station", False, has_stamp_book],
        ["castle town wall", "castle town cuccos", False, ct_cuccos],

        ["castle town", "teao 1", False, has_sword & has_whirlwind & has_source("Forest")],
        ["teao 1", "teao 2", False, And(has_source("Ocean"), has_boomerang, has_whip)],

        ["teao 2", "teao 3", False, And(has_source("Sand"), has_bow, has_sand_wand)],

        # # ======== Hyrule Castle =========

        ["castle town", "hyrule castle", False, None],
        ["hyrule castle", "hyrule castle sword minigame", False, has_sword & has_source("Snow")],

        # # ======== ToS Tunnel =========

        ["hyrule castle", "tower tunnel", False, None],
        ["tower tunnel", "tower tunnel block chest", False, can_kill_bat_pit | hard_logic],
        ["tower tunnel", "tower tunnel 2f chest", False, has_small_keys("Tunnel to ToS", 1)],

        # # ========== ToS ===================

        ["forest realm", "tos", True, can_enter_tos],
        ["tos", "tos 1f", True, None],
        ["tos", "tos 2", False, can_enter_tos_section(2)],
        ["tos", "tos 3", False, can_enter_tos_section(3)],
        ["tos", "tos 4", False, can_enter_tos_section(4)],
        ["tos", "tos 5", False, can_enter_tos_section(5)],


        ["tos 1f", "tos 1f chest", False, has_range | has_sword_beam],
        ["tos 1f", "tos 1f switch", False, can_kill_bat | can_possess_phantom(1, tower_section_lookup)],  # Phantom can hit switch
        ["tos 1f", "tos 2f", False, can_possess_phantom(1, tower_section_lookup) | vanilla_tears],
        ["tos 2f", "tos 2f raised chests", False, has_whirlwind],
        ["tos 2f", "tos 2f bomb wall", False, has_bombs],
        ["tos 2f", "tos 3f rail map", False, None],
        ["tos 3f rail map", "goal_forest_glyph", False, None],
        ["tos 3f rail map", "event_3f", False, None],

        ["tos 2", "tos 4f", True, None],
        ["tos 4f", "tos 4f whirlwind", False, has_whirlwind],
        ["tos 4f", "tos 5f phantom", False, can_possess_phantom(2,tower_section_lookup) | (vanilla_tears & has_whirlwind)],
        ["tos 5f phantom", "tos 5f spinnit key", False, has_whirlwind],
        ["tos 5f spinnit key", "tos 5f alt path", False, has_boomerang],
        ["tos 5f alt path", "tos 5f secret chest", False, has_bombs],
        ["tos 5f alt path", "tos 4f ne chest", False, has_bombs],  # needs whirlwind and boomerang to get here
        ["tos 5f alt path", "tos 6f chests", False, None],  # geozards only need sword + phantom
        ["tos 5f spinnit key", "tos 6f key", False, has_small_keys("ToS 2", 1)],  # already have whirlwind
        ["tos 6f key", "tos 7f rail map", False, has_small_keys("ToS 2", 2)],
        ["tos 7f rail map", "goal_snow_glyph", False, None],
        ["tos 7f rail map", "event_7f", False, None],

        ["tos 3", "tos 8f", True, None],
        ["tos 8f", "tos 8f bombs", False, has_bombs],
        ["tos 8f", "tos 9f phantom", False, vanilla_tears | can_possess_phantom(3, tower_section_lookup)], #
        ["tos 9f phantom", "tos 9f nw", False, has_whirlwind],
        ["tos 9f phantom", "tos 11f", False, has_damage],
        ["tos 11f", "event_12f", False, None],

        ["tos 4", "tos 13f", True, None],
        ["tos 13f", "tos 13f whip", False, has_whip],
        ["tos 13f", "tos 13f boomerang", False, has_boomerang],
        ["tos 13f", "tos 14f east", False, has_small_keys("ToS 4", 3) | (vanilla_tears & has_small_keys("ToS 4", 2))],
        ["tos 13f", "tos 13f phantom", False, can_possess_phantom(4, tower_section_lookup) | (vanilla_tears & has_whip & has_small_keys("ToS 4", 2))],
        ["tos 13f phantom", "tos 13f phantom whip", False, has_whip],
        ["tos 13f phantom", "tos 14f west", False, has_small_keys("ToS 4", 4)],

        ["tos 14f east", "tos 14f phantom", False, can_possess_phantom(4, tower_section_lookup) | (vanilla_tears & has_whip)],
        ["tos 14f east", "tos 15f", False, None],
        ["tos 15f", "tos 16f", False, (has_range | has_sword_beam) & has_whirlwind & has_small_keys("ToS 4", 3)],
        ["tos 16f", "event_17f", False, None],
        ["tos 16f", "tos 16f bombs", False, has_bombs],

        ["tos 5", "tos 18f", True, None],
        ["tos 18f", "tos 18f whip", False, has_whip],
        ["tos 18f", "tos 19f", False, has_small_keys("ToS 5", 1)],
        ["tos 18f", "tos 18f phantom", False, can_possess_phantom(5, tower_section_lookup)],

        ["tos 19f", "tos 19f south", False, has_bow & (has_boomerang | (can_possess_phantom(5, tower_section_lookup) & can_rotate_repeater))],
        ["tos 19f south", "tos 20f tear", False, has_boomerang | has_sword_beam],
        ["tos 19f", "tos 19f center", False, can_possess_phantom(5, tower_section_lookup) | (vanilla_tears & has_bow & has_boomerang)],
        ["tos 19f center", "tos 19f center chest", False, has_bow & (has_boomerang | has_sword_beam)],
        ["tos 19f center", "tos 18f phantom", False, None],
        ["tos 19f center", "tos 20f", False, has_small_keys("ToS 5", 2)],

        ["tos 20f", "tos 19f center 2", False, has_bow & can_rotate_repeater],
        ["tos 20f", "tos 22f", False, has_bow & can_rotate_repeater & has_whip],
        ["tos 22f", "tos staven", False, has_sword],
        ["tos staven", "event_staven", False, None],

        ["tos staven", "tos summit lower", True, None],
        ["tos summit lower", "tos summit", True, None],
        ["tos summit", "tos stamp stand", False, has_stamp_book],
        ["tos summit", "tos 6", False, has_bow_of_light],
        ["tos 30f", "tos 6", True, None],

        ["tos 30f", "tos 30f bomb wall", False, has_bombs],
        ["tos 30f", "tos 29f", False, can_possess_phantom(6, tower_section_lookup) & has_boomerang & has_whirlwind],
        ["tos 29f", "tos 29f sand wand", False, has_sand_wand],
        ["tos 29f sand wand", "tos 29f se", False, has_bow_of_light],

        ["tos 29f se", "tos 27f", False, has_small_keys("ToS 6", 3)],
        ["tos 27f", "tos 24f", False, has_whip],
        ["tos 24f", "event_24f", False, None],

        # # ======== Mayscore =========

        ["forest realm", "mayscore", False, None],
        ["mayscore", "mayscore stamp station", False, has_stamp_book],
        ["mayscore", "mayscore whip chest", False, has_whip],
        ["mayscore", "mayscore leaves", False, has_whirlwind],

        # # ======== Forest Sanctuary =========

        ["forest realm", "fos", False, None],
        ["fos", "fos stamp station", False, has_stamp_book],
        ["fos", "fos song statue", False, has_spirit_flute],
        ["fos", "fos chest", False, has_cuccos],

        # # ======== Wooded Temple =========

        ["wtt", "wt", False, None],
        ["forest source", "wt", False, None],
        ["wt", "wt stamp station", False, has_stamp_book & (has_whirlwind | hard_logic)],
        ["wt", "wt song statue", False, has_spirit_flute],
        ["wt", "wt 1f enemy chest", False, has_damage],
        ["wt 1f enemy chest", "wt 1f key", False, has_whirlwind],
        ["wt 1f enemy chest", "wt 2f enemy chest", False, None],
        ["wt 1f enemy chest", "wt 2f poison chest", False, has_whirlwind | hard_logic],
        ["wt", "wt 1f switch chest", False, has_whirlwind | hard_logic],
        ["wt", "wt 2f left", False, can_kill_bubble & has_small_keys("Wooded Temple", 1)],
        ["wt 2f left", "wt 3f chestnut chest", False, has_range_objects | has_sword_beam],
        ["wt 2f left", "wt 3f", False, has_small_keys("Wooded Temple", 2)],
        ["wt 3f", "wt 3f se chest", False, has_whirlwind | hard_logic],
        ["wt 3f", "wt stagnox", False, has_sword & has_whirlwind],
        ["wt stagnox", "goal_stagnox", False, None],
        ["wt stagnox", "event_stagnox", False, None],

        # # ============ Trading Post =============

        ["forest realm", "trading post", False, has_glyph("Ocean")],
        ["trading post", "trading post light song statue", False, has_spirit_flute],
        ["trading post", "trading post chest", False, (has_range | has_sword_beam) & has_sod & (has_sol | hard_logic)],
        ["trading post", "trading post stamp station", False, has_bombs & has_stamp_book],
        ["trading post", "linebeck trading", False, Has("Treasure: Regal Ring")],
        ["trading post", "trading post leaves", False, has_whirlwind],

        # # ========== Rabbit Haven ========

        ["snow realm", "rabbit haven", True, has_glyph("Snow")],
        ["rabbit haven", "rabbit haven 5 rabbits", False, has_total_rabbits(5)],
        ["rabbit haven", "rabbit haven 10 forest rabbits", False, has_rabbit_items("Grass", 10)],
        ["rabbit haven", "rabbit haven 10 snow rabbits", False, has_rabbit_items("Snow", 10)],

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # # ============ Snow Realm ===============

        ["snow realm", "blizzard temple tracks", True, has_temple_tracks("Blizzard") & has_glyph("Snow")],
        ["snow realm", "snow realm rabbits", False, has_net],
        ["blizzard temple tracks", "blizzard temple tracks rabbits", False, has_net],
        ["blizzard temple tracks rabbits", "snow realm blizzard rabbits", False, has_source("Snow")],
        ["blizzard temple tracks rabbits", "snow realm early blizzard rabbits", False, has_source("Snow") | hard_logic],

        ["blizzard temple tracks rabbits", "snowdrift station rabbit", False, Has("Snowdrift Station Tracks")],
        ["blizzard temple tracks", "icyspring tracks", True, Has("N Icy Spring Tracks")],
        ["icyspring tracks", "icyspring rabbits", False, has_net],

        ["forest realm se portal track", "blizzard temple tracks", False, has_temple_tracks("Blizzard") & has_portal("Trading Post to E Snow Realm", True)],
        ["blizzard temple tracks", "forest realm se portal track", False, Has("Forest Realm SE Portal Tracks") & has_portal("Trading Post to E Snow Realm", False)],
        ["tos", "snow realm source", True, has_source("Snow") & can_enter_tos],
        ["snow realm source", "blizzard temple tracks", True, has_source("Snow") & has_temple_tracks("Blizzard")],

        # ======== Anouki Village ========

        ["snow realm", "anouki village", False, None],
        ["anouki village", "anouki village stamp station", False, has_stamp_book],
        ["anouki village", "anouki village song statue", False, has_spirit_flute],
        ["anouki village", "anouki village bomb cave chest", False, has_bombs],
        ["anouki village", "anouki village lake chest", False, has_boomerang],

        # =========== Snow Sanctuary ==========

        ["snow realm", "ss", False, Has("Snow Sanctuary Cave Key") | has_temple_tracks("Blizzard")],
        ["ss", "ss stamp station", False, has_stamp_book],
        ["ss", "ss song", False, has_spirit_flute],

        ## ========== Blizzard Temple =========

        ["snow realm source", "bt", True, has_source('Snow')],
        ["blizzard temple tracks", "bt", True, has_temple_tracks("Blizzard")],
        ["bt", "bt b1 se", False, can_ring_bell & has_whirlwind],
        ["bt b1 se", "bt b1 e enemy chest", False, None],
        ["bt b1 se", "bt b1 ne enemy chest", False, can_kill_bubble],
        ["bt b1 se", "bt 1f ne chest", False, has_short_range | has_boomerang],
        ["bt 1f ne chest", "bt b1 sw chest", False, has_boomerang],
        ["bt b1 sw chest", "bt b1 nw enemy chest", False, has_small_keys("Blizzard Temple", 1) & can_kill_freezards_torch],
        ["bt b1 nw enemy chest", "bt stamp station", False, has_stamp_book],
        ["bt b1 nw enemy chest", "bt 1f nw chest", False, None],
        ["bt b1 nw enemy chest", "bt 1f torch chest", False, None],
        ["bt b1 nw enemy chest", "bt fraaz", False, has_sword],
        ["bt fraaz", "goal_fraaz", False, None],
        ["bt fraaz", "event_fraaz", False, None],

        # ========== Icy Spring ==========

        ["blizzard temple tracks", "icyspring", True, has_temple_tracks("Blizzard")],
        ["icyspring", "icyspring stamp station", False, has_stamp_book & has_boomerang],
        ["icyspring", "icyspring whip chest", False, has_whip],

        # ============ Snowdrift Station =========

        ["blizzard temple tracks", "snowdrift", True, Has("Snowdrift Station Tracks")],
        ["snowdrift", "snowdrift reward", False, (has_range | (has_sword_beam & hard_logic)) & can_kill_freezards],

        # ========== Slippery Station ==========
        ["blizzard temple tracks", "slippery", True, Has("Slippery Station Tracks") & (has_source("Snow") | Has("N Icy Spring Tracks"))],
        ["slippery", "slippery amateur", False, None],
        ["slippery", "slippery pro", False, None],
        ["slippery", "slippery champion", False, None],

        # ========== Bridge Worker's Home =======
        ["snow realm source", "bridge workers", True, has_source("Snow")],
        ["bridge workers", "bridge workers chest", False, has_sod],

        # ===== Dark Realm =====
        ["dark realm portal", "dark realm trains", False, has_dungeon_rewards(world.options.dungeons_required.value)],
        ["dark realm trains", "demon train", False, None],
        ["demon train", "cole fight", False, None],
        ["cole fight", "malladus 1", False, has_bow_of_light & has_sword],
        ["malladus 1", "malladus 2", False, has_spirit_flute & has_sword],
        ["malladus 2", "malladus goal", False, has_bow_of_light & has_sword],
        ["malladus 2", "malladus event", False, has_bow_of_light & has_sword],

        ["forest realm", "beedle", False, has_source("Snow")],
    ]

    required_rupees = 0
    if world.options.shopsanity.value == 1: required_rupees = 1500
    elif world.options.shopsanity.value == 2: required_rupees = 2100
    elif world.options.shopsanity.value == 3: required_rupees = 4600

    overworld_logic += [
        # Shops
        ["ss", "snow sanc shop", False, has_rupees(required_rupees)],

        ["beedle", "beedle bomb bag", False, has_rupees(required_rupees)],
        ["beedle", "beedle uncommon treasure", False, has_rupees(required_rupees)],
        ["beedle", "beedle rare treasure", False, has_rupees(required_rupees)],

        ["mayscore", "mayscore shop", False, has_rupees(required_rupees)],
        ["castle town", "castle town shop", False, has_rupees(required_rupees)],
    ]

    # Generate rabbit total items
    if world.options.rabbitsanity in ["on_total", "both"]:
        print(f"Creating total rabbit logic")
        overworld_logic += [
            [f"{realm.lower()} realm rabbits", f"{rabbit} Rabbit Count {i}", False,
             caught_rabbits(rabbit, i)] for i in range(1, 11)
            for realm, rabbit in zip(["Forest", "Snow"], ["Grass", "Snow"])
        ]

    return overworld_logic


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name

def create_connections(world: "SpiritTracksWorld", player: int, origin_name: str, options):
    all_logic = [
        make_overworld_logic(player, origin_name, world)
    ]

    entrance_lookup = {(e.entrance_region, e.exit_region): e for e in ENTRANCES.values()}
    world.set_completion_rule(Has("_beaten_game"))

    def create_entrance(r1, r2, rule_):
        entrance_data: "STTransition" or None = entrance_lookup.get((r1.name, r2.name), None)
        name = entrance_data.name if entrance_data else None

        entrance = r1.connect(r2, name)
        if rule_ is not None:
            # print(f"Setting rule {rule_}")
            world.set_rule(entrance, rule_)

        if entrance_data:
            # print(f"Creating connection {r1} -> {r2} | {entrance_data.name}")
            rando_type_bool = entrance_data.two_way
            entrance.randomization_type = EntranceType.TWO_WAY if rando_type_bool else EntranceType.ONE_WAY
            entrance.randomization_group = entrance_data.direction | entrance_data.category_group | entrance_data.island
            world.valid_entrances.append(entrance)

    # Create connections
    # print(f"Creating entrances: ")
    for logic_array in all_logic:
        for reg1, reg2, is_two_way, rule in logic_array:
            region_1 = world.get_region(reg1)
            region_2 = world.get_region(reg2)

            create_entrance(region_1, region_2, rule)
            if is_two_way:
                create_entrance(region_2, region_1, rule)
