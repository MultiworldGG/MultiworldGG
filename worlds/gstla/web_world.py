from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .option_groups import gstla_option_groups
from .option_presets import gstla_options_presets


class GSTLAWeb(WebWorld):
    theme = 'jungle'
    option_groups = gstla_option_groups
    options_presets = gstla_options_presets

    tut_en = Tutorial(
        'Multiworld Setup Guide',
        'A guide to setting up Golden Sun The Lost Age randomizer on your computer',
        'English',
        'setup_en.md',
        'setup/en',
        ['Dragion', 'PlatanoBailando'],
    )

    tutorials = [tut_en]
