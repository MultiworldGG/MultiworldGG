from __future__ import annotations

from copy import deepcopy

from .requirements import REQUIREMENTS

VOG_HINT_ROOM_AREA_NAMES: dict[str, str] = {
    "bone-bottom": "Mosslands",
    "the-marrow": "The Marrow",
    "weavenest-atla": "Weavenest",
    "wormways": "Wormways",
    "deep-docks": "Deep Docks",
    "shellwood": "Shellwood",
    "bellhart": "Bellhart",
    "far-fields": "Far Fields",
    "hunter-s-march": "Hunter's March",
    "cogwork-core": "Cogwork Core",
    "choral-chambers": "Choral Chambers",
    "grand-gate": "Grand Gate",
    "greymoor": "Greymoor",
    "moss-grotto": "Mosslands",
    "sinner-s-road": "Sinner's Road",
    "underworks": "Underworks",
    "whisp-thicket": "Greymoor",
    "blasted-steps": "Blasted Steps",
    "the-mist": "The Mist",
    "whispering-vaults": "Whispering Vaults",
    "high-halls": "High Halls",
    "whiteward": "Whiteward",
    "white-ward": "Whiteward",
    "bilewater": "Bilewater",
    "sands-of-karak": "Sands of Karak",
    "the-slab": "The Slab",
    "mount-fay": "Mount Fay",
    "memorium": "Memorium",
    "putrified-ducts": "Putrified Ducts",
    "the-cradle": "The Cradle",
    "the-abyss": "The Abyss",
    "verdania": "Verdania",
}

VOG_HINT_PATH_AREA_NAMES: dict[str, str] = {
    "Outlying Citadel - Lower Cogwork Core": "Cogwork Core",
    "Outlying Citadel - Cogwork Core": "Cogwork Core",
    "Outlying Citadel - High Halls Ventrica": "High Halls",
    "Outlying Citadel - Memorium": "Memorium",
    "Outlying Citadel - Library": "Whispering Vaults",
}

# Folder names usually match Vog's hint areas. The Choral Chambers folder also
# holds Grand Bellway and Songclave rooms, so those rooms need their own entries.
VOG_HINT_ROOM_ID_AREA_NAMES: dict[str, str] = {
    "choral-chambers/choral-chambers-below-ventrica": "Choral Chambers",
    "choral-chambers/choral-chambers-flea-room": "Choral Chambers",
    "choral-chambers/choral-chambers-flea-shaft": "Choral Chambers",
    "choral-chambers/choral-chambers-maintenance-tunnel": "Choral Chambers",
    "choral-chambers/choral-chambers-merchant-room": "Choral Chambers",
    "choral-chambers/choral-chambers-outside-spa": "Choral Chambers",
    "choral-chambers/choral-chambers-over-dininig": "Choral Chambers",
    "choral-chambers/choral-chambers-ventrica-room": "Choral Chambers",
    "choral-chambers/grand-bellway": "Choral Chambers",
    "choral-chambers/grand-bellway-side-room": "Choral Chambers",
    "choral-chambers/songclave": "Choral Chambers",
    "choral-chambers/songclave-tube": "Choral Chambers",
}

VOG_HINT_SHAKRA_AREAS = frozenset(
    (
        "Mosslands",
        "The Marrow",
        "Deep Docks",
        "Far Fields",
        "Wormways",
        "Hunter's March",
        "Greymoor",
        "Bellhart",
        "Shellwood",
        "Blasted Steps",
        "Sinner's Road",
        "Mount Fay",
        "Sands of Karak",
        "Bilewater",
    )
)

VOG_HINT_AREA_OVERRIDES: dict[str, frozenset[str]] = {
    "Throwing Ring": frozenset(("Bilewater",)),
    "Egg of Flealia": frozenset(("Putrified Ducts",)),
    "Bellhart - Bellshrine": frozenset(("Bellhart",)),
    "Boss: Bell Beast": frozenset(("The Marrow",)),
    "Boss: Last Judge": frozenset(("Grand Gate",)),
    "Relic: Weaver Effigy (Keelal, Shellwood)":
        frozenset(("Shellwood",)),
    "Boss: Crawfather": frozenset(("Greymoor",)),
    "Boss: Broodmother": frozenset(("The Slab",)),
    "Boss: Second Sentinel": frozenset(("High Halls",)),
    "Boss: Palestag": frozenset(("Verdania",)),
    "Boss: Clover Dancers": frozenset(("Verdania",)),
    "Wish: Queen's Egg": frozenset(("Sinner's Road",)),
    "Wish: Fine Pins": frozenset(("Songclave",)),
    "Wish: The Wandering Merchant":
        frozenset(("Choral Chambers",)),
    "Wish: My Missing Brother": frozenset(("Sinner's Road",)),
    "Wish: Balm for the Wounded": frozenset(("Whiteward",)),
    "Wish: Cloaks of the Choir": frozenset(("Songclave",)),
    "Wish: Building Up Songclave": frozenset(("Songclave",)),
    "Wish: Strengthening Songclave": frozenset(("Songclave",)),
    "Craw Summons": frozenset(("Greymoor",)),
    "Craggler - Beast Shard": frozenset(("Wormways",)),
    "Boss: Gurr the Outcast": frozenset(("Far Fields",)),
    "Boss: Raging Conchfly": frozenset(("Sands of Karak",)),
    "Pin Purchase: Bellway Pins": VOG_HINT_SHAKRA_AREAS,
    "Pin Purchase: Vendor Pins": VOG_HINT_SHAKRA_AREAS,
    **{
        location_name: frozenset(("Bellhart", "Shellwood"))
        for location_name in (
            "Pinmaster Plinney: Sharpened Needle",
            "Pinmaster Plinney: Shining Needle",
            "Pinmaster Plinney: Hivesteel Needle",
            "Pinmaster Plinney: Pale Steel Needle",
        )
    },
}

VOG_HINT_AREALESS_LOCATIONS = frozenset(
    {
        "Crest: Hunter",
        "Goal",
        "Beastling Call",
        *(
            f"Crest Slot: {crest} ({color} {slot})"
            for crest, color, slot in (
                ("Hunter", "Red", 1),
                ("Hunter", "Blue", 1),
                ("Hunter", "Yellow", 1),
                ("Reaper", "Red", 1),
                ("Reaper", "Blue", 1),
                ("Reaper", "Yellow", 1),
                ("Wanderer", "Blue", 1),
                ("Wanderer", "Blue", 2),
                ("Wanderer", "Yellow", 1),
                ("Beast", "Yellow", 1),
                ("Beast", "Yellow", 2),
                ("Witch", "Red", 1),
                ("Witch", "Blue", 1),
                ("Witch", "Blue", 2),
                ("Architect", "Blue", 1),
                ("Architect", "Yellow", 1),
                ("Architect", "Yellow", 2),
                ("Architect", "Blue", 2),
                ("Shaman", "Blue", 1),
                ("Shaman", "Blue", 2),
            )
        ),
    }
)

def empty_vog_hint_plan() -> dict[str, object]:
    return {
        "format": "area_counts_v1",
        "area_count": 0,
        "area_locations": {},
    }


def copy_vog_hint_plan(plan: dict[str, object]) -> dict[str, object]:
    return deepcopy(plan)


def get_vog_hint_areas(location_name: str) -> frozenset[str]:
    override_areas = VOG_HINT_AREA_OVERRIDES.get(location_name)
    if override_areas is not None:
        return override_areas

    areas: set[str] = set()
    for requirement in REQUIREMENTS.get(location_name, ()):
        path_name = requirement.path_name.strip()
        if path_name:
            area_name = VOG_HINT_PATH_AREA_NAMES.get(path_name)
            if area_name is None:
                area_name = path_name.split(" - ", 1)[0].strip()
            if area_name:
                areas.add(area_name)

        for dependency in (*requirement.all_of, *requirement.any_of):
            if not dependency.startswith("Room Node: "):
                continue
            room_id = dependency.removeprefix("Room Node: ").split(
                "#",
                1,
            )[0]
            area_name = VOG_HINT_ROOM_ID_AREA_NAMES.get(room_id)
            area_id = room_id.split(
                "/",
                1,
            )[0]
            if area_name is None:
                area_name = VOG_HINT_ROOM_AREA_NAMES.get(area_id)
            if area_name:
                areas.add(area_name)

    return frozenset(areas)


def build_vog_hint_plan(world) -> dict[str, object]:
    plan = empty_vog_hint_plan()
    count = world.get_vog_area_hint_count()
    if not count:
        return plan
    area_locations: dict[str, list[str]] = {}
    for location in world.multiworld.get_locations(world.player):
        if location.address is None or location.name in VOG_HINT_AREALESS_LOCATIONS:
            continue
        areas = get_vog_hint_areas(location.name)
        for area in areas:
            area_locations.setdefault(area, []).append(location.name)
    plan["area_locations"] = {
        area: sorted(set(locations))
        for area, locations in sorted(area_locations.items())
    }
    plan["area_count"] = min(count, len(area_locations))
    return plan
