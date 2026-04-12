from typing import Dict, NamedTuple, Optional, Tuple, Union

from rule_builder.rules import Rule, And, Has, Or

from ..enums import (
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorTags,
)


class ZorkGrandInquisitorLocationData(NamedTuple):
    game_state_trigger: Optional[
        Tuple[
            Union[
                Tuple[str, str],
                Tuple[int, int],
                Tuple[int, Tuple[int, ...]],
                Tuple[Tuple[int, ...], int],
                Tuple[str, Tuple[str, ...]],
            ],
            ...,
        ]
    ]
    archipelago_id: Optional[int]
    region: ZorkGrandInquisitorRegions
    description: Optional[str]
    tags: Optional[Tuple[ZorkGrandInquisitorTags, ...]] = None
    requirements: Rule = None
    event_item_name: Optional[str] = None


LOCATION_OFFSET = 9758067000

location_data: Dict[
    Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents], ZorkGrandInquisitorLocationData
] = {
    ZorkGrandInquisitorLocations.ALARM_SYSTEM_IS_DOWN: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tr2m"),),
        archipelago_id=LOCATION_OFFSET + 0,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Read the flyer on the bulletin board inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.AN_EXCELLENT_POPPING_UTENSIL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2196, 84),),
        archipelago_id=LOCATION_OFFSET + 1,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
        description="Inspect the dragon tooth as Griff",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.ARREST_THE_VANDAL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10789, 1),),
        archipelago_id=LOCATION_OFFSET + 2,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Hide in the barrel after setting the grand inquisitor doll on fire in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                ),
                Has(ZorkGrandInquisitorItems.CIGAR.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.ARTIFACTS_EXPLAINED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11787, 1), (11788, 1), (11789, 1)),
        archipelago_id=LOCATION_OFFSET + 3,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Activate the 3 artifact paintings in the GUE Tech hallways",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((8929, 1),),
        archipelago_id=LOCATION_OFFSET + 4,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Cast OBIDIL on the two-headed monster in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_OBIDIL.value)
        )
    ),
    ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9124, 1),),
        archipelago_id=LOCATION_OFFSET + 5,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Collect the letter you mailed from the White House at the 666 mailbox in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.A_SMALLWAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11777, 1),),
        archipelago_id=LOCATION_OFFSET + 6,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Cast IGRAM on the INFINITE purple word before the infinite hallway inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13278, 1),),
        archipelago_id=LOCATION_OFFSET + 7,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description="Cast THROCK on the mossy grate at the Flood Control Dam #3 station",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM.value),
                ),
                Has(ZorkGrandInquisitorItems.SPELL_THROCK.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.BEBURTT_DEMYSTIFIED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16315, 1),),
        archipelago_id=LOCATION_OFFSET + 8,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Cast KENDALL while reading the Better Spell Manufacturing in Under 10 Minutes book inside locker #11 in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value),
                Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.BETTER_SPELL_MANUFACTURING_IN_UNDER_10_MINUTES: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "th3x"),),
        archipelago_id=LOCATION_OFFSET + 9,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Read the book inside locker #11 in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value)
        ),
    ),
    ZorkGrandInquisitorLocations.BOING_BOING_BOING: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4220, 1),),
        archipelago_id=LOCATION_OFFSET + 10,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Place the snapdragon on the spring mushroom and hit it with the hammer behind the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HAMMER.value),
                Has(ZorkGrandInquisitorItems.SNAPDRAGON.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.BONK: ZorkGrandInquisitorLocationData(
        game_state_trigger=((19491, 1),),
        archipelago_id=LOCATION_OFFSET + 11,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Hit the snapdragon with the hammer in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HAMMER.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.BRAVE_SOULS_WANTED: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "us2g"),),
        archipelago_id=LOCATION_OFFSET + 12,
        region=ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        description="Look at the advertisement for old scratch in the Crossroads station",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.BROG_DO_GOOD: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2644, 1),),
        archipelago_id=LOCATION_OFFSET + 13,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Throw a boiled grue egg at the stalactites in the White House basement",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.BROG_EAT_ROCKS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2629, 1),),
        archipelago_id=LOCATION_OFFSET + 14,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Eat a rock in the White House basement",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2650, 1),),
        archipelago_id=LOCATION_OFFSET + 15,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Throw a grue egg at the stalactites in the White House basement",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value)
        )
    ),
    ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME: ZorkGrandInquisitorLocationData(
        game_state_trigger=((15715, 1),),
        archipelago_id=LOCATION_OFFSET + 16,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Smash the skull cage with the plank in the White House basement",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                ),
                Has(ZorkGrandInquisitorItems.BROGS_PLANK.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.CASTLE_WATCHING_A_FIELD_GUIDE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dv1t"),),
        archipelago_id=LOCATION_OFFSET + 17,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Read the book inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.CAVES_NOTES: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "th3y"),),
        archipelago_id=LOCATION_OFFSET + 18,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Read the book inside locker #11 in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value)
        )
    ),
    ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9543, 1),),
        archipelago_id=LOCATION_OFFSET + 19,
        region=ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        description="Activate the display at the Monastery Exhibit",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "cd6k"), (1673, 1), (1660, 1), (1312, 1)),
        archipelago_id=LOCATION_OFFSET + 20,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
        description="Escape with the Coconut of Quendor in Dragon Archipelago",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO.value),
                ),
                Has(ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.CRISIS_AVERTED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11769, 1),),
        archipelago_id=LOCATION_OFFSET + 21,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Stash the activated zork rocks in the dented locker in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value),
                Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.CUT_THAT_OUT_YOU_LITTLE_CREEP: ZorkGrandInquisitorLocationData(
        game_state_trigger=((19350, 1),),
        archipelago_id=LOCATION_OFFSET + 22,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on the door in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((17632, 1),),
        archipelago_id=LOCATION_OFFSET + 23,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Cast GOLGATEM on the lake when looking at the walking castle inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_BLINDS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                ),
                Has(ZorkGrandInquisitorItems.SPELL_GOLGATEM.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.DINGWHACKER_DELUXE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2417, 1),),
        archipelago_id=LOCATION_OFFSET + 24,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Activate the pachinko machine in the Past Port Foozle tavern",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "hp5e"), (8919, 2), (9, 100)),
        archipelago_id=LOCATION_OFFSET + 25,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Attack the two-headed monster with the sword in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SWORD.value)
        ),
    ),
    ZorkGrandInquisitorLocations.DONT_GO_SPENDING_IT_ALL_IN_ONE_PLACE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4512, 87),),
        archipelago_id=LOCATION_OFFSET + 26,
        region=ZorkGrandInquisitorRegions.ANYWHERE,
        description="Inspect a Zorkmid coin",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value)
        ),
    ),
    ZorkGrandInquisitorLocations.DOOOOOOWN: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3619, 3600),),
        archipelago_id=LOCATION_OFFSET + 27,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Lower the mailbox flag as Griff outside the White House",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DOWN: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3619, 5300),),
        archipelago_id=LOCATION_OFFSET + 28,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Lower the mailbox flag as Lucy outside the White House",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9216, 1),),
        archipelago_id=LOCATION_OFFSET + 29,
        region=ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
        description="Cast NARWILE on the time tunnel beyond the gates in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_NARWILE.value)
        )
    ),
    ZorkGrandInquisitorLocations.DUNCE_LOCKER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11851, 1),),
        archipelago_id=LOCATION_OFFSET + 30,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Open the locker by purchasing item #11 from the vending machine inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
            )
        )
    ),
    ZorkGrandInquisitorLocations.EGGPLANTS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3816, 11000),),
        archipelago_id=LOCATION_OFFSET + 31,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Activate the eggplants in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.ELSEWHERE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pc1e"),),
        archipelago_id=LOCATION_OFFSET + 32,
        region=ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL,
        description="Reach the well outside Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.EMERGENCY_MAGICATRONIC_MESSAGE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(((11784, 11786), 1),),
        archipelago_id=LOCATION_OFFSET + 33,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Activate the Belboz painting in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
    ),
    ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13743, 1),),
        archipelago_id=LOCATION_OFFSET + 34,
        region=ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        description="Cast KENDALL on the subway map in the Crossroads station",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value)
        ),
    ),
    ZorkGrandInquisitorLocations.FAT_LOT_OF_GOOD_THATLL_DO_YA: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16368, 1),),
        archipelago_id=LOCATION_OFFSET + 35,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Cast IGRAM on the invisible bridge guard at the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value)
        ),
    ),
    ZorkGrandInquisitorLocations.FIRE_FIRE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10277, (1, 2)),),
        archipelago_id=LOCATION_OFFSET + 36,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Set the grand inquisitor doll on fire in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                ),
                Has(ZorkGrandInquisitorItems.CIGAR.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.FLOOD_CONTROL_DAM_3_THE_NOT_REMOTELY_BORING_TALE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13259, 1),),
        archipelago_id=LOCATION_OFFSET + 37,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description="Look inside the book at the Flood Control Dam #3 station",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4222, 1),),
        archipelago_id=LOCATION_OFFSET + 38,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Cast THROCK on the spring mushroom, place the snapdragon and hit the mushroom with the hammer in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_THROCK.value),
                Has(ZorkGrandInquisitorItems.SNAPDRAGON.value),
                Has(ZorkGrandInquisitorItems.HAMMER.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.FROBUARY_3_UNDERGROUNDHOG_DAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dw2g"),),
        archipelago_id=LOCATION_OFFSET + 39,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Read the diary on the bed inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12892, 1),),
        archipelago_id=LOCATION_OFFSET + 40,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Use the 500 zorkmid bill on the change machine inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.ZORKMID_BILL_ACCESSIBLE.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.GO_AWAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10654, 1),),
        archipelago_id=LOCATION_OFFSET + 41,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on the window in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "sg6e"), (17103, 1), (15715, 1), (15707, 1)),
        archipelago_id=LOCATION_OFFSET + 42,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Collect the Skull of Yoruk in the White House basement",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                ),
                Has(ZorkGrandInquisitorItems.BROGS_PLANK.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.GUE_TECH_ENTRANCE_EXAM: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11082, 1), (11307, 1), (11536, 1)),
        archipelago_id=LOCATION_OFFSET + 43,
        region=ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
        description="Solve the entrance exam outside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((8443, 1),),
        archipelago_id=LOCATION_OFFSET + 44,
        region=ZorkGrandInquisitorRegions.HADES_SHORE,
        description="Answer all the questions correctly on the phone in Hades. Solution: 82895 or KENDALL + *",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.HELLO_THIS_IS_SHONA_FROM_GURTH_PUBLISHING: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4698, 1),),
        archipelago_id=LOCATION_OFFSET + 45,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Listen to the message on the answering machine inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10421, 1),),
        archipelago_id=LOCATION_OFFSET + 46,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Activate the dock winch with the plastic six-pack holder on the hook in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                ),
                Has(ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.HEY_FREE_DIRT: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11747, 1),),
        archipelago_id=LOCATION_OFFSET + 47,
        region=ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
        description="Dig in the dirt pile with the shovel outside of GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Has(ZorkGrandInquisitorItems.SHOVEL.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.HMMM_BIG_TOOTHPICK: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2194, 69),),
        archipelago_id=LOCATION_OFFSET + 48,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Inspect the plank as Brog",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.BROGS_PLANK.value)
        ),
    ),
    ZorkGrandInquisitorLocations.HMMM_INFORMATIVE_YET_DEEPLY_DISTURBING: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "mt2h"),),
        archipelago_id=LOCATION_OFFSET + 49,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Look at the infographic on the wall at the Monastery",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.HOW_TO_HYPNOTIZE_YOURSELF: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "uh1e"),),
        archipelago_id=LOCATION_OFFSET + 50,
        region=ZorkGrandInquisitorRegions.SUBWAY_HADES,
        description="Read the book in the Hades station",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.HOW_TO_WIN_AT_DOUBLE_FANUCCI: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "th3s"),),
        archipelago_id=LOCATION_OFFSET + 51,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Read the book inside locker #8 in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value)
        )
    ),
    ZorkGrandInquisitorLocations.IMBUE_BEBURTT: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12166, 1),),
        archipelago_id=LOCATION_OFFSET + 52,
        region=ZorkGrandInquisitorRegions.SPELL_LAB,
        description="Create a BEBURTT scroll by using the machines in the Spell Lab and running it through the spell checker. Solution: O M R I T",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.IM_COMPLETELY_NUDE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((19344, 1),),
        archipelago_id=LOCATION_OFFSET + 53,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on the door in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.INFLATUS_THE_ETERNAL: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "cd4h"),),
        archipelago_id=LOCATION_OFFSET + 54,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
        description="Visit the skeleton in Dragon Archipelago",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13060, 1),),
        archipelago_id=LOCATION_OFFSET + 55,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Use the sword on the foliage blocking the door at the Crossroads",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SWORD.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
                ),
            )
        )
    ),
    ZorkGrandInquisitorLocations.INVISIBLE_FLOWERS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12967, 1),),
        archipelago_id=LOCATION_OFFSET + 56,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Cast IGRAM on the umbrella flowers at the Crossroads",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value)
        ),
    ),
    ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12931, 1),),
        archipelago_id=LOCATION_OFFSET + 57,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Break the glass case with the hammer at the Crossroads",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HAMMER.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13062, 1),),
        archipelago_id=LOCATION_OFFSET + 58,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Cast REZROV on the door at the Crossroads",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_REZROV.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.ITS_ALMOST_AS_IF_IT_WERE_INFINITE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((11005, 15),),
        archipelago_id=LOCATION_OFFSET + 59,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Go DEEP in the infinite corridor inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
    ),
    ZorkGrandInquisitorLocations.ITS_ONE_OF_THOSE_ADVENTURERS_AGAIN: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pe3j"),),
        archipelago_id=LOCATION_OFFSET + 60,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Look at the door in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.ITS_PLAYING_A_LITTLE_HARD_TO_GET: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3816, 1006),),
        archipelago_id=LOCATION_OFFSET + 61,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Cast OBIDIL on the snapdragon in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_OBIDIL.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.IT_DOESNT_APPEAR_TO_BE_FOOLED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3816, 1009),),
        archipelago_id=LOCATION_OFFSET + 62,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Cast BEBURTT on the snapdragon in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_BEBURTT.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.I_AM_NOT_IMPRESSED: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", ("hp4f", "hp1g")), (8419, 1)),
        archipelago_id=LOCATION_OFFSET + 63,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Cast SNAVIG on Charon in Hades and interact with him",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value)
        ),
    ),
    ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3816, 1008),),
        archipelago_id=LOCATION_OFFSET + 64,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Cast THROCK on the snapdragon in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_THROCK.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value)
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.I_DONT_WANT_NO_TROUBLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10694, 1),),
        archipelago_id=LOCATION_OFFSET + 65,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on the door in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16374, 1),),
        archipelago_id=LOCATION_OFFSET + 66,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Cast GOLGATEM over the Spell Lab chasm",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
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
        )
    ),
    ZorkGrandInquisitorLocations.I_SPIT_ON_YOUR_FILTHY_COINAGE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tp1e"), (9, 87), (1011, 1)),
        archipelago_id=LOCATION_OFFSET + 67,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Try to bribe the invisible bridge guard at the Spell Lab with a zorkmid",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value)
        )
    ),
    ZorkGrandInquisitorLocations.LIT_SUNFLOWERS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4129, 1),),
        archipelago_id=LOCATION_OFFSET + 68,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Cast THROCK on the sunflowers in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_THROCK.value)
        ),
    ),
    ZorkGrandInquisitorLocations.LOOK_AN_ICE_CREAM_BAR: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12517, 1),),
        archipelago_id=LOCATION_OFFSET + 69,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Open the rightmost door of the frozen treat machine inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2498, (1, 2)),),
        archipelago_id=LOCATION_OFFSET + 70,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Mail the GLORF scroll with either Griff or Lucy outside the White House",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                    Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                ),
            )
        )
    ),
    ZorkGrandInquisitorLocations.MAKE_LOVE_NOT_WAR: ZorkGrandInquisitorLocationData(
        game_state_trigger=(((8623, 8734), 21),),
        archipelago_id=LOCATION_OFFSET + 71,
        region=ZorkGrandInquisitorRegions.HADES_SHORE,
        description="Attack Charon with the sword in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.CHARON_CALLED.value),
                Has(ZorkGrandInquisitorItems.SWORD.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.MEAD_LIGHT: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10485, 1),),
        archipelago_id=LOCATION_OFFSET + 72,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on Jack's door with the mead light in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.MEAD_LIGHT.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.ME_I_AM_THE_BOSS_OF_YOU: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "px1k"),),
        archipelago_id=LOCATION_OFFSET + 73,
        region=ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ,
        description="Look at the sign at the inquisition headquarters outside Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.MIKES_PANTS: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tr2p"),),
        archipelago_id=LOCATION_OFFSET + 74,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Read the flyer on the bulletin board inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4217, 1),),
        archipelago_id=LOCATION_OFFSET + 75,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Hit the spring mushroom with the hammer behind the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HAMMER.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.NATIONAL_TREASURE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((14318, 1),),
        archipelago_id=LOCATION_OFFSET + 76,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description="Destroy Flood Control Dam #3 by casting REZROV on the closed floodgate and then closing all floodgates",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_REZROV.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.NATURAL_AND_SUPERNATURAL_CREATURES_OF_QUENDOR: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dv1p"),),
        archipelago_id=LOCATION_OFFSET + 77,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Read the book inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12706, 1),),
        archipelago_id=LOCATION_OFFSET + 78,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Open the locker by purchasing item #8 from the vending machine inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.NOTHIN_LIKE_A_GOOD_STOGIE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4237, 1),),
        archipelago_id=LOCATION_OFFSET + 79,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Place the cigar in Harry's ashtray in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                ),
                Has(ZorkGrandInquisitorItems.CIGAR.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT: ZorkGrandInquisitorLocationData(
        game_state_trigger=((8935, 1),),
        archipelago_id=LOCATION_OFFSET + 80,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Cast SNAVIG on the two-headed monster in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value)
        ),
    ),
    ZorkGrandInquisitorLocations.NO_AUTOGRAPHS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10476, 1),),
        archipelago_id=LOCATION_OFFSET + 81,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on Jack's door in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.NO_BONDAGE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pe2e"), (10262, 2), (15150, 83)),
        archipelago_id=LOCATION_OFFSET + 82,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Activate the dock winch with the rope on the hook in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.NO_ONE_RETURNS_FROM_HADES: ZorkGrandInquisitorLocationData(
        game_state_trigger=((15204, 1),),
        archipelago_id=LOCATION_OFFSET + 83,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Try to pay the toll to Charon after going beyond the gates in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorEvents.BEYOND_GATES_OF_HELL_ACCESSED.value)
        )
    ),
    ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12164, 1),),
        archipelago_id=LOCATION_OFFSET + 84,
        region=ZorkGrandInquisitorRegions.SPELL_LAB,
        description="Run the soggy OBIDIL scroll through the spell checker in the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                ),
                Has(ZorkGrandInquisitorItems.SANDWITCH_WRAPPER.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON: ZorkGrandInquisitorLocationData(
        game_state_trigger=((1300, 1),),
        archipelago_id=LOCATION_OFFSET + 85,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
        description="Plug the dragon's nostrils with the inflatables and use the air pump on them in Dragon Archipelago",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2448, 1),),
        archipelago_id=LOCATION_OFFSET + 86,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        description="Knock on the door as Brog in Past Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4869, 1),),
        archipelago_id=LOCATION_OFFSET + 87,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Make a cup of cocoa inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.COCOA_INGREDIENTS.value),
                Has(ZorkGrandInquisitorItems.HUNGUS_LARD.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.OLD_SCRATCH_WINNER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4512, 32),),
        archipelago_id=LOCATION_OFFSET + 88,
        region=ZorkGrandInquisitorRegions.ANYWHERE,
        description="Solve the maze on the old scratch ticket",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.OLD_SCRATCH_CARD.value)
        ),
    ),
    ZorkGrandInquisitorLocations.ONLY_YOU_CAN_PREVENT_FOOZLE_FIRES: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pe5n"),),
        archipelago_id=LOCATION_OFFSET + 89,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Look at the poster in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((8651, 1),),
        archipelago_id=LOCATION_OFFSET + 90,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Cast SNAVIG on Charon and punch out in Hades",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value),
                Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4241, 1),),
        archipelago_id=LOCATION_OFFSET + 91,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Plug the hive with the hungus lard, remove it and slice the hive with the sword in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HUNGUS_LARD.value),
                Has(ZorkGrandInquisitorItems.SWORD.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.PERMASEAL: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "mt1g"),),
        archipelago_id=LOCATION_OFFSET + 92,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Look at the PermaSeal container in the Monastery",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.PLANETFALL: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pp1j"),),
        archipelago_id=LOCATION_OFFSET + 93,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP,
        description="Look at the computer inside Jack's shop in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.PLEASE_DONT_THROCK_THE_GRASS: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "te1g"),),
        archipelago_id=LOCATION_OFFSET + 94,
        region=ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
        description="Look at the sign outside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9404, 1),),
        archipelago_id=LOCATION_OFFSET + 95,
        region=ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        description="Cast NARWILE on the time tunnel in the Monastery Exhibit",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
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
            )
        )
    ),
    ZorkGrandInquisitorLocations.PROZORKED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4115, 1),),
        archipelago_id=LOCATION_OFFSET + 96,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Give the snapdragon the prozork tablet in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.PROZORK_TABLET.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.PURPLE_BEAST_ALARM_SYSTEM: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tp1f"),),
        archipelago_id=LOCATION_OFFSET + 97,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Look at the sign next to the guard at the Spell Lab Bridge",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4512, 98),),
        archipelago_id=LOCATION_OFFSET + 98,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Combine the mirrored scroll fragments in the mirror room inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS.value),
                Has(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MIRROR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.RESTOCKED_ON_GRUESDAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tr2h"),),
        archipelago_id=LOCATION_OFFSET + 99,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Read the flyer on the bulletin board inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.RIGHT_HELLO_YES_UH_THIS_IS_SNEFFLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4698, 3),),
        archipelago_id=LOCATION_OFFSET + 100,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Listen to the message on the answering machine inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.RIGHT_UH_SORRY_ITS_ME_AGAIN_SNEFFLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4698, 4),),
        archipelago_id=LOCATION_OFFSET + 101,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Listen to the message on the answering machine inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.SNAVIG_REPAIRED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12161, 1),),
        archipelago_id=LOCATION_OFFSET + 102,
        region=ZorkGrandInquisitorRegions.SPELL_LAB,
        description="Run the torn SNAVIG scroll through the spell checker in the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.SOUVENIR: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13408, 1),),
        archipelago_id=LOCATION_OFFSET + 103,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description="Press a zorkmid at the Flood Control Dam #3 station",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.SPELL_CHECK_COMPLETE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12168, 1),),
        archipelago_id=LOCATION_OFFSET + 104,
        region=ZorkGrandInquisitorRegions.SPELL_LAB,
        description="Insert a blank scroll sheet into the spell checker in the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9719, 1),),
        archipelago_id=LOCATION_OFFSET + 105,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Set the totemizer destination to Straight to Hell, turn off PermaSeal and totemize yourself in the Monastery",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                ),
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                ),
            )
        )
    ),
    ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((14511, 1), (14524, 5)),
        archipelago_id=LOCATION_OFFSET + 106,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Win the game of strip grue, fire, water against Jack inside the tavern in Past Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.SUCKING_ROCKS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12859, 1),),
        archipelago_id=LOCATION_OFFSET + 107,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Place and activate the perma-suck machine while the zork rocks are loose in the vending machine inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Has(ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.TALK_TO_ME_GRAND_INQUISITOR: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10299, 1),),
        archipelago_id=LOCATION_OFFSET + 108,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Activate the grand inquisitor doll in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.TAMING_YOUR_SNAPDRAGON: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dv1h"),),
        archipelago_id=LOCATION_OFFSET + 109,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Read the book inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.THAR_SHE_BLOWS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((1311, 1), (1312, 1)),
        archipelago_id=LOCATION_OFFSET + 110,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
        description="Pop the sea captain with the dragon tooth while the inflatables are tied with the rope and the coconut is in the raft inside the dragon's mouth in the Dragon Archipelago",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO.value),
                ),
                Has(ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.THATS_A_ROPE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10486, 1),),
        archipelago_id=LOCATION_OFFSET + 111,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on Jack's door with the rope in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.THATS_IT_JUST_KEEP_HITTING_THOSE_BUTTONS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13805, 1),),
        archipelago_id=LOCATION_OFFSET + 112,
        region=ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        description="Randomly press buttons on the complex subway map in the Crossroads station",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
    ),
    ZorkGrandInquisitorLocations.THATS_STILL_A_ROPE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tp1e"), (9, 83), (1011, 1)),
        archipelago_id=LOCATION_OFFSET + 113,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Use the rope on the invisible bridge guard at the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value)
        ),
    ),
    ZorkGrandInquisitorLocations.THATS_THE_SPIRIT: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10341, 95),),
        archipelago_id=LOCATION_OFFSET + 114,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Turn up the volume of the loudspeaker in Port Foozle to the maximum level",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9459, 1),),
        archipelago_id=LOCATION_OFFSET + 115,
        region=ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        description="Activate the display at the Monastery Exhibit",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9473, 1),),
        archipelago_id=LOCATION_OFFSET + 116,
        region=ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        description="Activate the display at the Monastery Exhibit",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO: ZorkGrandInquisitorLocationData(
        game_state_trigger=((9520, 1),),
        archipelago_id=LOCATION_OFFSET + 117,
        region=ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        description="Activate the display at the Monastery Exhibit",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.THE_ONLY_WAY_TO_WIN_IS_NOT_TO_PLAY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16286, 1),),
        archipelago_id=LOCATION_OFFSET + 118,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Cast KENDALL while reading How to Win at Double Fanucci inside locker #8 in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value),
                Has(ZorkGrandInquisitorItems.SPELL_KENDALL.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "me1j"),),
        archipelago_id=LOCATION_OFFSET + 119,
        region=ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        description="Look at the sign at the Monastery Exhibit",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND: ZorkGrandInquisitorLocationData(
        game_state_trigger=((13167, 1),),
        archipelago_id=LOCATION_OFFSET + 120,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Go through the turnstile after inserting a subway token at the Crossroads station",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SUBWAY_TOKEN.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "cd60"), (1524, 1)),
        archipelago_id=LOCATION_OFFSET + 121,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
        description="Visit the Dragon Archipelago as Lucy",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value)
        ),
    ),
    ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4219, 1),),
        archipelago_id=LOCATION_OFFSET + 122,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Cast THROCK on the spring mushroom and hit it with the hammer behind the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HAMMER.value),
                Has(ZorkGrandInquisitorItems.SPELL_THROCK.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.TIME_TRAVEL_FOR_DUMMIES: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "th3z"),),
        archipelago_id=LOCATION_OFFSET + 123,
        region=ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        description="Read the book inside locker #11 in the GUE Tech hallway",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value)
        ),
    ),
    ZorkGrandInquisitorLocations.TOTEMIZED_DAILY_BILLBOARD: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "px1h"),),
        archipelago_id=LOCATION_OFFSET + 124,
        region=ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ,
        description="Look at the billboard at the inquisition headquarters outside Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "cd60"), (1520, 1)),
        archipelago_id=LOCATION_OFFSET + 125,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
        description="Visit the Dragon Archipelago as Brog",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.TOTEM_BROG.value)
        ),
    ),
    ZorkGrandInquisitorLocations.UM_AH_UM_AH_UM_AH: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16997, 4),),
        archipelago_id=LOCATION_OFFSET + 126,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Read the mind of the bouncer 4 times inside the Past Port Foozle tavern",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.UMBRELLA_FLOWERS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12926, 1),),
        archipelago_id=LOCATION_OFFSET + 127,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Cast BEBURTT on the umbrella flowers at the Crossroads",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_BEBURTT.value)
        ),
    ),
    ZorkGrandInquisitorLocations.UP: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3619, 5200),),
        archipelago_id=LOCATION_OFFSET + 128,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Raise the mailbox flag as Lucy outside the White House",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.USELESS_BUT_FUN: ZorkGrandInquisitorLocationData(
        game_state_trigger=((14321, 1),),
        archipelago_id=LOCATION_OFFSET + 129,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description="Cast GOLGATEM above Flood Control Dam #3",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_GOLGATEM.value)
        ),
    ),
    ZorkGrandInquisitorLocations.UUUUUP: ZorkGrandInquisitorLocationData(
        game_state_trigger=((3619, 3500),),
        archipelago_id=LOCATION_OFFSET + 130,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Raise the mailbox flag as Griff outside the White House",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.VOYAGE_OF_CAPTAIN_ZAHAB: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "uh1h"),),
        archipelago_id=LOCATION_OFFSET + 131,
        region=ZorkGrandInquisitorRegions.SUBWAY_HADES,
        description="Read the book at the Hades station",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4034, 1),),
        archipelago_id=LOCATION_OFFSET + 132,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Add the mead light to Harry's bird bath and cast ZIMDOR on it in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value),
                Has(ZorkGrandInquisitorItems.MEAD_LIGHT.value),
                Has(ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO_PAST: ZorkGrandInquisitorLocationData(
        game_state_trigger=((17006, 5001),),
        archipelago_id=LOCATION_OFFSET + 133,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Read the mind of the bartender 2 times inside the Past Port Foozle tavern",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE: ZorkGrandInquisitorLocationData(
        game_state_trigger=((2461, 1),),
        archipelago_id=LOCATION_OFFSET + 134,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        description="Knock on the door as Griff in Past Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((15472, 1),),
        archipelago_id=LOCATION_OFFSET + 135,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Win the game of Alpine's Quandry inside the tavern in Past Port Foozle. Solution: 4+1 (Fly), 1, 2, 3 (or 3, 2)",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.WHAT_ARE_YOU_STUPID: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10484, 1),),
        archipelago_id=LOCATION_OFFSET + 136,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on Jack's door with the plastic six-pack holder in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL: ZorkGrandInquisitorLocationData(
        game_state_trigger=((4983, 1),),
        archipelago_id=LOCATION_OFFSET + 137,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Cast NARWILE on the time tunnel inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                ),
                Has(ZorkGrandInquisitorItems.SPELL_NARWILE.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.WHOOPS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((15959, (1, 2)),),
        archipelago_id=LOCATION_OFFSET + 138,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        description="Throw a grue egg at the stalactites off to the side in the White House basement",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            Has(ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value)
        )
    ),
    ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dc10"), (1596, 1)),
        archipelago_id=LOCATION_OFFSET + 139,
        region=ZorkGrandInquisitorRegions.WALKING_CASTLE,
        description="Cast OBIDIL on the walking castle inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.YAD_GOHDNUORGREDNU_3_YRAUBORF: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dm2g"),),
        archipelago_id=LOCATION_OFFSET + 140,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Read the diary on the bed in the mirror room inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_MIRROR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dg4e"), (4266, 1), (9, 21), (4035, 1)),
        archipelago_id=LOCATION_OFFSET + 141,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Attack Harry with the sword in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SWORD.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HARRY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.YOU_DONT_GO_MESSING_WITH_A_MANS_ZIPPER: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16405, 1),),
        archipelago_id=LOCATION_OFFSET + 142,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Cast REZROV on the invisible bridge guard at the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_REZROV.value)
        ),
    ),
    ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS: ZorkGrandInquisitorLocationData(
        game_state_trigger=((16342, 1),),
        archipelago_id=LOCATION_OFFSET + 143,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Cut the rope bridge with the sword at the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SWORD.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "qs1e"), (14511, 1), (14524, 5)),
        archipelago_id=LOCATION_OFFSET + 144,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Win the Cube of Foundation against Jack inside the tavern in Past Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.YOU_ONE_OF_THEM_AGITATORS_AINT_YA: ZorkGrandInquisitorLocationData(
        game_state_trigger=((10586, 1),),
        archipelago_id=LOCATION_OFFSET + 145,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Knock on the window in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE,),
    ),
    ZorkGrandInquisitorLocations.YOU_WANT_A_PIECE_OF_ME_DOCK_BOY: ZorkGrandInquisitorLocationData(
        game_state_trigger=((15151, 1),),
        archipelago_id=LOCATION_OFFSET + 146,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Activate the dock winch in Port Foozle",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.ZIMDOR_IS_UNDAMAGED: ZorkGrandInquisitorLocationData(
        game_state_trigger=((12167, 1),),
        archipelago_id=LOCATION_OFFSET + 147,
        region=ZorkGrandInquisitorRegions.SPELL_LAB,
        description="Insert the ZIMDOR scroll into the spell checker in the Spell Lab",
        tags=(ZorkGrandInquisitorTags.CORE, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB.value),
                )
            )
        )
    ),
    # Deathsanity
    ZorkGrandInquisitorLocations.DEATH_ARRESTED_WITH_JACK: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 1)),
        archipelago_id=LOCATION_OFFSET + 200 + 0,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Don't hide in the barrel after setting the grand inquisitor doll on fire in Port Foozle",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE.value),
                ),
                Has(ZorkGrandInquisitorItems.CIGAR.value)
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 20)),
        archipelago_id=LOCATION_OFFSET + 200 + 1,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Attack the quelbee hive with the sword in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SWORD.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_CLIMBED_OUT_OF_THE_WELL: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 21)),
        archipelago_id=LOCATION_OFFSET + 200 + 2,
        region=ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL,
        description="Climb out of the well after entering the Underground",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            Has(ZorkGrandInquisitorItems.WELL_ROPE.value)
        ),
    ),
    ZorkGrandInquisitorLocations.DEATH_EATEN_BY_A_GRUE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 18)),
        archipelago_id=LOCATION_OFFSET + 200 + 3,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Go down the stairs inside the White House as Griff or Lucy",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_JUMPED_IN_BOTTOMLESS_PIT: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 3)),
        archipelago_id=LOCATION_OFFSET + 200 + 4,
        region=ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
        description="Jump in one of the bottomless pits outside GUE Tech",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
    ),
    ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 37)),
        archipelago_id=LOCATION_OFFSET + 200 + 5,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        description="Lose the game of strip grue, fire, water against Jack inside the tavern in Past Port Foozle",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value),
                Has(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_LOST_SOUL_TO_OLD_SCRATCH: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 23)),
        archipelago_id=LOCATION_OFFSET + 200 + 6,
        region=ZorkGrandInquisitorRegions.ANYWHERE,
        description="Make 3 mistakes while solving the maze on the old scratch ticket",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorItems.OLD_SCRATCH_CARD.value)
        ),
    ),
    ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 29)),
        archipelago_id=LOCATION_OFFSET + 200 + 7,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Plug the hive with the hungus lard, remove it and wait in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.HUNGUS_LARD.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_SLICED_UP_BY_THE_INVISIBLE_GUARD: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 30)),
        archipelago_id=LOCATION_OFFSET + 200 + 8,
        region=ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        description="Annoy the invisible bridge guard at the Spell Lab until he kills you",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
    ),
    ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 4)),
        archipelago_id=LOCATION_OFFSET + 200 + 9,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Cast IGRAM on the CORRIDOR purple word before the infinite hallway inside GUE Tech and move forward",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_IGRAM.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 11)),
        archipelago_id=LOCATION_OFFSET + 200 + 10,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
        description="Don't move out of the dragon's mouth after popping an inflatable at the Dragon Archipelago",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value),
                Has(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO.value),
                ),
                Has(ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 34)),
        archipelago_id=LOCATION_OFFSET + 200 + 11,
        region=ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
        description="Cast THROCK on the grass outside GUE Tech",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_THROCK.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_INFINITY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 9)),
        archipelago_id=LOCATION_OFFSET + 200 + 12,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Infinity and with PermalSeal turned off at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_NEWARK_NEW_JERSEY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 33)),
        archipelago_id=LOCATION_OFFSET + 200 + 13,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Newark, New Jersey and with PermalSeal turned off at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_HALLS_OF_INQUISITION: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 8)),
        archipelago_id=LOCATION_OFFSET + 200 + 14,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Halls of Inquisition and with PermalSeal turned on at the Monastery.and with PermalSeal turned on at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_INFINITY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 7)),
        archipelago_id=LOCATION_OFFSET + 200 + 15,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Infinity and with PermalSeal turned on at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_NEWARK_NEW_JERSEY: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 6)),
        archipelago_id=LOCATION_OFFSET + 200 + 16,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Newark, New Jersey and with PermalSeal turned on at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_STRAIGHT_TO_HELL: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 5)),
        archipelago_id=LOCATION_OFFSET + 200 + 17,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Straight to Hell and with PermalSeal turned on at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_SURFACE_OF_MERZ: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 13)),
        archipelago_id=LOCATION_OFFSET + 200 + 18,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Surface of Merz and with PermalSeal turned on at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_SURFACE_OF_MERZ: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 32)),
        archipelago_id=LOCATION_OFFSET + 200 + 19,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Totemize yourself with the destination set to Surface of Merz and with PermalSeal turned off at the Monastery",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY,),
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY.value),
                )
            )
        )
    ),
    ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 10)),
        archipelago_id=LOCATION_OFFSET + 200 + 20,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Punch out with the wrong card after casting SNAVIG on Charon in Hades",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorItems.SPELL_SNAVIG.value)
        ),
    ),
    ZorkGrandInquisitorLocations.DEATH_ZORK_ROCKS_EXPLODED: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "gjde"), (2201, 19)),
        archipelago_id=LOCATION_OFFSET + 200 + 21,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Hold on to the activated zork rocks until they explode inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.DEATHSANITY, ZorkGrandInquisitorTags.MISSABLE),
        requirements=(
            Has(ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value)
        ),
    ),
    # Landmarksanity
    ZorkGrandInquisitorLocations.LANDMARK_DRAGON_ARCHIPELAGO: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "cd60"),),
        archipelago_id=LOCATION_OFFSET + 300 + 0,
        region=ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
        description="Arrive in Dragon Archipelago",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.LANDMARK_DUNGEON_MASTERS_HOUSE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dg40"),),
        archipelago_id=LOCATION_OFFSET + 300 + 1,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description="Stand in front of the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_FLOOD_CONTROL_DAM_3: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "ue1e"),),
        archipelago_id=LOCATION_OFFSET + 300 + 2,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description="Look at the dam at the Flood Control Dam #3 station",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_GATES_OF_HELL: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "hp50"),),
        archipelago_id=LOCATION_OFFSET + 300 + 3,
        region=ZorkGrandInquisitorRegions.HADES,
        description="Stand in front of the gates in Hades",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_GREAT_UNDERGROUND_EMPIRE_ENTRANCE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "uw10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 4,
        region=ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL,
        description="Stand in front of the entrance to the Great Underground at the bottom of the well",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_GUE_TECH_FOUNTAIN_INSIDE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tr10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 5,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Stand in front of the fountain inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_GUE_TECH_FOUNTAIN_OUTSIDE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "te50"),),
        archipelago_id=LOCATION_OFFSET + 300 + 6,
        region=ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
        description="Stand in front of the fountain outside GUE Tech",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_HADES_SHORE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "hp10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 7,
        region=ZorkGrandInquisitorRegions.HADES_SHORE,
        description="Arrive at the shore in Hades",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_INFINITE_CORRIDOR: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "th10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 8,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description="Step in the infinite corridor inside GUE Tech",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_INQUISITION_HEADQUARTERS: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "px10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 9,
        region=ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ,
        description="Stand outside the inquisition headquarters on the outskirts of Port Foozle",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_JACKS_SHOP: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pp10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 10,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP,
        description="Enter Jack's Shop in Port Foozle",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_MIRROR_ROOM: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dm10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 11,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description="Enter the mirror room inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.HOTSPOT_MIRROR.value),
                Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.LANDMARK_PAST_PORT_FOOZLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "qe10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 12,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        description="Arrive in Past Port Foozle",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
            )
        )
    ),
    ZorkGrandInquisitorLocations.LANDMARK_PORT_FOOZLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "pe10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 13,
        region=ZorkGrandInquisitorRegions.PORT_FOOZLE,
        description="Arrive in Port Foozle",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_SPELL_CHECKER: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "tp40"),),
        archipelago_id=LOCATION_OFFSET + 300 + 14,
        region=ZorkGrandInquisitorRegions.SPELL_LAB,
        description="Stand in front of the Spell Checker in the Spell Lab",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_TOTEMIZER: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "mt10"),),
        archipelago_id=LOCATION_OFFSET + 300 + 15,
        region=ZorkGrandInquisitorRegions.MONASTERY,
        description="Stand in front of the Totemizer in the Monastery",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_UMBRELLA_TREE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "uc1e"),),
        archipelago_id=LOCATION_OFFSET + 300 + 16,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Stand in front of the umbrella tree at the Crossroads",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_UNDERGROUND_UNDERGROUND_ENTRANCE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "uc60"),),
        archipelago_id=LOCATION_OFFSET + 300 + 17,
        region=ZorkGrandInquisitorRegions.CROSSROADS,
        description="Stand in front of the subway entrance at the Crossroads",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_WALKING_CASTLES_HEART: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "dc1h"), (1596, 1)),
        archipelago_id=LOCATION_OFFSET + 300 + 18,
        region=ZorkGrandInquisitorRegions.WALKING_CASTLE,
        description="Look at the heart of the walking castle inside the house in the Dungeon Master's Lair",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
    ),
    ZorkGrandInquisitorLocations.LANDMARK_WHITE_HOUSE: ZorkGrandInquisitorLocationData(
        game_state_trigger=(("location", "sw40"),),
        archipelago_id=LOCATION_OFFSET + 300 + 19,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description="Arrive at the White House",
        tags=(ZorkGrandInquisitorTags.LANDMARKSANITY,),
        requirements=(
            Or(
                Has(ZorkGrandInquisitorItems.TOTEM_BROG.value),
                Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
            )
        )
    ),
    # Events
    ZorkGrandInquisitorEvents.BEYOND_GATES_OF_HELL_ACCESSED: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
        description=None,
        event_item_name=ZorkGrandInquisitorEvents.BEYOND_GATES_OF_HELL_ACCESSED.value,
    ),
    ZorkGrandInquisitorEvents.CHARON_CALLED: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.HADES_SHORE,
        description=None,
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.CHARON_CALLED.value,
    ),
    ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value,
    ),
    ZorkGrandInquisitorEvents.DAM_DESTROYED: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SPELL_REZROV.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
    ),
    ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value),
                Has(ZorkGrandInquisitorItems.MEAD_LIGHT.value),
                Has(ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
    ),
    ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.DM_LAIR,
        description=None,
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                ),
                Has(ZorkGrandInquisitorItems.CIGAR.value),
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value,
    ),
    ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
    ),
    ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS.value),
                Has(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MIRROR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
    ),
    ZorkGrandInquisitorEvents.ROPE_GLORFABLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.WELL_ROPE.value),
                Has(ZorkGrandInquisitorItems.SPELL_GLORF.value),
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value,
    ),
    ZorkGrandInquisitorEvents.VICTORY: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.ENDGAME,
        description=None,
        event_item_name=ZorkGrandInquisitorEvents.VICTORY.value,
    ),
    ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.WHITE_HOUSE,
        description=None,
        requirements=(
            And(
                Or(
                    Has(ZorkGrandInquisitorItems.TOTEM_GRIFF.value),
                    Has(ZorkGrandInquisitorItems.TOTEM_LUCY.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
    ),
    ZorkGrandInquisitorEvents.ZORKMID_BILL_ACCESSIBLE: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.ANYWHERE,
        description=None,
        requirements=(
            Has(ZorkGrandInquisitorItems.OLD_SCRATCH_CARD.value)
        ),
        event_item_name=ZorkGrandInquisitorEvents.ZORKMID_BILL_ACCESSIBLE.value,
    ),
    ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED: ZorkGrandInquisitorLocationData(
        game_state_trigger=None,
        archipelago_id=None,
        region=ZorkGrandInquisitorRegions.GUE_TECH,
        description=None,
        requirements=(
            And(
                Has(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                ),
                Or(
                    Has(ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS.value),
                    Has(ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH.value),
                )
            )
        ),
        event_item_name=ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
    ),
}
