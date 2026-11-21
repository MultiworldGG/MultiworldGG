# All the dolphin connection messages used in the client
CONNECTION_REFUSED_STATUS: str = "Detected a non-randomized ROM for Super Mario Sunshine. Please close and load a different one. Retrying in 5 seconds..."
CONNECTION_LOST_STATUS: str = "Dolphin connection was lost. Please restart your emulator and make sure Super Mario Sunshine is running."
CONNECTION_VERIFY_SERVER: str = "Dolphin was confirmed to be opened and ready, Connect to the server when ready..."
CONNECTION_INITIAL_STATUS: str = "Dolphin emulator was not detected to be running. Retrying in 5 seconds..."
DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY: str = "Dolphin did not load the ROM correctly. Close only the game / dolphin launcher and try again..."
CONNECTION_CONNECTED_STATUS: str = "Dolphin is connected, AP is connected, Ready to play Super Mario Sunshine!"
AP_REFUSED_STATUS: str = "AP Refused to connect for one or more reasons, see above for more details."

WORLD_NAME = "Super Mario Sunshine"
CLIENT_NAME = "Super Mario Sunshine Client"
WORLD_VERSION = "0.6.3"
GAME_ID: str = "GMSEAP"
SMS_USA_MD5 = 0x0c6d2edae9fdf40dfc410ff1623e4119

DME_DOLPHIN_PROCESS_NAME = "DME_DOLPHIN_PROCESS_NAME"
WAIT_TIMER_LONG_TIMEOUT: int = 5
WAIT_TIMER_SHORT_TIMEOUT: float = 0.125

CUSTOM_CODE_OFFSET_START = 0x3F00A0
SMS_PLAYER_NAME_BYTE_LENGTH = 64