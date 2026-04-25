from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L4(D3DLevel):
    name = "Babe Land"
    levelnum = 3
    volumenum = 3
    keys = ["Red", "Blue"]
    location_defs = [
        {"id": 6, "name": "Red Boat RPG", "type": "sprite", "density": 0},
        {"id": 9, "name": "Red Boat Chaingun", "type": "sprite", "density": 3},
        {
            "id": 19,
            "name": "Red Auction Protective Boots",
            "type": "sprite",
            "density": 3,
        },
        {"id": 56, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 101, "name": "Red Upper 2 Pipebombs", "type": "sprite", "density": 0},
        {
            "id": 184,
            "name": "MP Boat Top Protective Boots",
            "type": "sprite",
            "density": 5,
        },
        {"id": 190, "name": "Castle Pipebombs", "type": "sprite", "density": 0},
        {"id": 191, "name": "Castle Jetpack", "type": "sprite", "density": 3},
        {"id": 200, "name": "Castle Holo Duke", "type": "sprite", "density": 4},
        {
            "id": 204,
            "name": "Red Auction Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 205, "name": "Red Auction Holo Duke", "type": "sprite", "density": 0},
        {"id": 210, "name": "Upper Main Pipebombs", "type": "sprite", "density": 3},
        {"id": 213, "name": "MP Red Key Medkit", "type": "sprite", "density": 5},
        {
            "id": 214,
            "name": "Blue Area Hidden Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 215, "name": "Blue Area Hidden Armor", "type": "sprite", "density": 4},
        {"id": 218, "name": "Pool Steroids", "type": "sprite", "density": 0},
        {"id": 220, "name": "Pool Medkit", "type": "sprite", "density": 0},
        {"id": 229, "name": "Inside Boat Shrinker", "type": "sprite", "density": 0},
        {"id": 230, "name": "Boat Top Freezethrower", "type": "sprite", "density": 0},
        {"id": 231, "name": "Castle Atomic Health", "type": "sprite", "density": 3},
        {"id": 232, "name": "Castle RPG", "type": "sprite", "density": 3},
        {"id": 233, "name": "Castle Devastator", "type": "sprite", "density": 0},
        {"id": 234, "name": "Castle Chaingun", "type": "sprite", "density": 0},
        {"id": 235, "name": "Castle Shotgun", "type": "sprite", "density": 0},
        {"id": 236, "name": "Upper Pool Chaingun", "type": "sprite", "density": 0},
        {"id": 238, "name": "Blue Area Back RPG", "type": "sprite", "density": 0},
        {"id": 245, "name": "Upper Main Atomic Health", "type": "sprite", "density": 0},
        {"id": 246, "name": "Ticket Booth Shotgun", "type": "sprite", "density": 0},
        {
            "id": 417,
            "name": "Duck Conveyor Atomic Health 1",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 418,
            "name": "Duck Conveyor Atomic Health 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 445, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 634, "name": "Red Upper Armor", "type": "sprite", "density": 0},
        {"id": 656, "name": "Castle Dive Tripmine 1", "type": "sprite", "density": 4},
        {"id": 657, "name": "Castle Dive Tripmine 2", "type": "sprite", "density": 3},
        {"id": 668, "name": "Castle Dive Scuba Gear", "type": "sprite", "density": 0},
        {"id": 694, "name": "Sky Secret Atomic Health", "type": "sprite", "density": 2},
        {"id": 755, "name": "Red Boat Shrinker", "type": "sprite", "density": 4},
        {"id": 90, "name": "Secret Blue Area Hidden Room", "type": "sector"},
        {"id": 193, "name": "Secret Blue Explosion", "type": "sector"},
        {"id": 200, "name": "Secret Sky", "type": "sector"},
        {"id": 336, "name": "Secret Prison", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Pool Steroids",
            ],
        )

        ticket_booth = self.region(
            "Ticket Booth",
            [
                "Ticket Booth Shotgun",
            ],
        )
        # Can use the rotating door to clip over into the ticket booth
        # Also possible to strafe into corner and grab
        # TODO_LOGIC: maybe lower difficulty
        self.connect(ret, ticket_booth, r.difficulty("hard") | r.jump)

        main_upper = self.region(
            "Upper Main Area",
            [
                "Upper Main Pipebombs",
                "Upper Main Atomic Health",
            ],
        )
        self.connect(ret, main_upper, r.jump)

        pool = self.region(
            "Pool",
            [
                "Pool Medkit",
            ],
        )
        self.connect(ret, pool, r.can_dive)

        upper_pool = self.region(
            "Upper Pool",
            [
                "Upper Pool Chaingun",
            ],
        )
        self.connect(ret, upper_pool, r.jump)

        pool_price = self.region(
            "Pool Price Area",
            [
                "Blue Key Card",
            ],
        )
        # Can sr50 from the rotating boats onto the price pillar with sprint/roids
        self.connect(ret, pool_price, r.jump | (r.sprint & r.difficulty("hard")))

        blue_area = self.region(
            "Blue Key Area",
            [],
        )
        # Need to cross the bridge to open the blue key area, sr50 jump on hard
        self.connect(
            ret,
            blue_area,
            self.blue_key & ((r.sr50 & r.jump) | r.jetpack(50)),
        )

        blue_secret = self.region(
            "Blue Secret",
            [
                "Secret Blue Explosion",
            ],
        )
        self.connect(blue_area, blue_secret, r.explosives & r.jump)

        blue_area_back = self.region(
            "Blue Area Behind Targets",
            [
                "Blue Area Back RPG",
                "Duck Conveyor Atomic Health 1",
                "Duck Conveyor Atomic Health 2",
            ],
        )
        self.connect(blue_area, blue_area_back, r.jump)

        blue_area_hidden = self.region(
            "Blue Area Hidden Room",
            [
                "Secret Blue Area Hidden Room",
                "Blue Area Hidden Night Vision Goggles",
                "Blue Area Hidden Armor",
                "Red Key Card",
            ],
        )
        self.connect(blue_area, blue_area_hidden, r.jump & r.can_crouch)

        red_area = self.region(
            "Red Key Area",
            [
                "MP Red Key Medkit",
                "Red Boat RPG",
                "Red Boat Chaingun",
                "Red Boat Shrinker",
                "Red Auction Night Vision Goggles",
            ],
        )
        self.restrict("MP Red Key Medkit", r.can_open | r.jump)
        self.connect(main_upper, red_area, self.red_key)

        red_upper_start = self.region(
            "Red Upper Area Start",
            [
                "Red Upper Armor",
            ],
        )
        # Can sr50 jump up using the sign
        self.connect(
            red_area,
            red_upper_start,
            r.jump | (r.can_jump & r.sr50),
        )

        red_upper = self.region(
            "Red Upper Area",
            [
                "Red Upper 2 Pipebombs",
                "Red Auction Holo Duke",
                "Red Auction Protective Boots",
            ],
        )
        self.connect(red_area, red_upper, r.jump)

        prison_secret = self.region(
            "Prison Secret Area",
            [
                "Secret Prison",
            ],
        )
        self.connect(red_area, prison_secret, r.explosives & r.jump)

        castle_dive = self.region(
            "Castle Dive Area",
            [
                "Castle Dive Tripmine 1",
                "Castle Dive Tripmine 2",
                "Castle Dive Scuba Gear",
                "Inside Boat Shrinker",
            ],
        )
        self.connect(red_area, castle_dive, r.can_dive)

        boat_top = self.region(
            "Boat Top",
            [
                "MP Boat Top Protective Boots",
                "Boat Top Freezethrower",
            ],
        )
        self.connect(red_area, boat_top, r.jetpack(50) | r.can_dive)

        castle = self.region(
            "Castle",
            [
                "Castle Atomic Health",
                "Castle RPG",
                "Castle Devastator",
                "Castle Chaingun",
                "Castle Shotgun",
            ],
        )
        castle_upper = self.region(
            "Castle Upper",
            [
                "Castle Pipebombs",
                "Castle Jetpack",
                "Castle Holo Duke",
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_open & r.can_use)
        self.connect(
            castle, castle_upper, r.can_open | (r.sr50 & r.jump) | r.jetpack(50)
        )
        # Switch for castle door can be activated from the outside
        self.connect(
            red_area,
            castle,
            (r.difficulty("medium") & r.can_jump & r.can_use) | r.jetpack(50),
        )
        # The other option is the button on top of the boat
        self.connect(boat_top, castle, r.true)

        sky_secret = self.region(
            "Sky Secret Area",
            [
                "Secret Sky",
                "Sky Secret Atomic Health",
            ],
        )
        # Only requires around 30 jetpack i believe
        self.connect(red_area, sky_secret, r.jetpack(50))
        return ret
