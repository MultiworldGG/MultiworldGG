from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups


class PikunikuWebWorld(WebWorld):
    game = "Pikuniku"
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Pikuniku for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jeffdev", "EthanScraggy22"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
