#im still too lazy to create an actual webworld, this is just for option grouping since its here for whatever reason

from worlds.AutoWorld import WebWorld
from BaseClasses import Tutorial
from .Options import option_groups
from . import Options

class SM64HackWebWorld(WebWorld):
    display_name = "Super Mario 64 Romhacks"
    bug_report_page = "https://github.com/DNVIC/archipelago-sm64hacks/issues"
    theme = "partyTime"
    tutorials = [
        Tutorial(
            "Setup Guide",
            "A guide to playing Romhacks for SM64 in MWGG.",
            "English",
            "setup_en.md",
            "setup/en",
            ["DNVIC"]
        )
    ]
    option_groups = option_groups
