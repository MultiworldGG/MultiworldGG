"""
Randomized stage palettes
RGB555 colors.

Each is just a preset that changes the hue, saturation, brightness value, and RGB tint of each palette color.
The RGB tint only changes in proportion to how gray the overall color is, so that already bright objects will take partial colors and all that jazz.

The first four kinda look like crap so consider this to be a WIP
"""

import colorsys

class Preset:
    def __init__(self, hue=0.0, sat=1.0, val=1.0, tint=None, mix=0.0):
        self.hue, self.sat, self.val, self.tint, self.mix = hue, sat, val, tint, mix

    def rgb5(self, r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r / 31, g / 31, b / 31)
        h = (h + self.hue / 360) % 1.0
        v = min(1.0, v * self.val)
        out = list(colorsys.hsv_to_rgb(h, min(1.0, s * self.sat), v))
        if self.tint:
            k = self.mix * (1 - s)
            out = [c * (1 - k) + t / 255 * k for c, t in zip(out, self.tint)]
        return tuple(max(0, min(31, round(c * 31))) for c in out)

PRESETS = {
    "snowy":  Preset(sat=0.85, val=1.10, tint=(0xCF, 0xE4, 0xFF), mix=0.55),
    "desert": Preset(hue=15, sat=1.05, val=1.05, tint=(0xF0, 0xC0, 0x70), mix=0.45),
    "dusk":   Preset(hue=-10, sat=1.15, val=0.85, tint=(0x60, 0x30, 0x90), mix=0.45),
    "neon":   Preset(hue=-35, sat=1.75, val=0.95, tint=(0xFF, 0x2F, 0xD0), mix=0.07),
    "hue60":  Preset(hue=60, sat=1.6, val=0.95),
    "hue120": Preset(hue=120, sat=1.6, val=0.95),
    "hue180": Preset(hue=180, sat=1.6, val=0.95),
    "hue240": Preset(hue=240, sat=1.6, val=0.95),
    "hue300": Preset(hue=300, sat=1.6, val=0.95),
}

# The hue shift looks good on every stage so I keep them all.
HUES = ["hue60", "hue120", "hue180", "hue240", "hue300"]

# Which stages can have which themes. Some stages simply looked better or worse, so they have
# been hand selected to not have specific palettes that looked bad.
STAGE_THEMES = {
    1:  ["desert", "dusk"],             # Derelict Spacecraft
    2:  ["snowy", "desert", "dusk"],    # Aegis Volcano Base
    3:  ["desert", "dusk"],             # Oceanic Highway Ruins
    4:  ["dusk"],                       # Weapons Repair Factory
    5:  ["snowy", "desert", "dusk"],    # Old Residential
    6:  ["snowy", "desert", "dusk"],    # Missile Factory
    7:  [],                             # Twilight Desert
    8:  [],                             # Forest of Anatre
    9:  ["desert", "dusk"],             # Frontline Ice Base
    10: ["desert", "dusk"],             # Area X-2
    11: ["snowy", "desert", "dusk"],    # Energy Facility
    12: ["desert", "dusk"],             # Snowy Plains
    13: ["desert", "dusk"],             # Sunken Library
    14: ["dusk"],                       # Giant Elevator
    15: ["snowy", "desert", "dusk"],    # Sub Arcadia
    16: ["snowy", "desert", "dusk"],    # Abandoned Research Laboratory
    17: [],                             # Resistance Base
}


def recolor(palette: bytes, preset: Preset) -> bytes:
    out = bytearray(len(palette))
    for i in range(0, len(palette), 2):
        v = palette[i] | (palette[i + 1] << 8)
        r, g, b = preset.rgb5(v & 31, (v >> 5) & 31, (v >> 10) & 31)
        w = r | (g << 5) | (b << 10)
        out[i], out[i + 1] = w & 0xFF, w >> 8
    return bytes(out)
