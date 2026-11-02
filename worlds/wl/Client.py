from typing import TYPE_CHECKING
import time

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import checkable_locations, boss_location_dict
from .Blocks import block_info_dict
from .Items import (
    item_table,
    lookup_id_to_name,
    lookup_trapid_to_name,
    lookup_junkid_to_name,
    powerup_order,
    course_unlock_names,
)
from .MapData import COURSES, MARKERS
from .Navigation import ALIASES, course_navigation
from .Names import ItemName

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

EXPECTED_ROM_NAME = "WLCOURSEAP"
powerup_ids = tuple(item_table[name].code for name in powerup_order)
progressive_id = item_table[ItemName.progressive_powerup].code
active_junk = (0xA80900, 0xA80800, 0xA80700)


class WarioLandClient(BizHawkClient):
    game = "Wario Land"
    system = ("GB", "GBC", "SGB")
    patch_suffix = ".apwl"

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        try:
            title, map_hook, navigation_hook = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x134, 16, "ROM"),
                    (0x21345, 3, "ROM"),
                    (0x21F93, 3, "ROM"),
                ],
            )
            if not title.startswith(EXPECTED_ROM_NAME.encode("ascii")):
                return False
            if map_hook != bytes.fromhex("CD 80 6A"):
                return False
        except (UnicodeDecodeError, bizhawk.RequestFailedError):
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        ctx.refresh_connect = True
        ctx.last_trap_time = 0
        ctx.local_last_death_link = ctx.last_death_link
        ctx.deathlink_pending = False
        ctx.was_dead = None
        ctx.save_slot = None
        ctx.tracker_level = None
        ctx.course_navigation_supported = navigation_hook == bytes.fromhex("C3 31 6E")
        ctx.navigation_signature = None
        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        length = (await bizhawk.read(ctx.bizhawk_ctx, [(0x674B0, 1, "ROM")]))[0][0]
        name = (await bizhawk.read(ctx.bizhawk_ctx, [(0x674B1, length, "ROM")]))[0]
        ctx.auth = name.rstrip(b"\x00").decode("utf-8")

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        from CommonClient import logger

        if ctx.auth_status != 3 or ctx.slot_data is None:
            ctx.refresh_connect = True
            ctx.was_dead = None
            return

        try:
            # one request keeps the save, its checksum, and the game state on the same frame
            saves, modes, demo, paused, action, live, ap, map_state = (
                await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [
                        (0xA000, 0xC4, "System Bus"),
                        (0xA8C3, 4, "System Bus"),
                        (0xA92D, 1, "System Bus"),
                        (0xA908, 1, "System Bus"),
                        (0xA91A, 1, "System Bus"),
                        (0xA804, 20, "System Bus"),
                        (0xA400, 0x100, "System Bus"),
                        (0xA790, 0x60, "System Bus"),
                    ],
                )
            )
            mode, slot = modes[0], saves[0xC3]
            if mode == 0 or mode > 12 or modes[3] or demo[0] or slot > 2:
                ctx.was_dead = None
                ctx.deathlink_pending = False
                ctx.local_last_death_link = ctx.last_death_link
                return
            save = saves[slot * 0x40 : slot * 0x40 + 0x20]
            if save[:4] != b"\x19d9W" or sum(save) & 0xFF != saves[0xC0 + slot]:
                return

            guards = [
                (0xA0C3, bytes([slot]), "System Bus"),
                (0xA8C3, bytes([mode]), "System Bus"),
                (0xA8C6, b"\x00", "System Bus"),
                (0xA92D, b"\x00", "System Bus"),
                (0xA4FE, ap[0xFE:0x100], "System Bus"),
            ]
            sync = ap[0xFA] == 0 or ctx.refresh_connect
            if sync or slot != ctx.save_slot:
                ctx.was_dead = None
                ctx.deathlink_pending = False
                ctx.local_last_death_link = ctx.last_death_link
            if sync:
                await ctx.update_death_link(bool(ctx.slot_data["death_link"]))

            writes = []
            if sync:
                writes.append((0xA413, b"\xff" * 14, "System Bus"))
            data = bytearray(ap)
            received = int.from_bytes(ap[0xFE:0x100], "little")
            if received > len(ctx.items_received):
                # the server may still be replaying ReceivedItems after reconnecting
                return
            junk_values = {}
            for item in ctx.items_received[received:]:
                received += 1
                code = item.item
                if code not in lookup_id_to_name:
                    logger.warning("Ignoring unknown Wario Land item ID %s", code)
                    continue
                if code in lookup_trapid_to_name:
                    continue
                if code in lookup_junkid_to_name:
                    if code in active_junk:
                        addr = code >> 8
                        if addr not in junk_values:
                            guards.append(
                                (addr, bytes([live[addr - 0xA804]]), "System Bus")
                            )
                        value = junk_values.get(addr, live[addr - 0xA804])
                        value = min(99, (value >> 4) * 10 + (value & 15) + 1)
                        new_value = (value // 10) * 16 + value % 10
                        junk_values[addr] = new_value
                        writes.append((addr, bytes([new_value]), "System Bus"))
                    continue
                addr = code >> 8
                data[addr - 0xA400] = min(255, data[addr - 0xA400] + 1)
                writes.append((addr, bytes([data[addr - 0xA400]]), "System Bus"))
                if code in powerup_ids or code == progressive_id:
                    writes.append((0xA410, b"\x01", "System Bus"))
                    if code == progressive_id:
                        powers = powerup_ids[: data[0x11]]
                    elif ctx.slot_data["get_previous_powerups"]:
                        powers = powerup_ids[: powerup_ids.index(code) + 1]
                    else:
                        powers = (code,)
                    for power in powers:
                        data[(power >> 8) - 0xA400] = 1
                        writes.append((power >> 8, b"\x01", "System Bus"))

            if received != int.from_bytes(ap[0xFE:0x100], "little"):
                writes.append((0xA4FE, received.to_bytes(2, "little"), "System Bus"))
            # recompute from the counter
            if data[0x12] >= ctx.slot_data["bosses_required"] and not data[0x27]:
                data[0x27] = 1
                writes.append((0xA427, b"\x01", "System Bus"))

            map_id, world_id = map_state[0x0C], map_state[0x0F]
            boss_world = 1 if world_id == 7 and map_id == 6 else world_id
            navigation_signature = None
            if ctx.course_navigation_supported:
                available = bytearray(48)
                for level_id in course_unlock_names:
                    available[level_id] = int(
                        not ctx.slot_data["level_unlocks"]
                        or bool(data[0xB0 + level_id])
                    )
                for level_id, gate in (
                    (25, 0x21),
                    (10, 0x22),
                    (28, 0x23),
                    (26, 0x24),
                    (20, 0x25),
                    (24, 0x26),
                    (40, 0x27),
                ):
                    available[level_id] = int(bool(data[gate]))
                available[10] &= bool(live[8] & 0x40)
                for alias, original in ALIASES.items():
                    available[alias] = available[original]
                if data[0xB0:0xE0] != available:
                    writes.append((0xA4B0, bytes(available), "System Bus"))
                    data[0xB0:0xE0] = available
                if mode != 1 or sync:
                    ctx.navigation_signature = None
                if (
                    mode == 1
                    and map_id in (4, 6, 10, 12, 14, 16, 18)
                    and boss_world < 7
                ):
                    world_open = tuple(bool(data[9 + i]) for i in range(7))
                    navigation_signature = (
                        boss_world,
                        bytes(available),
                        world_open,
                        bool(live[8] & 0x40),
                    )
                    if (
                        navigation_signature != ctx.navigation_signature
                        and map_state[0x0E] != 0x2F
                        and not any(map_state[i] for i in (0, 2, 3, 4, 0x17, 0x54))
                    ):
                        cache = course_navigation(
                            boss_world,
                            available,
                            world_open,
                            bool(live[8] & 0x40),
                            ALIASES.get(map_state[0x0E], map_state[0x0E]),
                        )
                        markers = [
                            (level, address, tile)
                            for world, level, address, tile in MARKERS
                            if world == boss_world
                        ]
                        tiles = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(address, 1, "System Bus") for _, address, _ in markers],
                        )
                        redraw = any(
                            bool(available[level]) == (value[0] == tile)
                            for (level, _, tile), value in zip(markers, tiles)
                        )
                        guards.extend(
                            (addr, expected, "System Bus")
                            for addr, expected in (
                                (0xA79C, bytes([map_id])),
                                (0xA79F, bytes([world_id])),
                                (0xA790, b"\x00"),
                                (0xA792, bytes(3)),
                                (0xA7A7, b"\x00"),
                                (0xA7E4, b"\x00"),
                            )
                        )
                        writes.extend(
                            (
                                (0xA500, cache, "System Bus"),
                                (0xA4E5, b"\x00", "System Bus"),
                            )
                        )
                        # changing worlds needs new routes, but its dots were already drawn on entry.
                        if redraw:
                            writes.append((0xA79C, bytes([map_id - 1]), "System Bus"))
                    else:
                        navigation_signature = None
            if (
                mode == 1
                and map_id in (4, 6, 10, 12, 14, 16, 18)
                and boss_world < 7
                and map_state[0x0E] != 0x2F  # C12's automatic walk has not finished
                and bool(data[0x21 + boss_world]) != bool(ap[0x8F])
                and not any(map_state[i] for i in (0, 2, 3, 4, 0x17, 0x54))
            ):
                # reload only stationary map
                guards.extend(
                    (address, value, "System Bus")
                    for address, value in (
                        (0xA79C, bytes([map_id])),
                        (0xA79F, bytes([world_id])),
                        (0xA790, b"\x00"),
                        (0xA792, bytes(3)),
                        (0xA7A7, b"\x00"),
                        (0xA7E4, b"\x00"),
                    )
                )
                writes.append((0xA79C, bytes([map_id - 1]), "System Bus"))

            server_locations = ctx.missing_locations | ctx.checked_locations
            new_checks = set()
            # only report committed progress
            for code in checkable_locations.values():
                if save[(code >> 8) - 0xA800] & (code & 0xFF):
                    new_checks.add(code)
                    if code in boss_location_dict:
                        new_checks.add(boss_location_dict[code])

            block_buffer = ap[0x2E:0x6E]
            if ctx.slot_data["blocksanity"] and mode not in (1, 2):
                pointer = int.from_bytes(block_buffer[:2], "little")
                if 0xA430 <= pointer <= 0xA46E and pointer % 2 == 0:
                    level = {0x17: 0x07, 0x24: 0x0E}.get(live[0], live[0])
                    for offset in range(2, len(block_buffer), 2):
                        address = int.from_bytes(
                            block_buffer[offset : offset + 2], "big"
                        )
                        block = block_info_dict.get((level << 16) | address)
                        if block is not None:
                            new_checks.add(block.locationID)

            gameplay = mode == 3 and paused[0] == 0
            dead = action[0] == 9
            outgoing_death = False
            incoming_death = False
            if gameplay and ctx.slot_data["death_link"]:
                outgoing_death = (
                    dead and ctx.was_dead is False and not ctx.deathlink_pending
                )
                incoming_death = (
                    not dead and ctx.local_last_death_link < ctx.last_death_link
                )
                if incoming_death:
                    guards.append((0xA91A, action, "System Bus"))
                    writes.append((0xA91A, b"\x09", "System Bus"))
            elif mode != 3:
                ctx.local_last_death_link = ctx.last_death_link
                ctx.deathlink_pending = False

            traps = [
                item
                for item in ctx.items_received[:received]
                if item.item in lookup_trapid_to_name
            ]
            activated = int.from_bytes(ap[0xFB:0xFD], "little")
            if sync:
                activated = len(traps)
            elif (
                activated < len(traps) and gameplay and not dead and not incoming_death
            ):
                if time.time() - ctx.last_trap_time > 5:
                    trap = traps[activated].item
                    if trap == 0xA38400:
                        writes.append((0xA384, b"\xff", "System Bus"))
                    elif trap == 0xA96400:
                        writes.append((0xA964, b"\x01\x01", "System Bus"))
                    elif trap == 0xA91A00:
                        writes.append((0xA91A, b"\x09", "System Bus"))
                    else:
                        writes.append((0xA61C, b"\x22", "System Bus"))
                    activated += 1
            if activated != int.from_bytes(ap[0xFB:0xFD], "little"):
                writes.append((0xA4FB, activated.to_bytes(2, "little"), "System Bus"))
            if sync:
                writes.append((0xA4FA, b"\x01", "System Bus"))
            if writes and not await bizhawk.guarded_write(
                ctx.bizhawk_ctx, writes, guards
            ):
                return
            if navigation_signature is not None:
                ctx.navigation_signature = navigation_signature
            if not sync and activated > int.from_bytes(ap[0xFB:0xFD], "little"):
                ctx.last_trap_time = time.time()
            ctx.refresh_connect = False
            ctx.save_slot = slot
            if mode == 3:
                ctx.was_dead = dead
                if incoming_death:
                    ctx.deathlink_pending = True
                    ctx.local_last_death_link = ctx.last_death_link
                elif not dead:
                    ctx.deathlink_pending = False
            else:
                ctx.was_dead = None
            if outgoing_death:
                await ctx.send_death(f"{ctx.auth} died from a garlic overdose.")
                ctx.local_last_death_link = ctx.last_death_link

            new_checks &= server_locations
            new_checks -= ctx.locations_checked
            ctx.locations_checked.update(new_checks)
            if new_checks:
                await ctx.send_msgs(
                    [{"cmd": "LocationChecks", "locations": sorted(new_checks)}]
                )

            # acknowledge only the buffer we read
            if any(block_buffer):
                await bizhawk.guarded_write(
                    ctx.bizhawk_ctx,
                    [(0xA42E, bytes(64), "System Bus")],
                    guards[:4] + [(0xA42E, block_buffer, "System Bus")],
                )

            if not ctx.finished_game:
                if ctx.slot_data["goal"] == 0:
                    complete = save[0x17] == 1
                else:
                    required = ctx.slot_data["required_garlic_cloves"]
                    complete = data[0x28] >= required
                if complete:
                    await ctx.send_msgs(
                        [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                    )
                    ctx.finished_game = True

            level = world_id + 0x30 if mode == 1 else live[0]
            if level != ctx.tracker_level:
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"warioland_curlevelid_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": level}],
                        }
                    ]
                )
                ctx.tracker_level = level
        except bizhawk.RequestFailedError:
            ctx.refresh_connect = True
