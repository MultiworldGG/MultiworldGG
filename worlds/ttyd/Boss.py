import typing

from .Options import BossRandomizer

if typing.TYPE_CHECKING:
    from . import TTYDWorld


class BossEncounter:
    name: str
    rel: str
    location_id: int | None
    enemy_count: int
    enemy_ids: list[int]
    boss_type: str

    def __init__(self, name: str, rel: str, location_id: int | None, enemy_count: int,
                 enemy_ids: list[str], boss_type: str):
        self.name = name
        self.rel = rel
        self.location_id = location_id
        self.enemy_count = enemy_count
        self.enemy_ids = [int(_id, 0) for _id in enemy_ids]
        self.boss_type = boss_type


def parse_json_bosses() -> list[BossEncounter]:
    import json
    import pkgutil

    return (json.loads(pkgutil.get_data(__name__, "json/bosses.json").decode("utf-8"),
                       object_hook=lambda d: BossEncounter(**d)))


def randomize_bosses(world: "TTYDWorld") -> None:
    option = world.options.boss_randomizer.value

    if option == BossRandomizer.option_vanilla:
        return
    elif option == BossRandomizer.option_chapter_bosses:
        pool = [b for b in world.bosses if b.boss_type == "chapter"]
    elif option == BossRandomizer.option_mini_bosses:
        pool = [b for b in world.bosses if b.boss_type == "mini"]
    elif option == BossRandomizer.option_full:
        pool = list(world.bosses)
    else:
        raise ValueError(f"Invalid boss randomizer option: {option}")

    if world.options.disable_intermissions:
        pool = [b for b in pool if b.name != "btlgrp_muj_muj_kanbu"]

    # Whole-group shuffle only: move each group's loadout intact, matching by size.
    groups = [b.enemy_ids[:] for b in pool]
    world.random.shuffle(groups)

    for boss in pool:
        idx = next((n for n, g in enumerate(groups) if len(g) == boss.enemy_count), None)
        if idx is None:
            sizes = sorted({len(g) for g in groups})
            raise ValueError(
                f"No boss group of size {boss.enemy_count} available for {boss.name} "
                f"(rel={boss.rel}). Available sizes: {sizes}"
            )
        boss.enemy_ids = groups.pop(idx)
