from __future__ import annotations
import os
import asyncio
import typing
import bsdiff4
import shutil
import json
import hashlib
import shutil

import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds import deltarune
from MultiServer import mark_raw, Context, Client
from Utils import async_start

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

ap_world_version = "v2.0.4"

# Try importing gui_enabled in Utils first before trying to import them from CommonClient
# Core AP will be officially moving it to Utils in the future, so this is in accommodation for that
gui_loaded_from_utils: bool = False
try:
    from Utils import gui_enabled

    gui_loaded_from_utils = True
except ImportError:
    pass

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (
        TrackerCommandProcessor as ClientCommandProcessor,
        TrackerGameContext as SuperContext,
        get_base_parser,
        server_loop,
    )

    tracker_loaded = True

    if not gui_loaded_from_utils:
        from worlds.tracker.TrackerClient import gui_enabled
except ModuleNotFoundError:
    from CommonClient import ClientCommandProcessor, CommonContext as SuperContext, get_base_parser, server_loop

    if not gui_loaded_from_utils:
        from CommonClient import gui_enabled

def guess_deltarune_path(path: str | None):
    tempInstall = ""
    if path == "steaminstall" or path == None:
        tempInstall = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\DELTARUNE"
        if os.path.exists(tempInstall):
            return tempInstall
        else:
            tempInstall = "C:\\Program Files\\Steam\\steamapps\\common\\DELTARUNE"
            if os.path.exists(tempInstall):
                return tempInstall

    if path == "steamdepot":
        tempInstall = "C:\\Program Files (x86)\\Steam\\steamapps\\content\\app_1671210\\depot_1671212"
        if os.path.exists(tempInstall):
            return tempInstall
        else:
            tempInstall = "C:\\Program Files\\Steam\\steamapps\\content\\app_1671210\\depot_1671212"
            if os.path.exists(tempInstall):
                return tempInstall

    return path


class DeltaruneCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_resync(self):
        """Manually trigger a resync."""
        if isinstance(self.ctx, DeltaruneContext):
            self.output(f"Syncing items.")
            self.ctx.syncing = True

    def _cmd_patch(self):
        """Patch the game. Only use this command if /auto_patch fails."""
        if isinstance(self.ctx, DeltaruneContext):
            os.makedirs(name=Utils.user_path("DELTARUNE"), exist_ok=True)
            self.ctx.patch_game()
            self.output("Patched.")

    def _cmd_delete_saves(self):
        """Delete all archipelago saves and caches"""
        if isinstance(self.ctx, DeltaruneContext):
            path = self.ctx.save_game_folder
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir), ignore_errors=False)
                    self.output(f"Deleted {os.path.join(root, dir)}")

    def _cmd_chosen_route(self):
        """Use this to figure out your chosen route, if you don't know or have forgotten."""
        if isinstance(self.ctx, DeltaruneContext):
            if self.ctx.chosen_route == "all_recruits":
                self.output(
                    """You're doing "All Recruits" - Progress through the story normally. Recruit Everyone!!!
Gaining recruits has been turned into checks."""
                )
            elif self.ctx.chosen_route == "weird_route":
                self.output(
                    """You're doing "Weird Route" - Proceed through the "Weird Route" storyline while losing all possible recruits.
Losing recruits has been turned into checks."""
                )
            elif self.ctx.chosen_route == "all_routes":
                self.output(
                    """You're doing "All Routes" - All checks from doing both the normal and weird route storylines exist.
Both gaining and losing recruits have been turned into checks."""
                )
            else:
                self.output("You'll need to connect to a Multiworld, first.")

    @mark_raw
    def _cmd_auto_patch(self, path: typing.Optional[str] = None):
        """Patch the game automatically."""
        if isinstance(self.ctx, DeltaruneContext):
            os.path.exists("DELTARUNE")
            for root, dirs, files in os.walk("DELTARUNE"):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.makedirs(name=Utils.user_path("DELTARUNE"), exist_ok=True)

            pathInstall = guess_deltarune_path(path)

            if not os.path.exists(pathInstall) or not os.path.isfile(os.path.join(pathInstall, "data.win")):
                self.output(
                    "ERROR: Cannot find DELTARUNE. Please rerun the command with the correct folder."
                    ' command. "/auto_patch (Steam directory)".'
                )
            else:
                error = False
                matching_hash = [
                    "9D1FEA9DE81219EA7304F32F1AE7A878",
                    "276441245F2F9C11061E36370E6E9C9D",
                    "F0ECF91309E55E93C1A9D6E10AF1064F",
                    "A3CC0CE00949C538DEC395BC07097069",
                    "300559ED63E1009FD694DEB2784BF1C6",
                ]
                matching_hash_1_05 = [
                    "5D3E158DBE6888FBF24471019FBDE3C9",
                    "F2CA0969E982C9DEDC77EA5EC0DB0972",
                    "D96E6AFD0B40F8B4A39CAE86D0F89A0B",
                    "A3D804E9B101C0D1A6C71117DA214F71",
                    "591BF5321C70F17818559B8A50A99A7F",
                ]
                matching_hash_1_05_30TBPS = [
                    "7A0DDC20059BDFB56E7E5523B0B65ABF",
                    "DEE4F1831C7438AEDD375DBE1B587C3F",
                    "51ABC72791C0AFA533F2DB1D7BE3D44E",
                    "085C34120F7E25B0766E105A56B14B0B",
                    "E5DA918F0C064AAE5068F871E5885605",
                ]
                for chapter in range(0, 5):
                    additional_path = ""
                    file_name = "data.win"

                    if chapter > 0:
                        additional_path = f"chapter{chapter}_windows/"

                    hash = ""

                    with open(f"{pathInstall}/{additional_path}{file_name}", "rb") as f:
                        hash = hashlib.file_digest(f, "md5").hexdigest().upper()

                    if hash != matching_hash[chapter]:
                        self.output(
                            f"{pathInstall}/{additional_path}{file_name} is not DELTARUNE 1.04 Vanilla. (Is your game 1.05 or modded ?)"
                        )
                        if hash == matching_hash_1_05[chapter]:
                            self.output("Detected as 1.05")
                        elif hash == matching_hash_1_05_30TBPS[chapter]:
                            self.output("Are you a speedrunner ? Because 1.05 30TBPS is detected")
                        else:
                            self.output(f"Expected: {matching_hash[chapter]}, got {hash}")

                        error = True

                if not error:
                    shutil.copytree(pathInstall, Utils.user_path("DELTARUNE"), dirs_exist_ok=True)
                    self.ctx.patch_game()
                    self.output("Patching successful!")


class DeltaruneContext(SuperContext):
    tags = {"TextOnly"}
    game = "DELTARUNE"
    command_processor = DeltaruneCommandProcessor
    items_handling = 0b111
    chapters = None
    chapter1 = 0
    chapter2 = 0
    chapter3 = 0
    chapter4 = 0
    completechapter1 = 0
    completechapter2 = 0
    completechapter3 = 0
    completechapter4 = 0
    ranchapters = 0
    item_balancing = 0
    goal_macguffin_amount = 1
    chosen_route = 0
    mandatoryboss = 0
    mandatorymantle = 0
    receivingtype = 0
    unused_items = 0
    save_game_folder = os.path.expandvars(r"%localappdata%/DELTARUNEAP")

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "DELTARUNE"

    def patch_game(self):
        with open(Utils.user_path("DELTARUNE", "chapter1_windows", "data.win"), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), deltarune.data_path("ch1.bsdiff"))
        with open(Utils.user_path("DELTARUNE", "chapter1_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter2_windows", "data.win"), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), deltarune.data_path("ch2.bsdiff"))
        with open(Utils.user_path("DELTARUNE", "chapter2_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter3_windows", "data.win"), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), deltarune.data_path("ch3.bsdiff"))
        with open(Utils.user_path("DELTARUNE", "chapter3_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "chapter4_windows", "data.win"), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), deltarune.data_path("ch4.bsdiff"))
        with open(Utils.user_path("DELTARUNE", "chapter4_windows", "data.win"), "wb") as f:
            f.write(patchedFile)
        with open(Utils.user_path("DELTARUNE", "data.win"), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), deltarune.data_path("deltarune.bsdiff"))
        with open(Utils.user_path("DELTARUNE", "data.win"), "wb") as f:
            f.write(patchedFile)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        async_start(process_deltarune_cmd(self, cmd, args))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "DELTARUNE Client " + ap_world_version + " - " + apname + " version"
        ui.logging_pairs = [("Client", "Archipelago")]
        return ui

    async def version_mismatch(self):
        DeltaruneCommandProcessor.output(self, 
            """*****\nWARNING: Incompatible DELTARUNEAP version. Unable to connect.\n*****""")
        await super().disconnect(False)

async def process_deltarune_cmd(ctx: DeltaruneContext, cmd: str, args: dict):
    if cmd == "Connected":
        try:
            options = args["slot_data"]["options"]
        except:
            await ctx.version_mismatch()
            return

async def send_testy():
    """i like to test oh yeah."""
    logger.info("I am testing yippeee...")


def main():
    Utils.init_logging("DeltaruneClient" + ap_world_version, exception_logger="Client")

    async def _main():
        ctx = DeltaruneContext(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="DELTARUNE Client, for text interfacing.")
    args = parser.parse_args()
    main()
