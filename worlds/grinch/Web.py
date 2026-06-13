from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .GrinchOptions import *
from Options import OptionGroup

class GrinchWeb(WebWorld):
    theme = "ice"
    option_groups = [
        # OptionGroup("Goal", [
        #     Goal,
        #     MissionsCompleted,
        #     MissionCompletedIncludeGiftSquash,
        # ]),
        OptionGroup("Item Pool", [
            ProgressiveVacuums,
            StartingArea,
            ProgressiveGadgets,
            Gadgetrando,
            Gadgetrandolist,
            ExcludeGC,
            Moverando,
            Moverandolist,
            RandomizeMissionItems,
            RandomizeSleighParts,
        ]),
        OptionGroup("Location Settings", [
            Missionsanity,
            ExcludeEnvironments,
            Gifts,
            Supadow,
            Killsanity,
            MiscLocations,
        ]),
        # OptionGroup("Logic Settings", [
        #     AdvancedLogic,
        # ]),
        OptionGroup("In-Game Tweaks", [
            UnlimitedEggs,
            DamageRate,
            MusicRando,
            ReducedCutscenes,
            TeleportMultibind,
        ]),
        OptionGroup("Filler/Trap Settings", [
            FillerWeight,
            TrapPercentage,
            TrapWeight,
            RingLinkOption,
            TrapLinkOption,
        ]),
    ]

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up The Grinch randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["MarioSpore"],
        )
    ]