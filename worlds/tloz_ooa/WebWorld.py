from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial

class OracleOfAgesWeb(WebWorld):
    theme = "grass"
    display_name = "The Legend of Zelda: Oracle of Ages"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Oracle of Ages for MultiworldGG on your computer.",
        "English",
        "ooa_setup_en.md",
        "ooa_setup/en",
        ["SenPierre"]
    )]