from BaseClasses import Region

from ..base_classes import D3DLevel


# I Hope I have all of the basic vertical transitions covered
class E3L4(D3DLevel):
    name = "L.A. Rumble"
    levelnum = 3
    volumenum = 2
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 59, "name": "Red Key Card", "type": "sprite", "density": 0},
        {
            "id": 82,
            "name": "Abortion Clinic Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 114, "name": "Billboard Shrinker", "type": "sprite", "density": 3},
        {"id": 135, "name": "Elevator Lobby Medkit", "type": "sprite", "density": 0},
        {
            "id": 136,
            "name": "Elevator Shaft Devastator",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 137,
            "name": "Abortion Clinic Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 244, "name": "Abortion Clinic Steroids", "type": "sprite", "density": 1},
        {"id": 247, "name": "MP Streets Shotgun", "type": "sprite", "density": 5},
        {"id": 248, "name": "Hooker Pipebombs", "type": "sprite", "density": 0},
        {"id": 274, "name": "Street Ledge Chaingun", "type": "sprite", "density": 4},
        {"id": 275, "name": "Streets Shotgun", "type": "sprite", "density": 3},
        {"id": 276, "name": "Office RPG", "type": "sprite", "density": 3},
        {
            "id": 277,
            "name": "Billboard Atomic Health 1",
            "type": "sprite",
            "density": 0,
        },
        {"id": 283, "name": "Street Ledge RPG", "type": "sprite", "density": 0},
        {
            "id": 336,
            "name": "Billboard Atomic Health 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 339, "name": "Office Jetpack", "type": "sprite", "density": 4},
        {"id": 391, "name": "Tower Top Medkit", "type": "sprite", "density": 1},
        {"id": 442, "name": "Sewer Pipebombs", "type": "sprite", "density": 1},
        {"id": 458, "name": "Street Ledge Armor", "type": "sprite", "density": 1},
        {"id": 468, "name": "Office Holo Duke", "type": "sprite", "density": 1},
        {"id": 475, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 500, "name": "MP Billboard Jetpack", "type": "sprite", "density": 5},
        {"id": 501, "name": "MP Street Ledge Jetpack", "type": "sprite", "density": 5},
        {"id": 502, "name": "MP Tower Top RPG", "type": "sprite", "density": 5},
        {"id": 503, "name": "MP Elevator Top Chaingun", "type": "sprite", "density": 5},
        {
            "id": 506,
            "name": "Sewer Walls Freezethrower",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 507,
            "name": "MP Abortion Clinic Atomic Health",
            "type": "sprite",
            "density": 5,
        },
        {
            "id": 508,
            "name": "MP Abortion Clinic Jetpack",
            "type": "sprite",
            "density": 5,
        },
        {
            "id": 509,
            "name": "MP Abortion Clinic Pipebombs",
            "type": "sprite",
            "density": 5,
        },
        {"id": 511, "name": "Street Ledge Tripmine 1", "type": "sprite", "density": 4},
        {"id": 512, "name": "Street Ledge Tripmine 2", "type": "sprite", "density": 4},
        {
            "id": 513,
            "name": "Streets Ledge Freezethrower",
            "type": "sprite",
            "density": 1,
        },
        {"id": 515, "name": "Street Ledge Medkit", "type": "sprite", "density": 3},
        {"id": 166, "name": "Secret Sewer Walls", "type": "sector"},
        {"id": 195, "name": "Secret Office Painting", "type": "sector"},
        {"id": 205, "name": "Secret Abortion Clinic Counter", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Sewer Pipebombs",
                "Streets Shotgun",
                "MP Streets Shotgun",
                "Hooker Pipebombs",
                "Abortion Clinic Night Vision Goggles",
                "MP Abortion Clinic Atomic Health",
                "MP Abortion Clinic Jetpack",
                "MP Abortion Clinic Pipebombs",
                "Abortion Clinic Steroids",
                "Blue Key Card",
            ],
        )
        self.restrict("Abortion Clinic Steroids", r.can_open)

        abortion_secret = self.region(
            "Abortion Clinic Secret",
            ["Secret Abortion Clinic Counter", "Abortion Clinic Atomic Health"],
        )
        # can pick up the item without, but I don't think you can activate the switch without crouch
        self.connect(ret, abortion_secret, r.can_crouch & r.can_use)

        sewer_walls = self.region(
            "Sewer Walls", ["Secret Sewer Walls", "Sewer Walls Freezethrower"]
        )
        self.connect(ret, sewer_walls, r.explosives)

        lower_ledges = self.region(
            "Lower Street Ledges",
            [
                "Street Ledge RPG",
                "Street Ledge Chaingun",
                "Street Ledge Medkit",
                "MP Street Ledge Jetpack",
            ],
        )
        self.connect(sewer_walls, lower_ledges, r.jump)
        self.connect(ret, lower_ledges, r.jetpack(50))

        billboard_lower_ledge = self.region(
            "Billboard Building Lower Ledge",
            [
                "Street Ledge Tripmine 1",
                "Street Ledge Tripmine 2",
                "Street Ledge Armor",
            ],
        )
        self.connect(ret, billboard_lower_ledge, r.jump)
        self.connect(lower_ledges, billboard_lower_ledge, r.true)

        side_ledge = self.region("Streets Side Ledge", ["Streets Ledge Freezethrower"])
        self.connect(
            ret, side_ledge, r.jetpack(50) | (r.difficulty("medium") & r.can_jump)
        )

        tower_lobby = self.region(
            "Tower Lobby", ["Elevator Lobby Medkit", "Elevator Shaft Devastator"]
        )
        self.connect(
            ret, tower_lobby, (self.blue_key & r.can_open) | (r.jump & r.explosives)
        )  # Might be able to wiggle up without jump somehow

        tower = self.region(
            "Tall Tower",
            [
                "MP Elevator Top Chaingun",
                "MP Tower Top RPG",
                "Tower Top Medkit",
            ],
        )
        self.connect(ret, tower, r.jetpack(100))
        self.connect(tower_lobby, tower, r.can_open)
        # Not a lot of fall damage going down, just have to aim to not be stuck in the shaft
        self.connect(tower, tower_lobby, r.true)
        self.connect(tower, side_ledge, r.true)
        self.connect(tower, lower_ledges, r.sprint | r.jump)
        self.connect(tower, billboard_lower_ledge, r.sprint | r.jump)

        # Every way of getting to this can also trigger the explosion
        broken_billboard = self.region(
            "Broken Billboard Building",
            [
                "Billboard Atomic Health 1",
                "Billboard Atomic Health 2",
                "Billboard Shrinker",
                "MP Billboard Jetpack",
            ],
        )
        self.connect(tower, broken_billboard, r.can_jump | r.sprint)
        self.connect(ret, broken_billboard, r.jetpack(100) | r.crouch_jump)
        self.restrict("Billboard Shrinker", r.can_jump | r.jetpack(100))

        office_building = self.region(
            "Office Building",
            [
                "Office Holo Duke",
                "Office RPG",
                "Office Jetpack",
                "Secret Office Painting",
                "Red Key Card",
                "Exit",
            ],
        )
        self.connect(broken_billboard, office_building, r.can_jump)
        self.connect(ret, office_building, r.jetpack(100))
        self.restrict("Exit", self.red_key & r.can_open)
        # Even SR50 + sprint doesn't seem fast enough to not get squished
        self.restrict(
            "Secret Office Painting",
            (
                (r.can_jump | r.jetpack(100))
                & (r.can_open | (r.glitched & r.fast_sprint & r.can_crouch))
            ),
        )
        self.restrict("Red Key Card", r.can_jump | r.jetpack(100))

        return ret
