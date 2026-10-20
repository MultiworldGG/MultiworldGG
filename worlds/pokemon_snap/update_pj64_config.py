# Massive credit to Donkey Kong 64 Randomizer for figuring out PJ64 LUA support.
from configparser import ConfigParser
import uuid
from .constants import CLIENT_NAME, ADAPTER_SCRIPT_NAME, PJ64_ENCODING, PJ64_PORT_KEY_NAME
import Utils

from pathlib import Path
from settings import get_settings, Settings

from logging import getLogger
logger = getLogger(CLIENT_NAME)

def safe_load_pj64_config() -> int:
    options: Settings = get_settings()
    # use_pj64: bool = bool(options["pokemon_snap_options"]["use_pj64"]) To be used maybe later
    pj64_exe_path: str = str(options["pokemon_snap_options"]["emulator_settings"]["path"])
    if not Path.exists(Path(pj64_exe_path)):
        pj64_exe_path = Utils.user_path(pj64_exe_path)

    pj64_parent_folder: Path = Path(pj64_exe_path).parent
    pj64_cfg_path: str = str(Path.joinpath(pj64_parent_folder, "Config", "Project64.cfg"))
    pj64_scripts_dir_path: Path = Path.joinpath(pj64_parent_folder, "Scripts")
    pj64_scripts_path: Path = Path.joinpath(pj64_scripts_dir_path, ADAPTER_SCRIPT_NAME)

    # Through some various controller setup testing, PJ64 does some weird formatting and sometimes
    #   pushes values to new lines. allow_no_value=True stops crashes on these corrupted/stray lines
    config: ConfigParser = ConfigParser(allow_no_value=True)
    config.optionxform = str # Forces output in the same format as the input in cfg
    config_updated: bool = False

    with open(pj64_cfg_path, 'r', encoding=PJ64_ENCODING) as f:
        config.read_file(f)

    if "Basic Mode" not in config["Settings"]:
        config.set("Settings", "Basic Mode", "0")
        config_updated = True

    if "Debugger" not in config:
        config.add_section("Debugger")
        config_updated = True

    # PJ64 only runs the autorun list when the debugger is enabled.
    if config.get("Debugger", "Debugger", fallback="0") != "1":
        config.set("Debugger", "Debugger", "1")
        config_updated = True

    # Pipe-delimited list; keep other scripts, drop stale PSAP adapters.
    existing: str = config.get("Debugger", "Autorun Scripts", fallback="")
    entries = [e.strip() for e in existing.split("|")
               if e.strip() and not e.strip().startswith("ap_psnap_pj64_adapter")]
    entries.append(ADAPTER_SCRIPT_NAME)
    autorun_val = "|".join(entries)
    if existing != autorun_val:
        config.set("Debugger", "Autorun Scripts", autorun_val)
        config_updated = True

    if not PJ64_PORT_KEY_NAME in config["Debugger"]:
        port = str(40000 + (uuid.uuid4().int % 10000))
        config.set("Debugger", PJ64_PORT_KEY_NAME, port)
        logger.info("Set port to " + str(port))
        config_updated = True

    # Always write the script so that we can force it to update
    Path.mkdir(pj64_scripts_dir_path, exist_ok=True)
    from importlib import resources
    adapter_str: str = resources.files("worlds.pokemon_snap").joinpath("data", ADAPTER_SCRIPT_NAME).read_text("utf-8")
    with open(str(pj64_scripts_path), 'w', encoding="utf-8") as f:
        f.write(adapter_str)

    ap_port: int = int(config.get("Debugger", PJ64_PORT_KEY_NAME))

    if config_updated:
        try:
            with open(pj64_cfg_path, 'w', encoding=PJ64_ENCODING) as f:
                config.write(f, space_around_delimiters=False)
            logger.info("Config successfully updated.")
        except Exception as e:
            logger.error("Error while updated PJ64 configuration. If this is your first time playing Pokemon Snap AP, "
                "you may need to close PJ64 and open the Pokemon Snap client first to update PJ64's settings file.")
            logger.error(f"Additional details about failure: {str(e)}")

    return ap_port