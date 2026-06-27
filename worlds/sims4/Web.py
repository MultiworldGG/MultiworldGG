from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class Sims4Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up The Sims 4 for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["mrsummer360"]
    )]