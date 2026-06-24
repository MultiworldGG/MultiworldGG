from typing import NamedTuple
from . import items

TAG_ITEM_BOX = "Item Box"
TAG_ITEM_BOX_INTERESTING = "*Interesting Item Box"
TAG_ITEM_BOX_GROUP = "*Item Box Group"
TAG_ITEM_BOX_SANITY = "*Boxsanity Item Box"
TAG_ITEM_BOX_CUSTOM = "*Custom Item Box"
TAG_ITEM_BOX_REPLACEABLE = "*Replaceable Item Box"

class ItemBoxGroup(NamedTuple):
    name: str
    count: int
    tags: set[str] = set()
    required_items: dict[str, int] = {}

BOX_NAMES: dict[str, list[ItemBoxGroup]] = {
    "Luigi Circuit": [
        ItemBoxGroup("First U-turn", 7),
        ItemBoxGroup("Last Turn", 5),
        ItemBoxGroup("50cc First Straight", 4),
        ItemBoxGroup("50cc Second Straight", 4),
        ItemBoxGroup("100cc Center", 4, required_items={items.PROGRESSIVE_CLASS:1}),
        ItemBoxGroup("100cc Chomp Shortcut", 2, {TAG_ITEM_BOX_INTERESTING}, {items.PROGRESSIVE_CLASS:1}),
        ItemBoxGroup("100cc Last Turn Shortcut", 2, {TAG_ITEM_BOX_INTERESTING}, {items.PROGRESSIVE_CLASS:1}),
    ],
    "Peach Beach": [
        ItemBoxGroup("Hidden Pipe", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("First Turn", 5),
        ItemBoxGroup("Beach Jump", 2, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Under Arc", 6),
        ItemBoxGroup("Ramp", 6),
        ItemBoxGroup("Fountain", 2, {TAG_ITEM_BOX_INTERESTING}),
    ],
    "Baby Park": [
        ItemBoxGroup("First Turn", 7),
        ItemBoxGroup("Second Turn", 7),
    ],
    "Dry Dry Desert": [
        ItemBoxGroup("Start", 4),
        ItemBoxGroup("First Turn", 5),
        ItemBoxGroup("Before Sand Pit", 4),
        ItemBoxGroup("After Sand Pit", 4),
        ItemBoxGroup("Between Pokeys", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Sand Hills", 5),
        ItemBoxGroup("Last Pokeys", 4),
    ],
    "Mushroom Bridge": [
        ItemBoxGroup("Left Lane", 2),
        ItemBoxGroup("Right Lane", 2),
        ItemBoxGroup("Pipe", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("First Tunnel", 3),
        ItemBoxGroup("Sidewalk", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Second Tunnel", 3),
        ItemBoxGroup("Bridge", 3),
        ItemBoxGroup("Bridge Top", 2, {TAG_ITEM_BOX_INTERESTING}),
    ],
    "Mario Circuit": [
        ItemBoxGroup("Start", 5),
        ItemBoxGroup("Before Tunnel", 4),
        ItemBoxGroup("Near Goombas", 6),
    ],
    "Daisy Cruiser": [
        ItemBoxGroup("First", 5),
        ItemBoxGroup("Dining Hall", 8, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Cargo Hatch", 2),
        ItemBoxGroup("Cargo Area", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Deck", 5),
    ],
    "Waluigi Stadium": [
        ItemBoxGroup("Start", 4),
        ItemBoxGroup("First Jump", 1),
        ItemBoxGroup("Second Jump", 1),
        ItemBoxGroup("Near Big Puddle", 4),
        ItemBoxGroup("First Piranha", 4),
        ItemBoxGroup("Second Piranha", 4),
        ItemBoxGroup("After Piranhas", 4),
        ItemBoxGroup("Last Jump", 1, {TAG_ITEM_BOX_INTERESTING}),
    ],
    "Sherbet Land": [
        ItemBoxGroup("Start", 4),
        ItemBoxGroup("Tunnel Beginning", 3),
        ItemBoxGroup("Tunnel End", 3),
        ItemBoxGroup("After Tunnel", 3),
        ItemBoxGroup("Before Ice", 5),
        ItemBoxGroup("On Ice", 4, {TAG_ITEM_BOX_INTERESTING}),
    ],
    "Mushroom City": [
        ItemBoxGroup("Outer Route", 2),
        ItemBoxGroup("First Block", 1),
        ItemBoxGroup("Last Straight Left Lane", 2),
        ItemBoxGroup("Last Straight Right Lane", 3),
        ItemBoxGroup("Start", 4),
        ItemBoxGroup("Alley", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Crossroad", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("After City", 4),
        ItemBoxGroup("Ramp", 3),
    ],
    "Yoshi Circuit": [
        ItemBoxGroup("First Turn", 4),
        ItemBoxGroup("Before Tunnel", 4),
        ItemBoxGroup("After Tunnel", 4),
        ItemBoxGroup("Before U-turn", 4),
        ItemBoxGroup("Tunnel Shortcut", 2, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Last Straight", 5),
    ],
    "DK Mountain": [
        ItemBoxGroup("Start", 4),
        ItemBoxGroup("Mountain Top", 4),
        ItemBoxGroup("Cliff U-turn", 4),
        ItemBoxGroup("Hairpin Turn", 5),
    ],
    "Wario Colosseum": [
        ItemBoxGroup("First Jump", 1),
        ItemBoxGroup("Second Jump", 1),
        ItemBoxGroup("Before Big Jump", 5),
        ItemBoxGroup("After Spiral", 4),
        ItemBoxGroup("Wide Curve", 5),
        ItemBoxGroup("Before Pit", 4),
        ItemBoxGroup("Pit Left", 2),
        ItemBoxGroup("Pit Jump", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Pit Right", 2),
        ItemBoxGroup("After Pit", 6),
        ItemBoxGroup("Last Jump", 4),
    ],
    "Dino Dino Jungle": [
        ItemBoxGroup("First Turn", 4),
        ItemBoxGroup("Over Logs", 2, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Under Dino", 4),
        ItemBoxGroup("Bridge", 2, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Cave", 3),
        ItemBoxGroup("Cave Shortcut", 1, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("After Cave", 4),
        ItemBoxGroup("Last Straight", 4),
    ],
    "Bowser's Castle": [
        ItemBoxGroup("Entrance", 4),
        ItemBoxGroup("Lava Room Left", 2),
        ItemBoxGroup("Lava Room Right", 2),
        ItemBoxGroup("Spinning Fire", 4, {TAG_ITEM_BOX_INTERESTING}),
        ItemBoxGroup("Balcon", 4),
        ItemBoxGroup("Cannon Room First", 3),
        ItemBoxGroup("Cannon Room Second", 3),
    ],
    "Rainbow Road": [
        ItemBoxGroup("Downhill", 4),
        ItemBoxGroup("U-turn", 5),
        ItemBoxGroup("Spiral", 4),
        ItemBoxGroup("After Spiral", 4),
        ItemBoxGroup("Big Pipe", 5),
        ItemBoxGroup("Last Jump", 4),
    ],
}

def get_loc_name_item_box(course: str, group: int, number: int = -1) -> str:
    """Returns box name if number is defined. If no number, then returns group name."""
    group: ItemBoxGroup = BOX_NAMES[course][group]
    if group.count == 1:
        return f"{course} - {group.name} Box"
    elif number == -1:
        return f"{course} - {group.name} Boxes"
    else:
        return f"{course} - {group.name} Box {number + 1}"


class CustomItemBox(NamedTuple):
    name: str
    replaces_group: str
    replaces_number: int
    position: tuple[float, float, float]
    tags: set[str] = set()

CUSTOM_BOXES: dict[str, list[CustomItemBox]] = {
    "Peach Beach": [
        CustomItemBox("Behind Cargo", "Under Arc", 5, (-10870, 1360, 26570)),
    ],
    "Baby Park": [
        CustomItemBox("Outer Edge", "Second Turn", 0, (14100, 6000, 0)),
    ],
    "Dry Dry Desert": [
        CustomItemBox("Sphinx", "Sand Hills", 2, (-34300, 6730, 14850)),
    ],
    "Mushroom Bridge": [
        CustomItemBox("Toad House", "Bridge", 1, (9300, 4240, -3200)),
    ],
    "Waluigi Stadium": [
        CustomItemBox("Under Second Jump", "First Piranha", 3, (-8030, 2055, -4950)),
    ],
    "Sherbet Land": [
        CustomItemBox("Under Freezie", "Before Ice", 4, (8250, 1520, 22020)),
    ],
    "Mushroom City": [
        CustomItemBox("Follow Cars", "After City", 3, (-19400, 5000, -900)),
    ],
    "DK Mountain": [
        CustomItemBox("Mountain Top", "Cliff U-turn", 3, (-250, 33830, -57200)),
    ],
    "Wario Colosseum": [
        CustomItemBox("Cage Top", "After Pit", 5, (2000, 29940, 820)),
    ],
    "Bowser's Castle": [
        CustomItemBox("Behind Start", "Balcon", 3, (7300, 8060, 18500)),
    ],
    "Rainbow Road": [
        CustomItemBox("Under Jump", "U-turn", 4, (-2630, 28500, -3930)),
    ],
}

def get_loc_name_custom_box(course: str, number: int) -> str:
    """Returns custom box name."""
    box: ItemBoxGroup = CUSTOM_BOXES[course][number]
    return f"{course} - {box.name} Box"
