from dataclasses import dataclass
from typing import Dict, Any

from Options import Visibility, Choice, Range, DeathLink, PerGameCommonOptions, OptionDict, FreeText, OptionSet, \
    OptionCounter, \
    Toggle, OptionList, DefaultOnToggle, OptionGroup
from .Items import AEItem
from schema import Schema, Or, Optional


class GoalOption(Choice):
    """Choose the victory condition for this world.

        mm: First Specter fight in Monkey Madness, with the vanilla condition (just get there).
        ppm: Second Specter fight in Peak Point Matrix, with the vanilla condition (catch all monkeys). Peak Point Matrix will have the vanilla entry condition.
        tokenhunt: Collecting enough Specter Token items throughout the world.
        mmtoken: First Specter fight in Monkey Madness, after collecting enough Specter Token items.
        ppmtoken: Second Specter fight in Peak Point Matrix, after collecting enough Specter Token items.

        Supported values: mm, ppm, tokenhunt, mmtoken, ppmtoken
        Default value: mm
    """

    display_name = "Goal"
    option_mm = 0x00
    option_ppm = 0x01
    option_tokenhunt = 0x02
    option_mmtoken = 0x03
    option_ppmtoken = 0x04
    default = option_mm


class FastTokenGoalOption(Choice):
    """If this is enabled and the chosen goal is `mmtoken` or `ppmtoken`, provides easy access to the goal boss once enough Specter Tokens have been obtained.
    When enough Specter Tokens have been obtained, hold START while confirming a stage in the level select to warp directly to your goal boss, bypassing all other requirements.

        off: MM/PPM will only be accessible through World Keys by normal means.
        on: You will be able to warp directly to your goal boss by holding START in the level select.

        Supported values: off, on
        Default value: off
    """

    display_name = "Fast Token Goal"
    option_off = 0x00
    option_on = 0x01
    default = option_off


class AllowCollectOption(Toggle):
        """
        Allows for the !collect command used by other players to catch monkeys or collect Specter Coins in your world. This behaves the same as automatically using the /syncprogress command after someone !collects.
        """
        display_name = "Allow Collect"


class RequiredTokensOption(Range):
    """Choose the required number of Specter Tokens for goal.

        Supported values: 5 - 60
        Default value: 20
    """

    display_name = "Required Tokens"
    range_start = 5
    range_end = 60
    default = 20


class TotalTokensOption(Range):
    """Choose the total number of Specter Tokens in the item pool.
        If a world requests a token requirement greater than the number of tokens created, then the total and required values will be swapped.

        Supported values: 5 - 60
        Default value: 30
    """

    display_name = "Total Tokens"
    range_start = 5
    range_end = 60
    default = 30


class TokenLocationsOption(Choice):
    """Choose where Specter Tokens can be placed in the multiworld.

        anywhere: Specter Tokens can be placed anywhere in the multiworld.
        ownworld: Specter Tokens can only be placed in your world.

        Supported values: anywhere, ownworld
        Default value: ownworld
    """

    display_name = "Token Locations"
    option_anywhere = 0x00
    option_ownworld = 0x01
    default = option_ownworld


class LogicOption(Choice):
    """Choose expected trick knowledge.

        normal: No advanced movement tech or out of bounds required, and hard monkeys will guarantee a helpful gadget. Some additional difficult or precise jumps won't be required either. May still require some out of the box thinking or non-standard routes. Suitable for casual players.
        hard: Movement tech can be required in places with a low penalty for failing. Suitable for players with speedrun knowledge.
        expert: All tricks and glitches can be required, and some monkeys may require resetting the room if not caught in a certain way. Can also require obscure game knowledge. Suitable for those seeking the ultimate challenge.

        Supported values: normal, hard, expert
        Default value: normal
    """

    display_name = "Logic"
    option_normal = 0x00
    option_hard = 0x01
    option_expert = 0x02
    default = option_normal


class InfiniteJumpOption(Choice):
    """Choose if the Infinite Jump trick should be put into logic.

        false: Infinite Jump is not put into logic.
        true: Infinite Jump is put into logic.

        Supported values: false, true
        Default value: false
    """
    display_name = "Infinite Jump"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class SuperFlyerOption(Choice):
    """Choose if the Super Flyer trick should be put into logic.

        false: Super Flyer is not put into logic.
        true: Super Flyer is put into logic.

        Supported values: false, true
        Default value: false
    """
    display_name = "Super Flyer"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class EntranceOption(Choice):
    """Choose how the level entrances should be randomized. Can be used to access Entrance Plando with the custom option. For "mm", "ppm" and "ppmtoken" goals, Peak Point Matrix will always be the last level with its vanilla unlock condition. Races will be included in randomization if coin shuffle is on, and excluded otherwise.

        off: Levels will be in the vanilla order.
        recommended: The recommended preset for your chosen goal will be selected. For mm, this is "Lock Endgame". For ppm and ppmtoken, this is "Lock PPM". For everything else, this is "Random".
        levelshuffle: Levels will be in a random order.
        erashuffle: Each era will contain the levels from a random other era. Dimension X, containing the Jake races and Peak Point Matrix, counts as an era.
        lockendgame: Levels will be in a random order, with Monkey Madness and Peak Point Matrix forced to the end.
        lockppm: Levels will be in a random order, with Peak Point Matrix forced to the end.
        goallevelfirst: Levels will be in a random order, with your goal level forced to the start.
        custom: Uses the Entrance Plando option to determine level order, allowing any level to be placed at any entrance, with the rest placed randomly. This overrides coin shuffle race level placements, but does not override the ppm goal Peak Point Matrix placement.

        Supported values: off, recommended, levelshuffle, erashuffle, lockendgame, lockppm, goallevelfirst, custom
        Default value: recommended
    """

    display_name = "Entrance"
    option_off = 0x00
    option_recommended = 0x01
    option_levelshuffle = 0x02
    option_erashuffle = 0x03
    option_lockendgame = 0x04
    option_lockppm = 0x05
    option_goallevelfirst = 0x06
    option_custom = 0x07
    default = option_recommended


class EntrancePlandoOption(OptionDict):
    """If Entrance is Custom, forces the chosen levels to the chosen entrances. Note that if you plando a level to the Peak Point Matrix entrance for the ppm goal, this placement will be ignored!
    
        Format is Entrance: Level. Monkey Madness: Dexter's Island will result in Dexter's Island being at the Monkey Madness entrance. Any entrance not set will have a random level. Any level assigned to more than one entrance will be placed at the later entrance.
        The default sequence is a "reverse lock endgame" sequence.
        Level names: "Fossil Field", "Primordial Ooze", "Molten Lava", "Thick Jungle", "Dark Ruins", "Cryptic Relics", "Stadium Attack", "Crabby Beach", "Coral Cave", "Dexter's Island", "Snowy Mammoth", "Frosty Retreat", "Hot Springs", "Gladiator Attack", "Sushi Temple", "Wabi Sabi Wall", "Crumbling Castle", "City Park", "Specter's Factory", "TV Tower", "Monkey Madness", "Peak Point Matrix"
    """

    display_name = "Entrance Plando"
    level_names = ["Fossil Field", "Primordial Ooze", "Molten Lava", "Thick Jungle", "Dark Ruins", "Cryptic Relics", "Stadium Attack", "Crabby Beach", "Coral Cave", "Dexter's Island", "Snowy Mammoth", "Frosty Retreat", "Hot Springs", "Gladiator Attack", "Sushi Temple", "Wabi Sabi Wall", "Crumbling Castle", "City Park", "Specter's Factory", "TV Tower", "Monkey Madness", "Peak Point Matrix"]
    default = {
        "Fossil Field": "TV Tower",
        "Primordial Ooze": "Specter's Factory",
        "Molten Lava": "City Park",
        "Thick Jungle": "Crumbling Castle",
        "Dark Ruins": "Wabi Sabi Wall",
        "Cryptic Relics": "Sushi Temple",
        "Stadium Attack": "Gladiator Attack",
        "Crabby Beach": "Hot Springs",
        "Coral Cave": "Frosty Retreat",
        "Dexter's Island": "Snowy Mammoth",
        "Snowy Mammoth": "Dexter's Island",
        "Frosty Retreat": "Coral Cave",
        "Hot Springs": "Crabby Beach",
        "Gladiator Attack": "Stadium Attack",
        "Sushi Temple": "Cryptic Relics",
        "Wabi Sabi Wall": "Dark Ruins",
        "Crumbling Castle": "Thick Jungle",
        "City Park": "Molten Lava",
        "Specter's Factory": "Primordial Ooze",
        "TV Tower": "Fossil Field",
        "Monkey Madness": "Monkey Madness",
        "Peak Point Matrix": "Peak Point Matrix"
    }
    schema = Schema({
        Optional(Or(*level_names)): Or(*level_names)
    })


class DoorShuffleOption(Choice):
    """Choose how the transitions between rooms (doors) are randomized.
    ***This option is currently disabled due to instability***

    off: Doors will lead to their vanilla destinations.
    same_level: Doors are shuffled with other doors within the same level.

    Supported values: off, same_level
    Default value: off
    """

    display_name = "Door Shuffle"
    visibility = Visibility.none
    option_off = 0x00
    option_same_level = 0x01
    #option_same_level_decoupled = 0x02
    #same_level_decoupled: Doors are shuffled within the same level, and returning through a door may take you somewhere different.
    #option_cross_level = 0x03
    #cross_level: Doors are shuffled across levels.
    default = option_off


class RandomizeStartingRoomOption(Choice):
    """Choose if the starting room for each level should be randomized.

        off: The starting room for each level is the original starting room.
        on: The starting room for each level is a random room from within that level.

        Supported values: off, on
        Default value: off
    """

    display_name = "Randomize Starting Room"
    option_off = 0x00
    option_on = 0x01
    default = option_off


class KeyOption(Choice):
    """Choose how many levels each World Key should unlock. The first three levels will always start unlocked.
        Races will be skipped if coin shuffle is off. Peak Point Matrix will require the same number of keys as the Monkey Madness entrance on a boss goal, and one additional key on a token hunt or token boss goal.

        world: Each World Key unlocks the 1 or 3 levels in the next world. Creates between 6 and 9 World Keys.
        level: Each World Key unlocks the next level. Creates between 16 and 19 World Keys.
        twolevels: Each World Key unlocks the next two levels. Creates between 8 and 10 World Keys.
        none: All levels are open from the beginning of the game.

        Supported values: world, level, twolevels, none
        Default value: world
    """

    display_name = "Unlocks per Key"
    option_world = 0x00
    option_level = 0x01
    option_twolevels = 0x02
    option_none = 0x03
    default = option_world


class ExtraKeysOption(Range):
    """Choose the number of extra World Keys that should be created.

        Supported values: 0 - 10
        Default value: 0
    """

    display_name = "Extra Keys"
    range_start = 0
    range_end = 10
    default = 0


class CoinOption(Choice):
    """Choose if Specter Coins should be added as locations.

        false: Specter Coins are not locations.
        true: The 60 Specter Coins are added as locations.

        Supported values: false, true
        Default value: false
    """

    display_name = "Coin"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class JacketOption(Choice):
    """Choose if static jackets should act as locations.

        false: Jackets are not locations.
        true: The 23 available jackets are added as locations.

        Supported values: false, true
        Default value: false
    """

    display_name = "Jacket"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class MailboxOption(Choice):
    """Choose if mailboxes in the Time Station and levels should act as locations.
        Training rooms are in a different option.

        false: Mailboxes are not locations.
        true: The 63 available mailboxes are added as locations.

        Supported values: false, true
        Default value: false
    """

    display_name = "Mailbox"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class TrainingRoomsOption(Choice):
    """Choose if locations inside training rooms should be included as checks.

        false: Training rooms have no checks.
        completion: Training rooms have 1 check on completion.
        mailboxes: Training room mailboxes count as checks.

        Supported values: false, completion, mailboxes
        Default value: false
    """

    display_name = "Training Rooms"
    option_false = 0x00
    option_completion = 0x01
    option_mailboxes = 0x02
    default = option_false


class LampOption(Choice):
    """Choose if Monkey Lamps should be locked and shuffled into the multiworld.

        false: Monkey Lamps will act in vanilla (catch enough monkeys in their level to open the door)
        true: The 8 Monkey Lamps will be items in the multiworld, that open their respective door when received.

        Supported values: false, true
        Default value: false
    """

    display_name = "Monkey Lamps"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class GadgetOption(Choice):
    """Choose a starting gadget aside from the Time Net.

        club: Start with the Stun Club.
        radar: Start with the Monkey Radar.
        sling: Start with the Slingback Shooter.
        hoop: Start with the Super Hoop.
        flyer: Start with the Sky Flyer.
        car: Start with the RC Car.
        punch: Start with the Magic Punch.
        waternet: Start with the Water Net.
        none: Start with no additional gadgets.

        Supported values: club, radar, sling, hoop, flyer, car, punch, waternet, none
        Default value: club
    """

    display_name = "Gadget"
    option_club = 0x00
    option_radar = 0x01
    option_sling = 0x02
    option_hoop = 0x03
    option_flyer = 0x04
    option_car = 0x05
    option_punch = 0x06
    option_waternet = 0x07
    option_none = 0x08
    default = option_club


class ShuffleNetOption(Choice):
    """Choose if the Time Net should be shuffled.
        This option requires at least one of coins and mailboxes to be shuffled to be used - if all locations in this world require the net, the net will be given at game start.

        false: Time Net is not shuffled, and is given at game start.
        true: Time Net is shuffled into the pool. The mailboxes in the Time Station will also be locations if this happens.

        Supported values: false, true
        Default value: false
    """
    display_name = "Shuffle Net"
    option_false = 0x00
    option_true = 0x01
    default = option_false


class ShuffleWaterNetOption(Choice):
    """Choose if the Water Net should be shuffled.

        off: Water Net is not shuffled, and is given at game start.
        progressive: Water Net is shuffled and split into parts, adding two Progressive Water Nets and Water Catch to the pool.
        - Progressive Water Net : The first allows Spike to swim on the surface and avoid drowning after a few seconds. The second allows Spike to dive underwater.
        - Water Catch: Allows shooting the Water Net.
        on: Water Net is shuffled, adding it to the pool as a single item.

        Supported values: off, progressive, on
        Default value: off
    """
    display_name = "Shuffle Water Net"
    option_off = 0x00
    option_progressive = 0x01
    option_on = 0x02
    default = option_off


class LowOxygenSounds(Choice):
    """Choose how quickly the low oxygen beep sound effect will play when underwater.

        off: Low Oxygen sounds will not play at all.
        half: Low Oxygen sounds will play less frequently.
        on: Low Oxygen Sounds will play normally.

        Supported values: off, half, on
        Default value: half
    """
    display_name = "Low Oxygen Sounds"
    option_off = 0x00
    option_half = 0x01
    option_on = 0x02
    default = option_half


class FillerPreset(Choice):
    """Choose the distribution of filler items.

        Normal: Balanced distribution with better items appearing less often.
        Bountiful: Nearly every filler item will be useful.
        Stingy: Nearly every filler item will be its smallest quantity.
        Nothing: Replace all filler items with Nothing.
        Custom: Use custom weights set with the option "customfillerweights".

        Supported values: normal, bountiful, stingy, nothing, custom
        Default value: normal
    """
    display_name = "Filler Preset"
    option_normal = 0x00
    option_bountiful = 0x01
    option_stingy = 0x02
    option_nothing = 0x03
    option_custom = 0x04
    default = option_normal


class CustomFillerWeights(OptionCounter):
    """Use custom weights for filler item distribution by choosing "Custom" in the "Filler Preset" option.
        This works the same way as other weighted options.
        You can use a weight of 0 to prevent that filler item from appearing.
        If all weights are set to 0, then all filler items will be Nothing.

        Range: 0 - 100
        Default values are the same as the Normal preset.
    """
    internal_name = "customfillerweights"
    display_name = "Custom Filler Weights"
    default_weight = 10
    min = 0
    max = 100
    valid_keys = frozenset({
        AEItem.Shirt.value, AEItem.Cookie.value, AEItem.FiveCookies.value, AEItem.Triangle.value,
        AEItem.BigTriangle.value, AEItem.BiggerTriangle.value, AEItem.Flash.value, AEItem.ThreeFlash.value,
        AEItem.Rocket.value, AEItem.ThreeRocket.value, AEItem.RainbowCookie.value, AEItem.Nothing.value})
    default = {
        AEItem.Shirt.value: 7,
        AEItem.Cookie.value: 16,
        AEItem.FiveCookies.value: 3,
        AEItem.Triangle.value: 31,
        AEItem.BigTriangle.value: 14,
        AEItem.BiggerTriangle.value: 4,
        AEItem.Flash.value: 9,
        AEItem.ThreeFlash.value: 3,
        AEItem.Rocket.value: 9,
        AEItem.ThreeRocket.value: 3,
        AEItem.RainbowCookie.value: 6,
        AEItem.Nothing.value: 0
    }


class TrapPercentage(Range):
    """Replace a percentage of filler items in the item pool with random traps.

        Range: 0 - 100
        Default value: 0
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeights(OptionCounter):
    """Specify the weighted chance of rolling individual trap items.

        You can use a weight of 0 to guarantee a particular trap will never appear.
        **This option is ignored when "TrapPercentage" option is set to an other value than "custom"

        Range: 0 - 100
        Default values:
          Banana Peel Trap: 15
          Gadget Shuffle Trap: 13
          Monkey Mash Trap: 5
          Icy Hot Pants Trap: 10
          Stun Trap: 7
          Camera Rotate Trap: 10
    """
    internal_name = "customtrapweights"
    display_name = "Custom Trap Weights"
    min = 0
    max = 100
    valid_keys = frozenset({
        AEItem.BananaPeelTrap.value, AEItem.GadgetShuffleTrap.value, AEItem.MonkeyMashTrap.value, AEItem.IcyHotPantsTrap.value, AEItem.StunTrap.value, AEItem.CameraRotateTrap.value
    })
    default = {
        AEItem.BananaPeelTrap.value: 15,  AEItem.GadgetShuffleTrap.value : 13, AEItem.MonkeyMashTrap.value: 5, AEItem.IcyHotPantsTrap.value: 10, AEItem.StunTrap.value: 7, AEItem.CameraRotateTrap.value: 10
    }


class TrapsOnReconnect(OptionSet):
    """Determine which traps are sent when reconnecting.

        This option determines which traps will be sent when reconnecting to the client.
        Traps that are not in this list will only activate when connected

        Supported values: "Banana Peel Trap", "Gadget Shuffle Trap", "Monkey Mash Trap", "Icy Hot Pants Trap", "Stun Trap", "Camera Rotate Trap"
    """
    internal_name = "trapsonreconnect"
    display_name = "Traps On Reconnect"
    supports_weighting = False
    valid_keys = frozenset({
        AEItem.BananaPeelTrap.value,AEItem.GadgetShuffleTrap.value, AEItem.MonkeyMashTrap.value, AEItem.IcyHotPantsTrap.value, AEItem.StunTrap.value, AEItem.CameraRotateTrap.value
    })


class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players

    You will also receive any linked traps from other players with Trap Link enabled,
    if you have a weight above "none" set for that trap
    """
    display_name = "Trap Link"


class ItemDisplayOption(Choice):
    """Set the default for the Bizhawk item display command. This can be changed in the client at any time. The position and duration of these messages can be changed in Bizhawk config at any time.

        off: Receiving an item will not show a message in Bizhawk.
        on: Receiving an item will show a message in Bizhawk.

        Supported values: off, on
        Default value: on
    """
    display_name = "Item Display"
    option_off = 0x00
    option_on = 0x01
    default = option_on


class KickoutPreventionOption(Choice):
    """Set the default for Kickout Prevention behavior. This can be changed in the client at any time.

        off: Will always kick you out after catching the level's last monkey or defeating a boss.
        on: Prevents the kickout when catching the last monkey or defeating a boss.

        Supported values: off, on
        Default value: on
    """
    display_name = "Kickout Prevention"
    option_off = 0x00
    option_on = 0x01
    default = option_on


class AutoEquipOption(Choice):
    """Set the default for Auto Equipping new gadgets. This can be changed in the client at any time.

        off: Received gadgets need to be manually equipped.
        on: Received gadgets will automatically be equipped to an open face button, if one exists.

        Supported values: off, on
        Default value: on
    """
    display_name = "Auto Equip"
    option_off = 0x00
    option_on = 0x01
    default = option_on


class SpikeColor(Choice):
    """Determine the color of Spike in-game. This can be changed in the client at any time.
        Can select between the following presets, or choose "custom" to use a custom color set with the "CustomSpikeColor" option.

        Supported values: vanilla, dark, white, red, green, blue, yellow, cyan, magenta, custom
        Default value: vanilla
    """
    display_name = "Spike Color"
    option_vanilla = 0
    option_dark = 1
    option_white = 2
    option_red = 3
    option_green = 4
    option_blue = 5
    option_yellow = 6
    option_cyan = 7
    option_magenta = 8
    option_custom = -1
    default = option_vanilla


class CustomSpikeColor(FreeText):
    """Use a custom color for Spike by choosing "Custom" in the "Spike Color" option.
        Enter an RGB hexadecimal value for the desired color.
        **Note: If an invalid color is entered, it will be set to the "Vanilla" preset!

        Range: 000000 to FFFFFF
        Default value: FFFFFF
    """
    display_name = "Custom Spike Color"
    default = "FFFFFF"


@dataclass
class ApeEscapeOptions(PerGameCommonOptions):
    goal: GoalOption
    fasttokengoal: FastTokenGoalOption
    allowcollect: AllowCollectOption
    requiredtokens: RequiredTokensOption
    totaltokens: TotalTokensOption
    tokenlocations: TokenLocationsOption
    logic: LogicOption
    infinitejump: InfiniteJumpOption
    superflyer: SuperFlyerOption
    entrance: EntranceOption
    entranceplando: EntrancePlandoOption
    doorshuffle: DoorShuffleOption
    randomizestartingroom: RandomizeStartingRoomOption
    unlocksperkey: KeyOption
    extrakeys: ExtraKeysOption
    coin: CoinOption
    jacket: JacketOption
    mailbox: MailboxOption
    trainingrooms: TrainingRoomsOption
    lamp: LampOption
    gadget: GadgetOption
    shufflenet: ShuffleNetOption
    shufflewaternet: ShuffleWaterNetOption
    lowoxygensounds: LowOxygenSounds
    fillerpreset: FillerPreset
    customfillerweights: CustomFillerWeights
    trappercentage: TrapPercentage
    trapweights: TrapWeights
    trapsonreconnect: TrapsOnReconnect
    trap_link: TrapLink
    itemdisplay: ItemDisplayOption
    kickoutprevention: KickoutPreventionOption
    autoequip: AutoEquipOption
    spikecolor: SpikeColor
    customspikecolor: CustomSpikeColor
    death_link: DeathLink

ape_escape_option_groups = [
    OptionGroup("Goal", [
        GoalOption,
        FastTokenGoalOption,
        RequiredTokensOption,
        TotalTokensOption,
        TokenLocationsOption,
    ]),
    OptionGroup("Logic & Abilities", [
        LogicOption,
        InfiniteJumpOption,
        SuperFlyerOption,
        GadgetOption,
    ]),
    OptionGroup("Entrance & World", [
        EntranceOption,
        EntrancePlandoOption,
        RandomizeStartingRoomOption,
        KeyOption,
        ExtraKeysOption,
    ]),
    OptionGroup("Items & Locations", [
        CoinOption,
        JacketOption,
        MailboxOption,
        TrainingRoomsOption,
        LampOption,
        ShuffleNetOption,
        ShuffleWaterNetOption,
    ]),
    OptionGroup("Filler & Traps", [
        FillerPreset,
        CustomFillerWeights,
        TrapPercentage,
        TrapWeights,
        TrapsOnReconnect,
    ]),
    OptionGroup("Quality of Life", [
        LowOxygenSounds,
        ItemDisplayOption,
        KickoutPreventionOption,
        AutoEquipOption,
        SpikeColor,
        CustomSpikeColor,
    ]),
]