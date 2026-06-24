# DELTARUNE Datastorage

All datastorage keys are prefixed with the player slot number than team number.

For example `current_location` is stored as `1_1_current_location` for player 1 in team 1.

## `current_location`

Dictionary of the current location data of a player

| Key              |        Type |
|------------------|------------:|
| current_chapter  |         int |
| current_room     |      string |

## `completed_chapters`

Dictionary of the state of chapter completion of a player.

| key              |        type |
|------------------|------------:|
| 1                |        bool |
| 2                |        bool |
| 3                |        bool |
| 4                |        bool |