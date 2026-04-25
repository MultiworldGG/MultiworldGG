from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L5(D3DLevel):
    name = "Movie Set"
    levelnum = 4
    volumenum = 2
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {
            "id": 0,
            "name": "Control Room Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 9, "name": "Moon Landing Atomic Health", "type": "sprite", "density": 1},
        {
            "id": 24,
            "name": "Vending Machine Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 39,
            "name": "Spacecraft Night Vision Goggles",
            "type": "sprite",
            "density": 1,
        },
        {"id": 40, "name": "Earth Vent Atomic Health", "type": "sprite", "density": 0},
        {"id": 41, "name": "Earth Jetpack", "type": "sprite", "density": 2},
        {"id": 43, "name": "3DRealms Freezethrower", "type": "sprite", "density": 2},
        {"id": 47, "name": "Subway Medkit", "type": "sprite", "density": 4},
        {"id": 51, "name": "3DRealms Atomic Health", "type": "sprite", "density": 4},
        {"id": 61, "name": "Studio Medkit", "type": "sprite", "density": 1},
        {"id": 71, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 80, "name": "Crate Atomic Health", "type": "sprite", "density": 1},
        {"id": 81, "name": "Crate Devastator", "type": "sprite", "density": 2},
        {"id": 105, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 170, "name": "Moon Landing Chaingun", "type": "sprite", "density": 4},
        {
            "id": 257,
            "name": "Beta Armor",
            "type": "sprite",
        },  # unreachable development room
        {"id": 258, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {
            "id": 261,
            "name": "Beta Holo Duke",
            "type": "sprite",
        },  # unreachable development room
        {"id": 267, "name": "Subway Shotgun", "type": "sprite", "density": 3},
        {"id": 268, "name": "Booth Medkit", "type": "sprite", "density": 1},
        {
            "id": 364,
            "name": "Spacecraft Wall Atomic Health",
            "type": "sprite",
            "density": 3,
        },
        {"id": 367, "name": "Spacecraft RPG", "type": "sprite", "density": 4},
        {"id": 371, "name": "Crash Site Steroids", "type": "sprite", "density": 1},
        {"id": 380, "name": "Studio Pipebombs", "type": "sprite", "density": 4},
        {"id": 415, "name": "Streets Pipebombs", "type": "sprite", "density": 3},
        {"id": 416, "name": "Control Room Tripmine 1", "type": "sprite", "density": 4},
        {"id": 417, "name": "Control Room Tripmine 2", "type": "sprite", "density": 4},
        {"id": 418, "name": "Earth Shrinker", "type": "sprite", "density": 4},
        {
            "id": 424,
            "name": "Vending Machine Atomic Health 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 425,
            "name": "Vending Machine Atomic Health 2",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 426,
            "name": "Vending Machine Atomic Health 3",
            "type": "sprite",
            "density": 4,
        },
        {"id": 480, "name": "Moon Landing Jetpack", "type": "sprite", "density": 4},
        {"id": 487, "name": "Subway Chaingun", "type": "sprite", "density": 0},
        {"id": 88, "name": "Secret Earth Screen", "type": "sector"},
        {"id": 149, "name": "Secret Crate", "type": "sector"},
        {"id": 183, "name": "Secret Vending Machine", "type": "sector"},
        {"id": 195, "name": "Secret 3DRealms", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
        {"id": 10, "name": "Secret Exit", "type": "exit"},
    ]
    events = ["Gate Control"]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Blue Key Card",
                "Subway Shotgun",
                "Streets Pipebombs",
                "Crash Site Steroids",
            ],
        )

        subway_entrance = self.region(
            "Subway Entrance", ["Exit", "Subway Medkit", "Subway Chaingun"]
        )
        # This is so easy I refuse to classify it as glitched
        self.connect(
            ret,
            subway_entrance,
            self.event("Gate Control")
            | (r.can_crouch & r.jump)
            | (r.jetpack(50) & r.can_crouch & r.difficulty("medium")),
        )
        self.restrict("Exit", r.can_use)

        start_ledges = self.region(
            "Outside Ledges",
            [
                "Booth Medkit",
                "Vending Machine Night Vision Goggles",
                "Secret 3DRealms",
                "3DRealms Freezethrower",
                "3DRealms Atomic Health",
            ],
        )
        self.connect(ret, start_ledges, r.jump)

        vending_machine = self.region(
            "Vending Machine",
            [
                "Secret Vending Machine",
                "Vending Machine Atomic Health 1",
                "Vending Machine Atomic Health 2",
                "Vending Machine Atomic Health 3",
            ],
        )
        self.connect(start_ledges, vending_machine, r.can_use)

        studio_floor_storage = self.region("Studio Floor Storage")
        # might be possible to do without steroids
        self.connect(
            ret,
            studio_floor_storage,
            (self.blue_key & r.can_open)
            | (
                r.glitched
                & r.difficulty("extreme")
                & r.fast_sprint
                & r.can_jump
                & r.tripmine
            ),
        )

        studio_floor_set = self.region(
            "Studio Floor Set",
            [
                "Yellow Key Card",
                "Moon Landing Chaingun",
                "Moon Landing Jetpack",
                "Studio Pipebombs",
                "Studio Medkit",
                "Secret Exit",
                "Moon Landing Atomic Health",
            ],
        )
        self.connect(
            ret,
            studio_floor_set,
            (r.glitched & r.difficulty("medium") & r.fast_sprint & r.can_crouch)
            | (
                r.glitched
                & r.difficulty("extreme")
                & r.fast_sprint
                & r.can_jump
                & r.tripmine
            ),
        )
        self.connect(studio_floor_set, studio_floor_storage, r.can_open | r.jetpack(50))
        self.connect(studio_floor_storage, studio_floor_set, r.can_open)
        self.restrict("Secret Exit", r.can_use)
        self.restrict("Moon Landing Atomic Health", r.jump)

        storage_ledges = self.region(
            "Studio Ledges",
            ["Crate Atomic Health"],
        )
        self.connect(studio_floor_storage, storage_ledges, r.jump)
        # can walk through vent
        self.connect(storage_ledges, studio_floor_set, r.true)

        storage_crate = self.region(
            "Storage Crate", ["Secret Crate", "Crate Devastator"]
        )
        self.connect(storage_ledges, storage_crate, r.can_open)

        space_craft = self.region(
            "Spacecraft Studio",
            [
                "Spacecraft Wall Atomic Health",
                "Spacecraft RPG",
                "Red Key Card",
                "Spacecraft Night Vision Goggles",
            ],
        )
        self.connect(
            studio_floor_storage,
            space_craft,
            (self.yellow_key & r.can_open)
            | (
                r.glitched
                & r.difficulty("extreme")
                & r.fast_sprint
                & r.can_jump
                & r.tripmine
            ),
        )

        earth_secret = self.region(
            "Behind the Earth Screen",
            [
                "Secret Earth Screen",
                "Earth Jetpack",
                "Earth Shrinker",
                "Earth Vent Atomic Health",
            ],
        )
        self.connect(space_craft, earth_secret, r.jump)
        self.restrict(
            "Earth Vent Atomic Health", r.can_jump & r.jetpack(50)
        )  # This has weird clipping stuff

        control_room = self.region("Subway Control Room", ["Gate Control"])
        self.connect(studio_floor_set, control_room, self.red_key & r.can_open)
        self.restrict("Gate Control", r.can_use)

        control_room_ledge = self.region(
            "Subway Control Room Ledge",
            [
                "Control Room Tripmine 1",
                "Control Room Tripmine 2",
                "Control Room Night Vision Goggles",
            ],
        )
        self.connect(control_room, control_room_ledge, r.jump)
        return ret
