from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class TwoThousandAndFortyEightWebWorld(WebWorld):
    game = "2048"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up 2048 for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ishigh"],
    )

    tutorials = [setup_en]
