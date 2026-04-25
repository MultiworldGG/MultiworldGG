from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L7(D3DLevel):
    name = "Lunar Reactor"
    levelnum = 6
    volumenum = 1
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {"id": 5, "name": "Toilet Steroids", "type": "sprite", "density": 3},
        {
            "id": 39,
            "name": "Start Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 50,
            "name": "Trash Compactor Atomic Health 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 51,
            "name": "Trash Compactor Atomic Health 2",
            "type": "sprite",
            "density": 3,
        },
        {"id": 77, "name": "Reactor RPG", "type": "sprite", "density": 0},
        {"id": 78, "name": "Reactor Lookout Shotgun", "type": "sprite", "density": 0},
        {"id": 109, "name": "Canyon Cave Armor", "type": "sprite", "density": 3},
        {
            "id": 111,
            "name": "Canyon Cave Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 120, "name": "Toilet Tripmine", "type": "sprite", "density": 4},
        {"id": 128, "name": "Canyon Floor Jetpack", "type": "sprite", "density": 0},
        {"id": 129, "name": "Reactor Vent Pipebombs", "type": "sprite", "density": 4},
        {"id": 132, "name": "Slime Holo Duke", "type": "sprite", "density": 2},
        {"id": 142, "name": "Slime Freezethrower", "type": "sprite", "density": 0},
        {"id": 147, "name": "Luke Skywalker Shrinker", "type": "sprite", "density": 2},
        {"id": 148, "name": "Crew Quarters Tripmine", "type": "sprite", "density": 4},
        {"id": 149, "name": "Crew Quarters Armor", "type": "sprite", "density": 3},
        {"id": 154, "name": "Crew Quarters Pipebombs", "type": "sprite", "density": 4},
        {"id": 158, "name": "Blue Vent Atomic Health", "type": "sprite", "density": 3},
        {"id": 160, "name": "Crew Quarters Chaingun", "type": "sprite", "density": 0},
        {
            "id": 164,
            "name": "Yellow Door Vent Atomic Health",
            "type": "sprite",
            "density": 3,
        },
        {"id": 165, "name": "Toilet Medkit", "type": "sprite", "density": 3},
        {"id": 175, "name": "Vent Devastator", "type": "sprite", "density": 0},
        {"id": 213, "name": "Toilet RPG", "type": "sprite", "density": 4},
        {"id": 882, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 883, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 954, "name": "Start Shotgun", "type": "sprite", "density": 3},
        {"id": 983, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {
            "id": 992,
            "name": "Slime Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 994, "name": "Reactor Stairs Tripmine", "type": "sprite", "density": 4},
        {"id": 995, "name": "Reactor Lookout Tripmine", "type": "sprite", "density": 3},
        {
            "id": 1028,
            "name": "Reactor Lookout Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 1029,
            "name": "Reactor Ledge Tripmine 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 1030,
            "name": "Reactor Ledge Tripmine 2",
            "type": "sprite",
            "density": 3,
        },
        {"id": 1040, "name": "Slime Protective Boots", "type": "sprite", "density": 4},
        {"id": 1042, "name": "Reactor Atomic Health", "type": "sprite", "density": 0},
        {"id": 181, "name": "Secret Trash Compactor", "type": "sector"},
        {"id": 206, "name": "Secret Slime Monitors", "type": "sector"},
        {"id": 330, "name": "Secret Luke Skywalker", "type": "sector"},
        {"id": 387, "name": "Secret Canyon Cave", "type": "sector"},
        {"id": 390, "name": "Secret Canyon Monitors", "type": "sector"},
        {"id": 395, "name": "Secret Reactor Ledge 1", "type": "sector"},
        {"id": 396, "name": "Secret Reactor Ledge 2", "type": "sector"},
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
                "Start Night Vision Goggles",
                "Start Shotgun",
                "Toilet Medkit",
                "Toilet Steroids",
                "Toilet Tripmine",
                "Blue Key Card",
                "Toilet RPG",
                "Yellow Door Vent Atomic Health",
            ],
        )
        self.connect(ret, past_door, r.can_open)
        self.restrict("Yellow Door Vent Atomic Health", r.jump)

        start_vents = self.region("Vents", ["Vent Devastator"])
        # Can't actually get to the top section with just a jetpack except from the reactor core room
        self.connect(
            past_door, start_vents, r.can_jump | (r.jetpack(50) & self.yellow_key)
        )

        crew_quarters = self.region(
            "Crew Quarters",
            [
                "Blue Vent Atomic Health",
                "Crew Quarters Tripmine",
                "Crew Quarters Armor",
                "Crew Quarters Pipebombs",
                "Crew Quarters Chaingun",
                "Secret Canyon Monitors",
            ],
        )
        self.connect(past_door, crew_quarters, self.blue_key)
        self.restrict("Blue Vent Atomic Health", r.jump)

        luke_cave = self.region(
            "Hoth Cave",
            [
                "Secret Luke Skywalker",
                "Luke Skywalker Shrinker",
            ],
        )
        # can just walk off
        # medium diff because it requires diagonal strafe without sprint
        self.connect(
            crew_quarters,
            luke_cave,
            r.can_use & (r.difficulty("medium") | r.sprint),
        )

        crumbling_canyon = self.region("Crumbling Canyon", ["Yellow Key Card"])
        # teleport up
        self.connect(luke_cave, crumbling_canyon, r.true)

        canyon_vent = self.region("Canyon Vent", [])
        self.connect(crumbling_canyon, canyon_vent, r.true)

        trash_compactor = self.region(
            "Behind Trash Compactor",
            [
                "Secret Trash Compactor",
                "Trash Compactor Atomic Health 1",
                "Trash Compactor Atomic Health 2",
            ],
        )
        # timing is a bit tight without sprinting
        self.connect(
            crew_quarters,
            trash_compactor,
            r.can_use & (r.can_sprint | r.difficulty("medium")),
        )

        canyon_cave = self.region(
            "Canyon Cave",
            ["Secret Canyon Cave", "Canyon Cave Armor", "Canyon Cave Atomic Health"],
        )
        # Can jump from top of vent after yellow key card
        self.connect(crew_quarters, canyon_cave, r.jump)

        canyon_floor = self.region("Canyon Floor", ["Canyon Floor Jetpack"])
        # fall damage isn't a big deal from here, can't actually pick it up safely from anywhere else as
        # dying takes precendence over collecting the item
        # Jetpack has access to this cave so we don't need any other entrances to the bottom floor
        self.connect(luke_cave, canyon_floor, r.difficulty("medium") | r.jetpack(50))

        slime_room = self.region(
            "Slime Vat",
            [
                "Slime Night Vision Goggles",
                "Slime Freezethrower",
                "Slime Protective Boots",
                "Secret Slime Monitors",
                "Red Key Card",
                "Slime Holo Duke",
            ],
        )
        # Can't squeeze in with a jump
        self.connect(crew_quarters, slime_room, r.can_crouch)
        self.connect(past_door, slime_room, self.red_key)
        self.connect(slime_room, canyon_vent, r.can_crouch)
        # fly up inside the vent to get to the top, unlocking the full circle
        self.connect(canyon_vent, crew_quarters, r.jetpack(50))
        # Bit tricky
        self.connect(
            canyon_vent,
            crumbling_canyon,
            r.difficulty("medium") & (r.can_jump | r.can_sprint | r.steroids),
        )
        # Tricky air curl without sprint
        self.connect(
            crumbling_canyon,
            luke_cave,
            r.jump | r.can_sprint | r.steroids | r.difficulty("hard"),
        )

        reactor_core = self.region(
            "Reactor Core",
            [
                "Reactor Vent Pipebombs",
                "Reactor Stairs Tripmine",
                "Reactor Lookout Tripmine",
                "Reactor Lookout Shotgun",
                "Reactor Lookout Night Vision Goggles",
                "Reactor RPG",
                "Exit",
            ],
        )
        self.restrict("Reactor Vent Pipebombs", r.jump)
        self.restrict("Exit", r.can_use)

        self.connect(past_door, reactor_core, self.yellow_key)
        # Can get in through the vent
        self.connect(reactor_core, crew_quarters, r.jump)

        reactor_ledges = self.region(
            "Reactor Ledges",
            [
                "Secret Reactor Ledge 1",
                "Secret Reactor Ledge 2",
                "Reactor Ledge Tripmine 1",
                "Reactor Ledge Tripmine 2",
                "Reactor Atomic Health",
            ],
        )
        self.connect(reactor_core, reactor_ledges, r.jump)
        self.restrict("Reactor Atomic Health", r.can_use)

        return ret
