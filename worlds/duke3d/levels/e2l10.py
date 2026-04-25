from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L10(D3DLevel):
    name = "Spin Cycle"
    levelnum = 9
    volumenum = 1
    keys = []
    location_defs = [
        {"id": 36, "name": "Beta Shrinker", "type": "sprite", "density": 0},
        {"id": 37, "name": "Gamma Freezethrower", "type": "sprite", "density": 0},
        {"id": 38, "name": "Delta RPG", "type": "sprite", "density": 0},
        {"id": 39, "name": "Alpha Chaingun", "type": "sprite", "density": 3},
        {"id": 61, "name": "Gamma Medkit", "type": "sprite", "density": 0},
        {"id": 141, "name": "MP Alpha Holo Duke", "type": "sprite", "density": 5},
        {"id": 142, "name": "MP Beta Jetpack", "type": "sprite", "density": 5},
        {
            "id": 143,
            "name": "MP Gamma Night Vision Goggles",
            "type": "sprite",
            "density": 5,
        },
        {"id": 144, "density": 5, "name": "MP Delta Jetpack", "type": "sprite"},
        {"id": 162, "name": "Beta Atomic Health", "type": "sprite"},
        {"id": 179, "name": "Alpha Medkit", "type": "sprite", "density": 0},
        {"id": 199, "name": "Delta Atomic Health", "type": "sprite", "density": 0},
        {"id": 206, "name": "Alpha Shotgun", "type": "sprite", "density": 3},
        {"id": 207, "name": "Alpha Pipebombs", "type": "sprite", "density": 4},
        {"id": 210, "name": "Delta Shotgun", "type": "sprite", "density": 3},
        {"id": 211, "name": "Delta Shrinker", "type": "sprite", "density": 4},
        {"id": 224, "name": "Alpha Armor", "type": "sprite", "density": 0},
        {
            "id": 225,
            "name": "Gamma Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 226, "name": "Beta Medkit", "type": "sprite", "density": 0},
        {"id": 257, "name": "Center Holo Duke", "type": "sprite", "density": 0},
        {"id": 258, "name": "Center Devastator", "type": "sprite", "density": 3},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        # Nothing to see here
        ret = self.region(self.name, [loc["name"] for loc in self.location_defs])
        # Just step onto one of the enemies to cross the gap
        # Battlelords make this tricky
        self.restrict("Exit", r.can_use & r.can_open & (r.jump | r.difficulty("hard")))

        self.restrict("Alpha Medkit", r.can_open)
        self.restrict("Gamma Medkit", r.can_open)
        self.restrict("Gamma Night Vision Goggles", r.can_open)
        self.restrict("Beta Atomic Health", r.can_open)
        self.restrict("Alpha Armor", r.can_open)
        self.restrict("Delta Atomic Health", r.can_open)
        self.restrict("Beta Medkit", r.can_open)
        self.restrict("Center Devastator", r.can_open & r.can_use)
        self.restrict("Center Holo Duke", r.can_open & r.can_use)

        return ret
