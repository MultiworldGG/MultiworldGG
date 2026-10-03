import logging

import base64
import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .constants import *
from .locations import all_locations
from .stage_data import microgame_data, game_data, game_groups, stages_with_large_scores, score_only_games

class WarioWareClient(BizHawkClient):
    game = GAME_NAME
    system = "GBA"
    patch_suffix = ".apwariowareinc"

    def __init__(self):
        super().__init__()
        self.flower_label = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            identifiers = await bizhawk.read(ctx.bizhawk_ctx, [
                (ROM_NAME_START, 0x0C, "ROM"),
                (AUTH_NUMBER_START, 0x03, "ROM"),
            ])
            if identifiers[0].decode("ascii") != "WARIOWAREINC":
                return False
            if identifiers[1] == b'\x00\x00\x00':
                return False
            if identifiers[1].decode("ascii") != "WW-":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(AUTH_NUMBER_START, 21, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.slot is None:
            return

        game_data = await bizhawk.read(ctx.bizhawk_ctx, [
            [STAGE_DATA, 0xE0, "EWRAM"],
            [MICROGAME_FLAGS, 0x100, "EWRAM"],
            [MICROGAME_HIGH_SCORE, 0x200, "EWRAM"],
            [SCENE_TYPE, 0x01, "IWRAM"],
            [STAGE_OPEN, 0x01, "IWRAM"],
            [SETTING_GOAL, 0x01, "ROM"],
            [MICROGAMES_LIST, 0x100, "ROM"],
        ])

        scene_type = int.from_bytes(game_data[3], "little")
        if scene_type not in [0x04, 0x03, 0x02]:
            return

        stage_data = bytearray(game_data[0])
        microgame_flags = bytearray(game_data[1])
        microgame_high_score = bytearray(game_data[2])
        stage_opened = int.from_bytes(game_data[4], "little")
        setting_required_muffins = int.from_bytes(game_data[5], "little")
        microgame_list = bytearray(game_data[6])

        received_index = int.from_bytes(stage_data[0xDA:0xDC], "little")
        mc_muffins = int.from_bytes(stage_data[0xDC:0xDE], "little")

        self.handle_flower_label(ctx, mc_muffins, setting_required_muffins)

        for _, loc_id in all_locations.items():
            if loc_id in ctx.locations_checked:
                continue

            loc_type = loc_id & TYPE_MASK
            stage_id = (loc_id & STAGE_MASK) >> 16
            data = loc_id & DATA_MASK

            if loc_type == STAGES:
                if stage_data[stage_id] >= 0x03:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == SCORE:
                if stage_id in stages_with_large_scores:
                    score = int.from_bytes(stage_data[stage_id+0x02:stage_id+0x05], "little")
                else:
                    score = int.from_bytes(stage_data[stage_id+0x02:stage_id+0x04], "little")
                if score >= data:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == MICROGAME:
                stage_idx = data * 0x02
                score = int.from_bytes(microgame_high_score[stage_idx:stage_idx+0x02], "little")
                if score >= 5:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == FLOWER:
                if microgame_flags[data] >= 0x03:
                    ctx.locations_checked.add(loc_id)

        await ctx.check_locations(ctx.locations_checked)

        if not ctx.finished_game and stage_opened == 0x1B:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        writes: list[tuple[int, Sequence[int], str]] = []

        if received_index < len(ctx.items_received):
            item = ctx.items_received[received_index]
            received_index += 1
            writes.append((RECEIVED_INDEX, received_index.to_bytes(2, "little"), "EWRAM"))

            item_name = ctx.item_names.lookup_in_slot(item.item)
            item_code = item.item & 0xFFF
            item_type = item.item & TYPE_MASK

            if item_type == MISC and item_code == 0x01:
                # give medals and open credits if needed
                mc_muffins += 1
                writes.append((MC_MUFFIN_COUNT, mc_muffins.to_bytes(2, "little"), "EWRAM"))
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Received a {item_name}!")
                if mc_muffins >= setting_required_muffins:
                    writes.append((STAGE_DATA+0xD8, (0x03).to_bytes(1, "little"), "EWRAM"))
                    await bizhawk.display_message(ctx.bizhawk_ctx, f"Unlocked Credits Staff Level! (You can now goal the game)")

            elif item_type == STAGES:
                if item_name in score_only_games:
                    writes.append((STAGE_DATA+item_code, (0x03).to_bytes(1, "little"), "EWRAM"))
                else:
                    writes.append((STAGE_DATA+item_code, (0x02).to_bytes(1, "little"), "EWRAM"))
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Unlocked {item_name}!")

            elif item_type == BUNDLES:
                for microgame_name in game_groups[item_name]:
                    microgame_id = microgame_data[microgame_name]
                    if microgame_id not in microgame_list:
                        continue
                    microgame_flags[microgame_id] |= 0x01
                    writes.append((MICROGAME_FLAGS+microgame_id, microgame_flags[microgame_id].to_bytes(1, "little"), "EWRAM"))
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Unlocked {item_name}!")

            elif item_type == MICROGAME:
                if item_code in microgame_list:
                    microgame_flags[item_code] |= 0x01
                    writes.append((MICROGAME_FLAGS+item_code, microgame_flags[item_code].to_bytes(1, "little"), "EWRAM"))

            await bizhawk.write(ctx.bizhawk_ctx, writes)

        else:
            await bizhawk.write(ctx.bizhawk_ctx, writes)
            return
            for loc_id in ctx.checked_locations:
                if loc_id in ctx.locations_checked:
                    continue
                ctx.locations_checked.add(loc_id)

                loc_type = loc_id & TYPE_MASK
                stage_id = (loc_id & STAGE_MASK) >> 16
                data = loc_id & DATA_MASK

                if loc_type == STAGES:
                    if not stage_data[stage_id] & 0x01:
                        writes.append((STAGE_DATA+stage_id, (stage_data[stage_id] | 0x01).to_bytes(1, "little"), "EWRAM"))
                elif loc_type == FLOWER:
                    if microgame_flags[data] != 0x03:
                        writes.append((STAGE_DATA+stage_id, (0x03).to_bytes(1, "little"), "EWRAM"))

            await bizhawk.write(ctx.bizhawk_ctx, writes)


    def handle_flower_label(self, ctx: "BizHawkClientContext", flower_count, flower_max) -> None:
        try:
            from kvui import MDLabel as Label
        except ImportError:
            from kvui import Label

        if not self.flower_label:
            self.flower_label = Label(text=f"", size_hint_x=None, width=120, halign="center")
            ctx.ui.connect_layout.add_widget(self.flower_label)

        self.flower_label.text = f"Flowers: {flower_count}/{flower_max}"
