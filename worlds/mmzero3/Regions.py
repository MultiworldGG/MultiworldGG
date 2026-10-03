from typing import Dict, List, NamedTuple


class MMZero3RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, MMZero3RegionData] = {
    "Menu": MMZero3RegionData([
        # Hub. Contains different checks based on game progress flags.
        "Resistance Base 1",
        "Resistance Base 2",
        "Resistance Base 3",

        # Intro
        "Derelict Spacecraft",

        # First 4 selectable main stages
        "Aegis Volcano Base",
        "Oceanic Highway Ruins",
        "Weapons Repair Factory",
        "Old Residential",

        # Intermission 1
        "Missile Factory",

        # Second 3
        "Twilight Desert",
        "Forest of Anatre",
        "Frontline Ice Base",

        # Intermission 2
        "Area X-2",

        #Final 4
        "Energy Facility",
        "Snowy Plains",
        "Sunken Library",
        "Giant Elevator",

        # Intermission 3
        "Sub Arcadia",

        # Final Level
        "Abandoned Research Laboratory",
    ]),

    "Resistance Base 1": MMZero3RegionData(),
    "Resistance Base 2": MMZero3RegionData(),
    "Resistance Base 3": MMZero3RegionData(),

    "Derelict Spacecraft": MMZero3RegionData(),

    "Aegis Volcano Base": MMZero3RegionData(),
    "Oceanic Highway Ruins": MMZero3RegionData(),
    "Weapons Repair Factory": MMZero3RegionData(),
    "Old Residential": MMZero3RegionData(),

    # Crea and Prea (two baby elves)
    "Missile Factory": MMZero3RegionData(),

    "Twilight Desert": MMZero3RegionData(),
    "Forest of Anatre": MMZero3RegionData(),
    "Frontline Ice Base": MMZero3RegionData(),

    # Copy X
    "Area X-2": MMZero3RegionData(),

    "Energy Facility": MMZero3RegionData(),
    "Snowy Plains": MMZero3RegionData(),
    "Sunken Library": MMZero3RegionData(),
    "Giant Elevator": MMZero3RegionData(),

    # Crea and Prea rematch (and shadow guy)
    "Sub Arcadia": MMZero3RegionData(),

    # Final stage
    "Abandoned Research Laboratory": MMZero3RegionData(),
}
