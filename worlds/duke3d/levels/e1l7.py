from BaseClasses import Region

from ..base_classes import D3DLevel


# This is a bit of a meme level with no exit, deathmatch only
# But it theoretically can be reached via glitches in the vanilla game, so might as well map it out
class E1L7(D3DLevel):
    name = "Faces of Death"
    levelnum = 6
    volumenum = 0
    keys = ["Blue"]
    location_defs = [
        # Don't think there's a way to get in here in single player for these two items
        {"name": "MP Side Room Devastator", "id": 0, "type": "sprite", "density": 5},
        {"name": "MP Side Room RPG", "id": 1, "type": "sprite", "density": 5},
        {"name": "Waterfall 2 Atomic Health", "id": 21, "type": "sprite", "density": 2},
        {"name": "Waterfall 2 Armor", "id": 22, "type": "sprite", "density": 4},
        {"name": "Waterfall 1 Armor", "id": 23, "type": "sprite", "density": 4},
        {"name": "Waterfall 1 Atomic Health", "id": 24, "type": "sprite", "density": 2},
        {
            "name": "Center Room Atomic Health 1",
            "id": 97,
            "type": "sprite",
            "density": 3,
        },
        {
            "name": "Center Room Atomic Health 2",
            "id": 98,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Center Room Armor", "id": 107, "type": "sprite", "density": 0},
        {"name": "Center Room Holo Duke", "id": 108, "type": "sprite", "density": 4},
        {"name": "Center Atomic Health", "id": 109, "type": "sprite", "density": 1},
        {"name": "Center Armor", "id": 110, "type": "sprite", "density": 3},
        {"name": "Center Protective Boots", "id": 111, "type": "sprite", "density": 4},
        {
            "name": "Center Night Vision Goggles",
            "id": 112,
            "type": "sprite",
            "density": 4,
        },
        {"name": "Center Steroids", "id": 113, "type": "sprite", "density": 4},
        {"name": "Center Room Tripmine 1", "id": 121, "type": "sprite", "density": 1},
        {"name": "Center Room Tripmine 2", "id": 122, "type": "sprite", "density": 4},
        {"name": "Side Room Pipebombs", "id": 127, "type": "sprite", "density": 0},
        {"name": "Water Tank Shotgun", "id": 179, "type": "sprite", "density": 0},
        {"name": "Water Tank Devastator", "id": 231, "type": "sprite", "density": 0},
        {"name": "Water Tank Freezethrower", "id": 232, "type": "sprite", "density": 4},
        {"name": "Water Tank Chaingun", "id": 233, "type": "sprite", "density": 1},
        {"name": "Water Tank RPG", "id": 234, "type": "sprite", "density": 4},
        {"name": "Water Tank Jetpack", "id": 235, "type": "sprite", "density": 3},
        {"name": "Water Tank Tripmine 1", "id": 236, "type": "sprite", "density": 1},
        {"name": "Water Tank Tripmine 2", "id": 237, "type": "sprite", "density": 4},
        {"name": "Water Tank Shrinker", "id": 238, "type": "sprite", "density": 3},
        {"name": "Main Room Pipebombs", "id": 248, "type": "sprite", "density": 0},
        {"name": "Blue Key Card", "id": 302, "type": "sprite", "density": 0},
        {"name": "Secret Behind Waterfall 1", "id": 110, "type": "sector"},
        {"name": "Secret Behind Waterfall 2", "id": 111, "type": "sector"},
    ]
    must_dive = True

    def main_region(self) -> Region:
        r = self.rules
        ret = self.region(self.name)

        main_area = self.region(
            "Main Area", ["Side Room Pipebombs", "Main Room Pipebombs"]
        )
        # The Battlelords here can be super painful, require some weapons on easier difficulties
        self.connect(ret, main_area, r.difficulty("hard") | (r.rpg & r.devastator))

        water_tanks = self.region(
            "Water Tanks",
            [
                "Water Tank Chaingun",
                "Water Tank Shotgun",
                "Water Tank Jetpack",
                "Water Tank Tripmine 1",
                "Water Tank Tripmine 2",
                "Water Tank Shrinker",
                "Water Tank Freezethrower",
                "Water Tank Devastator",
                "Water Tank RPG",
            ],
        )
        self.connect(ret, water_tanks, r.can_dive)

        waterfall = self.region(
            "Waterfall Secrets",
            [
                "Secret Behind Waterfall 1",
                "Secret Behind Waterfall 2",
                "Waterfall 1 Armor",
                "Waterfall 2 Armor",
                "Waterfall 1 Atomic Health",
                "Waterfall 2 Atomic Health",
            ],
        )
        # Need to jump on a battlelord to get in
        self.connect(
            ret, waterfall, r.jetpack(50) | (r.difficulty("hard") & r.can_jump)
        )

        central_platform = self.region(
            "Central Platform",
            [
                "Center Steroids",
                "Center Atomic Health",
                "Blue Key Card",
                "Center Protective Boots",
                "Center Night Vision Goggles",
                "Center Armor",
            ],
        )
        self.connect(ret, central_platform, r.jump)

        center_room = self.region(
            "Center Room",
            [
                "Center Room Armor",
                "Center Room Tripmine 1",
                "Center Room Tripmine 2",
                "Center Room Holo Duke",
                "Center Room Atomic Health 1",
                "Center Room Atomic Health 2",
            ],
        )
        self.connect(ret, center_room, self.blue_key)
        return ret
