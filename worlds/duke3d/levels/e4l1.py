from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L1(D3DLevel):
    name = "It's Impossible"
    levelnum = 0
    volumenum = 3
    keys = ["Blue", "Red"]
    location_defs = [
        {
            "id": 4,
            "name": "Basement Container Tripmine 1",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 47,
            "name": "Kitchen Freezer Freezethrower",
            "type": "sprite",
            "density": 0,
        },
        {"id": 53, "name": "Cave Night Vision Goggles", "type": "sprite", "density": 3},
        {
            "id": 54,
            "name": "Upper Canyon Ledge Holo Duke",
            "type": "sprite",
            "density": 2,
        },
        {"id": 56, "name": "Red Basement Pipebombs", "type": "sprite", "density": 0},
        {"id": 135, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 136, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {
            "id": 149,
            "name": "Basement Container Tripmine 2",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 150,
            "name": "Basement Container Tripmine 3",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 151,
            "name": "Upper Canyon Ledge Pipebombs",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 152,
            "name": "MP Upper Canyon Ledge Steroids",
            "type": "sprite",
            "density": 5,
        },
        {"id": 170, "name": "Cave Atomic Health", "type": "sprite", "density": 2},
        {
            "id": 192,
            "name": "Final Doors Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 373, "name": "Upstairs Computer RPG", "type": "sprite", "density": 2},
        {"id": 407, "name": "Bathroom Secret Medkit", "type": "sprite", "density": 2},
        {"id": 419, "name": "Briefing Room Armor", "type": "sprite", "density": 3},
        {"id": 539, "name": "Briefing Room Shotgun", "type": "sprite", "density": 0},
        {"id": 540, "name": "Bathroom Chaingun", "type": "sprite", "density": 3},
        {
            "id": 544,
            "name": "MP Outside Area Ledge Shotgun",
            "type": "sprite",
            "density": 5,
        },
        {
            "id": 545,
            "name": "MP Outside Area Ledge Chaingun",
            "type": "sprite",
            "density": 5,
        },
        {"id": 562, "name": "Briefing Room Pipebombs", "type": "sprite", "density": 4},
        {
            "id": 563,
            "name": "Kitchen Conveyer Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 633, "name": "Kitchen Secret Shrinker", "type": "sprite", "density": 2},
        {"id": 634, "name": "Kitchen Secret Armor", "type": "sprite", "density": 2},
        {"id": 655, "name": "Final Doors Devastator", "type": "sprite", "density": 0},
        {"id": 674, "name": "Exit Pipebombs", "type": "sprite", "density": 0},
        {"id": 839, "name": "Barracks Bed Steroids", "type": "sprite", "density": 0},
        {"id": 840, "name": "Barracks Bed Jetpack", "type": "sprite", "density": 2},
        {"id": 116, "name": "Secret Upstairs Computer", "type": "sector"},
        {"id": 221, "name": "Secret Final Doors", "type": "sector"},
        {"id": 232, "name": "Secret Kitchen Freezer", "type": "sector"},
        {"id": 270, "name": "Secret Cave", "type": "sector"},
        {"id": 274, "name": "Secret Bathroom", "type": "sector"},
        {"id": 388, "name": "Secret Barracks Bed", "type": "sector"},
        {"id": 414, "name": "Secret Upper Canyon Ledge", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [],
        )
        inside = self.region(
            "Inside",
            [
                "Secret Barracks Bed",
                "Barracks Bed Steroids",
                "Barracks Bed Jetpack",
                "Bathroom Chaingun",
                "Kitchen Freezer Freezethrower",
                "Briefing Room Pipebombs",
                "Briefing Room Armor",
            ],
        )
        self.connect(ret, inside, r.can_open)

        kitchen_conveyer = self.region(
            "Behind Kitchen Conveyer",
            [
                "Kitchen Conveyer Atomic Health",
            ],
        )
        kitchen_secret = self.region(
            "Kitchen Secret Area",
            [
                "Secret Kitchen Freezer",
                "Kitchen Secret Armor",
            ],
        )
        self.connect(inside, kitchen_secret, r.can_use)
        self.connect(kitchen_secret, kitchen_conveyer, r.can_dive)

        upper_kitchen_secret = self.region(
            "Upper Kitchen Secret",
            [
                "Kitchen Secret Shrinker",
            ],
        )
        self.connect(kitchen_secret, upper_kitchen_secret, r.jump)
        # Door clipping strikes again
        self.connect(
            inside,
            kitchen_conveyer,
            r.jump | r.difficulty("hard"),
        )
        # Can just jump through the wall from outside, hard because obscure
        self.connect(
            ret,
            kitchen_conveyer,
            (r.glitched & r.fast_sprint & r.can_jump & r.difficulty("hard")),
        )

        canyon_ledge = self.region(
            "Canyon Ledge",
            [
                "MP Outside Area Ledge Shotgun",
                "MP Outside Area Ledge Chaingun",
            ],
        )
        self.connect(ret, canyon_ledge, r.jump | r.can_open)

        upper_canyon = self.region(
            "Upper Canyon Ledge",
            [
                "MP Upper Canyon Ledge Steroids",
                "Upper Canyon Ledge Holo Duke",
                "Upper Canyon Ledge Pipebombs",
                "Secret Upper Canyon Ledge",
            ],
        )
        self.connect(canyon_ledge, upper_canyon, r.jump)

        dark_cave = self.region(
            "Dark Cave",
            [
                "Secret Cave",
                "Cave Night Vision Goggles",
                "Cave Atomic Health",
            ],
        )
        self.connect(canyon_ledge, dark_cave, r.can_use)

        bathroom_key = self.region(
            "Bathroom Key Card",
            [
                "Blue Key Card",
            ],
        )
        # Door Clipping never stops, also possible to walk up
        self.connect(inside, bathroom_key, r.jump | r.difficulty("hard"))

        behind_desk = self.region(
            "Behind Briefing Room Desk",
            [
                "Briefing Room Shotgun",
            ],
        )
        # Can walk over the desk with precise diagonal movement, hard because obscure
        self.connect(inside, behind_desk, r.jump | r.difficulty("hard"))

        bathroom_secret = self.region(
            "Bathroom Secret Region",
            [
                "Secret Bathroom",
                "Bathroom Secret Medkit",
            ],
        )
        self.connect(inside, bathroom_secret, r.fast_crouch_jump | (r.jump & r.can_use))

        basement_container = self.region(
            "Basement Container",
            [
                "Basement Container Tripmine 1",
                "Basement Container Tripmine 2",
                "Basement Container Tripmine 3",
            ],
        )
        # Door clipping on top of the container and SR50
        self.connect(inside, basement_container, r.jump | r.difficulty("hard"))

        blue_key_area = self.region(
            "Blue Key Room",
            [
                "Red Key Card",
                "Secret Upstairs Computer",
                "Upstairs Computer RPG",
            ],
        )
        self.connect(
            inside,
            blue_key_area,
            self.blue_key
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        janitor_closet = self.region(
            "Janitor Closet",
            [
                "Red Basement Pipebombs",
            ],
        )
        self.connect(
            inside,
            janitor_closet,
            self.red_key
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        mission_impossible = self.region(
            "Mission Impossible Room",
            [
                "Final Doors Devastator",
            ],
        )
        secret_cc = self.region(
            "Secret Cable Car",
            [
                "Secret Final Doors",
                "Final Doors Atomic Health",
            ],
        )
        # Triggering the tripmines requires 100 health and precise movement
        # Without saving this would probably need to be extreme logic
        self.connect(
            janitor_closet,
            mission_impossible,
            r.jump & r.can_use & (r.explosives | (r.sprint & r.difficulty("hard"))),
        )
        # Alternate path by jump-crouching near elevator by briefing room
        self.connect(
            inside,
            mission_impossible,
            (r.difficulty("hard") & r.fast_crouch_jump),
        )
        self.connect(
            mission_impossible, secret_cc, r.can_use | (r.can_crouch & r.fast_sprint)
        )

        exit_region = self.region(
            "Exit Region",
            [
                "Exit Pipebombs",
                "Exit",
            ],
        )
        # The pipebomb on the ground at the cracked door can be shot for a free explosion
        self.connect(
            mission_impossible,
            exit_region,
            r.can_open & (r.explosives | r.difficulty("medium")),
        )
        self.restrict("Exit", r.can_use)
        return ret
