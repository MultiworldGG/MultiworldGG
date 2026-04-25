from BaseClasses import Region

from ..base_classes import D3DLevel


class E1L2(D3DLevel):
    name = "Red Light District"
    levelnum = 1
    volumenum = 0
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {"name": "Blue Key Card", "id": 27, "type": "sprite", "density": 0},
        {"name": "Sewers Jetpack", "id": 51, "type": "sprite", "density": 2},
        {
            "name": "Sewers Night Vision Goggles",
            "id": 52,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Sewers Steroids", "id": 53, "type": "sprite", "density": 4},
        {"name": "Sewers Holo Duke", "id": 54, "type": "sprite", "density": 4},
        {"name": "Vent Pipebombs", "id": 63, "type": "sprite", "density": 4},
        {
            "name": "MP Steroids outside Strip Floor",
            "id": 120,
            "type": "sprite",
            "density": 5,
        },
        {
            "name": "Night Vision Goggles behind Curtains",
            "id": 170,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Strippers Chaingun", "id": 174, "type": "sprite", "density": 2},
        {"name": "Yellow Key Card", "id": 179, "type": "sprite", "density": 0},
        {"name": "Dark Area Atomic Health", "id": 183, "type": "sprite", "density": 2},
        {
            "name": "Toilets Night Vision Goggles",
            "id": 186,
            "type": "sprite",
            "density": 0,
        },
        {
            "name": "Pornography Store Shelves Pipebombs",
            "id": 188,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Pornography Store Shelves Armor",
            "id": 189,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Video Booth RPG", "id": 192, "type": "sprite", "density": 3},
        {
            "name": "Pornography Store Corner Holo Duke",
            "id": 208,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Red Key Card", "id": 249, "type": "sprite", "density": 0},
        {"name": "Sewers Atomic Health", "id": 260, "type": "sprite", "density": 0},
        {"name": "Sewers Pipebombs", "id": 265, "type": "sprite", "density": 3},
        {"name": "Attic Medkit", "id": 278, "type": "sprite", "density": 2},
        {"name": "MP Outside Ledge Jetpack", "id": 366, "type": "sprite", "density": 5},
        {"name": "Outside Ledge Armor", "id": 367, "type": "sprite", "density": 1},
        {
            "name": "Strip Club Entrance Shotgun",
            "id": 391,
            "type": "sprite",
            "density": 0,
        },
        {
            "name": "Video Booth Steroids",
            "id": 407,
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 1,
        },
        {
            "name": "Chaingun near Blue Key Card",
            "id": 442,
            "type": "sprite",
            "density": 3,
        },
        {"name": "Vent Atomic Health", "id": 497, "type": "sprite", "density": 2},
        {
            "name": "Pornography Store Shotgun",
            "id": 515,
            "type": "sprite",
            "density": 1,
        },
        {"name": "MP Bar RPG", "id": 751, "type": "sprite", "density": 5},
        {
            "name": "Pornography Store Atomic Health",
            "id": 822,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Construction Site Medkit", "id": 823, "type": "sprite", "density": 3},
        {
            "name": "MP DukeTag Outside Ledge Spawn Pipebombs",
            "id": 824,
            "type": "sprite",
            "density": 5,
        },  # This appears inaccessible in single player
        {"name": "Secret Strip Club Vents", "id": 91, "type": "sector"},
        {"name": "Secret Hidden Ledge behind Curtains", "id": 107, "type": "sector"},
        {"name": "Secret Pornography Store Corner", "id": 158, "type": "sector"},
        {"name": "Secret Pornography Store Shelves", "id": 161, "type": "sector"},
        {"name": "Secret Pornography Store Dark Area", "id": 172, "type": "sector"},
        {"name": "Secret Behind Strippers", "id": 177, "type": "sector"},
        {"name": "Secret Attic Hidden Compartment", "id": 187, "type": "sector"},
        {"name": "Secret Sewers", "id": 218, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(self.name)

        streets = self.region("Streets")
        # can duck into the ground with jetpack even without crouch
        self.connect(ret, streets, r.can_open | r.can_crouch | r.jetpack(50))

        store = self.region(
            "Pornography Store",
            [
                "Secret Pornography Store Shelves",
                "Pornography Store Shelves Armor",
                "Pornography Store Shelves Pipebombs",
                "Pornography Store Shotgun",
                "Secret Pornography Store Dark Area",
                "Dark Area Atomic Health",
                "Video Booth Steroids",
                "Video Booth RPG",
                "Toilets Night Vision Goggles",
                "Pornography Store Atomic Health",
            ],
        )
        self.connect(streets, store, r.can_open | r.glitch_kick)
        self.restrict("Pornography Store Atomic Health", r.jump)
        self.restrict(
            "Toilets Night Vision Goggles", r.can_use & (r.can_open | r.explosives)
        )
        self.restrict("Video Booth RPG", r.can_open)
        self.restrict("Video Booth Steroids", r.can_open)
        self.restrict("Pornography Store Shelves Armor", r.can_open)
        self.restrict("Pornography Store Shelves Pipebombs", r.can_open)
        self.restrict("Dark Area Atomic Health", r.can_open)
        self.restrict("Secret Pornography Store Dark Area", r.can_open)

        apartment = self.region(
            "Apartment", ["Chaingun near Blue Key Card", "Blue Key Card"]
        )
        self.connect(streets, apartment, r.jetpack(50))
        self.connect(store, apartment, r.can_open)
        self.restrict("Blue Key Card", r.can_open)

        streets_ledge = self.region(
            "Streets Ledge",
            [
                "MP Outside Ledge Jetpack",
                "Outside Ledge Armor",
            ],
        )
        self.connect(ret, streets_ledge, r.jump)

        store_corner = self.region(
            "Pornography Store Corner",
            [
                "Pornography Store Corner Holo Duke",
                "Secret Pornography Store Corner",
            ],
        )
        # can't fit up with jetpack
        self.connect(ret, store_corner, r.can_open & r.can_jump)

        strip_club = self.region(
            "Strip Club",
            [
                "Strip Club Entrance Shotgun",
                "MP Steroids outside Strip Floor",
                "MP Bar RPG",
                "Red Key Card",
            ],
        )
        self.restrict("Red Key Card", r.can_crouch & r.can_open)
        self.connect(ret, strip_club, self.yellow_key & r.can_open)

        sewers = self.region(
            "Sewers",
            [
                "Secret Sewers",
                "Sewers Steroids",
                "Sewers Pipebombs",
                "Sewers Atomic Health",
                "Sewers Night Vision Goggles",
                "Sewers Holo Duke",
                "Sewers Jetpack",
            ],
        )
        # One way connection only
        self.connect(strip_club, sewers, r.can_open)

        construction_site = self.region(
            "Construction Site", ["Construction Site Medkit", "Yellow Key Card"]
        )
        self.connect(
            ret,
            construction_site,
            (self.blue_key | (r.glitched & r.can_crouch & r.can_use)) & r.jump,
        )  # Can press button from outside

        # Can get to sewers, but the unlock for the door is on the other side only, so no connection to strip club
        self.connect(construction_site, sewers, r.explosives)
        # Can't survive pipe bomb or RPG explosion going up from the sewer
        self.connect(
            strip_club,
            construction_site,
            r.difficulty("hard")
            & ((r.devastator & r.jetpack(50)) | r.tripmine & r.jetpack(100)),
        )

        dance_floor = self.region(
            "Dance Floor",
            [
                "Secret Strip Club Vents",
                "Vent Atomic Health",
                "Vent Pipebombs",
                "Secret Behind Strippers",
                "Strippers Chaingun",
            ],
        )
        # Can't do anything in this without jumping, but does not require crouch to enter the vent
        self.connect(strip_club, dance_floor, self.red_key & r.can_open & r.jump)

        curtain_ledge = self.region(
            "Ledge behind Curtain",
            [
                "Secret Hidden Ledge behind Curtains",
                "Night Vision Goggles behind Curtains",
            ],
        )
        self.connect(
            dance_floor,
            curtain_ledge,
            (r.difficulty("medium") & r.can_jump) | r.jetpack(50),
        )

        # This level has a cutscene exit trigger, so we don't need Use to trigger it!
        attic = self.region(
            "Attic",
            [
                "Exit",
            ],
        )
        self.connect(attic, curtain_ledge, (r.sr50 & r.can_jump) | r.jetpack(50))
        self.connect(
            dance_floor,
            attic,
            (r.difficulty("medium") & r.can_jump)
            | (r.can_use & r.can_jump)
            | r.jetpack(50),
        )

        attic_secret = self.region(
            "Attic Compartment", ["Attic Medkit", "Secret Attic Hidden Compartment"]
        )
        self.connect(attic, attic_secret, r.can_open)

        return ret
