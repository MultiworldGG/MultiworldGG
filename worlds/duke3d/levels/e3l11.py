from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L11(D3DLevel):
    name = "Freeway"
    levelnum = 10
    volumenum = 2
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 20, "name": "Conveyor Control Armor", "type": "sprite", "density": 4},
        {
            "id": 21,
            "name": "Conveyor Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 24, "name": "Streets Pipebombs", "type": "sprite", "density": 4},
        {"id": 33, "name": "Underwater Shotgun", "type": "sprite", "density": 3},
        {"id": 61, "name": "Sewer Tripmine 1", "type": "sprite", "density": 4},
        {"id": 62, "name": "Sewer Tripmine 2", "type": "sprite", "density": 4},
        {"id": 72, "name": "Streets Steroids", "type": "sprite", "density": 3},
        {"id": 73, "name": "Ledge Steroids", "type": "sprite", "density": 3},
        {
            "id": 81,
            "name": "Conveyor Control Pipebombs",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 210,
            "name": "Trashcan Atomic Health",
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 4,
        },
        {"id": 211, "name": "Toppled Building Jetpack", "type": "sprite", "density": 0},
        {
            "id": 304,
            "name": "Trashcan Shotgun",
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 3,
        },
        {"id": 361, "name": "Underwater RPG", "type": "sprite", "density": 0},
        {"id": 363, "name": "Underwater Atomic Health", "type": "sprite", "density": 1},
        {"id": 364, "name": "Sewer Armor", "type": "sprite", "density": 1},
        {"id": 366, "name": "Streets Devastator", "type": "sprite", "density": 0},
        {"id": 367, "name": "Ledge Medkit", "type": "sprite", "density": 1},
        {
            "id": 372,
            "name": "Ledge Night Vision Goggles",
            "type": "sprite",
            "density": 1,
        },
        {
            "id": 376,
            "name": "Office Ledge Atomic Health 1",
            "type": "sprite",
            "density": 1,
        },
        {
            "id": 377,
            "name": "Office Ledge Atomic Health 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 378, "name": "Streets Medkit", "type": "sprite", "density": 4},
        {"id": 379, "name": "Streets Armor", "type": "sprite", "density": 1},
        {"id": 381, "name": "Office Chaingun", "type": "sprite", "density": 2},
        {"id": 384, "name": "Office Pipebombs", "type": "sprite", "density": 3},
        {"id": 386, "name": "Terminator RPG", "type": "sprite", "density": 1},
        {"id": 387, "name": "Conveyor Freezethrower", "type": "sprite", "density": 4},
        {"id": 388, "name": "Bedroom Shrinker", "type": "sprite", "density": 2},
        {"id": 390, "name": "Bathroom Freezethrower", "type": "sprite", "density": 2},
        {"id": 394, "name": "Dumpster Shotgun", "type": "sprite", "density": 3},
        {"id": 399, "name": "MP Underwater Jetpack", "type": "sprite", "density": 5},
        {"id": 463, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 465, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 120, "name": "Secret Bookshelf", "type": "sector"},
        {"id": 148, "name": "Secret Office Spawn Room", "type": "sector"},
        {"id": 229, "name": "Secret Conveyor Control Room", "type": "sector"},
        {"id": 242, "name": "Secret Bedroom Window", "type": "sector"},
        {"id": 246, "name": "Secret Bathroom", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(self.name, [])

        sewer = self.region(
            "Sewer",
            [
                "Underwater Shotgun",
                "Underwater RPG",
                "Sewer Tripmine 1",
                "Sewer Tripmine 2",
                "Sewer Armor",
            ],
        )
        self.connect(ret, sewer, r.can_dive)

        sewer_crack = self.region(
            "Sewer Crack", ["MP Underwater Jetpack", "Underwater Atomic Health"]
        )
        self.connect(sewer, sewer_crack, r.explosives)

        streets = self.region(
            "Streets",
            [
                "Trashcan Atomic Health",
                "Trashcan Shotgun",
                "Streets Devastator",
                "Streets Medkit",
                "Streets Pipebombs",
                "Streets Steroids",
                "Streets Armor",
                "Dumpster Shotgun",
                "Exit",
            ],
        )
        self.connect(sewer, streets, r.jump | r.explosives)
        self.restrict("Exit", self.red_key & r.can_open)

        streets_far_ledge = self.region("High Ledge", ["Ledge Steroids"])
        # enemy jump
        self.connect(
            streets,
            streets_far_ledge,
            r.jetpack(50) | (r.difficulty("medium") & r.can_jump),
        )

        streets_explosive_ledge = self.region("Exploding Ledge", ["Ledge Medkit"])
        self.connect(
            streets,
            streets_explosive_ledge,
            r.jetpack(50) | (r.can_jump & (r.explosives | r.difficulty("medium"))),
        )

        streets_easy_ledge = self.region("Easy Ledge", ["Ledge Night Vision Goggles"])
        self.connect(streets, streets_easy_ledge, r.jump)

        toppled_building = self.region("Toppled Building", ["Toppled Building Jetpack"])
        self.connect(streets, toppled_building, r.jump)

        hidden_bedroom = self.region(
            "Hidden Bedroom", ["Secret Bedroom Window", "Bedroom Shrinker"]
        )
        self.connect(
            streets,
            hidden_bedroom,
            r.jump & (r.can_open | r.glitched & r.can_crouch & r.fast_sprint),
        )

        hidden_bathroom = self.region(
            "Hidden Bathroom", ["Secret Bathroom", "Bathroom Freezethrower"]
        )
        self.connect(hidden_bedroom, hidden_bathroom, r.explosives)
        self.connect(
            streets_explosive_ledge,
            hidden_bathroom,
            r.jump & (r.can_open | r.glitched & r.can_crouch & r.fast_sprint),
        )

        conveyor_room = self.region(
            "Conveyor Room",
            [
                "Conveyor Night Vision Goggles",
                "Secret Conveyor Control Room",
                "Conveyor Control Pipebombs",
                "Conveyor Control Armor",
                "Red Key Card",
                "Conveyor Freezethrower",
                "Terminator RPG",
            ],
        )
        self.connect(
            streets, conveyor_room, (self.blue_key & r.can_open) | r.jetpack(50)
        )
        self.restrict("Terminator RPG", r.can_crouch)

        office = self.region(
            "Office Building",
            [
                "Blue Key Card",
                "Office Pipebombs",
                "Secret Bookshelf",
                "Office Ledge Atomic Health 1",
                "Office Ledge Atomic Health 2",
            ],
        )
        # can just walk off
        self.connect(toppled_building, office, r.true)
        self.restrict("Office Pipebombs", r.jump)
        self.restrict("Secret Bookshelf", r.can_crouch & r.can_open)

        spawn_room = self.region(
            "Office Spawn Room", ["Secret Office Spawn Room", "Office Chaingun"]
        )
        self.connect(office, spawn_room, r.explosives)

        return ret
