from typing import Dict
import dataclasses

from typing_extensions import override

from rule_builder.field_resolvers import FromOption, FromWorldAttr
from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    True_,
    False_,
    Has,
    #HasAll,
    #HasAny,
    HasAllCounts,
    #HasAnyCount,
    HasFromList,
    #HasFromListUnique,
    #HasGroup,
    #HasGroupUnique,
    #CanReachLocation,
    #CanReachRegion,
    #CanReachEntrance,
    Rule,
    OptionFilter,
)

from ...options import (
    HiddenBlockMode,
    PartnersAlwaysUsable,
    PowerStarHunt,
    SpiritRequirements,
    StarWayPowerStarsRequired,
    StarWaySpiritsRequired,
    StarBeamPowerStarsRequired,
    StarBeamSpiritsRequired,
)

# Gear Helper Rules

@dataclasses.dataclass()
class HasHammer(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has("Progressive Hammer", count=1).resolve(world)

@dataclasses.dataclass()
class HasSuperHammer(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has("Progressive Hammer", count=2).resolve(world)

@dataclasses.dataclass()
class HasUltraHammer(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has("Progressive Hammer", count=3).resolve(world)

@dataclasses.dataclass()
class HasBoots(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has("Progressive Boots", count=1).resolve(world)

@dataclasses.dataclass()
class HasSuperBoots(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has("Progressive Boots", count=2).resolve(world)

@dataclasses.dataclass()
class HasUltraBoots(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has("Progressive Boots", count=3).resolve(world)

# General World Interaction

@dataclasses.dataclass()
class CanFlipPanels(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (HasUltraHammer() | HasSuperBoots()).resolve(world)

@dataclasses.dataclass()
class CanShakeTrees(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (Has("Bombette") | HasHammer()).resolve(world)

@dataclasses.dataclass()
class CanSeeHiddenBlocks(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return CanUseAbilityWatt(
            options=[OptionFilter(
                HiddenBlockMode,
                HiddenBlockMode.option_Always_Visible,
                operator="lt",
            )],
            filtered_resolution=True,
        ).resolve(world)

### Partner Abilities

@dataclasses.dataclass()
class CanUseAbilityKooper(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Kooper",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

@dataclasses.dataclass()
class CanUseAbilityBombette(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Bombette",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

@dataclasses.dataclass()
class CanUseAbilityParakarry(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Parakarry",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

@dataclasses.dataclass()
class CanUseAbilityBow(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Bow",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

@dataclasses.dataclass()
class CanUseAbilityWatt(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Watt",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

@dataclasses.dataclass()
class CanUseAbilitySushie(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Sushie",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

@dataclasses.dataclass()
class CanUseAbilityLakilester(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return Has(
            "Lakilester",
            options=[OptionFilter(
                PartnersAlwaysUsable,
                False,
            )],
            filtered_resolution=True,
        ).resolve(world)

### Multiple Solutions to the task

@dataclasses.dataclass()
class CanHitGroundedBlocks(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (
            CanUseAbilityKooper()
            | CanUseAbilityBombette()
            | HasSuperBoots()
            | HasHammer()
        ).resolve(world)

@dataclasses.dataclass()
class CanHitFloatingBlocks(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (CanUseAbilityKooper() | HasBoots()).resolve(world)

@dataclasses.dataclass()
class CanHitGroundedSwitches(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (
            CanUseAbilityKooper()
            | CanUseAbilityBombette()
            | CanUseAbilityParakarry()
            | HasBoots()
            | HasHammer()
        ).resolve(world)

@dataclasses.dataclass()
class CanClimbSteps(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (CanUseAbilityParakarry() | HasBoots()).resolve(world)

@dataclasses.dataclass()
class CanReenterVerticalPipes(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (
            CanUseAbilityKooper()
            | CanUseAbilityParakarry()
            | HasBoots()
        ).resolve(world)

# Endgame requirements

@dataclasses.dataclass()
class CanOpenStarWay(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        rule_starway_spirits: Rule = HasFromList(
            "STARSPIRIT",
            count=FromOption(StarWaySpiritsRequired)
        )
        has_required_spirits: Rule = (
            Has(
                "STARSPIRIT_1",
                count=FromWorldAttr("require_eldstar")
            )
            & Has(
                "STARSPIRIT_2",
                count=FromWorldAttr("require_mamar")
            )
            & Has(
                "STARSPIRIT_3",
                count=FromWorldAttr("require_skolar")
            )
            & Has(
                "STARSPIRIT_4",
                count=FromWorldAttr("require_muskular")
            )
            & Has(
                "STARSPIRIT_5",
                count=FromWorldAttr("require_misstar")
            )
            & Has(
                "STARSPIRIT_6",
                count=FromWorldAttr("require_klevar")
            )
            & Has(
                "STARSPIRIT_7",
                count=FromWorldAttr("require_kalmar")
            )
        )

        rule_starway_spirits_specific: Rule = (
            has_required_spirits
            | False_(
                options=[OptionFilter(
                    SpiritRequirements,
                    SpiritRequirements.option_Any,
                    operator="ne",
                )],
                filtered_resolution=True,
            )
        )

        rule_starway_powerstars: Rule = Has(
            "Power Star",
            count=FromOption(StarWayPowerStarsRequired),
            options=[OptionFilter(PowerStarHunt, True)],
            filtered_resolution=True,
        )
        return (
            rule_starway_spirits
            & rule_starway_spirits_specific
            & rule_starway_powerstars
        ).resolve(world)

@dataclasses.dataclass()
class HasStarBeamRequirements(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        star_beam_star_spirits: Rule = HasFromList(
            "STARSPIRIT",
            count=FromOption(StarBeamSpiritsRequired)
        )
        star_beam_power_stars: Rule = Has(
            "Power Star",
            count=FromOption(StarBeamPowerStarsRequired),
            options=[OptionFilter(PowerStarHunt, True)],
            filtered_resolution=True,
        )

        return (
            star_beam_star_spirits
            & star_beam_power_stars
        ).resolve(world)

logichelpers: Dict[str, Rule] = {
    "Boots": "(Progressive_Boots, 1)",
    "Super_Boots": "(Progressive_Boots, 2)",
    "Ultra_Boots": "(Progressive_Boots, 3)",
    "Hammer": "(Progressive_Hammer, 1)",
    "Super_Hammer": "(Progressive_Hammer, 2)",
    "Ultra_Hammer": "(Progressive_Hammer, 3)",

    "can_flip_panels": "Ultra_Hammer or Super_Boots",

    "can_shake_trees": "Bombette or Hammer",

    "can_hit_grounded_blocks": "can_use_ability_bombette or can_use_ability_kooper or Super_Boots or Hammer",
    "can_hit_floating_blocks": "can_use_ability_kooper or Boots",
    "can_hit_grounded_switches": "can_use_ability_bombette or can_use_ability_kooper or Boots or Hammer or can_use_ability_parakarry",

    "can_climb_steps": "Boots or can_use_ability_parakarry",
    "saved_all_yoshi_kids": "'RF_SavedYoshiKid_1' and 'RF_SavedYoshiKid_2' and 'RF_SavedYoshiKid_3' and 'RF_SavedYoshiKid_4' and 'RF_SavedYoshiKid_5'",
    "can_reenter_vertical_pipes": "can_use_ability_kooper or Boots or can_use_ability_parakarry",

    "has_strong_aerial_partner": "Bow or Watt or Sushie or Lakilester",
    "has_weak_aerial_partner": "Goombario or Parakarry",

    "can_pass_kent": "(not kent_c_koopa == 1) or (('STARSPIRIT', 2) and (Boots or Goombario))",

    "can_see_hidden_blocks": "can_use_ability_watt or hidden_block_mode == 3",


    "can_use_ability_kooper": "Kooper or partners_always_usable",
    "can_use_ability_bombette": "Bombette or partners_always_usable",
    "can_use_ability_parakarry": "Parakarry or partners_always_usable",
    "can_use_ability_bow": "Bow or partners_always_usable",
    "can_use_ability_watt": "Watt or partners_always_usable",
    "can_use_ability_sushie": "Sushie or partners_always_usable",
    "can_use_ability_lakilester": "Lakilester or partners_always_usable"
}