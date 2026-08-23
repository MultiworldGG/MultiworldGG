from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class UncannyCatWebWorld(WebWorld):
    game = "Uncanny Cat Golf"
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Uncanny Cat Golf for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jeffdev"],
    )

    tutorials = [setup_en]
