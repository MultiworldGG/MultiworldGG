from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L8(D3DLevel):
    name = "Hotel Hell"
    levelnum = 7
    volumenum = 2
    keys = ["Blue", "Yellow"]
    location_defs = [
        {"id": 85, "name": "Shark Tank Atomic Health", "type": "sprite", "density": 1},
        {"id": 86, "name": "Shark Tank Scuba Gear 2", "type": "sprite", "density": 4},
        {
            "id": 99,
            "name": "Hallway Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 152, "name": "Hotel Room Vent Shrinker", "type": "sprite", "density": 0},
        {"id": 172, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 175, "name": "Toilet RPG", "type": "sprite", "density": 0},
        {"id": 182, "name": "Dive Board Pipebombs", "type": "sprite", "density": 0},
        {"id": 285, "name": "Toilet Atomic Health", "type": "sprite", "density": 1},
        {"id": 355, "name": "Outside Vent Steroids", "type": "sprite", "density": 4},
        {"id": 358, "name": "Apartment Devastator", "type": "sprite", "density": 3},
        {"id": 372, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {
            "id": 386,
            "name": "Trashcan Pipebombs",
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 3,
        },
        {"id": 392, "name": "Dumpster Medkit", "type": "sprite", "density": 0},
        {"id": 395, "name": "Dumpster Chaingun", "type": "sprite", "density": 4},
        {"id": 397, "name": "Ledge Shotgun", "type": "sprite", "density": 3},
        {"id": 423, "name": "Streets Atomic Health 1", "type": "sprite", "density": 0},
        {"id": 460, "name": "Hotel Room Armor", "type": "sprite", "density": 3},
        {"id": 478, "name": "Corner Tripmine 1", "type": "sprite", "density": 1},
        {"id": 479, "name": "Corner Tripmine 2", "type": "sprite", "density": 4},
        {"id": 564, "name": "Streets Atomic Health 2", "type": "sprite", "density": 4},
        {"id": 575, "name": "Shark Tank Pipebombs", "type": "sprite", "density": 4},
        {"id": 576, "name": "Shark Tank Medkit", "type": "sprite", "density": 2},
        {"id": 577, "name": "Viewpoint Holo Duke", "type": "sprite", "density": 3},
        {"id": 592, "name": "Shark Tank Scuba Gear 1", "type": "sprite", "density": 4},
        {"id": 596, "name": "Wine Rack Holo Duke", "type": "sprite", "density": 2},
        {
            "id": 657,
            "name": "Lobby Night Vision Goggles",
            "type": "sprite",
            "density": 1,
        },
        {"id": 663, "name": "Lobby Armor", "type": "sprite", "density": 3},
        {"id": 667, "name": "Lobby Medkit", "type": "sprite", "density": 1},
        {"id": 684, "name": "MP Lobby Jetpack", "type": "sprite", "density": 5},
        {"id": 685, "name": "MP Staircase Armor", "type": "sprite", "density": 5},
        {"id": 688, "name": "MP Streets Chaingun", "type": "sprite", "density": 5},
        {"id": 690, "name": "MP Hallway Freezethrower", "type": "sprite", "density": 5},
        {"id": 725, "name": "Shark Tank Freezethrower", "type": "sprite", "density": 3},
        {
            "id": 769,
            "name": "Indiana Jones Atomic Health",
            "type": "sprite",
            "density": 2,
        },
        {"id": 823, "name": "Exit Pipebombs", "type": "sprite", "density": 0},
        {"id": 827, "name": "Jungle Freezethrower", "type": "sprite", "density": 3},
        {"id": 138, "name": "Secret Shark Tank", "type": "sector"},
        {"id": 155, "name": "Secret Wine Rack", "type": "sector"},
        {"id": 284, "name": "Secret Indiana Jones", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
        {"id": 11, "name": "Secret Exit", "type": "exit"},
    ]
    events = ["Windows Opened"]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(self.name, ["Trashcan Pipebombs"])

        stadium_elevator = self.region("Stadium Elevator", ["Exit", "Exit Pipebombs"])
        # possible to clip over with sprint speed
        self.connect(
            ret,
            stadium_elevator,
            r.pipebomb & (r.jump | (r.sprint & r.difficulty("hard"))),
        )
        self.restrict("Exit", r.can_use)

        entrance_ledges = self.region(
            "Entrance Ledges",
            [
                "Ledge Shotgun",
                "Blue Key Card",
                "Outside Vent Steroids",
            ],
        )
        self.connect(ret, entrance_ledges, r.jump)
        dumpster = self.region(
            "Dumpster",
            [
                "Dumpster Chaingun",
                "Dumpster Medkit",
            ],
        )
        # Can step on a pigcops head using debris on the floor
        self.connect(ret, dumpster, r.jump | (r.difficulty("hard")))

        self.connect(
            entrance_ledges,
            stadium_elevator,
            r.crouch_jump | (r.can_jump & self.event("Windows Opened")),
        )

        hotel_lobby = self.region(
            "Lobby",
            [
                "Toilet RPG",
                "Lobby Medkit",
                "MP Streets Chaingun",
                "Lobby Armor",
            ],
        )
        self.restrict("Lobby Armor", r.jump & r.can_open)
        self.restrict(
            "Lobby Medkit",
            r.can_open | r.glitched & r.can_crouch & r.jump & r.fast_sprint,
        )
        # This would be so nice to bypass somehow
        self.connect(ret, hotel_lobby, self.blue_key & r.can_open)

        lobby_side_room = self.region(
            "Lobby Side Room", ["MP Lobby Jetpack", "Lobby Night Vision Goggles"]
        )
        self.connect(hotel_lobby, lobby_side_room, r.can_use)

        streets_ledge = self.region(
            "Streets Ledge", ["Streets Atomic Health 1", "Streets Atomic Health 2"]
        )
        # can probably jump on enemies
        self.connect(hotel_lobby, streets_ledge, r.jetpack(50))

        apartment = self.region(
            "Apartment Building", ["Yellow Key Card", "Apartment Devastator"]
        )
        self.connect(hotel_lobby, apartment, r.jump)

        upstairs = self.region(
            "Hotel Upstairs",
            [
                "Hallway Night Vision Goggles",
                "MP Hallway Freezethrower",
                "Jungle Freezethrower",
                "Secret Exit",
                "Secret Indiana Jones",
            ],
        )
        # can clip up from the broken reception tv
        self.connect(
            hotel_lobby, upstairs, (self.yellow_key & r.can_open) | r.crouch_jump
        )
        # can walk out through exploding wall
        self.connect(upstairs, streets_ledge, r.true)
        self.restrict("Secret Exit", r.can_use)
        self.restrict("Secret Indiana Jones", r.can_use)

        upstairs_doors = self.region(
            "Upstairs Doors",
            [
                "MP Staircase Armor",
                "Secret Wine Rack",
                "Wine Rack Holo Duke",
                "Secret Shark Tank",
                "Shark Tank Scuba Gear 1",
                "Shark Tank Pipebombs",
                "Shark Tank Medkit",
            ],
        )
        self.connect(upstairs, upstairs_doors, r.can_open)

        left_hotel_room = self.region("Left Hotel Room")
        self.connect(upstairs, left_hotel_room, r.can_open)
        self.connect(hotel_lobby, left_hotel_room, r.fast_crouch_jump)

        right_hotel_room = self.region("Right Hotel Room", ["Hotel Room Armor"])
        self.connect(upstairs, right_hotel_room, r.can_open)

        room_vent = self.region("Hotel Room Vent", ["Hotel Room Vent Shrinker"])
        self.connect(left_hotel_room, room_vent, r.jump)
        self.connect(room_vent, left_hotel_room, r.can_crouch)
        self.connect(room_vent, right_hotel_room, r.can_crouch)

        upstairs_corner = self.region(
            "Upstairs Corner", ["Corner Tripmine 1", "Corner Tripmine 2"]
        )
        self.connect(upstairs, upstairs_corner, r.can_use)

        upstairs_ledges = self.region(
            "Upstairs Ledges",
            [
                "Indiana Jones Atomic Health",
                "Dive Board Pipebombs",
                "Viewpoint Holo Duke",
                "Windows Opened",
            ],
        )
        self.connect(upstairs, upstairs_ledges, r.jump)
        self.restrict("Indiana Jones Atomic Health", r.can_use)

        shark_tank = self.region(
            "Shark Tank",
            ["Shark Tank Freezethrower"],
        )
        self.connect(upstairs, shark_tank, r.can_dive & r.jump)

        shark_tank_wall = self.region(
            "Shark Tank Wall", ["Shark Tank Atomic Health", "Shark Tank Scuba Gear 2"]
        )
        self.connect(shark_tank, shark_tank_wall, r.can_use)

        pool = self.region("Inside Pool", ["Toilet Atomic Health"])
        # There might be a different way to get here, maybe?
        self.connect(upstairs, pool, r.can_dive & r.explosives)
        return ret
