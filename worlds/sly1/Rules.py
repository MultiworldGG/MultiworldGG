from worlds.generic.Rules import add_rule, set_rule
from worlds.sly1.Types import episode_type_to_unlock
from worlds.sly1.Locations import hourglass_locations, vault_locations, did_include_hourglasses, get_bundle_amount_for_level
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.sly1 import Sly1World

def set_rules(world: "Sly1World"):
    player = world.player
    options = world.options
    bosses = ["Beat Raleigh", "Beat Muggshot", "Beat Mz. Ruby", "Beat Panda King"]

    # Episode Access
    add_rule(world.multiworld.get_entrance("Hideout -> Stealthy Approach", player),
             lambda state: state.has("Tide of Terror: Episode Unlock", player))
    add_rule(world.multiworld.get_entrance("Hideout -> Rocky Start", player),
             lambda state: state.has("Sunset Snake Eyes: Episode Unlock", player))
    add_rule(world.multiworld.get_entrance("Hideout -> Dread Swamp Path", player),
             lambda state: state.has("Vicious Voodoo: Episode Unlock", player))
    add_rule(world.multiworld.get_entrance("Hideout -> Perilous Ascent", player),
             lambda state: state.has("Fire in the Sky: Episode Unlock", player))
    
    # Main Hub Access
    add_rule(world.multiworld.get_entrance("Hideout -> Prowling the Grounds", player),
             lambda state: state.has("Tide of Terror: Key", player)
             and state.has("Tide of Terror: Episode Unlock", player))
    add_rule(world.multiworld.get_entrance("Hideout -> Muggshot's Turf", player),
             lambda state: state.has("Sunset Snake Eyes: Key", player)
             and state.has("Sunset Snake Eyes: Episode Unlock", player))
    add_rule(world.multiworld.get_entrance("Hideout -> Swamp's Dark Center", player),
             lambda state: state.has("Vicious Voodoo: Key", player)
             and state.has("Vicious Voodoo: Episode Unlock", player))
    add_rule(world.multiworld.get_entrance("Hideout -> Inside the Stronghold", player),
             lambda state: state.has("Fire in the Sky: Key", player)
             and state.has("Fire in the Sky: Episode Unlock", player))
    
    add_rule(world.multiworld.get_entrance("Stealthy Approach -> Prowling the Grounds", player),
             lambda state: state.has("Tide of Terror: Key", player))
    add_rule(world.multiworld.get_entrance("Rocky Start -> Muggshot's Turf", player),
             lambda state: state.has("Sunset Snake Eyes: Key", player))
    add_rule(world.multiworld.get_entrance("Dread Swamp Path -> Swamp's Dark Center", player),
             lambda state: state.has("Vicious Voodoo: Key", player))
    add_rule(world.multiworld.get_entrance("Perilous Ascent -> Inside the Stronghold", player),
             lambda state: state.has("Fire in the Sky: Key", player))
    
    # Hub 2 Access
    tricks: list = options.EnableTricks.value
    tot_second_half = True if "tot_second_half_early" in tricks else False
    sse_second_half = True if "sse_second_half_early" in tricks else False
    vv_second_half = True if "vv_second_half_early" in tricks else False
    fits_second_half = True if "fits_second_half_early" in tricks else False
    add_rule(world.multiworld.get_entrance("Prowling the Grounds -> Prowling the Grounds - Second Gate", player),
             lambda state: state.has("Tide of Terror: Key", player, 3) or tot_second_half)
    add_rule(world.multiworld.get_entrance("Muggshot's Turf -> Muggshot's Turf - Second Gate", player),
             lambda state: state.has("Sunset Snake Eyes: Key", player, 3) or sse_second_half)
    add_rule(world.multiworld.get_entrance("Swamp's Dark Center -> Swamp's Dark Center - Second Gate", player),
             lambda state: state.has("Vicious Voodoo: Key", player, 3) or vv_second_half)
    add_rule(world.multiworld.get_entrance("Inside the Stronghold -> Inside the Stronghold - Second Gate", player),
             lambda state: state.has("Fire in the Sky: Key", player, 3) or fits_second_half)
    
    # Boss Access
    raleigh_early = True if "tot_raleigh_early" in tricks else False
    muggshot_early = True if "sse_muggshot_early" in tricks else False
    # no skip into Mz. Ruby early yet...some day...
    panda_early = True if "fits_panda_early" in tricks else False
    add_rule(world.multiworld.get_entrance("Prowling the Grounds - Second Gate -> Eye of the Storm", player),
             lambda state: state.has("Tide of Terror: Key", player, 7) or raleigh_early)
    add_rule(world.multiworld.get_entrance("Muggshot's Turf - Second Gate -> Last Call", player),
             lambda state: state.has("Sunset Snake Eyes: Key", player, 7) or muggshot_early)
    add_rule(world.multiworld.get_entrance("Swamp's Dark Center - Second Gate -> Deadly Dance", player),
             lambda state: state.has("Vicious Voodoo: Key", player, 7))
    add_rule(world.multiworld.get_entrance("Inside the Stronghold - Second Gate -> Flame Fu!", player),
             lambda state: state.has("Fire in the Sky: Key", player, 7) or panda_early)
    
    # Cold Heart of Hate Access
    if options.UnlockClockwerk.value == 1:
        set_rule(world.multiworld.get_entrance("Hideout -> Cold Heart of Hate", player),
            lambda state: sum(state.has(boss, player) for boss in bosses) >= options.RequiredBosses.value)
    elif options.UnlockClockwerk.value == 2:
        set_rule(world.multiworld.get_entrance("Hideout -> Cold Heart of Hate", player),
            lambda state: state.has("Thievius Raccoonus Page", player, options.RequiredPages.value))
        
    # Cluesanity rules
    if options.ItemCluesanityBundleSize.value > 0:
        for name, data in vault_locations.items():
            level_name = name.split(':')[0]
            bundle_amount = get_bundle_amount_for_level(level_name, world.options.ItemCluesanityBundleSize.value)
            bottle_name = f'{level_name}: Bottle(s)'
            
            add_rule(world.multiworld.get_location(name, player),
                     lambda state, bn=bottle_name, ba=bundle_amount: state.has(bn, player, ba))

    # Hourglass Rules
    if did_include_hourglasses(world):
        for key, data in hourglass_locations.items():
            loc = world.multiworld.get_location(key, player)
            ep_name = episode_type_to_unlock[data.key_type].replace(": Episode Unlock", "")
            add_rule(loc, lambda state, key_name = f"{ep_name}: Key", key_req=data.key_requirement:
                state.has(key_name, player, key_req))

            if options.HourglassesRequireRoll:
                add_rule(loc, lambda state, roll = "Progressive Roll": state.has(roll, player, 1))

            if world.options.ItemCluesanityBundleSize.value > 0:
                level_name = key.split(':')[0]
                bundle_amount = get_bundle_amount_for_level(level_name, world.options.ItemCluesanityBundleSize.value)
                bottle_name = f'{level_name}: Bottle(s)'

                add_rule(world.multiworld.get_location(key, player),
                        lambda state, bn=bottle_name, ba=bundle_amount: state.has(bn, player, ba))

        add_rule(world.multiworld.get_location("Unseen Foe: Hourglass", player),
             lambda state: state.has("Progressive Invisibility", player, 1))

    # Extra rules for Unseen Foe
    invis_skip = True if "unseen_foe_invis_skip" in world.options.EnableTricks.value else False
    add_rule(world.multiworld.get_location("Unseen Foe: Key", player),
             lambda state: state.has("Progressive Invisibility", player, 1) or invis_skip)
    add_rule(world.multiworld.get_location("Unseen Foe: Vault", player),
             lambda state: state.has("Progressive Invisibility", player, 1) or invis_skip)
    for location in world.multiworld.get_locations(player):
        if "Unseen Foe" in location.name and "Bottle" in location.name:
            add_rule(location, lambda state: state.has("Progressive Invisibility", player, 1) or invis_skip)

    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)