from dataclasses import asdict, dataclass
from Options import DeathLink, DefaultOnToggle, Choice, ExcludeLocations, LocalItems, NamedRange, NonLocalItems, \
    Range, OptionGroup, PerGameCommonOptions, PriorityLocations, StartHints, StartInventory, StartLocationHints, \
    Visibility


class CemuChoice(Choice):
    cemu_pack: str
    cemu_option: str = ""
    cemu_selection_names: list[str] = ["off", "on"]


@dataclass
class XenobladeXOption():
    cemu_pack: str = ""
    cemu_option: str = ""
    cemu_selection: str = ""


class EnemyAggro(CemuChoice):
    """Increase or decrease the enemy aggression"""
    display_name = "Enemy Aggro"
    option_none = 0
    option_hell_never_deaggro = 1
    option_increase_range_x2 = 2
    option_decrease_range_2 = 3
    option_decrease_range_4 = 4
    cemu_pack = "BattleEscapeDistance"
    cemu_option = "Active Preset"
    cemu_selection_names = [
        "off",
        "Hell: Enemies will never de-aggro",
        "Increase Range x2",
        "Decrease Range / 2",
        "Decrease Range / 4",
    ]


class EnemyStats(CemuChoice):
    """Adjust the stats of the enemies"""
    display_name = "Damage Divisor"
    option_none = 0
    option_25_percent = 1
    option_50_percent = 2
    option_75_percent = 3
    option_125_percent = 4
    option_150_percent = 5
    option_200_percent = 6
    option_hell_300_percent = 7
    option_impossible_1000_percent = 8
    cemu_pack = "BattleEnemyStats"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Set at 25%",
        "Set at 50%",
        "Set at 75%",
        "Set at 125%",
        "Set at 150%",
        "Set at 200%",
        "Hell: Set at 300%",
        "Impossible: Set at 1000%",
    ]


class DamageDivisor(CemuChoice):
    """Divide your teams damage output. Note: Displayed damage values stay the same regardless"""
    display_name = "Damage Divisor"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    cemu_pack = "BattleDamageModGround2"
    cemu_option = "Damage Divisor"
    cemu_selection_names = [
        "off",
        "Damage / 2",
        "Damage / 3",
        "Damage / 5",
        "Damage / 10",
        "Damage / 50",
        "Damage / 100",
    ]


class DamageMultiplicator(CemuChoice):
    """Multiply your teams damage output. Note: Displayed damage values stay the same regardless"""
    display_name = "Damage Multiplier"
    option_none = 0
    option_x2 = 1
    option_x3 = 2
    option_x5 = 3
    option_x10 = 4
    option_x25 = 5
    option_x100 = 6
    cemu_pack = "BattleDamageModGround"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Damage x2",
        "Damage x3",
        "Damage x5",
        "Damage x10",
        "Damage x25",
        "Damage x100",
    ]


class QteAuto(CemuChoice):
    """Automatically completes Quicktime-Events with the specified rating"""
    display_name = "Quicktime-Event Auto"
    option_none = 0
    option_excellent = 1
    option_good = 2
    option_fail = 3
    cemu_pack = "BattleQteSoulVoices"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Force Excellent",
        "Force Good",
        "Force Fail / Disable Soul Voices",
    ]


class QteSpeed(CemuChoice):
    """Sets the speed for every Quicktime-Event manually"""
    display_name = "Quicktime-Event Speed"
    option_none = 0
    option_slow = 1
    option_mid = 2
    option_fast = 3
    option_faster = 4
    cemu_pack = "BattleQteSpeed"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Slow",
        "Mid",
        "Fast",
        "Faster",
    ]


class QteSkell(CemuChoice):
    """Restores skells automatically if the insurance is still valid"""
    display_name = "Skell Recovery"
    option_off = 0
    option_on = 1
    cemu_pack = "BattleQteDollLost"
    cemu_option = ""
    cemu_selection_names = [
        "off",
        "on"
    ]


class CollectionRange(CemuChoice):
    """Increases the collection range of items in the field"""
    display_name = "Collection Range"
    option_none = 0
    option_big = 1
    option_bigger = 2
    cemu_pack = "CollectiblesCatchRange"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Big Range",
        "Bigger Range",
    ]


class ArmorSlotUpgrades(CemuChoice):
    """Allows you to further upgrade armor slots."""
    display_name = "Armor Slot Upgrades"
    option_off = 0
    option_on = 1
    cemu_pack = "EquipmentArmorsCanHave3AugmentSlots"
    cemu_option = ""
    cemu_selection_names = [
        "off",
        "on"
    ]


class ArmorTraitsUpgrades(CemuChoice):
    """Allows you to further upgrade equipment traits. Optional without ressources"""
    display_name = "Equip Trait Upgrades"
    option_none = 0
    option_normal = 1
    option_cheat = 2
    cemu_pack = "EquipmentUnlimitedAugmentUpgrades"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Normal",
        "CHEAT - Ignore Miranium and resources requirements",
    ]


class LvPointsModifier(CemuChoice):
    """Modifies the level experience gain and disables 9999 exp cap"""
    display_name = "Lv-Points Modifier"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_5 = 4
    option_10 = 5
    option_50 = 6
    option_100 = 7
    option_1000 = 8
    cemu_pack = "ExpInnerExpPointsX"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "x1",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
        "x100",
        "x1000",
    ]


class BattlePointsModifier(CemuChoice):
    """Modifies the battle experience gain"""
    display_name = "Battle-Points Modifier"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    option_1000 = 7
    cemu_pack = "ExpBattlePointsX"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Quantity x2",
        "Quantity x3",
        "Quantity x5",
        "Quantity x10",
        "Quantity x50",
        "Quantity x100",
        "Quantity x1000",
    ]


class BladePointsModifier(CemuChoice):
    """Modifies the BLADE experience gain"""
    display_name = "BLADE-Points Modifier"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    cemu_pack = "ExpBladePointsS"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
    ]


class FrontierNavMiraniumFrequency(CemuChoice):
    """Alters the frequency of the Frontier-Nav Miranium bonuses"""
    display_name = "Froniter-Nav Miranium Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    option_10 = 4
    option_15 = 5
    option_20 = 6
    cemu_pack = "FrontierNavProbeMiraniumFrequency"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Every minute",
        "Every 2 minutes",
        "Every 5 minutes",
        "Every 10 minutes",
        "Every 15 minutes",
        "Every 20 minutes",
    ]


class FrontierNavMiraniumQuantity(CemuChoice):
    """Alters the quantity of the Frontier-Nav Miranium bonuses"""
    display_name = "Froniter-Nav Miranium Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    cemu_pack = "FrontierNavProbeMiraniumQuantity"
    cemu_option = "Miranium quantity"
    cemu_selection_names = [
        "Miranium x1",
        "Miranium x2",
        "Miranium x3",
        "Miranium x5",
        "Miranium x10",
        "Miranium x50",
        "Miranium x100",
    ]


class FrontierNavMoneyFrequency(CemuChoice):
    """Alters the frequency of the Frontier-Nav Money bonuses"""
    display_name = "Froniter-Nav Miranium Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    option_7 = 4
    option_10 = 5
    cemu_pack = "FrontierNavProbeMoneyFrequency"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Every minute",
        "Every 2 minutes",
        "Every 5 minutes",
        "Every 7 minutes",
        "Every 10 minutes",
    ]


class FrontierNavMoneyQuantity(CemuChoice):
    """Alters the quantity of the Frontier-Nav Money bonuses"""
    display_name = "Froniter-Nav Miranium Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    option_1000 = 7
    cemu_pack = "FrontierNavProbeMoneyQuantity"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
        "x100",
        "x1000",
    ]


class FrontierNavResourcesFrequency(CemuChoice):
    """Alters the frequency of the Frontier-Nav Resource bonuses"""
    display_name = "Froniter-Nav Miranium Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    cemu_pack = "FrontierNavProbeResourcesFrequency"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Every 1 minute",
        "Every 2 minutes",
        "Every 5 minutes",
    ]


class FrontierNavResourcesQuantity(CemuChoice):
    """Alters the quantity of the Frontier-Nav Resource bonuses"""
    display_name = "Froniter-Nav Miranium Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    cemu_pack = "FrontierNavProbeResourcesQuantity"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
        "x100",
    ]


class FrontierNavNoMiraniumCap(CemuChoice):
    """Removes the Miranium cap caused by missing storage probes"""
    display_name = "Frontier-Nav no Miranium Cap"
    option_off = 0
    option_on = 1
    cemu_pack = "FrontierNavProbeMiraniumQuantity"
    cemu_option = "Capped by Storage Probes"
    cemu_selection_names = [
        "Yes",
        "No",
    ]


class EquipAlternateRatio(CemuChoice):
    """In vanilla, equipment traits have a percent chance to be selected, some of them have 90 or 100%
    , while others have 10%. This mod changes that: everything above 80% is capped at 80%
    , and everything else is set to 20%"""
    display_name = "Treasure Alternate Ratio"
    option_off = 0
    option_on = 1
    cemu_pack = "LootEquipmentsAlternateRandomAffix"
    cemu_option = ""
    cemu_selection_names = [
        "off",
        "on"
    ]


class EquipChestCount(CemuChoice):
    """Alters the guranteed item count in treasure chests"""
    display_name = "Treasure Chest Count"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    cemu_pack = "LootEquipmentsForceCount"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Always 1 equipments",
        "Always 2 equipments",
        "Always 3 equipments",
    ]


class EquipQuality(CemuChoice):
    """Alters the guranteed equipment trait count"""
    display_name = "Treasure Traits"
    option_none = 0
    option_0_traits = 1
    option_1_traits = 2
    option_2_traits = 3
    option_3_traits = 4
    cemu_pack = "LootEquipmentsForceQuality"
    cemu_option = "Quality"
    cemu_selection_names = [
        "off",
        "Common (0 traits)",
        "Rare (1 trait)",
        "Unique (2 traits)",
        "Prime (3 traits)",
    ]


class EquipSlots(CemuChoice):
    """Alters the guranteed equipment augments slots count"""
    display_name = "Augment Slots"
    option_none = 0
    option_0 = 1
    option_1 = 2
    option_2 = 3
    option_3 = 4
    cemu_pack = "LootEquipmentsForceQuality"
    cemu_option = "Number of Slots"
    cemu_selection_names = [
        "off",
        "0 Slots",
        "1 Slot",
        "2 Slots",
        "3 Slots",
    ]


class BrokenEquip(CemuChoice):
    """Alters chance to get broken equipment"""
    display_name = "Broken Treasure"
    option_none = 0
    option_never = 1
    option_always = 2
    cemu_pack = "LootEquipmentsIgnoreBroken"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Never get broken equipment",
        "Always get broken equipment",
    ]


class MaterialsDropRatio(CemuChoice):
    """Alters the materials drop ratio"""
    display_name = "Treasure Drop Ratio"
    option_none = 0
    option_drop_100_percent = 1
    option_drop_70_percent = 2
    option_drop_50_percent = 3
    option_drop_30_percent = 4
    option_drop_0_percent = 5
    cemu_pack = "LootMaterialsDrop"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Set minimum drop to 100% (always drop)",
        "Set minimum drop to 70% (always drop)",
        "Set minimum drop to 50% (always drop)",
        "Set minimum drop to 30% (always drop)",
        "Set minimum drop to 0% (never drop)",
    ]


class TreasureQuality(CemuChoice):
    """Forces a specific quality"""
    display_name = "Treasure Quality"
    option_none = 0
    option_gold_quality = 1
    option_silver_quality = 2
    option_bronze_quality = 3
    option_no_treasure = 4
    cemu_pack = "LootTreasureQuality"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Gold quality",
        "Silver quality",
        "Bronze quality",
        "No treasure",
    ]


class MoonJumpWidth(CemuChoice):
    """Alters the jump width"""
    display_name = "Moon Jump Width"
    option_none = 0
    option_distance_150_percent = 1
    option_distance_160_percent = 2
    option_distance_170_percent = 3
    option_distance_180_percent = 4
    option_distance_190_percent = 5
    option_distance_200_percent = 6
    option_distance_250_percent = 7
    option_distance_300_percent = 8
    option_distance_500_percent = 9
    option_cheat_1000_percent = 10
    cemu_pack = "PhysicsJumpToTheMoon"
    cemu_option = "Horizontal Velocity (distance reached)"
    cemu_selection_names = [
        "Distance x1.0 (default)",
        "Distance x1.5",
        "Distance x1.6",
        "Distance x1.7",
        "Distance x1.8",
        "Distance x1.9",
        "Distance x2.0",
        "Distance x2.5",
        "Distance x3.0",
        "Distance x5.0",
        "CHEAT x100.0",
    ]


class MoonJumpHeight(CemuChoice):
    """Alters the jump height"""
    display_name = "Moon Jump Height"
    option_none = 0
    option_height_105_percent = 1
    option_height_106_percent = 2
    option_height_107_percent = 3
    option_height_108_percent = 4
    option_height_109_percent = 5
    option_height_110_percent = 6
    option_height_120_percent = 7
    option_height_130_percent = 8
    option_height_140_percent = 9
    option_height_150_percent = 10
    option_height_2500_percent = 11
    cemu_pack = "PhysicsJumpToTheMoon"
    cemu_option = "Vertical Velocity (height)"
    cemu_selection_names = [
        "Height x1.0 (default)",
        "Height x1.05",
        "Height x1.06",
        "Height x1.07",
        "Height x1.08",
        "Height x1.09",
        "Height x1.10",
        "Height x1.20",
        "Height x1.30",
        "Height x1.40",
        "Height x1.50",
        "CHEAT x25.0",
    ]


class MoonJumpType(CemuChoice):
    """Alters the landing type after the jump"""
    display_name = "Moon Jump Type"
    option_short_land = 0
    option_step_forward = 1
    option_normal_land = 2
    option_role = 3
    option_full_stop = 4
    option_half_stop = 5
    option_never_land_softlocks = 6
    cemu_pack = "PhysicsJumpToTheMoon"
    cemu_option = "Landing type"
    cemu_selection_names = [
        "Short land (4)",
        "Step foreward (6)",
        "Normal land (5)",
        "Role (3)",
        "Full stop (2)",
        "Half stop (1)",
        "Never land (0) SOFT LOCKS",
    ]


class RunForrestRun(CemuChoice):
    """Alters the running speed"""
    display_name = "Run Forrest, Run"
    option_none = 0
    option_speed_125_percent = 1
    option_speed_150_percent = 2
    option_speed_200_percent = 3
    option_speed_300_percent = 4
    option_cheat_2000_percent = 5
    cemu_pack = "PhysicsRunForrestRun"
    cemu_option = "Active preset"
    cemu_selection_names = [
        "off",
        "Speed x1.25",
        "Speed x1.5",
        "Speed x2",
        "Speed x3",
        "CHEAT x20",
    ]


class IncludeCollectopediaLocations(DefaultOnToggle):
    """Allows you to get items from collectopedia entries and adds those locations to the pool"""
    display_name = "Include Collectopedia Locations"


class IncludeEnemyBookLocations(DefaultOnToggle):
    """Allows you to get items from completing enemy entries(white dot in the menu)
    and adds those locations to the pool"""
    display_name = "Include Enemy Book Locations"


class EnemyBookThreshold(CemuChoice):
    """Sets the required kills to unlock a enemy location. White dot in enemy book appears at 3 for normal enemies.
    Uniques are fixed at 1"""
    display_name = "Enemy Book Threshold"
    default = 3
    option_discovery = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    cemu_pack = "AP"
    cemu_option = "EnemyBookThreshold"
    cemu_selection_names = [
        "discovery",
        "1",
        "2",
        "3",
    ]


class IncludeLocationLocations(DefaultOnToggle):
    """Allows you to get items from locations and adds those locations to the pool"""
    display_name = "Include Location Locations"


class IncludeQuestLocations(DefaultOnToggle):
    """Allows you to receive items from quests and adds those locations to the pool"""
    display_name = "Include Quest Locations"


class IncludeShopLocations(CemuChoice):
    """Allows you to receive items from the shop and adds those locations to the pool"""
    display_name = "Include Shop Locations"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "Shops"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeGroundArmor(CemuChoice):
    """Allows you to receive ground armor as items and adds those items to the pool"""
    display_name = "Include Ground Armor Items"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "GroundArmor"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeGroundWeapons(CemuChoice):
    """Allows you to receive ground weapons as items and adds those items to the pool"""
    display_name = "Include Ground Weapon Items"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "GroundWeapons"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeGroundAugments(CemuChoice):
    """Allows you to receive ground augments as items and adds those items to the pool"""
    display_name = "Include Ground Augment Items"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "GroundAugments"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeSkellArmor(CemuChoice):
    """Allows you to receive skell armor as items and adds those items to the pool"""
    display_name = "Include Skell Armor Items"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "SkellArmor"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeSkellWeapons(CemuChoice):
    """Allows you to receive skell weapons as items and adds those items to the pool"""
    display_name = "Include Skell Weapons Items"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "SkellWeapons"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeSkellAugments(CemuChoice):
    """Allows you to receive skell augments as items and adds those items to the pool"""
    display_name = "Include Skell Augment Items"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "SkellAugments"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeImportantItems(CemuChoice):
    """Allows you to receive important items and adds those items to the pool. Increases generation time"""
    display_name = "Include Important Items"
    default = 0
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "ImportantItems"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeBlueprints(CemuChoice):
    """Allows you to receive blueprints/schematics as items and adds those items to the pool."""
    display_name = "Include Blueprints"
    default = 0
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "Blueprints"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class IncludeCharacterLevel(CemuChoice):
    """Connects your logic level to your character level. This disables the normal way to increase your level.
     Dont enable if Logic Level Steps is disabled."""
    display_name = "Include Character Level"
    default = 1
    option_off = 0
    option_on = 1
    cemu_pack = "AP"
    cemu_option = "IncludeCharacterLevel"
    cemu_selection_names = [
        "disable",
        "on",
    ]


class LogicLevelSteps(NamedRange):
    """Defines the individual progress each level logic item provides. Higher means bigger ingame level increase
     per item, but lower item count in the pool"""
    display_name = "Logic Level Steps"
    default = 5
    range_start = 1
    range_end = 20
    special_range_names = {
        "disable": 0,
    }


class LogicLevelOvercap(Range):
    """Adds the specified number of level logic items to increase the chance of progressing"""
    display_name = "Logic Level Overcap"
    default = 0
    range_start = 0
    range_end = 20


class DrifterRangedWeaponType(CemuChoice):
    """Select the ranged weapon starter type for the drifter class"""
    display_name = "Drifter Ranged Weapon Type"
    option_assault_rifle_vanilla = 0
    option_sniper_rifle = 1
    option_dual_guns = 2
    option_gatling_gun = 3
    option_raygun = 4
    option_psycho_launchers = 5
    default = "random"  # type: ignore[assignment]
    cemu_pack = "AP"
    cemu_option = "DrifterRangedWeapon"
    cemu_selection_names = [
        "Assault Rifle",
        "Sniper Rifle",
        "Dual Guns",
        "Gatling Gun",
        "Raygun",
        "Psycho Launchers",
    ]


class DrifterMeleeWeaponType(CemuChoice):
    """Select the melee weapon starter type for the drifter class"""
    display_name = "Drifter Melee Weapon Type"
    option_longsword = 0
    option_javelin = 1
    option_dual_swords = 2
    option_shield = 3
    option_knife_vanilla = 4
    option_photon_sabre = 5
    default = "random"  # type: ignore[assignment]
    cemu_pack = "AP"
    cemu_option = "DrifterMeleeWeapon"
    cemu_selection_names = [
        "Longsword",
        "Javelin",
        "Dual Swords",
        "Shield",
        "Knife",
        "Photon Sabre",
    ]


class HiddenLocalItems(LocalItems):
    __doc__ = LocalItems.__doc__
    visibility = Visibility.template | Visibility.spoiler


class HiddenNonLocalItems(NonLocalItems):
    __doc__ = NonLocalItems.__doc__
    visibility = Visibility.template | Visibility.spoiler


class HiddenStartInventory(StartInventory):
    __doc__ = StartInventory.__doc__
    visibility = Visibility.template | Visibility.spoiler


class HiddenStartHints(StartHints):
    __doc__ = StartHints.__doc__
    visibility = Visibility.template | Visibility.spoiler


class HiddenStartLocationHints(StartLocationHints):
    __doc__ = StartLocationHints.__doc__
    visibility = Visibility.template | Visibility.spoiler


class HiddenExcludeLocations(ExcludeLocations):
    __doc__ = ExcludeLocations.__doc__
    visibility = Visibility.template | Visibility.spoiler


class HiddenPriorityLocations(PriorityLocations):
    __doc__ = PriorityLocations.__doc__
    visibility = Visibility.template | Visibility.spoiler


@dataclass
class XenobladeXOptions(PerGameCommonOptions):
    # Game
    death_link: DeathLink

    # Locations
    clp: IncludeCollectopediaLocations
    loc: IncludeLocationLocations
    # shp: IncludeShopLocations
    # qst: IncludeQuestLocations
    ebk: IncludeEnemyBookLocations
    enemy_book_threshold: EnemyBookThreshold

    # Items
    amr: IncludeGroundArmor
    wpn: IncludeGroundWeapons
    aug: IncludeGroundAugments
    skwpn: IncludeSkellWeapons
    skamr: IncludeSkellArmor
    skaug: IncludeSkellAugments
    impit: IncludeImportantItems
    # blp: IncludeBlueprints
    character_level: IncludeCharacterLevel

    # Logic
    logic_level_steps: LogicLevelSteps
    logic_level_overcap: LogicLevelOvercap

    # Customisation
    drifter_ranged_weapon_type: DrifterRangedWeaponType
    drifter_melee_weapon_type: DrifterMeleeWeaponType

    # Graphic packs
    enemy_aggro: EnemyAggro
    enemy_stats: EnemyStats
    damage_divisor: DamageDivisor
    damage_multiplicator: DamageMultiplicator
    qte_auto: QteAuto
    qte_speed: QteSpeed
    qte_skell: QteSkell
    collection_range: CollectionRange
    armor_slot_upgrades: ArmorSlotUpgrades
    armor_traits_upgrades: ArmorTraitsUpgrades
    lv_points_modifier: LvPointsModifier
    battle_points_modifier: BattlePointsModifier
    blade_points_modifier: BladePointsModifier
    frontier_nav_miranium_frequency: FrontierNavMiraniumFrequency
    frontier_nav_miranium_quantity: FrontierNavMiraniumQuantity
    frontier_nav_money_frequency: FrontierNavMoneyFrequency
    frontier_nav_money_quantity: FrontierNavMoneyQuantity
    frontier_nav_resources_frequency: FrontierNavResourcesFrequency
    frontier_nav_resources_quantity: FrontierNavResourcesQuantity
    frontier_nav_no_miranium_cap: FrontierNavNoMiraniumCap
    equip_alternate_ratio: EquipAlternateRatio
    equip_chest_count: EquipChestCount
    equip_quality: EquipQuality
    equip_slots: EquipSlots
    broken_equip: BrokenEquip
    materials_drop_ratio: MaterialsDropRatio
    treasure_quality: TreasureQuality
    moon_jump_width: MoonJumpWidth
    moon_jump_height: MoonJumpHeight
    moon_jump_type: MoonJumpType
    run_forrest_run: RunForrestRun

    # Removed
    local_items: HiddenLocalItems  # pyright: ignore[reportIncompatibleVariableOverride]
    non_local_items: HiddenNonLocalItems  # pyright: ignore[reportIncompatibleVariableOverride]
    start_inventory: HiddenStartInventory  # pyright: ignore[reportIncompatibleVariableOverride]
    start_hints: HiddenStartHints   # pyright: ignore[reportIncompatibleVariableOverride]
    start_location_hints: HiddenStartLocationHints  # pyright: ignore[reportIncompatibleVariableOverride]
    exclude_locations: HiddenExcludeLocations  # pyright: ignore[reportIncompatibleVariableOverride]
    priority_locations: HiddenPriorityLocations  # pyright: ignore[reportIncompatibleVariableOverride]


def generate_cemu_options(options: XenobladeXOptions) -> list[dict[str, str]]:
    return [asdict(XenobladeXOption(option.cemu_pack, option.cemu_option, option.cemu_selection_names[option.value]))
            for option in asdict(options).values() if isinstance(option, CemuChoice)]


option_groups: list[OptionGroup] = [
    OptionGroup("Locations", [
        IncludeCollectopediaLocations,
        IncludeLocationLocations,
        # IncludeQuestLocations,
        # IncludeShopLocations,
        IncludeEnemyBookLocations,
        EnemyBookThreshold,
    ]),
    OptionGroup("Items", [
        IncludeGroundArmor,
        IncludeGroundWeapons,
        IncludeGroundAugments,
        IncludeSkellWeapons,
        IncludeSkellArmor,
        IncludeSkellAugments,
        IncludeImportantItems,
        # IncludeBlueprints,
        IncludeCharacterLevel,
    ]),
    OptionGroup("Logic", [
        LogicLevelSteps,
        LogicLevelOvercap,
    ]),
    OptionGroup("Customisation", [
        DrifterRangedWeaponType,
        DrifterMeleeWeaponType,
    ]),
    OptionGroup("Graphic packs", [
        EnemyAggro,
        EnemyStats,
        DamageDivisor,
        DamageMultiplicator,
        QteAuto,
        QteSpeed,
        QteSkell,
        CollectionRange,
        ArmorSlotUpgrades,
        ArmorTraitsUpgrades,
        LvPointsModifier,
        BattlePointsModifier,
        BladePointsModifier,
        FrontierNavMiraniumFrequency,
        FrontierNavMiraniumQuantity,
        FrontierNavMoneyFrequency,
        FrontierNavMoneyQuantity,
        FrontierNavResourcesFrequency,
        FrontierNavResourcesQuantity,
        FrontierNavNoMiraniumCap,
        EquipAlternateRatio,
        EquipChestCount,
        EquipQuality,
        EquipSlots,
        BrokenEquip,
        MaterialsDropRatio,
        TreasureQuality,
        MoonJumpWidth,
        MoonJumpHeight,
        MoonJumpType,
        RunForrestRun,
    ])
]
