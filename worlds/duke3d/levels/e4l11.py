from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L11(D3DLevel):
    name = "Area 51"
    levelnum = 10
    volumenum = 3
    keys = ["Red", "Blue", "Yellow"]
    location_defs = [
        {"id": 50, "name": "UFO Atomic Health", "type": "sprite", "density": 2},
        {"id": 90, "name": "Vent Entrance Pipebombs", "type": "sprite", "density": 3},
        {"id": 94, "name": "MP Outside Pipebombs", "type": "sprite", "density": 5},
        {"id": 109, "name": "MP Blue Chaingun", "type": "sprite", "density": 5},
        {"id": 112, "name": "MP Red Steroids", "type": "sprite", "density": 5},
        {"id": 198, "name": "Elevator Drop Devastator", "type": "sprite", "density": 3},
        {
            "id": 234,
            "name": "Cave Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 252,
            "name": "Blue Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 254, "name": "Outside Pipebombs", "type": "sprite", "density": 0},
        {"id": 258, "name": "Crate Holo Duke", "type": "sprite", "density": 0},
        {"id": 275, "name": "Lake Pipebombs", "type": "sprite", "density": 2},
        {"id": 294, "name": "Blue Tripmine 1", "type": "sprite", "density": 0},
        {"id": 295, "name": "Blue Tripmine 2", "type": "sprite", "density": 3},
        {"id": 297, "name": "Blue Holo Duke", "type": "sprite", "density": 0},
        {"id": 298, "name": "Symbol Atomic Health", "type": "sprite", "density": 2},
        {"id": 299, "name": "Corner Steroids", "type": "sprite", "density": 2},
        {"id": 300, "name": "Blue Tripmine 3", "type": "sprite", "density": 4},
        {"id": 301, "name": "Blue Medkit", "type": "sprite", "density": 0},
        {"id": 302, "name": "MP Freezer Atomic Health", "type": "sprite", "density": 5},
        {"id": 304, "name": "Crate Armor", "type": "sprite", "density": 3},
        {"id": 306, "name": "Tele Cave Shotgun", "type": "sprite", "density": 0},
        {
            "id": 308,
            "name": "Vent Secret Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 311, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 335, "name": "Bunker Chaingun", "type": "sprite", "density": 0},
        {"id": 469, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 513, "name": "Vent Entrance Armor", "type": "sprite", "density": 0},
        {"id": 558, "name": "Conveyer Jetpack", "type": "sprite", "density": 0},
        {"id": 560, "name": "Conveyer Shrinker", "type": "sprite", "density": 3},
        {"id": 561, "name": "MP Cave Jetpack", "type": "sprite", "density": 5},
        {"id": 568, "name": "Bridge RPG", "type": "sprite", "density": 2},
        {"id": 584, "name": "Red Shotgun", "type": "sprite", "density": 3},
        {"id": 610, "name": "Elevator Drop Medkit", "type": "sprite", "density": 0},
        {"id": 637, "name": "Crate Scuba Gear", "type": "sprite", "density": 2},
        {"id": 656, "name": "Table Freezethrower", "type": "sprite", "density": 0},
        {"id": 690, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 50, "name": "Secret Symbol", "type": "sector"},
        {"id": 54, "name": "Secret Corner", "type": "sector"},
        {"id": 82, "name": "Secret Crate", "type": "sector"},
        {"id": 293, "name": "Secret Vent", "type": "sector"},
        {"id": 337, "name": "Secret Bridge", "type": "sector"},
        {"id": 440, "name": "Secret Lake", "type": "sector"},
        {"id": 574, "name": "Secret UFO", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "MP Outside Pipebombs",
                "Outside Pipebombs",
            ],
        )

        second_area = self.region(
            "Second Area",
            [
                "Bunker Chaingun",
            ],
        )
        # Can hop on troopers to get into the bunker
        self.connect(
            ret,
            second_area,
            r.jetpack(50)
            | (r.explosives & r.can_open)
            | (r.can_jump & r.difficulty("hard")),
        )

        bridge_secret = self.region(
            "Secret Bridge",
            [
                "Secret Bridge",
                "Bridge RPG",
            ],
        )
        # Can also get here from lake secret
        self.connect(second_area, bridge_secret, r.jetpack(50))

        cave = self.region(
            "Cave",
            [
                "MP Cave Jetpack",
                "Cave Night Vision Goggles",
            ],
        )
        self.connect(second_area, cave, r.jump)

        vent_entrance = self.region(
            "Vent Entrance",
            [
                "Vent Entrance Pipebombs",
                "Blue Key Card",
                "Tele Cave Shotgun",  # Can get this from outside
                "Vent Entrance Armor",
            ],
        )
        self.restrict("Vent Entrance Pipebombs", r.can_use)
        self.restrict("Blue Key Card", r.can_use)
        self.restrict(
            "Tele Cave Shotgun",
            r.can_use | r.jetpack(50) | (r.sprint & r.can_jump & r.difficulty("hard")),
        )
        self.connect(second_area, vent_entrance, r.jump)

        vent_secret = self.region(
            "Secret Vent",
            [
                "Secret Vent",
                "Vent Secret Atomic Health",
            ],
        )
        # 50ish for the vent and 25 for the no jump entrance to here
        self.connect(vent_entrance, vent_secret, r.jetpack(75) & r.can_use),

        blue_key_area = self.region(
            "Blue Key Area",
            [
                "Blue Tripmine 1",
                "Blue Tripmine 2",
                "Blue Tripmine 3",
                "Blue Night Vision Goggles",
                "MP Blue Chaingun",
            ],
        )
        self.restrict("Blue Tripmine 1", r.can_open | r.crouch_jump)
        self.restrict("Blue Tripmine 2", r.can_open | r.crouch_jump)
        self.restrict("Blue Tripmine 3", r.can_open | r.crouch_jump)
        self.restrict(
            "Blue Night Vision Goggles",
            r.can_open
            | (
                r.difficulty("extreme")
                & r.glitched
                & r.can_jump
                & r.fast_sprint
                & r.tripmine
            ),
        )
        self.restrict(
            "MP Blue Chaingun",
            r.can_open
            | (
                r.difficulty("extreme")
                & r.glitched
                & r.can_jump
                & r.fast_sprint
                & r.tripmine
            ),
        )
        # Clip through wall where sectors overlap or tripclip blue door
        self.connect(
            second_area,
            blue_key_area,
            (self.blue_key & r.can_open)
            | (
                r.difficulty("hard")
                & r.glitched
                & r.can_crouch
                & r.steroids
                & r.can_sprint
            )
            | (
                r.difficulty("extreme")
                & r.glitched
                & r.can_jump
                & r.fast_sprint
                & r.tripmine
            ),
        )

        blue_upper = self.region(
            "Blue Upper Area",
            [
                "Secret Symbol",
                "Symbol Atomic Health",
                "Secret Corner",
                "Corner Steroids",
                "Blue Holo Duke",
            ],
        )
        self.restrict("Secret Corner", r.can_open)
        self.restrict("Corner Steroids", r.can_open)
        # jetpack can't get onto the ledge for the trigger
        self.connect(
            blue_key_area,
            blue_upper,
            r.can_jump
            & (
                r.can_open
                | (
                    r.difficulty("extreme")
                    & r.glitched
                    & r.can_jump
                    & r.fast_sprint
                    & r.tripmine
                )
            ),
        )

        hidden_wall = self.region(
            "Blue Hidden Wall",
            [
                "Blue Medkit",
            ],
        )
        # Can sr50 on the ledge from the couch
        self.connect(blue_key_area, hidden_wall, r.can_use & (r.sr50 | r.jump))

        elevator_drop = self.region(
            "Elevator Drop",
            [
                "Elevator Drop Medkit",
                "Elevator Drop Devastator",
            ],
        )
        # Can fall right onto the medkit
        # Jetpack can be avoided but leaves the player at 25 health
        # Medium difficulty allows the player to escape the elevator pit
        self.connect(
            blue_key_area,
            elevator_drop,
            (
                r.can_open
                | (
                    r.glitched
                    & r.tripmine
                    & r.fast_sprint
                    & r.can_jump
                    & r.difficulty("extreme")
                )
            )
            & (
                r.difficulty("hard") | r.jetpack(50) | (r.difficulty("medium") & r.jump)
            ),
        ),

        past_elevator = self.region(
            "Past Elevator",
            [
                "Secret Crate",
                "Crate Armor",
                "Crate Scuba Gear",
            ],
        )
        self.restrict("Secret Crate", r.can_use)
        self.restrict("Crate Armor", r.can_use)
        self.restrict("Crate Scuba Gear", r.can_use)
        # Can fall from elevator into opening
        self.connect(elevator_drop, past_elevator, r.jump | r.difficulty("hard"))

        lake_secret = self.region(
            "Lake Secret Area",
            [
                "Secret Lake",
                "Lake Pipebombs",
            ],
        )
        # Can shoot pipebomb on the floor to trigger explosion, hard because missable
        self.connect(past_elevator, lake_secret, r.explosives | r.difficulty("hard"))
        self.connect(lake_secret, bridge_secret, r.can_use)

        alien_table = self.region(
            "Alien Table",
            [
                "Table Freezethrower",
            ],
        )
        # Can sr50 on this without jump by using the pillar base
        self.connect(past_elevator, alien_table, r.difficulty("hard") | r.jump)

        alien_freezer = self.region(
            "Alien Freezer",
            [
                "MP Freezer Atomic Health",
                "Red Key Card",
            ],
        )
        self.connect(past_elevator, alien_freezer, r.can_crouch)

        crates_upper = self.region(
            "Upper Crate Area",
            [
                "Crate Holo Duke",
            ],
        )
        self.connect(past_elevator, crates_upper, r.jump)

        conveyer_upper = self.region(
            "Conveyer Upper Area",
            [
                "Conveyer Jetpack",
                "Conveyer Shrinker",
            ],
        )
        self.connect(past_elevator, conveyer_upper, r.jump)

        ufo_secret = self.region(
            "Secret UFO",
            [
                "UFO Atomic Health",
                "Secret UFO",
            ],
        )

        self.connect(past_elevator, ufo_secret, r.can_use)

        red_key_area = self.region(
            "Red Key Area",
            [
                "Yellow Key Card",
                "Red Shotgun",
            ],
        )
        # This clip is possible with sprint and duck only
        # Clip on the switch by ducking while running into the window
        self.connect(
            past_elevator,
            red_key_area,
            (self.red_key & r.can_open)
            | (r.difficulty("hard") & r.can_crouch & r.sprint & r.glitched),
        )

        red_table = self.region(
            "Red Table",
            [
                "MP Red Steroids",
            ],
        )
        # Can sr50 on table
        self.connect(red_key_area, red_table, r.sr50 | r.jump)

        yellow_key_area = self.region(
            "Yellow Key Area",
            [
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_use)
        # Tripclip goes nuclear
        self.connect(
            past_elevator,
            yellow_key_area,
            r.can_open
            & r.can_use
            & (
                self.yellow_key
                | (
                    r.difficulty("hard")
                    & r.steroids
                    & r.can_sprint
                    & r.can_jump
                    & r.tripmine
                    & r.glitched
                )
            ),
        )
        return ret
