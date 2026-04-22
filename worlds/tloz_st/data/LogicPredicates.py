from BaseClasses import CollectionState
from Options import Accessibility
from .Constants import *
from .Items import ITEMS

# =========== Item States =============

def st_has_stamp_book(state, player):
    return state.has("Stamp Book", player)

def st_has_spirit_flute(state, player):
    return state.has("Spirit Flute", player)

def st_has_sword(state: CollectionState, player: int):
    return state.has("Sword (Progressive)", player) or state.has("Sword", player)

def st_has_shield(state: CollectionState, player: int):
    # Shield can be bought from shop
    return state.has("Shield", player)

def st_has_bow(state: CollectionState, player: int):
    return state.has("Bow (Progressive)", player)

def st_has_bombs(state: CollectionState, player: int):
    return state.has("Bombs (Progressive)", player)

def st_has_whirlwind(state: CollectionState, player: int):
    return state.has("Whirlwind", player)

def st_has_whip(state: CollectionState, player: int):
    return state.has("Whip", player)

def st_has_boomerang(state: CollectionState, player: int):
    return state.has("Boomerang", player)

def st_has_sand_wand(state: CollectionState, player: int):
    return state.has("Sand Wand", player)

def st_has_sword_beam_scroll(state: CollectionState, player: int):
    return state.has("Sword Beam Scroll", player)

def st_has_regal_necklace(state: CollectionState, player: int):
    return state.has("Regal Necklace", player)

def st_has_wood_heart(state: CollectionState, player: int):
    return state.has("Wood Heart", player)

def st_has_net(state: CollectionState, player: int):
    return state.has("Rabbit Net", player) and st_has_cannon(state, player)

def st_has_compass_of_light(state, player):
    required_shards = state.multiworld.worlds[player].options.compass_shard_count.value
    return state.has("Compass of Light", player) or state.has("Compass of Light Shard", player, required_shards)

def st_has_wagon(state, player):
    return state.has("Wagon", player)

def st_has_cargo(state, player, cargo, event):
    return st_has_wagon(state, player) and (
            state.has(f"Cargo: {cargo}", player)
            or state.has(event, player))

## ========== Rabbits ===========

def st_has_rabbit_items(state, player, realm, count=10):
    rabbit_count = state.count(f"{realm} Rabbit", player)
    return rabbit_count >= count

def st_has_total_rabbits(state: CollectionState, player: int, count):
    rabbit_total = sum([state.count(f"{realm} Rabbit", player) for realm in rabbit_realms])
    return rabbit_total >= count

def st_caught_rabbits(state, player, realm, count):
    return state.has(f"_caught_{realm.lower()}_rabbits", player, count)

def st_all_types_rabbits(state, player, count):
    return all([st_has_rabbit_items(state, player, r, count) for r in rabbit_realms])

## ========= Rail Items =============

def st_has_glyph(state: CollectionState, player: int, realm: str):
    return state.has_group(f"Tracks: {realm} Glyph", player)

def st_has_cannon(state: CollectionState, player: int):
    return state.has("Cannon", player)

def st_train_access(state, player):
    return any([
        not st_option_train_requires_forest_glyph(state, player),
        st_has_glyph(state, player, "Forest")
    ])

def st_has_source(state: CollectionState, player: int, realm: str):
    return state.has_group(f"Tracks: {realm} Source", player)

def st_has_temple_tracks(state, player, temple):
    return state.has_group(f"Tracks: {temple} Temple Tracks", player)

def st_has_misc_tracks(state: "CollectionState", player, tracks):
    return state.has_group(f"Tracks: {tracks}", player)

def st_has_portal(state, player, portal, forward):
    if state.multiworld.worlds[player].options.portal_behavior.value == 1:
        return True
    if state.multiworld.worlds[player].options.portal_behavior.value == 0:
        return forward and st_has_cannon(state, player)
    return state.has(f"Portal Unlock: {portal}", player) and (not forward or st_has_cannon(state, player))

def st_soft_cannon(state, player):
    return any([
        st_has_cannon(state, player),
        state.has("_UT_Glitched_Logic", player),
        state.multiworld.worlds[player].options.cannon_logic == "no_logic"])

# ============== Songs =======================

def st_has_awakening_song(state: CollectionState, player: int):
    return state.has("Song of Awakening", player) and st_has_spirit_flute(state, player)

def st_has_healing_song(state: CollectionState, player: int):
    return state.has("Song of Healing", player) and st_has_spirit_flute(state, player)

def st_has_birds_song(state: CollectionState, player: int):
    return state.has("Song of Birds", player) and st_has_spirit_flute(state, player)

def st_has_light_song(state: CollectionState, player: int):
    return state.has("Song of Light", player) and st_has_spirit_flute(state, player)

def st_has_discovery_song(state: CollectionState, player: int):
    return state.has("Song of Discovery", player) and st_has_spirit_flute(state, player)

def st_has_tears(state: CollectionState, player: int, section: int):
    options = state.multiworld.worlds[player].options
    section_count = min(state.multiworld.worlds[player].sections_included, 5)
    if options.shuffle_tos_sections and options.tear_sections == "progressive":
        section = state.multiworld.worlds[player].tower_section_lookup[section]
        # print(f"Section lookup {state.multiworld.worlds[player].tower_section_lookup}")

    return any([
        state.has(f"Tear of Light (ToS {section})", player, 3),
        state.has(f"Big Tear of Light (ToS {section})", player),
        state.has(f"Tear of Light (Progressive)", player, section*3),
        state.has(f"Tear of Light (Progressive)", player, section_count*3 + 1),
        state.has(f"Big Tear of Light (Progressive)", player, section),
        state.has(f"Tear of Light (All Sections)", player, 3),
        state.has(f"Big Tear of Light (All Sections)", player),
    ])

def st_has_bow_of_light(state, player):
    section_count = min(state.multiworld.worlds[player].sections_included, 5)
    return any([
        state.has("Bow of Light", player) and st_has_bow(state, player),
        state.has(f"Tear of Light (Progressive)", player, section_count*3 + 1),
        state.has(f"Big Tear of Light (Progressive)", player, section_count+1),
        state.has(f"Tear of Light (All Sections)", player, 4),
        state.has(f"Big Tear of Light (All Sections)", player, 2),
    ])

def st_can_possess_phantoms(state: CollectionState, player: int, floor: int):
    return any([
        state.has("Sword (Progressive)", player, 2),
        st_has_bow_of_light(state, player),
        st_has_sword(state, player) and st_has_tears(state, player, floor)
    ])

def st_vanilla_tears(state: CollectionState, player: int):
    return st_has_sword(state, player) and state.multiworld.worlds[player].options.randomize_tears.value == -1

# =========== Combined item states ================

def st_has_good_damage(state: CollectionState, player: int):
    return any([
        state.has("Sword (Progressive)", player),
        state.has("Bombs (Progressive)", player),
        state.has("Bow (Progressive)", player),
    ])

def st_has_damage(state: CollectionState, player: int):
    return any([
        st_has_good_damage(state, player),
        state.has("Whip", player),
    ])

def st_can_kill_bat(state: CollectionState, player: int):
    return any([
        st_has_damage(state, player),
        st_has_boomerang(state, player)
    ])


def st_can_kill_bubble(state: CollectionState, player: int):
    return any([
        st_has_bombs(state, player),
        st_has_bow(state, player),
        st_has_whip(state, player),
        all([
            st_has_sword(state, player), any([
                st_has_boomerang(state, player),
                st_has_whirlwind(state, player),
            ])
        ])
    ])

def st_has_range(state: CollectionState, player: int):
    return state.has_any(["Boomerang", "Bow (Progressive)"], player)

def st_has_range_objects(state, player):
    return state.has_any(["Boomerang", "Bow (Progressive)", "Whirlwind"], player)

def st_has_short_range(state: CollectionState, player: int):
    return any([st_has_mid_range(state, player),
                st_clever_bombs(state, player), ])


def st_can_rotate_repeater(state, player):
    return any([
        st_has_sword(state, player),
        st_has_boomerang(state, player),
        st_has_whip(state, player)
    ])

def st_has_mid_range(state: CollectionState, player: int):
    return any([st_has_range(state, player), st_has_whip(state, player),
                st_has_beam_sword(state, player)])


def st_has_beam_sword(state: CollectionState, player: int):
    return all([
        st_has_sword(state, player),
        st_has_sword_beam_scroll(state, player)
    ])

def st_can_ring_bell(state: CollectionState, player: int):
    return any([st_has_sword(state, player), st_has_boomerang(state, player)])

def st_can_kill_freezards(state, player):
    return all([
        any([
            st_has_shield(state, player),
            st_has_bow_of_light(state, player),
            st_option_hard_logic(state, player)
        ]),
        st_has_damage(state, player)
    ])

def st_can_kill_freezards_torch(state, player):
    return all([
        any([
            st_has_boomerang(state, player),
            st_has_shield(state, player),
            st_has_bow_of_light(state, player),
            st_option_hard_logic(state, player),
        ]),
        st_has_damage(state, player)
    ])

# ================ Rupee States ==================

def st_has_rupees(state: CollectionState, player: int, cost: int):
    # If has a farmable minigame and the means to sell, expensive things are in logic.
    options = state.multiworld.worlds[player].options
    treasure_count = state.count("Treasure", player) - 2500 if state.has("_can_sell_treasure", player) else 0
    return any([
        state.has("_UT_Glitched_Logic", player),
        all([
            state.has("_rupee_farming_spot", player),
            options.excess_random_treasure.value == 2,
            options.rupee_farming_logic.value == 1
        ]),
        all([
            state.has("_rupee_farming_spot", player),
            state.has("_can_sell_treasure", player),
            options.excess_random_treasure.value == 1,
            options.rupee_farming_logic.value == 1
        ]),
        state.count("Rupees", player) + treasure_count > cost
    ])

# ============ Option states =============

def st_option_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "glitched" or state.has("_UT_Glitched_Logic", player)


def st_option_normal_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic == "normal"


def st_option_hard_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["hard", "glitched"] or state.has("_UT_Glitched_Logic", player)

def st_option_not_glitched_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic in ["hard", "normal"]


def st_option_keysanity(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "anywhere"


def st_option_keys_vanilla(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity == "vanilla"


def st_option_keys_in_own_dungeon(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.keysanity in ["in_own_dungeon", "vanilla"]


# def st_option_stantoms_hard(state: CollectionState, player: int):
#     return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in ["require_weapon"],
#                 st_has_whip(state, player)])


# def st_option_stantoms_med(state: CollectionState, player: int):
#     return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in ["require_weapon", "require_stun"],
#                 any([
#                     st_has_bow(state, player),
#                     st_has_hammer(state, player),
#                     st_has_fire_sword(state, player)
#                 ])])
#
#
# def st_option_stantoms_easy(state: CollectionState, player: int):
#     return (state.multiworld.worlds[player].options.stantom_combat_difficulty in
#             ["require_weapon", "require_stun", "require_traps"])

#
# def st_option_stantoms_sword_only(state: CollectionState, player: int):
#     return all([state.multiworld.worlds[player].options.stantom_combat_difficulty in
#                 ["require_weapon", "require_stun", "require_traps", "require_stantom_sword"],
#                 st_has_stantom_sword(state, player)])


def st_clever_pots(state: CollectionState, player: int):
    return st_option_hard_logic(state, player)


def st_can_hit_switches(state: CollectionState, player: int):
    return any([st_option_hard_logic(state, player), st_can_kill_bat(state, player)])


def st_clever_bombs(state: CollectionState, player: int):
    return all([st_has_bombs(state, player),
                st_option_hard_logic(state, player)])

#
# def st_option_randomize_frogs(state: CollectionState, player: int):
#     return state.multiworld.worlds[player].options.randomize_frogs == "randomize"
#
#
# def st_option_start_with_frogs(state: CollectionState, player: int):
#     return state.multiworld.worlds[player].options.randomize_frogs == "start_with"


# def st_beat_required_dungeons(state: CollectionState, player: int):
#     # print(f"Dungeons required: {state.count_group('Current Metals', player)}/{state.multiworld.worlds[player].options.dungeons_required} {state.has_group("Current Metals", player,
#     #                       state.multiworld.worlds[player].options.dungeons_required)}")
#     return state.has_group("Current Metals", player,
#                            state.multiworld.worlds[player].options.dungeons_required)


def st_option_train_requires_forest_glyph(state: CollectionState, player: int):
    #state.multiworld.worlds[player].options.train_requires_forest_glyph
    return True


# For doing sneaky stuff with universal tracker UT
def st_is_ut(state: CollectionState, player: int):
    return getattr(state.multiworld, "generation_is_fake", False)


# ============= Key logic ==============

def st_has_small_keys(state: CollectionState, player: int, dung_name: str, amount: int = 1, ool: int = 4):
    return any([
        state.has(f"Small Key ({dung_name})", player, amount),
        state.has(f"Keyring ({dung_name})", player),
        (   state.has("_UT_Glitched_Logic", player)
            and state.has(f"Small Key ({dung_name})", player, ool)
        )
    ])


def st_has_boss_key(state: CollectionState, player: int, dung_name: str):
    return state.has(f"Boss Key ({dung_name})", player) or (
        state.has(f"Keyring ({dung_name})", player) and state.multiworld.worlds[player].options.big_keyrings)


#def st_has_boss_key_simple(state: CollectionState, player: int, dung_name: str):
 #   return any([
  #      st_has_boss_key(state, player, dung_name),
        #         st_is_ut(state, player)
  #  ])


def st_ut_small_key_vanilla_location(state, player):
    return all([
        st_is_ut(state, player),
        st_option_keys_vanilla(state, player)
    ])


def st_ut_small_key_own_dungeon(state, player):
    return all([
        st_is_ut(state, player),
        st_option_keys_in_own_dungeon(state, player)
    ])


# ======== Harder Logic ===========


def st_can_hit_tricky_switches(state: CollectionState, player: int):
    return any([
        st_clever_pots(state, player),
        st_has_short_range(state, player)
    ])


def st_can_boomerang_return(state: CollectionState, player: int):
    return all([
        st_has_boomerang(state, player),
        st_option_glitched_logic(state, player)
    ])


def st_can_arrow_despawn(state: CollectionState, player: int):
    return all([
        st_has_bow(state, player),
        st_option_glitched_logic(state, player)
    ])


def st_can_sword_glitch(state, player):
    return all([
        st_has_sword(state, player),
        st_option_glitched_logic(state, player)
    ])

def st_can_sword_scroll_clip(state, player):
    return all([
        st_has_sword(state, player),
        state.has("Swordsman's Scroll", player),
        st_option_glitched_logic(state, player)
    ])

def st_has_train(state, player):
    return all([st_has_glyph(state, player, "Forest"),
                any([
                    st_has_cannon(state, player),
                    state.multiworld.worlds[player].options.cannon_logic.value > 1,
                    state.multiworld.worlds[player].options.cannon_logic.value > 0 and state.has("_UT_Glitched_Logic", player)
                ]),
            ])

# ====== Specific locations =============


# Overworld

def st_castle_town_cuccos(state, player):
    return st_has_birds_song(state, player) or (st_has_whirlwind(state, player) and st_option_hard_logic(state, player))

def st_has_dungeon_rewards(state, player):
    if state.multiworld.worlds[player].options.dark_realm_access not in ["dungeons", "both"]:
        return True
    dungeon_count = state.multiworld.worlds[player].options.dungeons_required.value
    return state.has("_dungeon_reward", player, dungeon_count)

def st_can_fight_malladus(state, player):
    return st_has_sword(state, player) and st_has_bow_of_light(state, player)

def st_can_enter_tos(state, player):
    options = state.multiworld.worlds[player].options
    return any([
        options.tos_unlock_base_item.value == 0,
        options.tos_unlock_base_item.value == 1 and (
            state.has("Tower of Spirits Base", player) or
            state.has("Progressive ToS Section", player)
        )
    ])

def st_can_enter_tos_section(state, player, section):
    sources = [None, "Forest", "Snow", "Ocean", "Fire"]
    # print(f"Section: {section}")
    if section == 1:
        return st_can_enter_tos(state, player)
    options = state.multiworld.worlds[player].options
    # print(f"Open Tower: {options.tos_section_unlocks.value == 0}\n"
    #       f"Has Source {sources[section-1]} {st_has_source(state, player, sources[section-1])} and {options.tos_section_unlocks.value == 1}\n"
    #       f"Progressive: {options.tos_section_unlocks.value == 2} and:\n"
    #       f"\tProgressive Sections {state.has('Progressive ToS Section', player, section) and options.tos_unlock_base_item.value == 1}\n"
    #       f"\tNo Base {state.has('Progressive ToS Section', player, section) and options.tos_unlock_base_item.value == 1}\n"
    #       f"""Total: {any([
    #     options.tos_section_unlocks.value == 0,
    #     all([st_has_source(state, player, sources[section-1]), options.tos_section_unlocks.value == 1]),
    #     options.tos_section_unlocks.value == 2 and any([
    #         state.has("Progressive ToS Section", player, section) and options.tos_unlock_base_item.value == 1,
    #         state.has("Progressive ToS Section", player, section-1) and options.tos_unlock_base_item.value == 0,
    #     ])
    # ])}""")
    return any([
        options.tos_section_unlocks.value == 0,  # Open tower
        all([st_has_source(state, player, sources[section-1]), options.tos_section_unlocks.value == 1]),
        options.tos_section_unlocks.value == 2 and any([
            state.has("Progressive ToS Section", player, section) and options.tos_unlock_base_item.value == 1,
            state.has("Progressive ToS Section", player, section-1) and options.tos_unlock_base_item.value == 0,
        ])
    ])

def st_desert_temple_keys(state, player):
    return st_has_small_keys(state, player, "Desert Temple", 2, 1)

def st_mtt_center(state, player):
    return any([
        all([
            st_has_small_keys(state, player, "Mountain Temple", 2),
            any([
                st_has_boomerang(state, player),
                st_has_bombs(state, player),
                all([
                    st_option_hard_logic(state, player),
                    st_has_bow(state, player) or st_has_beam_sword(state, player) or st_has_whip(state, player)
                ])
            ])
        ]),
        all([
            st_option_glitched_logic(state, player),
            any([
                all([
                    st_has_small_keys(state, player, "Mountain Temple", 2, 1),
                    st_has_boomerang(state, player)
                ]),
                st_has_bombs(state, player)  # New rta method
            ])
        ])
    ])

def st_tos_14f_glitched(state, player):
    return any([
        st_has_small_keys(state, player, "ToS 4", 2, 1),
        all([
            st_option_glitched_logic(state, player),
            st_has_small_keys(state, player, "ToS 4", 0),
            st_has_boomerang(state, player) or st_has_whip(state, player)
        ])
    ])

def st_tos_15f_glitched(state, player):
    return any([
        all([
            st_has_range(state, player) or st_has_beam_sword(state, player),
            st_has_small_keys(state, player, "ToS 4", 3, 2)
        ]),
        all([
            st_option_glitched_logic(state, player),
            st_has_small_keys(state, player, "ToS 4", 3, 1),
            any([
                st_has_range(state, player),
                st_has_beam_sword(state, player),
                st_has_bombs(state, player) and st_has_whirlwind(state, player)
            ])
        ])
    ])

def st_hard_birds(state, player):
    return all([
        st_has_whip(state, player),
        st_has_birds_song(state, player) or st_option_hard_logic(state, player)
    ])

def st_has_passenger(state, player, passenger, event):
    return state.has(f"Passenger: {passenger}", player) or state.has(event, player)

