from worlds.generic.Rules import set_rule, forbid_item, forbid_items_for_player
from worlds.huniepop.Data import gift_id_to_name


def set_rules(multiworld, player, girls, girldata, goal):
    panties = set()
    girlsset = set()

    for girl in girls:
        panties.add(f"{girl}'s panties")
        girlsset.add(f"Unlock Girl({girl})")

        set_rule(multiworld.get_entrance(f"hub-{girl}", player), lambda state, g=girl: state.has(f"Unlock Girl({g})", player))

        forbid_item(multiworld.get_location(f"{girl} date 1", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl} date 2", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl} date 3", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl} date 4", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"Slept with {girl}", player), f"Unlock Girl({girl})", player)

        forbid_item(multiworld.get_location(f"{girl}'s Last Name", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Age", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Height", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Weight", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Occupation", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Cup Size", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Birthday", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Hobby", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Favourite Color", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Favourite Season", player), f"Unlock Girl({girl})", player)
        forbid_item(multiworld.get_location(f"{girl}'s Favourite Hangout", player), f"Unlock Girl({girl})", player)

        if girl == "kyu" or girl == "momo" or girl == "celeste" or girl == "venus":
            forbid_item(multiworld.get_location(f"{girl}'s Homeworld", player), f"Unlock Girl({girl})", player)
        else:
            forbid_item(multiworld.get_location(f"{girl}'s Education", player), f"Unlock Girl({girl})", player)

        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift1"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift1"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift2"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift2"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift3"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift3"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift4"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift4"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift5"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift5"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift6"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift6"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift7"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift7"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift8"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift8"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift9"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift9"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift10"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift10"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift11"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift11"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift12"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift12"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift13"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift13"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift14"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift14"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift15"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift15"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift16"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift16"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift17"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift17"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift18"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift18"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift19"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift19"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift20"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift20"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift21"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift21"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift22"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift22"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift23"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift23"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))
        set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift24"]]}", player), lambda state, g=girl, i=gift_id_to_name[girldata[girl]["gift24"]]: state.has(i, player) and state.has(f"Unlock Girl({g})", player))

        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift1"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift1"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift2"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift2"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift3"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift3"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift4"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift4"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift5"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift5"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift6"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift6"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift7"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift7"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift8"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift8"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift9"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift9"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift10"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift10"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift11"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift11"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift12"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift12"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift13"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift13"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift14"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift14"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift15"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift15"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift16"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift16"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift17"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift17"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift18"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift18"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift19"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift19"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift20"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift20"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift21"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift21"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift22"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift22"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift23"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift23"]]}"}, player)
        forbid_items_for_player(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift24"]]}", player), {f"Unlock Girl({girl})", f"{gift_id_to_name[girldata[girl]["gift24"]]}"}, player)

        if girl == "kyu":
            if "tiffany" in girls:
                set_rule(multiworld.get_location("given kyu tiffany's panties", player), lambda state: state.has("tiffany's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu tiffany's panties", player), {"Unlock Girl(kyu)", "tiffany's panties"}, player)
            if "aiko" in girls:
                set_rule(multiworld.get_location("given kyu aiko's panties", player), lambda state: state.has("aiko's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu aiko's panties", player), {"Unlock Girl(kyu)", "aiko's panties"}, player)
            if "kyanna" in girls:
                set_rule(multiworld.get_location("given kyu kyanna's panties", player), lambda state: state.has("kyanna's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu kyanna's panties", player), {"Unlock Girl(kyu)", "kyanna's panties"}, player)
            if "audrey" in girls:
                set_rule(multiworld.get_location("given kyu audrey's panties", player), lambda state: state.has("audrey's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu audrey's panties", player), {"Unlock Girl(kyu)", "audrey's panties"}, player)
            if "lola" in girls:
                set_rule(multiworld.get_location("given kyu lola's panties", player), lambda state: state.has("lola's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu lola's panties", player), {"Unlock Girl(kyu)", "lola's panties"}, player)
            if "nikki" in girls:
                set_rule(multiworld.get_location("given kyu nikki's panties", player), lambda state: state.has("nikki's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu nikki's panties", player), {"Unlock Girl(kyu)", "nikki's panties"}, player)
            if "jessie" in girls:
                set_rule(multiworld.get_location("given kyu jessie's panties", player), lambda state: state.has("jessie's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu jessie's panties", player), {"Unlock Girl(kyu)", "jessie's panties"}, player)
            if "beli" in girls:
                set_rule(multiworld.get_location("given kyu beli's panties", player), lambda state: state.has("beli's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu beli's panties", player), {"Unlock Girl(kyu)", "beli's panties"}, player)
            if "kyu" in girls:
                set_rule(multiworld.get_location("given kyu kyu's panties", player), lambda state: state.has("kyu's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu kyu's panties", player), {"Unlock Girl(kyu)", "kyu's panties"}, player)
            if "momo" in girls:
                set_rule(multiworld.get_location("given kyu momo's panties", player), lambda state: state.has("momo's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu momo's panties", player), {"Unlock Girl(kyu)", "momo's panties"}, player)
            if "celeste" in girls:
                set_rule(multiworld.get_location("given kyu celeste's panties", player), lambda state: state.has("celeste's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu celeste's panties", player), {"Unlock Girl(kyu)", "celeste's panties"}, player)
            if "venus" in girls:
                set_rule(multiworld.get_location("given kyu venus's panties", player), lambda state: state.has("venus's panties", player) and state.has(f"Unlock Girl(kyu)", player))
                forbid_items_for_player(multiworld.get_location("given kyu venus's panties", player), {"Unlock Girl(kyu)", "venus's panties"}, player)


    if goal == 1:
        set_rule(multiworld.get_location("Give kyu all available panties", player), lambda state: state.has_all(panties, player) and state.has(f"Unlock Girl(kyu)", player))
    else:
        set_rule(multiworld.get_location("Sleep with all girls", player), lambda state: state.has_all(girlsset, player))
