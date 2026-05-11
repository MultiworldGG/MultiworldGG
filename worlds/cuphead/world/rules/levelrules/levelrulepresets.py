### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from rule_builder.rules import Filtered, Has, HasAll, HasAny, HasGroup

from ...names import itemnames as i
from ..dep import deps
from ..dep.depfilter import DepFilter
from ..rb.rbbase import PresetData
from ..rb.rbrules import HasAnyWeapon, HasAnyWeaponEx, Preset

LrpPlane = PresetData(
    Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, False)]) |
    HasAny(i.item_plane_gun, i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic)]),
    "Plane"
)

LrpCrouch = PresetData(
    Has(i.item_ability_crouch) | DepFilter(deps.dep_rando_abilities, False),
    "Crouch"
)

LrpDash = PresetData(
    Has(i.item_ability_dash) | DepFilter(deps.dep_rando_abilities, False),
    "Dash"
)

LrpParry = PresetData(
    Has(
        i.item_ability_parry,
        options=[DepFilter(deps.dep_dlc_chalice_only, False)]
    ) |
    HasAll(
        i.item_ability_parry,
        i.item_ability_dash,
        options=[DepFilter(deps.dep_dlc_chalice_only)]
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Parry"
)

LrpPlaneParry = PresetData(
    Has(i.item_ability_plane_parry) | DepFilter(deps.dep_rando_abilities, False),
    "Plane Parry"
)

LrpPlaneShrink = PresetData(
    Has(i.item_ability_plane_shrink) | DepFilter(deps.dep_rando_abilities, False),
    "Plane Shrink"
)

LrpCrouchOrDash = PresetData(
    HasAny(i.item_ability_crouch, i.item_ability_dash) | DepFilter(deps.dep_rando_abilities, False),
    "Crouch or Dash"
)

LrpCrouchAndDash = PresetData(
    HasAll(i.item_ability_crouch, i.item_ability_dash) | DepFilter(deps.dep_rando_abilities, False),
    "Crouch and Dash"
)

LrpParryOrPSugar = PresetData(
    HasAny(
        i.item_ability_parry,
        i.item_charm_psugar,
        options=[DepFilter(deps.dep_dlc_chalice_only, False)]
    ) |
    HasAll(
        i.item_ability_parry,
        i.item_ability_dash,
        options=[DepFilter(deps.dep_dlc_chalice_only)]
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Parry or P. Sugar"
)

LrpDashOrParry = PresetData(
    HasAny(
        i.item_ability_dash,
        i.item_ability_parry,
        options=[DepFilter(deps.dep_dlc_chalice_only, False)]
    ) |
    Has(
        i.item_ability_dash,
        options=[DepFilter(deps.dep_dlc_chalice_only)]
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Dash or Parry"
)

LrpDashAndParry = PresetData(
    HasAll(i.item_ability_dash, i.item_ability_parry) | DepFilter(deps.dep_rando_abilities, False),
    "Dash and Parry"
)

LrpDashParryOrPSugar = PresetData(
    HasAny(
        i.item_ability_dash,
        i.item_ability_parry,
        i.item_charm_psugar,
        options=[DepFilter(deps.dep_dlc_chalice_only, False)]
    ) |
    Has(
        i.item_ability_dash,
        options=[DepFilter(deps.dep_dlc_chalice_only)]
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Dash, Parry, or P. Sugar"
)

LrpCrouchAndParry = PresetData(
    (
        HasAll(
            i.item_ability_crouch,
            i.item_ability_parry,
        ) &
        (Has(i.item_ability_dash) | DepFilter(deps.dep_dlc_chalice_only, False))
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Crouch and Parry"
)

LrpCrouchDashAndParry = PresetData(
    HasAll(
        i.item_ability_crouch,
        i.item_ability_dash,
        i.item_ability_parry,
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Crouch, Dash and Parry"
)

LrpAnySuper = PresetData(
    HasGroup(i.item_group_super, 1),
    "Any Super"
)

LrpWeaponEx = PresetData(
    HasAnyWeaponEx(),
    "Weapon EX"
)

LrpTopgrade = PresetData(
    Preset(LrpParryOrPSugar) &
    Filtered(
        Preset(LrpAnySuper) | Preset(LrpWeaponEx),
        options=[DepFilter(deps.dep_weapon_ex_rando)],
        filtered_resolution=True
    ),
    "Topgrade"
)

LrpPlaneTopgrade = PresetData(
    Preset(LrpPlaneParry) &
    HasAny(
        i.item_plane_ex,
        i.item_plane_super,
        i.item_dlc_cplane_ex,
        i.item_dlc_cplane_super,
        options=[DepFilter(deps.dep_weapon_ex_rando)],
        filtered_resolution=True
    ),
    "Plane Topgrade"
)

LrpRungunTopgrade = PresetData(
    Preset(
        LrpParryOrPSugar,
        options=[DepFilter(deps.dep_hard_logic, False), DepFilter(deps.dep_is_pacifist, False)],
        filtered_resolution=True
    ),
    "Run n Gun Topgrade"
)

LrpWeapon = PresetData(
    Filtered(
        HasAnyWeapon() |
        Filtered(
            Filtered(
                HasAnyWeaponEx() & Has(i.item_charm_coffee),
                options=[DepFilter(deps.dep_weapon_ex_separate)],
            ) |
            Preset(LrpParry) & Has(i.item_charm_whetstone), #|
            ## Or if we want to make things more difficult, go even more lax.
            #(HasGroup(i.item_group_super) & Has(i.item_charm_coffee)),
            options=[DepFilter(deps.dep_hard_logic)]
        ),
        options=[DepFilter(deps.dep_no_start_weapon)],
        filtered_resolution=True
    ),
    "Weapon"
)

LrpRungunWeapon = PresetData(
    Filtered(
        HasAnyWeapon() |
        Filtered(
            HasAnyWeaponEx() | Has(i.item_charm_coffee),
            options=[DepFilter(deps.dep_weapon_ex_separate)]
        ) |
        (Preset(LrpParry) & Has(i.item_charm_whetstone)), #|
        #(HasGroup(i.item_group_super) & Has(i.item_charm_coffee))
        options=[DepFilter(deps.dep_no_start_weapon), DepFilter(deps.dep_hard_logic, False)],
        filtered_resolution=True
    ),
    "Run n Gun Weapon",
)

LrpDlcCookie = PresetData(
    (Has(i.item_charm_dlc_cookie) | DepFilter(deps.dep_dlc_cookie, False)) &
    DepFilter(deps.dep_dlc_chalice),
    "DLC Cookie"
)

LrpDlcDoublejump = PresetData(
    Preset(LrpDlcCookie) &
    (Has(i.item_ability_dlc_cdoublejump) | DepFilter(deps.dep_rando_abilities, False)) &
    DepFilter(deps.dep_dlc_chalice),
    "DLC Double Jump"
)

LrpDashOrDlcDoublejump = PresetData(
    Has(
        i.item_ability_dash,
        options=[DepFilter(deps.dep_dlc_chalice, False)]
    ) |
    HasAny(
        i.item_ability_dash,
        i.item_ability_dlc_cdoublejump,
        options=[DepFilter(deps.dep_dlc_chalice)]
    ) |
    DepFilter(deps.dep_rando_abilities, False),
    "Dash or DLC Double Jump"
)

LrpDlcBossChaliced = PresetData(
    Preset(LrpDlcCookie) &
    Filtered(
        # chalice_only inherently requires Dash for LrpParry
        Preset(LrpTopgrade) & (Preset(LrpDash) | DepFilter(deps.dep_dlc_chalice_only)),
        options=[DepFilter(deps.dep_dlc_chaliced_grade_required)],
        filtered_resolution=True
    ),
    "DLC Boss Chaliced"
)

LrpDlcBossPlaneChaliced = PresetData(
    Preset(LrpDlcCookie) &
    (Preset(LrpPlaneTopgrade) | DepFilter(deps.dep_dlc_chaliced_grade_required, False)),
    "DLC Boss Plane Chaliced"
)

LrpDlcBossChalicedParry = PresetData(
    Preset(LrpDlcBossChaliced) &
    # grade_required will require DashAndParry already
    (Preset(LrpDashAndParry) | DepFilter(deps.dep_dlc_chaliced_grade_required)),
    "DLC Boss Chaliced Parry"
)

LrpDlcRungunChaliced = PresetData(
    Preset(LrpDlcCookie) &
    Filtered(
        Preset(LrpRungunTopgrade) &
        # chalice_only inherently requires Dash for LrpParry
        (Preset(LrpDash) | DepFilter(deps.dep_dlc_chalice_only)),
        options=[DepFilter(deps.dep_dlc_rungun_chaliced_grade_required)],
        filtered_resolution=True
    ),
    "DLC Run n Gun Chaliced"
)

LrpDlcRungunChalicedParry = PresetData(
    Preset(LrpDlcRungunChaliced) &
    # LrpDlcRungunChaliced will require Dash already if chalied_grade_required is on
    (Preset(LrpDash) | DepFilter(deps.dep_dlc_chaliced_grade_required)),
    "DLC Run n Gun Chaliced Parry"
)

LrpDlcRelic = PresetData(
    Has(i.item_charm_dlc_broken_relic),
    "DLC Relic"
)
