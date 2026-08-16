#ifndef AP_PLAYER_H
#define AP_PLAYER_H

// AP player ids are stored as 16-bit values in the ROM so large multiworlds
// with more than 255 slots can route items to the correct Archipelago player.
#define AP_MAX_PLAYER_ID 1024
#define AP_PLAYER_TABLE_SIZE (AP_MAX_PLAYER_ID + 1)

#endif
