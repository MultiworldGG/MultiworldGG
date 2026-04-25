from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World

skills_paths: dict[str, str] = {
    "Sword": "spell:1002",
    "Double Jump": "spell:3004",
    "Regenerate": "spell:2013",
    "Bow": "spell:1001",
    "Dash": "spell:4000",
    "Bash": "spell:3000",
    "Grapple": "spell:3001",
    "Glide": "spell:4002",
    "Flap": "spell:3005",
    "Grenade": "spell:2010",
    "Flash": "spell:2004",
    "Water Dash": "spell:4004",
    "Burrow": "spell:3002",
    "Launch": "spell:2019",
    "Clean Water": "file:assets/icons/game/water.png",
    "Water Breath": "opher:10",
    "Hammer": "spell:1000",
    "Sentry": "spell:2011",
    "Shuriken": "spell:2015",
    "Spear": "spell:2012",
    "Blaze": "spell:2016"
}

collectibles_paths: dict[str, str] = {
    "Health Fragment": "file:assets/icons/game/healthfragment.png",
    "Energy Fragment": "file:assets/icons/game/energyfragment.png",
    "Gorlek Ore": "file:assets/icons/game/gorlekore.png",
    "Keystone": "file:assets/icons/game/keystone.png",
    "Shard Slot": "file:assets/icons/game/shardslot.png",
    "Ancestral Light 1": "spell:4007",
    "Ancestral Light 2": "spell:4008"
}
shards_paths: dict[str, str] = {
    "Overcharge": "shard:1",
    "Triple Jump": "shard:2",
    "Wingclip": "shard:3",
    "Bounty": "shard:4",
    "Swap": "shard:5",
    "Magnet": "shard:8",
    "Splinter": "shard:9",
    "Reckless": "shard:13",
    "Quickshot": "shard:14",
    "Resilience": "shard:18",
    "Light Harvest": "shard:19",
    "Vitality": "shard:22",
    "Life Harvest": "shard:23",
    "Energy Harvest": "shard:25",
    "Energy (Shard)": "shard:26",
    "Life Pact": "shard:27",
    "Last Stand": "shard:28",
    "Sense": "shard:30",
    "Ultra Bash": "shard:32",
    "Ultra Grapple": "shard:33",
    "Overflow": "shard:34",
    "Thorn": "shard:35",
    "Catalyst": "shard:36",
    "Turmoil": "shard:38",
    "Sticky": "shard:39",
    "Finesse": "shard:40",
    "Spirit Surge": "shard:41",
    "Lifeforce": "shard:43",
    "Deflector": "shard:44",
    "Fracture": "shard:46",
    "Arcing": "shard:47"
}
upgrades_paths: dict[str, str] = {
    "Rapid Sentry": "opher:1",
    "Hammer Shockwave": "opher:3",
    "Static Shuriken": "opher:5",
    "Exploding Spear": "opher:7",
    "Charge Blaze": "opher:9",
    "Water Breath": "opher:10"
}
# Generated using the 'randomizer\assets\icons\bonus' folder and group_table["bonus"] + group_table["bonus+"]
bonus_paths: dict[str, str] = {
    "Health Regeneration": "file:assets/icons/bonus/healthregeneration.png",
    "Energy Regeneration": "file:assets/icons/bonus/energyregeneration.png",
    "Extra Double Jump": "file:assets/icons/bonus/extradoublejump.png",
    "Extra Air Dash": "file:assets/icons/bonus/extraairdash.png",
    "Blaze Efficiency": "file:assets/icons/bonus/blazeefficiency.png",
    "Spear Efficiency": "file:assets/icons/bonus/spearefficiency.png",
    "Shuriken Efficiency": "file:assets/icons/bonus/shurikenefficiency.png",
    "Sentry Efficiency": "file:assets/icons/bonus/sentryefficiency.png",
    "Bow Efficiency": "file:assets/icons/bonus/bowefficiency.png",
    "Regenerate Efficiency": "file:assets/icons/bonus/regenerateefficiency.png",
    "Flash Efficiency": "file:assets/icons/bonus/flashefficiency.png",
    "Grenade Efficiency": "file:assets/icons/bonus/grenadeefficiency.png",
    "Rapid Sword": "file:assets/icons/bonus/rapidsword.png",
    "Rapid Hammer": "file:assets/icons/bonus/rapidsmash.png",
    "Rapid Spear": "file:assets/icons/bonus/rapidspear.png",
    "Rapid Grenade": "file:assets/icons/bonus/rapidgrenade.png",
    "Quickshot Upgrade": "file:assets/icons/bonus/rapidquickshot.png",
    "Rapid Regenerate": "file:assets/icons/bonus/rapidregen.png",
    "Melting Bow":  skills_paths["Bow"],
    "Melting Blaze": "file:assets/icons/bonus/meltingblaze.png",
    "Melting Sword": "file:assets/icons/bonus/meltingsword.png",
    "Melting Hammer": skills_paths["Hammer"],
    "Melting Spear": "file:assets/icons/bonus/meltingspear.png",
    "Melting Shuriken": "file:assets/icons/bonus/meltingshuriken.png",
    "Uncharged Bashnades": "file:assets/icons/bonus/unchargedbashgrenade.png",
    "Extra Grenade": "file:assets/icons/bonus/extragrenade.png",
    "Splinter Grenade": "file:assets/icons/bonus/splintergrenade.png",
    "Unlimited Sentries": "file:assets/icons/bonus/unlimitedsentries.png",
    "Sentry Burst Upgrade": "file:assets/icons/bonus/sentryburstupgrade.png",
    "Sentry Fire Rate": "file:assets/icons/bonus/sentryattackspeed.png",
    "Extra Shurikens": "file:assets/icons/bonus/extrashuriken.png",
    "Splinter Shurikens": "file:assets/icons/bonus/splintershuriken.png",
    "Bashable Shurikens": "file:assets/icons/bonus/bashableshuriken.png",
    "Jumpgrade": "file:assets/icons/bonus/jumpgrade.png",
    "Skill Velocity": "file:assets/icons/bonus/skillvelocity.png",
}
others_paths: dict[str, str] = {
    "teleporter": "file:assets/icons/game/teleporter.png",
    "experience": "file:assets/icons/game/experience.png",
    "map": "file:assets/icons/game/map.png",
    "message": "file:assets/icons/game/message.png",
    "moki": "file:assets/icons/game/moki.png",
    "gauntlet": "shard:24",
    "plant": "shard:12",
    "heart": "spell:2008",
    "soundwave": "spell:2006",
    "gold_orb": "spell:2018"
}
archipelago_paths: dict[str, str] = {
    "progression": "file:assets/icons/archipelago/ap-important.png",
    "useful": "file:assets/icons/archipelago/ap-normal.png",
    "filler": "file:assets/icons/archipelago/ap-trash.png"
}


def get_item_iconpath(world: World, item: Item | None, keyword_based_icons: bool = True) -> str:
    if item is None:
        return ""

    # sometimes apworld use ints that since 0.6.0 need to be converted explicitly
    classification = ItemClassification(item.classification)

    icon_path = None
    if item.game == world.game:  # Try to use base game and rando icons
        if item.name.endswith("Spirit Light"):
            icon_path = others_paths["experience"]

        elif item.name.endswith(" TP"):
            icon_path = others_paths["teleporter"]

        elif skills_paths.get(item.name):
            icon_path = skills_paths[item.name]

        elif shards_paths.get(item.name):
            icon_path = shards_paths[item.name]

        elif collectibles_paths.get(item.name):
            icon_path = collectibles_paths[item.name]

        elif upgrades_paths.get(item.name):
            icon_path = upgrades_paths[item.name]

        elif bonus_paths.get(item.name):
            icon_path = bonus_paths[item.name]

    if keyword_based_icons and icon_path is None:  # Some generic icons for any games
        if "key" in item.name.lower():
            icon_path = collectibles_paths["Keystone"]
        elif "health" in item.name.lower() or "life" in item.name.lower() or "Heart" in item.name.lower():
            icon_path = collectibles_paths["Health Fragment"]
        elif "energy" in item.name.lower():
            icon_path = collectibles_paths["Energy Fragment"]
        elif "map" in item.name.lower():
            icon_path = others_paths["map"]
        elif "TP" in item.name:
            icon_path = others_paths["teleporter"]
        elif "ore" in item.name.lower():
            icon_path = collectibles_paths["Gorlek Ore"]
        elif "exp" in item.name.lower() or "xp" in item.name.lower() or "ability" in item.name.lower():
            icon_path = others_paths["experience"]

    if icon_path is None:  # Fallback to Classification system if keyword_based_icons is turned off or fail
        if ItemClassification.progression in classification:
            icon_path = archipelago_paths["progression"]

        elif ItemClassification.useful in classification:
            icon_path = archipelago_paths["useful"]

        else:
            icon_path = archipelago_paths["filler"]

    return icon_path
