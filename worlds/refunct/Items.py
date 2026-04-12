import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class RefunctItem(Item):
    game: str = "Refunct"
    button_nr: int


item_table = {f"Cluster {i}": ItemData(10000000 + i, ItemClassification.progression) for i in range(1, 32)}
item_table["Grass"] = ItemData(9999999, ItemClassification.progression_deprioritized_skip_balancing) 
item_table["Starting Platform"] = ItemData(9999998, ItemClassification.filler) 
item_table["Goal Location"] = ItemData(9999997, ItemClassification.progression)
item_table[":)"] = ItemData(9999996, ItemClassification.filler)

item_table["Ledge Grab"] = ItemData(9999990, ItemClassification.progression | ItemClassification.useful)
item_table["Progressive Wall Jump"] = ItemData(9999991, ItemClassification.progression | ItemClassification.useful)
item_table["Swim"] = ItemData(9999992, ItemClassification.progression | ItemClassification.useful)
item_table["Jump Pads"] = ItemData(9999993, ItemClassification.progression)
item_table["Pipes"] = ItemData(9999994, ItemClassification.progression)
item_table["Lifts"] = ItemData(9999995, ItemClassification.progression)

item_table["Red Cubes Bag"] = ItemData(9999989, ItemClassification.progression)
item_table["Green Cubes Bag"] = ItemData(9999988, ItemClassification.progression)
item_table["Blue Cubes Bag"] = ItemData(9999987, ItemClassification.progression)

item_table["Flower"] = ItemData(9999981, ItemClassification.filler)

item_table["Vanilla Minigame"] = ItemData(9999980, ItemClassification.progression)
item_table["Seeker Minigame"] = ItemData(9999970, ItemClassification.progression)
item_table["Button Galore Minigame"] = ItemData(9999960, ItemClassification.progression)
item_table["OG Randomizer Minigame"] = ItemData(9999950, ItemClassification.progression)

item_table["Block Brawl Minigame Reds"] = ItemData(9999941, ItemClassification.progression)
item_table["Block Brawl Minigame Blues"] = ItemData(9999942, ItemClassification.progression)
item_table["Block Brawl Minigame Greens"] = ItemData(9999943, ItemClassification.progression)
item_table["Block Brawl Minigame Yellows"] = ItemData(9999944, ItemClassification.progression)

item_table["Climb Line Minigame"] = ItemData(9999931, ItemClassification.progression)
item_table["Climb Spiral Minigame"] = ItemData(9999932, ItemClassification.progression)
item_table["Climb Chaos Minigame"] = ItemData(9999933, ItemClassification.progression)

item_table["Block Blub Minigame Reds"] = ItemData(9999921, ItemClassification.progression)
item_table["Block Blub Minigame Blues"] = ItemData(9999922, ItemClassification.progression)
item_table["Block Blub Minigame Greens"] = ItemData(9999923, ItemClassification.progression)
item_table["Block Blub Minigame Yellows"] = ItemData(9999924, ItemClassification.progression)

item_table["Refunct Mountain Minigame"] = ItemData(9999910, ItemClassification.progression)

# for i in range(0, 101):
#     item_table[f"DEBUGA {i}"] = ItemData(20000000 + i, ItemClassification.filler)
#     item_table[f"DEBUGB {i}"] = ItemData(30000000 + i, ItemClassification.filler)
#     item_table[f"DEBUGC {i}"] = ItemData(40000000 + i, ItemClassification.filler)
#     item_table[f"DEBUGD {i}"] = ItemData(50000000 + i, ItemClassification.filler)
# item_table[f"Disable Wall Ledge"] = ItemData(60000000, ItemClassification.filler)
# item_table[f"Enable One Wall"] = ItemData(60000001, ItemClassification.filler)
# item_table[f"Disable Swim"] = ItemData(60000005, ItemClassification.filler)
# item_table[f"Disable Jumppads"] = ItemData(60000010, ItemClassification.filler)
# item_table[f"DEBUG Goal"] = ItemData(60000015, ItemClassification.filler)

item_table[f"Dark skies"] = ItemData(9999001, ItemClassification.trap)
item_table[f"No skylight"] = ItemData(9999002, ItemClassification.trap)
item_table[f"Slo-mo"] = ItemData(9999003, ItemClassification.trap)
item_table[f"Fast-mo"] = ItemData(9999004, ItemClassification.trap)
# item_table[f"Disco sky"] = ItemData(9999005, ItemClassification.trap)
item_table[f"Starry sky"] = ItemData(9999006, ItemClassification.trap)
item_table[f"Red sky"] = ItemData(9999007, ItemClassification.trap)
item_table[f"Hurricane"] = ItemData(9999008, ItemClassification.trap)
item_table[f"Blurrrrgh"] = ItemData(9999009, ItemClassification.trap)

item_groups = {
    "Block Brawl Cubes": {
        "Block Brawl Minigame Reds",
        "Block Brawl Minigame Blues",
        "Block Brawl Minigame Greens",
        "Block Brawl Minigame Yellows",
    },
    "Block Blub Cubes": {
        "Block Blub Minigame Reds",
        "Block Blub Minigame Blues",
        "Block Blub Minigame Greens",
        "Block Blub Minigame Yellows",
    },
    "Cubes Bags": {
        "Red Cubes Bag",
        "Green Cubes Bag",
        "Blue Cubes Bag",
    },
    "Clusters": {
        f"Cluster {i}" for i in range(1, 31) 
    },
    "Minigames": {
        "Vanilla Minigame",
        "Seeker Minigame",
        "Button Galore Minigame",
        "OG Randomizer Minigame",
        "Block Brawl Minigame Reds",
        "Block Brawl Minigame Blues",
        "Block Brawl Minigame Greens",
        "Block Brawl Minigame Yellows",
        "Climb Line Minigame",
        "Climb Spiral Minigame",
        "Climb Chaos Minigame",
        "Block Blub Minigame Reds",
        "Block Blub Minigame Blues",
        "Block Blub Minigame Greens",
        "Block Blub Minigame Yellows",
    },
    "Abilities": {
        "Ledge Grab",
        "Progressive Wall Jump",
        "Swim",
        "Jump Pads",
        "Pipes",
        "Lifts",
    },
}
