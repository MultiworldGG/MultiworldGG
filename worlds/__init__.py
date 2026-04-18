import importlib
import importlib.abc
import importlib.machinery
import logging
import os
import sys
import zipimport
import time
import dataclasses
import json
from pathlib import Path
from types import ModuleType
from typing import List, Sequence, Dict
from zipfile import BadZipFile
import threading

from NetUtils import DataPackage
from Utils import local_path, user_path, Version, version_tuple, tuplize_version, messagebox

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
try:
    os.makedirs(user_folder, exist_ok=True)
except OSError:  # can't access/write?
    user_folder = None

__all__ = [
    "network_data_package",
    "network_data_package_single_game",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "failed_world_loads",
    "ensure_worlds_loaded",
    "rebuild_world_caches",
]


failed_world_loads: List[str] = []


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str  # typically relative path from this module
    is_zip: bool = False
    relative: bool = True  # relative to regular world import folder
    time_taken: float = -1.0
    version: Version = Version(0, 0, 0)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip}, relative={self.relative})"

    @property
    def resolved_path(self) -> str:
        if self.relative:
            return os.path.join(local_folder, self.path)
        return self.path

    def load(self) -> bool:
        try:
            start = time.perf_counter()
            importlib.import_module(f".{Path(self.path).stem}", "worlds")
            self.time_taken = time.perf_counter()-start
            return True

        except Exception:
            # A single world failing can still mean enough is working for the user, log and carry on
            import traceback
            import io
            file_like = io.StringIO()
            print(f"Could not load world {self}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            logging.exception(file_like.read())
            failed_world_loads.append(os.path.basename(self.path).rsplit(".", 1)[0])
            return False


# find potential world containers, currently folders and zip-importable .apworld's
def _scan_world_sources() -> List[WorldSource]:
    scanned_world_sources: List[WorldSource] = []
    for folder in (folder for folder in (user_folder, local_folder) if folder):
        relative = folder == local_folder
        for entry in os.scandir(folder):
            # prevent loading of __pycache__ and allow _* for non-world folders, disable files/folders starting with "."
            if not entry.name.startswith(("_", ".")):
                file_name = entry.name if relative else os.path.join(folder, entry.name)
                if entry.is_dir():
                    if os.path.isfile(os.path.join(entry.path, '__init__.py')):
                        scanned_world_sources.append(WorldSource(file_name, relative=relative))
                    elif os.path.isfile(os.path.join(entry.path, '__init__.pyc')):
                        scanned_world_sources.append(WorldSource(file_name, relative=relative))
                    else:
                        logging.warning(f"excluding {entry.name} from world sources because it has no __init__.py")
                elif entry.is_file() and entry.name.endswith(".apworld"):
                    scanned_world_sources.append(WorldSource(file_name, is_zip=True, relative=relative))
    scanned_world_sources.sort()
    return scanned_world_sources

world_sources: List[WorldSource] = _scan_world_sources()

from .AutoWorld import AutoWorldRegister

_worlds_loaded = False
_worlds_loading = False
_worlds_load_lock = threading.Lock()
_worlds_load_owner_thread_id: int | None = None

network_data_package: DataPackage
network_data_package_single_game: Dict[str, DataPackage]

from ._world_cache import (
    has_launcher_cache,
    rebuild_world_caches,
)


def _load_loose_worlds() -> list[WorldSource]:
    apworlds: list[WorldSource] = []
    for world_source in world_sources:
        # load all loose files first:
        if world_source.is_zip:
            apworlds.append(world_source)
        else:
            world_source.load()

    for world_source in world_sources:
        if world_source.is_zip:
            continue
        # look for manifest
        manifest = {}
        for dirpath, dirnames, filenames in os.walk(world_source.resolved_path):
            for file in filenames:
                if file.endswith("archipelago.json"):
                    with open(os.path.join(dirpath, file), mode="r", encoding="utf-8") as manifest_file:
                        manifest = json.load(manifest_file)
                    break
            if manifest:
                break
        game = manifest.get("game")
        if game in AutoWorldRegister.world_types:
            AutoWorldRegister.world_types[game].world_version = tuplize_version(manifest.get("world_version", "0.0.0"))
    return apworlds


_apworld_module_specs: dict[str, importlib.machinery.ModuleSpec] = {}


class _APWorldModuleFinder(importlib.abc.MetaPathFinder):
    def find_spec(
            self, fullname: str, _path: Sequence[str] | None, _target: ModuleType = None
    ) -> importlib.machinery.ModuleSpec | None:
        return _apworld_module_specs.get(fullname)


sys.meta_path.insert(0, _APWorldModuleFinder())


def _register_apworld_zip_spec(world_source: WorldSource) -> None:
    """Register the zip import spec for a single apworld so it can be imported."""
    world_name = Path(world_source.path).stem
    importer = zipimport.zipimporter(world_source.resolved_path)
    spec = importer.find_spec(f"worlds.{world_name}")
    if spec is not None:
        _apworld_module_specs[f"worlds.{world_name}"] = spec


def _load_apworlds(apworlds: list[WorldSource]) -> None:
    from .Files import APWorldContainer, InvalidDataError

    core_compatible: list[tuple[WorldSource, APWorldContainer]] = []

    def fail_world(game_name: str, reason: str, add_as_failed_to_load: bool = True) -> None:
        if add_as_failed_to_load:
            failed_world_loads.append(game_name)
        logging.warning(reason)

    for apworld_source in apworlds:
        apworld: APWorldContainer = APWorldContainer(apworld_source.resolved_path)
        # populate metadata
        try:
            apworld.read()
        except InvalidDataError as e:
            if version_tuple < (0, 7, 250):
                logging.error(
                    f"Invalid or missing manifest file for {apworld_source.resolved_path}. "
                    "This apworld will stop working with MultiworldGG ~v0.7.250."
                )
                logging.error(e)
            else:
                raise e
        except BadZipFile as e:
            err_message = (f"The world source {apworld_source.resolved_path} is not a valid zip. "
                           "It is likely either corrupted, or was packaged incorrectly.")

            if sys.stdout:
                raise RuntimeError(err_message) from e
            else:
                messagebox("Couldn't load worlds", err_message, error=True)
                sys.exit(1)

        if apworld.minimum_ap_version and apworld.minimum_ap_version > version_tuple:
            fail_world(apworld.game,
                       f"Did not load {apworld_source.path} "
                       f"as its minimum core version {apworld.minimum_ap_version} "
                       f"is higher than current core version {version_tuple}.")
        elif apworld.maximum_ap_version and apworld.maximum_ap_version < version_tuple:
            fail_world(apworld.game,
                       f"Did not load {apworld_source.path} "
                       f"as its maximum core version {apworld.maximum_ap_version} "
                       f"is lower than current core version {version_tuple}.")
        else:
            core_compatible.append((apworld_source, apworld))
    # load highest version first
    core_compatible.sort(
        key=lambda element: element[1].world_version if element[1].world_version else Version(0, 0, 0),
        reverse=True)

    for apworld_source, apworld in core_compatible:
        if apworld.game and apworld.game in AutoWorldRegister.world_types:
            fail_world(apworld.game,
                       f"Did not load {apworld_source.path} "
                       f"as its game {apworld.game} is already loaded.",
                       add_as_failed_to_load=False)
        else:
            _register_apworld_zip_spec(apworld_source)

            apworld_source.load()
            if apworld.game in AutoWorldRegister.world_types:
                # world could fail to load at this point
                if apworld.world_version:
                    AutoWorldRegister.world_types[apworld.game].world_version = apworld.world_version

def _build_network_data_packages() -> None:
    global network_data_package
    global network_data_package_single_game

    # Build the data package for each game.
    network_data_package = {
        "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
    }

    network_data_package_single_game = {
        game_name: {"games": {game_name: pkg_data}}
        for game_name, pkg_data in network_data_package["games"].items()
    }


def ensure_worlds_loaded() -> None:
    global _worlds_loaded
    global _worlds_loading
    global _worlds_load_owner_thread_id

    if _worlds_loaded:
        return

    current_thread_id = threading.get_ident()
    if _worlds_loading and _worlds_load_owner_thread_id == current_thread_id:
        # Guard re-entrant calls from the same loader thread.
        return

    with _worlds_load_lock:
        if _worlds_loaded:
            return

        _worlds_load_owner_thread_id = current_thread_id
        _worlds_loading = True
        try:
            try:
                from . import LauncherComponents
                LauncherComponents.prepare_for_worlds_load()
            except Exception as exc:
                logging.warning(f"Failed to prepare launcher components for world loading: {exc}")

            failed_world_loads.clear()
            apworlds = _load_loose_worlds()
            if apworlds:
                _load_apworlds(apworlds)
            _build_network_data_packages()

            if not has_launcher_cache():
                try:
                    from . import LauncherComponents
                    LauncherComponents.write_launcher_cache()
                except Exception as exc:
                    logging.warning(f"Failed to write launcher cache: {exc}")

            _worlds_loaded = True
        finally:
            _worlds_loading = False
            _worlds_load_owner_thread_id = None


def __getattr__(name: str):
    if name in {"network_data_package", "network_data_package_single_game"}:
        if name in globals():
            return globals()[name]

        if _worlds_loading:
            raise RuntimeError(
                f"Requested worlds.{name} while worlds are loading. "
                "This access during import can deadlock world initialization."
            )

        ensure_worlds_loaded()
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
