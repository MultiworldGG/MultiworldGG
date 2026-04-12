import typing
from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance, Location
from .Options import SRB2Options
from .Locations import SRB2Location, location_table, GFZ_table,THZ_table,DSZ_table,CEZ_table,ACZ_table,\
    RVZ_table,ERZ_table,BCZ_table


class SRB2Zones(int, Enum):
    GREENFLOWER = 1
    TECHNO_HILL = 2
    DEEP_SEA = 3
    CASTLE_EGGMAN = 4
    ARID_CANYON = 5
    RED_VOLCANO = 6
    EGG_ROCK = 7
    BLACK_CORE = 8
# TODO ADD the rest of the zones/ special stages


class SRB2Region(Region):
    subregions: typing.List[Region] = []


# sm64paintings is a dict of entrances, format LEVEL | AREA


def create_regions(world: MultiWorld, options: SRB2Options, player: int):
    regMM = Region("Menu", player, world, "Level Select")
    #create_default_locs(regMM, locSS_table)#TODO this might break something
    world.regions.append(regMM)
    regCredits = create_region("Credits", player, world)
    create_locs(regCredits,"Good Ending")



    if options.match_maps:
        regMPJVZ = create_region("Jade Valley Zone", player, world)
        create_locs(regMPJVZ,"Jade Valley Ring Emblem")
        regMPNFZ = create_region("Noxious Factory Zone", player, world)
        create_locs(regMPNFZ, "Noxious Factory Ring Emblem")
        regMPTPZ = create_region("Tidal Palace Zone", player, world)
        create_locs(regMPTPZ, "Tidal Palace Ring Emblem")
        regMPTCZ = create_region("Thunder Citadel Zone", player, world)
        create_locs(regMPTCZ, "Thunder Citadel Ring Emblem")
        regMPDTZ = create_region("Desolate Twilight Zone", player, world)
        create_locs(regMPDTZ, "Desolate Twilight Ring Emblem")
        regMPFMZ = create_region("Frigid Mountain Zone", player, world)
        create_locs(regMPFMZ, "Frigid Mountain Ring Emblem")
        regMPOHZ = create_region("Orbital Hangar Zone", player, world)
        create_locs(regMPOHZ, "Orbital Hangar Ring Emblem")
        regMPSFZ = create_region("Sapphire Falls Zone", player, world)
        create_locs(regMPSFZ, "Sapphire Falls Ring Emblem")
        regMPDBZ = create_region("Diamond Blizzard Zone", player, world)
        create_locs(regMPDBZ, "Diamond Blizzard Ring Emblem")
        regMPCSZ = create_region("Celestial Sanctuary Zone", player, world)
        create_locs(regMPCSZ, "Celestial Sanctuary Ring Emblem")
        regMPFCZ = create_region("Frost Columns Zone", player, world)
        create_locs(regMPFCZ, "Frost Columns Ring Emblem")
        regMPMMZ = create_region("Meadow Match Zone", player, world)
        create_locs(regMPMMZ, "Meadow Match Ring Emblem")
        regMPGLZ = create_region("Granite Lake Zone", player, world)
        create_locs(regMPGLZ, "Granite Lake Ring Emblem")
        regMPSSZ = create_region("Summit Showdown Zone", player, world)
        create_locs(regMPSSZ, "Summit Showdown Ring Emblem")
        regMPSShZ = create_region("Silver Shiver Zone", player, world)
        create_locs(regMPSShZ, "Silver Shiver Ring Emblem")
        regMPUBZ = create_region("Uncharted Badlands Zone", player, world)
        create_locs(regMPUBZ, "Uncharted Badlands Ring Emblem")
        regMPPSZ = create_region("Pristine Shores Zone", player, world)
        create_locs(regMPPSZ, "Pristine Shores Ring Emblem")
        regMPCHZ = create_region("Crystalline Heights Zone", player, world)
        create_locs(regMPCHZ, "Crystalline Heights Ring Emblem")
        regMPSWZ = create_region("Starlit Warehouse Zone", player, world)
        create_locs(regMPSWZ, "Starlit Warehouse Ring Emblem")
        regMPMAZ = create_region("Midnight Abyss Zone", player, world)
        create_locs(regMPMAZ, "Midnight Abyss Ring Emblem")
        regMPATZ = create_region("Airborne Temple Zone", player, world)
        create_locs(regMPATZ, "Airborne Temple Ring Emblem")



    regGFZ1 = create_region("Greenflower Zone 1", player, world)
    regGFZ2 = create_region("Greenflower Zone 2", player, world)
    regGFZ3 = create_region("Greenflower Zone 3", player, world)

    create_locs(regGFZ1, "Greenflower (Act 1) Star Emblem", "Greenflower (Act 1) Spade Emblem","Greenflower (Act 1) Heart Emblem",
                "Greenflower (Act 1) Diamond Emblem","Greenflower (Act 1) Club Emblem","Greenflower (Act 1) Clear",
                "Greenflower (Act 1) Emerald Token - Breakable Wall Near Bridge","Greenflower (Act 1) Emerald Token - Midair Top Path")
    create_locs(regGFZ2,"Greenflower (Act 2) Star Emblem", "Greenflower (Act 2) Spade Emblem", "Greenflower (Act 2) Heart Emblem",
                "Greenflower (Act 2) Diamond Emblem","Greenflower (Act 2) Club Emblem","Greenflower (Act 2) Clear",
                "Greenflower (Act 2) Emerald Token - Main Path Cave","Greenflower (Act 2) Emerald Token - Under Bridge Near End",
                "Greenflower (Act 2) Emerald Token - No Spin High on Ledge")
    create_locs(regGFZ3,"Greenflower (Act 3) Clear")
    if options.time_emblems:
        create_locs(regGFZ1, "Greenflower (Act 1) Time Emblem")
        create_locs(regGFZ2, "Greenflower (Act 2) Time Emblem")
        create_locs(regGFZ3, "Greenflower (Act 3) Time Emblem")
    if options.ring_emblems:
        create_locs(regGFZ1, "Greenflower (Act 1) Ring Emblem")
        create_locs(regGFZ2, "Greenflower (Act 2) Ring Emblem")
    if options.score_emblems:
        create_locs(regGFZ3, "Greenflower (Act 3) Score Emblem")

    if options.oneup_sanity:
        create_locs(regGFZ1,"Greenflower (Act 1) Monitor - Upper Spin Path in Cave","Greenflower (Act 1) Monitor - Single Pillar Near End","Greenflower (Act 1) Monitor - Highest Ledge")
        create_locs(regGFZ2,"Greenflower (Act 2) Monitor - Breakable Floor Near Springs 1","Greenflower (Act 2) Monitor - Open Area Behind Checkered Pillar", "Greenflower (Act 2) Monitor - Skylight in 2nd Cave",
        "Greenflower (Act 2) Monitor - Fenced Flower Ledge", "Greenflower (Act 2) Monitor - Near Star Emblem 1","Greenflower (Act 2) Monitor - Waterfall Top Near Start",
        "Greenflower (Act 2) Monitor - Pillar Next to End", "Greenflower (Act 2) Monitor - High Ledge After Final Cave", "Greenflower (Act 2) Monitor - Inside Fence Above Start")
    if options.superring_sanity:
        create_locs(regGFZ1,"Greenflower (Act 1) Monitor - Lake Side Path on Ledge","Greenflower (Act 1) Monitor - Spin Path Entrance","Greenflower (Act 1) Monitor - Alcove Near Bridges 2",
        "Greenflower (Act 1) Monitor - First Pillar","Greenflower (Act 1) Monitor - Across High Bridge in Flowers","Greenflower (Act 1) Monitor - High Ledge After Cave","Greenflower (Act 1) Monitor - Alcove Near Bridges 1",
        "Greenflower (Act 1) Monitor - Lake Alcove Near End","Greenflower (Act 1) Monitor - Spring Pillar Near End 1","Greenflower (Act 1) Monitor - Behind Bars in Cave","Greenflower (Act 1) Monitor - Behind Bushes Upper Path",
        "Greenflower (Act 1) Monitor - Spring Pillar Near End 2")

        create_locs(regGFZ2,"Greenflower (Act 2) Monitor - Main Path Springs", "Greenflower (Act 2) Monitor - Very High Alcove 1", "Greenflower (Act 2) Monitor - Very High Alcove 2",
        "Greenflower (Act 2) Monitor - Very High Alcove 3", "Greenflower (Act 2) Monitor - Very High Alcove 4", "Greenflower (Act 2) Monitor - Very High Alcove 5", "Greenflower (Act 2) Monitor - Very High Alcove 6",
        "Greenflower (Act 2) Monitor - Very High Alcove 7", "Greenflower (Act 2) Monitor - Very High Alcove 8", "Greenflower (Act 2) Monitor - Spade Emblem Cave 1", "Greenflower (Act 2) Monitor - Spade Emblem Cave 2",
        "Greenflower (Act 2) Monitor - Spade Emblem Cave 3", "Greenflower (Act 2) Monitor - In Fences Near Picnic", "Greenflower (Act 2) Monitor - Log on Final Path", "Greenflower (Act 2) Monitor - Near Springs Before End",
        "Greenflower (Act 2) Monitor - Square Pillar Before Big Ramp", "Greenflower (Act 2) Monitor - Behind Bush Near Start", "Greenflower (Act 2) Monitor - Wall Under High Alcove", "Greenflower (Act 2) Monitor - No Spin Inside Spikes",
        "Greenflower (Act 2) Monitor - Open Area on Ledge", "Greenflower (Act 2) Monitor - High Path River", "Greenflower (Act 2) Monitor - Spin Path Red Springs")

    regTHZ1 = create_region("Techno Hill Zone 1", player, world)
    regTHZ2 = create_region("Techno Hill Zone 2", player, world)
    regTHZ2M = create_region("Techno Hill Zone 2 Main", player, world)
    regTHZ3 = create_region("Techno Hill Zone 3", player, world)

    create_locs(regTHZ1, "Techno Hill (Act 1) Star Emblem", "Techno Hill (Act 1) Spade Emblem","Techno Hill (Act 1) Heart Emblem", "Techno Hill (Act 1) Diamond Emblem",
                        "Techno Hill (Act 1) Club Emblem","Techno Hill (Act 1) Clear","Techno Hill (Act 1) Emerald Token - On Pipes","Techno Hill (Act 1) Emerald Token - Alt Path Under Slime")
    create_locs(regTHZ2M,"Techno Hill (Act 2) Star Emblem", "Techno Hill (Act 2) Spade Emblem", "Techno Hill (Act 2) Heart Emblem", "Techno Hill (Act 2) Diamond Emblem",
    "Techno Hill (Act 2) Club Emblem","Techno Hill (Act 2) Clear","Techno Hill (Act 2) Emerald Token - Deep in Slime","Techno Hill (Act 2) Emerald Token - Knuckles Path Backtrack")
    create_locs(regTHZ3,"Techno Hill (Act 3) Clear")
    if options.time_emblems:
        create_locs(regTHZ1, "Techno Hill (Act 1) Time Emblem")
        create_locs(regTHZ2M, "Techno Hill (Act 2) Time Emblem")
        create_locs(regTHZ3, "Techno Hill (Act 3) Time Emblem")

    if options.ring_emblems:
        create_locs(regTHZ1, "Techno Hill (Act 1) Ring Emblem")
        create_locs(regTHZ2M, "Techno Hill (Act 2) Ring Emblem")
    if options.score_emblems:
        create_locs(regTHZ3, "Techno Hill (Act 3) Score Emblem")
    if options.oneup_sanity:
        create_locs(regTHZ1,
        "Techno Hill (Act 1) Monitor - Spin Under Conveyor Belt Door","Techno Hill (Act 1) Monitor - Knuckles Path Highest Ledge","Techno Hill (Act 1) Monitor - In Slime Above Spade Emblem",
        "Techno Hill (Act 1) Monitor - Spring Shell Pipe Challenge","Techno Hill (Act 1) Monitor - Pipe Room High Corner","Techno Hill (Act 1) Monitor - Top of Elevator Shaft","Techno Hill (Act 1) Monitor - Deep in Slime Near 2nd Checkpoint",
        "Techno Hill (Act 1) Monitor - Outside Pipe Room High Ledge","Techno Hill (Act 1) Monitor - High Ledge in Hole Near Start")
        create_locs(regTHZ2M,"Techno Hill (Act 2) Monitor - Under Slime Before 2nd Checkpoint",
        "Techno Hill (Act 2) Monitor - High Ledge Outside 1","Techno Hill (Act 2) Monitor - Near Spade Emblem","Techno Hill (Act 2) Monitor - Large Jump Into Slime C",
        "Techno Hill (Act 2) Monitor - Near Detons on Pillar","Techno Hill (Act 2) Monitor - Behind Glass Piston Path","Techno Hill (Act 2) Monitor - Knuckles Path Under Spiked Hallway",
        "Techno Hill (Act 2) Monitor - Egg Corp Cavity Under Slime","Techno Hill (Act 2) Monitor - Pillar Before End","Techno Hill (Act 2) Monitor - Egg Corp Deep in Slime",
        "Techno Hill (Act 2) Monitor - Near Amy Emerald Token","Techno Hill (Act 2) Monitor - Tall Pillar Outside Glass")
    if options.superring_sanity:
        create_locs(regTHZ1,"Techno Hill (Act 1) Monitor - Crate on Large Slime Lake",
        "Techno Hill (Act 1) Monitor - Upper Path in Alcove","Techno Hill (Act 1) Monitor - On Pipe Outside Pipe Room","Techno Hill (Act 1) Monitor - Alt Path on Ledge 1","Techno Hill (Act 1) Monitor - Low Ledge Before Pipe Room",
        "Techno Hill (Act 1) Monitor - Pipe Room on Ground","Techno Hill (Act 1) Monitor - Knuckles Path Behind Pipe","Techno Hill (Act 1) Monitor - Deep in Slime Towards Factory","Techno Hill (Act 1) Monitor - Knuckles Path on Ledge",
        "Techno Hill (Act 1) Monitor - Knuckles Path High Ledge","Techno Hill (Act 1) Monitor - First Factory Back Ledge","Techno Hill (Act 1) Monitor - End of Knuckles Path in Flowers","Techno Hill (Act 1) Monitor - Knuckles Path on Pipes",
        "Techno Hill (Act 1) Monitor - On Top of Piston Near End","Techno Hill (Act 1) Monitor - Before End on Crates","Techno Hill (Act 1) Monitor - Knuckles Path in Slime","Techno Hill (Act 1) Monitor - In Slime Near 2nd Checkpoint",
        "Techno Hill (Act 1) Monitor - Factory Deep in Slime","Techno Hill (Act 1) Monitor - Ledge Above Start","Techno Hill (Act 1) Monitor - Alt Path on Machine","Techno Hill (Act 1) Monitor - High Above Slime Lake 1",
        "Techno Hill (Act 1) Monitor - Breakable Wall Ledge","Techno Hill (Act 1) Monitor - High Above Slime Lake 2","Techno Hill (Act 1) Monitor - Yellow Springs Near Start","Techno Hill (Act 1) Monitor - Upper Path on Ledge",
        "Techno Hill (Act 1) Monitor - Upper Path Spring Corner","Techno Hill (Act 1) Monitor - First Factory in Slime","Techno Hill (Act 1) Monitor - Alt Path on Ledge 2","Techno Hill (Act 1) Monitor - In First Slime River",
        "Techno Hill (Act 1) Monitor - Deep in 2nd Slime River","Techno Hill (Act 1) Monitor - Upper Path Around Corner","Techno Hill (Act 1) Monitor - Highest Ledge Above Slime Lake","Techno Hill (Act 1) Monitor - Alt Path on Pillar",
        )

        create_locs(regTHZ2,
        "Techno Hill (Act 2) Monitor - Knuckles Path Before Diagonal Conveyors","Techno Hill (Act 2) Monitor - Behind Breakable Wall Near Start")

        create_locs(regTHZ2M,"Techno Hill (Act 2) Monitor - Knuckles Path Exit 1","Techno Hill (Act 2) Monitor - Knuckles Path Exit 2","Techno Hill (Act 2) Monitor - Barricade Path Under 1st Conveyor",
        "Techno Hill (Act 2) Monitor - Barricade Path End Ledge 1","Techno Hill (Act 2) Monitor - Barricade Path Cavity 1st Checkpoint","Techno Hill (Act 2) Monitor - Knuckles Path Metal Pillar",
        "Techno Hill (Act 2) Monitor - High Ledge Outside 2","Techno Hill (Act 2) Monitor - High Ledge Outside 3","Techno Hill (Act 2) Monitor - Piston Room High Ledge 1",
        "Techno Hill (Act 2) Monitor - Piston Room High Ledge 2","Techno Hill (Act 2) Monitor - Large Jump Into Slime S", "Techno Hill (Act 2) Monitor - Barricade Path End Ledge 2",
        "Techno Hill (Act 2) Monitor - Large Jump Into Slime W","Techno Hill (Act 2) Monitor - Outside Heart Emblem Door","Techno Hill (Act 2) Monitor - Large Jump Into Slime N",
        "Techno Hill (Act 2) Monitor - Behind Crates After 3rd Checkpoint","Techno Hill (Act 2) Monitor - Final Room Cavity in Pillar",
        "Techno Hill (Act 2) Monitor - Before Detons Behind Crates","Techno Hill (Act 2) Monitor - Near Heart Emblem 1","Techno Hill (Act 2) Monitor - Deton Room Behind Crate",
        "Techno Hill (Act 2) Monitor - Near Heart Emblem 2","Techno Hill (Act 2) Monitor - Egg Corp High Glass Platform",
        "Techno Hill (Act 2) Monitor - Egg Corp Upper Cavity Around Corner","Techno Hill (Act 2) Monitor - Egg Corp Under Slime W","Techno Hill (Act 2) Monitor - Egg Corp Under Slime E",
        "Techno Hill (Act 2) Monitor - Egg Corp Under Slime N","Techno Hill (Act 2) Monitor - Egg Corp Under Slime S","Techno Hill (Act 2) Monitor - After Turret Room Under Slime",
        "Techno Hill (Act 2) Monitor - Large Jump Into Slime E","Techno Hill (Act 2) Monitor - Near Club Emblem 1","Techno Hill (Act 2) Monitor - Near Club Emblem 2",
        "Techno Hill (Act 2) Monitor - Final Room Under Slime","Techno Hill (Act 2) Monitor - Before 2nd Checkpoint Breakable Wall L","Techno Hill (Act 2) Monitor - Before 2nd Checkpoint Breakable Wall R",
        "Techno Hill (Act 2) Monitor - Barricade Path on Crate","Techno Hill (Act 2) Monitor - Near Heart Emblem 3","Techno Hill (Act 2) Monitor - Final Room Behind Pipe",
        "Techno Hill (Act 2) Monitor - Near Diamond Emblem 1","Techno Hill (Act 2) Monitor - Near Diamond Emblem 2")

    regDSZ1 = create_region("Deep Sea Zone 1", player, world)
    regDSZ2 = create_region("Deep Sea Zone 2", player, world)
    regDSZ3 = create_region("Deep Sea Zone 3", player, world)

    create_locs(regDSZ1, "Deep Sea (Act 1) Star Emblem", "Deep Sea (Act 1) Spade Emblem","Deep Sea (Act 1) Heart Emblem", "Deep Sea (Act 1) Diamond Emblem","Deep Sea (Act 1) Club Emblem",
                        "Deep Sea (Act 1) Clear","Deep Sea (Act 1) Emerald Token - V on Right Path","Deep Sea (Act 1) Emerald Token - Underwater Air Pocket on Right Path",
                    "Deep Sea (Act 1) Emerald Token - Yellow Doors","Deep Sea (Act 1) Emerald Token - Large Underwater Curve", "Deep Sea (Act 1) Emerald Token - Waterslide Gargoyles")
    create_locs(regDSZ2, "Deep Sea (Act 2) Star Emblem", "Deep Sea (Act 2) Spade Emblem", "Deep Sea (Act 2) Heart Emblem", "Deep Sea (Act 2) Diamond Emblem",
                            "Deep Sea (Act 2) Club Emblem","Deep Sea (Act 2) Clear", "Deep Sea (Act 2) Emerald Token - Near Heart Emblem",
                            "Deep Sea (Act 2) Emerald Token - Red and Yellow Springs", "Deep Sea (Act 2) Emerald Token - Down Right From Goal", "Deep Sea (Act 2) Emerald Token - No Spin Spring Turnaround")
    create_locs(regDSZ3,"Deep Sea (Act 3) Clear")
    if options.time_emblems:
        create_locs(regDSZ1, "Deep Sea (Act 1) Time Emblem")
        create_locs(regDSZ2,"Deep Sea (Act 2) Time Emblem")
        create_locs(regDSZ3,"Deep Sea (Act 3) Time Emblem")
    if options.ring_emblems:
        create_locs(regDSZ1, "Deep Sea (Act 1) Ring Emblem")
        create_locs(regDSZ2,"Deep Sea (Act 2) Ring Emblem")
    if options.score_emblems:
        create_locs(regDSZ3, "Deep Sea (Act 3) Score Emblem")
    if options.oneup_sanity:
        create_locs(regDSZ1,"Deep Sea (Act 1) Monitor - Left Path First Water Around Corner","Deep Sea (Act 1) Monitor - Right Lower Route Sloped Ledge",
        "Deep Sea (Act 1) Monitor - Heart Emblem Backtrack to Club 1","Deep Sea (Act 1) Monitor - Sinking Pillar Button 1","Deep Sea (Act 1) Monitor - Near Waterslide Emerald Token",
        "Deep Sea (Act 1) Monitor - Purple Switch","Deep Sea (Act 1) Monitor - Left Path Tall Pillar After Waterslides","Deep Sea (Act 1) Monitor - Right Path Under Hidden Elevator",
        "Deep Sea (Act 1) Monitor - Waterfall Cave Opposite Spade Emblem","Deep Sea (Act 1) Monitor - Heart Emblem Backtrack to Club 2","Deep Sea (Act 1) Monitor - Broken Wall Near End",
        "Deep Sea (Act 1) Monitor - Yellow Switch","Deep Sea (Act 1) Monitor - Behind Fast Closing Door 1","Deep Sea (Act 1) Monitor - Behind Fast Closing Door 2",
        "Deep Sea (Act 1) Monitor - Waterfall Cave Near Cyan Door","Deep Sea (Act 1) Monitor - Near Diamond Emblem","Deep Sea (Act 1) Monitor - Right Right Subpath Breakable Wall Between Columns",
        "Deep Sea (Act 1) Monitor - Left Path Behind Cyan Door","Deep Sea (Act 1) Monitor - Waterslide Hidden Spring Room","Deep Sea (Act 1) Monitor - Behind Fast Closing Door 1",
        "Deep Sea (Act 1) Monitor - Behind Fast Closing Door 2")

        create_locs(regDSZ2,"Deep Sea (Act 2) Monitor - Spindash Fast Door 1",
        "Deep Sea (Act 2) Monitor - Gargoyle Path Wall Under Oval Platform", "Deep Sea (Act 2) Monitor - Spindash Fast Door 2", "Deep Sea (Act 2) Monitor - Knuckles Path Dark High Ledge",
        "Deep Sea (Act 2) Monitor - Knuckles Path Crushing Ceiling", "Deep Sea (Act 2) Monitor - Left Ledge Near End", "Deep Sea (Act 2) Monitor - Gargoyle Path Underwater Crack Behind Plants",
        "Deep Sea (Act 2) Monitor - Near Club Emblem", "Deep Sea (Act 2) Monitor - Gargoyle Path Inside 3rd Rising Pillar", "Deep Sea (Act 2) Monitor - Gargoyle Path Behind Periodic Waterfall",
        "Deep Sea (Act 2) Monitor - Main Path Roll Down Ramp Into Breakable Wall", "Deep Sea (Act 2) Monitor - Gargoyle Path Spiked Cliff Top", "Deep Sea (Act 2) Monitor - Waterslide Fail 2nd Jump",
        "Deep Sea (Act 2) Monitor - Waterslide Avoid Wall Spikes", "Deep Sea (Act 2) Monitor - Spindash Fast Door 3")



    if options.superring_sanity:
        create_locs(regDSZ1,"Deep Sea (Act 1) Monitor - Underwater After Red Spring Jump","Deep Sea (Act 1) Monitor - Right Path Beside Elevator",
"Deep Sea (Act 1) Monitor - Sinking Pillar Button 2","Deep Sea (Act 1) Monitor - Left Path Underwater Switch 1","Deep Sea (Act 1) Monitor - Left Path Underwater Switch 2",
"Deep Sea (Act 1) Monitor - Sinking Pillar Button 3","Deep Sea (Act 1) Monitor - Right Lower Route Under Sloped Ledge","Deep Sea (Act 1) Monitor - Below Star Emblem",
"Deep Sea (Act 1) Monitor - Left Path Ledge Over Water","Deep Sea (Act 1) Monitor - Right Path Underwater 1","Deep Sea (Act 1) Monitor - Right Path Underwater 2",
"Deep Sea (Act 1) Monitor - Left Path Shallow Water","Deep Sea (Act 1) Monitor - Right Right Subpath Merge Underwater 1","Deep Sea (Act 1) Monitor - Right Right Subpath Merge Underwater 2",
"Deep Sea (Act 1) Monitor - Left Path Behind Rubble","Deep Sea (Act 1) Monitor - Right Lower Path Before Broken Door","Deep Sea (Act 1) Monitor - After Waterslide",
"Deep Sea (Act 1) Monitor - Before End Behind Pillar","Deep Sea (Act 1) Monitor - Right Ending Path on Rocks","Deep Sea (Act 1) Monitor - Right Right Subpath High Rock Alcove",
"Deep Sea (Act 1) Monitor - Pillar Button Path Behind First Gargoyle","Deep Sea (Act 1) Monitor - Left Path Behind Waterslide Start","Deep Sea (Act 1) Monitor - Left Ending Path High on Rocks",
"Deep Sea (Act 1) Monitor - Right Path First Arch Top","Deep Sea (Act 1) Monitor - Right Ending Path Near Floating Mines","Deep Sea (Act 1) Monitor - Underwater Curve Cave on Rock",
"Deep Sea (Act 1) Monitor - Near End Behind Rubble","Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 1","Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 2",
"Deep Sea (Act 1) Monitor - Left Path Underwater Near Waterslide","Deep Sea (Act 1) Monitor - Red Spring Jump Left","Deep Sea (Act 1) Monitor - After Waterslide Underwater Around Corner",
"Deep Sea (Act 1) Monitor - Join Right Lower Route Underwater Wall Bottom","Deep Sea (Act 1) Monitor - Right Right Subpath Inside Waterfall")



        create_locs(regDSZ2,"Deep Sea (Act 2) Monitor - Right Waterslide Path Cave","Deep Sea (Act 2) Monitor - Left Ledge After Start","Deep Sea (Act 2) Monitor - Diagonal Pillars Near Spring Emerald Token",
"Deep Sea (Act 2) Monitor - Nospin Path Before Final Gate","Deep Sea (Act 2) Monitor - Main Path Pillars Behind Plants","Deep Sea (Act 2) Monitor - Main Path Pillars Gargoyle Ledge",
"Deep Sea (Act 2) Monitor - Main Path Behind First Right Plants","Deep Sea (Act 2) Monitor - Nospin Path Behind First Plants","Deep Sea (Act 2) Monitor - Fast Closing Door Front",
"Deep Sea (Act 2) Monitor - Underwater Before Final Waterslide","Deep Sea (Act 2) Monitor - Gargoyle Path Block in Water","Deep Sea (Act 2) Monitor - Gargoyle Path on Pillar",
"Deep Sea (Act 2) Monitor - Down Right From Goal on Rocky Ledge","Deep Sea (Act 2) Monitor - Gargoyle Path Spiked Pillar","Deep Sea (Act 2) Monitor - Gargoyle Path Behind Doors 1",
"Deep Sea (Act 2) Monitor - Gargoyle Path Behind Doors 2","Deep Sea (Act 2) Monitor - Cliffside Near Red Button","Deep Sea (Act 2) Monitor - Right Waterslide Path Switch Secret 1",
"Deep Sea (Act 2) Monitor - Right Waterslide Path Switch Secret 2","Deep Sea (Act 2) Monitor - Fountain Near Oval Platform","Deep Sea (Act 2) Monitor - Main Path Before Crushing Blocks",
"Deep Sea (Act 2) Monitor - Behind Plants Near End","Deep Sea (Act 2) Monitor - Before End 1","Deep Sea (Act 2) Monitor - Before End 2",
"Deep Sea (Act 2) Monitor - Crushing Ceiling Side 1","Deep Sea (Act 2) Monitor - Crushing Ceiling Side 2","Deep Sea (Act 2) Monitor - Down Right From Goal Underwater Cave",
"Deep Sea (Act 2) Monitor - Nospin Path Behind Spring Button Door 1","Deep Sea (Act 2) Monitor - Nospin Path Behind Spring Button Door 2","Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner L1",
"Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner R1","Deep Sea (Act 2) Monitor - Rising Water Platforms 1","Deep Sea (Act 2) Monitor - Rising Water Platforms 2",
"Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner R2","Deep Sea (Act 2) Monitor - Gargoyle Path Stalagmite Cave","Deep Sea (Act 2) Monitor - Gargoyle Path Pillar Between Gap",
"Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner L2","Deep Sea (Act 2) Monitor - Gargoyle Path After Rising Pillars Behind Plants")


    regCEZ1 = create_region("Castle Eggman Zone 1", player, world)
    regCEZ2 = create_region("Castle Eggman Zone 2", player, world)
    regCEZ3 = create_region("Castle Eggman Zone 3", player, world)
    create_locs(regCEZ1, "Castle Eggman (Act 1) Star Emblem", "Castle Eggman (Act 1) Spade Emblem", "Castle Eggman (Act 1) Heart Emblem", "Castle Eggman (Act 1) Diamond Emblem",
                "Castle Eggman (Act 1) Club Emblem", "Castle Eggman (Act 1) Clear","Castle Eggman (Act 1) Emerald Token - Behind Fence Near Start",
                "Castle Eggman (Act 1) Emerald Token - Spring Side Path","Castle Eggman (Act 1) Emerald Token - Inside Castle")

    create_locs(regCEZ2,"Castle Eggman (Act 2) Star Emblem", "Castle Eggman (Act 2) Spade Emblem", "Castle Eggman (Act 2) Heart Emblem", "Castle Eggman (Act 2) Diamond Emblem",
    "Castle Eggman (Act 2) Club Emblem","Castle Eggman (Act 2) Clear","Castle Eggman (Act 2) Emerald Token - First Outside Area","Castle Eggman (Act 2) Emerald Token - Corner of Right Courtyard",
    "Castle Eggman (Act 2) Emerald Token - Back Window of Left Courtyard","Castle Eggman (Act 2) Emerald Token - Spring Near Club Emblem","Castle Eggman (Act 2) Emerald Token - High Ledge Before Final Tower")

    create_locs(regCEZ3, "Castle Eggman (Act 3) Clear")
    if options.time_emblems:
        create_locs(regCEZ1, "Castle Eggman (Act 1) Time Emblem")
        create_locs(regCEZ2, "Castle Eggman (Act 2) Time Emblem")
        create_locs(regCEZ3, "Castle Eggman (Act 3) Time Emblem")
    if options.ring_emblems:
        create_locs(regCEZ1, "Castle Eggman (Act 1) Ring Emblem")
        create_locs(regCEZ2, "Castle Eggman (Act 2) Ring Emblem")
    if options.score_emblems:
        create_locs(regCEZ3, "Castle Eggman (Act 3) Score Emblem")
    if options.oneup_sanity:
        create_locs(regCEZ1,"Castle Eggman (Act 1) Monitor - Mud Path on Side Wall","Castle Eggman (Act 1) Monitor - Outside Bars First Tall Castle Wall",
        "Castle Eggman (Act 1) Monitor - Second Area Behind Overgrown Bars","Castle Eggman (Act 1) Monitor - Near Spade Emblem 1","Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 1",
        "Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 1","Castle Eggman (Act 1) Monitor - Main Path Sloped Spring Jumps","Castle Eggman (Act 1) Monitor - Bonfire Area Behind Tall Pillar",
        "Castle Eggman (Act 1) Monitor - Red Spring Path First Turnaround","Castle Eggman (Act 1) Monitor - Red Spring Path Pillar With Robo-Hoods")

        create_locs(regCEZ2,"Castle Eggman (Act 2) Monitor - Rafter Above Starting Area",
        "Castle Eggman (Act 2) Monitor - Front Left Path High Above Water","Castle Eggman (Act 2) Monitor - High Bookshelf Before Final Tower","Castle Eggman (Act 2) Monitor - Under Bridge Near 3rd Checkpoint",
        "Castle Eggman (Act 2) Monitor - Front Left Path High Ledge Before Swinging Chains","Castle Eggman (Act 2) Monitor - Bookshelf in Spike Pit Before Final Tower","Castle Eggman (Act 2) Monitor - First Top Path Hidden Ground Spring",
        "Castle Eggman (Act 2) Monitor - First Outside Area Pillar Near Star Emblem","Castle Eggman (Act 2) Monitor - Miss Red Springs Before 4th Checkpoint","Castle Eggman (Act 2) Monitor - Right Courtyard Corner Near Swinging Mace",
        "Castle Eggman (Act 2) Monitor - Rocky Ledge Opposite Club Emblem","Castle Eggman (Act 2) Monitor - Window of Left Courtyard","Castle Eggman (Act 2) Monitor - Left Path Mace Launch Side Corridor",
        "Castle Eggman (Act 2) Monitor - Right Path Thin Gray Bookshelf Top")

    if options.superring_sanity:
        create_locs(regCEZ1,"Castle Eggman (Act 1) Monitor - Lower Main Path Before Tilted Maces","Castle Eggman (Act 1) Monitor - Near Spade Emblem 2",
        "Castle Eggman (Act 1) Monitor - Near Spade Emblem 3","Castle Eggman (Act 1) Monitor - Left Path Cliff 1","Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 2",
        "Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 3","Castle Eggman (Act 1) Monitor - Titled Maces Cave 1","Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 2",
        "Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 3","Castle Eggman (Act 1) Monitor - Main Path Tree Ledge","Castle Eggman (Act 1) Monitor - Breakable Stone Near Start",
        "Castle Eggman (Act 1) Monitor - Trees Near Final Checkpoint","Castle Eggman (Act 1) Monitor - Titled Maces Cave 2","Castle Eggman (Act 1) Monitor - Wall Path Breakable Stone 1",
        "Castle Eggman (Act 1) Monitor - Final Checkpoint R","Castle Eggman (Act 1) Monitor - Final Checkpoint L","Castle Eggman (Act 1) Monitor - Red Spring Path Start Behind Tree",
        "Castle Eggman (Act 1) Monitor - Near Star Emblem 1","Castle Eggman (Act 1) Monitor - Near Star Emblem 2","Castle Eggman (Act 1) Monitor - First Swinging Mace Jump 1",
        "Castle Eggman (Act 1) Monitor - First Swinging Mace Jump 2","Castle Eggman (Act 1) Monitor - Wall Mace Cave Bottom","Castle Eggman (Act 1) Monitor - First Checkpoint Ring Circle",
        "Castle Eggman (Act 1) Monitor - Wall Path Breakable Stone 2","Castle Eggman (Act 1) Monitor - Corner Behind 2nd Checkpoint","Castle Eggman (Act 1) Monitor - Corner After Lower First Checkpoint",
        "Castle Eggman (Act 1) Monitor - Before Lower First Checkpoint","Castle Eggman (Act 1) Monitor - Alcove In First Mud Pit","Castle Eggman (Act 1) Monitor - Mud Path First Pit 1",
        "Castle Eggman (Act 1) Monitor - Mud Path First Pit 2","Castle Eggman (Act 1) Monitor - Near Club Emblem 1","Castle Eggman (Act 1) Monitor - Near Club Emblem 2",
        "Castle Eggman (Act 1) Monitor - Red Spring Path Second Turnaround","Castle Eggman (Act 1) Monitor - Red Spring Path On Slope","Castle Eggman (Act 1) Monitor - Left Path Cliff 2")
        create_locs(regCEZ2,"Castle Eggman (Act 2) Monitor - First Top Path Near Platforms","Castle Eggman (Act 2) Monitor - Outside Path Start",
        "Castle Eggman (Act 2) Monitor - Behind First Eggman Statue","Castle Eggman (Act 2) Monitor - First Top Path Stay On Platforms 1","Castle Eggman (Act 2) Monitor - First Spiked Mace Pit",
        "Castle Eggman (Act 2) Monitor - Left Courtyard Behind Wood Pillar","Castle Eggman (Act 2) Monitor - First Courtyard Behind Fountain","Castle Eggman (Act 2) Monitor - Gray Bookshelf Near Final Tower Token",
        "Castle Eggman (Act 2) Monitor - Below Right Courtyard Token","Castle Eggman (Act 2) Monitor - Before Final Tower Spike Pit Around Corner","Castle Eggman (Act 2) Monitor - Before Final Tower Spike Pit Under Ledge",
        "Castle Eggman (Act 2) Monitor - Pillar After Side Mace Launch 1","Castle Eggman (Act 2) Monitor - First Top Path Stay On Platforms 2","Castle Eggman (Act 2) Monitor - Near Club Emblem",
        "Castle Eggman (Act 2) Monitor - Behind Springs After Outside Path","Castle Eggman (Act 2) Monitor - Right Courtyard Back Left Corner","Castle Eggman (Act 2) Monitor - First Courtyard Front Right Corner",
        "Castle Eggman (Act 2) Monitor - Outside Path Near Spiked Maces","Castle Eggman (Act 2) Monitor - Left Courtyard Back Left Corner","Castle Eggman (Act 2) Monitor - Left After Floor Trap",
        "Castle Eggman (Act 2) Monitor - Left Courtyard Front Pillar","Castle Eggman (Act 2) Monitor - Left Courtyard Bottom Right Corner","Castle Eggman (Act 2) Monitor - Left Side Before Swinging Mace Launch",
        "Castle Eggman (Act 2) Monitor - First Top Path Falling Floor","Castle Eggman (Act 2) Monitor - Grass Room Spike Ball Stuck In Tree","Castle Eggman (Act 2) Monitor - Right Library Cracked Statue Base",
        "Castle Eggman (Act 2) Monitor - Left Library Bookshelf Between Pillars 1","Castle Eggman (Act 2) Monitor - Pillar After Side Mace Launch 2","Castle Eggman (Act 2) Monitor - First Courtyard Back Left Corner",
        "Castle Eggman (Act 2) Monitor - Left Library First Spike Pit","Castle Eggman (Act 2) Monitor - Grass Room Small Tree Ledge","Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Cracked Stone",
        "Castle Eggman (Act 2) Monitor - Right Side Before Swinging Mace Launch","Castle Eggman (Act 2) Monitor - Above Library Entrance 1","Castle Eggman (Act 2) Monitor - Above Library Entrance 2",
        "Castle Eggman (Act 2) Monitor - Left Library Bookshelf Between Pillars 2","Castle Eggman (Act 2) Monitor - Cracked Brick Right Library Outside","Castle Eggman (Act 2) Monitor - Right Library Moving Platforms Left Bookshelf",
        "Castle Eggman (Act 2) Monitor - Right Library Moving Platforms Right Bookshelf","Castle Eggman (Act 2) Monitor - Right Library Fake Statue","Castle Eggman (Act 2) Monitor - Side Mace Launch Right",
        "Castle Eggman (Act 2) Monitor - Side Mace Launch Left","Castle Eggman (Act 2) Monitor - Right Courtyard Square Pillar In Grass","Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Miss Jump 1",
        "Castle Eggman (Act 2) Monitor - Before First Courtyard Right Hallway","Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Miss Jump 2","Castle Eggman (Act 2) Monitor - Grass Room Spike Pit Side Room",
        "Castle Eggman (Act 2) Monitor - First Courtyard Back Right Corner","Castle Eggman (Act 2) Monitor - Right Courtyard First Pillar")

    regACZ1 = create_region("Arid Canyon Zone 1", player, world)
    regACZ2 = create_region("Arid Canyon Zone 2", player, world)
    regACZ3 = create_region("Arid Canyon Zone 3", player, world)
    create_locs(regACZ1, "Arid Canyon (Act 1) Star Emblem", "Arid Canyon (Act 1) Spade Emblem", "Arid Canyon (Act 1) Heart Emblem", "Arid Canyon (Act 1) Diamond Emblem",
                "Arid Canyon (Act 1) Club Emblem","Arid Canyon (Act 1) Clear","Arid Canyon (Act 1) Emerald Token - Speed Shoes Central Pillar",
    "Arid Canyon (Act 1) Emerald Token - Behind Pillar Before Exploding Ramp","Arid Canyon (Act 1) Emerald Token - Behind Wall and Spikes")
    create_locs(regACZ2, "Arid Canyon (Act 2) Star Emblem", "Arid Canyon (Act 2) Spade Emblem", "Arid Canyon (Act 2) Heart Emblem", "Arid Canyon (Act 2) Diamond Emblem","Arid Canyon (Act 2) Emerald Token - Left No Spin Path Minecarts",
    "Arid Canyon (Act 2) Emerald Token - Large Arch Cave Right Ledge","Arid Canyon (Act 2) Emerald Token - Knuckles Dark Path Around Wall",
    "Arid Canyon (Act 2) Club Emblem","Arid Canyon (Act 2) Clear")
    create_locs(regACZ3, "Arid Canyon (Act 3) Clear")
    if options.time_emblems:
        create_locs(regACZ1, "Arid Canyon (Act 1) Time Emblem")
        create_locs(regACZ2, "Arid Canyon (Act 2) Time Emblem")
        create_locs(regACZ3, "Arid Canyon (Act 3) Time Emblem")
    if options.ring_emblems:
        create_locs(regACZ1, "Arid Canyon (Act 1) Ring Emblem")
        create_locs(regACZ2, "Arid Canyon (Act 2) Ring Emblem")
    if options.score_emblems:
        create_locs(regACZ3, "Arid Canyon (Act 3) Score Emblem")
    if options.oneup_sanity:
        create_locs(regACZ1,"Arid Canyon (Act 1) Monitor - Top Plank Before Path Split","Arid Canyon (Act 1) Monitor - Cave Below First House","Arid Canyon (Act 1) Monitor - Main Area High Broken Road",
        "Arid Canyon (Act 1) Monitor - End of Sneakers Path Brown Pillar","Arid Canyon (Act 1) Monitor - TNT Path High Above Exploding Plank","Arid Canyon (Act 1) Monitor - Sneakers Path Stone Pillar Ramp",
    "Arid Canyon (Act 1) Monitor - Near Amy Emerald Token","Arid Canyon (Act 1) Monitor - High Ledge Above Start","Arid Canyon (Act 1) Monitor - Final Section Under Ceiling Near Checkpoint",
    "Arid Canyon (Act 1) Monitor - End of TNT Path Above Cave")

        create_locs(regACZ2,"Arid Canyon (Act 2) Monitor - Left Path Moving Platform Knuckles Wall","Arid Canyon (Act 2) Monitor - High Ledge Near Start",
    "Arid Canyon (Act 2) Monitor - Left Path End of Collapsing Plank","Arid Canyon (Act 2) Monitor - Large Arch Cave Thin Planks Right Side","Arid Canyon (Act 2) Monitor - Left Cliffside Ledge From Start",
    "Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top Middle","Arid Canyon (Act 2) Monitor - Looping Path Tall Brown Rock Pillar","Arid Canyon (Act 2) Monitor - Looping Path Small Cave High Up",
    "Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 1","Arid Canyon (Act 2) Monitor - Looping Path Low Ledge in Cave","Arid Canyon (Act 2) Monitor - Left Path High Ledge Cave",
    "Arid Canyon (Act 2) Monitor - Left Path Visible From Minecarts","Arid Canyon (Act 2) Monitor - Near Heart Emblem 1","Arid Canyon (Act 2) Monitor - Behind TNT Crates Near Diamond Emblem",
    "Arid Canyon (Act 2) Monitor - Ending Minecarts","Arid Canyon (Act 2) Monitor - Very High Ledge Between Left and Looping Path","Arid Canyon (Act 2) Monitor - TNT Barrel Ledge Near Star Emblem")

    if options.superring_sanity:
        create_locs(regACZ1,"Arid Canyon (Act 1) Monitor - First House","Arid Canyon (Act 1) Monitor - Knuckles Path Before Climb 1",
        "Arid Canyon (Act 1) Monitor - Main Area High Near Broken Road 1","Arid Canyon (Act 1) Monitor - Main Area High Near Broken Road 2","Arid Canyon (Act 1) Monitor - Main Area Small Crates",
        "Arid Canyon (Act 1) Monitor - Main Path Ledge Near Rope Hangs","Arid Canyon (Act 1) Monitor - TNT Path Near Exploding Ramp","Arid Canyon (Act 1) Monitor - Second House",
        "Arid Canyon (Act 1) Monitor - First Rock","Arid Canyon (Act 1) Monitor - Main Area Ledge After Plank 1","Arid Canyon (Act 1) Monitor - Under Road Before Heart Emblem",
        "Arid Canyon (Act 1) Monitor - Near Spade Emblem","Arid Canyon (Act 1) Monitor - Knuckles Path Around Corner","Arid Canyon (Act 1) Monitor - TNT Path High Ledge Before Exploding Ramp 1",
        "Arid Canyon (Act 1) Monitor - Knuckles Path Before Climb 2","Arid Canyon (Act 1) Monitor - TNT Path High Ledge Before Exploding Ramp 2","Arid Canyon (Act 1) Monitor - High Ledge Before First Path Split",
        "Arid Canyon (Act 1) Monitor - Main Area Ledge After Plank 2","Arid Canyon (Act 1) Monitor - TNT Path Behind Large Crate","Arid Canyon (Act 1) Monitor - Behind First Crate",
        "Arid Canyon (Act 1) Monitor - Nospin Path Behind Cacti","Arid Canyon (Act 1) Monitor - Main Area Miss Spring 1","Arid Canyon (Act 1) Monitor - Main Area Miss Spring 2",
        "Arid Canyon (Act 1) Monitor - Main Area Miss Spring 3","Arid Canyon (Act 1) Monitor - Main Path Wagon Wheel","Arid Canyon (Act 1) Monitor - Entrance Road To Knuckles Path",
        "Arid Canyon (Act 1) Monitor - Right Path Cave Behind Crates","Arid Canyon (Act 1) Monitor - Behind Cacti Near Falling Anvil","Arid Canyon (Act 1) Monitor - Behind Cacti End of TNT Path")
        create_locs(regACZ2,"Arid Canyon (Act 2) Monitor - Left Path Under Collapsing Plank","Arid Canyon (Act 2) Monitor - Left Path Second Platform",
        "Arid Canyon (Act 2) Monitor - Behind Plank Near Diamond Emblem","Arid Canyon (Act 2) Monitor - First Crate","Arid Canyon (Act 2) Monitor - Looping Path Low Ledge Behind Cacti",
        "Arid Canyon (Act 2) Monitor - Large Arch Cave Gap After Spikes","Arid Canyon (Act 2) Monitor - Large Arch Cave TNT Behind Crates","Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top 1",
        "Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top 2","Arid Canyon (Act 2) Monitor - Behind Crate Near Spade Emblem","Arid Canyon (Act 2) Monitor - TNT Barrels Near Star Emblem",
        "Arid Canyon (Act 2) Monitor - Canarivore Path Before Ramp 1","Arid Canyon (Act 2) Monitor - Canarivore Path Before Ramp 2","Arid Canyon (Act 2) Monitor - Left Path Tall Plank",
        "Arid Canyon (Act 2) Monitor - Looping Path Side Ledge 1","Arid Canyon (Act 2) Monitor - Looping Path Side Ledge 2","Arid Canyon (Act 2) Monitor - Large Arch Cave Middle Crates",
        "Arid Canyon (Act 2) Monitor - Below Heart Emblem Area","Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 2","Arid Canyon (Act 2) Monitor - Near Heart Emblem 2",
        "Arid Canyon (Act 2) Monitor - Near Heart Emblem 3","Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 3","Arid Canyon (Act 2) Monitor - Left Knuckles Path Back Ledge 1",
        "Arid Canyon (Act 2) Monitor - Left Knuckles Path Back Ledge 2","Arid Canyon (Act 2) Monitor - Left Knuckles Path Main Platform","Arid Canyon (Act 2) Monitor - Nospin Path After First Minecart 1",
        "Arid Canyon (Act 2) Monitor - Looping Path Ledge Near Rock","Arid Canyon (Act 2) Monitor - Near Arch Cave Token 1","Arid Canyon (Act 2) Monitor - Near Arch Cave Token 2",
        "Arid Canyon (Act 2) Monitor - Right Ledge Near Start","Arid Canyon (Act 2) Monitor - Nospin Path Before Second Minecart","Arid Canyon (Act 2) Monitor - Left Path Behind TNT Near End 1",
        "Arid Canyon (Act 2) Monitor - Left Path Behind TNT Near End 2","Arid Canyon (Act 2) Monitor - Left Path Near Wooden Bridge","Arid Canyon (Act 2) Monitor - Left Path Alternate Rail",
        "Arid Canyon (Act 2) Monitor - Nospin Path After First Minecart 2","Arid Canyon (Act 2) Monitor - Left Path Small Ledge Under Heart Emblem","Arid Canyon (Act 2) Monitor - Left Path Climb Wooden Spring Ladder",
        "Arid Canyon (Act 2) Monitor - Canarivore Path Join Left Path Ledge","Arid Canyon (Act 2) Monitor - Large Arch Cave Guarded By Green Snapper","Arid Canyon (Act 2) Monitor - Crate Before Final Minecart")

    regRVZ1 = create_region("Red Volcano Zone 1", player, world)
    create_locs(regRVZ1, "Red Volcano (Act 1) Star Emblem", "Red Volcano (Act 1) Spade Emblem", "Red Volcano (Act 1) Heart Emblem", "Red Volcano (Act 1) Diamond Emblem",
                "Red Volcano (Act 1) Club Emblem","Red Volcano (Act 1) Clear","Red Volcano (Act 1) Emerald Token - First Outside Area","Red Volcano (Act 1) Emerald Token - Hidden Ledge Near 4th Checkpoint",
    "Red Volcano (Act 1) Emerald Token - Rollout Rock Lavafall","Red Volcano (Act 1) Emerald Token - Behind Ending Rocket")
    if options.time_emblems:
        create_locs(regRVZ1, "Red Volcano (Act 1) Time Emblem")
    if options.ring_emblems:
        create_locs(regRVZ1, "Red Volcano (Act 1) Ring Emblem")
    if options.oneup_sanity:
        create_locs(regRVZ1,"Red Volcano (Act 1) Monitor - Lava Waves Pillar","Red Volcano (Act 1) Monitor - Thin Ledge First Outside Area","Red Volcano (Act 1) Monitor - First Outside Cave",
        "Red Volcano (Act 1) Monitor - Whirlwind Path Cave Around Corner","Red Volcano (Act 1) Monitor - Right Path Rising Lava Room Ledge","Red Volcano (Act 1) Monitor - Flame Jets Room Ledge",
        "Red Volcano (Act 1) Monitor - Behind Pillar Near End","Red Volcano (Act 1) Monitor - Near Heart Emblem","Red Volcano (Act 1) Monitor - Thin Ledge Second Outside Area")
    if options.superring_sanity:
        create_locs(regRVZ1,"Red Volcano (Act 1) Monitor - First Ledge","Red Volcano (Act 1) Monitor - First Outside Area Under Stone Platform",
        "Red Volcano (Act 1) Monitor - First Outside Area Tall Middle Rock","Red Volcano (Act 1) Monitor - First Outside Area Lower Back Grass","Red Volcano (Act 1) Monitor - Right Path Ledge After Falling Platform 1",
        "Red Volcano (Act 1) Monitor - Main Path Low Ledge","Red Volcano (Act 1) Monitor - Right Path Ledge After Falling Platform 2","Red Volcano (Act 1) Monitor - Right Path Rising Lava Room Middle Ledge",
        "Red Volcano (Act 1) Monitor - Final Path Split Ledge","Red Volcano (Act 1) Monitor - Second Outside Area Right Ledge 1","Red Volcano (Act 1) Monitor - Near Lavafall Token 1",
        "Red Volcano (Act 1) Monitor - Near Lavafall Token 2","Red Volcano (Act 1) Monitor - Second Outside Area Right Ledge 2")

    regERZ1 = create_region("Egg Rock Zone 1", player, world)
    regERZ2 = create_region("Egg Rock Zone 2", player, world)
    create_locs(regERZ1, "Egg Rock (Act 1) Star Emblem", "Egg Rock (Act 1) Spade Emblem", "Egg Rock (Act 1) Heart Emblem", "Egg Rock (Act 1) Diamond Emblem",
                "Egg Rock (Act 1) Club Emblem","Egg Rock (Act 1) Clear","Egg Rock (Act 1) Emerald Token - Gravity Conveyor Belts",
    "Egg Rock (Act 1) Emerald Token - Moving Platforms")



    create_locs(regERZ2, "Egg Rock (Act 2) Star Emblem", "Egg Rock (Act 2) Spade Emblem", "Egg Rock (Act 2) Heart Emblem", "Egg Rock (Act 2) Diamond Emblem","Egg Rock (Act 2) Clear",
    "Egg Rock (Act 2) Club Emblem","Egg Rock (Act 2) Emerald Token - Outside on Metal Beam","Egg Rock (Act 2) Emerald Token - Skip Gravity Pad",
    "Egg Rock (Act 2) Emerald Token - Disco Room")
    if options.time_emblems:
        create_locs(regERZ1, "Egg Rock (Act 1) Time Emblem")
        create_locs(regERZ2, "Egg Rock (Act 2) Time Emblem")
    if options.ring_emblems:
        create_locs(regERZ1, "Egg Rock (Act 1) Ring Emblem")
        create_locs(regERZ2, "Egg Rock (Act 2) Ring Emblem")
    if options.oneup_sanity:
        create_locs(regERZ1,"Egg Rock (Act 1) Monitor - Spin Path Crushers Corner","Egg Rock (Act 1) Monitor - Spin Path Guarded by Spincushion",
        "Egg Rock (Act 1) Monitor - Near Diamond Emblem 1","Egg Rock (Act 1) Monitor - Tails Path in Lava","Egg Rock (Act 1) Monitor - Near Star Emblem 1",
        "Egg Rock (Act 1) Monitor - Near End Behind Blue Pillar","Egg Rock (Act 1) Monitor - Gravity Lava Room","Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 1")

        create_locs(regERZ2,"Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 1","Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 2","Egg Rock (Act 2) Monitor - Left Path Red Platform Corner",
        "Egg Rock (Act 2) Monitor - Left Path Behind Blue Pillars","Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 1","Egg Rock (Act 2) Monitor - Air Lock Room Small Ledge",
        "Egg Rock (Act 2) Monitor - Near Spade Emblem","Egg Rock (Act 2) Monitor - Near Star Emblem 1","Egg Rock (Act 2) Monitor - Top of Turret Room",
        "Egg Rock (Act 2) Monitor - Left Path Surrounded by Eggman Monitors","Egg Rock (Act 2) Monitor - Disco Room 1","Egg Rock (Act 2) Monitor - Disco Room 2",
        "Egg Rock (Act 2) Monitor - Skip Gravity Pad Near Token","Egg Rock (Act 2) Monitor - Right Path Below Outside Start")

    if options.superring_sanity:
        create_locs(regERZ1,"Egg Rock (Act 1) Monitor - Near Star Emblem 2","Egg Rock (Act 1) Monitor - Near Star Emblem 3",
        "Egg Rock (Act 1) Monitor - 2D Area Zoom Tube Top","Egg Rock (Act 1) Monitor - Blue Pillar Before End","Egg Rock (Act 1) Monitor - Main Path End 1",
        "Egg Rock (Act 1) Monitor - Behind Moving Lasers","Egg Rock (Act 1) Monitor - Spin Path Crushers R","Egg Rock (Act 1) Monitor - Spin Path Crushers L",
        "Egg Rock (Act 1) Monitor - Outside Air Pocket Near End","Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 2","Egg Rock (Act 1) Monitor - Appearing Blocks Area Corner",
        "Egg Rock (Act 1) Monitor - Spin Path Gravity Room","Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 3","Egg Rock (Act 1) Monitor - Near Diamond Emblem 2",
        "Egg Rock (Act 1) Monitor - Knuckles Path Before Wall Conveyors","Egg Rock (Act 1) Monitor - Metal Beam Before End","Egg Rock (Act 1) Monitor - Right Before End",
        "Egg Rock (Act 1) Monitor - Main Path End 2")
        create_locs(regERZ2,"Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 2","Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 3",
        "Egg Rock (Act 2) Monitor - 2D Area Outside Ledge 1","Egg Rock (Act 2) Monitor - 2D Area Second Zoom Tube Exit","Egg Rock (Act 2) Monitor - 2D Area Outside Ledge 2",
        "Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 3","Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 4","Egg Rock (Act 2) Monitor - 2D Area Low Ledge",
        "Egg Rock (Act 2) Monitor - Near Star Emblem 2","Egg Rock (Act 2) Monitor - Near Star Emblem 3","Egg Rock (Act 2) Monitor - Near Zoom Tube Before Final Teleporter",
        "Egg Rock (Act 2) Monitor - Elevator Shaft","Egg Rock (Act 2) Monitor - Turret Room Back Right","Egg Rock (Act 2) Monitor - Right Path Spike Pit",
        "Egg Rock (Act 2) Monitor - Left Path Outside First Checkpoint 1","Egg Rock (Act 2) Monitor - Left Path Outside First Checkpoint 2","Egg Rock (Act 2) Monitor - Auto Gravity Area Pop-up Turrets",
        "Egg Rock (Act 2) Monitor - Starting Area Corner","Egg Rock (Act 2) Monitor - Right Path First Outside Area Entrance","Egg Rock (Act 2) Monitor - Right Path Near Second Checkpoint 1",
        "Egg Rock (Act 2) Monitor - Right Path Near Second Checkpoint 2","Egg Rock (Act 2) Monitor - Turret Room Back Left","Egg Rock (Act 2) Monitor - Air Lock Room Floor")

    regBCZ1 = create_region("Black Core Zone 1", player, world)
    regBCZ2 = create_region("Black Core Zone 2", player, world)
    regBCZ3 = create_region("Black Core Zone 3", player, world)
    create_locs(regBCZ1, "Black Core (Act 1) Clear")
    create_locs(regBCZ2,"Black Core (Act 2) Clear")
    create_locs(regBCZ3,"Black Core (Act 3) Clear")
    if options.time_emblems:
        create_locs(regBCZ1, "Black Core (Act 1) Time Emblem")
        create_locs(regBCZ2, "Black Core (Act 2) Time Emblem")
        create_locs(regBCZ3, "Black Core (Act 3) Time Emblem")
    if options.ring_emblems:
        create_locs(regBCZ1, "Black Core (Act 1) Ring Emblem")
    if options.score_emblems:
        create_locs(regBCZ2, "Black Core (Act 2) Score Emblem")
        create_locs(regBCZ3,"Black Core (Act 3) Score Emblem")
    if options.oneup_sanity:
        create_locs(regBCZ1,"Black Core (Act 1) Monitor - Half Pillar Above Spike Gate","Black Core (Act 1) Monitor - Behind Arrow Sign")
        create_locs(regBCZ2,"Black Core (Act 2) Monitor - Behind Computers")


    regFHZ = create_region("Frozen Hillside Zone", player, world)
    create_locs(regFHZ, "Frozen Hillside Star Emblem", "Frozen Hillside Spade Emblem", "Frozen Hillside Heart Emblem", "Frozen Hillside Diamond Emblem",
                "Frozen Hillside Club Emblem","Frozen Hillside Clear")
    if options.time_emblems:
        create_locs(regFHZ, "Frozen Hillside Time Emblem")
    if options.ring_emblems:
        create_locs(regFHZ, "Frozen Hillside Ring Emblem")
    if options.oneup_sanity:
        create_locs(regFHZ,"Frozen Hillside Monitor - First Snow Field Behind Ice","Frozen Hillside Monitor - Final Path Ledge Behind Ice")

    if options.superring_sanity:
        create_locs(regFHZ,"Frozen Hillside Monitor - Ledge Near Start 1","Frozen Hillside Monitor - Ledge Near Start 2","Frozen Hillside Monitor - Lower Path Alcove",
"Frozen Hillside Monitor - Right Path Inside Ice","Frozen Hillside Monitor - Left Path Cave Ledge","Frozen Hillside Monitor - First Area Tall Pillar","Frozen Hillside Monitor - First Area Lake Ledge",
"Frozen Hillside Monitor - Left Path Flowing Snow Ledge","Frozen Hillside Monitor - Frozen Lake Middle Platform","Frozen Hillside Monitor - Right Path Flowing Snow Behind Pillar","Frozen Hillside Monitor - Right Path Flowing Snow Lower Ice",
"Frozen Hillside Monitor - Converging Paths Under Overhang")

    regPTZ = create_region("Pipe Towers Zone", player, world)
    create_locs(regPTZ, "Pipe Towers Star Emblem", "Pipe Towers Spade Emblem", "Pipe Towers Heart Emblem", "Pipe Towers Diamond Emblem",
                "Pipe Towers Club Emblem","Pipe Towers Clear")
    if options.time_emblems:
        create_locs(regPTZ, "Pipe Towers Time Emblem")
    if options.ring_emblems:
        create_locs(regPTZ, "Pipe Towers Ring Emblem")
    if options.oneup_sanity:
        create_locs(regPTZ,"Pipe Towers ? Block - Above Start","Pipe Towers ? Block - Purple Mushroom Skylight","Pipe Towers ? Block - Ceiling Hole Near Flowing Water",
                "Pipe Towers ? Block - Near Diamond Emblem","Pipe Towers ? Block - Flowing Water Alt Path on Ledge","Pipe Towers ? Block - Underground Thwomp Room")
    regFFZ = create_region("Forest Fortress Zone", player, world)
    create_locs(regFFZ, "Forest Fortress Star Emblem", "Forest Fortress Spade Emblem", "Forest Fortress Heart Emblem", "Forest Fortress Diamond Emblem",
                "Forest Fortress Club Emblem","Forest Fortress Clear")
    if options.time_emblems:
        create_locs(regFFZ, "Forest Fortress Time Emblem")
    if options.ring_emblems:
        create_locs(regFFZ, "Forest Fortress Ring Emblem")
    if options.oneup_sanity:
        create_locs(regFFZ,"Forest Fortress Monitor - Near Hanging Wood Bridge 1","Forest Fortress Monitor - High Ledge Before Second Checkpoint","Forest Fortress Monitor - Low Ledge Before Goal 1",
        "Forest Fortress Monitor - In Ceiling After Final Checkpoint","Forest Fortress Monitor - Trees Near Diamond Emblem")

    if options.superring_sanity:
        create_locs(regFFZ,"Forest Fortress Monitor - Ledge Near First Swinging Mace","Forest Fortress Monitor - Main Path Ring Circle","Forest Fortress Monitor - Near Hanging Wood Bridge 2",
    "Forest Fortress Monitor - Near Hanging Wood Bridge 3","Forest Fortress Monitor - Main Path Tree Pillar","Forest Fortress Monitor - First Castle Wall Near Water",
    "Forest Fortress Monitor - First Castle Wall Underwater","Forest Fortress Monitor - Castle Lake Ledge","Forest Fortress Monitor - Vertical Mace Jump Ledge",
    "Forest Fortress Monitor - Before Final Checkpoint","Forest Fortress Monitor - Low Ledge Before Goal 2","Forest Fortress Monitor - Low Ledge Before Goal 3",
    "Forest Fortress Monitor - Overgrown Ledge Right Path 1","Forest Fortress Monitor - Spike Room Near Yellow Spring","Forest Fortress Monitor - Near Club Emblem 1",
    "Forest Fortress Monitor - Near Club Emblem 2","Forest Fortress Monitor - Inside Tower Near End","Forest Fortress Monitor - Overgrown Ledge Right Path 2",
    "Forest Fortress Monitor - Before Final Spring Chain","Forest Fortress Monitor - Castle Lake Underwater","Forest Fortress Monitor - Tower Before Club Emblem")


    regFDZ = create_region("Final Demo Zone", player, world)
    create_locs(regFDZ, "Final Demo Clear","Final Demo Emerald Token - Greenflower (Act 1) Breakable Wall Near Bridge",
    "Final Demo Emerald Token - Greenflower (Act 2) Underwater Cave",
    "Final Demo Emerald Token - Greenflower (Act 2) Under Bridge Near End",
    "Final Demo Emerald Token - Techno Hill (Act 1) On Pipes",
    "Final Demo Emerald Token - Techno Hill (Act 1) Alt Path Fans",
    "Final Demo Emerald Token - Techno Hill (Act 2) Breakable Wall",
    "Final Demo Emerald Token - Techno Hill (Act 2) Under Poison Near End",
    "Final Demo Emerald Token - Castle Eggman (Act 1) Small Lake Near Start",
    "Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear",
    "Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers")
    if options.oneup_sanity:
        create_locs(regFDZ,"Final Demo Monitor - Greenflower (Act 1) Ledge After Main Bridge","Final Demo Monitor - Greenflower (Act 2) Skylight in 2nd Cave","Final Demo Monitor - Greenflower (Act 2) Open Area Small Cave",
"Final Demo Monitor - Techno Hill (Act 1) Barrels Across Poison Lake","Final Demo Monitor - Techno Hill (Act 2) Ledge Near End","Final Demo Monitor - Techno Hill (Act 2) In Poison Near End","Final Demo Monitor - Castle Eggman (Act 1) On Castle Wall",
"Final Demo Monitor - Castle Eggman (Act 1) Red Spring Secret Cave 1","Final Demo Monitor - Castle Eggman (Act 1) Red Spring Secret Cave 2","Final Demo Monitor - Castle Eggman (Act 1) High Ledge Near Start","Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 1",
"Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard on Platform 1","Final Demo Monitor - Red Volcano (Act 1) Start","Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 1","Final Demo Monitor - Red Volcano (Act 1) Cave Near Falling Platforms")

    if options.superring_sanity:
        create_locs(regFDZ,"Final Demo Monitor - Greenflower (Act 1) First Pillar","Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 1","Final Demo Monitor - Greenflower (Act 1) Bridge Lake Top Ledge",
"Final Demo Monitor - Greenflower (Act 1) Floating Thok Barrier Ledge","Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 2","Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 3",
"Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 1","Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 2","Final Demo Monitor - Greenflower (Act 2) Main Path Near Springs",
        "Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1","Final Demo Monitor - Greenflower (Act 2) Very High Alcove 2","Final Demo Monitor - Greenflower (Act 2) Very High Alcove 3",
        "Final Demo Monitor - Greenflower (Act 2) Very High Alcove 4","Final Demo Monitor - Greenflower (Act 2) Very High Alcove 5","Final Demo Monitor - Greenflower (Act 2) Very High Alcove 6",
        "Final Demo Monitor - Greenflower (Act 2) Very High Alcove 7","Final Demo Monitor - Greenflower (Act 2) Very High Alcove 8","Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 3",
        "Final Demo Monitor - Greenflower (Act 2) Fence Near Spring Chain","Final Demo Monitor - Techno Hill (Act 1) Floating Platform 1","Final Demo Monitor - Techno Hill (Act 1) Metal Platform After Poison Lake",
        "Final Demo Monitor - Techno Hill (Act 1) Ledge Above First Poison","Final Demo Monitor - Techno Hill (Act 1) Right of Second Poison","Final Demo Monitor - Techno Hill (Act 1) On Pipes Near Token",
        "Final Demo Monitor - Techno Hill (Act 1) Floating Platform 2","Final Demo Monitor - Techno Hill (Act 2) Glass Conveyor Secret 1","Final Demo Monitor - Techno Hill (Act 2) Glass Conveyor Secret 2",
        "Final Demo Monitor - Techno Hill (Act 2) Flowing Poison","Final Demo Monitor - Castle Eggman (Act 1) Left Water Secret","Final Demo Monitor - Castle Eggman (Act 1) Moat Sewer 1",
        "Final Demo Monitor - Castle Eggman (Act 1) Moat Sewer 2","Final Demo Monitor - Castle Eggman (Act 1) Left Tunnel Before Act Clear","Final Demo Monitor - Castle Eggman (Act 1) Right Tunnel Before Act Clear",
        "Final Demo Monitor - Castle Eggman (Act 1) Tunnel Near Token","Final Demo Monitor - Castle Eggman (Act 1) Red Spring Cave","Final Demo Monitor - Castle Eggman (Act 1) Right Alcove Near Start",
        "Final Demo Monitor - Castle Eggman (Act 1) Left Path Spring Cave","Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 1","Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 2",
        "Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 3","Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 4","Final Demo Monitor - Castle Eggman (Act 2) Secret Corner in Fountain",
        "Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 2","Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 3","Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 4",
        "Final Demo Monitor - Castle Eggman (Act 2) Sewer Secret 1","Final Demo Monitor - Castle Eggman (Act 2) Sewer Secret 2","Final Demo Monitor - Castle Eggman (Act 2) Sewer Room On Pipe",
        "Final Demo Monitor - Castle Eggman (Act 2) Sewer Room Switch Corner 1","Final Demo Monitor - Castle Eggman (Act 2) Sewer Room Switch Corner 2","Final Demo Monitor - Castle Eggman (Act 2) Sewer Room Switch Corner 3",
        "Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Overhang","Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Pillar 1","Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Pillar 2",
        "Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Pillar 3","Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Platform 2","Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Platform 3",
        "Final Demo Monitor - Red Volcano (Act 1) Main Path After Checkpoint","Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 2","Final Demo Monitor - Red Volcano (Act 1) Main Path Under Pipes")

    regHHZ = create_region("Haunted Heights Zone", player, world)
    create_locs(regHHZ, "Haunted Heights Star Emblem", "Haunted Heights Spade Emblem", "Haunted Heights Heart Emblem", "Haunted Heights Diamond Emblem",
                "Haunted Heights Club Emblem","Haunted Heights Clear")
    if options.time_emblems:
        create_locs(regHHZ, "Haunted Heights Time Emblem")
    if options.ring_emblems:
        create_locs(regHHZ, "Haunted Heights Ring Emblem")
    if options.oneup_sanity:
        create_locs(regHHZ,"Haunted Heights Monitor - First Area Falling Platform","Haunted Heights Monitor - First Upper Path Disappearing Ledge","Haunted Heights Monitor - Spin Path Spinning Maces",
        "Haunted Heights Monitor - Third Area Deep in Slimefall","Haunted Heights Monitor - Third Area Conveyor Pillar","Haunted Heights Monitor - Knuckles Path Slime Under Platform",
        "Haunted Heights Monitor - Near Diamond Emblem","Haunted Heights Monitor - Ledge Before Final Checkpoint","Haunted Heights Monitor - Platform Before Goal",
        "Haunted Heights Monitor - Third Area High Alcove","Haunted Heights Monitor - Second Area Left High Ledge","Haunted Heights Monitor - Fang Path Breakable Floor Under Slime",
        "Haunted Heights Monitor - First Upper Path Dark Lower Ledge","Haunted Heights Monitor - Fang Path End Breakable Wall","Haunted Heights Monitor - First Area Highest Pillar",
        "Haunted Heights Monitor - First Lower Path Slime Before Checkpoint","Haunted Heights Monitor - First Lower Path Slimefall")

    if options.superring_sanity:
        create_locs(regHHZ,"Haunted Heights Monitor - Right Ledge Near Start","Haunted Heights Monitor - Grave Near Start",
        "Haunted Heights Monitor - First Slime Pit","Haunted Heights Monitor - First Area Under Grated Platform","Haunted Heights Monitor - Third Area Grated Platform 1",
        "Haunted Heights Monitor - Third Area Grated Platform 2","Haunted Heights Monitor - Knuckles Path Center Slime Platform","Haunted Heights Monitor - Third Area Bottom Entrances",
        "Haunted Heights Monitor - First Area Near Top Exit","Haunted Heights Monitor - Second Area Spike Ball Circle","Haunted Heights Monitor - Second Area Grassy Ledge",
        "Haunted Heights Monitor - First Area Near Conveyor Ramp","Haunted Heights Monitor - Third Area Knuckles Path Exit","Haunted Heights Monitor - Before Nospin Path Entrance",
        "Haunted Heights Monitor - Spin Conveyor Path Slime Corner","Haunted Heights Monitor - Nospin Path Behind Spikes","Haunted Heights Monitor - Fang Path Between Pipes",
        "Haunted Heights Monitor - Spin Path Behind First Ledge","Haunted Heights Monitor - Nospin Path Under High Ledge","Haunted Heights Monitor - Amy Path Spikes In Slime",
        "Haunted Heights Monitor - First Lower Path Entrance","Haunted Heights Monitor - Third Area Slimefall Lake","Haunted Heights Monitor - Third Area Ledge After Conveyors")

    regAGZ = create_region("Aerial Garden Zone", player, world)
    create_locs(regAGZ, "Aerial Garden Star Emblem", "Aerial Garden Spade Emblem", "Aerial Garden Heart Emblem", "Aerial Garden Diamond Emblem",
                "Aerial Garden Club Emblem","Aerial Garden Clear","Aerial Garden Emerald Token - First Room High Tower",
    "Aerial Garden Emerald Token - Underwater on Pillar",
    "Aerial Garden Emerald Token - Diamond Emblem 1",
    "Aerial Garden Emerald Token - Diamond Emblem 2",
    "Aerial Garden Emerald Token - Diamond Emblem 3",
    "Aerial Garden Emerald Token - Diamond Emblem 4")
    if options.time_emblems:
        create_locs(regAGZ, "Aerial Garden Time Emblem")
    if options.ring_emblems:
        create_locs(regAGZ, "Aerial Garden Ring Emblem")
    if options.oneup_sanity:
        create_locs(regAGZ,"Aerial Garden Monitor - Path Left 5 Thin Platforms Top 1","Aerial Garden Monitor - Path Right 3 Behind Statues","Aerial Garden Monitor - Triangle Hallway Spin Under Seaweed",
        "Aerial Garden Monitor - Path Right 1 Across Moving Platforms","Aerial Garden Monitor - Final Elevator Room Ledge 1","Aerial Garden Monitor - Path Left 6 Waterfall Top 1",
        "Aerial Garden Monitor - Path Right 5 Vertical Moving Platforms","Aerial Garden Monitor - Path Left 2 on Fountain","Aerial Garden Monitor - Path Left 2 Spin Into Bushes",
        "Aerial Garden Monitor - Path Left 4 Top Cave Clearing","Aerial Garden Monitor - Near Heart Emblem 1","Aerial Garden Monitor - Near Heart Emblem 2",
        "Aerial Garden Monitor - Near Heart Emblem 3","Aerial Garden Monitor - Near Heart Emblem 4","Aerial Garden Monitor - Path Left 4 High Thin Platforms",
        "Aerial Garden Monitor - Triangle Hallway Rafters 1","Aerial Garden Monitor - Line Hallway Outside R","Aerial Garden Monitor - Line Hallway Outside L",
        "Aerial Garden Monitor - First Room Near Emerald Token","Aerial Garden Monitor - Second Area Ledge Behind Fountain","Aerial Garden Monitor - Near Star Emblem 1",
        "Aerial Garden Monitor - Near Star Emblem 2","Aerial Garden Monitor - First Area Small Far Platform","Aerial Garden Monitor - Path Left 1 Gap Between Pillars 1",
        "Aerial Garden Monitor - Final Elevator Room Ledge 2","Aerial Garden Monitor - Fountain Room High Left Platform","Aerial Garden Monitor - Falling End Platform Trap",
        "Aerial Garden Monitor - Final Elevator Top S 1","Aerial Garden Monitor - Split Path Room Middle Ledge","Aerial Garden Monitor - Path Right 2 Tiny Platform",
        "Aerial Garden Monitor - Underwater Path Spring Pillars","Aerial Garden Monitor - Underwater Path Behind Corner")

    if options.superring_sanity:
        create_locs(regAGZ,"Aerial Garden Monitor - Triangle Hallway End 1","Aerial Garden Monitor - Triangle Hallway End 2",
        "Aerial Garden Monitor - Path Left 5 Thin Platforms Top 2","Aerial Garden Monitor - Path Left 5 Thin Platforms Top 3","Aerial Garden Monitor - Path Right 1 Grass Platform",
        "Aerial Garden Monitor - Near Heart Emblem 5","Aerial Garden Monitor - Near Heart Emblem 6","Aerial Garden Monitor - Near Heart Emblem 7",
        "Aerial Garden Monitor - Near Heart Emblem 8","Aerial Garden Monitor - Near Heart Emblem 9","Aerial Garden Monitor - Near Heart Emblem 10",
        "Aerial Garden Monitor - Near Heart Emblem 11","Aerial Garden Monitor - Near Heart Emblem 12","Aerial Garden Monitor - Near Heart Emblem 13",
        "Aerial Garden Monitor - Near Heart Emblem 14","Aerial Garden Monitor - Path Left 6 Waterfall Top 2","Aerial Garden Monitor - Path Left 3 Left Block Ledge",
        "Aerial Garden Monitor - Path Left 3 Block On Grass","Aerial Garden Monitor - Block After First Conveyor","Aerial Garden Monitor - Near Heart Emblem 15",
        "Aerial Garden Monitor - Path Left 1 Gap Between Pillars 2","Aerial Garden Monitor - Path Left 1 Gap Between Pillars 3","Aerial Garden Monitor - Path Left 1 Gap Between Pillars 4",
        "Aerial Garden Monitor - Path Left 1 Gap Between Pillars 5","Aerial Garden Monitor - Underwater Path Below Token","Aerial Garden Monitor - Knuckles Path Tall Room On Pillar",
        "Aerial Garden Monitor - Path Left 4 Before Triangle Switch","Aerial Garden Monitor - Path Left 3 High Ledge 1","Aerial Garden Monitor - Path Left 3 High Ledge 2",
        "Aerial Garden Monitor - Path Right 3 High Ledge 1","Aerial Garden Monitor - Path Right 3 High Ledge 2","Aerial Garden Monitor - Triangle Hallway Rafters 2",
        "Aerial Garden Monitor - Triangle Hallway Rafters 3","Aerial Garden Monitor - Path Left 6 Waterfall Top 3","Aerial Garden Monitor - First Area Back Left",
        "Aerial Garden Monitor - Second Area Left Low Ledge","Aerial Garden Monitor - First Area Flower Circle","Aerial Garden Monitor - Right Hallway Before Goal",
        "Aerial Garden Monitor - Outside Star Gate 1","Aerial Garden Monitor - Final Elevator Top W","Aerial Garden Monitor - Final Elevator Top E",
        "Aerial Garden Monitor - Split Path Room Left Pillars","Aerial Garden Monitor - Split Path Room Right Ledge","Aerial Garden Monitor - Outside Star Gate 2",
        "Aerial Garden Monitor - Final Elevator Bottom 1","Aerial Garden Monitor - Final Elevator Bottom 2","Aerial Garden Monitor - Final Elevator Top S 2",
        "Aerial Garden Monitor - Final Elevator Top S 3","Aerial Garden Monitor - Near Heart Emblem 16","Aerial Garden Monitor - Path Left 2 Near Fountain")


    regATZ = create_region("Azure Temple Zone", player, world)
    create_locs(regATZ, "Azure Temple Star Emblem", "Azure Temple Spade Emblem", "Azure Temple Heart Emblem", "Azure Temple Diamond Emblem","Azure Temple Club Emblem",
                "Azure Temple Clear")
    if options.time_emblems:
        create_locs(regATZ, "Azure Temple Time Emblem")
    if options.ring_emblems:
        create_locs(regATZ, "Azure Temple Ring Emblem")
    if options.oneup_sanity:
        create_locs(regATZ, "Azure Temple Monitor - Near Club Emblem 1",
                    "Azure Temple Monitor - Near Club Emblem 2",
                    "Azure Temple Monitor - Near Club Emblem 3")
        create_locs(regATZ,"Azure Temple Monitor - Main Path Behind Statues","Azure Temple Monitor - Main Path High Rocky Ledge",
        "Azure Temple Monitor - Bottom Path Side of Statue Hallway","Azure Temple Monitor - Rafters Near Spade Emblem 1","Azure Temple Monitor - Top Path High Ledge Behind Bars",
        "Azure Temple Monitor - Top Path Near Spiked Platform Ledge 1","Azure Temple Monitor - Bottom Path Buggle Room Rafters","Azure Temple Monitor - Near Star Emblem",
        "Azure Temple Monitor - Puzzle Path Corner 1","Azure Temple Monitor - Near Club Emblem 1","Azure Temple Monitor - Near Club Emblem 2",
        "Azure Temple Monitor - Near Club Emblem 3","Azure Temple Monitor - Inside Fountain Near End","Azure Temple Monitor - Near Heart Emblem 1",
        "Azure Temple Monitor - Action Path Rafters 1","Azure Temple Monitor - Gap Between Pillars Near First Checkpoint","Azure Temple Monitor - End of Puzzle Path",
        "Azure Temple Monitor - Action Nospin Path Ledge After Spring")

    if options.superring_sanity:
        create_locs(regATZ,"Azure Temple Monitor - Behind Left Starting Pillar","Azure Temple Monitor - Right Starting Ledge",
        "Azure Temple Monitor - Right Path Behind Corner","Azure Temple Monitor - Left Path First Ledge","Azure Temple Monitor - After First Checkpoint",
        "Azure Temple Monitor - Left Path Rocky Ledge 1","Azure Temple Monitor - Left Path Rocky Ledge 2","Azure Temple Monitor - Upper Main Path Behind Corner",
        "Azure Temple Monitor - Knuckles Path Start","Azure Temple Monitor - First Checkpoint Behind Stairs","Azure Temple Monitor - Top Path Gap After First Statue Hallway 1",
        "Azure Temple Monitor - Top Path Gap After First Statue Hallway 2","Azure Temple Monitor - Top Path Bubbles Before Checkpoint","Azure Temple Monitor - Bottom Path First Statue Hallway",
        "Azure Temple Monitor - Rafters Near Spade Emblem 2","Azure Temple Monitor - Bottom Path Metal Bars","Azure Temple Monitor - Knuckles Path Before Second Climb",
        "Azure Temple Monitor - Knuckles Path End","Azure Temple Monitor - Spade Emblem Room Knuckles Path Drop","Azure Temple Monitor - Rafters Near Spade Emblem 3",
        "Azure Temple Monitor - Top Path Corner After Checkpoint","Azure Temple Monitor - Top Path Behind Metal Bars","Azure Temple Monitor - Top Path Near Spiked Platform Ledge 2",
        "Azure Temple Monitor - Top Path Near Spiked Platform Ledge 3","Azure Temple Monitor - Bottom Path Buggle Room Corner","Azure Temple Monitor - Puzzle Path First Room",
        "Azure Temple Monitor - Bottom Path First Hallway Wall Gap 1","Azure Temple Monitor - Bottom Path First Hallway Wall Gap 2","Azure Temple Monitor - Puzzle Path Corner 2",
        "Azure Temple Monitor - Puzzle Path Corner 3","Azure Temple Monitor - Action Path First Room Ledge","Azure Temple Monitor - Near Heart Emblem 2",
        "Azure Temple Monitor - Near Heart Emblem 3","Azure Temple Monitor - Action Path Final Room First Ledge","Azure Temple Monitor - Near Diamond Emblem 1",
        "Azure Temple Monitor - Near Diamond Emblem 2","Azure Temple Monitor - Bottom Path Buggle Room Behind Statues","Azure Temple Monitor - Puzzle Path Final Room",
        "Azure Temple Monitor - Action Path Rafters 2","Azure Temple Monitor - Action Path Rafters 3","Azure Temple Monitor - Top Path First Hallway Secret",
        "Azure Temple Monitor - Knuckles Path First Rocky Ledge","Azure Temple Monitor - Knuckles Path Second Rocky Ledge","Azure Temple Monitor - Action Nospin Path Pillar")

    if options.nights_maps:

        regSPFFZ = create_region("Floral Field Zone", player, world)
        create_locs(regSPFFZ, "Floral Field Sun Emblem", "Floral Field Moon Emblem","Floral Field Clear")
        regSPTPZ = create_region("Toxic Plateau Zone", player, world)
        create_locs(regSPTPZ, "Toxic Plateau Sun Emblem", "Toxic Plateau Moon Emblem","Toxic Plateau Clear")
        regSPFCZ = create_region("Flooded Cove Zone", player, world)
        create_locs(regSPFCZ, "Flooded Cove Sun Emblem", "Flooded Cove Moon Emblem","Flooded Cove Clear")
        regSPCFZ = create_region("Cavern Fortress Zone", player, world)
        create_locs(regSPCFZ, "Cavern Fortress Sun Emblem", "Cavern Fortress Moon Emblem","Cavern Fortress Clear")
        regSPDWZ = create_region("Dusty Wasteland Zone", player, world)
        create_locs(regSPDWZ, "Dusty Wasteland Sun Emblem", "Dusty Wasteland Moon Emblem","Dusty Wasteland Clear")
        regSPMCZ = create_region("Magma Caves Zone", player, world)
        create_locs(regSPMCZ, "Magma Caves Sun Emblem", "Magma Caves Moon Emblem","Magma Caves Clear")
        regSPESZ = create_region("Egg Satellite Zone", player, world)
        create_locs(regSPESZ, "Egg Satellite Sun Emblem", "Egg Satellite Moon Emblem","Egg Satellite Clear")
        regSPBHZ = create_region("Black Hole Zone", player, world)
        create_locs(regSPBHZ, "Black Hole Sun Emblem", "Black Hole Moon Emblem","Black Hole Clear")
        regSPCCZ = create_region("Christmas Chime Zone", player, world)
        create_locs(regSPCCZ, "Christmas Chime Sun Emblem", "Christmas Chime Moon Emblem","Christmas Chime Clear")
        regSPDHZ = create_region("Dream Hill Zone", player, world)
        create_locs(regSPDHZ, "Dream Hill Sun Emblem", "Dream Hill Moon Emblem","Dream Hill Clear")

        regSPAPZ1 = create_region("Alpine Paradise Zone 1", player, world)
        regSPAPZ2 = create_region("Alpine Paradise Zone 2", player, world)
        create_locs(regSPAPZ1, "Alpine Paradise (Act 1) Sun Emblem", "Alpine Paradise (Act 1) Moon Emblem","Alpine Paradise (Act 1) Clear")
        create_locs(regSPAPZ2, "Alpine Paradise (Act 2) Sun Emblem", "Alpine Paradise (Act 2) Moon Emblem","Alpine Paradise (Act 2) Clear")

        if options.ntime_emblems:
            create_locs(regSPFFZ, "Floral Field Time Emblem")
            create_locs(regSPTPZ, "Toxic Plateau Time Emblem")
            create_locs(regSPFCZ, "Flooded Cove Time Emblem")
            create_locs(regSPCFZ, "Cavern Fortress Time Emblem")
            create_locs(regSPDWZ, "Dusty Wasteland Time Emblem")
            create_locs(regSPMCZ, "Magma Caves Time Emblem")
            create_locs(regSPESZ, "Egg Satellite Time Emblem")
            create_locs(regSPBHZ, "Black Hole Time Emblem")
            create_locs(regSPCCZ, "Christmas Chime Time Emblem")
            create_locs(regSPDHZ, "Dream Hill Time Emblem")
            create_locs(regSPAPZ1, "Alpine Paradise (Act 1) Time Emblem")
            create_locs(regSPAPZ2,"Alpine Paradise (Act 2) Time Emblem")

        if options.rank_emblems:
            create_locs(regSPFFZ, "Floral Field A Rank Emblem")
            create_locs(regSPTPZ, "Toxic Plateau A Rank Emblem")
            create_locs(regSPFCZ, "Flooded Cove A Rank Emblem")
            create_locs(regSPCFZ, "Cavern Fortress A Rank Emblem")
            create_locs(regSPDWZ, "Dusty Wasteland A Rank Emblem")
            create_locs(regSPMCZ, "Magma Caves A Rank Emblem")
            create_locs(regSPESZ, "Egg Satellite A Rank Emblem")
            create_locs(regSPBHZ, "Black Hole A Rank Emblem")
            create_locs(regSPCCZ, "Christmas Chime A Rank Emblem")
            create_locs(regSPDHZ, "Dream Hill A Rank Emblem")
            create_locs(regSPAPZ1, "Alpine Paradise (Act 1) A Rank Emblem")
            create_locs(regSPAPZ2,"Alpine Paradise (Act 2) A Rank Emblem")

    if options.match_maps and options.oneup_sanity:
        create_locs(regMPSFZ,"Sapphire Falls Monitor - Inside Central Platform")



    if options.match_maps and options.superring_sanity:
        create_locs(regMPJVZ, "Jade Valley Monitor - x:-336 y:768","Jade Valley Monitor - x:1440 y:-768","Jade Valley Monitor - x:1341 y:2218",
            "Jade Valley Monitor - x:1216 y:4960","Jade Valley Monitor - x:1921 y:564","Jade Valley Monitor - x:1890 y:497","Jade Valley Monitor - x:-4960 y:5312",
            "Jade Valley Monitor - x:-4928 y:5376","Jade Valley Monitor - x:1112 y:3915","Jade Valley Monitor - x:528 y:6672","Jade Valley Monitor - x:-6288 y:3296",
            "Jade Valley Monitor - x:-4199 y:4879","Jade Valley Monitor - x:-2288 y:-208","Jade Valley Monitor - x:-3416 y:1356","Jade Valley Monitor - x:4320 y:4576",
            "Jade Valley Monitor - x:4448 y:5984","Jade Valley Monitor - x:384 y:5248","Jade Valley Monitor - x:384 y:5312")
        create_locs(regMPNFZ, "Noxious Factory Monitor - x:1600 y:2624","Noxious Factory Monitor - x:-2048 y:3904","Noxious Factory Monitor - x:1472 y:2624",
            "Noxious Factory Monitor - x:-2752 y:256","Noxious Factory Monitor - x:-1728 y:-256","Noxious Factory Monitor - x:3424 y:1472","Noxious Factory Monitor - x:3456 y:1440",
            "Noxious Factory Monitor - x:-2464 y:2208","Noxious Factory Monitor - x:-2400 y:2208","Noxious Factory Monitor - x:-2400 y:2144","Noxious Factory Monitor - x:-2464 y:2144",
            "Noxious Factory Monitor - x:-1568 y:1312","Noxious Factory Monitor - x:-1376 y:1760","Noxious Factory Monitor - x:-1504 y:1760","Noxious Factory Monitor - x:1472 y:2752",
            "Noxious Factory Monitor - x:1600 y:2752","Noxious Factory Monitor - x:416 y:576","Noxious Factory Monitor - x:736 y:768","Noxious Factory Monitor - x:2112 y:-1920",
            "Noxious Factory Monitor - x:2496 y:3264","Noxious Factory Monitor - x:2496 y:3136","Noxious Factory Monitor - x:1440 y:-2336")
        create_locs(regMPTPZ, "Tidal Palace Monitor - x:-2624 y:-3072","Tidal Palace Monitor - x:-1920 y:-3616","Tidal Palace Monitor - x:0 y:-3232",
            "Tidal Palace Monitor - x:-4672 y:-1472","Tidal Palace Monitor - x:-4640 y:-1504","Tidal Palace Monitor - x:4128 y:-1824","Tidal Palace Monitor - x:3104 y:1088",
            "Tidal Palace Monitor - x:320 y:-1824","Tidal Palace Monitor - x:-3264 y:896","Tidal Palace Monitor - x:2784 y:1856","Tidal Palace Monitor - x:1472 y:-2304",
            "Tidal Palace Monitor - x:1184 y:-2976","Tidal Palace Monitor - x:-4384 y:-2560","Tidal Palace Monitor - x:-4256 y:-2560","Tidal Palace Monitor - x:-4096 y:384",
            "Tidal Palace Monitor - x:-2912 y:-2976","Tidal Palace Monitor - x:3136 y:1120","Tidal Palace Monitor - x:4064 y:-1824","Tidal Palace Monitor - x:4096 y:-1792",
            "Tidal Palace Monitor - x:-2656 y:-2656","Tidal Palace Monitor - x:1504 y:-96","Tidal Palace Monitor - x:1504 y:-224","Tidal Palace Monitor - x:-4160 y:1536",
            "Tidal Palace Monitor - x:-224 y:-672","Tidal Palace Monitor - x:224 y:-672")
        create_locs(regMPTCZ, "Thunder Citadel Monitor - x:-1234 y:-1124","Thunder Citadel Monitor - x:224 y:1760","Thunder Citadel Monitor - x:3520 y:4928",
            "Thunder Citadel Monitor - x:-4928 y:1856","Thunder Citadel Monitor - x:-448 y:1728","Thunder Citadel Monitor - x:3136 y:3200","Thunder Citadel Monitor - x:-1088 y:3232",
            "Thunder Citadel Monitor - x:-1056 y:3200","Thunder Citadel Monitor - x:-1088 y:3168","Thunder Citadel Monitor - x:-5056 y:1728","Thunder Citadel Monitor - x:-4603 y:7411",
            "Thunder Citadel Monitor - x:2341 y:6261","Thunder Citadel Monitor - x:2528 y:6016","Thunder Citadel Monitor - x:3392 y:1856","Thunder Citadel Monitor - x:320 y:2560",
            "Thunder Citadel Monitor - x:3328 y:1600","Thunder Citadel Monitor - x:1536 y:3392")
        create_locs(regMPDTZ, "Desolate Twilight Monitor - x:-512 y:-960","Desolate Twilight Monitor - x:480 y:-960","Desolate Twilight Monitor - x:2768 y:-3792",
            "Desolate Twilight Monitor - x:-768 y:1056","Desolate Twilight Monitor - x:864 y:1184","Desolate Twilight Monitor - x:-2624 y:3008","Desolate Twilight Monitor - x:-2580 y:3059",
            "Desolate Twilight Monitor - x:-128 y:-2688","Desolate Twilight Monitor - x:2913 y:212","Desolate Twilight Monitor - x:2904 y:275","Desolate Twilight Monitor - x:0 y:3584",
            "Desolate Twilight Monitor - x:2704 y:-3856")
        create_locs(regMPFMZ, "Frigid Mountain Monitor - x:3232 y:-3136","Frigid Mountain Monitor - x:1760 y:-1312","Frigid Mountain Monitor - x:6432 y:-384",
            "Frigid Mountain Monitor - x:1728 y:-1376","Frigid Mountain Monitor - x:6432 y:-320","Frigid Mountain Monitor - x:1072 y:558","Frigid Mountain Monitor - x:3744 y:-128",
            "Frigid Mountain Monitor - x:6432 y:-256","Frigid Mountain Monitor - x:5024 y:-2048","Frigid Mountain Monitor - x:5280 y:-4864","Frigid Mountain Monitor - x:5280 y:-4928",
            "Frigid Mountain Monitor - x:3808 y:-192")
        create_locs(regMPOHZ, "Orbital Hangar Monitor - x:4928 y:-4160","Orbital Hangar Monitor - x:4928 y:-5568","Orbital Hangar Monitor - x:3456 y:-2016",
            "Orbital Hangar Monitor - x:192 y:-3776","Orbital Hangar Monitor - x:192 y:-5440","Orbital Hangar Monitor - x:1984 y:-4768","Orbital Hangar Monitor - x:2016 y:-4064",
            "Orbital Hangar Monitor - x:2784 y:-7776","Orbital Hangar Monitor - x:3104 y:-7776","Orbital Hangar Monitor - x:4320 y:-6176","Orbital Hangar Monitor - x:1568 y:-6176",
            "Orbital Hangar Monitor - x:3104 y:-6176","Orbital Hangar Monitor - x:2784 y:-6176","Orbital Hangar Monitor - x:5472 y:-1984","Orbital Hangar Monitor - x:6464 y:-1216",
            "Orbital Hangar Monitor - x:32 y:-3296","Orbital Hangar Monitor - x:832 y:-7392","Orbital Hangar Monitor - x:2368 y:-2304","Orbital Hangar Monitor - x:2304 y:-2304",
            "Orbital Hangar Monitor - x:2240 y:-2304","Orbital Hangar Monitor - x:5952 y:-6592","Orbital Hangar Monitor - x:5344 y:-1984","Orbital Hangar Monitor - x:448 y:-4320",
            "Orbital Hangar Monitor - x:-320 y:-4896","Orbital Hangar Monitor - x:6592 y:-5760")
        create_locs(regMPSFZ, "Sapphire Falls Monitor - x:-912 y:-3872","Sapphire Falls Monitor - x:4288 y:-1248","Sapphire Falls Monitor - x:-4864 y:-832",
            "Sapphire Falls Monitor - x:-3616 y:3120","Sapphire Falls Monitor - x:-3616 y:3184","Sapphire Falls Monitor - x:-3616 y:3248","Sapphire Falls Monitor - x:1920 y:5632",
            "Sapphire Falls Monitor - x:3488 y:3936","Sapphire Falls Monitor - x:3424 y:3936","Sapphire Falls Monitor - x:-1568 y:5024","Sapphire Falls Monitor - x:3680 y:2848",
            "Sapphire Falls Monitor - x:4160 y:2592","Sapphire Falls Monitor - x:1408 y:4384","Sapphire Falls Monitor - x:-1472 y:5120","Sapphire Falls Monitor - x:-912 y:-3616",
            "Sapphire Falls Monitor - x:-16 y:-3136","Sapphire Falls Monitor - x:-544 y:-5344","Sapphire Falls Monitor - x:1184 y:-2176")
        create_locs(regMPDBZ, "Diamond Blizzard Monitor - x:64 y:-3520","Diamond Blizzard Monitor - x:2688 y:-3136","Diamond Blizzard Monitor - x:1856 y:-3968",
            "Diamond Blizzard Monitor - x:-2432 y:3168","Diamond Blizzard Monitor - x:-2752 y:1920","Diamond Blizzard Monitor - x:-1088 y:2432","Diamond Blizzard Monitor - x:1184 y:-1840",
            "Diamond Blizzard Monitor - x:0 y:-1024","Diamond Blizzard Monitor - x:-1408 y:-896","Diamond Blizzard Monitor - x:-1856 y:-5184","Diamond Blizzard Monitor - x:-1216 y:-3456",
            "Diamond Blizzard Monitor - x:1088 y:960","Diamond Blizzard Monitor - x:-64 y:2432","Diamond Blizzard Monitor - x:1056 y:2272","Diamond Blizzard Monitor - x:-1856 y:4224",
            "Diamond Blizzard Monitor - x:-1920 y:-2752","Diamond Blizzard Monitor - x:1296 y:400","Diamond Blizzard Monitor - x:1904 y:-1040","Diamond Blizzard Monitor - x:-576 y:-3744",
            "Diamond Blizzard Monitor - x:608 y:-4544","Diamond Blizzard Monitor - x:928 y:-4544","Diamond Blizzard Monitor - x:3392 y:2240","Diamond Blizzard Monitor - x:0 y:-3808",
            "Diamond Blizzard Monitor - x:-128 y:-3808","Diamond Blizzard Monitor - x:4160 y:-680","Diamond Blizzard Monitor - x:4160 y:-728")
        create_locs(regMPCSZ, "Celestial Sanctuary Monitor - x:1504 y:3168","Celestial Sanctuary Monitor - x:2880 y:6208","Celestial Sanctuary Monitor - x:-764 y:-1802",
            "Celestial Sanctuary Monitor - x:10048 y:4928","Celestial Sanctuary Monitor - x:6144 y:6720","Celestial Sanctuary Monitor - x:1792 y:64","Celestial Sanctuary Monitor - x:-2320 y:-1088",
            "Celestial Sanctuary Monitor - x:-1856 y:1472","Celestial Sanctuary Monitor - x:1792 y:-64","Celestial Sanctuary Monitor - x:4096 y:5088","Celestial Sanctuary Monitor - x:3648 y:2848",
            "Celestial Sanctuary Monitor - x:10112 y:4928","Celestial Sanctuary Monitor - x:4800 y:128","Celestial Sanctuary Monitor - x:7040 y:-3008","Celestial Sanctuary Monitor - x:4480 y:6592",
            "Celestial Sanctuary Monitor - x:4544 y:6592","Celestial Sanctuary Monitor - x:9088 y:320","Celestial Sanctuary Monitor - x:3084 y:2461","Celestial Sanctuary Monitor - x:-2368 y:-1136",
            "Celestial Sanctuary Monitor - x:192 y:5952","Celestial Sanctuary Monitor - x:256 y:5952","Celestial Sanctuary Monitor - x:4128 y:-1120")
        create_locs(regMPFCZ, "Frost Columns Monitor - x:-3776 y:3904","Frost Columns Monitor - x:-3872 y:3808","Frost Columns Monitor - x:-3616 y:1120",
            "Frost Columns Monitor - x:-1568 y:-1152","Frost Columns Monitor - x:1856 y:-1728","Frost Columns Monitor - x:1888 y:-1728","Frost Columns Monitor - x:1888 y:-1760",
            "Frost Columns Monitor - x:608 y:640","Frost Columns Monitor - x:1312 y:-960","Frost Columns Monitor - x:2048 y:768","Frost Columns Monitor - x:-1152 y:-1056",
            "Frost Columns Monitor - x:0 y:-3520","Frost Columns Monitor - x:-64 y:-3520","Frost Columns Monitor - x:560 y:736","Frost Columns Monitor - x:-1472 y:-96",
            "Frost Columns Monitor - x:-1472 y:-32","Frost Columns Monitor - x:-3296 y:3200","Frost Columns Monitor - x:-3328 y:3168","Frost Columns Monitor - x:-2080 y:-896",
            "Frost Columns Monitor - x:2112 y:-1088","Frost Columns Monitor - x:2112 y:-1344","Frost Columns Monitor - x:832 y:-1376")
        create_locs(regMPMMZ, "Meadow Match Monitor - x:-1536 y:1472","Meadow Match Monitor - x:-2688 y:320","Meadow Match Monitor - x:3520 y:-576",
            "Meadow Match Monitor - x:-64 y:-1088","Meadow Match Monitor - x:-1472 y:512","Meadow Match Monitor - x:1472 y:-864")
        create_locs(regMPGLZ, "Granite Lake Monitor - x:1728 y:3264","Granite Lake Monitor - x:-432 y:-1168","Granite Lake Monitor - x:4764 y:7933",
            "Granite Lake Monitor - x:5045 y:7647","Granite Lake Monitor - x:2352 y:384","Granite Lake Monitor - x:2064 y:-1136","Granite Lake Monitor - x:2304 y:1056",
            "Granite Lake Monitor - x:5472 y:1344","Granite Lake Monitor - x:1075 y:5651","Granite Lake Monitor - x:1293 y:7833","Granite Lake Monitor - x:4288 y:3040")
        create_locs(regMPSSZ, "Summit Showdown Monitor - x:5344 y:1952","Summit Showdown Monitor - x:4640 y:2400","Summit Showdown Monitor - x:-6624 y:-64",
            "Summit Showdown Monitor - x:-6480 y:-64","Summit Showdown Monitor - x:-6352 y:-64","Summit Showdown Monitor - x:-6176 y:1888","Summit Showdown Monitor - x:-6464 y:2592",
            "Summit Showdown Monitor - x:-4736 y:-128","Summit Showdown Monitor - x:2144 y:-1856","Summit Showdown Monitor - x:-1728 y:-1568","Summit Showdown Monitor - x:1696 y:-1568",
            "Summit Showdown Monitor - x:3056 y:976","Summit Showdown Monitor - x:1824 y:-800","Summit Showdown Monitor - x:-7456 y:-1696","Summit Showdown Monitor - x:-7008 y:-2144",
            "Summit Showdown Monitor - x:-7456 y:384","Summit Showdown Monitor - x:5600 y:2208","Summit Showdown Monitor - x:5088 y:1696","Summit Showdown Monitor - x:-1536 y:-2848",
            "Summit Showdown Monitor - x:3936 y:-1408","Summit Showdown Monitor - x:0 y:-224","Summit Showdown Monitor - x:-1216 y:-928","Summit Showdown Monitor - x:-4321 y:1792")
        create_locs(regMPSShZ, "Silver Shiver Monitor - x:4560 y:-8688","Silver Shiver Monitor - x:3648 y:-10176","Silver Shiver Monitor - x:6080 y:-12416",
            "Silver Shiver Monitor - x:7040 y:-11264","Silver Shiver Monitor - x:7680 y:-12608","Silver Shiver Monitor - x:7168 y:-11872","Silver Shiver Monitor - x:6976 y:-11872",
            "Silver Shiver Monitor - x:13824 y:-7392","Silver Shiver Monitor - x:13088 y:-3840","Silver Shiver Monitor - x:5440 y:-2688","Silver Shiver Monitor - x:5728 y:-2688",
            "Silver Shiver Monitor - x:8512 y:-3264","Silver Shiver Monitor - x:9024 y:-3904","Silver Shiver Monitor - x:2400 y:-3920","Silver Shiver Monitor - x:3392 y:-1824",
            "Silver Shiver Monitor - x:3392 y:-1728","Silver Shiver Monitor - x:3392 y:-1888","Silver Shiver Monitor - x:-96 y:-2768","Silver Shiver Monitor - x:32 y:-2768",
            "Silver Shiver Monitor - x:-192 y:-4672","Silver Shiver Monitor - x:1984 y:-5184","Silver Shiver Monitor - x:3056 y:-5568","Silver Shiver Monitor - x:3056 y:-5760",
            "Silver Shiver Monitor - x:-1344 y:-6464","Silver Shiver Monitor - x:176 y:-10384","Silver Shiver Monitor - x:4928 y:-17600","Silver Shiver Monitor - x:1952 y:-15648",
            "Silver Shiver Monitor - x:1856 y:-16320","Silver Shiver Monitor - x:192 y:-16960","Silver Shiver Monitor - x:-2368 y:-15424","Silver Shiver Monitor - x:-192 y:-15808",
            "Silver Shiver Monitor - x:-1120 y:-14048","Silver Shiver Monitor - x:9152 y:-15168","Silver Shiver Monitor - x:8384 y:-15168","Silver Shiver Monitor - x:11200 y:-17216",
            "Silver Shiver Monitor - x:11584 y:-13120","Silver Shiver Monitor - x:13632 y:-12320","Silver Shiver Monitor - x:15280 y:-26560","Silver Shiver Monitor - x:15696 y:-26560",
            "Silver Shiver Monitor - x:11744 y:-20960","Silver Shiver Monitor - x:11872 y:-21088","Silver Shiver Monitor - x:15360 y:-27360","Silver Shiver Monitor - x:15552 y:-27360",
            "Silver Shiver Monitor - x:6240 y:-13776","Silver Shiver Monitor - x:6304 y:-13808")
        create_locs(regMPUBZ, "Uncharted Badlands Monitor - x:1337 y:-1608","Uncharted Badlands Monitor - x:515 y:502","Uncharted Badlands Monitor - x:2522 y:114",
            "Uncharted Badlands Monitor - x:2080 y:2560","Uncharted Badlands Monitor - x:1920 y:1024","Uncharted Badlands Monitor - x:-1379 y:-2638","Uncharted Badlands Monitor - x:-992 y:32",
            "Uncharted Badlands Monitor - x:1152 y:3008","Uncharted Badlands Monitor - x:40 y:3323")
        create_locs(regMPPSZ, "Pristine Shores Monitor - x:6208 y:10720","Pristine Shores Monitor - x:4736 y:12288","Pristine Shores Monitor - x:4272 y:3440",
            "Pristine Shores Monitor - x:14272 y:7488","Pristine Shores Monitor - x:15808 y:12160","Pristine Shores Monitor - x:14936 y:13448","Pristine Shores Monitor - x:10336 y:11296",
            "Pristine Shores Monitor - x:11754 y:6506","Pristine Shores Monitor - x:16782 y:8472","Pristine Shores Monitor - x:13472 y:9024","Pristine Shores Monitor - x:13288 y:10444",
            "Pristine Shores Monitor - x:6080 y:8832","Pristine Shores Monitor - x:9296 y:12928","Pristine Shores Monitor - x:10672 y:6576","Pristine Shores Monitor - x:10680 y:12616",
            "Pristine Shores Monitor - x:3008 y:6528","Pristine Shores Monitor - x:2088 y:5240","Pristine Shores Monitor - x:4160 y:7176","Pristine Shores Monitor - x:6528 y:7936",
            "Pristine Shores Monitor - x:9944 y:7616")
        create_locs(regMPCHZ, "Crystalline Heights Monitor - x:4288 y:12384","Crystalline Heights Monitor - x:7392 y:8832","Crystalline Heights Monitor - x:3250 y:8402",
            "Crystalline Heights Monitor - x:7888 y:5600","Crystalline Heights Monitor - x:4416 y:11560","Crystalline Heights Monitor - x:2018 y:1218","Crystalline Heights Monitor - x:7314 y:-366",
            "Crystalline Heights Monitor - x:6418 y:3026","Crystalline Heights Monitor - x:1120 y:6192","Crystalline Heights Monitor - x:-360 y:12136","Crystalline Heights Monitor - x:2832 y:13836",
            "Crystalline Heights Monitor - x:6386 y:15954","Crystalline Heights Monitor - x:3104 y:17064","Crystalline Heights Monitor - x:7288 y:17568","Crystalline Heights Monitor - x:-784 y:-632",
            "Crystalline Heights Monitor - x:5410 y:1266","Crystalline Heights Monitor - x:1032 y:10464","Crystalline Heights Monitor - x:5384 y:5984","Crystalline Heights Monitor - x:5554 y:9730",
            "Crystalline Heights Monitor - x:6384 y:19336","Crystalline Heights Monitor - x:-544 y:4064","Crystalline Heights Monitor - x:-2704 y:12592")
        create_locs(regMPMAZ, "Midnight Abyss Monitor - x:-3264 y:3136","Midnight Abyss Monitor - x:3264 y:3136","Midnight Abyss Monitor - x:3264 y:-3136",
            "Midnight Abyss Monitor - x:-3264 y:-3136","Midnight Abyss Monitor - x:-2624 y:-2624","Midnight Abyss Monitor - x:2624 y:-2624","Midnight Abyss Monitor - x:2624 y:2624",
            "Midnight Abyss Monitor - x:-2624 y:2624","Midnight Abyss Monitor - x:-3136 y:3264","Midnight Abyss Monitor - x:3136 y:3264","Midnight Abyss Monitor - x:3136 y:-3264",
            "Midnight Abyss Monitor - x:-3136 y:-3264")
        create_locs(regMPATZ, "Airborne Temple Monitor - x:-2432 y:2432","Airborne Temple Monitor - x:2432 y:2432","Airborne Temple Monitor - x:2432 y:-2432",
            "Airborne Temple Monitor - x:-2432 y:-2432","Airborne Temple Monitor - x:-128 y:-128","Airborne Temple Monitor - x:128 y:-128","Airborne Temple Monitor - x:128 y:128",
            "Airborne Temple Monitor - x:-128 y:128","Airborne Temple Monitor - x:-256 y:256","Airborne Temple Monitor - x:256 y:256","Airborne Temple Monitor - x:256 y:-256",
            "Airborne Temple Monitor - x:-256 y:-256")

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None) -> Entrance:
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    return sourceRegion.connect(targetRegion, rule=rule)


def create_region(name: str, player: int, world: MultiWorld) -> SRB2Region:
    region = SRB2Region(name, player, world)
    world.regions.append(region)
    return region


def create_subregion(source_region: Region, name: str, *locs: str) -> SRB2Region:
    region = SRB2Region(name, source_region.player, source_region.multiworld)
    connection = Entrance(source_region.player, name, source_region)
    source_region.exits.append(connection)
    connection.connect(region)
    source_region.multiworld.regions.append(region)
    create_locs(region, *locs)
    return region


def set_subregion_access_rule(world, player, region_name: str, rule):
    world.get_entrance(world, player, region_name).access_rule = rule


def create_default_locs(reg: Region, default_locs: dict):
    create_locs(reg, *default_locs.keys())


def create_locs(reg: Region, *locs: str):
    reg.locations += [SRB2Location(reg.player, loc_name, location_table[loc_name], reg) for loc_name in locs]
