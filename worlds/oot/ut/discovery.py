import json

from ..Utils import data_path
from .entrances import ENTRANCE_IDS, FOUND_ENTRANCES_KEY


class EntranceDiscovery:
    def __init__(self):
        with open(data_path("generated/symbols.json")) as stream:
            symbol = json.load(stream)["AP_UT_FOUND_ENTRANCES"]
        self.address = int(symbol["address"], 16) - 0x03480000 + 0x00400000
        self.names = []
        self.found = set()
        self.rom_name = None

    def configure(self, rom_name, names):
        if rom_name != self.rom_name or names != self.names:
            self.rom_name = rom_name
            self.names = names
            self.found.clear()

    def poll(self, emu):
        if not self.names:
            return
        bits = [emu.read_u8(self.address + offset) for offset in range((len(ENTRANCE_IDS) + 7) // 8)]
        self.found.update(name for name in self.names
                          if bits[ENTRANCE_IDS[name] // 8] & (1 << (ENTRANCE_IDS[name] % 8)))


async def publish_discoveries(ctx, names):
    """Merge discoveries, so reconnects and multiple clients cannot erase them."""
    if ctx.slot is None or ctx.server is None:
        return
    names = set(names) & set(ctx.entrance_names)
    new_names = names - ctx.reported_entrances
    if not new_names:
        return
    await ctx.send_msgs([{
        "cmd": "Set", "key": FOUND_ENTRANCES_KEY.format(team=ctx.team, player=ctx.slot),
        "default": {}, "want_reply": False,
        "operations": [{"operation": "update", "value": {name: True for name in new_names}}],
    }])
    ctx.reported_entrances.update(new_names)
