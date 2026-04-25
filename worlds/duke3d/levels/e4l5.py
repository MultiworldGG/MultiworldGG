from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L5(D3DLevel):
    name = "Pigsty"
    levelnum = 4
    volumenum = 3
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {"id": 61, "name": "Basement Pipebombs", "type": "sprite", "density": 3},
        {"id": 76, "name": "Basement Atomic Health", "type": "sprite", "density": 2},
        {"id": 79, "name": "Security Steroids", "type": "sprite", "density": 0},
        {"id": 80, "name": "Graffiti Steroids", "type": "sprite", "density": 4},
        {"id": 90, "name": "Graffiti Freezethrower", "type": "sprite", "density": 4},
        {"id": 91, "name": "Graffiti Devastator", "type": "sprite", "density": 0},
        {"id": 92, "name": "Graffiti RPG", "type": "sprite", "density": 3},
        {"id": 123, "name": "Yellow Atomic Health", "type": "sprite", "density": 0},
        {"id": 142, "name": "MP Yellow Shotgun", "type": "sprite", "density": 5},
        {"id": 196, "name": "Basement Tripmine 1", "type": "sprite", "density": 3},
        {"id": 197, "name": "Basement Tripmine 2", "type": "sprite", "density": 4},
        {"id": 198, "name": "Basement Freezethrower", "type": "sprite", "density": 0},
        {"id": 211, "name": "Basement Jetpack", "type": "sprite", "density": 0},
        {"id": 260, "name": "Upstairs RPG", "type": "sprite", "density": 0},
        {"id": 264, "name": "Upstairs Medkit", "type": "sprite", "density": 4},
        {"id": 266, "name": "Bookshelf Atomic Health", "type": "sprite", "density": 2},
        {"id": 267, "name": "Red Area Steroids", "type": "sprite", "density": 3},
        {"id": 268, "name": "Poster Medkit", "type": "sprite", "density": 2},
        {"id": 363, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 441, "name": "Telephone Atomic Health", "type": "sprite", "density": 2},
        {"id": 528, "name": "Bookshelf Chaingun 1", "type": "sprite", "density": 3},
        {"id": 529, "name": "Bookshelf Chaingun 2", "type": "sprite", "density": 4},
        {"id": 530, "name": "Bookshelf Chaingun 3", "type": "sprite", "density": 4},
        {"id": 613, "name": "Start Shotgun", "type": "sprite", "density": 0},
        {"id": 618, "name": "Start Chaingun", "type": "sprite", "density": 0},
        {"id": 717, "name": "Basement Blue Pipebombs", "type": "sprite", "density": 3},
        {"id": 751, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 767, "name": "MP Hangout Jetpack", "type": "sprite", "density": 5},
        {"id": 768, "name": "Yellow Shrinker", "type": "sprite", "density": 0},
        {"id": 771, "name": "Start Armor", "type": "sprite", "density": 4},
        {
            "id": 773,
            "name": "Upstairs Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 811, "name": "Start Pipebombs", "type": "sprite", "density": 3},
        {"id": 812, "name": "MP Security Armor", "type": "sprite", "density": 5},
        {"id": 813, "name": "MP Security Shotgun", "type": "sprite", "density": 5},
        {"id": 841, "name": "Unreachable Holo Duke", "type": "sprite"},
        {"id": 854, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 5, "name": "Secret Telephone", "type": "sector"},
        {"id": 56, "name": "Secret Poster", "type": "sector"},
        {"id": 123, "name": "Secret Bookshelf", "type": "sector"},
        {"id": 465, "name": "Secret Graffiti", "type": "sector"},
        {"id": 469, "name": "Secret Basement", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
        {"id": 11, "name": "Secret Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Start Shotgun",
                "Start Chaingun",
                "Start Armor",
                "Start Pipebombs",
            ],
        )
        tele_secret = self.region(
            "Secret Telephone",
            [
                "Secret Telephone",
                "Telephone Atomic Health",
            ],
        )
        # Item can be barely grabbed without getting stuck
        self.connect(ret, tele_secret, r.can_jump & r.can_use)

        graffiti_secret = self.region(
            "Secret Graffiti",
            [
                "Secret Graffiti",
                "Graffiti Steroids",
                "Graffiti Freezethrower",
                "Graffiti Devastator",
                "Graffiti RPG",
            ],
        )
        self.connect(ret, graffiti_secret, r.jetpack(100))
        early_basement = self.region(
            "Early Basement",
            [
                "Basement Pipebombs",
                "Basement Jetpack",
            ],
        )
        past_car = self.region(
            "Lobby past car",
            [
                "Basement Tripmine 1",
                "Basement Tripmine 2",
                "Basement Freezethrower",
                "Basement Atomic Health",
                "Secret Basement",
                "Upstairs RPG",
                "Upstairs Medkit",
                "Upstairs Night Vision Goggles",
                "Blue Key Card",
            ],
        )
        self.restrict("Secret Basement", r.can_use)
        self.restrict("Basement Atomic Health", r.can_use)
        # Can walk off the stairs on top, a bit tricky without sprint
        # Other entry leads through manhole cover
        self.connect(ret, past_car, r.can_open & (r.sr50 | r.jump))
        self.connect(ret, early_basement, r.explosives)
        self.connect(early_basement, past_car, r.can_open)

        security_mons_upper = self.region(
            "Security Monitors Upper",
            [
                "Security Steroids",
                "MP Security Armor",
                "MP Security Shotgun",
            ],
        )
        # Can diagonal walk into security monitors and use crouch to clip up
        # Requires difficult sr50 without sprint
        self.connect(
            past_car,
            security_mons_upper,
            r.can_sprint & r.difficulty("medium") | r.difficulty("hard") | r.jump,
        )

        blue_key_area = self.region(
            "Blue Key Area",
            [
                "Secret Bookshelf",
                "Bookshelf Atomic Health",
                "Bookshelf Chaingun 1",
                "Bookshelf Chaingun 2",
                "Bookshelf Chaingun 3",
            ],
        )
        self.connect(past_car, blue_key_area, self.blue_key & r.can_open)
        # Can clip through basement blue key door with roid crouch jump
        basement_blue_area = self.region(
            "Basement Blue Area",
            [
                "Basement Blue Pipebombs",
                "Red Key Card",
            ],
        )
        self.connect(
            past_car,
            basement_blue_area,
            self.blue_key | (r.difficulty("medium") & r.crouch_jump & r.steroids),
        )

        red_key_area = self.region(
            "Red Key Area",
            [
                "Red Area Steroids",
                "Yellow Key Card",
            ],
        )
        self.connect(past_car, red_key_area, self.red_key & r.can_open)

        poster_secret = self.region(
            "Poster Secret Area",
            [
                "Secret Poster",
                "Poster Medkit",
            ],
        )
        # Strafe up the terminal on the right to get into the poster secret
        self.connect(
            red_key_area, poster_secret, r.can_open & (r.jump | r.difficulty("hard"))
        )

        yellow_key_area = self.region(
            "Yellow Key Area",
            [
                "Yellow Shrinker",
                "MP Yellow Shotgun",
                "Yellow Atomic Health",
            ],
        )
        self.connect(ret, yellow_key_area, self.yellow_key & r.can_open)

        secret_exit_area = self.region(
            "Secret Exit Area",
            [
                "Secret Exit",
            ],
        )
        self.restrict("Secret Exit", r.can_use)
        self.connect(yellow_key_area, secret_exit_area, r.jump)

        hangout_room = self.region(
            "Hangout Room",
            [
                "MP Hangout Jetpack",
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_use)
        self.connect(yellow_key_area, hangout_room, r.jump)

        # This location is unreachable behind a wall that's supposed to blow up:
        # {"id": 841, "name": "Unreachable Holo Duke", "type": "sprite"},
        return ret
