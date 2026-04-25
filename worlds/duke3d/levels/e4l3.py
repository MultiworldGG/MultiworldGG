from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L3(D3DLevel):
    name = "Shop-N-Bag"
    levelnum = 2
    volumenum = 3
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {"id": 18, "name": "MP Seal Chaingun", "type": "sprite", "density": 5},
        {"id": 21, "name": "Warehouse Pipebombs", "type": "sprite", "density": 3},
        {"id": 32, "name": "Openable Box Armor", "type": "sprite", "density": 2},
        {
            "id": 39,
            "name": "Storage Upper Freezethrower",
            "type": "sprite",
            "density": 3,
        },
        {"id": 40, "name": "Storage Upper Pipebombs", "type": "sprite", "density": 4},
        {
            "id": 41,
            "name": "Storage Upper Night Vision Goggles",
            "type": "sprite",
            "density": 2,
        },
        {"id": 116, "name": "MP Blue Vent Shrinker", "type": "sprite", "density": 5},
        {"id": 121, "name": "Blue Top Crate RPG", "type": "sprite", "density": 0},
        {"id": 122, "name": "MP Outside Shotgun", "type": "sprite", "density": 5},
        {"id": 126, "name": "MP Behind boxes RPG", "type": "sprite", "density": 5},
        {"id": 130, "name": "Shop Corridor Devastator", "type": "sprite", "density": 2},
        {"id": 131, "name": "Blue Fruit Tripmine 1", "type": "sprite", "density": 3},
        {"id": 132, "name": "Blue Fruit Tripmine 2", "type": "sprite", "density": 4},
        {"id": 133, "name": "Blue Fruit Tripmine 3", "type": "sprite", "density": 4},
        {
            "id": 134,
            "name": "Storage Upper Atomic Health",
            "type": "sprite",
            "density": 3,
        },
        {"id": 139, "name": "Shop Corridor Medkit", "type": "sprite", "density": 3},
        {"id": 148, "name": "Crate Shotgun", "type": "sprite", "density": 0},
        {
            "id": 158,
            "name": "Yellow Cashier Devastator",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 194,
            "name": "Warehouse Upper Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 228, "name": "Exploding Box Chaingun", "type": "sprite", "density": 2},
        {"id": 264, "name": "Blue Vent Atomic Health", "type": "sprite", "density": 0},
        {"id": 307, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 377, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 396, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 426, "name": "Manager Office Pipebombs", "type": "sprite", "density": 0},
        {"id": 442, "name": "Blue Fruit Armor", "type": "sprite", "density": 0},
        {
            "id": 445,
            "name": "Warehouse Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 446, "name": "MP Shop Blue Jetpack", "type": "sprite", "density": 5},
        {"id": 451, "name": "MP Red Storage Shotgun", "type": "sprite", "density": 5},
        {"id": 452, "name": "Red Storage Holo Duke", "type": "sprite", "density": 0},
        {"id": 492, "name": "Manager Office Steroids", "type": "sprite", "density": 3},
        {"id": 542, "name": "Trash Comp Medkit", "type": "sprite"},
        {"id": 547, "name": "Red Storage Steroids", "type": "sprite"},
        {"id": 549, "name": "Trash Comp Protective Boots", "type": "sprite"},
        {"id": 70, "name": "Secret Exploding Box", "type": "sector"},
        {"id": 176, "name": "Secret Shop Corridor", "type": "sector"},
        {"id": 274, "name": "Secret Yellow Cashier", "type": "sector"},
        {"id": 344, "name": "Secret Storage Upper", "type": "sector"},
        {"id": 349, "name": "Secret Openable Box", "type": "sector"},
        {"id": 362, "name": "Secret Trash Comp", "type": "sector"},
        {"id": 365, "name": "Secret Red Storage", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "MP Outside Shotgun",
            ],
        )

        over_fence = self.region(
            "Over fence",
            [],
        )
        # Can sr50 over the fence around the corner
        self.connect(ret, over_fence, r.sr50 | r.jump)

        over_fence_container = self.region(
            "Over fence container",
            [
                "Crate Shotgun",
            ],
        )
        self.connect(over_fence, over_fence_container, r.jump & r.can_open)

        over_fence_warehouse = self.region(
            "Over fence warehouse",
            [
                "Warehouse Pipebombs",
                "Warehouse Night Vision Goggles",
            ],
        )
        self.connect(over_fence, over_fence_warehouse, r.can_crouch)

        warehouse_upper = self.region(
            "Warehouse Upper",
            [
                "Warehouse Upper Atomic Health",
            ],
        )
        # I once got up here with just walk and sr50, couldnt reproduce yet
        self.connect(over_fence_warehouse, warehouse_upper, r.jump)

        shop_inside = self.region(
            "Shop Inside",
            [
                "Secret Shop Corridor",
                "Shop Corridor Devastator",
                "Shop Corridor Medkit",
                "Secret Openable Box",
                "Openable Box Armor",
            ],
        )
        self.restrict("Secret Openable Box", r.can_open)
        self.restrict("Openable Box Armor", r.can_open)
        # Strafe on the fence and sprint into the shop window
        self.connect(ret, shop_inside, r.jump | (r.difficulty("hard") & r.sprint))
        self.connect(shop_inside, over_fence_container, r.jump)

        behind_boxes = self.region(
            "Behind boxes",
            [
                "MP Behind boxes RPG",
                "Blue Key Card",
            ],
        )
        self.connect(shop_inside, behind_boxes, r.jump)

        shop_blue = self.region(
            "Shop Blue Key Area",
            [
                "MP Shop Blue Jetpack",
            ],
        )
        # Alternate path by clip-blowing up the boxes with the devastator
        self.connect(
            shop_inside,
            shop_blue,
            (self.blue_key & r.can_open)
            | (r.difficulty("hard") & (r.devastator | r.rpg) & r.glitched),
        )
        # Tripclip from outside
        self.connect(
            ret,
            shop_blue,
            (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        exploding_box = self.region(
            "Exploding Box",
            [
                "Secret Exploding Box",
                "Exploding Box Chaingun",
            ],
        )
        self.connect(shop_blue, exploding_box, r.explosives)

        blue_fruits = self.region(
            "Blue Fruit Area",
            [
                "Blue Fruit Armor",
                "Blue Fruit Tripmine 1",
                "Blue Fruit Tripmine 2",
                "Blue Fruit Tripmine 3",
            ],
        )
        # Can diagonal walk up in corner, easier with sprint?
        # Extreme difficulty strat needs to be double checked
        # | r.difficulty("extreme"))
        self.connect(
            shop_blue, blue_fruits, r.jump | (r.difficulty("hard") & r.can_sprint)
        )

        blue_vent_front = self.region(
            "Shop Blue Key Area Vent Front",
            [
                "MP Blue Vent Shrinker",
                "MP Seal Chaingun",
                "Yellow Key Card",
            ],
        )
        # This one is accessable with just jetpack
        # Can also drop in the other vent to grab one item
        # Hard logic can require using the jetpack drop as a makeshift crouch to get into the other vent
        self.connect(
            shop_blue,
            blue_vent_front,
            r.can_jump | (r.jetpack(50) & r.difficulty("hard")),
        )

        blue_vent_back = self.region(
            "Shop Blue Key Area Vent Back",
            [
                "Blue Top Crate RPG",
                "Blue Vent Atomic Health",
            ],
        )
        self.connect(shop_blue, blue_vent_back, r.jump)

        yellow_cashier = self.region(
            "Yellow Key Cashier Area",
            [
                "Manager Office Steroids",
            ],
        )
        self.restrict("Manager Office Steroids", r.can_open)
        self.connect(
            shop_blue,
            yellow_cashier,
            self.yellow_key
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        manager_upper = self.region(
            "Manager Area",
            [
                "Manager Office Pipebombs",
                "Red Key Card",
            ],
        )
        self.restrict("Manager Office Pipebombs", r.can_open)
        self.restrict("Red Key Card", r.can_open)
        # Can climb up to crates over the crack, permanently gone if blown up, hard because missable
        self.connect(yellow_cashier, manager_upper, r.jump | r.difficulty("hard"))

        yellow_cashier_secret = self.region(
            "Secret Yellow Cashier",
            [
                "Secret Yellow Cashier",
                "Yellow Cashier Devastator",
            ],
        )
        self.connect(yellow_cashier, yellow_cashier_secret, r.jump & r.can_open)
        # Can shoot the switch from the outside
        self.connect(
            ret, yellow_cashier_secret, r.difficulty("hard") & r.jump & r.can_open
        )

        storage_red = self.region(
            "Red Key Storage Area",
            [
                "Red Storage Holo Duke",
                "MP Red Storage Shotgun",
                "Red Storage Steroids",
                "Secret Red Storage",
            ],
        )
        self.restrict("Red Storage Steroids", r.can_open)
        self.restrict("Secret Red Storage", r.can_open)
        self.connect(shop_blue, storage_red, self.red_key)

        storage_red_upper = self.region(
            "Red Key Storage Upper Area",
            [
                "Storage Upper Atomic Health",
            ],
        )
        self.connect(storage_red, storage_red_upper, r.jump)

        storage_red_secret = self.region(
            "Red Key Storage Secret Area",
            [
                "Secret Storage Upper",
                "Storage Upper Freezethrower",
                "Storage Upper Pipebombs",
                "Storage Upper Night Vision Goggles",
            ],
        )
        # Possible to use enemies to jetpack into the tighter space,
        # 100 jetpack to make it less harsh
        self.connect(
            storage_red,
            storage_red_secret,
            r.can_open & ((r.jetpack(100) & r.difficulty("hard")) | r.can_jump),
        )

        trash_compactor = self.region(
            "Trash Compactor",
            [
                "Exit",
            ],
        )
        self.restrict("Exit", r.can_use)
        trash_compactor_secret = self.region(
            "Trash Compactor Secret Area",
            [
                "Trash Comp Protective Boots",
                "Trash Comp Medkit",
                "Secret Trash Comp",
            ],
        )
        # Can just shoot the switch from below
        self.connect(
            storage_red,
            trash_compactor,
            r.jump | r.difficulty("medium"),
        )
        self.connect(trash_compactor, trash_compactor_secret, r.can_open)
        self.connect(trash_compactor_secret, trash_compactor, r.can_open)
        # Shoot devestator/rpg through wall, leads straight to the exit by blowing up the secret
        self.connect(
            shop_blue,
            trash_compactor_secret,
            r.difficulty("hard") & (r.devastator | r.rpg) & r.glitched,
        )

        return ret
