import asyncio
from argparse import Namespace

import Utils
from CommonClient import server_loop
from Utils import gui_enabled

from .context import TwoThousandAndFortyEightContext


async def main(args: Namespace) -> None:
    if not gui_enabled:
        raise RuntimeError("GUI not enabled.")

    Utils.init_logging("2048")
    ctx = TwoThousandAndFortyEightContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

    ctx.run_gui()
    ctx.run_cli()

    ctx.client_loop = asyncio.create_task(ctx.client_logic_loop(), name="Client Loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()
