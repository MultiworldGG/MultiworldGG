from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L5(D3DLevel):
    name = "Occupied Territory"
    levelnum = 4
    volumenum = 1
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 71, "name": "Vent RPG", "type": "sprite", "density": 2},
        {"id": 85, "name": "Vent Armor", "type": "sprite", "density": 4},
        {
            "id": 90,
            "name": "MP Center Room Freezethrower",
            "type": "sprite",
            "density": 5,
        },
        {"id": 94, "name": "Slime Room Pipebombs 1", "type": "sprite", "density": 3},
        {"id": 95, "name": "Monitors Tripmine 1", "type": "sprite", "density": 3},
        {"id": 96, "name": "Monitors Tripmine 2", "type": "sprite", "density": 4},
        {"id": 97, "name": "MP Center Room Pipebombs", "type": "sprite", "density": 5},
        {"id": 110, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 299, "name": "Red Key Card", "type": "sprite", "density": 0},
        {
            "id": 317,
            "name": "Blastdoor Hole Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 346, "name": "Slime Room Devastator", "type": "sprite", "density": 0},
        {"id": 365, "name": "Start Chaingun", "type": "sprite", "density": 0},
        {"id": 366, "name": "Start Medkit", "type": "sprite", "density": 4},
        {"id": 367, "name": "Corridor Holo Duke", "type": "sprite", "density": 0},
        {"id": 369, "name": "MP Battlelord Shrinker", "type": "sprite", "density": 5},
        {"id": 370, "name": "Center Room Medkit", "type": "sprite", "density": 0},
        {"id": 372, "name": "Start Shotgun", "type": "sprite", "density": 3},
        {"id": 373, "name": "Ramp Steroids", "type": "sprite", "density": 4},
        {"id": 376, "name": "MP Large Door Jetpack", "type": "sprite", "density": 5},
        {"id": 377, "name": "Slime Room Pipebombs 2", "type": "sprite", "density": 4},
        {"id": 378, "name": "Monitors Atomic Health", "type": "sprite", "density": 2},
        {
            "id": 384,
            "name": "Hallway Alcove Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 386, "name": "MP Exit RPG", "type": "sprite", "density": 5},
        {
            "id": 426,
            "name": "Ramp Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 427,
            "name": "Slime Room Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 428,
            "name": "Large Door Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 429, "name": "Start Armor", "type": "sprite", "density": 4},
        {"id": 136, "name": "Secret Hallway Alcove", "type": "sector"},
        {"id": 185, "name": "Secret Blastdoor Hole", "type": "sector"},
        {"id": 225, "name": "Secret Vent", "type": "sector"},
        {"id": 238, "name": "Secret Monitors", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
        {"id": 10, "name": "Secret Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Start Shotgun",
                "Start Chaingun",
                "Start Armor",
                "Start Medkit",
            ],
        )

        past_door = self.region(
            "Past Door",
            [
                "Secret Vent",
                "Vent RPG",
                "Vent Armor",
                "Corridor Holo Duke",
                "Large Door Night Vision Goggles",
                "MP Large Door Jetpack",
                "Ramp Steroids",
                "Ramp Night Vision Goggles",
                "Slime Room Pipebombs 1",
                "Slime Room Pipebombs 2",
                "Slime Room Devastator",
                "Red Key Card",
                "Slime Room Night Vision Goggles",
            ],
        )
        self.connect(ret, past_door, r.can_open)

        blastdoor_secret = self.region(
            "Blastdoor Hole", ["Secret Blastdoor Hole", "Blastdoor Hole Atomic Health"]
        )
        # can't get a clip with only jetpack to work
        self.connect(
            ret, blastdoor_secret, r.can_crouch | (r.can_jump & r.difficulty("medium"))
        )

        hallway_alcove = self.region(
            "Hallway Drone Alcove",
            ["Secret Hallway Alcove", "Hallway Alcove Atomic Health"],
        )
        self.connect(
            past_door,
            hallway_alcove,
            r.jetpack(50)
            | r.can_jump & (r.difficulty("hard") | r.can_sprint & r.steroids),
        )

        battlelord_room = self.region(
            "Battlelord Chamber", ["MP Battlelord Shrinker", "Blue Key Card"]
        )
        self.connect(past_door, battlelord_room, self.red_key)

        battlelord_monitors = self.region(
            "Behind Monitors",
            [
                "Monitors Tripmine 1",
                "Monitors Tripmine 2",
                "Monitors Atomic Health",
                "Secret Monitors",
            ],
        )
        # Can just jump through the left two-way monitor to enter
        self.connect(
            battlelord_room,
            battlelord_monitors,
            (r.jump & (r.difficulty("medium") | r.can_crouch)),
        )

        center_room = self.region(
            "Center Room", ["MP Center Room Freezethrower", "Center Room Medkit"]
        )
        self.connect(
            past_door,
            center_room,
            self.blue_key | (r.glitched & r.can_crouch & r.steroids),
        )

        center_room_top = self.region(
            "Center Room Top", ["MP Center Room Pipebombs", "MP Exit RPG", "Exit"]
        )
        # Can hop onto an enemy jumping off the ledge, but this is giga cursed to time
        # center_room_top: (r.difficulty("extreme") & r.can_jump)
        # secret_exit: (r.difficulty("hard") & r.can_jump)
        self.connect(
            center_room,
            center_room_top,
            self.blue_key | r.jetpack(50),
        )

        secret_exit = self.region("Secret Exit Area", ["Secret Exit"])
        self.connect(
            center_room,
            secret_exit,
            r.jetpack(50),
        )
        #
        self.connect(
            center_room_top,
            secret_exit,
            r.jetpack(50)
            # jump without sprint is very precise
            | (r.jump & (r.difficulty("medium") | r.can_sprint))
            | (r.can_sprint & r.steroids),
        )
        self.restrict("Secret Exit", r.can_use)
        self.restrict("Exit", r.can_use)
        return ret
