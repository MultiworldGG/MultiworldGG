from Options import DeathLink, ProgressionBalancing, Accessibility, OptionGroup
from .Options import (Ending, Class, EntranceRandomization, RandomElements,
                      RequiredStrangeCoins, TotalStrangeCoins, Shopsanity, Dropsanity, Quenchsanity, EtnasPupil,
                      SecretDoorLock, SwitchLocks, DoorLocks, TrapPercent, CustomClass,
                      Filler, Traps, Grasssanity, Breakables, StartingArea, Levelsanity, Bookworm)

lunacid_option_groups = [
    OptionGroup("General", [
        Ending,
        Class,
        StartingArea,
        RandomElements,
        EntranceRandomization,
        RequiredStrangeCoins,
        TotalStrangeCoins
    ]),
    OptionGroup("Extra Shuffling", [
        Shopsanity,
        Dropsanity,
        Quenchsanity,
        EtnasPupil,
        Bookworm,
        Levelsanity,
        Grasssanity,
        Breakables
    ]),
    OptionGroup("Locks", [
        DoorLocks,
        SwitchLocks,
        SecretDoorLock
    ]),
    OptionGroup("Tweaks", [
        Filler,
        Traps,
        TrapPercent
    ]),
    OptionGroup("Advanced Options", [
        CustomClass,
        DeathLink,
        ProgressionBalancing,
        Accessibility,
    ])
]
