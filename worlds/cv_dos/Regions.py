from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
from .Rules import small_uppies, big_uppies
from .soul_regions import create_soul_regions
#from .in_game_data import goal_triggers
from .Options import GateItems
if TYPE_CHECKING:
    from . import DoSWorld


class DoSLocation(Location):
    game: str = "Castlevania: Dawn of Sorrow"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "DoSWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Lost Village Upper"),
        create_region(world, player, locations_per_region, "Lost Village Upper Doorway"),
        create_region(world, player, locations_per_region, "Lost Village Lower"),
        create_region(world, player, locations_per_region, "Lost Village Underground Bottom"), 
        create_region(world, player, locations_per_region, "Lost Village Underground Middle"), 
        create_region(world, player, locations_per_region, "Lost Village Underground Top"),
        create_region(world, player, locations_per_region, "Lost Village Courtyard"),

        create_region(world, player, locations_per_region, "Wizardry Lab Main"),
        create_region(world, player, locations_per_region, "Wizardry Lab West Gate"),
        create_region(world, player, locations_per_region, "Wizardry Lab East Gate"),
        create_region(world, player, locations_per_region, "Wizardry Lab Sunken"),
        create_region(world, player, locations_per_region, "Wizardry Lab Sunken West Door"),
        create_region(world, player, locations_per_region, "Wizardry Lab Sunken East Door"),

        create_region(world, player, locations_per_region, "Garden of Madness Lower"),
        create_region(world, player, locations_per_region, "Garden of Madness Upper"),
        create_region(world, player, locations_per_region, "Garden of Madness Water Blocked"),
        create_region(world, player, locations_per_region, "Garden of Madness Post-Boss"),
        create_region(world, player, locations_per_region, "Garden of Madness East Gate"),

        create_region(world, player, locations_per_region, "Demon Guest House Main"),
        create_region(world, player, locations_per_region, "Demon Guest House Puppet Wall Right"),
        create_region(world, player, locations_per_region, "Demon Guest House Lower"),
        create_region(world, player, locations_per_region, "Demon Guest House Number Puzzle"),
        create_region(world, player, locations_per_region, "Demon Guest House Number Puzzle West"),
        create_region(world, player, locations_per_region, "Demon Guest House West Wing"),
        create_region(world, player, locations_per_region, "Demon Guest House Upper"),

        create_region(world, player, locations_per_region, "Dark Chapel"),
        create_region(world, player, locations_per_region, "Dark Chapel Big Room"),
        create_region(world, player, locations_per_region, "Dark Chapel Catacombs Exit"),

        create_region(world, player, locations_per_region, "Condemned Tower Bottom"),
        create_region(world, player, locations_per_region, "Condemned Tower Main"),
        create_region(world, player, locations_per_region, "Condemned Tower Top"),

        create_region(world, player, locations_per_region, "Cursed Clock Tower Entrance"),
        create_region(world, player, locations_per_region, "Cursed Clock Tower Central"),
        create_region(world, player, locations_per_region, "Cursed Clock Tower Boss Area"),  # if i do warp room swap i need to make pre and post boss
        create_region(world, player, locations_per_region, "Cursed Clock Tower Post-Boss"),
        create_region(world, player, locations_per_region, "Cursed Clock Tower Exit"),

        create_region(world, player, locations_per_region, "Subterranean Hell Top Entrance"),
        create_region(world, player, locations_per_region, "Subterranean Hell East"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central/East Connection"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central Upper"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central Exit"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central Lower"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central/Shaft Divide"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Middle"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Top"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Bottom"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Bottom Stairs"),
        create_region(world, player, locations_per_region, "Subterranean Hell Spike Room West"),
        create_region(world, player, locations_per_region, "Subterranean Hell Spike Room East"),
        create_region(world, player, locations_per_region, "Subterranean Hell Button Gate Room"),

        create_region(world, player, locations_per_region, "Silenced Ruins Antechamber"),
        create_region(world, player, locations_per_region, "Silenced Ruins"),
        create_region(world, player, locations_per_region, "Silenced Ruins Back Exit"),
        create_region(world, player, locations_per_region, "Silenced Ruins Upper Entrance"),

        create_region(world, player, locations_per_region, "The Pinnacle"),
        create_region(world, player, locations_per_region, "The Pinnacle Throne Room"),
        create_region(world, player, locations_per_region, "The Pinnacle Lower"),

        create_region(world, player, locations_per_region, "Warp Room"),
    ]

    if world.mine_status != "Disabled":
        regions.extend([
        create_region(world, player, locations_per_region, "Mine of Judgment"),
        create_region(world, player, locations_per_region, "The Abyss"),
        create_region(world, player, locations_per_region, "The Abyss Beyond Abaddon")
        ])

    for region in world.common_souls:
        regions.append(create_region(world, player, locations_per_region, region))

    for region in world.uncommon_souls:
        regions.append(create_region(world, player, locations_per_region, region))

    for region in world.rare_souls:
        regions.append(create_region(world, player, locations_per_region, region))

    multiworld.regions += regions
    ########################################

    #Lost Village
    multiworld.get_region("Lost Village Upper", player).add_exits(["Wizardry Lab Main", "Lost Village Upper Doorway"],
                                                    {"Wizardry Lab Main": lambda state: state.has("Moat Drained", player),
                                                     "Lost Village Upper Doorway": lambda state: state.has_all({"Puppet Master Soul", "Flying Armor Soul"}, player) or state.has_any(small_uppies, player) or state.has_all({"Puppet Master Soul", "Skeleton Ape Soul"}, player)}) #Is the ape trick hard? Can be done without ape if speedboost on

    if world.options.open_drawbridge:
        # Open courtyard removes this rule
        multiworld.get_region("Lost Village Upper", player).add_exits(["Lost Village Courtyard"])
    else:
        multiworld.get_region("Lost Village Upper", player).add_exits(["Lost Village Courtyard"],
                                                    {"Lost Village Courtyard": lambda state: state.has_any(small_uppies, player)})

    multiworld.get_region("Lost Village Courtyard", player).add_exits(["Lost Village Upper", "Demon Guest House Lower"])

    multiworld.get_region("Lost Village Upper Doorway", player).add_exits(["Lost Village Upper", "Demon Guest House Number Puzzle West"])

    multiworld.get_region("Lost Village Lower", player).add_exits(["Lost Village Upper", "Warp Room"],
                                                    {"Lost Village Upper": lambda state: state.has(world.magic_seal_table["Lost Village"], player)})

    multiworld.get_region("Lost Village Underground Bottom", player).add_exits(["Lost Village Underground Middle", "Wizardry Lab Sunken"],
                                                    {"Lost Village Underground Middle": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                     "Wizardry Lab Sunken": lambda state: state.has("Rahab Soul", player)})

    multiworld.get_region("Lost Village Underground Middle", player).add_exits(["Lost Village Underground Top", "Wizardry Lab West Gate", "Lost Village Underground Bottom"],
                                                    {"Lost Village Underground Top": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Lost Village Underground Top", player).add_exits(["Lost Village Lower", "Lost Village Underground Middle"])
    #######################
    #Wizardry Lab

    multiworld.get_region("Wizardry Lab Main", player).add_exits(["Lost Village Lower", "Garden of Madness Lower", "Warp Room", "Wizardry Lab West Gate", "Wizardry Lab East Gate"],
                                                    {"Lost Village Lower": lambda state: state.has("Moat Drained", player),
                                                     "Garden of Madness Lower": lambda state: state.has("Balore Soul", player) or state.has_any(small_uppies, player),
                                                     "Wizardry Lab West Gate": lambda state: state.has("West Lab Gate Key", player),
                                                     "Wizardry Lab East Gate": lambda state: state.has("East Lab Gate Key", player)})

    multiworld.get_region("Wizardry Lab West Gate", player).add_exits(["Lost Village Underground Middle"])
    multiworld.get_region("Wizardry Lab East Gate", player).add_exits(["Subterranean Hell Shaft Top"])
    multiworld.get_region("Wizardry Lab Sunken West Door", player).add_exits(["Lost Village Underground Bottom", "Wizardry Lab Sunken"],
                                                    {"Wizardry Lab Sunken": lambda state: state.has("Rahab Soul", player)})

    multiworld.get_region("Wizardry Lab Sunken", player).add_exits(["Wizardry Lab Sunken West Door", "Wizardry Lab Sunken East Door"],
                                                {"Wizardry Lab Sunken West Door": lambda state: state.has_any(big_uppies, player)})

    multiworld.get_region("Wizardry Lab Sunken East Door", player).add_exits(["Wizardry Lab Sunken", "Subterranean Hell Spike Room West"],
                                                {"Wizardry Lab Sunken": lambda state: state.has("Rahab Soul", player)})
    
    if world.options.gate_items < GateItems.option_buttonsanity:
        multiworld.get_region("Wizardry Lab West Gate", player).add_exits(["Wizardry Lab Main"])
        multiworld.get_region("Wizardry Lab East Gate", player).add_exits(["Wizardry Lab Main"])
    else:
        multiworld.get_region("Wizardry Lab West Gate", player).add_exits(["Wizardry Lab Main"],
                                                                         {"Wizardry Lab Main": lambda state: state.has("West Lab Gate Key", player)})
        multiworld.get_region("Wizardry Lab East Gate", player).add_exits(["Wizardry Lab Main"],
                                                                         {"Wizardry Lab Main": lambda state: state.has("East Lab Gate Key", player)})
    ##########################
    #Garden of Madness
    multiworld.get_region("Garden of Madness Lower", player).add_exits(["Wizardry Lab Main", "Garden of Madness Water Blocked", "Demon Guest House Lower", "Garden of Madness Upper", "Dark Chapel", "Warp Room"],
                                                    {"Garden of Madness Water Blocked": lambda state: state.has("Rahab Soul", player),
                                                     "Garden of Madness Upper": lambda state: (state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player))})

    multiworld.get_region("Garden of Madness Water Blocked", player).add_exits(["Garden of Madness Lower", "Subterranean Hell Central Exit"],
                                                    {"Garden of Madness Lower": lambda state: state.has("Rahab Soul", player)})

    multiworld.get_region("Garden of Madness Upper", player).add_exits(["Garden of Madness Lower", "Garden of Madness Post-Boss"],
                                                    {"Garden of Madness Post-Boss": lambda state: state.has(world.magic_seal_table["Garden of Madness"], player)})

    multiworld.get_region("Garden of Madness Post-Boss", player).add_exits(["Garden of Madness Upper", "Demon Guest House Main", "Garden of Madness East Gate"],
                                                    {"Garden of Madness Upper": lambda state: state.has(world.magic_seal_table["Garden of Madness"], player),
                                                     "Garden of Madness East Gate": lambda state: state.has("Garden Gate Key", player)})

    multiworld.get_region("Garden of Madness East Gate", player).add_exits(["Cursed Clock Tower Entrance"])
    if world.options.gate_items < GateItems.option_buttonsanity:
        multiworld.get_region("Garden of Madness East Gate", player).add_exits(["Garden of Madness Post-Boss"])
    else:
        multiworld.get_region("Garden of Madness East Gate", player).add_exits(["Garden of Madness Post-Boss"],
                                                                               {"Garden of Madness Post-Boss": lambda state: state.has("Garden Gate Key", player)})
    #############################
    #Demon Guest House
    multiworld.get_region("Demon Guest House Main", player).add_exits(["Garden of Madness Post-Boss", "Demon Guest House Puppet Wall Right", "Demon Guest House Number Puzzle", "Demon Guest House West Wing"],
                                                                    {"Demon Guest House Puppet Wall Right": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player),
                                                                     "Demon Guest House West Wing": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Demon Guest House Puppet Wall Right", player).add_exits(["Demon Guest House Main", "Demon Guest House Lower"],
                                                                    {"Demon Guest House Main": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Demon Guest House Lower", player).add_exits(["Lost Village Upper", "Garden of Madness Lower", "Demon Guest House Puppet Wall Right"],
                                                                    {"Demon Guest House Puppet Wall Right": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Demon Guest House Number Puzzle", player).add_exits(["Demon Guest House Main", "Demon Guest House West Wing", "Demon Guest House Number Puzzle West"],
                                                                    {"Demon Guest House West Wing": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Demon Guest House Number Puzzle West", player).add_exits(["Lost Village Upper Doorway"])

    multiworld.get_region("Demon Guest House West Wing", player).add_exits(["Demon Guest House Main", "Demon Guest House Number Puzzle", "Warp Room"],
                                                                    {"Demon Guest House Main": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Demon Guest House Upper", player).add_exits(["Demon Guest House Main", "The Pinnacle Lower"])
    ###############################
    #Dark Chapel
    multiworld.get_region("Dark Chapel", player).add_exits(["Garden of Madness Lower", "Dark Chapel Catacombs Exit", "Dark Chapel Big Room", "Warp Room"],
                                                                    {"Dark Chapel Catacombs Exit": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player),
                                                                     "Dark Chapel Big Room": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Dark Chapel Big Room", player).add_exits(["Condemned Tower Bottom", "Dark Chapel"])

    multiworld.get_region("Dark Chapel Catacombs Exit", player).add_exits(["Subterranean Hell Top Entrance", "Dark Chapel"],
    {"Dark Chapel": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})
    ##########################################################################################################
    #Condemned Tower
    multiworld.get_region("Condemned Tower Bottom", player).add_exits(["Dark Chapel", "Dark Chapel Big Room", "Condemned Tower Main"],
                                                                    {"Condemned Tower Main": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                                     "Dark Chapel Big Room": lambda state: state.has_any(small_uppies, player)})
    if world.mine_status != "Disabled":
        if not world.mine_status or world.mine_status == "Open":
            multiworld.get_region("Condemned Tower Bottom", player).add_exits(["Mine of Judgment"])  # Add a ruleless connector here
        else:
            multiworld.get_region("Condemned Tower Bottom", player).add_exits(["Mine of Judgment"],
                                                                            {"Mine of Judgment": lambda state: state.has_all(world.mine_triggers, player)})

    multiworld.get_region("Condemned Tower Main", player).add_exits(["Condemned Tower Bottom", "Cursed Clock Tower Entrance", "Condemned Tower Top"],
                                                                    {"Cursed Clock Tower Entrance": lambda state: state.has("Tower Key", player),
                                                                     "Condemned Tower Top": lambda state: state.has(world.magic_seal_table["Condemned Tower"], player)})

    multiworld.get_region("Condemned Tower Top", player).add_exits(["Condemned Tower Main", "Warp Room"],
                                                                    {"Condemned Tower Main": lambda state: state.has(world.magic_seal_table["Condemned Tower"], player)})
                                                                    
    ################################
    #Cursed Clock Tower
    multiworld.get_region("Cursed Clock Tower Entrance", player).add_exits(["Garden of Madness East Gate", "Condemned Tower Main", "Cursed Clock Tower Central"],
                                                                    {"Cursed Clock Tower Central": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                                     "Condemned Tower Main": lambda state: state.has("Tower Key", player)})

    multiworld.get_region("Cursed Clock Tower Central", player).add_exits(["Cursed Clock Tower Entrance", "Cursed Clock Tower Boss Area"],
                                                                    {"Cursed Clock Tower Boss Area": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Cursed Clock Tower Boss Area", player).add_exits(["Cursed Clock Tower Central", "Cursed Clock Tower Post-Boss"],
                                                                    {"Cursed Clock Tower Post-Boss": lambda state: state.has(world.magic_seal_table["Cursed Clock Tower"], player)})

    multiworld.get_region("Cursed Clock Tower Post-Boss", player).add_exits(["Cursed Clock Tower Boss Area", "Cursed Clock Tower Exit", "Cursed Clock Tower Central", "Warp Room"],
                                                                    {"Cursed Clock Tower Boss Area": lambda state: state.has(world.magic_seal_table["Cursed Clock Tower"], player),
                                                                     "Cursed Clock Tower Exit": lambda state: state.has("Bat Company Soul", player)})

    multiworld.get_region("Cursed Clock Tower Exit", player).add_exits(["Cursed Clock Tower Post-Boss", "The Pinnacle Lower"],
                                                                    {"Cursed Clock Tower Post-Boss": lambda state: state.has("Bat Company Soul", player)})
    ####################################################################################
    #Subterranean Hell
    multiworld.get_region("Subterranean Hell Top Entrance", player).add_exits(["Dark Chapel Catacombs Exit", "Subterranean Hell East"],
                                                {"Subterranean Hell East": lambda state: state.has_all({"Rahab Soul", world.magic_seal_table["Subterranean Hell"]}, player)})

    multiworld.get_region("Subterranean Hell East", player).add_exits(["Subterranean Hell Top Entrance", "Subterranean Hell Central/East Connection", "Subterranean Hell Button Gate Room"],
                                                {"Subterranean Hell Top Entrance": lambda state: state.has_all({"Rahab Soul", world.magic_seal_table["Subterranean Hell"]}, player) and (state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)),
                                                 "Subterranean Hell Central/East Connection": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Subterranean Hell Central/East Connection", player).add_exits(["Subterranean Hell Central Upper", "Subterranean Hell East"],
                                                {"Subterranean Hell Central Upper": lambda state: state.has_any({"Rahab Soul", "Malphas Soul"}, player),
                                                "Subterranean Hell East": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Subterranean Hell Central Upper", player).add_exits(["Subterranean Hell Central/East Connection", "Subterranean Hell Central Exit", "Subterranean Hell Central Lower"],
                                                {"Subterranean Hell Central Exit": lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}, player),
                                                "Subterranean Hell Central/East Connection": lambda state: state.has_any({"Rahab Soul", "Malphas Soul"}, player)})

    multiworld.get_region("Subterranean Hell Central Exit", player).add_exits(["Subterranean Hell Central Upper", "Garden of Madness Water Blocked"],
                                                {"Subterranean Hell Central Upper": lambda state: state.has_any({"Rahab Soul", "Malphas Soul"}, player)})

    multiworld.get_region("Subterranean Hell Central Lower", player).add_exits(["Subterranean Hell Central Upper", "Subterranean Hell Central/Shaft Divide", "Warp Room", "Subterranean Hell Shaft Middle"],
                                                {"Subterranean Hell Central Upper": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                "Subterranean Hell Shaft Middle": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Subterranean Hell Shaft Middle", player).add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Shaft Bottom", "Subterranean Hell Shaft Top", "Subterranean Hell Shaft Bottom Stairs"],
                                                {"Subterranean Hell Central Lower": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Subterranean Hell Shaft Top": lambda state: state.has_any(big_uppies, player)})

    multiworld.get_region("Subterranean Hell Shaft Top", player).add_exits(["Subterranean Hell Shaft Middle", "Wizardry Lab East Gate"])

    multiworld.get_region("Subterranean Hell Shaft Bottom", player).add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Spike Room East", "Silenced Ruins Antechamber", "Subterranean Hell Shaft Bottom Stairs"],
                                                {"Subterranean Hell Shaft Middle": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                "Subterranean Hell Shaft Bottom Stairs": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Subterranean Hell Spike Room East": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Silenced Ruins Antechamber": lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Flying Armor Soul", "Black Panther Soul"}, player)})

    multiworld.get_region("Subterranean Hell Shaft Bottom Stairs", player).add_exits(["Subterranean Hell Shaft Bottom", "Subterranean Hell Central/Shaft Divide"],
                                                                                    {"Subterranean Hell Central/Shaft Divide": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Subterranean Hell Spike Room East", player).add_exits(["Subterranean Hell Shaft Bottom"])

    multiworld.get_region("Subterranean Hell Spike Room West", player).add_exits(["Wizardry Lab Sunken East Door"])

    multiworld.get_region("Subterranean Hell Central/Shaft Divide", player).add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Shaft Bottom Stairs"])

    multiworld.get_region("Subterranean Hell Button Gate Room", player).add_exits(["Subterranean Hell East", "Silenced Ruins Back Exit"],
                                                                                 {"Subterranean Hell East": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                                                  "Silenced Ruins Back Exit": lambda state: state.has("Cavern Gate Key", player)})

    #####################################################
    #Silenced Ruins
    multiworld.get_region("Silenced Ruins Antechamber", player).add_exits(["Subterranean Hell Shaft Bottom", "Silenced Ruins Upper Entrance"],
                                                {"Silenced Ruins Upper Entrance": lambda state: state.has("Zephyr Soul", player)})

    multiworld.get_region("Silenced Ruins Upper Entrance", player).add_exits(["Silenced Ruins Antechamber", "Silenced Ruins"],
                                                {"Silenced Ruins Antechamber": lambda state: state.has("Zephyr Soul", player)})

    multiworld.get_region("Silenced Ruins", player).add_exits(["Silenced Ruins Back Exit", "Silenced Ruins Upper Entrance", "Warp Room"],
                                                {"Silenced Ruins Upper Entrance": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Silenced Ruins Back Exit": lambda state: state.has_any(small_uppies, player) or state.has_all({"Puppet Master Soul", "Black Panther Soul"}, player)})

    multiworld.get_region("Silenced Ruins Back Exit", player).add_exits(["Silenced Ruins"])
    if world.options.gate_items < GateItems.option_buttonsanity:
        multiworld.get_region("Silenced Ruins Back Exit", player).add_exits(["Subterranean Hell Button Gate Room"])
    else:
        multiworld.get_region("Silenced Ruins Back Exit", player).add_exits(["Subterranean Hell Button Gate Room"],
                                                                            {"Subterranean Hell Button Gate Room": lambda state: state.has("Cavern Gate Key", player)})

    ###############################
    #The Pinnacle
    multiworld.get_region("The Pinnacle Lower", player).add_exits(["The Pinnacle", "Demon Guest House Upper", "Cursed Clock Tower Exit", "Warp Room"],
                                                                 {"The Pinnacle": lambda state: state.has_any(small_uppies, player),
                                                                 "Cursed Clock Tower Exit": lambda state: state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player),
                                                                 "Warp Room": lambda state: state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player)})

    multiworld.get_region("The Pinnacle", player).add_exits(["The Pinnacle Lower", "The Pinnacle Throne Room"],
                                                                 {"The Pinnacle Throne Room": lambda state: state.has_any(big_uppies, player)})

    ###############################
    #Mine of Judgment
    if world.mine_status != "Disabled":
        multiworld.get_region("Mine of Judgment", player).add_exits(["The Abyss", "Warp Room"],
                                                                    {"The Abyss": lambda state: state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player) and state.has(world.magic_seal_table["Mine of Judgment"], player)})

        multiworld.get_region("The Abyss", player).add_exits(["Mine of Judgment", "The Abyss Beyond Abaddon"],
                                                            {"Mine of Judgment": lambda state: state.has_any(small_uppies, player),
                                                            "The Abyss Beyond Abaddon": lambda state: state.has_any(big_uppies, player) and state.has(world.magic_seal_table["The Abyss"], player)})

        multiworld.get_region("The Abyss Beyond Abaddon", player).add_exits(["Warp Room"])

    multiworld.get_region("Warp Room", player).add_exits([world.starting_warp_region])
    multiworld.get_region("Subterranean Hell Spike Room East", player).add_exits(["Subterranean Hell Spike Room West"],
                            {"Subterranean Hell Spike Room West": lambda state: state.has("Rahab Soul", player) and (state.has_all({"Puppet Master Soul", "Skeleton Ape Soul"}, player) or state.has("Bone Ark Soul", player))})

    multiworld.get_region("Subterranean Hell Spike Room West", player).add_exits(["Subterranean Hell Spike Room East"],
                            {"Subterranean Hell Spike Room East": lambda state: state.has("Rahab Soul", player) and (state.has_all({"Puppet Master Soul", "Skeleton Ape Soul"}, player) or state.has("Bone Ark Soul", player))})

    if world.options.boost_speed:
        multiworld.get_region("Lost Village Upper", player).add_exits(["Lost Village Lower"], {
            "Lost Village Lower": lambda state: state.has(world.magic_seal_table["Lost Village"], player)
        })
    else:
        multiworld.get_region("Lost Village Upper", player).add_exits(["Lost Village Lower"], {
            "Lost Village Lower": lambda state: state.has(world.magic_seal_table["Lost Village"], player) and (state.has_any(small_uppies, player) or state.has_any({"Black Panther Soul", "Puppet Master Soul", "Flying Armor Soul"}, player))
        })

    create_soul_regions(world)

def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = DoSLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "DoSWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
    

# TODO; Skeletone Ape in tower with speedboost on
