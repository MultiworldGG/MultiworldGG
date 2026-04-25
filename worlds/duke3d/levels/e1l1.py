from BaseClasses import Region

from ..base_classes import D3DLevel


class E1L1(D3DLevel):
    name = "Hollywood Holocaust"
    levelnum = 0
    volumenum = 0
    keys = ["Red"]
    location_defs = [
        {
            "name": "Exit Ledge Night Vision Goggles",
            "id": 25,
            "type": "sprite",
            "density": 1,
        },
        {"name": "Bachelor RPG", "id": 26, "type": "sprite", "density": 2},
        {"name": "Bachelor Pipebombs", "id": 27, "type": "sprite", "density": 2},
        {"name": "Elevator Night Vision", "id": 40, "type": "sprite", "density": 0},
        {"name": "Bachelor Shotgun", "id": 44, "type": "sprite", "density": 4},
        {"name": "Bachelor Chaingun", "id": 45, "type": "sprite", "density": 4},
        {"name": "MP Start Shotgun", "id": 81, "type": "sprite", "density": 5},
        {"name": "Billboard RPG", "id": 82, "type": "sprite", "density": 2},
        {
            "name": "MP Chaingun behind Screen",
            "id": 111,
            "type": "sprite",
            "density": 5,
        },
        {
            "name": "Outside Ledge Atomic Health",
            "id": 170,
            "type": "sprite",
            "density": 3,
        },
        {
            "name": "Cash Register Atomic Health",
            "id": 209,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Arcade Holo Duke", "id": 297, "type": "sprite", "density": 0},
        {"name": "Cash Register Shotgun", "id": 337, "type": "sprite", "density": 3},
        {"name": "Toilet Medkit", "id": 376, "type": "sprite", "density": 3},
        {"name": "Projector Atomic Health", "id": 400, "type": "sprite", "density": 4},
        {"name": "Vent Holo Duke", "id": 411, "type": "sprite", "density": 1},
        {"name": "MP Exit Shotgun", "id": 421, "type": "sprite", "density": 5},
        {"name": "Projector Secret RPG", "id": 431, "type": "sprite", "density": 2},
        {"name": "Jetpack behind Screen", "id": 447, "type": "sprite", "density": 2},
        {"name": "Red Key Card", "id": 451, "type": "sprite", "density": 0},
        {"name": "Poster Steroids", "id": 527, "type": "sprite", "density": 2},
        {"name": "MP Apartment Chaingun", "id": 530, "type": "sprite", "density": 5},
        {"name": "Cinema Armor", "id": 532, "type": "sprite", "density": 0},
        {"name": "MP Red Door Pipebombs", "id": 535, "type": "sprite", "density": 5},
        {
            "name": "Cash Register Alcove Armor",
            "id": 546,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Projector Steroids", "id": 595, "type": "sprite", "density": 4},
        {"name": "Elevator Pipebombs", "id": 632, "type": "sprite", "density": 3},
        {"name": "Jetpack above Exit", "id": 633, "type": "sprite", "density": 0},
        {"name": "Secret Behind the Screen", "id": 149, "type": "sector"},
        {"name": "Secret Projector Hidden Room", "id": 154, "type": "sector"},
        {"name": "Secret Hidden Apartment", "id": 197, "type": "sector"},
        {"name": "Secret Projector Security Room", "id": 211, "type": "sector"},
        {"name": "Secret Behind Poster", "id": 238, "type": "sector"},
        {"name": "Secret Cash Register Alcove", "id": 241, "type": "sector"},
        {"name": "Secret Bachelor Apartment", "id": 249, "type": "sector"},
        {"name": "Secret Below Billboard", "id": 290, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "MP Start Shotgun",
            ],
        )

        cinema = self.region(
            "Cinema",
            [
                "Cinema Armor",
            ],
        )
        # Enter from outside via explosives through window and kicking the door
        self.connect(ret, cinema, r.can_open | (r.explosives & r.glitch_kick))

        projector_room = self.region(
            "Projector Room",
            [
                "Red Key Card",
                "Projector Steroids",
            ],
        )
        self.connect(cinema, projector_room, r.can_open | r.jetpack(50))

        toilet_vent = self.region(
            "Toilet Vent",
            [
                "Toilet Medkit",
                "Vent Holo Duke",
                "Secret Projector Security Room",
            ],
        )
        # sr50 down from the top of the vent and hold crouch as you fall to make it on top
        self.restrict(
            "Vent Holo Duke",
            r.explosives
            & (
                r.jump
                | (
                    r.can_crouch
                    & (r.difficulty("extreme") | (r.difficulty("medium") & r.sprint))
                )
            ),
        )
        # Access also possible from projector room with can_open
        self.connect(cinema, toilet_vent, r.jump | r.can_open)

        cash_register = self.region(
            "Cash Register",
            [
                "Cash Register Shotgun",
                "Cash Register Atomic Health",
            ],
        )
        self.connect(cinema, cash_register, r.can_open)

        cash_register_secret = self.region(
            "Cash Register Secret",
            [
                "Secret Cash Register Alcove",
                "Cash Register Alcove Armor",
            ],
        )
        self.connect(
            cinema, cash_register_secret, r.can_use & (r.jetpack(50) | r.can_open)
        )

        arcade = self.region("Arcade", ["Arcade Holo Duke"])
        self.connect(cinema, arcade, r.can_open)
        self.restrict("Arcade Holo Duke", r.can_use)

        exit_connector = self.region(
            "Exit Connector",
            ["MP Red Door Pipebombs"],
        )
        self.connect(arcade, exit_connector, self.red_key & r.can_open)

        apartment = self.region(
            "Apartments",
            [
                "Billboard RPG",
                "Outside Ledge Atomic Health",
                "Poster Steroids",
                "MP Apartment Chaingun",
                "Secret Hidden Apartment",
                "Secret Behind Poster",
                "Secret Below Billboard",
            ],
        )
        self.restrict(
            "Poster Steroids",
            r.can_open
            | (r.glitched & r.can_crouch & r.fast_sprint & r.difficulty("medium")),
        )
        self.restrict(
            "Secret Behind Poster",
            r.can_open
            | (r.glitched & r.can_crouch & r.fast_sprint & r.difficulty("medium")),
        )
        self.connect(ret, apartment, r.jump)

        projector_ledges = self.region(
            "Projector Ledges",
            [
                "Projector Atomic Health",
                "Projector Secret RPG",
                "Secret Projector Hidden Room",
            ],
        )
        self.connect(projector_room, projector_ledges, r.jump)

        elevator_alcove = self.region(
            "Elevator Alcove",
            [
                "Elevator Night Vision",
                "Elevator Pipebombs",
            ],
        )
        self.connect(cinema, elevator_alcove, r.jump & r.can_open)

        exit_ledge = self.region(
            "Exit Ledge",
            [
                "Exit Ledge Night Vision Goggles",
                "Exit",
                "MP Exit Shotgun",
            ],
        )
        self.connect(
            ret,
            exit_ledge,
            (r.difficulty("medium") & r.jump) | r.jetpack(50),
        )
        self.restrict("Exit", r.can_use)
        self.connect(exit_connector, exit_ledge, r.can_open)
        self.connect(exit_ledge, exit_connector, r.can_open)

        bachelor_secret = self.region(
            "Bachelor Apartment",
            [
                "Bachelor RPG",
                "Bachelor Pipebombs",
                "Bachelor Shotgun",
                "Bachelor Chaingun",
                "Secret Bachelor Apartment",
            ],
        )
        self.connect(exit_ledge, bachelor_secret, r.jump)

        behind_screen = self.region(
            "Behind the Screen",
            [
                "Secret Behind the Screen",
                "Jetpack behind Screen",
                "MP Chaingun behind Screen",
            ],
        )
        self.connect(
            exit_ledge, behind_screen, r.difficulty("medium")
        )  # Can just walk off the ledge
        self.connect(
            projector_room, behind_screen, (r.can_jump & r.explosives & r.can_use)
        )
        self.connect(ret, behind_screen, r.jetpack(50))

        top_of_building = self.region(f"Top of Building", ["Jetpack above Exit"])
        self.connect(ret, top_of_building, r.jetpack(200))
        self.connect(exit_ledge, top_of_building, r.crouch_jump)  # glitched logic
        return ret
