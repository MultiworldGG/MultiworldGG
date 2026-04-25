from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L10(D3DLevel):
    name = "Tier Drops"
    levelnum = 9
    volumenum = 2
    keys = []
    location_defs = [
        {"id": 0, "name": "Beta Shotgun", "type": "sprite", "density": 2},
        {"id": 3, "name": "Alpha Shotgun", "type": "sprite", "density": 2},
        {"id": 13, "name": "Delta Tripmine 1", "type": "sprite", "density": 4},
        {"id": 14, "name": "Delta Tripmine 2", "type": "sprite", "density": 4},
        {"id": 15, "name": "Delta Tripmine 3", "type": "sprite", "density": 4},
        {"id": 16, "name": "Alpha Armor", "type": "sprite", "density": 4},
        {"id": 17, "name": "Beta Night Vision Goggles", "type": "sprite", "density": 3},
        {"id": 18, "name": "Beta Medkit", "type": "sprite", "density": 4},
        {"id": 21, "name": "Gamma Jetpack", "type": "sprite", "density": 0},
        {"id": 30, "name": "Delta Pipebombs 1", "type": "sprite", "density": 2},
        {"id": 31, "name": "Delta Pipebombs 2", "type": "sprite", "density": 4},
        {"id": 38, "name": "Exit Freezethrower", "type": "sprite", "density": 0},
        {"id": 209, "name": "Brick RPG", "type": "sprite", "density": 1},
        {"id": 210, "name": "Brick Armor", "type": "sprite", "density": 4},
        {"id": 251, "name": "Desert Chaingun", "type": "sprite", "density": 3},
        {"id": 276, "name": "White Shrinker", "type": "sprite", "density": 0},
        {"id": 282, "name": "Green Devastator", "type": "sprite", "density": 3},
        {"id": 283, "name": "Alpha Steroids", "type": "sprite", "density": 3},
        {"id": 290, "name": "Delta Holo Duke", "type": "sprite", "density": 3},
        {"id": 314, "name": "Exit Atomic Health 1", "type": "sprite", "density": 4},
        {"id": 315, "name": "Exit Atomic Health 2", "type": "sprite", "density": 4},
        {"id": 316, "name": "Exit Atomic Health 3", "type": "sprite", "density": 4},
        {"id": 148, "name": "Secret Delta", "type": "sector"},
        {"id": 156, "name": "Secret Alpha", "type": "sector"},
        {"id": 164, "name": "Secret Beta", "type": "sector"},
        {"id": 172, "name": "Secret Gamma", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(self.name, ["White Shrinker"])

        centers = self.region(
            "The Rest of the Fucking Owl",
            [
                "Green Devastator",
                "Desert Chaingun",
                "Brick RPG",
                "Brick Armor",
            ],
        )
        self.connect(ret, centers, r.jump | (r.difficulty("medium") & r.fast_sprint))

        exit_hut = self.region(
            "Exit Room",
            [
                "Exit Freezethrower",
                "Exit Atomic Health 1",
                "Exit Atomic Health 2",
                "Exit Atomic Health 3",
                "Exit",
            ],
        )
        self.connect(centers, exit_hut, r.can_open)
        self.restrict("Exit", r.can_use)

        corners = self.region(
            "Corners",
            [
                "Alpha Shotgun",
                "Alpha Armor",
                "Alpha Steroids",
                "Secret Alpha",
                "Beta Shotgun",
                "Beta Night Vision Goggles",
                "Beta Medkit",
                "Secret Beta",
                "Gamma Jetpack",
                "Secret Gamma",
                "Delta Pipebombs 1",
                "Delta Pipebombs 2",
                "Delta Tripmine 1",
                "Delta Tripmine 2",
                "Delta Tripmine 3",
                "Delta Holo Duke",
                "Secret Delta",
            ],
        )
        self.connect(ret, corners, r.jump & r.can_open)
        return ret
