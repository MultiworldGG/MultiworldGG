# Links Awakening DX Beta Plando Guide

- [Entrance Plando](/tutorial/Links%20Awakening%20DX%20Beta/plando_en#entrance-plando)
- [Boss Plando](/tutorial/Links%20Awakening%20DX%20Beta/plando_en#boss-plando)
- [Miniboss Plando](/tutorial/Links%20Awakening%20DX%20Beta/plando_en#miniboss-plando)

## Entrance Plando

If you are using entrance rules with coupled entrances (normal or wild), the inverse of your plando connections will be automatically applied for you. For example, if you define:

```
"mabe_phone": "d1:inside"
```

You will also get:

```
"d1:inside": "mabe_phone"
```

You *can* define connections that would otherwise be impossible under your selected entrance rules and groups. It will take your defined connections without question and then try to make the rest work from there. Be careful though, if you leave things unbalanced, it will be impossible to generate a successful entrance mapping from your plando. For example, with options:

```
entrance_rules: normal
shuffle_junk: limited
shuffle_dungeons: limited
entrance_plando:
    "mabe_phone": "d1:inside"
```

While it will set up the inverse connection (`"d1:inside": "mabe_phone"`) for you, there is left one too many outside junk entrances, and one too many inside dungeon entrances. This can be fixed by creating a complementary connection:

```
entrance_rules: normal
shuffle_junk: limited
shuffle_dungeons: limited
entrance_plando:
    "mabe_phone": "d1:inside"
    "mabe_phone:inside": "d1"
```

### Vanilla Entrance Mapping
```
{
    "d8": "d8:inside",
    "phone_d8": "phone_d8:inside",
    "fire_cave_exit": "fire_cave_exit:inside",
    "fire_cave_entrance": "fire_cave_entrance:inside",
    "madbatter_taltal": "madbatter_taltal:inside",
    "left_taltal_entrance": "left_taltal_entrance:inside",
    "obstacle_cave_entrance": "obstacle_cave_entrance:inside",
    "left_to_right_taltalentrance": "left_to_right_taltalentrance:inside",
    "obstacle_cave_outside_chest": "obstacle_cave_outside_chest:inside",
    "obstacle_cave_exit": "obstacle_cave_exit:inside",
    "papahl_entrance": "papahl_entrance:inside",
    "papahl_exit": "papahl_exit:inside",
    "rooster_house": "rooster_house:inside",
    "bird_cave": "bird_cave:inside",
    "multichest_left": "multichest_left:inside",
    "multichest_right": "multichest_right:inside",
    "multichest_top": "multichest_top:inside",
    "right_taltal_connector1": "right_taltal_connector1:inside",
    "right_taltal_connector2": "right_taltal_connector2:inside",
    "right_taltal_connector3": "right_taltal_connector3:inside",
    "right_taltal_connector4": "right_taltal_connector4:inside",
    "right_taltal_connector5": "right_taltal_connector5:inside",
    "right_taltal_connector6": "right_taltal_connector6:inside",
    "right_fairy": "right_fairy:inside",
    "d7": "d7:inside",
    "writes_cave_left": "writes_cave_left:inside",
    "writes_cave_right": "writes_cave_right:inside",
    "writes_house": "writes_house:inside",
    "writes_phone": "writes_phone:inside",
    "d2": "d2:inside",
    "moblin_cave": "moblin_cave:inside",
    "photo_house": "photo_house:inside",
    "mambo": "mambo:inside",
    "d4": "d4:inside",
    "heartpiece_swim_cave": "heartpiece_swim_cave:inside",
    "raft_return_exit": "raft_return_exit:inside",
    "raft_house": "raft_house:inside",
    "raft_return_enter": "raft_return_enter:inside",
    "hookshot_cave": "hookshot_cave:inside",
    "toadstool_exit": "toadstool_exit:inside",
    "forest_madbatter": "forest_madbatter:inside",
    "toadstool_entrance": "toadstool_entrance:inside",
    "crazy_tracy": "crazy_tracy:inside",
    "witch": "witch:inside",
    "graveyard_cave_left": "graveyard_cave_left:inside",
    "graveyard_cave_right": "graveyard_cave_right:inside",
    "d0": "d0:inside",
    "castle_jump_cave": "castle_jump_cave:inside",
    "castle_main_entrance": "castle_main_entrance:inside",
    "castle_upper_left": "castle_upper_left:inside",
    "castle_upper_right": "castle_upper_right:inside",
    "castle_secret_exit": "castle_secret_exit:inside",
    "castle_secret_entrance": "castle_secret_entrance:inside",
    "castle_phone": "castle_phone:inside",
    "papahl_house_left": "papahl_house_left:inside",
    "papahl_house_right": "papahl_house_right:inside",
    "dream_hut": "dream_hut:inside",
    "rooster_grave": "rooster_grave:inside",
    "shop": "shop:inside",
    "madambowwow": "madambowwow:inside",
    "kennel": "kennel:inside",
    "start_house": "start_house:inside",
    "library": "library:inside",
    "ulrira": "ulrira:inside",
    "mabe_phone": "mabe_phone:inside",
    "trendy_shop": "trendy_shop:inside",
    "prairie_left_phone": "prairie_left_phone:inside",
    "prairie_left_cave1": "prairie_left_cave1:inside",
    "prairie_left_cave2": "prairie_left_cave2:inside",
    "prairie_left_fairy": "prairie_left_fairy:inside",
    "mamu": "mamu:inside",
    "d3": "d3:inside",
    "prairie_right_phone": "prairie_right_phone:inside",
    "seashell_mansion": "seashell_mansion:inside",
    "prairie_right_cave_top": "prairie_right_cave_top:inside",
    "prairie_right_cave_bottom": "prairie_right_cave_bottom:inside",
    "prairie_right_cave_high": "prairie_right_cave_high:inside",
    "prairie_to_animal_connector": "prairie_to_animal_connector:inside",
    "animal_to_prairie_connector": "animal_to_prairie_connector:inside",
    "d6": "d6:inside",
    "d6_connector_exit": "d6_connector_exit:inside",
    "d6_connector_entrance": "d6_connector_entrance:inside",
    "armos_fairy": "armos_fairy:inside",
    "armos_maze_cave": "armos_maze_cave:inside",
    "armos_temple": "armos_temple:inside",
    "d1": "d1:inside",
    "boomerang_cave": "boomerang_cave:inside",
    "banana_seller": "banana_seller:inside",
    "ghost_house": "ghost_house:inside",
    "richard_house": "richard_house:inside",
    "richard_maze": "richard_maze:inside",
    "prairie_low_phone": "prairie_low_phone:inside",
    "prairie_madbatter_connector_entrance": "prairie_madbatter_connector_entrance:inside",
    "prairie_madbatter_connector_exit": "prairie_madbatter_connector_exit:inside",
    "prairie_madbatter": "prairie_madbatter:inside",
    "d5": "d5:inside",
    "animal_phone": "animal_phone:inside",
    "animal_house1": "animal_house1:inside",
    "animal_house2": "animal_house2:inside",
    "animal_house3": "animal_house3:inside",
    "animal_house4": "animal_house4:inside",
    "animal_house5": "animal_house5:inside",
    "animal_cave": "animal_cave:inside",
    "desert_cave": "desert_cave:inside",
    "d8:inside": "d8",
    "phone_d8:inside": "phone_d8",
    "fire_cave_exit:inside": "fire_cave_exit",
    "fire_cave_entrance:inside": "fire_cave_entrance",
    "madbatter_taltal:inside": "madbatter_taltal",
    "left_taltal_entrance:inside": "left_taltal_entrance",
    "obstacle_cave_entrance:inside": "obstacle_cave_entrance",
    "left_to_right_taltalentrance:inside": "left_to_right_taltalentrance",
    "obstacle_cave_outside_chest:inside": "obstacle_cave_outside_chest",
    "obstacle_cave_exit:inside": "obstacle_cave_exit",
    "papahl_entrance:inside": "papahl_entrance",
    "papahl_exit:inside": "papahl_exit",
    "rooster_house:inside": "rooster_house",
    "bird_cave:inside": "bird_cave",
    "multichest_left:inside": "multichest_left",
    "multichest_right:inside": "multichest_right",
    "multichest_top:inside": "multichest_top",
    "right_taltal_connector1:inside": "right_taltal_connector1",
    "right_taltal_connector2:inside": "right_taltal_connector2",
    "right_taltal_connector3:inside": "right_taltal_connector3",
    "right_taltal_connector4:inside": "right_taltal_connector4",
    "right_taltal_connector5:inside": "right_taltal_connector5",
    "right_taltal_connector6:inside": "right_taltal_connector6",
    "right_fairy:inside": "right_fairy",
    "d7:inside": "d7",
    "writes_cave_left:inside": "writes_cave_left",
    "writes_cave_right:inside": "writes_cave_right",
    "writes_house:inside": "writes_house",
    "writes_phone:inside": "writes_phone",
    "d2:inside": "d2",
    "moblin_cave:inside": "moblin_cave",
    "photo_house:inside": "photo_house",
    "mambo:inside": "mambo",
    "d4:inside": "d4",
    "heartpiece_swim_cave:inside": "heartpiece_swim_cave",
    "raft_return_exit:inside": "raft_return_exit",
    "raft_house:inside": "raft_house",
    "raft_return_enter:inside": "raft_return_enter",
    "hookshot_cave:inside": "hookshot_cave",
    "toadstool_exit:inside": "toadstool_exit",
    "forest_madbatter:inside": "forest_madbatter",
    "toadstool_entrance:inside": "toadstool_entrance",
    "crazy_tracy:inside": "crazy_tracy",
    "witch:inside": "witch",
    "graveyard_cave_left:inside": "graveyard_cave_left",
    "graveyard_cave_right:inside": "graveyard_cave_right",
    "d0:inside": "d0",
    "castle_jump_cave:inside": "castle_jump_cave",
    "castle_main_entrance:inside": "castle_main_entrance",
    "castle_upper_left:inside": "castle_upper_left",
    "castle_upper_right:inside": "castle_upper_right",
    "castle_secret_exit:inside": "castle_secret_exit",
    "castle_secret_entrance:inside": "castle_secret_entrance",
    "castle_phone:inside": "castle_phone",
    "papahl_house_left:inside": "papahl_house_left",
    "papahl_house_right:inside": "papahl_house_right",
    "dream_hut:inside": "dream_hut",
    "rooster_grave:inside": "rooster_grave",
    "shop:inside": "shop",
    "madambowwow:inside": "madambowwow",
    "kennel:inside": "kennel",
    "start_house:inside": "start_house",
    "library:inside": "library",
    "ulrira:inside": "ulrira",
    "mabe_phone:inside": "mabe_phone",
    "trendy_shop:inside": "trendy_shop",
    "prairie_left_phone:inside": "prairie_left_phone",
    "prairie_left_cave1:inside": "prairie_left_cave1",
    "prairie_left_cave2:inside": "prairie_left_cave2",
    "prairie_left_fairy:inside": "prairie_left_fairy",
    "mamu:inside": "mamu",
    "d3:inside": "d3",
    "prairie_right_phone:inside": "prairie_right_phone",
    "seashell_mansion:inside": "seashell_mansion",
    "prairie_right_cave_top:inside": "prairie_right_cave_top",
    "prairie_right_cave_bottom:inside": "prairie_right_cave_bottom",
    "prairie_right_cave_high:inside": "prairie_right_cave_high",
    "prairie_to_animal_connector:inside": "prairie_to_animal_connector",
    "animal_to_prairie_connector:inside": "animal_to_prairie_connector",
    "d6:inside": "d6",
    "d6_connector_exit:inside": "d6_connector_exit",
    "d6_connector_entrance:inside": "d6_connector_entrance",
    "armos_fairy:inside": "armos_fairy",
    "armos_maze_cave:inside": "armos_maze_cave",
    "armos_temple:inside": "armos_temple",
    "d1:inside": "d1",
    "boomerang_cave:inside": "boomerang_cave",
    "banana_seller:inside": "banana_seller",
    "ghost_house:inside": "ghost_house",
    "richard_house:inside": "richard_house",
    "richard_maze:inside": "richard_maze",
    "prairie_low_phone:inside": "prairie_low_phone",
    "prairie_madbatter_connector_entrance:inside": "prairie_madbatter_connector_entrance",
    "prairie_madbatter_connector_exit:inside": "prairie_madbatter_connector_exit",
    "prairie_madbatter:inside": "prairie_madbatter",
    "d5:inside": "d5",
    "animal_phone:inside": "animal_phone",
    "animal_house1:inside": "animal_house1",
    "animal_house2:inside": "animal_house2",
    "animal_house3:inside": "animal_house3",
    "animal_house4:inside": "animal_house4",
    "animal_house5:inside": "animal_house5",
    "animal_cave:inside": "animal_cave",
    "desert_cave:inside": "desert_cave"
}
```

## Boss Plando

Color Dungeon and its boss cannot be mapped at this time. Also, while duplicate bosses are generally ok, there can only be one `ANGLER_FISH` and `EVIL_EAGLE` per world.

### Vanilla Boss Mapping

```
{
    "d1": "MOLDORM",
    "d2": "GENIE",
    "d3": "SLIME_EYE",
    "d4": "ANGLER_FISH",
    "d5": "SLIME_EEL",
    "d6": "FACADE",
    "d7": "EVIL_EAGLE",
    "d8": "HOT_HEAD"
}
```

## Miniboss Plando

### Vanilla Miniboss Mapping

```
{
    "0": "ROLLING_BONES",
    "1": "HINOX",
    "2": "DODONGO",
    "3": "CUE_BALL",
    "4": "GHOMA",
    "5": "SMASHER",
    "6": "GRIM_CREEPER",
    "7": "BLAINO",
    "c1": "AVALAUNCH",
    "c2": "GIANT_BUZZ_BLOB",
    "moblin_cave": "MOBLIN_KING",
    "armos_temple": "ARMOS_KNIGHT"
}
```