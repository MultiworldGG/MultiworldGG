from typing import Any, Dict

import Options as APOptions
from . import LuigiOptions as LMOptions

all_random_settings = { #TODO: Rename this because FillerWeights and TrapWeights are no longer fully random
    "progression_balancing":                          "random",
    "accessibility":                                  "random",
    LMOptions.RankRequirement.internal_name:           "random",
    LMOptions.GameMode.internal_name:                  "random",
    LMOptions.LuigiWalkSpeed.internal_name:            "random",
    LMOptions.LuigiFearAnim.internal_name:             "random",
    LMOptions.VacuumStart.internal_name:               "random",
    LMOptions.BetterVacuum.internal_name:              "random",
    LMOptions.StartWithBooRadar.internal_name:         "random",
    LMOptions.StartHiddenMansion.internal_name:        "random",
    LMOptions.PickupAnim.internal_name:                "random",
    LMOptions.LuigiMaxHealth.internal_name:            "random",
    LMOptions.RandomMusic.internal_name:               "random",
    LMOptions.DoorModelRando.internal_name:            "random",
    LMOptions.EarlyFirstKey.internal_name:             "random",
    LMOptions.DoorRando.internal_name:                 "random",
    LMOptions.PortraitHints.internal_name:             "random",
    LMOptions.HintDistribution.internal_name:          "random",
    LMOptions.SendHints.internal_name:                 "random",
    LMOptions.Toadsanity.internal_name:                "random",
    LMOptions.GoldMice.internal_name:                  "random",
    LMOptions.Boosanity.internal_name:                 "random",
    LMOptions.Portrification.internal_name:            "random",
    LMOptions.SilverPortrait.internal_name:            "random",
    LMOptions.GoldPortrait.internal_name:              "random",
    LMOptions.Lightsanity.internal_name:               "random",
    LMOptions.Walksanity.internal_name:                "random",
    LMOptions.SpeedySpirits.internal_name:             "random",
    LMOptions.WhatDoYouMean.internal_name:             "random",
    LMOptions.Grassanity.internal_name:                "random",
    LMOptions.BooGates.internal_name:                  "random",
    LMOptions.KingBooHealth.internal_name:             "random",
    LMOptions.BoolossusDifficulty.internal_name:       "random",
    LMOptions.MarioItems.internal_name:                "random",
    # LMOptions.WashroomBooCount.internal_name:          "random",
    LMOptions.BalconyBooCount.internal_name:           "random",
    LMOptions.FinalBooCount.internal_name:             "random",
    LMOptions.TrapLink.internal_name:                  "random",
    LMOptions.EnergyLink.internal_name:                "random",
    LMOptions.RingLink.internal_name:                  "random",
    LMOptions.ChestTypes.internal_name:                "random",
    LMOptions.TrapChestType.internal_name:             "random",
    LMOptions.Spookiness.internal_name:                "random",
    LMOptions.CallMario.internal_name:                 "random",
    LMOptions.BooHealthOption.internal_name:           "random",
    LMOptions.BooHealthValue.internal_name:            "random",
    LMOptions.BooSpeed.internal_name:                  "random",
    LMOptions.BooEscapeTime.internal_name:             "random",
    LMOptions.BooAnger.internal_name:                  "random",
    LMOptions.ExtraBooSpots.internal_name:             "random",
    LMOptions.Enemizer.internal_name:                  "random",
    LMOptions.RandomSpawn.internal_name:               "random",
    LMOptions.TrapPercentage.internal_name:            "random",
    "death_link":                                      "random",
}

allsanity_settings = {
    LMOptions.Toadsanity.internal_name:                "true",
    LMOptions.GoldMice.internal_name:                  "true",
    LMOptions.Furnisanity.internal_name:               ["Full"],
    LMOptions.Boosanity.internal_name:                 "true",
    LMOptions.Portrification.internal_name:            "true",
    LMOptions.SilverPortrait.internal_name:            "true",
    LMOptions.GoldPortrait.internal_name:              "true",
    LMOptions.Lightsanity.internal_name:               "true",
    LMOptions.Walksanity.internal_name:                "true",
    LMOptions.SpeedySpirits.internal_name:             "true",
    LMOptions.WhatDoYouMean.internal_name:             "true",
    LMOptions.Grassanity.internal_name:                "true",
}

money_settings = {
    LMOptions.FillerWeights.internal_name:             LMOptions.FillerWeights.all_on_dict,
    LMOptions.TrapWeights.internal_name:               LMOptions.TrapWeights.all_off_dict,
    LMOptions.TrapPercentage.internal_name:            0,
}

trap_settings = {
    LMOptions.FillerWeights.internal_name:             LMOptions.FillerWeights.all_off_dict,
    LMOptions.TrapWeights.internal_name:               LMOptions.TrapWeights.all_on_dict,
    LMOptions.TrapPercentage.internal_name:            100,
}

lm_options_presets: Dict[str, Dict[str, Any]] = {
    "All Random": all_random_settings,
    "I Love Money": money_settings,
    "Raining Traps": trap_settings,
    "Allsanity": allsanity_settings,
}