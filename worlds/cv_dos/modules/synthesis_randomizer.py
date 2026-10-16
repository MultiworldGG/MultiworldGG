from ..in_game_data import global_soul_table

normal_synth_souls = [
    # Shortswords
    "Armor Knight Soul",
    "Corpseweed Soul",
    "Great Armor Soul",
    "Mollusca Soul",
    "Treant Soul",
    "Lilith Soul",
    "Lilith Soul",
    "Catoblepas Soul",
    "Frozen Shade Soul",
    "Dead Pirate Soul",
    "Iron Golem Soul",
    "Iron Golem Soul",
    "Iron Golem Soul",
    "Arc Demon Soul",
    "Abaddon Soul",
    # Greatswords
    "Warg Soul",
    "Great Armor Soul",
    "Valkyrie Soul",
    "Lilith Soul",
    "Draghignazzo Soul",
    "Gergoth Soul",
    "Final Guard Soul",
    "Alastor Soul",
    # Rapiers
    "White Dragon Soul",
    "White Dragon Soul",
    "White Dragon Soul",
    "Quetzalcoatl Soul",
    "Malacoda Soul",
    # Spears
    "Armor Knight Soul",
    "Warg Soul",
    "Valkyrie Soul",
    "Mini Devil Soul",
    "Decarabia Soul",
    "Slogra Soul",
    "Erinys Soul",
    "Bugbear Soul",
    # Axes
    "Axe Armor Soul",
    "Manticore Soul",
    "Great Axe Armor Soul",
    "Final Guard Soul",
    "Death Soul",
    # Hammers
    "Needles Soul",
    "Bugbear Soul",
    # Katanas
    "Bomber Armor Soul",
    "Mini Devil Soul",
    "Devil Soul",
    "Barbariccia Soul",
    "Malachi Soul",
    "Gaibon Soul",
    "Malacoda Soul",
    # Fists
    "Zombie Soul",
    "Slaughterer Soul",
    "Hell Boar Soul",
    "Werewolf Soul",
]


def randomize_synthesis(world):
    valid_synth_souls = [
        "Imp Soul",
        "Skeleton Soul",
        "Zombie Soul",
        "Axe Armor Soul",
        "Student Witch Soul",
        "Warg Soul",
        "Bomber Armor Soul",
        "Amalaric Sniper Soul",
        "Cave Troll Soul",
        "Waiter Skeleton Soul",
        "Slime Soul",
        "Yorick Soul",
        "Une Soul",
        "Mandragora Soul",
        "Rycuda Soul",
        "Fleaman Soul",
        "Ripper Soul",
        "Guillotiner Soul",
        "Killer Clown Soul",
        "Malachi Soul",
        "Disc Armor Soul",
        "Great Axe Armor Soul",
        "Slaughterer Soul",
        "Hell Boar Soul",
        "Frozen Shade Soul",
        "Merman Soul",
        "Larva Soul",
        "Ukoback Soul",
        "Decarabia Soul",
        "Succubus Soul",
        "Slogra Soul",
        "Erinys Soul",
        "Homunculus Soul",
        "Witch Soul",
        "Fish Head Soul",
        "Mollusca Soul",
        "Dead Mate Soul",
        "Killer Fish Soul",
        "Malacoda Soul",
        "Flame Demon Soul",
        "Aguni Soul",
        "Abaddon Soul",
        "Armor Knight Soul",
        "Spin Devil Soul",
        "Skull Archer Soul",
        "Ghost Soul",
        "Yeti Soul",
        "Buer Soul",
        "Manticore Soul",
        "Mushussu Soul",
        "White Dragon Soul",
        "Catoblepas Soul",
        "Gorgon Soul",
        "Persephone Soul",
        "Flying Humanoid Soul",
        "Devil Soul",
        "Medusa Head Soul",
        "Final Guard Soul",
        "Werewolf Soul",
        "Alura Une Soul",
        "Iron Golem Soul",
        "Barbariccia Soul",
        "Valkyrie Soul",
        "Bat Soul",
        "Great Armor Soul",
        "Mini Devil Soul",
        "Harpy Soul",
        "Corpseweed Soul",
        "Quetzalcoatl Soul",
        "Needles Soul",
        "Alastor Soul",
        "Gaibon Soul",
        "Gergoth Soul",
        "Death Soul",
        "Golem Soul",
        "Bone Pillar Soul",
        "Lilith Soul",
        "Ghost Dancer Soul",
        "Tanjelly Soul",
        "Bugbear Soul",
        "Arc Demon Soul",
        "Giant Slug Soul",
        "Killer Doll Soul",
        "Tombstone Soul",
        "Treant Soul",
        "Ghoul Soul",
        "Skelerang Soul",
        "Dead Warrior Soul",
        "Dead Pirate Soul",
        "Draghignazzo Soul",
        "Heart Eater Soul",
        "Peeping Eye Soul",
        "Skeleton Farmer Soul",
        "The Creature Soul",
        "Mimic Soul",
        "Mothman Soul",
        "Ouija Table Soul",
        "Dead Crusader Soul",
        "Stolas Soul",
        "Wakwak Tree Soul"
    ]
    valid_synth_souls = [soul for soul in valid_synth_souls if soul not in world.important_souls]  # Filter out important souls

    world.synth_souls = normal_synth_souls.copy()
    if world.options.randomize_synthesis_souls:
        for i, soul in enumerate(world.synth_souls):
            world.synth_souls[i] = world.random.choice(valid_synth_souls)

    for i, soul in enumerate(world.synth_souls):  # We do this to get rid of any important souls if synthesis rando is off
        if soul in world.important_souls:
            world.synth_souls[i] = world.random.choice(valid_synth_souls)


def write_synthesis(world, rom):

    shortswords = world.synth_souls[:0x0F]
    greatswords = world.synth_souls[0x0F:0x17]
    rapiers = world.synth_souls[0x17:0x1C]
    spears = world.synth_souls[0x1C:0x24]
    axes = world.synth_souls[0x24:0x29]
    hammers = world.synth_souls[0x29:0x2B]
    katanas = world.synth_souls[0x2B:0x32]
    punchs = world.synth_souls[0x32:]

    for i, soul in enumerate(hammers):
        rom.write_to_file(0x209CC4D + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(punchs):
        rom.write_to_file(0x209CC59 + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(rapiers):
        rom.write_to_file(0x209CC6D + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(katanas):
        rom.write_to_file(0x209CC9D + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(greatswords):
        rom.write_to_file(0x209CCDD + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(spears):
        rom.write_to_file(0x209CD01 + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(shortswords):
        rom.write_to_file(0x209CD65 + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))

    for i, soul in enumerate(axes):
        rom.write_to_file(0x209CC85 + (4 * i), "arm9", bytearray([global_soul_table.index(soul)]))
