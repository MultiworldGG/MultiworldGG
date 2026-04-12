from ...Options import OracleOfSeasonsLinkedHerosCave, OracleOfSeasonsOptions
from .LogicPredicates import *


def make_d0_logic():
    return [
        # 0 keys
        ["enter d0", "d0 key chest", False, None],
        ["enter d0", "d0 rupee chest", False,
         # If hole is removed, stairs are added inside dungeon to make the chest reachable
         oos_option_no_d0_alt_entrance()
         ],
        ["d0 rupee chest", "enter d0", False, None],
        ["enter d0", "d0 hidden 2d section", False, Or(
            oos_can_kill_normal_enemy(),
            oos_has_boomerang(),
            oos_has_switch_hook()
        )],

        # 1 key
        ["enter d0", "d0 sword chest", False, Or(
            oos_has_small_keys(0, 1),
            oos_self_locking_small_key("Hero's Cave: Final Chest", 0),
            oos_self_locking_item("Hero's Cave: Final Chest", "Master Key (Hero's Cave)")
        )],
    ]


def make_d1_logic():
    return [
        # 0 keys
        ["enter d1", "d1 stalfos drop", False, Or(
            oos_can_kill_stalfos(),
            And(
                # Medium logic expects the player to be able to use bushes
                oos_option_medium_logic(),
                oos_has_bracelet()
            )
        )],

        ["enter d1", "d1 floormaster room", False, oos_can_use_ember_seeds(True)],

        ["d1 floormaster room", "d1 boss", False, And(
            oos_has_boss_key(1),
            oos_can_kill_armored_enemy(False, False)
        )],

        # 1 key
        ["enter d1", "d1 stalfos chest", False, And(
            oos_has_small_keys(1, 1),
            oos_can_kill_stalfos()
        )],

        ["d1 stalfos chest", "d1 goriya chest", False, And(
            oos_can_use_ember_seeds(True),
            oos_can_kill_normal_enemy(True)
        )],

        ["d1 stalfos chest", "d1 lever room", False, None],

        ["d1 stalfos chest", "d1 block-pushing room", False, Or(
            oos_can_kill_normal_enemy(),
            And(
                oos_option_hard_logic(),
                oos_has_bracelet()
            )
        )],

        ["d1 stalfos chest", "d1 railway chest", False, Or(
            oos_can_trigger_lever(),
            And(
                oos_option_hard_logic(),
                oos_has_bracelet()
            )
        )],

        ["d1 railway chest", "d1 button chest", False, None],

        # 2 keys
        ["d1 railway chest", "d1 basement", False, Or(
            oos_self_locking_small_key("Gnarled Root Dungeon: Item in Basement", 1),
            And(
                oos_can_remove_rockslide(False),
                oos_has_small_keys(1, 2),
                oos_can_kill_armored_enemy(False, True)
            )
        )],
    ]


def make_d2_logic():
    return [
        # 0 keys
        ["enter d2", "d2 torch room", True, None],
        ["d2 torch room", "d2 left from entrance", False, None],
        ["d2 torch room", "d2 rope drop", False, Or(
            oos_can_kill_normal_enemy(),
            oos_has_switch_hook()
        )],
        ["d2 torch room", "d2 arrow room", False, oos_can_use_ember_seeds(True)],

        ["d2 arrow room", "d2 torch room", False, oos_can_kill_normal_enemy()],
        ["d2 arrow room", "d2 rupee room", False, oos_can_remove_rockslide(False)],
        ["d2 arrow room", "d2 rope chest", False, Or(
            oos_can_kill_normal_enemy(),
            oos_has_switch_hook()
        )],
        ["d2 arrow room", "d2 blade chest", False, oos_can_kill_normal_enemy()],

        ["d2 blade chest", "d2 arrow room", False, None],  # Backwards path
        ["d2 blade chest", "d2 alt entrances", True, oos_has_bracelet()],
        ["d2 blade chest", "d2 roller chest", False, And(
            oos_can_remove_rockslide(False),
            oos_has_bracelet(),
        )],
        ["d2 alt entrances", "d2 spiral chest", False, And(
            oos_can_break_bush(False, True),
            Or(
                oos_has_bombs_for_tiles(),
                And(
                    # It's tight but doable
                    oos_option_medium_logic(),
                    oos_can_use_pegasus_seeds(),
                    oos_has_bombchus_for_tiles()
                )
            )
        )],
        ["d2 alt entrances", "d2 scrub", False, oos_has_rupees_for_shop("d2Scrub")],

        # 2 keys
        ["d2 roller chest", "d2 spinner", False, And(
            oos_has_small_keys(2, 2),
            oos_can_kill_facade()
        )],
        # terrace self-locking rules
        ["d2 arrow room", "d2 terrace chest", False, And(
            oos_has_small_keys(2, 2),
            oos_self_locking_small_key("Snake's Remains: Chest on Terrace", 2)
        )],
        # You can take the Facade miniboss teleporter to reach dungeon entrance, even if you entered the dungeon
        # through the alt-entrance
        ["d2 spinner", "d2 wild bombs", False, And(
            Or(
                oos_can_remove_rockslide(False),
                oos_has_small_keys(2, 3)  # spin the spinner to access the pol's voice room
            ),
            Or(
                oos_can_harvest_regrowing_bush(),
                oos_has_bombs()  # Bombs for more bombs is ok in any amount
            )
        )],
        ["d2 spinner", "d2 torch room", False, None],
        ["d2 spinner", "dodongo owl", False, oos_can_use_mystery_seeds()],
        ["d2 spinner", "d2 boss", False, And(
            oos_has_boss_key(2),
            oos_has_bombs(),  # regrowable there
            oos_has_bracelet()
        )],

        # 3 keys
        ["d2 arrow room", "d2 hardhat room", False, oos_has_small_keys(2, 3)],
        ["d2 hardhat room", "d2 pot chest", False, oos_can_break_pot()],
        ["d2 hardhat room", "d2 moblin chest", False, And(
            oos_can_kill_d2_hardhat(),
            Or(
                oos_can_kill_d2_far_moblin(),
                oos_can_harvest_regrowing_bush(),
                oos_has_bombs()  # Bombs for more bombs is ok in any amount
            )
        )],
        ["d2 hardhat room", "d2 wild bombs", False, And(
            oos_can_kill_d2_hardhat(),
            oos_can_harvest_regrowing_bush()
        )],
        ["d2 spinner", "d2 terrace chest", False, oos_has_small_keys(2, 3)],
    ]


def make_d3_logic():
    return [
        # 0 keys
        ["enter d3", "spiked beetles owl", False, oos_can_use_mystery_seeds()],
        ["enter d3", "d3 center", False, Or(
            oos_can_kill_spiked_beetle(),
            And(
                # Break pots to refill mysteries, and use them on the beetles to gale them away
                oos_option_medium_logic(),
                oos_can_use_mystery_seeds(),
                oos_can_break_pot()
            ),
            And(
                oos_option_medium_logic(),
                oos_can_flip_spiked_beetle(),
                oos_has_bracelet()
            )
        )],

        ["d3 center", "d3 water room", False, oos_has_feather()],
        ["d3 center", "d3 mimic stairs", False, Or(
            oos_has_bracelet(),
            And(
                oos_can_break_pot(),
                oos_has_cane()
            )
        )],
        ["d3 center", "trampoline owl", False, And(
            oos_has_feather(),
            oos_can_use_mystery_seeds()
        )],
        ["d3 center", "d3 trampoline chest", False, oos_has_feather()],
        ["d3 center", "d3 zol chest", False, oos_has_feather()],

        ["d3 mimic stairs", "d3 water room", True, None],
        ["d3 mimic stairs", "d3 roller chest", False, oos_has_bracelet()],
        ["d3 mimic stairs", "d3 quicksand terrace", False, oos_has_feather()],
        ["d3 quicksand terrace", "omuai owl", False, And(
            oos_can_use_mystery_seeds()
        )],
        ["d3 mimic stairs", "d3 moldorm chest", False, oos_can_kill_moldorm()],
        ["d3 mimic stairs", "d3 bombed wall chest", False, oos_can_remove_rockslide(False)],

        # 2 keys
        ["d3 water room", "d3 mimic chest", False, And(
            Or(
                oos_has_small_keys(3, 2),
                oos_self_locking_small_key("Poison Moth's Lair (1F): Chest in Mimics Room", 3)
            ),
            oos_can_kill_normal_enemy()
        )],
        ["d3 mimic stairs", "d3 omuai stairs", False, And(
            Or(
                oos_has_feather(),

                # With switch hook, even with pegasus, you can barely see the pots, so it's not casual friendly
                And(
                    oos_option_medium_logic(),
                    oos_has_switch_hook(2)
                ),
                And(
                    oos_option_medium_logic(),
                    oos_can_use_pegasus_seeds(),
                    oos_has_switch_hook()
                )
            ),
            oos_has_small_keys(3, 2),
            oos_has_bracelet(),
            oos_can_kill_armored_enemy(False, False)
        )],
        ["d3 omuai stairs", "d3 quicksand terrace", False, None],
        ["d3 omuai stairs", "d3 giant blade room", False, Or(
            oos_has_feather(),
            oos_option_hard_logic()
        )],
        ["d3 omuai stairs", "d3 boss", False, oos_has_boss_key(3)],
    ]


def make_d4_logic():
    return [
        # 0 keys
        ["enter d4", "d4 north of entrance", False, Or(
            oos_has_flippers(),
            oos_has_cape()
        )],
        ["d4 north of entrance", "d4 pot puzzle", False, And(
            oos_can_remove_rockslide(False),
            oos_has_bracelet()
        )],
        ["d4 north of entrance", "d4 maze chest", False, Or(
            oos_can_trigger_lever_from_minecart(),
            And(
                oos_option_hard_logic(),
                oos_has_bracelet()
            )
        )],
        ["d4 maze chest", "d4 dark room", False, oos_has_feather()],

        # 1 key
        ["enter d4", "d4 water ring room", False, And(
            oos_has_small_keys(4, 1),
            Or(
                oos_has_cape(),
                And(
                    # Feather is required to jump above spike lines
                    oos_has_feather(),
                    oos_has_flippers()
                )
            ),
            oos_can_remove_rockslide(False),
            Or(
                oos_can_kill_normal_enemy(),
                And(  # killing enemies with pots
                    oos_option_medium_logic(),
                    oos_has_bracelet(),
                ),
                And(  # pushing enemies in the water
                    oos_can_push_enemy(),
                    Or(
                        oos_has_boomerang(),
                        oos_has_switch_hook()
                    )
                )
            )
        )],

        ["enter d4", "d4 roller minecart", False, And(
            oos_has_small_keys(4, 1),
            oos_has_feather(),
            Or(
                oos_has_flippers(),
                And(
                    oos_option_hell_logic(),
                    oos_has_cape(),
                    oos_can_use_pegasus_seeds(),
                    oos_has_bombs_for_bombjump()
                )
            )
        )],

        ["d4 roller minecart", "d4 pool", False, And(
            Or(
                oos_has_flippers(),
                oos_option_medium_logic()
            ),
            Or(
                oos_can_kill_normal_enemy(),
                And(
                    oos_option_medium_logic(),
                    oos_has_bracelet()
                ),
                And(
                    oos_can_push_enemy(),
                    oos_has_switch_hook()
                )
            ),
            Or(
                oos_can_trigger_lever_from_minecart(),
                And(
                    oos_option_hard_logic(),
                    oos_has_bracelet()
                )
            )
        )],

        # 2 keys
        ["d4 roller minecart", "greater distance owl", False, And(
            oos_has_small_keys(4, 2),
            oos_can_use_mystery_seeds()
        )],

        ["d4 roller minecart", "d4 stalfos stairs", False, And(
            oos_has_small_keys(4, 2),
            Or(
                oos_can_kill_stalfos(),
                And(
                    # Kill Stalfos by using pots in the room
                    oos_option_medium_logic(),
                    oos_has_bracelet()
                )
            ),
            oos_can_jump_2_wide_pit()
        )],

        ["d4 stalfos stairs", "d4 terrace", False, None],
        ["d4 terrace", "d4 scrub", False, oos_has_rupees_for_shop("d4Scrub")],

        ["d4 stalfos stairs", "d4 torch chest", False, And(
            oos_has_seed_thrower(),
            oos_has_ember_seeds()
        )],

        ["d4 stalfos stairs", "d4 miniboss room", False, None],
        ["d4 miniboss room", "d4 miniboss room wild embers", False, oos_can_harvest_regrowing_bush()],

        ["d4 miniboss room", "d4 final minecart", False, And(
            oos_can_use_ember_seeds(False),
            oos_can_kill_armored_enemy(False, False)
        )],

        # 5 keys
        ["d4 final minecart", "d4 cracked floor room", False, Or(
            oos_has_small_keys(4, 5),
            oos_self_locking_small_key("Dancing Dragon Dungeon (1F): Crumbling Room Chest", 4)
        )],
        ["d4 final minecart", "d4 dive spot", False, And(
            Or(
                And(
                    Or(  # hit distant levers
                        oos_has_magic_boomerang(),
                        oos_has_seed_thrower()
                    ),
                    # In medium, switch is also valid, but a feather is required to get there anyway
                    oos_can_jump_2_wide_pit(),
                    oos_has_small_keys(4, 5),
                ),
                # For self-locking, we don't need to check if the player is able to
                # waste the key first to then get it back, only to get it back if they waste it
                oos_self_locking_small_key("Dancing Dragon Dungeon (1F): Eye Diving Spot Item", 4)
            ),
            oos_has_flippers()
        )],

        ["d4 final minecart", "d4 basement stairs", False, And(
            oos_has_small_keys(4, 5),
            Or(
                oos_has_boomerang(),
                oos_has_seed_thrower(),
                oos_has_switch_hook(),
                oos_option_hard_logic()
            )
        )],

        ["d4 basement stairs", "gohma owl", False, oos_can_use_mystery_seeds()],

        ["d4 basement stairs", "enter gohma", False, And(
            oos_has_boss_key(4),
            Or(
                And(
                    oos_has_seed_thrower(),
                    oos_can_use_ember_seeds(True)
                ),
                oos_can_jump_3_wide_pit(),
                And(  # throw seeds using satchel during a jump
                    oos_option_hard_logic(),
                    oos_has_feather(),
                    oos_can_use_ember_seeds(False)
                )
            )
        )],

        ["enter gohma", "d4 boss", False, Or(
            And(
                # Kill Gohma without breaking its pincer
                oos_option_medium_logic(),
                Or(
                    oos_has_seed_thrower(),
                    oos_option_hard_logic()  # You can kill Gohma with the satchel. Yup...
                ),
                Or(
                    oos_has_scent_seeds(),
                    oos_has_ember_seeds()
                )
            ),
            And(
                # Kill Gohma with sword beams (Gohma's minions give enough hearts to justify it)
                oos_option_medium_logic(),
                Or(
                    oos_has_noble_sword(),
                    oos_shoot_beams()
                )
            ),
            And(
                # Kill Gohma traditionally (break pincer, then spam seeds)
                Or(
                    oos_has_sword(),
                    oos_has_fools_ore()
                ),
                Or(
                    oos_can_use_ember_seeds(False),
                    oos_can_use_scent_seeds(),
                    And(
                        oos_option_medium_logic(),
                        oos_has_satchel(2),  # It may require quite a bunch of mystery seeds...
                        oos_can_use_mystery_seeds()
                    )
                )
            )
        )],
    ]


def make_d5_logic():
    return [
        # 0 keys
        ["enter d5", "d5 left chest", False, Or(
            oos_has_magnet_gloves(),
            oos_has_cape(),
            And(
                # Tight bomb jump to reach the chest
                oos_option_hell_logic(),
                oos_can_jump_3_wide_liquid(),
            )
        )],

        ["enter d5", "d5 spiral chest", False, And(
            oos_can_kill_moldorm(True),
            oos_can_kill_normal_enemy(True)
        )],

        ["enter d5", "d5 terrace chest", False, oos_has_magnet_gloves()],

        ["d5 terrace chest", "armos knights owl", False, oos_can_use_mystery_seeds()],
        ["d5 terrace chest", "d5 armos chest", False, And(
            oos_can_kill_moldorm(),
            oos_can_kill_normal_enemy()
        )],

        ["enter d5", "d5 cart bay", False, Or(
            oos_has_flippers(),
            oos_can_jump_2_wide_liquid()
        )],

        ["d5 cart bay", "d5 terrace chest", False, And(
            oos_has_feather(),
            oos_can_remove_rockslide(False)  # Bombchus can be thrown from the middle platform
        )],

        ["d5 cart bay", "d5 cart chest", False, oos_can_trigger_lever_from_minecart()],

        ["d5 cart bay", "d5 spinner chest", False, Or(
            oos_has_magnet_gloves(),
            oos_can_jump_5_wide_pit(),
            And(
                # Switch with the pots on the bottom left
                oos_option_medium_logic(),
                oos_has_switch_hook(2)
            ),
            And(
                # Wait for le helmasaur to be on the left side of the hole.
                # By being on the right border, you can see pixels of it and switch hook 1 with it
                oos_option_hell_logic(),
                oos_has_switch_hook()
            )
        )],

        ["d5 cart bay", "d5 drop ball", False, And(
            oos_can_trigger_lever_from_minecart(),
            Or(
                oos_can_kill_armored_enemy(True, True),
                oos_has_shield(),
                And(
                    oos_option_medium_logic(),
                    oos_has_shovel()
                ),
                And(
                    oos_option_medium_logic(),
                    # Pull the darknut in the water
                    oos_has_magnet_gloves()
                )
            )
        )],

        ["enter d5", "d5 pot room", False, And(
            oos_has_magnet_gloves(),
            oos_can_remove_rockslide(False),
            oos_has_feather()
        )],

        ["d5 cart bay", "d5 pot room", False, Or(
            oos_has_feather(),
            And(
                oos_option_hard_logic(),
                oos_can_use_pegasus_seeds()
            )
        )],

        ["d5 pot room", "d5 gibdo/zol chest", False, oos_can_kill_normal_enemy()],

        ["d5 cart bay", "d5 syger lobby", False, Or(
            oos_has_magnet_gloves(),
            oos_has_cape(),
        )],
        ["d5 pot room", "d5 syger lobby", False, Or(
            oos_has_magnet_gloves(),
            oos_has_cape(),
        )],

        ["d5 syger lobby", "d5 stalfos room", False, None],

        # 5 keys
        ["d5 syger lobby", "d5 post syger", False, And(
            oos_has_small_keys(5, 3),
            oos_can_kill_armored_enemy(False, False)
        )],

        ["enter d5", "d5 magnet ball chest", False,
         oos_self_locking_small_key("Unicorn's Cave: Magnet Gloves Chest", 5)],
        ["enter d5", "d5 basement", False, And(
            oos_self_locking_small_key("Unicorn's Cave: Treadmills Basement Item", 5),
            CanReachRegion("d5 drop ball"),
            oos_has_small_keys(5, 3),
            oos_has_magnet_gloves(),
            Or(
                oos_can_kill_magunesu(),
                And(
                    oos_option_medium_logic(),
                    oos_has_feather()
                )
            )
        )],

        ["d5 pot room", "d5 magnet ball chest", False, And(
            Or(
                oos_has_flippers(),
                And(
                    # Lower route pushing secret blocks requires knowledge, therefore is medium+.
                    # Going there requires jumping a 3.2 wide liquid gap which corresponds the best to a "4 wide pit"
                    # in terms of logic requirements.
                    oos_can_jump_4_wide_pit(),
                    oos_option_medium_logic(),
                    # Upper route would require 6 wide liquid that can only be jumped above with a bomb jump,
                    # which makes the lower route always better when in medium+.
                )
            ),
            oos_has_small_keys(5, 5),
        )],

        ["d5 post syger", "d5 basement", False, And(
            Or(
                oos_has_small_keys(5, 5),
                oos_self_locking_small_key("Unicorn's Cave: Treadmills Basement Item", 5)
            ),

            # Magnet ball button
            Or(
                And(
                    CanReachRegion("d5 drop ball"),
                    oos_has_magnet_gloves(),
                ),
                oos_has_cane()
            ),

            # Flamme wall
            Or(
                And(
                    oos_has_magnet_gloves(),
                    oos_can_kill_magunesu(),
                ),
                And(
                    oos_option_medium_logic(),
                    oos_has_feather()
                )
            ),

            # Basement
            Or(
                oos_has_magnet_gloves(),
                And(
                    oos_has_cane(),
                    oos_can_jump_3_wide_pit()
                )
            )
        )],

        ["d5 post syger", "d5 boss", False, And(
            oos_has_small_keys(5, 5),
            oos_has_magnet_gloves(),
            oos_has_boss_key(5),
            Or(
                oos_option_medium_logic(),
                oos_has_feather()
            ),
        )],
    ]


def make_d6_logic():
    return [
        # 0 keys
        ["enter d6", "d6 1F east", False, Or(
            # In room 4b3:
            # jump over the hole
            oos_has_feather(),

            # Break the crystals (with crumbling floor)
            oos_has_sword(),
            oos_has_bombs_for_tiles(),
            And(
                oos_option_medium_logic(),
                Has("Expert's Ring")
            ),

            # Walk through the holes
            oos_option_hard_logic()
        )],

        ["d6 1F east", "d6 rupee room", False, oos_can_remove_rockslide(False)],

        ["d6 1F east", "d6 1F terrace", False, None],
        ["enter d6", "d6 1F terrace", False, And(
            oos_has_small_keys(6, 2),
            Or(
                oos_has_magnet_gloves(),
                oos_has_cane()
            )
        )],

        ["d6 1F terrace", "d6 magnet ball drop", False, Or(
            And(
                oos_has_feather(),
                oos_has_magnet_gloves()
            ),
            oos_can_jump_4_wide_pit(),
            And(
                # Cane through the block
                oos_option_medium_logic(),
                oos_has_cane()
            )
        )],
        ["d6 1F terrace", "d6 crystal trap room", False, None],
        ["d6 1F terrace", "d6 U-room", False, And(
            oos_can_break_crystal(),
            Or(
                oos_has_magic_boomerang(),
                And(
                    # Clip into the right statues for the first orb,
                    # then manipulate the position to clip into the bottom right of the opening for the second one
                    oos_option_hell_logic(),
                    oos_has_shooter(),
                    oos_has_sword(False),
                    oos_can_use_pegasus_seeds()
                ),
                And(
                    # Just do the first one in hard, then use bombchus to kill the keese then hit the orb
                    oos_option_hard_logic(),
                    oos_has_shooter(),
                    oos_has_bombchus_to_fight(),
                )
            )
        )],
        ["d6 U-room", "d6 torch stairs", False, And(
            Or(
                # In easy, logic expects slingshot, but medium+ can expect satchel
                # as well since the distance between platforms & torches is a half-tile
                oos_has_seed_thrower(),
                oos_option_medium_logic()
            ),
            oos_can_use_ember_seeds(False)
        )],

        ["d6 torch stairs", "d6 escape room", False, oos_has_feather()],
        ["d6 escape room", "d6 vire chest", False, oos_can_kill_stalfos()],

        # 3 keys
        ["enter d6", "d6 beamos room", False, oos_has_small_keys(6, 3)],
        ["d6 beamos room", "d6 2F gibdo chest", False, None],
        ["d6 beamos room", "d6 2F armos chest", False, oos_can_remove_rockslide(False)],
        ["d6 2F armos chest", "d6 armos hall", False, oos_has_feather()],

        ["enter d6", "d6 spinner north", False, And(
            oos_can_break_crystal(),
            Or(
                oos_has_magnet_gloves(),
                And(  # Clip into the blocks to place the somaria block on the button
                    oos_option_hard_logic(),
                    oos_has_cane()
                )
            ),
            Or(
                oos_option_medium_logic(),  # Iframes through the spikes
                oos_has_feather()
            ),
            Or(
                And(
                    oos_has_small_keys(6, 1),

                    # Go through beamos room
                    And(
                        oos_can_remove_rockslide(False),
                        oos_has_feather()
                    ),

                    Or(
                        # Kill Vire (the rest doesn't matter because we don't care about not being able to not spend a key somewhere)
                        oos_has_sword(False),
                        oos_has_fools_ore(),
                        And(
                            oos_option_medium_logic(),
                            oos_has_bombs_to_fight()
                        ),
                        And(
                            # Fist Ring doesn't damage Vire
                            Has("expert's ring"),
                            oos_option_medium_logic()
                        )
                    )
                ),
                And(
                    oos_has_small_keys(6, 2),
                    Or(
                        # Go through beamos room
                        And(
                            oos_can_remove_rockslide(False),
                            oos_has_feather()
                        ),

                        # Kill Vire
                        oos_has_sword(False),
                        oos_has_fools_ore(),
                        And(
                            oos_option_medium_logic(),
                            oos_has_bombs_to_fight()
                        ),
                        And(
                            # Fist Ring doesn't damage Vire
                            Has("expert's ring"),
                            oos_option_medium_logic()
                        )
                    )
                ),
                oos_has_small_keys(6, 3),
            )
        )],

        ["d6 vire chest", "d6 enter vire", False, And(
            oos_has_small_keys(6, 3),
            Or(
                # Kill Vire
                oos_has_sword(False),
                oos_has_fools_ore(),
                And(
                    oos_option_medium_logic(),
                    oos_has_bombs_to_fight()
                ),
                And(
                    # Fist Ring doesn't damage Vire
                    Has("expert's ring"),
                    oos_option_medium_logic()
                )
            )
        )],
        ["d6 enter vire", "d6 pre-boss room", False, And(
            oos_has_small_keys(6, 3),
            Or(
                # Kill hardhats
                oos_has_magnet_gloves(),
                And(
                    oos_option_medium_logic(),
                    oos_has_gale_seeds(),
                    Or(
                        oos_has_seed_thrower(),
                        And(
                            oos_option_hard_logic(),
                            oos_has_satchel()
                        )
                    )
                )
            ),
            oos_has_feather()  # jump on trampoline
            # Switches here are considered trivial since we'll need magic boomerang for
            # Manhandla anyway
        )],

        ["d6 pre-boss room", "d6 boss", False, And(
            oos_has_boss_key(6),
            oos_has_magic_boomerang(),
            Or(
                oos_has_sword(),
                oos_has_fools_ore(),
                oos_has_seed_thrower(),
                # Has("expert's ring")
            )
        )],
    ]


def make_d7_logic():
    return [
        # 0 keys
        ["enter d7", "poe curse owl", False, oos_can_use_mystery_seeds()],
        ["enter d7", "d7 wizzrobe chest", False, oos_can_kill_normal_enemy_no_cane()],
        ["enter d7", "d7 bombed wall chest", False, oos_can_break_crystal()],
        ["enter d7", "d7 entrance wild embers", False, oos_can_harvest_regrowing_bush()],

        # 1 key
        ["enter d7", "enter poe A", False, And(
            oos_has_small_keys(7, 1),
            oos_has_seed_thrower(),
            oos_can_use_ember_seeds(True)
        )],

        ["enter poe A", "d7 pot room", False, And(
            Or(
                # Kill poe sister
                oos_can_kill_armored_enemy(False, False),
                And(
                    oos_option_medium_logic(),
                    oos_has_rod(),
                ),
                And(
                    # Mystery isn't reasonable due to having only ~8.8% chance of not getting a gale before killing the sister
                    oos_has_ember_seeds(),
                    Or(
                        oos_option_medium_logic(),
                        oos_has_satchel(2)
                    )
                )
            ),
            oos_has_bracelet()
        )],
        ["enter d7", "d7 pot room", False, And(
            # Poe skip
            oos_option_hell_logic(),
            oos_can_remove_rockslide(False),
            oos_can_use_pegasus_seeds(),
            oos_has_feather(),
            oos_has_bracelet(),
        )],

        ["d7 pot room", "d7 zol button", False, oos_has_feather()],
        ["d7 pot room", "d7 armos puzzle", False, Or(
            oos_can_jump_3_wide_pit(),
            oos_has_magnet_gloves()
        )],
        ["d7 pot room", "d7 magunesu chest", False, oos_has_cane()],

        ["d7 armos puzzle", "d7 magunesu chest", False, And(
            oos_can_kill_magunesu(),
            oos_has_magnet_gloves(),
            Or(
                oos_can_jump_3_wide_pit(),
                And(
                    # Really precise bomb jumps to cross the 3-holes
                    oos_option_hell_logic(),
                    oos_can_jump_2_wide_liquid()
                )
            )
        )],

        # 2 keys
        ["d7 pot room", "d7 quicksand chest", False, And(
            oos_has_small_keys(7, 2),
            oos_has_feather()
        )],
        ["d7 pot room", "d7 water stairs", False, And(
            # poe skip 2 : https://youtu.be/MIMm6q_yGyQ
            oos_option_hell_logic(),
            oos_has_small_keys(7, 2),
            oos_has_bombs_for_bombjump(),
            oos_has_cape(),
            oos_can_use_pegasus_seeds(),
            oos_has_flippers(),
            Has("Swimmer's Ring")
        )],

        # 3 keys
        ["d7 pot room", "enter poe B", False, And(
            oos_has_small_keys(7, 3),
            oos_can_use_ember_seeds(False),
            Or(
                oos_can_use_pegasus_seeds(),
                # Hard logic can do it without pegasus, it's very tight but doable
                oos_option_hard_logic()
            )
        )],

        ["enter poe B", "d7 water stairs", False, oos_has_flippers()],

        ["d7 water stairs", "d7 darknut bridge trampolines", False, Or(
            And(
                # Boomerang to activate the switch then magnet gloves to go to the trampolines
                oos_has_magnet_gloves(),
                oos_has_magic_boomerang()
            ),
            And(
                oos_option_hard_logic(),
                oos_has_feather(),
                oos_has_magnet_gloves()
            ),
        )],
        ["d7 water stairs", "d7 past darknut bridge", False, Or(
            # Just jump to the other side directly
            oos_can_jump_4_wide_pit(),
            oos_has_tight_switch_hook(),  # or hook to the other side

            And(
                oos_has_seed_thrower(),
                oos_has_scent_seeds()
            ),
            And(
                # Kill one darknut then pull the others
                oos_has_magnet_gloves(),
                Or(
                    oos_can_kill_armored_enemy(True, True),
                    oos_has_shield(),  # To push the darknut, the rod not really working
                    # Pull the right darknut by just going and stalling in the hole
                    oos_option_medium_logic(),
                )
            ),
            oos_shoot_beams()
        )],
        ["d7 past darknut bridge", "d7 darknut bridge trampolines", False, Or(
            # Reach trampolines directly
            oos_can_jump_3_wide_pit(),

            And(
                Or(
                    # Trigger the spinner switch
                    oos_has_sword(),
                    oos_has_fools_ore(),
                    oos_has_rod(),
                    oos_has_bombs_for_tiles(),
                    oos_has_bombchus_for_tiles()
                ),
                # Reach trampolines using the magnet gloves
                oos_has_feather(),
                oos_has_magnet_gloves()
            )
        )],

        ["d7 darknut bridge trampolines", "d7 spike chest", False, oos_can_kill_stalfos()],

        # 4 keys
        ["d7 water stairs", "d7 maze chest", False, And(
            oos_has_small_keys(7, 4),
            Or(
                oos_can_kill_armored_enemy(False, False),
                And(
                    Or(
                        oos_option_medium_logic() & oos_can_kill_moldorm(True),
                        oos_can_kill_moldorm()
                    ),
                    Or(
                        # Kill poe sisters
                        oos_has_rod(),
                        And(
                            # 18 embers are needed to kill the boss
                            oos_has_ember_seeds(),
                            Or(
                                oos_option_hard_logic(),
                                oos_can_harvest_regrowing_bush(),  # refill embers in the middle
                                oos_has_satchel(2)
                            )
                        )
                    ),
                )
            ),
            Or(
                oos_can_jump_3_wide_liquid(),  # Technically not a liquid but a diagonal pit
                And(
                    # Switch hook from above with the pot next to the button then jump in the hole
                    oos_option_medium_logic(),
                    oos_has_switch_hook(),
                    oos_can_jump_3_wide_pit()  # To pass the flying tiles room
                )
                # Casual could switch 2 from the left, but they'd have to jump in the hole to move out
                # which is against casual logic's spirit
            )
        )],

        ["d7 maze chest", "d7 B2F drop", False, Or(
            oos_has_magnet_gloves(),
            And(
                # The jumps in this room being pretty intricate, precise and counterintuitive,
                # we chose to put that in hard logic only.
                oos_option_hard_logic(),
                oos_can_jump_6_wide_pit()
            )
        )],

        # 5 keys
        ["enter d7", "d7 stalfos chest", False, And(
            oos_has_small_keys(7, 4),
            oos_self_locking_small_key("Explorer's Crypt (B1F): Chest in Jumping Stalfos Room", 7),
            Or(
                oos_can_jump_5_wide_pit(),
                And(
                    oos_option_hard_logic(),
                    oos_can_jump_1_wide_pit(False)
                )
            ),
            oos_can_kill_stalfos(),
        )],
        ["d7 maze chest", "d7 stalfos chest", False, And(
            oos_has_small_keys(7, 5),
            Or(
                oos_can_jump_5_wide_pit(),
                And(
                    oos_option_hard_logic(),
                    oos_can_jump_1_wide_pit(False)
                )
            ),
            oos_can_kill_stalfos(),
        )],

        ["d7 stalfos chest", "shining blue owl", False, oos_can_use_mystery_seeds()],

        ["enter d7", "d7 right of entrance", False, And(
            oos_can_kill_normal_enemy(),
            Or(
                oos_has_small_keys(7, 5),
                And(
                    oos_has_small_keys(7, 1),
                    oos_self_locking_small_key("Explorer's Crypt (1F): Chest Right of Entrance", 7)
                )
            )
        )],

        ["d7 maze chest", "d7 boss", False, And(
            oos_has_boss_key(7),
            Or(
                oos_has_sword(),
                oos_has_fools_ore(),
                # oos_can_punch()
            )
        )]
    ]


def make_d8_logic():
    return [
        # 0 keys
        ["enter d8", "d8 eye drop", False, And(
            oos_can_break_pot(),
            Or(
                oos_has_seed_thrower(),
                And(
                    oos_option_medium_logic(),
                    oos_has_feather(),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                )
            )
        )],

        ["enter d8", "d8 three eyes chest", False, And(
            oos_has_feather(),
            Or(
                oos_has_hyper_slingshot(),
                And(
                    oos_option_hell_logic(),
                    Or(
                        oos_has_satchel(),
                    ),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                ),
                And(
                    oos_option_hell_logic(),
                    oos_has_slingshot(),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_pegasus_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                ),
                And(
                    oos_option_hell_logic(),
                    oos_has_shooter(),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_pegasus_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                )
            )
        )],

        ["enter d8", "d8 hardhat room", False, oos_can_kill_magunesu()],

        ["d8 hardhat room", "d8 hardhat drop", False, Or(
            And(
                oos_can_remove_rockslide(False),  # For the bombchus, leave the hardhat stuck in the upper line to guide the bombchus
                oos_has_magnet_gloves()
            ),
            oos_can_use_gale_seeds_offensively()
        )],

        # 1 key
        ["d8 hardhat room", "d8 spike room", False, And(
            oos_has_small_keys(8, 1),
            Or(
                oos_has_cape(),
                And(  # Tight 2D section jump is hard mode without cape
                    oos_option_hard_logic(),
                    oos_has_feather(),
                    oos_can_use_pegasus_seeds()
                )
            )
        )],

        # 2 keys
        ["d8 spike room", "d8 spinner", False, oos_has_small_keys(8, 2)],
        ["d8 spinner", "silent watch owl", False, oos_can_use_mystery_seeds()],
        ["d8 spinner", "d8 magnet ball room", False, None],
        ["d8 spinner", "d8 armos chest", False, Or(
            oos_has_magnet_gloves(),
            And(
                # Clip into the block right of staircase with pegasus seeds and use the cane of somaria to activate the bridge, save&exit and redo the whole dungeon to get to the other side
                oos_option_hard_logic(),
                oos_can_use_pegasus_seeds(),
                oos_has_cane()
            )
        )],
        ["d8 spinner", "d8 spinner chest", False,
         oos_has_magnet_gloves()
         # Jump 2 liquid also, but this is covered earlier
         ],
        ["d8 spinner", "frypolar entrance", False, Or(
            oos_has_magnet_gloves(),
            And(
                oos_option_hell_logic(),
                oos_can_use_pegasus_seeds(),
                oos_has_cape(),
                oos_has_bombs_for_bombjump()
            )
        )],
        ["frypolar entrance", "frypolar owl", False, oos_can_use_mystery_seeds()],
        ["frypolar entrance", "d8 darknut chest", False, And(
            Or(
                oos_has_hyper_slingshot(),
                And(
                    oos_option_hell_logic(),
                    Or(
                        oos_has_satchel(),
                    ),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                ),
                And(
                    oos_option_hell_logic(),
                    oos_has_slingshot(),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_pegasus_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                ),
                And(
                    # This one is way easier to time by just bouncing on the left
                    # then going down as the seed spawns in the eye
                    oos_option_hard_logic(),
                    oos_has_shooter(),
                    Or(
                        oos_can_use_ember_seeds(False),
                        oos_can_use_scent_seeds(),
                        oos_can_use_pegasus_seeds(),
                        oos_can_use_mystery_seeds(),
                    )
                )
            ),
            # oos_can_kill_armored_enemy(),
            oos_can_remove_rockslide(False),
        )],

        # 3 keys
        ["frypolar entrance", "frypolar room", False, oos_has_small_keys(8, 3)],
        ["frypolar room", "frypolar room wild mystery", False, oos_can_harvest_regrowing_bush()],
        ["frypolar room", "beat frypolar", False, Or(
            # Requirements to kill Frypolar
            And(
                # Casual logic: mystery seeds method is considered mandatory since it's the easiest one
                oos_has_mystery_seeds(),
                oos_has_bracelet()
            ),
            And(
                # Medium logic: allow killing Frypolar with ember only, but with at least a Lv2 satchel
                # (the miniboss require 15 embers to die, so 20 max is a bit tight)
                oos_option_medium_logic(),
                oos_can_use_ember_seeds(False),
                oos_has_satchel(2),
            ),
            And(
                # Hard logic: yolo
                oos_option_hard_logic(),
                oos_can_use_ember_seeds(False)
            )
            # The means of throwing the seeds do not matter:
            # beat frypolar only leads to d8 ice puzzle room in hard-, which requires a HSS.
            # In hell, this is the only place where this region is used without HSS, but then, even satchel is enough
            # (In all honesty, hell players are probably doing HSS skip to come here, so the route is not *that* bad)
        )],
        ["beat frypolar", "d8 spinner chest", False, None],
        ["beat frypolar", "d8 ice puzzle room", False, And(
            oos_has_hyper_slingshot(),
            oos_can_use_ember_seeds(False),
        )],

        ["d8 ice puzzle room", "d8 pols voice chest", False, Or(
            oos_has_magic_boomerang(),
            oos_can_jump_6_wide_pit(),
            oos_has_shooter(),
            And(
                oos_option_medium_logic(),
                oos_has_bombchus_to_fight()
            )
        )],

        # 4 keys
        ["d8 ice puzzle room", "d8 crystal room", False, oos_has_small_keys(8, 4)],
        ["d8 crystal room", "magical ice owl", False, oos_can_use_mystery_seeds()],
        ["d8 crystal room", "d8 ghost armos drop", False, oos_can_remove_rockslide(False)],
        ["d8 crystal room", "d8 NE crystal", False, And(
            oos_has_bracelet(),
            oos_can_trigger_lever()
        )],
        ["d8 crystal room", "d8 SE crystal", False, oos_has_bracelet()],
        ["d8 crystal room", "d8 SW lava chest", False, None],
        ["d8 SE crystal", "d8 SE lava chest", False, None],

        ["d8 SE crystal", "d8 spark chest", False, None],
        ["d8 ice puzzle room", "d8 spark chest", False, And(
            # Switch hook from the ice puzzle, then s&q
            oos_option_medium_logic(),
            oos_has_switch_hook()
        )],

        # 6 keys
        ["d8 crystal room", "d8 NW crystal", False, And(
            oos_has_bracelet(),
            oos_has_small_keys(8, 6)
        )],
        ["d8 crystal room", "d8 SW crystal", False, And(
            oos_has_bracelet(),
            oos_has_small_keys(8, 6)
        )],

        # 7 keys
        ["d8 NW crystal", "d8 boss", False, And(
            oos_has_small_keys(8, 7),
            oos_has_boss_key(8),
            Or(
                oos_has_sword(),
                oos_has_fools_ore()
            )
        )],
    ]


def make_d11_logic(options: OracleOfSeasonsOptions):
    if not options.linked_heros_cave.value:
        return []
    logic = [
        ["enter d11", "d11 floor 1 chest", False, oos_has_bracelet()],
        ["d11 floor 1 chest", "d11 floor 2 keydrop", False, oos_can_jump_2_wide_pit()],
        ["d11 floor 2 keydrop", "d11 floor 2 chest", False, oos_has_small_keys(11)],
        ["d11 floor 2 chest", "d11 floor 3 torch keydrop", False, And(
            Or(
                oos_can_swim(False),
                And(
                    # Jump and break the pot
                    oos_option_hell_logic(),
                    oos_can_jump_5_wide_liquid(),
                    Or(
                        oos_has_noble_sword(),
                        Has("Biggoron's Sword"),
                    )
                )
            ),
            oos_can_use_ember_seeds(True),
        )],
        ["d11 floor 2 chest", "d11 floor 3 flooded room", False, And(
            oos_can_swim(False),
            oos_has_small_keys(11, 2),
            oos_can_use_ember_seeds(True),
            oos_has_seed_thrower()
        )],
        ["d11 floor 3 flooded room", "d11 floor 3 flooded keydrop", False, Or(
            oos_can_kill_normal_enemy(),
            oos_has_switch_hook()
        )],
        ["d11 floor 3 flooded room", "d11 floor 3 chest", False, And(
            oos_can_remove_rockslide(False),
            oos_has_small_keys(11, 3)
        )],
        ["d11 floor 3 chest", "d11 floor 4 chest", False, oos_has_magnet_gloves()],
        ["d11 floor 4 chest", "d11 floor 5 gauntlet", False, And(
            oos_can_jump_3_wide_pit(),
            Or(
                And(
                    Or(
                        oos_has_flute(),
                        oos_has_bombs_to_fight(),
                        oos_has_bombchus_to_fight()
                    ),
                    oos_can_kill_magunesu(),
                    oos_can_kill_spiked_beetle()
                ),
                And(
                    # Use the cane press a button at the same time Link is on the button to skip the lowest wave
                    # Counting starts at the top and goes clockwise, waves are:
                    # 0- Spiked Beetle
                    # 1- Gibdo
                    # 2- Arrow Darknut
                    # 3- Magunesu
                    # 4- Lynel
                    # 5- Iron Mask
                    # 6- Pol's Voice
                    # 7- Stalfos

                    # We need to fight at least 5 of these 8 waves, minimal requirement is oos_can_kill_normal_enemy_no_cane
                    # Waves 1, 5 and 7 can be beaten by it
                    # oos_can_kill_armored_enemy can clear waves 2 and 4, skipping 0, 3 and 6
                    # Otherwise, since we know we have embers already, we can also beat 4, but we need more seeds
                    # (only the seeds aren't in oos_can_kill_armored_enemy)
                    # Skip waves 0, 3 and 6 while finishing the waves 1, 5 and 7 with embers
                    # Now there are two waves left, 4 and 2, which can be beaten by cane
                    # A route can be wave 4 -> wave 5 (skip 3) -> wave 7 (skip 6) -> wave 1 (skip 0) -> wave 2
                    # (With enough bombs left, it's probably easier to switch wave 6 and wave 4 as lynels hurt a lot)

                    oos_option_hard_logic(),
                    oos_has_cane(),
                    Or(
                        oos_can_kill_armored_enemy(False, True),
                        oos_has_satchel(2)
                    )
                )
            )
        )],
        ["d11 floor 4 chest", "d11 floor 5 boomerang maze", False, And(
            oos_can_jump_3_wide_pit(),
            oos_has_small_keys(11, 4),
            Or(
                oos_has_magic_boomerang(),
                oos_has_bombchus_to_fight(),
                And(
                    oos_option_medium_logic(),
                    oos_has_sword(True),
                )
            )
        )],
        ["d11 floor 4 chest", "d11 final chest", False, And(
            oos_can_jump_3_wide_pit(),
            oos_has_small_keys(11, 5),
            # oos_has_rupees(80),
            oos_can_complete_d11_puzzle()
        )]
    ]
    if options.linked_heros_cave.value & OracleOfSeasonsLinkedHerosCave.no_alt_entrance:
        logic.append(["enter d11", "d11 alt entrance", False, None])
    else:
        logic.append(["d11 alt entrance", "enter d11", False, None])
    if options.linked_heros_cave.value & OracleOfSeasonsLinkedHerosCave.heros_cave:
        logic.append(["enter d0", "enter d11", False, None])
    return logic
