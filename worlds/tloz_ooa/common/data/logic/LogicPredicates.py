from rule_builder.rules import And, Or, CanReachRegion
from ....data.logic.Rulebuilder import *
from ..Constants import *
from ...Options import OraclesLogicDifficulty, OraclesDefaultSeedType, OraclesMasterKeys, OraclesDungeonShuffle, OraclesAnimalCompanion
from ....data.Constants import *


# Items predicates ############################################################


def oo_has_sword(accept_biggoron: bool = True) -> Rule:
    return Or(
        Has("Progressive Sword"),
        And(
            from_bool(accept_biggoron),
            Has("Biggoron's Sword")
        )
    )


def oo_has_noble_sword() -> Rule:
    return Has("Progressive Sword", 2)


def oo_has_shield() -> Rule:
    return Has("Progressive Shield")


def oo_has_satchel(level: int = 1) -> Rule:
    return Has("Seed Satchel", level)


def oo_has_shovel() -> Rule:
    return Has("Shovel")


def oo_has_flippers() -> Rule:
    return Has("Flippers")


# Cross items
def oo_has_cane() -> Rule:
    return Has("Cane of Somaria")


def oo_has_switch_hook(level: int = 1) -> Rule:
    return Has("Switch Hook", level)


def oo_has_tight_switch_hook() -> Rule:
    return Or(
        oo_has_switch_hook(2),
        And(
            oo_option_medium_logic(),
            oo_has_switch_hook()
        )
    )


def oo_has_shooter() -> Rule:
    return Has("Seed Shooter")


def oo_has_ember_seeds() -> Rule:
    return Or(
        Has("Ember Seeds"),
        from_option(OraclesDefaultSeedType, OraclesDefaultSeedType.option_ember),
        And(
            Has("_wild_ember_seeds"),
            oo_option_medium_logic()
        )
    )


def oo_has_scent_seeds() -> Rule:
    return Or(
        Has("Scent Seeds"),
        from_option(OraclesDefaultSeedType, OraclesDefaultSeedType.option_scent),
    )


def oo_has_pegasus_seeds() -> Rule:
    return Or(
        Has("Pegasus Seeds"),
        from_option(OraclesDefaultSeedType, OraclesDefaultSeedType.option_pegasus)
    )


def oo_has_mystery_seeds() -> Rule:
    return Or(
        Has("Mystery Seeds"),
        from_option(OraclesDefaultSeedType, OraclesDefaultSeedType.option_mystery),
        And(
            Has("_wild_mystery_seeds"),
            oo_option_medium_logic()
        )
    )


def oo_has_gale_seeds() -> Rule:
    return Or(
        Has("Gale Seeds"),
        from_option(OraclesDefaultSeedType, OraclesDefaultSeedType.option_gale)
    )


def oo_has_small_keys(dungeon_id: int, amount: int = 1) -> Rule:
    return Or(
        Has(f"Small Key ({DUNGEON_NAMES[dungeon_id]})", amount,
            options=[OptionFilter(OraclesMasterKeys, OraclesMasterKeys.option_disabled)]),
        Has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})",
            options=[OptionFilter(OraclesMasterKeys, OraclesMasterKeys.option_disabled, "ne")]),
    )


def oo_has_boss_key(dungeon_id: int) -> Rule:
    return Or(
        Has(f"Boss Key ({DUNGEON_NAMES[dungeon_id]})",
            options=[OptionFilter(OraclesMasterKeys, OraclesMasterKeys.option_all_dungeon_keys, "ne")]),
        Has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})",
            options=[OptionFilter(OraclesMasterKeys, OraclesMasterKeys.option_all_dungeon_keys)]),
    )


# Options and generation predicates ###########################################

def oo_option_medium_logic() -> Rule:
    return from_option(OraclesLogicDifficulty, OraclesLogicDifficulty.option_medium, "ge")


def oo_option_hard_logic() -> Rule:
    return from_option(OraclesLogicDifficulty, OraclesLogicDifficulty.option_hard, "ge")


def oo_option_hell_logic() -> Rule:
    return from_option(OraclesLogicDifficulty, OraclesLogicDifficulty.option_hell, "ge")


def oo_option_shuffled_dungeons() -> Rule:
    return from_option(OraclesDungeonShuffle, OraclesDungeonShuffle.option_true)


def oo_is_companion_ricky() -> Rule:
    return from_option(OraclesAnimalCompanion, OraclesAnimalCompanion.option_ricky)


def oo_is_companion_moosh() -> Rule:
    return from_option(OraclesAnimalCompanion, OraclesAnimalCompanion.option_moosh)


def oo_is_companion_dimitri() -> Rule:
    return from_option(OraclesAnimalCompanion, OraclesAnimalCompanion.option_dimitri)


def oo_has_essences(target_count: int) -> Rule:
    return HasGroup("Essences", target_count)


def oo_has_essences_for_maku_seed() -> Rule:
    return HasGroupOption("Essences", "required_essences")


# Various item predicates ###########################################
def oo_has_rupees_for_shop(shop_name: str) -> Rule:
    return Or(
        And(
            oo_option_hard_logic(),
            oo_has_shovel()
        ),
        HasRupeesForShop(shop_name)
    )


def oo_shoot_beams() -> Rule:
    return Or(
        And(
            oo_option_medium_logic(),
            oo_has_sword(False),
            Has("Energy Ring"),
        ),
        And(
            oo_option_medium_logic(),
            oo_has_noble_sword(),
            Or(
                Has("Heart Ring L-2"),
                And(
                    oo_option_hard_logic(),
                    Has("Heart Ring L-1"),
                )
            )
        )
    )


def oo_has_bombs(amount: int = 1) -> Rule:
    return Or(
        Has("Bombs", amount),
        And(
            # With medium logic is expected to know they can get free bombs
            # from D2 moblin room even if they never had bombs before
            from_bool(amount == 1),
            oo_option_medium_logic(),
            Has("_wild_bombs"),
        )
    )


def oo_has_bombchus(amount: int = 1) -> Rule:
    return Has("Bombchus", amount)


def oo_has_flute() -> Rule:
    return Or(
        oo_can_summon_ricky(),
        oo_can_summon_moosh(),
        oo_can_summon_dimitri()
    )


def oo_can_summon_ricky() -> Rule:
    return Has("Ricky's Flute")


def oo_can_summon_moosh() -> Rule:
    return Has("Moosh's Flute")


def oo_can_summon_dimitri() -> Rule:
    return Has("Dimitri's Flute")


# Seed-related predicates ###########################################


def oo_can_use_pegasus_seeds() -> Rule:
    return And(
        # Unlike other seeds, pegasus only have an interesting effect with the satchel
        oo_has_satchel(),
        oo_has_pegasus_seeds()
    )


# Break / kill predicates ###########################################

def oo_can_kill_facade() -> Rule:
    return Or(
        oo_has_bombs(),
        oo_has_bombchus(2)
    )


def oo_can_punch() -> Rule:
    return And(
        oo_option_medium_logic(),
        Or(
            Has("Fist Ring"),
            Has("Expert's Ring")
        )
    )


def oo_can_flip_spiked_beetle() -> Rule:
    return Or(
        oo_has_shield(),
        And(
            oo_option_medium_logic(),
            oo_has_shovel()
        )
    )


# Action predicates ###########################################

def oo_can_remove_snow(can_summon_companion: bool) -> Rule:
    return Or(
        oo_has_shovel(),
        And(
            from_bool(can_summon_companion),
            oo_has_flute()
        )
    )


def oo_can_swim(can_summon_companion: bool) -> Rule:
    return Or(
        oo_has_flippers(),
        And(
            from_bool(can_summon_companion),
            oo_can_summon_dimitri()
        )
    )


def oo_can_remove_rockslide(can_summon_companion: bool) -> Rule:
    return Or(
        oo_has_bombs(),
        And(
            oo_option_medium_logic(),
            oo_has_bombchus(4)
        ),
        And(
            from_bool(can_summon_companion),
            oo_can_summon_ricky()
        )
    )


# Self-locking items helper predicates ##########################################

def oo_self_locking_item(location_name: str, item_name: str) -> Rule:
    return ItemInLocation(location_name, item_name)


def oo_self_locking_small_key(region_name: str, dungeon: int) -> Rule:
    item_name = f"Small Key ({DUNGEON_NAMES[dungeon]})"
    return oo_self_locking_item(region_name, item_name)
