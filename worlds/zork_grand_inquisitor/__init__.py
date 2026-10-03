import worlds.LauncherComponents as LauncherComponents

from .world import ZorkGrandInquisitorWorld


def launch_client(*args) -> None:
    from .client import main
    LauncherComponents.launch(main, name="ZorkGrandInquisitorClient", args=args)


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Zork Grand Inquisitor Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT,
        icon="zork_grand_inquisitor"
    )
)

LauncherComponents.icon_paths["zork_grand_inquisitor"] = f"ap:{__name__}/zork_grand_inquisitor.png"
