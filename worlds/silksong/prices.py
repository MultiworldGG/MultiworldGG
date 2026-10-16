from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable


ROSARIES = "rosaries"
SHELL_SHARDS = "shell_shards"

NORMAL_SHOPS = "normal_shops"
BELLWAYS = "bellways"
MAPS = "maps"
PINS = "pins"
UPGRADES = "upgrades"
DONATIONS = "donations"
VOG_HINTS = "vog_hints"
VENTRICAS = "ventricas"
BENCHES = "benches"
MISCELLANEOUS = "miscellaneous"

SHELL_SHARD_BASE_CAPACITY = 400
SHELL_SHARD_CAPACITY_PER_TOOL_POUCH = 100
SHELL_SHARD_MAX_TOOL_POUCH_UPGRADES = 4

PRICE_CATEGORY_OPTION_NAMES: dict[str, str] = {
    NORMAL_SHOPS: "normal_shop_prices",
    BELLWAYS: "bellway_prices",
    MAPS: "map_prices",
    PINS: "pin_prices",
    UPGRADES: "upgrade_prices",
    DONATIONS: "donation_prices",
    VOG_HINTS: "vog_hint_prices",
    VENTRICAS: "ventrica_prices",
    BENCHES: "bench_prices",
    MISCELLANEOUS: "miscellaneous_prices",
}

PRICE_MODE_KEYS = frozenset(
    {"vanilla", "free", "shuffle", "cheap", "expensive"}
)


@dataclass(frozen=True)
class PriceSource:
    key: str
    category: str
    currency: str
    vanilla_price: int


# ShopItem.get_Cost supplies the displayed price, affordability test and
# payment. This manifest separates maps from Shakra's permanent map pins
# because the game presents them as distinct purchase families.
_SHOP_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('shop:Ant Merchant Curve Claws Tool', NORMAL_SHOPS, ROSARIES, 140),
    PriceSource('shop:Ant Merchant Fractured Mask Tool', NORMAL_SHOPS, ROSARIES, 260),
    PriceSource('shop:Ant Merchant Shard Pouch', NORMAL_SHOPS, ROSARIES, 100),
    PriceSource('shop:Architect Brolly Spike', NORMAL_SHOPS, ROSARIES, 230),
    PriceSource('shop:Architect Cogwork Saw', NORMAL_SHOPS, ROSARIES, 360),
    PriceSource('shop:Architect Key', NORMAL_SHOPS, ROSARIES, 110),
    PriceSource('shop:Architect Scuttlebrace', NORMAL_SHOPS, ROSARIES, 140),
    PriceSource('shop:Architect Shard Pouch', NORMAL_SHOPS, ROSARIES, 100),
    PriceSource('shop:Architect SilkShot', NORMAL_SHOPS, ROSARIES, 130),
    PriceSource('shop:Architect Tool Kit', NORMAL_SHOPS, ROSARIES, 450),
    PriceSource('shop:Bellhart Crest Socket', NORMAL_SHOPS, ROSARIES, 330),
    PriceSource('shop:Bellhart Furnishing Desk', NORMAL_SHOPS, ROSARIES, 380),
    PriceSource('shop:Bellhart Furnishing Gramaphone', NORMAL_SHOPS, ROSARIES, 490),
    PriceSource('shop:Bellhart Furnishing Lights', NORMAL_SHOPS, ROSARIES, 320),
    PriceSource('shop:Bellhart Furnishing Paint', NORMAL_SHOPS, ROSARIES, 520),
    PriceSource('shop:Bellhart Furnishing Spa', NORMAL_SHOPS, ROSARIES, 1100),
    PriceSource('shop:Bellhart Multibind', NORMAL_SHOPS, ROSARIES, 120),
    PriceSource('shop:Belltown Rosary String Medium', NORMAL_SHOPS, ROSARIES, 50),
    PriceSource('shop:Belltown Shard Pouch', NORMAL_SHOPS, ROSARIES, 100),
    PriceSource('shop:Belltown Spool Segment', NORMAL_SHOPS, ROSARIES, 270),
    PriceSource('shop:Belltown Tool Pouch', NORMAL_SHOPS, ROSARIES, 250),
    PriceSource('shop:Bonebottom Faith Token', NORMAL_SHOPS, ROSARIES, 500),
    PriceSource('shop:Bonebottom Mask Shard', NORMAL_SHOPS, ROSARIES, 300),
    PriceSource('shop:Bonebottom Rosary Magnet Tool', NORMAL_SHOPS, ROSARIES, 120),
    PriceSource('shop:Bonebottom Rosary Set', NORMAL_SHOPS, ROSARIES, 100),
    PriceSource('shop:Bonebottom Tool Metal', NORMAL_SHOPS, ROSARIES, 60),
    PriceSource('shop:City Merchant Heart Piece', NORMAL_SHOPS, ROSARIES, 750),
    PriceSource('shop:City Merchant Needolin Tool', NORMAL_SHOPS, ROSARIES, 320),
    PriceSource('shop:City Merchant Rosary String', NORMAL_SHOPS, ROSARIES, 50),
    PriceSource('shop:City Merchant Seal Chit', NORMAL_SHOPS, ROSARIES, 180),
    PriceSource('shop:City Merchant Simple Key', NORMAL_SHOPS, ROSARIES, 650),
    PriceSource('shop:City Merchant Spool Extender', NORMAL_SHOPS, ROSARIES, 720),
    PriceSource('shop:City Merchant Spool Piece', NORMAL_SHOPS, ROSARIES, 500),
    PriceSource('shop:City Merchant Tool Metal', NORMAL_SHOPS, ROSARIES, 180),
    PriceSource('shop:City Merchant Wallcling Tool', NORMAL_SHOPS, ROSARIES, 350),
    PriceSource('shop:City Merchant Ward Key', NORMAL_SHOPS, ROSARIES, 220),
    PriceSource('shop:Forge Lava Charm Tool', NORMAL_SHOPS, ROSARIES, 110),
    PriceSource('shop:Forge Shard Pouch', NORMAL_SHOPS, ROSARIES, 100),
    PriceSource('shop:Forge SilkShot', NORMAL_SHOPS, ROSARIES, 240),
    PriceSource('shop:Forge Sting Shard Tool', NORMAL_SHOPS, ROSARIES, 140),
    PriceSource('shop:Forge Tacks Tool', NORMAL_SHOPS, ROSARIES, 90),
    PriceSource('shop:Forge Tool Kit', NORMAL_SHOPS, ROSARIES, 180),
    PriceSource('shop:Grindle Crest Socket', NORMAL_SHOPS, ROSARIES, 250),
    PriceSource('shop:Grindle Lucky Dice Tool', NORMAL_SHOPS, ROSARIES, 300),
    PriceSource('shop:Grindle Mask Shard', NORMAL_SHOPS, ROSARIES, 320),
    PriceSource('shop:Grindle Psalm Cylinder', NORMAL_SHOPS, ROSARIES, 240),
    PriceSource('shop:Grindle Reserve Bind', NORMAL_SHOPS, ROSARIES, 800),
    PriceSource('shop:Grindle Rosary Magnet', NORMAL_SHOPS, ROSARIES, 220),
    PriceSource('shop:Grindle Rosary String', NORMAL_SHOPS, ROSARIES, 50),
    PriceSource('shop:Grindle Simple Key', NORMAL_SHOPS, ROSARIES, 600),
    PriceSource('shop:Grindle Spool Piece', NORMAL_SHOPS, ROSARIES, 680),
    PriceSource('shop:Grindle Thief Charm', NORMAL_SHOPS, ROSARIES, 350),
    PriceSource('shop:Grindle Thief Claw', NORMAL_SHOPS, ROSARIES, 740),
    PriceSource('shop:Grindle Tool Kit', NORMAL_SHOPS, ROSARIES, 700),
    PriceSource('shop:Grindle Tool Metal', NORMAL_SHOPS, ROSARIES, 120),
    PriceSource('shop:Grindle Tool Pouch', NORMAL_SHOPS, ROSARIES, 220),
    PriceSource('shop:Mapper Bellhart Map', MAPS, ROSARIES, 40),
    PriceSource('shop:Mapper Bellway Map Pin', PINS, ROSARIES, 60),
    PriceSource('shop:Mapper Bench Map Pin', PINS, ROSARIES, 60),
    PriceSource('shop:Mapper Boneforest Map', MAPS, ROSARIES, 50),
    PriceSource('shop:Mapper Compass Tool', NORMAL_SHOPS, ROSARIES, 70),
    PriceSource('shop:Mapper Coral Caverns Map', MAPS, ROSARIES, 90),
    PriceSource('shop:Mapper Crawl Map', MAPS, ROSARIES, 70),
    PriceSource('shop:Mapper Docks Map', MAPS, ROSARIES, 50),
    PriceSource('shop:Mapper Dustpens Map', MAPS, ROSARIES, 90),
    PriceSource('shop:Mapper Greymoor Map', MAPS, ROSARIES, 70),
    PriceSource('shop:Mapper Hunters Nest Map', MAPS, ROSARIES, 70),
    PriceSource('shop:Mapper JudgeSteps Map', MAPS, ROSARIES, 70),
    PriceSource('shop:Mapper Map Marker A', NORMAL_SHOPS, ROSARIES, 40),
    PriceSource('shop:Mapper Map Marker B', NORMAL_SHOPS, ROSARIES, 40),
    PriceSource('shop:Mapper Map Marker C', NORMAL_SHOPS, ROSARIES, 60),
    PriceSource('shop:Mapper Map Marker D', NORMAL_SHOPS, ROSARIES, 90),
    PriceSource('shop:Mapper Map Marker E', NORMAL_SHOPS, ROSARIES, 120),
    PriceSource('shop:Mapper Moss Grotto Map', MAPS, ROSARIES, 40),
    PriceSource('shop:Mapper Peak Map', MAPS, ROSARIES, 40),
    PriceSource('shop:Mapper Quill', NORMAL_SHOPS, ROSARIES, 50),
    PriceSource('shop:Mapper Shadow Map', MAPS, ROSARIES, 90),
    PriceSource('shop:Mapper Shellwood Map', MAPS, ROSARIES, 70),
    PriceSource('shop:Mapper Shop Map Pin', PINS, ROSARIES, 80),
    PriceSource('shop:Mapper Tube Map Pin', PINS, ROSARIES, 80),
    PriceSource('shop:Mapper Wilds Map', MAPS, ROSARIES, 50),
    PriceSource('shop:Pilgrims Rest Crest Socket Unlocker', NORMAL_SHOPS, ROSARIES, 150),
    PriceSource('shop:Pilgrims Rest Rosary String Small', NORMAL_SHOPS, ROSARIES, 50),
    PriceSource('shop:Pilgrims Rest Shard Pouch', NORMAL_SHOPS, ROSARIES, 100),
    PriceSource('shop:Pilgrims Rest Tool Pouch', NORMAL_SHOPS, ROSARIES, 220),
    PriceSource('shop:Pilgrims Rest Weighted Anklet Tool', NORMAL_SHOPS, ROSARIES, 160),
)


# ShopItem.IsAvailableNotInfinite identifies finite stock
# by a player-data bool or a SavedItem whose native IsUnique is true. These are
# the assets that have neither and therefore remain repeatable.
# They must not contribute prices to shuffled pools either.
INFINITE_SHOP_PRICE_KEYS = frozenset(
    {
        "shop:Ant Merchant Shard Pouch",
        "shop:Architect Shard Pouch",
        "shop:Bellhart Furnishing Paint",
        "shop:Belltown Rosary String Medium",
        "shop:Belltown Shard Pouch",
        "shop:Bonebottom Rosary Set",
        "shop:City Merchant Rosary String",
        "shop:Forge Shard Pouch",
        "shop:Grindle Rosary String",
        "shop:Pilgrims Rest Rosary String Small",
        "shop:Pilgrims Rest Shard Pouch",
    }
)

SHOP_PRICE_SOURCES: tuple[PriceSource, ...] = tuple(
    source
    for source in _SHOP_PRICE_SOURCES
    if source.key not in INFINITE_SHOP_PRICE_KEYS
)


# Bellway keys identify physical toll booths. The two Grand Gate booths share
# one station flag but have different prices, so they remain distinct
# sources and whichever one is bought first unlocks the station normally.
BELLWAY_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('bellway:Bellway_02:Bellway Toll Machine:UnlockedDocksStation', BELLWAYS, ROSARIES, 40),
    PriceSource('bellway:Bellway_03:Bellway Toll Machine:UnlockedBoneforestEastStation', BELLWAYS, ROSARIES, 40),
    PriceSource('bellway:Bellway_04:Bellway Toll Machine:UnlockedGreymoorStation', BELLWAYS, ROSARIES, 60),
    PriceSource('bellway:Belltown_basement:Bellway Toll Machine:UnlockedBelltownStation', BELLWAYS, ROSARIES, 60),
    PriceSource('bellway:Bellway_08:Bellway Toll Machine:UnlockedCoralTowerStation', BELLWAYS, ROSARIES, 60),
    PriceSource('bellway:Bellway_City:Bellway Toll Machine:UnlockedCityStation', BELLWAYS, ROSARIES, 80),
    PriceSource('bellway:Bellway_City:Bellway Toll Machine (1):UnlockedCityStation', BELLWAYS, ROSARIES, 40),
    PriceSource('bellway:Slab_06:Bellway Toll Machine:UnlockedPeakStation', BELLWAYS, ROSARIES, 40),
    PriceSource('bellway:Shellwood_19:Bellway Toll Machine:UnlockedShellwoodStation', BELLWAYS, ROSARIES, 40),
    PriceSource('bellway:Bellway_Shadow:Bellway Toll Machine:UnlockedShadowStation', BELLWAYS, ROSARIES, 80),
    PriceSource('bellway:Bellway_Aqueduct:Bellway Toll Machine:UnlockedAqueductStation', BELLWAYS, ROSARIES, 80),
)


# Plinney's first two services are already free/item-gated. These are the two
# services for which the Dialogue FSM reads a Rosary CostReference.
UPGRADE_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('upgrade:plinney:3', UPGRADES, ROSARIES, 450),
    PriceSource('upgrade:plinney:4', UPGRADES, ROSARIES, 680),
)


DONATION_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('donation:Belltown House Start', DONATIONS, ROSARIES, 250),
    PriceSource('donation:Belltown House Mid', DONATIONS, ROSARIES, 400),
    PriceSource('donation:Songclave Donation 1', DONATIONS, ROSARIES, 300),
    PriceSource('donation:Songclave Donation 2', DONATIONS, ROSARIES, 500),
    PriceSource('donation:Building Materials', DONATIONS, SHELL_SHARDS, 200),
    PriceSource('donation:Building Materials (Bridge)', DONATIONS, SHELL_SHARDS, 300),
    PriceSource('donation:Building Materials (Statue)', DONATIONS, SHELL_SHARDS, 440),
)


VOG_HINT_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('vog:area', VOG_HINTS, ROSARIES, 120),
)


VENTRICA_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('ventrica:arborium_tube:tube_toll_machine', VENTRICAS, ROSARIES, 80),
    PriceSource('ventrica:bellway_city:tube_toll_machine', VENTRICAS, ROSARIES, 80),
    PriceSource('ventrica:hang_06b:tube_toll_machine', VENTRICAS, ROSARIES, 80),
    PriceSource('ventrica:song_01b:tube_toll_machine', VENTRICAS, ROSARIES, 80),
    PriceSource('ventrica:song_enclave_tube:tube_toll_machine', VENTRICAS, ROSARIES, 80),
    PriceSource('ventrica:tube_hub:tube_toll_machine', VENTRICAS, ROSARIES, 80),
    PriceSource('ventrica:under_22:tube_toll_machine', VENTRICAS, ROSARIES, 80),
)


BENCH_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('bench:bellway_03:bell_toll_machine', BENCHES, ROSARIES, 30),
    PriceSource('bench:bellway_08:bell_toll_machine', BENCHES, ROSARIES, 40),
    PriceSource('bench:bellway_aqueduct:bell_toll_machine', BENCHES, ROSARIES, 60),
    PriceSource('bench:bellway_peak:bell_toll_machine', BENCHES, ROSARIES, 60),
    PriceSource('bench:bellway_shadow:bell_toll_machine', BENCHES, ROSARIES, 60),
    PriceSource('bench:bone_01c:bell_toll_machine', BENCHES, ROSARIES, 30),
    PriceSource('bench:bone_east_15:bell_toll_machine', BENCHES, ROSARIES, 30),
    PriceSource('bench:coral_02:bell_toll_machine', BENCHES, ROSARIES, 60),
    PriceSource('bench:dock_01:bell_toll_machine', BENCHES, ROSARIES, 30),
    PriceSource('bench:dust_10:bell_toll_machine', BENCHES, ROSARIES, 40),
    PriceSource('bench:shellwood_01b:bell_toll_machine', BENCHES, ROSARIES, 40),
    PriceSource('bench:shellwood_08c:bell_toll_machine', BENCHES, ROSARIES, 40),
    PriceSource('bench:under_01b:Understore Toll Bench (1)', BENCHES, ROSARIES, 15),
    PriceSource('bench:under_01b:Understore Toll Bench', BENCHES, ROSARIES, 15),
    PriceSource('bench:under_08:Understore Toll Bench (2)', BENCHES, ROSARIES, 15),
    PriceSource('bench:under_08:Understore Toll Bench', BENCHES, ROSARIES, 15),
    PriceSource('bench:under_08:Understore Toll Bench (1)', BENCHES, ROSARIES, 15),
)


MAP_MACHINE_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('map-machine:arborium_11:Map Machine', MAPS, ROSARIES, 70),
    PriceSource('map-machine:bellway_city:Map Machine', MAPS, ROSARIES, 70),
    PriceSource('map-machine:cradle_02:Map Machine (1)', MAPS, ROSARIES, 70),
    PriceSource('map-machine:hang_06b:Map Machine', MAPS, ROSARIES, 70),
    PriceSource('map-machine:library_04:Map Machine (1)', MAPS, ROSARIES, 70),
    PriceSource('map-machine:song_01b:Map Machine (2)', MAPS, ROSARIES, 70),
    PriceSource('map-machine:song_19_entrance:Map Machine (1)', MAPS, ROSARIES, 40),
    PriceSource('map-machine:ward_01:Map Machine (1)', MAPS, ROSARIES, 70),
)


MISCELLANEOUS_PRICE_SOURCES: tuple[PriceSource, ...] = (
    PriceSource('misc:bone_east_10:toll door interactible', MISCELLANEOUS, ROSARIES, 30),
    PriceSource('misc:pin-gallery', MISCELLANEOUS, ROSARIES, 25),
)


PRICE_SOURCES: tuple[PriceSource, ...] = (
    SHOP_PRICE_SOURCES
    + BELLWAY_PRICE_SOURCES
    + UPGRADE_PRICE_SOURCES
    + DONATION_PRICE_SOURCES
    + VOG_HINT_PRICE_SOURCES
    + VENTRICA_PRICE_SOURCES
    + BENCH_PRICE_SOURCES
    + MAP_MACHINE_PRICE_SOURCES
    + MISCELLANEOUS_PRICE_SOURCES
)

PRICE_SOURCE_BY_KEY: dict[str, PriceSource] = {
    source.key: source for source in PRICE_SOURCES
}

SHELL_SHARD_DONATION_LOCATION_BY_PRICE_KEY: dict[str, str] = {
    'donation:Building Materials': 'Wish: Bone Bottom Repairs',
    'donation:Building Materials (Bridge)': 'Wish: A Lifesaving Bridge',
    'donation:Building Materials (Statue)': 'Wish: An Icon of Hope',
}

if len(PRICE_SOURCE_BY_KEY) != len(PRICE_SOURCES):
    raise ValueError("Duplicate purchase-price source key")


def get_required_tool_pouch_count_for_shell_shard_price(
    price: int,
) -> int:
    if price < 0:
        raise ValueError("Shell Shard prices cannot be negative")
    required_count = max(
        0,
        (
            price
            - SHELL_SHARD_BASE_CAPACITY
            + SHELL_SHARD_CAPACITY_PER_TOOL_POUCH
            - 1
        ) // SHELL_SHARD_CAPACITY_PER_TOOL_POUCH,
    )
    if required_count > SHELL_SHARD_MAX_TOOL_POUCH_UPGRADES:
        maximum_capacity = (
            SHELL_SHARD_BASE_CAPACITY
            + SHELL_SHARD_CAPACITY_PER_TOOL_POUCH
            * SHELL_SHARD_MAX_TOOL_POUCH_UPGRADES
        )
        raise ValueError(
            f"Shell Shard price {price} exceeds the maximum capacity "
            f"of {maximum_capacity}."
        )
    return required_count


def get_shell_shard_donation_tool_pouch_requirements(
    purchase_prices: dict[str, int],
) -> dict[str, int]:
    return {
        location_name: get_required_tool_pouch_count_for_shell_shard_price(
            purchase_prices.get(
                price_key,
                PRICE_SOURCE_BY_KEY[price_key].vanilla_price,
            )
        )
        for price_key, location_name
        in SHELL_SHARD_DONATION_LOCATION_BY_PRICE_KEY.items()
    }


def _resolve_group(
    random: Random,
    sources: Iterable[PriceSource],
    mode: str,
    max_shell_shards: int,
) -> dict[str, int]:
    ordered_sources = sorted(sources, key=lambda source: source.key)
    if mode == "vanilla":
        return {
            source.key: source.vanilla_price
            for source in ordered_sources
        }
    if mode == "free":
        return {source.key: 0 for source in ordered_sources}
    if mode == "cheap":
        return {
            source.key: random.randint(1, 100)
            for source in ordered_sources
        }
    if mode == "expensive":
        return {
            source.key: random.randint(
                1,
                max_shell_shards if source.currency == SHELL_SHARDS else 500,
            )
            for source in ordered_sources
        }
    if mode != "shuffle":
        raise ValueError(f"Unknown purchase-price mode: {mode!r}")

    result: dict[str, int] = {}
    for currency in (ROSARIES, SHELL_SHARDS):
        currency_sources = [
            source
            for source in ordered_sources
            if source.currency == currency
        ]
        prices = [source.vanilla_price for source in currency_sources]
        random.shuffle(prices)
        result.update(
            {
                source.key: price
                for source, price in zip(currency_sources, prices)
            }
        )
    return result


def resolve_purchase_prices(
    random: Random,
    category_modes: dict[str, str],
    tool_pouch_count: int = SHELL_SHARD_MAX_TOOL_POUCH_UPGRADES,
) -> dict[str, int]:
    if not 0 <= tool_pouch_count <= SHELL_SHARD_MAX_TOOL_POUCH_UPGRADES:
        raise ValueError(f"Invalid Tool Pouch count: {tool_pouch_count!r}")
    max_shell_shards = SHELL_SHARD_BASE_CAPACITY + tool_pouch_count * SHELL_SHARD_CAPACITY_PER_TOOL_POUCH
    unknown_categories = set(category_modes).difference(
        PRICE_CATEGORY_OPTION_NAMES
    )
    if unknown_categories:
        raise ValueError(
            "Unknown purchase-price categories: "
            + ", ".join(sorted(unknown_categories))
        )

    result: dict[str, int] = {}
    for category in PRICE_CATEGORY_OPTION_NAMES:
        mode = category_modes.get(category, "vanilla")
        if mode not in PRICE_MODE_KEYS:
            raise ValueError(
                f"Unknown {category} purchase-price mode: {mode!r}"
            )
        result.update(
            _resolve_group(
                random,
                (
                    source
                    for source in PRICE_SOURCES
                    if source.category == category
                ),
                mode,
                max_shell_shards,
            )
        )

    if set(result) != set(PRICE_SOURCE_BY_KEY):
        raise ValueError("Purchase-price resolution missed a source")
    return result
