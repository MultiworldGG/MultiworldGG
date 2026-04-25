from BaseClasses import Region

from ..base_classes import D3DLevel


class E3L2(D3DLevel):
    name = "Bank Roll"
    levelnum = 1
    volumenum = 2
    keys = ["Blue", "Red"]
    location_defs = [
        {
            "id": 54,
            "name": "Top of Gears Protective Boots",
            "type": "sprite",
            "density": 4,
        },
        {"id": 66, "name": "Start Pipebombs", "type": "sprite", "density": 3},
        {
            "id": 85,
            "name": "Vending Machine Atomic Health",
            "type": "sprite",
            "density": 3,
        },
        {"id": 96, "name": "ATM Chaingun", "type": "sprite", "density": 2},
        {"id": 106, "name": "Pillar Pipebombs", "type": "sprite", "density": 3},
        {"id": 223, "name": "Bank Phone Holo Duke", "type": "sprite", "density": 2},
        {
            "id": 264,
            "name": "Dumpster Trashcan Steroids",
            "type": "sprite",
            "sprite_type": "trashcan",
            "density": 3,
        },
        {"id": 265, "name": "Dumpster Medkit", "type": "sprite", "density": 0},
        {"id": 354, "name": "Top of Gears Jetpack", "type": "sprite", "density": 3},
        {"id": 355, "name": "Red Key Card", "type": "sprite", "density": 0},
        {"id": 424, "name": "Start Shotgun", "type": "sprite", "density": 4},
        {"id": 425, "name": "Start Ledge RPG", "type": "sprite", "density": 0},
        {"id": 440, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {
            "id": 484,
            "name": "Office Painting Devastator",
            "type": "sprite",
            "density": 2,
        },
        {"id": 503, "name": "Bank Painting Jetpack", "type": "sprite", "density": 2},
        {"id": 506, "name": "Office Steroids", "type": "sprite", "density": 4},
        {
            "id": 507,
            "name": "Office Entrance Freezethrower",
            "type": "sprite",
            "density": 1,
        },
        {"id": 511, "name": "Switch Shrinker", "type": "sprite", "density": 1},
        {
            "id": 512,
            "name": "Office Entrance Pipebombs",
            "type": "sprite",
            "density": 3,
        },
        {"id": 516, "name": "Office Ledge Armor", "type": "sprite", "density": 3},
        {
            "id": 517,
            "name": "Office Far Ledge Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {
            "id": 518,
            "name": "Office Far Ledge Tripmine 1",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 519,
            "name": "Office Far Ledge Tripmine 2",
            "type": "sprite",
            "density": 4,
        },
        {"id": 533, "name": "Exit Medkit", "type": "sprite", "density": 0},
        {"id": 537, "name": "Gear Protective Boots", "type": "sprite", "density": 3},
        {"id": 539, "name": "Gear Atomic Health", "type": "sprite", "density": 2},
        {"id": 17, "name": "Secret Bank Phone", "type": "sector"},
        {"id": 119, "name": "Secret ATM", "type": "sector"},
        {"id": 190, "name": "Secret Office Painting", "type": "sector"},
        {"id": 208, "name": "Secret Bank Painting", "type": "sector"},
        {"id": 235, "name": "Secret Gears Breakable Wall", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Dumpster Medkit",
                "Start Pipebombs",
                "Start Shotgun",
                "Dumpster Trashcan Steroids",
                "Pillar Pipebombs",
                "Start Ledge RPG",
                # Door opens once automatically, don't need Open to get inside
                "Office Entrance Pipebombs",
                "Office Entrance Freezethrower",
                "Vending Machine Atomic Health",
            ],
        )
        self.restrict(
            "Start Ledge RPG",
            r.jetpack(50) | (r.can_jump & r.sprint)
            # need specifically an enforcer to jump up
            | (r.difficulty("hard") & r.can_jump),
        )
        self.restrict("Vending Machine Atomic Health", r.jump)

        office = self.region(
            "Office", ["Blue Key Card", "Office Steroids", "Office Ledge Armor"]
        )
        self.connect(ret, office, r.can_open | r.jetpack(50))

        far_ledge = self.region(
            "Office Far Ledge",
            [
                "Office Far Ledge Atomic Health",
                "Office Far Ledge Tripmine 1",
                "Office Far Ledge Tripmine 2",
            ],
        )
        self.connect(
            office, far_ledge, r.jump | r.sprint
        )  # Can maybe SR50 the gap from the other ledge

        office_ledges = self.region(
            "Office Ledges",
            [
                "Office Painting Devastator",
                "Secret Office Painting",
            ],
        )
        self.connect(office, office_ledges, r.jump)

        atm = self.region(
            "ATM",
            ["ATM Chaingun", "Secret ATM"],
        )
        self.connect(
            ret,
            atm,
            # need double sprint speed to clip without squishing
            (r.can_open | r.glitched & r.fast_sprint & r.can_crouch)
            & (r.jump | (r.difficulty("medium") & r.sprint)),
        )  # Can run off the ledge, timing is a bit tricky with steroids + no run

        bank = self.region("Bank Entrance")
        # Difficult trip clip
        self.connect(
            ret,
            bank,
            (self.blue_key & r.can_open)
            | (
                r.difficulty("extreme")
                & r.glitched
                & r.can_jump
                & r.fast_sprint
                & r.tripmine
            ),
        )

        bank_phone = self.region(
            "Bank Phone Secret",
            [
                "Bank Phone Holo Duke",
                "Secret Bank Phone",
            ],
        )
        self.connect(bank, bank_phone, r.jump)

        bank_painting = self.region(
            "Bank Painting Secret",
            [
                "Secret Bank Painting",
                "Bank Painting Jetpack",
            ],
        )
        self.connect(
            bank,
            bank_painting,
            r.jump & (r.can_open | (r.glitched & r.can_crouch & r.sprint)),
        )

        bank_backroom = self.region("Bank Backroom", ["Switch Shrinker"])
        self.connect(bank, bank_backroom, r.can_open)
        self.restrict("Switch Shrinker", r.jump)

        gears = self.region(
            "Gear Room",
            ["Gear Protective Boots"],
        )
        # the trigger plates are just a bit too tall
        self.connect(bank_backroom, gears, r.jump)

        top_of_gears = self.region(
            "Top of Gears",
            ["Top of Gears Protective Boots", "Top of Gears Jetpack", "Red Key Card"],
        )
        # can SR50 clip onto moving gear without sprint speed
        self.connect(
            gears,
            top_of_gears,
            r.can_open
            | r.jetpack(100)
            | r.glitched & ((r.difficulty("medium") & r.sprint) | r.difficulty("hard")),
        )

        gears_secret = self.region(
            "Gears Secret", ["Secret Gears Breakable Wall", "Gear Atomic Health"]
        )
        self.connect(gears, gears_secret, r.explosives)

        vault = self.region("Bank Vault", ["Exit Medkit", "Exit"])
        # Can shoot rockets through the wall corner, precise setup and deadly if you get it wrong
        self.connect(
            bank_backroom,
            vault,
            (self.red_key & r.can_open)
            | (r.glitched & r.difficulty("hard") & (r.rpg | r.devastator)),
        )
        self.connect(gears_secret, vault, r.pipebomb)  # Can throw through crack
        self.restrict("Exit", r.can_use)

        return ret
