from __future__ import annotations

from Options import OptionError

STEEL_SOUL_LOCATIONS = frozenset({
    "Shell Satchel", "Boss: Summoned Saviour", "Wish: A Vassal Lost",
})
CLASSIC_LOCATIONS = frozenset({
    "Dead Bug's Purse", "Blasted Steps - Silkeater", "Wish: Queen's Egg",
})
RESTING_SITE_GROUPS = (
    ("Shellwood_26", "Bone_East_14", "Aspid_01"),
    ("Hang_08", "Coral_28", "Aqueduct_05"),
)
RESTING_SITE_EVENTS = {
    "Shellwood_26": "7f363cc4-8807-432b-b65f-c7cae6b273fc",
    "Bone_East_14": "90794214-911f-4303-9beb-d85f2f59df28",
    "Aspid_01": "674c7ac1-7d70-4b78-b519-4977586dfd28",
    "Hang_08": "b7f5cc16-faaf-4068-9c58-509c27decb77",
    "Coral_28": "d3f813ea-2390-46b9-ba81-a529dcec533f",
    "Aqueduct_05": "d4425cb5-e042-4444-9ca7-5f94929f5e21",
}
RESTING_SITES_VISITED = "Event: Selected Steel Soul Resting Sites Visited"


def validate_resting_sites(sites, steel_soul):
    if not isinstance(sites, (list, tuple)) or any(not isinstance(site, str) for site in sites):
        raise OptionError("Steel Soul resting sites must be a list of scene names.")
    if not steel_soul:
        if sites:
            raise OptionError("Classic games cannot select Steel Soul resting sites.")
        return ()
    if (len(sites) != 3 or len(set(sites)) != 3
            or not set(sites).issubset(RESTING_SITE_EVENTS)
            or any(not set(sites).intersection(group) for group in RESTING_SITE_GROUPS)):
        raise OptionError("Steel Soul needs three distinct resting sites with at least one from each group.")
    return tuple(sites)


def choose_resting_sites(random):
    sites = [random.choice(group) for group in RESTING_SITE_GROUPS]
    remaining = [site for group in RESTING_SITE_GROUPS for site in group if site not in sites]
    return (*sites, random.choice(remaining))


def excluded_locations(steel_soul, act_one_only=False):
    if not steel_soul:
        return STEEL_SOUL_LOCATIONS
    return CLASSIC_LOCATIONS | (STEEL_SOUL_LOCATIONS - {"Shell Satchel"} if act_one_only else frozenset())


def resting_site_requirements(sites):
    from .requirements import req

    return (req("Option: Steel Soul On", *("Room Event: event:mapper/" + RESTING_SITE_EVENTS[site]
                 for site in sites), crest=False),) if sites else ()
