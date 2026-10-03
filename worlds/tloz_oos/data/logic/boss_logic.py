import dataclasses

from rule_builder.rules import And, Or

from ... import OracleOfSeasonsWorld
from . import Rule
from .logic_predicates import (
    oos_can_kill_armored_enemy,
    oos_can_punch,
    oos_can_use_ember_seeds,
    oos_can_use_mystery_seeds,
    oos_can_use_scent_seeds,
    oos_has_bombs,
    oos_has_bombs_to_fight,
    oos_has_bracelet,
    oos_has_ember_seeds,
    oos_has_feather,
    oos_has_fools_ore,
    oos_has_hearts_by_difficulty,
    oos_has_magic_boomerang,
    oos_has_magnet_gloves,
    oos_has_noble_sword,
    oos_has_satchel,
    oos_has_scent_seeds,
    oos_has_seed_thrower,
    oos_has_sword,
    oos_option_hard_logic,
    oos_option_hell_logic,
    oos_option_medium_logic,
    oos_shoot_beams,
)
from .rulebuilder import from_bool


def can_beat_aquamentus(_: int) -> Rule:
    return oos_can_kill_armored_enemy(False, False)


def can_beat_dodongo(dungeon: int) -> Rule:
    return And(
        Or(
            And(from_bool(dungeon == 2), oos_has_bombs()),
            oos_has_bombs_to_fight(),
        ),
        oos_has_bracelet(),
    )


def can_beat_mothula(_: int) -> Rule:
    return And(
        oos_can_kill_armored_enemy(False, False),
        oos_has_hearts_by_difficulty(4, 3, 3),
    )


def can_beat_gohma(_: int) -> Rule:
    return And(
        Or(
            And(
                # Kill Gohma without breaking its pincer
                oos_option_medium_logic(),
                Or(
                    oos_has_seed_thrower(),
                    oos_option_hard_logic(),  # You can kill Gohma with the satchel. Yup...
                ),
                Or(oos_has_scent_seeds(), oos_has_ember_seeds()),
            ),
            And(
                # Kill Gohma with sword beams (Gohma's minions give enough hearts to justify it)
                oos_option_medium_logic(),
                Or(oos_has_noble_sword(), oos_shoot_beams()),
            ),
            And(
                # Kill Gohma traditionally (break pincer, then spam seeds)
                Or(oos_has_sword(), oos_has_fools_ore()),
                Or(
                    oos_can_use_ember_seeds(False),
                    oos_can_use_scent_seeds(),
                    And(
                        oos_option_medium_logic(),
                        oos_has_satchel(2),  # It may require quite a bunch of mystery seeds...
                        oos_can_use_mystery_seeds(),
                    ),
                ),
            ),
        ),
        oos_has_hearts_by_difficulty(4, 3, 3),
    )


def can_beat_digdogger(_: int) -> Rule:
    return And(
        oos_has_magnet_gloves(),
        oos_has_hearts_by_difficulty(6, 4, 3),
    )


def can_beat_manhandla(_: int) -> Rule:
    return And(
        oos_has_magic_boomerang(),
        Or(
            oos_has_sword(),
            oos_has_fools_ore(),
            oos_has_seed_thrower(),
        ),
        oos_has_hearts_by_difficulty(6, 4, 3),
    )


def can_beat_gleeok(dungeon: int) -> Rule:
    return And(
        Or(
            oos_has_feather(),
            And(from_bool(dungeon == 1), oos_option_medium_logic()),
        ),
        Or(
            oos_has_sword(),
            oos_has_fools_ore(),
            And(
                oos_can_punch(),
                oos_has_hearts_by_difficulty(20, 7, 5),
            ),
            And(
                oos_option_hard_logic(),
                oos_has_bombs(9),
            ),
            And(
                oos_option_hell_logic(),
                oos_has_bombs_to_fight(),
            )
        ),
        oos_has_hearts_by_difficulty(8, 5, 3),
    )


def can_beat_medusa_head(_: int) -> Rule:
    return And(
        oos_has_feather(),
        Or(oos_has_sword(), oos_has_fools_ore()),
        oos_has_hearts_by_difficulty(8, 5, 3),
    )


@dataclasses.dataclass()
class CanBeatBoss(Rule, game=OracleOfSeasonsWorld.game):
    dungeon: int

    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        boss_rules = [
            can_beat_aquamentus,
            can_beat_dodongo,
            can_beat_mothula,
            can_beat_gohma,
            can_beat_digdogger,
            can_beat_manhandla,
            can_beat_gleeok,
            can_beat_medusa_head,
        ]
        return boss_rules[world.boss_mapping[self.dungeon] - 1](self.dungeon).resolve(world)
