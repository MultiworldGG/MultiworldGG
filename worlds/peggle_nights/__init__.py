import worlds.LauncherComponents as LauncherComponents

from .world import PeggleNightsWorld


def launch_client(*args) -> None:
    from .client import main
    LauncherComponents.launch(main, name="PeggleNightsClient", args=args)


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Peggle Nights Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT,
        icon="peggle_nights",
    )
)

LauncherComponents.icon_paths["peggle_nights"] = f"ap:{__name__}/icon.jpg"
