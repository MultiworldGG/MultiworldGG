# Fly Destination Plando In Pokemon Crystal

This guide details how to use the Fly Destination Plando and Blocklist options in Pokemon Crystal, how to format them
and the values that can be used.

## Options formatting

Fly Destination Plando is an structured as a dictionary, where the keys are
"Fly Destination 1" to "Fly Destination 23", and the accepted values are either a map name or a warp name (listed below),
or a list of weights for randomly picking values.

Fly Destination Blocklist is structured as a list, which accepts the same values as Fly Destination Plando.

Map names act as shortcuts for every flypoint located on that map.

### Example

```yaml
  fly_destination_plando:
    Fly Destination 1: Route 34 Daycare South Entrance
    Fly Destination 5: Route 41
    Fly Destination 8:
      Radio Tower Entrance: 50
      Lavender Radio Tower Entrance: 50

  fly_destination_blocklist:
    - Blackthorn City
    - Route 45
    - Dark Cave Southeast Entrance
    - Whirl Islands Northeast Entrance
```

With this setup, the Fly Unlock 1 item is guaranteed to grant a flypoint to the Route 34 Daycare's yard once obtained.
The Fly Unlock 5 item will have 3 possible flypoints: the Northwest, Southwest, Southeast entrances to Whirl Islands,
which are the 3 flypoints remaining on Route 41 after excluding the Northeast entrance, which is part of the blocklist.
Finally, the Fly Unlock 8 item will grant a flypoint in front of either Goldenrod or Lavender Radio Tower,
with a 50/50 chance.

Furthermore, the blocklist will ensure that no flypoint ever goes to Eastern Johto.

## Limitations

Because of how the in-game Fly map scrolls between locations, an arbitrary limitation of one flypoint per landmark was
put in place. A landmark is a scrollable point on the map. There is generally a one-to-one correspondence between a map
and its landmark, with the following relevant exceptions:
- Olivine City and Olivine Port are separate maps and share the Olivine City landmark
- Vermilion City and Vermilion Port are separate maps and share the Vermilion City landmark
- Route 10 South and Route 10 North are separate maps and share the Route 10 landmark
- Route 23 and Route 23 Restored are separate maps and share the Route 23 landmark

When combined with Randomize Fly Unlocks set to "Exclude Silver Cave", Fly Destination 12 will be pinned to the Silver
Cave Pokecenter.

## List of maps and warps that can be used

### New Bark Town

- Elm's House Entrance
- Elm's Lab Entrance
- Player's House Entrance
- Player's Neighbor's House Entrance

### Route 29

- Route 29-46 Gate South Entrance

### Cherrygrove City

- Cherrygrove Evolution Speech House Entrance
- Cherrygrove Guide Gent's House Entrance
- Cherrygrove Gym Speech House Entrance
- Cherrygrove Mart Entrance
- Cherrygrove Pokecenter Entrance
- Flooded Mine South Entrance
  - *NOTE*: This warp is only available when the Flooded Mine YAML option is enabled.

### Route 30

- Route 30 Berry House Entrance
- Mr. Pokemon's House Entrance

### Route 31

- Dark Cave Southwest Entrance
- Route 31 Gate East Entrance

### Violet City

- Route 31 Gate West Entrance
- Sprout Tower Entrance
- Violet Gym Entrance
- Violet Kyle's House Entrance
- Violet Mart Entrance
- Violet Nickname Speech House Entrance
- Violet Pokecenter Entrance
- Violet Pokemon Academy Entrance

### Route 32

- Route 32 Gate East Entrance
- Route 32 Pokecenter Entrance
- Union Cave North Entrance
- Flooded Mine North Entrance
  - *NOTE*: This warp is only available when the Flooded Mine YAML option is enabled.

### Ruins of Alph Outside

- Route 32 Gate West Entrance
- Route 36 Gate South Entrance
- Ruins of Alph Research Center Entrance
- Ruins of Alph Inner Chamber Entrance
- Ruins of Alph Kabuto Chamber Entrance
- Ruins of Alph Aerodactyl Chamber Entrance
- Ruins of Alph Ho-Oh Chamber Entrance
- Ruins of Alph Omanyte Chamber Entrance
- Union Cave Ho-Oh Entrance
- Union Cave Omanyte Entrance

### Route 33

- Union Cave South Entrance

### Azalea Town

- Azalea Charcoal Kiln Entrance
- Azalea Gym Entrance
- Azalea Mart Entrance
- Azalea Pokecenter Entrance
- Azalea-Ilex Forest Gate East Entrance
- Kurt's House Entrance
- Slowpoke Well Entrance

### Route 34

- Route 34 Daycare South Entrance
- Route 34 Daycare West Entrance
- Route 34-Ilex Forest Gate North Entrance

### Goldenrod City

- Bill's Family's House Entrance
- Goldenrod Bike Shop Entrance
- Goldenrod Dept. Store Entrance
- Goldenrod Flower Shop Entrance
- Goldenrod Game Corner Entrance
- Goldenrod Gym Entrance
- Goldenrod Happiness Rater Entrance
- Goldenrod Magnet Train Station Entrance
- Goldenrod Name Rater Entrance
- Goldenrod PP Speech House Entrance
- Goldenrod Pokecenter Entrance
- Goldenrod Underground North Entrance
- Goldenrod Underground South Entrance
- Radio Tower Entrance
- Route 35 Gate South Entrance

### Route 35

- Route 35 Gate North Entrance
- Route 35-National Park Gate South Entrance

### Route 36

- Route 36 Gate North Entrance
- Route 36-National Park Gate East Entrance

### Ecruteak City

- Burned Tower Entrance
- Ecruteak Dance Theater Entrance
- Ecruteak Gym Entrance
- Ecruteak Itemfinder House Entrance
- Ecruteak Lugia Speech Entrance
- Ecruteak Mart Entrance
- Ecruteak Pokecenter Entrance
- Route 38 Gate East Entrance
- Route 42 Gate West Entrance
- Tin Tower Entrance
- Tin Tower Gate Entrance
- Wise Trio's Room Entrance

### Tin Tower Roof

- Tin Tower Roof Stairs

### Route 38

- Route 38 Gate West Entrance

### Route 39

- Moomoo Farm Barn Entrance
- Moomoo Farm Entrance

### Olivine City

- Olivine Cafe Entrance
- Olivine Fishing Guru's House Entrance
- Olivine Gym Entrance
- Olivine Lighthouse Entrance
- Olivine Mart Entrance
- Olivine Pokecenter Entrance
- Olivine Port Passage Entrance
- Olivine Punishment Speech House Entrance
- Olivine Tim's House Entrance

### Olivine Port

- Olivine Port Stairs

### Route 40

- Route 40 Gate South Entrance

### Battle Tower Outside

- Battle Tower Entrance
- Route 40 Gate North Entrance

### Route 41

- Whirl Islands Northeast Entrance
- Whirl Islands Northwest Entrance
- Whirl Islands Southeast Entrance
- Whirl Islands Southwest Entrance

### Cianwood City

- Cianwood Gym Entrance
- Cianwood Lugia Speech House Entrance
- Cianwood Pharmacy Entrance
- Cianwood Photo Studio Entrance
- Cianwood Poke Seer's House Entrance
- Cianwood Pokecenter Entrance
- Mania's House Entrance

### Route 42

- Mount Mortar Center Entrance
- Mount Mortar East Entrance
- Mount Mortar West Entrance
- Route 42 Gate East Entrance

### Mahogany Town

- Mahogany Gym Entrance
- Mahogany Mart Entrance
- Mahogany Pokecenter Entrance
- Mahogany Red Gyarados Speech House Entrance
- Route 43 Gate South Entrance

### Route 43

- Route 43 Checkpoint North Entrance
- Route 43 Checkpoint South Entrance
- Route 43 Gate North Entrance

### Lake of Rage

- Lake of Rage Hidden Power House Entrance
- Lake of Rage Magikarp House Entrance

### Route 44

- Ice Path West Entrance

### Blackthorn City

- Blackthorn Dragon Speech House Entrance
- Blackthorn Emy's House Entrance
- Blackthorn Gym Entrance
- Blackthorn Mart Entrance
- Blackthorn Move Deleter's House Entrance
- Blackthorn Pokecenter Entrance
- Dragon's Den Entrance
- Ice Path East Entrance

### Route 45

- Dark Cave Northeast Entrance

### Route 46

- Dark Cave Southeast Entrance
- Route 29-46 Gate North Entrance

### Route 27

- Route 27 Sandstorm House Entrance
- Tohjo Falls East Entrance
- Tohjo Falls West Entrance

### Route 26

- Route 26 Day of Week Siblings' House Entrance
- Route 26 Heal House Entrance
- Victory Road Gate South Entrance

### Route 28

- Route 28 House Entrance
- Victory Road Gate West Entrance

### Silver Cave Outside

- Silver Cave Entrance
- Silver Cave Pokecenter Entrance

### Pallet Town

- Blue's House Entrance
- Oak's Lab Entrance
- Red's House Entrance

### Viridian City

- Viridian Gym Entrance
- Viridian Mart Entrance
- Viridian Nickname Speech House Entrance
- Viridian Pokecenter Entrance
- Viridian Trainer House Entrance

### Route 2

- Diglett's Cave North Entrance
- Route 2 Gate North Entrance
- Route 2 Gate South Entrance
- Route 2 Nugget House Entrance

### Pewter City

- Pewter Gym Entrance
- Pewter Mart Entrance
- Pewter Nidoran Speech House Entrance
- Pewter Pokecenter Entrance
- Pewter Snooze Speech House Entrance

### Route 3

- Mount Moon West Entrance

### Mount Moon Square

- Mount Moon Gift Shop Entrance
- Mount Moon Square North Exit
- Mount Moon Square South Exit

### Route 4

- Mount Moon East Entrance

### Cerulean City

- Cerulean Gym Badge Speech House Entrance
- Cerulean Gym Entrance
- Cerulean Mart Entrance
- Cerulean Pokecenter Entrance
- Cerulean Police Station Entrance
- Cerulean Trade Speech House Entrance

### Route 25

- Bill's House Entrance

### Route 5

- Route 5 Cleanse Tag House Entrance
- Route 5 Gate North Entrance
- Underground Path North Entrance

### Route 6

- Route 6 Gate South Entrance
- Underground Path South Entrance

### Vermilion City

- Diglett's Cave South Entrance
- Vermilion Diglett's Cave Speech House Entrance
- Vermilion Fishing Speech House Entrance
- Vermilion Gym Entrance
- Vermilion Magnet Train Speech House Entrance
- Vermilion Mart Entrance
- Vermilion Pokecenter Entrance
- Vermilion Pokemon Fan Club Entrance
- Vermilion Port Passage Entrance

### Vermilion Port

- Vermilion Port Stairs

### Route 9

- Rock Tunnel North Entrance

### Route 10 North

- Power Plant Entrance
- Route 10 Pokecenter Entrance

### Route 10 South

- Rock Tunnel South Entrance

### Lavender Town

- Lavender Mart Entrance
- Lavender Name Rater Entrance
- Lavender Pokecenter Entrance
- Lavender Radio Tower Entrance
- Lavender Soul House Entrance
- Lavender Speech House Entrance
- Mr. Fuji's House Entrance

### Route 8

- Route 8 Gate East Entrance
- Underground Path East Entrance

### Route 7

- Route 7 Gate West Entrance
- Underground Path West Entrance

### Celadon City

- Celadon Cafe Entrance
- Celadon Dept. Store Entrance
- Celadon Game Corner Entrance
- Celadon Game Corner Prize Room Entrance
- Celadon Gym Entrance
- Celadon Mansion Back Entrance
- Celadon Mansion Main Entrance
- Celadon Pokecenter Entrance

### Saffron City

- Mr. Psychic's House Entrance
- Route 5 Gate South Entrance
- Route 6 Gate North Entrance
- Route 7 Gate East Entrance
- Route 8 Gate West Entrance
- Saffron Copycat's House Entrance
- Saffron Fighting Dojo Entrance
- Saffron Gym Entrance
- Saffron Magnet Train Station Entrance
- Saffron Mart Entrance
- Saffron Pokecenter Entrance
- Silph Co. Entrance

### Route 12

- Route 12 Fishing Guru's House Entrance

### Route 15

- Route 15 Gate East Entrance

### Fuchsia City

- Bill's Brother's House Entrance
- Fuchsia Gym Entrance
- Fuchsia Mart Entrance
- Fuchsia Pokecenter Entrance
- Route 15 Gate West Entrance
- Route 19 Gate North Entrance
- Safari Zone Main Office Entrance
- Safari Zone Warden's House Entrance

### Route 18

- Route 17-18 Gate East Entrance

### Route 17

- Route 17-18 Gate West Entrance

### Route 16

- Route 16 Gate East Entrance
- Route 16 Gate West Entrance
- Route 16 House Entrance

### Route 19

- Route 19 Gate South Entrance

### Route 20

- Seafoam Gym Entrance

### Cinnabar Island

- Cinnabar Pokecenter Entrance

### Route 22

- Victory Road Gate East Entrance

### Route 23 Restored

> [!NOTE]
> These warps are only available when the Route 23 Restored YAML option is enabled

- Victory Road Gate North Entrance
- Victory Road South Entrance (Restored)

### Route 23

- Indigo Plateau Entrance
- Victory Road North Entrance
