from BaseClasses import Region

from ..base_classes import D3DLevel


class E1L6(D3DLevel):
    name = "Launch Facility"
    levelnum = 5
    volumenum = 0
    keys = ["Blue", "Red"]
    location_defs = [
        {"name": "Rocket Jetpack", "id": 0, "type": "sprite", "density": 0},
        {"name": "Toxic Waste Pool Shotgun", "id": 123, "type": "sprite", "density": 0},
        {"name": "Start Protective Boots", "id": 124, "type": "sprite", "density": 0},
        {
            "name": "Outside Rocket Night Vision Goggles",
            "id": 385,
            "type": "sprite",
            "density": 1,
        },
        {"name": "Dark Room RPG", "id": 395, "type": "sprite", "density": 3},
        {"name": "Dark Room Pipebombs 1", "id": 397, "type": "sprite", "density": 3},
        {"name": "Dark Room Pipebombs 2", "id": 398, "type": "sprite", "density": 4},
        {"name": "Spiral Chaingun", "id": 406, "type": "sprite", "density": 3},
        {"name": "Dark Room Atomic Health", "id": 410, "type": "sprite", "density": 0},
        {"name": "Blue Key Card", "id": 518, "type": "sprite", "density": 0},
        {"name": "Red Key Card", "id": 539, "type": "sprite", "density": 0},
        {
            "name": "Sewer Computers Atomic Health 1",
            "id": 561,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Sewer Computers Atomic Health 2",
            "id": 562,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Sewer Computers Atomic Health 3",
            "id": 563,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Sewer Protective Boots", "id": 567, "type": "sprite", "density": 0},
        {"name": "Dark Room Medkit", "id": 575, "type": "sprite", "density": 1},
        {
            "name": "Toxic Waste Pool Atomic Health 2",
            "id": 588,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Toxic Waste Pool Atomic Health 1",
            "id": 589,
            "type": "sprite",
            "density": 2,
        },
        {"name": "MP Spiral Holo Duke", "id": 625, "type": "sprite", "density": 5},
        {"name": "Vent Pipebombs", "id": 642, "type": "sprite", "density": 2},
        {"name": "Launch Room Steroids", "id": 643, "type": "sprite", "density": 3},
        {"name": "Start Armor", "id": 647, "type": "sprite", "density": 1},
        {"name": "MP Start Steroids", "id": 690, "type": "sprite", "density": 5},
        {"name": "MP Rocket Pit Pipebombs", "id": 691, "type": "sprite", "density": 5},
        {"name": "MP Toxic Waste Pool RPG", "id": 692, "type": "sprite", "density": 5},
        {"name": "MP Rocket Chaingun", "id": 693, "type": "sprite", "density": 5},
        {"name": "MP Gate Room Shotgun", "id": 696, "type": "sprite", "density": 5},
        {"name": "Launch Room Holo Duke", "id": 697, "type": "sprite", "density": 1},
        {"name": "Gate Room Armor", "id": 707, "type": "sprite", "density": 2},
        {"name": "MP Start Jetpack", "id": 726, "type": "sprite", "density": 5},
        {"name": "Secret Sewer Computers", "id": 218, "type": "sector"},
        {"name": "Secret Toxic Waste Pool", "id": 224, "type": "sector"},
        {"name": "Secret Dark Room Ceiling Vent", "id": 277, "type": "sector"},
        {"name": "Secret Gate Room Wall", "id": 327, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]
    must_dive = True
    events = ["Ready Rocket"]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "MP Start Jetpack",
                # can just walk off
                "MP Start Steroids",
                "Start Protective Boots",
                "Start Armor",
            ],
        )
        self.restrict(
            "Start Protective Boots",
            r.can_open | (r.crouch_jump & r.difficulty("hard")),
        )

        past_forcefield = self.region(
            "Past Forcefield",
            [
                "Spiral Chaingun",
                "MP Spiral Holo Duke",
                "Blue Key Card",
                "Dark Room Pipebombs 1",
                "Dark Room Pipebombs 2",
                "Dark Room RPG",
                "Dark Room Medkit",
                "Dark Room Atomic Health",
            ],
        )
        self.connect(ret, past_forcefield, r.can_use)
        self.restrict("Dark Room Atomic Health", r.sr50 | r.jump)

        waste_pool = self.region(
            "Secret Toxic Waste Pool",
            [
                "Secret Toxic Waste Pool",
                "Toxic Waste Pool Shotgun",
                "Toxic Waste Pool Atomic Health 1",
                "Toxic Waste Pool Atomic Health 2",
                "MP Toxic Waste Pool RPG",
            ],
        )
        self.connect(past_forcefield, waste_pool, r.can_dive)

        vent = self.region(
            "Dark Room Vent", ["Secret Dark Room Ceiling Vent", "Vent Pipebombs"]
        )
        # Plenty of lizard troopers to jump on
        self.connect(
            past_forcefield, vent, r.jetpack(50) | (r.difficulty("medium") & r.can_jump)
        )

        gate_corridor = self.region("Gate Corridor")

        gate_corridor_room = self.region(
            "Gate Corridor Room",
            [
                "MP Gate Room Shotgun",
                "Red Key Card",
            ],
        )
        # need to open door or get up through window, but need to lure an enemy from far to jump on them
        self.connect(
            gate_corridor,
            gate_corridor_room,
            r.can_open
            | r.jetpack(50)
            | (
                (r.difficulty("extreme") | (r.sprint & r.difficulty("hard")))
                & r.can_jump
            ),
        )
        self.connect(
            past_forcefield,
            gate_corridor,
            self.blue_key | r.crouch_jump,
        )

        gate_secret = self.region(
            "Gate Room Secret", ["Secret Gate Room Wall", "Gate Room Armor"]
        )
        self.connect(gate_corridor, gate_secret, r.can_open)

        launch_pad = self.region(
            "Launch Pad",
            [
                "Outside Rocket Night Vision Goggles",
            ],
        )
        self.connect(gate_corridor_room, launch_pad, r.true)
        self.connect(past_forcefield, launch_pad, r.crouch_jump)
        self.connect(launch_pad, gate_corridor, r.true)

        rocket = self.region(
            "Rocket",
            ["Rocket Jetpack", "MP Rocket Chaingun", "Ready Rocket"],
        )
        self.connect(launch_pad, rocket, r.can_open | r.jetpack(100))
        self.restrict("Ready Rocket", self.red_key)

        launch_room = self.region(
            "Launch Room", ["Launch Room Steroids", "Launch Room Holo Duke"]
        )
        self.connect(
            launch_pad,
            launch_room,
            r.can_crouch | (r.difficulty("hard") & r.jetpack(50)),
        )

        rocket_pit = self.region("Rocket Pit", ["MP Rocket Pit Pipebombs", "Exit"])
        # Need to get out of the launch room again. Might be possible to activate this from outside somehow?
        self.connect(
            launch_room, rocket_pit, self.event("Ready Rocket") & r.can_use & r.jump
        )
        self.restrict("Exit", r.can_use)

        sewer_ledge = self.region(
            "Sewer Ledge",
            [
                "Sewer Protective Boots",
            ],
        )
        # Can clip up the slope by walking into the corner of it
        self.connect(rocket_pit, sewer_ledge, r.jump | r.difficulty("medium"))

        sewer_secret = self.region(
            "Sewer Ledge Secret",
            [
                "Secret Sewer Computers",
                "Sewer Computers Atomic Health 1",
                "Sewer Computers Atomic Health 2",
                "Sewer Computers Atomic Health 3",
            ],
        )
        self.connect(
            sewer_ledge,
            sewer_secret,
            r.can_open
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        return ret
