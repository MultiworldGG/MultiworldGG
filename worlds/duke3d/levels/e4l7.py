from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L7(D3DLevel):
    name = "XXX-Stacy"
    levelnum = 6
    volumenum = 3
    keys = ["Red", "Blue"]
    location_defs = [
        {"id": 8, "name": "Crusher Scuba Gear", "type": "sprite", "density": 0},
        {"id": 29, "name": "Blue Holo Duke", "type": "sprite", "density": 4},
        {"id": 34, "name": "Crate Freezethrower", "type": "sprite", "density": 2},
        {"id": 35, "name": "MP Front Jetpack", "type": "sprite", "density": 5},
        {"id": 37, "name": "Blue Apt. Pipebombs", "type": "sprite", "density": 3},
        {
            "name": "Printer Trashcan Pipebombs",
            "id": 39,
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 4,
        },
        {"id": 83, "name": "Front Upper Armor", "type": "sprite", "density": 3},
        {"id": 84, "name": "Front Upper Atomic Health", "type": "sprite", "density": 4},
        {"id": 110, "name": "Crusher RPG", "type": "sprite", "density": 3},
        {"id": 112, "name": "Crusher Medkit", "type": "sprite", "density": 4},
        {"id": 165, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 166, "name": "Cola Tripmine 1", "type": "sprite", "density": 0},
        {"id": 167, "name": "Cola Tripmine 2", "type": "sprite", "density": 3},
        {"id": 170, "name": "Blue Devastator", "type": "sprite", "density": 3},
        {"id": 176, "name": "Outside Pipebombs", "type": "sprite", "density": 0},
        {"id": 177, "name": "Front Chaingun", "type": "sprite", "density": 3},
        {"id": 186, "name": "Front Protective Boots", "type": "sprite", "density": 0},
        {"id": 195, "name": "Blue Secret Shrinker", "type": "sprite", "density": 2},
        {"id": 207, "name": "MP Outside Shotgun", "type": "sprite", "density": 5},
        {"id": 216, "name": "Blue Atomic Health", "type": "sprite", "density": 0},
        {
            "id": 245,
            "name": "Blue Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 322, "name": "Blue Medkit", "type": "sprite", "density": 0},
        {"id": 331, "name": "Front Steroids", "type": "sprite", "density": 0},
        {"id": 365, "name": "MP Blue Jetpack", "type": "sprite", "density": 5},
        {"id": 372, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 420, "name": "Blue Shotgun", "type": "sprite", "density": 0},
        {
            "name": "Blue Apt. Trashcan Devastator",
            "id": 528,
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 4,
        },
        {"id": 591, "name": "Blue Apt. RPG", "type": "sprite", "density": 2},
        {"id": 65, "name": "Secret Blue Area", "type": "sector"},
        {"id": 232, "name": "Secret Crate", "type": "sector"},
        {"id": 265, "name": "Secret Blue Appartment", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True
    events = ["Raise Waterlevel"]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "MP Outside Shotgun",
                "Outside Pipebombs",
            ],
        )

        past_door = self.region(
            "Past Door",
            [
                "Front Protective Boots",
                "Front Chaingun",
                "Front Steroids",
                "MP Front Jetpack",
                "Printer Trashcan Pipebombs",
            ],
        )
        self.restrict("Front Protective Boots", r.can_open)
        # This requires a total of 3 tripclips, should this even be in logic?
        self.connect(
            ret,
            past_door,
            r.can_open
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        front_upper = self.region(
            "Front Upper",
            [
                "Front Upper Armor",
                "Front Upper Atomic Health",
                "Blue Key Card",
            ],
        )
        self.connect(past_door, front_upper, r.jump)

        crate_secret = self.region(
            "Crate Secret",
            [
                "Secret Crate",
                "Crate Freezethrower",
            ],
        )
        # can't fit with just jetpack
        self.connect(past_door, crate_secret, r.can_jump)

        blue_key_area = self.region(
            "Blue Key Area",
            [
                "Blue Medkit",
                "Blue Shotgun",
                "MP Blue Jetpack",
            ],
        )
        # Special crouch clip with jetpack included.
        self.connect(
            past_door,
            blue_key_area,
            (self.blue_key & r.jump)
            | (
                r.difficulty("hard")
                & (
                    r.fast_crouch_jump
                    | (r.glitched & r.jump & r.fast_sprint & r.can_crouch)
                )
            ),
        )

        water_control = self.region(
            "Water Control Area",
            [
                "Red Key Card",
                "Blue Holo Duke",
                "Blue Devastator",
                "Blue Atomic Health",
                "Raise Waterlevel",
            ],
        )
        self.restrict("Raise Waterlevel", r.can_use)
        self.restrict("Blue Atomic Health", r.can_open)
        self.connect(blue_key_area, water_control, r.can_open | r.can_dive)

        blue_apt = self.region(
            "Blue Apt.",
            [
                "Secret Blue Appartment",
                "Blue Apt. RPG",
                "Blue Apt. Pipebombs",
                "Blue Apt. Trashcan Devastator",
            ],
        )
        # SR50 jump possible for reaching the apartment
        self.connect(blue_key_area, blue_apt, (r.sr50 & r.can_jump) | r.jump)

        blue_dive = self.region(
            "Blue Dive Area",
            [
                "Blue Night Vision Goggles",
            ],
        )
        self.restrict("Blue Night Vision Goggles", r.can_open)
        # Crouchjump through window skips dive and jetpack requirement
        self.connect(
            blue_key_area,
            blue_dive,
            (r.can_dive & (self.event("Raise Waterlevel") | r.jetpack(50)))
            | r.crouch_jump,
        )

        cola_machine = self.region(
            "Blue Dive Area",
            [
                "Cola Tripmine 1",
                "Cola Tripmine 2",
            ],
        )
        self.connect(blue_dive, cola_machine, r.jump)

        blue_secret = self.region(
            "Secret Blue Area",
            [
                "Blue Secret Shrinker",
                "Secret Blue Area",
            ],
        )
        # Clip on top of trashcan and strafe around to secret
        # Either we can lower the water level with use
        # or we got here by not raising it (jetpack)
        self.connect(
            blue_dive,
            blue_secret,
            (r.can_use | r.jetpack(50))
            & (r.jump | (r.sr50 & r.can_open & r.difficulty("hard"))),
        )

        dive_crusher = self.region(
            "Dive Crusher",
            [
                "Crusher Scuba Gear",
                "Crusher RPG",
                "Crusher Medkit",
            ],
        )
        self.connect(blue_dive, dive_crusher, r.can_dive)

        red_key_area = self.region(
            "Red Key Area",
            [
                "Exit",
            ],
        )
        self.connect(blue_dive, red_key_area, self.red_key & r.can_open & r.can_use)
        return ret
