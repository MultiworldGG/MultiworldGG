from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import CanReachRegion, Has, HasFromList, Rule

from .items import ITEM_NAME_TO_ID
from .locations import LOCATION_NAME_TO_ID


if TYPE_CHECKING:
    from .world import FuniRaccoonWorld


@dataclass
class OutOfLogic(Rule["FuniRaccoonWorld"], game="Funi Raccoon Game"):
    description: str

    class Resolved(Rule.Resolved):
        glitches_item_name: str
        player: int
        description: str
        skip_cache = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(self.glitches_item_name, self.player)

        @override
        def item_dependencies(self):
            yield self.glitches_item_name, self.player

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [{"text": f"Glitch: {self.description}", "color": "magenta"}]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            return f"Glitch: {self.description}"

    @override
    def _instantiate(self, world: "FuniRaccoonWorld") -> "OutOfLogic.Resolved":
        return OutOfLogic.Resolved(
            glitches_item_name=world.glitches_item_name,
            player=world.player,
            description=self.description,
        )

# Items that have a "Store X" dumpster location. Store location IDs follow the pattern
# location_id == item_id + 1000, so this excludes Euros, strength upgrades, truck
# upgrades, and anything else that isn't deposited at the dumpster.
_STORE_LOCATION_IDS = {loc_id for loc_id in LOCATION_NAME_TO_ID.values() if 1001 <= loc_id <= 1999}
DUMPSTER_ITEMS = [
    name for name, item_id in ITEM_NAME_TO_ID.items()
    if (item_id + 1000) in _STORE_LOCATION_IDS
]
# The Kei Truck has no "Store Kei Truck" location but still counts toward the
# dumpster item score in-game.
DUMPSTER_ITEMS.append("Kei Truck")

# Store locations in regions where the Kei Truck is accessible — weight requirements
# don't apply OOL because the truck can carry heavy items.
_KT_DUMBBELL_LOCATIONS: frozenset[str] = frozenset({
    # Trasco Carpark (reachable via Blimbo Village with truck)
    "Store Trolley", "Store Coffee Shop (closed)", "Store CD Player", "Store Patrice",
    "Store Fridge", "Store Trasco Sign"
    # Fridge World
    "Store Milk Klubnika",
    # Blimbo Village
    "Store Blimbo Village Sign", "Store Gas Drum", 'Store "Cow"',
    "Store CHEESE", "Store Door", "Store Fone", "Store Ougham Stone",
    # Petrol Station
    "Store Gas Pumpo", "Store Police Car", "Store Knifedog",
    # Bildal Mines
    "Store Pickaxe",
    # Purgatory
    "Store My Favourite Chair",
    # Blimbo City
    "Store Coffee Cup", "Store Radiator", "Store Bin", "Store Suitcase", "Store Bell Boy", "Store Blimbo City Sign",
    # Pub
    "Store Cheeky Pint",
    # BLMB Reactor Core
    "Store Demon Core",
    # Garden World
    "Store Radio Blimbo", "Store Flowian",
    # The Forest
    "Store Eel Can",
    # Messed Up Canyon
    "Store BookBlo",
    # Pharmacy
    "Store Leeches!", "Store Anti Sads",
    # The Desert
    "Store Fridgling",
    # Municipal Wastes
    "Store Chairapist", "Store Real Gym", "Store Dumbbell",
    # The Gully
    "Store Belgium Waffle",
})

# Progressive Mystical Dumbbell requirements per store location.
# TINY (weight 1) items have no requirement and are omitted.
# SMALL=1, MEDIUM=2, HEAVY=3, CHUNKY=4.
_DUMBBELL_REQUIREMENTS: dict[str, int] = {
    # SMALL (weight 2) — requires 1 dumbbell
    "Store Dumbbell":                            1,
    "Store Vending Machine (accepts doubloons)": 1,
    "Store Washing Machine":                     1,
    "Store Paracetamol 650mg":                   1,
    "Store Heavy Stone Torch":                   1,
    "Store Sign":                                1,
    "Store Pirate":                              1,
    "Store Pirate 2":                            1,
    "Store Pirate 3":                            1,
    "Store Feral Dog":                           1,
    "Store Buisness Man":                        1,
    "Store Beenie, Our Savior":                  1,
    "Store Crisp":                               1,
    "Store My Favourite Chair":                  1,
    "Store Blimbo Village Sign":                 1,
    "Store Papa Tyre":                           1,
    "Store Broken Truck":                        1,
    "Store CHEESE":                              1,
    "Store Trolley":                             1,
    "Store Folding Chair":                       1,
    "Store Pickaxe":                             1,
    "Store Fone":                                1,
    "Store Coffee Cup":                          1,
    "Store Cheeky Pint":                         1,
    "Store CD Player":                           1,
    "Store Anti Sads":                           1,
    "Store Old Sign":                            1,
    "Store Warning Sign":                        1,
    "Store Priestess":                           1,
    "Store Beenie Saves The Orphans":            1,
    "Store Milk Klubnika":                       1,
    "Store Wriks Celler":                        1,
    "Store Door":                                1,
    "Store Goo Container":                       1,
    "Store Cheese Wife":                         1,
    # MEDIUM (weight 3) — requires 2 Dumbbell
    "Store Crack Head":                          2,
    "Store Patrick O'Hara":                      2,
    "Store Microwave":                           2,
    "Store Crisps Undying Love":                 2,
    'Store "Cow"':                               2,
    "Store Gas Drum":                            2,
    "Store Smoker":                              2,
    "Store Radiator":                            2,
    "Store Bench":                               2,
    "Store Bin":                                 2,
    "Store Knifedog":                            2,
    "Store Suitcase":                            2,
    "Store Flowian":                             2,
    "Store Bell Boy":                            2,
    "Store Demon Core":                          2,
    "Store Gas Pumpo":                           2,
    "Store Radio Blimbo":                        2,
    "Store Manhole Cover":                       2,
    "Store Eel Can":                             2,
    "Store Barrel":                              2,
    "Store BookBlo":                             2,
    "Store Fridge":                              2,
    "Store Fridgling":                           2,
    "Store Leeches!":                            2,
    "Store Chairapist":                          2,
    "Store Real Gym":                            2,
    "Store Patrice":                             2,
    "Store Office Chair":                        2,
    "Store Desk":                                2,
    # HEAVY (weight 4) — requires 3 Dumbbell
    "Store Windmill":                            3,
    "Store Ougham Stone":                        3,
    "Store Coffee Shop (closed)":                3,
    "Store Police Car":                          3,
    "Store Trasco Sign":                         3,
    "Store Mikk Masive Sign":                    3,
    # CHUNKY (weight 5) — requires all 4 Dumbbell
    "Store Gym":                                 4,
    "Store Belgium Waffle":                      4,
    "Store Friend Martin Friendship Statue":     4,
    "Store Blimbo City Sign":                    4,
}


def items(count: int) -> HasFromList:
    """Rule: player has deposited at least `count` collectible items."""
    return HasFromList(*DUMPSTER_ITEMS, count=count)


def _goal_rule(world: FuniRaccoonWorld):
    goals = world.options.goal.value
    rules = []
    if "orb" in goals:
        rules.append(Has("Progressive Cooling Rod", 3) & Has("Orb") & Has("Kei Truck") & items(world.options.act4_threshold.value))
    if "museum" in goals:
        rules.append(Has("Progressive Cooling Rod", 3) & Has("Belgium Waffle") & Has("Kei Truck") & Has("Progressive Mystical Dumbbell", 4) & items(100))
    if "fellowship" in goals:
        rules.append(Has("Priestess") & Has("GREENISH ABOMINATION") & Has("Kei Truck") & Has("Progressive Cooling Rod", 3) & items(world.options.act4_threshold.value))
    if "lugh" in goals:
        rules.append(Has("Green Mystical Gem") & Has("Blue Mystical Gem") & Has("Purple Mystical Gem") & Has("Red Mystical Gem") & Has("Kei Truck") & items(world.options.act4_threshold.value))
    if not rules:
        return Has("Progressive Cooling Rod", 3) & Has("Orb") & Has("Kei Truck") & items(world.options.act4_threshold.value)
    result = rules[0]
    for r in rules[1:]:
        result = result | r
    return result


def set_all_rules(world: FuniRaccoonWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: FuniRaccoonWorld) -> None:
    def rule(name: str, r) -> None:
        try:
            world.set_rule(world.get_location(name), r)
        except KeyError:
            return

    rule("Victory", _goal_rule(world))

    # Dumbbell size rules for store locations (TINY items have no requirement).
    # When dumpster_weight_blocking is disabled, having the Kei Truck is in-logic as an
    # alternative to dumbbells, but only for regions that require the truck to reach.
    # When enabled, weight is strictly enforced everywhere.
    weight_blocking = world.options.dumpster_weight_blocking.value
    for loc_name, count in _DUMBBELL_REQUIREMENTS.items():
        r = Has("Progressive Mystical Dumbbell", count)
        if loc_name in _KT_DUMBBELL_LOCATIONS and not weight_blocking:
            r |= Has("Kei Truck")
        rule(loc_name, r)

    # Store Fridge sits in Trasco Carpark but is also reachable by taking the train
    # to Brazil. It's hosted in Raccoon Central Station (always open), so gate it on
    # reaching either area, on top of its weight rule.
    _fridge = Has("Progressive Mystical Dumbbell", _DUMBBELL_REQUIREMENTS["Store Fridge"])
    if "Store Fridge" in _KT_DUMBBELL_LOCATIONS and not weight_blocking:
        _fridge |= Has("Kei Truck")
    rule("Store Fridge", _fridge & (CanReachRegion("Trasco Carpark") | CanReachRegion("Brazil")))

    # Store Windmill sits in Fields but is also storable from Blimbo Village once
    # Act 3 is open. It's hosted in Beenie HQ (no Goo gate), so gate it on reaching
    # either area, on top of its weight rule.
    rule("Store Windmill",
         Has("Progressive Mystical Dumbbell", _DUMBBELL_REQUIREMENTS["Store Windmill"])
         & (CanReachRegion("Fields") | CanReachRegion("Blimbo Village")))

    # Crack Head normally needs 2 dumbbells, but breaking him lets you store him early
    rule("Store Crack Head",
         Has("Progressive Mystical Dumbbell", _DUMBBELL_REQUIREMENTS["Store Crack Head"])
         | OutOfLogic("Crack Head can be broken and stored without dumbbells"))

    # Bell Boy additionally requires the Kei Truck Toaster (on top of its weight rule)
    _bell_boy = Has("Progressive Mystical Dumbbell", _DUMBBELL_REQUIREMENTS["Store Bell Boy"])
    if "Store Bell Boy" in _KT_DUMBBELL_LOCATIONS and not weight_blocking:
        _bell_boy |= Has("Kei Truck")
    rule("Store Bell Boy", _bell_boy & HasFromList("Kei Truck Toaster", "Kei Truck Boost", count=1))

    # Within Billdal Mines, boingler and Broken Wall also require the Pickaxe
    rule("Store boingler Cat",   Has("Pickaxe"))
    rule("Store Broken Wall", Has("Pickaxe"))

    # You need Beenie HQ access to store Michi Cat
    rule("Store Michi Cat", items(world.options.act2_threshold.value))

    # Gym Euro at end of train tracks requires Brob Energy; OOL sphere 1
    rule("Gym: Euro at end of train tracks",
         (Has("Brob Energy")) | OutOfLogic("Accessible without items"))

    # Behrman Speedway: normal logic needs Brob Energy + 4 Dumbbell; OOL just needs Brob Energy
    rule("Complete Behrman Speedway in under 1 minute",
         (Has("Brob Energy") & Has("Progressive Mystical Dumbbell", 4))
         | (Has("Brob Energy") & OutOfLogic("Speedway accessible with only Brob Energy")))
    
    # Patrick O'Hara requires Goo (inner Beenie HQ path) or Kei Truck + Blimbo Village access
    rule("Store Patrick O'Hara",
         Has("Progressive Mystical Dumbbell", 2) & (Has("Goo") | (items(world.options.act3_threshold.value) & Has("Kei Truck"))))

    # Evil Fish is out of logic before Goo; normal logic requires Goo to store it
    rule("Store Evil Fish", Has("Goo") | OutOfLogic("Evil Fish storable without Goo"))

    # Funi Marketable Plushie requires Goo to reach
    rule("Store Funi Marketable Plushie", Has("Goo"))

    # Chicken Farm items require Chicken to collect (the Norwich euro in that region does not)
    rule("Store Chicken",              Has("Chicken"))
    rule("Find Sombrero",              Has("Chicken"))
    rule("Chicken Farm: Euro on pillar", Has("Chicken"))

    # Lughling requires Butterfly
    rule("Store Lughling", Has("Butterfly"))

    # Act 4 is required for Funi Raccoon Game Deluxe
    rule("Store Funi Raccoon Game Deluxe",
         Has("Kei Truck") & Has("Progressive Cooling Rod", 1) & items(world.options.act4_threshold.value))

    # Gem Dumbbell Requirements
    rule("Eat Green Mystical Gem", Has("Progressive Mystical Dumbbell", 1))
    rule("Eat Blue Mystical Gem",  Has("Progressive Mystical Dumbbell", 2))

    # Higher Kei Truck scores require at least one truck upgrade
    _truck_upgrade = HasFromList("Kei Truck Boost", "Kei Truck Toaster", count=1) & Has("Kei Truck")
    for score_check in ("Get 2000 Score with Kei Truck", "Get 3000 Score with Kei Truck",
                        "Get 4000 Score with Kei Truck", "Get 5000 Score with Kei Truck"):
        rule(score_check, _truck_upgrade)


def set_completion_condition(world: FuniRaccoonWorld) -> None:
    world.set_completion_rule(_goal_rule(world))
