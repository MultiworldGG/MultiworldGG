from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L8(D3DLevel):
    name = "Critical Mass"
    levelnum = 7
    volumenum = 3
    keys = ["Red", "Blue", "Yellow"]
    location_defs = [
        {
            "id": 313,
            "name": "Warehouse Vent Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 323, "name": "MP Bookshelf Jetpack", "type": "sprite", "density": 5},
        {"id": 344, "name": "Control Freezethrower", "type": "sprite", "density": 0},
        {"id": 351, "name": "Control Armor", "type": "sprite", "density": 3},
        {"id": 352, "name": "Control Shotgun", "type": "sprite", "density": 4},
        {"id": 386, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 456, "name": "Homer Atomic Health", "type": "sprite", "density": 2},
        {"id": 479, "name": "Explosion Lower Medkit", "type": "sprite", "density": 2},
        {
            "id": 532,
            "name": "Explosion Lower Devastator",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 533,
            "name": "Explosion Lower Atomic Health",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 538,
            "name": "Explosion Lower Pipebombs",
            "type": "sprite",
            "density": 0,
        },
        {"id": 613, "name": "Front Upper Armor", "type": "sprite", "density": 0},
        {"id": 614, "name": "Warehouse Atomic Health", "type": "sprite", "density": 0},
        {"id": 648, "name": "Explosion Chaingun", "type": "sprite", "density": 4},
        {"id": 713, "name": "Outside Pipebombs", "type": "sprite", "density": 0},
        {"id": 714, "name": "Warehouse Shotgun", "type": "sprite", "density": 3},
        {
            "id": 724,
            "name": "Explosion Lower Holo Duke",
            "type": "sprite",
            "density": 3,
        },
        {"id": 733, "name": "Storage Medkit", "type": "sprite", "density": 3},
        {"id": 734, "name": "Storage Steroids", "type": "sprite", "density": 3},
        {
            "id": 735,
            "name": "Explosion Lower Protective Boots",
            "type": "sprite",
            "density": 4,
        },
        {"id": 761, "name": "Blue Dive Atomic Health", "type": "sprite", "density": 3},
        {"id": 762, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 827, "name": "Blue Upper Shrinker", "type": "sprite", "density": 2},
        {"id": 830, "name": "Blue Chaingun", "type": "sprite", "density": 0},
        {"id": 834, "name": "Blue Secret RPG", "type": "sprite", "density": 2},
        {"id": 835, "name": "Storage Tripmine 1", "type": "sprite", "density": 4},
        {"id": 836, "name": "Storage Tripmine 2", "type": "sprite", "density": 4},
        {"id": 854, "name": "Red Key Card", "type": "sprite", "density": 0},
        {
            "id": 863,
            "name": "Explosion Lower Scuba Gear",
            "type": "sprite",
            "density": 3,
        },
        {"id": 864, "name": "MP Explosion RPG", "type": "sprite", "density": 5},
        {"id": 868, "name": "MP Outside Freezethrower", "type": "sprite", "density": 5},
        {"id": 105, "name": "Secret Explosion Lower", "type": "sector"},
        {"id": 116, "name": "Secret Homer", "type": "sector"},
        {"id": 234, "name": "Secret Blue Area", "type": "sector"},
        {"id": 240, "name": "Secret Blue Upper", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True
    events = ["Meltdown"]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Outside Pipebombs",
                "MP Outside Freezethrower",
                "Front Upper Armor",
            ],
        )
        self.restrict("Outside Pipebombs", r.can_open)
        self.restrict("MP Outside Freezethrower", r.can_open)
        self.restrict("Front Upper Armor", r.can_open & r.jump)

        front_upper = self.region(
            "Front Upper",
            [
                "Warehouse Atomic Health",
                "Warehouse Shotgun",
                "Warehouse Vent Night Vision Goggles",
                "Explosion Chaingun",
                "Secret Homer",
                "Homer Atomic Health",
                "MP Explosion RPG",
            ],
        )
        self.connect(ret, front_upper, r.jump & r.can_open & r.can_use)

        expl_lower = self.region(
            "Explosion Lower",
            [
                "Explosion Lower Atomic Health",
                "Explosion Lower Pipebombs",
                "Explosion Lower Scuba Gear",
                "Secret Explosion Lower",
                "Explosion Lower Medkit",
                "Explosion Lower Devastator",
                "Explosion Lower Holo Duke",
                "Explosion Lower Protective Boots",
            ],
        )
        self.connect(front_upper, expl_lower, r.can_crouch & r.can_dive)

        upper_storage = self.region(
            "Storage Upper Area",
            [
                "Storage Steroids",
                "Storage Tripmine 1",
                "Storage Tripmine 2",
            ],
        )
        self.connect(expl_lower, upper_storage, r.jump)

        control_room = self.region(
            "Control Room",
            [
                "Storage Medkit",
                "Control Freezethrower",
                "Control Armor",
                "Control Shotgun",
                "Blue Key Card",
            ],
        )
        self.connect(expl_lower, control_room)

        blue_key_area = self.region(
            "Blue Key Area",
            [
                "Secret Blue Area",
                "Blue Secret RPG",
                "Blue Chaingun",
            ],
        )
        # Not many doors left to tripclip past
        self.connect(
            control_room,
            blue_key_area,
            self.blue_key
            | (r.glitched & r.steroids & r.can_sprint & r.can_jump & r.tripmine),
        )

        blue_upper = self.region(
            "Blue Key Upper Area",
            [
                "Secret Blue Upper",
                "Blue Upper Shrinker",
            ],
        )
        # 75 is generous, 60 could be enough
        self.connect(blue_key_area, blue_upper, r.jetpack(75))

        blue_dive = self.region(
            "Blue Dive Area",
            ["Blue Dive Atomic Health", "Yellow Key Card", "Meltdown"],
        )
        # Need blue keycard to escape the room
        self.restrict("Meltdown", self.blue_key)
        self.connect(blue_key_area, blue_dive, r.can_dive)

        yellow_key_area = self.region(
            "Yellow Key Area",
            [],
        )
        self.connect(control_room, yellow_key_area, self.yellow_key)

        yellow_bookshelf = self.region(
            "Office Bookshelf",
            [
                "MP Bookshelf Jetpack",
                "Red Key Card",
            ],
        )
        # Can clip up the bookshelf by using the door
        self.connect(yellow_key_area, yellow_bookshelf, r.jump | r.difficulty("hard"))

        red_key_area = self.region(
            "Red Key Area",
            [
                "Exit",
            ],
        )
        self.connect(
            yellow_key_area,
            red_key_area,
            r.can_crouch
            & r.jump
            & self.event("Meltdown")
            & (
                self.red_key
                | (
                    r.glitched
                    & r.tripmine
                    & r.fast_sprint
                    & r.can_jump
                    & r.difficulty("extreme")
                )
            ),
        )
        return ret
