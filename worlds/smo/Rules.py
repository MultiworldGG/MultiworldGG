from worlds.generic.Rules import set_rule
from .Options import SMOOptions
from .Logic import total_moons, count_moons


def set_rules(self, options : SMOOptions) -> None:
    """ Sets the placement rules for Super Mario Odyssey.
        Args:
            self: SMOWorld object for this player's world.
            options: The options from this player's yaml.
    """

    # Prevents a softlock in Bowser from not having this moon in the moon list
    #self.multiworld.get_location("Big Broodal Battle" , self.player).place_locked_item(self.create_item("Bowser's Story Moon"))


    # Cascade Story Progress
    # set_rule(self.multiworld.get_location("Multi Moon Atop the Falls", self.player), lambda state: state.has("Cascade Story Moon", self.player))

    # if options.goal >= 4:
    #     # Sand Story Progress
    #     set_rule(self.multiworld.get_location("Moon Shards in the Sand", self.player), lambda state: state.has("Sand Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Showdown on the Inverted Pyramid", self.player), lambda state: state.has("Sand Story Moon", self.player))
    #
    # if options.goal > 5:
    #     # Wooded Story Progress
    #     set_rule(self.multiworld.get_location("Flower Thieves of Sky Garden", self.player), lambda state: state.has("Wooded Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Path to the Secret Flower Field", self.player), lambda state: state.count("Wooded Story Moon", self.player) >= 1)
    #     set_rule(self.multiworld.get_location("Defend the Secret Flower Field!", self.player), lambda state: state.count("Wooded Story Moon", self.player) >= 2)
    #
    # if options.goal >= 9:
    #     # Metro Story Progress
    #     set_rule(self.multiworld.get_location("Powering Up the Station", self.player), lambda state: state.count("Metro Story Moon", self.player) >= 4)
    #     set_rule(self.multiworld.get_location("A Traditional Festival!", self.player), lambda state: state.count("Metro Story Moon", self.player) >= 5)
    #
    # if options.goal >= 12:
    #     # Seaside Story Progress
    #     # set_rule(self.multiworld.get_location("The Glass Is Half Full!", self.player), lambda state: state.has("Seaside Story Moon", self.player) and
    #     #     state.has("Seaside Story Moon", self.player) and state.has("Seaside Story Moon", self.player) and state.has("Seaside Story Moon", self.player))
    #     #
    #     # # Snow Story Progress
    #     # set_rule(self.multiworld.get_location("The Bound Bowl Grand Prix", self.player), lambda state: state.has("Snow Story Moon", self.player) and
    #     #     state.has("Snow Story Moon", self.player) and state.has("Snow Story Moon", self.player) and state.has("Snow Story Moon", self.player))
    #
    #     # Luncheon Story Progress
    #     set_rule(self.multiworld.get_location("Under the Cheese Rocks", self.player), lambda state: state.has("Luncheon Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Big Pot on the Volcano: Dive In!", self.player), lambda state: state.count("Luncheon Story Moon", self.player) >= 2)
    #     set_rule(self.multiworld.get_location("Cookatiel Showdown!", self.player), lambda state: state.count("Luncheon Story Moon", self.player) >= 3)
    #
    # if options.goal >= 15:
    #     # Bowser Story Progress
    #     set_rule(self.multiworld.get_location("Smart Bombing", self.player), lambda state: state.has("Bowser Story Moon", self.player))
    #     set_rule(self.multiworld.get_location("Big Broodal Battle", self.player), lambda state: state.count("Bowser Story Moon", self.player) >= 2)
    #     set_rule(self.multiworld.get_location("Showdown at Bowser's Castle", self.player), lambda state: state.count("Bowser Story Moon", self.player) >= 3)


    # Outfit Moons
    if self.options.goal > self.options.goal.option_lake:
        set_rule(self.multiworld.get_location("Mechanic Cap", self.player),
                 lambda state: state.has("Mechanic Cap", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))
        set_rule(self.multiworld.get_location("Mechanic Outfit", self.player),
                 lambda state: state.has("Mechanic Outfit", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))
        set_rule(self.multiworld.get_location("Fashionable Cap", self.player),
                 lambda state: state.has("Fashionable Cap", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))
        set_rule(self.multiworld.get_location("Fashionable Outfit", self.player),
                 lambda state: state.has("Fashionable Outfit", self.player) or
                (count_moons(self, state, "Lake", self.player) >= self.moon_counts["lake"] and
                count_moons(self, state, "Wooded", self.player) >= self.moon_counts["wooded"]))

    if self.options.goal > self.options.goal.option_metro:
        set_rule(self.multiworld.get_location("Pirate Hat", self.player),
             lambda state: state.has("Pirate Hat", self.player) or
            (count_moons(self, state, "Seaside", self.player) >= self.moon_counts["seaside"] and
            count_moons(self, state, "Snow", self.player) >= self.moon_counts["snow"]))
        set_rule(self.multiworld.get_location("Pirate Outfit", self.player),
                 lambda state: state.has("Pirate Outfit", self.player) or
                (count_moons(self, state, "Seaside", self.player) >= self.moon_counts["seaside"] and
                count_moons(self, state, "Snow", self.player) >= self.moon_counts["snow"]))
        # set_rule(self.multiworld.get_location("Clown Hat", self.player),
        #          lambda state: state.has("Clown Hat", self.player) or
        #         (count_moons(self, state, "Snow", self.player) and
        #         count_moons(self, state, "", self.player)))
        # set_rule(self.multiworld.get_location("Clown Suit", self.player),
        #          lambda state: state.has("Clown Suit", self.player) or
        #         (count_moons(self, state, "", self.player) and
        #         count_moons(self, state, "", self.player)))
        # set_rule(self.multiworld.get_location("", self.player),
        #          lambda state: state.has("", self.player) or
        #         (count_moons(self, state, "", self.player) and
        #         count_moons(self, state, "", self.player)))


    if self.options.goal > self.options.goal.option_moon:
        set_rule(self.multiworld.get_location("Cascade Kingdom - Caveman Cave-Fan", self.player),
                 lambda state: state.has("Caveman Headwear", self.player) and state.has("Caveman Outfit", self.player))
        set_rule(self.multiworld.get_location("Lake Kingdom - That Trendy “Pirate” Look", self.player),
                 lambda state: state.has("Pirate Hat", self.player) and state.has("Pirate Outfit", self.player))
        set_rule(self.multiworld.get_location("Lake Kingdom - Space Is “In” Right Now", self.player),
                 lambda state: state.has("Space Helmet", self.player) and state.has("Space Suit", self.player))
        set_rule(self.multiworld.get_location("Lake Kingdom - That “Old West” Style", self.player),
                 lambda state: state.has("Cowboy Hat", self.player) and state.has("Cowboy Outfit", self.player))
        set_rule(self.multiworld.get_location("Luncheon Kingdom - Mechanic: Repairs Complete!", self.player),
                 lambda state: state.has("Mechanic Cap", self.player) and state.has("Mechanic Outfit", self.player))
        set_rule(self.multiworld.get_location("Moon Kingdom - Doctor in the House", self.player),
                 lambda state: state.has("Doctor Headwear", self.player) and state.has("Doctor Outfit", self.player))
        set_rule(self.multiworld.get_location("Mushroom Kingdom - Totally Classic", self.player),
                 lambda state: (state.has("Mario 64 Cap", self.player) and state.has("Mario 64 Suit", self.player)) or (
                             state.has("Metal Mario Cap", self.player) and state.has("Metal Mario Clothes", self.player)))
        set_rule(self.multiworld.get_location("Mushroom Kingdom - Courtyard Chest Trap", self.player),
                 lambda state: (state.has("Mario 64 Cap", self.player) and state.has("Mario 64 Suit", self.player)) or (
                             state.has("Metal Mario Cap", self.player) and state.has("Metal Mario Clothes", self.player)))
        set_rule(self.multiworld.get_location("Metro Kingdom - Surprise Clown!", self.player),
                 lambda state: state.has("Clown Hat", self.player) and state.has("Clown Suit", self.player))

    # if options.goal > 15 or (options.shops != 0 and options.shops != 3):
    set_rule(self.multiworld.get_location("Sand Kingdom - Dancing with New Friends", self.player), lambda state: (state.has("Sombrero", self.player) and state.has("Poncho", self.player)) or state.has("Skeleton Suit", self.player))
    if self.options.goal > self.options.goal.option_lake:
        set_rule(self.multiworld.get_location("Lake Kingdom - I Feel Underdressed", self.player), lambda state: (state.has(
            "Swim Goggles", self.player) and state.has("Swimwear", self.player)) or state.has("Boxer Shorts",
                                                                                                      self.player))
        set_rule(self.multiworld.get_location("Wooded Kingdom - Exploring for Treasure", self.player),
                 lambda state: state.has("Explorer Hat", self.player) and state.has("Explorer Outfit", self.player))


    if self.options.goal > self.options.goal.option_metro:
        set_rule(self.multiworld.get_location("Metro Kingdom - Rewiring the Neighborhood", self.player),
                 lambda state: state.has("Builder Helmet", self.player) and state.has("Builder Outfit", self.player))
        set_rule(self.multiworld.get_location("Seaside Kingdom - A Relaxing Dance", self.player),
                 lambda state: state.has("Resort Hat", self.player) and state.has("Resort Outfit", self.player))
        set_rule(self.multiworld.get_location("Snow Kingdom - Moon Shards in the Cold Room", self.player),
                 lambda state: state.has("Snow Hood", self.player) and state.has("Snow Suit", self.player))
        set_rule(self.multiworld.get_location("Snow Kingdom - Slip Behind the Ice", self.player),
                 lambda state: state.has("Snow Hood", self.player) and state.has("Snow Suit", self.player))
        set_rule(self.multiworld.get_location("Snow Kingdom - I'm Not Cold!", self.player),
                 lambda state: state.has("Boxer Shorts", self.player))

    if self.options.goal > self.options.goal.option_metro:
        set_rule(self.multiworld.get_location("Luncheon Kingdom - A Strong Simmer", self.player),
                 lambda state: state.has("Chef Hat", self.player) and state.has("Chef Suit", self.player))
        set_rule(self.multiworld.get_location("Luncheon Kingdom - An Extreme Simmer", self.player),
                 lambda state: state.has("Chef Hat", self.player) and state.has("Chef Suit", self.player))

    if self.options.goal > self.options.goal.option_luncheon:
        set_rule(self.multiworld.get_location("Bowser Kingdom - Scene of Crossing the Poison Swamp", self.player),
                 lambda state: state.has("Samurai Helmet", self.player) and state.has("Samurai Armor", self.player))
        set_rule(self.multiworld.get_location("Bowser Kingdom - Taking Notes: In the Folding Screen", self.player),
                 lambda state: state.has("Samurai Helmet", self.player) and state.has("Samurai Armor", self.player))

    # Post Game Outfits
    if self.options.goal > self.options.goal.option_moon:
        for outfit in self.outfit_moon_counts.keys():
            if self.options.goal > self.options.goal.option_dark:
                if self.outfit_moon_counts[outfit] < self.moon_counts["dark"]:
                    set_rule(self.multiworld.get_location(outfit, self.player),
                         lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
                             outfit] or state.has(outfit, self.player))
            elif self.options.goal > self.options.goal.option_darker:
                if self.outfit_moon_counts[outfit] < self.moon_counts["darker"]:
                    set_rule(self.multiworld.get_location(outfit, self.player),
                             lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
                                 outfit] or state.has(outfit, self.player))

        # set_rule(self.multiworld.get_location("Luigi Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Luigi Cap"] or state.has("Luigi Cap", self.player))
        # set_rule(self.multiworld.get_location("Luigi Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Luigi Suit"] or state.has("Luigi Suit", self.player))
        # set_rule(self.multiworld.get_location("Doctor Headwear", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Doctor Headwear"] or state.has("Doctor Headwear", self.player))
        # set_rule(self.multiworld.get_location("Doctor Outfit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Doctor Outfit"] or state.has("Doctor Outfit", self.player))
        # set_rule(self.multiworld.get_location("Waluigi Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Waluigi Cap"] or state.has("Waluigi Cap", self.player))
        # set_rule(self.multiworld.get_location("Waluigi Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Waluigi Suit"] or state.has("Waluigi Suit", self.player))
        # set_rule(self.multiworld.get_location("Diddy Kong Hat", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Diddy Kong Hat"] or state.has("Diddy Kong Hat", self.player))
        # set_rule(self.multiworld.get_location("Diddy Kong Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Diddy Kong Suit"] or state.has("Diddy Kong Suit", self.player))
        # set_rule(self.multiworld.get_location("Wario Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Wario Cap"] or state.has("Wario Cap", self.player))
        # set_rule(self.multiworld.get_location("Wario Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Wario Suit"] or state.has("Wario Suit", self.player))
        # set_rule(self.multiworld.get_location("Hakama", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Hakama"] or state.has("Hakama", self.player))
        # set_rule(self.multiworld.get_location("Bowser's Top Hat", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bowser's Top Hat"] or state.has("Bowser's Top Hat", self.player))
        # set_rule(self.multiworld.get_location("Bowser's Tuxedo", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bowser's Tuxedo"] or state.has("Bowser's Tuxedo", self.player))
        # set_rule(self.multiworld.get_location("Bridal Veil", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bridal Veil"] or state.has("Bridal Veil", self.player))
        # set_rule(self.multiworld.get_location("Bridal Gown", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Bridal Gown"] or state.has("Bridal Gown", self.player))
        # set_rule(self.multiworld.get_location("Gold Mario Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Gold Mario Cap"] or state.has("Gold Mario Cap", self.player))
        # set_rule(self.multiworld.get_location("Gold Mario Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Gold Mario Suit"] or state.has("Gold Mario Suit", self.player))
        # set_rule(self.multiworld.get_location("Metal Mario Cap", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Metal Mario Cap"] or state.has("Metal Mario Cap", self.player))
        # set_rule(self.multiworld.get_location("Metal Mario Suit", self.player),
        #          lambda state: total_moons(self, state, self.player) >= self.outfit_moon_counts[
        #              "Metal Mario Suit"] or state.has("Metal Mario Suit", self.player))

    # # Completion State
    # if options.goal == "sand":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.count("Sand Multi-Moon", self.player) >= 2
    # if options.goal == "lake":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Lake Multi-Moon", self.player)
    # if options.goal == "metro":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.count("Metro Multi-Moon", self.player) >= 2
    # if options.goal == "luncheon":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.count("Luncheon Multi-Moon", self.player) >= 2
    # if options.goal == "moon":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Beat the Game", self.player)
    #     self.multiworld.get_location("Beat the Game", self.player).place_locked_item(self.create_item("Beat the Game"))
    # if options.goal == "dark":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Dark Side Multi-Moon", self.player)
    # if options.goal == "darker":
    #     self.multiworld.completion_condition[self.player] = lambda state: state.has("Darker Side Multi-Moon", self.player)

    # Place Goal moon at location
    if options.goal == "sand":
        self.multiworld.get_location("Sand Kingdom - The Hole in the Desert", self.player).place_locked_item(
            self.create_item("Sand Multi-Moon"))
    if options.goal == "lake":
        self.multiworld.get_location("Lake Kingdom - Broodals Over the Lake", self.player).place_locked_item(
            self.create_item("Lake Multi-Moon"))
    if options.goal == "metro":
        self.multiworld.get_location("Metro Kingdom - A Traditional Festival!", self.player).place_locked_item(
            self.create_item("Metro Multi-Moon"))
    if options.goal == "luncheon":
        self.multiworld.get_location("Luncheon Kingdom - Cookatiel Showdown!", self.player).place_locked_item(
            self.create_item("Luncheon Multi-Moon"))
    if options.goal == "dark":
        self.multiworld.get_location("Dark Side - Arrival at Rabbit Ridge!", self.player).place_locked_item(
            self.create_item("Dark Side Multi-Moon"))
    if options.goal == "darker":
        self.multiworld.get_location("Darker Side - A Long Journey's End!", self.player).place_locked_item(self.create_item("Darker Side Multi-Moon"))


    # Captures
    if options.capture_sanity.value == options.capture_sanity.option_true:
        # Cascade Story
        set_rule(self.multiworld.get_location("Cascade Kingdom - Our First Power Moon", self.player),
                 lambda state: state.has("Chain Chomp", self.player))
        set_rule(self.multiworld.get_location("Cascade Kingdom - Multi Moon Atop the Falls", self.player),
                 lambda state: (state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player)) and state.has(
            "Broode's Chain Chomp", self.player))
        set_rule(self.multiworld.get_location("Broode's Chain Chomp", self.player),
                 lambda state: state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player))
        #set_rule(self.multiworld.get_location("Our First Power Moon", self.player),
        #         lambda state: state.has("Chain Chomp", self.player) or state.has("T-Rex", self.player))
        #set_rule(self.multiworld.get_location("Multi Moon Atop the Falls", self.player),
        #         lambda state: state.has("Broode's Chain Chomp", self.player))
        # Sand Story
        set_rule(self.multiworld.get_location("Sand Kingdom - The Hole in the Desert", self.player),
                 lambda state: state.has("Bullet Bill", self.player) and state.has("Knucklotec's Fist", self.player))

        if self.options.goal > self.options.goal.option_lake:
            # Wooded Story
            set_rule(self.multiworld.get_location("Wooded Kingdom - Path to the Secret Flower Field", self.player),
                     lambda state: state.has("Sherm", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Defend the Secret Flower Field!", self.player),
                     lambda state: state.has("Uproot", self.player) and state.has("Sherm", self.player))

        if self.options.goal > self.options.goal.option_lake:
            # Metro Story
            set_rule(self.multiworld.get_location("Metro Kingdom - New Donk City's Pest Problem", self.player),
                     lambda state: state.has("Sherm", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Powering Up the Station", self.player),
                     lambda state: state.has("Manhole", self.player))

        if self.options.goal > self.options.goal.option_metro:
            # Seaside Story
            set_rule(self.multiworld.get_location("Seaside Kingdom - The Hot Spring Seal", self.player),
                     lambda state: state.has("Gushen", self.player))
            set_rule(self.multiworld.get_location("Seaside Kingdom - The Glass Is Half Full!", self.player),
                     lambda state: state.has("Gushen", self.player))
            # Snow Story
            set_rule(self.multiworld.get_location("Snow Kingdom - The Bound Bowl Grand Prix", self.player),
                     lambda state: state.has("Shiverian Racer", self.player))
            # Luncheon Story
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Under the Cheese Rocks", self.player),
                     lambda state: state.has("Hammer Bro", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Climb Up the Cascading Magma", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Big Pot on the Volcano: Dive In!", self.player),
                     lambda state: state.has("Meat", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Cookatiel Showdown!", self.player),
                     lambda state: state.has("Lava Bubble", self.player))

        if self.options.goal > self.options.goal.option_luncheon:
            # Ruined Story
            set_rule(self.multiworld.get_location("Ruined Kingdom - Battle with the Lord of Lightning!", self.player),
                     lambda state: state.has("Spark Pylon", self.player))
            # Bowser Story
            set_rule(self.multiworld.get_location("Bowser Kingdom - Infiltrate Bowser's Castle!", self.player),
                     lambda state: state.has("Spark Pylon", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Smart Bombing", self.player),
                     lambda state: state.has("Pokio", self.player))
            # Moon Story
            set_rule(self.multiworld.get_location("Beat the Game", self.player),
                     lambda state: state.has("Bowser", self.player))

        # Cap
        set_rule(self.multiworld.get_location("Cap Kingdom - Frog-jumping above the Fog", self.player),
                 lambda state: state.has("Frog", self.player))
        set_rule(self.multiworld.get_location("Cap Kingdom - Frog-jumping from the Top Deck", self.player),
                 lambda state: state.has("Frog", self.player))
        set_rule(self.multiworld.get_location("Cap Kingdom - Skimming the Poison Tide", self.player),
                 lambda state: state.has("Paragoomba", self.player))
        set_rule(self.multiworld.get_location("Cap Kingdom - Slipping through the Poison Tide", self.player),
                 lambda state: state.has("Paragoomba", self.player))
        set_rule(self.multiworld.get_location("Cap Kingdom - Push-Block Peril", self.player),
                 lambda state: state.has("Spark Pylon", self.player))
        set_rule(self.multiworld.get_location("Cap Kingdom - Hidden Among the Push-Blocks", self.player),
                 lambda state: state.has("Spark Pylon", self.player))
        set_rule(self.multiworld.get_location("Bonneton Tower Model", self.player),
                 lambda state: state.has("Spark Pylon", self.player) and state.has("Paragoomba" , self.player))

        # Cascade
        set_rule(self.multiworld.get_location("Cascade Kingdom - Chomp Through the Rocks", self.player),
                 lambda state: state.has("Chain Chomp", self.player))
        set_rule(self.multiworld.get_location("Cascade Kingdom - Dinosaur Nest: Running Wild!", self.player),
                 lambda state: state.has("T-Rex", self.player))
        set_rule(self.multiworld.get_location("Cascade Kingdom - Nice Shot with the Chain Chomp!", self.player),
                 lambda state: state.has("Chain Chomp", self.player))
        set_rule(self.multiworld.get_location("Cascade Kingdom - Very Nice Shot with the Chain Chomp!", self.player),
                 lambda state: state.has("Chain Chomp", self.player))
        set_rule(self.multiworld.get_location("Cascade Kingdom - Behind the Waterfall", self.player),
                 lambda state: state.has("Big Chain Chomp", self.player) or state.has("T-Rex", self.player))

        # Sand
        set_rule(self.multiworld.get_location("Sand Kingdom - Wandering Cactus", self.player),
                 lambda state: state.has("Cactus", self.player))
        set_rule(self.multiworld.get_location("Sand Kingdom - Underground Treasure Chest", self.player),
                 lambda state: state.has("Bullet Bill", self.player))
        set_rule(self.multiworld.get_location("Sand Kingdom - Fishing in the Oasis", self.player),
                 lambda state: state.has("Lakitu", self.player))
        set_rule(self.multiworld.get_location("Sand Kingdom - Love in the Heart of the Desert", self.player),
                 lambda state: state.has("Goomba", self.player))
        set_rule(self.multiworld.get_location("Sand Kingdom - You're Quite a Catch, Captain Toad!", self.player),
                 lambda state: state.has("Lakitu", self.player))
        set_rule(self.multiworld.get_location("Sand Kingdom - On the Lone Pillar", self.player),
                 lambda state: state.has("Bullet Bill", self.player))

        # Change when entrance rando implemented
        set_rule(self.multiworld.get_location("Sand Kingdom - Strange Neighborhood", self.player),
                 lambda state: state.has("Mini Rocket", self.player))
        set_rule(self.multiworld.get_location("Sand Kingdom - Above a Strange Neighborhood", self.player),
                 lambda state: state.has("Mini Rocket", self.player))
        set_rule(self.multiworld.get_location("Inverted Pyramid Model", self.player),
                 lambda state: state.has("Mini Rocket", self.player) and state.has("Bullet Bill", self.player) and state.has("Knucklotec's Fist", self.player))

        if self.options.goal > self.options.goal.option_lake:
            # Wooded
            set_rule(self.multiworld.get_location("Wooded Kingdom - By the Babbling Brook in the Deep Woods", self.player),
                     lambda state: state.has("Coin Coffer", self.player) or state.has("T-Rex", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - The Hard Rock in Deep Woods", self.player),
                     lambda state: state.has("Coin Coffer", self.player) or state.has("T-Rex", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - A Treasure Made of Coins", self.player),
                     lambda state: state.has("Coin Coffer", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Beneath the Roots of a Moving Tree", self.player),
                     lambda state: state.has("Tree", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Love in the Forest Ruins", self.player),
                     lambda state: state.has("Goomba", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Elevator Blind Spot", self.player),
                     lambda state: state.has("Sherm", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Inside the Rock in the Forest", self.player),
                     lambda state: state.has("Coin Coffer", self.player) or state.has("Sherm", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Stretching Your Legs", self.player),
                     lambda state: state.has("Uproot", self.player))
            # Add vine sub area uproot req if trick jump not possible
            # Change when entrance rando implemented
            set_rule(self.multiworld.get_location("Wooded Kingdom - Wandering in the Fog", self.player),
                     lambda state: state.has("Paragoomba", self.player) and state.has("Mini Rocket", self.player))
            set_rule(self.multiworld.get_location("Wooded Kingdom - Nut Hidden in the Fog", self.player),
                     lambda state: state.has("Mini Rocket", self.player))
            set_rule(self.multiworld.get_location("Steam Gardener Watering Can", self.player),
                     lambda state: state.has("Boulder", self.player))

            # Lake
            set_rule(self.multiworld.get_location("Lake Kingdom - End of the Hidden Passage", self.player),
                     lambda state: state.has("Zipper", self.player))
            set_rule(self.multiworld.get_location("Lake Kingdom - Lake Fishing", self.player),
                     lambda state: state.has("Lakitu", self.player))
            set_rule(self.multiworld.get_location("Lake Kingdom - I Met a Lake Cheep Cheep!", self.player),
                     lambda state: state.has("Cheep Cheep", self.player))
            set_rule(self.multiworld.get_location("Lake Kingdom - A Successful Repair Job", self.player),
                     lambda state: state.has("Puzzle Part (Lake Kingdom)", self.player))
            # Change when entrance rando implemented
            set_rule(self.multiworld.get_location("Lake Kingdom - Unzip the Chasm", self.player),
                     lambda state: state.has("Zipper", self.player))
            set_rule(self.multiworld.get_location("Lake Kingdom - Super-Secret Zipper", self.player),
                     lambda state: state.has("Zipper", self.player))
            set_rule(self.multiworld.get_location("Underwater Dome", self.player),
                     lambda state: state.has("Zipper", self.player))


        if self.options.goal > self.options.goal.option_lake:
            # Cloud
            set_rule(self.multiworld.get_location("Cloud Kingdom - Picture Match: Basically a Goomba", self.player),
                     lambda state: state.has("Picture Match Part (Goomba)", self.player))

            # Lost
            set_rule(self.multiworld.get_location("Lost Kingdom - Soaring Over the Forgotten Isle!", self.player),
                     lambda state: state.has("Glydon", self.player))
            set_rule(self.multiworld.get_location("Lost Kingdom - Twist ‘n' Turn-Up Treasure", self.player),
                     lambda state: state.has("Tropical Wiggler", self.player))

            # Metro
            set_rule(self.multiworld.get_location("Metro Kingdom - Remotely Captured Car", self.player),
                     lambda state: state.has("RC Car", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - RC Car Pro!", self.player),
                     lambda state: state.has("RC Car", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Rewiring the Neighborhood", self.player),
                     lambda state: state.has("Spark Pylon", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Off the Beaten Wire", self.player),
                     lambda state: state.has("Spark Pylon", self.player))
            # Change when entrance rando implemented
            set_rule(self.multiworld.get_location("Metro Kingdom - Moon Shards Under Siege", self.player),
                     lambda state: state.has("Taxi", self.player) and state.has("Sherm", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Sharpshooting Under Siege", self.player),
                     lambda state: state.has("Taxi", self.player) and state.has("Sherm", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Inside the Rotating Maze", self.player),
                     lambda state: state.has("Manhole", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Outside the Rotating Maze", self.player),
                     lambda state: state.has("Manhole", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Vaulting Up a High-Rise", self.player),
                     lambda state: state.has("Mini Rocket", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Hanging from a High-Rise", self.player),
                     lambda state: state.has("Mini Rocket", self.player))
            set_rule(self.multiworld.get_location("Metro Kingdom - Sewer Treasure", self.player),
                     lambda state: state.has("Manhole", self.player))
            set_rule(self.multiworld.get_location("Pauline Statue", self.player),
                     lambda state: state.has("Manhole", self.player) and state.has("Mini Rocket", self.player))

        if self.options.goal > self.options.goal.option_metro:
            # Seaside
            set_rule(self.multiworld.get_location("Seaside Kingdom - Love by the Seaside", self.player),
                     lambda state: state.has("Goomba", self.player))
            set_rule(self.multiworld.get_location("Seaside Kingdom - Fly Through the Narrow Valley", self.player),
                     lambda state: state.has("Gushen", self.player))
            set_rule(self.multiworld.get_location("Seaside Kingdom - Treasure Chest in the Narrow Valley", self.player),
                     lambda state: state.has("Gushen", self.player))
            set_rule(self.multiworld.get_location("Seaside Kingdom - Lighthouse Leaper", self.player),
                     lambda state: state.has("Glydon", self.player))
            set_rule(self.multiworld.get_location("Sand Jar", self.player),
                     lambda state: state.has("Gushen", self.player))
            # Change when entrance rando implemented
            set_rule(self.multiworld.get_location("Seaside Kingdom - Wading in the Cloud Sea", self.player),
                     lambda state: state.has("Mini Rocket", self.player))
            set_rule(self.multiworld.get_location("Seaside Kingdom - Sunken Treasure in the Cloud Sea", self.player),
                     lambda state: state.has("Mini Rocket", self.player))

            # Snow
            set_rule(self.multiworld.get_location("Snow Kingdom - Ice-Dodging Goomba Stack", self.player),
                     lambda state: state.has("Goomba", self.player))
            set_rule(self.multiworld.get_location("Snow Kingdom - Fishing in the Glacier!", self.player),
                     lambda state: state.has("Lakitu", self.player))
            set_rule(self.multiworld.get_location("Snow Kingdom - Snowline Circuit Class S", self.player),
                     lambda state: state.has("Shiverian Racer", self.player))
            set_rule(self.multiworld.get_location("Shiverian Nesting Dolls", self.player),
                     lambda state: state.has("Ty-foo", self.player))
            # Change when entrance rando implemented
            set_rule(self.multiworld.get_location("Snow Kingdom - Blowing and Sliding", self.player),
                     lambda state: state.has("Ty-foo", self.player))

            # Luncheon
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Love Above the Lava", self.player),
                     lambda state: state.has("Goomba", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - A Strong Simmer", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - An Extreme Simmer", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Excavate ‘n' Search the Cheese Rocks", self.player),
                     lambda state: state.has("Hammer Bro", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Climb the Cheese Rocks", self.player),
                     lambda state: state.has("Hammer Bro", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Light the Lantern on the Small Island", self.player),
                     lambda state: state.has("Fire Bro", self.player) or state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - All the Cracks Are Fixed", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Taking Notes: Swimming in Magma", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Magma Narrow Path", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Crossing to the Magma", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Treasure Beneath the Cheese Rocks", self.player),
                     lambda state: state.has("Hammer Bro", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Alcove Behind the Pillars of Magma", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Beneath the Rolling Vegetables", self.player),
                     lambda state: state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Golden Turnip Recipe 3", self.player),
                     lambda state: state.has("Hammer Bro", self.player))
            set_rule(self.multiworld.get_location("Souvenir Forks", self.player),
                     lambda state: state.has("Hammer Bro", self.player) and state.has("Lava Bubble", self.player))
            set_rule(self.multiworld.get_location("Vegetable Plate", self.player),
                     lambda state: state.has("Hammer Bro", self.player) and state.has("Lava Bubble", self.player))
            # Change when entrance rando implemented
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Fork Flickin' to the Summit", self.player),
                     lambda state: state.has("Volbonan", self.player))
            set_rule(self.multiworld.get_location("Luncheon Kingdom - Fork Flickin' Detour", self.player),
                     lambda state: state.has("Volbonan", self.player))

        if self.options.goal > self.options.goal.option_luncheon:
            # Bowser
            set_rule(self.multiworld.get_location("Bowser Kingdom - Stack up above the wall", self.player),
                     lambda state: state.has("Goomba", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Poking Your Nose in the Plaster Wall", self.player),
                     lambda state: state.has("Pokio", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Poking the Turret Wall", self.player),
                     lambda state: state.has("Pokio", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Jizo All in a Row", self.player),
                     lambda state: state.has("Jizo", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Underground Jizo", self.player),
                     lambda state: state.has("Jizo", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Fishing(?) in Bowser's Castle", self.player),
                     lambda state: state.has("Lakitu", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Jizo's Big Adventure", self.player),
                     lambda state: state.has("Jizo", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Jizo and the Hidden Room", self.player),
                     lambda state: state.has("Jizo", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Behind the Big Wall", self.player),
                     lambda state: state.has("Spark Pylon", self.player))
            set_rule(self.multiworld.get_location("Bowser Kingdom - Taking notes: Between spinies", self.player),
                     lambda state: state.has("Spark Pylon", self.player))

            # Moon
            #if self.options.goal > self.options.goal.option_moon:
            set_rule(self.multiworld.get_location("Moon Kingdom - Under the Bowser Statue", self.player),
                    lambda state: state.has("Bowser statue", self.player))
            set_rule(self.multiworld.get_location("Moon Kingdom - In a Hole in the Magma", self.player),
                     lambda state: state.has("Parabones", self.player))
            set_rule(self.multiworld.get_location("Moon Kingdom - Around the Barrier Wall", self.player),
                     lambda state: state.has("Banzai Bill", self.player))
            set_rule(self.multiworld.get_location("Moon Kingdom - Fly to the Treasure Chest and Back", self.player),
                 lambda state: state.has("Banzai Bill", self.player))


# for debugging purposes, you may want to visualize the layout of your world. Uncomment the following code to
# write a PlantUML diagram to the file "my_world.puml" that can help you see whether your regions and locations
# are connected and placed as desired
#     from Utils import visualize_regions
#     visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
