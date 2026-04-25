from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L8(D3DLevel):
    name = "Dark Side"
    levelnum = 7
    volumenum = 1
    keys = ["Blue", "Yellow"]
    location_defs = [
        {"id": 42, "name": "Overlord Pool Pipebombs", "type": "sprite", "density": 4},
        {
            "id": 156,
            "name": "Beta Wall Atomic Health 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 157,
            "name": "Beta Wall Atomic Health 2",
            "type": "sprite",
            "density": 3,
        },
        {"id": 203, "name": "Overlord Pool Shrinker", "type": "sprite", "density": 3},
        {"id": 206, "name": "Hatching Pipebombs", "type": "sprite", "density": 0},
        {"id": 207, "name": "Surface Pipebombs", "type": "sprite", "density": 0},
        {"id": 211, "name": "Spacesuit RPG", "type": "sprite", "density": 3},
        {"id": 212, "name": "Outlook Devastator", "type": "sprite", "density": 4},
        {"id": 226, "name": "Beta Armor", "type": "sprite", "density": 0},
        {"id": 242, "name": "Beta Pipebombs", "type": "sprite", "density": 0},
        {"id": 247, "name": "Reactor Control Armor", "type": "sprite", "density": 3},
        {"id": 251, "name": "Babes Shotgun", "type": "sprite", "density": 0},
        {"id": 257, "name": "Gamma Vent Atomic Health", "type": "sprite", "density": 3},
        {"id": 261, "name": "Gamma Medkit", "type": "sprite", "density": 0},
        {"id": 265, "name": "Top of Hub Chaingun", "type": "sprite", "density": 0},
        {"id": 266, "name": "Hub Crate RPG", "type": "sprite"},
        {
            "id": 269,
            "name": "Reactor Control Devastator",
            "type": "sprite",
            "density": 0,
        },
        {"id": 342, "name": "Hub Atomic Health 1", "type": "sprite", "density": 2},
        {"id": 343, "name": "Hub Atomic Health 2", "type": "sprite", "density": 3},
        {"id": 347, "name": "Alpha Lab Armor", "type": "sprite", "density": 3},
        {"id": 348, "name": "Alpha Lab Atomic Health", "type": "sprite", "density": 0},
        {"id": 359, "name": "Waste Pool Pipebombs", "type": "sprite", "density": 0},
        {"id": 361, "name": "Alpha Lab Tripmine", "type": "sprite", "density": 4},
        {"id": 363, "name": "Alpha Lab Pipebombs", "type": "sprite", "density": 3},
        {"id": 364, "name": "Alpha Lab Medkit", "type": "sprite", "density": 0},
        {"id": 372, "name": "Start Shotgun", "type": "sprite", "density": 4},
        {
            "id": 374,
            "name": "Crumbling Canyon Atomic Health",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 375,
            "name": "Crumbling Canyon Chaingun",
            "type": "sprite",
            "density": 0,
        },
        {"id": 406, "name": "MP Tank Chaingun", "type": "sprite", "density": 5},
        {"id": 407, "name": "Tank Shrinker", "type": "sprite", "density": 0},
        {"id": 520, "name": "Blue Key Card", "type": "sprite", "density": 0},
        {"id": 790, "name": "Hub Freezethrower", "type": "sprite", "density": 3},
        {"id": 797, "name": "Hub Armor", "type": "sprite", "density": 4},
        {"id": 801, "name": "Alpha Wall Devastator", "type": "sprite", "density": 2},
        {"id": 836, "name": "MP Tank RPG", "type": "sprite", "density": 5},
        {"id": 837, "name": "Alpha Pipebombs", "type": "sprite", "density": 4},
        {"id": 843, "name": "Yellow Key Card", "type": "sprite", "density": 0},
        {"id": 932, "name": "Start Armor", "type": "sprite", "density": 0},
        {
            "id": 952,
            "name": "Outlook Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {"id": 953, "name": "Alpha Lab Steroids", "type": "sprite", "density": 0},
        {"id": 954, "name": "Alpha Lab Holo Duke", "type": "sprite", "density": 3},
        {
            "id": 955,
            "name": "Reactor Control Protective Boots",
            "type": "sprite",
            "density": 4,
        },
        {
            "id": 989,
            "name": "Top of Hub Night Vision Goggles",
            "type": "sprite",
            "density": 0,
        },
        {"id": 990, "name": "Top of Hub Armor", "type": "sprite", "density": 4},
        {"id": 991, "name": "MP Start Jetpack", "type": "sprite", "density": 5},
        {
            "id": 992,
            "name": "MP Surface Atomic Health 1",
            "type": "sprite",
            "density": 5,
        },
        {
            "id": 993,
            "name": "MP Surface Atomic Health 2",
            "type": "sprite",
            "density": 5,
        },
        {"id": 994, "name": "MP Surface Steroids", "type": "sprite", "density": 5},
        {"id": 995, "name": "MP Surface Jetpack", "type": "sprite", "density": 5},
        {"id": 996, "name": "MP Surface Shrinker", "type": "sprite", "density": 5},
        {"id": 997, "name": "MP Surface RPG", "type": "sprite", "density": 5},
        {"id": 998, "name": "MP Surface Freezethrower", "type": "sprite", "density": 5},
        {"id": 1007, "name": "Gamma Tripmine 1", "type": "sprite", "density": 3},
        {"id": 1008, "name": "Gamma Shrinker", "type": "sprite", "density": 2},
        {"id": 1009, "name": "Gamma Tripmine 2", "type": "sprite", "density": 4},
        {"id": 1016, "name": "Outlook Atomic Health", "type": "sprite", "density": 0},
        {"id": 1017, "name": "Babes Pipebombs 1", "type": "sprite", "density": 2},
        {"id": 1018, "name": "Babes Pipebombs 2", "type": "sprite", "density": 3},
        {"id": 1019, "name": "Babes Pipebombs 3", "type": "sprite", "density": 4},
        {"id": 352, "name": "Secret Babes Wall", "type": "sector"},
        {"id": 579, "name": "Secret Alpha Lab Tanks", "type": "sector"},
        {"id": 647, "name": "Secret Hub Monitor", "type": "sector"},
        {"id": 675, "name": "Secret Beta Transport Wall", "type": "sector"},
        {"id": 701, "name": "Secret Alpha Cracked Wall", "type": "sector"},
        {"id": 713, "name": "Secret Gamma Monitor", "type": "sector"},
        {"id": 726, "name": "Secret Overlord Overhang", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
        {"id": 11, "name": "Secret Exit", "type": "exit"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [],
        )
        past_door = self.region(
            "Past Door",
            [
                "MP Start Jetpack",
                "Start Armor",
                "Start Shotgun",
                "Hub Atomic Health 1",
                "Hub Atomic Health 2",
                "Hub Armor",
                "Hub Freezethrower",
                "Secret Hub Monitor",
                "Alpha Pipebombs",
            ],
        )
        self.connect(ret, past_door, r.can_open)
        # can collect the items, but not the secret trigger
        self.restrict("Secret Hub Monitor", r.can_crouch)

        alpha_transport = self.region(
            "Alpha Transport",
            [
                "Alpha Lab Steroids",
                "Alpha Lab Tripmine",
                "Alpha Lab Medkit",
                "Alpha Lab Holo Duke",
                "Alpha Lab Pipebombs",
                "Secret Alpha Lab Tanks",
                "Crumbling Canyon Atomic Health",
                "Crumbling Canyon Chaingun",
            ],
        )
        self.connect(past_door, alpha_transport, r.can_use)

        alpha_wall = self.region(
            "Alpha Wall", ["Secret Alpha Cracked Wall", "Alpha Wall Devastator"]
        )
        self.connect(past_door, alpha_wall, r.explosives)

        alpha_lab_tanks = self.region(
            "Alpha Lab Tanks", ["MP Tank Chaingun", "MP Tank RPG", "Tank Shrinker"]
        )
        self.connect(alpha_transport, alpha_lab_tanks, r.can_dive)

        alpha_lab_backroom = self.region(
            "Alpha Lab Backroom",
            [
                "Blue Key Card",
                "Alpha Lab Armor",
                "Alpha Lab Atomic Health",
                "Waste Pool Pipebombs",
            ],
        )
        self.connect(alpha_transport, alpha_lab_backroom, r.jump)
        self.restrict("Waste Pool Pipebombs", r.can_dive)

        top_of_hub = self.region(
            "Top of Hub",
            [
                "Top of Hub Night Vision Goggles",
                "Top of Hub Armor",
                "Hub Crate RPG",
                "Top of Hub Chaingun",
                "Gamma Tripmine 1",
                "Gamma Tripmine 2",
            ],
        )
        self.connect(
            past_door,
            top_of_hub,
            self.blue_key | r.jetpack(50) | (r.difficulty("medium") & r.can_jump),
        )
        self.restrict(
            "Top of Hub Chaingun",
            r.jetpack(50)
            | (r.can_jump & (r.can_sprint | r.steroids | r.difficulty("medium"))),
        )

        gamma_transport = self.region(
            "Gamma Transport",
            [
                "Gamma Medkit",
                "Gamma Vent Atomic Health",  # can just walk in from below
                "Babes Shotgun",
                "Reactor Control Protective Boots",
                "Reactor Control Devastator",
            ],
        )
        self.connect(past_door, gamma_transport, r.can_use)

        gamma_secret = self.region(
            "Gamma Transport Secret", ["Secret Gamma Monitor", "Gamma Shrinker"]
        )
        self.connect(gamma_transport, gamma_secret, r.jump)

        babes_secret = self.region(
            "Cracked Wall near Babes",
            [
                "Secret Babes Wall",
                "Babes Pipebombs 1",
                "Babes Pipebombs 2",
                "Babes Pipebombs 3",
            ],
        )
        self.connect(gamma_transport, babes_secret, r.jump & r.explosives)

        reactor_control_ledge = self.region(
            "Reactor Control Ledge", ["Reactor Control Armor", "Yellow Key Card"]
        )
        # can get pushed up by enemies after explosion, but a bit annoying
        self.connect(
            gamma_transport, reactor_control_ledge, r.jump | r.difficulty("extreme")
        )

        beta_pre_transport = self.region(
            "Beta Pre-Transport",
            [
                "Beta Pipebombs",
            ],
        )
        self.connect(past_door, beta_pre_transport, self.yellow_key)

        beta_transport = self.region(
            "Beta Transport",
            [
                "Secret Beta Transport Wall",
                "Beta Wall Atomic Health 1",
                "Beta Wall Atomic Health 2",
                "Beta Armor",
                "Spacesuit RPG",
                "MP Surface Atomic Health 1",
                "MP Surface Atomic Health 2",
                "MP Surface Steroids",
                "MP Surface Jetpack",
                "MP Surface Shrinker",
                "MP Surface RPG",
                "MP Surface Freezethrower",
                "Outlook Night Vision Goggles",
                "Outlook Atomic Health",
                "Outlook Devastator",
                "Surface Pipebombs",
            ],
        )

        self.connect(beta_pre_transport, beta_transport, r.can_use)

        final_area = self.region(
            "Final Area",
            [
                "Hatching Pipebombs",
                "Overlord Pool Shrinker",
                "Overlord Pool Pipebombs",
                "Exit",
            ],
        )
        # can use surrounding enemies to blow up wall, but it's annoying to set up
        self.connect(beta_transport, final_area, r.explosives | r.difficulty("hard"))
        self.restrict("Exit", r.can_dive & r.can_use)

        secret_exit = self.region(
            "Overlord Overhang", ["Secret Overlord Overhang", "Secret Exit"]
        )
        self.connect(final_area, secret_exit, r.jump)
        self.restrict("Secret Exit", r.can_use)
        return ret
