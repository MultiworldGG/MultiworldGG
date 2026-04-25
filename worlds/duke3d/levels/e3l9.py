from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L9(D3DLevel):
    name = "Stadium"
    levelnum = 8
    volumenum = 2
    keys = []
    location_defs = [
        {"id": 1, "name": "MP Floor Armor", "type": "sprite", "density": 5},
        {"id": 12, "name": "MP Ledge Shotgun", "type": "sprite", "density": 5},
        {"id": 13, "name": "Floor Pipebombs 1", "type": "sprite", "density": 3},
        {"id": 14, "name": "Floor Pipebombs 2", "type": "sprite", "density": 3},
        {"id": 15, "name": "Floor Pipebombs 3", "type": "sprite", "density": 4},
        {"id": 16, "name": "Floor Pipebombs 4", "type": "sprite", "density": 4},
        {"id": 17, "name": "Ledge Shrinker 1", "type": "sprite", "density": 4},
        {"id": 18, "name": "MP Floor Chaingun", "type": "sprite", "density": 5},
        {"id": 19, "name": "MP Floor Freezethrower", "type": "sprite", "density": 5},
        {"id": 20, "name": "MP Floor RPG", "type": "sprite", "density": 5},
        {"id": 21, "name": "MP Floor Devastator", "type": "sprite", "density": 5},
        {"id": 23, "name": "Ledge Shrinker 2", "type": "sprite", "density": 4},
        {
            "id": 24,
            "name": "Ledge Night Vision Goggles 1",
            "type": "sprite",
            "density": 1,
        },
        {"id": 25, "name": "Ledge Holo Duke", "type": "sprite", "density": 0},
        {"id": 45, "name": "Ledge Chaingun", "type": "sprite", "density": 3},
        {"id": 46, "name": "Ledge Jetpack", "type": "sprite", "density": 0},
        {"id": 47, "name": "Ledge RPG", "type": "sprite", "density": 4},
        {"id": 48, "name": "Ledge Freezethrower", "type": "sprite", "density": 3},
        {"id": 49, "name": "Ledge Shotgun", "type": "sprite", "density": 1},
        {"id": 50, "name": "Ledge Devastator", "type": "sprite", "density": 3},
        {"id": 51, "name": "Floor Steroids 1", "type": "sprite", "density": 1},
        {"id": 52, "name": "Floor Steroids 2", "type": "sprite", "density": 0},
        {"id": 85, "name": "MP Ledge Jetpack 1", "type": "sprite", "density": 5},
        {"id": 86, "name": "MP Ledge Jetpack 2", "type": "sprite", "density": 5},
        {
            "id": 87,
            "name": "Floor Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {"id": 88, "name": "MP Ledge Chaingun", "type": "sprite", "density": 5},
        {"id": 89, "name": "MP Ledge Pipebombs", "type": "sprite", "density": 5},
        {"id": 90, "name": "MP Ledge Devastator", "type": "sprite", "density": 5},
        {"id": 91, "name": "MP Ledge RPG", "type": "sprite", "density": 5},
        {"id": 92, "name": "MP Ledge Shrinker", "type": "sprite", "density": 5},
        {"id": 93, "name": "MP Ledge Freezethrower", "type": "sprite", "density": 5},
        {"id": 94, "name": "Floor Medkit", "type": "sprite", "density": 4},
        {
            "id": 95,
            "name": "Ledge Night Vision Goggles 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 104, "name": "Floor Atomic Health 1", "type": "sprite", "density": 4},
        {"id": 105, "name": "Floor Atomic Health 2", "type": "sprite", "density": 4},
        {"id": 106, "name": "Floor Atomic Health 3", "type": "sprite", "density": 4},
        {"id": 107, "name": "Floor Atomic Health 4", "type": "sprite", "density": 4},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    has_boss = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "MP Floor Armor",
                "Floor Pipebombs 1",
                "Floor Pipebombs 2",
                "Floor Pipebombs 3",
                "Floor Pipebombs 4",
                "MP Floor Chaingun",
                "MP Floor Freezethrower",
                "MP Floor RPG",
                "MP Floor Devastator",
                "Floor Steroids 1",
                "Floor Steroids 2",
                "Floor Night Vision Goggles",
                "Floor Medkit",
                "Floor Atomic Health 1",
                "Floor Atomic Health 2",
                "Floor Atomic Health 3",
                "Floor Atomic Health 4",
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_kill_boss_3)

        ledge = self.region(
            "Stadium Ledge",
            [
                "MP Ledge Shotgun",
                "Ledge Shrinker 1",
                "Ledge Shrinker 2",
                "Ledge Night Vision Goggles 1",
                "Ledge Holo Duke",
                "Ledge Chaingun",
                "Ledge Jetpack",
                "Ledge RPG",
                "Ledge Freezethrower",
                "Ledge Shotgun",
                "Ledge Devastator",
                "MP Ledge Jetpack 1",
                "MP Ledge Jetpack 2",
                "MP Ledge Chaingun",
                "MP Ledge Pipebombs",
                "MP Ledge Devastator",
                "MP Ledge RPG",
                "MP Ledge Shrinker",
                "MP Ledge Freezethrower",
                "Ledge Night Vision Goggles 2",
            ],
        )
        self.connect(ret, ledge, r.jump)
        return ret
