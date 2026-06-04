from typing import Dict, List, NamedTuple, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, CollectionState

if TYPE_CHECKING:
    from . import ChainedEchoesWorld


class ChainedEchoesConnection(NamedTuple):
    destination: str  # Name of the region the connection leads to
    required_items: Dict[str, int]  # Item name → Count required


class ChainedEchoesRegion(NamedTuple):
    connections: List[ChainedEchoesConnection]  # List of connections from this region


def create_connection_rule(required_items: Dict[str, int], world: "ChainedEchoesWorld") -> Callable[[CollectionState], bool]:
    """
    Generate an access rule for a connection based on required items.
    """
    def rule(state: CollectionState) -> bool:
        return state.has_all_counts(required_items, world.player)
    return rule


# Define regions and their connections parsed from a text file
region_data_table: Dict[str, ChainedEchoesRegion] = {}

# Example region connections text data
region_txt = '''
Menu,Prologue
Prologue,Sandworm,Lenne Skill #1,1,Robb Skill #1,1
Sandworm,Krachan,Glenn Skill #1,1,Sienna Skill #1,1,Kylian Skill #1,1,Glenn Boost #1,1,Glenn Boost #2,1,Lenne Boost #1,1,Lenne Boost #2,1,Robb Boost #1,1,Robb Boost #2,1
Krachan,Flame Mantis,Victor Skill #1,1,Glenn Boost #3,1,Sienna Boost #1,1,Sienna Boost #2,1
Flame Mantis,Lich,Glenn Boost #4,1
Lich,Mines,Glenn Boost #5,1
Mines,Drill Breaker,Glenn Boost #6,1
Drill Breaker,Arlette,Ba'Thraz Skill #1,1,Glenn Boost #7,1,Victor Boost #1,1,Victor Boost #2,1,Victor Boost #3,1,Victor Boost #4,1,Robb Boost #3,1,Robb Boost #4,1
Arlette,Puppeteer,Glenn Boost #8,1
Puppeteer,Gin,Glenn Boost #9,1
Gin,Kondor,Glenn Boost #10,1
Kondor,Fridolyn,Glenn Boost #11,1
Fridolyn,Manor,Manor Key,1
Fridolyn,Matthye,Glenn Boost #12,1
Matthye,Donner,Glenn Boost #13,1
Donner,Godfrey,Glenn Boost #14,1
Godfrey,Shaved Head,Glenn Boost #15,1
Shaved Head,Endahrt,Amalia Skill #1,1,Glenn Boost #16,1
Endahrt,Living Wall,Amalia Boost #1,1,Amalia Boost #2,1,Amalia Boost #3,1,Amalia Boost #4,1,Amalia Boost #5,1,Amalia Boost #6,1,Ba'Thraz Boost #1,1,Ba'Thraz Boost #2,1,Ba'Thraz Boost #3,1,Ba'Thraz Boost #4,1,Ba'Thraz Boost #5,1,Ba'Thraz Boost #6,1
Living Wall,Church,Church Key,1
Living Wall,Miner's Section,Miner's Key,1
Living Wall,Baibai X
Living Wall,Marylea
Marylea,Raphael,Key Card A,1,Key Card B,1,Key Card C,1,Key Card D,1
Raphael,Chained Echo
Chained Echo,Norgant,Norgant's Key,1
Chained Echo,Maria
Maria,Nhysa
Nhysa,Black Sun,Silver Key,1
Black Sun,Memory
Memory,Whyatt,Gold Key,1
Whyatt,Endgame
Endgame,Eastern Ograne,Elevator Key,1
Eastern Ograne,Baalrut,Charon's Coin Bag,1
Baalrut,Sewers,Water Handle,1
'''

# Parse region data
for line in region_txt.strip().splitlines():
    if not line or line.startswith("//"):
        continue

    parts = line.split(",")
    if len(parts) < 2:
        print(f"Malformed line: {line}")  # Debugging output
        continue

    source_region = parts[0].strip()
    destination_region = parts[1].strip()
    required_items = {}

    # Parse item requirements if available
    if len(parts) > 2:
        for i in range(2, len(parts), 2):
            item = parts[i].strip()
            count = int(parts[i + 1].strip())
            required_items[item] = count

    # Ensure the source region exists
    if source_region not in region_data_table:
        region_data_table[source_region] = ChainedEchoesRegion(connections=[])

    # Add the connection to the source region
    region_data_table[source_region].connections.append(
        ChainedEchoesConnection(destination=destination_region, required_items=required_items)
    )

    # Ensure the destination region exists (even if it has no connections initially)
    if destination_region not in region_data_table:
        region_data_table[destination_region] = ChainedEchoesRegion(connections=[])


def create_regions(world: "ChainedEchoesWorld"):
    """
    Step 1: Create all regions and add them to the multiworld.
    """
    created_regions = {
        region_name: Region(region_name, world.player, world.multiworld)
        for region_name in region_data_table
    }
    world.multiworld.regions.extend(created_regions.values())

    """
    Step 2: Add connections between regions using entrances.
    """
    for region_name, region in region_data_table.items():
        source_region = created_regions[region_name]

        for connection in region.connections:
            destination_region = created_regions[connection.destination]

            # Create an entrance in the source region leading to the destination
            entrance_name = f"{source_region.name} -> {destination_region.name}"
            entrance = Entrance(world.player, entrance_name, source_region)

            # Connect the entrance to the destination region
            entrance.connect(destination_region)

            # If the connection has access rules, assign them to the entrance
            if connection.required_items:
                entrance.access_rule = create_connection_rule(connection.required_items, world)

            # Add the entrance to the source region's exits
            source_region.exits.append(entrance)