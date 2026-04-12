from __future__ import annotations
from random import Random
from collections.abc import Iterable
from ..auxiliary import format_list
from ..enums import ChaliceMode, ChaliceCheckMode, LevelShuffleMode, WeaponMode
from ..levels import levelshuffle, leveltype
from .protocols import CupheadNumericOption, CupheadOptionSet
from . import CupheadOptions

class OptionSanitizer:
    option_overrides: list[str] = []

    def __init__(
            self, player: int,
            options: CupheadOptions,
            random: Random,
            log_overrides: bool = True,
            sanitize_goal_options: bool = False
        ):
        self.option_overrides = []
        self.player = player
        self.options = options
        self.random = random
        self.log_overrides = log_overrides
        self.strict_goal_options = sanitize_goal_options

    def override_num_option(
            self,
            option: CupheadNumericOption,
            value: int,
            reason: str | None = None,
            quiet: bool = False
        ):
        _old_value_key = option.current_key
        option.value = value
        string = f"{option.name}: \"{_old_value_key}\" -> \"{option.current_key}\"."
        if reason:
            string += f" Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option \"{option.name}\" was overridden from \"{_old_value_key}\" to \"{option.current_key}\"."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")

    def override_option_set(
            self,
            option: CupheadOptionSet,
            values: Iterable[str],
            add_mode: bool = False,
            reason: str | None = None,
            quiet: bool = False
        ):
        values_str = format_list(values, enc_start="\"", enc_end="\"")
        mode_str = "added to" if add_mode else "removed from"
        string = f"{option.name}: \"{values_str}\" {mode_str} set."
        if reason:
            string += f" Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option \"{option.name}\" was overridden with \"{values_str}\" {mode_str} set."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")
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
            msg = f"Option \"{option.name}\" was overridden with set cleared."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")
        option.value.clear()

    def _sanitize_dlc_chalice_item_options(self, quiet: bool = False) -> None:
        _options = self.options
        ABILITIES_VAL = "abilities"
        if len(_options.dlc_chalice_items_separate.value) > 0:
            if ABILITIES_VAL in _options.dlc_chalice_items_separate.value and not _options.randomize_abilities:
                self.override_option_set(
                    _options.dlc_chalice_items_separate,
                    {ABILITIES_VAL},
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

    def _sanitize_dlc_chalice_checks(self, quiet: bool = False) -> None:
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

    def _sanitize_dlc_chalice_options(self, quiet: bool = False) -> None:
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

    def _sanitize_dlc_options(self) -> None:
        _options = self.options
        use_dlc = _options.use_dlc.value
        if not use_dlc:
            DLC_REASON = "DLC Off"
            # Sanitize mode
            if _options.mode.value > 4:
                # TODO: Once modes can be combined, remove this and use randint
                _MODE_CHOICES = [1, 2, 4]
                self.override_num_option(_options.mode, self.random.choice(_MODE_CHOICES), DLC_REASON)
            # Sanitize start_weapon
            if _options.start_weapon.value > 5:
                self.override_num_option(_options.start_weapon, self.random.randint(0,5), DLC_REASON)
        self._sanitize_dlc_chalice_options(not use_dlc)

    def _sanitize_goal_requirements(self) -> None:
        _options = self.options

        _GOAL_REASON = "Goal cannot be less than requirements"

        # Sanitize settings
        if _options.contract_goal_requirements.value < _options.contract_requirements.value:
            self.override_num_option(
                _options.contract_goal_requirements,
                _options.contract_requirements.value,
                f"Contract {_GOAL_REASON}"
            )
        if (_options.use_dlc and \
            _options.dlc_ingredient_goal_requirements.value < _options.dlc_ingredient_requirements.value):
            self.override_num_option(
                _options.dlc_ingredient_goal_requirements,
                _options.dlc_ingredient_requirements.value,
                f"Ingredient {_GOAL_REASON}"
            )

    def _sanitize_level_placement(self) -> None:
        options = self.options
        lpvalue = options.level_placements.value

        if len(lpvalue) < 1:
            return

        valid_levels = {
            x
            for y in
                levelshuffle.get_level_shuffle_lists(
                    bool(options.use_dlc),
                    LevelShuffleMode(options.mode),
                    bool(options.level_shuffle_kingdice)
                )
            for x in y[0] if x not in y[1]
        }

        INVALID_LEVEL_REASON = "Invalid level"
        INVALID_LEVEL_COMBO_REASON = "Invalid level combination"

        nlpvalue: dict[str, str] = {}
        for k,v in lpvalue.items():
            drop = False
            drop_reason = ""
            if k not in valid_levels or v not in valid_levels:
                drop = True
                drop_reason = INVALID_LEVEL_REASON
            elif leveltype.get_level_type(k) != leveltype.get_level_type(v):
                drop = True
                drop_reason = INVALID_LEVEL_COMBO_REASON
            if drop:
                string = f"level_placements: \"{k}: {v}\" removed from dict. Reason: {drop_reason}."
                self.option_overrides.append(string)
                if self.log_overrides:
                    msg = f"Option \"level_placements\" was overridden with \"{k}: {v}\" removed from dict."
                    msg_reason = f"Reason: {drop_reason}."
                    print(f"Warning: For player {self.player}: {msg} {msg_reason}")
            else:
                nlpvalue[k] = v
        options.level_placements.value = nlpvalue

    def sanitize_options(self) -> None:
        _options = self.options

        if self.strict_goal_options:
            self._sanitize_goal_requirements()

        if _options.weapon_mode.value == WeaponMode.EXCEPT_START:
            self.override_num_option(_options.weapon_mode, 0, "Unsupported option")

        self._sanitize_dlc_options()

        self._sanitize_level_placement()

        # Sanitize grade checks
        if not _options.expert_mode and _options.boss_grade_checks.value>3:
            self.override_num_option(_options.boss_grade_checks, 3, "Expert Off")
