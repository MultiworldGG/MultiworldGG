from enum import Enum

from BaseClasses import Item, ItemClassification


class AgainstTheStormItem(Item):
    game: str = "Against the Storm"

class ATSItemClassification(Enum):
    good = 1
    blueprint = 2
    filler = 3
    guardian_part = 4
    keepers_dlc_blueprint = 5
    biome_key = 6
    keepers_dlc_biome_key = 7
    nightwatchers_dlc_biome_key = 8

item_dict: dict[str, tuple[ItemClassification, ATSItemClassification, str | None]] = {
    "Guardian Heart": (ItemClassification.progression, ATSItemClassification.guardian_part, "Guardian Part"),
    "Guardian Blood": (ItemClassification.progression, ATSItemClassification.guardian_part, "Guardian Part"),
    "Guardian Feathers": (ItemClassification.progression, ATSItemClassification.guardian_part, "Guardian Part"),
    "Guardian Essence": (ItemClassification.progression, ATSItemClassification.guardian_part, "Guardian Part"),

    "Berries": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Eggs": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Insects": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Meat": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Mushrooms": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Roots": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Vegetables": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Fish": (ItemClassification.progression, ATSItemClassification.good, "Raw Food"),
    "Biscuits": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Jerky": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Pickled Goods": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Pie": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Porridge": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Skewers": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Paste": (ItemClassification.progression, ATSItemClassification.good, "Complex Food"),
    "Coats": (ItemClassification.progression, ATSItemClassification.good, "Clothing"),
    "Boots": (ItemClassification.progression, ATSItemClassification.good, "Clothing"),
    "Bricks": (ItemClassification.progression, ATSItemClassification.good, "Building Material"),
    "Fabric": (ItemClassification.progression, ATSItemClassification.good, "Building Material"),
    "Planks": (ItemClassification.progression, ATSItemClassification.good, "Building Material"),
    "Pipes": (ItemClassification.progression, ATSItemClassification.good, None),
    "Parts": (ItemClassification.progression, ATSItemClassification.good, None),
    "Wildfire Essence": (ItemClassification.useful, ATSItemClassification.good, None),
    "Ale": (ItemClassification.progression, ATSItemClassification.good, "Service Good"),
    "Incense": (ItemClassification.progression, ATSItemClassification.good, "Service Good"),
    "Scrolls": (ItemClassification.progression, ATSItemClassification.good, "Service Good"),
    "Tea": (ItemClassification.progression, ATSItemClassification.good, "Service Good"),
    "Training Gear": (ItemClassification.progression, ATSItemClassification.good, "Service Good"),
    "Wine": (ItemClassification.progression, ATSItemClassification.good, "Service Good"),
    "Clay": (ItemClassification.progression, ATSItemClassification.good, None),
    "Copper Ore": (ItemClassification.progression, ATSItemClassification.good, None),
    "Scales": (ItemClassification.progression, ATSItemClassification.good, None),
    "Crystallized Dew": (ItemClassification.progression, ATSItemClassification.good, "Metal"),
    "Grain": (ItemClassification.progression, ATSItemClassification.good, None),
    "Herbs": (ItemClassification.progression, ATSItemClassification.good, None),
    "Leather": (ItemClassification.progression, ATSItemClassification.good, None),
    "Plant Fiber": (ItemClassification.progression, ATSItemClassification.good, None),
    "Algae": (ItemClassification.progression, ATSItemClassification.good, None),
    "Reeds": (ItemClassification.progression, ATSItemClassification.good, None),
    "Resin": (ItemClassification.progression, ATSItemClassification.good, None),
    "Stone": (ItemClassification.progression, ATSItemClassification.good, None),
    "Salt": (ItemClassification.progression, ATSItemClassification.good, None),
    "Barrels": (ItemClassification.progression, ATSItemClassification.good, "Container"),
    "Copper Bars": (ItemClassification.progression, ATSItemClassification.good, "Metal"),
    "Flour": (ItemClassification.progression, ATSItemClassification.good, None),
    "Dye": (ItemClassification.progression, ATSItemClassification.good, None),
    "Pottery": (ItemClassification.progression, ATSItemClassification.good, "Container"),
    "Waterskins": (ItemClassification.progression, ATSItemClassification.good, "Container"),
    "Amber": (ItemClassification.progression, ATSItemClassification.good, None),
    "Pack of Building Materials": (ItemClassification.progression, ATSItemClassification.good, "Pack"),
    "Pack of Crops": (ItemClassification.progression, ATSItemClassification.good, "Pack"),
    "Pack of Luxury Goods": (ItemClassification.progression, ATSItemClassification.good, "Pack"),
    "Pack of Provisions": (ItemClassification.progression, ATSItemClassification.good, "Pack"),
    "Pack of Trade Goods": (ItemClassification.progression, ATSItemClassification.good, "Pack"),
    "Ancient Tablet": (ItemClassification.progression, ATSItemClassification.good, None),
    "Coal": (ItemClassification.progression, ATSItemClassification.good, "Fuel"),
    "Oil": (ItemClassification.progression, ATSItemClassification.good, "Fuel"),
    "Purging Fire": (ItemClassification.progression, ATSItemClassification.good, None),
    "Sea Marrow": (ItemClassification.progression, ATSItemClassification.good, "Fuel"),
    "Tools": (ItemClassification.progression, ATSItemClassification.good, None),

    "2 Starting Villagers": (ItemClassification.filler, ATSItemClassification.filler, None),
    "15 Starting Crystallized Dew": (ItemClassification.filler, ATSItemClassification.filler, None),
    "20 Starting Amber": (ItemClassification.filler, ATSItemClassification.filler, None),
    "6 Starting Parts": (ItemClassification.filler, ATSItemClassification.filler, None),
    "3 Starting Wildfire Essence": (ItemClassification.filler, ATSItemClassification.filler, None),
    "20 Starting Pipes": (ItemClassification.filler, ATSItemClassification.filler, None),
    "30 Starting Sea Marrow": (ItemClassification.filler, ATSItemClassification.filler, None),
    "30 Starting Oil": (ItemClassification.filler, ATSItemClassification.filler, None),
    "30 Starting Grain": (ItemClassification.filler, ATSItemClassification.filler, None),
    "15 Starting Pack of Provisions": (ItemClassification.filler, ATSItemClassification.filler, None),
    "25 Starting Mushrooms": (ItemClassification.filler, ATSItemClassification.filler, None),
    "40 Starting Insects": (ItemClassification.filler, ATSItemClassification.filler, None),
    "20 Starting Vegetables": (ItemClassification.filler, ATSItemClassification.filler, None),
    "20 Starting Stone": (ItemClassification.filler, ATSItemClassification.filler, None),
    "10 Starting Planks": (ItemClassification.filler, ATSItemClassification.filler, None),
    "10 Starting Tools": (ItemClassification.filler, ATSItemClassification.filler, None),
    "Survivor Bonding": (ItemClassification.filler, ATSItemClassification.filler, None),

    "Forager's Camp": (ItemClassification.progression, ATSItemClassification.blueprint, "Gathering Blueprint"),
    "Herbalist's Camp": (ItemClassification.progression, ATSItemClassification.blueprint, "Gathering Blueprint"),
    "Trapper's Camp": (ItemClassification.progression, ATSItemClassification.blueprint, "Gathering Blueprint"),
    "Fishing Hut": (ItemClassification.useful, ATSItemClassification.blueprint, "Gathering Blueprint"),
    "Clay Pit": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Forester's Hut": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Greenhouse": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Herb Garden": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Brineworks": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Plantation": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Small Farm": (ItemClassification.useful, ATSItemClassification.blueprint, "Fertile Soil Blueprint"),
    "Advanced Rain Collector": (ItemClassification.useful, ATSItemClassification.blueprint, None),
    "Bakery": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Beanery": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Brick Oven": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Butcher": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Cellar": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Cookhouse": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Granary": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Grill": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Ranch": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Smokehouse": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Alchemist's Hut": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Apothecary": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Artisan": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Brewery": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Brickyard": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Carpenter": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Clothier": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Cooperage": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Distillery": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Druid's Hut": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Furnace": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Kiln": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Leatherworker": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Lumber Mill": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Manufactory": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Press": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Provisioner": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Rain Mill": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Scribe": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Smelter": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Smithy": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Stamping Mill": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Supplier": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Teahouse": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Tinctury": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Tinkerer": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Toolshop": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Weaver": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Workshop": (ItemClassification.progression, ATSItemClassification.blueprint, None),
    "Cobbler": (ItemClassification.progression, ATSItemClassification.blueprint, None),

    "Pantry": (ItemClassification.progression, ATSItemClassification.keepers_dlc_blueprint, None),
    "Cannery": (ItemClassification.progression, ATSItemClassification.keepers_dlc_blueprint, None),

    "Bath House": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Clan Hall": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Academy": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Guild House": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Market": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Monastery": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Tavern": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Tea Doctor": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),
    "Temple": (ItemClassification.progression, ATSItemClassification.blueprint, "Service Blueprint"),

    "Forum": (ItemClassification.progression, ATSItemClassification.keepers_dlc_blueprint, "Service Blueprint"),

    "Royal Woodlands": (ItemClassification.progression, ATSItemClassification.biome_key, "Biome Key"),
    "Coral Forest": (ItemClassification.progression, ATSItemClassification.biome_key, "Biome Key"),
    "The Marshlands": (ItemClassification.progression, ATSItemClassification.biome_key, "Biome Key"),
    "Scarlet Orchard": (ItemClassification.progression, ATSItemClassification.biome_key, "Biome Key"),
    "Cursed Royal Woodlands": (ItemClassification.progression, ATSItemClassification.biome_key, "Biome Key"),
    "Coastal Grove": (ItemClassification.progression, ATSItemClassification.keepers_dlc_biome_key, "Biome Key"),
    "Ashen Thicket": (ItemClassification.progression, ATSItemClassification.keepers_dlc_biome_key, "Biome Key"),
    "Bamboo Flats": (ItemClassification.progression, ATSItemClassification.nightwatchers_dlc_biome_key, "Biome Key"),
    "Rocky Ravine": (ItemClassification.progression, ATSItemClassification.nightwatchers_dlc_biome_key, "Biome Key"),
    "Sealed Forest": (ItemClassification.progression, ATSItemClassification.biome_key, "Biome Key"),
}

def get_item_name_groups(item_dict: dict[str, tuple[ItemClassification, ATSItemClassification, str | None]]):
    item_groups: dict[str, set[str]] = {}
    for item_key, (_ap_classification, _classification, item_group) in item_dict.items():
        if item_group is None:
            continue

        if item_group in item_groups:
            item_groups[item_group].add(item_key)
        else:
            item_groups[item_group] = { item_key }

    return item_groups
