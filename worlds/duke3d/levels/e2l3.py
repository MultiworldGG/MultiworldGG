from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L3(D3DLevel):
    name = "Warp Factor"
    levelnum = 2
    volumenum = 1
    keys = ["Blue", "Yellow"]
    location_defs = [
        {"name": "Engine Room Atomic Health", "id": 9, "type": "sprite", "density": 4},
        {"name": "Engine Room Shotgun", "id": 10, "type": "sprite", "density": 4},
        {"name": "MP Drone Room Holo Duke", "id": 13, "type": "sprite", "density": 5},
        {"name": "Blue Key Card", "id": 14, "type": "sprite", "density": 0},
        {"name": "Main Room Shrinker", "id": 47, "type": "sprite", "density": 0},
        {"name": "Engine Room Armor", "id": 61, "type": "sprite", "density": 0},
        {"name": "MP Control Room Jetpack", "id": 91, "type": "sprite", "density": 5},
        {"name": "Ready Room Medkit", "id": 96, "type": "sprite", "density": 3},
        {"name": "Control Room Devastator", "id": 135, "type": "sprite", "density": 0},
        {"name": "Engine Room Tripmine", "id": 162, "type": "sprite", "density": 3},
        {"name": "Start Chaingun", "id": 177, "type": "sprite", "density": 0},
        {"name": "Wall Panel Freezethrower", "id": 182, "type": "sprite", "density": 0},
        {"name": "Wall Panel Pipebombs", "id": 226, "type": "sprite", "density": 0},
        {"name": "Reactor Atomic Health 1", "id": 274, "type": "sprite", "density": 0},
        {"name": "Reactor Atomic Health 2", "id": 275, "type": "sprite", "density": 3},
        {"name": "Control Room Medkit", "id": 284, "type": "sprite", "density": 0},
        {"name": "Yellow Key Card", "id": 316, "type": "sprite", "density": 0},
        {"name": "Control Room Holo Duke", "id": 496, "type": "sprite", "density": 0},
        {
            "name": "Conveyor Night Vision Goggles",
            "id": 694,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Control Room Steroids", "id": 695, "type": "sprite", "density": 0},
        {
            "name": "Engine Room Burrowed Atomic Health 1",
            "id": 699,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Drone Room Medkit", "id": 725, "type": "sprite", "density": 0},
        {
            "name": "Engine Room Burrowed Atomic Health 2",
            "id": 766,
            "type": "sprite",
            "density": 3,
        },
        {
            "name": "Engine Room Burrowed Atomic Health 3",
            "id": 767,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Main Room Shotgun", "id": 768, "type": "sprite", "density": 0},
        {"name": "Control Room RPG", "id": 772, "type": "sprite", "density": 4},
        {"name": "Left Wing RPG", "id": 782, "type": "sprite", "density": 0},
        {"name": "MP Control Room Armor", "id": 799, "type": "sprite", "density": 5},
        {"name": "MP Main Room Chaingun", "id": 801, "type": "sprite", "density": 5},
        {
            "name": "Really Ready Room Devastator",
            "id": 817,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Really Ready Room Freezethrower",
            "id": 818,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Bridge Chaingun", "id": 819, "type": "sprite", "density": 3},
        {"name": "Bridge Pipebombs", "id": 820, "type": "sprite", "density": 4},
        {"name": "Bridge RPG", "id": 821, "type": "sprite", "density": 4},
        {"name": "Bridge Atomic Health", "id": 822, "type": "sprite", "density": 2},
        {"name": "Secret Enterprise Bridge", "id": 42, "type": "sector"},
        {"name": "Secret Really Ready Room", "id": 297, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]
    events = ["Disable Forcefield"]

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Start Chaingun",
            ],
        )

        past_door = self.region(
            "Past Door",
            [
                "Wall Panel Freezethrower",
                "Wall Panel Pipebombs",
                "Drone Room Medkit",
                "MP Drone Room Holo Duke",
                "Engine Room Atomic Health",
                "Engine Room Shotgun",
                "Engine Room Tripmine",
                "Blue Key Card",
                "Engine Room Armor",
                "Main Room Shrinker",
                "MP Main Room Chaingun",
                "Main Room Shotgun",
            ],
        )
        self.connect(
            ret,
            past_door,
            r.can_open
            # Door seems to be too thick to tripclip past without getting squished :(
            # | (r.glitched & r.tripmine & r.fast_sprint & r.can_jump & r.difficulty("extreme")),
        )

        self.restrict("Blue Key Card", r.can_crouch)
        # Can walk on top of a flying trooper. Not fun, but possible
        self.restrict("Engine Room Armor", r.jump)

        wings = self.region(
            "Outer Wings",
            [
                "Yellow Key Card",  # Auto closing wings clip you up trivially
                "Engine Room Burrowed Atomic Health 1",
                "Engine Room Burrowed Atomic Health 2",
                "Engine Room Burrowed Atomic Health 3",
                "Left Wing RPG",
            ],
        )
        self.connect(past_door, wings, self.blue_key)

        # At this point both can_use and can_open are already required
        control_room = self.region(
            "Control Room",
            [
                "Conveyor Night Vision Goggles",
                "Control Room Devastator",
                "Disable Forcefield",
                "MP Control Room Armor",
                "MP Control Room Jetpack",
                "Control Room Holo Duke",
                "Control Room RPG",
                "Control Room Medkit",
                "Control Room Steroids",
                "Bridge Chaingun",
                "Secret Enterprise Bridge",
                "Bridge RPG",
                "Bridge Pipebombs",
                "Bridge Atomic Health",
                "Ready Room Medkit",
                "Secret Really Ready Room",  # can_use
                "Really Ready Room Devastator",  # can_use
                "Really Ready Room Freezethrower",  # can_use
            ],
        )
        self.restrict("Control Room Steroids", r.jump)
        self.connect(past_door, control_room, self.yellow_key)

        reactor = self.region("Reactor", ["Exit"])
        self.connect(
            past_door,
            reactor,
            self.event("Disable Forcefield")
            | (r.difficulty("hard") & (r.can_crouch & r.sprint)),
        )
        self.restrict("Exit", r.can_use)

        reactor_top = self.region(
            "Reactor Top", ["Reactor Atomic Health 1", "Reactor Atomic Health 2"]
        )
        self.connect(
            reactor,
            reactor_top,
            r.jetpack(50) | (r.sr50 & r.glitched),
        )
        return ret
