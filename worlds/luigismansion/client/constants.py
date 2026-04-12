""" Collection of commonly used constants for Luigi's Mansion. """
from enum import StrEnum

CLIENT_VERSION: str = "V0.6.1"
CLIENT_NAME: str = "Luigi's Mansion Client"
RANDOMIZER_NAME: str = "Luigi's Mansion"

AP_LOGGER_NAME: str = "Client"
AP_WORLD_VERSION_NAME: str = "APWorldVersion"

# All the dolphin connection messages used in the client
CONNECTION_REFUSED_STATUS: str = "Detected a non-randomized ROM for LM. Please close and load a different one. Retrying in 5 seconds..."
CONNECTION_LOST_STATUS: str = "Dolphin connection was lost. Please restart your emulator and make sure LM is running."
NO_SLOT_NAME_STATUS: str = "No slot name was detected. Ensure a randomized ROM is loaded. Retrying in 5 seconds..."
CONNECTION_VERIFY_SERVER: str = "Dolphin was confirmed to be opened and ready, Connect to the server when ready..."
CONNECTION_INITIAL_STATUS: str = "Dolphin emulator was not detected to be running. Retrying in 5 seconds..."
DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY: str = "Dolphin did not load the ROM correctly. Close only the game / dolphin launcher and try again..."
CONNECTION_CONNECTED_STATUS: str = "Dolphin is connected, AP is connected, Ready to play LM!"
AP_REFUSED_STATUS: str = "AP Refused to connect for one or more reasons, see above for more details."

# Static time to wait for health and death checks
CHECKS_WAIT: int = 3
LONGER_MODIFIER: int = 2

# This address is used to track which room Luigi is in within the main mansion map (Map2)
ROOM_ID_ADDR: int = 0x803D8B7C
ROOM_ID_OFFSET: int = 0x35C

# Wait timer constants for between loops
WAIT_TIMER_SHORT_TIMEOUT: float = 0.125
WAIT_TIMER_MEDIUM_TIMEOUT: float = 1.5
WAIT_TIMER_LONG_TIMEOUT: float = 5

# GC Regional String ID length
GC_REGION_ID_LEGNTH: int = 6

class LM_GC_IDs(StrEnum):
    USA_ID = "GLME01"
    JP_ID = "GLMJ01"
    PAL_ID = "GLMP01"

class MEMORY_CONSTANTS:
    """ Constants which reference Luigi's Mansion memory allocations. """

    TRAINING_BUTTON_LAYOUT_SCREEN: int = 0x803D33AE
    """ Flag 168: Room flag used to determine if the button layout screen during training is present. """