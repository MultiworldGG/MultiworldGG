from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)


# Logic Settings
class LogicRules(Choice):
    """
    Controls what types of tricks the logic can expect you to perform.

    - Glitchless: Only intended mechanics are required
    - Glitched: Some glitches may be required
    """

    # - No Logic: No logical requirements are enforced

    display_name = "Logic Rules"
    option_glitchless = 0
    option_glitched = 1
    # option_no_logic = 2
    default = 0


# region Generation
class TrapFrequency(Choice):
    """
    Controls the frequency of traps in the game.
    """

    display_name = "Trap Frequency"
    option_no_traps = 0
    option_few = 1
    option_many = 3
    option_mayhem = 7
    option_nightmare = 100
    default = 0


class GoldenBugsShuffled(Toggle):
    """
    If enabled, golden bugs will be shuffled into the itempool.
    If disabled, bugs will be vanilla and agitha will not be progression
    Note: If vanilla any precollected bugs will not be removed from vanilla locations
    """

    display_name = "Golden Bugs"
    default = True


class SkyCharactersShuffled(Toggle):
    """
    If enabled, sky characters will be shuffled into the itempool.
    If disabled, sky characters will be vanilla.
    Note: If vanilla any precollected sky characters will not be removed from vanilla locations
    """

    display_name = "Sky Characters"
    default = True


class NpcItemsShuffled(Toggle):
    """
    If enabled, Gifts from NPCs can be progression items.
    """

    display_name = "Gifts from NPCs"
    default = True


class ShopItemsShuffled(Toggle):
    """
    If enabled, Shop Items can be progression items.
    """

    display_name = "Shop Items"
    default = True


class HiddenSkillsShuffled(Toggle):
    """
    If enabled, golden wolfs can be progression items.
    *Hidden skills will always be shuffled into item pool.
    """

    display_name = "Hidden Skills"
    default = True


class PoeShuffled(Toggle):
    """
    If enabled, Poes will be shuffled into the itempool.
    If disabled, Poes will be vanilla.
    Note: If vanilla any precollected poes will not be removed from vanilla locations
    """

    display_name = "Poe Shuffled"
    default = True


class HeartPieceShuffled(Toggle):
    """
    If enabled, Heart Piece locations can contain progression items.
    """

    display_name = "Heart Pieces"
    default = True


class FreeStandingRupeeShuffle(Toggle):
    """
    If enabled, Freestanding Rupee locations can contain progression items.
    """

    display_name = "Freestanding Rupee Shuffle"
    default = False


class HiddenRupeeShuffle(Toggle):
    """
    If enabled, Hidden Rupee locations can contain progression items.
    """

    display_name = "Hidden Rupee Shuffle"
    default = False


class DungeonsShuffled(Toggle):
    """
    If enabled, Dungeons locations can contain progression items.
    Cannot be disabled if Overworld shuffle is disabled
    """

    display_name = "Dungeons Shuffled"
    default = True


class OverWoldShuffled(Toggle):
    """
    !!!!! Do not disable !!!!
    -- Currently disabling will cause generation failure --
    -- System to allow for succesful generation is in devlopment --

    If enabled, Overworld locations can contain progression items.
    Cannot be disabled if Dungeon shuffle is disabled
    Note:
    Disabling may lead to generation failures as the possible location count is reduced dramtically.
    """

    display_name = "Overworld Items"
    default = True


class EarlyShadowCrystal(Toggle):
    """
    When Enabled, the generator will be told to place the Shadow Crystal in the early spheres
    """

    display_name = "Early Shadow Crystal"
    default = False


# endregion
# region Dungeon Items


class DungeonItem(Choice):
    option_vanilla = 0
    option_own_dungeon = 1
    option_any_dungeon = 2
    option_anywhere = 3
    option_startwith = 4
    default = 0

    @property
    def in_dungeon(self) -> bool:
        return self.value in (0, 1, 2)


class SmallKeySettings(DungeonItem):
    """
    Controls how small keys are randomized.

    - **Start With Small Keys:** You will start the game with the small keys for all dungeons.
    - **Vanilla Small Keys:** Small keys will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Small Keys:** Small keys will be randomized locally within their own dungeon.
    - **Any Dungeon Small Keys:** Small keys will be randomized locally within any dungeon.
    - **Anywhere:** Small keys can be found in any progression location, if dungeons are randomized.

    Note:
    - Not shuffling Dungeons will overwrite this to vanilla, unless you selected start with
    - If vanilla any precollected keys will not be removed from vanilla locations
    """

    item_name_group = "Small Keys"
    display_name = "Randomize Small Keys"


class BigKeySettings(DungeonItem):
    """
    Controls how big keys are randomized.

    - **Start With Big Keys:** You will start the game with the big keys for all dungeons.
    - **Vanilla Big Keys:** Big keys will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Big Keys:** Big keys will be randomized locally within their own dungeon.
    - **Any Dungeon Big Keys:** Big keys will be randomized locally within any dungeon.
    - **Anywhere:** Big keys can be found in any progression location.

    Note:
    - Not shuffling Dungeons will overwrite this to vanilla, unless you selected start with
    - If vanilla any precollected keys will not be removed from vanilla locations
    """

    item_name_group = "Big Keys"
    display_name = "Randomize Big Keys"


class MapAndCompassSettings(DungeonItem):
    """
    Controls how dungeon maps and compasses are randomized.

    - **Start With Maps & Compasses:** You will start the game with the dungeon maps and compasses for all dungeons.
    - **Vanilla Maps & Compasses:** Dungeon maps and compasses will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Maps & Compasses:** Dungeon maps and compasses will be randomized locally within their own dungeon.
    - **Any Dungeon Maps & Compasses:** Dungeon maps and compasses will be randomized locally within any dungeon.
    - **Anywhere:** Dungeon maps and compasses can be found anywhere, without restriction.

    Note:
    - Not shuffling Dungeons will overwrite this to vanilla, unless you selected start with
    - If vanilla any precollected map or compass will not be removed from vanilla locations
    """

    item_name_group = "Maps and Compasses"
    display_name = "Randomize Maps & Compasses"


class DungeonRewardsProgression(Choice):
    """
    Controls whether dungeon reward and heart containers are forced to have progression items.
    Note: chossing vanilla with dungeons shuffled can cause generation issues so be careful when chosing vanilla
    """

    display_name = "Dungeon Rewards are prgression"
    option_any_progressive = 2
    option_vanilla = 1
    option_anything = 0
    default = 0


class SmallKeysOnBosses(Toggle):
    """
    If disabled, Small keys cannot be placed on boss rewards
    """

    display_name = "Small Keys on Bosses"
    default = False


# endregion
# region Access Settings


class CastleRequirements(Choice):
    """
    Controls requirements for accessing Hyrule Castle.

    - Open: The barrier around Hyrule Castle is dispelled from the beginning.
    - Fused Shadows: The barrier will be dispelled once the required number of Fused Shadows have been collected.
    - Mirror Shards: The barrier will be dispelled once the required number of Mirror Shards have been collected.
    - Dungeons: The barrier will be dispelled once the required number of Dungeons have been cleared.
    - Vanilla: The player must complete Palace of Twilight.
    - Poe Souls: The barrier will be dispelled once the required number of Poe Souls have been collected.
    - Hearts: The barrier will be dispelled once the required number of Hearts have been reached.

    """

    display_name = "Castle Requirements"
    option_open = 0
    option_fused_shadows = 1
    option_mirror_shards = 2
    option_dungeons = 3
    option_vanilla = 4
    option_poe_souls = 5
    option_hearts = 6
    default = 0


class CastleRequirementsCount(Range):
    """
    Controls the required number of things for the Castle requirements

    - Open: not used
    - Fused Shadows: max 3
    - Mirror Shards: max 4
    - Dungeons: max 8
    - Vanilla: not used
    - Poe Souls: max 60
    - Hearts: min 4, max 20
    """

    display_name = "Castle Requirement Count"
    range_end = 60
    range_start = 0
    default = 1


class CastleBKRequirements(Choice):
    """
    When enabled, the HC Big Key will be placed in its vanilla location with the gate in front of it locked. Only when the specified criteria have been met will the gate unlock.

    -None: The gate is opened and the key is randomized according to the respective Big Key settings.
    -Fused Shadows: The gate will open once the required number of Fused Shadows have been collected.
    -Mirror Shards: The gate will open once the required number of Mirror Shards have been collected.
    -Dungeons: The gate will open once the required number of Dungeons have been cleared.
    -Poe Souls: The gate will open once the required number of Poe Souls have been collected.
    -Hearts: The gate will open once the required number of Hearts have been reached."""

    display_name = "Castle Boss Key Requirements"
    option_none = 0
    option_fused_shadows = 1
    option_mirror_shards = 2
    option_dungeons = 3
    option_poe_souls = 4
    option_hearts = 5
    default = 0


class CastleBKRequirementsCount(Range):
    """
    Controls the required number of things for the Castle Boss Key requirements

    - Open: not used
    - Fused Shadows: max 3
    - Mirror Shards: max 4
    - Dungeons: max 8
    - Poe Souls: max 60
    - Hearts: min 4, max 20
    """

    display_name = "Castle Boss Key Requirement Count"
    range_end = 60
    range_start = 0
    default = 1


class PalaceRequirements(Choice):
    """
    Controls requirements for accessing Palace of Twilight.

    - Open: No requirements
    - Fused Shadows: Requires all Fused Shadows
    - Mirror Shards: Requires all Mirror Shards
    - Vanilla: Beat City in the Sky

    Note:
    Choosing Vanilla will force Palace of Twilight(PoT) to only have it's own dungeon items inside.
        i.e. If Vanilla and Keys Anywhere is picked Palace of Twilight Boss key cannot be in PoT and PoT. small key can only be in PoT.
    """

    display_name = "Palace Requirements"
    option_open = 0
    option_fused_shadows = 1
    option_mirror_shards = 2
    option_vanilla = 3
    default = 0


class FaronWoodsLogic(Choice):
    """
    Controls logic for accessing Faron Woods.

    - Open: No special requirements
    - Closed: Requires forest temple to be beaten before leaving faron woods

    Note:
    Choosing Closed will force dungeons items to be in Forest Temple if Any Dungeon is chosen for them
        This also removes Forest Temple from list of dungeons for other of that dungeon item to be in
    """

    display_name = "Faron Woods Logic"
    option_open = 0
    option_closed = 1
    default = 0


# endregion
# region Timesavers


class SkipMinorCutscenes(Toggle):
    """
    If enabled, minor cutscenes are skipped.
    """

    display_name = "Skip Minor Cutscenes"
    default = True


class FastIronBoots(Toggle):
    """
    If enabled, movement is not slowed when wearing Iron Boots.
    """

    display_name = "Fast Iron Boots"
    default = True


class QuickTransform(Toggle):
    """
    If enabled, you can quickly transform by pressing R + Y.
    """

    display_name = "Quick Transform"
    default = True


class TransformAnywhere(Toggle):
    """
    If enabled, the player can transform anywhere.
    """

    display_name = "Transform Anywhere"
    default = True


class ModifyShopModels(Toggle):
    """
    If enabled, swap shop models with the items that are placed there.
    """

    display_name = "Modify Shop Models"
    default = False


class GoronMinesEntrance(Choice):
    """
    Controls requirements for accessing the Goron Mines.

    - **Closed:** Player must wrestle Gor Coron to enter the mines.
    - **No Wrestling:** Player does not have to wrestle Gor Coron.
    - **Open:** Same as No Wrestling but you can use the elevator immediately.
    """

    display_name = "Goron Mines Entrance"
    option_closed = 0
    option_no_wrestling = 1
    option_open = 2
    default = 2


class SkipLakebedEntrance(Toggle):
    """
    If enabled, the Lakebed does not require water bombs.
    """

    display_name = "Lakebed Does not require water bombs"
    default = True


class SkipArbitersGroundsEntrance(Toggle):
    """
    If enabled, entering Arbiters Grounds does not require defeating King Bulblin.
    """

    display_name = "Arbiters Grounds Does not require Bulblin Camp"
    default = True


class SkipSnowpeakEntrance(Toggle):
    """
    If enabled, Snowpeak does not require Reekfish Scent.
    """

    display_name = "Snowpeak Does not require Reekfish Scent"
    default = True


class GroveEntrance(Toggle):
    """
    If enabled, Skull Kid will not need to be defeated to access Sacred Grove.
    """

    display_name = "Sacred Grove Entrance"
    default: False


class ToTEntrance(Choice):
    """
    Sets the minimum progressive sword level that is required to strike the pedestal in Sacred Grove and the Temple of Time.
    This means that if set to Ordon Sword, the pedestal can be struck with the Ordon, Master, or Light Sword, but not the Wooden Sword.

    If set to 'none', the player does not need to strike the sword into the pedestal.
    """

    display_name = "Temple of Time Sword Requirement"
    option_none = 0
    option_wooden_sword = 1
    option_ordon_sword = 2
    option_master_sword = 3
    option_light_sword = 4
    default = 0


class SkipCityInTheSkyEntrance(Toggle):
    """
    If enabled, City in The Sky does not require filled Skybook.
    """

    display_name = "City in The Sky Does not require filled Skybook"
    default = True


class InstantMessageText(Toggle):
    """
    If enabled, message text is instant.
    """

    display_name = "Instant Message Text"
    default = True


class OpenMap(Toggle):
    """
    If enabled, Map areas are unlocked and portals unlocked.
    """

    display_name = "Open Map"
    default = True


class IncreaseSpinnerSpeed(Toggle):
    """
    If enabled, spinner speed is increased.
    *Spinner speed not taken into account in logic.
    """

    display_name = "Increase Spinner Speed"
    default = True


class OpenDoorOfTime(Toggle):
    """
    If enabled, the Door of Time is open.
    """

    display_name = "Open Door of Time"
    default = False


class DamageMagnification(Choice):
    """
    Multiplies the damage the player takes.
    """

    display_name = "Damage Multiplier"
    option_vanilla = 1
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_ohko = 5
    default = 1


class BonksDoDamage(Toggle):
    """
    If enabled, bonks do damage.
    """

    display_name = "Bonks Do Damage"
    default = False


class SkipMajorCutscenes(Toggle):
    """
    If enabled, major cutscenes are skipped.
    """

    display_name = "Skip Major Cutscenes"
    default = True


class StartingToD(Choice):
    """
    Controls the starting time of day.
    """

    display_name = "Starting Time of Day"
    option_morning = 0
    option_noon = 1
    option_evening = 2
    option_night = 3
    default = 0


class GoronMinesShortcut(Toggle):
    """If enabled, all magnets within Goron Mines except the final one will automatically be activated. The final magnet remains deactivated to avoid a softlock."""

    display_name = "Active Goron Mine Magnets"
    default = False


class CastleShortcut(Toggle):
    """If enabled, the shortcut chandelier in the Hyrule Castle main hall will be lowered, and the double Dinalfos room will be cleared.

    This allows for you to continue from the main hall to the southern balcony more quickly and with fewer item requirements (ex: no Gale Boomerang).
    """

    display_name = "Lower Hyrule Castle Chandelier"
    default = False


class WalletSize(Choice):
    """Changes the capacity of the wallet
    - Reduced: Sets the wallet capacities to 99, 500, and 1000
    - Vanila: Sets the wallet capacities to 300, 600, and 1000.
    - HD: Sets the wallet capacities to 500, 1000, and 2000.
    - Large: Sets the wallet capacities to 1000, 5000, and 9999."""

    display_name = " Wallet Size"
    option_reduced = 0
    option_vanilla = 1
    option_hd = 2
    option_large = 3
    default = 1


class AutoFillWalet(Toggle):
    """Starts the player with a full wallet. Wallet upgrades will also fill the wallet."""

    display_name = "Automatically Fill Wallets"
    default = False


class SkipBridgeDona(Toggle):
    """If enabled, the bridge to Castle Town from Eldin Field will be automatically repaired."""

    display_name = "Skip Castle Town Bridge Donation"
    default = False


class IliaQuest(Choice):
    """
    With this setting, the player can choose the point in the sequence they want the Ilia Memory Quest to start.
    Selecting an item shuffles that specific item into world, precompleting the previous items in the quest.

    Later items in the sequence are vanilla with the exception of the 'Ilia Memory Reward' item, which is always randomized.

    Note:
    Skipped locations will still appear on UT / Trackers but will not be collectable
    """

    display_name = "Ilia Memory Quest"
    option_vanilla = 0
    option_letter = 1
    option_invoice = 2
    option_statue = 3
    option_charm = 4
    defult = 0


# endregion


@dataclass
class TPOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for The Wind Waker.
    """

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Item Pool Settings
    golden_bugs_shuffled: GoldenBugsShuffled
    sky_characters_shuffled: SkyCharactersShuffled
    npc_items_shuffled: NpcItemsShuffled
    shop_items_shuffled: ShopItemsShuffled
    hidden_skills_shuffled: HiddenSkillsShuffled
    poe_shuffled: PoeShuffled
    heart_piece_shuffled: HeartPieceShuffled
    freestanding_rupee_shuffled: FreeStandingRupeeShuffle
    hidden_rupee_shuffled: HiddenRupeeShuffle
    overworld_shuffled: OverWoldShuffled
    dungeons_shuffled: DungeonsShuffled

    # Dungeon Items
    small_key_settings: SmallKeySettings
    big_key_settings: BigKeySettings
    map_and_compass_settings: MapAndCompassSettings
    dungeon_rewards_progression: DungeonRewardsProgression
    small_keys_on_bosses: SmallKeysOnBosses

    # Logic Settings
    logic_rules: LogicRules
    castle_requirements: CastleRequirements
    castle_requirements_count: CastleRequirementsCount
    castle_bk_requirements: CastleBKRequirements
    castle_bk_requirements_count: CastleBKRequirementsCount
    palace_requirements: PalaceRequirements
    faron_woods_logic: FaronWoodsLogic

    # Timesavers
    skip_minor_cutscenes: SkipMinorCutscenes
    skip_major_cutscenes: SkipMajorCutscenes
    fast_iron_boots: FastIronBoots
    quick_transform: QuickTransform
    instant_message_text: InstantMessageText
    open_map: OpenMap
    increase_spinner_speed: IncreaseSpinnerSpeed
    open_door_of_time: OpenDoorOfTime
    wallet_size: WalletSize
    goron_mines_sc: GoronMinesShortcut
    castle_sc: CastleShortcut

    # Additional Settings
    transform_anywhere: TransformAnywhere
    modify_shop_models: ModifyShopModels
    bonks_do_damage: BonksDoDamage
    trap_frequency: TrapFrequency
    damage_magnification: DamageMagnification
    starting_tod: StartingToD
    auto_fill_wallet: AutoFillWalet
    skip_bridge_don: SkipBridgeDona
    ilia_quest: IliaQuest

    # Dungeon Entrance Settings
    skip_lakebed_entrance: SkipLakebedEntrance
    skip_arbiters_grounds_entrance: SkipArbitersGroundsEntrance
    skip_snowpeak_entrance: SkipSnowpeakEntrance
    skip_city_in_the_sky_entrance: SkipCityInTheSkyEntrance
    goron_mines_entrance: GoronMinesEntrance
    grove_entrance: GroveEntrance
    tot_entrance: ToTEntrance

    early_shadow_crystal: EarlyShadowCrystal


tp_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Item Pool / Location Settings",
        [
            GoldenBugsShuffled,
            SkyCharactersShuffled,
            NpcItemsShuffled,
            ShopItemsShuffled,
            HiddenSkillsShuffled,
            PoeShuffled,
            HeartPieceShuffled,
            FreeStandingRupeeShuffle,
            HiddenRupeeShuffle,
            OverWoldShuffled,
            DungeonsShuffled,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Logic Settings",
        [
            LogicRules,
            CastleRequirements,
            CastleRequirementsCount,
            CastleBKRequirements,
            CastleBKRequirementsCount,
            PalaceRequirements,
            FaronWoodsLogic,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Dungeon Items",
        [
            SmallKeySettings,
            BigKeySettings,
            MapAndCompassSettings,
            DungeonRewardsProgression,
            SmallKeysOnBosses,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Timesavers",
        [
            SkipMinorCutscenes,
            SkipMajorCutscenes,
            FastIronBoots,
            QuickTransform,
            InstantMessageText,
            OpenMap,
            IncreaseSpinnerSpeed,
            OpenDoorOfTime,
            EarlyShadowCrystal,
            GoronMinesShortcut,
            CastleShortcut,
            SkipBridgeDona,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Additional Settings",
        [
            TransformAnywhere,
            WalletSize,
            AutoFillWalet,
            BonksDoDamage,
            TrapFrequency,
            DamageMagnification,
            StartingToD,
            # HintDistribution,
            IliaQuest,
            ModifyShopModels,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Dungeon Entrance Settings",
        [
            SkipLakebedEntrance,
            SkipArbitersGroundsEntrance,
            SkipSnowpeakEntrance,
            SkipCityInTheSkyEntrance,
            GoronMinesEntrance,
            GroveEntrance,
            ToTEntrance,
        ],
        start_collapsed=True,
    ),
]
