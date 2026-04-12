from enum import Flag, auto
from typing import Dict, NamedTuple, Optional, Callable

from BaseClasses import Location, CollectionState
from worlds.phoa import PhoaOptions
from worlds.phoa.LogicExtensions import PhoaLogic


class PhoaFlag(Flag):
    DEFAULT = auto()
    MAINQUEST = auto()
    HEARTRUBY = auto()
    ENERGYGEM = auto()
    MOONSTONE = auto()
    DUNGEONITEM = auto()
    LUNARARTIFACT = auto()
    FISHINGSPOT = auto()
    NPCGIFTS = auto()
    MISC = auto()
    SHOPSANITY = auto()
    SMALLANIMALS = auto()
    RINCHESTS = auto()
    RINCONTAINERS = auto()
    GEOCHALLENGE = auto()


class PhoaLocation(Location):
    game: str = "Phoenotopia: Awakening"


class PhoaLocationData(NamedTuple):
    region: str
    address: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None
    flags: PhoaFlag = PhoaFlag.DEFAULT
    vanillaItem: str = ""


def get_location_data(player: Optional[int], options: Optional[PhoaOptions]) -> Dict[str, PhoaLocationData]:
    logic = PhoaLogic(player)

    locations: Dict[str, PhoaLocationData] = {
        "Panselo Village - Watchtower (West) - Chest": PhoaLocationData(
            region="panselo_village",
            address=7676061,
            flags=PhoaFlag.RINCHESTS,
            vanillaItem="35 Rin",
        ),
        "Panselo Village - Watchtower (West) - Hidden in box": PhoaLocationData(
            region="panselo_village",
            address=7676031,
            flags=PhoaFlag.MISC,
            vanillaItem="Cheese",
        ),
        "Panselo Village - Watchtower (West) - Lizard": PhoaLocationData(
            region="panselo_village",
            address=7676041,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Panselo Village - Free Gift from Panselo Shop Keeper Tao": PhoaLocationData(
            region="panselo_village",
            address=7676070,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Fruit Jam",
        ),
        "Panselo Village - Panselo Shop Item 1": PhoaLocationData(
            region="panselo_village",
            address=7676072,
            flags=PhoaFlag.SHOPSANITY,
            vanillaItem="Perro Egg",
        ),
        "Panselo Village - Panselo Shop Item 2": PhoaLocationData(
            region="panselo_village",
            address=7676073,
            flags=PhoaFlag.SHOPSANITY,
            vanillaItem="Milk",
        ),
        "Panselo Village - Panselo Shop Item 3": PhoaLocationData(
            region="panselo_village",
            address=7676074,
            flags=PhoaFlag.SHOPSANITY,
            vanillaItem="Panselo Potato",
        ),
        "Panselo Village - Panselo Shop Box 1 after abduction": PhoaLocationData(
            region="panselo_village",
            address=7676084,
            rule=lambda state: state.has("Slargummy boss defeated", player),
            flags=PhoaFlag.MISC,
            vanillaItem="Panselo Potato",
        ),
        "Panselo Village - Panselo Shop Box 2 after abduction": PhoaLocationData(
            region="panselo_village",
            address=7676085,
            rule=lambda state: state.has("Slargummy boss defeated", player),
            flags=PhoaFlag.MISC,
            vanillaItem="Perro Egg",
        ),
        "Panselo Village - Panselo Shop Box 3 after abduction": PhoaLocationData(
            region="panselo_village",
            address=7676086,
            rule=lambda state: state.has("Slargummy boss defeated", player),
            flags=PhoaFlag.MISC,
            vanillaItem="Fruit Jam",
        ),
        "Panselo Village - Panselo Shop Box 4 after abduction": PhoaLocationData(
            region="panselo_village",
            address=7676087,
            rule=lambda state: state.has("Slargummy boss defeated", player),
            flags=PhoaFlag.MISC,
            vanillaItem="Milk",
        ),
        "Panselo Village - Panselo Shop Box 5 after abduction": PhoaLocationData(
            region="panselo_village",
            address=7676088,
            rule=lambda state: state.has("Slargummy boss defeated", player),
            flags=PhoaFlag.MISC,
            vanillaItem="Panselo Potato",
        ),
        "Panselo Village - Dojo high up punchbag": PhoaLocationData(
            region="panselo_village",
            address=7676082,
            rule=lambda state: logic.can_deal_damage(state),
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="20 Rin",
        ),
        "Panselo Village - Play Prelude of Panselo": PhoaLocationData(
            region="panselo_village",
            address=7676089,
            rule=lambda state: logic.has_music_instrument(state),
            flags=PhoaFlag.NPCGIFTS,  # Sidequest?
            vanillaItem="Prelude of Panselo",
        ),
        "Panselo Village - Inside coop": PhoaLocationData(
            region="panselo_village",
            address=7676030,
            flags=PhoaFlag.MISC,
            vanillaItem="Perro Egg",
        ),
        "Panselo Village - Orphanage roof": PhoaLocationData(
            region="panselo_village",
            address=7676028,
            flags=PhoaFlag.MISC,
            vanillaItem="Dandelion",
        ),
        "Panselo Village - On table in girl's room": PhoaLocationData(
            region="panselo_village",
            address=7676032,
            flags=PhoaFlag.MISC,
            vanillaItem="Berry Fruit",
        ),
        "Panselo Village - Pot in boys Room": PhoaLocationData(
            region="panselo_village",
            address=7676058,
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="5 Rin",
        ),
        "Panselo Village - Box at right side of orphanage hall": PhoaLocationData(
            region="panselo_village",
            address=7676059,
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="9 Rin",
        ),
        "Panselo Village - Orphanage attic chest": PhoaLocationData(
            region="panselo_village",
            address=7676060,
            flags=PhoaFlag.RINCHESTS,
            vanillaItem="35 Rin",
        ),
        "Panselo Village - Nana's Pumpkin Muffin": PhoaLocationData(
            region="panselo_village",
            address=7676068,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Pumpkin Muffin",
        ),
        "Panselo Village - Yesterday's lunch from Kitt": PhoaLocationData(
            region="panselo_village",
            address=7676077,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Cooked Toad Leg",
        ),
        "Panselo Village - Kitt's money for the milk": PhoaLocationData(
            region="panselo_village",
            address=7676078,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="20 Rin",
        ),
        "Panselo Village - Amanda's gift lunch": PhoaLocationData(
            region="panselo_village",
            address=7676090,
            rule=lambda state: state.has("Slargummy boss defeated", player),
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Potato Lunch",
        ),
        "Panselo Village - Warehouse Chest": PhoaLocationData(
            region="panselo_village",
            address=7676062,
            rule=lambda state: logic.can_break_big_box_with_tools(state),
            flags=PhoaFlag.RINCHESTS,
            vanillaItem="25 Rin",
        ),
        "Panselo Village - Warehouse Free standing item": PhoaLocationData(
            region="panselo_village",
            address=7676080,
            flags=PhoaFlag.MAINQUEST,
            vanillaItem="Wooden Bat",
        ),
        "Panselo Village - Jon's Potato": PhoaLocationData(
            region="panselo_village",
            address=7676069,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Panselo Potato",
        ),
        "Panselo Village - On roof next to Stan": PhoaLocationData(
            region="panselo_village",
            address=7676029,
            flags=PhoaFlag.MISC,
            vanillaItem="Dandelion",
        ),
        "Panselo Village - Rutea's room": PhoaLocationData(
            region="panselo_village",
            address=7676001,
            flags=PhoaFlag.HEARTRUBY,
            vanillaItem="Heart Ruby",
        ),
        "Panselo Village - Watchtower (East) item up top": PhoaLocationData(
            region="panselo_village",
            address=7676000,
            rule=lambda state: logic.can_break_big_box_with_tools(state, exclude_spear=True),
            flags=PhoaFlag.HEARTRUBY,
            vanillaItem="Heart Ruby",
        ),
        "Panselo Region - End of secret fishing spot": PhoaLocationData(
            region="panselo_region",
            address=7676002,
            flags=PhoaFlag.ENERGYGEM,
            vanillaItem="Energy Gem",
        ),
        "Panselo Region - Franway roof": PhoaLocationData(
            region="panselo_region",
            address=7676034,
            flags=PhoaFlag.MISC,
            vanillaItem="Dandelion",
        ),
        "Panselo Region - GEO house roof": PhoaLocationData(
            region="panselo_region",
            address=7676033,
            flags=PhoaFlag.MISC,
            vanillaItem="Dandelion",
        ),
        "Panselo Region - GEO house reward": PhoaLocationData(
            region="panselo_region",
            address=7676083,
            flags=PhoaFlag.GEOCHALLENGE,
            rule=lambda state: logic.has_music_instrument(state)
                               and state.has("GEO Song", player),
            vanillaItem="Dandelion",
        ),
        "Panselo Region - Overworld encounter near Sunflower Road": PhoaLocationData(
            region="panselo_region",
            address=7676005,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Panselo Region - Underneath boulder north of Panselo": PhoaLocationData(
            region="panselo_region",
            address=7676004,
            rule=lambda state: logic.has_bombs(state) or logic.can_use_spear_bomb(state),
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Panselo Region - Northeastern treetops right stone pot": PhoaLocationData(
            region="panselo_region",
            address=7676003,
            rule=lambda state: logic.can_hit_switch_from_a_distance(state)
                               or state.has("Rocket Boots", player),
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Panselo Region - Northeastern treetops left stone pot": PhoaLocationData(
            region="panselo_region",
            address=7676081,
            rule=lambda state: logic.can_hit_switch_from_a_distance(state)
                               or state.has("Rocket Boots", player),
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="30 Rin",
        ),
        "Doki Forest - Cave guarded by Gummies - First item": PhoaLocationData(
            region="panselo_region",
            address=7676035,
            flags=PhoaFlag.MISC,
            vanillaItem="Doki Herb",
        ),
        "Doki Forest - Cave guarded by Gummies - Second item": PhoaLocationData(
            region="panselo_region",
            address=7676036,
            flags=PhoaFlag.MISC,
            vanillaItem="Doki Herb",
        ),
        "Doki Forest - Cave guarded by Gummies - Third item": PhoaLocationData(
            region="panselo_region",
            address=7676037,
            flags=PhoaFlag.MISC,
            vanillaItem="Doki Herb",
        ),
        "Doki Forest - Cave guarded by Gummies - Lizard": PhoaLocationData(
            region="panselo_region",
            address=7676042,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Doki Forest - Lizard at climbable roots": PhoaLocationData(
            region="panselo_region",
            address=7676043,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Doki Forest - Cave blocked by destructable blocks": PhoaLocationData(
            region="panselo_region",
            address=7676006,
            rule=lambda state: logic.has_explosives(state),
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Doki Forest - Chest through crawl space": PhoaLocationData(
            region="panselo_region",
            address=7676063,
            flags=PhoaFlag.RINCHESTS,
            vanillaItem="35 Rin",
        ),
        "Doki Forest - Lizard in alcove": PhoaLocationData(
            region="panselo_region",
            address=7676044,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Doki Forest - Campfire cave - First Lizard": PhoaLocationData(
            region="panselo_region",
            address=7676045,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Doki Forest - Campfire cave - Second Lizard": PhoaLocationData(
            region="panselo_region",
            address=7676046,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Doki Forest - Campfire cave - Pot high up above statue": PhoaLocationData(
            region="panselo_region",
            address=7676092,
            rule=lambda state: logic.has_sonic_spear(state),
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="50 Rin",
        ),
        "Doki Forest - Shelby's gift for lighting the campfire": PhoaLocationData(
            region="panselo_region",
            address=7676076,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Doki Herb",
        ),
        "Doki Forest - Fish underneath Anuri Temple": PhoaLocationData(
            region="panselo_region",
            address=7676007,
            rule=lambda state: logic.has_fishing_rod(state),
            flags=PhoaFlag.FISHINGSPOT,
            vanillaItem="Dragon's Scale",
        ),
        "Doki Forest - Gift from Seth": PhoaLocationData(
            region="panselo_region",
            address=7676071,
            flags=PhoaFlag.NPCGIFTS,
            vanillaItem="Mystery Meat",
        ),
        "Doki Forest - Gift from Alex": PhoaLocationData(
            region="panselo_region",
            address=7676008,
            flags=PhoaFlag.MAINQUEST,
            vanillaItem="Slingshot",
        ),
        "Doki Forest - On Top of Anuri Temple": PhoaLocationData(
            region="panselo_region",
            address=7676079,
            rule=lambda state: logic.has_sonic_spear(state),
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Anuri Temple - Lizard at top of climbable vines at entrance": PhoaLocationData(
            region="anuri_temple(main_entrance)",
            address=7676047,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Skeleton above first gate": PhoaLocationData(
            region="anuri_temple(main_entrance)",
            address=7676009,
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - Lizard behind Bombable Blocks": PhoaLocationData(
            region="anuri_temple(top_floor)",
            address=7676048,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Time the gates through Scaber funnel": PhoaLocationData(
            region="anuri_temple(scaber_switch_maze)",
            address=7676024,
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Anuri Temple - Lizard left of Anuri throne": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676050,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Lizard right of Anuri throne": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676049,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Fight toads in treasure room": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676016,
            flags=PhoaFlag.LUNARARTIFACT,
            vanillaItem="Lunar Vase",
        ),
        "Anuri Temple - Lizard at the end of treasure room": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676051,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Scabers maze": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676010,
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - High up pot in Scabers maze": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676066,
            rule=lambda state: logic.has_sonic_spear(state),
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="15 Rin",
        ),
        "Anuri Temple - Press the switches with pots and fruits": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676011,
            rule=lambda state: logic.can_hit_switch_from_a_distance(state, True),
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - Side entrance room - First Lizard": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676055,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Carry pot across the water steps": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676012,
            flags=PhoaFlag.ENERGYGEM,
            vanillaItem="Energy Gem",
        ),
        "Anuri Temple - Lizard in water steps room": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676054,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Stackable pots room - Hidden item": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676013,
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Anuri Temple - Stackable pots room - Lizard": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676053,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Stackable pots room - Anuri Skeleton": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676065,
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="15 Rin",
        ),
        "Anuri Temple - Sprint-jump on timed switches": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676014,
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - Hit three switches in many pots room": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676019,
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - Mouse in pot in many pots room": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676091,
            rule=lambda state: logic.has_bat(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Skeleton at bottom of right elevator room": PhoaLocationData(
            region="anuri_temple(main)",
            address=7676064,
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="15 Rin",
        ),
        "Anuri Temple - Side entrance room - Second Lizard": PhoaLocationData(
            region="anuri_temple(side_entrance)",
            address=7676056,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Side entrance first item": PhoaLocationData(
            region="anuri_temple(side_entrance)",
            address=7676038,
            flags=PhoaFlag.MISC,
            vanillaItem="Doki Herb",
        ),
        "Anuri Temple - Side entrance second item": PhoaLocationData(
            region="anuri_temple(side_entrance)",
            address=7676039,
            flags=PhoaFlag.MISC,
            vanillaItem="Doki Herb",
        ),
        "Anuri Temple - Moveable bridges room": PhoaLocationData(
            region="anuri_temple(moveable_bridge_area)",
            address=7676017,
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Anuri Temple - Lizard in movable bridge room": PhoaLocationData(
            region="anuri_temple(moveable_bridge_area)",
            address=7676052,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Slingshot the switch and surfacing Toads": PhoaLocationData(
            region="anuri_temple(moveable_bridge_area)",
            address=7676018,
            rule=lambda state: logic.has_slingshot(state),
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - Tall tower puzzle behind locked door": PhoaLocationData(
            region="anuri_temple(tall_tower_puzzle_room)",
            address=7676015,
            flags=PhoaFlag.HEARTRUBY,
            vanillaItem="Heart Ruby",
        ),
        "Anuri Temple - Tall tower puzzle side item": PhoaLocationData(
            region="anuri_temple(tall_tower_puzzle_room)",
            address=7676040,
            flags=PhoaFlag.MISC,
            vanillaItem="Doki Herb",
        ),
        "Anuri Temple Basement - Hit the switch hidden under breakable tomb": PhoaLocationData(
            region="anuri_temple(basement)",
            address=7676020,
            rule=lambda state: logic.has_explosives(state),
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple Basement - Push metal pot onto switch from above": PhoaLocationData(
            region="anuri_temple(basement)",
            address=7676021,
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple Basement - Within sarcophagus": PhoaLocationData(
            region="anuri_temple(basement)",
            address=7676022,
            rule=lambda state: logic.has_explosives(state),
            flags=PhoaFlag.MOONSTONE,
            vanillaItem="Moonstone",
        ),
        "Anuri Temple Basement - Defeat the glowing Slargummy": PhoaLocationData(
            region="anuri_temple(basement)",
            address=7676023,
            rule=lambda state: state.has("Crank Lamp", player),
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple Basement - Big pot in tomb tunnel": PhoaLocationData(
            region="anuri_temple(basement)",
            address=7676067,
            flags=PhoaFlag.RINCONTAINERS,
            vanillaItem="20 Rin",
        ),
        # "Anuri Temple - Fishing Spot After Slargummy": PhoaLocationData(
        #     region="anuri_temple(pond)",
        #     address=7676025,
        # ), # Moonstone
        # Camera doesn't move with the rod yet. Not sure why. This check also requires about 10 Energy Gems anyway
        "Anuri Temple - Bart's head crater": PhoaLocationData(
            region="anuri_temple(pond)",
            address=7676075,
            flags=PhoaFlag.MAINQUEST,
            vanillaItem="Mysterious Golem Head",
        ),
        "Anuri Temple - Use slingshot to hit the switches below": PhoaLocationData(
            region="anuri_temple(post_pond)",
            address=7676026,
            rule=lambda state: logic.has_slingshot(state)
                               or logic.has_sonic_spear(state),
            flags=PhoaFlag.DUNGEONITEM,
            vanillaItem="Anuri Pearlstone",
        ),
        "Anuri Temple - Lizard at treasure room before century toad": PhoaLocationData(
            region="anuri_temple(post_pond)",
            address=7676057,
            rule=lambda state: logic.can_hit_switch_from_a_distance(state),
            flags=PhoaFlag.SMALLANIMALS,
            vanillaItem="Mystery Meat",
        ),
        "Anuri Temple - Dive down in long vertical room": PhoaLocationData(
            region="anuri_temple(dive_room)",
            address=7676027,
            rule=lambda state: state.has("Life Saver", player),
            flags=PhoaFlag.LUNARARTIFACT,
            vanillaItem="Lunar Frog",
        ),
        # Events
        "Anuri Temple - Side entrance gate opened": PhoaLocationData(
            region="anuri_temple(main)",
            address=None,
        ),
        "Slargummy boss defeated": PhoaLocationData(
            region="anuri_temple(slargummy_boss)",
            address=None,
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
        ),
        "Strange Urn": PhoaLocationData(
            region="anuri_temple(urn_room)",
            address=None,
        ),
    }

    if not options:
        return locations

    filters = [
        (options.enable_main_quest_locations <= 0, PhoaFlag.MAINQUEST),
        (options.enable_heart_ruby_locations <= 0, PhoaFlag.HEARTRUBY),
        (options.enable_energy_gem_locations <= 0, PhoaFlag.ENERGYGEM),
        (options.enable_moonstone_locations <= 0, PhoaFlag.MOONSTONE),
        (options.enable_lunar_artifacts_locations <= 0, PhoaFlag.LUNARARTIFACT),
        (options.enable_fishing_spots <= 0, PhoaFlag.FISHINGSPOT),
        (options.enable_npc_gifts <= 0, PhoaFlag.NPCGIFTS),
        (options.enable_misc <= 0, PhoaFlag.MISC),
        (options.shop_sanity <= 0, PhoaFlag.SHOPSANITY),
        (options.enable_small_animal_drops <= 0, PhoaFlag.SMALLANIMALS),
        (options.enable_rin_locations <= 0, PhoaFlag.RINCHESTS),
        (options.enable_rin_locations <= 1, PhoaFlag.RINCONTAINERS),
        (options.enable_geo_challenge_rewards <= 0, PhoaFlag.GEOCHALLENGE)
    ]

    for option, flag in filters:
        if option:
            locations = {
                name: data for name, data in locations.items() if data.flags != flag
            }

    return locations
