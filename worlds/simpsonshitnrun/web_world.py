from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups

class SimpsonsHitNRunWebWorld(WebWorld):
    game = "Simpsons Hit and Run"

    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up The Simpsons Hit and Run for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Caesius"],
    )

    tutorials = [setup_en]

    option_groups = option_groups