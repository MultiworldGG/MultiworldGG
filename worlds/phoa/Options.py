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


class EnableMoonstoneLocations(DefaultOnToggle):
    """Include Moonstone locations."""
    display_name = "Moonstone locations"


class KeepExcludedStatusUpgradesInItemPool(DefaultOnToggle):
    """When enabled, Heart rubies, Energy gems and Moonstones will stay in the item pool if not included. Filler items are placed at the disabled locations.
    When disabled, these items can be acquired at their vanilla locations"""
    auto_display_name = "Keep status upgrades and moonstones in item pool when locations are excluded"


# class EnableDungeonKeys(DefaultOnToggle):
#     """Include dungeon key items like Anuri Pearlstones"""
#     display_name = "Include dungeon items"


class EnableLunarArtifactLocations(DefaultOnToggle):
    """Include Lunar Artifact locations"""
    display_name = "Include Lunar Artifact locations"


class EnableFishingSpots(DefaultOnToggle):
    """Include items gotten from catching fish"""
    display_name = "Include fishing spots"


class EnableNpcGifts(Toggle):
    """Include free gifts from NPCs"""
    display_name = "Include NPC gifts"


class EnableMisc(Toggle):
    """Include miscellaneous locations and items"""
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


class EnableGEOChallengeRewards(Toggle):
    """Includes the rewards you get from completing GEO challenges"""
    display_name = "Include GEO challenge rewards"


class StartWithWoodenBat(DefaultOnToggle):
    """Start out with wooden bat"""
    display_name = "Start with wooden bat"


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


@dataclass
class PhoaOptions(PerGameCommonOptions):
    enable_main_quest_locations: EnableMainQuestLocations
    enable_heart_ruby_locations: EnableHeartRubyLocations
    enable_energy_gem_locations: EnableEnergyGemLocations
    enable_moonstone_locations: EnableMoonstoneLocations
    # enable_dungeon_items: EnableDungeonKeys
    enable_lunar_artifacts_locations: EnableLunarArtifactLocations
    enable_fishing_spots: EnableFishingSpots
    enable_npc_gifts: EnableNpcGifts
    enable_misc: EnableMisc
    shop_sanity: EnableShopSanity
    enable_small_animal_drops: EnableSmallAnimalDrops
    enable_rin_locations: EnableRinLocations
    enable_geo_challenge_rewards: EnableGEOChallengeRewards
    start_with_wooden_bat: StartWithWoodenBat
    upgradable_bats: UpgradableBats
    upgradable_tools: UpgradableTools
    upgradable_spear: UpgradableSpear
    open_panselo_gates: OpenPanseloGates
    keep_excluded_status_upgrades_in_item_pool: KeepExcludedStatusUpgradesInItemPool
    death_link: DeathLink

    def get_slot_data_dict(self) -> dict[str, Any]:
        return self.as_dict(
            "enable_main_quest_locations",
            "enable_heart_ruby_locations",
            "enable_energy_gem_locations",
            "enable_moonstone_locations",
            # "enable_dungeon_items",
            "enable_lunar_artifacts_locations",
            "enable_fishing_spots",
            "enable_npc_gifts",
            "enable_misc",
            "shop_sanity",
            "enable_small_animal_drops",
            "enable_rin_locations",
            "enable_geo_challenge_rewards",
            "start_with_wooden_bat",
            "upgradable_bats",
            "upgradable_tools",
            "upgradable_spear",
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
            EnableMoonstoneLocations,
            # EnableDungeonKeys,
            EnableLunarArtifactLocations,
            EnableFishingSpots,
            EnableNpcGifts,
            EnableMisc,
            EnableShopSanity,
            EnableSmallAnimalDrops,
            EnableRinLocations,
            EnableGEOChallengeRewards,
        ],
    ),
    OptionGroup(
        "Item Randomizer Modes",
        [
            KeepExcludedStatusUpgradesInItemPool,
            StartWithWoodenBat,
            OpenPanseloGates,
            UpgradableBats,
            UpgradableTools,
            UpgradableSpear,
        ],
    ),
]
