from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str
    store_stock: int = 0


location_table: dict[str, LocationInfo] = {
    # Shallows
    "Shallows Piranha Chest": LocationInfo(10, "Shallows"),
    "Shallows Hidden Chest Near Gate": LocationInfo(11, "Shallows"),
    "Shallows Ruins Entrance Chest": LocationInfo(12, "Shallows"),
    "Shallows Bomb Blocked Chest 1": LocationInfo(13, "Shallows"),
    "Shallows Bomb Blocked Chest 2": LocationInfo(14, "Shallows"),
    "Ruins Left of Entrance Chest": LocationInfo(20, "Shallows"),
    "Ruins Center Chest": LocationInfo(21, "Ruins"),
    "Southwest of Ruins Chest": LocationInfo(22, "Spider"),
    "Piranha Cave Bomb Blocked Chest": LocationInfo(23, "Jelly"),
    "Piranha Cave Bottom Right Chest": LocationInfo(24, "Jelly"),
    "Boss Area Chest": LocationInfo(30, "Jelly"),
    "Slime Cave Upper Chest": LocationInfo(40, "Slime"),
    "Slime Cave Lower Chest": LocationInfo(41, "Slime"),
    "Eastern Cave Gift Chest": LocationInfo(50, "Shallows"),
    "Upper Spider Cave Chest": LocationInfo(60, "Spider"),
    "Lower Spider Cave Chest": LocationInfo(61, "Spider"),
    "Jelly Cave Chest": LocationInfo(70, "Jelly"),
    "Shallows Lever": LocationInfo(90, "Shallows"),
    "Ruins North Lever": LocationInfo(91, "Ruins"),
    "Boss Lever 1": LocationInfo(92, "Spider"),
    "Boss Lever 2": LocationInfo(93, "Jelly"),
    "Ruins Northeast Lever": LocationInfo(94, "Jelly"),
    "Ruins Southeast Lever": LocationInfo(95, "Jelly"),
    "Ruins Southwest Lever": LocationInfo(96, "Spider"),
    "Gift Area Emblem": LocationInfo(100, "Shallows"),
    "Slime Cave Emblem": LocationInfo(101, "Slime"),
    "Piranha Cave Emblem": LocationInfo(102, "Jelly"),
    "Slime Stick Store": LocationInfo(110, "Sticks"),
    "Slime Lance Store": LocationInfo(111, "Sticks"),
    "Slime Trident Store": LocationInfo(112, "Sticks"),
    "Shell Stick Store": LocationInfo(113, "Sticks"),
    "Shell Lance Store": LocationInfo(114, "Sticks"),
    "Shell Trident Store": LocationInfo(115, "Sticks"),
    "Elec Stick Store": LocationInfo(116, "Sticks"),
    "Elec Lance Store": LocationInfo(117, "Sticks"),
    "Elec Trident Store": LocationInfo(118, "Sticks"),
    "Slime Mallet Store": LocationInfo(120, "Mallets"),
    "Slime Sledge Store": LocationInfo(121, "Mallets"),
    "Shell Mallet Store": LocationInfo(122, "Mallets"),
    "Shell Sledge Store": LocationInfo(123, "Mallets"),
    "Elec Mallet Store": LocationInfo(124, "Mallets"),
    "Elec Sledge Store": LocationInfo(125, "Mallets"),
    "Slime Lid Store": LocationInfo(130, "Lids"),
    "Slime Buckler Store": LocationInfo(131, "Lids"),
    "Slime Tower Store": LocationInfo(132, "Lids"),
    "Shell Lid Store": LocationInfo(133, "Lids"),
    "Shell Buckler Store": LocationInfo(134, "Lids"),
    "Shell Tower Store": LocationInfo(135, "Lids"),
    "Elec Lid Store": LocationInfo(136, "Lids"),
    "Elec Buckler Store": LocationInfo(137, "Lids"),
    "Elec Tower Store": LocationInfo(138, "Lids"),
    "Small Potion Store": LocationInfo(140, "Potions"),
    "Medium Potion Store": LocationInfo(141, "Potions"),
    "Holy Potion Store": LocationInfo(142, "Potions"),
    "Evil Potion Store": LocationInfo(143, "Potions"),
    "Egg Store": LocationInfo(144, "Potions"),
    "Bomb Store": LocationInfo(150, "Bombs"),
    "Mist Orb Store": LocationInfo(151, "Bombs"),
    "Godblood Store": LocationInfo(152, "Bombs"),
    "Defeat Guelap": LocationInfo(200, "Ruins"),
    "Slime Stick Store 2": LocationInfo(210, "Sticks", 2),
    "Slime Lance Store 2": LocationInfo(211, "Sticks", 2),
    "Slime Trident Store 2": LocationInfo(212, "Sticks", 2),
    "Shell Stick Store 2": LocationInfo(213, "Sticks", 2),
    "Shell Lance Store 2": LocationInfo(214, "Sticks", 2),
    "Shell Trident Store 2": LocationInfo(215, "Sticks", 2),
    "Elec Stick Store 2": LocationInfo(216, "Sticks", 2),
    "Elec Lance Store 2": LocationInfo(217, "Sticks", 2),
    "Elec Trident Store 2": LocationInfo(218, "Sticks", 2),
    "Slime Mallet Store 2": LocationInfo(220, "Mallets", 2),
    "Slime Sledge Store 2": LocationInfo(221, "Mallets", 2),
    "Shell Mallet Store 2": LocationInfo(222, "Mallets", 2),
    "Shell Sledge Store 2": LocationInfo(223, "Mallets", 2),
    "Elec Mallet Store 2": LocationInfo(224, "Mallets", 2),
    "Elec Sledge Store 2": LocationInfo(225, "Mallets", 2),
    "Slime Lid Store 2": LocationInfo(230, "Lids", 2),
    "Slime Buckler Store 2": LocationInfo(231, "Lids", 2),
    "Slime Tower Store 2": LocationInfo(232, "Lids", 2),
    "Shell Lid Store 2": LocationInfo(233, "Lids", 2),
    "Shell Buckler Store 2": LocationInfo(234, "Lids", 2),
    "Shell Tower Store 2": LocationInfo(235, "Lids", 2),
    "Elec Lid Store 2": LocationInfo(236, "Lids", 2),
    "Elec Buckler Store 2": LocationInfo(237, "Lids", 2),
    "Elec Tower Store 2": LocationInfo(238, "Lids", 2),
    "Small Potion Store 2": LocationInfo(240, "Potions", 2),
    "Medium Potion Store 2": LocationInfo(241, "Potions", 2),
    "Holy Potion Store 2": LocationInfo(242, "Potions", 2),
    "Evil Potion Store 2": LocationInfo(243, "Potions", 2),
    "Egg Store 2": LocationInfo(244, "Potions", 2),
    "Bomb Store 2": LocationInfo(250, "Bombs", 2),
    "Mist Orb Store 2": LocationInfo(251, "Bombs", 2),
    "Godblood Store 2": LocationInfo(252, "Bombs", 2),
    "Slime Stick Store 3": LocationInfo(310, "Sticks", 3),
    "Slime Lance Store 3": LocationInfo(311, "Sticks", 3),
    "Slime Trident Store 3": LocationInfo(312, "Sticks", 3),
    "Shell Stick Store 3": LocationInfo(313, "Sticks", 3),
    "Shell Lance Store 3": LocationInfo(314, "Sticks", 3),
    "Shell Trident Store 3": LocationInfo(315, "Sticks", 3),
    "Elec Stick Store 3": LocationInfo(316, "Sticks", 3),
    "Elec Lance Store 3": LocationInfo(317, "Sticks", 3),
    "Elec Trident Store 3": LocationInfo(318, "Sticks", 3),
    "Slime Mallet Store 3": LocationInfo(320, "Mallets", 3),
    "Slime Sledge Store 3": LocationInfo(321, "Mallets", 3),
    "Shell Mallet Store 3": LocationInfo(322, "Mallets", 3),
    "Shell Sledge Store 3": LocationInfo(323, "Mallets", 3),
    "Elec Mallet Store 3": LocationInfo(324, "Mallets", 3),
    "Elec Sledge Store 3": LocationInfo(325, "Mallets", 3),
    "Slime Lid Store 3": LocationInfo(330, "Lids", 3),
    "Slime Buckler Store 3": LocationInfo(331, "Lids", 3),
    "Slime Tower Store 3": LocationInfo(332, "Lids", 3),
    "Shell Lid Store 3": LocationInfo(333, "Lids", 3),
    "Shell Buckler Store 3": LocationInfo(334, "Lids", 3),
    "Shell Tower Store 3": LocationInfo(335, "Lids", 3),
    "Elec Lid Store 3": LocationInfo(336, "Lids", 3),
    "Elec Buckler Store 3": LocationInfo(337, "Lids", 3),
    "Elec Tower Store 3": LocationInfo(338, "Lids", 3),
    "Small Potion Store 3": LocationInfo(340, "Potions", 3),
    "Medium Potion Store 3": LocationInfo(341, "Potions", 3),
    "Holy Potion Store 3": LocationInfo(342, "Potions", 3),
    "Evil Potion Store 3": LocationInfo(343, "Potions", 3),
    "Egg Store 3": LocationInfo(344, "Potions", 3),
    "Bomb Store 3": LocationInfo(350, "Bombs", 3),
    "Mist Orb Store 3": LocationInfo(351, "Bombs", 3),
    "Godblood Store 3": LocationInfo(352, "Bombs", 3),
    "Slime Stick Store 4": LocationInfo(410, "Sticks", 4),
    "Slime Lance Store 4": LocationInfo(411, "Sticks", 4),
    "Slime Trident Store 4": LocationInfo(412, "Sticks", 4),
    "Shell Stick Store 4": LocationInfo(413, "Sticks", 4),
    "Shell Lance Store 4": LocationInfo(414, "Sticks", 4),
    "Shell Trident Store 4": LocationInfo(415, "Sticks", 4),
    "Elec Stick Store 4": LocationInfo(416, "Sticks", 4),
    "Elec Lance Store 4": LocationInfo(417, "Sticks", 4),
    "Elec Trident Store 4": LocationInfo(418, "Sticks", 4),
    "Slime Mallet Store 4": LocationInfo(420, "Mallets", 4),
    "Slime Sledge Store 4": LocationInfo(421, "Mallets", 4),
    "Shell Mallet Store 4": LocationInfo(422, "Mallets", 4),
    "Shell Sledge Store 4": LocationInfo(423, "Mallets", 4),
    "Elec Mallet Store 4": LocationInfo(424, "Mallets", 4),
    "Elec Sledge Store 4": LocationInfo(425, "Mallets", 4),
    "Slime Lid Store 4": LocationInfo(430, "Lids", 4),
    "Slime Buckler Store 4": LocationInfo(431, "Lids", 4),
    "Slime Tower Store 4": LocationInfo(432, "Lids", 4),
    "Shell Lid Store 4": LocationInfo(433, "Lids", 4),
    "Shell Buckler Store 4": LocationInfo(434, "Lids", 4),
    "Shell Tower Store 4": LocationInfo(435, "Lids", 4),
    "Elec Lid Store 4": LocationInfo(436, "Lids", 4),
    "Elec Buckler Store 4": LocationInfo(437, "Lids", 4),
    "Elec Tower Store 4": LocationInfo(438, "Lids", 4),
    "Small Potion Store 4": LocationInfo(440, "Potions", 4),
    "Medium Potion Store 4": LocationInfo(441, "Potions", 4),
    "Holy Potion Store 4": LocationInfo(442, "Potions", 4),
    "Evil Potion Store 4": LocationInfo(443, "Potions", 4),
    "Egg Store 4": LocationInfo(444, "Potions", 4),
    "Bomb Store 4": LocationInfo(450, "Bombs", 4),
    "Mist Orb Store 4": LocationInfo(451, "Bombs", 4),
    "Godblood Store 4": LocationInfo(452, "Bombs", 4),
    "Slime Stick Store 5": LocationInfo(510, "Sticks", 5),
    "Slime Lance Store 5": LocationInfo(511, "Sticks", 5),
    "Slime Trident Store 5": LocationInfo(512, "Sticks", 5),
    "Shell Stick Store 5": LocationInfo(513, "Sticks", 5),
    "Shell Lance Store 5": LocationInfo(514, "Sticks", 5),
    "Shell Trident Store 5": LocationInfo(515, "Sticks", 5),
    "Elec Stick Store 5": LocationInfo(516, "Sticks", 5),
    "Elec Lance Store 5": LocationInfo(517, "Sticks", 5),
    "Elec Trident Store 5": LocationInfo(518, "Sticks", 5),
    "Slime Mallet Store 5": LocationInfo(520, "Mallets", 5),
    "Slime Sledge Store 5": LocationInfo(521, "Mallets", 5),
    "Shell Mallet Store 5": LocationInfo(522, "Mallets", 5),
    "Shell Sledge Store 5": LocationInfo(523, "Mallets", 5),
    "Elec Mallet Store 5": LocationInfo(524, "Mallets", 5),
    "Elec Sledge Store 5": LocationInfo(525, "Mallets", 5),
    "Slime Lid Store 5": LocationInfo(530, "Lids", 5),
    "Slime Buckler Store 5": LocationInfo(531, "Lids", 5),
    "Slime Tower Store 5": LocationInfo(532, "Lids", 5),
    "Shell Lid Store 5": LocationInfo(533, "Lids", 5),
    "Shell Buckler Store 5": LocationInfo(534, "Lids", 5),
    "Shell Tower Store 5": LocationInfo(535, "Lids", 5),
    "Elec Lid Store 5": LocationInfo(536, "Lids", 5),
    "Elec Buckler Store 5": LocationInfo(537, "Lids", 5),
    "Elec Tower Store 5": LocationInfo(538, "Lids", 5),
    "Small Potion Store 5": LocationInfo(540, "Potions", 5),
    "Medium Potion Store 5": LocationInfo(541, "Potions", 5),
    "Holy Potion Store 5": LocationInfo(542, "Potions", 5),
    "Evil Potion Store 5": LocationInfo(543, "Potions", 5),
    "Egg Store 5": LocationInfo(544, "Potions", 5),
    "Bomb Store 5": LocationInfo(550, "Bombs", 5),
    "Mist Orb Store 5": LocationInfo(551, "Bombs", 5),
    "Godblood Store 5": LocationInfo(552, "Bombs", 5),
    "Slime Stick Store 6": LocationInfo(610, "Sticks", 6),
    "Slime Lance Store 6": LocationInfo(611, "Sticks", 6),
    "Slime Trident Store 6": LocationInfo(612, "Sticks", 6),
    "Shell Stick Store 6": LocationInfo(613, "Sticks", 6),
    "Shell Lance Store 6": LocationInfo(614, "Sticks", 6),
    "Shell Trident Store 6": LocationInfo(615, "Sticks", 6),
    "Elec Stick Store 6": LocationInfo(616, "Sticks", 6),
    "Elec Lance Store 6": LocationInfo(617, "Sticks", 6),
    "Elec Trident Store 6": LocationInfo(618, "Sticks", 6),
    "Slime Mallet Store 6": LocationInfo(620, "Mallets", 6),
    "Slime Sledge Store 6": LocationInfo(621, "Mallets", 6),
    "Shell Mallet Store 6": LocationInfo(622, "Mallets", 6),
    "Shell Sledge Store 6": LocationInfo(623, "Mallets", 6),
    "Elec Mallet Store 6": LocationInfo(624, "Mallets", 6),
    "Elec Sledge Store 6": LocationInfo(625, "Mallets", 6),
    "Slime Lid Store 6": LocationInfo(630, "Lids", 6),
    "Slime Buckler Store 6": LocationInfo(631, "Lids", 6),
    "Slime Tower Store 6": LocationInfo(632, "Lids", 6),
    "Shell Lid Store 6": LocationInfo(633, "Lids", 6),
    "Shell Buckler Store 6": LocationInfo(634, "Lids", 6),
    "Shell Tower Store 6": LocationInfo(635, "Lids", 6),
    "Elec Lid Store 6": LocationInfo(636, "Lids", 6),
    "Elec Buckler Store 6": LocationInfo(637, "Lids", 6),
    "Elec Tower Store 6": LocationInfo(638, "Lids", 6),
    "Small Potion Store 6": LocationInfo(640, "Potions", 6),
    "Medium Potion Store 6": LocationInfo(641, "Potions", 6),
    "Holy Potion Store 6": LocationInfo(642, "Potions", 6),
    "Evil Potion Store 6": LocationInfo(643, "Potions", 6),
    "Egg Store 6": LocationInfo(644, "Potions", 6),
    "Bomb Store 6": LocationInfo(650, "Bombs", 6),
    "Mist Orb Store 6": LocationInfo(651, "Bombs", 6),
    "Godblood Store 6": LocationInfo(652, "Bombs", 6),
    "Garden": LocationInfo(997, "Shallows"),
    "Gold": LocationInfo(998, "Boss"),
    "Cherry": LocationInfo(999, "Boss")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> dict[str, int]:
    return {f"Divers - {name}": data.id_offset + get_game_base_id("Divers") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Divers": {f"Divers - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Divers" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Divers" in world.goal_games:
            if (loc_name == "Gold" and "Divers" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Divers - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Divers", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Divers", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break
        if loc_data.store_stock == 2 and world.options.divers_store_depth < 2:
            continue
        if loc_data.store_stock == 3 and world.options.divers_store_depth < 3:
            continue
        if loc_data.store_stock == 4 and world.options.divers_store_depth < 4:
            continue
        if loc_data.store_stock == 5 and world.options.divers_store_depth < 5:
            continue
        if loc_data.store_stock == 6 and world.options.divers_store_depth < 6:
            continue
        loc = Location(world.player, f"Divers - {loc_name}", get_game_base_id("Divers") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
