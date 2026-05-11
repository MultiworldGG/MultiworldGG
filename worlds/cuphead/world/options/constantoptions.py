### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from .. import enums as e
from .optionbase import BoolOption, ConstNumericOption, ConstToggle, EnumOption
from .protocols import NamedOption

## Option classes that are used internally and are constant value.
## They can never be set by the user. If set by the user, it will be
## ignored.

class BossPhaseChecks(EnumOption[e.BossPhaseCheckMode], ConstNumericOption, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    Enable phase checks for Boss Levels.
    Completing the phases in the fight will be a check.
    This excludes the final phase.
    """
    name = "boss_phase_checks"
    display_name = "Boss Phase Checks"
    enum_type = e.BossPhaseCheckMode
    value = 0


class BusterQuest(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "buster_quest"
    value = 1


class DlcRandomizeBoat(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "dlc_randomize_boat"
    value = 1


class DlcRequiresMausoleum(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "dlc_requires_mausoleum"
    value = 1


class FourMelQuest(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "fourmel_quest"
    value = 1


class GingerQuest(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "ginger_quest"
    value = 1


class LucienQuest(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "lucien_quest"
    value = 0


class MusicQuest(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "music_quest"
    value = 0


class RequireSecretShortcuts(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    """
    name = "require_secret_shortcuts"
    value = 1


class RandomizeAimAbilities(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    Randomize aiming abilities.
    You will start with only top-right.
    """
    name = "randomize_abilities_aim"
    display_name = "Randomize Aim Abilities"
    value = 0


class ShopMode(EnumOption[e.ShopMode], ConstNumericOption, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    --NOT YET IMPLEMENTED--
    Set shop mode.
    You get access to higher tiers the more shops you have access to.
    """
    name = "shop_mode"
    display_name = "Shop Mode"
    enum_type = e.ShopMode
    #visibility = Visibility.spoiler
    option_tiers = 0
    #option_strict_tiers = 1
    option_independent = 2
    default = 0
    value = 0


class WeaponGate(BoolOption, ConstToggle, NamedOption):
    """
    --NOT SUPPORTED OPTION--
    Add a weapon gate which only allows specific weapons for each fight.
    """
    name = "weapon_gate"
    display_name = "Weapon Gate"
    value = 0
