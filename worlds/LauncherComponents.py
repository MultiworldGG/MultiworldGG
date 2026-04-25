import bisect
import gzip
import hashlib
import json
import logging
import os
import pathlib
import pkgutil
import subprocess
import sys
import tempfile
import time
import weakref
from enum import Enum, auto
from typing import Any, Optional, Callable, Iterable, Tuple

from Utils import local_path, open_filename, is_frozen, is_kivy_running, open_file, user_path, read_apignore

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

_LAUNCHER_CACHE_PATH = local_path("data", "world_launcher_cache.json.gz")
_DEFAULT_ICON_PATH = local_path("data", "icon.png")
_LAUNCHER_ICON_CACHE_DIR = os.path.join(tempfile.gettempdir(), "mwgg_launcher_icons")

_COMPONENT_ORIGIN_ATTRIBUTE = "_mwgg_component_origin"
_COMPONENT_ORIGIN_BUILTIN = "builtin"
_COMPONENT_ORIGIN_WORLD = "world"
_COMPONENT_ORIGIN_OTHER = "other"
_COMPONENT_ORIGIN_CACHE = "cache_stub"

_INITIALIZING_COMPONENTS = True


class Type(Enum):
    TOOL = auto()
    MISC = auto()
    CLIENT = auto()
    ADJUSTER = auto()
    FUNC = auto()  # do not use anymore
    HIDDEN = auto()


class Component:
    """
    A Component represents a process launchable by MultiworldGG Launcher, either by a User action in the GUI,
    by resolving an archipelago/mwgg://user:pass@host:port link from the WebHost, by resolving a patch file's metadata,
    or by using a component name arg while running the Launcher in CLI i.e. `MultiworldGGLauncher.exe "Text Client"`

    Expected to be appended to LauncherComponents.component list to be used.
    """
    display_name: str
    """Used as the GUI button label and the component name in the CLI args"""
    description: str
    """Optional description displayed on the GUI underneath the display name"""
    type: Type
    """
    Enum "Type" classification of component intent, for filtering in the Launcher GUI
    If not set in the constructor, it will be inferred by display_name
    """
    script_name: Optional[str]
    """Recommended to use func instead; Name of file to run when the component is called"""
    frozen_name: Optional[str]
    """Recommended to use func instead; Name of the frozen executable file for this component"""
    icon: str  # just the name, no suffix
    """Lookup ID for the icon path in LauncherComponents.icon_paths"""
    cli: bool
    """Bool to control if the component gets launched in an appropriate Terminal for the OS"""
    func: Optional[Callable]
    """
    Function that gets called when the component gets launched
    Any arg besides the component name arg is passed into the func as well, so handling *args is suggested
    """
    file_identifier: Optional[Callable[[str], bool]]
    """
    Function that is run against patch file arg to identify which component is appropriate to launch
    If the function is an Instance of SuffixIdentifier the suffixes will also be valid for the Open Patch component
    """
    game_name: Optional[str]
    """Game name to identify component when handling launch links from WebHost"""
    supports_uri: Optional[bool]
    """Bool to identify if a component supports being launched by launch links from WebHost"""

    def __init__(self, display_name: str, script_name: Optional[str] = None, frozen_name: Optional[str] = None,
                 cli: bool = False, icon: str = 'icon', component_type: Optional[Type] = None,
                 func: Optional[Callable] = None, file_identifier: Optional[Callable[[str], bool]] = None,
                 game_name: Optional[str] = None, supports_uri: Optional[bool] = False, description: str = "") -> None:
        self.display_name = display_name
        self.description = description
        self.script_name = script_name
        self.frozen_name = frozen_name or (apname + script_name) if script_name else None
        self.icon = icon
        self.cli = cli
        if component_type == Type.FUNC:
            from Utils import deprecate
            deprecate(f"Launcher Component {self.display_name} is using Type.FUNC Type, which is pending removal.")
            component_type = Type.MISC

        self.type = component_type or (
            Type.CLIENT if "Client" in display_name else
            Type.ADJUSTER if "Adjuster" in display_name else Type.MISC)
        self.func = func
        self.file_identifier = file_identifier
        self.game_name = game_name
        self.supports_uri = supports_uri

    def handles_file(self, path: str):
        return self.file_identifier(path) if self.file_identifier else False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.display_name})"


def _is_worlds_loading() -> bool:
    worlds_module = sys.modules.get("worlds")
    return bool(getattr(worlds_module, "_worlds_loading", False))


def _classify_component_origin() -> str:
    if _is_worlds_loading():
        return _COMPONENT_ORIGIN_WORLD
    if _INITIALIZING_COMPONENTS:
        return _COMPONENT_ORIGIN_BUILTIN
    return _COMPONENT_ORIGIN_OTHER


def _component_origin(component: Component) -> str:
    origin = getattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, None)
    return origin if isinstance(origin, str) else _COMPONENT_ORIGIN_OTHER


def _tag_component(component: Component) -> None:
    origin = getattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, None)
    if not isinstance(origin, str):
        origin = _classify_component_origin()
    setattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, origin)


class ComponentList(list[Component]):
    def append(self, component: Component) -> None:
        _tag_component(component)
        super().append(component)

    def extend(self, components: Iterable[Component]) -> None:
        for component in components:
            self.append(component)

    def insert(self, index: int, component: Component) -> None:
        _tag_component(component)
        super().insert(index, component)


processes = weakref.WeakSet()

_rebuild_launcher_ui: Optional[Callable[[], None]] = None


def launch_subprocess(func: Callable, name: str | None = None, args: Tuple[str, ...] = ()) -> None:
    import multiprocessing
    process = multiprocessing.Process(target=func, name=name, args=args)
    process.start()
    processes.add(process)


def launch(func: Callable, name: str | None = None, args: Tuple[str, ...] = ()) -> None:
    from Utils import is_kivy_running
    if is_kivy_running():
        launch_subprocess(func, name, args)
    else:
        func(*args)


class SuffixIdentifier:
    suffixes: Iterable[str]

    def __init__(self, *args: str):
        self.suffixes = args

    def __call__(self, path: str) -> bool:
        if isinstance(path, str):
            for suffix in self.suffixes:
                if path.endswith(suffix):
                    return True
        return False


def launch_textclient(*args):
    import CommonClient
    launch(CommonClient.run_as_textclient, name="TextClient", args=args)


def _install_apworld(apworld_src: str = "") -> Optional[Tuple[pathlib.Path, pathlib.Path]]:
    if not apworld_src:
        apworld_src = open_filename('Select APWorld file to install', (('APWorld', ('.apworld',)),))
        if not apworld_src:
            # user closed menu
            return

    if not apworld_src.endswith(".apworld"):
        raise Exception(f"Wrong file format, looking for .apworld. File identified: {apworld_src}")

    apworld_path = pathlib.Path(apworld_src)

    try:
        import zipfile
        zip = zipfile.ZipFile(apworld_path)
        directories = [f.name for f in zipfile.Path(zip).iterdir() if f.is_dir()]
        if len(directories) == 1 and directories[0] in apworld_path.stem:
            module_name = directories[0]
            apworld_name = module_name + ".apworld"
        else:
            raise Exception("APWorld appears to be invalid or damaged. (expected a single directory)")
        zip.open(module_name + "/__init__.py")
    except ValueError as e:
        raise Exception("Archive appears invalid or damaged.") from e
    except KeyError as e:
        raise Exception("Archive appears to not be an apworld. (missing __init__.py)") from e

    import worlds
    if worlds.user_folder is None:
        raise Exception("Custom Worlds directory appears to not be writable.")
    for world_source in worlds.world_sources:
        if apworld_path.samefile(world_source.resolved_path):
            # Note that this doesn't check if the same world is already installed.
            # It only checks if the user is trying to install the apworld file
            # that comes from the installation location (worlds or custom_worlds)
            raise Exception(f"APWorld is already installed at {world_source.resolved_path}.")

    # TODO: run generic test suite over the apworld.
    # TODO: have some kind of version system to tell from metadata if the apworld should be compatible.

    target = pathlib.Path(worlds.user_folder) / apworld_name
    import shutil
    shutil.copyfile(apworld_path, target)

    # If a module with this name is already loaded, then we can't load it now.
    # TODO: We need to be able to unload a world module,
    # so the user can update a world without restarting the application.
    found_already_loaded = False
    for loaded_world in worlds.world_sources:
        loaded_name = pathlib.Path(loaded_world.path).stem
        if module_name == loaded_name:
            found_already_loaded = True
            break
    if found_already_loaded and is_kivy_running():
        raise Exception(f"Installed APWorld successfully, but '{module_name}' is already loaded, "
                        "so a Launcher restart is required to use the new installation.")
    world_source = worlds.WorldSource(str(target), is_zip=True, relative=False)
    bisect.insort(worlds.world_sources, world_source)
    if world_source.is_zip:
        worlds._register_apworld_zip_spec(world_source)
    components_before = len(components)
    world_source.load()
    new_components = list(components[components_before:])
    for component in new_components:
        setattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, _COMPONENT_ORIGIN_WORLD)
    _merge_installed_world_components_into_cache(new_components)
    worlds.rebuild_world_caches()

    return apworld_path, target


def install_apworld(apworld_path: str = "") -> None:
    try:
        res = _install_apworld(apworld_path)
        if res is None:
            logging.info("Aborting APWorld installation.")
            return
        source, target = res
    except Exception as e:
        import Utils
        Utils.messagebox("Notice", str(e), error=True)
        logging.exception(e)
    else:
        import Utils
        logging.info(f"Installed APWorld successfully, copied {source} to {target}.")
        Utils.messagebox("Install complete.", f"Installed APWorld from {source}.")
        if _rebuild_launcher_ui and is_kivy_running():
            from kivy.clock import Clock
            def _refresh_after_install(dt):
                _hydrate_launcher_components_from_cache()
                _rebuild_launcher_ui()  # type: ignore[misc]
            Clock.schedule_once(_refresh_after_install, 0)


def export_datapackage() -> None:
    import json

    from worlds import network_data_package

    path = user_path("datapackage_export.json")
    with open(path, "w") as f:
        json.dump(network_data_package, f, indent=4)

    open_file(path)


components: ComponentList = ComponentList([
    # Launcher
    Component('Launcher', 'Launcher', component_type=Type.HIDDEN),
    # Core
    Component('Host', 'MultiServer', f'{apname}Server', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.mwgg', '.zip'),
              description="Host a generated multiworld on your computer."),
    Component('Generate', 'Generate', cli=True,
              description="Generate a multiworld with the YAMLs in the players folder."),
    Component("Options Creator", "OptionsCreator", f"{apname}OptionsCreator", component_type=Type.TOOL,
              description=f"Visual creator for {apname} option files."),
    Component("Install APWorld", func=install_apworld, file_identifier=SuffixIdentifier(".apworld"),
              description=f"Install an APWorld to play games not included with {apname} by default."),
    Component('Text Client', 'CommonClient', f'{apname}TextClient', func=launch_textclient,
              description="Connect to a multiworld using the text client."),
    Component("Export Datapackage", func=export_datapackage, component_type=Type.TOOL,
            description="Write item/location data for installed worlds to a file and open it."),
])

for component in components:
    setattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, _COMPONENT_ORIGIN_BUILTIN)


# if registering an icon from within an apworld, the format "ap:module.name/path/to/file.png" can be used
icon_paths = {
    'icon': local_path('data', 'icon.png'),
    'mcicon': local_path('data', 'mcicon.png'),
    'discord': local_path('data', 'discord-mark-blue.png'),
}


def _component_suffixes(component: Component) -> tuple[str, ...]:
    if isinstance(component.file_identifier, SuffixIdentifier):
        return tuple(component.file_identifier.suffixes)
    return ()


def _serializable_callable(func: Optional[Callable]) -> tuple[Optional[str], Optional[str]]:
    if func is None:
        return None, None

    module = getattr(func, "__module__", None)
    qualname = getattr(func, "__qualname__", None)
    if not isinstance(module, str) or not isinstance(qualname, str):
        return None, None
    if "<locals>" in qualname:
        return None, None
    return module, qualname


def _component_identity(component: Component) -> tuple[Any, ...]:
    return (
        component.display_name,
        component.type.name,
        component.icon,
        component.description,
        bool(component.cli),
        component.script_name,
        component.frozen_name,
        component.game_name,
        bool(component.supports_uri),
        _component_suffixes(component),
    )


def _component_identity_from_cache(component_data: dict[str, Any]) -> tuple[Any, ...]:
    return (
        component_data["display_name"],
        component_data["type"],
        component_data["icon"],
        component_data["description"],
        component_data["cli"],
        component_data["script_name"],
        component_data["frozen_name"],
        component_data["game_name"],
        component_data["supports_uri"],
        tuple(component_data["file_suffixes"]),
    )


def _serialize_component(component: Component) -> dict[str, Any]:
    callable_module, callable_qualname = _serializable_callable(component.func)
    return {
        "display_name": component.display_name,
        "type": component.type.name,
        "icon": component.icon,
        "description": component.description,
        "cli": bool(component.cli),
        "script_name": component.script_name,
        "frozen_name": component.frozen_name,
        "game_name": component.game_name,
        "supports_uri": bool(component.supports_uri),
        "file_suffixes": list(_component_suffixes(component)),
        "callable_module": callable_module,
        "callable_qualname": callable_qualname,
    }


def _load_launcher_cache(check_freshness: bool = True) -> dict[str, Any] | None:
    if not os.path.isfile(_LAUNCHER_CACHE_PATH):
        return None

    try:
        with gzip.open(_LAUNCHER_CACHE_PATH, mode="rt", encoding="utf-8") as cache_file:
            payload = json.load(cache_file)
    except Exception as exc:
        logging.warning(f"Failed to read launcher cache from {_LAUNCHER_CACHE_PATH}: {exc}")
        return None

    serialized_components = payload.get("components")
    cached_icon_paths = payload.get("icon_paths")
    if not isinstance(serialized_components, list) or not isinstance(cached_icon_paths, dict):
        return None

    if check_freshness:
        cached_sources = payload.get("world_sources")
        if isinstance(cached_sources, list):
            worlds_module = sys.modules.get("worlds")
            current_sources = sorted(
                ws.path for ws in getattr(worlds_module, "world_sources", [])
            )
            if sorted(cached_sources) != current_sources:
                logging.debug("Launcher cache is stale (world sources changed), ignoring.")
                return None

    sanitized_icon_paths: dict[str, str] = {}
    for icon_key, icon_path in cached_icon_paths.items():
        if not isinstance(icon_key, str) or not isinstance(icon_path, str):
            return None
        sanitized_icon_paths[icon_key] = _normalize_cached_icon_path(icon_path)

    payload["icon_paths"] = sanitized_icon_paths

    for component_data in serialized_components:
        if not isinstance(component_data, dict):
            return None

        if not isinstance(component_data.get("display_name"), str):
            return None
        if not isinstance(component_data.get("type"), str) or component_data["type"] not in Type.__members__:
            return None
        if not isinstance(component_data.get("icon"), str):
            return None
        if not isinstance(component_data.get("description"), str):
            return None
        if not isinstance(component_data.get("cli"), bool):
            return None
        if not isinstance(component_data.get("supports_uri"), bool):
            return None

        script_name = component_data.get("script_name")
        frozen_name = component_data.get("frozen_name")
        game_name = component_data.get("game_name")
        if script_name is not None and not isinstance(script_name, str):
            return None
        if frozen_name is not None and not isinstance(frozen_name, str):
            return None
        if game_name is not None and not isinstance(game_name, str):
            return None

        file_suffixes = component_data.get("file_suffixes")
        if not isinstance(file_suffixes, list) or any(not isinstance(suffix, str) for suffix in file_suffixes):
            return None

        callable_module = component_data.get("callable_module")
        callable_qualname = component_data.get("callable_qualname")
        if callable_module is not None and not isinstance(callable_module, str):
            return None
        if callable_qualname is not None and not isinstance(callable_qualname, str):
            return None

    logging.debug(f"Loaded launcher cache from {_LAUNCHER_CACHE_PATH}.")
    return payload


def _launch_component(component: Component, launch_args: tuple[str, ...]) -> None:
    if component.func:
        component.func(*launch_args)
        return

    if component.script_name:
        from Launcher import get_exe, launch

        exe = get_exe(component)
        if not exe:
            logging.warning(f"Unable to resolve executable for launcher component {component.display_name}.")
            return
        launch([*exe, *launch_args], component.cli)
        return

    logging.warning(f"Component {component.display_name} does not appear to be executable.")


def _find_loaded_component(component_id: tuple[Any, ...]) -> Component | None:
    for component in components:
        if _component_origin(component) == _COMPONENT_ORIGIN_CACHE:
            continue
        if _component_identity(component) == component_id:
            return component
    return None


def _find_cached_stub(component_id: tuple[Any, ...]) -> Component | None:
    for component in components:
        if _component_origin(component) != _COMPONENT_ORIGIN_CACHE:
            continue
        if _component_identity(component) == component_id:
            return component
    return None


def _launch_cached_script_stub(component: Component, launch_args: tuple[str, ...]) -> tuple[bool, subprocess.Popen[Any] | None]:
    if not (component.script_name or component.frozen_name):
        return False, None

    from Launcher import get_exe, launch

    exe = get_exe(component)
    if not exe:
        return False, None
    if is_frozen():
        if not os.path.isfile(exe[0]):
            logging.debug("Cached launcher executable is missing for component %s.", component.display_name)
            return False, None
    elif len(exe) > 1 and not os.path.isfile(exe[1]):
        logging.debug("Cached launcher script is missing for component %s.", component.display_name)
        return False, None

    if component.cli:
        launch([*exe, *launch_args], component.cli)
        return True, None
    try:
        return True, subprocess.Popen([*exe, *launch_args])
    except FileNotFoundError:
        logging.debug("Cached launcher executable is missing for component %s.", component.display_name)
        return False, None


def _launch_cached_callable_stub(callable_module: str | None, callable_qualname: str | None,
                                 launch_args: tuple[str, ...]) -> tuple[bool, subprocess.Popen[Any] | None]:
    if not callable_module or not callable_qualname:
        return False, None

    from Launcher import launch_component_callable
    launched_process = launch_component_callable(callable_module, callable_qualname, launch_args)
    return launched_process is not None, launched_process


def _run_cached_component(component_id: tuple[Any, ...], callable_module: str | None,
                          callable_qualname: str | None, *launch_args: str) -> subprocess.Popen[Any] | None:
    launched, launched_process = _launch_cached_callable_stub(callable_module, callable_qualname, tuple(launch_args))
    if launched:
        return launched_process

    stub = _find_cached_stub(component_id)
    if stub is not None:
        launched, launched_process = _launch_cached_script_stub(stub, tuple(launch_args))
        if launched:
            return launched_process

    # Resolve through fully loaded world components so launch behavior matches the real component.
    from worlds import ensure_worlds_loaded
    ensure_worlds_loaded()
    component = _find_loaded_component(component_id)
    if component is None:
        logging.warning("Failed to resolve cached launcher component after world loading completed.")
        return None
    _launch_component(component, tuple(launch_args))
    return None


def _make_cached_component_func(component_id: tuple[Any, ...], callable_module: str | None,
                                callable_qualname: str | None) -> Callable[..., subprocess.Popen[Any] | None]:
    def _launch_cached(*launch_args: str) -> subprocess.Popen[Any] | None:
        return _run_cached_component(component_id, callable_module, callable_qualname, *launch_args)

    return _launch_cached


def prepare_for_worlds_load() -> None:
    if not components:
        return

    non_cached_components = [
        component for component in components
        if _component_origin(component) != _COMPONENT_ORIGIN_CACHE
    ]
    if len(non_cached_components) != len(components):
        components[:] = non_cached_components


def _hydrate_launcher_components_from_cache() -> None:
    if _is_worlds_loading():
        return

    worlds_module = sys.modules.get("worlds")
    if worlds_module is None:
        return

    payload = _load_launcher_cache()
    if payload is None:
        return

    prepare_for_worlds_load()
    icon_paths.update(payload["icon_paths"])

    known_components = {_component_identity(component) for component in components}
    for component_data in payload["components"]:
        component_id = _component_identity_from_cache(component_data)
        if component_id in known_components:
            continue

        suffixes = tuple(component_data["file_suffixes"])
        file_identifier = SuffixIdentifier(*suffixes) if suffixes else None
        cached_component = Component(
            component_data["display_name"],
            script_name=component_data["script_name"],
            frozen_name=component_data["frozen_name"],
            cli=component_data["cli"],
            icon=component_data["icon"],
            component_type=Type[component_data["type"]],
            func=_make_cached_component_func(
                component_id,
                component_data.get("callable_module"),
                component_data.get("callable_qualname"),
            ),
            file_identifier=file_identifier,
            game_name=component_data["game_name"],
            supports_uri=component_data["supports_uri"],
            description=component_data["description"],
        )
        setattr(cached_component, _COMPONENT_ORIGIN_ATTRIBUTE, _COMPONENT_ORIGIN_CACHE)
        components.append(cached_component)
        known_components.add(component_id)


def _write_cache_payload(payload: dict[str, Any]) -> None:
    cache_dir = os.path.dirname(_LAUNCHER_CACHE_PATH)
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)

    temp_file_path = ""
    try:
        file_descriptor, temp_file_path = tempfile.mkstemp(
            prefix="world_launcher_cache.",
            suffix=".tmp",
            dir=cache_dir or None,
        )
        with os.fdopen(file_descriptor, mode="wb") as temp_file:
            with gzip.GzipFile(fileobj=temp_file, mode="wb") as gzip_file:
                gzip_file.write(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            temp_file.flush()
            if hasattr(os, "fsync"):
                os.fsync(temp_file.fileno())

        os.replace(temp_file_path, _LAUNCHER_CACHE_PATH)
        logging.debug(f"Wrote launcher cache to {_LAUNCHER_CACHE_PATH}.")
    except Exception as exc:
        logging.warning(f"Failed to write launcher cache to {_LAUNCHER_CACHE_PATH}: {exc}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass


def write_launcher_cache() -> None:
    worlds_module = sys.modules.get("worlds")
    world_source_paths = sorted(
        ws.path for ws in getattr(worlds_module, "world_sources", [])
    )
    serialized_components = [
        _serialize_component(component)
        for component in components
        if _component_origin(component) == _COMPONENT_ORIGIN_WORLD
    ]
    serialized_icon_paths = {
        icon_key: icon_path
        for icon_key, icon_path in icon_paths.items()
        if isinstance(icon_key, str) and isinstance(icon_path, str)
    }
    _write_cache_payload({
        "components": serialized_components,
        "icon_paths": serialized_icon_paths,
        "world_sources": world_source_paths,
    })


def _merge_installed_world_components_into_cache(new_components: list[Component]) -> None:
    """Merge newly installed world's components into the existing launcher cache."""
    if not new_components:
        return

    new_entries = {
        _component_identity(c): _serialize_component(c)
        for c in new_components
    }

    # Skip freshness check — we're updating the cache after adding a new source.
    payload = _load_launcher_cache(check_freshness=False)
    if payload is None:
        payload = {"components": [], "icon_paths": {}}

    merged_components: dict[tuple, dict[str, Any]] = {}
    for entry in payload["components"]:
        merged_components[_component_identity_from_cache(entry)] = entry
    merged_components.update(new_entries)

    worlds_module = sys.modules.get("worlds")
    world_source_paths = sorted(
        ws.path for ws in getattr(worlds_module, "world_sources", [])
    )

    merged_icon_paths = dict(payload.get("icon_paths", {}))
    merged_icon_paths.update({
        k: v for k, v in icon_paths.items()
        if isinstance(k, str) and isinstance(v, str)
    })

    _write_cache_payload({
        "components": list(merged_components.values()),
        "icon_paths": merged_icon_paths,
        "world_sources": world_source_paths,
    })


def _normalize_cached_icon_path(icon_path: str) -> str:
    if icon_path.startswith("ap:"):
        return icon_path
    if os.path.isfile(icon_path):
        return icon_path

    icon_basename = os.path.basename(icon_path)
    if icon_basename:
        candidate_data_path = local_path("data", icon_basename)
        if os.path.isfile(candidate_data_path):
            return candidate_data_path

    return _DEFAULT_ICON_PATH


def resolve_icon_path(icon_path: str) -> str:
    if icon_path.startswith("ap:"):
        return _materialize_ap_icon(icon_path)
    return _normalize_cached_icon_path(icon_path)


def _materialize_ap_icon(icon_path: str) -> str:
    module_resource_path = icon_path.removeprefix("ap:")
    module_name, separator, resource_name = module_resource_path.partition("/")
    if not separator or not module_name or not resource_name:
        return _DEFAULT_ICON_PATH

    try:
        resource_data = pkgutil.get_data(module_name, resource_name)
    except Exception:
        resource_data = None
    if not resource_data:
        return _DEFAULT_ICON_PATH

    resource_extension = os.path.splitext(resource_name)[1] or ".png"
    icon_hash = hashlib.sha256(resource_data).hexdigest()
    icon_path_on_disk = os.path.join(_LAUNCHER_ICON_CACHE_DIR, f"{icon_hash}{resource_extension}")
    if os.path.isfile(icon_path_on_disk):
        return icon_path_on_disk

    try:
        os.makedirs(_LAUNCHER_ICON_CACHE_DIR, exist_ok=True)
        with open(icon_path_on_disk, "wb") as icon_file:
            icon_file.write(resource_data)
    except Exception:
        return _DEFAULT_ICON_PATH

    return icon_path_on_disk


def has_world_components() -> bool:
    return any(
        _component_origin(component) in {_COMPONENT_ORIGIN_WORLD, _COMPONENT_ORIGIN_CACHE}
        for component in components
    )


if not is_frozen():
    def _build_apworlds(*launch_args: str):
        import json
        import os
        import zipfile

        from worlds import AutoWorldRegister
        from worlds import ensure_worlds_loaded
        from worlds.Files import APWorldContainer
        from Launcher import open_folder

        ensure_worlds_loaded()

        import argparse
        parser = argparse.ArgumentParser(prog="Build APWorlds", description="Build script for APWorlds")
        parser.add_argument("worlds", type=str, default=(), nargs="*", help="names of APWorlds to build")
        parser.add_argument("--skip_open_folder", action="store_true", help="don't open the output build folder")
        args = parser.parse_args(launch_args)

        if args.worlds:
            games = [(game, AutoWorldRegister.world_types.get(game, None)) for game in args.worlds]
        else:
            games = [(worldname, worldtype) for worldname, worldtype in AutoWorldRegister.world_types.items()
                     if not worldtype.zip_path]

        global_apignores = read_apignore(local_path("data", "GLOBAL.apignore"))
        if not global_apignores:
            raise RuntimeError("Could not read global apignore file for build component")

        apworlds_folder = os.path.join("build", "apworlds")
        os.makedirs(apworlds_folder, exist_ok=True)
        for worldname, worldtype in games:
            if not worldtype:
                logging.error(f"Requested APWorld \"{worldname}\" does not exist.")
                continue
            file_name = os.path.split(os.path.dirname(worldtype.__file__))[1]
            world_directory = os.path.join("worlds", file_name)
            if os.path.isfile(os.path.join(world_directory, "archipelago.json")):
                with open(os.path.join(world_directory, "archipelago.json"), mode="r", encoding="utf-8") as manifest_file:
                    manifest = json.load(manifest_file)

                assert "game" in manifest, (
                    f"World directory {world_directory} has an archipelago.json manifest file, but it "
                    "does not define a \"game\"."
                )
                assert manifest["game"] == worldtype.game, (
                    f"World directory {world_directory} has an archipelago.json manifest file, but value of the "
                    f"\"game\" field ({manifest['game']} does not equal the World class's game ({worldtype.game})."
                )
            else:
                manifest = {}

            zip_path = os.path.join(apworlds_folder, file_name + ".apworld")
            apworld = APWorldContainer(str(zip_path))
            apworld.game = worldtype.game
            manifest.update(apworld.get_manifest())
            apworld.manifest_path = os.path.join(file_name, "archipelago.json")

            local_ignores = read_apignore(pathlib.Path(world_directory, ".apignore"))
            apignores = global_apignores + local_ignores if local_ignores else global_apignores

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for file in apignores.match_tree_files(world_directory, negate=True):
                    zf.write(pathlib.Path(world_directory, file), pathlib.Path(file_name, file))

                zf.writestr(apworld.manifest_path, json.dumps(manifest))

        if not args.skip_open_folder:
            open_folder(apworlds_folder)

    components.append(Component("Build APWorlds", func=_build_apworlds, cli=True,
                                description="Build APWorlds from loose-file world folders."))


_INITIALIZING_COMPONENTS = False
_hydrate_launcher_components_from_cache()
