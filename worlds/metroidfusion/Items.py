from BaseClasses import ItemClassification
from .data.items import all_item_data, events


class ItemData:
    name: str
    classification: ItemClassification
    groups: list[str]
    mars_id: int

    def __init__(self, name: str, classification: ItemClassification, groups: list[str], mars_id: int):
        self.name = name
        self.classification = classification
        self.groups = groups
        self.mars_id = mars_id

    def to_json(self):
        return {
            "name": self.name,
            "mars_id": self.mars_id
        }

    def __repr__(self):
        return self.name

item_table: dict[str, ItemData] = dict()

for item in all_item_data:
    item_table[item[0]] = ItemData(item[0], item[1], item[2], item[3])

item_names = [item for item in item_table.keys()]
placeholder_names: set[str] = {"False Requirement Flag",
                               "Wall Jump Boots",
                               "Point of No Return",
                               "Wall Jump Trick - Beginner",
                               "Wall Jump Trick - Advanced",
                               "Wall Jump Trick - Expert",
                               "Shinespark Trick - Beginner",
                               "Shinespark Trick - Advanced",
                               "Shinespark Trick - Expert",
                               "Combat - Advanced",
                               "Combat - Expert"}

valid_item_names = [*item_names, *[event[3] for event in events], *placeholder_names]

# Everything not listed here has a quantity of one
default_item_quantities = {
    "Nothing": 0,
    "Level 0 Keycard": 0,
    "Missile Tank": 48,
    "Energy Tank": 20,
    "Power Bomb Tank": 36,
    "Ice Trap": 0,
    "Infant Metroid": 0
}

major_upgrades = [
    "Missile Data",
    "Morph Ball",
    "Charge Beam",
    "Bomb Data",
    "Hi-Jump",
    "Speed Booster",
    "Level 1 Keycard",
    "Level 2 Keycard",
    "Level 3 Keycard",
    "Level 4 Keycard",
    "Super Missile",
    "Varia Suit",
    "Ice Missile",
    "Wide Beam",
    "Power Bomb Data",
    "Space Jump",
    "Plasma Beam",
    "Gravity Suit",
    "Diffusion Missile",
    "Wave Beam",
    "Screw Attack",
    "Ice Beam"
]

major_jingles = [
    *major_upgrades,
    "Infant Metroid"
]

ap_name_to_mars_name = {
    "Nothing": "NONE",
    "Level 0 Keycard": "LEVEL_0",
    "Missile Data": "MISSILES",
    "Morph Ball": "MORPH_BALL",
    "Charge Beam": "CHARGE_BEAM",
    "Level 1 Keycard": "LEVEL_1",
    "Bomb Data": "BOMBS",
    "Hi-Jump": "HI_JUMP",
    "Speed Booster": "SPEED_BOOSTER",
    "Level 2 Keycard": "LEVEL_2",
    "Super Missile": "SUPER_MISSILES",
    "Varia Suit": "VARIA_SUIT",
    "Level 3 Keycard": "LEVEL_3",
    "Ice Missile": "ICE_MISSILES",
    "Wide Beam": "WIDE_BEAM",
    "Power Bomb Data": "POWER_BOMBS",
    "Space Jump": "SPACE_JUMP",
    "Plasma Beam": "PLASMA_BEAM",
    "Gravity Suit": "GRAVITY_SUIT",
    "Level 4 Keycard": "LEVEL_4",
    "Diffusion Missile": "DIFFUSION_MISSILES",
    "Wave Beam": "WAVE_BEAM",
    "Screw Attack": "SCREW_ATTACK",
    "Ice Beam": "ICE_BEAM",
    "Missile Tank": "MISSILE_TANK",
    "Energy Tank": "ENERGY_TANK",
    "Power Bomb Tank": "POWER_BOMB_TANK",
    "Ice Trap": "ICE_TRAP",
    "Infant Metroid": "INFANT_METROID"
}

mars_name_to_ap_name = {v: k for k, v in ap_name_to_mars_name.items()}