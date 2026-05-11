from worlds.apeescape.Strings import AEDoor

DOUBLE_EXIT = AEDoor.SF_CONVEYOR1_EXIT.value
CONDITIONAL_ROOMS = {28}
DELAYED_BUTTON_ROOMS = {28}
BUTTON_ACCESS_DOORS = {AEDoor.DI_SLIDE_ROOM_GALLERY.value}
LOGIC_RESTRICTED_DOORS = {AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value}
LAMP_DEPTH_REQUIREMENTS = {
    AEDoor.SF_FACTORY_WHEEL_BOTTOM.value: 3,  # Wait until 3 monkeys are found to map this
}
HEAVY_GATES = {
        #AEDoor.SF_FACTORY_WHEEL_TOP.value,
        # Add any other doors here that require X monkeys or hard-to-get gadgets
    }
ZONE_LOCKS = {
    AEDoor.DI_SLIDE_ROOM_GALLERY.value,
    AEDoor.MM_CASTLE_MAIN_SPECTER1.value,
    AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value,
    AEDoor.CC_ENTRY_BOSS.value,
    AEDoor.TVT_LOBBY_WATER.value
}

# --- BUTTON & ZONE RELATIONSHIPS ---
BUTTON_MAPPINGS = {
    AEDoor.DI_SLIDE_ROOM_GALLERY.value: [
        AEDoor.DI_SLIDE_ROOM_GALLERY.value
    ],
    AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value: [
        AEDoor.MM_CASTLE_MAIN_SPECTER1.value
    ],
    AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value: [
        AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value
    ],
    AEDoor.CC_BUTTON_BASEMENT_WATER.value: [
        AEDoor.CC_ENTRY_BOSS.value
    ],
    AEDoor.CC_BUTTON_BASEMENT_LEDGE.value: [
        AEDoor.CC_ENTRY_BOSS.value
    ],
    AEDoor.TVT_LOBBY_OUTSIDE.value: [
        AEDoor.TVT_LOBBY_WATER.value
    ],
    AEDoor.TVT_LOBBY_TANK.value: [
        AEDoor.TVT_LOBBY_WATER.value
    ],
}

ALL_BUTTONS = set(BUTTON_MAPPINGS.keys())

# --- CONDITIONAL LOCKS ---
LAMP_ZONE_LOCKS = {
    AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value
}

LAMP_BUTTON_MAPPINGS = {
    AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value: [
        AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value
    ]
}

LAMP_RESTRICTIVE_ROOMS = frozenset([AEDoor.DI_TENTACLE.value,
                               AEDoor.DI_GALLERY_TENTACLE.value])

SAME_ROOM_EXCEPTION = frozenset([AEDoor.SF_CONVEYOR1_EXIT.value,
                                 AEDoor.SF_CONVEYOR2_EXIT.value,
                                 AEDoor.SF_CONVEYOR3_EXIT.value,
                                 AEDoor.SF_CONVEYOR4_EXIT.value,
                                 AEDoor.SF_CONVEYOR5_EXIT.value,
                                 AEDoor.SF_CONVEYOR6_EXIT.value])

EXITS_ONLY_DOOR = frozenset([AEDoor.SF_CONVEYOR1_EXIT.value,
                                 AEDoor.SF_CONVEYOR2_EXIT.value,
                                 AEDoor.SF_CONVEYOR3_EXIT.value,
                                 AEDoor.SF_CONVEYOR4_EXIT.value,
                                 AEDoor.SF_CONVEYOR5_EXIT.value,
                                 AEDoor.SF_CONVEYOR6_EXIT.value,
                                 AEDoor.MM_COASTER1_ENTRY.value,
                                 AEDoor.MM_COASTER2_ENTRY.value,
                                 AEDoor.MM_COASTER_ENTRY_DISEMBARK.value,
                                 AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value,
                                 AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value])

ONEWAY_SHUFFLE_DOOR = frozenset([AEDoor.SF_CONVEYOR1_ENTRY.value,
                                 AEDoor.SF_CONVEYOR2_ENTRY.value,
                                 AEDoor.SF_CONVEYOR3_ENTRY.value,
                                 AEDoor.SF_CONVEYOR4_ENTRY.value,
                                 AEDoor.SF_CONVEYOR5_ENTRY.value,
                                 AEDoor.SF_CONVEYOR6_ENTRY.value,
                                 AEDoor.SF_CONVEYOR7_ENTRY.value,
                                #AEDoor.MM_SL_HUB_WESTERN.value,
                                #AEDoor.MM_SL_HUB_COASTER.value,
                                #AEDoor.MM_SL_HUB_CIRCUS.value,
                                #AEDoor.MM_SL_HUB_GO_KARZ.value,
                                #AEDoor.MM_WESTERN_SL_HUB.value,
                                #AEDoor.MM_COASTER_ENTRY_SL_HUB.value,
                                #AEDoor.MM_CIRCUS_SL_HUB.value,
                                #AEDoor.MM_GO_KARZ_SL_HUB.value,
                                 AEDoor.MM_COASTER_ENTRY_COASTER1.value,
                                 AEDoor.MM_COASTER1_COASTER2.value,
                                 AEDoor.MM_COASTER2_HAUNTED_HOUSE.value,
                                 AEDoor.MM_COFFIN_COASTER_ENTRY.value,
                                 AEDoor.MM_CASTLE_MAIN_SPECTER1.value,
                                 AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value])

BOSSES_SHUFFLE_DOOR = frozenset([AEDoor.CC_ENTRY_BOSS.value,
                                 AEDoor.CC_BOSS_ROOM.value,
                                 AEDoor.MM_CASTLE_MAIN_SPECTER1.value,
                                 AEDoor.MM_SPECTER1_ROOM.value,
                                 AEDoor.TVT_TANK_BOSS.value,
                                 AEDoor.TVT_BOSS_TANK.value
                                 ])

APEESCAPE_MAX_ATTEMPTS: int = 100
APEESCAPE_DEBUG: bool = True