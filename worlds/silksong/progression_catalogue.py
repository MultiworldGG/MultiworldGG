from __future__ import annotations

import json
import pkgutil


def _tuples(value):
    return tuple(_tuples(part) for part in value) if isinstance(value, list) else value


_data = json.loads(pkgutil.get_data(__package__, "progression_catalogue.json"))
if _data["schema"] != 1:
    raise ValueError("Unsupported progression catalogue.")
BOSS_IDS = frozenset(_data["bosses"])
WISH_IDS = frozenset(_data["wishes"])
STORY_GATES = _tuples(_data["story_gates"])
DONATIONS = _tuples(_data["donations"])
COLLECTIONS = _tuples(_data["collections"])
NPC_DELIVERIES = _tuples(_data["npc_deliveries"])
