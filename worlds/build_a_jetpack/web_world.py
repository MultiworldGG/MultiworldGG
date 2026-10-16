from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class BuildJetpackWebWorld(WebWorld):
    game = "Build a Jetpack"
    theme = "ocean"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Build a Jetpack for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ChromaNyan"],
    )
    tutorials = [setup_en]