# This file is generated. Manual changes will be lost
# fmt: off
# ruff: noqa
# mypy: disable-error-code="misc"
from __future__ import annotations

import typing_extensions as typ


# Definitions
Seed: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 2147483647']
TypeU4: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 15']
TypeU5: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 31']
TypeU8: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 255']
TypeU10: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 1023']
AreaId: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 6']
AreaIdKey = typ.Literal[
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6'
]
MinimapIdKey = typ.Literal[
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10'
]
SectorId: typ.TypeAlias = typ.Annotated[int, '1 <= value <= 6']
ShortcutSectorList: typ.TypeAlias = typ.Annotated[list[SectorId], 'len() == 6']
HueRotation: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 360']
ValidSources = typ.Literal[
    'MAIN_DECK_DATA',
    'ARACHNUS',
    'CHARGE_CORE_X',
    'LEVEL_1',
    'TRO_DATA',
    'ZAZABI',
    'SERRIS',
    'LEVEL_2',
    'PYR_DATA',
    'MEGA_X',
    'LEVEL_3',
    'ARC_DATA_1',
    'WIDE_CORE_X',
    'ARC_DATA_2',
    'YAKUZA',
    'NETTORI',
    'NIGHTMARE',
    'LEVEL_4',
    'AQA_DATA',
    'WAVE_CORE_X',
    'RIDLEY',
    'BOILER',
    'ANIMALS',
    'AUXILIARY_POWER'
]
ValidItems = typ.Literal[
    'NONE',
    'LEVEL_0',
    'MISSILES',
    'MORPH_BALL',
    'CHARGE_BEAM',
    'LEVEL_1',
    'BOMBS',
    'HI_JUMP',
    'SPEED_BOOSTER',
    'LEVEL_2',
    'SUPER_MISSILES',
    'VARIA_SUIT',
    'LEVEL_3',
    'ICE_MISSILES',
    'WIDE_BEAM',
    'POWER_BOMBS',
    'SPACE_JUMP',
    'PLASMA_BEAM',
    'GRAVITY_SUIT',
    'LEVEL_4',
    'DIFFUSION_MISSILES',
    'WAVE_BEAM',
    'SCREW_ATTACK',
    'ICE_BEAM',
    'MISSILE_TANK',
    'ENERGY_TANK',
    'POWER_BOMB_TANK',
    'ICE_TRAP',
    'INFANT_METROID'
]
ValidItemSprites = typ.Literal[
    'EMPTY',
    'MISSILES',
    'LEVEL_0',
    'MORPH_BALL',
    'CHARGE_BEAM',
    'LEVEL_1',
    'BOMBS',
    'HI_JUMP',
    'SPEED_BOOSTER',
    'LEVEL_2',
    'SUPER_MISSILES',
    'VARIA_SUIT',
    'LEVEL_3',
    'ICE_MISSILES',
    'WIDE_BEAM',
    'POWER_BOMBS',
    'SPACE_JUMP',
    'PLASMA_BEAM',
    'GRAVITY_SUIT',
    'LEVEL_4',
    'DIFFUSION_MISSILES',
    'WAVE_BEAM',
    'SCREW_ATTACK',
    'ICE_BEAM',
    'MISSILE_TANK',
    'ENERGY_TANK',
    'POWER_BOMB_TANK',
    'ANONYMOUS',
    'SHINY_MISSILE_TANK',
    'SHINY_POWER_BOMB_TANK',
    'INFANT_METROID',
    'SAMUS_HEAD',
    'WALLJUMP_BOOTS',
    'RANDOVANIA',
    'ARCHIPELAGO_COLOR',
    'ARCHIPELAGO_MONOCHROME'
]
ValidAbilities = typ.Literal[
    'MISSILES',
    'MORPH_BALL',
    'CHARGE_BEAM',
    'BOMBS',
    'HI_JUMP',
    'SPEED_BOOSTER',
    'SUPER_MISSILES',
    'VARIA_SUIT',
    'ICE_MISSILES',
    'WIDE_BEAM',
    'POWER_BOMBS',
    'SPACE_JUMP',
    'PLASMA_BEAM',
    'GRAVITY_SUIT',
    'DIFFUSION_MISSILES',
    'WAVE_BEAM',
    'SCREW_ATTACK',
    'ICE_BEAM'
]
ValidElevatorTops = typ.Literal[
    'OPERATIONS_DECK_TOP',
    'MAIN_HUB_TO_SECTOR_1',
    'MAIN_HUB_TO_SECTOR_2',
    'MAIN_HUB_TO_SECTOR_3',
    'MAIN_HUB_TO_SECTOR_4',
    'MAIN_HUB_TO_SECTOR_5',
    'MAIN_HUB_TO_SECTOR_6',
    'MAIN_HUB_TOP',
    'HABITATION_DECK_TOP',
    'SECTOR_1_TO_RESTRICTED_LAB'
]
ValidElevatorBottoms = typ.Literal[
    'OPERATIONS_DECK_BOTTOM',
    'MAIN_HUB_BOTTOM',
    'RESTRICTED_LAB_TO_SECTOR_1',
    'HABITATION_DECK_BOTTOM',
    'SECTOR_1_TO_MAIN_HUB',
    'SECTOR_2_TO_MAIN_HUB',
    'SECTOR_3_TO_MAIN_HUB',
    'SECTOR_4_TO_MAIN_HUB',
    'SECTOR_5_TO_MAIN_HUB',
    'SECTOR_6_TO_MAIN_HUB'
]
ValidLanguages = typ.Literal[
    'JAPANESE_KANJI',
    'JAPANESE_HIRAGANA',
    'ENGLISH',
    'GERMAN',
    'FRENCH',
    'ITALIAN',
    'SPANISH'
]
ValidMusicTracks = typ.Literal[
    'UNUSED_1',
    'AFTER_EVENT',
    'SECTOR_1',
    'SECTOR_2',
    'SECTOR_3',
    'SECTOR_5',
    'SECTOR_4',
    'SECTOR_6',
    'NAVIGATION_ROOM',
    'SECURITY_DATA_ROOM',
    'ITEM_JINGLE',
    'LOADING_SAVE',
    'MESSAGE_POPUP',
    'SA_X_APPEARANCE',
    'SA_X_CHASE',
    'BOSS_TENSION',
    'ARACHNUS_BATTLE',
    'ZAZABI_BATTLE',
    'BOX_BATTLE',
    'MAIN_DECK_AMBIENCE',
    'UNUSED_1F',
    'UNUSED_20',
    'SILENCE_1_SHIP',
    'TENSION',
    'MAIN_DECK_LIVELY',
    'OMEGA_METROID_DEFEATED',
    'OPERATIONS_DECK',
    'OPERATIONS_DECK_ELEVATOR_OFFLINE_SOUND_AND_AMBIENCE',
    'X_INVASION_DETECTION',
    'SA_X_ELEVATOR',
    'HEADING_TO_NIGHTMARE_RIDLEY',
    'OPERATIONS_DECK_ELEVATOR_OFFLINE_SOUND',
    'OPERATIONS_DECK_ELEVATOR_OFFLINE_AMBIENCE',
    'MAIN_BOILER_COOLDOWN_MISSION',
    'STATION_ESCAPE',
    'OBJECTIVE_COMPLETE',
    'SECTOR_4_UNDERWATER',
    'SECTOR_4_UNDERWATER_UNUSED',
    'SERRIS_YAKUZA_BATTLE',
    'VARIA_CORE_X_BATTLE',
    'NIGHTMARE_BATTLE',
    'NEO_RIDLEY_BATTLE',
    'CHOZO_STATUE_CORE_X_BATTLE',
    'NETTORI_BATTLE',
    'PRE_TITLE_END',
    'TITLE',
    'SA_X_BATTLE',
    'EPILOGUE_END',
    'ENDING',
    'EPILOGUE',
    'DISQUIETING',
    'SHOCK',
    'SILENCE_1',
    'MAIN_BOILER_OVERHEATING',
    'FINAL_ORDER',
    'SILENCE_2',
    'INTRIGUE',
    'UNUSED_5E',
    'UNEASE'
]
MusicMapping: typ.TypeAlias = dict[ValidMusicTracks, ValidMusicTracks]
MessageLanguages: typ.TypeAlias = dict[ValidLanguages, str]

class ItemMessages(typ.TypedDict, total=False):
    kind: typ.Required[ItemMessagesKind]
    languages: MessageLanguages
    centered: bool = True
    message_id: typ.Annotated[int, '0 <= value <= 56']
    """The Message ID, will display one of the predefined messages in the ROM"""

ItemMessagesKind = typ.Literal[
    'CUSTOM_MESSAGE',
    'MESSAGE_ID'
]
Jingle = typ.Literal[
    'MINOR',
    'MAJOR'
]

class BlockLayerItem(typ.TypedDict, total=False):
    x: TypeU8
    """The X position in the room that should get edited."""

    y: TypeU8
    """The Y position in the room that should get edited."""

    value: TypeU10
    """The value that should be used to edit the room. For backgrounds, this is calculated via `((Row-1) * ColumnsInTileset) + (Column-1)`."""

BlockLayer: typ.TypeAlias = typ.Annotated[list[BlockLayerItem], 'Unique items']
HintLocks = typ.Literal[
    'OPEN',
    'LOCKED',
    'GREY',
    'BLUE',
    'GREEN',
    'YELLOW',
    'RED'
]

# Schema entries

class MarsschemamfLocationsMajorLocationsItem(typ.TypedDict):
    source: ValidSources
    """Valid major locations."""

    item: ValidItems
    """Valid items for shuffling."""

    item_messages: typ.NotRequired[ItemMessages]
    jingle: Jingle

class MarsschemamfLocationsMinorLocationsItem(typ.TypedDict):
    area: AreaId
    """The area ID where this item is located."""

    room: TypeU8
    """The room ID where this item is located."""

    block_x: TypeU8
    """The X-coordinate in the room where this item is located."""

    block_y: TypeU8
    """The Y-coordinate in the room where this item is located."""

    item: ValidItems
    """Valid items for shuffling."""

    item_sprite: typ.NotRequired[ValidItemSprites]
    """Valid graphics for minor location items."""

    item_messages: typ.NotRequired[ItemMessages]
    jingle: Jingle

class MarsschemamfLocations(typ.TypedDict):
    """Specifies how the item locations in the game should be changed."""

    major_locations: typ.Annotated[list[MarsschemamfLocationsMajorLocationsItem], 'len() == 23', 'Unique items']
    """Specifies how the major item locations should be changed. A major item location is a location where an item is obtained by defeating a boss or interacting with a device."""

    minor_locations: typ.Annotated[list[MarsschemamfLocationsMinorLocationsItem], 'len() == 103', 'Unique items']
    """Specifies how the minor item locations should be changed. A minor item location is a location where an item is obtained by touching a tank block."""


class MarsschemamfStartingLocation(typ.TypedDict):
    """The location the player should spawn at the start of the game."""

    area: AreaId
    """The area ID of the starting location."""

    room: TypeU8
    """The room ID of the starting location."""

    block_x: TypeU8
    """The X-coordinate in the room where the player should spawn. If the room contains a save station, then this value will not be taken into consideration."""

    block_y: TypeU8
    """The Y-coordinate in the room where the player should spawn. If the room contains a save station, then this value will not be taken into consideration."""

MarsschemamfStartingItemsSecurityLevelsItem = typ.Literal[
    0,
    1,
    2,
    3,
    4
]

class MarsschemamfStartingItems(typ.TypedDict, total=False):
    energy: typ.Annotated[int, '1 <= value <= 2099'] = 99
    """How much energy the player should start with on a new save file."""

    missiles: typ.Annotated[int, '0 <= value <= 999'] = 10
    """How many missiles the player should start with on a new save file (the amount unlocked by collecting missile data)."""

    power_bombs: typ.Annotated[int, '0 <= value <= 99'] = 10
    """How many power bombs the player should start with on a new save file (the amount unlocked by collecting power bomb data)."""

    abilities: typ.Annotated[list[ValidAbilities], 'Unique items'] = []
    """Which abilities the player should start with on a new save file."""

    security_levels: typ.Annotated[list[MarsschemamfStartingItemsSecurityLevelsItem], 'Unique items'] = [0]
    """Which security levels will be unlocked from the start."""

    downloaded_maps: typ.Annotated[list[AreaId], 'Unique items'] = []
    """Which area maps will be downloaded from the start."""


class MarsschemamfTankIncrements(typ.TypedDict):
    """How much ammo/health tanks provide when collected."""

    missile_tank: typ.Annotated[int, '-1000 <= value <= 1000'] = 5
    """How much ammo missile tanks provide when collected."""

    energy_tank: typ.Annotated[int, '-2100 <= value <= 2100'] = 100
    """How much health energy tanks provide when collected."""

    power_bomb_tank: typ.Annotated[int, '-100 <= value <= 100'] = 2
    """How much ammo power bomb tanks provide when collected."""

    missile_data: typ.NotRequired[typ.Annotated[int, '0 <= value <= 1000']] = 10
    """How much ammo Missile Launcher Data provides when collected."""

    power_bomb_data: typ.NotRequired[typ.Annotated[int, '0 <= value <= 100']] = 10
    """How much ammo Power Bomb Data provides when collected."""


class MarsschemamfElevatorConnections(typ.TypedDict):
    """Defines the elevator that each elevator connects to."""

    elevator_tops: typ.Annotated[dict[ValidElevatorTops, ValidElevatorBottoms], 'len() >= 10']
    """Defines the bottom elevator that each top elevator connects to."""

    elevator_bottoms: typ.Annotated[dict[ValidElevatorBottoms, ValidElevatorTops], 'len() >= 10']
    """Defines the top elevator that each bottom elevator connects to."""


class MarsschemamfSectorShortcuts(typ.TypedDict):
    """Defines the sector that each sector shortcut connects to."""

    left_areas: ShortcutSectorList
    """Destination areas on the left side of sectors."""

    right_areas: ShortcutSectorList
    """Destination areas on the right side of sectors"""

MarsschemamfDoorLocksItemLockType = typ.Literal[
    'OPEN',
    'LEVEL_0',
    'LEVEL_1',
    'LEVEL_2',
    'LEVEL_3',
    'LEVEL_4',
    'LOCKED'
]

class MarsschemamfDoorLocksItem(typ.TypedDict):
    area: AreaId
    """The area ID where this door is located."""

    door: TypeU8
    """The door ID of this door."""

    lock_type: MarsschemamfDoorLocksItemLockType
    """The type of cover on the hatch."""

MarsschemamfPalettesRandomizeKey = typ.Literal[
    'TILESETS',
    'ENEMIES',
    'SAMUS',
    'BEAMS'
]

@typ.final
class MarsschemamfPalettesRandomize(typ.TypedDict, total=False):
    """The range to use for rotating palette hues."""

    hue_min: HueRotation = None
    """The minimum value to use for rotating palette hues. If not specified, the patcher will randomly generate one."""

    hue_max: HueRotation = None
    """The maximum value to use for rotating palette hues. If not specified, the patcher will randomly generate one."""


MarsschemamfPalettesColorSpace = typ.Literal[
    'HSV',
    'OKLAB'
]

@typ.final
class MarsschemamfPalettes(typ.TypedDict, total=False):
    """Properties for randomized in-game palettes."""

    seed: Seed = None
    """A number used to initialize the random number generator for palettes. If not specified, the patcher will randomly generate one."""

    randomize: typ.Required[dict[MarsschemamfPalettesRandomizeKey, MarsschemamfPalettesRandomize]]
    """What kind of palettes should be randomized."""

    color_space: MarsschemamfPalettesColorSpace = 'OKLAB'
    """The color space to use for rotating palette hues."""

    symmetric: bool = True
    """Randomly rotates hues in the positive or negative direction true."""


@typ.final
class MarsschemamfRng(typ.TypedDict):
    """Properties for manipulating RNG-elements in the game. Specifying any value as 255 will cause that value to fallback to vanilla behaviour."""

    Gadora: typ.Annotated[list[TypeU8], 'len() == 10'] = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
    """Specifies for each Gadora, how many Beams it will shoot before opening its vulnerable eye. The order is by their internal IDs: Arachnus, Charge Core, Zazabi, Serris, Varia Core, Wide Core, Nightmare, Ridley, Nettori, Yakuza."""

    Zazabi: typ.Annotated[list[TypeU8], 'len() == 4'] = [255, 255, 255, 255]
    """Specifies how many additional jumps Zazabi does in rounds 1 to 3, and how long it additionally crawls for in round 4. The final calculation the game uses is (CurrentRound-1)+ProvidedNumber for phase 1-3, and 60+ProvidedNumber for phase 4."""

    Yakuza: TypeU8 = 255
    """Specifies how many additional rounds of sweeping around Yakuza does in Phase 1 of its fight before opening its mouth. The final calculation the game uses is 1+ProvidedNumber."""


class MarsschemamfNavigationTextNavigationTerminals(typ.TypedDict, total=False):
    """Assigns each navigation room a specific text."""

    MAIN_DECK_WEST: str
    """Specifies what text should appear at the west Navigation Terminal in Main Deck."""

    MAIN_DECK_EAST: str
    """Specifies what text should appear at the east Navigation Terminal in Main Deck."""

    OPERATIONS_DECK: str
    """Specifies what text should appear at the Navigation Terminal in Operations Deck."""

    SECTOR_1_ENTRANCE: str
    """Specifies what text should appear at the Navigation Terminal in Sector 1."""

    SECTOR_2_ENTRANCE: str
    """Specifies what text should appear at the Navigation Terminal in Sector 2."""

    SECTOR_3_ENTRANCE: str
    """Specifies what text should appear at the Navigation Terminal in Sector 3."""

    SECTOR_4_ENTRANCE: str
    """Specifies what text should appear at the Navigation Terminal in Sector 4."""

    SECTOR_5_ENTRANCE: str
    """Specifies what text should appear at the Navigation Terminal in Sector 5."""

    SECTOR_6_ENTRANCE: str
    """Specifies what text should appear at the Navigation Terminal in Sector 6."""

    AUXILIARY_POWER: str
    """Specifies what text should appear at the Navigation Terminal near the Auxiliary Power Station."""

    RESTRICTED_LABS: str
    """Specifies what text should appear at the Navigation Terminal in the Restricted Labs."""


class MarsschemamfNavigationTextShipText(typ.TypedDict, total=False):
    """Assigns the ship specific text."""

    INITIAL_TEXT: str
    """Specifies what text should appear at the initial ship communication."""

    CONFIRM_TEXT: str
    """Specifies what text should appear at the ship after confirming 'No' on subsequent ship communications."""


@typ.final
class MarsschemamfNavigationText(typ.TypedDict, total=False):
    """Specifies text for a specific language."""

    navigation_terminals: MarsschemamfNavigationTextNavigationTerminals
    """Assigns each navigation room a specific text."""

    ship_text: MarsschemamfNavigationTextShipText
    """Assigns the ship specific text."""



class MarsschemamfTitleTextItem(typ.TypedDict, total=False):
    text: typ.Annotated[str, '/^[ -~]{0,30}$/']
    """The ASCII text for this line"""

    line_num: typ.Annotated[int, '0 <= value <= 20']
MarsschemamfCreditsTextItemLineType = typ.Literal[
    'BLANK',
    'BLUE',
    'RED',
    'WHITE',
    'WHITE_BIG'
]

class MarsschemamfCreditsTextItem(typ.TypedDict, total=False):
    line_type: typ.Required[MarsschemamfCreditsTextItemLineType]
    """The color and line height of the text (or blank)."""

    text: typ.Annotated[str, '/^[ -~]{0,34}$/']
    """The ASCII text for this line."""

    blank_lines: TypeU8 = 0
    """Inserts the provided number of blank lines after the text line."""

    centered: bool = True
    """Centers the text horizontally when true."""

MarsschemamfNavStationLocksKey = typ.Literal[
    'MAIN_DECK_WEST',
    'MAIN_DECK_EAST',
    'OPERATIONS_DECK',
    'RESTRICTED_LABS',
    'AUXILIARY_POWER',
    'SECTOR_1_ENTRANCE',
    'SECTOR_2_ENTRANCE',
    'SECTOR_3_ENTRANCE',
    'SECTOR_4_ENTRANCE',
    'SECTOR_5_ENTRANCE',
    'SECTOR_6_ENTRANCE'
]


class MarsschemamfEnvironmentalDamage(typ.TypedDict):
    lava: TypeU8 = 20
    """The amount of damage per second taken while submerged in lava."""

    acid: TypeU8 = 60
    """The amount of damage per second taken while submerged in acid."""

    heat: TypeU8 = 6
    """The amount of damage per second taken while in a heated environment."""

    cold: TypeU8 = 15
    """The amount of damage per second taken while in a cold environment."""

    subzero: TypeU8 = 6
    """The amount of damage per second taken while in Sub-Zero Containment. Currently unused, will always use Cold."""


@typ.final
class MarsschemamfLevelEdits(typ.TypedDict, total=False):
    """Specifies the Room ID."""

    bg1: BlockLayer
    """The BG1 layer that should be edited."""

    bg2: BlockLayer
    """The BG2 layer that should be edited."""

    clipdata: BlockLayer
    """The Clipdata layer that should be edited."""




class MarsschemamfMinimapEditsItem(typ.TypedDict, total=False):
    x: TypeU5
    """The X position in the minimap that should get edited."""

    y: TypeU5
    """The Y position in the minimap that should get edited."""

    tile: TypeU10
    """The tile value that should be used to edit the minimap."""

    palette: TypeU4
    """The palette row to use for the tile."""

    h_flip: bool = False
    """Whether the tile should be horizontally flipped or not."""

    v_flip: bool = False
    """Whether the tile should be vertically flipped or not."""



class MarsschemamfRoomNamesItem(typ.TypedDict):
    area: AreaId
    """The area ID where this room is located."""

    room: TypeU8 = 3
    """The room ID."""

    name: typ.Annotated[str, 'len() <= 112']
    """Specifies what text should appear for this room. Two lines are available, with an absolute maximum of 56 characters per line, if all characters used are small. Text will auto-wrap if the next word doesn't fit on the line. If the text is too long, it will be truncated. Use 
 to force a line break. If not provided, will display 'Room name not provided'."""


class Marsschemamf(typ.TypedDict, total=False):
    """
    Metroid Fusion patching schema
    
    A json schema describing the input for patching Metroid Fusion via mars_patcher.
    """

    seed_hash: typ.Required[typ.Annotated[str, '/^[0-9A-Z]{8}$/']]
    """A seed hash that will be displayed on the file select screen."""

    music_replacement: MusicMapping
    """Shuffles the in-game music."""

    locations: typ.Required[MarsschemamfLocations]
    """Specifies how the item locations in the game should be changed."""

    required_metroid_count: typ.Required[typ.Annotated[int, '0 <= value <= 20']]
    """The number of infant Metroids that must be collected to beat the game."""

    starting_location: MarsschemamfStartingLocation
    """The location the player should spawn at the start of the game."""

    starting_items: MarsschemamfStartingItems = None
    tank_increments: MarsschemamfTankIncrements = None
    """How much ammo/health tanks provide when collected."""

    elevator_connections: MarsschemamfElevatorConnections
    """Defines the elevator that each elevator connects to."""

    sector_shortcuts: MarsschemamfSectorShortcuts
    """Defines the sector that each sector shortcut connects to."""

    door_locks: list[MarsschemamfDoorLocksItem]
    """List of all lockable doors and their lock type."""

    palettes: MarsschemamfPalettes = None
    """Properties for randomized in-game palettes."""

    rng: MarsschemamfRng
    """Properties for manipulating RNG-elements in the game. Specifying any value as 255 will cause that value to fallback to vanilla behaviour."""

    navigation_text: dict[ValidLanguages, MarsschemamfNavigationText] = None
    """Specifies text to be displayed at navigation rooms and the ship."""

    title_text: list[MarsschemamfTitleTextItem] = None
    """Lines of ASCII text to write to the title screen."""

    credits_text: list[MarsschemamfCreditsTextItem]
    """Lines of text to insert into the credits."""

    nav_station_locks: dict[MarsschemamfNavStationLocksKey, HintLocks]
    """Sets the required Security Levels for accessing Navigation Terminals."""

    disable_demos: bool = False
    """Disables title screen demos when true."""

    instant_unmorph: bool = False
    """When true, enables instant unmorphing via the SELECT button."""

    nerf_gerons: bool = False
    """When true, changes the Geron weaknesses to only be weak to their 'intended' values."""

    use_alternative_hud_health_layout: bool = False
    """When true, changes the HUD health layout to display 'currentHP/totalHP'."""

    use_toggle_for_secondary_weapon_selection: bool = False
    """When true, makes it so that pressing the R-Button toggles the secondary weapon selection instead of needing to hold it."""

    skip_door_transitions: bool = False
    """Makes all door transitions instant when true."""

    stereo_default: bool = True
    """Forces stereo sound by default when true."""

    disable_music: bool = False
    """Disables all music tracks when true."""

    disable_sound_effects: bool = False
    """Disables all sound effects when true."""

    environmental_damage: MarsschemamfEnvironmentalDamage
    missile_limit: TypeU8 = 3
    """Changes how many missiles can be on-screen at a time. The vanilla game has it set to 2, the randomizer changes it to 3 by default. Zero Mission uses 4."""

    unexplored_map: bool = False
    """When enabled, starts you with a map where all unexplored items and non-visited tiles have a gray background. This is different from the downloaded map stations where there, the full tile is gray."""

    level_edits: dict[AreaIdKey, dict[str, MarsschemamfLevelEdits]]
    """Specifies room edits that should be done. These will be applied last."""

    minimap_edits: dict[MinimapIdKey, list[MarsschemamfMinimapEditsItem]]
    """Specifies minimap edits that should be done."""

    hide_doors_on_minimap: bool = False
    """When enabled, hides doors on the minimap. This is automatically enabled when the 'DoorLocks' field is provided."""

    room_names: typ.Annotated[list[MarsschemamfRoomNamesItem], 'Unique items']
    """Specifies a name to be displayed when the A Button is pressed on the pause menu."""

    reveal_hidden_tiles: bool = False
    """When enabled, reveals normally hidden blocks that are breakable by upgrades. Hidden pickup tanks are not revealed regardless of this setting."""

MarsSchemaMF: typ.TypeAlias = Marsschemamf
