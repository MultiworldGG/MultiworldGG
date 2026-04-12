import typing
from collections import defaultdict

from .Options import EnemyRandomizer

if typing.TYPE_CHECKING:
    from . import TTYDWorld


class Encounter:
    name: str
    rel: str
    location_id: int | None
    enemy_count: int
    enemy_ids: list[int]

    def __init__(self, name: str, rel: str, location_id: int | None, enemy_count: int, enemy_ids: list[str]):
        self.name = name
        self.rel = rel
        self.location_id = location_id
        self.enemy_count = enemy_count
        self.enemy_ids = [int(_id, 0) for _id in enemy_ids]

def parse_json_encounters() -> list[Encounter]:
    import json
    import pkgutil

    return (json.loads(pkgutil.get_data(__name__, "json/enemies.json").decode("utf-8"),
                       object_hook=lambda d: Encounter(**d)))

def randomize_encounters(world: "TTYDWorld") -> None:
    encounter_shuffle_type = world.options.encounter_shuffle_type.value

    # rel -> list[list[enemy_id]]
    rel_groups: dict[str, list[list[int]]] = defaultdict(list)

    if world.options.enemy_randomizer == EnemyRandomizer.option_within_chapter:
        # Build buckets from existing encounters
        by_rel = defaultdict(list)
        for enc in world.encounters:
            by_rel[enc.rel].append(enc)

        for rel, encs in by_rel.items():
            if encounter_shuffle_type == 0:
                # shuffle whole groups (keeping compositions)
                groups = [e.enemy_ids[:] for e in encs]
                world.random.shuffle(groups)
            elif encounter_shuffle_type == 1:
                # shuffle individuals within the chapter/rel then repartition by each encounter's size
                enemies = [_id for e in encs for _id in e.enemy_ids]
                world.random.shuffle(enemies)
                groups = [[enemies.pop() for _ in range(e.enemy_count)] for e in encs]
                world.random.shuffle(groups)
            else:
                raise ValueError(f"Invalid encounter_shuffle_type: {encounter_shuffle_type}")

            rel_groups[rel] = groups

    elif world.options.enemy_randomizer == EnemyRandomizer.option_randomize:
        # Single global bucket; store under a sentinel key
        rel = "__ALL__"

        if encounter_shuffle_type == 0:
            groups = [e.enemy_ids[:] for e in world.encounters]
            world.random.shuffle(groups)
        elif encounter_shuffle_type == 1:
            enemies = [_id for e in world.encounters for _id in e.enemy_ids]
            world.random.shuffle(enemies)
            groups = [[enemies.pop() for _ in range(e.enemy_count)] for e in world.encounters]
            world.random.shuffle(groups)
        else:
            raise ValueError(f"Invalid encounter_shuffle_type: {encounter_shuffle_type}")

        rel_groups[rel] = groups

    else:
        raise ValueError(f"Invalid enemy randomizer option: {world.options.enemy_randomizer}")

    # Assign back
    for encounter in world.encounters:
        key = encounter.rel if world.options.enemy_randomizer == EnemyRandomizer.option_within_chapter else "__ALL__"
        bucket = rel_groups[key]

        idx = next((n for n, g in enumerate(bucket) if len(g) == encounter.enemy_count), None)
        if idx is None:
            sizes = sorted({len(g) for g in bucket})
            raise ValueError(
                f"No group of size {encounter.enemy_count} available for encounter {getattr(encounter,'name',None)} "
                f"(rel={getattr(encounter,'rel',None)}). Available sizes in bucket: {sizes}"
            )

        encounter.enemy_ids = bucket.pop(idx)
