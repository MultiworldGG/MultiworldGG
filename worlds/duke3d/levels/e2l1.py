from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L1(D3DLevel):
    name = "Spaceport"
    levelnum = 0
    volumenum = 1
    keys = ["Blue", "Red"]
    location_defs = [
        {
            "name": "Underwater Night Vision Goggles",
            "id": 31,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Vent Pipebombs", "id": 40, "type": "sprite", "density": 2},
        {"name": "Elevator Armor", "id": 54, "type": "sprite", "density": 4},
        {"name": "Elevator Shrinker", "id": 58, "type": "sprite", "density": 2},
        {
            "name": "MP Elevator Corner Freezethrower",
            "id": 60,
            "type": "sprite",
            "density": 5,
        },
        {"name": "Middle Floor Jetpack", "id": 69, "type": "sprite", "density": 0},
        {
            "name": "Attic Night Vision Goggles",
            "id": 81,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Underwater Jetpack", "id": 110, "type": "sprite", "density": 2},
        {"name": "Bottom Floor Medkit", "id": 155, "type": "sprite", "density": 3},
        {"name": "Start Shotgun", "id": 156, "type": "sprite", "density": 1},
        {"name": "Bottom Floor Scuba Gear", "id": 165, "type": "sprite", "density": 4},
        {"name": "Blue Key Card", "id": 180, "type": "sprite", "density": 0},
        {"name": "Middle Floor Pipebombs", "id": 235, "type": "sprite", "density": 0},
        {
            "name": "Underwater Atomic Health 1",
            "id": 276,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Underwater Atomic Health 2",
            "id": 277,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Bottom Floor Armor", "id": 280, "type": "sprite", "density": 4},
        {"name": "Top Floor Atomic Health", "id": 289, "type": "sprite", "density": 4},
        {"name": "Red Key Card", "id": 318, "type": "sprite", "density": 0},
        {"name": "Bottom Floor Holo Duke", "id": 367, "type": "sprite", "density": 0},
        {"name": "Space Shuttle RPG", "id": 373, "type": "sprite", "density": 0},
        {"name": "Underwater Chaingun", "id": 374, "type": "sprite", "density": 2},
        {"name": "MP Attic Tripmine 1", "id": 385, "type": "sprite", "density": 5},
        {"name": "MP Attic Tripmine 2", "id": 386, "type": "sprite", "density": 5},
        {"name": "MP Attic Tripmine 3", "id": 387, "type": "sprite", "density": 5},
        {"name": "MP Start Armor", "id": 396, "type": "sprite", "density": 5},
        {"name": "Top Floor Devastator", "id": 399, "type": "sprite", "density": 2},
        {
            "name": "Middle Room Atomic Health",
            "id": 420,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Space Shuttle Steroids", "id": 422, "type": "sprite", "density": 3},
        {
            "name": "Monitor Wall Atomic Health",
            "id": 448,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Secret Top Floor", "id": 4, "type": "sector"},
        {"name": "Secret Timed Alcove", "id": 275, "type": "sector"},
        {"name": "Secret Elevator Corner", "id": 304, "type": "sector"},
        {"name": "Secret Ventilation Shaft", "id": 321, "type": "sector"},
        {"name": "Secret Shrinker Room", "id": 334, "type": "sector"},
        {"name": "Secret Monitor Wall", "id": 354, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Space Shuttle RPG",
                "Space Shuttle Steroids",
                "Start Shotgun",
            ],
        )

        monitor_secret = self.region(
            "Monitor Secret",
            [
                "Secret Monitor Wall",
                "Monitor Wall Atomic Health",
            ],
        )
        self.connect(ret, monitor_secret, r.can_open)

        timed_alcove_secret = self.region(
            "Timed Alcove",
            [
                "MP Start Armor",
                "Secret Timed Alcove",
            ],
        )
        self.connect(ret, timed_alcove_secret, r.jump)

        past_first_forcefield = self.region(
            "Past First Forcefield",
            [
                "Bottom Floor Holo Duke",
                "Bottom Floor Armor",
                "Bottom Floor Medkit",
                "Bottom Floor Scuba Gear",
                "Blue Key Card",
            ],
        )
        self.connect(ret, past_first_forcefield, r.can_use & r.can_open)

        start_ledges = self.region(
            "Early Ledges",
            [
                "Secret Ventilation Shaft",
                "Vent Pipebombs",
            ],
        )
        self.connect(past_first_forcefield, start_ledges, r.jump)

        hidden_water_passage = self.region(
            "Hidden Water Passage",
            ["Underwater Chaingun", "Underwater Night Vision Goggles"],
        )
        self.connect(
            past_first_forcefield, hidden_water_passage, r.can_dive & r.can_open
        )

        middle_floor = self.region(
            "Middle Floor",
            [
                "Middle Floor Pipebombs",
                "Exit",
                "Middle Floor Jetpack",
            ],
        )

        shrinker_secret = self.region(
            "Shrinker Secret",
            [
                "Secret Shrinker Room",
                "Elevator Shrinker",
                "Elevator Armor",
            ],
        )
        self.connect(middle_floor, shrinker_secret, r.can_open)

        self.connect(past_first_forcefield, middle_floor, self.blue_key & r.can_open)
        # Tripmine Clip + Glitch Kick can be used to get past the doors leading to the exit
        # Sadly need can_open to get to middle floor (for now)
        self.restrict("Exit", self.red_key & r.can_open & r.can_use)
        self.restrict("Middle Floor Jetpack", r.jump)

        middle_floor_ledge = self.region(
            "Middle Floor Jetpack Ledge",
            [
                "Middle Room Atomic Health",
                "Secret Elevator Corner",
                "MP Elevator Corner Freezethrower",
            ],
        )
        self.connect(middle_floor, middle_floor_ledge, r.jetpack(50) & r.can_open)

        pool = self.region(
            "Underwater Section",
            [
                "Red Key Card",
                "Underwater Jetpack",
                "Underwater Atomic Health 1",
                "Underwater Atomic Health 2",
            ],
        )
        # Need to get to the second floor to disable force field
        self.connect(middle_floor, pool, r.jump & r.can_dive & r.can_use)

        upper_floor = self.region(
            "Top Floor",
            ["Secret Top Floor", "Top Floor Atomic Health", "Top Floor Devastator"],
        )
        self.connect(middle_floor, upper_floor, r.jetpack(75) & r.can_use)

        attic = self.region(
            "Attic",
            [
                "MP Attic Tripmine 1",
                "MP Attic Tripmine 2",
                "MP Attic Tripmine 3",
                "Attic Night Vision Goggles",
            ],
        )
        self.connect(middle_floor, attic, r.jetpack(100) & r.can_use)

        return ret
