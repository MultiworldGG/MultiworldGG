from __future__ import annotations
from .names import ItemNames, LocationNames
from .options import CupheadOptions, options as odefs
from . import enums as e

# These are settings stored and accessed by other classes
class WorldConfig:
    use_dlc: bool
    mode: e.GameMode
    hard_logic: bool
    expert_mode: bool
    start_weapon: int
    weapon_mode: e.WeaponMode
    level_shuffle: e.LevelShuffleMode
    level_shuffle_kingdice: bool
    level_shuffle_seed: str
    level_placements: dict[str, str]
    freemove_isles: bool
    shop_mode: e.ShopMode
    weapon_gate: bool
    randomize_abilities: bool
    randomize_abilities_aim: bool
    maxhealth_upgrades: int
    traps: int
    filler_item_weights: list[tuple[str, int]]
    trap_item_weights: list[tuple[str, int]]
    boss_grade_checks: e.GradeCheckMode
    rungun_grade_checks: e.GradeCheckMode
    boss_secret_checks: bool
    kingdice_bosssanity: bool
    dlc_boss_chalice_checks: e.ChaliceCheckMode
    dlc_rungun_chalice_checks: e.ChaliceCheckMode
    dlc_kingdice_chalice_checks: e.ChaliceCheckMode
    dlc_chess_chalice_checks: e.ChaliceCheckMode
    buster_quest: bool
    ginger_quest: bool
    fourmel_quest: bool
    lucien_quest: bool
    silverworth_quest: bool
    pacifist_quest: bool
    dlc_chalice: e.ChaliceMode
    music_quest: bool
    dlc_kingsleap: e.ChessCastleMode
    dlc_cactusgirl_quest: bool
    coin_amounts: tuple[int, int, int]
    contract_requirements: tuple[int, int, int]
    dlc_ingredient_requirements: int
    contract_goal_requirements: int
    dlc_ingredient_goal_requirements: int
    require_secret_shortcuts: bool
    dlc_randomize_boat: bool
    dlc_requires_mausoleum: bool
    dlc_chalice_items_separate: e.ItemGroups
    dlc_curse_mode: e.CurseMode
    minimum_filler: int
    trap_loadout_anyweapon: bool

    def _setup(self, options: CupheadOptions) -> None:
        self.use_dlc = bool(options.use_dlc.value)
        self.mode = e.GameMode(options.mode.value)
        self.hard_logic = False #bool(options.hard_logic.value)
        self.expert_mode = bool(options.expert_mode.value)
        self.start_weapon = int(options.start_weapon.value)
        self.weapon_mode = e.WeaponMode(options.weapon_mode.value)
        self.level_shuffle = e.LevelShuffleMode(options.level_shuffle.value)
        self.level_shuffle_kingdice = bool(options.level_shuffle_kingdice)
        self.level_shuffle_seed = options.level_shuffle_seed.value
        self.level_placements = options.level_placements.value
        self.freemove_isles = bool(options.freemove_isles.value)
        self.shop_mode = e.ShopMode.TIERS #e.ShopMode(options.shop_mode.value)
        self.weapon_gate = False #bool(options.weapon_gate.value)
        self.randomize_abilities = bool(options.randomize_abilities.value)
        self.randomize_abilities_aim = False #bool(options.randomize_abilities_aim.value)
        self.boss_grade_checks = e.GradeCheckMode(options.boss_grade_checks.value)
        self.rungun_grade_checks = e.GradeCheckMode(options.rungun_grade_checks.value)
        self.boss_secret_checks = bool(options.boss_secret_checks.value)
        self.kingdice_bosssanity = bool(options.kingdice_bosssanity.value)
        self.dlc_boss_chalice_checks = e.ChaliceCheckMode(options.dlc_boss_chalice_checks.value)
        self.dlc_rungun_chalice_checks = e.ChaliceCheckMode(options.dlc_rungun_chalice_checks.value)
        self.dlc_kingdice_chalice_checks = e.ChaliceCheckMode(options.dlc_kingdice_chalice_checks.value)
        self.dlc_chess_chalice_checks = e.ChaliceCheckMode(options.dlc_chess_chalice_checks.value)
        self.buster_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = False
        self.silverworth_quest = bool(options.silverworth_quest.value)
        self.pacifist_quest = bool(options.pacifist_quest.value)
        self.music_quest = False
        self.dlc_chalice = e.ChaliceMode(options.dlc_chalice.value)
        self.dlc_kingsleap = e.ChessCastleMode(options.dlc_kingsleap.value)
        self.dlc_cactusgirl_quest = bool(options.dlc_cactusgirl_quest.value)
        self.maxhealth_upgrades = options.maxhealth_upgrades.value
        self.traps = options.traps.value
        self.trap_item_weights = self._get_trap_item_weights(options)
        self.filler_item_weights = self._get_filler_item_weights(options)
        self.coin_amounts = self._get_coin_amounts(options)
        self.contract_requirements = self._get_contract_requirements(options)
        self.dlc_ingredient_requirements = options.dlc_ingredient_requirements.value
        self.contract_goal_requirements = options.contract_goal_requirements.value
        self.dlc_ingredient_goal_requirements = options.dlc_ingredient_goal_requirements.value
        self.require_secret_shortcuts = True
        self.dlc_randomize_boat = True
        self.dlc_requires_mausoleum = True
        self.dlc_chalice_items_separate = self._get_separate_items_mode(options)
        self.dlc_curse_mode = e.CurseMode.VANILLA
        self.minimum_filler = options.minimum_filler.value
        self.trap_loadout_anyweapon = bool(options.trap_loadout_anyweapon.value)

    def _setup_default(self) -> None:
        self.use_dlc = bool(odefs.DeliciousLastCourse.default)
        self.mode = e.GameMode(odefs.GameMode.default)
        self.hard_logic = False #bool(odefs.HardLogic.default)
        self.expert_mode = bool(odefs.ExpertMode.default)
        self.start_weapon = 0
        self.weapon_mode = e.WeaponMode(odefs.WeaponMode.default)
        self.level_shuffle = e.LevelShuffleMode(odefs.LevelShuffle.default)
        self.level_shuffle_kingdice = bool(odefs.LevelShuffleDicePalace.default)
        self.level_shuffle_seed = "0"
        self.level_placements = odefs.LevelPlacements.default
        self.freemove_isles = bool(odefs.FreeMoveIsles.default)
        self.shop_mode = e.ShopMode.TIERS #e.ShopMode(options.shop_mode.value)
        self.weapon_gate = False #bool(odefs.WeaponGate.default)
        self.randomize_abilities = bool(odefs.RandomizeAbilities.default)
        self.randomize_abilities_aim = False #bool(odefs.RandomizeAimAbilities.default)
        self.boss_grade_checks = e.GradeCheckMode(odefs.BossGradeChecks.default)
        self.rungun_grade_checks = e.GradeCheckMode(odefs.RunGunGradeChecks.default)
        self.boss_secret_checks = bool(odefs.BossSecretChecks.default)
        self.kingdice_bosssanity = bool(odefs.DicePalaceBossSanity.default)
        self.dlc_boss_chalice_checks = e.ChaliceCheckMode(odefs.DlcBossChaliceChecks.default)
        self.dlc_rungun_chalice_checks = e.ChaliceCheckMode(odefs.DlcRunGunChaliceChecks.default)
        self.dlc_kingdice_chalice_checks = e.ChaliceCheckMode(odefs.DlcDicePalaceChaliceChecks.default)
        self.dlc_chess_chalice_checks = e.ChaliceCheckMode(odefs.DlcChessChaliceChecks.default)
        self.buster_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = False
        self.silverworth_quest = bool(odefs.SilverworthQuest.default)
        self.pacifist_quest = bool(odefs.PacifistQuest.default)
        self.music_quest = False
        self.dlc_chalice = e.ChaliceMode(odefs.DlcChaliceMode.default)
        self.dlc_kingsleap = e.ChessCastleMode(odefs.DlcChessCastle.default)
        self.dlc_cactusgirl_quest = bool(odefs.DlcCactusGirlQuest.default)
        self.maxhealth_upgrades = odefs.MaxHealthUpgrades.default
        self.traps = odefs.Traps.default
        self.trap_item_weights = self._get_trap_item_weights(None)
        self.filler_item_weights = self._get_filler_item_weights(None)
        self.coin_amounts = self._get_coin_amounts(None)
        self.contract_requirements = self._get_contract_requirements(None)
        self.dlc_ingredient_requirements = odefs.DlcIngredientRequirements.default
        self.contract_goal_requirements = odefs.ContractGoalRequirements.default
        self.dlc_ingredient_goal_requirements = odefs.DlcIngredientGoalRequirements.default
        self.require_secret_shortcuts = True
        self.dlc_randomize_boat = True
        self.dlc_requires_mausoleum = True
        self.dlc_chalice_items_separate = self._get_separate_items_mode(None)
        self.dlc_curse_mode = e.CurseMode.VANILLA
        self.minimum_filler = odefs.MinimumFillerItems.default
        self.trap_loadout_anyweapon = bool(odefs.TrapLoadoutAnyWeapon.default)

    def __init__(self, options: CupheadOptions | None = None) -> None:
        if options:
            self._setup(options)
        else:
            self._setup_default()

    def _get_coin_amounts(self, options: CupheadOptions | None) -> tuple[int, int, int]:
        extra_coins = options.extra_coins.value if options else odefs.ExtraCoins.default
        total_single_coins = (40 if self.use_dlc else 37) + extra_coins
        total_double_coins = 5 if self.use_dlc else 0
        total_triple_coins = 2 if self.use_dlc else 1

        return (total_single_coins, total_double_coins, total_triple_coins)

    def _get_contract_requirements(self, options: CupheadOptions | None) -> tuple[int, int, int]:
        max_contracts = (5, 10, 17)
        total_req = options.contract_requirements.value if options else odefs.ContractRequirements.default
        die1 = min(total_req // 3, max_contracts[0])
        die2 = min((die1 + total_req) // 2, max_contracts[1])

        return (die1, die2, total_req)

    def _get_filler_item_weights(self, options: CupheadOptions | None) -> list[tuple[str, int]]:
        filler_items: list[str] = [
            ItemNames.item_level_extrahealth,
            ItemNames.item_level_supercharge,
            ItemNames.item_level_fastfire,
        ]
        filler_item_weights: list[int] = [
            options.filler_weight_extrahealth.value,
            options.filler_weight_supercharge.value,
            options.filler_weight_fastfire.value,
        ] if options else [
            odefs.FillerWeightExtraHealth.default,
            odefs.FillerWeightSuperRecharge.default,
            odefs.FillerWeightFastFire.default,
        ]
        return [
            (item, weight) for item, weight in zip(filler_items, filler_item_weights, strict=True) if weight > 0
        ]

    def _get_trap_item_weights(self, options: CupheadOptions | None) -> list[tuple[str, int]]:
        trap_items: list[str] = [
            ItemNames.item_level_trap_fingerjam,
            ItemNames.item_level_trap_slowfire,
            ItemNames.item_level_trap_superdrain,
            ItemNames.item_level_trap_loadout,
            ItemNames.item_level_trap_screen,
        ]
        trap_item_weights: list[int] = [
            options.trap_weight_fingerjam.value,
            options.trap_weight_slowfire.value,
            options.trap_weight_superdrain.value,
            options.trap_weight_loadout.value,
            0,
        ] if options else [
            odefs.TrapWeightFingerJam.default,
            odefs.TrapWeightSlowFire.default,
            odefs.TrapWeightSuperDrain.default,
            odefs.TrapWeightLoadout.default,
            0,
        ]
        return [
            (trap, weight) for trap, weight in zip(trap_items, trap_item_weights, strict=True) if weight > 0
        ]

    def _get_separate_items_mode(self, options: CupheadOptions | None) -> e.ItemGroups:
        _set = (
            options.dlc_chalice_items_separate.value if options else odefs.DlcChaliceItemsSeparate.default
        )
        _val = e.ItemGroups.NONE

        def _get_bit(opt: str, item_group: e.ItemGroups) -> int:
            return item_group if opt in _set else e.ItemGroups.NONE

        _val |= _get_bit("core_items", e.ItemGroups.CORE_ITEMS)
        _val |= _get_bit("weapon_ex", e.ItemGroups.WEAPON_EX)
        _val |= _get_bit("abilities", e.ItemGroups.ABILITIES)

        return e.ItemGroups.NONE

    def is_dlc_chalice_items_separate(self, item_group: e.ItemGroups) -> bool:
        return (self.dlc_chalice_items_separate & item_group) > 0

    def is_goal_used(self, goal: str) -> bool:
        if goal == LocationNames.loc_event_goal_devil:
            return (
                self.mode == e.GameMode.BEAT_DEVIL or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_DEVIL_NO_ISLE4
            )
        elif goal == LocationNames.loc_event_dlc_goal_saltbaker:
            return (
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY
            )
        return False
