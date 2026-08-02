# This whole file was copy/pasted from the existing ALttP AP implementation, then edited as needed.

from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Dict

from NetUtils import ClientStatus
from worlds.AutoSNIClient import SNIClient

from . import Regions, RomAddresses
from .ALttPDoorRandomizer import Regions as DRRegions

if TYPE_CHECKING:
    from SNIClient import SNIContext


logger = logging.getLogger("alttpr")
ROM_PLAYER_LIMIT = 255

class ALttPRSNIClient(SNIClient):
    game = "The Legend of Zelda: A Link to the Past"
    patch_suffix = ".apalttpr"


    async def get_rom_name(self, ctx: SNIContext) -> str:
        from SNIClient import snes_read
        rom_name = await snes_read(ctx, RomAddresses.ROMNAME_START, RomAddresses.ROMNAME_SIZE)
        if rom_name is None or all(byte == b"\x00" for byte in rom_name) or rom_name[:4] != b"LTTP":
            return None
        return rom_name


    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name = await self.get_rom_name(ctx)
        if rom_name is None:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001  # full local
        ctx.rom = rom_name
        # TODO: Deathlink
        return True


    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        gamemode = await snes_read(ctx, RomAddresses.WRAM_START + 0x10, 1)
        if gamemode in RomAddresses.ENDGAME_MODES:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        if gamemode is None or gamemode[0] not in RomAddresses.INGAME_MODES:
            return

        data = await snes_read(ctx, RomAddresses.RECV_PROGRESS_ADDR, 8)
        if data is None:
            return

        recv_index = data[0] | (data[1] << 8)
        recv_item = data[2]
        roomid = data[4] | (data[5] << 8)
        roomdata = data[6]
        scout_location = data[7]

        if recv_index < len(ctx.items_received) and recv_item == 0:
            item = ctx.items_received[recv_index]
            recv_index += 1
            snes_buffered_write(ctx, RomAddresses.RECV_PROGRESS_ADDR, bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))
            snes_buffered_write(ctx, RomAddresses.RECV_ITEM_ADDR, bytes([item.item]))
            snes_buffered_write(ctx, RomAddresses.RECV_ITEM_PLAYER_ADDR, bytes([min(ROM_PLAYER_LIMIT, item.player) if item.player != ctx.slot else 0]))
        if scout_location > 0 and scout_location in ctx.locations_info:
            # I'm suspicious that this will crash with a player ID >256, or possibly every time?
            # I don't think this code ever gets called tbh
            snes_buffered_write(ctx, RomAddresses.SCOUTREPLY_LOCATION_ADDR, bytes([scout_location]))
            snes_buffered_write(ctx, RomAddresses.SCOUTREPLY_ITEM_ADDR, bytes([ctx.locations_info[scout_location][0]]))
            snes_buffered_write(ctx, RomAddresses.SCOUTREPLY_PLAYER_ADDR, bytes([min(ROM_PLAYER_LIMIT, ctx.locations_info[scout_location][1])]))

        await snes_flush_writes(ctx)

        if scout_location > 0 and scout_location not in ctx.locations_scouted:
            ctx.locations_scouted.add(scout_location)
            logger.info(f'Scouting item at {list(ctx.lookup_id_to_name.keys())[scout_location - 1]}')
            await ctx.send_msgs(ctx.socket, [['LocationScouts', [scout_location]]])
        await self.track_locations(ctx, roomid, roomdata)


    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        # TODO: Deathlink
        pass


    def on_package(self, ctx: SNIContext, cmd: str, args: Dict[str, Any]) -> None:
        # TODO: Get items from server
        pass


    def should_collect(self, ctx, location_id: int) -> bool:
        return ctx.allow_collect and location_id in ctx.checked_locations \
                and location_id not in ctx.locations_checked and location_id in ctx.locations_info \
                and ctx.locations_info[location_id].player != ctx.slot


    # TODO: This function can be massively condensed by e.g. combining underworld and overworld
    # code into a single function that gets called twice.
    async def track_locations(self, ctx, roomid, roomdata) -> bool:
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes
        location_id: int
        new_locations = []

        def new_check(location_id):
            new_locations.append(location_id)
            ctx.locations_checked.add(location_id)

        # Check for shops
        try:
            misc_data = await snes_read(ctx, RomAddresses.SHOP_SRAM_START, RomAddresses.SHOP_SRAM_LEN)
            for cnt, b in enumerate(misc_data):
                my_check = 0x400000 + cnt
                if int(b) > 0 and my_check not in ctx.locations_checked:
                    new_check(my_check)
        except Exception as e:
            print(e)
            logging.warning(e)

        for location_id, (loc_roomid, loc_mask) in RomAddresses.location_table_uw.items():
            try:
                if location_id not in ctx.locations_checked and loc_roomid == roomid and \
                        (roomdata << 4) & loc_mask != 0:
                    new_check(location_id)
            except Exception as e:
                logger.exception(f"Exception: {e}")

        uw_begin = 0x129
        ow_end = uw_end = 0
        uw_unchecked = {}
        uw_checked = {}
        for location, (roomid, mask) in RomAddresses.location_table_uw.items():
            location_id = Regions.lookup_name_to_id[location]
            if location_id not in ctx.locations_checked:
                uw_unchecked[location_id] = (roomid, mask)
                uw_begin = min(uw_begin, roomid)
                uw_end = max(uw_end, roomid + 1)
            if self.should_collect(ctx, location_id):
                uw_begin = min(uw_begin, roomid)
                uw_end = max(uw_end, roomid + 1)
                uw_checked[location_id] = (roomid, mask)

        if uw_begin < uw_end:
            uw_data = await snes_read(ctx, RomAddresses.SAVEDATA_START + (uw_begin * 2), (uw_end - uw_begin) * 2)
            if uw_data is not None:
                for location_id, (roomid, mask) in uw_unchecked.items():
                    offset = (roomid - uw_begin) * 2
                    roomdata = uw_data[offset] | (uw_data[offset + 1] << 8)
                    if roomdata & mask != 0:
                        new_check(location_id)
                if uw_checked:
                    uw_data = list(uw_data)
                    for location_id, (roomid, mask) in uw_checked.items():
                        offset = (roomid - uw_begin) * 2
                        roomdata = uw_data[offset] | (uw_data[offset + 1] << 8)
                        roomdata |= mask
                        uw_data[offset] = roomdata & 0xFF
                        uw_data[offset + 1] = roomdata >> 8
                    snes_buffered_write(ctx, RomAddresses.SAVEDATA_START + (uw_begin * 2), bytes(uw_data))

        ow_begin = 0x82
        ow_unchecked = {}
        ow_checked = {}
        for location, screenid in RomAddresses.location_table_ow.items():
            location_id = Regions.lookup_name_to_id[location]
            if location_id not in ctx.locations_checked:
                ow_unchecked[location_id] = screenid
                ow_begin = min(ow_begin, screenid)
                ow_end = max(ow_end, screenid + 1)
                if self.should_collect(ctx, location_id):
                    ow_checked[location_id] = screenid

        if ow_begin < ow_end:
            ow_data = await snes_read(ctx, RomAddresses.SAVEDATA_START + 0x280 + ow_begin, ow_end - ow_begin)
            if ow_data is not None:
                for location_id, screenid in ow_unchecked.items():
                    if ow_data[screenid - ow_begin] & 0x40 != 0:
                        new_check(location_id)
                if ow_checked:
                    ow_data = list(ow_data)
                    for location_id, screenid in ow_checked.items():
                        ow_data[screenid - ow_begin] |= 0x40
                    snes_buffered_write(ctx, RomAddresses.SAVEDATA_START + 0x280 + ow_begin, bytes(ow_data))

        if not all([location in ctx.locations_checked for location in RomAddresses.location_table_boss.keys()]):
            boss_data = await snes_read(ctx, RomAddresses.SAVEDATA_START + 0x472, 2)
            if boss_data is not None:
                boss_value = boss_data[0] | (boss_data[1] << 8)
                for location, mask in RomAddresses.location_table_boss.items():
                    if boss_value & mask != 0 and location not in ctx.locations_checked:
                        new_check(Regions.lookup_name_to_id[location])

        if not ctx.locations_checked.issuperset(RomAddresses.location_table_npc):
            npc_data = await snes_read(ctx, RomAddresses.SAVEDATA_START + 0x410, 2)
            if npc_data is not None:
                npc_value_changed = False
                npc_value = npc_data[0] | (npc_data[1] << 8)
                for location, mask in RomAddresses.location_table_npc.items():
                    location_id = Regions.lookup_name_to_id[location]
                    if npc_value & mask != 0 and location_id not in ctx.locations_checked:
                        new_check(location_id)
                    if self.should_collect(ctx, location_id):
                        npc_value |= mask
                        npc_value_changed = True
                if npc_value_changed:
                    npc_data = bytes([npc_value & 0xFF, npc_value >> 8])
                    snes_buffered_write(ctx, RomAddresses.SAVEDATA_START + 0x410, npc_data)

        if not ctx.locations_checked.issuperset(RomAddresses.location_table_misc):
            misc_data = await snes_read(ctx, RomAddresses.SAVEDATA_START + 0x3c6, 4)
            if misc_data is not None:
                misc_data = list(misc_data)
                misc_data_changed = False
                for location, (offset, mask) in RomAddresses.location_table_misc.items():
                    location_id = Regions.lookup_name_to_id[location]
                    assert (0x3c6 <= offset <= 0x3c9)
                    if misc_data[offset - 0x3c6] & mask != 0 and location_id not in ctx.locations_checked:
                        new_check(location_id)
                    if self.should_collect(ctx, location_id):
                        misc_data_changed = True
                        misc_data[offset - 0x3c6] |= mask
                if misc_data_changed:
                    snes_buffered_write(ctx, RomAddresses.SAVEDATA_START + 0x3c6, bytes(misc_data))

        if not all([location in ctx.locations_checked for location in RomAddresses.location_table_pot_items.keys()]):
            pot_items_data = await snes_read(ctx, RomAddresses.POT_ITEMS_SRAM_START, RomAddresses.ITEM_SRAM_SIZE)
            if pot_items_data is not None:
                for location, (offset, mask) in RomAddresses.location_table_pot_items.items():
                    pot_value = pot_items_data[offset] | (pot_items_data[offset + 1] << 8)
                    if pot_value & mask != 0 and location not in ctx.locations_checked:
                        new_check(Regions.lookup_name_to_id[location])

        if not all([location in ctx.locations_checked for location in RomAddresses.location_table_sprite_items.keys()]):
            sprite_items_data = await snes_read(ctx, RomAddresses.SPRITE_ITEMS_SRAM_START, RomAddresses.ITEM_SRAM_SIZE)
            if sprite_items_data is not None:
                for location, (offset, mask) in RomAddresses.location_table_sprite_items.items():
                    sprite_value = sprite_items_data[offset] | (sprite_items_data[offset + 1] << 8)
                    if sprite_value & mask != 0 and location not in ctx.locations_checked:
                        new_check(Regions.lookup_name_to_id[location])

        if new_locations:
            # verify rom is still the same:
            rom_name = await snes_read(ctx, RomAddresses.ROMNAME_START, RomAddresses.ROMNAME_SIZE)
            if rom_name is None or all(byte == b"\x00" for byte in rom_name) or rom_name[:4] != b"LTTP" or \
                    rom_name != ctx.rom:
                logger.info(f"Discarding recent {len(new_locations)} checks as ROM Status has changed.")
                return False
            else:
                await ctx.check_locations(new_locations)
        await snes_flush_writes(ctx)
        return True
