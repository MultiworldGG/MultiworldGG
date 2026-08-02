from dataclasses import dataclass
from typing import Any

from Options import Toggle, PerGameCommonOptions, DeathLink, Choice, DefaultOnToggle, OptionGroup


class EnableMainQuestLocations(DefaultOnToggle):
    """Include locations usually containing items to complete the main quest. When disabled, core items will stay in the item pool and filler items are placed at these locations"""
    display_name = "Main quest item locations"


class EnableHeartRubyLocations(DefaultOnToggle):
    """Include Heart ruby locations."""
    display_name = "Heart Ruby locations"


class EnableEnergyGemLocations(DefaultOnToggle):
    """Include Energy gem locations."""
    display_name = "Energy Gem locations"


class EnableAncientVault(Toggle):
    """Include upgrades from Ancient Vault.
    Warning: The logical requirement to clear this is bare minimum. Even while having every item in the game I consider these checks extremely difficult. God gamers only."""
    display_name = "Ancient Vault upgrades"


class EnableMoonstoneLocations(DefaultOnToggle):
    """Include Moonstone locations."""
    display_name = "Moonstone locations"


class KeepExcludedStatusUpgradesInItemPool(DefaultOnToggle):
    """When enabled, Heart rubies, Energy gems and Moonstones will stay in the item pool if not included. Filler items are placed at the disabled locations.
    When disabled, these items can be acquired at their vanilla locations.
    Warning: disabling this setting is incompatible with certain other settings as these items are required in the pool"""
    display_name = "Keep status upgrades and moonstones in item pool when locations are excluded"


class EnableLunarArtifactLocations(DefaultOnToggle):
    """Include Lunar Artifact locations"""
    display_name = "Include Lunar Artifact locations"


class EnableFishingSpots(DefaultOnToggle):
    """Include items gotten from catching fish"""
    display_name = "Include fishing spots"


class EnableNpcGifts(Toggle):
    """Include free gifts from NPCs"""
    display_name = "Include NPC gifts"


class EnablePlantoRewards(Toggle):
    """Include rewards from Mr. Planto after giving them food units"""
    display_name = "Include Planto rewards"


class EnableItemsInBreakables(Toggle):
    """Include utility items found in breakable objects like pots and boxes"""
    display_name = "Include items in breakables objects"


class EnableSidequests(Toggle):
    """Include checks related to sidequests"""
    display_name = "Include sidequests"


class EnableFreestandingItems(Toggle):
    """Include utility items found in freestanding locations"""
    display_name = "Include freestanding items"


class EnableMinigames(Toggle):
    """Include items won through minigames"""
    display_name = "Include minigames"


class EnablePerros(Toggle):
    """Include findable Perros"""
    display_name = "Include Perros"


class EnableMisc(Toggle):
    """Include miscellaneous locations (Strange Urn & Atai berry selling reward)"""
    display_name = "Include miscellaneous"


class EnableShopSanity(Toggle):
    """Includes items that can be bought it shops"""
    display_name = "Shop sanity"


class EnableSmallAnimalDrops(Toggle):
    """Includes drops from animals like lizards, mice and scorpions"""
    display_name = "Include small animal drops"


class EnableRinLocations(Choice):
    """Includes rin pickups from chests and other breakables that give at least 5 rin"""
    display_name = "Include rin locations"
    option_no = 0
    option_chests_only = 1
    option_everything = 2
    default = 1


class EnableTrapChests(Toggle):
    """Includes chests that usually contain only 1 Rin"""
    display_name = "Include small animal drops"


class EnableGEOChallengeRewards(Toggle):
    """Includes the rewards you get from completing GEO challenges"""
    display_name = "Include GEO challenge rewards"


class EnableOuroborosShrines(Toggle):
    """Includes the rewards at the end of Ouroboros Shrines"""
    display_name = "Include Ouroboros shrines"


# Dungeon item shuffle

class DungeonItemShuffle(Choice):
    """Determines where dungeon items can be placed.
    - **Vanilla**: Places dungeon items at their vanilla location
    - **Own Dungeon**: Places dungeon items shuffled within their dungeon
    - **Anywhere**: Dungeon items can be found across the multiworld"""
    display_name = "Dungeon item shuffle"
    option_vanilla = 0
    option_own_dungeon = 1
    option_anywhere = 2
    default = 1


class AnuriPearlstoneShuffle(DungeonItemShuffle):
    """Determines where Anuri Pearlstones can be placed.
    - **Vanilla**: Places Anuri Pearlstones at their vanilla location
    - **Own Dungeon**: Places Anuri Pearlstones shuffled within their dungeon
    - **Anywhere**: Anuri Pearlstones can be found across the multiworld"""
    display_name = "Anuri Pearlstone shuffle"
    default = 1


class OuroGuardKeyShuffle(DungeonItemShuffle):
    """Determines where Ouro Guard Keys can be placed.
    - **Vanilla**: Places Ouro Guard Keys at their vanilla location
    - **Own Dungeon**: Places Ouro Guard Keys shuffled within their dungeon
    - **Anywhere**: Ouro Guard Keys can be found across the multiworld"""
    display_name = "Ouro Guard Key shuffle"
    default = 1


# Quality of life settings

class StartWithWoodenBat(DefaultOnToggle):
    """Start out with wooden bat"""
    display_name = "Start with wooden bat"


class BundleAnuriPearlstones(Toggle):
    """Bundles Anuri Pearlstones into an Anuri Pearlstone necklace with infinite uses"""
    display_name = "Bundle Anuri Pearlstones"


class BundleOuroGuardKeys(Toggle):
    """Bundles Ouro Guard Keys into an Ouro Guard Keyring with infinite uses"""
    display_name = "Bundle Ouro Guard Keys"


class OpenPanseloGates(Toggle):
    """Opens the Panselo gates by default. The gates require a weapon to be opened. Enabling this setting will increase the amount of starting locations"""
    display_name = "Open Panselo gates"


class UpgradableBats(Toggle):
    """Instead of finding bats of random tiers, upgrade up one tier every time you find a bat"""
    display_name = "Upgradable bats"


class UpgradableTools(Toggle):
    """Upgradable tools are found in order. e.g. civilian crossbow is always found before double crossbow"""
    display_name = "Upgradable moonstone tools"


class UpgradableSpear(Toggle):
    """Instead of Sonic Spear and Spear Bomb being two separate items, you will always find Sonic Spear first and then upgrade with the Spear Bomb"""
    display_name = "Upgradable Spear"


class UpgradablePrelude(Toggle):
    """Instead of Prelude of Panselo and the Spell of Rejuvenation being two separate items, you will always find Prelude of Panselo first and then upgrade it with the Spell of Rejuvenation first"""
    display_name = "Upgradable Prelude of Panselo"


@dataclass
class PhoaOptions(PerGameCommonOptions):
    enable_main_quest_locations: EnableMainQuestLocations
    enable_heart_ruby_locations: EnableHeartRubyLocations
    enable_energy_gem_locations: EnableEnergyGemLocations
    enable_ancient_vault: EnableAncientVault
    enable_moonstone_locations: EnableMoonstoneLocations
    enable_lunar_artifacts_locations: EnableLunarArtifactLocations
    enable_fishing_spots: EnableFishingSpots
    enable_npc_gifts: EnableNpcGifts
    enable_planto_rewards: EnablePlantoRewards
    enable_breakables: EnableItemsInBreakables
    enable_sidequests: EnableSidequests
    enable_freestanding: EnableFreestandingItems
    enable_minigames: EnableMinigames
    enable_perros: EnablePerros
    enable_misc: EnableMisc
    shop_sanity: EnableShopSanity
    enable_small_animal_drops: EnableSmallAnimalDrops
    enable_rin_locations: EnableRinLocations
    enable_trap_chests: EnableTrapChests
    enable_geo_challenge_rewards: EnableGEOChallengeRewards
    enable_ouroboros_shrines: EnableOuroborosShrines
    anuri_pearlstone_shuffle: AnuriPearlstoneShuffle
    ouro_guard_key_shuffle: OuroGuardKeyShuffle
    start_with_wooden_bat: StartWithWoodenBat
    bundle_anuri_pearlstones: BundleAnuriPearlstones
    bundle_ouro_guard_keys: BundleOuroGuardKeys
    upgradable_bats: UpgradableBats
    upgradable_tools: UpgradableTools
    upgradable_spear: UpgradableSpear
    upgradable_prelude: UpgradablePrelude
    open_panselo_gates: OpenPanseloGates
    keep_excluded_status_upgrades_in_item_pool: KeepExcludedStatusUpgradesInItemPool
    death_link: DeathLink

    def get_slot_data_dict(self) -> dict[str, Any]:
        return self.as_dict(
            "enable_main_quest_locations",
            "enable_heart_ruby_locations",
            "enable_energy_gem_locations",
            "enable_ancient_vault",
            "enable_moonstone_locations",
            "enable_lunar_artifacts_locations",
            "enable_fishing_spots",
            "enable_npc_gifts",
            "enable_planto_rewards",
            "enable_breakables",
            "enable_sidequests",
            "enable_freestanding",
            "enable_minigames",
            "enable_perros",
            "enable_misc",
            "shop_sanity",
            "enable_small_animal_drops",
            "enable_rin_locations",
            "enable_trap_chests",
            "enable_geo_challenge_rewards",
            "enable_ouroboros_shrines",
            "anuri_pearlstone_shuffle",
            "ouro_guard_key_shuffle",
            "start_with_wooden_bat",
            "bundle_anuri_pearlstones",
            "bundle_ouro_guard_keys",
            "upgradable_bats",
            "upgradable_tools",
            "upgradable_spear",
            "upgradable_prelude",
            "open_panselo_gates",
            "keep_excluded_status_upgrades_in_item_pool",
            "death_link",
        )


phoa_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Progress Locations",
        [
            EnableMainQuestLocations,
            EnableHeartRubyLocations,
            EnableEnergyGemLocations,
            EnableAncientVault,
            EnableMoonstoneLocations,
            EnableLunarArtifactLocations,
            EnableFishingSpots,
            EnableNpcGifts,
            EnablePlantoRewards,
            EnableItemsInBreakables,
            EnableSidequests,
            EnableFreestandingItems,
            EnableMinigames,
            EnablePerros,
            EnableMisc,
            EnableShopSanity,
            EnableSmallAnimalDrops,
            EnableRinLocations,
            EnableTrapChests,
            EnableGEOChallengeRewards,
            EnableOuroborosShrines,
        ],
    ),
    OptionGroup(
        "Dungeon Item Shuffle",
        [
            AnuriPearlstoneShuffle,
            OuroGuardKeyShuffle,
        ],
    ),
    OptionGroup(
        "Item Randomizer Modes",
        [
            KeepExcludedStatusUpgradesInItemPool,
            StartWithWoodenBat,
            BundleAnuriPearlstones,
            BundleOuroGuardKeys,
            OpenPanseloGates,
            UpgradableBats,
            UpgradableTools,
            UpgradableSpear,
            UpgradablePrelude,
        ],
    ),
]
