import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image
from location_positions import LOCATION_POSITIONS
from wishes import CHECKS, TURN_INS


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


def build(geometry_path, image_root, output, world, catalogue_path=None):
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
    pool_gates = {member: e["gate"] for e in pool for member in e.get("members", [e["id"]])}
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

    rooms = {room["id"]: room for room in geometry["rooms"]}
    scenes = {(room["in_game_id"] or "").casefold() for room in rooms.values()}
    # We're going to build it up as an arbitrary list of dicts, then print it into a file
    # we need a map from scene name to map index, and i want it in python so it's easier to import
    maps, locations, mapping = [], [], {}
    missing_images, image_mismatches, rejected, unknown_checks, unknown_entrances = [], [], [], [], []
    physical_entrances, positioned_entrances, positioned_checks = set(), set(), set()
    missing_links, turn_ins, entrance_details = [], {}, {}
    ignored = Counter()

    ## Assemble maps

    for room in geometry["rooms"]:
        scene = room["in_game_id"]
        width, height = room["image_pixel_width"], room["image_pixel_height"]
        image_name = f"01-geometry/{room['image_guid']}.webp"
        image_path = image_root / f"{room['image_guid']}.webp"
        actual_size = None
        if image_path.is_file():
            with Image.open(image_path) as image:
                actual_size = image.size
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
            location_names = [name for name in location_names if name not in CHECKS]
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
            point = image_point(entrance, room, width, height, entrance=True)
            gate = entrance.get("in_game_id") or pool_gates.get(entrance["id"])
            native = native_gates.get(((scene or "").casefold(), gate))
            if point is None and native:
                point = image_point(native, room, width, height, entrance=True)
            if point is None:
                continue
            # Keep existing markers for scripted links, without adding new ones.
            if nonphysical and (entrance.get("image_pixel_x") is None or entrance.get("image_pixel_y") is None):
                continue
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
            if not scene or scene in mapping:
                raise ValueError(f"Room map has no unique scene: {room['name']}")
            mapping[scene] = len(maps)
            temp_map = {"name": room["name"], "img": image_name}
            if room["scene_height"]:
                temp_map["location_size"] = max(int(3 * height / room["scene_height"]), 1) # Three scene units tall
                temp_map["location_border_thickness"] = max(int(0.5 * height / room["scene_height"]), 1)
            maps.append(temp_map)
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
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [("maps.json", maps), ("locations.json", locations), ("errors.json", errors)]:
        (output / filename).write_text(json.dumps(data, indent=1), encoding="utf-8")
    source = "# Generated File\n\nfrom typing import Any\n\nmapping = {\n"
    source += "".join(f"\t{json.dumps(scene)}:{index},\n" for scene, index in mapping.items())
    source += "}\n\n\ndef ut_page_index(data: Any) -> int:\n\tif data in mapping:\n\t\treturn mapping[data]\n\treturn 0\n\n"
    source += "tracker_map_groups = [\n"
    source += "".join(f"\t({json.dumps(group)}, [{', '.join(f'({json.dumps(imap)},{json.dumps(imap)})' for imap in maps)}]),\n" for group, maps in map_groups.items())
    source += "]\n\n"
    (output / "mapping.py").write_text(source, encoding="utf-8")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build UT maps and report remaining mapping gaps.")
    parser.add_argument("--geometry", type=Path, default=Path("room_geometry_data.json"))
    parser.add_argument("--images", type=Path)
    parser.add_argument("--catalogue", type=Path, help="Room catalogue containing native gate annotations")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    errors = build(args.geometry, args.images or args.geometry.parent / "01-geometry",
                   args.output, Path(__file__).resolve().parent.parent, args.catalogue)
    print(f"Missing locations: {len(errors['missing_locs'])}; physical entrances: {len(errors['missing_ents'])}; "
          f"room images: {len(errors['missing_images'])}")

