from Options import Option
from rule_builder.rules import Has, HasAll
from worlds.generic.Rules import forbid_item, forbid_items_for_player
from worlds.huniepop.Data import gift_id_to_name


def set_rules(world):
    multiworld  = world.multiworld
    player = world.player
    girldata = world.girldata

    is_ut = getattr(multiworld, "generation_is_fake", False)

    panties = set()
    girlsset = set()

    for girl in world.enabledgirls:
        panties.add(f"{girl}'s panties")
        girlsset.add(f"Unlock Girl({girl})")

        world.set_rule(multiworld.get_entrance(f"hub-{girl}", player), Has(f"Unlock Girl({girl})"))

        if world.options.progressive_dates:
            if not is_ut:
                world.set_rule(multiworld.get_location(f"{girl} date 1", player), Has("Date Pass", 1))
                world.set_rule(multiworld.get_location(f"{girl} date 2", player), Has("Date Pass", 2))
                world.set_rule(multiworld.get_location(f"{girl} date 3", player), Has("Date Pass", 3))
                world.set_rule(multiworld.get_location(f"{girl} date 4", player), Has("Date Pass", 4))
                world.set_rule(multiworld.get_location(f"Slept with {girl}", player), Has("Date Pass", 5))

        if not is_ut and not world.options.disable_girl_gifts.value:
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift1"]]}", player), Has(gift_id_to_name[girldata[girl]["gift1"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift2"]]}", player), Has(gift_id_to_name[girldata[girl]["gift2"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift3"]]}", player), Has(gift_id_to_name[girldata[girl]["gift3"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift4"]]}", player), Has(gift_id_to_name[girldata[girl]["gift4"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift5"]]}", player), Has(gift_id_to_name[girldata[girl]["gift5"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift6"]]}", player), Has(gift_id_to_name[girldata[girl]["gift6"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift7"]]}", player), Has(gift_id_to_name[girldata[girl]["gift7"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift8"]]}", player), Has(gift_id_to_name[girldata[girl]["gift8"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift9"]]}", player), Has(gift_id_to_name[girldata[girl]["gift9"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift10"]]}", player), Has(gift_id_to_name[girldata[girl]["gift10"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift11"]]}", player), Has(gift_id_to_name[girldata[girl]["gift11"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift12"]]}", player), Has(gift_id_to_name[girldata[girl]["gift12"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift13"]]}", player), Has(gift_id_to_name[girldata[girl]["gift13"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift14"]]}", player), Has(gift_id_to_name[girldata[girl]["gift14"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift15"]]}", player), Has(gift_id_to_name[girldata[girl]["gift15"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift16"]]}", player), Has(gift_id_to_name[girldata[girl]["gift16"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift17"]]}", player), Has(gift_id_to_name[girldata[girl]["gift17"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift18"]]}", player), Has(gift_id_to_name[girldata[girl]["gift18"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift19"]]}", player), Has(gift_id_to_name[girldata[girl]["gift19"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift20"]]}", player), Has(gift_id_to_name[girldata[girl]["gift20"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift21"]]}", player), Has(gift_id_to_name[girldata[girl]["gift21"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift22"]]}", player), Has(gift_id_to_name[girldata[girl]["gift22"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift23"]]}", player), Has(gift_id_to_name[girldata[girl]["gift23"]]) & Has(f"Unlock Girl({girl})"))
            world.set_rule(multiworld.get_location(f"Gift {girl} {gift_id_to_name[girldata[girl]["gift24"]]}", player), Has(gift_id_to_name[girldata[girl]["gift24"]]) & Has(f"Unlock Girl({girl})"))

        if girl == "kyu":
            for gp in world.enabledgirls:
                world.set_rule(multiworld.get_location(f"given kyu {gp}'s panties", player), HasAll(f"{gp}'s panties","Unlock Girl(kyu)"))

    if world.options.goal.value == 1:
        world.set_rule(multiworld.get_location("Give kyu all available panties", player), HasAll(*panties) & Has(f"Unlock Girl(kyu)"))
    else:
        if world.options.progressive_dates and not is_ut:
            world.set_rule(multiworld.get_location("Sleep with all girls", player), HasAll(*girlsset) & Has("Date Pass", 5))
        else:
            world.set_rule(multiworld.get_location("Sleep with all girls", player), HasAll(*girlsset))

    if not is_ut and world.shopslots > 0:
        if world.options.progressive_dates:
            world.set_rule(multiworld.get_entrance("hub-shop", player), Has("Date Pass", 4))