from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class Duke3DWebWorld(WebWorld):
    game = "Duke Nukem 3D"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Duke Nukem 3D for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["randomcodegen"],
    )

    tutorials = [setup_en]
