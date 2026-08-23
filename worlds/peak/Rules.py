from typing import TYPE_CHECKING

from BaseClasses import Location, Entrance

if TYPE_CHECKING:
    from . import PeakWorld

CALDERA_LOCATIONS = [
    "Acquire Big Egg", "Acquire Egg", "Acquire Cooked Bird", "Volcanology Badge", "Wanderer Badge", "Cool Cucumber Badge", "Bundled Up Badge",
    "Acquire Candlestick", "Acquire Anti-Zooka", "Acquire The Early Worm", "Acquire Warp Fungus",
    "Acquire Frog", "Acquire Ritual Dagger", "Acquire Frog Legs", "Acquire Rocketpack",
    "Acquire Jetpack", "Acquire Fanny Pack",
    "Acquire Scout's Tenacity", "Acquire Scout's Generosity", "Acquire Scout's Ambition",
    "Acquire Scout's Initiative", "Acquire Small Egg",
]

KILN_LOCATIONS = [
    "Acquire Strange Gem", "Peak Badge", "Speed Climber Badge", "Lone Wolf Badge", "Participation Badge",
    "Survivalist Badge", "Naturalist Badge", "Leave No Trace Badge", "Balloon Badge", "Bing Bong Badge",
    "Gourmand Badge", "High Altitude Badge", "Knot Tying Badge", "24 Karat Badge",
    "Acquire Scout's Honor"
]

ROOTS_LOCATIONS = [
    "Acquire Red Shroomberry", "Acquire Blue Shroomberry", "Acquire Yellow Shroomberry",
    "Acquire Green Shroomberry", "Acquire Purple Shroomberry",
    "Acquire Mandrake", "Acquire Bounce Shroom", "Acquire Cloud Fungus", "Mycoacrobatics Badge",
    "Tread Lightly Badge", "Undead Encounter Badge",
    "Web Security Badge", "Advanced Mycology Badge", "Forestry Badge",
]

TROPICS_LOCATIONS = [
    "Acquire Red Clusterberry", "Acquire Yellow Clusterberry", "Acquire Black Clusterberry",
    "Acquire Purple Kingberry", "Acquire Yellow Kingberry", "Acquire Green Kingberry",
    "Acquire Brown Berrynana", "Acquire Blue Berrynana", "Acquire Pink Berrynana",
    "Acquire Yellow Berrynana", "Acquire Yellow Berrynana Peel", "Acquire Pink Berrynana Peel",
    "Acquire Honeycomb", "Acquire Beehive", "Arborist Badge", "Foraging Badge",
    "Acquire Blue Berrynana Peel", "Acquire Magic Bean", "Acquire Tick", "Acquire Brown Berrynana Peel",
    "Acquire Scorchberry", "Trailblazer Badge",
]

MESA_LOCATIONS = [
    "Acquire Cactus", "Acquire Aloe Vera", "Acquire Sunscreen", "Acquire Ancient Idol",
    "Acquire Red Prickleberry", "Acquire Gold Prickleberry", "Acquire Scorpion", "Acquire Torch",
    "Megaentomology Badge", "Astronomy Badge",
    "Daredevil Badge", "Needlepoint Badge", "Acquire Parasol", "Acquire Dynamite", "Nomad Badge",
]

ALPINE_LOCATIONS = [
    "Acquire Orange Winterberry", "Acquire Napberry", "Acquire Yellow Winterberry",
    "Animal Serenading Badge", "Acquire Heat Pack", "Alpinist Badge",
]


def _get_vanilla_biome_level(location_name):
    if location_name in TROPICS_LOCATIONS or location_name in ROOTS_LOCATIONS:
        return 1
    if location_name in MESA_LOCATIONS or location_name in ALPINE_LOCATIONS:
        return 2
    if location_name in CALDERA_LOCATIONS:
        return 3
    if location_name in KILN_LOCATIONS:
        return 4
    return 0


MYSTICAL_MIN_LEVELS = {
    "Acquire Fanny Pack": 1,
    "Acquire Balloon": 1,
    "Acquire Ritual Dagger": 2,
    "Acquire Faerie Lantern": 2,
    "Acquire Pandora's Lunchbox": 2,
    "Acquire Rocketpack": 2,
    "Acquire Bugle of Friendship": 2,
    "Acquire Portable Stove": 2,
    "Acquire Sports Drink": 2,
    "Acquire Anti-Zooka": 3,
    "Acquire Book of Bones": 3,
    "Acquire Pirate's Compass": 3,
    "Acquire Scout Effigy": 3,
    "Acquire Jetpack": 3,
    "Acquire Warp Fungus": 3,
    "Acquire Checkpoint Flag": 3,
}


def _apply_mystical_minimums(assignments):
    for loc, min_level in MYSTICAL_MIN_LEVELS.items():
        if loc in assignments and assignments[loc] < min_level:
            assignments[loc] = min_level
    return assignments


def generate_loot_biome_assignments(acquire_locations, random_source, loot_sanity_mode):
    vanilla = {loc: _get_vanilla_biome_level(loc) for loc in acquire_locations}
    if loot_sanity_mode == 0:
        return _apply_mystical_minimums(vanilla)

    shuffleable_names = []
    shuffleable_levels = []
    fixed = {}

    for loc, level in vanilla.items():
        if level == 4:
            fixed[loc] = level
        else:
            shuffleable_names.append(loc)
            shuffleable_levels.append(level)

    random_source.shuffle(shuffleable_levels)

    result = dict(zip(shuffleable_names, shuffleable_levels))
    result.update(fixed)
    return _apply_mystical_minimums(result)


def set_rule(spot: Location | Entrance, rule):
    spot.access_rule = rule


def add_rule(spot: Location | Entrance, rule, combine="and"):
    old_rule = spot.access_rule
    if old_rule is Location.access_rule:
        spot.access_rule = rule if combine == "and" else old_rule
    else:
        if combine == "and":
            spot.access_rule = lambda state: rule(state) and old_rule(state)
        else:
            spot.access_rule = lambda state: rule(state) or old_rule(state)


def apply_rules(world: "PeakWorld"):
    """Apply all access rules for Peak locations."""
    player = world.player
    required_ascent = world.options.ascent_count.value
    goals = world.options.goals.value
    progressive_stamina_enabled = world.options.progressive_stamina.value

    # Biome access rules
    try:
        if progressive_stamina_enabled:
            set_rule(world.get_location("Roots Access"),
                     lambda state: state.has("Progressive Mountain", player, 1) and
                                   state.has("Progressive Stamina Bar", player, 2))
            set_rule(world.get_location("Tropics Access"),
                     lambda state: state.has("Progressive Mountain", player, 1) and
                                   state.has("Progressive Stamina Bar", player, 2))

            set_rule(world.get_location("Mesa Access"),
                     lambda state: state.has("Progressive Mountain", player, 2) and
                                   state.has("Progressive Stamina Bar", player, 3))
            set_rule(world.get_location("Alpine Access"),
                     lambda state: state.has("Progressive Mountain", player, 2) and
                                   state.has("Progressive Stamina Bar", player, 3))

            set_rule(world.get_location("Caldera Access"),
                     lambda state: state.has("Progressive Mountain", player, 3) and
                                   state.has("Progressive Stamina Bar", player, 3))
            set_rule(world.get_location("Kiln Access"),
                     lambda state: state.has("Progressive Mountain", player, 4) and
                                   state.has("Progressive Stamina Bar", player, 3))
        else:
            set_rule(world.get_location("Roots Access"),
                     lambda state: state.has("Progressive Mountain", player, 1))
            set_rule(world.get_location("Tropics Access"),
                     lambda state: state.has("Progressive Mountain", player, 1))

            set_rule(world.get_location("Mesa Access"),
                     lambda state: state.has("Progressive Mountain", player, 2))
            set_rule(world.get_location("Alpine Access"),
                     lambda state: state.has("Progressive Mountain", player, 2))

            set_rule(world.get_location("Caldera Access"),
                     lambda state: state.has("Progressive Mountain", player, 3))
            set_rule(world.get_location("Kiln Access"),
                     lambda state: state.has("Progressive Mountain", player, 4))
    except KeyError:
        pass

    item_sanity = world.options.item_sanity.value

    # Acquire locations - when ItemSanity is on, require having received the unlock item from AP first
    # When ItemSanity is off, acquire locations only need biome access (handled below)
    acquire_item_rules = {
        "Acquire Rope Spool": "Rope Spool Unlock",
        "Acquire Rope Cannon": "Rope Cannon Unlock",
        "Acquire Anti-Rope Spool": "Anti-Rope Spool Unlock",
        "Acquire Anti-Rope Cannon": "Anti-Rope Cannon Unlock",
        "Acquire Chain Launcher": "Chain Launcher Unlock",
        "Acquire Piton": "Piton Unlock",
        "Acquire Rescue Claw": "Rescue Claw Unlock",
        "Acquire Magic Bean": "Magic Bean Unlock",
        "Acquire Parasol": "Parasol Unlock",
        "Acquire Balloon": "Balloon Unlock",
        "Acquire Balloon Bunch": "Balloon Bunch Unlock",
        "Acquire Scout Cannon": "Scout Cannon Unlock",
        "Acquire Flying Disc": "Flying Disc Unlock",
        "Acquire Guidebook": "Guidebook Unlock",
        "Acquire Portable Stove": "Portable Stove Unlock",
        "Acquire Checkpoint Flag": "Checkpoint Flag Unlock",
        "Acquire Lantern": "Lantern Unlock",
        "Acquire Flare": "Flare Unlock",
        "Acquire Torch": "Torch Unlock",
        "Acquire Faerie Lantern": "Faerie Lantern Unlock",
        "Acquire Blowgun": "Blowgun Unlock",
        "Acquire Cactus": "Cactus Unlock",
        "Acquire Compass": "Compass Unlock",
        "Acquire Pirate's Compass": "Pirate's Compass Unlock",
        "Acquire Binoculars": "Binoculars Unlock",
        "Acquire Bandages": "Bandages Unlock",
        "Acquire First-Aid Kit": "First-Aid Kit Unlock",
        "Acquire Antidote": "Antidote Unlock",
        "Acquire Heat Pack": "Heat Pack Unlock",
        "Acquire Cure-All": "Cure-All Unlock",
        "Acquire Remedy Fungus": "Remedy Fungus Unlock",
        "Acquire Medicinal Root": "Medicinal Root Unlock",
        "Acquire Aloe Vera": "Aloe Vera Unlock",
        "Acquire Sunscreen": "Sunscreen Unlock",
        "Acquire Marshmallow": "Marshmallow Unlock",
        "Acquire Glizzy": "Glizzy Unlock",
        "Acquire Fortified Milk": "Fortified Milk Unlock",
        "Acquire Scout Effigy": "Scout Effigy Unlock",
        "Acquire Cursed Skull": "Cursed Skull Unlock",
        "Acquire Pandora's Lunchbox": "Pandora's Lunchbox Unlock",
        "Acquire Ancient Idol": "Ancient Idol Unlock",
        "Acquire Strange Gem": "Strange Gem Unlock",
        "Acquire Book of Bones": "Book of Bones Unlock",
        "Acquire Cloud Fungus": "Cloud Fungus Unlock",
        "Acquire Bugle of Friendship": "Bugle of Friendship Unlock",
        "Acquire Bugle": "Bugle Unlock",
        "Acquire Shelf Shroom": "Shelf Shroom Unlock",
        "Acquire Bounce Shroom": "Bounce Shroom Unlock",
        "Acquire Button Shroom": "Button Shroom Unlock",
        "Acquire Bugle Shroom": "Bugle Shroom Unlock",
        "Acquire Cluster Shroom": "Cluster Shroom Unlock",
        "Acquire Chubby Shroom": "Chubby Shroom Unlock",
        "Acquire Trail Mix": "Trail Mix Unlock",
        "Acquire Granola Bar": "Granola Bar Unlock",
        "Acquire Scout Cookies": "Scout Cookies Unlock",
        "Acquire Airline Food": "Airline Food Unlock",
        "Acquire Energy Drink": "Energy Drink Unlock",
        "Acquire Sports Drink": "Sports Drink Unlock",
        "Acquire Big Lollipop": "Big Lollipop Unlock",
        "Acquire Big Egg": "Big Egg Unlock",
        "Acquire Egg": "Egg Unlock",
        "Acquire Cooked Bird": "Cooked Bird Unlock",
        "Acquire Honeycomb": "Honeycomb Unlock",
        "Acquire Beehive": "Beehive Unlock",
        "Acquire Scorpion": "Scorpion Unlock",
        "Acquire Tick": "Tick Unlock",
        "Acquire Conch": "Conch Unlock",
        "Acquire Dynamite": "Dynamite Unlock",
        "Acquire Bing Bong": "Bing Bong Unlock",
        "Acquire Mandrake": "Mandrake Unlock",
        "Acquire Red Crispberry": "Red Crispberry Unlock",
        "Acquire Green Crispberry": "Green Crispberry Unlock",
        "Acquire Yellow Crispberry": "Yellow Crispberry Unlock",
        "Acquire Coconut": "Coconut Unlock",
        "Acquire Coconut Half": "Coconut Half Unlock",
        "Acquire Brown Berrynana": "Brown Berrynana Unlock",
        "Acquire Blue Berrynana": "Blue Berrynana Unlock",
        "Acquire Pink Berrynana": "Pink Berrynana Unlock",
        "Acquire Yellow Berrynana": "Yellow Berrynana Unlock",
        "Acquire Orange Winterberry": "Orange Winterberry Unlock",
        "Acquire Yellow Winterberry": "Yellow Winterberry Unlock",
        "Acquire Red Prickleberry": "Red Prickleberry Unlock",
        "Acquire Gold Prickleberry": "Gold Prickleberry Unlock",
        "Acquire Red Shroomberry": "Red Shroomberry Unlock",
        "Acquire Blue Shroomberry": "Blue Shroomberry Unlock",
        "Acquire Green Shroomberry": "Green Shroomberry Unlock",
        "Acquire Yellow Shroomberry": "Yellow Shroomberry Unlock",
        "Acquire Purple Shroomberry": "Purple Shroomberry Unlock",
        "Acquire Purple Kingberry": "Purple Kingberry Unlock",
        "Acquire Yellow Kingberry": "Yellow Kingberry Unlock",
        "Acquire Green Kingberry": "Green Kingberry Unlock",
        "Acquire Napberry": "Napberry Unlock",
        "Acquire Black Clusterberry": "Black Clusterberry Unlock",
        "Acquire Red Clusterberry": "Red Clusterberry Unlock",
        "Acquire Yellow Clusterberry": "Yellow Clusterberry Unlock",
        "Acquire Scorchberry": "Scorchberry Unlock",
        "Acquire Scoutmaster's Bugle": "Scoutmaster's Bugle Unlock",
        "Acquire Yellow Berrynana Peel": "Yellow Berrynana Unlock",
        "Acquire Pink Berrynana Peel": "Pink Berrynana Unlock",
        "Acquire Blue Berrynana Peel": "Blue Berrynana Unlock",
        "Acquire Brown Berrynana Peel": "Brown Berrynana Unlock",

        # Gloom & Citadel update
        "Acquire Anti-Zooka": "Anti-Zooka Unlock",
        "Acquire The Early Worm": "The Early Worm Unlock",
        "Acquire Warp Fungus": "Warp Fungus Unlock",
        "Acquire Glider": "Glider Unlock",
        "Acquire Ritual Dagger": "Ritual Dagger Unlock",
        "Acquire Candlestick": "Candlestick Unlock",
        "Acquire Frog": "Frog Unlock",
        "Acquire Rocketpack": "Rocketpack Unlock",
        "Acquire Jetpack": "Jetpack Unlock",
        "Acquire Fanny Pack": "Progressive Pack",
        "Acquire Backpack": "Progressive Pack",
        "Acquire Frog Legs": "Frog Legs Unlock",
        "Acquire Scout's Tenacity": "Scout's Tenacity Unlock",
        "Acquire Scout's Generosity": "Scout's Generosity Unlock",
        "Acquire Scout's Ambition": "Scout's Ambition Unlock",
        "Acquire Scout's Initiative": "Scout's Initiative Unlock",
        "Acquire Scout's Honor": "Scout's Honor Unlock",
        "Acquire Small Egg": "Small Egg Unlock",
    }

    scout_amulet_sanity = world.options.scout_amulet_sanity.value
    scout_amulet_locations = {
        "Acquire Scout's Tenacity", "Acquire Scout's Generosity",
        "Acquire Scout's Ambition", "Acquire Scout's Initiative",
        "Acquire Scout's Honor",
    }
    progressive_amulets = item_sanity and scout_amulet_sanity and "Free The Soul" in goals
    amulet_chain_counts = {
        "Acquire Strange Gem": 1,
        "Acquire Scout's Tenacity": 2,
        "Acquire Scout's Generosity": 3,
        "Acquire Scout's Ambition": 4,
        "Acquire Scout's Initiative": 5,
        "Acquire Scout's Honor": 6,
    }

    # Generate loot biome assignments (shuffled when loot sanity is on)
    loot_sanity_mode = world.options.loot_sanity.value
    loot_biome = generate_loot_biome_assignments(
        acquire_item_rules.keys(), world.random, loot_sanity_mode
    )
    # The five Scout amulet items keep their vanilla biomes when they are not part of loot sanity
    if not scout_amulet_sanity:
        for _name in scout_amulet_locations:
            if _name in loot_biome:
                loot_biome[_name] = _get_vanilla_biome_level(_name)

    world.loot_biome_assignments = loot_biome

    # Apply acquire item rules using the (possibly shuffled) biome assignments
    for location_name, required_item in acquire_item_rules.items():
        try:
            biome_level = loot_biome.get(location_name, 0)
            needs_unlock = item_sanity and (scout_amulet_sanity or location_name not in scout_amulet_locations)
            if needs_unlock:
                if biome_level == 0:
                    set_rule(world.get_location(location_name),
                             lambda state, item=required_item:
                             state.has(item, player))
                else:
                    set_rule(world.get_location(location_name),
                             lambda state, item=required_item, lvl=biome_level:
                             state.has(item, player) and
                             state.has("Progressive Mountain", player, lvl))
            else:
                if biome_level == 0:
                    set_rule(world.get_location(location_name), lambda state: True)
                else:
                    set_rule(world.get_location(location_name),
                             lambda state, lvl=biome_level:
                             state.has("Progressive Mountain", player, lvl))
        except KeyError:
            pass

    if not item_sanity:
        try:
            set_rule(world.get_location("Acquire Portable Stove"),
                     lambda state: state.has("Progressive Mountain", player, 1))
        except KeyError:
            pass
        try:
            set_rule(world.get_location("Acquire Antidote"),
                     lambda state: state.has("Progressive Mountain", player, 1))
        except KeyError:
            pass
        try:
            set_rule(world.get_location("Acquire Pirate's Compass"),
                     lambda state: state.has("Progressive Mountain", player, 4))
        except KeyError:
            pass

    # Scout's Honor also requires the other four Scout's items and the Strange Gem, on top of its biome level
    if item_sanity and scout_amulet_sanity and not progressive_amulets:
        _scout_unlocks = [
            "Scout's Tenacity Unlock", "Scout's Generosity Unlock",
            "Scout's Ambition Unlock", "Scout's Initiative Unlock",
            "Strange Gem Unlock",
        ]
        try:
            _honor_level = loot_biome.get("Acquire Scout's Honor", 0)
            set_rule(world.get_location("Acquire Scout's Honor"),
                     lambda state, lvl=_honor_level: (
                         state.has("Scout's Honor Unlock", player) and
                         state.has_all(_scout_unlocks, player) and
                         (lvl == 0 or state.has("Progressive Mountain", player, lvl))))
        except KeyError:
            pass

    # Scout's Honor comes from the statue's Strange Gem, which is gated by Strange Gem Unlock
    if item_sanity and not scout_amulet_sanity:
        try:
            add_rule(world.get_location("Acquire Scout's Honor"),
                     lambda state: state.has("Strange Gem Unlock", player))
        except KeyError:
            pass

    # Backpack is the second Progressive Pack
    if item_sanity:
        try:
            _pack_lvl = loot_biome.get("Acquire Backpack", 0)
            set_rule(world.get_location("Acquire Backpack"),
                     lambda state, lvl=_pack_lvl: (
                         state.has("Progressive Pack", player, 2) and
                         (lvl == 0 or state.has("Progressive Mountain", player, lvl))))
        except KeyError:
            pass

    # Free The Soul goal: the amulet chain is a single progressive item
    if progressive_amulets:
        for _loc_name, _count in amulet_chain_counts.items():
            try:
                _lvl = loot_biome.get(_loc_name, 0)
                set_rule(world.get_location(_loc_name),
                         lambda state, c=_count, lvl=_lvl: (
                             state.has("Progressive Amulet Unlock", player, c) and
                             (lvl == 0 or state.has("Progressive Mountain", player, lvl))))
            except KeyError:
                pass

    # Build unlock-to-biome-level mapping from loot assignments
    # For unlocks that map to multiple acquire locations, use the minimum biome level
    unlock_to_biome = {}
    for acquire_loc, unlock_name in acquire_item_rules.items():
        level = loot_biome.get(acquire_loc, 0)
        if unlock_name not in unlock_to_biome or level < unlock_to_biome[unlock_name]:
            unlock_to_biome[unlock_name] = level

    def _biome_rule(lvl):
        if lvl == 0:
            return lambda state: True
        return lambda state, l=lvl: state.has("Progressive Mountain", player, l)

    def _unlock_and_biome_rule(unlock, lvl):
        if lvl == 0:
            return lambda state, u=unlock: state.has(u, player)
        return lambda state, u=unlock, l=lvl: state.has(u, player) and state.has("Progressive Mountain", player, l)

    def _apply_single_item_badge(badge_name, unlock_name):
        try:
            lvl = unlock_to_biome.get(unlock_name, 0)
            if item_sanity:
                set_rule(world.get_location(badge_name), _unlock_and_biome_rule(unlock_name, lvl))
            else:
                set_rule(world.get_location(badge_name), _biome_rule(lvl))
        except KeyError:
            pass

    # All regular badge locations are always accessible
    regular_badges = [
        "Mycology Badge",
        "Endurance Badge", "Toxicology Badge", "Bouldering Badge",
        "Cooking Badge", "Plunderer Badge",
        "Esoterica Badge", "Beachcomber Badge", "Mentorship Badge",
        "Disaster Response Badge", "Competitive Eating Badge",
        "Cryptogastronomy Badge", "Calcium Intake Badge", "Applied Esoterica Badge",
        "Happy Camper Badge", "First Aid Badge", "Clutch Badge",
        "Emergency Preparedness Badge", "Bookworm Badge", "Resourcefulness Badge",
        "Ultimate Badge",
    ]

    special_badges = {"Mycology Badge", "Applied Esoterica Badge", "Bouldering Badge",
                      "Calcium Intake Badge", "Competitive Eating Badge",
                      "Cryptogastronomy Badge", "Disaster Response Badge", "Esoterica Badge",
                      "Toxicology Badge", "Ultimate Badge", "Beachcomber Badge",
                      "Plunderer Badge", "Endurance Badge", "Mentorship Badge",
                      "First Aid Badge"}
    for badge_name in [b for b in regular_badges if b not in special_badges]:
        try:
            set_rule(world.get_location(badge_name), lambda state: True)
        except KeyError:
            pass

    try:
        if progressive_stamina_enabled:
            set_rule(world.get_location("Endurance Badge"),
                     lambda state:
                     state.has("Progressive Stamina Bar", player, 3) and
                     state.has("Progressive Endurance", player, 2) and
                     state.has("Progressive Mountain", player, 1))
        else:
            set_rule(world.get_location("Endurance Badge"),
                     lambda state:
                     state.has("Progressive Endurance", player, 2) and
                     state.has("Progressive Mountain", player, 1))
    except KeyError:
        pass

    try:
        if item_sanity:
            set_rule(world.get_location("Mycology Badge"),
                     lambda state:
                     state.has("Bugle Shroom Unlock", player) and
                     state.has("Button Shroom Unlock", player) and
                     state.has("Chubby Shroom Unlock", player) and
                     state.has("Cluster Shroom Unlock", player) and
                     state.has("Progressive Mountain", player, 1))
        else:
            set_rule(world.get_location("Mycology Badge"),
                     lambda state: state.has("Progressive Mountain", player, 1))
    except KeyError:
        pass

    try:
        if item_sanity:
            set_rule(world.get_location("Aeronautics Badge"),
                     lambda state:
                     (state.has("Balloon Unlock", player) or
                      state.has("Balloon Bunch Unlock", player)) and
                     state.has("Progressive Mountain", player, 4))
        else:
            set_rule(world.get_location("Aeronautics Badge"),
                     lambda state: state.has("Progressive Mountain", player, 4))
    except KeyError:
        pass

    # Applied Esoterica Badge - Book of Bones
    _apply_single_item_badge("Applied Esoterica Badge", "Book of Bones Unlock")

    _apply_single_item_badge("Mentorship Badge", "Scoutmaster's Bugle Unlock")
    _apply_single_item_badge("Hang Gliding Badge", "Glider Unlock")
    _apply_single_item_badge("Last Resort Badge", "Ritual Dagger Unlock")

    try:
        set_rule(world.get_location("Medieval History Badge"),
                 lambda state: state.has("Kiln Access", player))
    except KeyError:
        pass
    try:
        set_rule(world.get_location("Exorcist Badge"),
                 lambda state: state.has("Caldera Access", player))
    except KeyError:
        pass
    try:
        set_rule(world.get_location("Jester Badge"),
                 lambda state: state.has("Caldera Access", player))
    except KeyError:
        pass
    try:
        set_rule(world.get_location("Bellringer Badge"),
                 lambda state: state.has("Caldera Access", player))
    except KeyError:
        pass
    try:
        set_rule(world.get_location("Archery Badge"),
                 lambda state: state.has("Kiln Access", player))
    except KeyError:
        pass
    try:
        set_rule(world.get_location("Well Rested Badge"),
                 lambda state: state.has("Caldera Access", player))
    except KeyError:
        pass

    try:
        set_rule(world.get_location("First Aid Badge"),
                 lambda state: state.has("Progressive Mountain", player, 1))
    except KeyError:
        pass

    # Bouldering Badge - Piton
    _apply_single_item_badge("Bouldering Badge", "Piton Unlock")

    # Calcium Intake Badge - Fortified Milk
    _apply_single_item_badge("Calcium Intake Badge", "Fortified Milk Unlock")

    # Competitive Eating Badge - Glizzy
    _apply_single_item_badge("Competitive Eating Badge", "Glizzy Unlock")

    # Cryptogastronomy Badge - Mandrake
    _apply_single_item_badge("Cryptogastronomy Badge", "Mandrake Unlock")

    # Disaster Response Badge - Rescue Claw
    _apply_single_item_badge("Disaster Response Badge", "Rescue Claw Unlock")

    # Esoterica Badge - ANY of 11 items; biome = min level among them
    try:
        eso_unlocks = [
            "Ancient Idol Unlock", "Anti-Rope Cannon Unlock", "Anti-Rope Spool Unlock",
            "Bugle of Friendship Unlock", "Cure-All Unlock", "Cursed Skull Unlock",
            "Faerie Lantern Unlock", "Pandora's Lunchbox Unlock", "Scout Effigy Unlock",
            "Scoutmaster's Bugle Unlock", "Book of Bones Unlock",
        ]
        eso_biome = min(unlock_to_biome.get(u, 0) for u in eso_unlocks)
        if item_sanity:
            set_rule(world.get_location("Esoterica Badge"),
                     lambda state, lvl=eso_biome:
                     (state.has("Ancient Idol Unlock", player) or
                      state.has("Anti-Rope Cannon Unlock", player) or
                      state.has("Anti-Rope Spool Unlock", player) or
                      state.has("Bugle of Friendship Unlock", player) or
                      state.has("Cure-All Unlock", player) or
                      state.has("Cursed Skull Unlock", player) or
                      state.has("Faerie Lantern Unlock", player) or
                      state.has("Pandora's Lunchbox Unlock", player) or
                      state.has("Scout Effigy Unlock", player) or
                      state.has("Scoutmaster's Bugle Unlock", player) or
                      state.has("Book of Bones Unlock", player)) and
                     (lvl == 0 or state.has("Progressive Mountain", player, lvl)))
        else:
            set_rule(world.get_location("Esoterica Badge"), _biome_rule(eso_biome))
    except KeyError:
        pass

    # Plunderer Badge - requires 1 Progressive Mountain
    try:
        set_rule(world.get_location("Plunderer Badge"),
                 lambda state: state.has("Progressive Mountain", player, 1))
    except KeyError:
        pass

    # Beachcomber Badge - awarded at the Shore campfire, reachable from the start
    try:
        set_rule(world.get_location("Beachcomber Badge"), lambda state: True)
    except KeyError:
        pass

    # Ultimate Badge - Flying Disc
    _apply_single_item_badge("Ultimate Badge", "Flying Disc Unlock")

    try:
        if item_sanity:
            set_rule(world.get_location("Toxicology Badge"),
                     lambda state:
                     (state.has("Antidote Unlock", player) or
                      state.has("Cure-All Unlock", player) or
                      state.has("First-Aid Kit Unlock", player) or
                      state.has("Medicinal Root Unlock", player)) and
                     state.has("Progressive Mountain", player, 1))
        else:
            set_rule(world.get_location("Toxicology Badge"),
                     lambda state: state.has("Progressive Mountain", player, 1))
    except KeyError:
        pass

    luggage_no_gate = [
        "Open 1 luggage",
        "Open 5 luggage",
        "Open 10 luggage",
    ]
    luggage_mountain_gates = {
        1: ["Open 15 luggage", "Open 20 luggage", "Open 25 luggage", "Open 30 luggage"],
        2: ["Open 35 luggage", "Open 40 luggage", "Open 45 luggage", "Open 50 luggage"],
        3: ["Open 55 luggage", "Open 60 luggage", "Open 65 luggage", "Open 70 luggage"],
        4: ["Open 75 luggage", "Open 80 luggage", "Open 85 luggage", "Open 90 luggage",
            "Open 95 luggage", "Open 100 luggage"],
    }
    single_run_no_gate = [
        "Open 2 luggage in a single run",
        "Open 5 luggage in a single run",
        "Open 10 luggage in a single run",
    ]
    single_run_mountain_gates = {
        1: ["Open 15 luggage in a single run"],
        2: ["Open 20 luggage in a single run"],
    }

    for luggage_name in luggage_no_gate + single_run_no_gate:
        try:
            set_rule(world.get_location(luggage_name), lambda state: True)
        except KeyError:
            pass

    for gate_set in (luggage_mountain_gates, single_run_mountain_gates):
        for mountains_needed, locations in gate_set.items():
            for luggage_name in locations:
                try:
                    set_rule(world.get_location(luggage_name),
                             lambda state, m=mountains_needed: state.has("Progressive Mountain", player, m))
                except KeyError:
                    pass

    try:
        if item_sanity:
            set_rule(world.get_location("Idol Dunked"),
                     lambda state: state.has("Ancient Idol Unlock", player) and
                                   state.has("Kiln Access", player))
        else:
            set_rule(world.get_location("Idol Dunked"),
                     lambda state: state.has("Kiln Access", player))
    except KeyError:
        pass
    try:
        set_rule(world.get_location("All Badges Collected"),
                 lambda state: state.has_all(
                     ["Roots Access", "Tropics Access", "Mesa Access",
                      "Alpine Access", "Caldera Access", "Kiln Access"], player))
    except KeyError:
        pass

    # Biome-locked badges (not in acquire_item_rules)
    # Badges with item requirements use the loot shuffle to determine biome access.
    # Badges without item requirements keep their vanilla biome access.
    for mesa_item in MESA_LOCATIONS:
        if mesa_item not in acquire_item_rules:
            try:
                if mesa_item == "Astronomy Badge" and item_sanity:
                    astro_biome = unlock_to_biome.get("Binoculars Unlock", 0)
                    set_rule(world.get_location(mesa_item),
                             _unlock_and_biome_rule("Binoculars Unlock", astro_biome))
                elif mesa_item == "Daredevil Badge" and item_sanity:
                    dare_biome = unlock_to_biome.get("Scout Cannon Unlock", 0)
                    set_rule(world.get_location(mesa_item),
                             _unlock_and_biome_rule("Scout Cannon Unlock", dare_biome))
                elif mesa_item == "Needlepoint Badge" and item_sanity:
                    needle_biome = unlock_to_biome.get("Cactus Unlock", 0)
                    set_rule(world.get_location(mesa_item),
                             _unlock_and_biome_rule("Cactus Unlock", needle_biome))
                elif mesa_item == "Needlepoint Badge":
                    needle_biome = unlock_to_biome.get("Cactus Unlock", 0)
                    set_rule(world.get_location(mesa_item), _biome_rule(needle_biome))
                else:
                    set_rule(world.get_location(mesa_item),
                             lambda state: state.has("Mesa Access", player))
            except KeyError:
                pass

    for alpine_item in ALPINE_LOCATIONS:
        if alpine_item not in acquire_item_rules:
            try:
                if alpine_item == "Animal Serenading Badge" and item_sanity:
                    serenade_unlocks = ["Bugle Unlock", "Scoutmaster's Bugle Unlock",
                                        "Bugle of Friendship Unlock"]
                    serenade_biome = min(unlock_to_biome.get(u, 0) for u in serenade_unlocks)
                    set_rule(world.get_location(alpine_item),
                             lambda state, lvl=serenade_biome:
                             (state.has("Bugle Unlock", player) or
                              state.has("Scoutmaster's Bugle Unlock", player) or
                              state.has("Bugle of Friendship Unlock", player)) and
                             state.has("Alpine Access", player) and
                             (lvl == 0 or state.has("Progressive Mountain", player, lvl)))
                else:
                    set_rule(world.get_location(alpine_item),
                             lambda state: state.has("Alpine Access", player))
            except KeyError:
                pass

    for roots_item in ROOTS_LOCATIONS:
        if roots_item not in acquire_item_rules:
            try:
                if roots_item == "Advanced Mycology Badge" and item_sanity:
                    adv_myc_unlocks = ["Red Shroomberry Unlock", "Blue Shroomberry Unlock",
                                       "Green Shroomberry Unlock", "Yellow Shroomberry Unlock",
                                       "Purple Shroomberry Unlock"]
                    adv_myc_biome = max(unlock_to_biome.get(u, 0) for u in adv_myc_unlocks)
                    set_rule(world.get_location(roots_item),
                             lambda state, lvl=adv_myc_biome:
                             state.has("Red Shroomberry Unlock", player) and
                             state.has("Blue Shroomberry Unlock", player) and
                             state.has("Green Shroomberry Unlock", player) and
                             state.has("Yellow Shroomberry Unlock", player) and
                             state.has("Purple Shroomberry Unlock", player) and
                             (lvl == 0 or state.has("Progressive Mountain", player, lvl)))
                else:
                    set_rule(world.get_location(roots_item),
                             lambda state: state.has("Roots Access", player))
            except KeyError:
                pass

    berry_unlocks = [
        "Red Crispberry Unlock", "Green Crispberry Unlock", "Yellow Crispberry Unlock",
        "Brown Berrynana Unlock", "Blue Berrynana Unlock", "Pink Berrynana Unlock", "Yellow Berrynana Unlock",
        "Orange Winterberry Unlock", "Yellow Winterberry Unlock",
        "Red Prickleberry Unlock", "Gold Prickleberry Unlock",
        "Red Shroomberry Unlock", "Blue Shroomberry Unlock", "Green Shroomberry Unlock",
        "Yellow Shroomberry Unlock", "Purple Shroomberry Unlock",
        "Purple Kingberry Unlock", "Yellow Kingberry Unlock", "Green Kingberry Unlock",
        "Napberry Unlock",
        "Black Clusterberry Unlock", "Red Clusterberry Unlock", "Yellow Clusterberry Unlock",
    ]

    # Foraging Badge - need 5 berries; biome = 5th-lowest biome level among all berries
    berry_biome_levels = sorted(unlock_to_biome.get(b, 0) for b in berry_unlocks)
    foraging_biome = berry_biome_levels[4] if len(berry_biome_levels) >= 5 else 0

    for tropics_item in TROPICS_LOCATIONS:
        if tropics_item not in acquire_item_rules:
            try:
                if tropics_item == "Foraging Badge" and item_sanity:
                    set_rule(world.get_location(tropics_item),
                             lambda state, lvl=foraging_biome:
                             sum(1 for b in berry_unlocks if state.has(b, player)) >= 5 and
                             (lvl == 0 or state.has("Progressive Mountain", player, lvl)))
                elif tropics_item == "Foraging Badge":
                    set_rule(world.get_location(tropics_item), _biome_rule(foraging_biome))
                else:
                    set_rule(world.get_location(tropics_item),
                             lambda state: state.has("Tropics Access", player))
            except KeyError:
                pass

    for caldera_item in CALDERA_LOCATIONS:
        if caldera_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(caldera_item),
                         lambda state: state.has("Caldera Access", player))
            except KeyError:
                pass

    for kiln_item in KILN_LOCATIONS:
        if kiln_item not in acquire_item_rules:
            try:
                if kiln_item == "24 Karat Badge" and item_sanity:
                    set_rule(world.get_location(kiln_item),
                             lambda state: state.has("Ancient Idol Unlock", player) and
                                           state.has("Kiln Access", player))
                elif kiln_item == "Bing Bong Badge" and item_sanity:
                    set_rule(world.get_location(kiln_item),
                             lambda state: state.has("Bing Bong Unlock", player) and
                                           state.has("Kiln Access", player))
                elif kiln_item == "Knot Tying Badge" and item_sanity:
                    knot_unlocks = ["Rope Spool Unlock", "Anti-Rope Spool Unlock",
                                    "Rope Cannon Unlock", "Anti-Rope Cannon Unlock"]
                    knot_biome = min(unlock_to_biome.get(u, 0) for u in knot_unlocks)
                    set_rule(world.get_location(kiln_item),
                             lambda state, lvl=knot_biome:
                             state.has("Kiln Access", player) and
                             (state.has("Rope Spool Unlock", player) or
                              state.has("Anti-Rope Spool Unlock", player) or
                              state.has("Rope Cannon Unlock", player) or
                              state.has("Anti-Rope Cannon Unlock", player)) and
                             (lvl == 0 or state.has("Progressive Mountain", player, lvl)))
                elif kiln_item == "Knot Tying Badge":
                    set_rule(world.get_location(kiln_item),
                             lambda state: state.has("Kiln Access", player))
                elif kiln_item == "Gourmand Badge" and item_sanity:
                    gourmand_unlocks = ["Coconut Unlock", "Honeycomb Unlock",
                                        "Yellow Winterberry Unlock", "Egg Unlock"]
                    gourmand_biome = max(unlock_to_biome.get(u, 0) for u in gourmand_unlocks)
                    set_rule(world.get_location(kiln_item),
                             lambda state, lvl=gourmand_biome:
                             state.has("Coconut Unlock", player) and
                             state.has("Honeycomb Unlock", player) and
                             state.has("Yellow Winterberry Unlock", player) and
                             state.has("Egg Unlock", player) and
                             (lvl == 0 or state.has("Progressive Mountain", player, lvl)))
                elif kiln_item == "Gourmand Badge":
                    gourmand_unlocks = ["Coconut Unlock", "Honeycomb Unlock",
                                        "Yellow Winterberry Unlock", "Egg Unlock"]
                    gourmand_biome = max(unlock_to_biome.get(u, 0) for u in gourmand_unlocks)
                    set_rule(world.get_location(kiln_item), _biome_rule(gourmand_biome))
                else:
                    set_rule(world.get_location(kiln_item),
                             lambda state: state.has("Kiln Access", player))
            except KeyError:
                pass

    # Ascent locations require their corresponding Ascent Completed events
    roman_numerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

    max_relevant_ascent = 8
    if "Reach Peak" in goals:
        max_relevant_ascent = required_ascent

    _amulet_chain_unlocks = [
        "Strange Gem Unlock", "Scout's Tenacity Unlock", "Scout's Generosity Unlock",
        "Scout's Ambition Unlock", "Scout's Initiative Unlock", "Scout's Honor Unlock",
    ]

    def _amulet_chain_rule(state):
        if progressive_amulets:
            return state.has("Progressive Amulet Unlock", player, 6)
        if item_sanity and scout_amulet_sanity:
            return state.has_all(_amulet_chain_unlocks, player)
        if item_sanity:
            return state.has("Strange Gem Unlock", player)
        return True

    def _ascent_rule_base(asc, with_stamina):
        if asc in [3, 4, 5]:
            if with_stamina:
                return lambda state, a=asc: (state.has("Kiln Access", player) and
                                             state.has("Progressive Ascent", player, a) and
                                             state.has("Progressive Stamina Bar", player, 3))
            return lambda state, a=asc: (state.has("Kiln Access", player) and
                                         state.has("Progressive Ascent", player, a))
        if asc in [6, 7, 8]:
            if with_stamina:
                return lambda state, a=asc: (state.has("Kiln Access", player) and
                                             state.has("Progressive Ascent", player, a) and
                                             state.has("Progressive Stamina Bar", player, 3) and
                                             state.has("Progressive Endurance", player, 4))
            return lambda state, a=asc: (state.has("Kiln Access", player) and
                                         state.has("Progressive Ascent", player, a) and
                                         state.has("Progressive Endurance", player, 4))
        return lambda state, a=asc: (state.has("Kiln Access", player) and
                                     state.has("Progressive Ascent", player, a))

    def _ascent_rule(asc, with_stamina):
        base = _ascent_rule_base(asc, with_stamina)
        if asc == 8:
            return lambda state, b=base: b(state) and _amulet_chain_rule(state)
        return base

    # Event locations for ascent completion
    for ascent_num in range(1, max_relevant_ascent + 1):
        try:
            set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                     _ascent_rule(ascent_num, progressive_stamina_enabled))
        except KeyError:
            pass

    # Ascent badge locations require Progressive Ascent
    for ascent_num in range(1, max_relevant_ascent + 1):
        roman_num = roman_numerals[ascent_num - 1]
        ascent_locations = [
            f"Beachcomber {roman_num} Badge (Ascent {ascent_num})",
            f"Trailblazer {roman_num} Badge (Ascent {ascent_num})",
            f"Alpinist {roman_num} Badge (Ascent {ascent_num})",
            f"Volcanology {roman_num} Badge (Ascent {ascent_num})",
            f"Nomad {roman_num} Badge (Ascent {ascent_num})",
            f"Forestry {roman_num} Badge (Ascent {ascent_num})",
            f"Wanderer {roman_num} Badge (Ascent {ascent_num})",
        ]

        for ascent_name in ascent_locations:
            try:
                set_rule(world.get_location(ascent_name),
                         _ascent_rule(ascent_num, progressive_stamina_enabled))
            except KeyError:
                pass

    # Freeing the Scoutmaster's soul needs Scout's Honor (the amulet chain) and Kiln access
    try:
        set_rule(world.get_location("Soul Freed"),
                 lambda state: state.has("Kiln Access", player) and _amulet_chain_rule(state))
    except KeyError:
        pass

    # Rule Zero Badge is awarded for winning a run through the Nadir,
    # which requires the Scoutmaster's Soul item to begin the climb
    try:
        set_rule(world.get_location("Rule Zero Badge"),
                 lambda state: state.has("Kiln Access", player) and
                               state.has("Scoutmaster's Soul", player) and
                               _amulet_chain_rule(state))
    except KeyError:
        pass

    # Scout sashes require completion of ALL previous ascents
    scout_sashe_requirements = {
        "Rabbit Scout sashe (Ascent 1)": ["Kiln Access"],
        "Raccoon Scout sashe (Ascent 2)": ["Ascent 1 Completed", "Kiln Access"],
        "Mule Scout sashe (Ascent 3)": ["Ascent 1 Completed", "Ascent 2 Completed", "Kiln Access"],
        "Kangaroo Scout sashe (Ascent 4)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                            "Kiln Access"],
        "Owl Scout sashe (Ascent 5)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                       "Ascent 4 Completed", "Kiln Access"],
        "Wolf Scout sashe (Ascent 6)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                        "Ascent 4 Completed", "Ascent 5 Completed", "Kiln Access"],
        "Goat Scout sashe (Ascent 7)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                        "Ascent 4 Completed", "Ascent 5 Completed", "Ascent 6 Completed", "Kiln Access"]
    }

    for scout_name, required_ascents in scout_sashe_requirements.items():
        try:
            if scout_name == "Rabbit Scout sashe (Ascent 1)":
                set_rule(world.get_location(scout_name),
                         lambda state: state.has("Progressive Ascent", player, 1) and
                         state.has("Progressive Mountain", player, 4))
            else:
                import re
                match = re.search(r'\(Ascent (\d+)\)', scout_name)
                if match:
                    scout_ascent = int(match.group(1))
                    if scout_ascent in [1, 2]:
                        set_rule(world.get_location(scout_name),
                                 lambda state, reqs=required_ascents, asc=scout_ascent:
                                 all(state.has(ascent, player) for ascent in reqs) and
                                 state.has("Progressive Ascent", player, asc) and
                                 state.has("Progressive Mountain", player, 4))
                    elif scout_ascent in [3, 4, 5]:
                        set_rule(world.get_location(scout_name),
                                 lambda state, reqs=required_ascents, asc=scout_ascent, stam=progressive_stamina_enabled:
                                 all(state.has(ascent, player) for ascent in reqs) and
                                 state.has("Progressive Ascent", player, asc) and
                                 state.has("Progressive Mountain", player, 4) and
                                 (not stam or state.has("Progressive Stamina Bar", player, 3)))
                    elif scout_ascent in [6, 7]:
                        set_rule(world.get_location(scout_name),
                                 lambda state, reqs=required_ascents, asc=scout_ascent, stam=progressive_stamina_enabled:
                                 all(state.has(ascent, player) for ascent in reqs) and
                                 state.has("Progressive Ascent", player, asc) and
                                 state.has("Progressive Mountain", player, 4) and
                                 (not stam or state.has("Progressive Stamina Bar", player, 3)) and
                                 state.has("Progressive Endurance", player, 4))
        except KeyError:
            pass