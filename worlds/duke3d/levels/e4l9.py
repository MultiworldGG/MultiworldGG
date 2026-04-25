from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L9(D3DLevel):
    name = "Derelict"
    levelnum = 8
    volumenum = 3
    keys = ["Red", "Blue", "Yellow"]
    location_defs = [
        {"id": 10, "name": "Kitchen Medkit", "type": "sprite", "density": 2},
        {
            "id": 65,
            "name": "Yellow Upper Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 185, "name": "Crusher Atomic Health", "type": "sprite", "density": 0},
        {"id": 211, "name": "Captains Shrinker", "type": "sprite", "density": 2},
        {"id": 214, "name": "Captains Atomic Health 1", "type": "sprite", "density": 3},
        {"id": 215, "name": "Captains Atomic Health 2", "type": "sprite", "density": 4},
        {
            "id": 216,
            "name": "Captains Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 217, "name": "Captains Armor", "type": "sprite", "density": 3},
        {"id": 223, "name": "Barracks Steroids", "type": "sprite", "density": 0},
        {"id": 229, "name": "TV Chaingun", "type": "sprite", "density": 2},
        {"id": 261, "name": "Yellow Pipebombs", "type": "sprite", "density": 3},
        {"id": 504, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 626, "name": "Yellow Upper Pipebombs", "type": "sprite", "density": 3},
        {"id": 834, "name": "Crate Protective Boots", "type": "sprite", "density": 3},
        {"id": 960, "name": "Upper Deck Steroids", "type": "sprite", "density": 0},
        {"id": 961, "name": "Upper Deck Medkit", "type": "sprite", "density": 0},
        {"id": 962, "name": "Scan Room RPG", "type": "sprite", "density": 4},
        {"id": 964, "name": "Outside Dive RPG", "type": "sprite", "density": 0},
        {
            "id": 967,
            "name": "Upper Deck Atomic Health 1",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 968,
            "name": "Upper Deck Atomic Health 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 969, "name": "Ship Deck Scuba Gear", "type": "sprite", "density": 3},
        {
            "id": 970,
            "name": "MP Outside Dive Jetpack 1",
            "type": "sprite",
            "density": 5,
        },
        {
            "id": 971,
            "name": "MP Outside Dive Jetpack 2",
            "type": "sprite",
            "density": 5,
        },
        {"id": 972, "name": "MP Yellow Final Jetpack", "type": "sprite", "density": 5},
        {"id": 973, "name": "Ship Deck Armor", "type": "sprite", "density": 0},
        {"id": 976, "name": "Upper Deck Shotgun", "type": "sprite", "density": 3},
        {"id": 977, "name": "Low Deck Chaingun", "type": "sprite", "density": 0},
        {"id": 980, "name": "Upper Deck Shrinker", "type": "sprite", "density": 0},
        {"id": 983, "name": "Upper Deck Tripmine 1", "type": "sprite", "density": 3},
        {"id": 984, "name": "Upper Deck Tripmine 2", "type": "sprite", "density": 4},
        {"id": 988, "name": "Crate Freezethrower", "type": "sprite", "density": 3},
        {"id": 989, "name": "Crate Devastator", "type": "sprite", "density": 0},
        {
            "id": 992,
            "name": "Scan Room  Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 994, "name": "Crate RPG", "type": "sprite", "density": 2},
        {"id": 995, "name": "MP Crate Jetpack", "type": "sprite", "density": 5},
        {"id": 996, "name": "Low Deck Atomic Health", "type": "sprite", "density": 0},
        {"id": 997, "name": "Low Deck Holo Duke", "type": "sprite", "density": 0},
        {"id": 1007, "name": "Big Crate Pipebombs 1", "type": "sprite", "density": 3},
        {"id": 1008, "name": "Big Crate Pipebombs 2", "type": "sprite", "density": 4},
        {"id": 1009, "name": "Big Crate Armor", "type": "sprite", "density": 4},
        {"id": 1010, "name": "Fire Atomic Health", "type": "sprite", "density": 0},
        {
            "id": 1011,
            "name": "Next to Crusher Chaingun",
            "type": "sprite",
            "density": 3,
        },
        {"id": 1012, "name": "Next to Crusher Shotgun", "type": "sprite", "density": 4},
        {"id": 1021, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 1022, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 1058, "name": "Yellow Atomic Health", "type": "sprite", "density": 0},
        {"id": 1081, "name": "Yellow Protective Boots", "type": "sprite", "density": 0},
        {"id": 1082, "name": "Yellow Steroids", "type": "sprite", "density": 3},
        {
            "id": 1111,
            "name": "Yellow Water Tank Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 1118,
            "name": "Yellow Underwater Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 1173, "name": "MP Yellow Jetpack", "type": "sprite", "density": 5},
        {"id": 1181, "name": "Dive Secret Chaingun", "type": "sprite", "density": 2},
        {"id": 1182, "name": "Dive Secret Steroids", "type": "sprite", "density": 3},
        {
            "id": 1183,
            "name": "Dive Secret Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {"id": 1184, "name": "Dive Secret Armor", "type": "sprite", "density": 4},
        {"id": 1185, "name": "TV Timed Shotgun", "type": "sprite", "density": 3},
        {"id": 347, "name": "Secret Crate", "type": "sector"},
        {"id": 718, "name": "Secret TV", "type": "sector"},
        {"id": 761, "name": "Secret Captains Cabin", "type": "sector"},
        {"id": 795, "name": "Secret Dive", "type": "sector"},
        {"id": 800, "name": "Secret Kitchen", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [],
        )

        outside_dive = self.region(
            "Outside Dive",
            [
                "Outside Dive RPG",
                "MP Outside Dive Jetpack 1",
                "MP Outside Dive Jetpack 2",
                "Secret Dive",
                "Dive Secret Chaingun",
                "Dive Secret Steroids",
                "Dive Secret Night Vision Goggles",
                "Dive Secret Armor",
            ],
        )
        self.connect(ret, outside_dive, r.can_dive)

        ship_deck = self.region(
            "Ship Deck",
            [
                "Ship Deck Armor",
                "Ship Deck Scuba Gear",
            ],
        )
        self.connect(ret, ship_deck)

        upper_deck_outside = self.region(
            "Upper Deck Outside",
            [
                "Upper Deck Steroids",
                "Upper Deck Medkit",
                "Upper Deck Atomic Health 1",
                "Upper Deck Atomic Health 2",
                "Upper Deck Shotgun",
            ],
        )
        # Without jetpack requires enemy jump or sr50 to get over outside gap
        self.connect(
            ship_deck, upper_deck_outside, r.jetpack(50) | (r.sr50 & r.can_jump)
        )

        upper_deck_inside = self.region(
            "Upper Deck Inside",
            [
                "Upper Deck Shrinker",
                "Upper Deck Tripmine 1",
                "Upper Deck Tripmine 2",
                "Crate Freezethrower",
                "Crate Devastator",
                "Low Deck Atomic Health",
                "Low Deck Chaingun",
                "Low Deck Holo Duke",
            ],
        )
        # Can't get up there with just jetpack, but it might be possible to just grab it anyway at the right angle
        self.restrict("Crate Freezethrower", r.can_jump)
        self.restrict("Low Deck Atomic Health", r.can_use & r.jump)
        scan_room = self.region(
            "Scan Room",
            [
                "Blue Key Card",
                "Scan Room RPG",
                "Scan Room  Night Vision Goggles",
            ],
        )
        self.connect(ship_deck, scan_room, r.jetpack(50))
        # The door clips in this map are incredibly squish death heavy, thus extreme difficulty
        self.connect(
            upper_deck_inside,
            scan_room,
            r.can_open
            | (r.fast_sprint & r.can_crouch & r.glitched & r.difficulty("extreme")),
        )
        self.connect(
            upper_deck_outside,
            upper_deck_inside,
            r.can_open
            | (r.fast_sprint & r.can_crouch & r.glitched & r.difficulty("extreme")),
        )

        blue_key_area = self.region(
            "Blue Key Area",
            [
                "Barracks Steroids",
                "Red Key Card",
                "Captains Armor",
                "Captains Night Vision Goggles",
            ],
        )
        self.restrict("Captains Night Vision Goggles", r.jump)
        self.connect(upper_deck_inside, blue_key_area, (self.blue_key & r.can_open))
        # Alternate path to blue key area through roid clip
        # Needs can_open or jetpack for elevator
        self.connect(
            outside_dive,
            blue_key_area,
            r.glitched
            & (r.can_open | r.jetpack(50))  # elevator
            & (
                r.can_open
                | (r.fast_sprint & r.can_crouch & r.glitched & r.difficulty("extreme"))
            )  # door clip if no open from elevator requirement
            & (
                (r.steroids & (r.can_crouch | r.can_jump))
                | (r.can_sprint & r.can_jump)
                | (r.can_sprint & r.jetpack(50)) & r.difficulty("hard")
            ),  # clip from secret to blue key area
        )

        blue_key_lower = self.region(
            "Blue Key Lower Area",
            [
                "Secret Kitchen",
                "Kitchen Medkit",
            ],
        )
        self.connect(blue_key_area, blue_key_lower, r.can_crouch & r.can_use)

        blue_key_upper = self.region(
            "Blue Key Upper Area",
            [
                "Secret Captains Cabin",
                "Captains Shrinker",
                "Captains Atomic Health 1",
                "Captains Atomic Health 2",
            ],
        )
        self.connect(blue_key_area, blue_key_upper, r.jump & r.can_use)

        tv_secret_area = self.region(
            "TV Secret Area",
            [
                "Secret TV",
                "TV Chaingun",
                "TV Timed Shotgun",
            ],
        )
        self.connect(blue_key_area, tv_secret_area, r.can_jump)

        red_key_area = self.region(
            "Red Key Area",
            [
                "Fire Atomic Health",
            ],
        )
        # Another roid clip that doesnt require jump to pull off
        # TODO_LOGIC: Maybe possible with only r.can_sprint & r.can_crouch
        self.connect(
            blue_key_area,
            red_key_area,
            (self.red_key & r.can_open)
            | (r.fast_sprint & r.can_crouch & r.glitched & r.difficulty("extreme")),
        )

        red_upper = self.region(
            "Red Upper Area",
            [
                "Crusher Atomic Health",
                "Big Crate Pipebombs 1",
                "Big Crate Pipebombs 2",
                "Big Crate Armor",
                "Next to Crusher Chaingun",
                "Next to Crusher Shotgun",
                "Yellow Key Card",
            ],
        )
        self.connect(red_key_area, red_upper, r.jump)

        yellow_key_area = self.region(
            "Yellow Key Area",
            [
                "MP Yellow Jetpack",
                "Yellow Atomic Health",
                "Yellow Pipebombs",
                "Yellow Steroids",
                "Yellow Protective Boots",
            ],
        )
        # Caught trippin
        self.connect(
            blue_key_area,
            yellow_key_area,
            self.yellow_key
            | (
                r.difficulty("extreme")
                & r.can_jump
                & r.tripmine
                & r.glitched
                & r.fast_sprint
            ),
        )

        crate_secret = self.region(
            "Secret Crate",
            [
                "Secret Crate",
                "Crate RPG",
                "MP Crate Jetpack",
                "Crate Protective Boots",
            ],
        )
        self.connect(yellow_key_area, crate_secret, r.jump)

        yellow_underwater = self.region(
            "Yellow Underwater",
            [
                "Yellow Underwater Atomic Health",
            ],
        )
        # Takes 70ish HP to get there on the slime
        self.connect(
            yellow_key_area,
            yellow_underwater,
            r.difficulty("hard") & r.can_dive & r.can_crouch & r.can_sprint,
        )

        yellow_upper = self.region(
            "Yellow Upper Area",
            [
                "Yellow Upper Atomic Health",
                "Yellow Upper Pipebombs",
            ],
        )
        self.restrict(
            "Yellow Upper Atomic Health",
            (r.can_open & r.can_use)
            | (r.fast_sprint & r.can_crouch & r.glitched & r.difficulty("extreme")),
        )
        self.restrict(
            "Yellow Upper Pipebombs",
            (r.can_open & r.can_use)
            | (r.fast_sprint & r.can_crouch & r.glitched & r.difficulty("extreme")),
        )
        # Takes 80ish HP to get there on the slime, we can barely survive this path
        self.connect(
            yellow_key_area,
            yellow_upper,
            r.jetpack(50)
            | (
                r.difficulty("hard") & r.can_dive & r.can_crouch & r.can_sprint & r.jump
            ),
        )
        self.connect(yellow_upper, yellow_underwater, r.can_dive)

        yellow_final = self.region(
            "Yellow Final Area",
            [
                "MP Yellow Final Jetpack",
                "Yellow Water Tank Atomic Health",
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_use)
        # TODO_LOGIC: There is a way to clip to the exit from the starting dive
        # even the slime dive route only uses 20 scuba, so no need to count here
        self.connect(yellow_upper, yellow_final, r.can_dive)
        return ret
