import random

from .Regions import ALL_REGIONS_INFO

bonk_trap: dict[int, list[int]] = {
  ALL_REGIONS_INFO["Mount Crumpit"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Whoville"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["City Hall"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Post Office"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Who Forest"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Ski Resort"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Civic Center"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Who Dump"].map_id: [0x81],
  ALL_REGIONS_INFO["Generator Building"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Power Plant"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Minefield"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Who Lake"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Scout's Hut"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["North Shore"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Mayor's Villa"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Submarine World"].map_id: [0x019E],
}
banana_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Mount Crumpit"].map_id: [0xAC],
    ALL_REGIONS_INFO["Whoville"].map_id: [0xAC],
    ALL_REGIONS_INFO["City Hall"].map_id: [0xAC],
    ALL_REGIONS_INFO["Post Office"].map_id: [0xAC],
    ALL_REGIONS_INFO["Who Forest"].map_id: [0xAC],
    ALL_REGIONS_INFO["Ski Resort"].map_id: [0xAC],
    ALL_REGIONS_INFO["Civic Center"].map_id: [0xAC],
    ALL_REGIONS_INFO["Who Dump"].map_id: [0xAC],
    ALL_REGIONS_INFO["Generator Building"].map_id: [0xAC],
    ALL_REGIONS_INFO["Power Plant"].map_id: [0xAC],
    ALL_REGIONS_INFO["Minefield"].map_id: [0xAC],
    ALL_REGIONS_INFO["Who Lake"].map_id: [0xAC],
    ALL_REGIONS_INFO["Scout's Hut"].map_id: [0xAC],
    ALL_REGIONS_INFO["North Shore"].map_id: [0xAC],
    ALL_REGIONS_INFO["Mayor's Villa"].map_id: [0xAC],
    ALL_REGIONS_INFO["Clock Tower"].map_id: [0xAC],
}
electrocution_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Who Dump"].map_id: [0x01A3, 0x01A4],
    ALL_REGIONS_INFO["Generator Building"].map_id: [0x019B, 0x019C],
    ALL_REGIONS_INFO["Power Plant"].map_id: [0x0197],
    ALL_REGIONS_INFO["Minefield"].map_id: [0x0198],
}
push_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Who Forest"].map_id: [0x01BF],
    ALL_REGIONS_INFO["Ski Resort"].map_id: [0x01B3],
    ALL_REGIONS_INFO["Civic Center"].map_id: [0x01BA],
    ALL_REGIONS_INFO["Who Dump"].map_id: [0x01A7],
    ALL_REGIONS_INFO["Scout's Hut"].map_id: [0x01AA],
    ALL_REGIONS_INFO["North Shore"].map_id: [0x019C],
    ALL_REGIONS_INFO["Mayor's Villa"].map_id: [0x019D],
}
ice_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Whoville"].map_id: [0x0079],
    ALL_REGIONS_INFO["Ski Resort"].map_id: [0x0079],
    ALL_REGIONS_INFO["Civic Center"].map_id: [0x0079],
}
bee_trap: dict[int, list[int]] = {
    ALL_REGIONS_INFO["Who Lake"].map_id: [0x01A1],
}
damage_trap: dict[int, list[int]] = {
  ALL_REGIONS_INFO["Mount Crumpit"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Whoville"].map_id: [0x80, 0x81, 0x79],
  ALL_REGIONS_INFO["City Hall"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Post Office"].map_id: [0x80, 0x81],
  ALL_REGIONS_INFO["Who Forest"].map_id: [0x80, 0x81, 0x01BF],
  ALL_REGIONS_INFO["Ski Resort"].map_id: [0x80, 0x81, 0x01B3, 0x79],
  ALL_REGIONS_INFO["Civic Center"].map_id: [0x80, 0x81, 0x01BA, 0x79],
  ALL_REGIONS_INFO["Who Dump"].map_id: [0x81, 0x1A7, 0x01A3, 0x01A4],
  ALL_REGIONS_INFO["Generator Building"].map_id: [0x80, 0x81, 0x019B, 0x019C],
  ALL_REGIONS_INFO["Power Plant"].map_id: [0x80, 0x81, 0x197],
  ALL_REGIONS_INFO["Minefield"].map_id: [0x80, 0x81, 0x198],
  ALL_REGIONS_INFO["Who Lake"].map_id: [0x80, 0x81, 0x1A1],
  ALL_REGIONS_INFO["Scout's Hut"].map_id: [0x80, 0x81, 0x01AA],
  ALL_REGIONS_INFO["North Shore"].map_id: [0x80, 0x81, 0x19C],
  ALL_REGIONS_INFO["Mayor's Villa"].map_id: [0x80, 0x81, 0x19D],
  ALL_REGIONS_INFO["Submarine World"].map_id: [0x019E],
}

# Converts traps received from trap link into one of the above list
BEE_TRAP_EQUIV = ["Army Trap", "Buyon Trap", "Ghost", "Gooey Bag", "OmoTrap", "Police Trap"]
ICE_TRAP_EQUIV = ["Chaos Control Trap", "Freeze Trap", "Frozen Trap", "Honey Trap", "Paralyze Trap", "Stun Trap", "Bubble Trap"]
DAMAGE_TRAP_EQUIV = ["Banana Trap", "Bomb", "Bonk Trap", "Fire Trap", "Laughter Trap", "Nut Trap", "Push Trap",
"Squash Trap", "Thwimp Trap", "TNT Barrel Trap", "Meteor Trap", "Double Damage", "Spike Ball Trap"]
BONK_TRAP_EQUIV = [""]
# SPRING_TRAP_EQUIV = ["Eject Ability", "Hiccup Trap", "Jump Trap", "Jumping Jacks Trap", "Whoops! Trap"]
HOME_TRAP_EQUIV = ["Blue Balls Curse", "Instant Death Trap", "Get Out Trap"]
# SLOWNESS_TRAP_EQUIV = ["Iron Boots Trap", "Slow Trap", "Sticky Floor Trap"]
# CUTSCENE_TRAP_EQUIV = ["Phone Trap"]
ELEC_TRAP_EQUIV = []
DEPL_TRAP_EQUIV = ["Dry Trap"]
BANANA_TRAP_EQUIV = []
PUSH_TRAP_EQUIV = []

def convert_trap(map_id: int, trap_name: str) -> int | None:
    if trap_name in BONK_TRAP_EQUIV and map_id in bonk_trap:
        return random.choice(bonk_trap[map_id])
    elif trap_name in ELEC_TRAP_EQUIV and map_id in electrocution_trap:
        return  random.choice(electrocution_trap[map_id])
    elif trap_name in BANANA_TRAP_EQUIV and map_id in banana_trap:
        return  random.choice(banana_trap[map_id])
    elif trap_name in PUSH_TRAP_EQUIV and map_id in push_trap:
        return  random.choice(push_trap[map_id])
    elif trap_name in ICE_TRAP_EQUIV and map_id in ice_trap:
        return  random.choice(ice_trap[map_id])
    elif trap_name in BEE_TRAP_EQUIV and map_id in bee_trap:
        return  random.choice(bee_trap[map_id])
    elif trap_name in DAMAGE_TRAP_EQUIV and map_id in damage_trap:
        return random.choice(damage_trap[map_id])
    else:
        return None