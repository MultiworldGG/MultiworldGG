import argparse
import hashlib
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from location_positions import LOCATION_POSITIONS
from wishes import CHECKS, TURN_INS


NATIVE_CHECK_POSITIONS = frozenset({
    'Relic: Weaver Effigy (Camora, Moss Grotto)',
    'Bone Bottom - Rosary Dish',
})


def map_frame(room, image_path):
    # Song_20b's image covers the top 80 units of its 243-unit native scene.
    if room['in_game_id'] == 'Song_20b' and tuple(room[k] for k in
            ('scene_min_x', 'scene_min_y', 'scene_max_x', 'scene_max_y')) == (0, 0, 50, 80):
        if hashlib.sha256(image_path.read_bytes()).hexdigest() != '39cc2abe070ae316a5fec4a02b85e57608349a47288b5858291b26c3915a172b':
            raise ValueError('Rotating Tunnel image changed; review its map crop before rebuilding.')
        return dict(room, scene_min_y=163, scene_max_y=243)
    return room


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def is_spatial(name):
    return not name.startswith(("First Kill: ", "Crest Slot: ")) and name not in {"Crest: Hunter", "Goal"}


def scene_point(x, y, room, width, height, entrance=False):
    scene_width, scene_height = room["scene_width"], room["scene_height"]
    if x is None or y is None or not width or not height or not scene_width or not scene_height:
        return None
    x -= room["scene_min_x"]
    y -= room["scene_min_y"]
    margin = 1 if entrance else 0
    if not (-margin <= x <= scene_width + margin and -margin <= y <= scene_height + margin):
        return None
    # Gate centres can sit just outside the room boundary.
    return min(width, max(0, x * width / scene_width)), min(height, max(0, height - y * height / scene_height))


def image_point(entry, room, width, height, entrance=False):
    if not width or not height:
        return None
    x, y = entry.get("image_pixel_x"), entry.get("image_pixel_y")
    if x is not None and y is not None and 0 <= x <= width and 0 <= y <= height:
        return x, y
    if not entry.get("annotation_enabled"):
        return None
    return scene_point(entry.get("annotation_x"), entry.get("annotation_y"), room, width, height, entrance)


def marker(room, names, point, name=None):
    return {
        "name": name or names[0],
        "sections": [{"name": value} for value in names],
        "map_locations": [{"map": room["name"], "x": int(point[0]),
                           "y": int(point[1])}], # Actually in image coords cause they love me
    }


def build(geometry_path, image_root, output, world, catalogue_path=None, pack_path=None, manifest_path=None):
    from PIL import Image
    geometry = load(geometry_path)
    graph = load(world / "room_graph_data.json")
    pool = load(world / "entrance_pool.json")
    catalogue = set(load(world / "map_logic.json")["logic"]["requirements"])
    expected = {name for name in catalogue if is_spatial(name)}
    positions = LOCATION_POSITIONS
    by_scene = defaultdict(list)
    for position in positions:
        if position["name"] in expected:
            by_scene[position["scene"].casefold()].append(position)

    # Load entrance names first so we can ignore any that aren't real
    names = {e["id"]: f"{room['name']} - {e['name']} ({e['alias']})"
             for room in graph["rooms"] for e in room.get("transitions", [])}
    pool_names = {e["name"] for e in pool}
    pool_gates = {e['id']: e['gate'] for e in pool}
    pool_gates.update({alias['port']: alias['gate'] for e in pool for alias in e.get('aliases', [])
                       if alias['port'] != e['id']})
    native_gates = {}
    map_groups = {}
    catalogue_path = catalogue_path or geometry_path.parent / "silksong-room-catalogue.json"
    if catalogue_path.is_file():
        for room in load(catalogue_path)["rooms"]:
            scene = room.get("inGameId")
            if not scene or room.get("isArchived"):
                continue
            for gate in sorted(room.get("transitions", []), key=lambda g: not g.get("isArchived", False)):
                if gate.get("inGameId"):
                    native_gates[scene.casefold(), gate["inGameId"]] = {
                        "annotation_x": gate.get("annotationSceneUnitX"),
                        "annotation_y": gate.get("annotationSceneUnitY"),
                        "annotation_enabled": gate.get("enableAnnotation", False),
                        "in_game_x": gate.get('inGamePositionX'),
                        "in_game_y": gate.get('inGamePositionY'),
                    }
    for entrance in pool:
        for member in entrance.get("members", [entrance["id"]]):
            names[member] = entrance["name"]

    checks = defaultdict(list) # This one is going to be annoying
    check_rooms = defaultdict(set)
    for room in graph["rooms"]:
        for check in room.get("checks", []) + room.get("locations", []): # Because y'all can't decide to be right or wrong
            name = check.get("canonical_location")
            if name in expected:
                key = room["id"], check["label"]
                if name not in checks[key]:
                    checks[key].append(name)
                check_rooms[name].add(room["name"])

    for room_id, label, name in (
            ('the-slab/slab-first-sinner', 'Boss: First Sinner', 'Journal: First Sinner'),
            ('the-abyss/abyss-cocoon', 'Boss: Lost Lace', 'Journal: Lost Lace')):
        if name in expected:
            checks[room_id, label].append(name)

    rooms = {room["id"]: room for room in geometry["rooms"]}
    scenes = {(room["in_game_id"] or "").casefold() for room in rooms.values()}
    # We're going to build it up as an arbitrary list of dicts, then print it into a file
    # we need a map from scene name to map index, and i want it in python so it's easier to import
    maps, locations, mapping, image_manifest = [], [], {}, {}
    missing_images, image_mismatches, rejected, unknown_checks, unknown_entrances = [], [], [], [], []
    physical_entrances, positioned_entrances, positioned_checks = set(), set(), set()
    missing_links, turn_ins, entrance_details = [], {}, {}
    ignored = Counter()
    entrance_anchors = {}

    ## Assemble maps

    for original_room in geometry["rooms"]:
        room = original_room
        scene = room["in_game_id"]
        width, height = room["image_pixel_width"], room["image_pixel_height"]
        image_name = f"01-geometry/{room['image_guid']}.webp"
        image_path = image_root / f"{room['image_guid']}.webp"
        actual_size = None
        if image_path.is_file():
            with Image.open(image_path) as image:
                actual_size = image.size
            room = map_frame(room, image_path)
        elif scene:
            missing_images.append({"room": room["name"], "scene": scene, "image": image_name})
        if width and height:
            if actual_size and actual_size != (width, height):
                image_mismatches.append({"room": room["name"], "scene": scene, "image": image_name,
                                         "export_dimensions": [width, height], "image_dimensions": list(actual_size)})
        elif actual_size:
            width, height = actual_size

        children = []
        for entry in room.get("locations", []):
            location_names = checks.get((room["id"], entry.get("name")), [])
            if not location_names:
                if entry.get("name") in expected:
                    unknown_checks.append({"room": room["name"], "name": entry["name"]})
                else:
                    ignored[entry.get("location_type") or "untyped"] += 1
                continue
            location_names = [name for name in location_names
                              if name not in CHECKS and name not in NATIVE_CHECK_POSITIONS]
            if not location_names:
                continue
            point = image_point(entry, room, width, height)
            if point is not None:
                children.append(marker(room, location_names, point))

        positioned = {section["name"] for child in children for section in child["sections"]}
        for position in by_scene.get((scene or "").casefold(), []):
            name = position["name"]
            if name in positioned or name in CHECKS:
                continue
            point = scene_point(position["x"], position["y"], room, width, height)
            reason = None
            frame_matches = (position["width"], position["height"]) == (room["scene_max_x"], room["scene_max_y"])
            if room["scene_min_x"] or room["scene_min_y"]:
                frame_matches |= position["width"] >= room["scene_max_x"] and position["height"] >= room["scene_max_y"]
            if not width or not height:
                reason = "missing image dimensions"
            elif not frame_matches:
                reason = "coordinate frames differ"
            elif point is None:
                reason = "position outside room"
            if reason:
                rejected.append({"name": name, "scene": scene, "room": room["name"], "reason": reason,
                                 "source_dimensions": [position["width"], position["height"]],
                                 "map_dimensions": [room["scene_max_x"], room["scene_max_y"]]})
                continue
            children.append(marker(room, [name], point))
            positioned.add(name)
        positioned_checks.update(positioned)

        for entrance in room.get("transitions", []):
            name = names.get(entrance.get("id"))
            if name is None:
                unknown_entrances.append({"room": room["name"], "id": entrance.get("id")})
                continue
            target = rooms.get((entrance.get("target") or "").split("@")[0])
            nonphysical = not scene or room.get("is_metadata_only")
            if not entrance.get("in_game_id") and name not in pool_names:
                nonphysical |= bool(target and (target.get("is_metadata_only") or not target.get("in_game_id")))
                nonphysical |= entrance.get("name", "").casefold() in {"quest rebirth", "slab capture", "dummy", "unknown"}
            if nonphysical:
                missing_links.append({"name": name, "reason": "menu, scripted link or placeholder"})
            else:
                physical_entrances.add(name)
                entrance_details[name] = {"name": name, "room": room["name"], "scene": scene,
                                          "id": entrance["id"], "gate": entrance.get("in_game_id")}
            gate = pool_gates.get(entrance['id']) or entrance.get('in_game_id')
            native = native_gates.get(((scene or "").casefold(), gate))
            corrected_gate = gate != entrance.get('in_game_id')
            point = None if corrected_gate else image_point(entrance, room, width, height, entrance=True)
            if point is None and native:
                point = (scene_point(native['in_game_x'], native['in_game_y'], room, width, height, entrance=True)
                         if corrected_gate else image_point(native, room, width, height, entrance=True))
            if (point is None and scene == 'Last_Dive' and entrance['id'] == 'the-abyss/last-dive@d2'
                    and entrance.get('target') == 'the-abyss/abyss-cocoon@d'):
                # The cinematic leaves from the same spot, there isn't a second door.
                arrival = next((e for e in room['transitions'] if e.get('in_game_id') == 'door_cutscenePosition'), None)
                if arrival:
                    point = image_point(arrival, room, width, height, entrance=True)
            # These left-hand gates sit beyond the cropped edge of the column image.
            if point is None and scene == 'Shadow_09' and gate in {'left1', 'left2', 'left3'}:
                x, y = entrance.get('annotation_x'), entrance.get('annotation_y')
                if x is not None and 15 <= x < room['scene_min_x'] == 28:
                    point = scene_point(room['scene_min_x'], y, room, width, height, entrance=True)
            if point is None:
                continue
            # Keep existing markers for scripted links, without adding new ones.
            if nonphysical and (entrance.get("image_pixel_x") is None or entrance.get("image_pixel_y") is None):
                continue
            if name in pool_names and entrance.get("id") and scene:
                normalizedX = point[0] / width;
                normalizedY = point[1] / height;
                entrance_anchors[entrance["id"]] = {
                    "scene": scene, 
                    "gate": gate,
                    "x": round(normalizedX, 6),
                    "y": round(1.0 - normalizedY, 6),
                }
            children.append(marker(room, [name], point))
            positioned_entrances.add(name)

        if scene == "Ward_02":
            boss_marker = next((child for child in children
                                if any(s["name"] == "Boss: The Unravelled" for s in child["sections"])), None)
            if boss_marker:
                for child in children:
                    if any(s["name"] in {"Journal: The Unravelled", "The Unravelled - Silk Heart"}
                           for s in child["sections"]):
                        child["map_locations"] = boss_marker["map_locations"]

        grouped = {}
        for child in children:
            point = child["map_locations"][0]
            key = point["x"], point["y"]
            if key not in grouped:
                grouped[key] = child
            else:
                sections = grouped[key]["sections"]
                sections.extend(section for section in child["sections"] if section not in sections)
        children = list(grouped.values())

        for host, (position, _) in TURN_INS.items():
            host_scene, x, y, host_width, host_height = position
            if scene != host_scene:
                continue
            point = scene_point(x, y, room, width, height)
            if (host_width, host_height) != (room["scene_max_x"], room["scene_max_y"]) or point is None:
                turn_ins[host] = {"host": host, "room": room["name"], "scene": scene,
                                 "reason": "coordinate frames differ" if width and height else "missing image dimensions",
                                 "source_dimensions": [host_width, host_height],
                                 "map_dimensions": [room["scene_max_x"], room["scene_max_y"]]}
                continue
            children.append(marker(room, [f"Turn-in: {name}" for name in CHECKS],
                                   point, name=host))
            turn_ins[host] = None

        if children:
            if actual_size is None:
                raise ValueError(f"Map markers have no image: {room['name']}")
            if not scene or scene in mapping:
                raise ValueError(f"Room map has no unique scene: {room['name']}")
            mapping[scene] = len(maps)
            temp_map = {"name": room["name"], "img": image_name}
            if room["scene_height"]:
                temp_map["location_size"] = max(int(3 * height / room["scene_height"]), 1) # Three scene units tall
                temp_map["location_border_thickness"] = max(int(0.5 * height / room["scene_height"]), 1)
            maps.append(temp_map)
            image_manifest[image_name] = dict(sha256=hashlib.sha256(image_path.read_bytes()).hexdigest(),
                                             width=width, height=height)
            locations.append({"name": room["name"], "children": children}) # Don't add a map with nothing on it
            if "room_group_name" in room:
                if room["room_group_name"] not in map_groups:
                    map_groups[room["room_group_name"]] = []
                map_groups[room["room_group_name"]].append(room["name"])

    present_hosts = {host for host, issue in turn_ins.items() if issue is None}
    positioned_checks.update(name for name, (_, host) in CHECKS.items() if host in present_hosts)
    missing = expected - positioned_checks
    missing_rooms = defaultdict(set)
    for position in positions:
        if position["name"] in missing and position["scene"].casefold() not in scenes:
            missing_rooms[position["scene"].casefold()].add(position["name"])
    for host, (position, _) in TURN_INS.items():
        if host not in turn_ins:
            turn_ins[host] = {"host": host, "scene": position[0], "reason": "missing room"}
    errors = {
        "coverage_source": "map_logic.json",
        "missing_locs": sorted(missing),
        "missing_ents": sorted(physical_entrances - positioned_entrances),
        "entrance_details": [entrance_details[name] for name in sorted(physical_entrances - positioned_entrances)],
        "missing_rooms": [{"scene": scene, "locations": sorted(values)} for scene, values in sorted(missing_rooms.items())],
        "missing_images": missing_images,
        "image_mismatches": image_mismatches,
        "rejected_positions": [row for row in rejected if row["name"] in missing],
        "missing_turn_ins": [issue for issue in turn_ins.values() if issue is not None],
        "skipped_locs": [row for row in unknown_checks if row["name"] in missing],
        "skipped_ents": unknown_entrances,
        "unpositioned_locs": [{"name": name, "rooms": sorted(check_rooms[name])} for name in sorted(missing)
                             if not any(p["name"] == name for p in positions)],
        "ignored": {"non_spatial_checks": sorted(catalogue - expected),
                    "geometry_objects": dict(sorted(ignored.items())),
                    "aliases_resolved_elsewhere": [row for row in unknown_checks if row["name"] not in missing],
                    "nonphysical_links": [row for row in missing_links if row["name"] not in positioned_entrances]},
    }
    if image_mismatches:
        raise ValueError('Map images do not match the exported dimensions: ' +
                         ', '.join(row['room'] for row in image_mismatches))
    if (output / 'mapping.py').exists():
        import ast
        old = ast.parse((output / 'mapping.py').read_text(encoding='utf-8'))
        previous = next(ast.literal_eval(node.value) for node in old.body
                        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'mapping'
                                                               for t in node.targets))
        lost = previous.keys() - mapping.keys()
        if lost:
            raise ValueError('Rebuild would remove existing room maps: ' + ', '.join(sorted(lost)))
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [("maps.json", maps), ("locations.json", locations), ("errors.json", errors), ("entrance_anchors.json", entrance_anchors)]:
        (output / filename).write_text(json.dumps(data, indent=1), encoding="utf-8")
    source = "# Generated File\n\nfrom typing import Any\n\nmapping = {\n"
    source += "".join(f"\t{json.dumps(scene)}:{index},\n" for scene, index in mapping.items())
    source += "}\n\n\ndef ut_page_index(data: Any) -> int:\n\treturn mapping.get(data, -1) if isinstance(data, str) else -1\n\n"
    source += "tracker_map_groups = [\n"
    for group, pages in map_groups.items():
        source += f"\t({json.dumps(group)}, [\n"
        source += "".join(f"\t\t({json.dumps(page)}, {json.dumps(page)}),\n" for page in pages)
        source += "\t]),\n"
    source += "]\n\n"
    (output / "mapping.py").write_text(source, encoding="utf-8")
    if manifest_path:
        manifest = dict(images=image_manifest,
                        files={name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                               for name in ('maps.json', 'locations.json', 'mapping.py', 'entrance_anchors.json')},
                        inputs={name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in (
                            ('geometry', geometry_path), ('catalogue', catalogue_path),
                            ('graph', world / 'room_graph_data.json'), ('pool', world / 'entrance_pool.json'),
                            ('logic', world / 'map_logic.json'), ('generator', Path(__file__)),
                            ('positions', Path(__file__).with_name('location_positions.py')),
                            ('wishes', Path(__file__).with_name('wishes.py'))) if path.is_file()})
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=1), encoding='utf-8')
    if pack_path:
        pack_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(pack_path, 'w', compression=zipfile.ZIP_STORED) as pack:
            for name in sorted(image_manifest):
                info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                pack.writestr(info, (image_root / Path(name).name).read_bytes())
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build UT maps and report remaining mapping gaps.")
    parser.add_argument("--geometry", type=Path, default=Path("room_geometry_data.json"))
    parser.add_argument("--images", type=Path)
    parser.add_argument("--catalogue", type=Path, help="Room catalogue containing native gate annotations")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--pack', type=Path, help='Write the matching UT image pack')
    parser.add_argument('--manifest', type=Path, help='Write validation metadata to this separate file')
    args = parser.parse_args()
    errors = build(args.geometry, args.images or args.geometry.parent / "01-geometry",
                   args.output, Path(__file__).resolve().parent.parent, args.catalogue, args.pack, args.manifest)
    print(f"Missing locations: {len(errors['missing_locs'])}; physical entrances: {len(errors['missing_ents'])}; "
          f"room images: {len(errors['missing_images'])}")

