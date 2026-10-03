"""EnergyLink: exchanges in-game money against the shared server-side energy pool."""

from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from .data import data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


ENERGY_LINK_NONE = 0
ENERGY_LINK_REQUEST_DEPOSIT = 1
ENERGY_LINK_REQUEST_WITHDRAW = 2
ENERGY_LINK_DONE = 3
ENERGY_LINK_ERROR_INSUFFICIENT = 4
ENERGY_LINK_ERROR_DISCONNECTED = 5

ENERGY_LINK_EXCHANGE_RATE = 50_000_000  # energy units per in-game dollar
ENERGY_LINK_DEPOSIT_TAX_NUM = 1         # 1/4 = 25% deposit tax
ENERGY_LINK_DEPOSIT_TAX_DEN = 4
ENERGY_LINK_MAX_DOLLARS = 999_999       # MaxMoney in Crystal


def money3_to_int(bs) -> int:
    # wMoney is a 24-bit big-endian binary integer, not BCD.
    return (bs[0] << 16) | (bs[1] << 8) | bs[2]


def int_to_money3(n: int) -> bytes:
    n = max(0, min(ENERGY_LINK_MAX_DOLLARS, int(n)))
    return bytes([(n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])


async def handle_energy_link(ctx: "BizHawkClientContext", guard) -> None:
    status_addr = data.ram_addresses["wArchipelagoEnergyLinkStatus"]
    amount_addr = data.ram_addresses["wArchipelagoEnergyLinkAmount"]
    pool_addr = data.ram_addresses["wArchipelagoEnergyLinkPool"]
    energy_key = f"EnergyLink{ctx.team}"

    pool_units = ctx.stored_data.get(energy_key) or 0
    pool_dollars = pool_units // ENERGY_LINK_EXCHANGE_RATE
    await bizhawk.guarded_write(
        ctx.bizhawk_ctx,
        [(pool_addr, list(int_to_money3(pool_dollars)), "WRAM")],
        [guard],
    )

    status_read = await bizhawk.guarded_read(
        ctx.bizhawk_ctx, [(status_addr, 1, "WRAM")], [guard])
    if not status_read:
        return
    status = status_read[0][0]
    if status not in (ENERGY_LINK_REQUEST_DEPOSIT, ENERGY_LINK_REQUEST_WITHDRAW):
        return

    amount_read = await bizhawk.guarded_read(
        ctx.bizhawk_ctx, [(amount_addr, 3, "WRAM")], [guard])
    if not amount_read:
        return
    dollars = money3_to_int(amount_read[0])
    if dollars <= 0:
        await bizhawk.write(ctx.bizhawk_ctx,
                            [(status_addr, [ENERGY_LINK_DONE], "WRAM")])
        return

    # Refuse if the socket is down: send_msgs silently no-ops, and a DONE write here
    # would make ROM debit the wallet for a Set that never reached the server.
    if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
        await bizhawk.write(ctx.bizhawk_ctx, [(status_addr, [ENERGY_LINK_ERROR_DISCONNECTED], "WRAM")])
        return

    from CommonClient import logger
    if status == ENERGY_LINK_REQUEST_DEPOSIT:
        tax = dollars * ENERGY_LINK_DEPOSIT_TAX_NUM // ENERGY_LINK_DEPOSIT_TAX_DEN
        net = dollars - tax
        delta = net * ENERGY_LINK_EXCHANGE_RATE
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": energy_key,
            "default": 0,
            "operations": [
                {"operation": "add", "value": delta},
                {"operation": "max", "value": 0},
            ],
        }])
        await bizhawk.write(ctx.bizhawk_ctx,
                            [(status_addr, [ENERGY_LINK_DONE], "WRAM")])
        logger.info(f"EnergyLink: deposited ${net} (${tax} tax).")
    else:
        cost = dollars * ENERGY_LINK_EXCHANGE_RATE
        if pool_units < cost:
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(status_addr, [ENERGY_LINK_ERROR_INSUFFICIENT], "WRAM")])
            logger.info(f"EnergyLink: withdraw ${dollars} refused (pool only ${pool_dollars}).")
            return
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": energy_key,
            "default": 0,
            "operations": [
                {"operation": "add", "value": -cost},
                {"operation": "max", "value": 0},
            ],
        }])
        await bizhawk.write(ctx.bizhawk_ctx,
                            [(status_addr, [ENERGY_LINK_DONE], "WRAM")])
        logger.info(f"EnergyLink: withdrew ${dollars}.")
