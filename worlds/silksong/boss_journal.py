from __future__ import annotations

import json
import pkgutil

CATALOGUE = tuple(json.loads(pkgutil.get_data(__package__, "boss_journal.json")))
JOURNAL = "Hunter's Journal"
JOURNAL_LOCATION = "Nuu - Hunter's Journal"
BY_LOCATION = {"Journal: " + row["name"]: row for row in CATALOGUE}
COMPLETIONS = {"Journal Completion: " + row["name"]: row for row in CATALOGUE if row["kills_required"] > 1}
ITEM_BY_LOCATION = {JOURNAL_LOCATION: JOURNAL, **{
    location: "Journal Entry: " + row["name"] for location, row in BY_LOCATION.items()
}, **{name: "Journal Completion: " + row["name"] for name, row in COMPLETIONS.items()}}


def sources(row, excluded, act):
    return tuple(source for source in row["sources"]
                 if source["boss"] not in excluded and source["act"] <= act)


def excluded_locations(excluded, act):
    entries = {name for name, row in BY_LOCATION.items() if not sources(row, excluded, act)}
    notes = {name for name, row in COMPLETIONS.items()
             if "Journal: " + row["name"] in entries or row.get("completion_act", 1) > act
             or row.get("completion_boss") in excluded
             or "completion_events" in row and len(sources(row, excluded, act)) != len(row["sources"])}
    return frozenset(entries | notes)



def unknown_locations(unknown, excluded, act):
    result = {name for name, row in BY_LOCATION.items()
              if name not in excluded and all(source["boss"] in unknown for source in sources(row, excluded, act))}
    result.update(name for name, row in COMPLETIONS.items()
                  if name not in excluded and (row.get("completion_boss") in unknown
                      or "completion_boss" not in row and any(source["boss"] in unknown for source in sources(row, excluded, act))))
    return frozenset(result)


def base_requirements(requirements, req):
    result = {JOURNAL_LOCATION: (req("Room Node: greymoor/greymoor-halfway-home#room", crest=False),)}
    for location, row in BY_LOCATION.items():
        result[location] = tuple(dict.fromkeys(rule for source in row["sources"]
            for rule in requirements.get(source["boss"], tuple(req(event, crest=False) for event in source["events"]))))
    for name, row in COMPLETIONS.items():
        result[name] = requirements[row["completion_boss"]] if "completion_boss" in row else (req(*row["completion_events"], crest=False),)
    moss = BY_LOCATION["Journal: Moss Mother"]
    result["Journal: Moss Mother"] = tuple(req(event, crest=False) for source in moss["sources"] for event in source["events"])
    return result


def location_overrides(world, overrides):
    if world.get_category_mode("Journal") == "vanilla":
        return overrides
    from .progression_shuffle import world_location_requirements
    from .requirements import req, REQUIREMENTS
    from .boss_souls import gate
    result = dict(overrides)
    excluded = world.get_goal_excluded_location_names()
    act = int(world.get_content_scope().removeprefix("act_"))
    unknown = world.get_logic_unknown_locations()
    for name, row in BY_LOCATION.items():
        if name in excluded:
            continue
        rules = []
        for source in sources(row, excluded, act):
            if source["boss"] in unknown:
                continue
            if row["name"] == "Moss Mother":
                rules.extend(gate(world, tuple(req(event, crest=False) for event in source["events"]), source["boss"]))
            elif source["boss"] in REQUIREMENTS:
                rules.extend(world_location_requirements(world, source["boss"]))
            else:
                rules.extend(gate(world, tuple(req(event, crest=False) for event in source["events"]), source["boss"]))
        result[name] = tuple(dict.fromkeys(rules))
    for name, row in COMPLETIONS.items():
        if name in excluded:
            continue
        result[name] = (world_location_requirements(world, row["completion_boss"]) if "completion_boss" in row
                        else (req(*row["completion_events"], crest=False),))
    return result
