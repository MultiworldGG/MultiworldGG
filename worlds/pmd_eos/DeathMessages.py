from typing import List, NamedTuple

common_weight = 40
uncommon_weight = 20
rare_weight = 10
ultra_rare_weight = 1


class DeathMessages(NamedTuple):
    death_string: str = ""
    message_weight: int = 0


death_message_list = [
    DeathMessages(" drowned in Lappy's wealth of popcorn", ultra_rare_weight),
    DeathMessages(" got YOOM-TAH'd", uncommon_weight),
    DeathMessages(" got on Chatot's Bad Side", uncommon_weight),
    DeathMessages(" tried (and failed) to steal from Kecleon", rare_weight),
    DeathMessages(" drowned in the C of Time", rare_weight),
    DeathMessages(" drowned in the Sea of Time", uncommon_weight),
    DeathMessages(" was done in by a monster house", common_weight),
    DeathMessages(" couldn't move diagonally", uncommon_weight),
    DeathMessages(" was done in by a Chestnut Trap whilst fighting a monster house", uncommon_weight),
    DeathMessages(" fell asleep during Sentry Duty", uncommon_weight),
    DeathMessages(" died from a Wonder Tile", rare_weight),
    DeathMessages(" was transformed into a Spoink and stopped bouncing!", rare_weight),
    DeathMessages(" ran out of Reviver Seeds", common_weight),
    DeathMessages(" choked to death on a Cheesy Onion", ultra_rare_weight),
    DeathMessages(" slipped on a banana peel thrown by Cryptic", ultra_rare_weight),
    DeathMessages(" got crushed by Sceptile's insane amount of checks", ultra_rare_weight),
    DeathMessages(" found a bug that Fiery missed", ultra_rare_weight),
    DeathMessages(" slipped on a banana peel thrown by Cryptic", ultra_rare_weight),
    DeathMessages(" was Hecka Bad at the game", ultra_rare_weight),
    DeathMessages(" fell for JaiFain's Lookalike Dungeon", ultra_rare_weight),
    DeathMessages(" couldn't stop looking at Kattnip's sprites", ultra_rare_weight),
    DeathMessages(" couldn't live and didn't learn", ultra_rare_weight),
    DeathMessages(" looked too closely at Nido's Tracker Images", ultra_rare_weight),
    DeathMessages(" should have asked for Jimmy's Help", ultra_rare_weight),
    DeathMessages(" should have found one of Tailsdk's hints", rare_weight),
    DeathMessages(" made an enemy of 'Heartan'", rare_weight),
    DeathMessages(" made an enemy of 'Mespirit'", rare_weight),
    DeathMessages(" made an enemy of 'Keckleon'", rare_weight),
    DeathMessages(" got lost in the Premier Inn", ultra_rare_weight),
    DeathMessages(" accidentally found themselves in MLSS", ultra_rare_weight),
    DeathMessages(" picked up the Apple of Doom", rare_weight),
]

death_message_weights = [message.message_weight for message in death_message_list]
