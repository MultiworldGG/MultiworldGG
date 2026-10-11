"""Archipelago world for Ratchet & Clank: Size Matters (PSP/PS2)"""
from worlds.LauncherComponents import (
    Component,
    SuffixIdentifier,
    Type,
    components,
    icon_paths,
    launch_subprocess,
)

from worlds.rac_size_matters.world import (
    RACSizeMatterWorld,
)


def run_client(_url: str | None = None):
    """Launch the R&C: Size Matters Archipelago client."""
    from worlds.rac_size_matters.client import run_client as _run
    launch_subprocess(_run, name="RACSmClient")


components.append(Component(
    "Ratchet & Clank: Size Matters Client",
    func=run_client,
    component_type=Type.CLIENT,
    file_identifier=SuffixIdentifier(".aprsm"),
    icon="rsm_icon",
    description="Launch the Client for connecting to Ratchet & Clank: Size Matters",
))

icon_paths["rsm_icon"] = f"ap:{__name__}/images/Size_Matters_Icon.png"
