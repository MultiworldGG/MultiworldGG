from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L6(D3DLevel):
    name = "Rabid Transit"
    levelnum = 5
    volumenum = 2
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 1, "name": "Track Steroids", "type": "sprite", "density": 2},
        {"id": 8, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 20, "name": "Blue Key Freezethrower", "type": "sprite", "density": 3},
        {"id": 21, "name": "Library Pipebombs", "type": "sprite", "density": 3},
        {
            "id": 53,
            "name": "Vending Machine Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 91, "name": "Underwater Shrinker", "type": "sprite", "density": 0},
        {"id": 92, "name": "Bookshelf Atomic Health", "type": "sprite", "density": 2},
        {"id": 140, "name": "Track Devastator", "type": "sprite", "density": 1},
        {
            "id": 283,
            "name": "Magazine Store Night Vision Goggles",
            "type": "sprite",
            "density": 1,
        },
        {"id": 296, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 333, "name": "Entrance Shotgun", "type": "sprite", "density": 1},
        {"id": 334, "name": "Poster Chaingun", "type": "sprite", "density": 2},
        {"id": 339, "name": "Magazine Holo Duke", "type": "sprite", "density": 2},
        {"id": 342, "name": "Entrance Pipebombs", "type": "sprite", "density": 4},
        {"id": 361, "name": "Blue Key Armor", "type": "sprite", "density": 4},
        {"id": 362, "name": "Blue Key Medkit", "type": "sprite", "density": 4},
        {"id": 364, "name": "Blue Door Atomic Health", "type": "sprite", "density": 3},
        {"id": 365, "name": "Train Chaingun", "type": "sprite", "density": 0},
        {"id": 366, "name": "Train Atomic Health", "type": "sprite", "density": 4},
        {"id": 367, "name": "Train RPG", "type": "sprite", "density": 3},
        {"id": 368, "name": "Train Medkit", "type": "sprite", "density": 4},
        {"id": 385, "name": "Blue Door Tripmine 1", "type": "sprite", "density": 3},
        {"id": 386, "name": "Blue Door Tripmine 2", "type": "sprite", "density": 4},
        {"id": 387, "name": "Blue Door Tripmine 3", "type": "sprite", "density": 4},
        {"id": 388, "name": "Blue Door Tripmine 4", "type": "sprite", "density": 4},
        {"id": 389, "name": "Blue Door Tripmine 5", "type": "sprite", "density": 0},
        {
            "id": 411,
            "name": "MP Blue Door Night Vision Goggles",
            "type": "sprite",
            "density": 5,
        },
        {"id": 429, "name": "Alien Base Devastator", "type": "sprite", "density": 2},
        {"id": 472, "name": "Track Atomic Health", "type": "sprite", "density": 4},
        {"id": 6, "name": "Secret Post Box Wall", "type": "sector"},
        {"id": 132, "name": "Secret Poster", "type": "sector"},
        {"id": 149, "name": "Secret Bookshelves", "type": "sector"},
        {"id": 163, "name": "Secret Magazines", "type": "sector"},
        {"id": 172, "name": "Secret Alien Base", "type": "sector"},
        {"id": 182, "name": "Secret Track Wall", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Entrance Shotgun",
                "Entrance Pipebombs",
                "Vending Machine Atomic Health",
                "Train Chaingun",
                "Train Atomic Health",
                "Train RPG",
                "Train Medkit",
                "Track Devastator",
                "Blue Door Tripmine 1",
                "Blue Door Tripmine 2",
                "Blue Door Tripmine 3",
                "Blue Door Tripmine 4",
                "Blue Door Tripmine 5",
            ],
        )
        self.restrict("Track Devastator", r.can_open)
        self.restrict("Vending Machine Atomic Health", r.can_use)

        magazine_secret = self.region(
            "Behind the Magazine Machine", ["Secret Magazines", "Magazine Holo Duke"]
        )
        self.connect(ret, magazine_secret, r.can_crouch & r.jump)

        start_ledges = self.region(
            "Subway Ledges",
            [
                "Magazine Store Night Vision Goggles",
                "Blue Key Card",
                "Blue Key Freezethrower",
                "Blue Key Medkit",
                "Blue Key Armor",
            ],
        )
        self.connect(ret, start_ledges, r.jump)
        self.restrict("Magazine Store Night Vision Goggles", r.can_use)

        duke_poster = self.region("Duke Poster", ["Secret Poster", "Poster Chaingun"])
        self.connect(
            ret,
            duke_poster,
            (r.jump & r.can_open)
            | (r.difficulty("hard") & r.crouch_jump)
            | r.fast_crouch_jump,
        )

        track_wall = self.region(
            "Track Breakable Wall",
            ["Secret Track Wall", "Track Steroids", "Track Atomic Health"],
        )
        self.connect(ret, track_wall, r.explosives)

        blue_door = self.region(
            "Behind Blue Door",
            [
                "Red Key Card",
                "MP Blue Door Night Vision Goggles",
                "Blue Door Atomic Health",
                "Secret Post Box Wall",
            ],
        )
        self.connect(ret, blue_door, (self.blue_key & r.can_open) | r.glitch_kick)
        self.restrict(
            "Secret Post Box Wall",
            r.jump & (r.can_open | (r.glitched & r.can_crouch & r.fast_sprint)),
        )

        alien_base = self.region(
            "Alien Base", ["Secret Alien Base", "Alien Base Devastator"]
        )
        self.connect(blue_door, alien_base, r.can_open)
        self.restrict("Alien Base Devastator", r.can_use)

        library = self.region("Library", ["Library Pipebombs"])
        self.connect(ret, library, self.red_key & r.can_open)

        bookshelf = self.region(
            "Bookshelves", ["Secret Bookshelves", "Bookshelf Atomic Health"]
        )
        self.connect(
            library,
            bookshelf,
            r.jetpack(50) | (r.can_jump & (r.explosives | r.difficulty("medium"))),
        )

        exit_area = self.region("Exit Area", ["Exit", "Underwater Shrinker"])
        self.connect(library, exit_area, r.can_dive)
        self.restrict("Exit", r.can_use)
        return ret
