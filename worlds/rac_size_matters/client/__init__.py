"""Archipelago client for Ratchet & Clank: Size Matters via PCSX2 PINE."""
from __future__ import annotations

import asyncio
import sys
from argparse import Namespace

from CommonClient import get_base_parser, gui_enabled, handle_url_arg, server_loop

from .command_processor import RACCommandProcessor
from .context import RACContext, tracker_loaded

__all__ = ["RACCommandProcessor", "RACContext", "run_client"]


async def main(args: Namespace) -> None:
    ctx = RACContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if tracker_loaded:
        ctx.run_generator()

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    asyncio.create_task(ctx.game_watcher(), name="RAC game watcher")

    await ctx.exit_event.wait()
    await ctx.shutdown()


def run_client(*args: str) -> None:
    from Utils import init_logging

    init_logging("RACClient")
    parser = get_base_parser(description="R&C Size Matters Archipelago Client")
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    parsed_args = handle_url_arg(parser.parse_args(args))

    if not gui_enabled:
        if not parsed_args.connect and sys.stdin and sys.stdin.isatty():
            parsed_args.connect = input("Archipelago server address (host:port): ").strip() or None
        if not parsed_args.name and sys.stdin and sys.stdin.isatty():
            parsed_args.name = input("Slot name: ").strip() or None
        if not parsed_args.password and sys.stdin and sys.stdin.isatty():
            password = input("Password (leave blank if none): ").strip()
            parsed_args.password = password or None

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(parsed_args))
    colorama.deinit()
