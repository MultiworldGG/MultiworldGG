from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L1(D3DLevel):
    name = "Raw Meat"
    levelnum = 0
    volumenum = 2
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 78, "name": "Booth Jetpack", "type": "sprite", "density": 3},
        {"id": 115, "name": "Start Ledge Chaingun", "type": "sprite", "density": 4},
        {
            "id": 116,
            "name": "Start Ledge Atomic Health",
            "type": "sprite",
            "density": 1,
        },
        {"id": 161, "name": "Sushi Belt Atomic Health", "type": "sprite", "density": 1},
        {"id": 305, "name": "Sushi Belt Freezethrower", "type": "sprite", "density": 2},
        {"id": 308, "name": "Start Pit Atomic Health", "type": "sprite", "density": 0},
        {"id": 309, "name": "Start Pit Pipebombs", "type": "sprite", "density": 4},
        {"id": 389, "name": "Sushi Belt Steroids", "type": "sprite", "density": 4},
        {"id": 452, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 457, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 492, "name": "Booth Shotgun", "type": "sprite", "density": 1},
        {"id": 497, "name": "Hallway Poster Shrinker", "type": "sprite", "density": 2},
        {"id": 499, "name": "Booth Backroom Steroids", "type": "sprite", "density": 0},
        {"id": 500, "name": "Booth Medkit", "type": "sprite", "density": 3},
        {"id": 524, "name": "Karaoke RPG", "type": "sprite", "density": 0},
        {"id": 536, "name": "Stove Jetpack", "type": "sprite", "density": 3},
        {"id": 543, "name": "Start Pool Pipebombs", "type": "sprite", "density": 1},
        {"id": 561, "name": "Sink Atomic Health", "type": "sprite", "density": 1},
        {"id": 564, "name": "Kitchen Armor", "type": "sprite", "density": 0},
        {"id": 569, "name": "Kitchen Vent Tripmine", "type": "sprite", "density": 3},
        {
            "id": 570,
            "name": "Sushi Belt Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 574, "name": "MP Garage Door Shotgun", "type": "sprite", "density": 5},
        {"id": 575, "name": "MP Booth Chaingun", "type": "sprite", "density": 5},
        {"id": 577, "name": "MP Garage Pool Medkit", "type": "sprite", "density": 5},
        {"id": 608, "name": "Start Devastator", "type": "sprite", "density": 0},
        {"id": 609, "name": "Start Pool Holo Duke", "type": "sprite", "density": 3},
        {
            "id": 624,
            "name": "Sushi Belt Cupboard Pipebombs",
            "type": "sprite",
            "density": 2,
        },
        {"id": 632, "name": "Garage Door Scuba Gear", "type": "sprite", "density": 1},
        {"id": 636, "name": "Hallway Armor", "type": "sprite", "density": 0},
        {
            "id": 656,
            "name": "Night Vision Goggles behind Urn",
            "type": "sprite",
            "density": 3,
        },
        {"id": 135, "name": "Secret Geisha Wall", "type": "sector"},
        {"id": 137, "name": "Secret Hallway Sign", "type": "sector"},
        {"id": 161, "name": "Secret Sushi Belt Wall", "type": "sector"},
        {"id": 287, "name": "Secret Wine Cabinet", "type": "sector"},
        {"id": 332, "name": "Secret Sushi Belt Cupboard", "type": "sector"},
        {"id": 338, "name": "Secret Hallway Wall", "type": "sector"},
        {"id": 344, "name": "Secret Hallway Poster", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    events = ["Backrooms Switch"]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Start Devastator",
                "Booth Jetpack",
                "Booth Shotgun",
                "Night Vision Goggles behind Urn",
                "Secret Geisha Wall",
            ],
        )
        self.restrict("Start Devastator", r.can_open | r.crouch_jump)
        self.restrict("Booth Jetpack", r.can_open)
        self.restrict(
            "Secret Geisha Wall", r.jump | r.can_crouch | r.difficulty("hard")
        )  # Can crouch into the wall from the sign or step up on an enemy

        start_ledge = self.region(
            "Start Ledge", ["Start Ledge Chaingun", "Start Ledge Atomic Health"]
        )
        # Can't seem to make this with SR50 only, can lure liztrooper to step up, easy manip
        self.connect(ret, start_ledge, r.sprint | r.jump | r.difficulty("hard"))

        start_pool = self.region(
            "Start Pool", ["Start Pool Holo Duke", "Start Pool Pipebombs"]
        )
        self.connect(ret, start_pool, r.can_dive)

        start_pit = self.region(
            "Start Pit",
            [
                "Start Pit Atomic Health",
                "Start Pit Pipebombs",
            ],
        )
        # Can get on these by stepping up over enemies
        self.connect(ret, start_pit, r.jump | r.difficulty("hard"))

        hallway_sign = self.region(
            "Hallway Sign", ["Secret Hallway Sign", "Hallway Armor"]
        )
        # Item will be picked up if you do the clip down to the club through the wall panel
        self.connect(
            ret,
            hallway_sign,
            (r.can_open & r.jump) | (r.fast_crouch_jump & r.difficulty("hard")),
        )

        hallway_poster = self.region(
            "Hallway Poster", ["Secret Hallway Poster", "Hallway Poster Shrinker"]
        )
        # Can get on these by stepping up over enemies
        self.connect(ret, hallway_poster, r.can_use & (r.jump | r.difficulty("hard")))

        booths = self.region(
            "Booths", ["Booth Medkit", "MP Booth Chaingun", "Secret Hallway Wall"]
        )
        # If we could trigger the explosion from outside with a clip, could skip the open requirement
        self.connect(ret, booths, r.can_open)
        self.restrict("Secret Hallway Wall", r.explosives)

        booth_backroom = self.region(
            "Booth Backroom", ["Backrooms Switch", "Booth Backroom Steroids"]
        )
        self.connect(
            booths,
            booth_backroom,
            r.can_crouch & r.jump
            | (r.difficulty("medium") & r.can_jump & r.jetpack(50)),
        )  # can get in with just jetpack but we're stuck then, possible to clip out with jump
        self.restrict("Backrooms Switch", r.can_use)

        hatch_room = self.region(
            "Hatching Room",
            ["Blue Key Card", "MP Garage Door Shotgun", "Garage Door Scuba Gear"],
        )
        self.connect(ret, hatch_room, self.event("Backrooms Switch"))

        garage_pool = self.region(
            "Garage Pool", ["MP Garage Pool Medkit", "Red Key Card"]
        )
        self.connect(hatch_room, garage_pool, r.can_dive)
        # clipping from here to the kitchen sink was a EDuke32 only bug, I think

        club_room = self.region(
            "Club Room",
            [
                "Karaoke RPG",
                # can pick up from outside, no opening doors required
                "Sushi Belt Night Vision Goggles",
            ],
        )
        self.connect(
            ret,
            club_room,
            (self.blue_key & r.can_open)
            | (
                r.difficulty("medium")
                & ((r.glitched & r.fast_sprint & r.can_crouch) | r.crouch_jump)
            ),
        )

        sushi_belt = self.region(
            "Sushi Belt", ["Sushi Belt Atomic Health", "Sushi Belt Steroids"]
        )
        self.connect(club_room, sushi_belt, r.jump)  # there might be a way to clip up

        sushi_belt_wall = self.region(
            "Sushi Belt Wall", ["Secret Sushi Belt Wall", "Sushi Belt Freezethrower"]
        )
        self.connect(club_room, sushi_belt_wall, r.can_use)

        sushi_belt_cupboard = self.region(
            "Sushi Belt Cupboard",
            ["Secret Sushi Belt Cupboard", "Sushi Belt Cupboard Pipebombs"],
        )
        self.connect(
            club_room, sushi_belt_cupboard, r.can_crouch & r.can_use & r.can_open
        )

        kitchen_vent = self.region("Kitchen Vent", ["Kitchen Vent Tripmine"])
        self.connect(club_room, kitchen_vent, r.jump)

        kitchen = self.region("Kitchen", ["Kitchen Armor", "Secret Wine Cabinet"])
        self.connect(club_room, kitchen, r.can_open)
        self.connect(kitchen, club_room, r.can_open)
        self.connect(kitchen_vent, kitchen, r.true)
        self.connect(kitchen, kitchen_vent, r.can_jump)
        self.restrict("Secret Wine Cabinet", r.can_open)

        kitchen_ledges = self.region(
            "Kitchen Ledges",
            [
                "Stove Jetpack",
                "Sink Atomic Health",
            ],
        )
        self.connect(
            club_room, kitchen_ledges, r.jump
        )  # there might be a way to clip up the ledges
        self.restrict("Stove Jetpack", r.can_open)

        garage = self.region("Garage", ["Exit"])
        # Tripclip never disappoints
        self.connect(
            club_room,
            garage,
            (self.red_key & r.can_open)
            | (
                r.difficulty("extreme")
                & r.glitched
                & r.sprint
                & r.tripmine
                & r.can_jump
            ),
        )
        self.restrict("Exit", r.jump & r.can_use)
        return ret
