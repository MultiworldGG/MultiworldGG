from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L9(D3DLevel):
    name = "Overlord"
    levelnum = 8
    volumenum = 1
    keys = []
    location_defs = [
        {"id": 7, "name": "Timed Wall RPG", "type": "sprite"},
        {"id": 8, "name": "Control Room Armor", "type": "sprite", "density": 4},
        {"id": 9, "name": "Waterfall Armor", "type": "sprite", "density": 4},
        {"id": 10, "name": "Vents Pipebombs 1", "type": "sprite", "density": 3},
        {"id": 12, "name": "Overlord Tunnel Medkit", "type": "sprite", "density": 3},
        {"id": 13, "name": "Broken Wall Medkit", "type": "sprite", "density": 3},
        {
            "id": 14,
            "name": "Waterfall Night Vision Goggles",
            "type": "sprite",
            "density": 4,
        },
        {"id": 15, "name": "Waterfall Scuba Gear", "type": "sprite", "density": 3},
        {"id": 16, "name": "Hidden Wall Atomic Health", "type": "sprite", "density": 2},
        {"id": 39, "name": "Hidden Wall Armor", "type": "sprite", "density": 3},
        {"id": 69, "name": "Waterfall Tripmine", "type": "sprite", "density": 3},
        {"id": 70, "name": "Overlord Tripmine 1", "type": "sprite", "density": 3},
        {"id": 71, "name": "Overlord Tripmine 2", "type": "sprite", "density": 4},
        {"id": 73, "name": "Overlord Atomic Health", "type": "sprite", "density": 0},
        {
            "id": 78,
            "name": "Combination Lock Scuba Gear",
            "type": "sprite",
            "density": 3,
        },
        {
            "id": 81,
            "name": "Control Room Night Vision Goggles",
            "type": "sprite",
            "density": 3,
        },
        {"id": 83, "name": "Control Room Chaingun", "type": "sprite", "density": 0},
        {
            "id": 84,
            "name": "Vents Center Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 86, "name": "Waterfall Atomic Health", "type": "sprite", "density": 0},
        {"id": 93, "name": "Waterfall Shrinker", "type": "sprite", "density": 0},
        {
            "id": 94,
            "name": "Overlord Tunnel Devastator",
            "type": "sprite",
            "density": 3,
        },
        {"id": 96, "name": "Waterfall RPG", "type": "sprite", "density": 0},
        {"id": 100, "name": "Reactor Freezethrower", "type": "sprite", "density": 0},
        {"id": 102, "name": "Start Underwater Shotgun", "type": "sprite", "density": 0},
        {
            "id": 104,
            "name": "Start Underwater Atomic Health",
            "type": "sprite",
            "density": 0,
        },
        {"id": 159, "name": "Vents Pipebombs 2", "type": "sprite", "density": 4},
        {"id": 395, "name": "Waterfall Holo Duke", "type": "sprite", "density": 0},
        {"id": 396, "name": "Overlord Tunnel Jetpack", "type": "sprite", "density": 0},
        {"id": 413, "name": "Timed Wall Medkit", "type": "sprite", "density": 3},
        {"id": 415, "name": "Timed Wall Atomic Health", "type": "sprite", "density": 2},
        {
            "id": 424,
            "name": "Waterfall Wall Pipebombs 1",
            "type": "sprite",
            "density": 2,
        },
        {
            "id": 425,
            "name": "Waterfall Wall Pipebombs 2",
            "type": "sprite",
            "density": 3,
        },
        {"id": 203, "name": "Secret Hidden Reactor Wall", "type": "sector"},
        {"id": 219, "name": "Secret Timed Overlord Wall", "type": "sector"},
        {"id": 225, "name": "Secret Waterfall Wall", "type": "sector"},
        {"id": 246, "name": "Secret Timed Reactor Wall", "type": "sector"},
        {"id": 0, "name": "Exit", "type": "exit"},
    ]
    must_dive = True
    has_boss = True

    def main_region(self) -> Region:
        r = self.rules
        # lucky us, we start underwater so we can swim without dive until we surface!
        ret = self.region(
            self.name,
            [
                "Start Underwater Shotgun",
                "Start Underwater Atomic Health",
                "Secret Hidden Reactor Wall",
                "Hidden Wall Atomic Health",
                "Hidden Wall Armor",
            ],
        )
        self.restrict("Start Underwater Atomic Health", r.can_use)

        start_ledge = self.region(
            "Start Ledge",
            [
                "Combination Lock Scuba Gear",
                "Broken Wall Medkit",
                "Waterfall Tripmine",
                "Waterfall Armor",
                "Waterfall Shrinker",
                "Waterfall Scuba Gear",
                "Waterfall Night Vision Goggles",
                "Waterfall RPG",
                "Waterfall Holo Duke",
                "Waterfall Atomic Health",
            ],
        )
        # Can sometimes step up on to the ledge by strafing into the wall as you emerge from the water
        # Marked as extreme difficulty, as it's a single attempt trick per level start and no setup exists for now
        self.connect(ret, start_ledge, r.jump | r.difficulty("extreme"))
        self.restrict("Waterfall Holo Duke", r.dive(100))

        reactor = self.region(
            "Reactor",
            ["Reactor Freezethrower", "Secret Timed Reactor Wall", "Timed Wall RPG"],
        )
        self.connect(
            start_ledge,
            reactor,
            (r.jump & r.can_use) | (r.jetpack(50) & r.difficulty("medium")),
        )

        waterfall_wall = self.region(
            "Waterfall Wall",
            [
                "Secret Waterfall Wall",
                "Waterfall Wall Pipebombs 1",
                "Waterfall Wall Pipebombs 2",
            ],
        )
        self.connect(start_ledge, waterfall_wall, r.explosives)

        vents = self.region(
            "Ventilation Shafts",
            [
                "Vents Center Atomic Health",
                "Vents Pipebombs 1",
                "Vents Pipebombs 2",
                "Control Room Night Vision Goggles",
                "Control Room Chaingun",
                "Control Room Armor",
            ],
        )
        # It's slow, but going via waterfall room gets you in with no sprint requirements
        self.connect(
            start_ledge, vents, r.jetpack(25) | (r.can_jump & (r.sr50 | r.can_use))
        )

        overlord_chamber = self.region(
            "Overlord Chamber",
            [
                "Overlord Tripmine 1",
                "Overlord Tripmine 2",
                "Overlord Atomic Health",
                "Secret Timed Overlord Wall",
                "Timed Wall Medkit",
                "Timed Wall Atomic Health",
                "Exit",
            ],
        )
        # Why fight when you can just press the exit button, requires jumping to press
        self.restrict("Exit", r.can_kill_boss_2 | (r.glitched & r.can_jump))
        self.connect(vents, overlord_chamber, r.true)

        overlord_tunnel = self.region(
            "Overlord Tunnel",
            [
                "Overlord Tunnel Devastator",
                "Overlord Tunnel Jetpack",
                "Overlord Tunnel Medkit",
            ],
        )
        self.connect(overlord_chamber, overlord_tunnel, r.jump & r.dive(100))
        return ret
