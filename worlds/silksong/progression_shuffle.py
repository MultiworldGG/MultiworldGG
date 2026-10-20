from __future__ import annotations

from dataclasses import dataclass, replace
from random import Random
from types import MappingProxyType
from typing import Callable, Mapping

from .requirements import LocationRequirement, req
from .locations import BOSS_CREDIT_BY_LOCATION, BOSS_CREDIT_LOCATIONS
from .progression_catalogue import (
    STORY_GATES as _STORY_GATES, DONATIONS as _DONATIONS,
    COLLECTIONS as _COLLECTIONS, NPC_DELIVERIES as _NPC_DELIVERIES, WISH_IDS as SUPPORTED_WISH_IDS,
)

SCHEMA = 2
DIRECT_NOTICE_OFFERS = frozenset({"Mossberry Collection Pre", "Save the Fleas Pre"})
Rules = tuple[LocationRequirement, ...]
NATIVE_WISH_FOLLOWUPS = frozenset({"Wood Witch Curse", "Doctor Curse Cure", "Extractor Blue Worms"})


def offer_event(identity: str) -> str:
    return f"Wish Offer: {identity}"


def completion_event(identity: str) -> str:
    return f"Wish Completed: {identity}"


def defeat_event(identity: str) -> str:
    return f"Boss Defeated Here: {identity}"


def credit_event(identity: str) -> str:
    return f"Boss Credit: {identity}"


@dataclass(frozen=True)
class WishContract:
    identity: str
    offer: Rules
    task: Rules
    effects: tuple[tuple[str, Rules], ...] = ()
    completion_aliases: tuple[str, ...] = ()
    locations: tuple[str, ...] = ()
    acceptance_aliases: tuple[str, ...] = ()
    reward_alternatives: Rules = ()
    requires_acceptance: bool = True
    native_acceptance: Rules = ()


@dataclass(frozen=True)
class BossContract:
    identity: str
    encounter: Rules


@dataclass(frozen=True)
class Assignments:
    wishes: tuple[tuple[str, str], ...] = ()
    bosses: tuple[str, ...] = ()

    def to_slot_data(self) -> dict[str, object]:
        return {"schema": SCHEMA, "wishes": dict(self.wishes), "bosses": list(self.bosses)}

    @classmethod
    def from_slot_data(
        cls, data: object, wish_ids: frozenset[str], boss_ids: frozenset[str]
    ) -> Assignments:
        if not isinstance(data, dict) or set(data) != {"schema", "wishes", "bosses"}:
            raise ValueError("Invalid progression shuffle data.")
        if type(data["schema"]) is not int or data["schema"] != SCHEMA:
            raise ValueError("Unsupported progression shuffle schema.")
        return cls(
            _validate_permutation(data["wishes"], wish_ids, "wish"),
            _validate_bosses(data["bosses"], boss_ids),
        )


def _validate_bosses(data, expected):
    if not isinstance(data, list) or any(type(name) is not str for name in data):
        raise ValueError("Invalid boss credit identities.")
    if len(data) != len(expected) or set(data) != expected:
        raise ValueError("Boss credits must cover each eligible boss once.")
    return tuple(sorted(data))


def _validate_permutation(data: object, expected: frozenset[str], kind: str):
    if not isinstance(data, dict) or any(
        type(source) is not str or type(target) is not str
        for source, target in data.items()
    ):
        raise ValueError(f"Invalid {kind} assignments.")
    if set(data) != expected or set(data.values()) != expected:
        raise ValueError(f"{kind.capitalize()} assignments must cover each eligible identity once.")
    return tuple(sorted(data.items()))


def _index(contracts):
    result = {}
    for contract in contracts:
        if not contract.identity or contract.identity in result:
            raise ValueError("Progression contracts need unique nonempty identities.")
        result[contract.identity] = contract
    return result


def compile_events(
    assignments: Assignments,
    wishes: tuple[WishContract, ...],
    bosses: tuple[BossContract, ...],
) -> Mapping[str, Rules]:
    wish_index = _index(wishes)
    boss_index = _index(bosses)
    validated = Assignments.from_slot_data(
        assignments.to_slot_data(), frozenset(wish_index), frozenset(boss_index)
    )
    if validated != assignments:
        raise ValueError("Progression assignments must use canonical ordering without duplicate sources.")
    result: dict[str, Rules] = {}

    def add(name, rules):
        if name in result:
            raise ValueError(f"Duplicate progression event: {name}")
        result[name] = rules

    for source, target in assignments.wishes:
        direct = wish_index[source].native_acceptance if source in DIRECT_NOTICE_OFFERS else ()
        add(offer_event(source), (*wish_index[source].offer, *direct))
        accepted = offer_event(source)
        if wish_index[target].native_acceptance and target not in DIRECT_NOTICE_OFFERS:
            accepted = f"Wish Accepted: {target}"
            add(accepted, (req(offer_event(source), crest=False), *wish_index[target].native_acceptance))
        for alias in wish_index[target].acceptance_aliases:
            add(alias, (req(accepted, crest=False),))
        add(completion_event(target), tuple(
            replace(rule, all_of=(accepted, *rule.all_of)) if wish_index[target].requires_acceptance else rule
            for rule in wish_index[target].task
        ))
    for identity, contract in wish_index.items():
        for name in contract.completion_aliases:
            add(name, (req(completion_event(identity), crest=False),))
        for name, rules in contract.effects:
            add(name, tuple(
                replace(rule, all_of=(completion_event(identity), *rule.all_of))
                for rule in rules
            ))
    for identity in assignments.bosses:
        add(defeat_event(identity), boss_index[identity].encounter)
        add(credit_event(identity), (req(BOSS_CREDIT_BY_LOCATION[identity], crest=False),))
    return MappingProxyType(result)


def choose_assignments(
    random: Random,
    wish_ids: frozenset[str],
    boss_ids: frozenset[str],
    is_valid: Callable[[Assignments], bool],
    planned: Mapping[str, str] | None = None,
) -> Assignments:
    planned = dict(planned or {})
    if (not planned.keys() <= wish_ids or not set(planned.values()) <= wish_ids
            or len(set(planned.values())) != len(planned)):
        raise ValueError("Wish plando must use eligible offers and each wish at most once.")
    mapping = {name: name for name in sorted(wish_ids)}
    for source, target in planned.items():
        previous = next(name for name, wish in mapping.items() if wish == target)
        mapping[previous], mapping[source] = mapping[source], target
    current = Assignments(tuple(sorted(mapping.items())), tuple(sorted(boss_ids)))
    if not is_valid(current):
        if not planned:
            raise ValueError("The starting progression layout is not valid for these settings.")
        current = None
    sources = sorted(wish_ids - planned.keys())
    remaining = sorted(wish_ids - set(planned.values()))
    for _ in range(8):
        targets = list(remaining)
        random.shuffle(targets)
        candidate = Assignments(tuple(sorted((*planned.items(), *zip(sources, targets)))), tuple(sorted(boss_ids)))
        if candidate != current and is_valid(candidate):
            return candidate
    if current is None:
        from Options import OptionError
        raise OptionError("Wish plando could not produce a valid progression layout. Choose an earlier offer or change the assignments.")
    for pass_index in range(2):
        shuffled = list(sources)
        random.shuffle(shuffled)
        for first, second in zip(shuffled, shuffled[1:]):
            mapping = dict(current.wishes)
            if pass_index and mapping[first] != first and mapping[second] != second:
                continue
            mapping[first], mapping[second] = mapping[second], mapping[first]
            candidate = replace(current, wishes=tuple(sorted(mapping.items())))
            if is_valid(candidate):
                current = candidate
    return current


def planned_wishes(world, eligible):
    from Options import OptionError
    from .locations import wish_offer_display_name

    option = getattr(world.options, 'wish_plando', None)
    requested = option.value if option is not None else {}
    names = {wish_offer_display_name(name).removeprefix('Wish: ').casefold(): name for name in eligible}
    result = {}
    for offer, wish in requested.items():
        if not isinstance(offer, str) or not isinstance(wish, str):
            raise OptionError('Wish plando needs wish names on both sides of each assignment.')
        resolved = []
        for label in (offer, wish):
            identity = names.get(label.removeprefix('Wish: ').casefold())
            if identity is None:
                choices = ', '.join(sorted(wish_offer_display_name(name) for name in eligible))
                raise OptionError(f'Wish plando: {label!r} is not an available offer or wish with these settings. Available wishes: {choices or "none; enable Shuffle Wish Offers"}.')
            resolved.append(identity)
        source, target = resolved
        if source in result or target in result.values():
            raise OptionError('Wish plando must use each offer and each wish at most once.')
        result[source] = target
    return result


def donation_contracts(graph: Mapping[str, Rules], eligible_locations: frozenset[str]):
    result = []
    for identity, location, completed, task_terms in _DONATIONS:
        if location not in eligible_locations:
            continue
        alternatives = graph.get(completed)
        if not alternatives or any(not set(task_terms).issubset(rule.all_of) for rule in alternatives):
            raise ValueError(f"Donation requirements need review: {identity}")
        offers = tuple(replace(rule, all_of=tuple(
            name for name in rule.all_of if name not in task_terms
        )) for rule in alternatives)
        result.append(WishContract(identity, offers, (req(*task_terms, crest=False),),
                                   completion_aliases=(completed,), locations=(location,)))
    return tuple(result)


def board_contracts(graph: Mapping[str, Rules], eligible_locations: frozenset[str]):
    from .requirements import get_location_requirements

    wishes = list(donation_contracts(graph, eligible_locations))
    prefix = "Room Event: event:mapper/reviewed:"
    for identity, location, stem in _COLLECTIONS:
        if location not in eligible_locations:
            continue
        accepted, collected, completed = (prefix + stem + suffix for suffix in
                                          ("-accepted", "-collected", "-completed"))
        if any(not graph.get(name) for name in (accepted, collected, completed)):
            raise ValueError(f"Missing reviewed wish contract: {identity}")
        wishes.append(WishContract(identity, graph[accepted], (req(collected, crest=False),),
            completion_aliases=(completed,), locations=(location,), acceptance_aliases=(accepted,)))
    location = "Wish: Silver Bells"
    if location in eligible_locations:
        accepted = prefix + "silver-bells-accepted"
        board = "Room Node: wish-menus/bellhart-wish-wall#room"
        tasks = get_location_requirements(location)
        if not graph.get(accepted) or any(not {board, accepted}.issubset(rule.all_of) for rule in tasks):
            raise ValueError("Silver Bells requirements need review.")
        tasks = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name not in {board, accepted}))
                      for rule in tasks)
        wishes.append(WishContract("Shiny Bell Goomba", graph[accepted], tasks,
            completion_aliases=("Event: Silver Bells Completed",), locations=(location,),
            acceptance_aliases=(accepted,)))
    location = "Wish: The Terrible Tyrant"
    if location in eligible_locations:
        accepted = "Room Event: event:mapper/78b0f7da-0b97-450d-9dce-5f414eb081d8"
        completed = "Room Event: event:mapper/5c0df955-bafd-448b-a820-938f390ac925"
        board = "Room Node: wish-menus/bone-bottom-wish-wall#room"
        tasks = graph[completed]
        if any(not {board, accepted}.issubset(rule.all_of) for rule in tasks):
            raise ValueError("The Terrible Tyrant requirements need review.")
        tasks = tuple(replace(rule, all_of=tuple(name for name in rule.all_of
                      if name not in {board, accepted})) for rule in tasks)
        wishes.append(WishContract("Skull King", graph[accepted], tasks,
            completion_aliases=(completed,), locations=(location,), acceptance_aliases=(accepted,)))
    from .locations import canonicalize_location_name
    rock_locations = tuple(canonicalize_location_name(name) for name in
                           ("Wish: Volatile Flintbeetles", "Memory Locket: Volatile Flintbeetles"))
    if any(name in eligible_locations for name in rock_locations):
        accepted = "Room Event: event:mapper/7c3615cb-a431-4cd0-8047-47aaffa9e9b7"
        completed = prefix + "volatile-flintbeetles-completed"
        board = "Room Node: bone-bottom/bone-bottom-town#ground-level"
        task = graph[completed]
        if any(board not in rule.all_of for rule in task):
            raise ValueError("Volatile Flintbeetles requirements need review.")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name != board))
                     for rule in task)
        fallback = tuple(rule for rule in get_location_requirements(rock_locations[0])
                         if "Act: 3" in rule.all_of)
        wishes.append(WishContract("Rock Rollers", graph[accepted], task,
            completion_aliases=(completed, "Event: Volatile Flintbeetles Completed",
                                "Room Event: event:mapper/559e7c1d-8a73-4246-956c-2b92014d6a6a"),
            locations=rock_locations, acceptance_aliases=(accepted,), reward_alternatives=fallback))
    hunts = (
        ("Beastfly Hunt", "savage-beastfly", "8c0e8bd4-275b-4700-aaf7-47fbd85ec5ec",
         "6f5cfe78-ceda-4042-ab4f-4a3feed69d90", "bellhart",
         "Savage Beastfly - Mask Shard", ("Savage Beastfly - Mask Shard",)),
        ("Ant Trapper", "hidden-hunter", "d6a03aad-9f4d-44a8-8a9d-eeb1cfdd535a",
         "0f141fc6-4ef6-4d26-b8c4-ea8bd134bffc", "bellhart",
         "The Hidden Hunter - Mask Shard", ("The Hidden Hunter - Mask Shard",)),
        ("Broodmother Hunt", "wailing-mother", "c09a7403-e792-4754-9e9e-beb8779bbb5f",
         "0dd94f77-255c-486d-814b-dc93ec3487b8", "songclave", "Boss: Broodmother", ()),
    )
    for identity, stem, accepted_id, completed_id, board_name, scope, locations in hunts:
        if scope not in eligible_locations:
            continue
        accepted = "Room Event: event:mapper/" + accepted_id
        completed = "Room Event: event:mapper/" + completed_id
        canonical_accepted = prefix + stem + "-accepted"
        board = "Room Node: wish-menus/" + board_name + "-wish-wall#room"
        alternatives = graph[completed]
        if not graph.get(canonical_accepted) or any(board not in rule.all_of for rule in alternatives):
            raise ValueError(f"Hunt requirements need review: {identity}")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of
                     if name not in {board, accepted})) for rule in alternatives)
        wishes.append(WishContract(identity, graph[canonical_accepted], task,
            completion_aliases=(completed,), locations=locations,
            acceptance_aliases=(accepted, canonical_accepted)))
    scripted = (
        ("Save City Merchant", "Wish: The Wandering Merchant", "reviewed:wandering-merchant-accepted",
         "reviewed:wandering-merchant-completed", "5010bcbc-fb54-41bd-aa5d-d963672530da"),
        ("Save City Merchant Bridge", "Wish: The Lost Merchant", "reviewed:lost-merchant-accepted",
         "36657c01-a7ca-49db-b968-25cddb4d03fc", "3ec80e9b-7dba-40a2-a03e-27af65163fa8"),
        ("Save Sherma", "Wish: Balm for the Wounded", "1ffbf873-aff5-463f-848e-e72eead5740e",
         "1f53c165-7afb-4362-9607-d334f05dd642", None),
        ("Save Courier Short", "Wish: My Missing Courier", "d847827f-61c9-4864-a5c1-e793e8f5e5b6",
         "6f548027-ef2e-40aa-80cc-c73ae72a91a3", None),
        ("Save Courier Tall", "Wish: My Missing Brother", "reviewed:missing-brother-accepted",
         "0fcbb574-ecbe-403c-a48c-f28ddf2a99fe", "cae6ad8c-2f49-4bfb-960e-4627c7236487"),
        ("Garmond Black Threaded", "Wish: Hero's Call", "reviewed:heros-call-accepted",
         "ce4da52d-b73b-4ecf-8bed-7dbd973d9ed1", "e53e8f20-3bd0-42c4-9c99-f590480d132f"),
        ("Tormented Trobbio", "Wish: Pain, Anguish and Misery", "e3aa041c-9a5e-4339-a484-de44ae9fc762",
         "cc95561d-69cd-485b-a6e2-489866df4549", None),
    )
    event_prefix = "Room Event: event:mapper/"
    for identity, location, accepted_id, completed_id, alias_id in scripted:
        if location not in eligible_locations:
            continue
        accepted, completed = event_prefix + accepted_id, event_prefix + completed_id
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError(f"Scripted wish requirements need review: {identity}")
        aliases = (accepted,) if alias_id is None else (accepted, event_prefix + alias_id)
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name not in aliases))
                     for rule in graph[completed])
        wishes.append(WishContract(identity, graph[accepted], task,
            completion_aliases=(completed,), acceptance_aliases=aliases))
    if "Wish: Final Audience" in eligible_locations:
        accepted = event_prefix + "d885d4f4-5024-4d4b-bfa9-fe9400739e54"
        defeated = event_prefix + "ee149de1-e2ea-47b1-b0b7-4bacbc14c856"
        if not graph.get(accepted) or not graph.get(defeated):
            raise ValueError("Final Audience requirements need review.")
        wishes.append(WishContract("Song Knight", graph[accepted], (req(defeated, crest=False),),
            completion_aliases=(event_prefix + "f328e597-6706-4cb4-8e5b-d9fc1d77de13",),
            acceptance_aliases=(accepted,), requires_acceptance=False))
    if "Throwing Ring" in eligible_locations:
        accepted = event_prefix + "c376d00f-e0b5-40e2-8235-4adf83525a32"
        completed = event_prefix + "12bb5519-6e56-48c3-b0e1-5e937bcbd48a"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("Trail's End requirements need review.")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name != accepted))
                     for rule in graph[completed])
        wishes.append(WishContract("Shakra Final Quest", graph[accepted], task,
            completion_aliases=(completed, "Event: Trail's End Completed"),
            locations=("Throwing Ring",), acceptance_aliases=(accepted,)))
    staged = (
        ("Crow Feathers Pre", "Crawbug Clearing (Creige) - Crafting Kit", "6bfbd2bf-d752-4854-8c7c-e985e5002e3f",
         "reviewed:crawbug-clearing-accepted", "reviewed:crawbug-clearing-completed", True),
        ("Save the Fleas Pre", "Flea Brew", "6e848e78-c196-477b-9a86-d2ad1bb53a43",
         "5f0154a5-b85b-4b7d-b18f-8108ca7de17f", "reviewed:lost-fleas-completed", True),
        ("Mossberry Collection Pre", "Druid's Eye", "b7aa064f-7ccf-4d90-b34b-b8c5aa245862",
         "e5299e8f-a6da-40fe-a48b-beccdd59d096", "82399cd2-c16b-42ad-b615-e698dae6245d", True),
        ("Pinstress Battle Pre", "Wish: Fatal Resolve", "0e5ce913-0045-406c-a9f2-823a23b9df3a",
         "reviewed:fatal-resolve-accepted", "reviewed:pinstress-defeated", False),
        ("Flea Games Pre", "Ecstasy of the End - Pale Oil", "6d3048ed-02ef-47f5-9efe-e49f50f37e11",
         "reviewed:flea-festival-started", "2b3c2d69-7749-429d-b1df-0b1690ec4d40", True),
    )
    for identity, scope, offered_id, native_id, completed_id, alias_completion in staged:
        if scope not in eligible_locations:
            continue
        offered, native, completed = (event_prefix + name for name in (offered_id, native_id, completed_id))
        if any(not graph.get(name) for name in (offered, native, completed)):
            raise ValueError(f"Staged wish requirements need review: {identity}")
        offer = graph[offered]
        if identity == "Crow Feathers Pre":
            offer = tuple(replace(rule, all_of=tuple(
                "Room Node: wish-menus/bellhart-wish-wall#room" if name ==
                "Room Node: greymoor/greymoor-halfway-home#room" else name for name in rule.all_of))
                for rule in graph[native])
        if identity == "Flea Games Pre":
            offer = (req("Room Node: wish-menus/bellhart-wish-wall#room", native,
                         "Ancestral Art: Silk Soar", crest=False),)
        wishes.append(WishContract(identity, offer, graph[completed],
            completion_aliases=(completed,) if alias_completion else (),
            native_acceptance=graph[native]))
    return tuple(wishes) + npc_contracts(graph, eligible_locations)


def npc_contracts(graph: Mapping[str, Rules], eligible_locations: frozenset[str]):
    prefix = "Room Event: event:mapper/reviewed:"
    wishes = []
    for identity, location, stem in _NPC_DELIVERIES:
        if location not in eligible_locations:
            continue
        accepted = prefix + "courier-" + stem + "-accepted"
        completed = prefix + "courier-" + stem + "-delivered"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError(f"Courier requirements need review: {identity}")
        if any(accepted not in rule.all_of for rule in graph[completed]):
            raise ValueError(f"Courier delivery has no acceptance prerequisite: {identity}")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name != accepted))
                     for rule in graph[completed])
        wishes.append(WishContract(identity, graph[accepted], task,
            completion_aliases=(completed,), acceptance_aliases=(accepted,)))
    if "Wish: Great Taste of Pharloom" in eligible_locations:
        accepted = prefix + "gourmand-quest-accepted"
        completed = prefix + "great-taste-completed"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("Great Taste requirements need review.")
        if any(accepted not in rule.all_of for rule in graph[completed]):
            raise ValueError("Great Taste has no acceptance prerequisite.")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name != accepted))
                     for rule in graph[completed])
        wishes.append(WishContract("Great Gourmand", graph[accepted], task,
            completion_aliases=(completed,), acceptance_aliases=(accepted,)))
    location = "Wish: Pinmaster's Oil"
    if location in eligible_locations:
        from .requirements import get_location_requirements
        offered = "Room Event: event:mapper/419069f7-4bcf-42b1-a112-08cab969636a"
        task = get_location_requirements(location)
        if not graph.get(offered) or not task:
            raise ValueError("Pinmaster's Oil requirements need review.")
        wishes.append(WishContract("A Pinsmiths Tools", graph[offered], task,
            completion_aliases=("Event: Pinmaster's Oil Completed",
                "Room Event: event:mapper/33fc0209-2a45-4288-a993-c1aa336d6b8f"), locations=(location,)))
    if "Drifter's Cloak" in eligible_locations:
        accepted = "Room Event: event:mapper/2073ea77-7260-4926-b66e-28a57fe0a4c4"
        completed = "Room Event: event:mapper/88ab2f59-9e0c-41a1-ab62-d18f910e4f88"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("Flexible Spines requirements need review.")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name != accepted))
                     for rule in graph[completed])
        wishes.append(WishContract("Brolly Get", graph[accepted], task,
            completion_aliases=(completed,), acceptance_aliases=(accepted,)))
    if "Wish: Passing of the Age" in eligible_locations:
        accepted = prefix + "passing-age-accepted"
        completed = prefix + "herald-visit-7"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("Passing of the Age requirements need review.")
        wishes.append(WishContract("Mr Mushroom", graph[accepted], graph[completed],
            completion_aliases=(completed,), acceptance_aliases=(accepted,)))
    if "Pollip Pouch" in eligible_locations:
        accepted = "Room Event: event:mapper/27c9f587-ce44-47a5-8a93-494bdf16f46b"
        completed = "Room Event: event:mapper/fe8b52a9-f154-4a76-b35b-be05595cd934"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("Rite of the Pollip requirements need review.")
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name != accepted))
                     for rule in graph[completed])
        wishes.append(WishContract("Shell Flowers", graph[accepted], task,
            completion_aliases=(completed,), acceptance_aliases=(accepted,)))
    if "Longclaw" in eligible_locations:
        accepted = prefix + "huntress-quest-accepted"
        completed = prefix + "huntress-quest-completed"
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("Huntress requirements need review.")
        wishes.append(WishContract("Huntress Quest", graph[accepted], graph[completed],
            completion_aliases=(completed,), acceptance_aliases=(accepted,)))
    if "Pollip Pouch" in eligible_locations:
        event_prefix = "Room Event: event:mapper/"
        started = event_prefix + "0579d689-67d7-443a-a85b-916aa61ccabe"
        cursed = event_prefix + "d6230e21-4fd9-496e-8296-2a7630bbfce5"
        accepted = prefix + "infestation-operation-accepted"
        completed = event_prefix + "cf97a141-ac87-4c38-b4a5-231eca44dc3a"
        if any(not graph.get(name) for name in (started, cursed, accepted, completed)):
            raise ValueError("Curse wish requirements need review.")
        wishes.append(WishContract("Wood Witch Curse", graph[started], graph[started],
            completion_aliases=(started, cursed)))
        cure = graph["Event: Rite of Rebirth Completed"]
        if len(cure) != 1 or cure[0] != req(*cure[0].all_of, crest=False):
            raise ValueError("Native cure requirements need review.")
        aliases = (accepted, event_prefix + "b289af30-9c97-4eb4-bd24-1750bc91adfe")
        task = tuple(replace(rule, all_of=tuple(dict.fromkeys((
            *(name for name in rule.all_of if name not in aliases), *cure[0].all_of))))
            for rule in graph[completed])
        if "Crest: Witch" in eligible_locations:
            wishes.append(WishContract("Doctor Curse Cure", graph[accepted], task,
                locations=("Crest: Witch",), completion_aliases=(completed,),
                acceptance_aliases=aliases))
    alchemy = (
        ("Extractor Blue", {"Needle Phial", "Plasmium Phial"},
         "3d9fe91e-cdc7-4e50-abe5-627563550f32", "9730064b-fd6c-40d9-a7d9-7ec9ed669b96",
         (), ("reviewed:alchemist-assistant-completed",)),
        ("Extractor Blue Worms", {"Wish: Advanced Alchemy"},
         "reviewed:advanced-alchemy-accepted", "reviewed:advanced-alchemy-completed",
         ("92179acc-052d-4562-894b-c345512cd620",), ()),
    )
    for identity, scopes, accepted_id, completed_id, accepted_ids, completed_ids in alchemy:
        if not scopes.intersection(eligible_locations):
            continue
        event_prefix = "Room Event: event:mapper/"
        accepted, completed = event_prefix + accepted_id, event_prefix + completed_id
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError(f"Alchemy requirements need review: {identity}")
        aliases = (accepted, *(event_prefix + name for name in accepted_ids))
        task = tuple(replace(rule, all_of=tuple(name for name in rule.all_of if name not in aliases))
                     for rule in graph[completed])
        wishes.append(WishContract(identity, graph[accepted], task,
            completion_aliases=(completed, *(event_prefix + name for name in completed_ids)),
            acceptance_aliases=aliases))
    if "Wish: A Vassal Lost" in eligible_locations:
        accepted = "Room Event: event:mapper/512aa8e5-5da8-4afd-b906-c6f270dab172"
        completed = "Room Event: event:mapper/da476bc2-0b8d-4b9c-b040-2e0f75c197b8"
        from .game_modes import RESTING_SITES_VISITED
        if not graph.get(accepted) or not graph.get(completed):
            raise ValueError("A Vassal Lost requirements need review.")
        task = tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, RESTING_SITES_VISITED))))
                     for rule in graph[completed])
        wishes.append(WishContract("Steel Sentinel", graph[accepted], task,
            completion_aliases=(completed,), acceptance_aliases=(accepted,), locations=("Wish: A Vassal Lost",)))
    return tuple(wish for wish in wishes if wish.identity not in NATIVE_WISH_FOLLOWUPS)


def wish_location_rules(wishes: tuple[WishContract, ...]) -> Mapping[str, Rules]:
    result = {}
    for contract in wishes:
        for location in contract.locations:
            if location in result:
                raise ValueError(f"Multiple shuffled wishes own {location}")
            result[location] = (req(completion_event(contract.identity), crest=False), *contract.reward_alternatives)
    return MappingProxyType(result)


SUPPORTED_BOSS_IDS = BOSS_CREDIT_LOCATIONS
_EVENT_PREFIX = "Room Event: event:mapper/"


def _event_name(name):
    return name if name.startswith(("Room Node: ", "Event: ")) else _EVENT_PREFIX + name


def _story_rules(rules, dependencies, boss):
    replacement = credit_event(boss)
    return tuple(replace(rule,
        all_of=tuple(replacement if name in dependencies else name for name in rule.all_of),
        any_of=tuple(replacement if name in dependencies else name for name in rule.any_of))
        for rule in rules)


def story_route_rules(owner, rules, bosses):
    for boss, dependencies, event_names, _ in _STORY_GATES:
        if boss in bosses and owner in {_event_name(name) for name in event_names}:
            rules = _story_rules(rules, frozenset(_event_name(name) for name in dependencies), boss)
    return rules


def story_rules(graph, eligible, boss_ids):
    from .requirements import get_location_requirements

    events, locations = {}, {}
    for boss, dependencies, event_names, location_names in _STORY_GATES:
        if boss not in boss_ids:
            continue
        dependencies = frozenset(_event_name(name) for name in dependencies)
        for short_name in event_names:
            name = _event_name(short_name)
            events[name] = _story_rules(events.get(name, graph[name]), dependencies, boss)
        if boss == "Boss: Widow":
            location_names = (*location_names, *(name for name in eligible if name.startswith("Relic Turn-in: ")))
        for name in location_names:
            if name in eligible:
                locations[name] = _story_rules(locations.get(name, get_location_requirements(name)), dependencies, boss)
    if "Boss: Summoned Saviour" in boss_ids:
        from .game_modes import RESTING_SITES_VISITED
        name = _EVENT_PREFIX + "da476bc2-0b8d-4b9c-b040-2e0f75c197b8"
        events[name] = tuple(replace(rule, all_of=(*rule.all_of, RESTING_SITES_VISITED)) for rule in events[name])
    if "Boss: Groal the Great" in boss_ids:
        name = "Event: Trail's End Completed"
        boss = "Boss: Groal the Great"
        events[name] = tuple(replace(rule,
            all_of=(*rule.all_of, credit_event(boss)),
            required_locations=tuple(location for location in rule.required_locations if location != boss))
            if boss in rule.required_locations else rule for rule in graph[name])
    if "Boss: Lace (Cradle)" in boss_ids:
        from .wish_events import SILK_AND_SOUL_LACE_DEFEATED_ITEM
        name = "Event: Silk and Soul Offered"
        events[name] = _story_rules(graph[name], {SILK_AND_SOUL_LACE_DEFEATED_ITEM}, "Boss: Lace (Cradle)")
    if "Boss: Great Conchflies" in boss_ids:
        credit = credit_event("Boss: Great Conchflies")
        name = _EVENT_PREFIX + "44adf080-8baa-4759-99b4-65c923940cc5"
        events[name] = tuple(replace(rule, all_of=(*rule.all_of, credit)) for rule in graph[name])
        if "Boss: Raging Conchfly" in eligible:
            locations["Boss: Raging Conchfly"] = tuple(replace(rule, all_of=(*rule.all_of, credit))
                for rule in get_location_requirements("Boss: Raging Conchfly"))
    if "Boss: Bell Beast" in boss_ids:
        events["Event: Ordinary Silk Blockades Cleared"] = (req(credit_event("Boss: Bell Beast"), crest=False),)
    return events, locations


_EMPTY = {"schema": SCHEMA, "wishes": {}, "bosses": []}


def world_location_requirements(world, name, **options):
    from .requirements import get_location_requirements
    override = getattr(world, "_progression_location_rules", {}).get(name)
    from .boss_souls import gate_location
    from .npc_souls import gate_location as npc_gate
    from .enemy_souls import gate_location as enemy_gate
    from .silk_economy import gate_location as silk_gate
    return silk_gate(world, enemy_gate(world, name, npc_gate(world, name, gate_location(world, name, override if override is not None else get_location_requirements(name, **options)))))


def prepare_world(world, graph):
    from .locations import location_data_table
    from .requirements import get_location_requirements

    from .boss_souls import gate_graph, gate_location, location_overrides
    from .npc_souls import gate_graph as npc_graph, location_overrides as npc_locations
    from .enemy_souls import gate_graph as enemy_graph
    graph = enemy_graph(world, npc_graph(world, gate_graph(world, graph)))
    eligible = frozenset(location_data_table) - world.get_goal_excluded_location_names()
    boss_ids = SUPPORTED_BOSS_IDS & eligible if world.get_category_mode("Boss") != "vanilla" else frozenset()
    story_events, story_locations = story_rules(graph, eligible, boss_ids)
    bosses = tuple(BossContract(name, gate_location(world, name, story_locations.get(name, get_location_requirements(name))))
                   for name in sorted(boss_ids))
    graph = {**graph, **story_events}
    from .npc_souls import gate_wishes
    wishes = gate_wishes(world, board_contracts(graph, eligible)) if world.options.shuffle_wish_offers else ()
    passthrough = getattr(world.multiworld, "re_gen_passthrough", {}).get(world.game)
    wish_ids = frozenset(contract.identity for contract in wishes)
    boss_ids = frozenset(contract.identity for contract in bosses)
    if passthrough is not None:
        assignments = Assignments.from_slot_data(passthrough["progression_shuffle"], wish_ids, boss_ids)
    else:
        planned_wishes(world, wish_ids)
        assignments = Assignments(tuple((name, name) for name in sorted(wish_ids)),
                                  tuple(sorted(boss_ids)))
    world._progression_wishes = wishes
    world._progression_bosses = bosses
    world._progression_assignments = assignments
    world._progression_location_rules = npc_locations(world, location_overrides(world, {**story_locations, **wish_location_rules(wishes)}))
    from .enemy_souls import location_overrides as enemy_locations
    world._progression_location_rules = enemy_locations(world, world._progression_location_rules)
    world._progression_story_events = story_events
    world._progression_events = compile_events(assignments, wishes, bosses)
    from .silk_economy import prepare_world as silk_graph, location_overrides as silk_locations
    world._progression_location_rules = silk_locations(world, world._progression_location_rules)
    from .boss_journal import location_overrides as journal_locations
    world._progression_location_rules = journal_locations(world, world._progression_location_rules)
    return silk_graph(world, {**graph, **world._progression_events})


def _replace_events(world, assignments):
    from .native_regions import choose_requirement_anchor, native_rule_options, region_label
    from .room_graph_logic import native_region_name
    from .requirement_rules import _invalidate_native_source_player, build_requirements_rule

    _invalidate_native_source_player(world.multiworld, world.player)
    events = compile_events(assignments, world._progression_wishes, world._progression_bosses)
    from .silk_economy import gate_location as silk_gate
    events = {name: silk_gate(world, rules) for name, rules in events.items()}
    options = native_rule_options(world)
    names = world._silksong_native_abstract_names
    for owner, alternatives in events.items():
        if alternatives == world._progression_events.get(owner):
            continue
        target = world.multiworld.get_region(native_region_name(owner), world.player)
        for entrance in tuple(target.entrances):
            entrance.parent_region.exits.remove(entrance)
            target.entrances.remove(entrance)
            for name in entrance.access_rule.region_dependencies():
                region = world.multiworld.get_region(name, world.player)
                connections = world.multiworld.indirect_connections.get(region)
                if connections is not None:
                    connections.discard(entrance)
                    if not connections:
                        del world.multiworld.indirect_connections[region]
        grouped = {}
        for requirement in alternatives:
            anchor = choose_requirement_anchor(requirement, world._silksong_native_region_names, owner)
            grouped.setdefault(anchor, []).append(requirement)
        for anchor, rules in grouped.items():
            parent = world.multiworld.get_region(native_region_name(anchor) if anchor else "Menu", world.player)
            entrance = world.create_entrance(parent, target, build_requirements_rule(
                tuple(rules), anchor_requirement_name=anchor,
                extra_abstract_requirement_names=names, **options,
            ), f"{parent.name} -> {target.name}")
            if entrance is not None:
                entrance.display_name = f'{region_label(anchor or "Menu")} -> {region_label(owner)}'
    world._silksong_native_abstract_requirements.update(events)
    world._progression_events = events
    world._progression_assignments = assignments


def _preparation_locations(world):
    multiworld = world.multiworld
    if (not multiworld.groups
            and all(location.item.player == location.player
                    for location in multiworld.get_filled_locations())
            and all(exit.connected_region is None or exit.connected_region.player == world.player
                    for region in world.get_regions() for exit in region.exits)):
        return world.get_locations()
    return None


def _preparation_state(world, guaranteed=(), base_state=None, *, locations=None):
    if locations is None:
        locations = _preparation_locations(world)
    if base_state is None:
        state = world.multiworld.get_all_state(perform_sweep=locations is None)
    else:
        state = base_state.copy()
        state.rule_builder_cache[world.player] = {
            key: value for key, value in state.rule_builder_cache[world.player].items() if value
        }
        reachable = state.reachable_regions[world.player]
        state.blocked_connections[world.player] = {
            entrance for region in reachable for entrance in region.exits
            if entrance.connected_region not in reachable
        }
    if locations is not None:
        for location in guaranteed:
            state.advancements.add(location)
            state.collect(location.item, True, location)
        from .requirement_rules import sweep_native_sources

        sweep_native_sources(state, locations)
    return state


def _without_progression_events(world, evaluate):
    from rule_builder.rules import False_
    from .room_graph_logic import native_region_name
    from .requirement_rules import _invalidate_native_source_player

    saved = []
    blocked = False_().resolve(world)
    try:
        for name in world._progression_events:
            region = world.multiworld.get_region(native_region_name(name), world.player)
            for entrance in region.entrances:
                saved.append((entrance, entrance.access_rule))
                entrance.access_rule = blocked
        _invalidate_native_source_player(world.multiworld, world.player)
        return evaluate()
    finally:
        for entrance, rule in saved:
            entrance.access_rule = rule
        _invalidate_native_source_player(world.multiworld, world.player)


def _guaranteed_preparation_state(world):
    if _preparation_locations(world) is None:
        return None
    return _without_progression_events(world, lambda: _preparation_state(world))


def _optimistic_preparation_state(world, foreign_rewards, local_rewards):
    state = world.multiworld.get_all_state(perform_sweep=False)
    for item in foreign_rewards:
        state.collect(item, True)
    state.sweep_for_advancements(local_rewards)
    return state


def finalize_world(world):
    from BaseClasses import CollectionState

    if not world._progression_wishes:
        return
    if getattr(world.multiworld, "re_gen_passthrough", {}).get(world.game) is not None:
        return
    multiworld = world.multiworld
    guaranteed = _guaranteed_preparation_state(world)
    preparation_locations = _preparation_locations(world)
    baseline = _preparation_state(world, base_state=guaranteed, locations=preparation_locations)
    locations = preparation_locations
    check_local_first = locations is None and not multiworld.groups and any(
        other.game != world.game for other in multiworld.worlds.values())
    if locations is None:
        locations = multiworld.get_locations()
    required = tuple(location for location in locations if location.can_reach(baseline))
    from .room_graph_logic import native_region_name
    completion_names = tuple(completion_event(contract.identity) for contract in world._progression_wishes)
    completion_names += tuple(credit_event(contract.identity) for contract in world._progression_bosses)
    required_events = tuple(multiworld.get_region(native_region_name(name), world.player)
                            for name in completion_names
                            if multiworld.get_region(native_region_name(name), world.player).can_reach(baseline))
    accepted = world._progression_assignments
    foreign_rewards = tuple(location.item for location in multiworld.get_filled_locations()
                            if location.player != world.player and location.item.player == world.player)
    local_rewards = tuple(location for location in world.get_locations()
                          if location.item is not None and location.item.player == world.player)

    from .category_fill import _flea_pool_is_placeable

    capacity_independent = _without_progression_events(
        world, lambda: _flea_pool_is_placeable(multiworld, world.player))

    def valid(candidate):
        nonlocal accepted
        if candidate == accepted:
            return True
        _replace_events(world, candidate)
        if check_local_first:
            optimistic = _optimistic_preparation_state(world, foreign_rewards, local_rewards)
            if not all(region.can_reach(optimistic) for region in required_events):
                _replace_events(world, accepted)
                return False
        state = _preparation_state(world, base_state=guaranteed, locations=preparation_locations)
        accessible = all(location.can_reach(state) for location in required) and all(
            region.can_reach(state) for region in required_events)
        if accessible and not capacity_independent:
            accessible = _flea_pool_is_placeable(multiworld, world.player)
        if accessible:
            accepted = candidate
            return True
        _replace_events(world, accepted)
        return False

    selected = choose_assignments(world.random,
        frozenset(contract.identity for contract in world._progression_wishes),
        frozenset(contract.identity for contract in world._progression_bosses), valid,
        planned_wishes(world, frozenset(contract.identity for contract in world._progression_wishes)))
    assert selected == accepted
    multiworld.state = CollectionState(multiworld)


def export_world(world, slot_data):
    from .requirements import _export_requirement_group, export_wish_logic_events

    from .game_modes import RESTING_SITES_VISITED, resting_site_requirements
    slot_data["abstract_requirements"][RESTING_SITES_VISITED] = _export_requirement_group(resting_site_requirements(world._steel_soul_sites))
    slot_data["progression_shuffle"] = world._progression_assignments.to_slot_data()
    for name, requirements in {**world._progression_story_events, **world._progression_events}.items():
        slot_data["abstract_requirements"][name] = _export_requirement_group(requirements)
    for name, requirements in world._progression_location_rules.items():
        slot_data["requirements"][name] = _export_requirement_group(requirements)
    slot_data["logic_events"] = export_wish_logic_events(
        slot_data["requirements"], world._silksong_active_wish_logic_events)
