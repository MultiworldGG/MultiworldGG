import worlds.LauncherComponents as LauncherComponents

from .world import PinballFX3World


def launch_client(*args) -> None:
    from .client import main
    LauncherComponents.launch(main, name="PinballFX3Client", args=args)


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Pinball FX3 Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT,
        icon="pinball_fx3",
    )
)

LauncherComponents.icon_paths["pinball_fx3"] = f"ap:{__name__}/icon.jpg"
