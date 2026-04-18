from enum import Enum, StrEnum


class BlastShieldType(Enum):
    Bomb = "Bomb"
    Charge_Beam = "Charge Beam"
    Flamethrower = "Flamethrower"
    Ice_Spreader = "Ice Spreader"
    Wavebuster = "Wavebuster"
    Power_Bomb = "Power Bomb"
    Super_Missile = "Super Missile"
    Missile = "Missile"
    Disabled = "Disabled"  # This is technically a door type, but functionally we want to add it the way that shields are added
    No_Blast_Shield = "None"


class CombatLogicDifficulty(Enum):
    NO_LOGIC = -1
    NORMAL = 0
    MINIMAL = 1


class ConnectionState(Enum):
    DISCONNECTED = 0
    IN_GAME = 1
    IN_MENU = 2
    MULTIPLE_DOLPHIN_INSTANCES = 3


class DoorLockType(StrEnum):
    Blue = "Blue"
    Wave = "Wave Beam"
    Ice = "Ice Beam"
    Plasma = "Plasma Beam"
    Missile = "Missile"
    Power_Beam = "Power Beam Only"
    Bomb = "Bomb"
    None_ = "None"

    def __str__(self):
        return self.value


class HudColor(Enum):
    DEFAULT = [102 / 255, 174 / 255, 225 / 255]
    RED = [1.0, 0.0, 0.0]
    GREEN = [0.0, 1.0, 0.0]
    BLUE = [0.0, 0.0, 1.0]
    VIOLET = [1.0, 0.0, 1.0]
    YELLOW = [1.0, 1.0, 0.0]
    CYAN = [0.0, 1.0, 1.0]
    WHITE = [1.0, 1.0, 1.0]
    ORANGE = [1.0, 0.5, 0.0]
    PINK = [1.0, 0.5, 1.0]
    LIME = [0.5, 1.0, 0.0]
    TEAL = [0.5, 1.0, 1.0]
    PURPLE = [0.5, 0.0, 1.0]


class MetroidPrimeArea(StrEnum):
    Tallon_Overworld = "Tallon Overworld"
    Chozo_Ruins = "Chozo Ruins"
    Magmoor_Caverns = "Magmoor Caverns"
    Phendrana_Drifts = "Phendrana Drifts"
    Phazon_Mines = "Phazon Mines"

    def __str__(self):
        return self.value


class MetroidPrimeSuit(Enum):
    Power = 0
    Gravity = 1
    Varia = 2
    Phazon = 3
    FusionPower = 4
    FusionGravity = 5
    FusionVaria = 6
    FusionPhazon = 7

    @staticmethod
    def get_by_key(key: str):
        for suit in MetroidPrimeSuit:
            if suit.name == key:
                return suit
        return None


class MetroidPrimeLevel(Enum):
    """Game worlds with their corresponding IDs in memory"""

    Impact_Crater = 3241871825
    Phendrana_Drifts = 2831049361
    Frigate_Orpheon = 361692695
    Magmoor_Caverns = 1056449404
    Phazon_Mines = 2980859237
    Tallon_Overworld = 972217896
    Chozo_Ruins = 2214002543
    End_of_Game = 332894565


class ProgressiveUpgrade(StrEnum):
    Progressive_Power_Beam = "Progressive Power Beam"
    Progressive_Ice_Beam = "Progressive Ice Beam"
    Progressive_Wave_Beam = "Progressive Wave Beam"
    Progressive_Plasma_Beam = "Progressive Plasma Beam"
    Progressive_Bomb = "Progressive Bomb"

    def __str__(self):
        return self.value


class RoomName(Enum):
    Antechamber = "Antechamber"
    Arboretum_Access = "Arboretum Access"
    Arboretum = "Arboretum"
    Burn_Dome_Access = "Burn Dome Access"
    Burn_Dome = "Burn Dome"
    Crossway_Access_South = "Crossway Access South"
    Crossway_Access_West = "Crossway Access West"
    Crossway = "Crossway"
    Dynamo_Access = "Dynamo Access"
    Dynamo = "Dynamo"
    East_Atrium = "East Atrium"
    East_Furnace_Access = "East Furnace Access"
    Elder_Chamber = "Elder Chamber"
    Elder_Hall_Access = "Elder Hall Access"
    Energy_Core_Access = "Energy Core Access"
    Energy_Core = "Energy Core"
    Eyon_Tunnel = "Eyon Tunnel"
    Furnace = "Furnace"
    Gathering_Hall_Access = "Gathering Hall Access"
    Gathering_Hall = "Gathering Hall"
    Hall_of_the_Elders = "Hall of the Elders"
    Hive_Totem = "Hive Totem"
    Magma_Pool = "Magma Pool"
    Main_Plaza = "Main Plaza"
    Map_Station = "Map Station"
    Meditation_Fountain = "Meditation Fountain"
    North_Atrium = "North Atrium"
    Nursery_Access = "Nursery Access"
    Piston_Tunnel = "Piston Tunnel"
    Plaza_Access = "Plaza Access"
    Reflecting_Pool_Access = "Reflecting Pool Access"
    Reflecting_Pool = "Reflecting Pool"
    Ruined_Fountain_Access = "Ruined Fountain Access"
    Ruined_Fountain = "Ruined Fountain"
    Ruined_Gallery = "Ruined Gallery"
    Ruined_Nursery = "Ruined Nursery"
    Ruined_Shrine_Access = "Ruined Shrine Access"
    Ruined_Shrine = "Ruined Shrine"
    Ruins_Entrance = "Ruins Entrance"
    Save_Station_1 = "Save Station 1"
    Save_Station_2 = "Save Station 2"
    Save_Station_3 = "Save Station 3"
    Sun_Tower_Access = "Sun Tower Access"
    Sun_Tower = "Sun Tower"
    Sunchamber_Access = "Sunchamber Access"
    Sunchamber_Lobby = "Sunchamber Lobby"
    Sunchamber = "Sunchamber"
    Totem_Access = "Totem Access"
    Tower_Chamber = "Tower Chamber"
    Tower_of_Light_Access = "Tower of Light Access"
    Tower_of_Light = "Tower of Light"
    Training_Chamber_Access = "Training Chamber Access"
    Training_Chamber = "Training Chamber"
    Transport_Access_North = "Transport Access North"
    Transport_Access_South = "Transport Access South"
    Transport_to_Magmoor_Caverns_North = "Transport to Magmoor Caverns North"
    Transport_to_Tallon_Overworld_East = "Transport to Tallon Overworld East"
    Transport_to_Tallon_Overworld_North = "Transport to Tallon Overworld North"
    Transport_to_Tallon_Overworld_South = "Transport to Tallon Overworld South"
    Vault_Access = "Vault Access"
    Vault = "Vault"
    Watery_Hall_Access = "Watery Hall Access"
    Watery_Hall = "Watery Hall"
    West_Furnace_Access = "West Furnace Access"
    End_Cinema = "End Cinema"
    Crater_Entry_Point = "Crater Entry Point"
    Crater_Missile_Station = "Crater Missile Station"
    Crater_Tunnel_A = "Crater Tunnel A"
    Crater_Tunnel_B = "Crater Tunnel B"
    Metroid_Prime_Lair = "Metroid Prime Lair"
    Phazon_Core = "Phazon Core"
    Phazon_Infusion_Chamber = "Phazon Infusion Chamber"
    Subchamber_Five = "Subchamber Five"
    Subchamber_Four = "Subchamber Four"
    Subchamber_One = "Subchamber One"
    Subchamber_Three = "Subchamber Three"
    Subchamber_Two = "Subchamber Two"
    Burning_Trail = "Burning Trail"
    Fiery_Shores = "Fiery Shores"
    Geothermal_Core = "Geothermal Core"
    Lake_Tunnel = "Lake Tunnel"
    Lava_Lake = "Lava Lake"
    Magmoor_Workstation = "Magmoor Workstation"
    Monitor_Station = "Monitor Station"
    Monitor_Tunnel = "Monitor Tunnel"
    North_Core_Tunnel = "North Core Tunnel"
    Pit_Tunnel = "Pit Tunnel"
    Plasma_Processing = "Plasma Processing"
    Save_Station_Magmoor_A = "Save Station Magmoor A"
    Save_Station_Magmoor_B = "Save Station Magmoor B"
    Shore_Tunnel = "Shore Tunnel"
    South_Core_Tunnel = "South Core Tunnel"
    Storage_Cavern = "Storage Cavern"
    Transport_to_Chozo_Ruins_North = "Transport to Chozo Ruins North"
    Transport_to_Phazon_Mines_West = "Transport to Phazon Mines West"
    Transport_to_Phendrana_Drifts_North = "Transport to Phendrana Drifts North"
    Transport_to_Phendrana_Drifts_South = "Transport to Phendrana Drifts South"
    Transport_to_Tallon_Overworld_West = "Transport to Tallon Overworld West"
    Transport_Tunnel_A = "Transport Tunnel A"
    Transport_Tunnel_B = "Transport Tunnel B"
    Transport_Tunnel_C = "Transport Tunnel C"
    Triclops_Pit = "Triclops Pit"
    Twin_Fires_Tunnel = "Twin Fires Tunnel"
    Twin_Fires = "Twin Fires"
    Warrior_Shrine = "Warrior Shrine"
    Workstation_Tunnel = "Workstation Tunnel"
    Central_Dynamo = "Central Dynamo"
    Elevator_A = "Elevator A"
    Elevator_Access_A = "Elevator Access A"
    Elevator_Access_B = "Elevator Access B"
    Elevator_B = "Elevator B"
    Elite_Control_Access = "Elite Control Access"
    Elite_Control = "Elite Control"
    Elite_Quarters_Access = "Elite Quarters Access"
    Elite_Quarters = "Elite Quarters"
    Elite_Research = "Elite Research"
    Fungal_Hall_A = "Fungal Hall A"
    Fungal_Hall_Access = "Fungal Hall Access"
    Fungal_Hall_B = "Fungal Hall B"
    Main_Quarry = "Main Quarry"
    Maintenance_Tunnel = "Maintenance Tunnel"
    Map_Station_Mines = "Map Station Mines"
    Metroid_Quarantine_A = "Metroid Quarantine A"
    Metroid_Quarantine_B = "Metroid Quarantine B"
    Mine_Security_Station = "Mine Security Station"
    Missile_Station_Mines = "Missile Station Mines"
    Omega_Research = "Omega Research"
    Ore_Processing = "Ore Processing"
    Phazon_Mining_Tunnel = "Phazon Mining Tunnel"
    Phazon_Processing_Center = "Phazon Processing Center"
    Processing_Center_Access = "Processing Center Access"
    Quarantine_Access_A = "Quarantine Access A"
    Quarantine_Access_B = "Quarantine Access B"
    Quarry_Access = "Quarry Access"
    Research_Access = "Research Access"
    Save_Station_Mines_A = "Save Station Mines A"
    Save_Station_Mines_B = "Save Station Mines B"
    Save_Station_Mines_C = "Save Station Mines C"
    Security_Access_A = "Security Access A"
    Security_Access_B = "Security Access B"
    Storage_Depot_A = "Storage Depot A"
    Storage_Depot_B = "Storage Depot B"
    Transport_Access = "Transport Access"
    Transport_to_Magmoor_Caverns_South = "Transport to Magmoor Caverns South"
    Ventilation_Shaft = "Ventilation Shaft"
    Waste_Disposal = "Waste Disposal"
    Aether_Lab_Entryway = "Aether Lab Entryway"
    Canyon_Entryway = "Canyon Entryway"
    Chamber_Access = "Chamber Access"
    Chapel_of_the_Elders = "Chapel of the Elders"
    Chapel_Tunnel = "Chapel Tunnel"
    Chozo_Ice_Temple = "Chozo Ice Temple"
    Control_Tower = "Control Tower"
    Courtyard_Entryway = "Courtyard Entryway"
    East_Tower = "East Tower"
    Frost_Cave_Access = "Frost Cave Access"
    Frost_Cave = "Frost Cave"
    Frozen_Pike = "Frozen Pike"
    Gravity_Chamber = "Gravity Chamber"
    Hunter_Cave_Access = "Hunter Cave Access"
    Hunter_Cave = "Hunter Cave"
    Hydra_Lab_Entryway = "Hydra Lab Entryway"
    Ice_Ruins_Access = "Ice Ruins Access"
    Ice_Ruins_East = "Ice Ruins East"
    Ice_Ruins_West = "Ice Ruins West"
    Lower_Edge_Tunnel = "Lower Edge Tunnel"
    North_Quarantine_Tunnel = "North Quarantine Tunnel"
    Observatory_Access = "Observatory Access"
    Observatory = "Observatory"
    Phendrana_Canyon = "Phendrana Canyon"
    Phendrana_Shorelines = "Phendrana Shorelines"
    Phendranas_Edge = "Phendrana's Edge"
    Pike_Access = "Pike Access"
    Plaza_Walkway = "Plaza Walkway"
    Quarantine_Access = "Quarantine Access"
    Quarantine_Cave = "Quarantine Cave"
    Quarantine_Monitor = "Quarantine Monitor"
    Research_Core_Access = "Research Core Access"
    Research_Core = "Research Core"
    Research_Entrance = "Research Entrance"
    Research_Lab_Aether = "Research Lab Aether"
    Research_Lab_Hydra = "Research Lab Hydra"
    Ruined_Courtyard = "Ruined Courtyard"
    Ruins_Entryway = "Ruins Entryway"
    Save_Station_A = "Save Station A"
    Save_Station_B = "Save Station B"
    Save_Station_C = "Save Station C"
    Save_Station_D = "Save Station D"
    Security_Cave = "Security Cave"
    Shoreline_Entrance = "Shoreline Entrance"
    South_Quarantine_Tunnel = "South Quarantine Tunnel"
    Specimen_Storage = "Specimen Storage"
    Storage_Cave = "Storage Cave"
    Temple_Entryway = "Temple Entryway"
    Transport_to_Magmoor_Caverns_West = "Transport to Magmoor Caverns West"
    Upper_Edge_Tunnel = "Upper Edge Tunnel"
    West_Tower_Entrance = "West Tower Entrance"
    West_Tower = "West Tower"
    Alcove = "Alcove"
    Arbor_Chamber = "Arbor Chamber"
    Artifact_Temple = "Artifact Temple"
    Biohazard_Containment = "Biohazard Containment"
    Biotech_Research_Area_1 = "Biotech Research Area 1"
    Canyon_Cavern = "Canyon Cavern"
    Cargo_Freight_Lift_to_Deck_Gamma = "Cargo Freight Lift to Deck Gamma"
    Connection_Elevator_to_Deck_Beta = "Connection Elevator to Deck Beta"
    Deck_Beta_Conduit_Hall = "Deck Beta Conduit Hall"
    Deck_Beta_Security_Hall = "Deck Beta Security Hall"
    Deck_Beta_Transit_Hall = "Deck Beta Transit Hall"
    Frigate_Access_Tunnel = "Frigate Access Tunnel"
    Frigate_Crash_Site = "Frigate Crash Site"
    Great_Tree_Chamber = "Great Tree Chamber"
    Great_Tree_Hall = "Great Tree Hall"
    Gully = "Gully"
    Hydro_Access_Tunnel = "Hydro Access Tunnel"
    Landing_Site = "Landing Site"
    Life_Grove_Tunnel = "Life Grove Tunnel"
    Life_Grove = "Life Grove"
    Main_Ventilation_Shaft_Section_A = "Main Ventilation Shaft Section A"
    Main_Ventilation_Shaft_Section_B = "Main Ventilation Shaft Section B"
    Main_Ventilation_Shaft_Section_C = "Main Ventilation Shaft Section C"
    Overgrown_Cavern = "Overgrown Cavern"
    Reactor_Access = "Reactor Access"
    Reactor_Core = "Reactor Core"
    Root_Cave = "Root Cave"
    Root_Tunnel = "Root Tunnel"
    Savestation = "Savestation"
    Tallon_Canyon = "Tallon Canyon"
    Temple_Hall = "Temple Hall"
    Temple_Lobby = "Temple Lobby"
    Temple_Security_Station = "Temple Security Station"
    Transport_to_Chozo_Ruins_East = "Transport to Chozo Ruins East"
    Transport_to_Chozo_Ruins_South = "Transport to Chozo Ruins South"
    Transport_to_Chozo_Ruins_West = "Transport to Chozo Ruins West"
    Transport_to_Magmoor_Caverns_East = "Transport to Magmoor Caverns East"
    Transport_to_Phazon_Mines_East = "Transport to Phazon Mines East"
    Transport_Tunnel_D = "Transport Tunnel D"
    Transport_Tunnel_E = "Transport Tunnel E"
    Waterfall_Cavern = "Waterfall Cavern"


class StartRoomDifficulty(Enum):
    Normal = -1
    Safe = 0
    Dangerous = 1
    Buckle_Up = 2


class SuitUpgrade(StrEnum):
    Power_Beam = "Power Beam"
    Ice_Beam = "Ice Beam"
    Wave_Beam = "Wave Beam"
    Plasma_Beam = "Plasma Beam"
    Missile_Expansion = "Missile Expansion"
    Scan_Visor = "Scan Visor"
    Morph_Ball_Bomb = "Morph Ball Bomb"
    Power_Bomb_Expansion = "Power Bomb Expansion"
    Flamethrower = "Flamethrower"
    Thermal_Visor = "Thermal Visor"
    Charge_Beam = "Charge Beam"
    Super_Missile = "Super Missile"
    Grapple_Beam = "Grapple Beam"
    X_Ray_Visor = "X-Ray Visor"
    Ice_Spreader = "Ice Spreader"
    Space_Jump_Boots = "Space Jump Boots"
    Morph_Ball = "Morph Ball"
    Combat_Visor = "Combat Visor"
    Boost_Ball = "Boost Ball"
    Spider_Ball = "Spider Ball"
    Power_Suit = "Power Suit"
    Gravity_Suit = "Gravity Suit"
    Varia_Suit = "Varia Suit"
    Phazon_Suit = "Phazon Suit"
    Energy_Tank = "Energy Tank"
    Wavebuster = "Wavebuster"
    Unlimited_Missiles = "Unlimited Missiles"
    Unlimited_Power_Bombs = "Unlimited Power Bombs"
    Missile_Launcher = "Missile Launcher"
    Main_Power_Bomb = "Power Bomb (Main)"
    Spring_Ball = "Spring Ball"
    Power_Charge_Beam = "Charge Beam (Power)"
    Wave_Charge_Beam = "Charge Beam (Wave)"
    Ice_Charge_Beam = "Charge Beam (Ice)"
    Plasma_Charge_Beam = "Charge Beam (Plasma)"
    Nothing = "Nothing"
    #Floaty_Jump = "Floaty Jump"
    #Ice_Trap = "Ice Trap"

    def __str__(self):
        return self.value


class TrickDifficulty(Enum):
    No_Tricks = -1
    Easy = 0
    Medium = 1
    Hard = 2


class TrickType(StrEnum):
    L_Jump = "L Jump"
    L_Jump_Space_Jump = "L-Jump Space Jump"
    R_Jump = "R-Jump"
    R_Jump_Space_Jump = "R-Jump Space Jump"
    Scan_Dash = "Scan Dash"
    Scan_Dash_Space_Jump = "Scan Dash"
    Slope_Jump_With_Space_Jump = "Slope Jump With Space Jump"
    Slope_Jump = "Slope Jump No Space Jump"
    Combat_Dash = "Combat Dash"
    Combat_Dash_Space_Jump = "Combat Dash"
    Infinite_Speed = "Infinite Speed"
    Double_Bomb_Jump = "Double Bomb Jump"
    No_XRay = "No XRay"

    def __str__(self):
        return self.value