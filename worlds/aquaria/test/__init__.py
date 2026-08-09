"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Base class for the Aquaria randomizer unit tests
"""
import typing

from BaseClasses import CollectionState
from test.bases import WorldTestBase
from ..Locations import AquariaLocationNames

# Every location accessible after the home water.
after_home_water_locations = [
    AquariaLocationNames.SUN_CRYSTAL,
    AquariaLocationNames.HOME_WATERS_TRANSTURTLE,
    AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH,
    AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH,
    AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_TO_THE_RIGHT_OF_THE_SAVE_CRYSTAL,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_SMALL_PATH_BEFORE_MITHALAS,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_PATH_FROM_THE_LEFT_ENTRANCE,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_CLEARING_CLOSE_TO_THE_BOTTOM_EXIT,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_BIG_CLEARING_CLOSE_TO_THE_SAVE_CRYSTAL,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_BIG_CLEARING_TO_THE_TOP_EXIT,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_FIRST_URN_IN_THE_MITHALAS_EXIT,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_SECOND_URN_IN_THE_MITHALAS_EXIT,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_THIRD_URN_IN_THE_MITHALAS_EXIT,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_TURTLE_ROOM,
    AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_TRANSTURTLE,
    AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_BEHIND_THE_CHOMPER_FISH,
    AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS,
    AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_BULB_CLOSE_TO_THE_RIGHT_EXIT,
    AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_BULB_BEHIND_THE_CHOMPER_FISH,
    AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_KING_SKULL,
    AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_RIGHT_PART,
    AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_LEFT_PART,
    AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_CENTER_PART,
    AquariaLocationNames.ARNASSI_RUINS_SONG_PLANT_SPORE,
    AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR,
    AquariaLocationNames.ARNASSI_RUINS_ARNASSI_STATUE,
    AquariaLocationNames.ARNASSI_RUINS_TRANSTURTLE,
    AquariaLocationNames.ARNASSI_RUINS_CRAB_ARMOR,
    AquariaLocationNames.SIMON_SAYS_AREA_TRANSTURTLE,
    AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_THE_LEFT_CITY_PART,
    AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_THE_LEFT_CITY_PART,
    AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_RIGHT_PART,
    AquariaLocationNames.MITHALAS_CITY_BULB_AT_THE_TOP_OF_THE_CITY,
    AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_A_BROKEN_HOME,
    AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_A_BROKEN_HOME,
    AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_BOTTOM_LEFT_PART,
    AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_ONE_OF_THE_HOMES,
    AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_ONE_OF_THE_HOMES,
    AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_ONE_OF_THE_HOMES,
    AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_ONE_OF_THE_HOMES,
    AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_THE_CITY_RESERVE,
    AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_THE_CITY_RESERVE,
    AquariaLocationNames.MITHALAS_CITY_THIRD_URN_IN_THE_CITY_RESERVE,
    AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_AT_THE_END_OF_THE_TOP_PATH,
    AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_AT_THE_END_OF_THE_TOP_PATH,
    AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_TOP_PATH,
    AquariaLocationNames.MITHALAS_CITY_MITHALAS_POT,
    AquariaLocationNames.MITHALAS_CITY_URN_IN_THE_CASTLE_FLOWER_TUBE_ENTRANCE,
    AquariaLocationNames.MITHALAS_CITY_DOLL,
    AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_BULB_IN_THE_FLESH_HOLE,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_BLUE_BANNER,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BEDROOM,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_OF_THE_SINGLE_LAMP_PATH,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_OF_THE_SINGLE_LAMP_PATH,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BOTTOM_ROOM,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_ON_THE_ENTRANCE_PATH,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_ON_THE_ENTRANCE_PATH,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
    AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD,
    AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_TOP_RIGHT_ROOM,
    AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_TOP_RIGHT_ROOM,
    AquariaLocationNames.MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_TOP_RIGHT_ROOM,
    AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_BOTTOM_RIGHT_PATH,
    AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_BOTTOM_RIGHT_PATH,
    AquariaLocationNames.MITHALAS_CATHEDRAL_URN_BEHIND_THE_FLESH_VEIN,
    AquariaLocationNames.MITHALAS_CATHEDRAL_URN_IN_THE_TOP_LEFT_EYES_BOSS_ROOM,
    AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN,
    AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN,
    AquariaLocationNames.MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN,
    AquariaLocationNames.MITHALAS_CATHEDRAL_FOURTH_URN_IN_THE_TOP_RIGHT_ROOM,
    AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS,
    AquariaLocationNames.MITHALAS_CATHEDRAL_URN_BELOW_THE_LEFT_ENTRANCE,
    AquariaLocationNames.MITHALAS_CATHEDRAL_BULB_IN_THE_FLESH_ROOM_WITH_FLEAS,
    AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_IN_THE_CENTER_PART,
    AquariaLocationNames.CATHEDRAL_UNDERGROUND_FIRST_BULB_IN_THE_TOP_LEFT_PART,
    AquariaLocationNames.CATHEDRAL_UNDERGROUND_SECOND_BULB_IN_THE_TOP_LEFT_PART,
    AquariaLocationNames.CATHEDRAL_UNDERGROUND_THIRD_BULB_IN_THE_TOP_LEFT_PART,
    AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_CLOSE_TO_THE_SAVE_CRYSTAL,
    AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_IN_THE_BOTTOM_RIGHT_PATH,
    AquariaLocationNames.MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD,
    AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_BOTTOM_LEFT_CLEARING,
    AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_PATH_DOWN_FROM_THE_TOP_LEFT_CLEARING,
    AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_TOP_LEFT_CLEARING,
    AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG,
    AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG,
    AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_LEFT_OF_THE_CENTER_CLEARING,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_BIG_ROOM,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_SMALL_ROOM,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_CENTER_CLEARING,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BLACK_PEARL,
    AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS,
    AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS,
    AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY,
    AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_TRANSTURTLE,
    AquariaLocationNames.KELP_FOREST_BOTTOM_RIGHT_AREA_ODD_CONTAINER,
    AquariaLocationNames.KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD,
    AquariaLocationNames.KELP_FOREST_BOSS_ROOM_BULB_AT_THE_BOTTOM_OF_THE_AREA,
    AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_FISH_CAVE_PUZZLE,
    AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_INSIDE_THE_FISH_PASS,
    AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_IN_THE_SECOND_ROOM,
    AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_SEED_BAG,
    AquariaLocationNames.MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE,
    AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
    AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_IN_LI_S_CAVE,
    AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_TOP_RIGHT_PATH,
    AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_HIDDEN_BEHIND_THE_BLOCKING_ROCK,
    AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_TRANSTURTLE,
    AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS,
    AquariaLocationNames.TURTLE_CAVE_TURTLE_EGG,
    AquariaLocationNames.TURTLE_CAVE_BULB_IN_BUBBLE_CLIFF,
    AquariaLocationNames.TURTLE_CAVE_URCHIN_COSTUME,
    AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_IN_THE_MIDDLE_OF_THE_WALL_JUMP_CLIFF,
    AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_GOLDEN_STARFISH,
    AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
    AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_TRANSTURTLE,
    AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_LEFT_PATH,
    AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_SPIRIT_PATH,
    AquariaLocationNames.THE_VEIL_BOTTOM_AREA_VERSE_EGG,
    AquariaLocationNames.THE_VEIL_BOTTOM_AREA_STONE_HEAD,
    AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
    AquariaLocationNames.OCTOPUS_CAVE_BULB_IN_THE_PATH_BELOW_THE_OCTOPUS_CAVE_PATH,
    AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
    AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
    AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
    AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_LEFT_PART,
    AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_RIGHT_PART,
    AquariaLocationNames.SUN_TEMPLE_BULB_AT_THE_TOP_OF_THE_HIGH_DARK_ROOM,
    AquariaLocationNames.SUN_TEMPLE_GOLDEN_GEAR,
    AquariaLocationNames.SUN_TEMPLE_FIRST_BULB_OF_THE_TEMPLE,
    AquariaLocationNames.SUN_TEMPLE_BULB_ON_THE_RIGHT_PART,
    AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_HIDDEN_ROOM_OF_THE_RIGHT_PART,
    AquariaLocationNames.SUN_TEMPLE_SUN_KEY,
    AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_PATH_BULB,
    AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_PATH_BULB,
    AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB,
    AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB,
    AquariaLocationNames.SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD,
    AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_HIDDEN_PATH_ROOM,
    AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_RIGHT_PART,
    AquariaLocationNames.ABYSS_LEFT_AREA_GLOWING_SEED,
    AquariaLocationNames.ABYSS_LEFT_AREA_GLOWING_PLANT,
    AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS,
    AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM,
    AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_MIDDLE_PATH,
    AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_MIDDLE_PATH,
    AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_LEFT_GREEN_ROOM,
    AquariaLocationNames.ABYSS_RIGHT_AREA_TRANSTURTLE,
    AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_ROOM_TO_THE_RIGHT,
    AquariaLocationNames.ICE_CAVERN_FIRST_BULB_IN_THE_TOP_EXIT_ROOM,
    AquariaLocationNames.ICE_CAVERN_SECOND_BULB_IN_THE_TOP_EXIT_ROOM,
    AquariaLocationNames.ICE_CAVERN_THIRD_BULB_IN_THE_TOP_EXIT_ROOM,
    AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_LEFT_ROOM,
    AquariaLocationNames.KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY,
    AquariaLocationNames.KING_JELLYFISH_CAVE_JELLYFISH_COSTUME,
    AquariaLocationNames.THE_WHALE_VERSE_EGG,
    AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
    AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_IN_THE_LEFT_BOTTOM_ROOM,
    AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_IN_THE_LITTLE_PIPE_ROOM,
    AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
    AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_BEFORE_THE_BEDROOM,
    AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME,
    AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
    AquariaLocationNames.THE_BODY_CENTER_AREA_BREAKING_LI_S_CAGE,
    AquariaLocationNames.THE_BODY_CENTER_AREA_BULB_ON_THE_MAIN_PATH_BLOCKING_TUBE,
    AquariaLocationNames.THE_BODY_LEFT_AREA_FIRST_BULB_IN_THE_TOP_FACE_ROOM,
    AquariaLocationNames.THE_BODY_LEFT_AREA_SECOND_BULB_IN_THE_TOP_FACE_ROOM,
    AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_BELOW_THE_WATER_STREAM,
    AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_TOP_FACE_ROOM,
    AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM,
    AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_FACE_ROOM,
    AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_BOTTOM_FACE_ROOM,
    AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM,
    AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_JELLY_ZAP_ROOM,
    AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_NAUTILUS_ROOM,
    AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME,
    AquariaLocationNames.FINAL_BOSS_AREA_FIRST_BULB_IN_THE_TURTLE_ROOM,
    AquariaLocationNames.FINAL_BOSS_AREA_SECOND_BULB_IN_THE_TURTLE_ROOM,
    AquariaLocationNames.FINAL_BOSS_AREA_THIRD_BULB_IN_THE_TURTLE_ROOM,
    AquariaLocationNames.FINAL_BOSS_AREA_TRANSTURTLE,
    AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
    AquariaLocationNames.SIMON_SAYS_AREA_BEATING_SIMON_SAYS,
    AquariaLocationNames.BEATING_FALLEN_GOD,
    AquariaLocationNames.BEATING_MITHALAN_GOD,
    AquariaLocationNames.BEATING_DRUNIAN_GOD,
    AquariaLocationNames.BEATING_LUMEREAN_GOD,
    AquariaLocationNames.SUNKEN_CITY_BEATING_GOLEM,
    AquariaLocationNames.BEATING_THE_GOLEM,
    AquariaLocationNames.BEATING_NAUTILUS_PRIME,
    AquariaLocationNames.BEATING_BLASTER_PEG_PRIME,
    AquariaLocationNames.BEATING_MERGOG,
    AquariaLocationNames.BEATING_MITHALAN_PRIESTS,
    AquariaLocationNames.BEATING_OCTOPUS_PRIME,
    AquariaLocationNames.BEATING_CRABBIUS_MAXIMUS,
    AquariaLocationNames.BEATING_MANTIS_SHRIMP_PRIME,
    AquariaLocationNames.BEATING_KING_JELLYFISH_GOD_PRIME,
    AquariaLocationNames.FIRST_SECRET,
    AquariaLocationNames.SECOND_SECRET,
    AquariaLocationNames.THIRD_SECRET,
    AquariaLocationNames.OBJECTIVE_COMPLETE,
]


class AquariaTestBase(WorldTestBase):
    """Base class for Aquaria unit tests"""
    game = "Aquaria"

    def reachable_spot(self, state: CollectionState, player: int | None = None,
                       resolution_hint: str = "Location") -> typing.List[str]:
        """
        Retrieve a list of spot that can be reached from the current player with the given `state`.
        The `resolution_hint` parameter specifies which kind of spot to look for. It can take
        "Location", "Entrance" or "Region" as values. Defaults to "Location".
        """
        assert resolution_hint in ("Location", "Region", "Entrance")
        if resolution_hint == "Region":
            reachable_spot: typing.List[str] = [location.name for location in
                                                [region for region in self.multiworld.get_regions(player) if
                                                 region.can_reach(state)]]
        elif resolution_hint == "Entrance":
            reachable_spot: typing.List[str] = [location.name for location in
                                                [entrance for entrance in self.multiworld.get_entrances(player) if
                                                 entrance.can_reach(state)]]
        else:
            reachable_spot: typing.List[str] = [location.name for location in
                                                self.multiworld.get_reachable_locations(state, player)]
        return reachable_spot

    def assertAccessWith(self, spots: typing.List[str], item_names: typing.List[str],
                         initial_items: typing.List[str] = None, resolution_hint: str = "Location"):
        """
        Assert that when the items are not collect, the spots are not reachable, but when
        the items are collected, the spots are accessible. Also assert that no other new spots can be
        accessed when the items are collected.
        The `resolution_hint` parameter specifies which kind of spot to look for. It can take
        "Location", "Entrance" or "Region" as values. Defaults to "Location".
        """
        if initial_items is None:
            initial_items = []
        assert resolution_hint in ("Location", "Region", "Entrance")
        state = CollectionState(self.multiworld)
        for item in initial_items:
            state.collect(self.get_item_by_name(item))
        reachable_spot_before = self.reachable_spot(state, self.player, resolution_hint)
        for spot in spots:
            self.assertFalse(state.can_reach(spot, resolution_hint, self.player),
                             f"{spot} is reachable without {item_names}")
        items = self.get_items_by_name(item_names)
        for item in items:
            state.collect(item)
        reachable_spot_after = self.reachable_spot(state, self.player, resolution_hint)
        for spot in reachable_spot_before:
            reachable_spot_after.remove(spot)
        for spot in spots:
            self.assertTrue(state.can_reach(spot, resolution_hint, self.player),
                            f"{spot} is not reachable with {item_names}")
            reachable_spot_after.remove(spot)
        if len(reachable_spot_after) > 0:
            self.assertTrue(len(reachable_spot_after) == 0,
                            f"Reachable with {item_names} but not without: {reachable_spot_after}")

