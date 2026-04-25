from BaseClasses import Region

from ..base_classes import D3DLevel


class E1L5(D3DLevel):
    name = "The Abyss"
    levelnum = 4
    volumenum = 0
    keys = ["Blue"]
    location_defs = [
        {"name": "Battlelord Medkit", "id": 4, "type": "sprite", "density": 0},
        {
            "name": "Battlelord Atomic Health 1",
            "id": 11,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Battlelord Atomic Health 2",
            "id": 12,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Waterfall Chaingun", "id": 24, "type": "sprite", "density": 0},
        {"name": "MP Start Chaingun", "id": 78, "type": "sprite", "density": 5},
        {"name": "Battlelord Jetpack", "id": 79, "type": "sprite", "density": 3},
        {"name": "Battlelord Armor", "id": 80, "type": "sprite", "density": 4},
        {
            "name": "Cracked Wall End Atomic Health",
            "id": 112,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Fire Pit Pipe Bombs", "id": 131, "type": "sprite", "density": 3},
        {
            "name": "Top of Spaceship Atomic Health",
            "id": 216,
            "type": "sprite",
            "density": 2,
        },
        {"name": "Spaceship Shaft RPG", "id": 221, "type": "sprite", "density": 1},
        {"name": "Spaceship Shaft Chaingun", "id": 222, "type": "sprite", "density": 3},
        {
            "name": "Fire Pit Night Vision Goggles",
            "id": 262,
            "type": "sprite",
            "density": 1,
        },
        {"name": "Canyon Chaingun", "id": 291, "type": "sprite", "density": 3},
        {"name": "MP Secret Fire Pit Armor", "id": 294, "type": "sprite", "density": 5},
        {"name": "Pipebombs near Blue Gate", "id": 311, "type": "sprite", "density": 1},
        {"name": "Start Shotgun", "id": 316, "type": "sprite", "density": 1},
        {
            "name": "Earthquake Atomic Health 1",
            "id": 373,
            "type": "sprite",
            "density": 1,
        },
        {
            "name": "Earthquake Atomic Health 2",
            "id": 374,
            "type": "sprite",
            "density": 3,
        },
        {"name": "Blue Key Card", "id": 375, "type": "sprite", "density": 0},
        {
            "name": "Cracked Wall Middle Atomic Health",
            "id": 410,
            "type": "sprite",
            "density": 0,
        },
        {"name": "Fire Pit RPG", "id": 439, "type": "sprite", "density": 0},
        {
            "name": "Dancing Shaman Atomic Health 1",
            "id": 466,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Dancing Shaman Atomic Health 2",
            "id": 472,
            "type": "sprite",
            "density": 4,
        },
        {
            "name": "Dancing Shaman Atomic Health 3",
            "id": 473,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Red Waterfall Pipe Bombs", "id": 524, "type": "sprite", "density": 0},
        {"name": "Start Protective Boots", "id": 604, "type": "sprite", "density": 0},
        {
            "name": "Bottom of Ruins Protective Boots",
            "id": 682,
            "type": "sprite",
            "density": 1,
        },
        {"name": "Fire Place Medkit", "id": 689, "type": "sprite", "density": 0},
        {
            "name": "Toxic River Protective Boots",
            "id": 698,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Start RPG", "id": 718, "type": "sprite", "density": 3},
        {
            "name": "Secret Fire Pit Night Vision Goggles",
            "id": 726,
            "type": "sprite",
            "density": 3,
        },
        {"name": "Secret Fire Pit Medkit", "id": 727, "type": "sprite", "density": 0},
        {"name": "Toxic River Holo Duke", "id": 733, "type": "sprite", "density": 4},
        {"name": "Toxic River Medkit", "id": 734, "type": "sprite", "density": 1},
        {"name": "Ruins Staircase Shotgun", "id": 737, "type": "sprite", "density": 1},
        {"name": "Fire Pit Steroids", "id": 738, "type": "sprite", "density": 2},
        {
            "name": "Cracked Wall Bottom Atomic Health",
            "id": 740,
            "type": "sprite",
            "density": 3,
        },
        {
            "name": "Cracked Wall Protective Boots",
            "id": 741,
            "type": "sprite",
            "density": 3,
        },
        {"name": "Cracked Wall Medkit", "id": 742, "type": "sprite", "density": 1},
        {"name": "Spaceship Entrance Armor", "id": 744, "type": "sprite", "density": 3},
        {
            "name": "Earthquake Night Vision Goggles",
            "id": 817,
            "type": "sprite",
            "density": 3,
        },
        {
            "name": "Red Waterfall Cave Protective Boots",
            "id": 868,
            "type": "sprite",
            "density": 3,
        },
        {
            "name": "MP Shrinker Room Steroids",
            "id": 876,
            "type": "sprite",
            "density": 5,
        },
        {
            "name": "MP Cracked Wall Bottom Pipebombs",
            "id": 879,
            "type": "sprite",
            "density": 5,
        },
        {"name": "Canyon Pillars RPG", "id": 884, "type": "sprite", "density": 0},
        {"name": "MP Fire Pit Jetpack", "id": 1032, "type": "sprite", "density": 5},
        {"name": "MP Fire Place RPG", "id": 1039, "type": "sprite", "density": 5},
        {
            "name": "MP Ruins Staircase Atomic Health",
            "id": 1041,
            "type": "sprite",
            "density": 5,
        },
        {
            "name": "MP Ruins Staircase Armor",
            "id": 1042,
            "type": "sprite",
            "density": 5,
        },
        {
            "name": "MP Bottom of Ruins Shotgun",
            "id": 1044,
            "type": "sprite",
            "density": 5,
        },
        {"name": "Fire Pit Atomic Health", "id": 1046, "type": "sprite", "density": 3},
        {
            "name": "Secret Fire Pit Atomic Health 1",
            "id": 1047,
            "type": "sprite",
            "density": 2,
        },
        {
            "name": "Secret Fire Pit Atomic Health 2",
            "id": 1048,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Secret Red Waterfall Passage", "id": 7, "type": "sector"},
        {"name": "Secret Dancing Shaman", "id": 21, "type": "sector"},
        {"name": "Secret Top of Spaceship", "id": 257, "type": "sector"},
        {"name": "Secret Fire Pit Hidden Wall", "id": 354, "type": "sector"},
        {"name": "Secret Fire Pit Teleporter", "id": 440, "type": "sector"},
        {"name": "Secret Fire Pit Ledge", "id": 441, "type": "sector"},
        {"name": "Exit", "id": 0, "type": "exit"},
    ]
    events = ["Earthquake", "Canyon Explosion"]
    has_boss = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(
            self.name,
            [
                "Start RPG",
                "Start Shotgun",
                "Start Protective Boots",
                "MP Start Chaingun",
                "Blue Key Card",
                "Canyon Chaingun",
                "Toxic River Medkit",
                "Toxic River Holo Duke",
                "Toxic River Protective Boots",
                "Earthquake Night Vision Goggles",
            ],
        )
        # Can pick it up pushing into the pillar from the back left at just the right angle
        self.restrict("Blue Key Card", r.jump | r.difficulty("medium"))
        self.restrict("Earthquake Night Vision Goggles", r.jump)
        # Tripclip
        self.restrict(
            "Start Protective Boots",
            r.can_open
            | (
                r.glitched
                & r.tripmine
                & r.fast_sprint
                & r.can_jump
                & r.difficulty("extreme")
            ),
        )

        blue_gate = self.region("Beyond Blue Key Gate", ["Pipebombs near Blue Gate"])
        # Gate opens automatically, no Open required
        # Crouch jump has a reliable setup, very hard to time without one
        # Easier path is just to trooper hop around the outside on hard difficulty
        # which removes any need for glitched
        self.connect(
            ret,
            blue_gate,
            self.blue_key | (r.difficulty("hard") & r.can_jump) | r.jetpack(50),
        )

        fault_trigger = self.region(
            "Earthquake Trigger",
            [
                "Earthquake",
                "Secret Fire Pit Night Vision Goggles",
                "Secret Fire Pit Medkit",
            ],
        )
        self.connect(
            blue_gate, fault_trigger, r.jump
        )  # jetpack also gets here without blue key by above logic

        beyond_fault = self.region(
            "After Earthquake",
            [
                "Earthquake Atomic Health 1",
                "Earthquake Atomic Health 2",
                "Ruins Staircase Shotgun",
                "MP Fire Place RPG",
                # TODO: Test if these belongs to beyond_fault or small_ledges
                # "MP Ruins Staircase Atomic Health",
                # "MP Ruins Staircase Armor",
                "Fire Pit Pipe Bombs",
                "Fire Pit Atomic Health",
                "Secret Fire Pit Teleporter",
                "Bottom of Ruins Protective Boots",
                "MP Bottom of Ruins Shotgun",
                "Fire Pit RPG",
                "Waterfall Chaingun",
            ],
        )
        self.connect(fault_trigger, beyond_fault, self.event("Earthquake"))
        # can clip through, skipping the hand trigger
        self.restrict("Fire Pit RPG", (r.jump & r.can_use) | r.crouch_jump)
        # Can sr50 or sprint onto the waterfall alcove
        self.restrict("Waterfall Chaingun", r.jump | r.sr50)

        fault_doors = self.region(
            "Doors after Earthquake",
            ["Fire Pit Steroids", "Secret Fire Pit Hidden Wall"],
        )
        self.connect(beyond_fault, fault_doors, r.can_open)

        fault_buttons = self.region("Buttons after Earthquake", ["Fire Place Medkit"])
        self.connect(beyond_fault, fault_buttons, r.can_use)

        secret_fire_pit_ledge = self.region(
            "Secret Fire Pit Ledge",
            [
                "Secret Fire Pit Atomic Health 1",
                "Secret Fire Pit Atomic Health 2",
                "MP Secret Fire Pit Armor",
            ],
        )
        # you can clip up here somehow, I just don't know how to reproduce it
        self.connect(
            beyond_fault, secret_fire_pit_ledge, r.jump | r.difficulty("extreme")
        )

        small_ledges = self.region(
            "Ledges after Earthquake",
            [
                "MP Ruins Staircase Atomic Health",
                "MP Ruins Staircase Armor",
                "Secret Fire Pit Ledge",
            ],
        )
        # always have like 20 jetpack left from earthquake at this point, should all be fine
        self.connect(beyond_fault, small_ledges, r.jump)

        fire_pit_ledge = self.region(
            "Fire Pit Ledge", ["Fire Pit Night Vision Goggles", "MP Fire Pit Jetpack"]
        )
        # Can SR50 over with sprint speed
        self.connect(
            beyond_fault,
            fire_pit_ledge,
            r.jump | r.fast_sprint | (r.difficulty("hard") & r.sprint),
        )

        shrinker_ledge = self.region(
            "Shrinker Room Ledge", ["MP Shrinker Room Steroids", "Canyon Explosion"]
        )
        self.connect(
            beyond_fault, shrinker_ledge, r.can_use | (r.crouch_jump & r.jetpack(50))
        )
        # Would get stuck in the room afterward otherwise if we can't leave
        self.restrict(
            "Canyon Explosion", (r.can_shrink & r.jump & r.can_use) | r.crouch_jump
        )

        # anything beyond here on pure jetpack uses 50 fuel to get to the red canyon area and make progress
        # it might be possible in just 50 to get here, but that seems a harsh requirement
        red_waterfall = self.region(
            "Red Waterfall",
            [
                "Red Waterfall Cave Protective Boots",
                "Red Waterfall Pipe Bombs",
                "Secret Red Waterfall Passage",
            ],
        )
        # some more leniency on easy logic
        self.connect(
            beyond_fault,
            red_waterfall,
            r.can_jump | r.jetpack(150) | (r.jetpack(100) & r.difficulty("medium")),
        )
        self.restrict("Secret Red Waterfall Passage", r.explosives)

        shaman_secret = self.region(
            "Shaman Secret",
            [
                "Dancing Shaman Atomic Health 1",
                "Dancing Shaman Atomic Health 2",
                "Dancing Shaman Atomic Health 3",
                "Secret Dancing Shaman",
            ],
        )
        # Can clip through the right side lava waterfall
        self.connect(red_waterfall, shaman_secret, r.can_use | r.crouch_jump)

        ship_entrance = self.region(
            "Ship Entrance",
            [
                "MP Cracked Wall Bottom Pipebombs",
                "Cracked Wall Bottom Atomic Health",
                "Cracked Wall Middle Atomic Health",
                "Cracked Wall Protective Boots",
                "Cracked Wall Medkit",
                "Cracked Wall End Atomic Health",
                "Canyon Pillars RPG",
                "Spaceship Entrance Armor",
            ],
        )
        # some leniency on easy
        self.connect(
            beyond_fault,
            ship_entrance,
            self.event("Canyon Explosion")
            & (r.can_jump | r.jetpack(150) | (r.jetpack(100) & r.difficulty("medium"))),
        )

        top_of_spaceship = self.region(
            "Top of Spaceship",
            ["Secret Top of Spaceship", "Top of Spaceship Atomic Health"],
        )
        self.connect(
            ship_entrance,
            top_of_spaceship,
            r.can_open
            | r.jetpack(250)
            | (r.jetpack(200) & r.difficulty("medium"))
            | r.fast_crouch_jump,
        )

        spaceship = self.region(
            "Spaceship",
            [
                "Spaceship Shaft RPG",
                "Spaceship Shaft Chaingun",
                "Battlelord Medkit",
                "Battlelord Atomic Health 1",
                "Battlelord Atomic Health 2",
                "Battlelord Jetpack",
                "Battlelord Armor",
                "Exit",
            ],
        )
        # Big drop, can't get back
        self.connect(ship_entrance, spaceship, r.can_open)
        # Clip to DM exit near boss drop
        self.restrict(
            "Exit",
            r.can_kill_boss_1
            | (r.glitched & r.difficulty("hard") & r.fast_sprint & r.can_jump),
        )
        self.restrict("Spaceship Shaft RPG", r.jump)
        self.restrict("Spaceship Shaft Chaingun", r.jump)

        return ret
