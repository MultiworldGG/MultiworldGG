from BaseClasses import Region

from ..base_classes import D3DLevel


class E2L2(D3DLevel):
    name = "Incubator"
    levelnum = 1
    volumenum = 1
    keys = ["Yellow"]
    location_defs = [
        {"name": "MP Underwater Jetpack", "id": 34, "type": "sprite", "density": 5},
        {"name": "Overgrown Passage Jetpack", "id": 67, "type": "sprite", "density": 4},
        {"name": "Wall Panel Freezethrower", "id": 69, "type": "sprite", "density": 3},
        {"name": "Underwater Devastator", "id": 82, "type": "sprite", "density": 0},
        {
            "name": "Drone Alcove Atomic Health",
            "id": 99,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Hidden Screen Room Armor", "id": 103, "type": "sprite", "density": 2},
        {
            "name": "MP Control Room Freezethrower",
            "id": 130,
            "type": "sprite",
            "density": 5,
        },
        {"name": "EDF Logo Medkit", "id": 132, "type": "sprite", "density": 2},
        {"name": "Pool Steroids", "id": 133, "type": "sprite", "density": 0},
        {"name": "Pool Medkit", "id": 134, "type": "sprite", "density": 4},
        {
            "name": "Hidden Screen Room Pipebombs",
            "id": 171,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Armory RPG", "id": 179, "type": "sprite", "density": 0},
        {"name": "Pipebombs behind Turret", "id": 225, "type": "sprite", "density": 0},
        {
            "name": "Beta Scuba Gear",
            "id": 264,
            "type": "sprite",
        },  # Unused beta room of the map
        {
            "name": "Force Field Control Atomic Health 1",
            "id": 266,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Force Field Control Atomic Health 2",
            "id": 267,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Force Field Control Chaingun",
            "id": 268,
            "type": "sprite",
            "density": 0,
        },
        {
            "name": "Beta Medkit",
            "id": 285,
            "type": "sprite",
        },  # Unused beta room of the map
        {
            "name": "Beta Steroids",
            "id": 325,
            "type": "sprite",
        },  # Unused beta room of the map
        {"name": "Armory Tripmine 1", "id": 390, "type": "sprite", "density": 4},
        {"name": "Armory Tripmine 2", "id": 391, "type": "sprite", "density": 3},
        {"name": "Armory Tripmine 3", "id": 392, "type": "sprite", "density": 0},
        {"name": "Wall Panel Holo Duke", "id": 410, "type": "sprite", "density": 2},
        {
            "name": "Cupboard Night Vision Goggles",
            "id": 432,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Yellow Key Card", "id": 524, "type": "sprite", "density": 0},
        {"name": "Start Shotgun", "id": 525, "type": "sprite", "density": 0},
        {"name": "Control Room Pipebombs", "id": 549, "type": "sprite", "density": 0},
        {
            "name": "Overgrown Passage Shrinker",
            "id": 579,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Secret EDF Logo", "id": 142, "type": "sector"},
        {"name": "Secret Force Field Control Wall", "id": 153, "type": "sector"},
        {"name": "Secret Hidden Screen Room 1", "id": 155, "type": "sector"},
        {"name": "Secret Hidden Screen Room 2", "id": 156, "type": "sector"},
        {"name": "Secret Wall Panel", "id": 248, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]
    events = ["Lower Walls"]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [],
        )

        past_entrance = self.region(
            "Past entrance",
            [
                "Start Shotgun",
            ],
        )
        self.connect(ret, past_entrance, r.can_open)

        past_button = self.region(
            "Past button",
            [
                "Secret EDF Logo",
                "EDF Logo Medkit",  # Can just grab this through the wall!
                "Armory Tripmine 1",
                "Armory Tripmine 2",
                "Armory Tripmine 3",
                "Secret Wall Panel",
                "Wall Panel Freezethrower",
                "Wall Panel Holo Duke",
                "Force Field Control Atomic Health 1",
                "Force Field Control Atomic Health 2",
                "Force Field Control Chaingun",
                "Secret Force Field Control Wall",
                "Armory RPG",
                "Yellow Key Card",
            ],
        )
        self.connect(past_entrance, past_button, r.can_use)
        self.restrict("Secret EDF Logo", r.jump)

        hidden_screen_room = self.region(
            "Hidden Screen Room",
            [
                "Secret Hidden Screen Room 1",
                "Secret Hidden Screen Room 2",
                "Hidden Screen Room Pipebombs",  # Can crouch-jump to this item but start requires can_open
                "Hidden Screen Room Armor",
            ],
        )
        # Able to clip up the corner with mouse movement and diagonal strafing
        self.connect(
            past_entrance,
            hidden_screen_room,
            r.can_open
            & (
                r.jump | (r.difficulty("hard") & r.can_sprint) | r.difficulty("extreme")
            ),
        )

        drone_alcove = self.region(
            "Drone Alcove",
            [
                "Drone Alcove Atomic Health",
            ],
        )
        self.connect(past_entrance, drone_alcove, r.crouch_jump | (r.can_use & r.jump))

        early_ledges = self.region(
            "Wall Compartments",
            [
                "Cupboard Night Vision Goggles",  # can_open inherited from start
            ],
        )
        self.connect(past_entrance, early_ledges, r.jump)
        # Logic past this point unchanged since open and use is already required

        # Can clip up to the exit switch fairly easily
        waterfall = self.region(
            "Waterfall",
            ["Pool Medkit", "Pool Steroids", "Exit", "Pipebombs behind Turret"],
        )
        self.restrict(
            "Exit", r.can_use & r.can_open
        )  # Possible to tripmine clip through door after button use

        self.connect(
            past_button,
            waterfall,
            self.event("Lower Walls")
            | (
                # TODO_LOGIC: find a way to somewhat reliably clip with jetpack and no sprint
                # without sprint the clip is very inconsistent
                # & ((r.difficulty("medium") & r.jetpack(100)) | r.jetpack(200))
                # current strats are: corner-crouch and jump-clip through the door
                r.glitched
                & (
                    (r.difficulty("hard") & (r.can_sprint | r.steroids))
                    | (r.difficulty("extreme") & r.can_jump)
                )
            ),
        )
        # Cursed cumulative jetpack logic
        # Can crouchjump in here but can_open is required to get here
        self.restrict(
            "Pipebombs behind Turret",
            self.event("Lower Walls") & r.jetpack(50)
            | (
                r.glitched
                & ((r.difficulty("medium") & r.jetpack(150)) | r.jetpack(250))
            ),
        )

        control_room = self.region(
            "Control Room",
            ["Control Room Pipebombs", "MP Control Room Freezethrower", "Lower Walls"],
        )
        # Only a few tripclip resistant doors left
        self.connect(
            past_button,
            control_room,
            self.yellow_key
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        back_cave = self.region(
            "Overgrown Passage",
            ["Overgrown Passage Shrinker", "Overgrown Passage Jetpack"],
        )
        # Can probably clip walk up the right wall, but I can't find the setup
        # Very cursed jetpack calcs
        self.connect(
            waterfall,
            back_cave,
            r.can_jump
            | self.event("Lower Walls") & r.jetpack(50)
            | (
                r.glitched
                & ((r.difficulty("medium") & r.jetpack(150)) | r.jetpack(250))
            ),
        )

        incubator_pool = self.region(
            "Incubator Pool", ["MP Underwater Jetpack", "Underwater Devastator"]
        )
        self.connect(waterfall, incubator_pool, r.can_dive)
        return ret
