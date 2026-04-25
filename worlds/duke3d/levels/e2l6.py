from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L6(D3DLevel):
    name = "Tiberius Station"
    levelnum = 5
    volumenum = 1
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 32, "name": "Timed Wall RPG", "type": "sprite", "density": 2},
        {
            "id": 42,
            "name": "Toxic Room Protective Boots",
            "type": "sprite",
            "density": 3,
        },
        {"id": 43, "name": "Toxic Room Scuba Gear", "type": "sprite", "density": 0},
        {
            "id": 45,
            "name": "Underwater Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 46, "name": "Underwater Medkit", "type": "sprite", "density": 4},
        {"id": 115, "name": "Toxic Room Wall Jetpack", "type": "sprite", "density": 2},
        {"id": 181, "name": "Supplies Medkit", "type": "sprite", "density": 2},
        {"id": 346, "name": "Supplies Armor 1", "type": "sprite", "density": 0},
        {"id": 347, "name": "Supplies Armor 2", "type": "sprite", "density": 3},
        {"id": 348, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {
            "id": 430,
            "name": "Water Fountain Pipebombs 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 431,
            "name": "Water Fountain Pipebombs 2",
            "type": "sprite",
            "density": 3,
        },
        {"id": 490, "name": "Armory Shrinker", "type": "sprite", "density": 0},
        {"id": 507, "name": "Timed Devastator", "type": "sprite", "density": 0},
        {"id": 508, "name": "Monitor Room Shotgun", "type": "sprite", "density": 3},
        {"id": 509, "name": "Monitor Room Holo Duke", "type": "sprite", "density": 0},
        {"id": 526, "name": "Corridor Wall Steroids", "type": "sprite", "density": 3},
        {"id": 527, "name": "Timed Room Atomic Health", "type": "sprite", "density": 0},
        {
            "id": 540,
            "name": "Toxic Alcove Atomic Health 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 541,
            "name": "Toxic Alcove Atomic Health 2",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 544,
            "name": "Corridor Wall Explosion RPG",
            "type": "sprite",
            "density": 0,
        },
        {"id": 545, "name": "Toxic Room Freezethrower", "type": "sprite", "density": 4},
        {"id": 549, "name": "Exit Vent Medkit", "type": "sprite", "density": 3},
        {"id": 551, "name": "Exit Room Chaingun", "type": "sprite", "density": 0},
        {"id": 567, "name": "Bathroom Tripmine 1", "type": "sprite", "density": 0},
        {"id": 568, "name": "Bathroom Tripmine 2", "type": "sprite", "density": 3},
        {
            "id": 607,
            "name": "Armory Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 608,
            "name": "Corridor Wall Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 609,
            "name": "MP Toilet Night Vision Goggles",
            "type": "sprite",
            "density": 5,
        },
        {"id": 610, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 67, "name": "Secret Toxic Alcove 1", "type": "sector"},
        {"id": 72, "name": "Secret Toxic Alcove 2", "type": "sector"},
        {"id": 136, "name": "Secret Corridor Wall", "type": "sector"},
        {"id": 145, "name": "Secret Toxic Room Wall", "type": "sector"},
        {"id": 166, "name": "Secret Water Fountain Wall", "type": "sector"},
        {"id": 258, "name": "Secret Supplies", "type": "sector"},
        {"id": 288, "name": "Secret Vent Wall Crack", "type": "sector"},
        {"id": 309, "name": "Secret Timed Wall", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    events = ["Explode Wall"]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(self.name, [])

        entry_room = self.region(
            "Entry Room",
            [
                "Water Fountain Pipebombs 1",
                "Water Fountain Pipebombs 2",
                "Secret Water Fountain Wall",
                "Blue Key Card",
                "Monitor Room Shotgun",
                "Secret Vent Wall Crack",
            ],
        )
        # sad, jetpack doesn't work
        self.connect(ret, entry_room, r.can_jump)
        self.restrict("Secret Vent Wall Crack", r.jump & r.explosives)

        l_armory = self.region(
            "Left Armory",
            [
                "Supplies Armor 1",
                "Supplies Armor 2",
                "Secret Supplies",
                "Supplies Medkit",
            ],
        )
        self.restrict("Secret Supplies", r.can_open)
        self.restrict("Supplies Medkit", r.can_open)

        r_armory = self.region(
            "Right Armory",
            [
                "Armory Shrinker",
                "Armory Night Vision Goggles",
            ],
        )

        self.connect(entry_room, l_armory, r.can_use)
        self.connect(entry_room, r_armory, r.can_use)

        corridor_wall = self.region(
            "Corridor Wall",
            [
                "Secret Corridor Wall",
                "Corridor Wall Steroids",
                "Corridor Wall Night Vision Goggles",
            ],
        )
        self.connect(
            entry_room,
            corridor_wall,
            r.can_open
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )
        self.restrict("Corridor Wall Steroids", r.jump)

        timed_room = self.region(
            "Timed Room", ["Timed Room Atomic Health", "Timed Devastator"]
        )
        self.connect(
            entry_room,
            timed_room,
            r.can_use
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )
        self.restrict("Timed Room Atomic Health", r.jump)

        early_ledges = self.region("Early Ledges", ["Monitor Room Holo Duke"])
        self.connect(entry_room, early_ledges, r.jump & r.can_crouch & r.can_open)

        past_door = self.region(
            "Past Door",
            [
                "Bathroom Tripmine 1",
                "Bathroom Tripmine 2",
                "MP Toilet Night Vision Goggles",
                "Corridor Wall Explosion RPG",
            ],
        )
        self.connect(entry_room, past_door, r.can_open)

        toxic_room = self.region(
            "Toxic Room",
            [
                "Toxic Room Protective Boots",
                "Toxic Room Scuba Gear",
                "Toxic Room Freezethrower",
            ],
        )
        self.connect(past_door, toxic_room, r.jump | self.blue_key)

        toxic_alcoves = self.region(
            "Toxic Alcoves",
            [
                "Toxic Alcove Atomic Health 1",
                "Toxic Alcove Atomic Health 2",
                "Secret Toxic Alcove 1",
                "Secret Toxic Alcove 2",
            ],
        )
        self.connect(toxic_room, toxic_alcoves, r.can_use | (r.jump & r.can_open))

        toxic_dive = self.region(
            "Toxic Dive",
            ["Underwater Night Vision Goggles", "Red Key Card", "Underwater Medkit"],
        )
        self.connect(toxic_room, toxic_dive, r.can_dive)

        toxic_room_wall = self.region(
            "Toxic Room Breakable Wall",
            ["Secret Toxic Room Wall", "Toxic Room Wall Jetpack", "Explode Wall"],
        )
        self.connect(toxic_room, toxic_room_wall, r.explosives)

        exit_vent = self.region("Exit Room Vent", ["Exit Vent Medkit"])
        self.connect(
            past_door, exit_vent, r.jetpack(50) | (r.difficulty("medium") & r.can_jump)
        )

        timed_wall = self.region(
            "Timed Wall Secret", ["Secret Timed Wall", "Timed Wall RPG"]
        )
        self.connect(
            exit_vent,
            timed_wall,
            r.jetpack(50) | (r.can_jump & self.event("Explode Wall")),
        )

        exit_room = self.region("Exit Room", ["Exit", "Exit Room Chaingun"])
        self.connect(toxic_room, exit_room, self.red_key)
        self.connect(exit_vent, exit_room, r.true)
        self.restrict("Exit", r.jump & r.can_use)
        return ret
