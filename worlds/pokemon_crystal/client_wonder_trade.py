"""Wonder Trade: swaps a party Pokemon with another player via a shared server-side pool."""

import asyncio
import copy
import random
import time
import uuid
from typing import Optional, TYPE_CHECKING

import Utils
import worlds._bizhawk as bizhawk
from .data import data
from .util_wonder_trade import pokemon_data_to_json, json_to_pokemon_data, trade_is_eligible

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class WonderTradeMixin:
    """Wonder Trade state and handlers, mixed into the Bizhawk client."""

    wonder_trade_update_event: asyncio.Event
    latest_wonder_trade_reply: dict
    wonder_trade_cooldown: int
    wonder_trade_cooldown_timer: int
    queued_received_trade: Optional[str]
    wonder_trade_in_flight: bool

    def initialize_wonder_trade(self) -> None:
        self.wonder_trade_update_event = asyncio.Event()
        self.latest_wonder_trade_reply = {}
        self.wonder_trade_cooldown = 5000
        self.wonder_trade_cooldown_timer = 0
        self.queued_received_trade = None
        self.wonder_trade_in_flight = False

    async def handle_wonder_trade(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger

        magic_addr = data.sram_addresses["sArchipelagoWonderTradeMagic"]
        status_addr = data.sram_addresses["sArchipelagoWonderTradeStatus"]
        send_addr = data.sram_addresses["sArchipelagoWonderTradeSendBuffer"]
        player_id_addr = data.ram_addresses["wPlayerID"]

        try:
            read_result = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (magic_addr, 3, "CartRAM"),
                    (status_addr, 1, "CartRAM"),
                    (send_addr, 48 + 11 + 11, "CartRAM"),
                    (player_id_addr, 2, "WRAM"),
                ],
            )
        except bizhawk.RequestFailedError:
            return

        # Skip until the ROM script has initialized the SRAM section — fresh
        # cartridges may have undefined SRAM contents and we mustn't act on
        # garbage status bytes.
        if read_result[0] != b"\xa5\x5a\xc3":
            return

        status = read_result[1][0]
        send_blob = read_result[2]
        # Trade identity is the player's trainer ID, not ctx.slot — this lets
        # two saves with different TIDs on the same AP slot still trade, and
        # prevents a save from claiming its own offerings.
        own_tid = int.from_bytes(read_result[3], "big")

        # Status stays at READY (1) until we deliver a partner mon and flip to
        # INCOMING (3); the IN_FLIGHT distinction is purely client-side. The
        # ROM script's .Waiting branch handles both transient states.
        if status != 1:
            return

        if not self.wonder_trade_in_flight:
            party_mon = bytes(send_blob[0:48])
            nickname = bytes(send_blob[48:48 + 11])
            ot = bytes(send_blob[48 + 11:48 + 22])
            trainer_id = int.from_bytes(party_mon[6:8], "big")
            player_female = False
            try:
                gender_read = await bizhawk.read(
                    ctx.bizhawk_ctx, [(data.ram_addresses["wPlayerGender"], 1, "WRAM")]
                )
                player_female = bool(gender_read[0][0] & 1)
            except (KeyError, bizhawk.RequestFailedError):
                pass

            json_blob = pokemon_data_to_json(party_mon, nickname, ot, trainer_id, player_female)
            self.wonder_trade_in_flight = True
            Utils.async_start(self.wonder_trade_send(ctx, json_blob, own_tid))
            return

        if self.queued_received_trade is not None:
            decoded = json_to_pokemon_data(self.queued_received_trade)
            await bizhawk.write(ctx.bizhawk_ctx, [
                (data.sram_addresses["sArchipelagoWonderTradeRecvBuffer"], decoded["party_mon"], "CartRAM"),
                (data.sram_addresses["sArchipelagoWonderTradeRecvNick"], decoded["nickname"], "CartRAM"),
                (data.sram_addresses["sArchipelagoWonderTradeRecvOT"], decoded["ot"], "CartRAM"),
                (status_addr, [3], "CartRAM"),
            ])
            logger.info("Wonder trade received!")
            self.queued_received_trade = None
            self.wonder_trade_in_flight = False
            return

        pool_key = f"pokemon_wonder_trades_{ctx.team}"
        if self.wonder_trade_cooldown_timer <= 0 and pool_key in ctx.stored_data:
            pool = ctx.stored_data.get(pool_key, {}) or {}
            eligible = any(
                trade_is_eligible(item, own_tid)
                for key, item in pool.items()
                if key != "_lock"
            )
            if eligible:
                self.queued_received_trade = await self.wonder_trade_receive(ctx, own_tid)
                if self.queued_received_trade is None:
                    self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                    self.wonder_trade_cooldown = min(self.wonder_trade_cooldown * 2, 60000)
                    self.wonder_trade_cooldown += random.randrange(0, 500)
                else:
                    self.wonder_trade_cooldown = 5000
        else:
            self.wonder_trade_cooldown_timer -= int(ctx.watcher_timeout * 1000)

    async def wonder_trade_acquire(self, ctx: "BizHawkClientContext", keep_trying: bool = False) -> Optional[dict]:
        while not ctx.exit_event.is_set():
            lock = int(time.time_ns() / 1000000)
            message_uuid = str(uuid.uuid4())
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "want_reply": True,
                "operations": [{"operation": "update", "value": {"_lock": lock}}],
                "uuid": message_uuid,
            }])

            self.wonder_trade_update_event.clear()
            try:
                await asyncio.wait_for(self.wonder_trade_update_event.wait(), 5)
            except asyncio.TimeoutError:
                if not keep_trying:
                    return None
                continue

            reply = copy.deepcopy(self.latest_wonder_trade_reply)

            if reply.get("uuid", None) != message_uuid:
                if not keep_trying:
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown / 1000)
                continue

            if reply["value"]["_lock"] != lock:
                if not keep_trying:
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown / 1000)
                continue

            if lock - reply["original_value"]["_lock"] < 5000:
                self.wonder_trade_cooldown = min(self.wonder_trade_cooldown * 2, 60000)
                self.wonder_trade_cooldown += random.randrange(0, 500)
                if not keep_trying:
                    self.wonder_trade_cooldown_timer = self.wonder_trade_cooldown
                    return None
                await asyncio.sleep(self.wonder_trade_cooldown / 1000)
                continue

            self.wonder_trade_cooldown = 5000
            return reply

    async def wonder_trade_send(self, ctx: "BizHawkClientContext", blob: str, own_tid: int) -> None:
        from CommonClient import logger

        posted = False
        try:
            reply = await self.wonder_trade_acquire(ctx, keep_trying=True)
            if reply is None:
                return

            slot = 0
            while str(slot) in reply["value"]:
                slot += 1

            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "operations": [{"operation": "update", "value": {
                    "_lock": 0,
                    str(slot): (own_tid, blob),
                }}],
            }])
            posted = True
            logger.info("Wonder trade sent! Waiting for a partner.")
        finally:
            if not posted:
                # Pool didn't accept the offer — let the next watcher tick retry.
                self.wonder_trade_in_flight = False

    async def wonder_trade_receive(self, ctx: "BizHawkClientContext", own_tid: int) -> Optional[str]:
        reply = await self.wonder_trade_acquire(ctx)
        if reply is None:
            return None

        candidate_slots = [
            int(slot)
            for slot, item in reply["value"].items()
            if slot != "_lock" and trade_is_eligible(item, own_tid)
        ]
        if not candidate_slots:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_wonder_trades_{ctx.team}",
                "default": {"_lock": 0},
                "operations": [{"operation": "update", "value": {"_lock": 0}}],
            }])
            return None

        chosen = random.choice(candidate_slots)
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"pokemon_wonder_trades_{ctx.team}",
            "default": {"_lock": 0},
            "operations": [
                {"operation": "update", "value": {"_lock": 0}},
                {"operation": "pop", "value": str(chosen)},
            ],
        }])
        return reply["value"][str(chosen)][1]
