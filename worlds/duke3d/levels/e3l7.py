from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L7(D3DLevel):
    name = "Fahrenheit"
    levelnum = 6
    volumenum = 2
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {"id": 39, "name": "Pool Shotgun", "type": "sprite", "density": 3},
        {
            "id": 60,
            "name": "Building Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 77, "name": "MP Broadcast Jetpack", "type": "sprite", "density": 5},
        {"id": 80, "name": "Building Freezethrower", "type": "sprite", "density": 2},
        {"id": 88, "name": "Fire Station Medkit", "type": "sprite", "density": 3},
        {"id": 89, "name": "Fire Truck Holo Duke", "type": "sprite", "density": 0},
        {"id": 134, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 192, "name": "Window Medkit", "type": "sprite", "density": 3},
        {"id": 202, "name": "Passage Armor", "type": "sprite", "density": 1},
        {"id": 203, "name": "MP Crates Jetpack", "type": "sprite", "density": 5},
        {"id": 259, "name": "Crates Atomic Health", "type": "sprite", "density": 1},
        {"id": 268, "name": "Pool Ledge Pipebombs", "type": "sprite", "density": 0},
        {"id": 294, "name": "Broadcast Devastator", "type": "sprite", "density": 1},
        {"id": 295, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 299, "name": "Set Chaingun", "type": "sprite", "density": 3},
        {"id": 334, "name": "Wine Rack Medkit", "type": "sprite", "density": 2},
        {"id": 335, "name": "Building Steroids", "type": "sprite", "density": 4},
        {"id": 344, "name": "Pool Shrinker", "type": "sprite", "density": 4},
        {"id": 347, "name": "Broadcast Tripmine", "type": "sprite", "density": 4},
        {"id": 348, "name": "Building Tripmine", "type": "sprite", "density": 4},
        {"id": 368, "name": "Exit RPG", "type": "sprite", "density": 0},
        {"id": 422, "name": "Pool Medkit", "type": "sprite", "density": 4},
        {"id": 426, "name": "Fire Station RPG", "type": "sprite", "density": 4},
        {
            "id": 429,
            "name": "Fire Station Atomic Health",
            "type": "sprite",
            "density": 3,
        },
        {"id": 430, "name": "Curtain Atomic Health", "type": "sprite", "density": 2},
        {"id": 431, "name": "Broadcast Shotgun", "type": "sprite", "density": 1},
        {"id": 432, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 111, "name": "Secret Broadcast", "type": "sector"},
        {"id": 133, "name": "Secret Wine Rack", "type": "sector"},
        {"id": 176, "name": "Secret Painting", "type": "sector"},
        {"id": 179, "name": "Secret Curtain", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        # a big container is in our way
        # can't go anywhere at the start, sad
        ret = self.region(self.name, [])

        # and once we get out, there's still nothing in reach just yet
        start_area = self.region("Start Area", [])
        # Can jump into the right side of the ceiling to clip out
        self.connect(
            ret,
            start_area,
            r.can_open | r.glitched & (r.can_jump | (r.can_crouch & r.sprint)),
        )

        start_ledges = self.region("Start Ledges", ["Pool Ledge Pipebombs"])
        self.connect(start_area, start_ledges, r.jump)

        pool = self.region(
            "Pool", ["Pool Shotgun", "Pool Shrinker", "Pool Medkit", "Blue Key Card"]
        )
        self.connect(start_ledges, pool, r.can_dive)

        exit_area = self.region("Exit Area", ["Exit RPG", "Exit"])
        self.connect(pool, exit_area, self.red_key & r.can_open)
        self.restrict("Exit", r.jump & r.explosives & r.can_use)

        plaza = self.region("Plaza", ["Passage Armor"])
        self.connect(
            start_area,
            plaza,
            (self.blue_key & r.can_open),
        )

        fire_truck = self.region(
            "Fire Truck", ["Fire Station Medkit", "Fire Truck Holo Duke"]
        )
        # pretty tricky jump off a flying lizard trooper
        # extreme variant requires sr50 to make the jump
        self.connect(
            start_area,
            fire_truck,
            r.jetpack(50)
            | (r.difficulty("hard") & r.can_jump & r.sprint)
            | (r.difficulty("extreme") & r.can_jump),
        )
        # need an enforcer to jump over the fence
        self.connect(
            fire_truck,
            plaza,
            r.can_open | r.jetpack(50) | r.difficulty("hard") & r.can_jump,
        )
        self.connect(plaza, fire_truck, r.can_open | r.jump)
        self.restrict("Fire Truck Holo Duke", r.jump)
        self.restrict(
            "Fire Station Medkit",
            r.can_open | r.crouch_jump,
        )

        plaza_ledges = self.region(
            "Plaza ledges",
            [
                "MP Crates Jetpack",
                "Crates Atomic Health",
                "Window Medkit",
                "Building Tripmine",
                "Building Night Vision Goggles",
                "Building Steroids",
                "Wine Rack Medkit",
                "Secret Wine Rack",
            ],
        )
        self.connect(plaza, plaza_ledges, r.jump)

        secret_painting = self.region(
            "Painting", ["Secret Painting", "Building Freezethrower"]
        )
        self.connect(
            plaza_ledges,
            secret_painting,
            r.can_open | r.glitched & r.sprint & r.can_crouch,
        )

        fire_station = self.region(
            "Fire Station",
            ["Fire Station RPG", "Fire Station Atomic Health", "Yellow Key Card"],
        )
        # This one doesn't even require sprinting speed to clip into
        # Its also possible to blow up the wall using the explosion from a drone enemy
        self.connect(
            fire_truck,
            fire_station,
            r.explosives | (r.jump & r.can_crouch) | r.difficulty("extreme"),
        )
        self.restrict(
            "Yellow Key Card",
            r.can_use | r.jetpack(50) | (r.sr50 & r.can_jump),
        )

        broadcast = self.region(
            "Broadcast Building",
            [
                "Broadcast Tripmine",
                "Broadcast Devastator",
            ],
        )
        self.connect(fire_truck, broadcast, self.yellow_key & r.can_open)

        control_room = self.region(
            "Broadcast Control Room",
            ["Secret Broadcast", "MP Broadcast Jetpack", "Red Key Card"],
        )
        self.connect(broadcast, control_room, r.can_open)

        film_set = self.region(
            "Film Set",
            ["Set Chaingun", "Curtain Atomic Health", "Secret Curtain"],
        )
        self.connect(broadcast, film_set, r.can_open)

        broadcast_top = self.region("Top of Broadcast Building", ["Broadcast Shotgun"])
        self.connect(
            fire_truck,
            broadcast_top,
            r.jetpack(50) | (r.difficulty("medium") & r.can_jump),
        )
        # Roid crouch-clip to get inside the building from the top
        self.connect(
            broadcast_top, broadcast, r.fast_crouch_jump & r.difficulty("hard")
        )
        # Door is locked, not that this should ever be a limiting factor on the routing
        self.connect(broadcast, broadcast_top, self.yellow_key & r.can_open)
        return ret
