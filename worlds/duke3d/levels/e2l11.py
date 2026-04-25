from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L11(D3DLevel):
    name = "Lunatic Fringe"
    levelnum = 10
    volumenum = 1
    keys = []
    location_defs = [
        {"id": 28, "name": "Center Ring Shrinker", "type": "sprite", "density": 0},
        {"id": 58, "name": "Top Ledge Devastator", "type": "sprite", "density": 0},
        {
            "id": 63,
            "name": "MP Center Ring Night Vision Goggles",
            "type": "sprite",
            "density": 5,
        },
        {"id": 92, "name": "Bottom Ring Holo Duke", "type": "sprite", "density": 0},
        {"id": 93, "name": "Center Ring RPG", "type": "sprite", "density": 0},
        {"id": 96, "name": "Bottom Ring Armor", "type": "sprite", "density": 0},
        {"id": 99, "name": "MP Center Ring Jetpack", "type": "sprite", "density": 5},
        {
            "id": 102,
            "name": "Center Ring Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 104, "name": "Top Ledge Pipebombs", "type": "sprite", "density": 3},
        {"id": 109, "name": "Center Ring Steroids", "type": "sprite", "density": 3},
        {"id": 111, "name": "Bottom Ring Tripmine", "type": "sprite", "density": 4},
        {"id": 112, "name": "Top Ledge Medkit", "type": "sprite", "density": 4},
        {"id": 113, "name": "MP Top Ledge Shrinker", "type": "sprite", "density": 5},
        {"id": 115, "name": "Center Ring Chaingun", "type": "sprite", "density": 0},
        {"id": 123, "name": "Center Ring Shotgun", "type": "sprite", "density": 4},
        {
            "id": 124,
            "name": "Bottom Ring Freezethrower",
            "type": "sprite",
            "density": 0,
        },
        {"id": 125, "name": "Bottom Ring Shotgun", "type": "sprite"},
        {"id": 127, "name": "Center Ring Pipebombs", "type": "sprite", "density": 3},
        {
            "id": 180,
            "name": "Center Top Atomic Health 1",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 181,
            "name": "Center Top Atomic Health 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [],
        )

        past_door = self.region(
            "Past Door",
            [
                "Top Ledge Devastator",
                "Top Ledge Pipebombs",
                "MP Top Ledge Shrinker",
                "Top Ledge Medkit",
                "Bottom Ring Holo Duke",
                "Bottom Ring Armor",
                "Bottom Ring Tripmine",
                "Bottom Ring Freezethrower",
                "Bottom Ring Shotgun",
                "Center Ring Shotgun",
            ],
        )
        self.connect(ret, past_door, r.can_use)
        self.restrict("Bottom Ring Holo Duke", r.can_open | r.fast_crouch_jump)
        self.restrict("Bottom Ring Armor", r.can_open | r.fast_crouch_jump)

        center_ring = self.region(
            "Center Top Ring",
            [
                "Center Ring RPG",
                "MP Center Ring Night Vision Goggles",
                "Center Ring Chaingun",
                "Center Ring Steroids",
                "Center Ring Pipebombs",
                "Center Ring Atomic Health",
                "MP Center Ring Jetpack",
                "Center Ring Shrinker",
                "Exit",
            ],
        )
        # can walk across a lizard trooper from the start
        self.connect(past_door, center_ring, r.jump | r.difficulty("medium"))
        self.restrict("Exit", r.can_use & (r.can_shrink | r.crouch_jump))

        center_top = self.region(
            "Center Top Platform",
            ["Center Top Atomic Health 1", "Center Top Atomic Health 2"],
        )
        self.connect(center_ring, center_top, r.jump)
        return ret
