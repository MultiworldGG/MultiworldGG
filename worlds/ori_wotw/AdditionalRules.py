"""Additional location rules that are not extracted from `areas.wotw`."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import WotWWorld

from worlds.generic.Rules import set_rule

from .Options import LogicDifficulty


def combat_rules(world: WotWWorld):
    """Defines rules for combat and light."""
    player = world.player
    options = world.options
    diff = options.difficulty

    if diff == LogicDifficulty.option_moki:
        world.connect_to_menu("DepthsLight", rule=lambda s: s.has_any(("UpperDepths.ForestsEyes", "Flash"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s: s.has_any(("Bow", "Spear"), player))
        world.connect_to_menu("Combat.Aerial",
                              rule=lambda s: s.has_any(("Double Jump", "Launch"), player))
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: s.has("Bash", player))
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has_any(("Sword", "Hammer", "Bow"), player))

    elif diff == LogicDifficulty.option_gorlek:  # Gorlek
        world.connect_to_menu("DepthsLight",
                              rule=lambda s: s.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s: s.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear"), player))
        world.connect_to_menu("Combat.Aerial",
                              rule=lambda s: s.has_any(("Double Jump", "Launch", "Bash"), player))
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: s.has("Bash", player))
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    elif diff == LogicDifficulty.option_kii:  # Kii
        world.connect_to_menu("DepthsLight",
                              rule=lambda s: s.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s: s.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear"), player))
        world.connect_to_menu("Combat.Aerial", rule=lambda s: True)
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: True)
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    else:  # diff == LogicDifficulty.option_unsafe
        world.connect_to_menu("DepthsLight",
                              rule=lambda s: s.has_any(("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s:
                              s.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"), player))
        world.connect_to_menu("Combat.Aerial", rule=lambda s: True)
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has_any(("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has_any(("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: True)
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has_any(("Sword", "Hammer", "Bow", "Shuriken", "Grenade", "Spear"),
                                                       player))


def unreachable_rules(world: WotWWorld):
    """Rules to handle unreachable events."""
    player = world.player
    options = world.options
    diff = options.difficulty
    unreach: list[str]
    if diff == LogicDifficulty.option_moki:
        unreach = ["WestHollow.AboveJumppad -> WestHollow.LowerTongueRetracted",
                   "OuterWellspring.EntranceDoor -> OuterWellspring.FallingWheel",
                   "UpperWastes.OutsideRuins -> UpperWastes.WormEscapeEnd",
                   "MarshSpawn.PoolsBurrowsSignpost -> E.MarshSpawn.PoolsBurrowsSignpost",
                   "OuterWellspring.EntranceDoor -> H.OuterWellspring.EntranceDoor",
                   "OuterWellspring.EntranceDoor -> E.OuterWellspring.EntranceDoor",
                   "WoodsMain.TrialStart -> C.WoodsMain.TrialStart",
                   "WoodsMain.AbovePit -> E.WoodsMain.AbovePit",
                   "UpperReach.TreeRoom -> C.UpperReach.TreeRoom",
                   "UpperDepths.FirstKSRoom -> C.UpperDepths.FirstKSRoom",
                   "UpperDepths.FirstKSRoom -> E.UpperDepths.FirstKSRoom",
                   "UpperDepths.Central -> E.UpperDepths.Central",
                   "LowerDepths.West -> H.LowerDepths.West",
                   "LowerDepths.West -> E.LowerDepths.West",
                   "UpperWastes.MissilePuzzleMiddle -> C.UpperWastes.MissilePuzzleMiddle",
                   "WillowsEnd.Upper -> E.WillowsEnd.Upper"]
    elif diff == LogicDifficulty.option_gorlek:
        unreach = ["OuterWellspring.EntranceDoor -> OuterWellspring.FallingWheel",
                   "UpperWastes.OutsideRuins -> UpperWastes.WormEscapeEnd",
                   "MarshSpawn.PoolsBurrowsSignpost -> E.MarshSpawn.PoolsBurrowsSignpost",
                   "OuterWellspring.EntranceDoor -> E.OuterWellspring.EntranceDoor",
                   "WoodsMain.TrialStart -> C.WoodsMain.TrialStart",
                   "WoodsMain.AbovePit -> E.WoodsMain.AbovePit",
                   "UpperReach.TreeRoom -> C.UpperReach.TreeRoom",
                   "UpperDepths.FirstKSRoom -> C.UpperDepths.FirstKSRoom",
                   "UpperDepths.FirstKSRoom -> E.UpperDepths.FirstKSRoom",
                   "UpperDepths.Central -> E.UpperDepths.Central"]
    elif diff == LogicDifficulty.option_kii:
        unreach = ["OuterWellspring.EntranceDoor -> OuterWellspring.FallingWheel",
                   "UpperWastes.OutsideRuins -> UpperWastes.WormEscapeEnd",
                   "OuterWellspring.EntranceDoor -> E.OuterWellspring.EntranceDoor",
                   "WoodsMain.TrialStart -> C.WoodsMain.TrialStart",
                   "WoodsMain.AbovePit -> E.WoodsMain.AbovePit",
                   "UpperReach.TreeRoom -> C.UpperReach.TreeRoom",
                   "UpperDepths.FirstKSRoom -> C.UpperDepths.FirstKSRoom",
                   "UpperDepths.FirstKSRoom -> E.UpperDepths.FirstKSRoom",
                   "UpperDepths.Central -> E.UpperDepths.Central"]
    else:  # diff == LogicDifficulty.option_unsafe
        unreach = []

    for entr in unreach:  # Connect these events when the seed is completed, to make them reachable.
        set_rule(world.get_entrance(entr), lambda s: s.has("Victory", player))


def ut_combat_rules(world: WotWWorld, one_level: bool, max_logic: bool):
    """Defines rules for combat and light, used by UT for glitched logic."""
    player = world.player
    options = world.options
    diff = options.difficulty

    # Gorlek
    if diff == LogicDifficulty.option_moki and one_level and not max_logic:
        world.connect_to_menu("DepthsLight",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Grenade", "Bow", "Shuriken", "Sentry", "Spear"), player))
        world.connect_to_menu("Combat.Aerial",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(("Double Jump", "Launch", "Bash"),
                                                                                     player))
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: s.has("UTGlitch", player) and s.has("Bash", player))
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("UTGlitch", player) and s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    # Kii
    if diff == LogicDifficulty.option_gorlek and one_level and not max_logic:
        world.connect_to_menu("DepthsLight",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Grenade", "Bow", "Shuriken", "Sentry", "Spear"), player))
        world.connect_to_menu("Combat.Aerial", rule=lambda s: s.has("UTGlitch", player))
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: s.has("UTGlitch", player))
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("UTGlitch", player) and s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Sword", "Hammer", "Bow", "Shuriken", "Grenade"), player))

    # Unsafe
    if diff == LogicDifficulty.option_kii and one_level or diff != LogicDifficulty.option_unsafe and max_logic:
        world.connect_to_menu("DepthsLight",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("UpperDepths.ForestsEyes", "Flash", "Bow"), player))
        world.connect_to_menu("Combat.Ranged",
                              rule=lambda s:
                              s.has_any(("Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"), player))
        world.connect_to_menu("Combat.Aerial", rule=lambda s: s.has("UTGlitch", player))
        world.connect_to_menu("Combat.Dangerous",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Double Jump", "Dash", "Bash", "Launch"), player))
        world.connect_to_menu("Combat.Shielded",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Hammer", "Launch", "Grenade", "Spear"), player))
        world.connect_to_menu("Combat.Bat", rule=lambda s: s.has("UTGlitch", player))
        world.connect_to_menu("Combat.Sand", rule=lambda s: s.has("UTGlitch", player) and s.has("Burrow", player))
        world.connect_to_menu("BreakCrystal",
                              rule=lambda s: s.has("UTGlitch", player) and s.has_any(
                                  ("Sword", "Hammer", "Bow", "Shuriken", "Grenade", "Spear"), player))
