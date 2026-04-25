from BaseClasses import Region

from ..base_classes import D3DLevel


class E1L3(D3DLevel):
    name = "Death Row"
    levelnum = 2
    volumenum = 0
    keys = ["Blue", "Red", "Yellow"]
    location_defs = [
        {
            "name": "Control Room Secret Atomic Health",
            "id": 48,
            "type": "sprite",
            "density": 3,
        },
        {"name": "Control Room Vent Armor", "id": 79, "type": "sprite", "density": 0},
        {"name": "Gallery Medkit", "id": 160, "type": "sprite", "density": 0},
        {
            "name": "Cell Block 01 Broken Wall Atomic Health",
            "id": 185,
            "type": "sprite",
            "density": 1,
        },
        {"name": "Electric Chair Shotgun", "id": 236, "type": "sprite", "density": 2},
        {
            "name": "Control Room Secret Pipebombs",
            "id": 269,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Submarine Gate Scuba Gear",
            "id": 280,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Gear Room Atomic Health", "id": 367, "type": "sprite", "density": 1},
        {"name": "Cell Block 01 RPG", "id": 411, "type": "sprite", "density": 0},
        {"name": "MP Courtyard Medkit", "id": 413, "type": "sprite", "density": 5},
        {"name": "Yellow Key Card", "id": 485, "type": "sprite", "density": 0},
        {
            "name": "Courtyard Tunnel Atomic Health 1",
            "id": 488,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Courtyard Tunnel Atomic Health 2",
            "id": 489,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Courtyard Tunnel Atomic Health 3",
            "id": 490,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Submarine Engine Room Medkit",
            "id": 504,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Underwater Pipebombs", "id": 532, "type": "sprite", "density": 1},
        {"name": "Chapel Chaingun", "id": 564, "type": "sprite", "density": 2},
        {"name": "MP Showers Shotgun", "id": 598, "type": "sprite", "density": 5},
        {"name": "Showers Protective Boots", "id": 606, "type": "sprite", "density": 3},
        {
            "name": "Hanged Monk Atomic Health",
            "id": 642,
            "type": "sprite",
            "sprite_type": "monk",
            "density": 1,
        },
        {"name": "Gallery Holo Duke", "id": 672, "type": "sprite", "density": 1},
        {"name": "Chapel Rafters Armor", "id": 676, "type": "sprite", "density": 2},
        {
            "name": "Chapel Rafters Atomic Health",
            "id": 677,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Gear Room Night Vision Goggles",
            "id": 697,
            "type": "sprite",
            "density": 3,
        },
        {"name": "Blue Key Card", "id": 699, "type": "sprite", "density": 0},
        {
            "name": "Submarine Gate Hidden Night Vision Goggles",
            "id": 803,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Breakable Canyon Wall Steroids",
            "id": 813,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Courtyard Pipebombs", "id": 847, "type": "sprite", "density": 3},
        {"name": "Red Key Card", "id": 851, "type": "sprite", "density": 0},
        {"name": "Gear Room RPG", "id": 856, "type": "sprite", "density": 4},
        {
            "name": "MP Cell Block 01 Broken Wall Holo Duke",
            "id": 870,
            "type": "sprite",
            "density": 5,
        },
        {"name": "Control Room Chaingun", "id": 899, "type": "sprite", "density": 1},
        {"name": "Chapel Window Steroids", "id": 902, "type": "sprite", "density": 0},
        {"name": "MP Cell Block 02 Jetpack", "id": 903, "type": "sprite", "density": 5},
        {"name": "Secret Courtyard Tunnel", "id": 76, "type": "sector"},
        {"name": "Secret Electric Chair", "id": 296, "type": "sector"},
        {"name": "Secret Chapel Rafters", "id": 304, "type": "sector"},
        {"name": "Secret Chapel Window", "id": 317, "type": "sector"},
        {"name": "Secret Behind Bed", "id": 379, "type": "sector"},
        {"name": "Secret Submarine Engine Room", "id": 387, "type": "sector"},
        {"name": "Secret Submarine Gate Hidden Alcove", "id": 393, "type": "sector"},
        {"name": "Secret Breakable Canyon Wall", "id": 401, "type": "sector"},
        {"name": "Secret Control Room Right Alcove", "id": 424, "type": "sector"},
        {"name": "Secret Control Room Left Alcove", "id": 426, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]
    events = ["Unlock Cell Blocks"]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(self.name)

        electric_chair = self.region("Secret Electric Chair")
        self.add_locations(
            ["Secret Electric Chair", "Electric Chair Shotgun"], electric_chair
        )
        # Can walk onto the window, shoot the button, and get into the lowering sector without crouch or opening
        # the door
        self.connect(
            ret,
            electric_chair,
            r.difficulty("medium") | (r.can_crouch & (r.can_open | r.jump)),
        )

        hallway = self.region(
            "Main Hallway",
            [
                "Gallery Holo Duke",
                "Gallery Medkit",
                "Hanged Monk Atomic Health",
                "Chapel Rafters Atomic Health",
                "Chapel Rafters Armor",
                "Secret Chapel Rafters",
                "Secret Behind Bed",
            ],
        )
        # Use trick above to get onto electric chair, raise platform again, then a precise SR50 gets you out
        self.connect(
            ret,
            hallway,
            r.difficulty("hard") | (r.difficulty("medium") & r.sprint) | r.jump,
        )
        # need open to turn bed, doesn't even matter how we get into the cell
        self.restrict("Secret Behind Bed", r.can_crouch & r.can_open)
        self.restrict("Gallery Holo Duke", r.can_open)

        altar = self.region(
            "Chapel Altar",
            ["Chapel Window Steroids"],
        )
        # Can walk onto liztroopers from the pew to get up, might need two to line up without sprint
        self.connect(
            hallway,
            altar,
            r.jump | r.difficulty("extreme") | (r.difficulty("hard") & r.sprint),
        )

        behind_altar = self.region(
            "Behind Chapel Altar", ["Secret Chapel Window", "Chapel Chaingun"]
        )
        # Crouchjump through the left side
        self.connect(altar, behind_altar, r.can_use | r.fast_crouch_jump)

        gears = self.region(
            "Gear Room",
            [
                "Gear Room RPG",
                "Blue Key Card",
                "Gear Room Night Vision Goggles",
                "Gear Room Atomic Health",
            ],
        )
        # you can easily sprint clip (or a cursed SR50 clip without sprint) onto the top gear but that doesn't get us
        # anywhere. The liztrooper clips around wildly, and it seems impossible to manipulate him as a stepping stone
        # reliably in time before he kills you. It is possible to get to both ledges with him though!
        self.connect(hallway, gears, r.jump)
        self.restrict("Blue Key Card", r.can_open)
        self.restrict("Gear Room Night Vision Goggles", r.can_open)

        # This is a bit weird, can not jetpack up, only exit from vent
        control_vent = self.region(
            "Hallway Vent",
            [
                "Control Room Vent Armor",
            ],
        )
        self.connect(hallway, control_vent, r.jetpack(100) & r.difficulty("hard"))

        control_room = self.region(
            "Control Room",
            [
                "Yellow Key Card",
                "MP Showers Shotgun",
                "Showers Protective Boots",
                "Cell Black 01 Broken Wall Atomic Health",
            ],
        )
        self.connect(hallway, control_room, self.blue_key & r.can_open)

        control_room_center = self.region("Control Room Center")
        # can wiggle through window
        self.connect(control_room, control_room_center, r.true)
        # this transition only matters if we come from the vent, so add the jetpack requirements from that on top
        self.connect(
            control_room_center,
            control_room,
            r.can_open | r.glitch_kick | r.jetpack(200),
        )

        control_room_top = self.region(
            "Control Room Top",
            ["Unlock Cell Blocks", "Control Room Chaingun"],
        )
        # Doors automatically open when using key!
        self.connect(control_room_center, control_room_top, self.red_key)
        self.connect(control_room_top, control_vent, r.jump)
        # Can easily clip up corner
        self.restrict("Control Room Chaingun", r.jump | r.difficulty("medium"))
        self.restrict("Unlock Cell Blocks", r.can_open & r.can_use)
        # Okay, I lied earlier. We can get into the vent proper if we are not on a jetpack. This requires
        # abusing a liztrooper to push you, but they are notoriously annoying to get into the vent
        # It is technically possible with just jumping on one, but the most reliable idea is to just float in with
        # a jetpack and hope the trooper follows you
        self.connect(
            control_vent, control_room_top, r.difficulty("extreme") & r.jetpack(180)
        )

        control_room_bridge = self.region("Control Room Outside Bridge")
        # Can jump on a pigcop to get up, either sprint past explosives or blow em up to get inside
        self.connect(
            control_room_center,
            control_room_bridge,
            r.jetpack(50) | (r.difficulty("medium") & r.can_jump),
        )
        self.connect(
            control_room_bridge,
            control_room_top,
            r.can_open & (r.explosives | (r.sprint & r.difficulty("hard"))),
        )
        # Seem to always get squished without steroids
        self.connect(
            control_room_top,
            control_room_bridge,
            (r.can_open & (r.explosives | (r.sprint & r.difficulty("hard"))))
            | r.fast_crouch_jump,
        )

        control_room_ledges = self.region(
            "Control Room Top Ledges",
            [
                "Secret Control Room Left Alcove",
                "Control Room Secret Pipebombs",
                "Secret Control Room Right Alcove",
                "Control Room Secret Atomic Health",
            ],
        )
        self.connect(control_room_bridge, control_room_ledges, r.jump & r.can_use)

        courtyard = self.region("Courtyard")
        self.add_locations(["MP Courtyard Medkit", "Red Key Card"], courtyard)
        # Can also just kick the yellow door to open it
        self.connect(
            control_room_center,
            courtyard,
            (self.yellow_key & r.can_open) | r.glitch_kick,
        )

        courtyard_ledge = self.region(
            "Courtyard Ledge",
            [
                "Secret Courtyard Tunnel",
                "Courtyard Tunnel Atomic Health 1",
                "Courtyard Tunnel Atomic Health 2",
                "Courtyard Tunnel Atomic Health 3",
                "Courtyard Pipebombs",
            ],
        )
        self.connect(courtyard, courtyard_ledge, r.jump)

        courtyard_canyon = self.region(
            "Courtyard Canyon",
            [
                "Secret Breakable Canyon Wall",
                "Breakable Canyon Wall Steroids",
            ],
        )
        self.connect(courtyard, courtyard_canyon, r.jump & r.explosives)

        cell_block_01 = self.region(
            "Cell Block 01",
            [
                "MP Cell Block 01 Broken Wall Holo Duke",
            ],
        )
        self.connect(control_room, cell_block_01, self.event("Unlock Cell Blocks"))
        self.connect(courtyard_canyon, cell_block_01, r.explosives_count(2))

        cell_block_01_room = self.region(
            "Cell Block 01 Far Room", ["Cell BLock 01 RPG"]
        )
        # this is a bit of a mess, and the logic only really ever matters if we break access into the control room
        # without blue key
        self.connect(cell_block_01, cell_block_01_room, r.can_use)
        self.connect(
            courtyard_canyon, cell_block_01_room, r.crouch_jump & r.difficulty("medium")
        )
        self.connect(
            courtyard_ledge,
            cell_block_01_room,
            ((r.crouch_jump & r.jetpack(50)) | r.fast_crouch_jump)
            & r.difficulty("hard"),
        )

        cell_block_02_room = self.region(
            "Cell Block 01 Middle Room", ["MP Cell Block 02 Jetpack"]
        )
        self.connect(
            control_room,
            cell_block_02_room,
            self.event("Unlock Cell Blocks") & r.can_use,
        )
        # don't think you can make this jump even with steroids and sprint
        self.connect(courtyard, cell_block_02_room, r.explosives & r.jetpack(50))
        # pretty sure this is entirely useless, but it's possible
        self.connect(
            cell_block_02_room,
            courtyard,
            r.glitched & r.pipebomb & r.difficulty("hard"),
        )

        dock_tunnel = self.region("Escape Tunnel to Dock")
        self.connect(
            control_room, dock_tunnel, self.event("Unlock Cell Blocks") & r.can_use
        )
        self.connect(
            courtyard_ledge,
            dock_tunnel,
            ((r.crouch_jump & r.jetpack(50)) | r.fast_crouch_jump)
            & r.difficulty("hard"),
        )

        dock = self.region("Submarine Dock", ["Submarine Gate Scuba Gear"])
        # Can shoot pipebombs to get to dock area, no explosive unlocks necessary!
        self.connect(dock_tunnel, dock, r.true)
        self.connect(dock, courtyard, r.can_use)
        # Don't think this does anything yet, but better mark it down if we ever find an early sub clip or something
        self.connect(courtyard, control_room, self.yellow_key | r.glitch_kick)

        dock_secret = self.region(
            "Submarine Dock Door Secret",
            [
                "Secret Submarine Gate Hidden Alcove",
                "Submarine Gate Hidden Night Vision Goggles",
            ],
        )
        # can wiggle on a pigcop or octabrain to get up
        self.connect(dock, dock_secret, r.can_open & (r.jump | r.difficulty("hard")))

        submarine = self.region(
            "Submarine",
            [
                "Underwater Pipebombs",
                "Exit",
            ],
        )
        self.connect(dock, submarine, r.can_dive)
        self.restrict("Exit", r.can_use)

        engine_room = self.region(
            "Submarine Engine",
            ["Secret Submarine Engine Room", "Submarine Engine Room Medkit"],
        )
        self.connect(submarine, engine_room, r.can_open)

        return ret
