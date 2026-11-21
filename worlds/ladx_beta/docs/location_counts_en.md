# Links Awakening DX Beta Location Counts Guide

At default options, the game has **222 locations**.

The minimum location count is **26** with:
```
overworld: dungeon_dive
condense_dungeons:
    - Color Dungeon
    - Tail Cave
    - Bottle Grotto
    - Key Cavern
    - Angler's Tunnel
    - Catfish's Maw
    - Face Shrine
    - Eagle's Tower
    - Turtle Rock
```

The maximum location count is **255** with:
```
owlsanity: both
```

## Overworld

Standard overworld has **90 locations**.

Overworld location changes by option:

`goal: seashells` | `tradequest: false` | `owlsanity: overworld`
--------------|---------------------|----------
-2            |-14                  |+10

Dungeon dive overworld has **7 locations**, and none of the above settings can modify it.

## Dungeons

Dungeon        | Default | `owlsanity: dungeon` | `condense_dungeons`
---------------|--------------------|-----------|----------
Color Dungeon  |9                   |12 (+3)    |2 (-7)
Tail Cave      |12                  |15 (+3)    |2 (-10)
Bottle Grotto  |14                  |17 (+3)    |3 (-11)
Key Cavern     |19                  |22 (+3)    |2 (-16)
Angler's Tunnel|15                  |16 (+1)    |2 (-13)
Catfish's Maw  |14                  |16 (+2)    |2 (-12)
Face Shrine    |16                  |18 (+2)    |2 (-14)
Eagle's Tower  |13                  |16 (+3)    |2 (-11)
Turtle Rock    |20                  |23 (+3)    |2 (-18)
**Total**      |**132**             |**155** (+23)|**19** (-113)