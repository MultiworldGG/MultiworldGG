### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable
from random import Random

from ..auxiliary import format_list
from ..enums import ChaliceCheckMode, ChaliceMode, ChessCastleMode, CurseMode, LogicMode, WeaponMode
from ..levels import levelshuffle, leveltype
from . import CupheadOptions
from .protocols import CupheadNumericOption, CupheadOptionSet


class OptionSanitizer:
    def __init__(
            self,
            player: int,
            player_name: str,
            options: CupheadOptions,
            random: Random,
            solo: bool,
            log_overrides: bool = True,
            sanitize_goal_options: bool = False,
        ):
        self.option_overrides: list[str] = []
        self.player = player
        self.player_name = player_name
        self.options = options
        self.random = random
        self.solo = solo
        self.log_overrides = log_overrides
        self.strict_goal_options = sanitize_goal_options

    def print_warning(self, message: str):
        if self.log_overrides:
            print(f"Warning: For player {self.player} ({self.player_name}): {message}")

    def override_num_option(
            self,
            option: CupheadNumericOption,
            value: int,
            reason: str | None = None,
            quiet: bool = False
        ):
        _old_value_key = option.current_key
        option.value = value
        string = f'{option.name}: "{_old_value_key}" -> "{option.current_key}".'
        if reason:
            string += f" Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f'Option "{option.name}" was overridden from "{_old_value_key}" to "{option.current_key}".'
            msg_reason = f"Reason: {reason}."
            self.print_warning(f"{msg} {msg_reason}")

    def override_option_set(
            self,
            option: CupheadOptionSet,
            values: Iterable[str],
            add_mode: bool = False,
            reason: str | None = None,
            quiet: bool = False
        ):
        values_str = format_list(values, enc_start="'", enc_end="'")
        mode_str = "added to" if add_mode else "removed from"
        string = f"{option.name}: '{values_str}' {mode_str} set."
        if reason:
            string += f" Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option '{option.name}' was overridden with '{values_str}' {mode_str} set."
            msg_reason = f"Reason: {reason}."
            self.print_warning(f"{msg} {msg_reason}")
        if add_mode:
            option.value.update(values)
        else:
            option.value.difference_update(values)

    def override_option_set_clear(
            self,
            option: CupheadOptionSet,
            reason: str | None = None,
            quiet: bool = False
        ):
        string = f"{option.name}: Set cleared."
        if reason:
            string += f" Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option '{option.name}' was overridden with set cleared."
            msg_reason = f"Reason: {reason}."
            self.print_warning(f"{msg} {msg_reason}")
        option.value.clear()

    def _sanitize_dlc_chalice_item_options(self, quiet: bool = False):
        _options = self.options
        abilities_val = "abilities"
        if len(_options.dlc_chalice_items_separate.value) > 0:
            if abilities_val in _options.dlc_chalice_items_separate.value and not _options.randomize_abilities:
                self.override_option_set(
                    _options.dlc_chalice_items_separate,
                    {abilities_val},
                    False,
                    "Randomize Abilities Off",
                    quiet
                )
            if _options.dlc_chalice.value == int(ChaliceMode.CHALICE_ONLY):
                self.override_option_set_clear(
                    _options.dlc_chalice_items_separate,
                    "Chalice Mode is Chalice Only",
                    True
                )

    def _sanitize_dlc_chalice_checks(self, quiet: bool = False):
        _options = self.options
        _boss_cchecks = _options.dlc_boss_chalice_checks.value
        _rungun_cchecks = _options.dlc_rungun_chalice_checks.value
        if (_boss_cchecks & ChaliceCheckMode.GRADE_REQUIRED) > 0 and _options.boss_grade_checks.value == 0:
            _boss_cchecks &= ~ChaliceCheckMode.GRADE_REQUIRED
            self.override_num_option(
                _options.dlc_boss_chalice_checks, _boss_cchecks, "Boss Grade Checks Disabled", True
            )
        if (_rungun_cchecks & ChaliceCheckMode.GRADE_REQUIRED) > 0 and _options.rungun_grade_checks.value == 0:
            _rungun_cchecks &= ~ChaliceCheckMode.GRADE_REQUIRED
            self.override_num_option(
                _options.dlc_rungun_chalice_checks, _rungun_cchecks, "Run n' Gun Grade Checks Disabled", True,
            )

    def _sanitize_dlc_chalice_options(self, quiet: bool = False):
        _options = self.options
        _cm_disabled = int(ChaliceMode.DISABLED)
        _cm_chalice_only = int(ChaliceMode.CHALICE_ONLY)
        if _options.dlc_chalice.value == _cm_disabled or _options.dlc_chalice.value == _cm_chalice_only:
            chalice_reason = "Chalice Only" if _options.dlc_chalice.value == _cm_chalice_only else "Chalice Off"
            _ccm_disable = int(ChaliceCheckMode.DISABLED)
            if _options.dlc_boss_chalice_checks.value:
                self.override_num_option(_options.dlc_boss_chalice_checks, _ccm_disable, chalice_reason, True)
            if _options.dlc_rungun_chalice_checks.value:
                self.override_num_option(_options.dlc_rungun_chalice_checks, _ccm_disable, chalice_reason, True)
            if _options.dlc_kingdice_chalice_checks.value:
                self.override_num_option(_options.dlc_kingdice_chalice_checks, _ccm_disable, chalice_reason, True)
            if _options.dlc_chess_chalice_checks.value:
                self.override_num_option(_options.dlc_chess_chalice_checks, _ccm_disable, chalice_reason, True)
            if _options.dlc_cactusgirl_quest.value:
                self.override_num_option(_options.dlc_cactusgirl_quest, _ccm_disable, chalice_reason, quiet)
        self._sanitize_dlc_chalice_item_options(quiet)
        self._sanitize_dlc_chalice_checks(quiet)

    def _sanitize_dlc_options(self):  # noqa: C901
        _options = self.options
        use_dlc = _options.use_dlc.value
        if not use_dlc:
            dlc_reason = "DLC Off"
            _ccm_disable = int(ChaliceCheckMode.DISABLED)
            if _options.dlc_chalice.value != int(ChaliceMode.DISABLED):
                self.override_num_option(_options.dlc_chalice, int(ChaliceMode.DISABLED), dlc_reason, True)
            if _options.dlc_curse_mode.value != int(CurseMode.OFF):
                self.override_num_option(_options.dlc_curse_mode, int(CurseMode.OFF), dlc_reason, True)
            if _options.dlc_kingsleap.value != int(ChessCastleMode.EXCLUDE):
                self.override_num_option(_options.dlc_kingsleap, int(ChessCastleMode.EXCLUDE), dlc_reason, True)
            if _options.dlc_boss_chalice_checks.value != _ccm_disable:
                self.override_num_option(_options.dlc_boss_chalice_checks, _ccm_disable, dlc_reason, True)
            if _options.dlc_rungun_chalice_checks.value != _ccm_disable:
                self.override_num_option(_options.dlc_rungun_chalice_checks, _ccm_disable, dlc_reason, True)
            if _options.dlc_kingdice_chalice_checks.value != _ccm_disable:
                self.override_num_option(_options.dlc_kingdice_chalice_checks, _ccm_disable, dlc_reason, True)
            if _options.dlc_chess_chalice_checks.value != _ccm_disable:
                self.override_num_option(_options.dlc_chess_chalice_checks, _ccm_disable, dlc_reason, True)
            if _options.dlc_cactusgirl_quest.value:
                self.override_num_option(_options.dlc_cactusgirl_quest, 0, dlc_reason, True)
            # Sanitize mode
            if _options.mode.value > 4:
                # TODO: Once modes can be combined, remove this and use randint
                _mode_choices = [1, 2, 4]
                self.override_num_option(_options.mode, self.random.choice(_mode_choices), dlc_reason)
            # Sanitize start_weapon
            if _options.start_weapon.value > 5 and not _options.start_weapon.is_none():
                self.override_num_option(_options.start_weapon, self.random.randint(0,5), dlc_reason)
        self._sanitize_dlc_chalice_options(not use_dlc)

    def _sanitize_goal_requirements(self):
        _options = self.options

        _goal_reason = "Goal cannot be less than requirements"

        # Sanitize settings
        if _options.contract_goal_requirements.value < _options.contract_requirements.value:
            self.override_num_option(
                _options.contract_goal_requirements,
                _options.contract_requirements.value,
                f"Contract {_goal_reason}"
            )
        if (
            _options.use_dlc and
            _options.dlc_ingredient_goal_requirements.value < _options.dlc_ingredient_requirements.value
        ):
            self.override_num_option(
                _options.dlc_ingredient_goal_requirements,
                _options.dlc_ingredient_requirements.value,
                f"Ingredient {_goal_reason}"
            )

    def _sanitize_level_placement(self):
        options = self.options
        lpvalue = options.level_placements.value

        if len(lpvalue) < 1:
            return

        valid_levels = {
            x
            for y in
                levelshuffle.get_level_shuffle_lists(
                    bool(options.use_dlc),
                    options.level_shuffle.evalue,
                    bool(options.level_shuffle_kingdice)
                )
            for x in y[0] if x not in y[1]
        }

        invalid_level_reason = "Invalid level"
        invalid_level_combo_reason = "Invalid level combination"

        nlpvalue: dict[str, str] = {}
        for k,v in lpvalue.items():
            drop = False
            drop_reason = ""
            if k not in valid_levels or v not in valid_levels:
                drop = True
                drop_reason = invalid_level_reason
            elif leveltype.get_level_type(k) != leveltype.get_level_type(v):
                drop = True
                drop_reason = invalid_level_combo_reason
            if drop:
                string = f"level_placements: '{k}: {v}' removed from dict. Reason: {drop_reason}."
                self.option_overrides.append(string)
                if self.log_overrides:
                    msg = f"Option 'level_placements' was overridden with '{k}: {v}' removed from dict."
                    msg_reason = f"Reason: {drop_reason}."
                    self.print_warning(f"{msg} {msg_reason}")
            else:
                nlpvalue[k] = v
        options.level_placements.value = nlpvalue

    def _is_minimal_accessibility(self) -> bool:
        accessibility = getattr(self.options, "accessibility", None)
        if accessibility is None:
            return False
        current_key = getattr(accessibility, "current_key", "")
        if isinstance(current_key, str) and current_key.lower() == "minimal":
            return True
        value = getattr(accessibility, "value", None)
        return isinstance(value, str) and value.lower() == "minimal"

    def _populate_accessibility_risks(self, risks_ref: list[str]):  # noqa: C901
        options = self.options

        if options.randomize_abilities.value:
            risks_ref.append("randomize_abilities")
        if options.weapon_mode.value != int(WeaponMode.NORMAL):
            risks_ref.append("weapon_mode != normal")
        if options.start_weapon.is_none():
            risks_ref.append("start_weapon = none")
        if options.boss_grade_checks.value > 0:
            risks_ref.append("boss_grade_checks")
        if options.rungun_grade_checks.value > 0:
            risks_ref.append("rungun_grade_checks")
        if options.silverworth_quest.value:
            risks_ref.append("silverworth_quest")
        if options.pacifist_quest.value:
            risks_ref.append("pacifist_quest")
        if options.dlc_boss_chalice_checks.value > 0:
            risks_ref.append("dlc_boss_chalice_checks")
        if options.dlc_rungun_chalice_checks.value > 0:
            risks_ref.append("dlc_rungun_chalice_checks")
        if options.dlc_kingdice_chalice_checks.value > 0:
            risks_ref.append("dlc_kingdice_chalice_checks")
        if options.dlc_chess_chalice_checks.value > 0:
            risks_ref.append("dlc_chess_chalice_checks")
        if options.dlc_cactusgirl_quest.value:
            risks_ref.append("dlc_cactusgirl_quest")

    def _warn_accessibility_risks(self):
        if not self._is_minimal_accessibility():
            return

        risks: list[str] = []

        self._populate_accessibility_risks(risks)

        if len(risks) < 1:
            return

        risk_str = format_list(risks, enc_start="'", enc_end="'")
        self.print_warning(
            "Accessibility is set to 'minimal' with high-risk options enabled "
            f"({risk_str}). This combination is known to increase generation failure chance."
        )

    def _warn_risks(self):
        options = self.options

        self._warn_accessibility_risks()

        if options.start_weapon.is_none() and options.logic_mode != LogicMode.HARD:
            self.print_warning("Currently, setting start_weapon to 'none' may fail unless Logic Mode is set to 'hard'.")
        if self.solo and options.start_weapon.is_none():
            self.print_warning(
                "Currently, single-player generation with start_weapon set to 'none' may fail because the first sphere "
                "can have too few valid early locations."
            )

    def sanitize_options(self):
        _options = self.options

        if self.strict_goal_options:
            self._sanitize_goal_requirements()

        if _options.weapon_mode.value == WeaponMode.EXCEPT_START:
            self.override_num_option(_options.weapon_mode, 0, "Unsupported option")

        if (
            _options.start_weapon.is_none() and
            (_options.weapon_mode.value & WeaponMode.EXCEPT_START) > 0
        ):
            self.override_num_option(
                _options.weapon_mode,
                _options.weapon_mode.value & ~WeaponMode.EXCEPT_START,
                "Start weapon set to 'none'"
            )

        self._sanitize_dlc_options()

        self._sanitize_level_placement()

        # Sanitize grade checks
        if not _options.expert_mode and _options.boss_grade_checks.value>3:
            self.override_num_option(_options.boss_grade_checks, 3, "Expert Off")

        self._warn_risks()
