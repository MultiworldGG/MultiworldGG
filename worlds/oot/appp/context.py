from random import Random
from types import SimpleNamespace

from ..Location import DisableType
from ..Messages import update_message_by_id


def item_record(data):
    if data is None:
        return None
    data = dict(data)
    data["looks_like_item"] = item_record(data.get("looks_like_item"))
    return SimpleNamespace(**data)


class PatchContext(SimpleNamespace):
    """Seed data loaded from an .apoot file for patch_rom."""

    def __init__(self, data):
        super().__init__(**data["settings"])
        self.__dict__.update((key, value) for key, value in data.items() if key != "settings")
        self.player_names = {int(player): name for player, name in data["player_names"].items()}
        self.random = Random(data["text_rng_seed"])
        self.scrub_prices = {int(key): value for key, value in self.scrub_prices.items()}
        self.trap_appearances = {int(key): item_record(value) for key, value in data["trap_appearances"].items()}
        self.locations = {}
        self.region_locations = {}
        for record in data["locations"]:
            record = dict(record)
            region_name = record.pop("region")
            record["item"] = item_record(record["item"])
            record["disabled"] = DisableType(record["disabled"])
            default = record["default"]
            if isinstance(default, list):
                record["default"] = ([tuple(entry) for entry in default]
                                     if default and isinstance(default[0], list) else tuple(default))
            location = SimpleNamespace(**record)
            self.locations[location.name] = location
            self.region_locations.setdefault(region_name, []).append(location)
        self.entrances = []
        for record in data["entrances"]:
            record = dict(record)
            replacement = record.pop("replacement")
            entrance = SimpleNamespace(**record)
            entrance.replaces = (None if replacement is None else
                                 entrance if replacement["name"] == entrance.name else
                                 SimpleNamespace(**replacement))
            self.entrances.append(entrance)
        entrance_by_name = {entrance.name: entrance for entrance in self.entrances}
        self.shuffled_grotto_entrances = [entrance_by_name[name] for name in data["shuffled_grotto_entrances"]]

    def apply_writes(self, rom, name):
        for address, value in self.writes[name]:
            rom.write_bytes(address, bytes.fromhex(value))

    def apply_messages(self, messages, name):
        for message_id, text, opts in self.messages[name]:
            update_message_by_id(messages, message_id, text, opts)
