from .Rules import big_uppies, small_uppies

def create_soul_regions(world):
    player = world.player
    multiworld = world.multiworld
    multiworld.get_region("Lost Village Upper", player).add_exits(["Yeti Soul", "Axe Armor Soul", "Warg Soul", "Skeleton Soul", "Bat Soul", "Armor Knight Soul", "Zombie Soul",
                                                                   "Peeping Eye Soul"],
    {"Yeti Soul": lambda state: state.has("Waiter Skeleton Soul", player),
     "Armor Knight Soul": lambda state: state.has_any(big_uppies, player)})

    multiworld.get_region("Lost Village Upper Doorway", player).add_exits(["Skelerang Soul", "Peeping Eye Soul"])

    multiworld.get_region("Lost Village Lower", player).add_exits(["Spin Devil Soul", "Skeleton Soul", "Armor Knight Soul", "Bat Soul", "Zombie Soul", "Student Witch Soul",
                                                                   "Ouija Table Soul"],
    {"Student Witch Soul": lambda state: state.has("Moat Drained", player)})

    multiworld.get_region("Lost Village Courtyard", player).add_exits(["Warg Soul", "Hell Boar Soul", "Skeleton Ape Soul"],
    {"Hell Boar Soul": lambda state: state.has_any(big_uppies, player)})

    multiworld.get_region("Lost Village Underground Top", player).add_exits(["Axe Armor Soul", "Merman Soul", "Great Axe Armor Soul"])
    multiworld.get_region("Lost Village Underground Bottom", player).add_exits(["White Dragon Soul"])

    ####### WIZARDRY LAB SOULS ########
    multiworld.get_region("Wizardry Lab Main", player).add_exits(["Slime Soul", "Axe Armor Soul", "Bomber Armor Soul", "Student Witch Soul", "Skull Archer Soul", "Skeleton Soul",
                                                                  "Slaughterer Soul", "Manticore Soul", "Armor Knight Soul", "Golem Soul", "Ghost Soul", "The Creature Soul"])
    multiworld.get_region("Wizardry Lab West Gate", player).add_exits(["Great Axe Armor Soul", "Heart Eater Soul"])
    multiworld.get_region("Wizardry Lab East Gate", player).add_exits(["Cave Troll Soul", "Mimic Soul"])
    multiworld.get_region("Wizardry Lab Sunken", player).add_exits(["Homunculus Soul", "Killer Fish Soul", "Larva Soul", "Mimic Soul"])  # Should this mimic be here? ghosts aren't? Hmmm
    multiworld.get_region("Wizardry Lab Sunken West Door", player).add_exits(["Iron Golem Soul", "Ghost Soul"])

    ####### GARDEN OF MADNESS ######

    multiworld.get_region("Garden of Madness Lower", player).add_exits(["Corpseweed Soul", "Une Soul", "Skelerang Soul", "Mandragora Soul", "Catoblepas Soul", "Mollusca Soul",
                                                                        "Yorick Soul", "Rycuda Soul", "Treant Soul", "Skeleton Ape Soul", "Skeleton Farmer Soul", "Mimic Soul"],
                          {"Mimic Soul": lambda state: state.has_any(small_uppies, player)})
    multiworld.get_region("Garden of Madness Upper", player).add_exits(["Corpseweed Soul", "Rycuda Soul", "Mollusca Soul", "Barbariccia Soul", "Skeleton Ape Soul", "Treant Soul",])
    multiworld.get_region("Garden of Madness Post-Boss", player).add_exits(["Corpseweed Soul", "Skelerang Soul", "Une Soul", "Skeleton Ape Soul", "Ghoul Soul"])
    multiworld.get_region("Garden of Madness East Gate", player).add_exits(["Wakwak Tree Soul"])
    ##### DEMON GUEST HOUSE ####

    multiworld.get_region("Demon Guest House Lower", player).add_exits(["Axe Armor Soul", "Skeleton Soul", "Peeping Eye Soul"])
    multiworld.get_region("Demon Guest House Puppet Wall Right", player).add_exits(["Skelerang Soul"])
    multiworld.get_region("Demon Guest House Main", player).add_exits(["Persephone Soul", "Skelerang Soul", "Devil Soul", "Lilith Soul", "Ghost Dancer Soul", "Killer Clown Soul",
                                                                       "Waiter Skeleton Soul", "Valkyrie Soul", "Killer Doll Soul", "Bone Pillar Soul"])
    multiworld.get_region("Demon Guest House Number Puzzle West", player).add_exits(["Persephone Soul"])

    multiworld.get_region("Demon Guest House West Wing", player).add_exits(["Buer Soul", "Killer Clown Soul", "Lilith Soul", "Quetzalcoatl Soul", "Killer Doll Soul", "Bone Pillar Soul"])
    multiworld.get_region("Demon Guest House Upper", player).add_exits(["Flame Demon Soul", "Malachi Soul", "Skelerang Soul", "Werewolf Soul", "Ghost Dancer Soul",
                                                                        "Student Witch Soul", "Lilith Soul", "Witch Soul", "Succubus Soul", "Persephone Soul",
                                                                        "Iron Golem Soul", "Mimic Soul"])
    ##### DARK CHAPEL #####

    multiworld.get_region("Dark Chapel", player).add_exits(["Guillotiner Soul", "Witch Soul", "Mini Devil Soul", "Amalaric Sniper Soul", "Ghost Dancer Soul", "Hell Boar Soul",
                                                            "White Dragon Soul", "Great Armor Soul", "Quetzalcoatl Soul", "Ghoul Soul", "The Creature Soul", "Bone Pillar Soul",
                                                            "Barbariccia Soul", "Valkyrie Soul", "Ghost Soul", "Tombstone Soul"], # Is ghost here? double check this
                        {"Quetzalcoatl Soul": lambda state: state.has(world.magic_seal_table["Dark Chapel"], player)})

    multiworld.get_region("Dark Chapel Big Room", player).add_exits(["Mini Devil Soul", "Quetzalcoatl Soul", "Valkyrie Soul"])
    multiworld.get_region("Dark Chapel Catacombs Exit", player).add_exits(["Catoblepas Soul"])
    #####CONDEMNED TOWER #####
    multiworld.get_region("Condemned Tower Bottom", player).add_exits(["Draghignazzo Soul", "Skeleton Ape Soul", "Great Axe Armor Soul"])
    multiworld.get_region("Condemned Tower Main", player).add_exits(["Buer Soul", "Disc Armor Soul", "Werewolf Soul", "Fleaman Soul"])

    ##### CURSED CLOCK TOWER ######
    multiworld.get_region("Cursed Clock Tower Entrance", player).add_exits(["Harpy Soul", "Catoblepas Soul", "Imp Soul", "Malachi Soul", "Dead Pirate Soul",
                                                                            "Medusa Head Soul", "Tanjelly Soul"])
    multiworld.get_region("Cursed Clock Tower Central", player).add_exits(["Slime Soul", "Imp Soul", "Medusa Head Soul", "Bugbear Soul", "Tanjelly Soul"])
    multiworld.get_region("Cursed Clock Tower Boss Area", player).add_exits(["Flying Humanoid Soul"],
    {"Flying Humanoid Soul": lambda state: state.has("Mandragora Soul", player)})
    multiworld.get_region("Cursed Clock Tower Exit", player).add_exits(["Devil Soul", "Harpy Soul"])
    ##### SUBTERRANEAN HELL #####

    multiworld.get_region("Subterranean Hell Top Entrance", player).add_exits(["Cave Troll Soul", "Decarabia Soul", "Une Soul", "Dead Pirate Soul"],
    {"Decarabia Soul": lambda state: state.has(world.magic_seal_table["Subterranean Hell"], player)})

    multiworld.get_region("Subterranean Hell East", player).add_exits(["Decarabia Soul", "Merman Soul", "Fish Head Soul", "Needles Soul", "Frozen Shade Soul", "Killer Fish Soul",
                                                                       "Mimic Soul", "Procel Soul"],
    {"Decarabia Soul": lambda state: state.has("Rahab Soul", player),
     "Fish Head Soul": lambda state: state.has("Rahab Soul", player),
     "Needles Soul": lambda state: state.has("Rahab Soul", player),
     "Mimic Soul": lambda state: state.has("Rahab Soul", player)})

    multiworld.get_region("Subterranean Hell Central/East Connection", player).add_exits(["Une Soul", "Alura Une Soul"])

    multiworld.get_region("Subterranean Hell Shaft Bottom", player).add_exits(["Merman Soul", "Dead Pirate Soul", "Ukoback Soul", "Medusa Head Soul"])
    multiworld.get_region("Subterranean Hell Shaft Middle", player).add_exits(["Frozen Shade Soul", "Devil Soul"])
    multiworld.get_region("Subterranean Hell Shaft Top", player).add_exits(["Killer Fish Soul", "Ukoback Soul"])
    multiworld.get_region("Subterranean Hell Central Lower", player).add_exits(["Merman Soul", "Frozen Shade Soul", "Dead Pirate Soul", "Procel Soul"])
    multiworld.get_region("Subterranean Hell Central Upper", player).add_exits(["Merman Soul", "Ukoback Soul", "Frozen Shade Soul", "Dead Pirate Soul", "Killer Fish Soul", "Needles Soul", "Bone Ark Soul"],
                            {"Needles Soul": lambda state: state.has("Rahab Soul", player),
                            "Killer Fish Soul": lambda state: state.has("Rahab Soul", player)})
    multiworld.get_region("Subterranean Hell Central Exit", player).add_exits(["Merman Soul", "Ukoback Soul", "Frozen Shade Soul", "Mimic Soul"])

    ####S ILENCED RUINS #####
    multiworld.get_region("Silenced Ruins", player).add_exits(["Dead Mate Soul", "Skeleton Soul", "Bat Soul", "Skull Archer Soul", "Devil Soul", "Larva Soul", "Skelerang Soul",
                                                               "Ghoul Soul", "Dead Crusader Soul", "Bone Ark Soul"],
    {"Devil Soul": lambda state: state.has("Balore Soul", player)})
    multiworld.get_region("Silenced Ruins Back Exit", player).add_exits(["Waiter Skeleton Soul"])
    multiworld.get_region("Silenced Ruins Upper Entrance", player).add_exits(["Waiter Skeleton Soul", "Peeping Eye Soul", "Gorgon Soul"])

    ##### PINNACLE #####
    multiworld.get_region("The Pinnacle", player).add_exits(["Guillotiner Soul", "Mothman Soul", "Werewolf Soul", "Mushussu Soul", "Alastor Soul",
                                                             "Dead Crusader Soul", "Erinys Soul", "Final Guard Soul"],
    {"Mothman Soul": lambda state: state.has("Rycuda Soul", player)})
    multiworld.get_region("The Pinnacle Lower", player).add_exits(["Guillotiner Soul", "Succubus Soul", "Malachi Soul", "Mushussu Soul", "Werewolf Soul", "Flame Demon Soul",
                                                                   "Bugbear Soul", "Dead Warrior Soul", "Erinys Soul"])

    if world.mine_status != "Disabled":
        multiworld.get_region("Mine of Judgment", player).add_exits(["Slogra Soul", "Ripper Soul", "Gaibon Soul", "Tanjelly Soul", "Giant Slug Soul", "Bugbear Soul"])
        multiworld.get_region("The Abyss", player).add_exits(["Alastor Soul", "Mud Demon Soul", "Frozen Shade Soul", "Malachi Soul", "White Dragon Soul", "Malacoda Soul",
                                                              "Arc Demon Soul", "Erinys Soul", "Heart Eater Soul", "Stolas Soul", "Final Guard Soul"])
        multiworld.get_region("The Abyss Beyond Abaddon", player).add_exits(["Black Panther Soul", "Succubus Soul", "Iron Golem Soul"])
        