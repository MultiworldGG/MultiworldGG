from __future__ import annotations

import asyncio
import json
import os
import urllib.parse
from pathlib import Path

from CommonClient import ClientCommandProcessor, gui_enabled, get_base_parser, server_loop, logger, ClientStatus
from MultiServer import mark_raw

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

from . import Sims4World

# Gets the sims 4 mods folder

if Sims4World.settings.mods_folder.exists():
    mod_data_path = Path(Sims4World.settings.mods_folder) / "mod_data" / "s4ap"

# reads and prints json files

def print_json(obj: object, name: str, ctx: SimsContext):
    full_path = os.path.join(mod_data_path, name)
    if not os.path.exists(mod_data_path):
        ctx.gui_error(title="Sims 4 files not found.",
                      text=f"Could not find sims 4 mod files, make sure you installed the mod correctly and have ran sims 4.")
    else:
        with open(full_path, 'w') as f:
            json.dump(obj, f)

mtime = None


def load_json(name):
    global mtime
    full_path = os.path.join(mod_data_path, name)
    if os.path.isfile(full_path):
        next_mtime = os.path.getmtime(full_path)
        if mtime != next_mtime:
            mtime = next_mtime
            try:
                with open(full_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        else:
            return None
    else:
        return None


class SimsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    @mark_raw
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        print_json(False, 'sync.json', self.ctx)

    @mark_raw
    def _cmd_goal(self):
        """Displays the goal of the AP"""
        self.output(self.ctx.goal)

    @mark_raw
    def _cmd_career(self):
        """Displays the selected career in the Yaml"""
        self.output(self.ctx.career)

    @mark_raw
    def _cmd_set_path(self, sims_4_mods_path: str = ''):
        """Set the file path to the Sims 4 mods folder manually (if automatic detection fails)"""
        p = sims_4_mods_path
        global mod_data_path
        if p == '':
            self.output('no path inputed')
        elif os.path.exists(os.path.join(p, 'mod_data', 's4ap')):
            self.output('Sims 4 mods folder found')
            mod_data_path = os.path.join(p, 'mod_data', 's4ap')
        else:
            self.ctx.gui_error(title='Sims 4 mods folder not found',
                               text=f'Make sure the file path you inputed is correct.')
            self.output(
                f'Could not find mod_data folder\nif the path you inputed is correct make sure you have enabled script mods in the sims 4 and run the game \nPath: {p}')


class SimsContext(SuperContext):
    game = 'The Sims 4'
    command_processor = SimsCommandProcessor
    items_handling = 0b111
    want_slot_data = True
    tags = {"AP"}

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.syncing = False
        self.goal = None
        self.career = None

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago The Sims 4 Client"
        return ui

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.goal = args["slot_data"]["goal"]
            self.career = args["slot_data"]["career"]
            url = urllib.parse.urlparse(self.server_address)
            payload = {
                'cmd': "Connected",
                'host': url.hostname,
                'port': url.port,
                'name': self.slot_info[self.slot].name,
                'seed_name': self.seed_name,
                'goal': self.goal,
                'career': self.career
            }
            print_json(payload, 'connection_status.json', self)


        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']

        elif cmd == "ReceivedItems":
            payload = {
                'cmd': 'ReceivedItems',
                'items': [self.item_names.lookup_in_game(item.item) for item in args['items']],
                'item_ids': [item.item for item in args["items"]],
                'locations': [self.location_names.lookup_in_slot(location.location, location.player) for location in args['items']],
                'players': [self.player_names[player.player] for player in args["items"]],
                'index': args["index"]
            }
            print_json(payload, 'items.json', ctx=self)

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


async def game_watcher(ctx: SimsContext):
    while not ctx.exit_event.is_set():
        if ctx.syncing:
            sync_msg = [{'cmd': 'Sync'}]
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        if (ctx.server and ctx.slot) is not None:
            json_data = load_json('locations_cached.json')
            if json_data is not None:
                if "Locations" in json_data and json_data["Locations"] is not None and json_data["Seed"] == ctx.seed_name:
                    # locations_to_remove = []
                    for data in json_data["Locations"]:
                        for location_id in ctx.missing_locations:
                            location_current_name = ctx.location_names.lookup_in_game(location_id)
                            if location_current_name == data:
                                if ctx.goal == data.split("(", 1)[0].strip().replace(" ", "_").lower() and not ctx.finished_game:
                                    await SimsContext.send_msgs(ctx, [
                                        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                                    ctx.finished_game = True
                                await SimsContext.send_msgs(ctx,
                                                            [{"cmd": "LocationChecks", "locations": [location_id]}])
                                # locations_to_remove.append(data)
                                break
                    # for loc in locations_to_remove:
                    #     json_data["Locations"].remove(loc)
                    #     print_json(json_data, 'locations_cached.json', ctx)
            json_data = load_json('sync.json')
            if json_data is not None:
                if json_data:
                    ctx.syncing = True
                    print_json(False, 'sync.json', ctx)
        await asyncio.sleep(0.5)


def main():
    async def _main():
        parser = get_base_parser(description="The Sims 4 Client, for text interfacing.")
        args, rest = parser.parse_known_args()

        ctx = SimsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await watcher_task
        await ctx.shutdown()

    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    main()
