from BaseClasses import Region

from ..base_classes import D3DLevel


class E4L2(D3DLevel):
    name = "Duke-Burger"
    levelnum = 1
    volumenum = 3
    keys = ["Blue", "Red"]
    location_defs = [
        {"id": 59, "name": "Slaughterhouse Tripmine", "type": "sprite", "density": 3},
        {"id": 75, "name": "Conveyer Upper RPG", "type": "sprite", "density": 2},
        {"id": 98, "name": "Kitchen Vent Pipebombs", "type": "sprite", "density": 4},
        {"id": 101, "name": "Kitchen Vent Steroids", "type": "sprite", "density": 2},
        {"id": 102, "name": "Kitchen Vent Medkit", "type": "sprite", "density": 3},
        {"id": 125, "name": "Inside DB Freezethrower", "type": "sprite", "density": 0},
        {"id": 140, "name": "Dog Kennel Pipebombs", "type": "sprite", "density": 2},
        {"id": 150, "name": "Manager Room Tripmine 1", "type": "sprite", "density": 0},
        {"id": 151, "name": "Manager Room Tripmine 2", "type": "sprite", "density": 3},
        {"id": 198, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 217, "name": "Manager Room Armor", "type": "sprite", "density": 0},
        {"id": 354, "name": "Kitchen Fryer Armor", "type": "sprite", "density": 0},
        {
            "id": 355,
            "name": "Slaughterhouse Vent Medkit",
            "type": "sprite",
            "density": 0,
        },
        {"id": 413, "name": "Outside Atomic Health", "type": "sprite", "density": 3},
        {"id": 414, "name": "Outside Pipebombs", "type": "sprite", "density": 4},
        {"id": 416, "name": "MP Inside DB RPG", "type": "sprite", "density": 5},
        {"id": 417, "name": "Kitchen Shotgun", "type": "sprite", "density": 4},
        {"id": 418, "name": "Kitchen Corner Chaingun", "type": "sprite", "density": 0},
        {"id": 423, "name": "Outside Steroids", "type": "sprite", "density": 0},
        {
            "id": 563,
            "name": "MP Outside Sign Holo Duke",
            "type": "sprite",
            "density": 5,
        },
        {
            "id": 595,
            "name": "Slaughterhouse Devastator",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 656,
            "name": "Counter Burger Box Atomic Health",
            "type": "sprite",
            "sprite_type": "jollymeal",
            "density": 1,
        },
        {
            "id": 657,
            "name": "Kitchen Burger Box Atomic Health",
            "type": "sprite",
            "sprite_type": "jollymeal",
            "density": 4,
        },
        {"id": 663, "name": "Outside Sign Shrinker", "type": "sprite", "density": 0},
        {"id": 664, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {
            "id": 679,
            "name": "Kitchen Back Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 748,
            "name": "Kitchen Back Freezethrower",
            "type": "sprite",
            "density": 2,
        },
        {"id": 102, "name": "Secret Dog Kennel", "type": "sector"},
        {"id": 311, "name": "Secret Kitchen Vent", "type": "sector"},
        {"id": 313, "name": "Secret Conveyer Upper", "type": "sector"},
        {"id": 321, "name": "Secret Kitchen Back", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Outside Atomic Health",
                "Outside Pipebombs",
                "Outside Steroids",
            ],
        )

        outside_sign = self.region(
            "Outside Sign",
            [
                "Outside Sign Shrinker",
                "MP Outside Sign Holo Duke",
                "Blue Key Card",
            ],
        )
        self.connect(ret, outside_sign, r.jump)
        self.restrict(
            "Outside Sign Shrinker",
            r.can_use | (r.fast_sprint & r.can_crouch & r.glitched),
        )
        self.restrict(
            "Blue Key Card", r.can_use | (r.fast_sprint & r.can_crouch & r.glitched)
        )

        kitchen_secret = self.region(
            "Kitchen Vent",
            [
                "Kitchen Vent Pipebombs",
                "Kitchen Vent Steroids",
                "Kitchen Vent Medkit",
                "Secret Kitchen Vent",
            ],
        )
        # Can enter without crouch but cant exit, maybe hard difficulty?
        self.connect(ret, kitchen_secret, (r.can_jump & r.sr50) | r.jetpack(50))

        inside_db_front = self.region(
            "Inside DB Front",
            [
                "MP Inside DB RPG",
                "Counter Burger Box Atomic Health",
                "Inside DB Freezethrower",
            ],
        )
        # Can't find a way to grab this without getting on the counter
        self.restrict("Counter Burger Box Atomic Health", r.jump)
        inside_db_kitchen = self.region(
            "Inside DB Kitchen",
            [
                "Red Key Card",
                "Kitchen Shotgun",
                "Kitchen Burger Box Atomic Health",
            ],
        )
        self.connect(inside_db_kitchen, inside_db_front, r.true)
        # Can go in through kitchen secret or go in the normal way
        self.connect(
            ret,
            inside_db_front,
            self.blue_key
            | (
                r.glitched
                & r.jump
                & r.fast_sprint
                & r.can_crouch
                & r.difficulty("hard")
            ),  # not an ordinary fast crouchjump because jetpack also works
        )
        self.connect(kitchen_secret, inside_db_kitchen, r.can_crouch)
        # Outside path requires shrinker to get to kitchen area,
        # Glitched logic allows jumpclip through shrinker path (no sprint required)
        self.connect(
            inside_db_front,
            inside_db_kitchen,
            (r.glitched & r.can_jump & r.can_crouch & r.difficulty("hard"))
            | r.can_shrink,
        )

        kitchen_corner = self.region(
            "Kitchen Corner",
            [
                "Kitchen Corner Chaingun",
            ],
        )
        # This one can be gotten by diagonal walking onto the counter instead of having jump
        # Hard difficulty because if certain entities are destroyed it wont work anymore
        # The other alternative is to drop onto it from kitchen_secret
        self.connect(inside_db_kitchen, kitchen_corner, r.difficulty("hard") | r.jump)

        kitchen_fryer = self.region(
            "Kitchen Fryer",
            [
                "Kitchen Fryer Armor",
            ],
        )
        # TODO_LOGIC: Can maybe be grabbed by diagonal walking into the corner?
        self.connect(
            inside_db_kitchen,
            kitchen_fryer,
            r.jump | (r.difficulty("hard") & r.can_sprint),
        )

        kitchen_back_secret = self.region(
            "Secret Kitchen Back",
            [
                "Kitchen Back Freezethrower",
                "Secret Kitchen Back",
            ],
        )
        # Can jump/jetpack instead of duck to activate switch at desk
        # TODO_LOGIC: Extreme logic: Use enforcer to clip on topmost box for secret
        # r.jetpack(100) & r.difficulty("extreme") 100 jetpack just to be nice and allow more attempts
        self.connect(
            inside_db_kitchen,
            kitchen_back_secret,
            r.can_use & r.can_jump & (r.can_crouch | r.difficulty("medium")),
        )

        kitchen_back_crate = self.region(
            "Kitchen Back Crate",
            [
                "Kitchen Back Night Vision Goggles",
            ],
        )
        self.connect(inside_db_kitchen, kitchen_back_crate, r.jump)

        slaughterhouse = self.region(
            "Slaughterhouse",
            [
                "Slaughterhouse Devastator",
            ],
        )
        self.connect(inside_db_kitchen, slaughterhouse, self.red_key)

        slaughterhouse_vent = self.region(
            "Slaughterhouse Vent",
            [
                "Slaughterhouse Vent Medkit",
            ],
        )
        self.connect(slaughterhouse, slaughterhouse_vent, r.jump)

        # Can just walk/run past the tripmines. a bit obscure, so medium difficulty.
        conveyers = self.region(
            "Slaughterhouse Conveyers",
            [
                "Slaughterhouse Tripmine",
            ],
        )
        self.connect(slaughterhouse, conveyers, r.difficulty("medium") | r.explosives)

        conveyers_upper = self.region(
            "Slaughterhouse Conveyers Upper",
            [
                "Secret Conveyer Upper",
                "Conveyer Upper RPG",
            ],
        )
        self.connect(conveyers, conveyers_upper, r.jump & r.can_use)

        dog_kennel = self.region(
            "Secret Dog Kennel",
            [
                "Secret Dog Kennel",
                "Dog Kennel Pipebombs",
            ],
        )
        self.connect(conveyers_upper, dog_kennel, r.jump & r.explosives & r.can_open)

        manager_room_inside = self.region(
            "Manager Room Inside",
            [],
        )
        manager_room_outside = self.region(
            "Manager Room Outside",
            [
                "Manager Room Tripmine 1",
                "Manager Room Tripmine 2",
            ],
        )
        self.connect(conveyers_upper, manager_room_inside, r.true)
        self.connect(manager_room_inside, manager_room_outside, r.true)

        exit_room = self.region(
            "Exit room",
            [
                "Exit",
            ],
        )
        # Outside path requires open or jump
        self.connect(manager_room_outside, manager_room_inside, r.can_open | r.jump)
        # Inside path only requires use
        self.connect(manager_room_inside, exit_room, r.can_use)

        # Alternate path by blowing up office wall from the outside
        # Medium difficulty because its obscure
        self.connect(
            ret,
            manager_room_outside,
            r.difficulty("medium") & r.pipebomb & r.can_crouch & r.glitched,
        )

        manager_room_cabinet = self.region(
            "Manager Room Cabinet",
            [
                "Manager Room Armor",
            ],
        )
        self.connect(manager_room_inside, manager_room_cabinet, r.jump)
        return ret
