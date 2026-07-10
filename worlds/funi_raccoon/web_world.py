from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class FuniRaccoonWebWorld(WebWorld):
    game = "Funi Raccoon Game"
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Funi Raccoon Game for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jeffdev"],
    )

    tutorials = [setup_en]
