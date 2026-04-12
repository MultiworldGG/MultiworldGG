from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule, forbid_items_for_player
from worlds.huniepop2 import default_pairs, uniqueid_to_name, shoeid_to_name, girl_outfits


def set_rules(multiworld, player, girls, pairs, startpairs, questions, outfits, gamedata):
    is_ut = getattr(multiworld, "generation_is_fake", False)

    for girl in girls:
        set_rule(multiworld.get_entrance(f"hub-{girl}", player), lambda state, p=player, g=girl, ps=pairs: girl_unlocked(state, p, g))

        if not is_ut:
            set_rule(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique1"]]}", player), lambda state, p=player, g=girl, i=uniqueid_to_name[gamedata[girl]["unique1"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", player))
            set_rule(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique2"]]}", player), lambda state, p=player, g=girl, i=uniqueid_to_name[gamedata[girl]["unique2"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", player))
            set_rule(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique3"]]}", player), lambda state, p=player, g=girl, i=uniqueid_to_name[gamedata[girl]["unique3"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", player))
            set_rule(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique4"]]}", player), lambda state, p=player, g=girl, i=uniqueid_to_name[gamedata[girl]["unique4"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", player))

            set_rule(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe1"]]}", player), lambda state, p=player, g=girl, i=shoeid_to_name[gamedata[girl]["shoe1"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", player))
            set_rule(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe2"]]}", player), lambda state, p=player, g=girl, i=shoeid_to_name[gamedata[girl]["shoe2"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", player))
            set_rule(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe3"]]}", player), lambda state, p=player, g=girl, i=shoeid_to_name[gamedata[girl]["shoe3"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", player))
            set_rule(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe4"]]}", player), lambda state, p=player, g=girl, i=shoeid_to_name[gamedata[girl]["shoe4"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", player))

        if not outfits:
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][0]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][0]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][1]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][1]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][2]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][2]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][3]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][3]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][4]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][4]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][5]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][5]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][6]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][6]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][7]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][7]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][8]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][8]: state.has(f"{g} {o} Outfit", player))
            set_rule(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][9]} Outfit", player), lambda state, g=girl, o=girl_outfits[girl][9]: state.has(f"{g} {o} Outfit", player))

        if not is_ut:
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique1"]]}", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique2"]]}", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique3"]]}", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {uniqueid_to_name[gamedata[girl]["unique4"]]}", player), get_lock_items(girl), player)

            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe1"]]}", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe2"]]}", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe3"]]}", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Gift {girl} {shoeid_to_name[gamedata[girl]["shoe4"]]}", player), get_lock_items(girl), player)

        if questions:
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite drink", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Ice Cream Flavor", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Music Genre", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Movie Genre", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Online Activity", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Phone App", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Type Of Exercise", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Outdoor Activity", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Theme Park Ride", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Friday Night", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Sunday Morning", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Weather", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Holiday", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Pet", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite School Subject", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Place to shop", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Trait In Partner", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Own Body Part", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Sex Position", player), get_lock_items(girl), player)
            forbid_items_for_player(multiworld.get_location(f"Learn {girl}'s favourite Porn Category", player), get_lock_items(girl), player)
        if not outfits:
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][0]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][0]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][1]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][1]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][2]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][2]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][3]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][3]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][4]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][4]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][5]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][5]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][6]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][6]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][7]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][7]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][8]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][8]} Outfit"}, player)
            forbid_items_for_player(multiworld.get_location(f"Date {girl} in {girl_outfits[girl][9]} Outfit", player), get_lock_items(girl) | {f"{girl} {girl_outfits[girl][9]} Outfit"}, player)



    for pair in pairs:#pair_unlocked
        set_rule(multiworld.get_entrance(f"hub-pair{pair}", player), lambda state, p=player, ps=pair: pair_unlocked(state, p, ps))


def get_lock_items(girl: str) -> set:
    items = [f"Unlock Girl({girl})"]
    for pair in default_pairs:
        if girl in pair:
            items.append(f"Pair Unlock ({pair[0]}/{pair[1]})")
            if f"Unlock Girl({pair[0]})" not in items:
                items.append(f"Unlock Girl({pair[0]})")
            if f"Unlock Girl({pair[1]})" not in items:
                items.append(f"Unlock Girl({pair[1]})")
    return set(items)

def pair_unlocked(state: CollectionState, player: int, pair: str) -> bool:
    girl1 = pair[1:-1].split('/')[0]
    girl2 = pair[1:-1].split('/')[1]
    return state.has(f"Unlock Girl({girl1})", player) and state.has(f"Unlock Girl({girl2})", player) and state.has(f"Pair Unlock {pair}", player)

def girl_unlocked(state: CollectionState, player: int, girl: str) -> bool:
    par = False
    for p in default_pairs:
        if girl in p:
            par = par or (state.has(f"Pair Unlock ({p[0]}/{p[1]})", player) and state.has(f"Unlock Girl({p[0]})", player) and state.has(f"Unlock Girl({p[1]})", player))
    return par
