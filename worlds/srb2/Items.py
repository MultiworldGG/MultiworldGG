from typing import NamedTuple

from BaseClasses import Item, ItemClassification


class SRB2Item(Item):
    game: str = "Sonic Robo Blast 2"

class SRB2ItemData(NamedTuple):
    code: int | None = None
    classification: ItemClassification = ItemClassification.progression


generic_item_data_table: dict[str, SRB2ItemData] = {
    "Emblem": SRB2ItemData(1, ItemClassification.progression_deprioritized_skip_balancing),
    "Chaos Emerald": SRB2ItemData(2),
    "Progressive Emblem Hint": SRB2ItemData(3, ItemClassification.useful),
    "1UP": SRB2ItemData(4, ItemClassification.filler),

    "& Knuckles": SRB2ItemData(70, ItemClassification.trap | ItemClassification.useful),
    "50 Rings": SRB2ItemData(71, ItemClassification.filler),
    "20 Rings": SRB2ItemData(72, ItemClassification.filler),
    "10 Rings": SRB2ItemData(73, ItemClassification.filler),
    "+5 Starting Rings": SRB2ItemData(74, ItemClassification.useful),
    "1000 Points": SRB2ItemData(76, ItemClassification.filler),
    "Temporary Invincibility": SRB2ItemData(78, ItemClassification.filler),
    "Temporary Super Sneakers": SRB2ItemData(79, ItemClassification.filler),
    "Sound Test": SRB2ItemData(80, ItemClassification.filler),
    "Double Rings": SRB2ItemData(84, ItemClassification.filler),


    #"Extended Invincibility": SRB2ItemData(90, ItemClassification.useful),
    #"Extended Super Sneakers": SRB2ItemData(91, ItemClassification.useful),
    #"Max Drill Increase": SRB2ItemData(92, ItemClassification.useful),
}

# reversed controls
# super ring drain - drains rings and kills you when you run out
#increased defense - taking damage only gets rid of 100 rings
# killing dead
# 1 ring
# gambling

# toss flag or die
# eggman virus

# play credits

# no character ability - no thok, no flying, no player.charability
# get made fun of - hud element that makes fun of you


# Spindash //prog roll WILL work because rolling down slopes

# something to nerf knuckles
# progressive tails flight
# Fang's Popgun
# metal sonic's booster

#wacky ideas
# monitors
# checkpoints
# goal posts
# Emerald tokens
# ideya capsules
# floating mines (prog trap?)
# TNT barrels (prog trap?)

# shield upgrades
# force - +1 hit | no knockback on hit
# attract - can target monitors/springs | doesnt short out in water
# wind - gets rid of smog | extra jump
# armageddon - deflects projectiles (helps with atz club)
# elemental - spike protection | electric protection | better fire trail


# pity -
# flame - liquids dont destroy it
# bubble - anti fire?
# lightning - extra jump




traps_item_data_table:dict[str, SRB2ItemData] = {

    "Forced Gravity Boots": SRB2ItemData(5, ItemClassification.trap),
    "Forced Pity Shield": SRB2ItemData(6, ItemClassification.trap),
    "Replay Tutorial": SRB2ItemData(7, ItemClassification.trap),
    "Ring Loss": SRB2ItemData(8, ItemClassification.trap),
    "Dropped Inputs": SRB2ItemData(9, ItemClassification.trap),#rework to drop inputs randomly over 30 seconds
    "Slippery Floors": SRB2ItemData(75, ItemClassification.trap),
    "Sonic Forces": SRB2ItemData(77, ItemClassification.trap),
    "Self-Propelled Bomb": SRB2ItemData(81, ItemClassification.trap),
    "Shrink Monitor": SRB2ItemData(82, ItemClassification.trap),
    "Grow Monitor": SRB2ItemData(83, ItemClassification.trap),
    #"Reversed Controls": SRB2ItemData(85, ItemClassification.trap),
    "Jumpscare": SRB2ItemData(86, ItemClassification.trap)
#Slip trap

}
objects_item_table: dict[str, SRB2ItemData] = {
    "Zoom Tubes": SRB2ItemData(150),#power erz1 erz2
    "Rope Hangs": SRB2ItemData(151),#power #acz1, erz2
    "Swinging Maces": SRB2ItemData(152),#power #ffz cez1 cez2
    "Minecarts": SRB2ItemData(153),#power #acz2
    "Rollout Rocks": SRB2ItemData(154),#power #rvz
    "Gargoyle Statues": SRB2ItemData(155),#object #dsz1 dsz2
    "Air Bubbles": SRB2ItemData(156),#object most zones
    "Buoyant Slime": SRB2ItemData(157),#floor thz1 thz2
    "Dust Devils": SRB2ItemData(158),#object acz1 acz2
    "Yellow Springs": SRB2ItemData(159),#object
    "Red Springs": SRB2ItemData(160),#object
    "Blue Springs": SRB2ItemData(161,ItemClassification.useful),#object

    #"NiGHTS Bumpers": SRB2ItemData(162),  # object
    #"Ideya Capsules": SRB2ItemData(163),  # object
    #"Starposts": SRB2ItemData(164),  # object (probably a bad idea)
    #"Signposts": SRB2ItemData(165),  # object (probably a bad idea)
    #"Floating Mines": SRB2ItemData(166, ItemClassification.progression | ItemClassification.trap),  # object
    #"TNT Barrels": SRB2ItemData(167, ItemClassification.progression | ItemClassification.trap),  # object
}

zones_item_data_table: dict[str, SRB2ItemData] = {
    "Greenflower Zone": SRB2ItemData(10),
    "Techno Hill Zone": SRB2ItemData(11),
    "Deep Sea Zone": SRB2ItemData(12),
    "Castle Eggman Zone": SRB2ItemData(13),
    "Arid Canyon Zone": SRB2ItemData(14),
    "Red Volcano Zone": SRB2ItemData(15),
    "Egg Rock Zone": SRB2ItemData(16),
    "Black Core Zone": SRB2ItemData(17),

    "Frozen Hillside Zone": SRB2ItemData(18),
    "Pipe Towers Zone": SRB2ItemData(19),
    "Forest Fortress Zone": SRB2ItemData(20),
    "Final Demo Zone": SRB2ItemData(21),

    "Haunted Heights Zone": SRB2ItemData(22),
    "Aerial Garden Zone": SRB2ItemData(23),
    "Azure Temple Zone": SRB2ItemData(24),
}
acts_item_data_table: dict[str,SRB2ItemData]={

    "Greenflower Zone (Act 1)": SRB2ItemData(105),
    "Greenflower Zone (Act 2)": SRB2ItemData(106),
    "Greenflower Zone (Act 3)": SRB2ItemData(107),
    "Techno Hill Zone (Act 1)": SRB2ItemData(108),
    "Techno Hill Zone (Act 2)": SRB2ItemData(109),
    "Techno Hill Zone (Act 3)": SRB2ItemData(110),
    "Deep Sea Zone (Act 1)": SRB2ItemData(111),
    "Deep Sea Zone (Act 2)": SRB2ItemData(112),
    "Deep Sea Zone (Act 3)": SRB2ItemData(113),
    "Castle Eggman Zone (Act 1)": SRB2ItemData(114),
    "Castle Eggman Zone (Act 2)": SRB2ItemData(115),
    "Castle Eggman Zone (Act 3)": SRB2ItemData(116),
    "Arid Canyon Zone (Act 1)": SRB2ItemData(117),
    "Arid Canyon Zone (Act 2)": SRB2ItemData(118),
    "Arid Canyon Zone (Act 3)": SRB2ItemData(119),
    "Red Volcano Zone (Act 1)": SRB2ItemData(120),
    #"Red Volcano Zone (Act 2)": SRB2ItemData(121),
    #"Red Volcano Zone (Act 3)": SRB2ItemData(122),
    "Egg Rock Zone (Act 1)": SRB2ItemData(123),
    "Egg Rock Zone (Act 2)": SRB2ItemData(124),
    #"Egg Rock Zone (Act 3)": SRB2ItemData(125),
    "Black Core Zone (Act 1)": SRB2ItemData(126),
    "Black Core Zone (Act 2)": SRB2ItemData(127),
    "Black Core Zone (Act 3)": SRB2ItemData(128),
    "Frozen Hillside Zone": SRB2ItemData(18),
    "Pipe Towers Zone": SRB2ItemData(19),
    "Forest Fortress Zone": SRB2ItemData(20),
    "Final Demo Zone": SRB2ItemData(21),

    "Haunted Heights Zone": SRB2ItemData(22),
    "Aerial Garden Zone": SRB2ItemData(23),
    "Azure Temple Zone": SRB2ItemData(24),
}

special_item_data_table: dict[str, SRB2ItemData] = {
    "Floral Field Zone": SRB2ItemData(25),
    "Toxic Plateau Zone": SRB2ItemData(26),
    "Flooded Cove Zone": SRB2ItemData(27),
    "Cavern Fortress Zone": SRB2ItemData(28),
    "Dusty Wasteland Zone": SRB2ItemData(29),
    "Magma Caves Zone": SRB2ItemData(30),
    "Egg Satellite Zone": SRB2ItemData(31),
    "Black Hole Zone": SRB2ItemData(32),

    "Christmas Chime Zone": SRB2ItemData(33),
    "Dream Hill Zone": SRB2ItemData(34),
    "Alpine Paradise Zone": SRB2ItemData(35),
}

sp_acts_item_data_table: dict[str, SRB2ItemData] = {
"Alpine Paradise Zone (Act 1)": SRB2ItemData(129),
"Alpine Paradise Zone (Act 2)": SRB2ItemData(130),
}


character_item_data_table: dict[str, SRB2ItemData] = {
    "Tails": SRB2ItemData(50),
    "Knuckles": SRB2ItemData(51),
    "Fang": SRB2ItemData(52),
    "Amy": SRB2ItemData(53),
    "Metal Sonic": SRB2ItemData(54),
    "Sonic": SRB2ItemData(55),

}
other_item_table:dict[str, SRB2ItemData] = {
    "Whirlwind Shield":SRB2ItemData(56),
    "Armageddon Shield":SRB2ItemData(57),
    "Elemental Shield":SRB2ItemData(58),
    "Attraction Shield": SRB2ItemData(59, ItemClassification.useful),
    "Force Shield": SRB2ItemData(60, ItemClassification.useful),
    "Flame Shield": SRB2ItemData(61, ItemClassification.useful),
    "Bubble Shield": SRB2ItemData(62),
    "Lightning Shield": SRB2ItemData(63)
}
nights_item_table:dict[str, SRB2ItemData] = {
"Super Paraloop": SRB2ItemData(100, ItemClassification.progression),
"Nightopian Helper": SRB2ItemData(101, ItemClassification.useful),
"Link Freeze": SRB2ItemData(102, ItemClassification.useful),
"Extra Time": SRB2ItemData(103, ItemClassification.progression),
"Drill Refill": SRB2ItemData(104, ItemClassification.useful),
}



mpmatch_item_table:dict[str, SRB2ItemData] = {
"Jade Valley Zone":SRB2ItemData(200),
"Noxious Factory Zone":SRB2ItemData(201),
"Tidal Palace Zone":SRB2ItemData(202),
"Thunder Citadel Zone":SRB2ItemData(203),
"Desolate Twilight Zone":SRB2ItemData(204),
"Frigid Mountain Zone":SRB2ItemData(205),
"Orbital Hangar Zone":SRB2ItemData(206),
"Sapphire Falls Zone":SRB2ItemData(207),
"Diamond Blizzard Zone":SRB2ItemData(208),
"Celestial Sanctuary Zone":SRB2ItemData(209),
"Frost Columns Zone":SRB2ItemData(210),
"Meadow Match Zone":SRB2ItemData(211),
"Granite Lake Zone":SRB2ItemData(212),
"Summit Showdown Zone":SRB2ItemData(213),
"Silver Shiver Zone":SRB2ItemData(214),
"Uncharted Badlands Zone":SRB2ItemData(215),
"Pristine Shores Zone":SRB2ItemData(216),
"Crystalline Heights Zone":SRB2ItemData(217),
"Starlit Warehouse Zone":SRB2ItemData(218),
"Midnight Abyss Zone":SRB2ItemData(219),
"Airborne Temple Zone":SRB2ItemData(220),

}





item_data_table = {
    **generic_item_data_table,
    **zones_item_data_table,
    **acts_item_data_table,
    **objects_item_table,
    **character_item_data_table,
    **other_item_table,
    **mpmatch_item_table,
    **traps_item_data_table,
    **nights_item_table,
    **special_item_data_table,
    **sp_acts_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
