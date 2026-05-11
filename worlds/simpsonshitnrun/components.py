from worlds.LauncherComponents import Component, SuffixIdentifier, components, Type, icon_paths
import asyncio
from pathlib import Path
try:
    from . import settings
except ImportError:
    import settings

def run_client(ap_url=None):
    asyncio.run(run_client_async(ap_url))

async def run_client_async(ap_url=None):
    from .SHARClient import SHARContext
    ctx = SHARContext()
    await ctx.initialize()
    if ap_url:
        await ctx.handle_apshar(Path(ap_url))
    else:
        await ctx.start()

def _launch_shar_client_process():
    import os, sys, subprocess
    client_path = os.path.join(os.path.dirname(__file__), "SHARClient.py")
    subprocess.Popen([sys.executable, client_path])


icon_paths["Donut"] = f"ap:{__name__}/icons/Donut.png"
components.append(
    Component(
        "Simpsons Hit & Run Client",
        func=run_client,
        game_name="Simpsons Hit and Run",
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apshar"),
        cli=False,
        icon="Donut"
    )
)

class SHARSettings(settings.Group):
    class SHARRandomizerExe(settings.FilePath):
        """
        Path to SHARRandomizer.exe to auto-launch.
        Example: "C:/Program Files (x86)/Vivendi Universal Games/The Simpsons Hit & Run/AP/SHARRandomizerFrontend.exe"
        """
        description = "Path to SHARRandomizerFrontend.exe"

    class LucasLauncherExe(settings.FilePath):
        """
        Path to Lucas' Mod Launcher.exe to auto-launch.
        Can't auto launch straight into running the mod saldy.
        Example: "C:/Program Files (x86)/Vivendi Universal Games/The Simpsons Hit & Run/Lucas Simpsons Hit & Run Mod Launcher.exe"
        """
        description = "Path to Lucas' Mod Launcher.exe"

    sharrandomizer: SHARRandomizerExe = SHARRandomizerExe("")
    lucas_launcher: LucasLauncherExe = LucasLauncherExe("")