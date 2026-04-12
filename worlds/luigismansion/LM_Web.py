from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

import Options
from .Presets import lm_options_presets
from . import LuigiOptions

class LMWeb(WebWorld):
    theme = "stone"
    options_presets = lm_options_presets
    option_groups = [
        Options.OptionGroup("Extra Locations", [
            LuigiOptions.Furnisanity,
            LuigiOptions.Toadsanity,
            LuigiOptions.GoldMice,
            LuigiOptions.Boosanity,
            LuigiOptions.Portrification,
            LuigiOptions.SilverPortrait,
            LuigiOptions.GoldPortrait,
            LuigiOptions.SpeedySpirits,
            LuigiOptions.Lightsanity,
            LuigiOptions.Walksanity,
            LuigiOptions.Grassanity,
            LuigiOptions.WhatDoYouMean,
        ]),
        Options.OptionGroup("Access Options", [
            LuigiOptions.RankRequirement,
            LuigiOptions.GameMode,
            LuigiOptions.VacuumStart,
            LuigiOptions.MarioItems,
            LuigiOptions.BooGates,
            # LuigiOptions.WashroomBooCount,
            LuigiOptions.BalconyBooCount,
            LuigiOptions.FinalBooCount,
            LuigiOptions.Enemizer,
            LuigiOptions.DoorRando,
            LuigiOptions.RandomSpawn,
            LuigiOptions.EarlyFirstKey,
        ]),
        Options.OptionGroup("QOL Changes", [
            LuigiOptions.LuigiWalkSpeed,
            LuigiOptions.LuigiMaxHealth,
            LuigiOptions.LuigiFearAnim,
            LuigiOptions.PickupAnim,
            LuigiOptions.ShowSelfReceivedItems,
            Options.DeathLink,
            LuigiOptions.TrapLink,
            LuigiOptions.TrapLinkClientMsgs,
            LuigiOptions.EnergyLink,
            LuigiOptions.RingLink,
            LuigiOptions.RingLinkClientMsgs,
            LuigiOptions.BetterVacuum,
            LuigiOptions.StartWithBooRadar,
            LuigiOptions.StartHiddenMansion,
            LuigiOptions.HintDistribution,
            LuigiOptions.PortraitHints,
            LuigiOptions.SendHints,
        ]),
        Options.OptionGroup("Enemy Stats", [
            LuigiOptions.KingBooHealth,
            LuigiOptions.BoolossusDifficulty,
            LuigiOptions.BooHealthOption,
            LuigiOptions.BooHealthValue,
            LuigiOptions.BooSpeed,
            LuigiOptions.BooEscapeTime,
            LuigiOptions.BooAnger,
            LuigiOptions.ExtraBooSpots,
            LuigiOptions.PortraitHealthOption,
            LuigiOptions.PortraitHealthValue
        ]),
        Options.OptionGroup("Cosmetics", [
            LuigiOptions.RandomMusic,
            LuigiOptions.DoorModelRando,
            LuigiOptions.ChestTypes,
            LuigiOptions.TrapChestType,
            LuigiOptions.Spookiness,
            LuigiOptions.CallMario,
        ]),
        Options.OptionGroup("Filler Weights", [
            LuigiOptions.FillerWeights,
            LuigiOptions.TrapPercentage,
            LuigiOptions.TrapWeights,
        ]),
    ]

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Luigi's Mansion randomizer connected to a MultiworldGG Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["BootsinSoots", "SomeJakeGuy"],
        )
    ]
