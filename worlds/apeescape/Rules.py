from typing import TYPE_CHECKING

from BaseClasses import Region, Item, ItemClassification, CollectionState
from .Regions import connect_regions, ApeEscapeLevel
from .Strings import AEItem, AEDoor, AELocation
from .RAMAddress import RAM

if TYPE_CHECKING:
    from . import ApeEscapeWorld


def set_rules(world: "ApeEscapeWorld"):
    # Detect if connected with UT and put the shuffled order back into the initialize_level_list function
    if hasattr(world.multiworld, "re_gen_passthrough"):
        levelids = world.passthrough["entranceids"]
        firstroomids = world.passthrough["firstrooms"]
        world.levellist = initialize_level_list(levelids)
        world.firstrooms = initialize_room_list(world, RAM.roomsperlevel, levelids, firstroomids)
    else:
        # Normal world generation
        world.levellist = initialize_level_list()
        # If entrances aren't shuffled, then we don't need to shuffle the entrances.
        if (world.options.entrance != 0x00):
            world.random.shuffle(world.levellist)
            # Some levels need to be kept at a specific entrance - put those back.
            world.levellist = fixed_levels(world.levellist, world.options.entrance, world.options.coin, world.options.goal)
        world.firstrooms = initialize_room_list(world, RAM.roomsperlevel)
    world.levellist = set_calculated_level_data(world.levellist, world.options.unlocksperkey, world.options.goal, world.options.coin)

    # Make a copy of the list for passing to the client for entrance shuffle purposes. We know this list has the levels sorted in the order they'd be presented in-game (so whatever is at the Fossil Field entrance first, etc.)
    world.entranceorder = list(world.levellist)
    # If entrances weren't shuffled, then this list is already sorted. We sort the list for ease of setting up access rules in the logic files.
    if (world.options.entrance != 0x00):
        world.levellist.sort()

    set_entrances(world, world.options.logic)
    set_doors(world, world.options.logic)
    set_transitions(world, world.options.logic)
    set_locations(world, world.options.logic)

    if world.using_ut:
        # For Out-of-logic checks in UT:
        # Re-gen entries/region rules with max difficulty (Expert) and glitched UT item
        set_entrances(world, "expert")
        set_doors(world, "expert")
        set_transitions(world, "expert")
        set_locations(world, "expert")


# Entrances are specifically connections between the Time Station (level select) and a level.
# If we ever want to change the starting room of a level, this is where we would set that room.
def set_entrances(self, logic):
    connect_regions(self, "Menu", AEDoor.TIME_ENTRY.value, lambda state: True)

    roomperlevelsKeys = list(RAM.roomsperlevel.keys())
    roomperlevelsValues = list(RAM.roomsperlevel.values())
    LevelperFirstRooms = []
    RoomRegion = []
    for y in self.firstrooms:
        LevelperFirstRooms.append(
            roomperlevelsKeys[[roomperlevelsValues[x].__contains__(y) for x in range(0, 22)].index(True)])
        RoomRegion.append(RAM.roomstostring[y])
    SortedEntries = [x for _, x in sorted(zip(LevelperFirstRooms, RoomRegion))]
    connect_regions(self, "Menu", SortedEntries[0], lambda state: Keys(state, self, self.levellist[0].keys))
    connect_regions(self, "Menu", SortedEntries[1], lambda state: Keys(state, self, self.levellist[1].keys))
    connect_regions(self, "Menu", SortedEntries[2], lambda state: Keys(state, self, self.levellist[2].keys))
    connect_regions(self, "Menu", SortedEntries[3], lambda state: Keys(state, self, self.levellist[3].keys))
    connect_regions(self, "Menu", SortedEntries[4], lambda state: Keys(state, self, self.levellist[4].keys))
    connect_regions(self, "Menu", SortedEntries[5], lambda state: Keys(state, self, self.levellist[5].keys))
    connect_regions(self, "Menu", SortedEntries[6], lambda state: Keys(state, self, self.levellist[6].keys))
    connect_regions(self, "Menu", SortedEntries[7], lambda state: Keys(state, self, self.levellist[7].keys))
    connect_regions(self, "Menu", SortedEntries[8], lambda state: Keys(state, self, self.levellist[8].keys))
    connect_regions(self, "Menu", SortedEntries[9], lambda state: Keys(state, self, self.levellist[9].keys))
    connect_regions(self, "Menu", SortedEntries[10], lambda state: Keys(state, self, self.levellist[10].keys))
    connect_regions(self, "Menu", SortedEntries[11], lambda state: Keys(state, self, self.levellist[11].keys))
    connect_regions(self, "Menu", SortedEntries[12], lambda state: Keys(state, self, self.levellist[12].keys))
    connect_regions(self, "Menu", SortedEntries[13], lambda state: Keys(state, self, self.levellist[13].keys))
    connect_regions(self, "Menu", SortedEntries[14], lambda state: Keys(state, self, self.levellist[14].keys))
    connect_regions(self, "Menu", SortedEntries[15], lambda state: Keys(state, self, self.levellist[15].keys))
    connect_regions(self, "Menu", SortedEntries[16], lambda state: Keys(state, self, self.levellist[16].keys))
    connect_regions(self, "Menu", SortedEntries[17], lambda state: Keys(state, self, self.levellist[17].keys))
    connect_regions(self, "Menu", SortedEntries[18], lambda state: Keys(state, self, self.levellist[18].keys))
    connect_regions(self, "Menu", SortedEntries[19], lambda state: Keys(state, self, self.levellist[19].keys))
    connect_regions(self, "Menu", SortedEntries[20], lambda state: Keys(state, self, self.levellist[20].keys))
    if self.options.goal == "ppm": # If Specter 2 is the goal, require enough keys and all monkeys.
        connect_regions(self, "Menu", SortedEntries[21], lambda state: Keys(state, self, self.levellist[21].keys) and HasAllMonkeys(state, self))
    elif self.options.goal == "ppmtoken": # If Specter 2 token is the goal, require enough keys and tokens.
        connect_regions(self, "Menu", SortedEntries[21], lambda state: Keys(state, self, self.levellist[21].keys) and Tokens(state, self, min(self.options.requiredtokens, self.options.totaltokens)))
    elif self.options.goal == "tokenhunt" or self.options.goal == "mmtoken": # If other token goal, just require keys.
        connect_regions(self, "Menu", SortedEntries[21], lambda state: Keys(state, self, self.levellist[21].keys))

    # If the goal is not token hunt, then there is a victory item on the worlds' final boss.
    if self.options.goal != "tokenhunt":
        # Redundant, but maybe relevant if we get more goals in the future
        if self.options.goal in ("mm","mmtoken","ppm","ppmtoken"):
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
    else:
        self.multiworld.completion_condition[self.player] = lambda state: Tokens(state, self, min(self.options.requiredtokens, self.options.totaltokens))


# A door is defined as a connection between rooms, typically bi-directional.
# For the logic behind door shuffle, this is the section to change.
def set_doors(self, logic):
    # I'm not sure if these have to be manually connected in both directions? There are a few one-ways in here, so probably better to be explicit?
    # Time Station
    connect_regions(self, AEDoor.TIME_MAIN_TRAINING.value, AEDoor.TIME_TRAINING_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MAIN_MINIGAME.value, AEDoor.TIME_MINIGAME_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_TRAINING_MAIN.value, AEDoor.TIME_MAIN_TRAINING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MINIGAME_MAIN.value, AEDoor.TIME_MAIN_MINIGAME.value,
                        lambda state: True)

    connect_regions(self, AEDoor.TIME_TRAINING_MAIN.value, AEDoor.TIME_TRAINING_WATERNET.value,
                    lambda state: True)

    # Fossil Field (level contains no doors)
    # Primordial Ooze (level contains no doors)
    # Molten Lava
    connect_regions(self, AEDoor.ML_ENTRY_VOLCANO.value, AEDoor.ML_VOLCANO_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY_TRICERATOPS.value, AEDoor.ML_TRICERATOPS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AEDoor.ML_ENTRY_VOLCANO.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AEDoor.ML_ENTRY_TRICERATOPS.value,
                        lambda state: True)
    # Thick Jungle
    connect_regions(self, AEDoor.TJ_ENTRY_MUSHROOM.value, AEDoor.TJ_MUSHROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_ENTRY_FISH.value, AEDoor.TJ_FISH_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_ENTRY_BOULDER.value, AEDoor.TJ_BOULDER_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_ENTRY_MUSHROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_FISH_ENTRY.value, AEDoor.TJ_ENTRY_FISH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_FISH_TENT.value, AEDoor.TJ_TENT_FISH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_TENT_FISH.value, AEDoor.TJ_FISH_TENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_BOULDER_TENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_ENTRY_BOULDER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_TENT_BOULDER.value,
                        lambda state: True)
    # Dark Ruins
    connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AEDoor.DR_FAN_OUTSIDE_FENCE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_HOLE.value, AEDoor.DR_FAN_OUTSIDE_HOLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value, AEDoor.DR_OBELISK_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, AEDoor.DR_OBELISK_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_BUTTON.value, AEDoor.DR_WATER_SIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, AEDoor.DR_WATER_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_FENCE.value, AEDoor.DR_OUTSIDE_FENCE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AEDoor.DR_OUTSIDE_HOLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OBELISK_TOP.value, AEDoor.DR_OUTSIDE_OBELISK_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_WATER_SIDE.value, AEDoor.DR_OUTSIDE_WATER_BUTTON.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_WATER_LEDGE.value, AEDoor.DR_OUTSIDE_WATER_LEDGE.value,
                        lambda state: True)
    # Cryptic Relics
    connect_regions(self, AEDoor.CR_ENTRY_SIDE_ROOM.value, AEDoor.CR_SIDE_ROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_ENTRY_MAIN_RUINS.value, AEDoor.CR_MAIN_RUINS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_SIDE_ROOM_ENTRY.value, AEDoor.CR_ENTRY_SIDE_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_MAIN_RUINS_ENTRY.value, AEDoor.CR_ENTRY_MAIN_RUINS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value,
                        lambda state: True)
    # Stadium Attack (level contains no doors)
    # Crabby Beach
    connect_regions(self, AEDoor.CB_ENTRY_SECOND_ROOM.value, AEDoor.CB_SECOND_ROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AEDoor.CB_ENTRY_SECOND_ROOM.value,
                        lambda state: True)
    # Coral Cave
    connect_regions(self, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value,
                        lambda state: True)
    # Dexter's Island
    connect_regions(self, AEDoor.DI_ENTRY_STOMACH.value, AEDoor.DI_STOMACH_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AEDoor.DI_ENTRY_STOMACH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_STOMACH_SLIDE_ROOM.value, AEDoor.DI_SLIDE_ROOM_STOMACH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_STOMACH_SLIDE_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY.value, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_SLIDE_ROOM_GALLERY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERY_TENTACLE.value, AEDoor.DI_TENTACLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_TENTACLE.value, AEDoor.DI_GALLERY_TENTACLE.value,
                        lambda state: True)
    # Snowy Mammoth (level contains no doors)
    # Frosty Retreat
    connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AEDoor.FR_CAVERNS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AEDoor.FR_ENTRY_CAVERNS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AEDoor.FR_WATER_CAVERNS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AEDoor.FR_CAVERNS_WATER.value,
                        lambda state: True)
    # Hot Springs
    connect_regions(self, AEDoor.HS_ENTRY_HOT_SPRING.value, AEDoor.HS_HOT_SPRING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value, AEDoor.HS_POLAR_BEAR_CAVE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_HOT_SPRING.value, AEDoor.HS_ENTRY_HOT_SPRING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value,
                        lambda state: True)
    # Gladiator Attack (level contains no doors)
    # Sushi Temple
    connect_regions(self, AEDoor.ST_ENTRY_TEMPLE.value, AEDoor.ST_TEMPLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY_WELL.value, AEDoor.ST_WELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_TEMPLE.value, AEDoor.ST_ENTRY_TEMPLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_WELL.value, AEDoor.ST_ENTRY_WELL.value,
                        lambda state: True)
    # Wabi Sabi Wall
    connect_regions(self, AEDoor.WSW_ENTRY_GONG.value, AEDoor.WSW_GONG_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AEDoor.WSW_ENTRY_GONG.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_GONG_MIDDLE.value, AEDoor.WSW_MIDDLE_GONG.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AEDoor.WSW_GONG_MIDDLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AEDoor.WSW_OBSTACLE_MIDDLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_MIDDLE_OBSTACLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_OBSTACLE_BARREL.value, AEDoor.WSW_BARREL_OBSTACLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AEDoor.WSW_OBSTACLE_BARREL.value,
                        lambda state: True)
    # Crumbling Castle
    connect_regions(self, AEDoor.CC_ENTRY_CASTLE.value, AEDoor.CC_CASTLEMAIN_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AEDoor.CC_BELL_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BASEMENT.value, AEDoor.CC_BASEMENT_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BOSS.value, AEDoor.CC_BOSS_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_ENTRY_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_BELL.value, AEDoor.CC_BELL_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_ELEVATOR_CASTLEMAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AEDoor.CC_ENTRY_BELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BELL_CASTLE.value, AEDoor.CC_CASTLEMAIN_BELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AEDoor.CC_CASTLEMAIN_ELEVATOR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ELEVATOR_BASEMENT.value, AEDoor.CC_BASEMENT_ELEVATOR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_ENTRY.value, AEDoor.CC_ENTRY_BASEMENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_ELEVATOR_BASEMENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BUTTON_BASEMENT_WATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_UP.value, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AEDoor.CC_BASEMENT_BUTTON_DOWN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value, AEDoor.CC_BASEMENT_BUTTON_UP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BOSS_ROOM.value, AEDoor.CC_ENTRY_BOSS.value,
                        lambda state: True)
    # City Park
    connect_regions(self, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AEDoor.CP_BARREL_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_BARREL_SEWERS_FRONT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARREL_OUTSIDE.value, AEDoor.CP_OUTSIDE_BARREL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARREL_SEWERS_FRONT.value, AEDoor.CP_SEWERSFRONT_BARREL.value,
                        lambda state: True)
    # Specter's Factory
    connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AEDoor.SF_FACTORY_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_OUTSIDE.value, AEDoor.SF_OUTSIDE_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_RC_CAR_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_WHEEL_FACTORY_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_MECH.value, AEDoor.SF_MECH_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_WHEEL_FACTORY_TOP.value, AEDoor.SF_FACTORY_WHEEL_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AEDoor.SF_FACTORY_MECH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_MECH_LAVA.value, AEDoor.SF_LAVA_MECH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_LAVA_MECH.value, AEDoor.SF_MECH_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_LAVA_CONVEYOR.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_LAVA_CONVEYOR.value,
                        lambda state: True)
    # Specter's Factory Conveyor Room
    connect_regions(self, AEDoor.SF_CONVEYOR1_ENTRY.value, AEDoor.SF_CONVEYOR1_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR2_ENTRY.value, AEDoor.SF_CONVEYOR1_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR3_ENTRY.value, AEDoor.SF_CONVEYOR2_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR4_ENTRY.value, AEDoor.SF_CONVEYOR3_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR5_ENTRY.value, AEDoor.SF_CONVEYOR4_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR6_ENTRY.value, AEDoor.SF_CONVEYOR5_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR7_ENTRY.value, AEDoor.SF_CONVEYOR6_EXIT.value,
                        lambda state: True)
    # TV Tower
    connect_regions(self, AEDoor.TVT_OUTSIDE_LOBBY.value, AEDoor.TVT_LOBBY_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_OUTSIDE_LOBBY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_LOBBY_WATER.value, AEDoor.TVT_WATER_LOBBY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_LOBBY_TANK.value, AEDoor.TVT_TANK_LOBBY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AEDoor.TVT_LOBBY_WATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AEDoor.TVT_LOBBY_TANK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_FAN.value, AEDoor.TVT_FAN_TANK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_BOSS.value, AEDoor.TVT_BOSS_TANK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_FAN_TANK.value, AEDoor.TVT_TANK_FAN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_BOSS_TANK.value, AEDoor.TVT_TANK_BOSS.value,
                        lambda state: True)
    # Monkey Madness
    connect_regions(self, AEDoor.MM_SL_HUB_WESTERN.value, AEDoor.MM_WESTERN_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_COASTER.value, AEDoor.MM_COASTER_ENTRY_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CIRCUS.value, AEDoor.MM_CIRCUS_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_GO_KARZ.value, AEDoor.MM_GO_KARZ_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CRATER.value, AEDoor.MM_CRATER_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AEDoor.MM_SL_HUB_WESTERN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AEDoor.MM_SL_HUB_COASTER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_COASTER1.value, AEDoor.MM_COASTER1_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CIRCUS_SL_HUB.value, AEDoor.MM_SL_HUB_CIRCUS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_GO_KARZ_SL_HUB.value, AEDoor.MM_SL_HUB_GO_KARZ.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER1_COASTER2.value, AEDoor.MM_COASTER2_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER2_HAUNTED_HOUSE.value, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COFFIN_COASTER_ENTRY.value, AEDoor.MM_COASTER_ENTRY_DISEMBARK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CRATER_SL_HUB.value, AEDoor.MM_SL_HUB_CRATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_SPECTER1.value, AEDoor.MM_SPECTER1_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value,
                        lambda state: True)


# A transition is defined as navigating between two doors in the same room.
def set_transitions(self, logic):
    # I'm not sure if these have to be manually connected in both directions? I think they do because connections are asymmetric.
    # Time Station
    connect_regions(self, AEDoor.TIME_ENTRY.value, AEDoor.TIME_MAIN_TRAINING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_ENTRY.value, AEDoor.TIME_MAIN_MINIGAME.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MAIN_TRAINING.value, AEDoor.TIME_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MAIN_MINIGAME.value, AEDoor.TIME_ENTRY.value,
                        lambda state: True)

    # Fossil Field (level contains a single room)
    # Primordial Ooze (level contains a single room)
    # Molten Lava
    connect_regions(self, AEDoor.ML_ENTRY.value, AEDoor.ML_ENTRY_VOLCANO.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY.value, AEDoor.ML_ENTRY_TRICERATOPS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY_VOLCANO.value, AEDoor.ML_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY_TRICERATOPS.value, AEDoor.ML_ENTRY.value,
                        lambda state: True)

    # Thick Jungle
    # Entry Room
    connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_MUSHROOM.value,
                        lambda state: True)
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_BOULDER.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_BOULDER.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_FISH.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_FISH.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.TJ_ENTRY_MUSHROOM.value, AEDoor.TJ_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_ENTRY_BOULDER.value, AEDoor.TJ_ENTRY.value, 
                        lambda state: CanDive(state, self))
    connect_regions(self, AEDoor.TJ_ENTRY_FISH.value, AEDoor.TJ_ENTRY.value, 
                        lambda state: CanSwim(state, self))
    # Mushroom Room
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_MUSHROOMMAIN.value, 
                        lambda state: HasFlyer(state, self) and CanHitWheel(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_MUSHROOMMAIN.value, 
                        lambda state: (IJ(state, self) or HasHoop(state, self) or (HasFlyer(state, self) and CanHitWheel(state, self))))
    else:
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_MUSHROOMMAIN.value, 
                        lambda state: IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    # Fish Room
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.TJ_FISH_ENTRY.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.TJ_FISH_ENTRY.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: CanSwim(state, self) or IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_FISH_TENT.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: CanHitWheel(state, self) and CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.TJ_FISH_TENT.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: (CanHitWheel(state, self) or SuperFlyer(state, self, AEDoor.TJ_FISH_TENT.value)) and CanSwim(state, self))
    connect_regions(self, AEDoor.TJ_FISHBOAT.value, AEDoor.TJ_FISH_ENTRY.value,
                        lambda state: True)
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AEDoor.TJ_FISH_TENT.value, 
                        lambda state: HasSling(state, self) or HasPunch(state, self) or (CanSwim(state, self) and CanHitMultiple(state, self)))
    else:
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AEDoor.TJ_FISH_TENT.value, 
                        lambda state: HasSling(state, self) or HasPunch(state, self) or (CanSwim(state, self) and CanHitMultiple(state, self)) or SuperFlyer(state, self, AEDoor.TJ_FISHBOAT.value))
    # Tent/Vine Room
    connect_regions(self, AEDoor.TJ_TENT_FISH.value, AEDoor.TJ_TENT_BOULDER.value,
                        lambda state: True)
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_TENT_FISH.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_TENT_FISH.value, 
                        lambda state: CanSwim(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_TENT_FISH.value, 
                        lambda state: CanSwim(state, self) or IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    # Boulder Room
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_BOULDER_TENT.value, 
                        lambda state: CanSwim(state, self) and (HasFlyer(state, self) or IJ(state, self)))
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_BOULDER_TENT.value, 
                        lambda state: CanSwim(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_BOULDER_ENTRY.value, 
                        lambda state: CanSwim(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_BOULDER_ENTRY.value, 
                        lambda state: CanSwim(state, self) or ((IJ(state, self) or HasHoop(state, self)) and HasFlyer(state, self)))
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_BOULDER_ENTRY.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))

    # Dark Ruins
    # Outside
    if logic == "normal":
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_FENCE.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_FENCE.value, 
                        lambda state: HasFlyer(state, self) or HasHoop(state, self) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_FENCE.value, 
                        lambda state: True)
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_HOLE.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_WATER_BUTTON.value, 
                        lambda state: CanHitOnce(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, 
                        lambda state: HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_HOLE.value, AEDoor.DR_ENTRY.value, 
                        lambda state: state.has("DR-Block", self.player, 1))
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_BUTTON.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, AEDoor.DR_OUTSIDE_HOLE.value,
                        lambda state: True)
    # Fan Basement
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_FENCE.value, AEDoor.DR_FAN_OUTSIDE_HOLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AEDoor.DR_FAN_OUTSIDE_FENCE.value,
                        lambda state: True)
    # Obelisk
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AEDoor.DR_OBELISK_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OBELISK_TOP.value, AEDoor.DR_OBELISK_BOTTOM.value,
                        lambda state: True)
    # Water Basement
    connect_regions(self, AEDoor.DR_WATER_SIDE.value, AEDoor.DR_WATER_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_WATER_LEDGE.value, AEDoor.DR_WATER_SIDE.value,
                        lambda state: True)

    # Cryptic Relics
    # Entry Area
    connect_regions(self, AEDoor.CR_ENTRY.value, AEDoor.CR_ENTRYOBA.value, 
                        lambda state: CanHitOnce(state, self))
    connect_regions(self, AEDoor.CR_ENTRY_SIDE_ROOM.value, AEDoor.CR_ENTRYOBA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_ENTRY_MAIN_RUINS.value, AEDoor.CR_ENTRYOBA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_ENTRYOBA.value, AEDoor.CR_ENTRY_SIDE_ROOM.value, 
                        lambda state: CanHitOnce(state, self))
    connect_regions(self, AEDoor.CR_ENTRYOBA.value, AEDoor.CR_ENTRY_MAIN_RUINS.value, 
                        lambda state: CanHitOnce(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CR_ENTRYOBA.value, AEDoor.CR_ENTRY.value, 
                        lambda state: HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.CR_ENTRYOBA.value, AEDoor.CR_ENTRY.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    # Relics
    connect_regions(self, AEDoor.CR_MAIN_RUINS_ENTRY.value, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, 
                        lambda state: HasSling(state, self) or HasPunch(state, self))
    connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AEDoor.CR_MAIN_RUINS_ENTRY.value, 
                        lambda state: CanHitOnce(state, self))

    # Stadium Attack (level contains a single room)
    # Crabby Beach
    connect_regions(self, AEDoor.CB_ENTRY.value, AEDoor.CB_ENTRY_SECOND_ROOM.value, 
                        lambda state: CB_Lamp(state, self))
    connect_regions(self, AEDoor.CB_ENTRY_SECOND_ROOM.value, AEDoor.CB_ENTRY.value,
                        lambda state: True)

    # Coral Cave
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, 
                        lambda state: CanSwim(state, self) or IJ(state, self) or (HasHoop(state, self) and SuperFlyer(state, self, AEDoor.CCAVE_ENTRY.value)))
    connect_regions(self, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, AEDoor.CCAVE_ENTRY.value, 
                        lambda state: CanDive(state, self))

    # Dexter's Island
    # Outside
    connect_regions(self, AEDoor.DI_ENTRY.value, AEDoor.DI_ENTRY_STOMACH.value, 
                        lambda state: CanHitOnce(state, self))
    connect_regions(self, AEDoor.DI_ENTRY_STOMACH.value, AEDoor.DI_ENTRY.value,
                        lambda state: True)
    # Stomach
    connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AEDoor.DI_STOMACH_SLIDE_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_STOMACH_SLIDE_ROOM.value, AEDoor.DI_STOMACH_ENTRY.value,
                        lambda state: True)
    # Slide
    if logic == "normal":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, 
                        lambda state: CanSwim(state, self) and CanHitMultiple(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, 
                        lambda state: CanHitMultiple(state, self))
    else:
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, 
                        lambda state: CanHitOnce(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY.value, 
                        lambda state: state.has("DI-Button", self.player, 1) and CanHitOnce(state, self))
    else:
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY.value, 
                        lambda state: (state.has("DI-Button", self.player, 1) and CanHitOnce(state, self)) or IJ(state, self))
    if logic == "expert": # This connection is only valid on expert difficulty.
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AEDoor.DI_SLIDE_ROOM_STOMACH.value, 
                        lambda state: IJ(state, self))
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY.value, AEDoor.DI_SLIDE_ROOM_STOMACH.value, 
                        lambda state: CanHitOnce(state, self))
    # Gallery
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, 
                        lambda state: CanDive(state, self))
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, 
                        lambda state: CanDive(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_GALLERYBOULDER.value, 
                        lambda state: HasHoop(state, self) or HasRC(state, self))
    else:
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_GALLERYBOULDER.value, 
                        lambda state: HasHoop(state, self) or HasRC(state, self) or IJ(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AEDoor.DI_GALLERY_TENTACLE.value, 
                        lambda state: DI_Lamp(state, self))
    connect_regions(self, AEDoor.DI_GALLERY_TENTACLE.value, AEDoor.DI_GALLERYBOULDER.value, 
                        lambda state: DI_Lamp(state, self))

    # Snowy Mammoth (level contains a single room)
    # Frosty Retreat
    # Outside
    if logic == "normal":
        connect_regions(self, AEDoor.FR_ENTRY.value, AEDoor.FR_ENTRY_CAVERNS.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.FR_ENTRY.value, AEDoor.FR_ENTRY_CAVERNS.value, 
                        lambda state: True)
    # Caverns
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AEDoor.FR_CAVERNS_WATER.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AEDoor.FR_CAVERNS_WATER.value, 
                        lambda state: True)
    connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AEDoor.FR_CAVERNS_ENTRY.value,
                        lambda state: True)

    # Hot Springs
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.HS_ENTRY.value, AEDoor.HS_ENTRY_HOT_SPRING.value, 
                        lambda state: HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.HS_ENTRY.value, AEDoor.HS_ENTRY_HOT_SPRING.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.HS_ENTRY.value, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_ENTRY_HOT_SPRING.value, AEDoor.HS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value, AEDoor.HS_ENTRY.value,
                        lambda state: True)

    # Gladiator Attack (level contains a single room)
    # Sushi Temple
    connect_regions(self, AEDoor.ST_ENTRY.value, AEDoor.ST_ENTRY_TEMPLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY.value, AEDoor.ST_ENTRY_WELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY_TEMPLE.value, AEDoor.ST_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY_WELL.value, AEDoor.ST_ENTRY.value,
                        lambda state: True)

    # Wabi Sabi Wall
    # Entry
    connect_regions(self, AEDoor.WSW_ENTRY.value, AEDoor.WSW_ENTRY_GONG.value,
                        lambda state: True)
    # Gong Room
    if logic == "normal":
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AEDoor.WSW_GONG_MIDDLE.value, 
                        lambda state: HasNet(state, self) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AEDoor.WSW_GONG_MIDDLE.value, 
                        lambda state: HasNet(state, self) or IJ(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.WSW_GONG_MIDDLE.value, AEDoor.WSW_GONG_ENTRY.value,
                        lambda state: True)
    # Middle
    if logic == "normal":
        connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AEDoor.WSW_MIDDLE_OBSTACLE.value, 
                        lambda state: HasSling(state, self) or HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AEDoor.WSW_MIDDLE_OBSTACLE.value, 
                        lambda state: HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AEDoor.WSW_MIDDLE_GONG.value,
                        lambda state: True)
    # Obstacle Course
    if logic == "normal":
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_OBSTACLE_BARREL.value, 
                        lambda state: CanHitWheel(state, self) or HasFlyer(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_OBSTACLE_BARREL.value, 
                        lambda state: CanHitWheel(state, self) or HasFlyer(state, self) or HasNet(state, self))
    else:
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_OBSTACLE_BARREL.value, 
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_OBSTACLE_BARREL.value, AEDoor.WSW_OBSTACLE_MIDDLE.value,
                        lambda state: True)

    # Crumbling Castle
    # Outside
    connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_CASTLE.value,
                        lambda state: True)
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_BASEMENT.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_BASEMENT.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_BELL.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.CC_ENTRY_CASTLE.value, AEDoor.CC_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BASEMENT.value, AEDoor.CC_ENTRY.value, 
                        lambda state: CanSwim(state, self))
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AEDoor.CC_ENTRY.value,
                        lambda state: True)
    # Boss Door - must be able to reach and hit the button in another room.
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AEDoor.CC_ENTRY_BOSS.value,
                        lambda state: state.has("CC-Button", self.player, 1) and CanHitOnce(state, self)) 
    # Castle
    connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAIN_BELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_BELL.value, AEDoor.CC_CASTLEMAIN_ENTRY.value,
                        lambda state: True)
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, 
                        lambda state: CRC_Lamp(state, self))
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, 
                        lambda state: CRC_Lamp(state, self) or SuperFlyer(state, self, AEDoor.CC_CASTLEMAIN_ENTRY.value) or IJ(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAIN_ENTRY.value, 
                        lambda state: HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAIN_ENTRY.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: CRC_Lamp(state, self))
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: CRC_Lamp(state, self) or IJ(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: HasFlyer(state, self) and CRC_Lamp(state, self))
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: (HasFlyer(state, self) and CRC_Lamp(state, self)) or IJ(state, self) or SuperFlyer(state, self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value))
    # Bell Tower
    connect_regions(self, AEDoor.CC_BELL_CASTLE.value, AEDoor.CC_BELL_ENTRY.value, 
                        lambda state: CanHitWheel(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AEDoor.CC_BELL_CASTLE.value,
                        lambda state: True)
    # Elevator Room
    if logic == "normal":
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AEDoor.CC_ELEVATOR_BASEMENT.value, 
                        lambda state: HasClub(state, self) or HasSling(state, self) or HasPunch(state, self))
    else:
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AEDoor.CC_ELEVATOR_BASEMENT.value, 
                        lambda state: CanHitOnce(state, self))
    connect_regions(self, AEDoor.CC_ELEVATOR_BASEMENT.value, AEDoor.CC_ELEVATOR_CASTLEMAIN.value,
                        lambda state: True)
    # Waterway
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ENTRY.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: CanSwim(state, self) and HasPunch(state, self))
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ENTRY.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: CanSwim(state, self) and (HasPunch(state, self) or IJ(state, self) or HasFlyer(state, self)))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: CanSwim(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: CanSwim(state, self) or SuperFlyer(state, self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value))
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: CanSwim(state, self) or SuperFlyer(state, self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value) or IJ(state, self))
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_UP.value, AEDoor.CC_BASEMENT_ELEVATOR.value,
                        lambda state: True)
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_ENTRY.value, 
                        lambda state: CanHitOnce(state, self) and (CanSwim(state, self) or HasFlyer(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_ENTRY.value, 
                        lambda state: CanHitOnce(state, self) and (CanSwim(state, self) or IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self)))
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_ENTRY.value, 
                        lambda state: CanHitOnce(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, 
                        lambda state: CanSwim(state, self) or IJ(state, self) or HasFlyer(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_UP.value, 
                        lambda state: IJ(state, self))
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_UP.value, 
                        lambda state: IJ(state, self) or HasFlyer(state, self))
    # Button Room
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value, AEDoor.CC_BUTTON_BASEMENT_WATER.value,
                        lambda state: True)
    
    # City Park
    # Outside
    connect_regions(self, AEDoor.CP_ENTRY.value, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, 
                        lambda state: CP_Lamp(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_ENTRY.value, AEDoor.CP_OUTSIDE_BARREL.value, 
                        lambda state: IJ(state, self) and CanDive(state, self))
    else:
        connect_regions(self, AEDoor.CP_ENTRY.value, AEDoor.CP_OUTSIDE_BARREL.value, 
                        lambda state: (IJ(state, self) or HasFlyer(state, self)) and CanDive(state, self))
    connect_regions(self, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, AEDoor.CP_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AEDoor.CP_ENTRY.value, 
                        lambda state: CanDive(state, self))
    # Front Sewer
    if logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_SEWERSFRONT_BARREL.value, 
                        lambda state: HasRC(state, self) and (CanSwim(state, self) or HasFlyer(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_SEWERSFRONT_BARREL.value, 
                        lambda state: (HasRC(state, self) or IJ(state, self)) and (CanSwim(state, self) or HasFlyer(state, self) or HasHoop(state, self)))
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_SEWERSFRONT_BARREL.value, 
                        lambda state: (HasRC(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value)) and (CanSwim(state, self) or HasFlyer(state, self) or HasHoop(state, self)))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, 
                        lambda state: HasRC(state, self) and (CanSwim(state, self) or HasFlyer(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, 
                        lambda state: HasRC(state, self) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, 
                        lambda state: HasRC(state, self) or IJ(state, self) or (HasHoop(state, self) and HasFlyer(state, self)))
    # Back Sewer
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CP_BARREL_SEWERS_FRONT.value, AEDoor.CP_BARRELSEWERMIDDLE.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.CP_BARREL_SEWERS_FRONT.value, AEDoor.CP_BARRELSEWERMIDDLE.value, 
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARREL_OUTSIDE.value, AEDoor.CP_BARRELSEWERMIDDLE.value, 
                        lambda state: CanDive(state, self))
    connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AEDoor.CP_BARREL_SEWERS_FRONT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AEDoor.CP_BARREL_OUTSIDE.value, 
                        lambda state: CanDive(state, self))

    # Specter's Factory
    # Outside
    connect_regions(self, AEDoor.SF_ENTRY.value, AEDoor.SF_OUTSIDE_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AEDoor.SF_ENTRY.value, 
                        lambda state: HasFlyer(state, self) or HasPunch(state, self))
    # Main Factory
    connect_regions(self, AEDoor.SF_FACTORY_OUTSIDE.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, 
                        lambda state: SF_Lamp(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: IJ(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: (HasHoop(state, self) and HasFlyer(state, self)) or SuperFlyer(state, self, AEDoor.SF_FACTORY_RC_CAR.value) or IJ(state, self))
    else:
        connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    if logic == "normal" or logic == "expert":
        connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_MECH.value, 
                        lambda state: CanHitWheel(state, self))
    else: # This is correct as CanHitWheel includes Flyer only on expert, making hard the unique.
        connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_MECH.value, 
                        lambda state: CanHitWheel(state, self) or SuperFlyer(state, self, AEDoor.SF_FACTORY_WHEEL_TOP.value))
    connect_regions(self, AEDoor.SF_FACTORY_MECH.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: CanHitWheel(state, self))
    # Triple Wheel
    if logic == "normal":
        connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_TOP.value, 
                        lambda state: HasClub(state, self) or ((HasSling(state, self) or HasPunch(state, self)) and HasFlyer(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_TOP.value, 
                        lambda state: HasClub(state, self) or ((HasSling(state, self) or HasPunch(state, self) or HasHoop(state, self)) and HasFlyer(state, self)) or SuperFlyer(state, self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value))
    else:
        connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_TOP.value, 
                        lambda state: HasClub(state, self) or HasHoop(state, self) or HasFlyer(state, self) or IJ(state, self) or (HasPunch(state, self) and (HasRadar(state, self) or HasSling(state, self) or HasRC(state, self) or HasNet(state, self))))
    connect_regions(self, AEDoor.SF_WHEEL_FACTORY_TOP.value, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value,
                        lambda state: True)
    # Mech Room
    connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AEDoor.SF_MECH_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_MECH_LAVA.value, AEDoor.SF_MECH_FACTORY.value,
                        lambda state: True)
    # Lava Room
    if logic == "normal" or logic == "expert":
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AEDoor.SF_LAVA_CONVEYOR.value, 
                        lambda state: CanHitWheel(state, self))
    else: # This is correct as CanHitWheel includes Flyer only on expert, making hard the unique.
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AEDoor.SF_LAVA_CONVEYOR.value, 
                        lambda state: CanHitWheel(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.SF_LAVA_CONVEYOR.value, AEDoor.SF_LAVA_MECH.value,
                        lambda state: True)
    # Conveyor Room (at least it's all True...)
    connect_regions(self, AEDoor.SF_CONVEYOR1_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR2_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR3_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR4_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR5_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR6_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR1_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR2_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR3_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR4_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR5_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR6_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR7_ENTRY.value,
                        lambda state: True)

    # TV Tower
    # Outside
    connect_regions(self, AEDoor.TVT_ENTRY.value, AEDoor.TVT_OUTSIDE_LOBBY.value,
                        lambda state: True)
    # Lobby
    if logic == "normal":
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_WATER.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_WATER.value,
                        lambda state: HasFlyer(state, self) or HasSling(state, self) or HasClub(state, self))
    else:
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_WATER.value, 
                        lambda state: HasFlyer(state, self) or HasSling(state, self) or HasHoop(state, self) or HasClub(state, self))
    connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_TANK.value, 
                        lambda state: TVT_Lobby_Lamp(state, self))
    connect_regions(self, AEDoor.TVT_LOBBY_WATER.value, AEDoor.TVT_LOBBY_OUTSIDE.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    connect_regions(self, AEDoor.TVT_LOBBY_TANK.value, AEDoor.TVT_LOBBY_OUTSIDE.value,
                        lambda state: True)
    # Tank Room
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AEDoor.TVT_TANK_FAN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AEDoor.TVT_TANK_BOSS.value, 
                        lambda state: TVT_Tank_Lamp(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TVT_TANK_FAN.value, AEDoor.TVT_TANK_LOBBY.value, 
                        lambda state: HasPunch(state, self))
    else:
        connect_regions(self, AEDoor.TVT_TANK_FAN.value, AEDoor.TVT_TANK_LOBBY.value, 
                        lambda state: HasPunch(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.TVT_TANK_FAN.value))
    connect_regions(self, AEDoor.TVT_TANK_BOSS.value, AEDoor.TVT_TANK_LOBBY.value,
                        lambda state: True)

    # Monkey Madness
    # Specter Land
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_WESTERN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_COASTER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_CIRCUS.value,
                        lambda state: True)
    # This is not a mistake because the apworld pre-opens the Jake arena as part of handling the Lobby door.
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_GO_KARZ.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_CRATER.value, 
                        lambda state: MM_DoubleDoor(state, self))
    connect_regions(self, AEDoor.MM_SL_HUB_WESTERN.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_COASTER.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CIRCUS.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_GO_KARZ.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CRATER.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    # Coaster (several one-way connections here)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AEDoor.MM_COASTER_ENTRY_COASTER1.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER1_ENTRY.value, AEDoor.MM_COASTER1_COASTER2.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER2_ENTRY.value, AEDoor.MM_COASTER2_HAUNTED_HOUSE.value,
                        lambda state: True)
    if logic == "normal":
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, 
                        lambda state: CanHitMultiple(state, self) or HasHoop(state, self))
    else:
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, 
                        lambda state: CanHitOnce(state, self))
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AEDoor.MM_COFFIN_COASTER_ENTRY.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_DISEMBARK.value, AEDoor.MM_COASTER_ENTRY_SL_HUB.value,
                        lambda state: True)
    # Crater
    connect_regions(self, AEDoor.MM_CRATER_SL_HUB.value, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value,
                        lambda state: True)
    if logic == "normal":
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AEDoor.MM_CRATER_SL_HUB.value, 
                        lambda state: HasFlyer(state, self))
    else:
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AEDoor.MM_CRATER_SL_HUB.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
    # Castle Outside
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value,
                        lambda state: MM_Lamp(state, self))
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
                        lambda state: True)
    # Castle Foyer
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, 
                        lambda state: HasHoop(state, self) and HasRC(state, self))
    else:
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, 
                        lambda state: HasRC(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_SPECTER1.value, 
                        lambda state: state.has("MM-Painting", self.player, 1))
    else:
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_SPECTER1.value, 
                        lambda state: state.has("MM-Painting", self.player, 1) or IJ(state, self) or SuperFlyer(state, self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value))
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, 
                        lambda state: HasHoop(state, self) or HasRC(state, self))
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, 
                        lambda state: state.has("MM-Button", self.player, 1) and (CanHitWheel(state, self) or HasFlyer(state, self)))
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value,
                        lambda state: True)
    # Monkey Head + Inside Climb + Outside Climb
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value,
                        lambda state: True)
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, 
                        lambda state: HasFlyer(state, self) and HasRC(state, self) and HasSling(state, self))
    else:
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, 
                        lambda state: (HasFlyer(state, self) and HasRC(state, self) and HasSling(state, self)) or IJ(state, self))


# A location is always accessed from a transition. The level entrance is a special case of a transition.
def set_locations(self, logic):

    # Time Station
    if self.options.mailbox == "true" or (self.options.shufflenet == "true" and self.options.coin == "true"):
        connect_regions(self, AEDoor.TIME_ENTRY.value, AELocation.Mailbox60.value,
                        lambda state: True)
        connect_regions(self, AEDoor.TIME_ENTRY.value, AELocation.Mailbox61.value,
                        lambda state: True)
        connect_regions(self, AEDoor.TIME_MINIGAME_MAIN.value, AELocation.Mailbox62.value,
                        lambda state: True)
        connect_regions(self, AEDoor.TIME_TRAINING_MAIN.value, AELocation.Mailbox63.value,
                        lambda state: True)

    # Fossil Field
    connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1Noonan.value,
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1Jorjy.value,
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1Nati.value,
                        lambda state: HasNet(state, self))
    if logic == "normal":
       connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1TrayC.value,
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
       connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1TrayC.value,
                        lambda state: HasNet(state, self))

    if self.options.coin == "true":
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Coin1.value,
                        lambda state: True)
    
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Mailbox1.value,
                        lambda state: True)
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Mailbox2.value,
                        lambda state: True)
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Mailbox3.value,
                        lambda state: CanHitOnce(state, self))
    
    # Primordial Ooze
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Shay.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2DrMonk.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Ahchoo.value, 
                        lambda state: HasNet(state, self) or HasWaterNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Grunt.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Grunt.value, 
                        lambda state: (CanSwim(state, self) or HasHoop(state, self) or HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Grunt.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Tyrone.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Gornif.value, 
                        lambda state: CanSwim(state, self) and (HasNet(state, self) or HasWaterNet(state, self)))
    else:
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Gornif.value, 
                        lambda state: HasNet(state, self) or HasWaterNet(state, self))

    if self.options.coin == "true":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Coin2.value,
                        lambda state: CanDive(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox4.value,
                        lambda state: True)
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox5.value,
                        lambda state: True)
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox6.value,
                        lambda state: True)
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox7.value,
                        lambda state: True)
    
    # Molten Lava
    # Outside
    connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3Scotty.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3Coco.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3JThomas.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3JThomas.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3Moggan.value, 
                        lambda state: HasNet(state, self))
    # Volcano
    connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AELocation.W1L3Barney.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AELocation.W1L3Mattie.value, 
                        lambda state: HasNet(state, self))
    # Triceratops
    if logic == "normal":
         connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.W1L3Rocky.value, 
                        lambda state: HasSling(state, self) and (HasClub(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
         connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.W1L3Rocky.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.Coin3.value,
                        lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.Mailbox8.value,
                        lambda state: True)
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.Mailbox9.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AELocation.Mailbox10.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.Mailbox11.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.Mailbox12.value, 
                        lambda state: HasSling(state, self))

    # Thick Jungle
    # Entry
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.W2L1Marquez.value, 
                        lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.W2L1Marquez.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.W2L1Livinston.value, 
                        lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.W2L1Livinston.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.W2L1George.value, 
                        lambda state: HasNet(state, self))
    # Mushroom
    connect_regions(self, AEDoor.TJ_MUSHROOMMAIN.value, AELocation.W2L1Gonzo.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.TJ_MUSHROOMMAIN.value, AELocation.W2L1Zanzibar.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.W2L1Alphonse.value, 
                        lambda state: HasFlyer(state, self) and CanHitWheel(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.W2L1Alphonse.value, 
                        lambda state: (IJ(state, self) or HasHoop(state, self) or (HasFlyer(state, self) and CanHitWheel(state, self))) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.W2L1Alphonse.value, 
                        lambda state: (IJ(state, self) or HasHoop(state, self) or (HasFlyer(state, self) and (CanHitMultiple(state, self) or HasRC(state, self))) or SuperFlyer(state, self, AEDoor.TJ_MUSHROOM_ENTRY.value)) and HasNet(state, self))
    # Fish
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.W2L1Maki.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.W2L1Maki.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.W2L1Herb.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.TJ_FISH_TENT.value, AELocation.W2L1Dilweed.value, 
                        lambda state: HasNet(state, self))
    # Tent
    connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.W2L1Stoddy.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.W2L1Mitong.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.W2L1Nasus.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.W2L1Nasus.value, 
                        lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    # Boulder
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AELocation.W2L1Elehcim.value, 
                        lambda state: CanSwim(state, self) and HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AELocation.W2L1Elehcim.value, 
                        lambda state: CanSwim(state, self) and HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AELocation.W2L1Elehcim.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AELocation.W2L1Elehcim.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AELocation.W2L1Selur.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AELocation.W2L1Selur.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))

    if self.options.coin == "true":
        if logic == "normal" or logic == "hard":
            connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Coin6.value, 
                            lambda state: HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Coin6.value, 
                            lambda state: IJ(state, self) or (HasHoop(state, self) and CanSwim(state, self)) or HasFlyer(state, self))
        connect_regions(self, AEDoor.TJ_MUSHROOMMAIN.value, AELocation.Coin7.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Coin8.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.Coin9.value, 
                        lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Mailbox13.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Mailbox14.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.Mailbox15.value, 
                        lambda state: CanHitOnce(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.Mailbox16.value, 
                            lambda state: HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.Mailbox16.value, 
                            lambda state: IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self))
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Mailbox17.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Mailbox18.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Mailbox19.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.Mailbox20.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AELocation.Mailbox21.value, 
                        lambda state: CanHitOnce(state, self))

    # Dark Ruins
    # Outside
    if logic == "normal":
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Kyle.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Kyle.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, AELocation.W2L2Kyle.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Stan.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Stan.value, 
                        lambda state: (HasFlyer(state, self) or HasHoop(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Stan.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AELocation.W2L2Stan.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Kenny.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, AELocation.W2L2Kenny.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Cratman.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.W2L2Mooshy.value, 
                        lambda state: HasNet(state, self))
    # Fan
    if logic == "normal":
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.W2L2Nuzzy.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.W2L2Nuzzy.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.W2L2Mav.value, 
                        lambda state: HasNet(state, self))
    # Obelisk
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.W2L2Papou.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.W2L2Trance.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.W2L2Bernt.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    # Water
    if logic == "normal":
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Runt.value, 
                        lambda state: (HasSling(state, self) or HasRC(state, self) or CanSwim(state, self)) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Runt.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasRC(state, self) or CanSwim(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Runt.value, 
                        lambda state: HasNet(state, self) or ((HasRC(state, self) or CanDive(state, self)) and HasWaterNet(state, self)))
    if logic == "normal":
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Hoolah.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Hoolah.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Chino.value, 
                        lambda state: (HasSling(state, self) or HasRC(state, self) or CanSwim(state, self)) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Chino.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasRC(state, self) or CanSwim(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.W2L2Chino.value, 
                        lambda state: HasNet(state, self) or ((HasRC(state, self) or CanDive(state, self)) and HasWaterNet(state, self)))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Coin11.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
        elif logic == "hard":
            connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Coin11.value, 
                            lambda state: HasFlyer(state, self) or HasHoop(state, self) or IJ(state, self))
        else:
            connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Coin11.value, 
                            lambda state: True)
        connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AELocation.Coin11.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.Coin12.value, 
                        lambda state: True)
        if logic == "normal":
            connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.Coin13.value, 
                            lambda state: HasRC(state, self) or HasPunch(state, self))
        else:
            connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.Coin13.value, 
                            lambda state: HasFlyer(state, self) or HasRC(state, self) or HasPunch(state, self))
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.Coin14.value, 
                        lambda state: CanDive(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox22.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox23.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox24.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox25.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.Mailbox26.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.Mailbox27.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.Mailbox28.value, 
                        lambda state: CanHitOnce(state, self))

    # Cryptic Relics
    # Entry
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.W2L3Bazzle.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.W2L3Bazzle.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.W2L3Freeto.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CR_ENTRYOBA.value, AELocation.W2L3Freeto.value, 
                        lambda state: IJ(state, self) and HasPunch(state, self) and HasNet(state, self))
    # Side Room
    if logic == "normal":
        connect_regions(self, AEDoor.CR_SIDE_ROOM_ENTRY.value, AELocation.W2L3Troopa.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CR_SIDE_ROOM_ENTRY.value, AELocation.W2L3Troopa.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    # Main Ruins
    connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.W2L3Stymie.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.W2L3Spanky.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and CanSwim(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.W2L3Spanky.value, 
                        lambda state: ((CanHitWheel(state, self) and CanSwim(state, self)) or IJ(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.W2L3Spanky.value, 
                        lambda state: ((CanHitWheel(state, self) and CanSwim(state, self)) or IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.W2L3Jesta.value, 
                        lambda state: ((CanHitWheel(state, self) or (HasFlyer(state, self) and CanSwim(state, self))) and HasNet(state, self)))
    # Pillar
    if logic == "normal":
        connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AELocation.W2L3Pally.value, 
                        lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AELocation.W2L3Pally.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AELocation.W2L3Crash.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AELocation.W2L3Crash.value, 
                        lambda state: (HasRC(state, self) or HasSling(state, self) or SuperFlyer(state, self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value)) and HasNet(state, self))
    
    if self.options.coin == "true":
        if logic == "normal" or logic == "hard":
            connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.Coin17.value, 
                            lambda state: (CanHitWheel(state, self) and CanSwim(state, self)) or IJ(state, self) or HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.Coin17.value, 
                            lambda state: (CanHitWheel(state, self) and CanSwim(state, self)) or IJ(state, self) or HasFlyer(state, self) or HasHoop(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.Mailbox29.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.Mailbox30.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.CR_MAIN_RUINS_ENTRY.value, AELocation.Mailbox31.value,
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.Mailbox32.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and CanSwim(state, self))
        connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AELocation.Mailbox33.value, 
                        lambda state: CanHitOnce(state, self))

    # Stadium Attack
    if self.options.coin == "true":
        connect_regions(self, AEDoor.SA_ENTRY.value, AEDoor.SA_COMPLETE.value, 
                        lambda state: CanSwim(state, self))

    # Crabby Beach
    # First
    connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.W4L1CoolBlue.value, 
                        lambda state: HasNet(state, self) or HasWaterNet(state, self))
    connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.W4L1Sandy.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.W4L1ShellE.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.W4L1Gidget.value, 
                        lambda state: HasNet(state, self))
    # Second
    connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.W4L1Shaka.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.W4L1Puka.value, 
                        lambda state: (HasFlyer(state, self) or CanHitMultiple(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.W4L1MaxMahalo.value, 
                        lambda state: HasFlyer(state, self) and HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.W4L1MaxMahalo.value, 
                        lambda state: (IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and (HasSling(state, self) or HasClub(state, self) or HasPunch(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.W4L1Moko.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.Coin21.value, 
                        lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.Mailbox34.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.Mailbox35.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.Mailbox36.value, 
                        lambda state: CanHitOnce(state, self))

    # Coral Cave
    # First
    if logic == "normal":
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Chip.value, 
                        lambda state: CanSwim(state, self) and HasWaterNet(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Chip.value, 
                        lambda state: CanSwim(state, self) and (HasNet(state, self) or HasWaterNet(state, self)))
    if logic == "normal":
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Oreo.value, 
                        lambda state: ((((HasHoop(state, self) and CanHitMultiple(state, self)) or HasSling(state, self)) and CanSwim(state, self)) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Oreo.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self) or HasHoop(state, self) or IJ(state, self)) and (CanHitWheel(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Puddles.value, 
                        lambda state: CanDive(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Puddles.value, 
                        lambda state: (CanDive(state, self) or (CanSwim(state, self) and IJ(state, self)) or SuperFlyer(state, self, AEDoor.CCAVE_ENTRY.value)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Puddles.value, 
                        lambda state: (CanDive(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.CCAVE_ENTRY.value) or (HasHoop(state, self) and HasFlyer(state, self))) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Kalama.value, 
                        lambda state: (((((HasHoop(state, self) and CanHitMultiple(state, self)) or HasSling(state, self)) and CanSwim(state, self)) or HasFlyer(state, self)) and HasNet(state, self)) or HasWaterNet(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_ENTRY.value, AELocation.W4L2Kalama.value, 
                        lambda state: ((CanSwim(state, self) or HasFlyer(state, self) or HasHoop(state, self) or IJ(state, self)) and (CanHitWheel(state, self) or HasFlyer(state, self)) and HasNet(state, self)) or HasWaterNet(state, self))
    # Second
    connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.W4L2Iz.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.W4L2BongBong.value, 
                        lambda state: (CanHitMultiple(state, self) or HasHoop(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.W4L2BongBong.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.W4L2Jux.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.W4L2Pickles.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.W4L2Pickles.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasRC(state, self) or HasPunch(state, self)) and HasNet(state, self))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Coin23.value, 
                            lambda state: CanDive(state, self))
        else:
            connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Coin23.value, 
                            lambda state: CanDive(state, self) or HasRC(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Mailbox37.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Mailbox38.value, 
                        lambda state: CanHitOnce(state, self))

    # Dexter's Island
    # Outside
    connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.W4L3TonTon.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.W4L3Stuw.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.W4L3Stuw.value, 
                        lambda state: (CanHitOnce(state, self) or CanSwim(state, self)) and HasNet(state, self))
    # Stomach
    if logic == "normal":
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.W4L3Mars.value, 
                        lambda state: HasRC(state, self) and (HasNet(state, self) or (CanDive(state, self) and HasWaterNet(state, self))))
    else:
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.W4L3Mars.value, 
                        lambda state: HasRC(state, self) and (HasNet(state, self) or HasWaterNet(state, self)))
    connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.W4L3Murky.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.W4L3Horke.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and CanHitMultiple(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.W4L3Horke.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.W4L3Horke.value, 
                        lambda state: (CanSwim(state, self) or IJ(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    # Slide
    # Gallery
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AELocation.W4L3Howeerd.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AELocation.W4L3Howeerd.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AELocation.W4L3Robbin.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AELocation.W4L3Robbin.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AELocation.W4L3Jakkee.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AELocation.W4L3Frederic.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AELocation.W4L3Baba.value, 
                        lambda state: HasNet(state, self))
    # Tentacle
    connect_regions(self, AEDoor.DI_TENTACLE.value, AELocation.W4L3Quirck.value, 
                        lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Coin24.value, 
                            lambda state: CanHitOnce(state, self))
        else:
            connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Coin24.value, 
                            lambda state: CanHitOnce(state, self) or CanSwim(state, self))
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.Coin25.value, 
                        lambda state: CanDive(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AELocation.Coin28.value, 
                            lambda state: CanSwim(state, self) and (HasPunch(state, self) or HasNet(state, self)))
        else:
            connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AELocation.Coin28.value, 
                            lambda state: HasPunch(state, self) or HasNet(state, self))
        if logic == "hard": # This connection does not exist on normal difficulty!
            connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AELocation.Coin28.value, 
                            lambda state: (HasClub(state, self) or HasPunch(state, self) or IJ(state, self)) and (HasPunch(state, self) or HasNet(state, self)))
        elif logic == "expert":
            connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AELocation.Coin28.value, 
                            lambda state: (HasClub(state, self) or HasPunch(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value)) and (HasPunch(state, self) or HasNet(state, self)))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Mailbox39.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Mailbox40.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AELocation.Mailbox41.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, AELocation.Mailbox42.value, 
                        lambda state: CanHitOnce(state, self))

    # Snowy Mammoth
    connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Popcicle.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Iced.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Rickets.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Rickets.value, 
                        lambda state: (HasSling(state, self) or (HasClub(state, self) and HasFlyer(state, self))) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Rickets.value, 
                        lambda state: (HasSling(state, self) or HasPunch(state, self) or (HasClub(state, self) and HasFlyer(state, self))) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Skeens.value, 
                        lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Skeens.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Denggoy.value, 
                        lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Denggoy.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Chilly.value, 
                        lambda state: (CanHitMultiple(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.W5L1Chilly.value, 
                        lambda state: HasNet(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Coin29.value, 
                        lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox43.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox44.value, 
                        lambda state: CanHitOnce(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox45.value, 
                            lambda state: CanHitMultiple(state, self) or HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox45.value, 
                            lambda state: True)

    # Frosty Retreat
    # Entry
    connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AELocation.W5L2Storm.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AELocation.W5L2Qube.value, 
                        lambda state: HasNet(state, self))
    # Water
    if logic == "normal":
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Ranix.value, 
                        lambda state: (CanSwim(state, self) and HasNet(state, self)) or (HasSling(state, self) and CanDive(state, self) and HasWaterNet(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Ranix.value, 
                        lambda state: (CanSwim(state, self) and HasNet(state, self)) or ((HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and CanDive(state, self) and HasWaterNet(state, self)))
    else:
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Ranix.value, 
                        lambda state: ((CanSwim(state, self) or IJ(state, self) or (HasSling(state, self) and HasHoop(state, self) and HasFlyer(state, self))) and HasNet(state, self)) or ((HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and (HasNet(state, self) or (CanDive(state, self) and HasWaterNet(state, self)))))
    if logic == "normal":
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Sharpe.value, 
                        lambda state: (CanSwim(state, self) or HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Sharpe.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Sticky.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Droog.value, 
                        lambda state: CanDive(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.W5L2Droog.value, 
                        lambda state: (CanDive(state, self) or HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    # Caverns
    connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AELocation.W5L2Gash.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AELocation.W5L2Kundra.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AELocation.W5L2Shadow.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AELocation.W5L2Shadow.value, 
                        lambda state: HasNet(state, self))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AELocation.Coin30.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
        else:
            connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AELocation.Coin30.value, 
                            lambda state: True)
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.Coin31.value, 
                        lambda state: CanDive(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AELocation.Coin32.value, 
                            lambda state: CanSwim(state, self) or HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AELocation.Coin32.value, 
                            lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AELocation.Mailbox46.value, 
                        lambda state: CanHitOnce(state, self))

    # Hot Springs
    # Entry
    connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.W5L3Punky.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.W5L3Ameego.value, 
                        lambda state: CanDive(state, self) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.W5L3Yoky.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.W5L3Yoky.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.W5L3Jory.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.W5L3Jory.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.HS_ENTRY_HOT_SPRING.value, AELocation.W5L3Yoky.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.HS_ENTRY_HOT_SPRING.value, AELocation.W5L3Jory.value, 
                        lambda state: HasNet(state, self))
    # Onsen
    connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.W5L3Crank.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.W5L3Claxter.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.W5L3Looza.value, 
                        lambda state: HasNet(state, self))
    # Polar Bear
    if logic == "normal":
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.W5L3Roti.value, 
                        lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.W5L3Roti.value, 
                        lambda state: (CanHitMultiple(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.HS_POLAR_BEAR_CAVE.value)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.W5L3Dissa.value, 
                        lambda state: CanHitMultiple(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.W5L3Dissa.value, 
                        lambda state: (CanHitMultiple(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.HS_POLAR_BEAR_CAVE.value)) and HasNet(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.Coin34.value, 
                        lambda state: True)
        if logic == "normal":
            connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.Coin35.value, 
                            lambda state: CanHitMultiple(state, self))
        else:
            connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.Coin35.value, 
                            lambda state: CanHitMultiple(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.HS_POLAR_BEAR_CAVE.value))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.Mailbox47.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and CanHitOnce(state, self))
        connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.Mailbox48.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.Mailbox49.value, 
                        lambda state: True)

    # Gladiator Attack
    if self.options.coin == "true":
        connect_regions(self, AEDoor.GA_ENTRY.value, AEDoor.GA_COMPLETE.value, 
                        lambda state: HasFlyer(state, self))

    # Sushi Temple
    # Entry
    connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.W7L1Taku.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.W7L1Rocka.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.W7L1Maralea.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.W7L1Wog.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.W7L1Wog.value, 
                        lambda state: (HasSling(state, self) or HasClub(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    # Temple
    connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Mayi.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Owyang.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Long.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Elly.value, 
                        lambda state: HasFlyer(state, self) and (HasHoop(state, self) or HasSling(state, self) or HasRC(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Elly.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Chunky.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.W7L1Chunky.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    # Well
    if logic == "normal":
        connect_regions(self, AEDoor.ST_WELL.value, AELocation.W7L1Voti.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.ST_WELL.value, AELocation.W7L1Voti.value, 
                        lambda state: (HasSling(state, self) or (HasHoop(state, self) and HasFlyer(state, self)) or SuperFlyer(state, self, AEDoor.ST_WELL.value)) and HasNet(state, self))
    connect_regions(self, AEDoor.ST_WELL.value, AELocation.W7L1QuelTin.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.ST_WELL.value, AELocation.W7L1Phaldo.value, 
                        lambda state: HasNet(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.Coin37.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.Coin38.value, 
                        lambda state: True)
        if logic == "normal":
            connect_regions(self, AEDoor.ST_WELL.value, AELocation.Coin39.value, 
                            lambda state: HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.ST_WELL.value, AELocation.Coin39.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.Mailbox50.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.Mailbox51.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.ST_WELL.value, AELocation.Mailbox52.value, 
                        lambda state: CanHitOnce(state, self))

    # Wabi Sabi Wall
    # Entry
    connect_regions(self, AEDoor.WSW_ENTRY_GONG.value, AELocation.W7L2Minky.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.WSW_ENTRY_GONG.value, AELocation.W7L2Zobbro.value, 
                        lambda state: HasNet(state, self))
    # Gong
    connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.W7L2Xeeto.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.W7L2Moops.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.W7L2Zanabi.value, 
                        lambda state: HasNet(state, self))
    # Middle
    connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AELocation.W7L2Doxs.value, 
                        lambda state: HasNet(state, self))
    # Obstacle Course
    connect_regions(self, AEDoor.WSW_OBSTACLE_BARREL.value, AELocation.W7L2Buddha.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AELocation.W7L2Fooey.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AELocation.W7L2Fooey.value, 
                        lambda state: (HasSling(state, self) or HasRC(state, self)) and HasNet(state, self))
    # Barrel
    if logic == "normal":
        connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.W7L2Kong.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.W7L2Kong.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.W7L2Phool.value, 
                        lambda state: (HasFlyer(state, self) or HasSling(state, self) or (HasHoop(state, self) and (HasClub(state, self) or HasPunch(state, self)))) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.W7L2Phool.value, 
                        lambda state: (HasFlyer(state, self) or HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.WSW_ENTRY_GONG.value, AELocation.Coin40.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.Coin41.value, 
                        lambda state: HasNet(state, self))
        if logic == "normal" or logic == "hard":
            connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.Coin44.value, 
                            lambda state: HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.Coin44.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.Mailbox53.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AELocation.Mailbox54.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AELocation.Mailbox55.value, 
                        lambda state: CanHitOnce(state, self))
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AELocation.Mailbox56.value, 
                        lambda state: CanHitWheel(state, self) or HasFlyer(state, self))

    # Crumbling Castle
    # Outside
    connect_regions(self, AEDoor.CC_ENTRY.value, AELocation.W7L3Robart.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_ENTRY.value, AELocation.W7L3Igor.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_ENTRY.value, AELocation.W7L3Naners.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AELocation.W7L3Neeners.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AELocation.W7L3Charles.value, 
                        lambda state: HasPunch(state, self) and HasNet(state, self))
    # Castle
    connect_regions(self, AEDoor.CC_CASTLEMAINTHRONEROOM.value, AELocation.W7L3Gustav.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_CASTLEMAINTHRONEROOM.value, AELocation.W7L3Wilhelm.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_CASTLEMAINTHRONEROOM.value, AELocation.W7L3Emmanuel.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_CASTLEMAINTHRONEROOM.value, AELocation.W7L3SirCutty.value, 
                        lambda state: HasNet(state, self))
    # Waterway
    connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AELocation.W7L3Calligan.value, 
                        lambda state: (HasPunch(state, self) or CanDive(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AELocation.W7L3Castalist.value, 
                        lambda state: CanDive(state, self) and HasWaterNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AELocation.W7L3Deveneom.value, 
                        lambda state: HasWaterNet(state, self) or (HasNet(state, self) and CanSwim(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AELocation.W7L3Deveneom.value, 
                        lambda state: HasWaterNet(state, self) or (HasNet(state, self) and (HasFlyer(state, self) or CanSwim(state, self))))
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AELocation.W7L3Deveneom.value, 
                        lambda state: HasWaterNet(state, self) or (HasNet(state, self) and (HasFlyer(state, self) or IJ(state, self) or CanSwim(state, self))))
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AELocation.W7L3Deveneom.value,
                        lambda state: (HasNet(state, self) or HasWaterNet(state, self)))
    # Button Room
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AELocation.W7L3Astur.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AELocation.W7L3Kilserack.value, 
                        lambda state: HasNet(state, self) or (HasWaterNet(state, self) and CanDive(state, self)))
    # Elevator
    connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AELocation.W7L3Ringo.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AELocation.W7L3Densil.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AELocation.W7L3Figero.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AELocation.W7L3Figero.value, 
                        lambda state: HasNet(state, self))
    # Bell Tower
    connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AELocation.W7L3Fej.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AELocation.W7L3Joey.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AELocation.W7L3Joey.value, 
                        lambda state: (HasHoop(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AELocation.W7L3Joey.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CC_BELL_CASTLE.value, AELocation.W7L3Donqui.value, 
                        lambda state: HasNet(state, self))
    # Boss Room
    connect_regions(self, AEDoor.CC_BOSS_ROOM.value, AELocation.Boss73.value, 
                        lambda state: CanHitMultiple(state, self))
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AELocation.Coin45.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.CC_CASTLEMAINTHRONEROOM.value, AELocation.Coin46.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AELocation.Coin49.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AELocation.Coin50.value, 
                        lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CC_ENTRY.value, AELocation.Mailbox57.value, 
                        lambda state: CanHitOnce(state, self))

    # City Park
    # Outside
    if logic == "normal":
        connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.W8L1Kaine.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.W8L1Kaine.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.W8L1Jaxx.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.W8L1Gehry.value, 
                        lambda state: IJ(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.W8L1Gehry.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.W8L1Alcatraz.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AELocation.W8L1Gehry.value, 
                        lambda state: CanDive(state, self) and HasNet(state, self))
    # Front Sewer
    connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.W8L1Tino.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.W8L1QBee.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.W8L1QBee.value, 
                        lambda state: (HasRC(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value)) and HasNet(state, self))
    connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.W8L1McManic.value, 
                        lambda state: (HasRC(state, self) or HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.W8L1QBee.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.W8L1QBee.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.W8L1McManic.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and HasRC(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.W8L1McManic.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.W8L1McManic.value, 
                        lambda state: (HasRC(state, self) or IJ(state, self) or (HasHoop(state, self) and HasFlyer(state, self))) and HasNet(state, self))
    # Back Sewer
    connect_regions(self, AEDoor.CP_BARREL_SEWERS_FRONT.value, AELocation.W8L1Dywan.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1CKHutch.value, 
                        lambda state: CanDive(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1Winky.value, 
                        lambda state: HasNet(state, self) or (CanDive(state, self) and HasWaterNet(state, self)))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1BLuv.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1BLuv.value, 
                        lambda state: (CanSwim(state, self) or HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1Camper.value, 
                        lambda state: CanDive(state, self) and (HasWaterNet(state, self) or HasNet(state, self)))
    else:
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1Camper.value, 
                        lambda state: (CanDive(state, self) and (HasWaterNet(state, self) or HasNet(state, self))) or ((IJ(state, self) or SuperFlyer(state, self, AEDoor.CP_BARRELSEWERMIDDLE.value)) and HasRC(state, self) and HasNet(state, self)))
    if logic == "normal":
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1Huener.value, 
                        lambda state: CanSwim(state, self) and HasFlyer(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1Huener.value, 
                        lambda state: (CanSwim(state, self) or HasHoop(state, self)) and HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.W8L1Huener.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.Coin53.value, 
                            lambda state: IJ(state, self))
        else:
            connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.Coin53.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
        connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AELocation.Coin53.value, 
                        lambda state: CanDive(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.Coin54.value, 
                            lambda state: HasRC(state, self))
        elif logic == "hard":
            connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.Coin54.value, 
                            lambda state: HasRC(state, self) or IJ(state, self))
        else:
            connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.Coin54.value, 
                            lambda state: HasRC(state, self) or IJ(state, self) or (SuperFlyer(state, self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value)))
        if logic == "normal" or logic == "hard":
            connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.Coin54.value, 
                            lambda state: HasRC(state, self))
        else:
            connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.Coin54.value, 
                            lambda state: (HasRC(state, self) or IJ(state, self) or (HasHoop(state, self) and HasFlyer(state, self))))
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.Coin55.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))

    # Specter's Factory
    # Outside
    connect_regions(self, AEDoor.SF_ENTRY.value, AELocation.W8L2BigShow.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AELocation.W8L2Dreos.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AELocation.W8L2BigShow.value, 
                        lambda state: (HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AELocation.W8L2BigShow.value, 
                        lambda state: HasNet(state, self))
    # Factory
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AELocation.W8L2Reznor.value, 
                        lambda state: HasNet(state, self))
    # Car Room
    if logic == "normal":
        connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AELocation.W8L2Urkel.value, 
                        lambda state: (HasRC(state, self) or HasPunch(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AELocation.W8L2Urkel.value, 
                        lambda state: (HasRC(state, self) or HasPunch(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.SF_RC_CAR_FACTORY.value) or (HasHoop(state, self) and HasFlyer(state, self))) and HasNet(state, self))
    # Lava Room
    connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.W8L2VanillaS.value, 
                        lambda state: HasPunch(state, self) and HasNet(state, self))
    if logic == "normal" or logic == "expert":
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.W8L2Radd.value, 
                        lambda state: CanHitWheel(state, self) and HasNet(state, self))
    else: # This is correct as CanHitWheel includes Flyer only on expert, making hard the unique.
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.W8L2Radd.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.W8L2Shimbo.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.W8L2Shimbo.value, 
                        lambda state: (HasRC(state, self) or HasSling(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.W8L2Shimbo.value, 
                        lambda state: HasNet(state, self))
    # Conveyor Room
    if logic == "normal":
        connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AELocation.W8L2Hurt.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self)) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AELocation.W8L2Hurt.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self) or HasSling(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AELocation.W8L2Hurt.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self) or HasSling(state, self) or HasHoop(state, self) or HasRC(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AELocation.W8L2String.value, 
                        lambda state: HasNet(state, self))
    # Mech Room
    if logic == "normal":
        connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AELocation.W8L2Khamo.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self)) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AELocation.W8L2Khamo.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self) or HasSling(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AELocation.W8L2Khamo.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self) or HasSling(state, self) or HasHoop(state, self) or HasRC(state, self)) and HasNet(state, self))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AELocation.Coin58.value, 
                            lambda state: HasRC(state, self) or HasPunch(state, self) or IJ(state, self))
        else:
            connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AELocation.Coin58.value, 
                            lambda state: HasRC(state, self) or HasPunch(state, self) or IJ(state, self) or SuperFlyer(state, self, AEDoor.SF_RC_CAR_FACTORY.value) or (HasHoop(state, self) and HasFlyer(state, self)))
        if logic == "normal" or logic == "expert": # CanHitWheel includes Flyer on expert.
            connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.Coin59.value, 
                            lambda state: CanHitWheel(state, self))
        else:
            connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.Coin59.value, 
                            lambda state: CanHitWheel(state, self) or HasFlyer(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.SF_ENTRY.value, AELocation.Mailbox58.value, 
                        lambda state: True)

    # TV Tower
    # Outside
    connect_regions(self, AEDoor.TVT_OUTSIDE_LOBBY.value, AELocation.W8L3Fredo.value,
                        lambda state: HasPunch(state, self) and HasNet(state, self))
    # Basement
    if logic == "normal":
        connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AELocation.W8L3Charlee.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AELocation.W8L3Charlee.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AELocation.W8L3Mach3.value, 
                        lambda state: HasNet(state, self) or HasWaterNet(state, self))
    # Lobby
    connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AELocation.W8L3Tortuss.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AELocation.W8L3Manic.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AELocation.W8L3Manic.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self) or HasHoop(state, self)) and HasNet(state, self))
    # Tank
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AELocation.W8L3Ruptdis.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AELocation.W8L3Eighty7.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.TVT_TANK_FAN.value, AELocation.W8L3Danio.value, 
                        lambda state: HasNet(state, self))
    # Fan
    connect_regions(self, AEDoor.TVT_FAN_TANK.value, AELocation.W8L3Roosta.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.TVT_FAN_TANK.value, AELocation.W8L3Tellis.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.TVT_FAN_TANK.value, AELocation.W8L3Whack.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    connect_regions(self, AEDoor.TVT_FAN_TANK.value, AELocation.W8L3Frostee.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    # Boss
    if logic == "normal":
        connect_regions(self, AEDoor.TVT_BOSS_TANK.value, AELocation.Boss83.value, 
                        lambda state: HasSling(state, self))
    else:
        connect_regions(self, AEDoor.TVT_BOSS_TANK.value, AELocation.Boss83.value, 
                        lambda state: HasSling(state, self) or (HasFlyer(state, self) and HasRC(state, self)))
    
    if self.options.coin == "true":
        if logic == "normal":
            connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AELocation.Coin64.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
        else:
            connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AELocation.Coin64.value, 
                            lambda state: True)
        connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AELocation.Coin66.value, 
                        lambda state: True)

    # Monkey Madness
    # Coaster (multiple rooms)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AELocation.W9L1Goopo.value, 
                        lambda state: HasNet(state, self))
    # Haunted House
    if logic == "normal":
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AELocation.W9L1Porto.value, 
                        lambda state: (CanHitMultiple(state, self) or HasHoop(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AELocation.W9L1Porto.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    # Coffin Room
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AELocation.W9L1Slam.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AELocation.W9L1Junk.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AELocation.W9L1Crib.value, 
                        lambda state: HasNet(state, self))
    # Circus
    if logic == "normal":
        connect_regions(self, AEDoor.MM_CIRCUS_SL_HUB.value, AELocation.W9L1Professor.value, 
                        lambda state: HasFlyer(state, self) and (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)))
    elif logic == "hard":
        connect_regions(self, AEDoor.MM_CIRCUS_SL_HUB.value, AELocation.W9L1Professor.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)))
    else:
        connect_regions(self, AEDoor.MM_CIRCUS_SL_HUB.value, AELocation.W9L1Professor.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and (CanHitMultiple(state, self) or HasRC(state, self)))
    # Go Karz
    if logic == "normal":
        connect_regions(self, AEDoor.MM_GO_KARZ_SL_HUB.value, AELocation.W9L1Jake.value, 
                        lambda state: HasClub(state, self) or HasPunch(state, self))
    else:
        connect_regions(self, AEDoor.MM_GO_KARZ_SL_HUB.value, AELocation.W9L1Jake.value, 
                        lambda state: CanHitMultiple(state, self))
    # Western Land
    if logic == "normal":
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Nak.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Nak.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Nak.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Cloy.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Shaw.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Shaw.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Shaw.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Flea.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Flea.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.W9L1Flea.value, 
                        lambda state: (HasSling(state, self) or HasHoop(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    # Crater
    if logic == "normal":
        connect_regions(self, AEDoor.MM_CRATER_SL_HUB.value, AELocation.W9L1Schafette.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_CRATER_SL_HUB.value, AELocation.W9L1Schafette.value, 
                        lambda state: HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AELocation.W9L1Schafette.value, 
                        lambda state: HasFlyer(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AELocation.W9L1Schafette.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AELocation.W9L1Schafette.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self) or HasHoop(state, self)) and HasNet(state, self))
    # Castle Outside
    if logic == "normal":
        connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AELocation.W9L1Donovan.value, 
                        lambda state: state.has("MM-UFOs", self.player, 1) and HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AELocation.W9L1Donovan.value, 
                        lambda state: state.has("MM-UFOs", self.player, 1) and (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AELocation.W9L1Laura.value, 
                        lambda state: state.has("MM-UFOs", self.player, 1) and HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AELocation.W9L1Laura.value, 
                        lambda state: state.has("MM-UFOs", self.player, 1) and (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and HasNet(state, self))
    # Castle Foyer
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.W9L1Uribe.value, 
                        lambda state: HasPunch(state, self) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.W9L1Gordo.value, 
                        lambda state: HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.W9L1Gordo.value, 
                        lambda state: (HasRC(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.W9L1Raeski.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.W9L1Poopie.value, 
                        lambda state: CanHitOnce(state, self) and HasNet(state, self))
    # Inside Climb
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, AELocation.W9L1Teacup.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, AELocation.W9L1Shine.value, 
                        lambda state: HasNet(state, self))
    # Space Climb
    connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AELocation.W9L1Wrench.value, 
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AELocation.W9L1Bronson.value, 
                        lambda state: HasFlyer(state, self) and HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AELocation.W9L1Bronson.value, 
                        lambda state: ((HasFlyer(state, self) and HasRC(state, self)) or IJ(state, self)) and HasNet(state, self))
    # Monkey Head Room
    connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.W9L1Bungee.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.W9L1Carro.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and HasRC(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.W9L1Carro.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and (HasRC(state, self) or HasSling(state, self)) and HasNet(state, self))
    if logic == "normal":
        connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.W9L1Carlito.value, 
                        lambda state: HasSling(state, self) and HasFlyer(state, self) and HasNet(state, self))
    elif logic == "hard":
        connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.W9L1Carlito.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.W9L1Carlito.value, 
                        lambda state: (CanHitWheel(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    # "Warning" Side Room
    if logic == "normal":
        connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AELocation.W9L1BG.value, 
                        lambda state: HasSling(state, self) and HasNet(state, self))
    else:
        connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AELocation.W9L1BG.value, 
                        lambda state: (HasSling(state, self) or HasFlyer(state, self)) and HasNet(state, self))
    # Specter 1
    if logic == "normal" or logic == "hard":
        connect_regions(self, AEDoor.MM_SPECTER1_ROOM.value, AELocation.Specter.value, 
                        lambda state: (HasClub(state, self) or HasPunch(state, self)) and ((self.options.goal != "mmtoken") or Tokens(state, self, min(self.options.requiredtokens, self.options.totaltokens))))
    else:
        connect_regions(self, AEDoor.MM_SPECTER1_ROOM.value, AELocation.Specter.value, 
                        lambda state: (HasClub(state, self) or HasSling(state, self) or HasPunch(state, self)) and ((self.options.goal != "mmtoken") or Tokens(state, self, min(self.options.requiredtokens, self.options.totaltokens))))

    if self.options.coin == "true":
        connect_regions(self, AEDoor.MM_COASTER1_ENTRY.value, AELocation.Coin73.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.MM_COASTER2_ENTRY.value, AELocation.Coin74.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AELocation.Coin75.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.Coin77.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AELocation.Coin78.value, 
                        lambda state: HasFlyer(state, self) or IJ(state, self))
        connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AELocation.Coin79.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.Coin80.value, 
                        lambda state: CanHitOnce(state, self))
        if logic == "normal" or logic == "hard":
            connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AELocation.Coin82.value, 
                            lambda state: HasFlyer(state, self) and HasRC(state, self))
        else:
            connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AELocation.Coin82.value, 
                            lambda state: (HasFlyer(state, self) and HasRC(state, self)) or IJ(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.Coin84.value, 
                            lambda state: HasSling(state, self) and HasFlyer(state, self))
        elif logic == "hard":
            connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.Coin84.value, 
                            lambda state: HasClub(state, self) or HasSling(state, self) or HasPunch(state, self) or HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.Coin84.value, 
                            lambda state: CanHitWheel(state, self) or HasFlyer(state, self))
        if logic == "normal":
            connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AELocation.Coin85.value, 
                            lambda state: HasFlyer(state, self))
        else:
            connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AELocation.Coin85.value, 
                            lambda state: HasFlyer(state, self) or IJ(state, self))
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AELocation.Mailbox59.value, 
                        lambda state: True)

    # Peak Point Matrix
    if self.options.goal != "mm":
        connect_regions(self, AEDoor.PPM_ENTRY.value, AELocation.Specter2.value, 
                        lambda state: HasSling(state, self) and (HasClub(state, self) or HasHoop(state, self) or HasPunch(state, self)) and HasNet(state, self))
    if self.options.fasttokengoal == self.options.fasttokengoal.option_on:
        if self.options.goal == "mmtoken":
            connect_regions(self, AEDoor.TIME_TRAINING_WATERNET.value, AEDoor.MM_SPECTER1_ROOM.value,
                            lambda state: Tokens(state, self,min(self.options.requiredtokens, self.options.totaltokens)))
        if self.options.goal == "ppmtoken":
            connect_regions(self, AEDoor.TIME_TRAINING_WATERNET.value, AEDoor.PPM_ENTRY.value,
                            lambda state: Tokens(state, self, min(self.options.requiredtokens, self.options.totaltokens)))
# Item Checking Helper Functions
def Keys(state, world, count):
    return state.has(AEItem.Key.value, world.player, count)


def Tokens(state, world, count):
    # Check to see if the settings would create tokens at all.
    if world.options.goal == "mm" or world.options.goal == "ppm":
        return True

    return state.has(AEItem.Token.value, world.player, count)


def HasClub(state, world):
    return state.has(AEItem.Club.value, world.player, 1)


def HasNet(state, world):
    return state.has(AEItem.Net.value, world.player, 1)


def HasRadar(state, world):
    return state.has(AEItem.Radar.value, world.player, 1)


def HasSling(state, world):
    return state.has(AEItem.Sling.value, world.player, 1)


def HasHoop(state, world):
    return state.has(AEItem.Hoop.value, world.player, 1)


def HasFlyer(state, world):
    return state.has(AEItem.Flyer.value, world.player, 1)


def HasRC(state, world):
    return state.has(AEItem.Car.value, world.player, 1)


def HasPunch(state, world):
    return state.has(AEItem.Punch.value, world.player, 1)


def CanSwim(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 1))


def CanDive(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 2))


# Logic Helper Functions
def HasWaterNet(state, world): # CanSwim + CanWaterCatch together
    return (state.has(AEItem.WaterNet.value, world.player, 1) or (state.has(AEItem.WaterCatch.value, world.player, 1) and state.has(AEItem.ProgWaterNet.value, world.player, 1)))


def CanHitOnce(state, world):
    return HasClub(state, world) or HasRadar(state, world) or HasSling(state, world) or HasHoop(state, world) or HasFlyer(state, world) or HasRC(state, world) or HasPunch(state, world)


def CanHitMultiple(state, world):
    if world.options.logic == "normal":
        return HasClub(state, world) or HasSling(state, world) or HasPunch(state, world)
    else:
        return HasClub(state, world) or HasSling(state, world) or HasHoop(state, world) or HasPunch(state, world)


def CanHitWheel(state, world):
    if world.options.logic == "normal" or world.options.logic == "hard":
        return CanHitMultiple(state, world)
    else:
        return CanHitMultiple(state, world) or HasFlyer(state, world) or HasRC(state, world)


def SuperFlyer(state, world, region) -> bool:
    # If the option is off, Super Flyer is not in logic.
    if world.options.superflyer == "false":
        return False

    # If the difficulty is normal, Super Flyer is never in logic.
    if world.options.logic == "normal":
        return False

    # If the player does not have the required gadgets, Super Flyer is unavailable.
    if (HasFlyer(state, world) and (HasNet(state, world) or HasClub(state, world) or HasSling(state, world) or HasPunch(state, world))) == False:
        return False

    # If the player can reach this location without activating the Flyer, Super Flyer is available. To check for this, we check for the ability to access this region on a modified CollectionState. The Radar conveniently has the same ground pound properties as the Flyer while introducing no new access, and so replacing the Flyer with the Radar in this state serves as a valid check.
    teststate = state.copy()
    teststate.remove(world.create_item(AEItem.Flyer.value))
    teststate.collect(world.create_item(AEItem.Radar.value), prevent_sweep = True)
    return world.get_region(region).can_reach(teststate)


def IJ(state, world):
    return HasSling(state, world) and world.options.infinitejump == "true"


# Lamp and Door Functions
def MM_DoubleDoor(state, world):
    return state.has(AEItem.MM_DoubleDoorKey.value, world.player, 1)


def CB_Lamp(state, world):
    if state.has(AEItem.CB_Lamp.value, world.player, 1):
        return True

    return state.has("CB Monkey", world.player, 3) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W4L1CoolBlue.value, AELocation.W4L1Sandy.value, AELocation.W4L1ShellE.value, AELocation.W4L1Gidget.value, AELocation.W4L1Shaka.value, AELocation.W4L1MaxMahalo.value, AELocation.W4L1Moko.value, AELocation.W4L1Puka.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 3


def DI_Lamp(state, world):
    if state.has(AEItem.DI_Lamp.value, world.player, 1):
        return True

    return state.has("DI Monkey", world.player, 5) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W4L3Stuw.value, AELocation.W4L3TonTon.value, AELocation.W4L3Murky.value, AELocation.W4L3Howeerd.value, AELocation.W4L3Robbin.value, AELocation.W4L3Jakkee.value, AELocation.W4L3Frederic.value, AELocation.W4L3Baba.value, AELocation.W4L3Mars.value, AELocation.W4L3Horke.value, AELocation.W4L3Quirck.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 5


def CRC_Lamp(state, world):
    if state.has(AEItem.CrC_Lamp.value, world.player, 1):
        return True

    return state.has("CrC Monkey", world.player, 5) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W7L3Naners.value, AELocation.W7L3Robart.value, AELocation.W7L3Neeners.value, AELocation.W7L3Gustav.value, AELocation.W7L3Wilhelm.value, AELocation.W7L3Emmanuel.value, AELocation.W7L3SirCutty.value, AELocation.W7L3Calligan.value, AELocation.W7L3Castalist.value, AELocation.W7L3Deveneom.value, AELocation.W7L3Igor.value, AELocation.W7L3Charles.value, AELocation.W7L3Astur.value, AELocation.W7L3Kilserack.value, AELocation.W7L3Ringo.value, AELocation.W7L3Densil.value, AELocation.W7L3Figero.value, AELocation.W7L3Fej.value, AELocation.W7L3Joey.value, AELocation.W7L3Donqui.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 5


def CP_Lamp(state, world):
    if state.has(AEItem.CP_Lamp.value, world.player, 1):
        return True

    return state.has("CP Monkey", world.player, 3) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W8L1Kaine.value, AELocation.W8L1Jaxx.value, AELocation.W8L1Gehry.value, AELocation.W8L1Alcatraz.value, AELocation.W8L1Tino.value, AELocation.W8L1QBee.value, AELocation.W8L1McManic.value, AELocation.W8L1Dywan.value, AELocation.W8L1CKHutch.value, AELocation.W8L1Winky.value, AELocation.W8L1BLuv.value, AELocation.W8L1Camper.value, AELocation.W8L1Huener.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 3


def SF_Lamp(state, world):
    if state.has(AEItem.SF_Lamp.value, world.player, 1):
        return True

    return state.has("SF Monkey", world.player, 3) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W8L2BigShow.value, AELocation.W8L2Dreos.value, AELocation.W8L2Reznor.value, AELocation.W8L2Urkel.value, AELocation.W8L2VanillaS.value, AELocation.W8L2Radd.value, AELocation.W8L2Shimbo.value, AELocation.W8L2Hurt.value, AELocation.W8L2String.value, AELocation.W8L2Khamo.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 3


def TVT_Lobby_Lamp(state, world):
    if state.has(AEItem.TVT_Lobby_Lamp.value, world.player, 1):
        return True

    return state.has("TVT Monkey", world.player, 3) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W8L3Fredo.value, AELocation.W8L3Charlee.value, AELocation.W8L3Mach3.value, AELocation.W8L3Tortuss.value, AELocation.W8L3Manic.value, AELocation.W8L3Ruptdis.value, AELocation.W8L3Eighty7.value, AELocation.W8L3Danio.value, AELocation.W8L3Roosta.value, AELocation.W8L3Tellis.value, AELocation.W8L3Whack.value, AELocation.W8L3Frostee.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 3


def TVT_Tank_Lamp(state, world):
    if state.has(AEItem.TVT_Tank_Lamp.value, world.player, 1):
        return True

    return state.has("TVT Monkey", world.player, 6) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W8L3Fredo.value, AELocation.W8L3Charlee.value, AELocation.W8L3Mach3.value, AELocation.W8L3Tortuss.value, AELocation.W8L3Manic.value, AELocation.W8L3Ruptdis.value, AELocation.W8L3Eighty7.value, AELocation.W8L3Danio.value, AELocation.W8L3Roosta.value, AELocation.W8L3Tellis.value, AELocation.W8L3Whack.value, AELocation.W8L3Frostee.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 6


def MM_Lamp(state, world):
    if state.has(AEItem.MM_Lamp.value, world.player, 1):
        return True

    # TODO: check exactly which monkeys apply to this lamp.
    return state.has("MM UFO Monkey", world.player, 2) and world.options.lamp == "false"

#    locs_to_check = [AELocation.W9L1Donovan.value, AELocation.W9L1Laura.value]
#    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)
#    return locs_accessible >= 2


def HasAllMonkeys(state, world):
# ''' Event item checking - floods spoiler logs. NOTE: Add "# " to the beginning to uncomment.
    return (state.has("FF Monkey", world.player, 4) and state.has("PO Monkey", world.player, 4)
        and state.has("ML Monkey", world.player, 7) and state.has("TJ Monkey", world.player, 14)
        and state.has("DR Monkey", world.player, 13) and state.has("CR Monkey", world.player, 8)
        and state.has("CB Monkey", world.player, 8) and state.has("CoC Monkey", world.player, 8)
        and state.has("DI Monkey", world.player, 11) and state.has("SM Monkey", world.player, 6)
        and state.has("FR Monkey", world.player, 9) and state.has("HS Monkey", world.player, 9)
        and state.has("ST Monkey", world.player, 12) and state.has("WSW Monkey", world.player, 10)
        and state.has("CrC Monkey", world.player, 20) and state.has("CP Monkey", world.player, 13)
        and state.has("SF Monkey", world.player, 10) and state.has("TVT Monkey", world.player, 12)
        and state.has("MM Monkey", world.player, 24))
'''
# '''

''' can_reach checking - seems to error out sometimes. NOTE: Add "# " to the beginning to uncomment.
    locs_to_check = [
    AELocation.W1L1Noonan.value, AELocation.W1L1Jorjy.value, AELocation.W1L1Nati.value,
    AELocation.W1L1TrayC.value, AELocation.W1L2Shay.value, AELocation.W1L2DrMonk.value,
    AELocation.W1L2Grunt.value, AELocation.W1L2Ahchoo.value, AELocation.W1L2Gornif.value,
    AELocation.W1L2Tyrone.value, AELocation.W1L3Scotty.value, AELocation.W1L3Coco.value,
    AELocation.W1L3JThomas.value, AELocation.W1L3Mattie.value, AELocation.W1L3Barney.value,
    AELocation.W1L3Rocky.value, AELocation.W1L3Moggan.value, AELocation.W2L1Marquez.value,
    AELocation.W2L1Livinston.value, AELocation.W2L1George.value, AELocation.W2L1Maki.value,
    AELocation.W2L1Herb.value, AELocation.W2L1Dilweed.value, AELocation.W2L1Mitong.value,
    AELocation.W2L1Stoddy.value, AELocation.W2L1Nasus.value, AELocation.W2L1Selur.value,
    AELocation.W2L1Elehcim.value, AELocation.W2L1Gonzo.value, AELocation.W2L1Alphonse.value,
    AELocation.W2L1Zanzibar.value, AELocation.W2L2Mooshy.value, AELocation.W2L2Kyle.value,
    AELocation.W2L2Cratman.value, AELocation.W2L2Nuzzy.value, AELocation.W2L2Mav.value,
    AELocation.W2L2Stan.value, AELocation.W2L2Bernt.value, AELocation.W2L2Runt.value,
    AELocation.W2L2Hoolah.value, AELocation.W2L2Papou.value, AELocation.W2L2Kenny.value,
    AELocation.W2L2Trance.value, AELocation.W2L2Chino.value, AELocation.W2L3Troopa.value,
    AELocation.W2L3Spanky.value, AELocation.W2L3Stymie.value, AELocation.W2L3Pally.value,
    AELocation.W2L3Freeto.value, AELocation.W2L3Jesta.value, AELocation.W2L3Bazzle.value,
    AELocation.W2L3Crash.value, AELocation.W4L1CoolBlue.value, AELocation.W4L1Sandy.value,
    AELocation.W4L1ShellE.value, AELocation.W4L1Gidget.value, AELocation.W4L1Shaka.value,
    AELocation.W4L1MaxMahalo.value, AELocation.W4L1Moko.value, AELocation.W4L1Puka.value,
    AELocation.W4L2Chip.value, AELocation.W4L2Oreo.value, AELocation.W4L2Puddles.value,
    AELocation.W4L2Kalama.value, AELocation.W4L2Iz.value, AELocation.W4L2Jux.value,
    AELocation.W4L2BongBong.value, AELocation.W4L2Pickles.value, AELocation.W4L3Stuw.value,
    AELocation.W4L3TonTon.value, AELocation.W4L3Murky.value, AELocation.W4L3Howeerd.value,
    AELocation.W4L3Robbin.value, AELocation.W4L3Jakkee.value, AELocation.W4L3Frederic.value,
    AELocation.W4L3Baba.value, AELocation.W4L3Mars.value, AELocation.W4L3Horke.value,
    AELocation.W4L3Quirck.value, AELocation.W5L1Popcicle.value, AELocation.W5L1Iced.value,
    AELocation.W5L1Denggoy.value, AELocation.W5L1Skeens.value, AELocation.W5L1Rickets.value,
    AELocation.W5L1Chilly.value, AELocation.W5L2Storm.value, AELocation.W5L2Qube.value,
    AELocation.W5L2Gash.value, AELocation.W5L2Kundra.value, AELocation.W5L2Shadow.value,
    AELocation.W5L2Ranix.value, AELocation.W5L2Sticky.value, AELocation.W5L2Sharpe.value,
    AELocation.W5L2Droog.value, AELocation.W5L3Punky.value, AELocation.W5L3Ameego.value,
    AELocation.W5L3Roti.value, AELocation.W5L3Dissa.value, AELocation.W5L3Yoky.value,
    AELocation.W5L3Jory.value, AELocation.W5L3Crank.value, AELocation.W5L3Claxter.value,
    AELocation.W5L3Looza.value, AELocation.W7L1Taku.value, AELocation.W7L1Rocka.value,
    AELocation.W7L1Maralea.value, AELocation.W7L1Wog.value, AELocation.W7L1Long.value,
    AELocation.W7L1Mayi.value, AELocation.W7L1Owyang.value, AELocation.W7L1QuelTin.value,
    AELocation.W7L1Phaldo.value, AELocation.W7L1Voti.value, AELocation.W7L1Elly.value,
    AELocation.W7L1Chunky.value, AELocation.W7L2Minky.value, AELocation.W7L2Zobbro.value,
    AELocation.W7L2Xeeto.value, AELocation.W7L2Moops.value, AELocation.W7L2Zanabi.value,
    AELocation.W7L2Buddha.value, AELocation.W7L2Fooey.value, AELocation.W7L2Doxs.value,
    AELocation.W7L2Kong.value, AELocation.W7L2Phool.value, AELocation.W7L3Naners.value,
    AELocation.W7L3Robart.value, AELocation.W7L3Neeners.value, AELocation.W7L3Gustav.value,
    AELocation.W7L3Wilhelm.value, AELocation.W7L3Emmanuel.value, AELocation.W7L3SirCutty.value,
    AELocation.W7L3Calligan.value, AELocation.W7L3Castalist.value, AELocation.W7L3Deveneom.value,
    AELocation.W7L3Igor.value, AELocation.W7L3Charles.value, AELocation.W7L3Astur.value,
    AELocation.W7L3Kilserack.value, AELocation.W7L3Ringo.value, AELocation.W7L3Densil.value,
    AELocation.W7L3Figero.value, AELocation.W7L3Fej.value, AELocation.W7L3Joey.value,
    AELocation.W7L3Donqui.value, AELocation.W8L1Kaine.value, AELocation.W8L1Jaxx.value,
    AELocation.W8L1Gehry.value, AELocation.W8L1Alcatraz.value, AELocation.W8L1Tino.value,
    AELocation.W8L1QBee.value, AELocation.W8L1McManic.value, AELocation.W8L1Dywan.value,
    AELocation.W8L1CKHutch.value, AELocation.W8L1Winky.value, AELocation.W8L1BLuv.value,
    AELocation.W8L1Camper.value, AELocation.W8L1Huener.value, AELocation.W8L2BigShow.value,
    AELocation.W8L2Dreos.value, AELocation.W8L2Reznor.value, AELocation.W8L2Urkel.value,
    AELocation.W8L2VanillaS.value, AELocation.W8L2Radd.value, AELocation.W8L2Shimbo.value,
    AELocation.W8L2Hurt.value, AELocation.W8L2String.value, AELocation.W8L2Khamo.value, 
    AELocation.W8L3Fredo.value, AELocation.W8L3Charlee.value, AELocation.W8L3Mach3.value,
    AELocation.W8L3Tortuss.value, AELocation.W8L3Manic.value, AELocation.W8L3Ruptdis.value,
    AELocation.W8L3Eighty7.value, AELocation.W8L3Danio.value, AELocation.W8L3Roosta.value,
    AELocation.W8L3Tellis.value, AELocation.W8L3Whack.value, AELocation.W8L3Frostee.value,
    AELocation.W9L1Goopo.value, AELocation.W9L1Porto.value, AELocation.W9L1Slam.value,
    AELocation.W9L1Junk.value, AELocation.W9L1Crib.value, AELocation.W9L1Nak.value,
    AELocation.W9L1Cloy.value, AELocation.W9L1Shaw.value, AELocation.W9L1Flea.value,
    AELocation.W9L1Schafette.value, AELocation.W9L1Donovan.value, AELocation.W9L1Laura.value,
    AELocation.W9L1Uribe.value, AELocation.W9L1Gordo.value, AELocation.W9L1Raeski.value,
    AELocation.W9L1Poopie.value, AELocation.W9L1Teacup.value, AELocation.W9L1Shine.value,
    AELocation.W9L1Wrench.value, AELocation.W9L1Bronson.value, AELocation.W9L1Bungee.value,
    AELocation.W9L1Carro.value, AELocation.W9L1Carlito.value, AELocation.W9L1BG.value
    ]
    locs_accessible = CountAccessibleLocations(state, world, locs_to_check)

    return locs_accessible >= 204
'''
# '''


# Using this method seems to cause race condition errors in playthrough calculation?
def CountAccessibleLocations(state, world, locs_to_check):
    locs_accessible = 0
    for x in range(len(locs_to_check)):
        if state.can_reach(world.get_region(locs_to_check[x]), "Region", world.player):
            locs_accessible = locs_accessible + 1
    return locs_accessible


# Entrance Shuffle Helper Functions
def initialize_level_list(setlevelids = None):

    baselevelnames = ["Fossil Field", "Primordial Ooze", "Molten Lava", "Thick Jungle", "Dark Ruins", "Cryptic Relics", "Stadium Attack", "Crabby Beach", "Coral Cave", "Dexter's Island", "Snowy Mammoth", "Frosty Retreat", "Hot Springs", "Gladiator Attack", "Sushi Temple", "Wabi Sabi Wall", "Crumbling Castle", "City Park", "Specter's Factory", "TV Tower", "Monkey Madness", "Peak Point Matrix"]
    baselevelids = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11,
                0x14, 0x15, 0x16, 0x18, 0x1E]
    # If not using UT, use the vanilla list
    if setlevelids is None:
        levelids = baselevelids
        levelnames = baselevelnames
    # Using UT, will replace the vanilla list with the already shuffled one
    else:
        levelnames = [baselevelnames[baselevelids.index(setlevelids[x])] for x in range(0, 22)]
        levelids = setlevelids

    levellist = []
    for x in range (0, 22):
        # Vanilla position
        if setlevelids is None:
            vanillapos = x
        # Using UT: will get the vanilla level order of the level in the shuffled list
        else:
            vanillapos = baselevelids.index(setlevelids[x])
        levellist.append(ApeEscapeLevel(levelnames[x], levelids[x], vanillapos))
    return levellist


def initialize_room_list(world, roomsperlevel, setlevelids = None, setroomids = None):
    # baselevelnames = ["Fossil Field", "Primordial Ooze", "Molten Lava", "Thick Jungle", "Dark Ruins", "Cryptic Relics", "Stadium Attack", "Crabby Beach", "Coral Cave", "Dexter's Island", "Snowy Mammoth", "Frosty Retreat", "Hot Springs", "Gladiator Attack", "Sushi Temple", "Wabi Sabi Wall", "Crumbling Castle", "City Park", "Specter's Factory", "TV Tower", "Monkey Madness", "Peak Point Matrix"]
    baselevelids = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x14, 0x15, 0x16, 0x18, 0x1E]
    firstroomids = [0x01, 0x02, 0x03, 0x06, 0x0B, 0x0F, 0x13, 0x14, 0x16, 0x18, 0x1D, 0x1E, 0x21, 0x24, 0x25, 0x28, 0x2D, 0x35, 0x38, 0x3F, 0x45, 0x57]
    firstroomlist = []

    # Using UT, will replace the vanilla list with the already shuffled one
    if world.using_ut == True:
        levelids = setlevelids
        orderedfirstroomids = setroomids
    else:
        levelids = [world.levellist[x].entrance for x in range(0, 22)]

        orderedfirstroomids = []
        excludedrooms_LampsOff = [27] # Exclude certain rooms if LampShuffle is off
        excludedrooms = []
        for x in range (0, 22):

            levelrooms = list(roomsperlevel[levelids[x]])
            # Rooms exclusion
            levelrooms = [item for item in levelrooms if item not in excludedrooms]
            # Exclude some rooms if Lamps are not shuffled, to prevent getting stuck
            if world.options.lamp == 0x00:
                levelrooms = [item for item in levelrooms if item not in excludedrooms_LampsOff]
            levelrooms.sort()
            if world.options.randomizestartingroom == 0x00: # Option off
                orderedfirstroomids.append(levelrooms[0])
            else:
                if setroomids:
                    orderedfirstroomids.append(levelids[x])
                else:
                    randomroom = world.random.randint(0, len(levelrooms) - 1)
                    orderedfirstroomids.append(levelrooms[randomroom])

    return orderedfirstroomids


def level_to_bytes(name):
    bytelist = []
    for x in name:
        bytelist.append(character_lookup(x))
    return bytelist


def character_lookup(byte):
    if byte.isspace():  # Space
        return 255
    if byte.isalpha():
        return ord(byte) - 49  # Both uppercase and lowercase letters
    if byte.isdecimal():
        if int(byte) < 6:
            return ord(byte) + 58  # 0-5
        else:
            return ord(byte) + 68  # 6-9
    if ord(byte) == 39:  # Single apostrophe
        return 187
    if ord(byte) == 46:  # Period
        return 172
    if ord(byte) == 47:  # Slash
        return 141
    if ord(byte) == 58:  # Colon
        return 174


def fixed_levels(levellist, entoption, coinoption, goaloption):
    # Reset position of Peak Point Matrix for mm (postgame), ppm and ppm token (endgame)
    # If MM is locked and mmtoken is the goal, then place PPM at the end anyway
    if goaloption == 0x00 or goaloption == 0x01 or goaloption == 0x04 or (entoption == 0x02 and goaloption == 0x03):
        for x in range (0, 22):
            if levellist[x].entrance == 0x1E:
                levellist[x], levellist[21] = levellist[21], levellist[x]
    # Reset position of Monkey Madness if the option requires it
    if entoption == 0x02:
        for x in range (0, 22):
            if levellist[x].entrance == 0x18:
                levellist[x], levellist[20] = levellist[20], levellist[x]
    # Reset position of races if coin shuffle isn't on
    if coinoption == 0x00:
        for x in range (0, 22):
            if levellist[x].entrance == 0x07: # Stadium Attack
                levellist[x], levellist[6] = levellist[6], levellist[x]
        for x in range (0, 22):
            if levellist[x].entrance == 0x0E: # Gladiator Attack
                levellist[x], levellist[13] = levellist[13], levellist[x]
    return levellist


def set_calculated_level_data(levellist, keyoption, goaloption, coinoption):
    reqkeys = get_required_keys(keyoption, goaloption, coinoption)
    for x in range (0, 22):
        levellist[x].bytes = level_to_bytes(levellist[x].name)
        levellist[x].keys = reqkeys[x]
        levellist[x].newpos = x
    return levellist


def get_required_keys(key, goal, coin):
    reqkeys = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if key == 0x03:  # none
        return reqkeys

    if key == 0x00:  # world
        reqkeys = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6]
    if key == 0x01:  # level
        reqkeys = [0, 0, 0, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15, 16, 16]
    if key == 0x02:  # two
        reqkeys = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 8]

    if goal == 0x02 or goal == 0x03 or goal == 0x04: # If PPM unlocks only by keys, make it unlock later than MM.
        reqkeys[21] = reqkeys[21] + 1

    if coin == 0x01: # If the races have locations, make everything after them require an extra key for each.
        for x in range (7, 22):
            reqkeys[x] = reqkeys[x] + 1
        for x in range (14, 22):
            reqkeys[x] = reqkeys[x] + 1

    return reqkeys
