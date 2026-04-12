from typing import Dict, Optional, Tuple

from rule_builder.rules import Rule, And, Has, Or

from ..enums import (
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorRegions,
)


Entrance = Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]
EntranceRuleData = Dict[Entrance, Optional[Rule]]


entrance_rule_data: EntranceRuleData = {
    (ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL, ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL): (
        And(
            Has(ZorkGrandInquisitorItems.WELL_ROPE.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_BUCKET.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL): None,
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.DM_LAIR): (
        And(
            Has(ZorkGrandInquisitorItems.SWORD.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_REZROV.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): (
        And(
            Has(ZorkGrandInquisitorItems.SUBWAY_TOKEN.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.TELEPORTER): None,
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR): (
        And(
            Has(ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value),
            Has(ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value),
        )
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.TELEPORTER): None,
    (ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.DM_LAIR): (
        Or(
            Has(ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_HOUSE_EXIT.value),
            Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
        )
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.WALKING_CASTLE): (
        And(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_BLINDS.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
            ),
            Has(ZorkGrandInquisitorItems.SPELL_OBIDIL.value),
        )
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.WHITE_HOUSE): (
        And(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
            ),
            Has(ZorkGrandInquisitorItems.SPELL_NARWILE.value),
            Has(ZorkGrandInquisitorItems.SPELL_YASTARD.value),
        )
    ),
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO, ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON): (
        And(
            Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO, ZorkGrandInquisitorRegions.HADES_BEYOND_GATES): None,
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON, ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO): None,
    (ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE): (
        Or(
            Has(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS.value),
            Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
        )
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        Or(
            Has(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR.value),
            Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
        )
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE, ZorkGrandInquisitorRegions.GUE_TECH): (
        Or(
            Has(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS.value),
            Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
        )
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY, ZorkGrandInquisitorRegions.GUE_TECH): None,
    (ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        And(
            Has(ZorkGrandInquisitorItems.STUDENT_ID.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.GUE_TECH): (
        Or(
            Has(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS.value),
            Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
        )
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.TELEPORTER): None,
    (ZorkGrandInquisitorRegions.HADES, ZorkGrandInquisitorRegions.HADES_BEYOND_GATES): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value),
            Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
        )
    ),
    (ZorkGrandInquisitorRegions.HADES, ZorkGrandInquisitorRegions.HADES_SHORE): (
        And(
            Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
            Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value),
        )
    ),
    (ZorkGrandInquisitorRegions.HADES_BEYOND_GATES, ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_NARWILE.value),
            Has(ZorkGrandInquisitorItems.SPELL_YASTARD.value),
        )
    ),
    (ZorkGrandInquisitorRegions.HADES_BEYOND_GATES, ZorkGrandInquisitorRegions.HADES): None,
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.HADES): (
        And(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
            ),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
            ),
            Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
        )
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.SUBWAY_HADES): None,
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.TELEPORTER): None,
    (ZorkGrandInquisitorRegions.MONASTERY, ZorkGrandInquisitorRegions.HADES_SHORE): (
        And(
            Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
            ),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.MONASTERY, ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT): (
        And(
            Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
            ),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): None,
    (ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT, ZorkGrandInquisitorRegions.MONASTERY): None,
    (ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT, ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST): (
        And(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
            ),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
            ),
            Has(ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value),
            Has(ZorkGrandInquisitorItems.SPELL_NARWILE.value),
            Has(ZorkGrandInquisitorItems.SPELL_YASTARD.value),
        )
    ),
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST
    ): None,
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ
    ): None,
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL
    ): None,
    (ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST, ZorkGrandInquisitorRegions.PORT_FOOZLE): None,
    (ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL, ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL): (
        Has(ZorkGrandInquisitorItems.WELL_ROPE.value)
    ),
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST
    ): None,
    (ZorkGrandInquisitorRegions.PORT_FOOZLE, ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST): None,
    (ZorkGrandInquisitorRegions.PORT_FOOZLE, ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP): (
        And(
            Has(ZorkGrandInquisitorItems.CIGAR.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
            ),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
            ),
        )
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP, ZorkGrandInquisitorRegions.PORT_FOOZLE): None,
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST, ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT): None,
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST, ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN): (
        And(
            Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN, ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST): None,
    (ZorkGrandInquisitorRegions.SPELL_LAB, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): None,
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY): (
        Or(
            Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT.value),
            Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
        )
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.SPELL_LAB): (
        And(
            Has(ZorkGrandInquisitorItems.SWORD.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
            ),
            Has(ZorkGrandInquisitorEvents.DAM_DESTROYED.value),
            Has(ZorkGrandInquisitorItems.SPELL_GOLGATEM.value),
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
            )
        )
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.TELEPORTER): None,
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value),
            Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value),
        )
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_HADES): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value),
            Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value),
        )
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        And(
            Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value),
            Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value),
        )
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM, ZorkGrandInquisitorRegions.SUBWAY_HADES): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_HADES, ZorkGrandInquisitorRegions.HADES_SHORE): None,
    (ZorkGrandInquisitorRegions.SUBWAY_HADES, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_HADES, ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_HADES, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.MONASTERY): (
        Has(ZorkGrandInquisitorItems.MONASTERY_ROPE.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_HADES): (
        Has(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value)
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.TELEPORTER): None,
    (ZorkGrandInquisitorRegions.TELEPORTER, ZorkGrandInquisitorRegions.CROSSROADS): (
        And(
            Has(ZorkGrandInquisitorItems.MAP.value),
            Has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS.value),
        )
    ),
    (ZorkGrandInquisitorRegions.TELEPORTER, ZorkGrandInquisitorRegions.DM_LAIR): (
        And(
            Has(ZorkGrandInquisitorItems.MAP.value),
            Has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value),
        )
    ),
    (ZorkGrandInquisitorRegions.TELEPORTER, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        And(
            Has(ZorkGrandInquisitorItems.MAP.value),
            Has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value),
        )
    ),
    (ZorkGrandInquisitorRegions.TELEPORTER, ZorkGrandInquisitorRegions.HADES_SHORE): (
        And(
            Has(ZorkGrandInquisitorItems.MAP.value),
            Has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value),
        )
    ),
    (ZorkGrandInquisitorRegions.TELEPORTER, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        And(
            Has(ZorkGrandInquisitorItems.MAP.value),
            Has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value),
        )
    ),
    (ZorkGrandInquisitorRegions.TELEPORTER, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        And(
            Has(ZorkGrandInquisitorItems.MAP.value),
            Has(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value),
        )
    ),
    (ZorkGrandInquisitorRegions.WALKING_CASTLE, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR): None,
    (ZorkGrandInquisitorRegions.WHITE_HOUSE, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR): None,
    (ZorkGrandInquisitorRegions.WHITE_HOUSE, ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR): (
        And(
            Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
            Has(ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH.value),
        )
    ),
    (ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR, ZorkGrandInquisitorRegions.WHITE_HOUSE): None,
}

