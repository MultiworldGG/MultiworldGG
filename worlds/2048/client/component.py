import asyncio
from collections.abc import Sequence

import colorama

from worlds.LauncherComponents import Component, Type, components, launch


def run_client(*args: str) -> None:
    launch(launch_client, name="2048", args= args)


def launch_client(*args: Sequence[str]) -> None:
    from CommonClient import get_base_parser, handle_url_arg

    from .client import main

    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    colorama.just_fix_windows_console()

    asyncio.run(main(launch_args))
    colorama.deinit()


components.append(
    Component(
        "2048 Client",
        func=run_client,
        game_name="2048",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
