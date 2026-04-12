import worlds.LauncherComponents as LauncherComponents

from .world import PeggleDeluxeWorld


def launch_client(*args) -> None:
    from .client import main
    LauncherComponents.launch(main, name="PeggleDeluxeClient", args=args)


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Peggle Deluxe Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT,
        icon="peggle_deluxe",
    )
)

LauncherComponents.icon_paths["peggle_deluxe"] = f"ap:{__name__}/icon.jpg"
