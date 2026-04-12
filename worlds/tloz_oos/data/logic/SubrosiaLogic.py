from .LogicPredicates import *


def make_subrosia_logic():
    return [
        # Portals ###############################################################

        ["volcanoes east portal", "subrosia temple sector", True, None],
        ["subrosia market portal", "subrosia market sector", True, None],
        ["strange brothers portal", "subrosia hide and seek sector", True, oos_has_feather()],
        ["house of pirates portal", "subrosia pirates sector", True, None],
        ["great furnace portal", "subrosia furnace sector", True, None],
        ["volcanoes west portal", "subrosia volcano sector", True, None],
        ["d8 entrance portal", "d8 entrance", True, None],

        # TODO when alt starting locations are implemented, there probably needs to be a way to re-use this forced transition
        ["pirates after bell", "western coast after ship", False, None],

        # Regions ###############################################################

        ["subrosia temple sector", "subrosia market sector", False, oos_can_jump_1_wide_liquid(False)],
        ["subrosia market sector", "subrosia temple sector", False, Or(
            oos_can_date_rosa(),
            oos_can_jump_1_wide_liquid(False)
        )],
        ["subrosia market sector", "subrosia east junction", False, Or(
            oos_has_magnet_gloves(),
            # As it is a "diagonal" pit, it is considered as a 3.5-wide pit
            oos_can_jump_3_wide_liquid()
        )],
        ["subrosia east junction", "subrosia market sector", False, Or(
            # This backwards route adds itself on top of the two-way route right above this one, adding the option
            # to remove the rock using the bracelet to turn this pit into a 2-wide jump
            And(
                oos_has_bracelet(),
                oos_can_jump_2_wide_pit()
            ),
            oos_has_magnet_gloves(),
            # As it is a "diagonal" pit, it is considered as a 3.5-wide pit
            oos_can_jump_3_wide_liquid()  # Could deserve an upgrade but isn't quite worth a hell classification
        )],

        ["subrosia temple sector", "subrosia bridge sector", True, oos_has_feather()],
        ["subrosia volcano sector", "subrosia bridge sector", False, And(
            oos_has_bracelet(),
            oos_can_jump_3_wide_liquid()
        )],
        ["subrosia volcano sector", "bomb temple remains", False, oos_has_bombs()],

        ["subrosia hide and seek sector", "subrosia market sector", False, And(
            oos_has_bracelet(),
            oos_has_feather(),
            Or(
                oos_can_jump_2_wide_liquid(),
                oos_has_magnet_gloves()
            )
        )],
        ["subrosia market sector", "subrosia hide and seek sector", False, And(
            # H&S skip, with bracelet : https://youtu.be/lH1yvshG3LE
            # H&S skip, without bracelet : https://youtube.com/clip/Ugkx6EcYk0akEEgfO1SuhSfAO3Px5KCTtUKD
            oos_option_hell_logic(),
            oos_has_feather(),
            oos_can_use_pegasus_seeds(),
            oos_has_bombs_for_bombjump(),
            # Old H&S skip doesn't require bracelet
        )],
        ["subrosia hide and seek sector", "subrosia temple sector", True, oos_can_jump_4_wide_liquid()],
        ["subrosia hide and seek sector", "subrosia pirates sector", True, oos_has_feather()],

        ["subrosia east junction", "subrosia furnace sector", False, oos_has_feather()],
        ["subrosia furnace sector", "subrosia east junction", False, Or(
            oos_has_feather(),
            And(
                oos_option_medium_logic(),
                oos_has_switch_hook()
            )
        )],

        # Locations ###############################################################

        ["subrosia temple sector", "subrosian dance hall", False, None],
        ["subrosia temple sector", "subrosian smithy ore", False, Or(
            Has("Hard Ore"),
            oos_self_locking_item("Subrosia: Smithy Hard Ore Reforge", "Hard Ore")
        )],
        ["subrosia temple sector", "subrosian smithy bell", False, Or(
            Has("Rusty Bell"),
            oos_self_locking_item("Subrosia: Smithy Rusty Bell Reforge", "Rusty Bell")
        )],
        ["subrosia temple sector", "smith secret", False, oos_has_shield()],

        ["subrosia temple sector", "temple of seasons", False, None],
        ["subrosia temple sector", "tower of winter", False, Or(
            oos_has_feather(),
            oos_can_trigger_far_switch()
        )],
        ["subrosia temple sector", "tower of summer", False, And(
            oos_can_date_rosa(),
            oos_has_bracelet(),
        )],
        ["subrosia temple sector", "tower of autumn", False, And(
            oos_has_feather(),
            Has("Bomb Flower")
        )],
        ["subrosia temple sector", "subrosian secret", False, And(
            oos_can_jump_1_wide_pit(False),
            oos_has_magic_boomerang()
        )],

        ["subrosia market sector", "subrosia seaside", False, oos_has_shovel()],
        ["subrosia market sector", "subrosia market star ore", False, Or(
            Has("Star Ore"),
            oos_self_locking_item("Subrosia: Market #1", "Star Ore")
        )],
        ["subrosia market sector", "subrosia market ore chunks", False, oos_can_buy_market()],

        ["subrosia hide and seek sector", "subrosia hide and seek", False, oos_has_shovel()],
        ["subrosia hide and seek sector", "tower of spring", False, oos_has_feather()],
        ["subrosia hide and seek sector", "subrosian wilds chest", False, And(
            oos_has_feather(),
            Or(
                oos_has_magnet_gloves(),
                oos_can_jump_4_wide_pit()
            )
        )],
        ["subrosian wilds chest", "subrosian wilds digging spot", False, And(
            Or(
                oos_can_jump_3_wide_pit(),
                oos_has_magnet_gloves()
            ),
            oos_has_feather(),
            oos_has_shovel()
        )],

        ["subrosia hide and seek sector", "subrosian house", False, oos_has_feather()],
        ["subrosia hide and seek sector", "subrosian 2d cave", False, oos_has_feather()],

        ["subrosia bridge sector", "subrosia, open cave", False, None],
        ["subrosia bridge sector", "subrosia, locked cave", False, And(
            oos_can_date_rosa(),
            oos_has_feather()
        )],
        ["subrosia bridge sector", "subrosian chef trade", False, Or(
            Has("Iron Pot"),
            oos_self_locking_item("Subrosia: Subrosian Chef Trade", "Iron Pot")
        )],

        ["subrosia east junction", "subrosia village chest", False, Or(
            oos_has_magnet_gloves(),
            oos_can_jump_4_wide_pit(),
            And(
                # early red ore : https://youtu.be/fB10dV2Gunk
                oos_option_hell_logic(),
                oos_has_feather(),
                oos_can_use_pegasus_seeds(),
                oos_has_bombs_for_bombjump()
            )
        )],

        ["subrosia furnace sector", "great furnace", False, And(
            CanReachRegion("tower of autumn"),
            Or(
                Has("Red Ore"),
                oos_self_locking_item("Subrosia: Item Smelted in Great Furnace", "Red Ore")
            ),
            Or(
                Has("Blue Ore"),
                oos_self_locking_item("Subrosia: Item Smelted in Great Furnace", "Blue Ore")
            ),
        )],
        ["subrosia furnace sector", "subrosian sign guy", False, oos_can_break_sign()],
        ["subrosia furnace sector", "subrosian buried bomb flower", False, And(
            oos_has_feather(),
            oos_has_bracelet()
        )],

        ["subrosia temple sector", "subrosia temple digging spot", False, oos_has_shovel()],
        ["subrosia temple sector", "subrosia bath digging spot", False, And(
            oos_can_jump_1_wide_pit(False),
            Or(
                oos_can_jump_3_wide_liquid(),
                oos_has_magnet_gloves()
            ),
            oos_has_shovel()
        )],
        ["subrosia market sector", "subrosia market digging spot", False, oos_has_shovel()],

        ["subrosia bridge sector", "subrosia bridge digging spot", False, oos_has_shovel()],

        ["subrosia pirates sector", "pirates after bell", False, Has("Pirate's Bell")],
    ]
