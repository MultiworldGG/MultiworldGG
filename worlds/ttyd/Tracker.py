"""
Compiler for the in-game tracker: bakes the final, post-options access logic
(regions, connections, per-location rules) into /mod/tracker.bin for the mod's
evaluator. The mod evaluates rules against live game state (pouchCheckItem,
party joins, curse items, star counts), so Python stays the single source of
truth for logic while the game only interprets bytecode.

Bytecode ops (all big-endian):
  0x00 TRUE
  0x01 FALSE
  0x02 AND   u8 n, then n sub-expressions
  0x03 OR    u8 n, then n sub-expressions
  0x04 HAS   u16 item (rom id, or 0x7F00 = "stars" pseudo), u16 count
  0x05 REACH_LOC    u16 location index
  0x06 REACH_REGION u8 region index
  0x07 COUNT_LOCS   u8 n, u8 k, n * u16 location index   (>= k reachable)
  0x08 COUNT_ITEMS  u8 n, u8 k, n * u16 rom id           (>= k owned)

tracker.bin layout:
  header (36B): magic 'TRK2', u16 regionCount, u16 locationCount,
                u16 connectionCount, u16 nodeCount, u32 offLocations,
                u32 offConnections, u32 offNodes, u32 offRules, u32 offStrings,
                u32 offTattle
  Location (12B): u16 nameOff, u16 ruleOff (0xFFFF = TRUE), u8 region,
                  u8 gswType (0 GSW byte >= value, 1 GSWF set, 2 tattle
                  any-of-units keyed by gswId = locId - 78780850, 0xFF
                  undetectable), u16 gswId, u8 gswValue, u8 flags (bit0 =
                  disabled), u8 dispRegion (region for node membership; differs
                  from `region` for display-only groups like Cooking), u8 pad
  Connection (4B): u8 src, u8 dst, u16 ruleOff
  Node (16B): char prefix[7] NUL-padded, u8 gateRegion, u8 dispCount,
              u8 disp[6], u8 pad
"""
import json
import pkgutil
import struct
import typing

from .Data import location_gsw_info, location_to_unit, star_locations, GSWType
from .Locations import all_locations
from .Options import StarShuffle, EnemyRandomizer, BossRandomizer, Goal, PalaceSkip

if typing.TYPE_CHECKING:
    from . import TTYDWorld

STARS_PSEUDO_ITEM = 0x7F00

REGIONS = [
    "Menu",                                  # 0
    "Rogueport",                             # 1
    "Rogueport (Westside)",                  # 2
    "Rogueport Sewers",                      # 3
    "Rogueport Sewers Westside",             # 4
    "Rogueport Sewers Westside Ground",      # 5
    "Petal Meadows (Left)",                  # 6
    "Petal Meadows (Right)",                 # 7
    "Hooktail's Castle",                     # 8
    "Boggly Woods",                          # 9
    "Great Tree",                            # 10
    "Glitzville",                            # 11
    "Twilight Town",                         # 12
    "Twilight Trail",                        # 13
    "Creepy Steeple",                        # 14
    "Keelhaul Key",                          # 15
    "Pirate's Grotto",                       # 16
    "Excess Express",                        # 17
    "Riverside Station",                     # 18
    "Poshley Heights",                       # 19
    "Fahr Outpost",                          # 20
    "X-Naut Fortress",                       # 21
    "Palace of Shadow",                      # 22
    "Palace of Shadow (Post-Riddle Tower)",  # 23
    "Pit of 100 Trials",                     # 24
    "Shadow Queen",                          # 25
    "Tattlesanity",                          # 26
    "Cooking",                               # 27 (display-only: no connections)
]
REGION_IDX = {name: i for i, name in enumerate(REGIONS)}

# Region -> location tag (mirrors Regions.get_regions_dict)
REGION_TAGS = {
    "Rogueport": "rogueport",
    "Rogueport (Westside)": "rogueport_westside",
    "Rogueport Sewers": "sewers",
    "Rogueport Sewers Westside": "sewers_westside",
    "Rogueport Sewers Westside Ground": "sewers_westside_ground",
    "Petal Meadows (Left)": "petal_left",
    "Petal Meadows (Right)": "petal_right",
    "Hooktail's Castle": "hooktails_castle",
    "Boggly Woods": "boggly_woods",
    "Great Tree": "great_tree",
    "Glitzville": "glitzville",
    "Twilight Town": "twilight_town",
    "Twilight Trail": "twilight_trail",
    "Creepy Steeple": "creepy_steeple",
    "Keelhaul Key": "keelhaul_key",
    "Pirate's Grotto": "pirates_grotto",
    "Excess Express": "excess_express",
    "Riverside Station": "riverside",
    "Poshley Heights": "poshley_heights",
    "Fahr Outpost": "fahr_outpost",
    "X-Naut Fortress": "xnaut_fortress",
    "Palace of Shadow": "palace",
    "Palace of Shadow (Post-Riddle Tower)": "riddle_tower",
    "Pit of 100 Trials": "pit",
    "Tattlesanity": "tattle",
}

# StateLogic functions expressed in the rules.json expression dialect.
# Keep 1:1 with StateLogic.py.
STATELOGIC: dict = {
    "super_hammer": {"has": {"item": "Progressive Hammer", "count": 1}},
    "ultra_hammer": {"has": {"item": "Progressive Hammer", "count": 2}},
    "super_boots": {"has": {"item": "Progressive Boots", "count": 1}},
    "ultra_boots": {"has": {"item": "Progressive Boots", "count": 2}},
    "tube_curse": {"and": [{"has": "Paper Mode"}, {"has": "Tube Mode"}]},
    "key_any": {"or": [{"has": "Red Key"}, {"has": "Blue Key"}]},
    "westside": {"or": [{"has": "Contact Lens"}, {"has": "Bobbery"},
                        {"function": "tube_curse"}, {"function": "ultra_hammer"}]},
    "petal_left": {"has": "Plane Mode"},
    "hooktails_castle": {"and": [{"has": "Sun Stone"}, {"has": "Moon Stone"},
                                 {"or": [{"has": "Koops"}, {"has": "Bobbery"}]}]},
    "boggly_woods": {"has": "Paper Mode"},
    "great_tree": {"has": "Flurrie"},
    "glitzville": {"has": "Blimp Ticket"},
    "sewer_westside": {"or": [
        {"function": "tube_curse"},
        {"has": "Bobbery"},
        {"and": [{"has": "Paper Mode"}, {"has": "Contact Lens"}]},
        {"and": [{"function": "ultra_hammer"},
                 {"or": [{"has": "Paper Mode"},
                         {"and": [{"function": "ultra_boots"}, {"has": "Yoshi"}]}]}]},
    ]},
    "sewer_westside_ground": {"or": [
        {"and": [{"has": "Contact Lens"}, {"has": "Paper Mode"}]},
        {"has": "Bobbery"},
        {"function": "tube_curse"},
        {"function": "ultra_hammer"},
    ]},
    "twilight_town": {"or": [
        {"and": [{"function": "sewer_westside"}, {"has": "Yoshi"}]},
        {"and": [{"function": "sewer_westside_ground"}, {"function": "ultra_boots"}]},
    ]},
    "twilight_trail": {"and": [{"function": "twilight_town"}, {"function": "tube_curse"}]},
    "steeple": {"and": [{"has": "Paper Mode"}, {"has": "Flurrie"}, {"function": "super_boots"}]},
    "keelhaul_key": {"and": [{"has": "Yoshi"}, {"function": "tube_curse"}, {"has": "Old Letter"}]},
    "pirates_grotto": {"and": [{"has": "Yoshi"}, {"has": "Bobbery"}, {"has": "Skull Gem"},
                               {"function": "super_boots"}]},
    "excess_express": {"has": "Train Ticket"},
    "riverside": {"and": [{"has": "Vivian"}, {"has": "Autograph"}, {"has": "Ragged Diary"},
                          {"has": "Blanket"}, {"has": "Vital Paper"}, {"has": "Train Ticket"}]},
    "poshley_heights": {"and": [{"has": "Station Key 1"}, {"has": "Elevator Key (Station)"},
                                {"function": "super_hammer"}, {"function": "ultra_boots"}]},
    "fahr_outpost": {"and": [{"function": "ultra_hammer"}, {"function": "twilight_town"}]},
    "moon": {"and": [{"has": "Bobbery"}, {"has": "Goldbob Guide"}]},
    "ttyd": {"or": [
        {"has": "Plane Mode"},
        {"function": "super_hammer"},
        {"and": [{"has": "Flurrie"},
                 {"or": [{"has": "Bobbery"}, {"function": "tube_curse"},
                         {"and": [{"has": "Contact Lens"}, {"has": "Paper Mode"}]}]}]},
    ]},
    "pit": {"and": [{"has": "Paper Mode"}, {"has": "Plane Mode"}]},
    "pit_westside_ground": {"and": [
        {"has": "Flurrie"},
        {"or": [{"and": [{"has": "Contact Lens"}, {"has": "Paper Mode"}]},
                {"has": "Bobbery"}, {"function": "tube_curse"}, {"function": "ultra_hammer"}]},
    ]},
    "riddle_tower": {"and": [{"function": "tube_curse"}, {"has": "Palace Key"}, {"has": "Bobbery"},
                             {"has": "Boat Mode"}, {"has": "Star Key"},
                             {"has": {"item": "Palace Key (Tower)", "count": 8}}]},
    "super_blue_pipes": {"and": [{"function": "super_hammer"}, {"function": "super_boots"}]},
    "ultra_blue_pipes": {"and": [{"function": "ultra_hammer"}, {"function": "super_boots"}]},
}

# Map-node prefixes (mapMarkers[i].map_prefix) -> (fast-travel gate region,
# regions aggregated for the hover display). Mirrors customWarp.h destinations.
NODES = [
    ("gor",    "Rogueport",             ["Rogueport", "Rogueport (Westside)"]),
    ("tik",    "Rogueport Sewers",      ["Rogueport Sewers", "Rogueport Sewers Westside",
                                         "Rogueport Sewers Westside Ground", "Pit of 100 Trials"]),
    ("hei",    "Petal Meadows (Left)",  ["Petal Meadows (Left)", "Petal Meadows (Right)"]),
    ("nok",    "Petal Meadows (Right)", ["Petal Meadows (Right)"]),
    ("gon",    "Hooktail's Castle",     ["Hooktail's Castle"]),
    ("win",    "Boggly Woods",          ["Boggly Woods"]),
    ("hou",    "Boggly Woods",          ["Boggly Woods"]),
    ("mri",    "Great Tree",            ["Great Tree"]),
    ("tou",    "Glitzville",            ["Glitzville"]),
    ("usu",    "Twilight Town",         ["Twilight Town"]),
    ("gra",    "Twilight Trail",        ["Twilight Trail"]),
    ("jin",    "Creepy Steeple",        ["Creepy Steeple"]),
    ("muj",    "Keelhaul Key",          ["Keelhaul Key"]),
    ("dou",    "Pirate's Grotto",       ["Pirate's Grotto"]),
    ("rsh",    "Excess Express",        ["Excess Express"]),
    ("eki",    "Riverside Station",     ["Riverside Station"]),
    ("pik",    "Poshley Heights",       ["Poshley Heights"]),
    ("sin",    "Poshley Heights",       ["Poshley Heights"]),
    ("bom",    "Fahr Outpost",          ["Fahr Outpost"]),
    ("moo",    "X-Naut Fortress",       ["X-Naut Fortress"]),
    ("aji",    "X-Naut Fortress",       ["X-Naut Fortress"]),
    ("las",    "Palace of Shadow",      ["Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)",
                                         "Shadow Queen"]),
    ("las_09", "Palace of Shadow",      ["Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)",
                                         "Shadow Queen"]),
    # Virtual nodes: mod-added map markers (not fast-travelable)
    ("tattle", "Tattlesanity",          ["Tattlesanity"]),
    ("cook",   "Rogueport (Westside)",  ["Cooking"]),
]


class TrackerCompiler:
    def __init__(self, world: "TTYDWorld"):
        self.world = world
        items = json.loads(pkgutil.get_data(__name__, "json/items.json").decode("utf-8"))
        self.item_rom = {it["item_name"]: it["rom_id"] for it in items}
        # pseudo-items
        self.item_rom["stars"] = STARS_PSEUDO_ITEM

        self.locations = [loc for loc in all_locations]
        self.loc_idx = {loc.name: i for i, loc in enumerate(self.locations)}

        self.rule_pool = bytearray()
        self.rule_cache: dict = {}
        self.string_pool = bytearray()
        self.string_cache: dict = {}

    # ---- pools ----
    def add_string(self, s: str) -> int:
        if s in self.string_cache:
            return self.string_cache[s]
        off = len(self.string_pool)
        self.string_pool += s.encode("ascii", "replace") + b"\x00"
        self.string_cache[s] = off
        return off

    def add_rule(self, code: bytes) -> int:
        key = bytes(code)
        if key in self.rule_cache:
            return self.rule_cache[key]
        off = len(self.rule_pool)
        assert off <= 0xFFFE, "rule pool overflow"
        self.rule_pool += code
        self.rule_cache[key] = off
        return off

    # ---- expression compilation (rules.json dialect) ----
    def compile_expr(self, r) -> bytes:
        if r is None or r is True:
            return b"\x00"
        if r is False:
            return b"\x01"
        if "or" in r:
            subs = [self.compile_expr(x) for x in r["or"]]
            return bytes([0x03, len(subs)]) + b"".join(subs)
        if "and" in r:
            subs = [self.compile_expr(x) for x in r["and"]]
            return bytes([0x02, len(subs)]) + b"".join(subs)
        if "has" in r:
            hv = r["has"]
            if isinstance(hv, dict):
                item, count = hv.get("item", ""), hv.get("count", 1)
            else:
                item, count = hv, r.get("count", 1)
            if item == "required_stars":
                roms = [113 + c for c in self.world.required_chapters]
                return struct.pack(">BBB", 0x08, len(roms), count) + b"".join(
                    struct.pack(">H", x) for x in roms)
            rom = self.item_rom[item]
            return struct.pack(">BHH", 0x04, rom, count)
        if "function" in r:
            fn = r["function"]
            if isinstance(fn, dict):
                name, count = fn.get("name", ""), fn.get("count")
            else:
                name, count = fn, None
            if name == "chapter_completions":
                idxs = [self.loc_idx[n] for n in star_locations if n in self.loc_idx]
                return struct.pack(">BBB", 0x07, len(idxs), int(count)) + b"".join(
                    struct.pack(">H", i) for i in idxs)
            return self.compile_expr(STATELOGIC[name])
        if "can_reach" in r:
            return struct.pack(">BH", 0x05, self.loc_idx[r["can_reach"]])
        if "reach_region" in r:
            return struct.pack(">BB", 0x06, REGION_IDX[r["reach_region"]])
        return b"\x01"  # unknown -> FALSE (matches Rules.py fallback)

    # ---- per-seed rule assembly ----
    def location_rules(self) -> dict:
        from .Rules import get_tattle_rules_dict, get_random_enemy_tattle_rules_dict
        from .Locations import location_id_to_name, get_locations_by_tags, get_location_ids
        from .Data import pit_exclusive_tattle_stars_required
        from .Options import PitItems

        world = self.world
        rules_json = json.loads(pkgutil.get_data(__name__, "json/rules.json").decode("utf-8"))
        out: dict = {}

        for name, req in rules_json.items():
            if name not in self.loc_idx:
                continue
            if name == "Glitzville Promoter's Office: Jolene's Trouble Reward" and not world.options.troublesanity:
                out[name] = {"has": {"item": "Battle Trunks", "count": 20}}
                continue
            out[name] = req

        # Palace final staircase stars gate (Rules.set_rules)
        for name in ["Palace of Shadow Final Staircase: Ultra Shroom",
                     "Palace of Shadow Final Staircase: Jammin' Jelly"]:
            extra = {"has": {"item": "stars", "count": world.options.goal_stars.value}}
            out[name] = {"and": [out[name], extra]} if name in out else extra

        # Tattle gating (mirrors Rules.set_tattle_rules)
        if world.options.tattlesanity:
            goombella = {"has": "Goombella"}
            for loc in get_locations_by_tags("tattle"):
                if loc.name in world.disabled_locations:
                    continue
                out[loc.name] = ({"and": [out[loc.name], goombella]}
                                 if loc.name in out else goombella)
            dynamic = (world.options.enemy_randomizer != EnemyRandomizer.option_vanilla
                       or world.options.boss_randomizer != BossRandomizer.option_vanilla)
            tattle_dict = (get_random_enemy_tattle_rules_dict(world) if dynamic
                           else get_tattle_rules_dict())
            pit_ids = set(get_location_ids(get_locations_by_tags("pit_floor")))
            pit_names = {n for names in pit_exclusive_tattle_stars_required.values() for n in names}
            for loc_name, gate_ids in tattle_dict.items():
                if loc_name in world.disabled_locations or loc_name not in self.loc_idx:
                    continue
                if len(gate_ids) == 0:
                    # Shadow-Queen-access family (Rules.py lines 65-72)
                    if world.options.palace_skip == PalaceSkip.option_true and world.options.goal != Goal.option_shadow_queen:
                        cond = {"has": {"item": "stars", "count": world.options.palace_stars.value}}
                    elif world.options.goal == Goal.option_shadow_queen:
                        cond = {"can_reach": "Shadow Queen"}
                    else:
                        cond = {"can_reach": "Palace of Shadow Final Staircase: Ultra Shroom"}
                else:
                    ids = [i for i in gate_ids if location_id_to_name[i] not in world.disabled_locations]
                    if not ids:
                        continue
                    if world.options.pit_items != PitItems.option_all and loc_name not in pit_names:
                        non_pit = [i for i in ids if i not in pit_ids]
                        if non_pit:
                            ids = non_pit
                    cond = {"or": [{"can_reach": location_id_to_name[i]} for i in ids]}
                out[loc_name] = {"and": [out[loc_name], cond]} if loc_name in out else cond
        return out

    def connections(self) -> list:
        world = self.world
        opts = world.options
        stars_all = opts.star_shuffle.value == StarShuffle.option_all

        def palace_expr(count: int):
            star = ({"has": {"item": "stars", "count": count}} if stars_all
                    else {"has": {"item": "required_stars", "count": count}})
            return {"and": [{"function": "ttyd"}, star]}

        conns = [
            ("Menu", "Rogueport", None),
            ("Menu", "Tattlesanity", None),
            ("Rogueport", "Rogueport Sewers", None),
            ("Rogueport", "Rogueport Sewers Westside", {"function": "sewer_westside"}),
            ("Rogueport Sewers Westside", "Twilight Town", {"has": "Yoshi"}),
            ("Rogueport", "Rogueport Sewers Westside Ground", {"function": "sewer_westside_ground"}),
            ("Rogueport Sewers Westside Ground", "Pit of 100 Trials", {"function": "pit_westside_ground"}),
            ("Rogueport Sewers Westside Ground", "Rogueport (Westside)", None),
            ("Rogueport Sewers Westside Ground", "Twilight Town", {"function": "ultra_boots"}),
            ("Rogueport Sewers", "Pit of 100 Trials", {"function": "pit"}),
            ("Rogueport", "Palace of Shadow", palace_expr(opts.palace_stars.value)),
            ("Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)", {"function": "riddle_tower"}),
            ("Palace of Shadow (Post-Riddle Tower)", "Shadow Queen",
             {"and": [{"can_reach": "Palace of Shadow Final Staircase: Ultra Shroom"},
                      {"has": {"item": "stars", "count": opts.goal_stars.value}}]}),
            ("Rogueport", "Fahr Outpost", {"function": "fahr_outpost"}),
            ("Rogueport", "Keelhaul Key", {"function": "keelhaul_key"}),
            ("Keelhaul Key", "Pirate's Grotto", {"function": "pirates_grotto"}),
            ("Rogueport", "Rogueport (Westside)", {"function": "westside"}),
            ("Rogueport (Westside)", "Glitzville", {"function": "glitzville"}),
            ("Rogueport (Westside)", "Rogueport Sewers Westside", {"has": "Paper Mode"}),
            ("Rogueport (Westside)", "Excess Express", {"function": "excess_express"}),
            ("Excess Express", "Riverside Station", {"function": "riverside"}),
            ("Riverside Station", "Poshley Heights", {"function": "poshley_heights"}),
            ("Rogueport Sewers", "Petal Meadows (Left)", {"function": "petal_left"}),
            ("Rogueport Sewers", "Boggly Woods", {"function": "boggly_woods"}),
            ("Twilight Town", "Twilight Trail", {"function": "twilight_trail"}),
            ("Twilight Trail", "Creepy Steeple", {"function": "steeple"}),
            ("Petal Meadows (Left)", "Petal Meadows (Right)", None),
            ("Petal Meadows (Left)", "Hooktail's Castle", {"function": "hooktails_castle"}),
            ("Boggly Woods", "Great Tree", {"function": "great_tree"}),
            ("Fahr Outpost", "X-Naut Fortress", {"function": "moon"}),
        ]
        if opts.palace_skip:
            conns.append(("Rogueport", "Shadow Queen", palace_expr(opts.goal_stars.value)))
        if opts.open_westside:
            conns.append(("Menu", "Rogueport (Westside)", None))
        if opts.blue_pipe_toggle:
            conns.append(("Rogueport Sewers", "Petal Meadows (Right)",
                          {"or": [{"function": "super_blue_pipes"}, {"function": "petal_left"}]}))
            conns.append(("Rogueport Sewers", "Boggly Woods",
                          {"or": [{"function": "super_blue_pipes"}, {"function": "boggly_woods"}]}))
            conns.append(("Rogueport Sewers", "Keelhaul Key",
                          {"or": [{"function": "ultra_blue_pipes"}, {"function": "keelhaul_key"}]}))
            conns.append(("Rogueport Sewers", "Poshley Heights",
                          {"or": [{"function": "ultra_blue_pipes"},
                                  {"and": [{"reach_region": "Rogueport (Westside)"},
                                           {"function": "excess_express"},
                                           {"function": "riverside"},
                                           {"function": "poshley_heights"}]}]}))
        excluded = self.world.excluded_regions
        return [(s, t, r) for (s, t, r) in conns if s not in excluded and t not in excluded]

    def location_region(self, loc) -> int:
        if loc.name == "Shadow Queen":
            return REGION_IDX["Shadow Queen"]
        tags = set(loc.tags)
        if "tattle" in tags:
            return REGION_IDX["Tattlesanity"]
        for region, tag in REGION_TAGS.items():
            if tag in tags:
                return REGION_IDX[region]
        return REGION_IDX["Rogueport"]  # untagged fallback

    def build(self) -> bytes:
        world = self.world
        rules = self.location_rules()

        loc_entries = bytearray()
        for i, loc in enumerate(self.locations):
            name_off = self.add_string(loc.name)
            rule_off = 0xFFFF
            if loc.name in rules:
                rule_off = self.add_rule(self.compile_expr(rules[loc.name]))
            region = self.location_region(loc)
            flags = 1 if loc.name in world.disabled_locations else 0

            gsw_type, gsw_id, gsw_value = 0xFF, 0, 0
            if loc.name == "Shadow Queen":
                gsw_type, gsw_id, gsw_value = 0, 1708, 18
            elif loc.id is not None:
                info = location_gsw_info.get(loc.id)
                if loc.id in location_to_unit:
                    gsw_type, gsw_id, gsw_value = 2, loc.id - 78780850, 0
                elif info is not None and info[1] != 0:
                    gsw_type = 0 if info[0] == GSWType.GSW else 1
                    gsw_id, gsw_value = info[1], info[2]

            disp_region = REGION_IDX["Cooking"] if "cooking" in loc.tags else region
            loc_entries += struct.pack(">HHBBHBBBx", name_off, rule_off, region,
                                       gsw_type, gsw_id, gsw_value & 0xFF, flags, disp_region)

        conn_entries = bytearray()
        conns = self.connections()
        for (src, dst, expr) in conns:
            rule_off = 0xFFFF if expr is None else self.add_rule(self.compile_expr(expr))
            conn_entries += struct.pack(">BBH", REGION_IDX[src], REGION_IDX[dst], rule_off)

        node_entries = bytearray()
        for prefix, gate, disp in NODES:
            disp_idx = [REGION_IDX[r] for r in disp][:6]
            node_entries += struct.pack(">7sBB6sB", prefix.encode("ascii"), REGION_IDX[gate],
                                        len(disp_idx), bytes(disp_idx).ljust(6, b"\x00"), 0)

        # tattle any-of-units table for gswType 2: 124 u16 offsets (indexed by
        # locId - 78780850) into {u8 n, n*u8 unit} records that follow the table.
        tattle_table = bytearray()
        tattle_units = bytearray()
        for lid in range(78780850, 78780974):
            units = location_to_unit.get(lid, [])
            tattle_table += struct.pack(">H", len(tattle_units))
            tattle_units += bytes([len(units)]) + bytes(u & 0xFF for u in units)

        header_size = 36
        off_loc = header_size
        off_conn = off_loc + len(loc_entries)
        off_nodes = off_conn + len(conn_entries)
        off_rules = off_nodes + len(node_entries)
        off_strings = off_rules + len(self.rule_pool)
        off_tattle = off_strings + len(self.string_pool)

        header = struct.pack(">4sHHHHIIIIII", b"TRK2", len(REGIONS), len(self.locations),
                             len(conns), len(NODES), off_loc, off_conn, off_nodes,
                             off_rules, off_strings, off_tattle)
        assert len(header) == header_size

        return bytes(header) + bytes(loc_entries) + bytes(conn_entries) + bytes(node_entries) \
            + bytes(self.rule_pool) + bytes(self.string_pool) + bytes(tattle_table) + bytes(tattle_units)


def build_tracker_bin(world: "TTYDWorld") -> bytes:
    return TrackerCompiler(world).build()
