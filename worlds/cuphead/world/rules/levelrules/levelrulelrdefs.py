### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from rule_builder.rules import Filtered

from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbrules import Preset
from . import levelrulepresets as lrp

LrdBossBaronessChalice = (
    Preset(lrp.LrpDlcDoublejump) #&
    ## Maybe need duck?
    #(Preset(lrp.LrpCrouch) | DepFilter(deps.dep_hard_logic))
)

LrdBossBaronessChaliceOnly = (
    LrdBossBaronessChalice |
    DepFilter(deps.dep_dlc_chalice_only, False)
)

LrdBossDragonChaliced = (
    Preset(lrp.LrpDlcBossChaliced) &
    Filtered(
        Preset(lrp.LrpDash) | Preset(lrp.LrpDlcDoublejump),
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    )
)

LrdBossPirateChalice = (
    (Preset(lrp.LrpCrouch) | (Preset(lrp.LrpDashAndParry) & Preset(lrp.LrpDlcDoublejump))) |
    DepFilter(deps.dep_rando_abilities, False)
)

LrdBossSallyStagePlaySecret = (
    Preset(lrp.LrpParry) &
    (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
)

LrdBossTrainChaliced = (
    Preset(lrp.LrpDlcBossChalicedParry) &
    Filtered(
        Preset(lrp.LrpDlcDoublejump),
        options=[DepFilter(deps.dep_dlc_chalice_only, False), DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    )
)

LrdParryLogic = (
    (Preset(lrp.LrpParryOrPSugar) & DepFilter(deps.dep_hard_logic)) |
    (Preset(lrp.LrpParry) & DepFilter(deps.dep_hard_logic, False))
)

LrdDlcBossRumRunnersEarlyPhase = (
    Preset(lrp.LrpCrouch) &
    (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only, False))
)

LrdDlcBossRumRunnersChaliced = (
    Preset(lrp.LrpDlcBossChalicedParry) &
    (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_dlc_chalice_only))
)

LrdDlcBossSnowCultChaliced = (
    Preset(lrp.LrpDlcBossChaliced) &
    (Preset(lrp.LrpDlcDoublejump) | DepFilter(deps.dep_hard_logic))
)

LrdDlcBossAirplaneChaliced = (
    Preset(lrp.LrpDlcCookie) &
    Filtered(
        Preset(lrp.LrpCrouchOrDash) &
        (Preset(lrp.LrpCrouch) | (Preset(lrp.LrpDash) & Preset(lrp.LrpDlcDoublejump))),
        options=[DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    )
)

LrdDlcChessCastleChaliced = (
    Preset(lrp.LrpDash) | DepFilter(deps.dep_dlc_chalice_only)
)
