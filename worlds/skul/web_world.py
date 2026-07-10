from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class SkulWebWorld(WebWorld):
    game = "Skul: The Hero Slayer"
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Skul: The Hero Slayer for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Yacob", "Jeffdev"],
    )

    tutorials = [setup_en]
