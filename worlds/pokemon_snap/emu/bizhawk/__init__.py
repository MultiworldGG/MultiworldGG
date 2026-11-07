import asyncio, base64
import worlds._bizhawk as bizhawk
import Utils

from typing import Sequence
from CommonClient import get_base_parser, server_loop, gui_enabled, logger
from worlds._bizhawk.context import BizHawkClientContext, _game_watcher, _patch_and_run_game
from worlds._bizhawk.client import BizHawkClient

from .ut_context import ContextClass
from .. import PokemonSnapGenericEmuClient
from ... import addresses as addr
from ...constants import GAME_NAME
from ...client import PokemonSnapClient

INT_SIZE = {
    'u8':  1,
    's8':  1,
    'u16': 2,
    's16': 2,
    'u32': 4,
    's32': 4,
}

SIGNEDNESS = {
    'u8':  False,
    's8':  True,
    'u16': False,
    's16': True,
    'u32': False,
    's32': True,
}

ADDR_MASK = 0x1FFFFFFF

class PokemonSnapBizHawkClient(BizHawkClient, PokemonSnapGenericEmuClient):
    client: PokemonSnapClient
    game = GAME_NAME
    system = "N64"
    _last_validation_error: str | None = None

    def _log_validation_error(self, message: str):
        if message != self._last_validation_error:
            logger.error(message)
            self._last_validation_error = message

    async def validate_rom(self, ctx: BizHawkClientContext):
        rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x20, 12, 'ROM')]))[0]
        if rom_name_bytes != b'POKEMON SNAP':
            self._log_validation_error('Not a Pokemon Snap ROM')
            return False

        rom_size = await bizhawk.get_memory_size(ctx.bizhawk_ctx, 'ROM')
        if rom_size < addr.AUTH_ROM + addr.AUTH_LEN or (await self._read_raw_auth_token(ctx)) == addr.UNPATCHED_AUTH:
            self._log_validation_error('Unpatched ROM')
            return False

        memory_size = await bizhawk.get_memory_size(ctx.bizhawk_ctx, 'RDRAM')
        if memory_size < 8_000_000:
            self._log_validation_error('In BizHawk, enable the expansion pak (N64 -> Use Expansion Slot). '
                                       'Then reboot the core (Emulation -> Reboot Core).')
            return False

        self._last_validation_error = None
        self.client = PokemonSnapClient()
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        ctx.slot_data = {}
        return True

    async def _read_raw_auth_token(self, ctx: BizHawkClientContext):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(addr.AUTH_ROM, addr.AUTH_LEN, 'ROM')]))[0]

    async def set_auth(self, ctx):
        raw_auth_token = await self._read_raw_auth_token(ctx)
        if raw_auth_token == addr.UNPATCHED_AUTH:
            return None
        ctx.auth = base64.b64encode(raw_auth_token).decode('ascii')

    async def game_watcher(self, ctx: BizHawkClientContext):
        try:
            if not (ctx.slot and ctx.slot_data): return
            magic = (await self.read(ctx, [(addr.EXPANSION_MAGIC, 4, 'u32')]))[0][0]
            if magic != addr.EXPANSION_LOADED:
                return

            await self.client.check_snap_locations(self, ctx)
            await self.client.receive_snap_items(self, ctx)
        except bizhawk.RequestFailedError:
            pass

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

    async def read(self, ctx: BizHawkClientContext, read_list: Sequence[tuple[int, int, str]]):
        # Convert the read requests
        bizhawk_read_list = [(addr & ADDR_MASK, size, 'RDRAM') for addr, size, _ in read_list]
        bizhawk_results = await bizhawk.read(ctx.bizhawk_ctx, bizhawk_read_list)
        # Convert the results
        results = []
        for i, (_, size, int_type) in enumerate(read_list):
            result_bytes = bizhawk_results[i]
            int_size = INT_SIZE[int_type]
            converted_result = [int.from_bytes(result_bytes[j:j+int_size], byteorder='big', signed=SIGNEDNESS[int_type])
                                for j in range(0, size, int_size)]
            results.append(converted_result)
        return results

    async def write(self, ctx: BizHawkClientContext, write_list: Sequence[tuple[int, Sequence[int], str]]):
        # Convert the write requests
        bizhawk_write_list = []
        for address, ints, write_type in write_list:
            bytes_to_write = b''.join(int.to_bytes(n, length=INT_SIZE[write_type], byteorder='big', signed=SIGNEDNESS[write_type]) for n in ints)
            bizhawk_write_list.append((address & ADDR_MASK, bytes_to_write, 'RDRAM'))
        return await bizhawk.write(ctx.bizhawk_ctx, bizhawk_write_list)


def launch(*launch_args: str) -> None:
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an Archipelago patch file")
        args = parser.parse_args(launch_args)

        if args.patch_file != "":
            metadata = _patch_and_run_game(args.patch_file)
            server = metadata.get("server")
            if server:  # ignore missing and empty string servers
                args.connect = server

        ctx = ContextClass(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher_task = asyncio.create_task(_game_watcher(ctx), name="GameWatcher")

        try:
            await watcher_task
        except Exception as e:
            logger.exception(e)

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("BizHawkClient", exception_logger="Client")
    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()