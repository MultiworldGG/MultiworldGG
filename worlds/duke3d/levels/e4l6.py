from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L6(D3DLevel):
    name = "Going Postal"
    levelnum = 5
    volumenum = 3
    keys = ["Red", "Blue", "Yellow"]
    location_defs = [
        {
            "id": 25,
            "name": "Firetruck Protective Boots",
            "type": "sprite",
            "density": 3,
        },
        {"id": 26, "name": "Firetruck Devastator", "type": "sprite", "density": 2},
        {"id": 81, "name": "Container Pipebombs", "type": "sprite", "density": 3},
        {"id": 84, "name": "Blue Vent Shrinker", "type": "sprite", "density": 2},
        {"id": 145, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 206, "name": "Red Chaingun", "type": "sprite", "density": 0},
        {"id": 209, "name": "Red Armor", "type": "sprite", "density": 3},
        {"id": 210, "name": "Red Medkit", "type": "sprite", "density": 4},
        {"id": 217, "name": "Red Pipebombs", "type": "sprite", "density": 4},
        {"id": 266, "name": "Red Tripmine 1", "type": "sprite", "density": 0},
        {"id": 267, "name": "Red Tripmine 2", "type": "sprite", "density": 3},
        {"id": 277, "name": "Front Holo Duke", "type": "sprite", "density": 0},
        {"id": 279, "name": "Red Atomic Health", "type": "sprite", "density": 0},
        {"id": 281, "name": "Blue Freezethrower", "type": "sprite", "density": 3},
        {"id": 284, "name": "Locker Steroids", "type": "sprite", "density": 3},
        {"id": 286, "name": "Locker Armor", "type": "sprite", "density": 4},
        {"id": 287, "name": "Behind Counter Shotgun", "type": "sprite", "density": 0},
        {"id": 288, "name": "Blue Desk Pipebombs", "type": "sprite", "density": 0},
        {"id": 290, "name": "Blue Crates Devastator", "type": "sprite", "density": 0},
        {
            "id": 291,
            "name": "Conveyer Upper Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 293, "name": "Blue Steroids", "type": "sprite", "density": 4},
        {"id": 294, "name": "Blue Armor", "type": "sprite", "density": 3},
        {
            "id": 295,
            "name": "MP Conveyer Upper Jetpack",
            "type": "sprite",
            "density": 5,
        },
        {"id": 296, "name": "Conveyer Upper Medkit", "type": "sprite", "density": 3},
        {"id": 305, "name": "Locker Crate Chaingun", "type": "sprite", "density": 2},
        {"id": 306, "name": "Basement RPG", "type": "sprite", "density": 0},
        {
            "id": 353,
            "name": "Locker Secret Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 464, "name": "Blue Atomic Health", "type": "sprite", "density": 0},
        {"id": 530, "name": "Firetruck Atomic Health", "type": "sprite", "density": 0},
        {"id": 534, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 590, "name": "Red Devastator", "type": "sprite", "density": 4},
        {"id": 635, "name": "Paw Shotgun", "type": "sprite", "density": 0},
        {
            "id": 665,
            "name": "Blue Conveyer Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 672, "name": "Locker Secret Medkit", "type": "sprite", "density": 2},
        {"id": 724, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 750, "name": "Front Vent Pipebombs", "type": "sprite", "density": 0},
        {"id": 185, "name": "Secret Locker", "type": "sector"},
        {"id": 250, "name": "Secret Blue Vent", "type": "sector"},
        {"id": 302, "name": "Secret Firetruck", "type": "sector"},
        {"id": 317, "name": "Secret Front Vent", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Front Holo Duke",
            ],
        )

        start_upper = self.region(
            "Start Upper",
            [
                "Container Pipebombs",
                "Firetruck Atomic Health",
                "Secret Firetruck",
                "Firetruck Protective Boots",
                "Firetruck Devastator",
            ],
        )
        self.restrict("Secret Firetruck", r.can_use)
        self.restrict("Firetruck Protective Boots", r.can_use)
        self.restrict("Firetruck Devastator", r.can_use)
        self.connect(ret, start_upper, r.jump)

        paw_secret = self.region(
            "Paw Secret",
            [
                "Paw Shotgun",
            ],
        )
        # Can grab the item by jumping and sr40ing towards the opening
        # alternatively crouchjump or duckclip to the item
        self.connect(
            ret,
            paw_secret,
            r.crouch_jump
            | (r.glitched & r.jump & r.fast_sprint & r.can_crouch)
            | (r.can_use & (r.can_crouch | r.difficulty("hard") & r.can_jump)),
        )

        behind_counter = self.region(
            "Behind Counter",
            [
                "Behind Counter Shotgun",
            ],
        )
        self.connect(ret, behind_counter, r.jump)

        behind_counter_door = self.region(
            "Behind Counter Door",
            [
                "Locker Steroids",
            ],
        )
        # Possible with slow crouch jump
        self.connect(
            behind_counter,
            behind_counter_door,
            r.can_use
            | (r.glitched & r.can_jump & r.can_crouch & r.difficulty("medium")),
        )

        basement = self.region(
            "Basement",
            [
                "Basement RPG",
            ],
        )
        self.connect(behind_counter, basement, r.can_use)
        self.connect(
            behind_counter_door,
            basement,
            r.can_use
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        behind_lockers = self.region(
            "Behind Lockers",
            [
                "Locker Armor",
                "Blue Key Card",
                "Secret Locker",
                "Locker Secret Atomic Health",
            ],
        )
        self.connect(behind_counter_door, behind_lockers, r.can_open)

        front_vent = self.region(
            "Front Vent",
            [
                "Front Vent Pipebombs",
            ],
        )
        # Can grab the item by jumping towards the vent
        self.connect(
            ret,
            front_vent,
            r.can_open
            & ((r.can_crouch & r.jump) | (r.difficulty("hard") & r.can_jump)),
        )

        front_vent_secret = self.region(
            "Secret Front Vent",
            [
                "Secret Front Vent",
            ],
        )
        self.connect(ret, front_vent_secret, r.can_open & r.can_crouch & r.jump)

        locker_secret_upper = self.region(
            "Locker Secret Upper",
            [
                "Locker Crate Chaingun",
            ],
        )
        self.connect(behind_lockers, locker_secret_upper, r.jump)

        locker_secret_grate = self.region(
            "Locker Secret Grate",
            [
                "Locker Secret Medkit",
            ],
        )
        # Can grab the item by strafing into the wall and jumping
        # TODO_LOGIC: maybe medium
        self.connect(
            behind_lockers,
            locker_secret_grate,
            r.explosives & (r.can_crouch | (r.difficulty("hard") & r.can_jump)),
        )

        blue_key_area = self.region(
            "Blue Key Area",
            [
                "Blue Steroids",
                "Blue Armor",
                "Blue Freezethrower",
                "Blue Atomic Health",
            ],
        )
        blue_key_area_alt = self.region(
            "Blue Key Area Alternate Path",
            [],
        )
        self.connect(behind_counter_door, blue_key_area, self.blue_key)
        # Alternative path by pipebombing the MAIL door, medium for obscurity
        self.connect(
            ret,
            blue_key_area_alt,
            r.can_crouch & r.pipebomb & r.glitched & r.difficulty("medium"),
        )

        blue_vent_secret = self.region(
            "Secret Blue Vent",
            [
                "Secret Blue Vent",
                "Blue Vent Shrinker",
            ],
        )

        self.connect(blue_key_area, blue_vent_secret, r.can_crouch)

        blue_crates = self.region(
            "Blue Crates",
            [
                "Blue Crates Devastator",
            ],
        )
        self.connect(blue_key_area, blue_crates, r.jump)

        conveyer_ducking = self.region(
            "Blue Conveyer Ducking",
            [
                "Blue Conveyer Atomic Health",
            ],
        )
        # Can actually get in here by flying up with jetpack and dropping as makeshift crouch
        self.connect(
            blue_key_area,
            conveyer_ducking,
            r.can_crouch | (r.difficulty("hard") & r.jetpack(50)),
        )

        blue_desk = self.region(
            "Blue Desk",
            [
                "Blue Desk Pipebombs",
            ],
        )
        # Can get up by clipping on the post bag and sr50ing over to conveyer
        # Hard difficulty because tank can blow up mailbag
        self.connect(blue_key_area, blue_desk, r.jump | r.difficulty("hard"))
        self.connect(blue_key_area_alt, blue_desk, r.jump | r.difficulty("hard"))

        conveyer_upper = self.region(
            "Blue Conveyer Upper",
            [
                "Conveyer Upper Night Vision Goggles",
                "MP Conveyer Upper Jetpack",
                "Conveyer Upper Medkit",
                "Red Key Card",
            ],
        )
        self.connect(
            blue_key_area,
            conveyer_upper,
            (
                r.jump & r.difficulty("medium")
                | (r.difficulty("hard") & r.can_crouch)
                | (r.jump & r.can_crouch)
            ),
        )
        self.connect(
            blue_key_area_alt,
            conveyer_upper,
            (
                r.jump & r.difficulty("medium")
                | (r.difficulty("hard") & r.can_crouch)
                | (r.jump & r.can_crouch)
            ),
        )
        self.connect(
            blue_key_area_alt,
            blue_key_area,
            r.jump | r.can_open | (r.difficulty("hard") & r.can_crouch),
        )

        red_key_area = self.region(
            "Red Key Area",
            [
                "Red Tripmine 1",
                "Red Tripmine 2",
                "Red Chaingun",
                "Red Armor",
                "Red Medkit",
                "Red Pipebombs",
                "Red Devastator",
                "Yellow Key Card",
                "Red Atomic Health",
            ],
        )
        # Shrink clip exists here, very tight unshrink window to clip through the door
        # TODO_LOGIC: Extreme difficulty?
        self.connect(blue_key_area, red_key_area, self.red_key & r.jump & r.can_crouch)

        yellow_key_area = self.region(
            "Yellow Key Area",
            [
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_use)
        # Tripclips solve everything
        self.connect(
            red_key_area,
            yellow_key_area,
            (self.yellow_key & r.can_open)
            | (
                r.difficulty("extreme")
                & r.steroids
                & r.can_sprint
                & r.can_jump
                & r.tripmine
                & r.glitched
            ),
        )
        return ret
