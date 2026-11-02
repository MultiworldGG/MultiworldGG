from typing import TYPE_CHECKING, Callable
from BaseClasses import Entrance
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from .Macros import *
from ..options import *

if TYPE_CHECKING:
    from .. import TPWorld


# All connections created are present in this file, even if the rule is always True.
# This is to allow for easy change / lookup of connection rules
def set_region_access_rules(world: "TPWorld", player: int):

    assert isinstance(world, World), f"[Twilight Princess] {world=}"

    def set_rule_if_exits(
        exit: Entrance,
        rule: Callable[[CollectionState], bool],
        glitched_rule: Callable[[CollectionState], bool] = None,
    ):

        if (
            world.options.logic_rules.value == LogicRules.option_glitched
            and glitched_rule
        ):
            # assert glitched_rule, f"[Twilight Princess] {location=} has no glitched rule"
            set_rule(exit, glitched_rule)
        # elif world.options.logic_rules.value == LogicRules.option_no_logic:
        #     set_rule(exit, lambda state: (True))
        else:
            set_rule(exit, rule)

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Entrance -> Outside Arbiters Grounds"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Entrance -> Arbiters Grounds Lobby"),
        lambda state: (
            can_use(state, player, "Arbiters Grounds Small Key", 1)
            and can_use(state, player, "Lantern")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Lobby -> Arbiters Grounds Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Lobby -> Arbiters Grounds East Wing"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Lobby -> Arbiters Grounds West Wing"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Lobby -> Arbiters Grounds After Poe Gate"),
        lambda state: (
            can_defeat_Poe(state, player)
            and can_use(state, player, "Shadow Crystal")
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_GhoulRat(state, player)
            and can_defeat_Stalfos(state, player)
            and can_use(state, player, "Arbiters Grounds Small Key", 4)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds East Wing -> Arbiters Grounds Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds West Wing -> Arbiters Grounds Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds After Poe Gate -> Arbiters Grounds Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Arbiters Grounds After Poe Gate -> Arbiters Grounds Boss Room"
        ),
        lambda state: (
            can_use(state, player, "Spinner")
            and can_use(state, player, "Arbiters Grounds Big Key")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Arbiters Grounds Boss Room -> Mirror Chamber Lower"),
        lambda state: (can_defeat_Stallord(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Boss Room -> City in The Sky Entrance"),
        lambda state: (can_defeat_Argorok(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "City in The Sky Central Tower Second Floor -> City in The Sky West Wing"
        ),
        lambda state: (can_use(state, player, "Progressive Clawshot", 2)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "City in The Sky Central Tower Second Floor -> City in The Sky Lobby"
        ),
        lambda state: (
            (
                can_use(state, player, "Progressive Clawshot", 1)
                and can_use(state, player, "Iron Boots")
                and can_use(state, player, "Shadow Crystal")
            )
            and (
                state._tp_damage_magnification(player)
                != DamageMagnification.option_ohko
            )
        ),
        lambda state: (
            (
                can_use(state, player, "Progressive Clawshot", 1)
                and can_use(state, player, "Iron Boots")
                and (
                    can_use(state, player, "Shadow Crystal")
                    or can_do_lja(state, player)
                )
            )
            and (
                state._tp_damage_magnification(player)
                != DamageMagnification.option_ohko
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky East Wing -> City in The Sky Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Entrance -> Lake Hylia"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Entrance -> City in The Sky Lobby"),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 1)
            or (
                can_use(state, player, "Progressive Hero's Bow", 1)
                and can_do_lja(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Lobby -> City in The Sky Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Lobby -> City in The Sky East Wing"),
        lambda state: (
            can_use(state, player, "Spinner")
            and can_use(state, player, "City in The Sky Small Key", 1)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Lobby -> City in The Sky West Wing"),
        lambda state: (
            (
                can_use(state, player, "Progressive Clawshot")
                and can_use(state, player, "Spinner")
            )
            or can_use(state, player, "Progressive Clawshot", 2)
        ),
        lambda state: (
            (
                can_use(state, player, "Progressive Clawshot")
                or can_do_lja(state, player)
            )
            and can_use(state, player, "Spinner")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky Lobby -> City in The Sky North Wing"),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_BabaSerpent(state, player)
            and can_defeat_Kargarok(state, player)
            and can_use(state, player, "Shadow Crystal")
            and can_use(state, player, "Iron Boots")
        ),
        lambda state: (can_use(state, player, "Progressive Clawshot", 2)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "City in The Sky Lobby -> City in The Sky Central Tower Second Floor"
        ),
        lambda state: (
            state.can_reach_region("City in The Sky Central Tower Second Floor", player)
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_use(state, player, "Iron Boots")
        ),
        lambda state: (
            can_use(state, player, "Progressive Clawshot")
            and can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky North Wing -> City in The Sky Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky North Wing -> City in The Sky Boss Room"),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_Aeralfos(state, player)
            and can_use(state, player, "City in The Sky Big Key")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("City in The Sky West Wing -> City in The Sky Lobby"),
        lambda state: (can_use(state, player, "Progressive Clawshot", 2)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "City in The Sky West Wing -> City in The Sky Central Tower Second Floor"
        ),
        lambda state: (can_use(state, player, "Progressive Clawshot", 2)),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Boss Room -> South Faron Woods"),
        lambda state: (can_defeat_Diababa(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple East Wing -> Forest Temple Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple East Wing -> Forest Temple North Wing"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Entrance -> North Faron Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Entrance -> Forest Temple Lobby"),
        lambda state: (
            can_defeat_Walltula(state, player)
            and can_defeat_Bokoblin(state, player)
            and can_break_monkey_cage(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Lobby -> Forest Temple Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Lobby -> Forest Temple East Wing"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Lobby -> Forest Temple West Wing"),
        lambda state: (
            can_burn_webs(state, player)
            and (
                (
                    can_use(state, player, "Forest Temple Small Key", 2)
                    and can_defeat_Bokoblin(state, player)
                )
                or can_use(state, player, "Progressive Clawshot", 1)
            )
        ),
        lambda state: (
            can_burn_webs(state, player)
            and (
                (
                    can_use(state, player, "Forest Temple Small Key", 2)
                    and can_defeat_Bokoblin(state, player)
                )
                or can_use(state, player, "Progressive Clawshot", 1)
                or can_do_lja(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple Lobby -> Ook"),
        lambda state: (
            can_use(state, player, "Lantern")
            and can_defeat_Walltula(state, player)
            and can_defeat_Bokoblin(state, player)
            and can_break_monkey_cage(state, player)
            and can_use(state, player, "Forest Temple Small Key", 4)
        ),
        lambda state: (
            (
                state.can_reach_region("Forest Temple West Wing", player)
                and can_do_lja(state, player)
            )
            or (
                can_use(state, player, "Lantern")
                and can_defeat_Bombling(state, player)
                and can_defeat_Walltula(state, player)
                and can_defeat_BigBaba(state, player)
                and can_defeat_Bokoblin(state, player)
                and can_break_monkey_cage(state, player)
                and can_use(state, player, "Forest Temple Small Key", 4)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple North Wing -> Forest Temple East Wing"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple North Wing -> Forest Temple Boss Room"),
        lambda state: (
            can_use(state, player, "Forest Temple Big Key")
            and can_use(state, player, "Gale Boomerang")
            and (
                can_free_all_monkeys(state, player)
                or can_use(state, player, "Progressive Clawshot", 1)
            )
        ),
        lambda state: (
            can_use(state, player, "Forest Temple Big Key")
            and (
                can_do_lja(state, player)
                or (
                    can_use(state, player, "Gale Boomerang")
                    and (
                        can_free_all_monkeys(state, player)
                        or can_use(state, player, "Progressive Clawshot", 1)
                    )
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple West Wing -> Forest Temple Lobby"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Forest Temple West Wing -> Ook"),
        lambda state: (can_use(state, player, "Gale Boomerang")),
        lambda state: (
            can_use(state, player, "Gale Boomerang")
            or can_use(state, player, "Shadow Crystal")
            or has_sword(state, player)
            or has_bombs(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Ook -> Forest Temple West Wing"),
        lambda state: (
            can_defeat_Ook(state, player) and can_use(state, player, "Gale Boomerang")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Boss Room -> Lower Kakariko Village"),
        lambda state: (can_defeat_Fyrus(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Goron Mines Crystal Switch Room -> Goron Mines Magnet Room"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Crystal Switch Room -> Goron Mines North Wing"),
        lambda state: (
            (
                (can_use(state, player, "Iron Boots") and has_sword(state, player))
                or can_use(state, player, "Progressive Hero's Bow", 1)
            )
            and can_use(state, player, "Goron Mines Small Key", 2)
        ),
        lambda state: (
            can_use(state, player, "Goron Mines Small Key", 2)
            and (
                can_use(state, player, "Progressive Hero's Bow", 1)
                or (can_use(state, player, "Iron Boots") and has_sword(state, player))
                or (
                    (
                        can_do_lja(state, player)
                        or (has_sword(state, player) and has_bombs(state, player))
                    )
                    and (
                        can_use(state, player, "Progressive Clawshot", 1)
                        or can_use(state, player, "Ball and Chain")
                        or has_bombs(state, player)
                    )
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Goron Mines Entrance -> Death Mountain Sumo Hall Goron Mines Tunnel"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Entrance -> Goron Mines Magnet Room"),
        lambda state: (
            can_use(state, player, "Iron Boots")
            and can_break_wooden_door(state, player)
        ),
        lambda state: (
            (
                can_use(state, player, "Iron Boots")
                or can_use(state, player, "Shadow Crystal")
            )
            and (
                can_break_wooden_door(state, player)
                or can_do_bs_moon_boots(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Lower West Wing -> Goron Mines Magnet Room"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Magnet Room -> Goron Mines Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Magnet Room -> Goron Mines Lower West Wing"),
        lambda state: (
            can_use(state, player, "Goron Mines Small Key", 1)
            or (state._tp_gm_shortcut(player) and can_use(state, player, "Iron Boots"))
        ),
        lambda state: (
            can_use(state, player, "Goron Mines Small Key", 1)
            or (
                (state._tp_gm_shortcut(player) or has_sword(state, player))
                and can_use(state, player, "Iron Boots")
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Goron Mines Magnet Room -> Goron Mines Crystal Switch Room"
        ),
        lambda state: (
            (
                can_use(state, player, "Goron Mines Small Key", 1)
                or state._tp_gm_shortcut(player)
            )
            and can_use(state, player, "Iron Boots")
        ),
        lambda state: (
            (
                can_use(state, player, "Goron Mines Small Key", 1)
                or state._tp_gm_shortcut(player)
                or has_sword(state, player)
            )
            and can_use(state, player, "Iron Boots")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines North Wing -> Goron Mines Crystal Switch Room"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines North Wing -> Goron Mines Upper East Wing"),
        lambda state: (can_use(state, player, "Goron Mines Small Key", 3)),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines North Wing -> Goron Mines Boss Room"),
        lambda state: (
            can_use(state, player, "Progressive Hero's Bow", 1)
            and can_use(state, player, "Iron Boots")
            and can_defeat_Bulblin(state, player)
            and can_use(state, player, "Goron Mines Key Shard", 3)
        ),
        lambda state: (
            can_use(state, player, "Goron Mines Key Shard", 3)
            and can_use(state, player, "Progressive Hero's Bow", 1)
            and (
                (
                    can_use(state, player, "Iron Boots")
                    and can_defeat_Bulblin(state, player)
                )
                or can_use(state, player, "Progressive Clawshot")
                or can_do_lja(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Upper East Wing -> Goron Mines North Wing"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Goron Mines Upper East Wing -> Goron Mines Magnet Room"),
        lambda state: (
            can_use(state, player, "Iron Boots")
            and can_defeat_Dangoro(state, player)
            and can_use(state, player, "Progressive Hero's Bow", 1)
        ),
        lambda state: (
            can_use(state, player, "Iron Boots")
            and can_defeat_Dangoro(state, player)
            and (
                can_use(state, player, "Progressive Hero's Bow", 1)
                or can_defeat_Beamos(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Ganondorf Castle -> Hyrule Castle Tower Climb"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Entrance -> Castle Town North Inside Barrier"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Entrance -> Hyrule Castle Main Hall"),
        lambda state: (can_use(state, player, "Hyrule Castle Small Key", 1)),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Entrance -> Hyrule Castle Outside West Wing"),
        lambda state: (can_defeat_Bokoblin_Red(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Entrance -> Hyrule Castle Outside East Wing"),
        lambda state: (can_defeat_Bokoblin_Red(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Graveyard -> Hyrule Castle Outside East Wing"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Main Hall -> Hyrule Castle Above Lantern Staircase"
        ),
        lambda state: (
            can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_Darknut(state, player)
            and can_use(state, player, "Gale Boomerang")
        ),
        lambda state: (
            can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_defeat_Darknut(state, player)
            and can_use(state, player, "Gale Boomerang")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Main Hall -> Hyrule Castle After Double Dinalfos"
        ),
        lambda state: (
            can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and state._tp_hc_shortcut(player)
            and can_use(state, player, "Progressive Clawshot", 2)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Above Lantern Staircase -> Hyrule Castle Main Hall"
        ),
        lambda state: (can_defeat_Darknut(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Above Lantern Staircase -> Hyrule Castle After Double Dinalfos"
        ),
        lambda state: (
            can_use(state, player, "Lantern") and can_defeat_Dinalfos(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Above Lantern Staircase -> Hyrule Castle After Double Darknuts"
        ),
        lambda state: (
            can_knock_down_hc_painting(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Darknut(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle After Double Dinalfos -> Hyrule Castle Main Hall"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle After Double Dinalfos -> Hyrule Castle Above Lantern Staircase"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle After Double Dinalfos -> Hyrule Castle Third Floor Balcony"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle After Double Darknuts -> Hyrule Castle Main Hall"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle After Double Darknuts -> Hyrule Castle Above Lantern Staircase"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle After Double Darknuts -> Hyrule Castle Third Floor Balcony"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Main Hall -> Hyrule Castle Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Outside East Wing -> Hyrule Castle Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Outside East Wing -> Hyrule Castle Graveyard"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Outside West Wing -> Hyrule Castle Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Third Floor Balcony -> Hyrule Castle Tower Climb"
        ),
        lambda state: (can_use(state, player, "Hyrule Castle Small Key", 2)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Third Floor Balcony -> Hyrule Castle After Double Dinalfos"
        ),
        lambda state: (
            (can_use(state, player, "Lantern") and can_defeat_Dinalfos(state, player))
            or state._tp_hc_shortcut(player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Third Floor Balcony -> Hyrule Castle After Double Darknuts"
        ),
        lambda state: (
            can_defeat_Darknut(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_knock_down_hc_painting(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Hyrule Castle Tower Climb -> Hyrule Castle Third Floor Balcony"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Tower Climb -> Hyrule Castle Treasure Room"),
        lambda state: (
            can_use(state, player, "Hyrule Castle Small Key", 3)
            and can_use(state, player, "Spinner")
            and can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_Darknut(state, player)
            and can_defeat_Lizalfos(state, player)
        ),
        lambda state: (
            can_use(state, player, "Hyrule Castle Small Key", 3)
            and (can_use(state, player, "Spinner") or can_do_js_lja(state, player))
            and can_use(state, player, "Progressive Clawshot")
            and can_defeat_Darknut(state, player)
            and can_defeat_Lizalfos(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Tower Climb -> Ganondorf Castle"),
        lambda state: (
            can_use(state, player, "Spinner")
            and can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_Darknut(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_use(state, player, "Hyrule Castle Big Key")
            and can_defeat_Ganondorf(state, player)
        ),
        lambda state: (
            (can_use(state, player, "Spinner") or can_do_js_lja(state, player))
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_defeat_Darknut(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_use(state, player, "Hyrule Castle Big Key")
            and can_defeat_Ganondorf(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Castle Treasure Room -> Hyrule Castle Tower Climb"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lakebed Temple Boss Room -> Lake Hylia Lanayru Spring"),
        lambda state: (can_defeat_Morpheel(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lakebed Temple Central Room -> Lakebed Temple Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lakebed Temple Central Room -> Lakebed Temple East Wing Second Floor"
        ),
        lambda state: (can_use(state, player, "Lakebed Temple Small Key", 1)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lakebed Temple Central Room -> Lakebed Temple East Wing First Floor"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lakebed Temple Central Room -> Lakebed Temple West Wing"),
        lambda state: (
            can_use(state, player, "Lakebed Temple Small Key", 3)
            and can_smash(state, player)
            and can_use(state, player, "Progressive Clawshot", 1)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lakebed Temple Central Room -> Lakebed Temple Boss Room"),
        lambda state: (
            can_use(state, player, "Lakebed Temple Small Key", 3)
            and can_launch_bombs(state, player)
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_use(state, player, "Lakebed Temple Big Key")
        ),
        lambda state: (
            (
                can_use(state, player, "Progressive Clawshot", 1)
                and (
                    can_use(state, player, "Progressive Master Sword", 1)
                    or can_use(state, player, "Lakebed Temple Big Key")
                )
            )
            or can_do_lja(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lakebed Temple East Wing First Floor -> Lakebed Temple Central Room"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lakebed Temple East Wing Second Floor -> Lakebed Temple Central Room"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lakebed Temple East Wing Second Floor -> Lakebed Temple East Wing First Floor"
        ),
        lambda state: (
            can_launch_bombs(state, player)
            or can_use(state, player, "Progressive Clawshot", 1)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lakebed Temple Entrance -> Lake Hylia Lakebed Temple Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lakebed Temple Entrance -> Lakebed Temple Central Room"),
        lambda state: (
            can_use(state, player, "Zora Armor") and can_launch_bombs(state, player)
        ),
        lambda state: (
            (can_use(state, player, "Zora Armor") or can_do_air_refill(state, player))
            and (can_launch_bombs(state, player) or can_step_clip(state, player))
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lakebed Temple West Wing -> Lakebed Temple Central Room"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Palace of Twilight Entrance -> Mirror Chamber Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Entrance -> Palace of Twilight West Wing"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Entrance -> Palace of Twilight East Wing"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Entrance -> Palace of Twilight Central First Room"
        ),
        lambda state: (can_use(state, player, "Progressive Master Sword", 4)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight West Wing -> Palace of Twilight Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight East Wing -> Palace of Twilight Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Central First Room -> Palace of Twilight Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Central First Room -> Palace of Twilight Outside Room"
        ),
        lambda state: (
            can_use(state, player, "Palace of Twilight Small Key", 5)
            and can_use(state, player, "Progressive Master Sword", 4)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Outside Room -> Palace of Twilight Central First Room"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Outside Room -> Palace of Twilight North Tower"
        ),
        lambda state: (can_use(state, player, "Palace of Twilight Small Key", 6)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight North Tower -> Palace of Twilight Outside Room"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight North Tower -> Palace of Twilight Boss Room"
        ),
        lambda state: (
            can_defeat_ZantHead(state, player)
            and can_use(state, player, "Progressive Master Sword", 4)
            and can_use(state, player, "Palace of Twilight Big Key")
            and can_defeat_ShadowBeast(state, player)
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_use(state, player, "Palace of Twilight Small Key", 7)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Palace of Twilight Boss Room -> Palace of Twilight Entrance"
        ),
        lambda state: (can_defeat_Zant(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Left Door -> Snowpeak Ruins Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Left Door -> Snowpeak Summit Lower Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Right Door -> Snowpeak Ruins Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Right Door -> Snowpeak Summit Lower Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Boss Room -> Snowpeak Summit Lower"),
        lambda state: (can_defeat_Blizzeta(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Yeto and Yeta"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Second Floor Mini Freezard Room"
        ),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            and can_use(state, player, "Snowpeak Ruins Small Key", 3)
        ),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            and (
                can_use(state, player, "Snowpeak Ruins Small Key", 4)
                or can_use(state, player, "Progressive Clawshot", 1)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Wooden Beam Room"
        ),
        lambda state: (can_use(state, player, "Ball and Chain")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins West Courtyard"
        ),
        lambda state: (can_use(state, player, "Snowpeak Ruins Small Key", 2)),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Chapel"
        ),
        lambda state: (False),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Caged Freezard Room Lower"
        ),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room Lower -> Snowpeak Ruins Caged Freezard Room"
        ),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Caged Freezard Room Lower -> Snowpeak Ruins Entrance"
        ),
        lambda state: (False),
        lambda state: (can_do_lja(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Chapel -> Snowpeak Ruins West Courtyard"),
        lambda state: (can_defeat_Chilfos(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Chapel -> Snowpeak Ruins Boss Room"),
        lambda state: (can_use(state, player, "Bedroom Key")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Darkhammer Room -> Snowpeak Ruins West Courtyard"
        ),
        lambda state: (can_defeat_Darkhammer(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins East Courtyard -> Snowpeak Ruins Yeto and Yeta"
        ),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            or can_use(state, player, "Ball and Chain")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins East Courtyard -> Snowpeak Ruins West Courtyard"
        ),
        lambda state: (can_use(state, player, "Ball and Chain")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins East Courtyard -> Snowpeak Ruins Northeast Chilfos Room First Floor"
        ),
        lambda state: (
            (
                can_use(state, player, "Snowpeak Ruins Small Key", 4)
                and can_defeat_MiniFreezard(state, player)
            )
            or (
                can_use(state, player, "Snowpeak Ruins Small Key", 2)
                and can_use(state, player, "Progressive Clawshot", 1)
                and can_defeat_MiniFreezard(state, player)
            )
        ),
        lambda state: (
            (
                can_use(state, player, "Snowpeak Ruins Small Key", 4)
                and can_defeat_MiniFreezard(state, player)
            )
            or (
                can_use(state, player, "Ball and Chain")
                and can_use(state, player, "Progressive Clawshot", 1)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Entrance -> Snowpeak Ruins Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Entrance -> Snowpeak Ruins Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Entrance -> Snowpeak Ruins Yeto and Yeta"),
        lambda state: (True),
    )
    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Entrance -> Snowpeak Ruins Caged Freezard Room Lower"
        ),
        lambda state: (False),
        lambda state: (can_do_lja(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Northeast Chilfos Room First Floor -> Snowpeak Ruins East Courtyard"
        ),
        lambda state: (can_use(state, player, "Snowpeak Ruins Small Key", 4)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Northeast Chilfos Room First Floor -> Snowpeak Ruins Yeto and Yeta"
        ),
        lambda state: (can_defeat_Chilfos(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Northeast Chilfos Room First Floor -> Snowpeak Ruins Northeast Chilfos Room Second Floor"
        ),
        lambda state: (False),
        lambda state: (can_do_lja(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Northeast Chilfos Room Second Floor -> Snowpeak Ruins Northeast Chilfos Room First Floor"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Northeast Chilfos Room Second Floor -> Snowpeak Ruins Yeto and Yeta"
        ),
        lambda state: (can_use(state, player, "Ball and Chain")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Yeto and Yeta"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Northeast Chilfos Room Second Floor"
        ),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_defeat_Chilfos(state, player)
        ),
        lambda state: (
            (
                can_use(state, player, "Ball and Chain")
                and can_use(state, player, "Progressive Clawshot", 1)
                and can_defeat_Chilfos(state, player)
            )
            or can_do_lja(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Caged Freezard Room"
        ),
        lambda state: (can_use(state, player, "Snowpeak Ruins Small Key", 4)),
        lambda state: (
            can_use(state, player, "Snowpeak Ruins Small Key", 4)
            or (
                can_use(state, player, "Ball and Chain")
                and can_use(state, player, "Progressive Clawshot", 1)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins West Cannon Room -> Snowpeak Ruins West Courtyard"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins West Cannon Room -> Snowpeak Ruins Wooden Beam Room"
        ),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins West Courtyard -> Snowpeak Ruins Yeto and Yeta"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins West Courtyard -> Snowpeak Ruins East Courtyard"
        ),
        lambda state: (can_use(state, player, "Ball and Chain")),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            or can_use(state, player, "Snowpeak Ruins Small Key", 4)
            or can_use(state, player, "Ordon Goat Cheese")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins West Courtyard -> Snowpeak Ruins West Cannon Room"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins West Courtyard -> Snowpeak Ruins Chapel"),
        lambda state: (
            (
                can_use(state, player, "Snowpeak Ruins Small Key", 4)
                and can_use(state, player, "Ordon Goat Cheese")
            )
            and can_use(state, player, "Ball and Chain")
            and has_bombs(state, player)
        ),
        lambda state: (
            can_use(state, player, "Snowpeak Ruins Small Key", 4)
            or can_use(state, player, "Ordon Goat Cheese")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins West Courtyard -> Snowpeak Ruins Darkhammer Room"
        ),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            or (
                (
                    can_use(state, player, "Snowpeak Ruins Small Key", 2)
                    or can_use(state, player, "Ordon Goat Cheese")
                )
                and has_bombs(state, player)
            )
        ),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            or (
                (
                    can_use(state, player, "Snowpeak Ruins Small Key", 4)
                    or can_use(state, player, "Ordon Goat Cheese")
                )
                and has_bombs(state, player)
            )
            or (
                can_use(state, player, "Shadow Crystal")
                and (
                    state._tp_damage_magnification(player)
                    != DamageMagnification.option_ohko
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Wooden Beam Room -> Snowpeak Ruins West Cannon Room"
        ),
        lambda state: (can_use(state, player, "Ball and Chain")),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins Caged Freezard Room"
        ),
        lambda state: (can_use(state, player, "Ordon Goat Cheese")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins West Courtyard"
        ),
        lambda state: (can_use(state, player, "Ordon Pumpkin")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins East Courtyard"
        ),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            or can_use(state, player, "Ball and Chain")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Armos Antechamber -> Temple of Time Central Mechanical Platform"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Temple of Time Boss Room -> Sacred Grove Past"),
        lambda state: (can_defeat_Armogohma(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Central Mechanical Platform -> Temple of Time Connecting Corridors"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Central Mechanical Platform -> Temple of Time Armos Antechamber"
        ),
        lambda state: (can_use(state, player, "Spinner")),
        lambda state: (can_use(state, player, "Spinner") or can_do_lja(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Central Mechanical Platform -> Temple of Time Moving Wall Hallways"
        ),
        lambda state: (
            can_use(state, player, "Spinner")
            and (can_use(state, player, "Temple of Time Small Key", 2))
        ),
        lambda state: (
            (can_use(state, player, "Spinner") or can_do_lja(state, player))
            and can_use(state, player, "Temple of Time Small Key", 2)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Connecting Corridors -> Temple of Time Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Connecting Corridors -> Temple of Time Central Mechanical Platform"
        ),
        lambda state: (
            has_ranged_item(state, player)
            and can_defeat_YoungGohma(state, player)
            and can_defeat_Lizalfos(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Crumbling Corridor -> Temple of Time Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Crumbling Corridor -> Temple of Time Boss Room"
        ),
        lambda state: (
            can_use(state, player, "Progressive Dominion Rod", 1)
            and can_use(state, player, "Temple of Time Big Key")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Darknut Arena -> Temple of Time Upper Spike Trap Corridor"
        ),
        lambda state: (
            can_defeat_Darknut(state, player)
            and can_use(state, player, "Progressive Dominion Rod", 1)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Entrance -> Sacred Grove Past Behind Window"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Entrance -> Temple of Time Connecting Corridors"
        ),
        lambda state: (can_use(state, player, "Temple of Time Small Key", 1)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Entrance -> Temple of Time Crumbling Corridor"
        ),
        lambda state: (
            (
                can_use(state, player, "Progressive Dominion Rod", 1)
                and can_use(state, player, "Progressive Hero's Bow", 1)
                and can_use(state, player, "Spinner")
                and can_defeat_Lizalfos(state, player)
                and can_defeat_Dinalfos(state, player)
                and can_defeat_Darknut(state, player)
                and can_use(state, player, "Temple of Time Small Key", 3)
            )
            or state._tp_open_door_of_time(player)
        ),
        lambda state: (
            can_use(state, player, "Progressive Dominion Rod", 1)
            or state._tp_open_door_of_time(player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Floor Switch Puzzle Room -> Temple of Time Scales of Time"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Moving Wall Hallways -> Temple of Time Central Mechanical Platform"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Moving Wall Hallways -> Temple of Time Scales of Time"
        ),
        lambda state: (
            can_use(state, player, "Progressive Hero's Bow", 1)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Dinalfos(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Scales of Time -> Temple of Time Moving Wall Hallways"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Scales of Time -> Temple of Time Floor Switch Puzzle Room"
        ),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 1)
            and can_use(state, player, "Spinner")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Scales of Time -> Temple of Time Upper Spike Trap Corridor"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Upper Spike Trap Corridor -> Temple of Time Scales of Time"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Temple of Time Upper Spike Trap Corridor -> Temple of Time Darknut Arena"
        ),
        lambda state: (
            can_defeat_Lizalfos(state, player)
            and can_defeat_BabyGohma(state, player)
            and can_defeat_YoungGohma(state, player)
            and can_defeat_Armos(state, player)
            and can_use(state, player, "Temple of Time Small Key", 3)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Near Kakariko -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Near Kakariko -> Death Mountain Trail"),
        lambda state: (
            can_use(state, player, "Iron Boots")
            or can_complete_goron_mines(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Trail -> Death Mountain Near Kakariko"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Trail -> Death Mountain Volcano"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Volcano -> Death Mountain Trail"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Volcano -> Death Mountain Outside Sumo Hall"
        ),
        lambda state: (
            can_use(state, player, "Iron Boots")
            and (
                can_defeat_Goron(state, player)
                or can_complete_goron_mines(state, player)
            )
            and can_complete_eldin_twilight(state, player)  # always True
        ),
        lambda state: (
            (can_use(state, player, "Iron Boots") or has_shield(state, player))
            and (
                can_defeat_Goron(state, player)
                or can_complete_goron_mines(state, player)
            )
            and can_complete_eldin_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Volcano -> Death Mountain Elevator Lower"),
        lambda state: (
            state.can_reach_region("Death Mountain Elevator Lower", player)
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_open
            )
        ),
        lambda state: (
            state.can_reach_region("Death Mountain Elevator Lower", player)
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_open
            )
            or (
                has_sword(state, player)
                and (
                    can_do_lja(state, player)
                    or can_use(state, player, "Shadow Crystal")
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Volcano -> Death Mountain Hot Spring"),
        lambda state: (can_defeat_Goron(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Outside Sumo Hall -> Death Mountain Volcano"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Outside Sumo Hall -> Death Mountain Sumo Hall"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Elevator Lower -> Death Mountain Volcano"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Elevator Lower -> Death Mountain Sumo Hall Elevator"
        ),
        lambda state: (can_use(state, player, "Iron Boots")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Elevator Lower -> Death Mountain Hot Spring"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Hot Spring -> Death Mountain Elevator Lower"
        ),
        lambda state: (
            state.can_reach_region("Death Mountain Elevator Lower", player)
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_open
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Death Mountain Hot Spring -> Death Mountain Volcano"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall -> Death Mountain Outside Sumo Hall"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall -> Death Mountain Sumo Hall Elevator"
        ),
        lambda state: (
            can_use(state, player, "Iron Boots")
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_no_wrestling
            )
            or (
                state._tp_goron_mines_enterance(player)
                != GoronMinesEntrance.option_closed
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall -> Death Mountain Sumo Hall Goron Mines Tunnel"
        ),
        lambda state: (
            can_use(state, player, "Iron Boots")
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_no_wrestling
            )
            or (
                state._tp_goron_mines_enterance(player)
                != GoronMinesEntrance.option_closed
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall Elevator -> Death Mountain Elevator Lower"
        ),
        lambda state: (can_use(state, player, "Iron Boots")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall Elevator -> Death Mountain Sumo Hall"
        ),
        lambda state: (
            (
                state.can_reach_region("Death Mountain Sumo Hall", player)
                and can_use(state, player, "Iron Boots")
            )
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_no_wrestling
            )
            or (
                state._tp_goron_mines_enterance(player)
                != GoronMinesEntrance.option_closed
            )
        ),
        lambda state: (
            (
                state.can_reach_region("Death Mountain Sumo Hall", player)
                and can_use(state, player, "Iron Boots")
            )
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_no_wrestling
            )
            or (
                state._tp_goron_mines_enterance(player)
                != GoronMinesEntrance.option_closed
            )
            or can_use(state, player, "Spinner")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall Goron Mines Tunnel -> Death Mountain Sumo Hall"
        ),
        lambda state: (
            (
                state.can_reach_region("Death Mountain Sumo Hall", player)
                and can_use(state, player, "Iron Boots")
            )
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_no_wrestling
            )
            or (
                state._tp_goron_mines_enterance(player)
                != GoronMinesEntrance.option_closed
            )
        ),
        lambda state: (
            (
                state.can_reach_region("Death Mountain Sumo Hall", player)
                and can_use(state, player, "Iron Boots")
            )
            or (
                state._tp_goron_mines_enterance(player)
                == GoronMinesEntrance.option_no_wrestling
            )
            or (
                state._tp_goron_mines_enterance(player)
                != GoronMinesEntrance.option_closed
            )
            or can_use(state, player, "Spinner")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Death Mountain Sumo Hall Goron Mines Tunnel -> Goron Mines Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hidden Village -> Eldin Field Outside Hidden Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hidden Village -> Hidden Village Impaz House"),
        lambda state: (can_use(state, player, "Progressive Hero's Bow", 1)),
    )

    set_rule_if_exits(
        world.get_entrance("Hidden Village Impaz House -> Hidden Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge -> Kakariko Gorge Cave Entrance"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge -> Kakariko Gorge Behind Gate"),
        lambda state: (
            can_complete_eldin_twilight(state, player)  # always True
            or state.can_reach_region("Faron Field", player)
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge -> Faron Field"),
        lambda state: (can_complete_eldin_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge -> Eldin Field"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge -> Kakariko Gorge Keese Grotto"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_eldin_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge Cave Entrance -> Kakariko Gorge"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge Cave Entrance -> Eldin Lantern Cave"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge Behind Gate -> Kakariko Gorge"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            or can_use(state, player, "Gate Keys")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge Behind Gate -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Lantern Cave -> Kakariko Gorge Cave Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Gorge Keese Grotto -> Kakariko Gorge"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Eldin Field Near Castle Town"),
        lambda state: (
            (
                state.can_reach_region("Eldin Field Near Castle Town", player)
                and can_complete_eldin_twilight(state, player)  # always True
                and can_complete_lanayru_twilight(state, player)  # always True
                and state.can_reach_region("Kakariko Malo Mart", player)
            )
            or state._tp_skip_bridge_donation(player)
        ),
        lambda state: (
            (
                (
                    state.can_reach_region("Kakariko Malo Mart", player)
                    or can_use(state, player, "Shadow Crystal")
                )
                and can_complete_eldin_twilight(state, player)  # always True
            )
            or state._tp_skip_bridge_donation(player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Eldin Field Lava Cave Ledge"),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 1)
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Eldin Field From Lava Cave Lower"),
        lambda state: (False),
        lambda state: (
            (
                can_use(state, player, "Shadow Crystal")
                and can_complete_eldin_twilight(state, player)  # always True
            )
            or can_do_lja(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Kakariko Gorge"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Kakariko Village Behind Gate"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> North Eldin Field"),
        lambda state: (can_smash(state, player)),
        lambda state: (
            can_smash(state, player)
            or (
                can_use(state, player, "Shadow Crystal")
                and can_complete_eldin_twilight(state, player)  # always True
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Eldin Field Bomskit Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field -> Eldin Field Water Bomb Fish Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Near Castle Town -> Eldin Field"),
        lambda state: (
            (
                state.can_reach_region("Kakariko Malo Mart", player)
                and can_complete_eldin_twilight(state, player)  # always True
                and can_complete_lanayru_twilight(state, player)  # always True
            )
            or state._tp_skip_bridge_donation(player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Near Castle Town -> Outside Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Lava Cave Ledge -> Eldin Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Eldin Field Lava Cave Ledge -> Eldin Field Lava Cave Upper"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field From Lava Cave Lower -> Eldin Field"),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Eldin Field From Lava Cave Lower -> Eldin Field Lava Cave Lower"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("North Eldin Field -> Eldin Field"),
        lambda state: (can_smash(state, player)),
        lambda state: (
            can_smash(state, player)
            or (
                can_do_map_glitch(state, player)
                and can_complete_eldin_twilight(state, player)  # always True
                and (
                    can_complete_lanayru_twilight(state, player)  # always True
                    or can_use(state, player, "Horse Call")
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("North Eldin Field -> Eldin Field Outside Hidden Village"),
        lambda state: (
            (
                state.can_reach_region("Kakariko Renados Sanctuary", player)
                and can_use(state, player, "Wooden Statue")
            )
            or (state._tp_ilia_quest(player) == IliaQuest.option_charm)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("North Eldin Field -> Eldin Field Grotto Platform"),
        lambda state: (can_use(state, player, "Spinner")),
    )

    set_rule_if_exits(
        world.get_entrance("North Eldin Field -> Lanayru Field"),
        lambda state: (can_complete_eldin_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Outside Hidden Village -> North Eldin Field"),
        lambda state: (
            state.can_reach_region("Kakariko Renados Sanctuary", player)
            and can_use(state, player, "Wooden Statue")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Outside Hidden Village -> Hidden Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Grotto Platform -> North Eldin Field"),
        lambda state: (can_use(state, player, "Spinner")),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Grotto Platform -> Eldin Field Stalfos Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Eldin Field Lava Cave Upper -> Eldin Field Lava Cave Ledge"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Eldin Field Lava Cave Upper -> Eldin Field Lava Cave Lower"
        ),
        lambda state: (can_use(state, player, "Iron Boots")),
        lambda state: (
            can_use(state, player, "Iron Boots")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Eldin Field Lava Cave Lower -> Eldin Field From Lava Cave Lower"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Bomskit Grotto -> Eldin Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Water Bomb Fish Grotto -> Eldin Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Eldin Field Stalfos Grotto -> Eldin Field Grotto Platform"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Upper Kakariko Village"),
        lambda state: (
            (can_complete_goron_mines(state, player) or can_smash(state, player))
            and can_complete_eldin_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Village Behind Gate"),
        lambda state: (can_complete_eldin_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Gorge Behind Gate"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Graveyard"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Death Mountain Near Kakariko"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lower Kakariko Village -> Kakariko Renados Sanctuary Front Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lower Kakariko Village -> Kakariko Renados Sanctuary Front Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lower Kakariko Village -> Kakariko Renados Sanctuary Back Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lower Kakariko Village -> Kakariko Renados Sanctuary Back Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Malo Mart"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Elde Inn Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Elde Inn Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Bug House Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Bug House Ceiling Hole"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lower Kakariko Village -> Kakariko Barnes Bomb Shop Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Kakariko Village -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Kakariko Village -> Kakariko Top of Watchtower"),
        lambda state: (
            can_complete_goron_mines(state, player)
            and can_complete_eldin_twilight(state, player)  # always True
        ),
        lambda state: (
            can_complete_goron_mines(state, player)
            and can_complete_eldin_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Kakariko Village -> Kakariko Barnes Bomb Shop Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Kakariko Village -> Kakariko Watchtower Lower Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Kakariko Village -> Kakariko Watchtower Dig Spot"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Top of Watchtower -> Upper Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Top of Watchtower -> Kakariko Watchtower Upper Door"
        ),
        lambda state: (True),
    )

    # TODO verify "Kakariko Watchtower Upper Door -> Kakariko Top of Watchtower"
    # and "Kakariko Watchtower Upper Door -> Kakariko Watchtower"

    set_rule_if_exits(
        world.get_entrance("Kakariko Village Behind Gate -> Lower Kakariko Village"),
        lambda state: (
            can_use(state, player, "Gate Keys")
            or can_complete_eldin_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Village Behind Gate -> Eldin Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Front Left Door -> Lower Kakariko Village"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Front Left Door -> Kakariko Renados Sanctuary"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Front Right Door -> Lower Kakariko Village"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Front Right Door -> Kakariko Renados Sanctuary"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Back Left Door -> Lower Kakariko Village"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Back Left Door -> Kakariko Renados Sanctuary"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Back Right Door -> Lower Kakariko Village"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Back Right Door -> Kakariko Renados Sanctuary"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Front Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Front Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Back Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Back Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Basement"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Renados Sanctuary Basement -> Kakariko Renados Sanctuary"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Malo Mart -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Elde Inn Left Door -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Elde Inn Left Door -> Kakariko Elde Inn"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Elde Inn Right Door -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Elde Inn Right Door -> Kakariko Elde Inn"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Elde Inn -> Kakariko Elde Inn Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Elde Inn -> Kakariko Elde Inn Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Bug House Door -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Bug House Door -> Kakariko Bug House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Bug House Ceiling Hole -> Kakariko Bug House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Bug House Ceiling Hole -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Bug House -> Kakariko Bug House Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Bug House -> Kakariko Bug House Ceiling Hole"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Barnes Bomb Shop Lower -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Barnes Bomb Shop Lower -> Kakariko Barnes Bomb Shop Upper"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Barnes Bomb Shop Upper -> Upper Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Barnes Bomb Shop Upper -> Kakariko Barnes Bomb Shop Lower"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower Lower Door -> Upper Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower Lower Door -> Kakariko Watchtower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower Dig Spot -> Upper Kakariko Village"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower Dig Spot -> Kakariko Watchtower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Kakariko Watchtower Upper Door -> Kakariko Top of Watchtower"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower Upper Door -> Kakariko Watchtower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower -> Kakariko Watchtower Lower Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower -> Kakariko Watchtower Dig Spot"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Watchtower -> Kakariko Watchtower Upper Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Graveyard -> Lower Kakariko Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Kakariko Graveyard -> Lake Hylia"),
        lambda state: (
            can_use(state, player, "Gate Keys")
            and (
                can_use(state, player, "Iron Boots")
                or can_use(state, player, "Zora Armor")
            )
            and can_use_water_bombs(state, player)
            and can_complete_eldin_twilight(state, player)  # always True
        ),
        lambda state: (
            (
                has_heavy_mod(state, player)
                and can_use_water_bombs(state, player)
                and can_use(state, player, "Gate Keys")
                and can_complete_eldin_twilight(state, player)  # always True
            )
            or (
                (has_heavy_mod(state, player) or can_use(state, player, "Zora Armor"))
                and (
                    (
                        has_bombs(state, player)
                        and (
                            has_sword(state, player)
                            or can_use(state, player, "Spinner")
                        )
                    )
                    or can_do_lja(state, player)
                    or can_do_moon_boots(state, player)
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods -> South Faron Woods Behind Gate"),
        lambda state: (
            can_use(state, player, "Faron Woods Coro Key")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods -> South Faron Woods Owl Statue Area"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods -> Ordon Bridge"),
        lambda state: (
            can_complete_prologue(state, player)  # always True
            and can_complete_faron_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods -> Faron Field"),
        lambda state: (
            can_clear_forest(state, player)
            and can_complete_faron_twilight(state, player)  # always True
            and can_complete_prologue(state, player)  # always True
        ),
        lambda state: (
            can_clear_forest_glitched(state, player)
            and can_complete_faron_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods -> Faron Woods Coros House Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods Behind Gate -> South Faron Woods"),
        lambda state: (
            can_use(state, player, "Faron Woods Coro Key")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "South Faron Woods Behind Gate -> Faron Woods Cave Southern Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods Coros Ledge -> South Faron Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "South Faron Woods Coros Ledge -> Faron Woods Coros House Upper"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("South Faron Woods Owl Statue Area -> South Faron Woods"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "South Faron Woods Owl Statue Area -> South Faron Woods Above Owl Statue"
        ),
        lambda state: (
            can_clear_forest(state, player)
            and can_use(state, player, "Progressive Dominion Rod", 2)
            and can_use(state, player, "Shadow Crystal")
            and can_complete_faron_twilight(state, player)  # always True
        ),
        lambda state: (
            can_clear_forest_glitched(state, player)
            and can_use(state, player, "Progressive Dominion Rod", 2)
            and can_use(state, player, "Shadow Crystal")
            and can_complete_faron_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "South Faron Woods Above Owl Statue -> South Faron Woods Owl Statue Area"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "South Faron Woods Above Owl Statue -> Mist Area Near Owl Statue Chest"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Faron Woods Coros House Lower -> Faron Woods Coros House Upper"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Woods Coros House Lower -> South Faron Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Faron Woods Coros House Upper -> Faron Woods Coros House Lower"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Faron Woods Coros House Upper -> South Faron Woods Coros Ledge"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Faron Woods Cave Southern Entrance -> South Faron Woods Behind Gate"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Woods Cave Southern Entrance -> Faron Woods Cave"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Woods Cave -> Faron Woods Cave Southern Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Woods Cave -> Faron Woods Cave Northern Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Near Faron Woods Cave -> Mist Area Inside Mist"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern") or can_do_map_glitch(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near Faron Woods Cave -> Mist Area Under Owl Statue Chest"
        ),
        lambda state: (
            can_use(state, player, "Lantern")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near Faron Woods Cave -> Faron Woods Cave Northern Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Inside Mist -> Mist Area Near Faron Woods Cave"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern")
            or (
                state.can_reach_region("South Faron Woods", player)
                and can_do_map_glitch(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Inside Mist -> Mist Area Under Owl Statue Chest"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern") or can_do_map_glitch(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Inside Mist -> Mist Area Outside Faron Mist Cave"
        ),
        lambda state: (
            can_use(state, player, "Lantern")
            and (
                can_complete_faron_twilight(state, player)  # always True
                or can_use(state, player, "Shadow Crystal")
            )
        ),
        lambda state: (
            can_use(state, player, "Lantern")
            or (
                state.can_reach_region("South Faron Woods", player)
                and can_do_map_glitch(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Inside Mist -> Mist Area Near North Faron Woods"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern")
            or (
                state.can_reach_region("South Faron Woods", player)
                and can_do_map_glitch(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Under Owl Statue Chest -> Mist Area Inside Mist"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern") or can_do_map_glitch(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Under Owl Statue Chest -> Mist Area Center Stump"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near Owl Statue Chest -> Mist Area Under Owl Statue Chest"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near Owl Statue Chest -> South Faron Woods Above Owl Statue"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Center Stump -> Mist Area Inside Mist"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern") or can_do_map_glitch(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Center Stump -> Mist Area Near North Faron Woods"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Outside Faron Mist Cave -> Mist Area Inside Mist"
        ),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern") or can_do_map_glitch(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Outside Faron Mist Cave -> Mist Area Faron Mist Cave"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Mist Area Near North Faron Woods -> Mist Area Inside Mist"),
        lambda state: (can_use(state, player, "Lantern")),
        lambda state: (
            can_use(state, player, "Lantern") or can_do_map_glitch(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near North Faron Woods -> Mist Area Near Faron Woods Cave"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near North Faron Woods -> Mist Area Near North Faron Woods Behind Gate"
        ),
        lambda state: (can_use(state, player, "North Faron Woods Gate Key")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near North Faron Woods Behind Gate -> Mist Area Near North Faron Woods"
        ),
        lambda state: (can_use(state, player, "North Faron Woods Gate Key")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Near North Faron Woods Behind Gate -> North Faron Woods"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("North Faron Lost Woods Entrance -> Lost Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Faron Woods Cave Northern Entrance -> Mist Area Near Faron Woods Cave"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Woods Cave Northern Entrance -> Faron Woods Cave"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Mist Area Faron Mist Cave -> Mist Area Outside Faron Mist Cave"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("North Faron Woods -> Forest Temple Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "North Faron Woods -> Mist Area Near North Faron Woods Behind Gate"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("North Faron Woods -> North Faron Lost Woods Entrance"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_faron_twilight(state, player)  # always True
        ),
        lambda state: (
            (
                can_use(state, player, "Shadow Crystal")
                and can_complete_faron_twilight(state, player)  # always True
            )
            or (has_bombs(state, player) and can_do_lja(state, player))
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field -> South Faron Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field -> Kakariko Gorge"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field -> Lake Hylia Bridge"),
        lambda state: (can_use(state, player, "Gate Keys")),
        lambda state: (
            can_use(state, player, "Gate Keys")
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field -> Faron Field Corner Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field -> Faron Field Fishing Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field -> Outside Castle Town South"),
        lambda state: (
            can_get_hot_spring_water(state, player)
            and state.can_reach_region("Outside Castle Town South", player)
        ),
        lambda state: (
            state.can_reach_region("Castle Town South", player)
            and has_bottle(state, player)
            and state.can_reach_region("Outside Castle Town South", player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field Corner Grotto -> Faron Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Faron Field Fishing Grotto -> Faron Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lost Woods -> Lost Woods Lower Battle Arena"),
        lambda state: (
            (
                can_defeat_SkullKid(state, player)
                and can_use(state, player, "Shadow Crystal")
            )
            or (state._tp_grove_entrance(player))
        ),
        lambda state: (
            (
                can_defeat_SkullKid(state, player)
                and can_use(state, player, "Shadow Crystal")
            )
            or (state._tp_grove_entrance(player))
            or can_do_js_moon_boots(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lost Woods -> Lost Woods Upper Battle Arena"),
        lambda state: (
            (
                can_defeat_SkullKid(state, player)
                and can_use(state, player, "Shadow Crystal")
            )
            or (state._tp_grove_entrance(player))
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lost Woods -> North Faron Lost Woods Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lost Woods Lower Battle Arena -> Lost Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lost Woods Lower Battle Arena -> Sacred Grove Lower"),
        lambda state: (
            can_defeat_SkullKid(state, player) or (state._tp_grove_entrance(player))
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lost Woods Lower Battle Arena -> Lost Woods Baba Serpent Grotto"
        ),
        lambda state: (
            can_smash(state, player) and can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lost Woods Upper Battle Arena -> Sacred Grove Before Block"
        ),
        lambda state: (
            can_defeat_SkullKid(state, player) or (state._tp_grove_entrance(player))
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lost Woods Baba Serpent Grotto -> Lost Woods Lower Battle Arena"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Sacred Grove Before Block -> Lost Woods Upper Battle Arena"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Before Block -> Sacred Grove Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Upper -> Sacred Grove Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Upper -> Sacred Grove Past"),
        lambda state: (can_strike_pedestal(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Lower -> Lost Woods Lower Battle Arena"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Lower -> Sacred Grove Upper"),
        lambda state: (
            state.can_reach_region("Sacred Grove Before Block", player)
            or (state._tp_grove_entrance(player))
        ),
        lambda state: (
            state.can_reach_region("Sacred Grove Before Block", player)
            or (state._tp_grove_entrance(player))
            or can_do_js_moon_boots(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Past -> Sacred Grove Past Behind Window"),
        lambda state: (can_strike_pedestal(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Past -> Sacred Grove Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Sacred Grove Past Behind Window -> Sacred Grove Past"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Sacred Grove Past Behind Window -> Temple of Time Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Cave of Ordeals Floors 01-11 -> Gerudo Desert Cave of Ordeals Plateau"
        ),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Cave of Ordeals Floors 01-11 -> Gerudo Desert Cave of Ordeals Floors 12-21"
        ),
        lambda state: (
            can_use(state, player, "Spinner")
            and can_defeat_Bokoblin(state, player)
            and can_defeat_Keese(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_HangingBabaSerpent(state, player)
            and can_defeat_Skulltula(state, player)
            and can_defeat_Bulblin(state, player)
            and can_defeat_TorchSlug(state, player)
            and can_defeat_FireKeese(state, player)
            and can_defeat_Dodongo(state, player)
            and can_defeat_Tektite(state, player)
            and can_defeat_Lizalfos(state, player)
        ),
        lambda state: (
            (can_use(state, player, "Spinner") or can_do_lja(state, player))
            and can_defeat_Bokoblin(state, player)
            and can_defeat_Keese(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_HangingBabaSerpent(state, player)
            and can_defeat_Skulltula(state, player)
            and can_defeat_Bulblin(state, player)
            and can_defeat_TorchSlug(state, player)
            and can_defeat_FireKeese(state, player)
            and can_defeat_Dodongo(state, player)
            and can_defeat_Tektite(state, player)
            and can_defeat_Lizalfos(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Cave of Ordeals Floors 12-21 -> Gerudo Desert Cave of Ordeals Floors 22-31"
        ),
        lambda state: (
            can_defeat_Helmasaur(state, player)
            and can_defeat_Rat(state, player)
            and can_use(state, player, "Ball and Chain")
            and can_defeat_Chu(state, player)
            and can_defeat_ChuWorm(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Bulblin(state, player)
            and can_defeat_Keese(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_Stalhound(state, player)
            and can_defeat_Poe(state, player)
            and can_defeat_Leever(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Cave of Ordeals Floors 22-31 -> Gerudo Desert Cave of Ordeals Floors 32-41"
        ),
        lambda state: (
            can_defeat_Bokoblin(state, player)
            and can_defeat_IceKeese(state, player)
            and can_use(state, player, "Progressive Dominion Rod", 2)
            and can_defeat_Keese(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_GhoulRat(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Bulblin(state, player)
            and can_defeat_Stalfos(state, player)
            and can_defeat_Skulltula(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_FireBubble(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Cave of Ordeals Floors 32-41 -> Gerudo Desert Cave of Ordeals Floors 42-50"
        ),
        lambda state: (
            can_defeat_Beamos(state, player)
            and can_defeat_Keese(state, player)
            and can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_TorchSlug(state, player)
            and can_defeat_FireKeese(state, player)
            and can_defeat_Dodongo(state, player)
            and can_defeat_FireBubble(state, player)
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Poe(state, player)
            and can_defeat_GhoulRat(state, player)
            and can_defeat_Chu(state, player)
            and can_defeat_IceKeese(state, player)
            and can_defeat_Freezard(state, player)
            and can_defeat_Chilfos(state, player)
            and can_defeat_IceBubble(state, player)
            and can_defeat_Leever(state, player)
            and can_defeat_Darknut(state, player)
        ),
        lambda state: (
            can_defeat_Beamos(state, player)
            and can_defeat_Keese(state, player)
            and (
                can_use(state, player, "Progressive Clawshot", 2)
                or can_do_lja(state, player)
            )
            and can_defeat_TorchSlug(state, player)
            and can_defeat_FireKeese(state, player)
            and can_defeat_Dodongo(state, player)
            and can_defeat_FireBubble(state, player)
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Poe(state, player)
            and can_defeat_GhoulRat(state, player)
            and can_defeat_Chu(state, player)
            and can_defeat_IceKeese(state, player)
            and can_defeat_Freezard(state, player)
            and can_defeat_Chilfos(state, player)
            and can_defeat_IceBubble(state, player)
            and can_defeat_Leever(state, player)
            and can_defeat_Darknut(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert -> Gerudo Desert Cave of Ordeals Plateau"),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 1)
            and can_defeat_ShadowBeast(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert -> Gerudo Desert Basin"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert -> Gerudo Desert Skulltula Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Cave of Ordeals Plateau -> Gerudo Desert"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Cave of Ordeals Plateau -> Gerudo Desert Cave of Ordeals Floors 01-11"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Basin -> Gerudo Desert"),
        lambda state: (can_defeat_Bulblin(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Basin -> Gerudo Desert North East Ledge"),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Basin -> Gerudo Desert Outside Bulblin Camp"),
        lambda state: (can_defeat_Bulblin(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Basin -> Gerudo Desert Chu Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert North East Ledge -> Gerudo Desert Basin"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert North East Ledge -> Gerudo Desert Rock Grotto"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Outside Bulblin Camp -> Gerudo Desert Basin"),
        lambda state: (
            state.can_reach_region("Gerudo Desert Basin", player)
            and can_defeat_Bulblin(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Outside Bulblin Camp -> Bulblin Camp"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Skulltula Grotto -> Gerudo Desert"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Gerudo Desert Chu Grotto -> Gerudo Desert Basin"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Gerudo Desert Rock Grotto -> Gerudo Desert North East Ledge"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Bulblin Camp -> Gerudo Desert Outside Bulblin Camp"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Bulblin Camp -> Outside Arbiters Grounds"),
        lambda state: (
            (
                can_use(state, player, "Gerudo Desert Bulblin Camp Key")
                and can_defeat_KingBulblinDesert(state, player)
            )
            or state._tp_skip_arbiters_entrance(player)
        ),
        lambda state: (
            (
                can_defeat_KingBulblinDesert(state, player)
                and (
                    can_use(state, player, "Gerudo Desert Bulblin Camp Key")
                    or (can_do_map_glitch(state, player) and has_sword(state, player))
                )
            )
            or state._tp_skip_arbiters_entrance(player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Arbiters Grounds -> Bulblin Camp"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Arbiters Grounds -> Arbiters Grounds Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Mirror Chamber Lower -> Arbiters Grounds Boss Room"),
        lambda state: (
            state.can_reach_region("Arbiters Grounds Boss Room", player)
            and can_defeat_Stallord(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mirror Chamber Lower -> Mirror Chamber Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Mirror Chamber Upper -> Mirror Chamber Lower"),
        lambda state: (
            can_defeat_ShadowBeast(state, player)
            or (
                can_use(state, player, "Shadow Crystal")
                and can_use(state, player, "Mirror Chamber Portal Item")
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mirror Chamber Upper -> Mirror Chamber Portal"),
        lambda state: (
            (
                can_defeat_ShadowBeast(state, player)
                or (
                    can_use(state, player, "Shadow Crystal")
                    and can_use(state, player, "Mirror Chamber Portal Item")
                )
            )
            and (
                (
                    state._tp_palace_requirements(player)
                    == PalaceRequirements.option_open
                )
                or (
                    (
                        state._tp_palace_requirements(player)
                        == PalaceRequirements.option_fused_shadows
                    )
                    and can_use(state, player, "Progressive Fused Shadow", 3)
                )
                or (
                    (
                        state._tp_palace_requirements(player)
                        == PalaceRequirements.option_mirror_shards
                    )
                    and can_use(state, player, "Progressive Mirror Shard", 4)
                )
                or (
                    (
                        state._tp_palace_requirements(player)
                        == PalaceRequirements.option_vanilla
                    )
                    and can_complete_city_in_the_sky(state, player)
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mirror Chamber Portal -> Mirror Chamber Upper"),
        lambda state: (
            can_defeat_ShadowBeast(state, player)
            or (
                can_use(state, player, "Shadow Crystal")
                and can_use(state, player, "Mirror Chamber Portal Item")
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Mirror Chamber Portal -> Palace of Twilight Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town West -> Outside Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town West -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town West -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town West -> Castle Town STAR Game"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always true
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town STAR Game -> Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town North"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town Goron House Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town Goron House Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Center -> Castle Town Malo Mart"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always true
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Goron House Left Door -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Goron House Left Door -> Castle Town Goron House"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Goron House Right Door -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Goron House Right Door -> Castle Town Goron House"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Goron House -> Castle Town Goron House Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Goron House -> Castle Town Goron House Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Goron House Balcony -> Castle Town Goron House"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Goron House -> Castle Town Goron House Balcony"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Malo Mart -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town North -> Castle Town North Behind First Door"),
        lambda state: (can_complete_MDH(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town North -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town North Behind First Door -> Castle Town North"),
        lambda state: (can_complete_MDH(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town North Behind First Door -> Castle Town North Inside Barrier"
        ),
        lambda state: (can_break_hc_barrier(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town North Inside Barrier -> Castle Town North Behind First Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town North Inside Barrier -> Hyrule Castle Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town East -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town East -> Outside Castle Town East"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town East -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town East -> Castle Town Doctors Office Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town East -> Castle Town Doctors Office Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Doctors Office Balcony -> Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Balcony -> Castle Town Doctors Office Upper"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Doctors Office Left Door -> Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Left Door -> Castle Town Doctors Office Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Doctors Office Right Door -> Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Right Door -> Castle Town Doctors Office Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Entrance -> Castle Town Doctors Office Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Entrance -> Castle Town Doctors Office Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Entrance -> Castle Town Doctors Office Lower"
        ),
        lambda state: (
            can_use(state, player, "Invoice")
            or (state._tp_ilia_quest(player) == IliaQuest.option_statue)
            or (state._tp_ilia_quest(player) == IliaQuest.option_charm)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Lower -> Castle Town Doctors Office Entrance"
        ),
        lambda state: (
            can_use(state, player, "Invoice")
            or (state._tp_ilia_quest(player) == IliaQuest.option_statue)
            or (state._tp_ilia_quest(player) == IliaQuest.option_charm)
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Lower -> Castle Town Doctors Office Upper"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Upper -> Castle Town Doctors Office Lower"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Castle Town Doctors Office Upper -> Castle Town Doctors Office Balcony"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town Center"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town Agithas House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town Seer House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town Jovanis House"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> Castle Town Telmas Bar"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town South -> South Castle Town Doors"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("South Castle Town Doors -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("South Castle Town Doors -> Outside Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Agithas House -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Seer House -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Jovanis House -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Castle Town Telmas Bar -> Castle Town South"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Lanayru Field Cave Entrance"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Lanayru Field Behind Boulder"),
        lambda state: (can_smash(state, player)),
        lambda state: (can_smash(state, player) or can_do_map_glitch(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Hyrule Field Near Spinner Rails"),
        lambda state: (can_smash(state, player)),
        lambda state: (
            can_smash(state, player)
            or (
                can_do_map_glitch(state, player)
                and can_complete_lanayru_twilight(state, player)  # always True
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> North Eldin Field"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Outside Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Lanayru Field Chu Grotto"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Lanayru Field Skulltula Grotto"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field -> Lanayru Field Poe Grotto"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Cave Entrance -> Lanayru Field"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Cave Entrance -> Lanayru Ice Puzzle Cave"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Behind Boulder -> Lanayru Field"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Behind Boulder -> Zoras Domain West Ledge"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Field Near Spinner Rails -> Lanayru Field"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Hyrule Field Near Spinner Rails -> Lake Hylia Bridge"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Ice Puzzle Cave -> Lanayru Field Cave Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Chu Grotto -> Lanayru Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Skulltula Grotto -> Lanayru Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lanayru Field Poe Grotto -> Lanayru Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Outside Castle Town West -> Outside Castle Town West Grotto Ledge"
        ),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and (
                can_use(state, player, "Progressive Clawshot", 1)
                or can_do_map_glitch(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town West -> Lanayru Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town West -> Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town West -> Lake Hylia Bridge"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Outside Castle Town West Grotto Ledge -> Outside Castle Town West"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Outside Castle Town West Grotto Ledge -> Outside Castle Town West Helmasaur Grotto"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Outside Castle Town West Helmasaur Grotto -> Outside Castle Town West Grotto Ledge"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town East -> Eldin Field Near Castle Town"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town East -> Castle Town East"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town South -> Lake Hylia"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Outside Castle Town South -> Outside Castle Town South Tektite Grotto"
        ),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town South -> Faron Field"),
        lambda state: (can_get_hot_spring_water(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Castle Town South -> South Castle Town Doors"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Outside Castle Town South Tektite Grotto -> Outside Castle Town South"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Bridge -> Lake Hylia Bridge Grotto Ledge"),
        lambda state: (
            can_launch_bombs(state, player)
            and can_use(state, player, "Progressive Clawshot", 1)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Bridge -> Hyrule Field Near Spinner Rails"),
        lambda state: (can_smash(state, player)),
        lambda state: (can_smash(state, player) or can_do_map_glitch(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Bridge -> Outside Castle Town West"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Bridge -> Faron Field"),
        lambda state: (
            can_use(state, player, "Gate Keys")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
        lambda state: (
            (
                can_use(state, player, "Gate Keys")
                or can_use(state, player, "Shadow Crystal")
            )
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Bridge -> Lake Hylia Flight By Fowl"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Bridge Grotto Ledge -> Lake Hylia Bridge"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lake Hylia Bridge Grotto Ledge -> Lake Hylia Bridge Bubble Grotto"
        ),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lake Hylia Bridge Bubble Grotto -> Lake Hylia Bridge Grotto Ledge"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Lake Hylia Cave Entrance"),
        lambda state: (
            can_smash(state, player) and can_warp_meteor(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Lake Hylia Lakebed Temple Entrance"),
        lambda state: (
            can_use(state, player, "Zora Armor")
            and (
                state._tp_skip_lakebed_entrance(player)
                or (
                    can_use(state, player, "Iron Boots")
                    and can_use_water_bombs(state, player)
                )
            )
        ),
        lambda state: (
            can_use(state, player, "Zora Armor") or can_do_air_refill(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Gerudo Desert"),
        lambda state: (
            can_use(state, player, "Auru's Memo")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Upper Zoras River"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Lake Hylia Lanayru Spring"),
        lambda state: (can_warp_meteor(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lake Hylia Flight By Fowl -> Lake Hylia Shell Blade Grotto"
        ),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Flight By Fowl -> Lake Hylia"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Flight By Fowl -> Lake Hylia Bridge"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Lake Hylia Water Toadpoli Grotto"),
        lambda state: (
            can_use(state, player, "Shadow Crystal")
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> City in The Sky Entrance"),
        lambda state: (
            (
                can_use(state, player, "Progressive Sky Book", 7)
                or state._tp_skip_city_in_the_sky_entrance(player)
            )
            and can_use(state, player, "Progressive Clawshot", 1)
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia -> Lake Hylia Flight By Fowl"),
        lambda state: (can_complete_lanayru_twilight(state, player)),  # always True
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Cave Entrance -> Lake Hylia"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Cave Entrance -> Lake Hylia Long Cave"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Lakebed Temple Entrance -> Lake Hylia"),
        lambda state: (
            can_use(state, player, "Zora Armor")
            and (
                state._tp_skip_lakebed_entrance(player)
                or (
                    can_use(state, player, "Iron Boots")
                    and can_use_water_bombs(state, player)
                )
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lake Hylia Lakebed Temple Entrance -> Lakebed Temple Entrance"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Lanayru Spring -> Lake Hylia"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Long Cave -> Lake Hylia Cave Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Lake Hylia Shell Blade Grotto -> Lake Hylia Flight By Fowl"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Lake Hylia Water Toadpoli Grotto -> Lake Hylia"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Zoras River -> Lanayru Field"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Zoras River -> Fishing Hole"),
        lambda state: (
            (
                state.can_reach_region("Zoras Domain Throne Room", player)
                and can_complete_eldin_twilight(state, player)  # always True
            )
            or can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Zoras River -> Zoras Domain"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Zoras River -> Upper Zoras River Izas House"),
        lambda state: (
            (
                has_sword(state, player)
                or (
                    can_defeat_ShadowBeast(state, player)
                    and state._tp_transform_anywhere(player)
                )
                or can_use(state, player, "Upper Zoras River Portal Item")
            )
            and can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Zoras River Izas House -> Upper Zoras River"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Upper Zoras River Izas House -> Lake Hylia"),
        lambda state: (can_use(state, player, "Progressive Hero's Bow", 1)),
    )

    set_rule_if_exits(
        world.get_entrance("Fishing Hole -> Upper Zoras River"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Fishing Hole -> Fishing Hole House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Fishing Hole -> Fishing Hole Piece of Heart"),
        lambda state: (can_use(state, player, "Progressive Clawshot", 1)),
    )

    set_rule_if_exits(
        world.get_entrance("Fishing Hole House -> Fishing Hole"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Fishing Hole House -> Fishing Hole Piece of Heart"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain -> Zoras Domain West Ledge"),
        lambda state: (
            can_use(state, player, "Progressive Clawshot", 1)
            or can_use(state, player, "Shadow Crystal")
            or can_smash(state, player)
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain -> Upper Zoras River"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain -> Zoras Domain Snowpeak Entrance"),
        lambda state: (
            (
                state.can_reach_region("Zoras Domain Throne Room", player)
                and can_complete_eldin_twilight(state, player)  # always True
                and can_use(state, player, "Ball and Chain")
            )
            or can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain -> Zoras Domain Top of Waterfall"),
        lambda state: (
            can_warp_meteor(state, player)  # always True
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain Snowpeak Entrance -> Snowpeak Climb Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain Snowpeak Entrance -> Zoras Domain"),
        lambda state: (
            can_use(state, player, "Ball and Chain")
            or can_complete_lanayru_twilight(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain West Ledge -> Zoras Domain"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain West Ledge -> Lanayru Field Behind Boulder"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain West Ledge -> Zoras Domain Top of Waterfall"),
        lambda state: (can_smash(state, player)),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain Throne Room -> Zoras Domain Top of Waterfall"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain Top of Waterfall -> Zoras Domain"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Zoras Domain Top of Waterfall -> Zoras Domain Throne Room"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Links House -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Links House -> Ordon Spring"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Outside Links House -> Ordon Links House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Links House -> Outside Links House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Outside Links House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Ordon Ranch Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Ordon Seras Shop"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Ordon Shield House Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Ordon Sword House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Ordon Bos House Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Village -> Ordon Bos House Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Seras Shop -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Shield House Lower -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Shield House Lower -> Ordon Shield House Upper"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Shield House Upper -> Ordon Shield House Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Shield House Upper -> Ordon Village"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Sword House -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bos House Left Door -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bos House Left Door -> Ordon Bos House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bos House Right Door -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bos House Right Door -> Ordon Bos House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bos House -> Ordon Bos House Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bos House -> Ordon Bos House Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch Entrance -> Ordon Ranch"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch Entrance -> Ordon Village"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch -> Ordon Ranch Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch -> Ordon Ranch Stable"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch Stable -> Ordon Ranch"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch Stable -> Ordon Ranch Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Ranch Grotto -> Ordon Ranch Stable"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Spring -> Outside Links House"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Spring -> Ordon Bridge"),
        lambda state: (
            (
                state.can_reach_region("Outside Links House", player)
                and has_sword(state, player)
                and can_use(state, player, "Slingshot")
            )
            or can_complete_prologue(state, player)  # always True
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bridge -> Ordon Spring"),
        lambda state: (
            (
                state.can_reach_region("Outside Links House", player)
                and has_sword(state, player)
                and can_use(state, player, "Slingshot")
            )
            or can_complete_prologue(state, player)  # always True
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Ordon Bridge -> South Faron Woods"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Climb Lower -> Snowpeak Climb Upper"),
        lambda state: (
            (
                state._tp_skip_snowpeak_entrance(player)
                or (
                    state.can_reach_region("Zoras Domain", player)
                    and can_use(state, player, "Progressive Fishing Rod", 2)
                )
            )
            and can_use(state, player, "Shadow Crystal")
        ),
        lambda state: (
            (
                state._tp_skip_snowpeak_entrance(player)
                or (
                    state.can_reach_region("Zoras Domain", player)
                    and can_use(state, player, "Progressive Fishing Rod", 2)
                )
            )
            or can_use(state, player, "Shadow Crystal")
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Climb Lower -> Zoras Domain Snowpeak Entrance"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Climb Upper -> Snowpeak Climb Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Climb Upper -> Snowpeak Summit Upper"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Climb Upper -> Snowpeak Ice Keese Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Climb Upper -> Snowpeak Freezard Grotto"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Ice Keese Grotto -> Snowpeak Climb Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Freezard Grotto -> Snowpeak Climb Upper"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Summit Upper -> Snowpeak Summit Lower"),
        lambda state: (
            (
                can_use(state, player, "Snowpeak Portal Item")
                or can_defeat_ShadowBeast(state, player)
            )
            and (
                (
                    not state._tp_bonks_do_damage(player)
                    or (
                        state._tp_bonks_do_damage(player)
                        and (
                            (
                                state._tp_damage_magnification(player)
                                != DamageMagnification.option_ohko
                            )
                            or can_use_bottled_fairy(state, player)
                        )
                    )
                )
                or can_complete_snowpeak_ruins(state, player)
            )
        ),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Summit Upper -> Snowpeak Climb Upper"),
        lambda state: (can_use(state, player, "Shadow Crystal")),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Summit Lower -> Snowpeak Summit Lower Left Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Summit Lower -> Snowpeak Summit Lower Right Door"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Summit Lower Left Door -> Snowpeak Ruins Left Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Summit Lower Left Door -> Snowpeak Summit Lower"),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance(
            "Snowpeak Summit Lower Right Door -> Snowpeak Ruins Right Door"
        ),
        lambda state: (True),
    )

    set_rule_if_exits(
        world.get_entrance("Snowpeak Summit Lower Right Door -> Snowpeak Summit Lower"),
        lambda state: (True),
    )
