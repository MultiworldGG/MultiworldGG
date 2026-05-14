import logging
import random  # For picking whether P1 or P2 gets remainder studs after halving.
from typing import Mapping


from ..common import UintField
from ..common_addresses import player_character_entity_iter, is_in_chapter_free_play, CHARACTER_POWER_UP_TIMER
from ..type_aliases import TCSContext
from ...items import GENERIC_BY_NAME


logger = logging.getLogger("Client")


# TODO: We should add to the in-level studs instead, additionally adding to the True Jedi meter. If the player exits
#  without saving, then they will enter the Cantina and receive the Studs there instead, so they cannot abuse exiting
#  without saving re-giving them the studs, which would have otherwise allowed for entering another level and getting
#  the True Jedi progress there.
# Note, this is not the in-level stud count. We don't add to that, because it is not saved.
STUD_COUNT_ADDRESS = 0x86e4fc
MAX_STUD_COUNT = 4_000_000_000


STUDS_AP_ID_TO_VALUE: Mapping[int, int] = {
    GENERIC_BY_NAME["Silver Stud"].code: 10,
    GENERIC_BY_NAME["Gold Stud"].code: 100,
    GENERIC_BY_NAME["Blue Stud"].code: 1000,
    GENERIC_BY_NAME["Purple Stud"].code: 10000,
}


CHARACTER_STUD_COUNTER_POINTER = UintField(0x7fc)


# todo?: The stud counts for each player appear to be static addresses, which begs the question of why each player
#  controlled character entity has a pointer to one of these addresses.
# CURRENT_AREA_STUDS_P1_ADDRESS = 0x855f58
# CURRENT_AREA_STUDS_P2_ADDRESS = 0x855f68


def give_studs_item(ctx: TCSContext, ap_item_id: int) -> None:
    """
    Grant Studs to the player. Unlike other items, Studs are a consumable resource, so cannot simply be set to the
    number of received studs and instead must use the last/next item index from AP to determine when a Studs item is
    newly received by the current save file.
    """
    studs_to_add = STUDS_AP_ID_TO_VALUE.get(ap_item_id)
    if studs_to_add is None:
        logger.warning("Tried to receive unknown Studs item with item ID %i", ap_item_id)
        return

    # Multiply by the player's current maximum score multiplier.
    # The currently enabled score multipliers are not used because players could forget to enable them and then receive
    # a load of studs and then feel bad that they forgot to enable their multipliers.
    studs_to_add *= ctx.acquired_generic.current_score_multiplier

    give_studs(ctx, studs_to_add)


def drop_remainder_towards_zero(value: int, divisor: int) -> tuple[int, int]:
    """Drop the remainder of division by `divisor`, so that the returned value is divisible by `divisor`."""
    if divisor < 1:
        raise ValueError(f"Invalid divisor {divisor}. Divisor must be positive.")
    if value == 0:
        return 0, 0
    elif value > 0:
        # 15 % 10 == 5, so the remainder must be subtracted to approach zero.
        remainder = value % divisor
        return value - remainder, remainder
    else:
        # -15 % 10 == 5, so the remainder must be added to approach zero.
        assert value < 0
        remainder = value % divisor
        return value + remainder, -remainder


def give_studs(ctx: TCSContext,
               shared_studs_to_add: int = 0,
               p1_studs_to_add: int = 0,
               p2_studs_to_add: int = 0,
               only_give_if_in_level: bool = False,
               allow_power_up_multiplier: bool = True
               ):
    """
    Give studs to the active players.

    The studs_to_add may be negative to remove studs.

    If both players are active, the studs will be split between them.
    """

    # Keep studs to increments of 10 (1x Silver Stud)
    # Combined studs are kept separately in-case there is a better remainder when all values are combined.
    combined, _remainder = drop_remainder_towards_zero(shared_studs_to_add + p1_studs_to_add + p2_studs_to_add, 10)
    shared_studs_to_add, _remainder = drop_remainder_towards_zero(shared_studs_to_add, 10)
    p1_studs_to_add, _remainder = drop_remainder_towards_zero(p1_studs_to_add, 10)
    p2_studs_to_add, _remainder = drop_remainder_towards_zero(p2_studs_to_add, 10)

    if not shared_studs_to_add and not p1_studs_to_add and not p2_studs_to_add:
        # Nothing to do.
        return

    in_level_studs_addresses = []
    if is_in_chapter_free_play(ctx):
        player_studs = (p1_studs_to_add, p2_studs_to_add)
        for player_number, character_address in player_character_entity_iter(ctx):
            studs_address = CHARACTER_STUD_COUNTER_POINTER.get(ctx, character_address)
            if studs_address != 0:
                # Power Up doubles received studs.
                # todo: Add support for further doubling received studs when in a Double Score Zone.
                if (allow_power_up_multiplier
                        and (shared_studs_to_add > 0 or player_studs[player_number - 1] > 0)
                        and CHARACTER_POWER_UP_TIMER.get(ctx, character_address) > 0.0):
                    multiplier = 2
                else:
                    multiplier = 1
                in_level_studs_addresses.append((studs_address, multiplier))

    if in_level_studs_addresses:
        # Add the studs directly to the player(s)' stud counters.
        if len(in_level_studs_addresses) == 1:
            # There is only one player, so give them the combined amount of studs.
            if combined:
                in_level_studs_address, multiplier = in_level_studs_addresses[0]
                current_stud_count = ctx.read_uint(in_level_studs_address, raw=True)
                # Never go below zero, or above MAX_STUD_COUNT.
                new_stud_count = max(0, min(current_stud_count + combined * multiplier, MAX_STUD_COUNT))
                ctx.write_uint(in_level_studs_address, new_stud_count, raw=True)
        else:
            if shared_studs_to_add:
                # Always keep granted studs to increments of 10. The amount will be halved to give half to each player,
                # so check the remainder for 20 which will become 10 after halving.
                studs_to_add, remainder_after_halving = drop_remainder_towards_zero(shared_studs_to_add, 20)
                p1_studs = studs_to_add // 2
                p2_studs = p1_studs
                if remainder_after_halving:
                    # Pick randomly who gets the 10 studs remainder.
                    if random.randint(0, 1):
                        p1_studs += remainder_after_halving
                    else:
                        p2_studs += remainder_after_halving
                # Add any individually granted studs.
                p1_studs += p1_studs_to_add
                p2_studs += p2_studs_to_add
            else:
                p1_studs = p1_studs_to_add
                p2_studs = p2_studs_to_add

            # Give the studs to each player, taking into account any additional multipliers they each have.
            for (in_level_studs_address, multiplier), player_studs_to_add in zip(in_level_studs_addresses,
                                                                                 (p1_studs, p2_studs)):
                if player_studs_to_add == 0:
                    continue
                current_stud_count = ctx.read_uint(in_level_studs_address, raw=True)
                # Never go below zero, or above MAX_STUD_COUNT.
                new_stud_count = max(0, min(current_stud_count + player_studs_to_add * multiplier, MAX_STUD_COUNT))
                ctx.write_uint(in_level_studs_address, new_stud_count, raw=True)
    elif not only_give_if_in_level:
        # Add the studs directly to the save data's stud counter.
        if combined:
            current_stud_count = ctx.read_uint(STUD_COUNT_ADDRESS)
            # Never go below zero, or above MAX_STUD_COUNT.
            new_stud_count = max(0, min(current_stud_count + combined, MAX_STUD_COUNT))
            ctx.write_uint(STUD_COUNT_ADDRESS, new_stud_count)
