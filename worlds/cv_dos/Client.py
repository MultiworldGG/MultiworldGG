from typing import TYPE_CHECKING

from NetUtils import ClientStatus
from .in_game_data import global_soul_table, world_version
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import struct

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class DoSClient(BizHawkClient):
    game = "Castlevania: Dawn of Sorrow"
    system = "NDS"
    patch_suffix = ".apcvdos"
    most_recent_connect: str = ""
    client_version: str = world_version
    has_received_death: bool = False
    state_is_dying: int = 0
    has_reset_from_death: bool = True
    seen_events: list = []

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            game_id = await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 0x12, "ROM")])
            game_id = game_id[0].decode("ascii")
            if game_id != "CASTLEVANIA1ACVEA4":
                return False  # Only check Dawn roms

            # Check ROM name/patch version
            validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0x02F6DD7C, 16, "ROM"),
                                                                   (0x0B1BD4, 2, "Main RAM")])

            vanilla_check = struct.unpack("H", validation_data[1])[0]  # Check the extended C.Tower stuff
            if vanilla_check != 0x8000:  # If this is not set, assume the rom is vanilla
                if self.most_recent_connect != "Vanilla ROM":
                    ctx.gui_error("Unrandomized ROM", f"Loaded ROM appears to be unmodified. Please load a Castlevania: Dawn of Sorrow Archipelago ROM.")
                    self.most_recent_connect = "Vanilla ROM"
                return False

            # This is a DoS ROM
            patch_version = validation_data[0].rstrip(b"\x69")
            patch_version = patch_version.decode("ascii")

            if patch_version != self.client_version:
                if "Bad patch version" != self.most_recent_connect:
                    # We only want to display this error once
                    ctx.gui_error("Bad Version", f"Installed Dawn of Sorrow APworld version {self.client_version} does not match patch version {patch_version}")
                    self.most_recent_connect = "Bad patch version"
                return False

            post_validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0x02F6DD8D, 1, "ROM")])  # DL
            death_link_flag = int.from_bytes(post_validation_data[0])
            if death_link_flag:
                await ctx.update_death_link(True)
            else:
                await ctx.update_death_link(False)
            
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.locations_checked = set()
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:

        slot_name_bytes = await bizhawk.read(
            ctx.bizhawk_ctx, [(0x2F6DD50, 0x14, "ROM")])

        slot_name_bytes = slot_name_bytes[0].rstrip(b'\xFF')
        ctx.auth = slot_name_bytes.decode("ascii")

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"]:
            self.has_received_death = True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        if ctx.server_version.build > 0:
            ctx.connected = True
        else:
            ctx.connected = False
            ctx.refresh_connect = True

        if ctx.slot_data is not None:
            ctx.data_present = True
        else:
            ctx.data_present = False

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        read_state = await bizhawk.read(
            ctx.bizhawk_ctx, [
                (0x0F7190, 0x10, "Main RAM"),  # Check table
                (0x0F7257, 0x01, "Main RAM"),  # Game Mode
                (0x11504C, 0x01, "Main RAM"),  # Current Map
                (0x0F703C, 0x04, "Main RAM"),  # Gameplay timer. Will be 0 if not in game
                (0x308930, 0x20, "Main RAM"),  # AP data
                (0x0F6DFC, 0x01, "Main RAM"),  # Game state, we only care about the Dead flag
                (0x0F7180, 0x01, "Main RAM"),  # Moat Drain Switch flag
                (0x0F7038, 0x02, "Main RAM"),  # Boss Bitflags, used for Dario, Dmitrii and the Garden cutscene
            ]
        )

        game_mode = int.from_bytes(read_state[1], "little")
        cur_map = int.from_bytes(read_state[2], "little")
        game_timer = int.from_bytes(read_state[3], "little")
        ap_data = bytearray(read_state[4])
        death_state = int.from_bytes(read_state[5])
        moat_switch = int.from_bytes(read_state[6])
        event_flags = int.from_bytes(read_state[7], "little")

        if "DeathLink" in ctx.tags:
            await self.handle_deathlink(death_state, ctx)

        if game_mode == 1 or not game_timer:
            # We don't want to connect during Julius mode
            # We also use the game timer as a signal that we're in game, as it's zeroed out on the menu
            return

        await self.check_locations(read_state, ap_data, ctx)
        await self.give_items(ap_data, ctx)

        events = {
            "MoatDrained": (moat_switch >> 2) & 1,
            "DmitriiDefeated": (event_flags >> 3) & 1,
            "DarioDefeated": (event_flags >> 5) & 1,
            "DarknessRejected": (event_flags >> 14) & 1,
        }
        for event, seen in events.items():
            if bool(seen) != (event in self.seen_events):
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"{event}",
                            "default": 0,
                            "want_reply": True,
                            "operations": [{"operation": "replace", "value": seen}],
                        }
                    ]
                )
        self.seen_events = [e for e in events if events[e]]

        if not ctx.finished_game and cur_map == 0x0D:  # Map 0x0D is used for the Epilogue. If we're here, trigger goal
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    @staticmethod
    async def check_locations(read_state, ap_data, ctx):
        new_checks = []
        location_flags = read_state[0]
        soul_flag_table = list(ap_data[:0x10])
        button_items = ap_data[0x13]

        from .static_location_data import location_ids, location_data_table
        for location_name in location_ids:
            loc_id = location_ids[location_name]
            if loc_id not in ctx.server_locations or loc_id in ctx.locations_checked:
                continue
            loc_type = location_data_table[location_name].location_type
            if loc_type == "Normal" or loc_type == "Easter Egg":
                offset = int(loc_id / 8)
                bit = int(1 << (loc_id % 8))
                flag = location_flags[offset]
                if flag & bit:
                    new_checks.append(loc_id)
            elif loc_type == "Soul":
                index = global_soul_table.index(location_name)
                bit = 1 << (index % 8)
                offset = int(index / 8)
                flag = soul_flag_table[offset]
            elif loc_type == "Button":
                bit = 1 << (loc_id - 0x200)
                flag = button_items
            else:
                flag = 0
                bit = 0

            if flag & bit:
                new_checks.append(loc_id)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])

    @staticmethod
    async def give_items(ap_data, ctx):
        current_received_item = ap_data[0x10]
        total_items_received = int.from_bytes(ap_data[0x1E:0x20], "little")

        if total_items_received < len(ctx.items_received) and current_received_item == 0:
            item = ctx.items_received[total_items_received]
            total_items_received += 1
            item_data = struct.pack(">H", item.item)
            await bizhawk.write(ctx.bizhawk_ctx, [(0x308940, item_data, "Main RAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x30894E, struct.pack("H", total_items_received), "Main RAM")])

    async def handle_deathlink(self, current_death_state, ctx):
        if current_death_state & 0x40:  # If the player is currently dead
            if self.has_received_death:  # This is the death that we just got from the server
                self.has_received_death = False
                self.has_reset_from_death = False
            else:  # Received death is false, meaning the player actually died here
                if self.has_reset_from_death:  # We only want this to run once per death
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} died!")
                    self.has_reset_from_death = False
        else:
            if self.has_received_death:
                # Kill the player
                await bizhawk.write(ctx.bizhawk_ctx, [(0x308AAC, int.to_bytes(0x01), "Main RAM")])
            else:
                # This should be normal gameplay after relaoding
                self.has_reset_from_death = True
