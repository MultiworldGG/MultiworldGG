import datetime
import logging
from collections import Counter
from typing import Dict, TextIO, List

from .items import item_table, item_name_groups, item_name_to_id, create_item, create_all_items
from .locations import get_location_datas, EventId
from .regions import create_regions_and_locations
from BaseClasses import Tutorial, Item, ItemClassification
from .options import AM2ROptions, LocationSettings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, icon_paths, launch

import os
import ssl
import json
import urllib.request
import zipfile
from pathlib import Path
from io import TextIOWrapper

logger = logging.getLogger("AM2R")

# Ensure module-level CA bundle is available to stdlib SSL where possible.
def _ensure_module_certs() -> None:
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
        logger.debug("AM2R: using certifi CA bundle %s", certifi.where())
    except Exception:
        logger.debug("AM2R: certifi not available; will try per-request contexts")

# Call early so stdlib SSL picks it up when possible
_ensure_module_certs()

def _open_url(url: str, timeout: int = 10) -> dict:
    def _read_with_ctx(ctx):
        if ctx is None:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        else:
            with urllib.request.urlopen(url, context=ctx, timeout=timeout) as resp:
                return json.loads(resp.read().decode())

    try:
        return _read_with_ctx(None)
    except Exception as e_default:
        logger.debug("AM2R default SSL fetch failed: %s", e_default)

    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        return _read_with_ctx(ctx)
    except Exception as e_certifi:
        logger.debug("AM2R certifi-backed fetch failed: %s", e_certifi)

    try:
        ctx = ssl._create_unverified_context()
        logger.warning("AM2R: falling back to unverified SSL context for remote metadata fetch (insecure).")
        return _read_with_ctx(ctx)
    except Exception as e_unverified:
        logger.warning("AM2R: all attempts to fetch URL failed: %s", e_unverified)
        raise

def _parse_version(v):
    if not v:
        return ()
    parts = []
    for p in str(v).split("."):
        try:
            parts.append(int(p))
        except Exception:
            parts.append(p)
    return tuple(parts)

def _compare_versions(a, b):
    pa = _parse_version(a)
    pb = _parse_version(b)
    for xa, xb in zip(pa, pb):
        if xa == xb:
            continue
        try:
            return (xa > xb) - (xa < xb)
        except Exception:
            xa_s, xb_s = str(xa), str(xb)
            return (xa_s > xb_s) - (xa_s < xb_s)
    return (len(pa) > len(pb)) - (len(pa) < len(pb))

def get_version():
    metadata_json = {}
    url = "https://raw.githubusercontent.com/Ehseezed/Archipelago-Integration/refs/heads/8th-Aniversary/worlds/am2r/archipelago.json"

    try:
        metadata_json = _open_url(url)
    except Exception as e:
        logger.warning("Failed to fetch remote metadata: %s", e)
        metadata_json = {}

    dirpath = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(dirpath, "archipelago.json")
    local_json = {}

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            local_json = json.load(f)
    except Exception:
        try:
            p = Path(dirpath)
            parts = p.parts
            ap_index = next((i for i, part in enumerate(parts) if part.lower().endswith(".apworld")), None)
            if ap_index is not None:
                archive_path = Path(*parts[: ap_index + 1])
                internal_parts = parts[ap_index + 1 :]
                candidate = "/".join((*internal_parts, "archipelago.json")) if internal_parts else "archipelago.json"
                try:
                    with zipfile.ZipFile(str(archive_path), "r") as z:
                        namelist = z.namelist()
                        target = candidate if candidate in namelist else next((n for n in namelist if n.lower().endswith("archipelago.json")), None)
                        if target:
                            with z.open(target) as bf:
                                with TextIOWrapper(bf, encoding="utf-8") as f:
                                    local_json = json.load(f)
                        else:
                            logger.warning("No archipelago.json found inside archive %s (checked %s)", archive_path, candidate)
                except Exception as e:
                    logger.warning("Failed to read metadata from archive %s: %s", archive_path, e)
            else:
                logger.debug("Failed to read local metadata: file not found at %s", full_path)
        except Exception as e:
            logger.warning("Failed to locate .apworld archive for local metadata: %s", e)

    web_version = metadata_json.get("world_version") if metadata_json else None
    local_version = local_json.get("world_version") if local_json else None
    return local_version, web_version


def launch_client():
    from .Client import launch as am2r_client
    launch(am2r_client, name="AM2RClient")

icon_paths["am2r_icon"] = f"ap:{__name__}/icon.png"
components.append(
    Component("AM2R Client", func=launch_client, component_type=Type.CLIENT, icon="am2r_icon")
)



def _parse_version(v):
    if not v:
        return ()
    parts = []
    for p in str(v).split("."):
        try:
            parts.append(int(p))
        except Exception:
            # non-numeric parts are compared lexically as backup
            parts.append(p)
    return tuple(parts)

def _compare_versions(a, b):
    pa = _parse_version(a)
    pb = _parse_version(b)
    # compare element-wise
    for xa, xb in zip(pa, pb):
        if xa == xb:
            continue
        try:
            return (xa > xb) - (xa < xb)
        except Exception:
            # fallback to string compare if different types
            xa_s, xb_s = str(xa), str(xb)
            return (xa_s > xb_s) - (xa_s < xb_s)
    # longer version is greater if prefix equal
    return (len(pa) > len(pb)) - (len(pa) < len(pb))


def get_version():
    import urllib.request
    import os
    import json
    import zipfile
    from pathlib import Path
    from io import TextIOWrapper
    import ssl

    metadata_json = {}
    url = "https://raw.githubusercontent.com/Ehseezed/Archipelago-Integration/refs/heads/8th-Aniversary/worlds/am2r/archipelago.json"

    def _fetch_with_context(ctx):
        if ctx is None:
            with urllib.request.urlopen(url) as metadata_resp:
                return json.loads(metadata_resp.read().decode())
        else:
            with urllib.request.urlopen(url, context=ctx) as metadata_resp:
                return json.loads(metadata_resp.read().decode())

    try:
        metadata_json = _fetch_with_context(None)
    except Exception as e:
        logger.warning(f"Failed to fetch remote metadata: {e}")
        # Try certifi-provided CA bundle if available
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
            metadata_json = _fetch_with_context(ctx)
        except Exception as e2:
            logger.warning(f"Retry with certifi failed: {e2}")
            # Last-resort: unverified context (warn loudly)
            try:
                ctx = ssl._create_unverified_context()
                logger.warning("Falling back to unverified SSL context for remote metadata fetch (not recommended).")
                metadata_json = _fetch_with_context(ctx)
            except Exception as e3:
                logger.warning(f"All remote metadata fetch attempts failed: {e3}")
                metadata_json = {}

    dirpath = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(dirpath, "archipelago.json")
    local_json = {}

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            local_json = json.load(f)
    except Exception:
        try:
            p = Path(dirpath)
            parts = p.parts
            ap_index = next((i for i, part in enumerate(parts) if part.lower().endswith(".apworld")), None)
            if ap_index is not None:
                archive_path = Path(*parts[: ap_index + 1])
                internal_parts = parts[ap_index + 1 :]
                candidate = "/".join((*internal_parts, "archipelago.json")) if internal_parts else "archipelago.json"
                try:
                    with zipfile.ZipFile(str(archive_path), "r") as z:
                        namelist = z.namelist()
                        target = candidate if candidate in namelist else next((n for n in namelist if n.lower().endswith("archipelago.json")), None)
                        if target:
                            with z.open(target) as bf:
                                with TextIOWrapper(bf, encoding="utf-8") as f:
                                    local_json = json.load(f)
                        else:
                            logger.warning(f"No archipelago.json found inside archive {archive_path} (checked {candidate})")
                except Exception as e:
                    logger.warning(f"Failed to read metadata from archive {archive_path}: {e}")
            else:
                logger.warning(f"Failed to read local metadata: file not found at {full_path}")
        except Exception as e:
            logger.warning(f"Failed to locate .apworld archive for local metadata: {e}")

    web_version = metadata_json.get("world_version") if metadata_json else None
    local_version = local_json.get("world_version") if local_json else None
    return local_version, web_version



class AM2RWeb(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://github.com/Ehseezed/Archipelago-Integration/issues"
    tutorials = [
        Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MultiworldGG AM2R software on your computer. This guide covers single-player, multiworld, multitroid, and related software.",
        "English",
        "setup_en_mwgg.md",
        "setup/en",
        ["Zed"]
    )]


class AM2RWorld(World):
    """
    AM2R is a remake of the classic Metroid 2 game for the Game Boy that tries its best to keep the feel
    of the original as well as filling in some gaps to more closely tie into Metroid Fusion and brings some
    items from there as well.
    """
    game = "AM2R"
    options: AM2ROptions
    options_dataclass = AM2ROptions

    web = AM2RWeb()

    item_name_to_id = item_name_to_id
    location_name_to_id = {location.name: location.code for location in get_location_datas(None, None)}

    item_name_groups = item_name_groups
    data_version = 1

    def fill_slot_data(self) -> Dict[str, object]:
        local_version, web_version = get_version()
        try:
            if local_version is None or web_version is None:
                raise ValueError("One or both version values are not valid")
            cmp = _compare_versions(local_version, web_version)
            if cmp < 0:
                logger.warning(
                    "A new version of AM2R is available: latest %s, you are using %s. Consider updating.",
                    web_version, local_version
                )
            elif cmp > 0:
                logger.warning(
                    "Development version detected: you are running AM2R %s ahead of latest release %s.",
                    local_version, web_version
                )
        except Exception as e:
            err = "Failed to validate version data because: "
            if local_version is None:
                err += "local version is invalid. "
            if web_version is None:
                err += "web version is invalid. "
            logger.warning(err + str(e))

        local_version = "unknown" if local_version is None else local_version
        if datetime.datetime.now().month == 4 and datetime.datetime.now().day == 1:
             isAprilFool = True
        else:
            isAprilFool = False

        return {
            "Version": local_version,
            "MetroidsRequired": self.options.MetroidsRequired.value,
            "TrapFillPercentage": self.options.TrapFillPercentage.value,
            "TrapSprites": self.options.TrapSprites.value,
            "Tozos": self.options.Tozos.value,
            "CustomDeathLinkMessages": list(self.options.CustomDeathLinkMessages.value),
            "DeathlinkMessagePacks": list(self.options.DeathlinkMessagePacks.value),
            "DeathLink": self.options.DeathLink.value,
            "TrapSeed": self.options.WrongWarpTrapSeed.value,
            "AprilFoolsSurprise": True if isAprilFool else self.options.ForceAprilFoolsSurprise.value,
        }

    def create_regions(self) -> None:
        create_regions_and_locations(self.multiworld, self.player)
        self.multiworld.get_location("The Last Metroid is in Captivity", self.player).place_locked_item(self.create_event("The Galaxy is at Peace"))

    def create_item(self, name: str) -> Item:
        return create_item(self.player, name, True)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        if self.options.MetroidsRequired > self.options.MetroidsInPool:
            logger.warning(f"Metroids in pool raised to {self.options.MetroidsRequired.value} for {self.multiworld.get_player_name(self.player)} because the given count was too low for the requirement.")
        if self.options.LocationSettings != LocationSettings.option_add_metroids_and_A6:
            self.multiworld.get_location("Deep Caves: Lil\' Bro", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Deep Caves: Big Sis", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Omega Nest: SA-X Queen Lucina", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Omega Nest: Epsilon", self.player).place_locked_item(self.create_item("Metroid"))
            self.multiworld.get_location("Omega Nest: Druid", self.player).place_locked_item(self.create_item("Metroid"))
            if self.options.LocationSettings != LocationSettings.option_add_metroids_no_A6:
                self.multiworld.get_location("The Forgotten Alpha", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple: Friendly Spider", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple Nest: Moe", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple Nest: Larry", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Golden Temple Nest: Curly", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Main Caves: Freddy Fazbear", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Station: Turbine Terror", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Station: The Lookout", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Station: Recent Guardian", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: EnderMahan", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: Carnage Awful", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: Venom Awesome", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Hydro Nest: Something More, Something Awesome",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: Mimolette", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: The Big Cheese", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: Mohwir", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: Chirn", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: BHHarbinger", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Nest: AbyssalCreature", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Complex: Sisyphus", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Industrial Complex: And then there\'s this Asshole",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Inside Industrial: Guardian of Doom Treadmill",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Inside Industrial: Rawsome1234 by the Lava Lake",self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Research Camp Dual Alphas: Marco", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Research Camp Dual Alphas: Polo", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Mines: Unga", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Mines: Gunga", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Patricia", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Variable \"GUH\"", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Slagathor, the Ruler", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Mr.Sandman", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Anakin", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("The Tower: Xander", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("EMP: Sir Zeta Commander of the Alpha Squadron", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Timmy", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Tommy", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Terry", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Telly", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center Alpha Squadron: Martin", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center: Gamma Bros Mario", self.player).place_locked_item(self.create_item("Metroid"))
                self.multiworld.get_location("Distribution Center: Gamma Bros Luigi", self.player).place_locked_item(self.create_item("Metroid"))

        if self.options.LocationSettings == LocationSettings.option_items_no_A6 or self.options.LocationSettings == LocationSettings.option_add_metroids_no_A6:
            self.options.exclude_locations.value.add("Deep Caves: Drivel Ballspark")
            self.options.exclude_locations.value.add("Deep Caves: Ramulken Lava Pool")
            self.options.exclude_locations.value.add("Deep Caves: After Omega")

        create_all_items(self)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("The Galaxy is at Peace", self.player)
