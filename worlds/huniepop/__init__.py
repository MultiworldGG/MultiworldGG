import logging

from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.huniepop.Data import girllist, rand_girl_data, gift_id_to_name
from worlds.huniepop.Items import item_table, HPItem, panties_item, gift_item, girl_unlock, token_item, junk_item, item_datapackage, filler_items
from worlds.huniepop.Locations import location_table, HPLocation, loc_datapackage
from worlds.huniepop.Options import HPOptions
from worlds.huniepop.Rules import set_rules

class HuniePopWeb(WebWorld):
    rating: str = "nsfw"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Hunie Pop randomizer connected to an MWGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["dotsofdarkness"]
    )]


class HuniePop(World):
    """
    HuniePop is a unique sim experience around 8 girls.
    It's a gameplay first approach that's part dating sim, part puzzle game, with light RPG elements.
    """
    game = "Hunie Pop"

    item_name_to_id = item_table
    location_name_to_id = location_table
    web = HuniePopWeb()
    options_dataclass = HPOptions
    options: HPOptions

    startgirls = []
    startgirl = -1
    enabledgirls = []
    girldata = {}

    totalloc = 0
    totalitem = 0

    trashitems = 0
    shopslots = 0

    def generate_early(self):
        self.startgirls = []
        self.startgirl = -1
        self.girldata = {}
        self.totalloc = 0
        self.totalitem = 0

        if "kyu" not in self.options.enabled_girls.value and self.options.goal.value==1:
            logging.warning(f"""(Hunie Pop) Adding "kyu" to "enabled_girls" for Player:"{self.player_name}" since goal is "Give kyu all available panties\"""")
            self.options.enabled_girls.value.add("kyu")


        self.enabledgirls = list(self.options.enabled_girls.value.copy())
        self.startgirls = self.random.sample(self.enabledgirls, self.options.number_of_starting_girls.value)
        self.startgirl = girllist.index(self.random.sample(self.startgirls, 1)[0])+1


        self.girldata = rand_girl_data(self.options, self.random)

        totallocations = 0
        totalitems = 0

        #total locations
        if True: #date locations
            totallocations += (4*len(self.enabledgirls))
        if True: #sleep with locations
            totallocations += len(self.enabledgirls)
        if "kyu" in self.enabledgirls: #pantie turn in locations
            totallocations += len(self.enabledgirls)
        if True: #gift locations
            totallocations += (24*len(self.enabledgirls))
        if True: #question locations
            totallocations += (12*len(self.enabledgirls))
        if True: #shop locations
            totallocations += self.options.number_shop_items.value


        #total items
        if True: #girl unlock items
            totalitems += len(self.enabledgirls) - len(self.startgirls)
        if True: #pantie items
            totalitems += len(self.enabledgirls)
        if True: #gift items
            totalitems += (len(self.enabledgirls) * 24)
        if True: #token items
            totalitems += (8*6)


        if totallocations != totalitems:
            if totallocations > totalitems:
                self.trashitems = totallocations-totalitems
                self.shopslots = self.options.number_shop_items.value
                totalitems = totallocations
            else:
                self.shopslots = totalitems - (totallocations - self.options.number_shop_items.value)
                totallocations = totalitems

        self.totalloc = totallocations
        self.totalitem = totalitems


    def create_regions(self):
        hub_region = Region("Menu", self.player, self.multiworld)

        if self.options.goal.value == 0:
            hub_region.add_locations({"Sleep with all girls":self.location_name_to_id["Sleep with all girls"]}, HPLocation)

        self.multiworld.regions.append(hub_region)


        for girl in self.enabledgirls:
            girlregion = Region(f"{girl} Region", self.player, self.multiworld)

            girlregion.add_locations({
                f"{girl} date 1": self.location_name_to_id[f"{girl} date 1"],
                f"{girl} date 2": self.location_name_to_id[f"{girl} date 2"],
                f"{girl} date 3": self.location_name_to_id[f"{girl} date 3"],
                f"{girl} date 4": self.location_name_to_id[f"{girl} date 4"],
                f"Slept with {girl}": self.location_name_to_id[f"Slept with {girl}"],
                f"{girl}'s Last Name": self.location_name_to_id[f"{girl}'s Last Name"],
                f"{girl}'s Age": self.location_name_to_id[f"{girl}'s Age"],
                f"{girl}'s Height": self.location_name_to_id[f"{girl}'s Height"],
                f"{girl}'s Weight": self.location_name_to_id[f"{girl}'s Weight"],
                f"{girl}'s Occupation": self.location_name_to_id[f"{girl}'s Occupation"],
                f"{girl}'s Cup Size": self.location_name_to_id[f"{girl}'s Cup Size"],
                f"{girl}'s Birthday": self.location_name_to_id[f"{girl}'s Birthday"],
                f"{girl}'s Hobby": self.location_name_to_id[f"{girl}'s Hobby"],
                f"{girl}'s Favourite Color": self.location_name_to_id[f"{girl}'s Favourite Color"],
                f"{girl}'s Favourite Season": self.location_name_to_id[f"{girl}'s Favourite Season"],
                f"{girl}'s Favourite Hangout": self.location_name_to_id[f"{girl}'s Favourite Hangout"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift1"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift1"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift2"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift2"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift3"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift3"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift4"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift4"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift5"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift5"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift6"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift6"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift7"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift7"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift8"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift8"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift9"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift9"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift10"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift10"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift11"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift11"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift12"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift12"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift13"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift13"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift14"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift14"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift15"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift15"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift16"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift16"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift17"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift17"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift18"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift18"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift19"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift19"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift20"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift20"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift21"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift21"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift22"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift22"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift23"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift23"]]}"],
                f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift24"]]}": self.location_name_to_id[f"Gift {girl} {gift_id_to_name[self.girldata[girl]["gift24"]]}"],

            }, HPLocation)

            if girl == "kyu" or girl == "momo" or girl == "celeste" or girl == "venus":
                girlregion.add_locations({f"{girl}'s Homeworld": self.location_name_to_id[f"{girl}'s Homeworld"]}, HPLocation)
            else:
                girlregion.add_locations({f"{girl}'s Education": self.location_name_to_id[f"{girl}'s Education"]}, HPLocation)

            if girl == "kyu":
                if "tiffany" in self.enabledgirls:
                    girlregion.add_locations({"given kyu tiffany's panties": self.location_name_to_id["given kyu tiffany's panties"]}, HPLocation)
                if "aiko" in self.enabledgirls:
                    girlregion.add_locations({"given kyu aiko's panties": self.location_name_to_id["given kyu aiko's panties"]}, HPLocation)
                if "kyanna" in self.enabledgirls:
                    girlregion.add_locations({"given kyu kyanna's panties": self.location_name_to_id["given kyu kyanna's panties"]}, HPLocation)
                if "audrey" in self.enabledgirls:
                    girlregion.add_locations({"given kyu audrey's panties": self.location_name_to_id["given kyu audrey's panties"]}, HPLocation)
                if "lola" in self.enabledgirls:
                    girlregion.add_locations({"given kyu lola's panties": self.location_name_to_id["given kyu lola's panties"]}, HPLocation)
                if "nikki" in self.enabledgirls:
                    girlregion.add_locations({"given kyu nikki's panties": self.location_name_to_id["given kyu nikki's panties"]}, HPLocation)
                if "jessie" in self.enabledgirls:
                    girlregion.add_locations({"given kyu jessie's panties": self.location_name_to_id["given kyu jessie's panties"]}, HPLocation)
                if "beli" in self.enabledgirls:
                    girlregion.add_locations({"given kyu beli's panties": self.location_name_to_id["given kyu beli's panties"]}, HPLocation)
                if "kyu" in self.enabledgirls:
                    girlregion.add_locations({"given kyu kyu's panties": self.location_name_to_id["given kyu kyu's panties"]}, HPLocation)
                if "momo" in self.enabledgirls:
                    girlregion.add_locations({"given kyu momo's panties": self.location_name_to_id["given kyu momo's panties"]}, HPLocation)
                if "celeste" in self.enabledgirls:
                    girlregion.add_locations({"given kyu celeste's panties": self.location_name_to_id["given kyu celeste's panties"]}, HPLocation)
                if "venus" in self.enabledgirls:
                    girlregion.add_locations({"given kyu venus's panties": self.location_name_to_id["given kyu venus's panties"]}, HPLocation)

                if self.options.goal.value == 1:
                    girlregion.add_locations({"Give kyu all available panties": self.location_name_to_id["Give kyu all available panties"]}, HPLocation)


            hub_region.connect(girlregion, f"hub-{girl}")


        if self.shopslots > 0:
            shop_region = Region("shop", self.player, self.multiworld)
            for i in range(self.shopslots):
                shop_region.add_locations({f"shop_location: {i+1}" : self.location_name_to_id[f"shop_location: {i+1}"]}, HPLocation)
            hub_region.connect(shop_region, "hub-shop")




    def create_item(self, name: str) -> HPItem:
        if name in girl_unlock or name in panties_item or name in gift_item or name == "Goal Achieved":
            return HPItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        if name in token_item:
            return HPItem(name, ItemClassification.useful, self.item_name_to_id[name], self.player)

        return HPItem(name, ItemClassification.filler, self.item_name_to_id[name], self.player)



    def create_items(self):
        for girl in self.enabledgirls:
            if girl in self.startgirls:
                self.multiworld.push_precollected(self.create_item(f"Unlock Girl({girl})"))
            else:
                self.multiworld.itempool.append(self.create_item(f"Unlock Girl({girl})"))
            self.multiworld.itempool.append((self.create_item(f"{girl}'s panties")))

            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift1"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift2"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift3"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift4"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift5"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift6"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift7"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift8"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift9"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift10"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift11"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift12"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift13"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift14"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift15"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift16"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift17"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift18"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift19"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift20"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift21"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift22"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift23"]])))
            self.multiworld.itempool.append((self.create_item(gift_id_to_name[self.girldata[girl]["gift24"]])))



        for t in token_item:
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))
            self.multiworld.itempool.append(self.create_item(t))


        if self.trashitems > 0:
            if self.options.filler_item.value == 0:
                for i in range(self.trashitems):
                    self.multiworld.itempool.append(self.create_item("Nothing"))
            else:
                for i in range(self.trashitems):
                    self.multiworld.itempool.append(self.create_item(self.random.choice([*filler_items])))


    def set_rules(self):
        if self.options.goal.value == 1:
            self.multiworld.get_location("Give kyu all available panties", self.player).place_locked_item(self.create_item("Goal Achieved"))
        else:
            self.multiworld.get_location("Sleep with all girls", self.player).place_locked_item(self.create_item("Goal Achieved"))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal Achieved", self.player)

        set_rules(self.multiworld, self.player, self.enabledgirls, self.girldata, self.options.goal.value)

        if self.shopslots > self.options.exclude_shop_items:
            for i in range(self.shopslots):
                if i>=self.options.exclude_shop_items:
                    self.multiworld.get_location(f"shop_location: {i + 1}", self.player).progress_type = LocationProgressType.EXCLUDED

    #something to stop warnings happening in console when running tests
    def get_filler_item_name(self) -> str:
        return self.random.choice(list(filler_items.keys()))

    def fill_slot_data(self) -> dict:
        returndict = {
            "start_girl": self.startgirl,

            "number_of_shop_items": self.shopslots,
            "shop_item_cost": self.options.shop_item_cost.val,
            "shop_gift_cost": self.options.shop_gift_cost.val,
            "shop_date_gift_cost": self.options.shop_date_gift_cost.val,
            "hunie_gift_cost": self.options.hunie_gift_cost.val,

            "puzzle_moves": self.options.puzzle_moves.value,
            "puzzle_affection_base": self.options.puzzle_affection_base.value,
            "puzzle_affection_add": self.options.puzzle_affection_add.value,

            "girldata": self.girldata,

            "total_loc": self.totalloc,
            "total_item": self.totalitem,

            "world_version": self.world_version,
            "goal": self.options.goal.value,

            "deathlink": self.options.deathlink.value,

            "tiffany_enabled": "tiffany" in self.options.enabled_girls.value,
            "aiko_enabled": "aiko" in self.options.enabled_girls.value,
            "kyanna_enabled": "kyanna" in self.options.enabled_girls.value,
            "audrey_enabled": "audrey" in self.options.enabled_girls.value,
            "lola_enabled": "lola" in self.options.enabled_girls.value,
            "nikki_enabled": "nikki" in self.options.enabled_girls.value,
            "jessie_enabled": "jessie" in self.options.enabled_girls.value,
            "beli_enabled": "beli" in self.options.enabled_girls.value,
            "kyu_enabled": "kyu" in self.options.enabled_girls.value,
            "momo_enabled": "momo" in self.options.enabled_girls.value,
            "celeste_enabled": "celeste" in self.options.enabled_girls.value,
            "venus_enabled": "venus" in self.options.enabled_girls.value,

            **item_datapackage,

            **loc_datapackage,
        }

        return returndict