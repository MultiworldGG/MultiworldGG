from BaseClasses import CollectionState
from ..Items import GoldenBugs, BossItems
from ..RoomFunctions import RoomFunctions
from ..options import *


# region Glichless Logic
def can_use(state: CollectionState, player: int, item: str, count: int = 1):
    if item == "Lantern":
        return state.has(item, player, count) and can_refill_oil(state, player)
    elif item == "Progressive Hero's Bow":
        return state.has(item, player, count) and can_get_arrows(state, player)
    else:
        return state.has(item, player, count)


def can_warp(state: CollectionState, player: int):
    if not can_use(state, player, "Shadow Crystal"):
        return False
    return any(
        state.can_reach_region(room, player) for room in RoomFunctions.warp_rooms
    )


def can_get_hot_spring_water(state: CollectionState, player: int):
    return (
        state.can_reach_region("Lower Kakariko Village", player)
        or (
            state.can_reach_region("Death Mountain Elevator Lower", player)
            and can_defeat_Goron(state, player)
        )
    ) and has_bottle(state, player)


def has_damaging_item(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or has_bombs(state, player)
        or can_use(state, player, "Iron Boots")
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Spinner")
    )


def has_sword(state: CollectionState, player: int, count=1):
    return can_use(state, player, "Progressive Master Sword", count)


def can_defeat_Aeralfos(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Clawshot") and (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Shadow Crystal")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
    )


def can_defeat_Armos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Progressive Clawshot")
        or has_bombs(state, player)
        or can_use(state, player, "Spinner")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_BabaSerpent(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_HangingBabaSerpent(state: CollectionState, player: int):
    return (
        can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Progressive Hero's Bow")
    ) and can_defeat_BabaSerpent(state, player)


def can_defeat_BabyGohma(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Clawshot")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bari(state: CollectionState, player: int):
    return can_use_water_bombs(state, player) or can_use(
        state, player, "Progressive Clawshot"
    )


def can_defeat_Beamos(state: CollectionState, player: int):
    return (
        can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or has_bombs(state, player)
    )


def can_defeat_BigBaba(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Spinner")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Chu(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Progressive Clawshot")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bokoblin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bokoblin_Red(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow", 3)
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
        or (
            can_do_difficult_combat(state, player)
            and (
                can_use(state, player, "Iron Boots")
                or can_use(state, player, "Spinner")
            )
        )
    )


def can_defeat_Bombfish(state: CollectionState, player: int):
    return (
        can_use(state, player, "Iron Boots")
        or (state._tp_glitched(player) and can_use(state, player, "Magic Armor"))
    ) and (
        has_sword(state, player)
        or can_use(state, player, "Progressive Clawshot")
        or (
            has_shield(state, player)
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
    )


def can_defeat_Bombling(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Progressive Clawshot")
    )


def can_defeat_Bomskit(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
    )


def can_defeat_Bubble(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bulblin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Chilfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Spinner")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ChuWorm(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    ) and (has_bombs(state, player) or can_use(state, player, "Progressive Clawshot"))


def can_defeat_Darknut(state: CollectionState, player: int):
    return has_sword(state, player) or (
        can_do_difficult_combat(state, player)
        and (has_bombs(state, player) or can_use(state, player, "Ball and Chain"))
    )


def can_defeat_DekuBaba(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or (
            has_shield(state, player)
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Clawshot")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_DekuLike(state: CollectionState, player: int):
    return has_bombs(state, player)


def can_defeat_Dodongo(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Dinalfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Shadow Crystal")
    )


def can_defeat_FireBubble(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_FireKeese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_FireToadpoli(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (
            can_use(state, player, "Hylian Shield")
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
        or (
            can_do_difficult_combat(state, player)
            and can_use(state, player, "Shadow Crystal")
        )
    )


def can_defeat_Freezard(state: CollectionState, player: int):
    return can_use(state, player, "Ball and Chain")


def can_defeat_Goron(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (can_do_niche_stuff(state, player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or (
            has_shield(state, player)
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
        or can_use(state, player, "Slingshot")
        or (
            can_do_difficult_combat(state, player) and can_use(state, player, "Lantern")
        )
        or can_use(state, player, "Progressive Clawshot")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_GhoulRat(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal")


def can_defeat_Guay(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or (
            can_do_difficult_combat(state, player) and can_use(state, player, "Spinner")
        )
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Slingshot")
    )


def can_defeat_Helmasaur(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Helmasaurus(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_IceBubble(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_IceKeese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Poe(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal")


def can_defeat_Kargarok(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Keese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Leever(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
    )


def can_defeat_Lizalfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_MiniFreezard(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Moldorm(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
    )


def can_defeat_PoisonMite(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Lantern")
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
    )


def can_defeat_Puppet(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Rat(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_RedeadKnight(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowBeast(state: CollectionState, player: int):
    return has_sword(state, player) or (
        can_use(state, player, "Shadow Crystal") and can_midna_charge(state, player)
    )


def can_defeat_ShadowBulblin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowDekuBaba(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (can_do_niche_stuff(state, player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or (
            has_shield(state, player)
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Clawshot")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowInsect(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal")


def can_defeat_ShadowKargarok(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowKeese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Shadow Crystal")
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowVermin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShellBlade(state: CollectionState, player: int):
    return can_use_water_bombs(state, player) or (
        has_sword(state, player)
        and (
            can_use(state, player, "Iron Boots")
            or (state._tp_glitched(player) and can_use(state, player, "Magic Armor"))
        )
    )


def can_defeat_Skullfish(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
    )


def can_defeat_Skulltula(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Stalfos(state: CollectionState, player: int):
    return can_smash(state, player)


def can_defeat_Stalhound(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Stalchild(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Tektite(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_TileWorm(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    ) and can_use(state, player, "Gale Boomerang")


def can_defeat_Toado(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
    )


def can_defeat_WaterToadpoli(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (
            has_shield(state, player)
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
        or (
            can_do_difficult_combat(state, player)
            and can_use(state, player, "Shadow Crystal")
        )
    )


def can_defeat_TorchSlug(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
    )


def can_defeat_Walltula(state: CollectionState, player: int):
    return (
        can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Progressive Clawshot")
    )


def can_defeat_WhiteWolfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
    )


def can_defeat_YoungGohma(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
    )


def can_defeat_ZantHead(state: CollectionState, player: int):
    return (
        can_use(state, player, "Shadow Crystal") or has_sword(state, player)
    ) or can_use_backslice_as_sword(state, player)


def can_defeat_Ook(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Dangoro(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Shadow Crystal")
        or (
            can_do_niche_stuff(state, player)
            and (
                can_use(state, player, "Ball and Chain")
                or (
                    can_use(state, player, "Progressive Hero's Bow")
                    and has_bombs(state, player)
                )
            )
        )
    ) and can_use(state, player, "Iron Boots")


def can_defeat_CarrierKargarok(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal")


def can_defeat_TwilitBloat(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal")


def can_defeat_DekuToad(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_SkullKid(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Hero's Bow")


def can_defeat_KingBulblinBridge(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Hero's Bow")


def can_defeat_KingBulblinDesert(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Progressive Hero's Bow", 3)
        or can_use_backslice_as_sword(state, player)
        or (
            can_do_difficult_combat(state, player)
            and (
                can_use(state, player, "Spinner")
                or can_use(state, player, "Iron Boots")
                or has_bombs(state, player)
                or can_use(state, player, "Progressive Hero's Bow", 2)
            )
        )
    )


def can_defeat_KingBulblinCastle(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Shadow Crystal")
        or can_use(state, player, "Progressive Hero's Bow", 3)
        or (
            can_do_difficult_combat(state, player)
            and (
                can_use(state, player, "Spinner")
                or can_use(state, player, "Iron Boots")
                or has_bombs(state, player)
                or can_use_backslice_as_sword(state, player)
            )
        )
    )


def can_defeat_DeathSword(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        and (
            can_use(state, player, "Gale Boomerang")
            or can_use(state, player, "Progressive Hero's Bow")
            or can_use(state, player, "Progressive Clawshot")
        )
        and can_use(state, player, "Shadow Crystal")
    )


def can_defeat_Darkhammer(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or (
            can_do_difficult_combat(state, player)
            and can_use_backslice_as_sword(state, player)
        )
    )


def can_defeat_PhantomZant(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal") or has_sword(state, player)


def can_defeat_Diababa(state: CollectionState, player: int):
    return can_launch_bombs(state, player) or (
        can_use(state, player, "Gale Boomerang")
        and (
            has_sword(state, player)
            or can_use(state, player, "Ball and Chain")
            or (state._tp_glitched(player) and can_use(state, player, "Iron Boots"))
            or can_use(state, player, "Shadow Crystal")
            or has_bombs(state, player)
            or (
                can_do_difficult_combat(state, player)
                and can_use_backslice_as_sword(state, player)
            )
        )
    )


def can_defeat_Fyrus(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Hero's Bow")
        and can_use(state, player, "Iron Boots")
        and (
            has_sword(state, player)
            or (
                can_do_difficult_combat(state, player)
                and can_use_backslice_as_sword(state, player)
            )
        )
    )


def can_defeat_Morpheel(state: CollectionState, player: int):
    return (
        can_use(state, player, "Zora Armor")
        and can_use(state, player, "Iron Boots")
        and has_sword(state, player)
        and can_use(state, player, "Progressive Clawshot")
    ) or (
        state._tp_glitched(player)
        and (
            can_use(state, player, "Progressive Clawshot")
            and can_do_air_refill(state, player)
            and has_sword(state, player)
        )
    )


def can_defeat_Stallord(state: CollectionState, player: int):
    return (can_use(state, player, "Spinner") and has_sword(state, player)) or (
        can_do_difficult_combat(state, player) and can_use(state, player, "Spinner")
    )


def can_defeat_Blizzeta(state: CollectionState, player: int):
    return can_use(state, player, "Ball and Chain")


def can_defeat_Armogohma(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Hero's Bow")
        and can_get_arrows(state, player)
    ) and can_use(state, player, "Progressive Dominion Rod")


def can_defeat_Argorok(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Clawshot", 2)
        and has_sword(state, player, 2)
        and (
            can_use(state, player, "Iron Boots")
            or (
                can_do_niche_stuff(state, player)
                and can_use(state, player, "Magic Armor")
            )
        )
    )


def can_defeat_Zant(state: CollectionState, player: int):
    return has_sword(state, player, 3) and (
        can_use(state, player, "Gale Boomerang")
        and can_use(state, player, "Progressive Clawshot")
        and can_use(state, player, "Ball and Chain")
        and (
            can_use(state, player, "Iron Boots")
            or (state._tp_glitched(player) and can_use(state, player, "Magic Armor"))
        )
        and (
            can_use(state, player, "Zora Armor")
            or (state._tp_glitched(player) and can_do_air_refill(state, player))
        )
    )


def can_defeat_Ganondorf(state: CollectionState, player: int):
    return (
        can_use(state, player, "Shadow Crystal")
        and has_sword(state, player, 3)
        and can_use(state, player, "Progressive Hidden Skill")
    )


def can_smash(state: CollectionState, player: int):
    return can_use(state, player, "Ball and Chain") or has_bombs(state, player)


def can_burn_webs(state: CollectionState, player: int):
    return (
        can_use(state, player, "Lantern")
        or has_bombs(state, player)
        or can_use(state, player, "Ball and Chain")
    )


def has_ranged_item(state: CollectionState, player: int):
    return (
        can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Progressive Clawshot")
        or can_use(state, player, "Gale Boomerang")
    )


def has_shield(state: CollectionState, player: int):
    return (
        can_use(state, player, "Hylian Shield")
        or (
            state.can_reach_region("Kakariko Malo Mart", player)
            and not state._tp_shops_shuffled(player)
        )
        or (
            state.can_reach_region("Castle Town Goron House", player)
            and not state._tp_shops_shuffled(player)
        )
        or state.can_reach_region("Death Mountain Hot Spring", player)
    )


def can_use_bottled_fairy(state: CollectionState, player: int):
    return has_bottle(state, player) and state.can_reach_region("Lake Hylia", player)


def can_use_bottled_fairies(state: CollectionState, player: int):
    return has_bottles(state, player) and state.can_reach_region("Lake Hylia", player)


def can_use_oil_bottle(state: CollectionState, player: int):
    return can_use(state, player, "Lantern") and has_bottle(state, player)


def can_launch_bombs(state: CollectionState, player: int):
    return (
        can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Progressive Hero's Bow")
    ) and has_bombs(state, player)


def can_cut_hanging_web(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Clawshot")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Ball and Chain")
    )


def get_player_health(state: CollectionState, player: int):
    return (
        3
        + (state.count("Piece of Heart", player) * 0.2)
        + state.count("Heart Container", player)
    )


def can_knock_down_hc_painting(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Hero's Bow")
        or (
            can_do_niche_stuff(state, player)
            and (
                has_bombs(state, player)
                or (
                    has_sword(state, player)
                    and can_use(state, player, "Progressive Hidden Skill", 6)
                )
            )
        )
        or (
            state._tp_glitched(player)
            and (
                (has_sword(state, player) and can_do_moon_boots(state, player))
                or can_do_bs_moon_boots(state, player)
            )
        )
    )


def can_break_monkey_cage(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or can_use(state, player, "Iron Boots")
        or can_use(state, player, "Spinner")
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Shadow Crystal")
        or has_bombs(state, player)
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Progressive Clawshot")
        or (
            state._tp_glitched(player)
            and has_shield(state, player)
            and can_use(state, player, "Progressive Hidden Skill", 2)
        )
    )


def can_press_mines_switch(state: CollectionState, player: int):
    return can_use(state, player, "Iron Boots") or (
        state._tp_glitched(player) and can_use(state, player, "Ball and Chain")
    )


def can_free_all_monkeys(state: CollectionState, player: int):
    return (
        can_break_monkey_cage(state, player)
        and (
            can_use(state, player, "Lantern")
            or (
                can_use(state, player, "Forest Temple Small Key", 4)
                and (has_bombs(state, player) or can_use(state, player, "Iron Boots"))
            )
        )
        and can_burn_webs(state, player)
        and can_use(state, player, "Gale Boomerang")
        and can_defeat_Bokoblin(state, player)
        and can_use(state, player, "Forest Temple Small Key", 4)
    )


def can_knock_down_HangingBaba(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Progressive Clawshot")
        or can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Slingshot")
    )


def can_break_wooden_door(state: CollectionState, player: int):
    return (
        can_use(state, player, "Shadow Crystal")
        or has_sword(state, player)
        or can_smash(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def has_bombs(state: CollectionState, player: int):
    return can_use(state, player, "Bomb Bag") and (
        state.can_reach_region("Kakariko Barnes Bomb Shop Lower", player)
        or (
            state.can_reach_region("Eldin Field Water Bomb Fish Grotto", player)
            and can_use(state, player, "Progressive Fishing Rod")
        )
        or state.can_reach_region("City in The Sky Entrance", player)
    )


def can_use_water_bombs(state: CollectionState, player: int):
    return can_use(state, player, "Bomb Bag") and (
        state.can_reach_region("Kakariko Barnes Bomb Shop Lower", player)
        or (
            state.can_reach_region("Eldin Field Water Bomb Fish Grotto", player)
            and can_use(state, player, "Progressive Fishing Rod")
        )
        or (
            state.can_reach_region("Kakariko Barnes Bomb Shop Lower", player)
            and state.can_reach_region("Castle Town Malo Mart", player)
        )
    )


def can_get_arrows(state: CollectionState, player: int):
    return (
        state.can_reach_region("Lost Woods", player)
        or (
            can_complete_goron_mines(state, player)
            and state.can_reach_region("Kakariko Malo Mart", player)
        )
        or (
            state.can_reach_region("Castle Town Goron House Balcony", player)
            and not state._tp_shops_shuffled(player)
        )
    )


def can_refill_oil(state: CollectionState, player: int):
    return (
        state.can_reach_region("North Faron Woods", player)
        or state.can_reach_region("South Faron Woods", player)
        or state.can_reach_region("Arbiters Grounds Entrance", player)
        or (
            state.can_reach_region("Lake Hylia Long Cave", player)
            and can_smash(state, player)
        )
        or state.can_reach_region("Ordon Seras Shop", player)
        or (
            can_complete_goron_mines(state, player)
            and state.can_reach_region("Lower Kakariko Village", player)
        )
        or (
            state.can_reach_region("Castle Town Goron House", player)
            and not state._tp_shops_shuffled(player)
        )
        or state.can_reach_region("Death Mountain Hot Spring", player)
        or state.can_reach_region("City in The Sky Entrance", player)
        or (
            state.can_reach_region("Hyrule Castle Main Hall", player)
            and can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_use(state, player, "Progressive Clawshot", 2)
            and can_defeat_Darknut(state, player)
        )
        or (
            state.can_reach_region("Eldin Lantern Cave", player)
            and can_destroy_webs_without_lantern(state, player)
            and can_defeat_Chu(state, player)
        )
        or (
            state.can_reach_region("Hyrule Castle Graveyard", player)
            and can_smash(state, player)
        )
    )


def can_complete_prologue(state: CollectionState, player: int):
    return True
    # return (
    #     (
    #         state.can_reach_region("North Faron Woods", player)
    #         and can_defeat_Bokoblin(state, player)
    #     )
    #     or state._tp_skip_prologue(player)


def can_complete_goats1(state: CollectionState, player: int):
    return state.can_reach_region("Ordon Ranch", player) or can_complete_prologue(
        state, player
    )


def can_complete_MDH(state: CollectionState, player: int):
    return True
    # return (
    #     state._tp_skip_mdh(player)
    #     or (
    #         can_complete_lakebed_temple(state, player)
    #         and state.can_reach_region("Castle Town South", player)
    #     )
    # )


def can_strike_pedestal(state: CollectionState, player: int):
    return (
        state._tp_tot_entrance(player) == ToTEntrance.option_none
        or (
            state._tp_tot_entrance(player) == ToTEntrance.option_wooden_sword
            and has_sword(state, player, 1)
        )
        or (
            state._tp_tot_entrance(player) == ToTEntrance.option_ordon_sword
            and has_sword(state, player, 2)
        )
        or (
            state._tp_tot_entrance(player) == ToTEntrance.option_master_sword
            and has_sword(state, player, 3)
        )
        or (
            state._tp_tot_entrance(player) == ToTEntrance.option_light_sword
            and has_sword(state, player, 4)
        )
    )


def can_clear_forest(state: CollectionState, player: int):
    return (
        (
            can_complete_forest_temple(state, player)
            or (state._tp_faron_woods_logic(player) == FaronWoodsLogic.option_open)
        )
        and can_complete_prologue(state, player)
        and can_complete_faron_twilight(state, player)
    )


def can_complete_faron_twilight(state: CollectionState, player: int):
    return True
    # return (
    #     state._tp_faron_twilight_cleared(player)
    #     or (
    #         can_complete_prologue(state, player)
    #         and state.can_reach_region("South Faron Woods", player)
    #         and state.can_reach_region("Faron Woods Coros House Lower", player)
    #         and state.can_reach_region("Mist Area Near Faron Woods Cave", player)
    #         and state.can_reach_region("North Faron Woods", player)
    #         and state.can_reach_region("Ordon Spring", player)
    #         and (
    #             not state._tp_bonks_do_damage(player)
    #             or (
    #                 state._tp_bonks_do_damage(player)
    #                 and (
    #                     (
    #                         state._tp_damage_magnification(player)
    #                         is not DamageMagnification.option_ohko
    #                     )
    #                     or can_use_bottled_fairies(state, player)
    #                 )
    #             )
    #         )
    #     )
    # )


def can_complete_eldin_twilight(state: CollectionState, player: int):
    return True
    # return (
    #     state._tp_eldin_twilight_cleared(player)
    #     or (
    #         state.can_reach_region("Faron Field", player)
    #         and state.can_reach_region("Lower Kakariko Village", player)
    #         and state.can_reach_region("Kakariko Graveyard", player)
    #         and state.can_reach_region("Kakariko Malo Mart", player)
    #         and state.can_reach_region("Kakariko Barnes Bomb Shop Upper", player)
    #         and state.can_reach_region("Kakariko Renados Sanctuary Basement", player)
    #         and state.can_reach_region("Kakariko Elde Inn", player)
    #         and state.can_reach_region("Kakariko Bug House", player)
    #         and state.can_reach_region("Upper Kakariko Village", player)
    #         and state.can_reach_region("Kakariko Watchtower", player)
    #         and state.can_reach_region("Death Mountain Volcano", player)
    #         and (
    #             not state._tp_bonks_do_damage(player)
    #             or (
    #                 state._tp_bonks_do_damage(player)
    #                 and (
    #                     (
    #                         state._tp_damage_magnification(player)
    #                         is not DamageMagnification.option_ohko
    #                     )
    #                     or can_use_bottled_fairies(state, player)
    #                 )
    #             )
    #         )
    #     )
    # )


def can_complete_lanayru_twilight(state: CollectionState, player: int):
    return True
    # return (
    #     state._tp_lanayru_twilight_cleared(player)
    #     or (
    #         (
    #             state.can_reach_region("North Eldin Field", player)
    #             or can_use(state, player, "Shadow Crystal")
    #         )
    #         and state.can_reach_region("Zoras Domain", player)
    #         and state.can_reach_region("Zoras Domain Throne Room", player)
    #         and state.can_reach_region("Upper Zoras River", player)
    #         and state.can_reach_region("Lake Hylia", player)
    #         and state.can_reach_region("Lake Hylia Lanayru Spring", player)
    #         and state.can_reach_region("Castle Town South", player)
    #         and (
    #             not state._tp_bonks_do_damage(player)
    #             or (
    #                 state._tp_bonks_do_damage(player)
    #                 and (
    #                     (
    #                         state._tp_damage_magnification(player)
    #                         is not DamageMagnification.option_ohko
    #                     )
    #                     or can_use_bottled_fairies(state, player)
    #                 )
    #             )
    #         )
    #     )
    # )


def can_complete_all_twilight(state: CollectionState, player: int):
    return (
        can_complete_faron_twilight(state, player)
        and can_complete_eldin_twilight(state, player)
        and can_complete_lanayru_twilight(state, player)
    )


def can_complete_forest_temple(state: CollectionState, player: int):
    return can_use(state, player, "Diababa Defeated")


def can_complete_goron_mines(state: CollectionState, player: int):
    return can_use(state, player, "Fyrus Defeated")


def can_complete_lakebed_temple(state: CollectionState, player: int):
    return can_use(state, player, "Morpheel Defeated")


def can_complete_arbiters_grounds(state: CollectionState, player: int):
    return can_use(state, player, "Stallord Defeated")


def can_complete_snowpeak_ruins(state: CollectionState, player: int):
    return can_use(state, player, "Blizzeta Defeated")


def can_complete_temple_of_time(state: CollectionState, player: int):
    return can_use(state, player, "Armogohma Defeated")


def can_complete_city_in_the_sky(state: CollectionState, player: int):
    return can_use(state, player, "Argorok Defeated")


def can_complete_palace_of_twilight(state: CollectionState, player: int):
    return can_use(state, player, "Zant Defeated")


def can_complete_all_dungeons(state: CollectionState, player: int):
    return (
        can_complete_forest_temple(state, player)
        and can_complete_goron_mines(state, player)
        and can_complete_lakebed_temple(state, player)
        and can_complete_arbiters_grounds(state, player)
        and can_complete_snowpeak_ruins(state, player)
        and can_complete_temple_of_time(state, player)
        and can_complete_city_in_the_sky(state, player)
        and can_complete_palace_of_twilight(state, player)
    )


def has_bug(state: CollectionState, player: int):
    for bug in GoldenBugs:
        if can_use(state, player, bug):
            return True
    return False


def can_unlock_ordona_map(state: CollectionState, player: int):
    if state._tp_open_map(player) and True:  # setting skip prologue
        return True
    for mapRoom in RoomFunctions.OrdonaMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_faron_map(state: CollectionState, player: int):
    if state._tp_open_map(player) and True:  # setting faron twilight cleared
        return True
    for mapRoom in RoomFunctions.FaronMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_eldin_map(state: CollectionState, player: int):
    if state._tp_open_map(player) and True:  # setting eldin twilight cleared
        return True
    for mapRoom in RoomFunctions.EldinMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_lanayru_map(state: CollectionState, player: int):
    if state._tp_open_map(player) and True:  # setting lanayru twilight cleared
        return True
    for mapRoom in RoomFunctions.LanayruMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_snowpeak_map(state: CollectionState, player: int):
    if state._tp_open_map(player) and state._tp_skip_snowpeak_entrance(player):
        return True
    for mapRoom in RoomFunctions.SnowpeakMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_gerudo_map(state: CollectionState, player: int):
    if state._tp_open_map(player):
        return True
    for mapRoom in RoomFunctions.GerudoMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_do_difficult_combat(state: CollectionState, player: int):
    # TODO: Change to use setting once it's made
    return False


def can_do_niche_stuff(state: CollectionState, player: int):
    # TODO: Change to use setting once it's made
    return state._tp_glitched(player)


def can_use_backslice_as_sword(state: CollectionState, player: int):
    return state._tp_glitched(player) and can_use(
        state, player, "Progressive Hidden Skill", 3
    )


def can_get_bug_with_lantern(state: CollectionState, player: int):
    # TODO: If option to not have bug models replaced becomes a thing, this function can be useful
    return False


# endregion
# region Gliched Logic


def has_sword_or_BS(state: CollectionState, player: int):
    return has_sword(state, player) or can_use(
        state, player, "Progressive Hidden Skill", 3
    )


def has_bottle(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Bottle") and can_use(
        state, player, "Lantern"
    )


def has_bottles(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Bottle", 2) and can_use(
        state, player, "Lantern"
    )


def has_heavy_mod(state: CollectionState, player: int):
    return can_use(state, player, "Iron Boots", player) or can_use(
        state, player, "Magic Armor"
    )


def has_cutscene_item(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Sky Book")
        or has_bottle(state, player)
        or can_use(state, player, "Horse Call")
    )


def can_do_lja(state: CollectionState, player: int):
    return has_sword(state, player) and can_use(state, player, "Gale Boomerang")


def can_do_js_lja(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        and can_use(state, player, "Gale Boomerang")
        and can_use(state, player, "Progressive Hidden Skill", 6)
    )


def can_do_map_glitch(state: CollectionState, player: int):
    return can_use(state, player, "Shadow Crystal") and state.can_reach_region(
        "Kakariko Gorge", player
    )


def can_do_storage(state: CollectionState, player: int):
    return can_do_map_glitch(state, player) and has_one_handed_item(state, player)


def has_one_handed_item(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or has_bottle(state, player)
        or can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Progressive Clawshot")
        or can_use(state, player, "Lantern")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Dominion Rod")
    )


def can_do_moon_boots(state: CollectionState, player: int):
    return has_sword(state, player) and (
        can_use(state, player, "Magic Armor")
        or (
            can_use(state, player, "Iron Boots")
            and (get_item_wheel_slot_count(state, player) >= 3)
        )
    )  # Ensure you can equip something over boots TODO: moon boots item count logic?


def can_do_js_moon_boots(state: CollectionState, player: int):
    return can_do_moon_boots(state, player) and can_use(
        state, player, "Progressive Hidden Skill", 6
    )


def can_do_bs_moon_boots(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Hidden Skill", 3) and can_use(
        state, player, "Magic Armor"
    )


def can_do_eb_moon_boots(state: CollectionState, player: int):
    return (
        can_do_moon_boots(state, player)
        and can_use(state, player, "Progressive Hidden Skill")
        and has_sword(state, player, 2)
    )


def can_do_hs_moon_boots(state: CollectionState, player: int):
    return (
        can_do_moon_boots(state, player)
        and can_use(state, player, "Progressive Hidden Skill", 4)
        and has_sword(state, player)
        and has_shield(state, player)
    )


def can_do_fly_glitch(state: CollectionState, player: int):
    return can_use(state, player, "Progressive Fishing Rod") and has_heavy_mod(
        state, player
    )


def can_do_air_refill(state: CollectionState, player: int):
    return can_use_water_bombs(state, player) and (
        can_use(state, player, "Magic Armor")
        or (
            can_use(state, player, "Iron Boots")
            and (get_item_wheel_slot_count(state, player) >= 3)
        )
    )


def can_do_hidden_village_glitched(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Ball and Chain")
        or (
            can_use(state, player, "Slingshot")
            and (
                can_use(state, player, "Shadow Crystal")
                or has_sword(state, player)
                or has_bombs(state, player)
                or can_use(state, player, "Iron Boots")
                or can_use(state, player, "Spinner")
            )
        )
    )


def can_do_ft_windless_bridge_room(state: CollectionState, player: int):
    return (
        has_bombs(state, player)
        or can_do_bs_moon_boots(state, player)
        or can_do_js_moon_boots(state, player)
    )


def can_clear_forest_glitched(state: CollectionState, player: int):
    return can_complete_prologue(state, player) and (
        (state._tp_faron_woods_logic(player) == FaronWoodsLogic.option_open)
        or can_complete_forest_temple(state, player)
        or can_do_lja(state, player)
        or can_do_map_glitch(state, player)
    )


def can_complete_eldin_twilight_glitched(state: CollectionState, player: int):
    return state._tp_eldin_twilight_cleared(player) or can_clear_forest_glitched(
        state, player
    )


def can_skip_key_to_deku_toad(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Hidden Skill", 3)
        or can_do_bs_moon_boots(state, player)
        or can_do_js_moon_boots(state, player)
        or can_do_lja(state, player)
        or (
            has_bombs(state, player)
            and (
                has_heavy_mod(state, player)
                or can_use(state, player, "Progressive Hidden Skill", 6)
            )
        )
    )


def can_warp_meteor(state: CollectionState, player: int):
    return can_complete_lanayru_twilight(state, player) or (
        can_complete_eldin_twilight(state, player)
        and state.can_reach_region("Zoras Domain Throne Room", player)
        and can_use(state, player, "Shadow Crystal")
    )


def can_break_hc_barrier(state: CollectionState, player: int):
    dungeonCount = 0
    for item in BossItems:
        if can_use(state, player, item):
            dungeonCount += 1
    return (
        # Open
        (state._tp_castle_requirements(player) == CastleRequirements.option_open)
        # Fused Shadow
        or (
            (
                state._tp_castle_requirements(player)
                == CastleRequirements.option_fused_shadows
            )
            and can_use(
                state, player, "Progressive Fused Shadow", state._tp_hc_amount(player)
            )
        )
        # Mirror Shard
        or (
            (
                state._tp_castle_requirements(player)
                == CastleRequirements.option_mirror_shards
            )
            and can_use(
                state, player, "Progressive Mirror Shard", state._tp_hc_amount(player)
            )
        )
        # Dungeon
        or (
            (
                state._tp_castle_requirements(player)
                == CastleRequirements.option_dungeons
            )
            and (dungeonCount >= state._tp_hc_amount(player))
        )
        # Vanilla
        or (
            (state._tp_castle_requirements(player) == CastleRequirements.option_vanilla)
            and can_complete_palace_of_twilight(state, player)
        )
        # Poe
        or (
            (
                state._tp_castle_requirements(player)
                == CastleRequirements.option_poe_souls
            )
            and can_use(state, player, "Poe Soul", state._tp_hc_amount(player))
        )
        # Hearts
        or (
            (state._tp_castle_requirements(player) == CastleRequirements.option_hearts)
            and (get_player_health(state, player) >= state._tp_hc_amount(player))
        )
    )


def can_buy_magic_armor(state: CollectionState, player: int):
    return (
        (state._tp_wallet_size(player) == WalletSize.option_large)
        or (
            (state._tp_wallet_size(player) == WalletSize.option_reduced)
            and can_use(state, player, "Progressive Wallet", 2)
        )
        or (
            (
                (state._tp_wallet_size(player) == WalletSize.option_vanilla)
                or (state._tp_wallet_size(player) == WalletSize.option_hd)
            )
            and can_use(state, player, "Progressive Wallet")
        )
    )


def can_destroy_webs_without_lantern(state: CollectionState, player: int):
    return has_bombs(state, player) or can_use(state, player, "Ball and Chain")


def can_midna_charge(state: CollectionState, player: int):
    return can_complete_MDH(state, player) and can_complete_all_twilight(state, player)


def can_open_hc_bk_gate(state: CollectionState, player: int):
    dungeonCount = 0
    for item in BossItems:
        if can_use(state, player, item):
            dungeonCount += 1
    return (
        (state._tp_castle_bk_requirements(player) == CastleBKRequirements.option_none)
        or (
            (
                state._tp_castle_bk_requirements(player)
                == CastleBKRequirements.option_fused_shadows
            )
            and can_use(
                state,
                player,
                "Progressive Fused Shadow",
                state._tp_hc_bk_amount(player),
            )
        )
        or (
            (
                state._tp_castle_bk_requirements(player)
                == CastleBKRequirements.option_mirror_shards
            )
            and can_use(
                state,
                player,
                "Progressive Mirror Shard",
                state._tp_hc_bk_amount(player),
            )
        )
        or (
            (
                state._tp_castle_bk_requirements(player)
                == CastleBKRequirements.option_dungeons
            )
            and (dungeonCount >= state._tp_hc_bk_amount(player))
        )
        or (
            (
                state._tp_castle_bk_requirements(player)
                == CastleBKRequirements.option_poe_souls
            )
            and can_use(state, player, "Poe Soul", state._tp_hc_bk_amount(player))
        )
        or (
            (
                state._tp_castle_bk_requirements(player)
                == CastleBKRequirements.option_hearts
            )
            and (get_player_health(state, player) >= state._tp_hc_bk_amount(player))
        )
    )


def can_step_clip(state: CollectionState, player: int):
    return (
        can_use(state, player, "Progressive Master Sword")
        or can_use(state, player, "Progressive Clawshot")
        or can_use(state, player, "Progressive Dominion Rod")
        or can_use(state, player, "Ball and Chain")
        or can_use(state, player, "Progressive Hero's Bow")
        or can_use(state, player, "Gale Boomerang")
        or can_use(state, player, "Lantern")
        or can_use(state, player, "Slingshot")
        or can_use(state, player, "Progressive Fishing Rod")
        or has_bombs(state, player)
        or has_bottle(state, player)
    )


def get_item_wheel_slot_count(state: CollectionState, player: int):
    count = 0
    for item in (
        "Progressive Clawshot",
        "Progressive Dominion Rod",
        "Ball and Chain",
        "Spinner",
        "Progressive Hero's Bow",
        "Iron Boots",
        "Gale Boomerang",
        "Lantern",
        "Slingshot",
        "Progressive Fishing Rod",
        "Hawkeye",
        "Bomb Bag",
        "Bomb Bag",
        "Bomb Bag",
        # "Empty Bottle (Fishing Hole)",
        # "Milk (half) (Sera Bottle)",
        # "Lantern Oil (Coro Bottle)",
        # "Great Fairy Tears (Jovani)",
        "Auru's Memo",
        "Renado's Letter",
        "Horse Call",
    ):
        if state.has(item, player):
            count += 1

    count += state.count("Progressive Bottle", player)
    return count
