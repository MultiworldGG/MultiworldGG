from .Rules import big_uppies, small_uppies
from .Options import SoulRandomizer
from rule_builder.rules import Has


def create_soul_regions(world):
    world.get_region("Lost Village Upper").add_exits(["Axe Armor Soul", "Warg Soul",  "Skeleton Soul", "Bat Soul",
                                                      "Armor Knight Soul", "Zombie Soul", "Peeping Eye Soul"],
                                                     {"Armor Knight Soul": small_uppies})

    world.get_region("Lost Village Upper Doorway").add_exits(["Skelerang Soul", "Peeping Eye Soul"])

    world.get_region("Lost Village Lower").add_exits(["Spin Devil Soul", "Skeleton Soul", "Armor Knight Soul", "Bat Soul", "Zombie Soul", "Student Witch Soul",
                                                      "Ouija Table Soul"],
                                                     {"Student Witch Soul": Has("Moat Drained")})

    world.get_region("Lost Village Courtyard").add_exits(["Warg Soul", "Hell Boar Soul", "Skeleton Ape Soul"],
                                                         {"Hell Boar Soul": big_uppies})

    world.get_region("Lost Village Underground Top").add_exits(["Axe Armor Soul", "Merman Soul", "Great Axe Armor Soul"])
    world.get_region("Lost Village Underground Bottom").add_exits(["White Dragon Soul"])

    # WIZARDRY LAB SOULS ########
    world.get_region("Wizardry Lab Main").add_exits(["Slime Soul", "Axe Armor Soul", "Bomber Armor Soul",
                                                     "Student Witch Soul", "Skull Archer Soul", "Skeleton Soul",
                                                     "Slaughterer Soul", "Manticore Soul", "Armor Knight Soul",
                                                     "Golem Soul", "Ghost Soul", "The Creature Soul"])

    world.get_region("Wizardry Lab West Gate").add_exits(["Great Axe Armor Soul", "Heart Eater Soul"])
    world.get_region("Wizardry Lab East Gate").add_exits(["Cave Troll Soul", "Mimic Soul"])
    world.get_region("Wizardry Lab Sunken").add_exits(["Homunculus Soul", "Killer Fish Soul", "Larva Soul", "Mimic Soul"])  # Should this mimic be here? ghosts aren't? Hmmm
    world.get_region("Wizardry Lab Sunken West Door").add_exits(["Iron Golem Soul", "Ghost Soul"])

    # GARDEN OF MADNESS ######

    world.get_region("Garden of Madness Lower").add_exits(["Corpseweed Soul", "Une Soul", "Skelerang Soul", "Mandragora Soul", "Catoblepas Soul", "Mollusca Soul",
                                                           "Yorick Soul", "Rycuda Soul", "Treant Soul", "Skeleton Ape Soul", "Skeleton Farmer Soul", "Mimic Soul"],
                                                          {"Mimic Soul": small_uppies})
    world.get_region("Garden of Madness Upper").add_exits(["Corpseweed Soul", "Rycuda Soul", "Mollusca Soul", "Barbariccia Soul", "Skeleton Ape Soul", "Treant Soul",])
    world.get_region("Garden of Madness Post-Boss").add_exits(["Corpseweed Soul", "Skelerang Soul", "Une Soul", "Skeleton Ape Soul", "Ghoul Soul"])
    world.get_region("Garden of Madness East Gate").add_exits(["Wakwak Tree Soul"])
    # DEMON GUEST HOUSE ####

    world.get_region("Demon Guest House Lower").add_exits(["Axe Armor Soul", "Skeleton Soul", "Peeping Eye Soul"])
    world.get_region("Demon Guest House Puppet Wall Right").add_exits(["Skelerang Soul"])
    world.get_region("Demon Guest House Main").add_exits(["Persephone Soul", "Skelerang Soul", "Devil Soul", "Lilith Soul", "Ghost Dancer Soul", "Killer Clown Soul",
                                                          "Waiter Skeleton Soul", "Valkyrie Soul", "Killer Doll Soul", "Bone Pillar Soul"])
    world.get_region("Demon Guest House Number Puzzle West").add_exits(["Persephone Soul"])

    world.get_region("Demon Guest House West Wing").add_exits(["Buer Soul", "Killer Clown Soul", "Lilith Soul", "Quetzalcoatl Soul", "Killer Doll Soul", "Bone Pillar Soul"])
    world.get_region("Demon Guest House Upper").add_exits(["Flame Demon Soul", "Malachi Soul", "Skelerang Soul", "Werewolf Soul", "Ghost Dancer Soul",
                                                           "Student Witch Soul", "Lilith Soul", "Witch Soul", "Succubus Soul", "Persephone Soul",
                                                           "Iron Golem Soul", "Mimic Soul"])
    # #### DARK CHAPEL #####

    world.get_region("Dark Chapel").add_exits(["Guillotiner Soul", "Witch Soul", "Mini Devil Soul", "Amalaric Sniper Soul", "Ghost Dancer Soul", "Hell Boar Soul",
                                               "White Dragon Soul", "Great Armor Soul", "Ghoul Soul", "The Creature Soul", "Bone Pillar Soul",
                                               "Barbariccia Soul", "Valkyrie Soul", "Ghost Soul", "Tombstone Soul"])

    if not world.options.boss_shuffle or world.boss_slots["Dark Chapel"] != "Rahab":
        world.get_region("Dark Chapel").connect(world.get_region("Quetzalcoatl Soul"),
                                                rule=Has(world.magic_seal_table["Dark Chapel"]))

    world.get_region("Dark Chapel Big Room").add_exits(["Mini Devil Soul", "Quetzalcoatl Soul", "Valkyrie Soul"])
    world.get_region("Dark Chapel Post-Button").add_exits(["Tombstone Soul"])
    world.get_region("Dark Chapel Catacombs Exit").add_exits(["Catoblepas Soul"])
    # CONDEMNED TOWER #####
    world.get_region("Condemned Tower Bottom").add_exits(["Draghignazzo Soul", "Skeleton Ape Soul", "Great Axe Armor Soul"])
    world.get_region("Condemned Tower Main").add_exits(["Buer Soul", "Disc Armor Soul", "Werewolf Soul", "Fleaman Soul"])

    # CURSED CLOCK TOWER ######
    world.get_region("Cursed Clock Tower Entrance").add_exits(["Harpy Soul", "Catoblepas Soul", "Imp Soul", "Malachi Soul", "Dead Pirate Soul",
                                                               "Medusa Head Soul", "Tanjelly Soul"])
    world.get_region("Cursed Clock Tower Central").add_exits(["Slime Soul", "Imp Soul", "Medusa Head Soul", "Bugbear Soul", "Tanjelly Soul"])
    world.get_region("Cursed Clock Tower Exit").add_exits(["Devil Soul", "Harpy Soul"])
    # SUBTERRANEAN HELL #####

    world.get_region("Subterranean Hell Top Entrance").add_exits(["Cave Troll Soul", "Decarabia Soul", "Une Soul", "Dead Pirate Soul"],
                                                                 {"Decarabia Soul": Has(world.magic_seal_table["Subterranean Hell"])})

    world.get_region("Subterranean Hell East").add_exits(["Decarabia Soul", "Merman Soul", "Fish Head Soul", "Needles Soul", "Frozen Shade Soul", "Killer Fish Soul",
                                                          "Mimic Soul", "Procel Soul"],
                                                         {"Decarabia Soul": Has("Rahab Soul"),
                                                          "Fish Head Soul": Has("Rahab Soul"),
                                                          "Needles Soul": Has("Rahab Soul"),
                                                          "Mimic Soul": Has("Rahab Soul")})

    world.get_region("Subterranean Hell Central/East Connection").add_exits(["Une Soul", "Alura Une Soul"])

    world.get_region("Subterranean Hell Shaft Bottom").add_exits(["Merman Soul", "Dead Pirate Soul", "Ukoback Soul", "Medusa Head Soul"])
    world.get_region("Subterranean Hell Shaft Middle").add_exits(["Frozen Shade Soul", "Devil Soul"])
    world.get_region("Subterranean Hell Shaft Top").add_exits(["Killer Fish Soul", "Ukoback Soul"])
    world.get_region("Subterranean Hell Central Lower").add_exits(["Merman Soul", "Frozen Shade Soul", "Dead Pirate Soul", "Procel Soul"])
    world.get_region("Subterranean Hell Central Upper").add_exits(["Merman Soul", "Ukoback Soul", "Frozen Shade Soul", "Dead Pirate Soul", "Killer Fish Soul", "Needles Soul", "Bone Ark Soul"],
                                                                  {"Needles Soul": Has("Rahab Soul"),
                                                                   "Killer Fish Soul": Has("Rahab Soul")})
    world.get_region("Subterranean Hell Central Exit").add_exits(["Merman Soul", "Ukoback Soul", "Frozen Shade Soul", "Mimic Soul"])

    # ###S ILENCED RUINS #####
    world.get_region("Silenced Ruins").add_exits(["Dead Mate Soul", "Skeleton Soul", "Bat Soul", "Skull Archer Soul", "Devil Soul", "Larva Soul", "Skelerang Soul",
                                                  "Ghoul Soul", "Dead Crusader Soul", "Bone Ark Soul"],
                                                 {"Devil Soul": Has("Balore Soul")})
    world.get_region("Silenced Ruins Back Exit").add_exits(["Waiter Skeleton Soul"])
    world.get_region("Silenced Ruins Upper Entrance").add_exits(["Waiter Skeleton Soul", "Peeping Eye Soul", "Gorgon Soul"])

    # PINNACLE #####
    world.get_region("The Pinnacle").add_exits(["Guillotiner Soul", "Werewolf Soul", "Mushussu Soul", "Alastor Soul",
                                                "Dead Crusader Soul", "Erinys Soul", "Final Guard Soul"])
    world.get_region("The Pinnacle Lower").add_exits(["Guillotiner Soul", "Succubus Soul", "Malachi Soul", "Mushussu Soul", "Werewolf Soul", "Flame Demon Soul",
                                                      "Bugbear Soul", "Dead Warrior Soul", "Erinys Soul"])

    world.get_region("The Pinnacle Left Exit").add_exits(["Succubus Soul", "Erinys Soul"])

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.get_region("The Pinnacle").connect(world.get_region("Mothman Soul"), rule=Has("Rycuda Soul"))
        world.get_region("Lost Village Upper").connect(world.get_region("Yeti Soul"), rule=Has("Waiter Skeleton Soul"))
        world.get_region("Cursed Clock Tower Boss Area").connect(world.get_region("Flying Humanoid Soul"), rule=Has("Mandragora Soul"))

    if world.mine_status != "Disabled":
        world.get_region("Mine of Judgment").add_exits(["Slogra Soul", "Ripper Soul", "Gaibon Soul", "Tanjelly Soul", "Giant Slug Soul", "Bugbear Soul"])
        world.get_region("The Abyss").add_exits(["Alastor Soul", "Mud Demon Soul", "Frozen Shade Soul", "Malachi Soul", "White Dragon Soul", "Malacoda Soul",
                                                 "Arc Demon Soul", "Erinys Soul", "Heart Eater Soul", "Stolas Soul", "Final Guard Soul"])
        world.get_region("The Abyss Beyond Abaddon").add_exits(["Black Panther Soul", "Succubus Soul", "Iron Golem Soul"])
        