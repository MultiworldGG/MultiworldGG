import asyncio

import colorama

from worlds.LauncherComponents import Component, Type, components, launch

component_name = "TLOZ Oracle sprite editor"
version = 1
loading = True

for component_id in range(len(components)):
    component = components[component_id]
    if component.display_name == component_name:
        if getattr(component, "version", 0) >= version:
            loading = False
        else:
            del components[component_id]
        break # Only one component is supposed to exit anyway, so we don't need to check anything else

if loading:
    def run_client() -> None:
        launch(launch_sprite_editor, name=component_name)


    def launch_sprite_editor() -> None:
        from .client import main

        colorama.just_fix_windows_console()

        asyncio.run(main())
        colorama.deinit()


    component = Component(component_name,
                          component_type=Type.TOOL, func=run_client,
                          description="An UI to extract and manipulates Link's sprite in Oracle of Seasons and Ages.\n"
                                      "Editing the sprite should be done with an external program.")
    components.append(component)
