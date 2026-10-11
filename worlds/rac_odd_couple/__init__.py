"""Archipelago world for the Ratchet & Clank: The Odd Couple Flash minigame."""
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from worlds.rac_odd_couple.world import OddCoupleWorld  # noqa: F401 - registers world
from worlds.rac_odd_couple.patch import OddCouplePatch, OddCouplePatchExtension  # noqa: F401 - registers handlers


def run_client(*args: str):
    """Launch the Odd Couple Archipelago client. If invoked by opening a
    .apoddcouple patch file, that file's path is passed through as an arg."""
    from worlds.rac_odd_couple.client import launch
    launch_subprocess(launch, name="OddCoupleClient", args=args)


components.append(Component(
    "Ratchet & Clank: The Odd Couple Client",
    func=run_client,
    component_type=Type.CLIENT,
    file_identifier=SuffixIdentifier(".apoddcouple"),
    description="Launch the Client for connecting to Ratchet & Clank: The Odd Couple",
))
