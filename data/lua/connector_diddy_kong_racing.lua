-- Diddy Kong Racing Connector Lua
-- Adapted by zakwiz from the Banjo-Tooie Connector Lua

-- Banjo-Tooie Connector Lua by Mike Jackson (jjjj12212) with the help of Rose (Oktorose),
-- the OOT Archipelago team, ScriptHawk BT.lua & kaptainkohl for BTrando.lua, modifications from Unalive & HemiJackson

status, _ = pcall(require, "common")
if not status then
    print("ERROR: Missing required Lua dependencies, this Lua script must be placed in the data/lua folder of your Archipelago installation.")
    return
end

socket = require("socket")
json = require("json")

REQUIRED_BIZHAWK_MAJOR_VERSION = 2
MINIMUM_BIZHAWK_MINOR_VERSION = 10
VANILLA_ROM_HASH = "0CB115D8716DBBC2922FDA38E533B9FE63BB9670"
PATCHED_ROM_HASH = "70317F5C9B130B948C6257E0F4835C5C067380D5"
APWORLD_VERSION = "DKRv1.1.4"

STATE_OK = "Ok"
STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
STATE_UNINITIALIZED = "Uninitialized"
current_state = STATE_UNINITIALIZED
frame = 0

slot_loaded = false
in_save_file = false
in_save_file_counter = 0
save_file_init_complete = false
current_map = 0
paused = false

receive_map = {}
message_queue = {}
n64_sent_message_count = 0

BYTE = "BYTE"
BIT = "BIT"

TIMBERS_ISLAND_BALLOON = "TIMBERS_ISLAND_BALLOON"
DINO_DOMAIN_BALLOON = "DINO_DOMAIN_BALLOON"
SNOWFLAKE_MOUNTAIN_BALLOON = "SNOWFLAKE_MOUNTAIN_BALLOON"
SHERBET_ISLAND_BALLOON = "SHERBET_ISLAND_BALLOON"
DRAGON_FOREST_BALLOON = "DRAGON_FOREST_BALLOON"
FUTURE_FUN_LAND_BALLOON = "FUTURE_FUN_LAND_BALLOON"
FIRE_MOUNTAIN_KEY = "FIRE_MOUNTAIN_KEY"
ICICLE_PYRAMID_KEY = "ICICLE_PYRAMID_KEY"
DARKWATER_BEACH_KEY = "DARKWATER_BEACH_KEY"
SMOKEY_CASTLE_KEY = "SMOKEY_CASTLE_KEY"
WIZPIG_AMULET_PIECE = "WIZPIG_AMULET_PIECE"
TT_AMULET_PIECE = "TT_AMULET_PIECE"

ITEM_IDS = {
    TIMBERS_ISLAND_BALLOON = 1616000,
    DINO_DOMAIN_BALLOON = 1616001,
    SNOWFLAKE_MOUNTAIN_BALLOON = 1616002,
    SHERBET_ISLAND_BALLOON = 1616003,
    DRAGON_FOREST_BALLOON = 1616004,
    FUTURE_FUN_LAND_BALLOON = 1616005,
    FIRE_MOUNTAIN_KEY = 1616006,
    ICICLE_PYRAMID_KEY = 1616007,
    DARKWATER_BEACH_KEY = 1616008,
    SMOKEY_CASTLE_KEY = 1616009,
    WIZPIG_AMULET_PIECE = 1616010,
    TT_AMULET_PIECE = 1616011
}

ITEM_ID_TO_ROMHACK_ITEM_INDEX = {
    [1616000] = 0,
    [1616001] = 1,
    [1616002] = 2,
    [1616003] = 3,
    [1616004] = 4,
    [1616005] = 5,
    [1616006] = 6,
    [1616007] = 7,
    [1616008] = 8,
    [1616009] = 9,
    [1616010] = 10,
    [1616011] = 11
}

Ram = {
    RDRAM_BASE = 0x80000000,
    RDRAM_SIZE = 0x800000,
    ADDRESS = {
        IN_SAVE_FILE_1 = 0x214E72,
        IN_SAVE_FILE_2 = 0x214E76,
        IN_SAVE_FILE_3 = 0x21545A,
        PAUSED = 0x115F79,
        CHARACTER_UNLOCKS = 0x0DFD9B,
        CURRENT_MAP = 0x121167,
        TIMBERS_ISLAND_BALLOONS_1 = 0x1FCAE8,
        TIMBERS_ISLAND_BALLOONS_2 = 0x1FCAE9,
        BOSS_COMPLETION_1 = 0x1FC9DC,
        BOSS_COMPLETION_2 = 0x1FC9DD,
        -- Dino Domain
        ANCIENT_LAKE = 0x1FCAFF,
        FOSSIL_CANYON = 0x1FCAF7,
        JUNGLE_FALLS = 0x1FCB5F,
        HOT_TOP_VOLCANO = 0x1FCB07,
        FIRE_MOUNTAIN = 0x1FCB17,
        -- Snowflake Mountain
        EVERFROST_PEAK = 0x1FCB1F,
        WALRUS_COVE = 0x1FCB03,
        SNOWBALL_VALLEY = 0x1FCB0F,
        FROSTY_VILLAGE = 0x1FCB5B,
        ICICLE_PYRAMID = 0x1FCB57,
        -- Sherbet Island
        WHALE_BAY = 0x1FCB0B,
        CRESCENT_ISLAND = 0x1FCB13,
        PIRATE_LAGOON = 0x1FCAFB,
        TREASURE_CAVES = 0x1FCB63,
        DARKWATER_BEACH = 0x1FCB53,
        -- Dragon Forest
        WINDMILL_PLAINS = 0x1FCB3B,
        GREENWOOD_VILLAGE = 0x1FCB33,
        BOULDER_CANYON = 0x1FCB37,
        HAUNTED_WOODS = 0x1FCB67,
        SMOKEY_CASTLE = 0x1FCB4F,
        -- Future Fun Land
        SPACEDUST_ALLEY = 0x1FCB2F,
        DARKMOON_CAVERNS = 0x1FCB6B,
        SPACEPORT_ALPHA = 0x1FCB27,
        STAR_CITY = 0x1FCB6F
    }
}

function Ram:check_flag(byte, _bit)
    local current_value = mainmemory.readbyte(byte)

    return bit.check(current_value, _bit)
end

function Ram:set_flag(byte, _bit)
    local current_value = mainmemory.readbyte(byte)
    mainmemory.writebyte(byte, bit.set(current_value, _bit))
end

function Ram:get_value(byte)
    return mainmemory.readbyte(byte)
end

function Ram:set_value(byte, value)
    return mainmemory.writebyte(byte, value)
end

function Ram:increment_counter(byte)
    local current_value = mainmemory.readbyte(byte)
    mainmemory.writebyte(byte, current_value + 1)
end

function Ram:decrement_counter(byte)
    local current_value = mainmemory.readbyte(byte)
    mainmemory.writebyte(byte, current_value - 1)
end

function Ram:dereference_pointer(addr)
    if type(addr) == "number" and addr >= 0 and addr < (self.RDRAM_SIZE - 4) then
        local address = mainmemory.read_u32_be(addr);
        if self:is_pointer(address) then
            return address - self.RDRAM_BASE;
        end
    end
end

function Ram:is_pointer(value)
    return type(value) == "number" and value >= self.RDRAM_BASE and value < self.RDRAM_BASE + self.RDRAM_SIZE;
end

RomHack = {
    BASE_POINTER = 0x400000,
    MAX_MESSAGE_BYTES = 50,
    RECEIVED_ITEM_COUNTS = 0x0,
    DOOR_COSTS = 0xF,
    TRACKS  = 0x3C,
      ACTUAL_TRACK = 0x0,
      ADVENTURE = 0x1,
      MUSIC = 0x2,
    MESSAGE_TEXT = 0x83,
    N64_RECEIVED_MESSAGE_COUNT = 0xBE,
    SETTINGS = 0xBF,
      VICTORY_CONDITION = 0x0,
      OPEN_WORLDS = 0x1,
      SHUFFLE_WIZPIG_AMULET = 0x2,
      SHUFFLE_TT_AMULET = 0x3,
      DOOR_PROGRESSION = 0x4,
      SHUFFLE_DOOR_REQUIREMENTS = 0x6,
      BOSS_1_REGIONAL_BALLOONS = 0x7,
      BOSS_2_REGIONAL_BALLOONS = 0x8,
      WIZPIG_1_AMULET_PIECES = 0x9,
      WIZPIG_2_AMULET_PIECES = 0xA,
      WIZPIG_2_BALLOONS = 0xB,
      SKIP_TROPHY_RACES = 0xC,
      RANDOMIZE_CHARACTER_ON_MAP_CHANGE = 0xD,
      CHANGE_BALLOONS = 0xE,
      POWER_UP_BALLOON_TYPE = 0xF,
      SHUFFLE_VEHICLES = 0x11,
      SHUFFLE_VEHICLES_INCLUDING_OVERWORLD = 0x12,
      BOULDER_CANYON_BELL_BALLOON = 0x10,
      SHUFFLE_TRACKS = 0x13,
      SHUFFLE_OPPONENT_KARTS = 0x14,
    N64_PROCESSED_MESSAGE_COUNT = 0xD4,
    N64_KEYS_LOCATION = 0xD5,
    N64_BALLOON_LOCATIONS = 0xD8,
    N64_BALLOON_ID = 0xE0,
    N64_BALLOON_COLLECTED = 0xE2,
      N64_BALLOON_INDEX = 0,
    TOTAL_BALLOONS = 0x4D9,
    N64_SILVERCOINS_LOCATIONS = 0x4E8,
    N64_SILVERCOINS_ID = 0x4F0,
    N64_SILVERCOINS_COLLECTED = 0x4F2,
      N64_SILVERCOINS_INDEX = 0,
    ROM_MAJOR_VERSION = 0x570,
    ROM_MINOR_VERSION = 0x572,
    ROM_PATCH_VERSION = 0x573
}

function RomHack:set_base_address()
    self.base_address = Ram:dereference_pointer(self.BASE_POINTER)
end

function RomHack:check_flag(byte, _bit)
    return Ram:check_flag(self.base_address + byte, _bit)
end

function RomHack:set_flag(byte, _bit)
    Ram:set_flag(self.base_address + byte, _bit)
end

function RomHack:get_value(byte)
    return Ram:get_value(self.base_address + byte)
end

function RomHack:set_value(byte, value)
    return Ram:set_value(self.base_address + byte, value)
end

function RomHack:increment_counter(byte)
    local current_value = self:get_value(byte)
    self:set_value(byte, current_value + 1)
end

ITEM_TO_LOCATION_ADDRESSES = {
    [TIMBERS_ISLAND_BALLOON] = {
        ["1616100"] = { -- Bridge Balloon
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_1,
            [BIT] = 2
        },
        ["1616101"] = { -- Waterfall Balloon
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_1,
            [BIT] = 6
        },
        ["1616102"] = { -- River Balloon
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_2,
            [BIT] = 6
        },
        ["1616103"] = { -- Ocean Balloon
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_2,
            [BIT] = 2
        },
        ["1616104"] = { -- Taj Car Race
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_2,
            [BIT] = 3
        },
        ["1616105"] = { -- Taj Hovercraft Race
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_1,
            [BIT] = 3
        },
        ["1616106"] = { -- Taj Plane Race
            [BYTE] = Ram.ADDRESS.TIMBERS_ISLAND_BALLOONS_1,
            [BIT] = 4
        }
    },
    [DINO_DOMAIN_BALLOON] = {
        ["1616200"] = { -- Ancient Lake 1
            [BYTE] = Ram.ADDRESS.ANCIENT_LAKE,
            [BIT] = 1
        },
        ["1616201"] = { -- Ancient Lake 2
            [BYTE] = Ram.ADDRESS.ANCIENT_LAKE,
            [BIT] = 2
        },
        ["1616202"] = { -- Fossil Canyon 1
            [BYTE] = Ram.ADDRESS.FOSSIL_CANYON,
            [BIT] = 1
        },
        ["1616203"] = { -- Fossil Canyon 2
            [BYTE] = Ram.ADDRESS.FOSSIL_CANYON,
            [BIT] = 2
        },
        ["1616204"] = { -- Jungle Falls 1
            [BYTE] = Ram.ADDRESS.JUNGLE_FALLS,
            [BIT] = 1
        },
        ["1616205"] = { -- Jungle Falls 2
            [BYTE] = Ram.ADDRESS.JUNGLE_FALLS,
            [BIT] = 2
        },
        ["1616206"] = { -- Hot Top Volcano 1
            [BYTE] = Ram.ADDRESS.HOT_TOP_VOLCANO,
            [BIT] = 1
        },
        ["1616207"] = { -- Hot Top Volcano 2
            [BYTE] = Ram.ADDRESS.HOT_TOP_VOLCANO,
            [BIT] = 2
        }
    },
    [SNOWFLAKE_MOUNTAIN_BALLOON] = {
        ["1616300"] = { -- Everfrost Peak 1
            [BYTE] = Ram.ADDRESS.EVERFROST_PEAK,
            [BIT] = 1
        },
        ["1616301"] = { -- Everfrost Peak 2
            [BYTE] = Ram.ADDRESS.EVERFROST_PEAK,
            [BIT] = 2
        },
        ["1616302"] = { -- Walrus Cove 1
            [BYTE] = Ram.ADDRESS.WALRUS_COVE,
            [BIT] = 1
        },
        ["1616303"] = { -- Walrus Cove 2
            [BYTE] = Ram.ADDRESS.WALRUS_COVE,
            [BIT] = 2
        },
        ["1616304"] = { -- Snowball Valley 1
            [BYTE] = Ram.ADDRESS.SNOWBALL_VALLEY,
            [BIT] = 1
        },
        ["1616305"] = { -- Snowball Valley 2
            [BYTE] = Ram.ADDRESS.SNOWBALL_VALLEY,
            [BIT] = 2
        },
        ["1616306"] = { -- Frosty Village 1
            [BYTE] = Ram.ADDRESS.FROSTY_VILLAGE,
            [BIT] = 1
        },
        ["1616307"] = { -- Frosty Village 2
            [BYTE] = Ram.ADDRESS.FROSTY_VILLAGE,
            [BIT] = 2
        }
    },
    [SHERBET_ISLAND_BALLOON] = {
        ["1616400"] = { -- Whale Bay 1
            [BYTE] = Ram.ADDRESS.WHALE_BAY,
            [BIT] = 1
        },
        ["1616401"] = { -- Whale Bay 2
            [BYTE] = Ram.ADDRESS.WHALE_BAY,
            [BIT] = 2
        },
        ["1616402"] = { -- Crescent Island 1
            [BYTE] = Ram.ADDRESS.CRESCENT_ISLAND,
            [BIT] = 1
        },
        ["1616403"] = { -- Crescent Island 2
            [BYTE] = Ram.ADDRESS.CRESCENT_ISLAND,
            [BIT] = 2
        },
        ["1616404"] = { -- Pirate Lagoon 1
            [BYTE] = Ram.ADDRESS.PIRATE_LAGOON,
            [BIT] = 1
        },
        ["1616405"] = { -- Pirate Lagoon 2
            [BYTE] = Ram.ADDRESS.PIRATE_LAGOON,
            [BIT] = 2
        },
        ["1616406"] = { -- Treasure Caves 1
            [BYTE] = Ram.ADDRESS.TREASURE_CAVES,
            [BIT] = 1
        },
        ["1616407"] = { -- Treasure Caves 2
            [BYTE] = Ram.ADDRESS.TREASURE_CAVES,
            [BIT] = 2
        }
    },
    [DRAGON_FOREST_BALLOON] = {
        ["1616500"] = { -- Windmill Plains 1
            [BYTE] = Ram.ADDRESS.WINDMILL_PLAINS,
            [BIT] = 1
        },
        ["1616501"] = { -- Windmill Plains 2
            [BYTE] = Ram.ADDRESS.WINDMILL_PLAINS,
            [BIT] = 2
        },
        ["1616502"] = { -- Greenwood Village 1
            [BYTE] = Ram.ADDRESS.GREENWOOD_VILLAGE,
            [BIT] = 1
        },
        ["1616503"] = { -- Greenwood Village 2
            [BYTE] = Ram.ADDRESS.GREENWOOD_VILLAGE,
            [BIT] = 2
        },
        ["1616504"] = { -- Boulder Canyon 1
            [BYTE] = Ram.ADDRESS.BOULDER_CANYON,
            [BIT] = 1
        },
        ["1616505"] = { -- Boulder Canyon 2
            [BYTE] = Ram.ADDRESS.BOULDER_CANYON,
            [BIT] = 2
        },
        ["1616506"] = { -- Haunted Woods 1
            [BYTE] = Ram.ADDRESS.HAUNTED_WOODS,
            [BIT] = 1
        },
        ["1616507"] = { -- Haunted Woods 2
            [BYTE] = Ram.ADDRESS.HAUNTED_WOODS,
            [BIT] = 2
        }
    },
    [FUTURE_FUN_LAND_BALLOON] = {
        ["1616600"] = { -- Spacedust Alley 1
            [BYTE] = Ram.ADDRESS.SPACEDUST_ALLEY,
            [BIT] = 1
        },
        ["1616601"] = { -- Spacedust Alley 2
            [BYTE] = Ram.ADDRESS.SPACEDUST_ALLEY,
            [BIT] = 2
        },
        ["1616602"] = { -- Darkmoon Caverns 1
            [BYTE] = Ram.ADDRESS.DARKMOON_CAVERNS,
            [BIT] = 1
        },
        ["1616603"] = { -- Darkmoon Caverns 2
            [BYTE] = Ram.ADDRESS.DARKMOON_CAVERNS,
            [BIT] = 2
        },
        ["1616604"] = { -- Spaceport Alpha 1
            [BYTE] = Ram.ADDRESS.SPACEPORT_ALPHA,
            [BIT] = 1
        },
        ["1616605"] = { -- Spaceport Alpha 2
            [BYTE] = Ram.ADDRESS.SPACEPORT_ALPHA,
            [BIT] = 2
        },
        ["1616606"] = { -- Star City 1
            [BYTE] = Ram.ADDRESS.STAR_CITY,
            [BIT] = 1
        },
        ["1616607"] = { -- Star City 2
            [BYTE] = Ram.ADDRESS.STAR_CITY,
            [BIT] = 2
        }
    },
    [FIRE_MOUNTAIN_KEY] = {
        ["1616208"] = {
            [BYTE] = RomHack.N64_KEYS_LOCATION,
            [BIT] = 1
        }
    },
    [ICICLE_PYRAMID_KEY] = {
        ["1616308"] = {
            [BYTE] = RomHack.N64_KEYS_LOCATION,
            [BIT] = 3
        }
    },
    [DARKWATER_BEACH_KEY] = {
        ["1616408"] = {
            [BYTE] = RomHack.N64_KEYS_LOCATION,
            [BIT] = 2
        }
    },
    [SMOKEY_CASTLE_KEY] = {
        ["1616508"] = {
            [BYTE] = RomHack.N64_KEYS_LOCATION,
            [BIT] = 4
        },
    },
    [WIZPIG_AMULET_PIECE] = {
        ["1616210"] = { -- Tricky 2
            [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
            [BIT] = 7
        },
        ["1616310"] = { -- Bluey 2
            [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_1,
            [BIT] = 1
        },
        ["1616410"] = { -- Bubbler 2
            [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_1,
            [BIT] = 0
        },
        ["1616510"] = { -- Smokey 2
            [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_1,
            [BIT] = 2
        },
    },
    [TT_AMULET_PIECE] = {
        ["1616209"] = { -- Fire Mountain
            [BYTE] = Ram.ADDRESS.FIRE_MOUNTAIN,
            [BIT] = 1
        },
        ["1616309"] = { -- Icicle Pyramid
            [BYTE] = Ram.ADDRESS.ICICLE_PYRAMID,
            [BIT] = 1
        },
        ["1616409"] = { -- Darkwater Beach
            [BYTE] = Ram.ADDRESS.DARKWATER_BEACH,
            [BIT] = 1
        },
        ["1616509"] = { -- Smokey Castle
            [BYTE] = Ram.ADDRESS.SMOKEY_CASTLE,
            [BIT] = 1
        },
    }
}

local BALLOON_ITEM_ID_TO_BOSS_1_COMPLETION_ADDRESS = {
    [ITEM_IDS.DINO_DOMAIN_BALLOON] = {
        [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
        [BIT] = 1
    },
    [ITEM_IDS.SNOWFLAKE_MOUNTAIN_BALLOON] = {
        [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
        [BIT] = 3
    },
    [ITEM_IDS.SHERBET_ISLAND_BALLOON] = {
        [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
        [BIT] = 2
    },
    [ITEM_IDS.DRAGON_FOREST_BALLOON] = {
        [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
        [BIT] = 4
    }
}

VICTORY_CONDITION_TO_ADDRESS = {
    [0] = { -- Wizpig 1
        [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
        [BIT] = 0
    },
    [1] = { -- Wizpig 2
        [BYTE] = Ram.ADDRESS.BOSS_COMPLETION_2,
        [BIT] = 5
    }
}

VANILLA_TRACK_ADDRESS_ORDER = {
    Ram.ADDRESS.ANCIENT_LAKE,
    Ram.ADDRESS.FOSSIL_CANYON,
    Ram.ADDRESS.JUNGLE_FALLS,
    Ram.ADDRESS.HOT_TOP_VOLCANO,
    Ram.ADDRESS.EVERFROST_PEAK,
    Ram.ADDRESS.WALRUS_COVE,
    Ram.ADDRESS.SNOWBALL_VALLEY,
    Ram.ADDRESS.FROSTY_VILLAGE,
    Ram.ADDRESS.WHALE_BAY,
    Ram.ADDRESS.CRESCENT_ISLAND,
    Ram.ADDRESS.PIRATE_LAGOON,
    Ram.ADDRESS.TREASURE_CAVES,
    Ram.ADDRESS.WINDMILL_PLAINS,
    Ram.ADDRESS.GREENWOOD_VILLAGE,
    Ram.ADDRESS.BOULDER_CANYON,
    Ram.ADDRESS.HAUNTED_WOODS,
    Ram.ADDRESS.SPACEDUST_ALLEY,
    Ram.ADDRESS.DARKMOON_CAVERNS,
    Ram.ADDRESS.SPACEPORT_ALPHA,
    Ram.ADDRESS.STAR_CITY
}

VANILLA_TRACK_ADDRESS_TO_INDEX = {
    [Ram.ADDRESS.ANCIENT_LAKE] = 1,
    [Ram.ADDRESS.FOSSIL_CANYON] = 2,
    [Ram.ADDRESS.JUNGLE_FALLS] = 3,
    [Ram.ADDRESS.HOT_TOP_VOLCANO] = 4,
    [Ram.ADDRESS.EVERFROST_PEAK] = 5,
    [Ram.ADDRESS.WALRUS_COVE] = 6,
    [Ram.ADDRESS.SNOWBALL_VALLEY] = 7,
    [Ram.ADDRESS.FROSTY_VILLAGE] = 8,
    [Ram.ADDRESS.WHALE_BAY] = 9,
    [Ram.ADDRESS.CRESCENT_ISLAND] = 10,
    [Ram.ADDRESS.PIRATE_LAGOON] = 11,
    [Ram.ADDRESS.TREASURE_CAVES] = 12,
    [Ram.ADDRESS.WINDMILL_PLAINS] = 13,
    [Ram.ADDRESS.GREENWOOD_VILLAGE] = 14,
    [Ram.ADDRESS.BOULDER_CANYON] = 15,
    [Ram.ADDRESS.HAUNTED_WOODS] = 16,
    [Ram.ADDRESS.SPACEDUST_ALLEY] = 17,
    [Ram.ADDRESS.DARKMOON_CAVERNS] = 18,
    [Ram.ADDRESS.SPACEPORT_ALPHA] = 19,
    [Ram.ADDRESS.STAR_CITY] = 20
}

function main()
    print("Diddy Kong Racing Archipelago Version: " .. APWORLD_VERSION)
    print("----------------")

    validate_bizhawk_version()
    validate_rom_hash()

    server, error = socket.bind("localhost", 21221)

    event.onframeend(handle_frame)
end

function validate_bizhawk_version()
    local bizhawk_version = client.getversion()
    local first_dot_index, _ = string.find(bizhawk_version, ".", 1, true)
    local second_dot_index, _ = string.find(bizhawk_version, ".", first_dot_index + 1, true)
    local bizhawk_major_version = tonumber(string.sub(bizhawk_version, 0, first_dot_index))
    local bizhawk_minor_version
    if second_dot_index then
        bizhawk_minor_version = tonumber(string.sub(bizhawk_version, first_dot_index + 1, second_dot_index))
    else
        bizhawk_minor_version = tonumber(string.sub(bizhawk_version, first_dot_index + 1))
    end
    if bizhawk_major_version ~= REQUIRED_BIZHAWK_MAJOR_VERSION or bizhawk_minor_version < MINIMUM_BIZHAWK_MINOR_VERSION then
        error("ERROR: Your Bizhawk version (" .. bizhawk_version .. ") is not supported, the minimum supported version is " .. REQUIRED_BIZHAWK_MAJOR_VERSION .. "." .. MINIMUM_BIZHAWK_MINOR_VERSION)
    end
end

function validate_rom_hash()
    local rom_hash = gameinfo.getromhash()
    if rom_hash == VANILLA_ROM_HASH then
        error("ERROR: Incorrect ROM hash, you're using the vanilla Diddy Kong Racing ROM, use the patched ROM instead (see client for location)")
    elseif rom_hash ~= PATCHED_ROM_HASH then
        error("ERROR: Incorrect ROM hash, make sure you're running the correct patched Diddy Kong Racing ROM")
    end
end

function handle_frame()
    frame = frame + 1
    if current_state == STATE_UNINITIALIZED then
        if  frame % 60 == 1 then
            server:settimeout(2)
            local client, timeout = server:accept()

            if not timeout then
                print("Initial connection made")
                print("----------------")

                current_state = STATE_INITIAL_CONNECTION_MADE
                socket = client
                socket:settimeout(0)
            else
                print("ERROR: Connection failed, ensure Diddy Kong Racing Client is running and connected, then re-run connector_diddy_kong_racing.lua")
                print("----------------")

                return
            end
        end
    else
        if frame % 10 == 1 then
            check_if_in_save_file()
            if slot_loaded and in_save_file then
                dpad_stats()

                if not save_file_init_complete then
                    set_races_as_visited()
                    save_file_init_complete = true
                end
            end
        end

        if frame % 60 == 1 then
            local new_map = Ram:get_value(Ram.ADDRESS.CURRENT_MAP)
            if new_map == 0x17 then -- Title screen
                Ram:set_flag(Ram.ADDRESS.CHARACTER_UNLOCKS, 0) -- Unlock T.T.
                Ram:set_flag(Ram.ADDRESS.CHARACTER_UNLOCKS, 1) -- Unlock Drumstick

                if slot_loaded then -- For when game is reset while connected
                    pass_settings_to_romhack()
                end
            end

            if new_map ~= current_map then
                current_map = new_map
                client.saveram()
            end

            communicate_with_client()

            if slot_loaded then
                display_next_message_if_no_message_displayed()
            end
        end
    end
end

function check_if_in_save_file()
    local in_save_file_1 = Ram:get_value(Ram.ADDRESS.IN_SAVE_FILE_1) ~= 0
    local in_save_file_2 = Ram:get_value(Ram.ADDRESS.IN_SAVE_FILE_2) ~= 0
    local in_save_file_3 = Ram:get_value(Ram.ADDRESS.IN_SAVE_FILE_3) ~= 0

    if in_save_file then
        if not (in_save_file_1 and in_save_file_2 and in_save_file_3) then
            print("Exited save file")
            print("----------------")
            in_save_file = false
            init_complete = false
            in_save_file_counter = 0
        end
    elseif in_save_file_1 and in_save_file_2 and in_save_file_3 then
        if in_save_file_counter == 6 then
            print("Entered save file")
            print("Press D-PAD UP to see collected items")
            print("----------------")
            in_save_file = true
        else
            in_save_file_counter = in_save_file_counter + 1
        end
    end
end

function set_races_as_visited()
    Ram:set_flag(Ram.ADDRESS.ANCIENT_LAKE, 0)
    Ram:set_flag(Ram.ADDRESS.FOSSIL_CANYON, 0)
    Ram:set_flag(Ram.ADDRESS.JUNGLE_FALLS, 0)
    Ram:set_flag(Ram.ADDRESS.HOT_TOP_VOLCANO, 0)
    Ram:set_flag(Ram.ADDRESS.EVERFROST_PEAK, 0)
    Ram:set_flag(Ram.ADDRESS.WALRUS_COVE, 0)
    Ram:set_flag(Ram.ADDRESS.SNOWBALL_VALLEY, 0)
    Ram:set_flag(Ram.ADDRESS.FROSTY_VILLAGE, 0)
    Ram:set_flag(Ram.ADDRESS.WHALE_BAY, 0)
    Ram:set_flag(Ram.ADDRESS.CRESCENT_ISLAND, 0)
    Ram:set_flag(Ram.ADDRESS.PIRATE_LAGOON, 0)
    Ram:set_flag(Ram.ADDRESS.TREASURE_CAVES, 0)
    Ram:set_flag(Ram.ADDRESS.WINDMILL_PLAINS, 0)
    Ram:set_flag(Ram.ADDRESS.GREENWOOD_VILLAGE, 0)
    Ram:set_flag(Ram.ADDRESS.BOULDER_CANYON, 0)
    Ram:set_flag(Ram.ADDRESS.HAUNTED_WOODS, 0)
    Ram:set_flag(Ram.ADDRESS.SPACEDUST_ALLEY, 0)
    Ram:set_flag(Ram.ADDRESS.DARKMOON_CAVERNS, 0)
    Ram:set_flag(Ram.ADDRESS.SPACEPORT_ALPHA, 0)
    Ram:set_flag(Ram.ADDRESS.STAR_CITY, 0)
end

function communicate_with_client()
    if not player and not seed then
        get_slot_data()
    else
        send_request_to_client()

        response, error = socket:receive()
        if error == "closed" then
            if current_state == STATE_OK then
                print("Connection closed")
                print("----------------")
            end

            current_state = STATE_UNINITIALIZED

            return
        elseif error == "timeout" then
            return
        elseif error then
            print(error)
            print("----------------")
            current_state = STATE_UNINITIALIZED

            return
        end

        process_client_response(json.decode(response))
    end
end

function get_slot_data()
    local request = {}
    request["getSlot"] = true

    local message = json.encode(request) .. "\n"
    socket:send(message)
    response, error = socket:receive()

    if error == "closed" then
        if current_state == STATE_OK then
            print("Connection closed")
            print("----------------")
        end

        current_state = STATE_UNINITIALIZED

        return
    elseif error == "timeout" then
        return
    elseif error then
        print(error)
        print("----------------")

        current_state = STATE_UNINITIALIZED

        return
    end

    process_slot(json.decode(response))
end

function process_slot(slot)
    if slot["slot_player"] and slot["slot_player"] ~= "" then
        player = slot["slot_player"]
    end

    if slot["slot_seed"] and slot["slot_seed"] ~= "" then
        seed = slot["slot_seed"]
    end

    if slot["slot_victory_condition"] and slot["slot_victory_condition"] ~= "" then
        victory_condition = slot["slot_victory_condition"]
    end

    if slot["slot_shuffle_wizpig_amulet"] and slot["slot_shuffle_wizpig_amulet"] == "true" then
        shuffle_wizpig_amulet = true
    else
        shuffle_wizpig_amulet = false
    end

    if slot["slot_shuffle_tt_amulet"] and slot["slot_shuffle_tt_amulet"] == "true" then
        shuffle_tt_amulet = true
    else
        shuffle_tt_amulet = false
    end

    if slot["slot_open_worlds"] and slot["slot_open_worlds"] == "true" then
        open_worlds = true
    else
        open_worlds = false
    end

    if slot["slot_door_unlock_requirements"] and next(slot["slot_door_unlock_requirements"]) then
        door_unlock_requirements = slot["slot_door_unlock_requirements"]
    end

    if slot["slot_door_requirement_progression"] and slot["slot_door_requirement_progression"] ~= "" then
        door_requirement_progression = slot["slot_door_requirement_progression"]
    end

    if slot["slot_shuffle_door_requirements"] and slot["slot_shuffle_door_requirements"] == "true" then
        shuffle_door_requirements = true
    else
        shuffle_door_requirements = false
    end

    if slot["slot_shuffle_race_entrances"] and slot["slot_shuffle_race_entrances"] == "true" then
        shuffle_race_entrances = true
    else
        shuffle_race_entrances = false
    end

    if slot["slot_entrance_order"] and next(slot["slot_entrance_order"]) then
        entrance_order = slot["slot_entrance_order"]
        track_address_order = {}
        for i, entrance_num in pairs(entrance_order) do
            -- Convert from 0-indexed to 1-indexed
            track_address_order[entrance_num + 1] = VANILLA_TRACK_ADDRESS_ORDER[i]
        end
    end

    if slot["slot_boss_1_regional_balloons"] and slot["slot_boss_1_regional_balloons"] ~= "" then
        boss_1_regional_balloons = slot["slot_boss_1_regional_balloons"]
    end

    if slot["slot_boss_2_regional_balloons"] and slot["slot_boss_2_regional_balloons"] ~= "" then
        boss_2_regional_balloons = slot["slot_boss_2_regional_balloons"]
    end

    if slot["slot_wizpig_1_amulet_pieces"] and slot["slot_wizpig_1_amulet_pieces"] ~= "" then
        wizpig_1_amulet_pieces = slot["slot_wizpig_1_amulet_pieces"]
    end

    if slot["slot_wizpig_2_amulet_pieces"] and slot["slot_wizpig_2_amulet_pieces"] ~= "" then
        wizpig_2_amulet_pieces = slot["slot_wizpig_2_amulet_pieces"]
    end

    if slot["slot_wizpig_2_balloons"] and slot["slot_wizpig_2_balloons"] ~= "" then
        wizpig_2_balloons = slot["slot_wizpig_2_balloons"]
    end

    if slot["slot_skip_trophy_races"] and slot["slot_skip_trophy_races"] == "true" then
        skip_trophy_races = true
    else
        skip_trophy_races = false
    end

    if slot["slot_randomize_character_on_map_change"] and slot["slot_randomize_character_on_map_change"] == "true" then
        randomize_character_on_map_change = true
    else
        randomize_character_on_map_change = false
    end

    if slot["slot_track_versions"] and next(slot["slot_track_versions"]) then
        track_versions = slot["slot_track_versions"]
    end

    if slot["slot_music"] and next(slot["slot_music"]) then
        music = slot["slot_music"]
    end

    if slot["slot_power_up_balloon_type"] and slot["slot_power_up_balloon_type"] ~= "" then
        power_up_balloon_type = slot["slot_power_up_balloon_type"]
    end

    if seed then
        pass_settings_to_romhack()
        slot_loaded = true
    else
        return false
    end

    return true
end

function pass_settings_to_romhack()
    RomHack:set_base_address()

    RomHack:set_value(RomHack.SETTINGS + RomHack.VICTORY_CONDITION, victory_condition)
    RomHack:set_value(RomHack.SETTINGS + RomHack.OPEN_WORLDS, open_worlds and 1 or 0)
    RomHack:set_value(RomHack.SETTINGS + RomHack.SHUFFLE_WIZPIG_AMULET, shuffle_wizpig_amulet and 1 or 0)
    RomHack:set_value(RomHack.SETTINGS + RomHack.SHUFFLE_TT_AMULET, shuffle_tt_amulet and 1 or 0)
    RomHack:set_value(RomHack.SETTINGS + RomHack.DOOR_PROGRESSION, door_requirement_progression)
    RomHack:set_value(RomHack.SETTINGS + RomHack.SHUFFLE_DOOR_REQUIREMENTS, shuffle_door_requirements and 1 or 0)
    RomHack:set_value(RomHack.SETTINGS + RomHack.BOSS_1_REGIONAL_BALLOONS, boss_1_regional_balloons)
    RomHack:set_value(RomHack.SETTINGS + RomHack.BOSS_2_REGIONAL_BALLOONS, boss_2_regional_balloons)
    RomHack:set_value(RomHack.SETTINGS + RomHack.WIZPIG_1_AMULET_PIECES, wizpig_1_amulet_pieces)
    RomHack:set_value(RomHack.SETTINGS + RomHack.WIZPIG_2_AMULET_PIECES, wizpig_2_amulet_pieces)
    RomHack:set_value(RomHack.SETTINGS + RomHack.WIZPIG_2_BALLOONS, wizpig_2_balloons)
    RomHack:set_value(RomHack.SETTINGS + RomHack.SKIP_TROPHY_RACES, skip_trophy_races and 1 or 0)
    RomHack:set_value(RomHack.SETTINGS + RomHack.RANDOMIZE_CHARACTER_ON_MAP_CHANGE, randomize_character_on_map_change and 1 or 0)
    RomHack:set_value(RomHack.SETTINGS + RomHack.SHUFFLE_TRACKS, shuffle_race_entrances and 1 or 0)

    -- Enable shuffle vehicles and send all vehicles to make the player vehicle correct when shuffling tracks
    RomHack:set_value(RomHack.SETTINGS + RomHack.SHUFFLE_VEHICLES, 1)
    RomHack:set_value(RomHack.RECEIVED_ITEM_COUNTS + 12, 1) -- Kart
    RomHack:set_value(RomHack.RECEIVED_ITEM_COUNTS + 13, 1) -- Hovercraft
    RomHack:set_value(RomHack.RECEIVED_ITEM_COUNTS + 14, 1) -- Plane

    if door_unlock_requirements then
        for i, requirement in pairs(door_unlock_requirements) do
            local romhack_door_offset
            if i < 5 then
                -- Convert from 1-indexed to 0-indexed
                romhack_door_offset = i - 1
            else
                -- Skip Future Fun Land door cost
                romhack_door_offset = i
            end
            RomHack:set_value(RomHack.DOOR_COSTS + romhack_door_offset, requirement)
        end
    end

    for i, entrance_num in pairs(entrance_order) do
        local track_base_address = RomHack.TRACKS + (i * 3)
        -- Add 1 to entrance_num because 0 means vanilla
        RomHack:set_value(track_base_address, entrance_num + 1)
        RomHack:set_value(track_base_address + 1, track_versions[i] and 1 or 0)
        -- Add 1 to track_num because 0 means vanilla
        RomHack:set_value(track_base_address + 2, music[i] + 1)
    end

    if (power_up_balloon_type ~= 0) then
        RomHack:set_value(RomHack.SETTINGS + RomHack.CHANGE_BALLOONS, 1)

        local setting_to_value = {
            [1] = 5,
            [2] = 6,
            [3] = 0,
            [4] = 1,
            [5] = 2,
            [6] = 3,
            [7] = 4
        }
        RomHack:set_value(RomHack.SETTINGS + RomHack.POWER_UP_BALLOON_TYPE, setting_to_value[power_up_balloon_type])
    end

    RomHack:set_flag(RomHack.SETTINGS + RomHack.BOULDER_CANYON_BELL_BALLOON, 0)
end

function send_request_to_client()
    local request = {}
    request["playerName"] = player
    request["locations"] = get_local_checks()
    request["gameComplete"] = is_game_complete()
    request["currentMap"] = current_map

    if not in_save_file then
        request["sync_ready"] = "false"
    else
        request["sync_ready"] = "true"
    end

    local message = json.encode(request) .. "\n"
    local response, error = socket:send(message)
    if not response then
        print(error)
        print("----------------")
    elseif current_state == STATE_INITIAL_CONNECTION_MADE then
        current_state = STATE_TENTATIVELY_CONNECTED
    elseif current_state == STATE_TENTATIVELY_CONNECTED then
        print("Connected")
        print("----------------")

        current_state = STATE_OK
    end
end

function get_local_checks()
    local checks = {}
    for item, location_addresses in pairs(ITEM_TO_LOCATION_ADDRESSES) do
        for location_id, address in pairs(location_addresses) do
            if not checks[item] then
                checks[item] = {}
            end

            local is_collected
            if item == FIRE_MOUNTAIN_KEY
            or item == ICICLE_PYRAMID_KEY
            or item == DARKWATER_BEACH_KEY
            or item == SMOKEY_CASTLE_KEY then
                is_collected = RomHack:check_flag(address[BYTE], address[BIT])
            elseif item == DINO_DOMAIN_BALLOON
                or item == SNOWFLAKE_MOUNTAIN_BALLOON
                or item == SHERBET_ISLAND_BALLOON
                or item == DRAGON_FOREST_BALLOON
                or item == FUTURE_FUN_LAND_BALLOON then
                local vanilla_track_index = VANILLA_TRACK_ADDRESS_TO_INDEX[address[BYTE]]
                local track_address = track_address_order[vanilla_track_index]
                is_collected = Ram:check_flag(track_address, address[BIT])
            else
                is_collected = Ram:check_flag(address[BYTE], address[BIT])
            end

            checks[item][location_id] = is_collected
        end
    end

    previous_checks = checks

    return checks
end

function is_game_complete()
    if victory_condition and in_save_file then
        local victory_condition_address = VICTORY_CONDITION_TO_ADDRESS[victory_condition]
        if Ram:check_flag(victory_condition_address[BYTE], victory_condition_address[BIT]) then
            return "true"
        end
    end
    return "false"
end

function process_client_response(response)
    if not response then
        return
    end

    if response["slot_player"] then
        return
    end

    if next(response["items"]) then
        process_items((response["items"]))
    end

    if next(response["messages"]) then
        process_messages(response["messages"])
    end
end

function process_items(items)
    local new_item_received = false
    for ap_id, item_id in pairs(items) do
        local ap_id_string = tostring(ap_id)
        if not receive_map[ap_id_string] then
            receive_map[ap_id_string] = tostring(item_id)
            new_item_received = true
        end
    end

    if new_item_received then
        update_in_game_totals()
    end
end

function process_messages(messages)
    for _, message in pairs(messages) do
        if message["to_player"] == player then
            local message_start
            if message["from_player"] == player then
                message_start = "You found"
            else
                message_start = "Received"
            end

            local item_id = message["item_id"]
            local message_article
            if item_id == ITEM_IDS.FIRE_MOUNTAIN_KEY
            or item_id == ITEM_IDS.ICICLE_PYRAMID_KEY
            or item_id == ITEM_IDS.DARKWATER_BEACH_KEY
            or item_id == ITEM_IDS.SMOKEY_CASTLE_KEY then
                message_article = "the"
            else
                message_article = "a"
            end

            local item_name = message["item_name"]
            add_message_to_queue(string.format("%s %s %s", message_start, message_article, item_name));
        end
    end
end

function add_message_to_queue(message)
    table.insert(message_queue, message)
end

function display_next_message_if_no_message_displayed()
    local n64_processed_message_count = RomHack:get_value(RomHack.N64_PROCESSED_MESSAGE_COUNT)
    local n64_received_message_count = RomHack:get_value(RomHack.N64_RECEIVED_MESSAGE_COUNT)
    if n64_processed_message_count == n64_received_message_count then
        local displayed_message_id
        for id, message in pairs(message_queue) do
            display_message(message)
            displayed_message_id = id
            break
        end
        if displayed_message_id then
            table.remove(message_queue, displayed_message_id)
        end
    end
end

function display_message(message)
    local message_length = string.len(message)
    for i = 0, RomHack.MAX_MESSAGE_BYTES - 2 do
        if i < message_length then
            RomHack:set_value(RomHack.MESSAGE_TEXT + i, message:byte(i + 1));
        else
            RomHack:set_value(RomHack.MESSAGE_TEXT + i, 0);
        end
    end
    RomHack:set_value(RomHack.MESSAGE_TEXT + RomHack.MAX_MESSAGE_BYTES - 1, 0);
    n64_sent_message_count = n64_sent_message_count + 1
    RomHack:set_value(RomHack.N64_RECEIVED_MESSAGE_COUNT, n64_sent_message_count);
end

function update_totals_if_paused()
    local new_paused = Ram:check_flag(Ram.ADDRESS.PAUSED, 0)

    if new_paused and not paused then
        update_in_game_totals()
    end

    paused = new_paused
end

function update_in_game_totals()
    for item_id, romhack_item_index in pairs(ITEM_ID_TO_ROMHACK_ITEM_INDEX) do
        local item_count_to_set = get_received_item_count(item_id)

        if item_id >= 1616001 and item_id <= 1616004 then -- Regional balloons
            item_count_to_set = math.min(item_count_to_set, 8)

            if item_count_to_set >= boss_2_regional_balloons then
                local boss_1_completion_address = BALLOON_ITEM_ID_TO_BOSS_1_COMPLETION_ADDRESS[item_id]
                Ram:set_flag(boss_1_completion_address[BYTE], boss_1_completion_address[BIT])
            end
        elseif item_id >= 1616006 and item_id <= 1616009 then -- Keys
            item_count_to_set = math.min(item_count_to_set, 1)
        elseif item_id >= 1616010 and item_id <= 1616011 then -- Amulets
            item_count_to_set = math.min(item_count_to_set, 4)
        end

        RomHack:set_value(RomHack.RECEIVED_ITEM_COUNTS + romhack_item_index, item_count_to_set)
    end

    client.saveram()
end

function dpad_stats()
    local check_controls = joypad.get()

    if check_controls then
        if check_controls["P1 DPad U"] then
            print("Dino Domain balloons: " .. get_received_item_count(ITEM_IDS.DINO_DOMAIN_BALLOON))
            print("Snowflake Mountain balloons: " .. get_received_item_count(ITEM_IDS.SNOWFLAKE_MOUNTAIN_BALLOON))
            print("Sherbet Island balloons: " .. get_received_item_count(ITEM_IDS.SHERBET_ISLAND_BALLOON))
            print("Dragon Forest balloons: " .. get_received_item_count(ITEM_IDS.DRAGON_FOREST_BALLOON))
            print("")
            print("Keys:")
            if get_received_item_count(ITEM_IDS.FIRE_MOUNTAIN_KEY) > 0 then
                print("Fire Mountain")
            end
            if get_received_item_count(ITEM_IDS.ICICLE_PYRAMID_KEY) > 0 then
                print("Icicle Pyramid")
            end
            if get_received_item_count(ITEM_IDS.DARKWATER_BEACH_KEY) > 0 then
                print("Darkwater Beach")
            end
            if get_received_item_count(ITEM_IDS.SMOKEY_CASTLE_KEY) > 0 then
                print("Smokey Castle")
            end
            print("")
            print("Wizpig amulet pieces: " .. get_received_item_count(ITEM_IDS.WIZPIG_AMULET_PIECE))
            print("T.T. amulet pieces: " .. get_received_item_count(ITEM_IDS.TT_AMULET_PIECE))
            print("----------------")
        end
    end
end

function get_received_item_count(item_id)
    local received_item_count = 0
    if receive_map then
        for _, item in pairs(receive_map) do
            if item == tostring(item_id) then
                received_item_count = received_item_count + 1
            end
        end
    end

    return received_item_count
end

main()
