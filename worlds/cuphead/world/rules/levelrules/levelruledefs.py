### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from rule_builder.rules import Filtered, Has

from ...names import itemnames as i
from ...names import locationnames as l
from ...names import regionnames as lv
from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbfieldresolvers import ContractReqsResolver, DlcIngredientReqsResolver
from ..rb.rbrules import Preset
from . import levelrulelrdefs as lrd
from . import levelrulepresets as lrp
from .levelrulebase import InheritMode, LevelDef, LevelRules, LocationDef

levelrules = LevelRules(
    {
        lv.level_boss_veggies: LevelDef(
            exit_location=l.loc_level_boss_veggies,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_boss_veggies: LocationDef(),
                l.loc_level_boss_veggies_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_veggies_secret: LocationDef(),
                l.loc_level_boss_veggies_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_veggies_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
                l.loc_level_boss_veggies_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_boss_slime: LevelDef(
            exit_location=l.loc_level_boss_slime,
            access=Preset(lrp.LrpWeapon),
            base=Preset(lrp.LrpCrouchOrDash),
            locations={
                l.loc_level_boss_slime: LocationDef(),
                l.loc_level_boss_slime_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_slime_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_slime_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_level_boss_slime_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
            },
        ),
        lv.level_boss_frogs: LevelDef(
            exit_location=l.loc_level_boss_frogs,
            access=Preset(lrp.LrpWeapon),
            base=Preset(lrp.LrpParryOrPSugar),
            locations={
                l.loc_level_boss_frogs: LocationDef(),
                l.loc_level_boss_frogs_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_frogs_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_frogs_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_level_boss_frogs_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
            },
        ),
        lv.level_boss_flower: LevelDef(
            exit_location=l.loc_level_boss_flower,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_boss_flower: LocationDef(),
                l.loc_level_boss_flower_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_flower_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_flower_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
                l.loc_level_boss_flower_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_boss_baroness: LevelDef(
            exit_location=l.loc_level_boss_baroness,
            access=Preset(lrp.LrpWeapon),
            base=Preset(lrp.LrpParryOrPSugar),
            locations={
                l.loc_level_boss_baroness: LocationDef(
                    rule=lrd.LrdBossBaronessChaliceOnly
                ),
                l.loc_level_boss_baroness_topgrade: LocationDef(
                    rule=(lrd.LrdBossBaronessChaliceOnly & Preset(lrp.LrpTopgrade))
                ),
                l.loc_level_boss_baroness_phase1: LocationDef(
                    rule=lrd.LrdBossBaronessChaliceOnly,
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_baroness_phase2: LocationDef(
                    rule=lrd.LrdBossBaronessChaliceOnly,
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_baroness_phase3: LocationDef(
                    rule=lrd.LrdBossBaronessChaliceOnly,
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_baroness_phase4: LocationDef(
                    rule=lrd.LrdBossBaronessChaliceOnly
                ),
                l.loc_level_boss_baroness_event_agrade: LocationDef(
                    rule=(lrd.LrdBossBaronessChaliceOnly & Preset(lrp.LrpTopgrade))
                ),
                l.loc_level_boss_baroness_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & lrd.LrdBossBaronessChalice),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_baroness_event_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & lrd.LrdBossBaronessChalice),
                    inherit=InheritMode.NONE
                ),
            },
        ),
        lv.level_boss_clown: LevelDef(
            exit_location=l.loc_level_boss_clown,
            access=Preset(lrp.LrpWeapon),
            base=Preset(lrp.LrpDashOrParry),
            locations={
                l.loc_level_boss_clown: LocationDef(),
                l.loc_level_boss_clown_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_clown_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_clown_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_level_boss_clown_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
            },
        ),
        lv.level_boss_dragon: LevelDef(
            exit_location=l.loc_level_boss_dragon,
            access=Preset(lrp.LrpWeapon),
            base=(
                Filtered(
                    Preset(lrp.LrpDash) | Preset(lrp.LrpDlcDoublejump),
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                    filtered_resolution=True
                )
            ),
            locations={
                l.loc_level_boss_dragon: LocationDef(),
                l.loc_level_boss_dragon_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_dragon_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_dragon_dlc_chaliced: LocationDef(
                    rule=lrd.LrdBossDragonChaliced,
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_boss_dragon_event_dlc_chaliced: LocationDef(
                    rule=lrd.LrdBossDragonChaliced,
                    inherit=InheritMode.NONE,
                ),
            },
        ),
        lv.level_boss_bee: LevelDef(
            exit_location=l.loc_level_boss_bee,
            access=Preset(lrp.LrpWeapon),
            base=(Preset(lrp.LrpDashOrDlcDoublejump) | DepFilter(deps.dep_hard_logic)),
            locations={
                l.loc_level_boss_bee: LocationDef(),
                l.loc_level_boss_bee_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_bee_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_bee_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
                l.loc_level_boss_bee_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_boss_pirate: LevelDef(
            exit_location=l.loc_level_boss_pirate,
            access=Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpCrouch) |
                (Preset(lrp.LrpDashAndParry) &
                    (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False)))
            ),
            locations={
                l.loc_level_boss_pirate: LocationDef(),
                l.loc_level_boss_pirate_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_pirate_phase1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_pirate_phase2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_pirate_phase3: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_pirate_phase4: LocationDef(),
                l.loc_level_boss_pirate_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_pirate_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & lrd.LrdBossPirateChalice),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_pirate_event_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & lrd.LrdBossPirateChalice),
                    inherit=InheritMode.NONE
                ),
            },
        ),
        lv.level_boss_mouse: LevelDef(
            exit_location=l.loc_level_boss_mouse,
            access=Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpCrouch) &
                ((Preset(lrp.LrpParry) & DepFilter(deps.dep_dlc_chalice_only)) |
                    (Preset(lrp.LrpParryOrPSugar) & DepFilter(deps.dep_dlc_chalice_only, False)))
            ),
            locations={
                l.loc_level_boss_mouse: LocationDef(
                    rule=(Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                ),
                l.loc_level_boss_mouse_topgrade: LocationDef(
                    rule=(
                        Preset(lrp.LrpTopgrade) &
                        (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                    )
                ),
                l.loc_level_boss_mouse_phase1: LocationDef(),
                l.loc_level_boss_mouse_phase2: LocationDef(
                    rule=(Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                ),
                l.loc_level_boss_mouse_phase3: LocationDef(),
                l.loc_level_boss_mouse_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_mouse_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & Preset(lrp.LrpDlcDoublejump))
                ),
                l.loc_level_boss_mouse_event_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & Preset(lrp.LrpDlcDoublejump))
                ),
            },
        ),
        lv.level_boss_sallystageplay: LevelDef(
            exit_location=l.loc_level_boss_sallystageplay,
            access=Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpParry) &
                Filtered(
                    Preset(lrp.LrpDlcDoublejump) | Preset(lrp.LrpCrouch),
                    options=[DepFilter(deps.dep_dlc_chalice_only)],
                    filtered_resolution=True
                )
            ),
            locations={
                l.loc_level_boss_sallystageplay: LocationDef(),
                l.loc_level_boss_sallystageplay_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_sallystageplay_phase1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_sallystageplay_phase1s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_phase2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_boss_sallystageplay_phase2s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_phase3: LocationDef(),
                l.loc_level_boss_sallystageplay_phase3s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_phase4: LocationDef(),
                l.loc_level_boss_sallystageplay_phase4s: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_secret: LocationDef(
                    rule=lrd.LrdBossSallyStagePlaySecret,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_sallystageplay_dlc_chaliced: LocationDef(
                    rule=(
                        Preset(lrp.LrpDlcBossChalicedParry) &
                        (Preset(lrp.LrpDlcDoublejump) | Preset(lrp.LrpCrouch))
                    ),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_boss_sallystageplay_event_dlc_chaliced: LocationDef(
                    rule=(
                        Preset(lrp.LrpDlcBossChalicedParry) &
                        (Preset(lrp.LrpDlcDoublejump) | Preset(lrp.LrpCrouch))
                    ),
                    inherit=InheritMode.NONE
                ),
            },
        ),
        lv.level_boss_train: LevelDef(
            exit_location=l.loc_level_boss_train,
            access=Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpParry) &
                Filtered(
                    Preset(lrp.LrpDlcDoublejump),
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                    filtered_resolution=True
                )
            ),
            locations={
                l.loc_level_boss_train: LocationDef(),
                l.loc_level_boss_train_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_train_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_train_dlc_chaliced: LocationDef(rule=(lrd.LrdBossTrainChaliced)),
                l.loc_level_boss_train_event_dlc_chaliced: LocationDef(rule=(lrd.LrdBossTrainChaliced)),
            },
        ),
        lv.level_boss_kingdice: LevelDef(
            exit_location=l.loc_level_boss_kingdice,
            access=(
                Has(i.item_contract, ContractReqsResolver()) &
                Preset(lrp.LrpWeapon) &
                Preset(lrp.LrpParryOrPSugar)
            ),
            base=(Preset(lrp.LrpPlane) & Preset(lrp.LrpDashAndParry)),
            locations={
                l.loc_level_boss_kingdice: LocationDef(),
                l.loc_level_boss_kingdice_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_kingdice_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_kingdice_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_level_boss_kingdice_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
            },
        ),
        lv.level_boss_plane_blimp: LevelDef(
            exit_location=l.loc_level_boss_plane_blimp,
            access=Preset(lrp.LrpPlane),
            locations={
                l.loc_level_boss_plane_blimp: LocationDef(),
                l.loc_level_boss_plane_blimp_topgrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_blimp_event_agrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_blimp_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
                l.loc_level_boss_plane_blimp_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
            },
        ),
        lv.level_boss_plane_genie: LevelDef(
            exit_location=l.loc_level_boss_plane_genie,
            access=Preset(lrp.LrpPlane),
            locations={
                l.loc_level_boss_plane_genie: LocationDef(),
                l.loc_level_boss_plane_genie_topgrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_genie_secret: LocationDef(rule=Preset(lrp.LrpPlaneShrink)),
                l.loc_level_boss_plane_genie_event_agrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_genie_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
                l.loc_level_boss_plane_genie_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
            },
        ),
        lv.level_boss_plane_bird: LevelDef(
            exit_location=l.loc_level_boss_plane_bird,
            access=Preset(lrp.LrpPlane),
            base=(Has(i.item_plane_bombs) | DepFilter(deps.dep_hard_logic)),
            locations={
                l.loc_level_boss_plane_bird: LocationDef(),
                l.loc_level_boss_plane_bird_topgrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_bird_event_agrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_bird_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
                l.loc_level_boss_plane_bird_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
            },
        ),
        lv.level_boss_plane_mermaid: LevelDef(
            exit_location=l.loc_level_boss_plane_mermaid,
            access=Preset(lrp.LrpPlane),
            locations={
                l.loc_level_boss_plane_mermaid: LocationDef(),
                l.loc_level_boss_plane_mermaid_topgrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_mermaid_event_agrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_mermaid_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
                l.loc_level_boss_plane_mermaid_event_dlc_chaliced: LocationDef(
                    rule=Preset(lrp.LrpDlcBossPlaneChaliced)
                ),
            },
        ),
        lv.level_boss_plane_robot: LevelDef(
            exit_location=l.loc_level_boss_plane_robot,
            access=(Preset(lrp.LrpPlane) & Preset(lrp.LrpPlaneParry)),
            locations={
                l.loc_level_boss_plane_robot: LocationDef(),
                l.loc_level_boss_plane_robot_topgrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_robot_event_agrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_boss_plane_robot_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
                l.loc_level_boss_plane_robot_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
            },
        ),
        lv.level_boss_devil: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            base=(
                Filtered(
                    Preset(lrp.LrpDlcDoublejump) | Preset(lrp.LrpDashAndParry),
                    options=[
                        DepFilter(deps.dep_dlc_chalice_not_separate),
                        DepFilter(deps.dep_hard_logic),
                    ],
                    filtered_resolution=True
                ) &
                Filtered(
                    Preset(lrp.LrpDashAndParry),
                    options=[
                        DepFilter(
                            (deps.dep_dlc_chalice_not_separate, deps.dep_hard_logic),
                            value=False,
                            any=True
                        ),
                    ],
                    filtered_resolution=True
                )
            ),
            locations={
                l.loc_level_boss_devil: LocationDef(),
                l.loc_level_boss_devil_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_devil_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_boss_devil_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_level_boss_devil_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_event_goal_devil: LocationDef(),
            },
        ),
        lv.level_dlc_boss_oldman: LevelDef(
            exit_location=l.loc_level_dlc_boss_oldman,
            access=Preset(lrp.LrpWeapon),
            base=(Preset(lrp.LrpDash) & Preset(lrp.LrpParryOrPSugar)),
            locations={
                l.loc_level_dlc_boss_oldman: LocationDef(),
                l.loc_level_dlc_boss_oldman_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_dlc_boss_oldman_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
                l.loc_level_dlc_boss_oldman_event_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChalicedParry)),
            },
        ),
        lv.level_dlc_boss_rumrunners: LevelDef(
            exit_location=l.loc_level_dlc_boss_rumrunners,
            access=Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpCrouchAndParry) &
                (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
            ),
            locations={
                l.loc_level_dlc_boss_rumrunners: LocationDef(),
                l.loc_level_dlc_boss_rumrunners_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_dlc_boss_rumrunners_phase1: LocationDef(
                    rule=lrd.LrdDlcBossRumRunnersEarlyPhase,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_dlc_boss_rumrunners_phase2: LocationDef(
                    rule=lrd.LrdDlcBossRumRunnersEarlyPhase,
                    inherit=InheritMode.NONE
                ),
                l.loc_level_dlc_boss_rumrunners_phase3: LocationDef(),
                l.loc_level_dlc_boss_rumrunners_phase4: LocationDef(),
                l.loc_level_dlc_boss_rumrunners_dlc_chaliced: LocationDef(
                    rule=lrd.LrdDlcBossRumRunnersChaliced
                ),
                l.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LocationDef(
                    rule=lrd.LrdDlcBossRumRunnersChaliced
                ),
            },
        ),
        lv.level_dlc_boss_snowcult: LevelDef(
            exit_location=l.loc_level_dlc_boss_snowcult,
            access=Preset(lrp.LrpWeapon),
            base=(
                Filtered(
                    Preset(
                        lrp.LrpDlcDoublejump,
                        options=[DepFilter(deps.dep_dlc_chalice_only)],
                    ) |
                    Filtered(
                        (Preset(lrp.LrpDlcDoublejump) | Preset(lrp.LrpDash)) |
                        DepFilter(deps.dep_expert_mode, False),
                        options=[DepFilter(deps.dep_dlc_chalice_only, False)]
                    ),
                    options=[DepFilter(deps.dep_hard_logic, False)],
                    filtered_resolution=True
                )
            ),
            locations={
                l.loc_level_dlc_boss_snowcult: LocationDef(),
                l.loc_level_dlc_boss_snowcult_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_dlc_boss_snowcult_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossSnowCultChaliced),
                l.loc_level_dlc_boss_snowcult_event_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossSnowCultChaliced),
            },
        ),
        lv.level_dlc_boss_airplane: LevelDef(
            exit_location=l.loc_level_dlc_boss_airplane,
            access=Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpCrouchOrDash, options=[DepFilter(deps.dep_dlc_chalice_only, False)]) |
                Filtered(
                    Preset(lrp.LrpCrouchOrDash, options=[DepFilter(deps.dep_hard_logic)]) |
                    Filtered(
                        Preset(lrp.LrpCrouch) | (Preset(lrp.LrpDash) & Preset(lrp.LrpDlcDoublejump)),
                        options=[DepFilter(deps.dep_hard_logic, False)]
                    ),
                    options=[DepFilter(deps.dep_dlc_chalice_only)],
                )
            ),
            locations={
                l.loc_level_dlc_boss_airplane: LocationDef(),
                l.loc_level_dlc_boss_airplane_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_dlc_boss_airplane_secret: LocationDef(),
                l.loc_level_dlc_boss_airplane_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossAirplaneChaliced),
                l.loc_level_dlc_boss_airplane_event_dlc_chaliced: LocationDef(rule=lrd.LrdDlcBossAirplaneChaliced),
            },
        ),
        lv.level_dlc_boss_plane_cowboy: LevelDef(
            exit_location=l.loc_level_dlc_boss_plane_cowboy,
            access=Preset(lrp.LrpPlane),
            locations={
                l.loc_level_dlc_boss_plane_cowboy: LocationDef(),
                l.loc_level_dlc_boss_plane_cowboy_topgrade: LocationDef(rule=Preset(lrp.LrpPlaneTopgrade)),
                l.loc_level_dlc_boss_plane_cowboy_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossPlaneChaliced)),
                l.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced: LocationDef(
                    rule=Preset(lrp.LrpDlcBossPlaneChaliced)
                ),
            },
        ),
        lv.level_dlc_boss_saltbaker: LevelDef(
            exit_location=None,
            access=Has(i.item_dlc_ingredient, DlcIngredientReqsResolver()) & Preset(lrp.LrpWeapon),
            base=(
                Preset(lrp.LrpParry) &
                (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
            ),
            locations={
                l.loc_level_dlc_boss_saltbaker: LocationDef(),
                l.loc_level_dlc_boss_saltbaker_topgrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_dlc_boss_saltbaker_phase1: LocationDef(
                    rule=(
                        Preset(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                            filtered_resolution=True
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_dlc_boss_saltbaker_phase2: LocationDef(
                    rule=(
                        Preset(lrp.LrpParry) &
                        Preset(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                            filtered_resolution=True
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_dlc_boss_saltbaker_phase3: LocationDef(
                    rule=(
                        Preset(lrp.LrpParry) &
                        Preset(
                            lrp.LrpDlcDoublejump,
                            options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                            filtered_resolution=True
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_dlc_boss_saltbaker_phase4: LocationDef(),
                l.loc_level_dlc_boss_saltbaker_event_agrade: LocationDef(rule=Preset(lrp.LrpTopgrade)),
                l.loc_level_dlc_boss_saltbaker_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & Preset(lrp.LrpDlcDoublejump)),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChalicedParry) & Preset(lrp.LrpDlcDoublejump)),
                    inherit=InheritMode.NONE
                ),
                l.loc_event_dlc_goal_saltbaker: LocationDef(),
            },
        ),
        lv.level_dicepalace_boss_booze: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_dicepalace_boss_booze: LocationDef(),
                l.loc_level_dicepalace_boss_booze_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_dicepalace_boss_chips: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_dicepalace_boss_chips: LocationDef(),
                l.loc_level_dicepalace_boss_chips_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_dicepalace_boss_cigar: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            base=Preset(lrp.LrpDash),
            locations={
                l.loc_level_dicepalace_boss_cigar: LocationDef(),
                l.loc_level_dicepalace_boss_cigar_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_dicepalace_boss_domino: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_dicepalace_boss_domino: LocationDef(),
                l.loc_level_dicepalace_boss_domino_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_dicepalace_boss_rabbit: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            base=Preset(lrp.LrpParry),
            locations={
                l.loc_level_dicepalace_boss_rabbit: LocationDef(
                    rule=(Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                ),
                l.loc_level_dicepalace_boss_rabbit_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcBossChaliced) & Preset(lrp.LrpDlcDoublejump))
                ),
            },
        ),
        lv.level_dicepalace_boss_plane_horse: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpPlane),
            locations={
                l.loc_level_dicepalace_boss_plane_horse: LocationDef(),
                l.loc_level_dicepalace_boss_plane_horse_dlc_chaliced: LocationDef(
                    rule=Preset(lrp.LrpDlcBossPlaneChaliced)
                ),
            },
        ),
        lv.level_dicepalace_boss_roulette: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_dicepalace_boss_roulette: LocationDef(),
                l.loc_level_dicepalace_boss_roulette_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_dicepalace_boss_eightball: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon),
            locations={
                l.loc_level_dicepalace_boss_eightball: LocationDef(),
                l.loc_level_dicepalace_boss_eightball_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcBossChaliced)),
            },
        ),
        lv.level_dicepalace_boss_plane_memory: LevelDef(
            exit_location=None,
            access=(Preset(lrp.LrpPlane) & Preset(lrp.LrpPlaneParry)),
            locations={
                l.loc_level_dicepalace_boss_plane_memory: LocationDef(),
                l.loc_level_dicepalace_boss_plane_memory_dlc_chaliced: LocationDef(
                    rule=Preset(lrp.LrpDlcBossPlaneChaliced)
                ),
            },
        ),
        lv.level_rungun_forest: LevelDef(
            exit_location=l.loc_level_rungun_forest,
            base=Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpDash),
            locations={
                l.loc_level_rungun_forest: LocationDef(),
                l.loc_level_rungun_forest_agrade: LocationDef(rule=Preset(lrp.LrpRungunTopgrade)),
                l.loc_level_rungun_forest_pacifist: LocationDef(),
                l.loc_level_rungun_forest_coin1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin3: LocationDef(
                    rule=Preset(lrp.LrpParryOrPSugar),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_forest_coin4: LocationDef(rule=Preset(lrp.LrpDash), inherit=InheritMode.NONE),
                l.loc_level_rungun_forest_coin5: LocationDef(
                    rule=Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpDash),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_forest_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcRungunChaliced)),
                l.loc_level_rungun_forest_event_agrade: LocationDef(rule=Preset(lrp.LrpRungunTopgrade)),
                l.loc_level_rungun_forest_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_tree: LevelDef(
            exit_location=l.loc_level_rungun_tree,
            base=(
                Preset(lrp.LrpDash) &
                (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
            ),
            locations={
                l.loc_level_rungun_tree: LocationDef(rule=Preset(lrp.LrpRungunWeapon)),
                l.loc_level_rungun_tree_agrade: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpRungunTopgrade))
                ),
                l.loc_level_rungun_tree_pacifist: LocationDef(),
                l.loc_level_rungun_tree_coin1: LocationDef(rule=Preset(lrp.LrpParryOrPSugar), inherit=InheritMode.NONE),
                l.loc_level_rungun_tree_coin2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_tree_coin3: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_tree_coin4: LocationDef(),
                l.loc_level_rungun_tree_coin5: LocationDef(),
                l.loc_level_rungun_tree_dlc_chaliced: LocationDef(
                    rule=(
                        Preset(lrp.LrpRungunWeapon) &
                        Preset(lrp.LrpDlcRungunChaliced) &
                        (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only))
                    )
                ),
                l.loc_level_rungun_tree_event_agrade: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpRungunTopgrade))
                ),
                l.loc_level_rungun_tree_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_circus: LevelDef(
            exit_location=l.loc_level_rungun_circus,
            base=(
                Preset(lrp.LrpRungunWeapon) &
                (Preset(lrp.LrpParryOrPSugar) | Preset(lrp.LrpDlcDoublejump)) &
                (Preset(lrp.LrpDash) | DepFilter(deps.dep_hard_logic)) &
                Filtered(
                    Preset(lrp.LrpDlcDoublejump),
                    options=[DepFilter(deps.dep_dlc_chalice_only), DepFilter(deps.dep_hard_logic, False)],
                    filtered_resolution=True
                )
            ),
            locations={
                l.loc_level_rungun_circus: LocationDef(),
                l.loc_level_rungun_circus_agrade: LocationDef(),
                l.loc_level_rungun_circus_pacifist: LocationDef(),
                l.loc_level_rungun_circus_coin1: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_circus_coin2: LocationDef(inherit=InheritMode.NONE),
                l.loc_level_rungun_circus_coin3: LocationDef(),
                l.loc_level_rungun_circus_coin4: LocationDef(),
                l.loc_level_rungun_circus_coin5: LocationDef(),
                l.loc_level_rungun_circus_dlc_chaliced: LocationDef(
                    rule=(
                        Preset(lrp.LrpDlcRungunChaliced) &
                        Preset(lrp.LrpDashAndParry) &
                        Filtered(
                            Preset(lrp.LrpDlcDoublejump),
                            options=[
                                DepFilter(deps.dep_dlc_chalice_only, False),
                                DepFilter(deps.dep_hard_logic, False)
                            ],
                            filtered_resolution=True
                        )
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_rungun_circus_event_agrade: LocationDef(),
                l.loc_level_rungun_circus_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_funhouse: LevelDef(
            exit_location=l.loc_level_rungun_funhouse,
            base=(
                Preset(lrp.LrpRungunWeapon) &
                (
                    Preset(lrp.LrpParry) |
                    Filtered(
                        Has(i.item_charm_psugar) & Preset(lrp.LrpDash),
                        options=[DepFilter(deps.dep_dlc_chalice_only, False)],
                    )
                )
            ),
            locations={
                l.loc_level_rungun_funhouse: LocationDef(),
                l.loc_level_rungun_funhouse_agrade: LocationDef(),
                l.loc_level_rungun_funhouse_pacifist: LocationDef(),
                l.loc_level_rungun_funhouse_coin1: LocationDef(
                    rule=Preset(lrp.LrpParryOrPSugar),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin2: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpParryOrPSugar)),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin3: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpParryOrPSugar)),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin4: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpParryOrPSugar)),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_funhouse_coin5: LocationDef(),
                l.loc_level_rungun_funhouse_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcRungunChaliced)),
                l.loc_level_rungun_funhouse_event_agrade: LocationDef(rule=Preset(lrp.LrpRungunTopgrade)),
                l.loc_level_rungun_funhouse_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_harbour: LevelDef(
            exit_location=l.loc_level_rungun_harbour,
            base=(
                Preset(lrp.LrpRungunWeapon) &
                Preset(lrp.LrpDash) &
                (Preset(lrp.LrpParry) | DepFilter(deps.dep_hard_logic)) &
                (Preset(lrp.LrpParryOrPSugar) | DepFilter(deps.dep_hard_logic, False)) &
                (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
            ),
            locations={
                l.loc_level_rungun_harbour: LocationDef(),
                l.loc_level_rungun_harbour_agrade: LocationDef(),
                l.loc_level_rungun_harbour_pacifist: LocationDef(),
                l.loc_level_rungun_harbour_coin1: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpDashParryOrPSugar)),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_harbour_coin2: LocationDef(
                    rule=Preset(lrp.LrpRungunWeapon),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_harbour_coin3: LocationDef(
                    rule=(Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpParryOrPSugar)),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_harbour_coin4: LocationDef(
                    rule=(
                        Preset(lrp.LrpRungunWeapon) & (
                            Preset(lrp.LrpParry) |
                            Filtered(
                                Has(i.item_charm_psugar) & Preset(lrp.LrpDash),
                                options=[DepFilter(deps.dep_hard_logic)]
                            )
                        ) &
                        (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                    ),
                    inherit=InheritMode.NONE,
                ),
                l.loc_level_rungun_harbour_coin5: LocationDef(),
                l.loc_level_rungun_harbour_dlc_chaliced: LocationDef(
                    rule=(
                        Preset(lrp.LrpDlcRungunChaliced) &
                        (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only))
                    )
                ),
                l.loc_level_rungun_harbour_event_agrade: LocationDef(rule=Preset(lrp.LrpRungunTopgrade)),
                l.loc_level_rungun_harbour_event_pacifist: LocationDef(),
            },
        ),
        lv.level_rungun_mountain: LevelDef(
            exit_location=l.loc_level_rungun_mountain,
            base=(
                Preset(lrp.LrpRungunWeapon) &
                (
                    Preset(lrp.LrpDash) |
                    (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice, False))
                )
            ),
            locations={
                l.loc_level_rungun_mountain: LocationDef(),
                l.loc_level_rungun_mountain_agrade: LocationDef(rule=Preset(lrp.LrpRungunTopgrade)),
                l.loc_level_rungun_mountain_pacifist: LocationDef(),
                l.loc_level_rungun_mountain_coin1: LocationDef(
                    rule=Preset(lrp.LrpRungunWeapon),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_coin2: LocationDef(
                    rule=Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpDashOrDlcDoublejump),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_coin3: LocationDef(
                    rule=Preset(lrp.LrpRungunWeapon),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_coin4: LocationDef(
                    rule=(
                        Preset(lrp.LrpRungunWeapon) &
                        (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                    ),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_coin5: LocationDef(
                    rule=Preset(lrp.LrpRungunWeapon) & Preset(lrp.LrpDashOrDlcDoublejump),
                    inherit=InheritMode.NONE
                ),
                l.loc_level_rungun_mountain_dlc_chaliced: LocationDef(rule=Preset(lrp.LrpDlcRungunChaliced)),
                l.loc_level_rungun_mountain_event_agrade: LocationDef(rule=Preset(lrp.LrpRungunTopgrade)),
                l.loc_level_rungun_mountain_event_pacifist: LocationDef(),
            },
        ),
        lv.level_mausoleum_i: LevelDef(exit_location=None, access=Preset(lrp.LrpParryOrPSugar), locations={}),
        lv.level_mausoleum_ii: LevelDef(exit_location=None, access=lrd.LrdParryLogic, locations={}),
        lv.level_mausoleum_iii: LevelDef(exit_location=None, access=lrd.LrdParryLogic, locations={}),
        lv.level_dlc_chesscastle_pawn: LevelDef(
            exit_location=None,
            access=lrd.LrdParryLogic,
            locations={
                l.loc_level_dlc_chesscastle_pawn: LocationDef(),
                l.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LocationDef(rule=lrd.LrdDlcChessCastleChaliced),
            },
        ),
        lv.level_dlc_chesscastle_knight: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpParry),
            locations={
                l.loc_level_dlc_chesscastle_knight: LocationDef(
                    rule=(Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
                ),
                l.loc_level_dlc_chesscastle_knight_dlc_chaliced: LocationDef(
                    rule=(Preset(lrp.LrpDlcDoublejump) & lrd.LrdDlcChessCastleChaliced)
                ),
            },
        ),
        lv.level_dlc_chesscastle_bishop: LevelDef(
            exit_location=None,
            access=lrd.LrdParryLogic,
            locations={
                l.loc_level_dlc_chesscastle_bishop: LocationDef(),
                l.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LocationDef(rule=lrd.LrdDlcChessCastleChaliced),
            },
        ),
        lv.level_dlc_chesscastle_rook: LevelDef(
            exit_location=None,
            access=lrd.LrdParryLogic,
            locations={
                l.loc_level_dlc_chesscastle_rook: LocationDef(),
                l.loc_level_dlc_chesscastle_rook_dlc_chaliced: LocationDef(rule=lrd.LrdDlcChessCastleChaliced),
            },
        ),
        lv.level_dlc_chesscastle_queen: LevelDef(
            exit_location=None,
            access=lrd.LrdParryLogic,
            locations={
                l.loc_level_dlc_chesscastle_queen: LocationDef(),
                l.loc_level_dlc_chesscastle_queen_dlc_chaliced: LocationDef(rule=lrd.LrdDlcChessCastleChaliced),
            },
        ),
        lv.level_dlc_chesscastle_run: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpParry),
            locations={
                l.loc_level_dlc_chesscastle_run: LocationDef(),
                l.loc_level_dlc_chesscastle_run_dlc_chaliced: LocationDef(rule=lrd.LrdDlcChessCastleChaliced),
            },
        ),
        lv.level_tutorial: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon) & Preset(lrp.LrpCrouchDashAndParry),
            locations={}
        ),
        lv.level_dlc_tutorial: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpDlcCookie),
            locations={
                l.loc_level_dlc_tutorial_coin: LocationDef(
                    rule=Preset(lrp.LrpDashAndParry) & Preset(lrp.LrpDlcDoublejump)
                )
            },
        ),
        lv.level_dlc_graveyard: LevelDef(
            exit_location=None,
            access=Preset(lrp.LrpWeapon) & Has(i.item_charm_dlc_broken_relic),
            locations={
                l.loc_level_dlc_graveyard: LocationDef(rule=Preset(lrp.LrpDashAndParry) & Preset(lrp.LrpDlcDoublejump))
            },
        ),
    }
)
