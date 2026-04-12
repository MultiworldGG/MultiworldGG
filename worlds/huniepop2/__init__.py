from typing import Any

from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Data import default_pairs, girl_outfits, uniqueid_to_name, shoeid_to_name, randomise_stuff, default_girl_outfit, baggageid_to_name, girl_list
from .Items import HP2Item, token_item, token_item_amounts, filler_item, outfits_item, fairy_wings_item, gift_shoe_item, gift_unique_item, pair_unlock_item, girl_unlock_item, item_list, item_datapackage

from .Locations import location_table, HP2Location, shop_loc_start, loc_datapackage
from .Options import HP2Options, starting_pairs, starting_girls
from .Rules import set_rules, girl_unlocked
from ..generic.Rules import set_rule

class HuniePop2Web(WebWorld):
    rating: str = "nsfw"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Hunie Pop 2 randomizer connected to an MWGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["dotsofdarkness"]
    )]

class HuniePop2(World):
    """
    HuniePop 2: Double Date is a 2021 tile-matching and dating sim adult video game. The game follows the dating adventures of the main character 
    as they try to woo several different women in their home town; its characters are drawn in anime art style and they have a fully-voiced and animated dialog.
    """
    game = "Hunie Pop 2"
    item_name_to_id = item_list
    item_id_to_name = {item_list[name]: name for name in item_list}
    item_name_groups = {
        "wings": fairy_wings_item,
        "girls": girl_unlock_item,
        "pairs": pair_unlock_item
    }

    options_dataclass = HP2Options
    options: HP2Options

    web = HuniePop2Web()
    startingpairs = []
    startinggirls = []
    shopslots = 0
    trashitems = 0
    wingval = 0

    totall = 0
    totali = 0

    gamedata = {}

    location_name_to_id = location_table

    pair_order = (
        "(abia/lola)",
        "(lola/nora)",
        "(candace/nora)",
        "(ashley/polly)",
        "(ashley/lillian)",
        "(lillian/zoey)",
        "(lailani/sarah)",
        "(jessie/lailani)",
        "(brooke/jessie)",
        "(jessie/lola)",
        "(lola/zoey)",
        "(abia/jessie)",
        "(lailani/lillian)",
        "(abia/lillian)",
        "(sarah/zoey)",
        "(polly/zoey)",
        "(nora/sarah)",
        "(brooke/sarah)",
        "(candace/lailani)",
        "(abia/candace)",
        "(candace/polly)",
        "(ashley/nora)",
        "(ashley/brooke)",
        "(brooke/polly)"
    )
    girl_order = (
        "lola",
        "jessie",
        "lillian",
        "zoey",
        "sarah",
        "lailani",
        "candace",
        "nora",
        "brooke",
        "ashley",
        "abia",
        "polly"
    )

    girls_enabled = set()
    pairs_enabled = set()

    def generate_early(self):
        numpairs = self.options.number_of_starting_pairs.value
        numgirls = self.options.number_of_starting_girls.value

        self.startingpairs = []
        self.startinggirls = []

        self.gamedata = {}
        self.gamedata = randomise_stuff(self.random, self.options)

        self.girls_enabled = self.options.enabled_girls.value

        pair_girls = set()
        for p in default_pairs:
            if p[0] in self.options.enabled_girls.value and p[1] in self.options.enabled_girls.value:
                pair_girls.add((f"({p[0]}/{p[1]})", p[0], p[1]))

        for pair in pair_girls:
            self.pairs_enabled.add(pair[0])

        if len(pair_girls) < self.options.boss_wings_requirement.value:
            print(f"ENABLED PAIRS LESS THAN BOSS WING REQUIREMENT SETTING VALUE TO MATCH NUMBER OF PAIRS:{len(pair_girls)}")
            self.options.boss_wings_requirement.value = len(pair_girls)

        self.wingval = self.options.boss_wings_requirement.value

        if len(self.pairs_enabled) != 24:
            self.options.boss_wings_requirement.value = min(24, (self.options.boss_wings_requirement.value + (24 - len(self.pairs_enabled))))

        # get random number of pairs based on what's set in options
        temppairs = pair_girls.copy()
        tempgirl = []
        i = 1
        while i <= numpairs:
            pair = temppairs.pop()
            self.startingpairs.append(f"Pair Unlock {pair[0]}")
            tempgirl.append(pair[1])
            tempgirl.append(pair[2])
            i += 1

        # add all the girls required for the starting pairs
        y = 0
        for g in tempgirl:
            xstr = f"Unlock Girl({g})"
            if not xstr in self.startinggirls:
                self.startinggirls.append(xstr)
                y += 1

        # add more starting girls if needed
        if y < numgirls:
            girllist = self.girls_enabled.copy()
            while y < numgirls:
                girl = girllist.pop()
                gstr = f"Unlock Girl({girl})"
                if not gstr in self.startinggirls:
                    self.startinggirls.append(gstr)
                    y += 1

                if len(girllist) < 1:
                    break

        totallocations = 0
        totalitems = 0

        # get number of items that will in the itempool
        if not self.options.lovers_instead_wings.value:  # fairy wings
            totalitems += len(self.pairs_enabled)
        if True:  # tokenlvups
            totalitems += 32
        if True:  # girl unlocks
            totalitems += len(self.girls_enabled) - len(self.startinggirls)
        if True:  # pair unlocks
            totalitems += len(self.pairs_enabled) - len(self.startingpairs)
        if True:  # gift unique
            totalitems += (len(self.girls_enabled) * 4)
        if True:  # gift shoe
            totalitems += (len(self.girls_enabled) * 4)
        if not self.options.disable_baggage.value:  # baggagage
            totalitems += (len(self.girls_enabled) * 3)
        if not self.options.disable_outfits.value:
            totalitems += (len(self.girls_enabled) * 9)

        # get the number of location that will be in the starting pool
        if True:  # pair attracted/lovers
            totallocations += (len(self.pairs_enabled) * 2)
        if True:  # unique gift
            totallocations += (len(self.girls_enabled) * 4)
        if True:  # shoe gift
            totallocations += (len(self.girls_enabled) * 4)
        if self.options.enable_questions.value:  # favroute question
            totallocations += (len(self.girls_enabled) * 20)
        if self.options.number_shop_items.value > 0:  # shop locations
            totallocations += self.options.number_shop_items.value
        if not self.options.disable_outfits.value:
            totallocations += (len(self.girls_enabled) * 10)

        if totallocations != totalitems:
            if totallocations > totalitems:
                self.trashitems = totallocations - totalitems
                self.shopslots = self.options.number_shop_items.value
            else:
                self.shopslots = totalitems - (totallocations - self.options.number_shop_items.value)

        self.totall = totalitems + self.trashitems + 1
        self.totali = totalitems + self.trashitems + len(self.startinggirls) + len(self.startingpairs)
        self.options.number_shop_items.value = self.shopslots

    def create_regions(self):
        is_ut = getattr(self.multiworld, "generation_is_fake", False)

        hub_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(hub_region)

        boss_region = Region("Boss Region", self.player, self.multiworld)
        boss_region.add_locations({"Goal Check": None}, HP2Location)
        boss_region.add_locations({"Nymphojinn Battle": self.location_name_to_id["Nymphojinn Battle"]}, HP2Location)
        self.multiworld.get_location("Goal Check", self.player).place_locked_item(HP2Item(f"Boss Unlocked", ItemClassification.progression, None, self.player))
        hub_region.connect(boss_region, "hub-boss")

        # print(f"total shop slots:{self.shopslots}")
        if self.shopslots > 0:
            shop_region = Region("Shop Region", self.player, self.multiworld)
            hub_region.connect(shop_region, "hub-shop")
            for i in range(self.shopslots):
                # self.location_name_to_id[f"shop_location: {i+1}"] = 69420506+i
                shop_region.add_locations({f"shop_location: {i + 1}": shop_loc_start + i + 1}, HP2Location)

        for pair in self.pairs_enabled:
            pairregion = Region(f"{pair} Region", self.player, self.multiworld)
            pairregion.add_locations({
                f"Pair Attracted {pair}": self.location_name_to_id[f"Pair Attracted {pair}"],
                f"Pair Lovers {pair}": self.location_name_to_id[f"Pair Lovers {pair}"]
            }, HP2Location)
            hub_region.connect(pairregion, f"hub-pair{pair}")

        for girl in self.girls_enabled:
            girlregion = Region(f"{girl} Region", self.player, self.multiworld)
            if self.options.enable_questions:
                girlregion.add_locations({
                    f"Learn {girl}'s favourite drink": self.location_name_to_id[f"Learn {girl}'s favourite drink"],
                    f"Learn {girl}'s favourite Ice Cream Flavor": self.location_name_to_id[f"Learn {girl}'s favourite Ice Cream Flavor"],
                    f"Learn {girl}'s favourite Music Genre": self.location_name_to_id[f"Learn {girl}'s favourite Music Genre"],
                    f"Learn {girl}'s favourite Movie Genre": self.location_name_to_id[f"Learn {girl}'s favourite Movie Genre"],
                    f"Learn {girl}'s favourite Online Activity": self.location_name_to_id[f"Learn {girl}'s favourite Online Activity"],
                    f"Learn {girl}'s favourite Phone App": self.location_name_to_id[f"Learn {girl}'s favourite Phone App"],
                    f"Learn {girl}'s favourite Type Of Exercise": self.location_name_to_id[f"Learn {girl}'s favourite Type Of Exercise"],
                    f"Learn {girl}'s favourite Outdoor Activity": self.location_name_to_id[f"Learn {girl}'s favourite Outdoor Activity"],
                    f"Learn {girl}'s favourite Theme Park Ride": self.location_name_to_id[f"Learn {girl}'s favourite Theme Park Ride"],
                    f"Learn {girl}'s favourite Friday Night": self.location_name_to_id[f"Learn {girl}'s favourite Friday Night"],
                    f"Learn {girl}'s favourite Sunday Morning": self.location_name_to_id[f"Learn {girl}'s favourite Sunday Morning"],
                    f"Learn {girl}'s favourite Weather": self.location_name_to_id[f"Learn {girl}'s favourite Weather"],
                    f"Learn {girl}'s favourite Holiday": self.location_name_to_id[f"Learn {girl}'s favourite Holiday"],
                    f"Learn {girl}'s favourite Pet": self.location_name_to_id[f"Learn {girl}'s favourite Pet"],
                    f"Learn {girl}'s favourite School Subject": self.location_name_to_id[f"Learn {girl}'s favourite School Subject"],
                    f"Learn {girl}'s favourite Place to shop": self.location_name_to_id[f"Learn {girl}'s favourite Place to shop"],
                    f"Learn {girl}'s favourite Trait In Partner": self.location_name_to_id[f"Learn {girl}'s favourite Trait In Partner"],
                    f"Learn {girl}'s favourite Own Body Part": self.location_name_to_id[f"Learn {girl}'s favourite Own Body Part"],
                    f"Learn {girl}'s favourite Sex Position": self.location_name_to_id[f"Learn {girl}'s favourite Sex Position"],
                    f"Learn {girl}'s favourite Porn Category": self.location_name_to_id[f"Learn {girl}'s favourite Porn Category"]
                }, HP2Location)
            if not is_ut:
                girlregion.add_locations({
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique1"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique1"]]}"],
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique2"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique2"]]}"],
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique3"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique3"]]}"],
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique4"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique4"]]}"],

                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe1"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe1"]]}"],
                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe2"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe2"]]}"],
                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe3"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe3"]]}"],
                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe4"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe4"]]}"],
                }, HP2Location)

            if not self.options.disable_outfits.value:
                girlregion.add_locations({
                    f"Date {girl} in {girl_outfits[girl][0]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][0]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][1]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][1]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][2]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][2]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][3]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][3]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][4]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][4]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][5]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][5]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][6]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][6]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][7]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][7]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][8]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][8]} Outfit"],
                    f"Date {girl} in {girl_outfits[girl][9]} Outfit": self.location_name_to_id[f"Date {girl} in {girl_outfits[girl][9]} Outfit"],
                }, HP2Location)

            self.multiworld.regions.append(girlregion)
            hub_region.connect(girlregion, f"hub-{girl}")

    def create_item(self, name: str) -> HP2Item:
        if name == "Goal Achieved":
            return HP2Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        if name in girl_unlock_item or name in pair_unlock_item or name in gift_unique_item or name in gift_shoe_item or name in fairy_wings_item or name in outfits_item:
            # print(f"{name}: is progression")
            return HP2Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
        if name in token_item:
            # print(f"{name}: is useful")
            return HP2Item(name, ItemClassification.useful, self.item_name_to_id[name], self.player)
        # print(f"{name}: is none")
        return HP2Item(name, ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_items(self):
        for pair in self.pairs_enabled:
            if f"Pair Unlock {pair}" in self.startingpairs:
                self.multiworld.push_precollected(self.create_item(f"Pair Unlock {pair}"))
            else:
                self.multiworld.itempool.append(self.create_item(f"Pair Unlock {pair}"))

        for girl in self.girls_enabled:
            if f"Unlock Girl({girl})" in self.startinggirls:
                self.multiworld.push_precollected(self.create_item(f"Unlock Girl({girl})"))
            else:
                self.multiworld.itempool.append(self.create_item(f"Unlock Girl({girl})"))

            if not self.options.disable_baggage.value:
                self.multiworld.itempool.append(self.create_item(f"Found {girl}'s {baggageid_to_name[self.gamedata[girl]["baggage1"]]} Baggage"))
                self.multiworld.itempool.append(self.create_item(f"Found {girl}'s {baggageid_to_name[self.gamedata[girl]["baggage2"]]} Baggage"))
                self.multiworld.itempool.append(self.create_item(f"Found {girl}'s {baggageid_to_name[self.gamedata[girl]["baggage3"]]} Baggage"))

            self.multiworld.itempool.append(self.create_item(f"{shoeid_to_name[self.gamedata[girl]["shoe1"]]} Gift"))
            self.multiworld.itempool.append(self.create_item(f"{shoeid_to_name[self.gamedata[girl]["shoe2"]]} Gift"))
            self.multiworld.itempool.append(self.create_item(f"{shoeid_to_name[self.gamedata[girl]["shoe3"]]} Gift"))
            self.multiworld.itempool.append(self.create_item(f"{shoeid_to_name[self.gamedata[girl]["shoe4"]]} Gift"))

            self.multiworld.itempool.append(self.create_item(f"{uniqueid_to_name[self.gamedata[girl]["unique1"]]} Unique Gift"))
            self.multiworld.itempool.append(self.create_item(f"{uniqueid_to_name[self.gamedata[girl]["unique2"]]} Unique Gift"))
            self.multiworld.itempool.append(self.create_item(f"{uniqueid_to_name[self.gamedata[girl]["unique3"]]} Unique Gift"))
            self.multiworld.itempool.append(self.create_item(f"{uniqueid_to_name[self.gamedata[girl]["unique4"]]} Unique Gift"))

            if not self.options.disable_outfits.value:
                for outfit in girl_outfits[girl]:
                    if outfit is default_girl_outfit[girl]:
                        self.multiworld.push_precollected(self.create_item(f"{girl} {outfit} Outfit"))
                    else:
                        self.multiworld.itempool.append(self.create_item(f"{girl} {outfit} Outfit"))



        if not self.options.lovers_instead_wings.value:
            for pair in self.pairs_enabled:
                self.multiworld.itempool.append(self.create_item(f"Fairy Wings {pair}"))

        if True:
            for token in token_item:
                for i in range(token_item_amounts[token]):
                    self.multiworld.itempool.append(self.create_item(token))

        # if self.trashitems > 0:
        #    for i in range(self.trashitems):
        #        self.multiworld.itempool.append(self.create_item("nothing"))

        if self.trashitems > 0:
            for i in range(self.trashitems):
                if self.options.filler_item.value == 1:
                    self.multiworld.itempool.append(self.create_item("nothing"))
                elif self.options.filler_item.value == 2:
                    self.multiworld.itempool.append(self.create_item("Fruit Seeds"))
                elif self.options.filler_item.value == 3:
                    self.multiworld.itempool.append(self.create_item(self.random.choice(list(filler_item.keys()))))

    #something to stop warnings happening in console when running tests
    def get_filler_item_name(self) -> str:
        return self.random.choice(list(filler_item.keys()))

    def set_rules(self):

        self.multiworld.get_location("Nymphojinn Battle", self.player).place_locked_item(self.create_item("Goal Achieved"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal Achieved", self.player)

        set_rules(self.multiworld, self.player, self.girls_enabled, self.pairs_enabled, self.startingpairs, self.options.enable_questions.value, self.options.disable_outfits.value, self.gamedata)

        if self.shopslots > self.options.exclude_shop_items:
            for i in range(self.shopslots):
                if i >= self.options.exclude_shop_items:
                    self.multiworld.get_location(f"shop_location: {i + 1}", self.player).progress_type = LocationProgressType.EXCLUDED

        if self.options.lovers_instead_wings.value:
            boss = set()
            for pair in self.pairs_enabled:
                boss.add(f"Pair Unlock {pair}")
            for girl in self.girls_enabled:
                boss.add(f"Unlock Girl({girl})")
            set_rule(self.multiworld.get_location("Goal Check", self.player), lambda state: state.has_all(boss, self.player))
            set_rule(self.multiworld.get_location("Nymphojinn Battle", self.player), lambda state: state.has_all(boss, self.player))
        else:
            wings = set()
            for pair in self.pairs_enabled:
                wings.add(f"Fairy Wings {pair}")
            set_rule(self.multiworld.get_location("Goal Check", self.player), lambda state: state.has_from_list(wings, self.player, self.wingval))
            set_rule(self.multiworld.get_location("Nymphojinn Battle", self.player), lambda state: state.has_from_list(wings, self.player, self.wingval))

        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    # Method for making Universal Tracker work properly
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        self.gamedata = slot_data["gamedata"]

        for girl in girl_list:
            if slot_data[girl]:
                print(f"hello {girl}")
                grigion = self.multiworld.get_region(f"{girl} Region", self.player)
                print("hello")
                grigion.add_locations({
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique1"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique1"]]}"],
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique2"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique2"]]}"],
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique3"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique3"]]}"],
                    f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique4"]]}": self.location_name_to_id[f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique4"]]}"],

                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe1"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe1"]]}"],
                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe2"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe2"]]}"],
                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe3"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe3"]]}"],
                    f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe4"]]}": self.location_name_to_id[f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe4"]]}"],
                }, HP2Location)

                set_rule(self.multiworld.get_location(f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique1"]]}", self.player), lambda state, p=self.player, g=girl, i=uniqueid_to_name[self.gamedata[girl]["unique1"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", self.player))
                set_rule(self.multiworld.get_location(f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique2"]]}", self.player), lambda state, p=self.player, g=girl, i=uniqueid_to_name[self.gamedata[girl]["unique2"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", self.player))
                set_rule(self.multiworld.get_location(f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique3"]]}", self.player), lambda state, p=self.player, g=girl, i=uniqueid_to_name[self.gamedata[girl]["unique3"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", self.player))
                set_rule(self.multiworld.get_location(f"Gift {girl} {uniqueid_to_name[self.gamedata[girl]["unique4"]]}", self.player), lambda state, p=self.player, g=girl, i=uniqueid_to_name[self.gamedata[girl]["unique4"]]: girl_unlocked(state, p, g) and state.has(f"{i} Unique Gift", self.player))

                set_rule(self.multiworld.get_location(f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe1"]]}", self.player), lambda state, p=self.player, g=girl, i=shoeid_to_name[self.gamedata[girl]["shoe1"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", self.player))
                set_rule(self.multiworld.get_location(f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe2"]]}", self.player), lambda state, p=self.player, g=girl, i=shoeid_to_name[self.gamedata[girl]["shoe2"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", self.player))
                set_rule(self.multiworld.get_location(f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe3"]]}", self.player), lambda state, p=self.player, g=girl, i=shoeid_to_name[self.gamedata[girl]["shoe3"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", self.player))
                set_rule(self.multiworld.get_location(f"Gift {girl} {shoeid_to_name[self.gamedata[girl]["shoe4"]]}", self.player), lambda state, p=self.player, g=girl, i=shoeid_to_name[self.gamedata[girl]["shoe4"]]: girl_unlocked(state, p, g) and state.has(f"{i} Gift", self.player))




    def fill_slot_data(self) -> dict:
        returndict = {
            "number_blue_seed": self.options.number_blue_seed.value,
            "number_green_seed": self.options.number_green_seed.value,
            "number_orange_seed": self.options.number_orange_seed.value,
            "number_red_seed": self.options.number_red_seed.value,
            "number_shop_items": self.options.number_shop_items.value,
            "enable_questions": self.options.enable_questions.value,
            "disable_baggage": self.options.disable_baggage.value,
            "lovers_instead_wings": self.options.lovers_instead_wings.value,
            "affection_start": self.options.puzzle_goal_start.value,
            "affection_add": self.options.puzzle_goal_add.value,
            "boss_affection": self.options.puzzle_goal_boss.value,
            "start_moves": self.options.puzzle_moves.value,
            "hide_shop_item_details": self.options.hide_shop_item_details.value,
            "world_version": self.world_version,
            "outfit_date_complete": self.options.outfits_require_date_completion.value,
            "boss_wing_requirement": self.options.boss_wings_requirement.value,
            "player_gender": self.options.player_gender.value,
            "polly_gender": self.options.polly_gender.value,
            "game_difficulty": self.options.game_difficulty.value,
            "total_items": self.totali,
            "total_locations": self.totall,

            "startgirls": self.startinggirls,
            "startpairs": self.startingpairs,


            "lola": "lola" in self.girls_enabled,
            "jessie": "jessie" in self.girls_enabled,
            "lillian": "lillian" in self.girls_enabled,
            "zoey": "zoey" in self.girls_enabled,
            "sarah": "sarah" in self.girls_enabled,
            "lailani": "lailani" in self.girls_enabled,
            "candace": "candace" in self.girls_enabled,
            "nora": "nora" in self.girls_enabled,
            "brooke": "brooke" in self.girls_enabled,
            "ashley": "ashley" in self.girls_enabled,
            "abia": "abia" in self.girls_enabled,
            "polly": "polly" in self.girls_enabled,

            **item_datapackage,
            **loc_datapackage,

            "gamedata": self.gamedata,
            "pairs_enabled": self.pairs_enabled,
        }

        return returndict
