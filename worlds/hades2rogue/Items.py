from typing import Dict, List, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

from .Routes import ROUTES, ROUTE_NAMES, boss_event, boss_victory, COMBAT_HELPER_NPCS_ALL


class ItemData(NamedTuple):
    code: Optional[int]
    progression: bool
    event: bool = False
    trap: bool = False
    useful: bool = False


hades2_base_item_id = 1

# --- Weapons (Nocturnal Arms) -------------------------------------------------
# Short names map to: Staff = Witch's Staff, Blades = Sister Blades,
# Flames = Umbral Flames, Axe = Moonstone Axe, Skull = Argent Skull,
# Coat = Black Coat. Melinoe starts with the Staff by default.
item_table_weapons: Dict[str, ItemData] = {
    "Staff Weapon Unlock Item": ItemData(hades2_base_item_id + 0, True),
    "Blades Weapon Unlock Item": ItemData(hades2_base_item_id + 1, True),
    "Flames Weapon Unlock Item": ItemData(hades2_base_item_id + 2, True),
    "Axe Weapon Unlock Item": ItemData(hades2_base_item_id + 3, True),
    "Skull Weapon Unlock Item": ItemData(hades2_base_item_id + 4, True),
    "Coat Weapon Unlock Item": ItemData(hades2_base_item_id + 5, True),
}

# --- Filler items (the 4 meta-progression currencies) -------------------------
item_table_filler: Dict[str, ItemData] = {
    "Ashes": ItemData(hades2_base_item_id + 6, False),
    # REMOVED: Psyche filler stubbed out (GraspSanity is always on now, and Psyche has no
    # sink in this mod once it is). Item id offset 7 retired; do not reuse.
    # "Psyche": ItemData(hades2_base_item_id + 7, False),
    # REMOVED: Bones filler stubbed out (no sink in this mod -- Cauldron incantations are
    # blocked entirely). Item id offset 8 retired; do not reuse.
    # "Bones": ItemData(hades2_base_item_id + 8, False),
    "Nectar": ItemData(hades2_base_item_id + 9, False),
    # Moon Dust (CardUpgradePoints) = the Arcana upgrade currency. Only joins the filler
    # rotation when ArcanaSanity is not Progressive (so manual upgrades are allowed).
    "Moon Dust": ItemData(hades2_base_item_id + 153, False),
}

# --- Grasp (graspsanity) ------------------------------------------------------
# Each Progressive Grasp raises max Grasp by the grasp_intervals option amount.
item_table_grasp: Dict[str, ItemData] = {
    "Progressive Grasp": ItemData(hades2_base_item_id + 10, False, useful=True),
}

# --- Arcana cards (arcanasanity) ----------------------------------------------
# One entry per Arcana Card, named by its card title. In "Arcana" mode each is a
# single unlock item; in "Progressive_Arcana" mode multiple copies stack (1st
# unlocks, the rest upgrade). The Lua mod maps these titles to internal card ids.
arcana_titles = [
    "The Sorceress", "Wayward Son", "Huntress", "Eternity", "Moon",
    "Furies", "Persistence", "Messenger", "Unseen", "Night",
    "Swift Runner", "Death", "Centaur", "Origination", "Lovers",
    "The Enchantress", "Boatman", "Artificer", "Excellence", "Queen",
    "The Fates", "Champions", "Strength", "Divinity", "Judgment",
]
item_table_arcana: Dict[str, ItemData] = {
    f"{title} Arcana": ItemData(hades2_base_item_id + 11 + i, False, useful=True)
    for i, title in enumerate(arcana_titles)
}
# Progressive_Arcana mode uses these names instead, so the 3 copies read clearly as
# "Progressive <Card> Arcana" in the spoiler. The Lua mod treats them the same as
# "<Card> Arcana" (first unlocks, the rest upgrade).
item_table_arcana_progressive: Dict[str, ItemData] = {
    f"Progressive {title} Arcana": ItemData(hades2_base_item_id + 126 + i, False, useful=True)
    for i, title in enumerate(arcana_titles)
}

# --- Vow removal (reverse_vow) ------------------------------------------------
# In reverse_vow mode you start with vows active; each "<Vow> Vow Removal" item
# lowers that vow's level by one. The Lua mod maps these names to ShrineUpgrades.
vow_names = [
    "Pain", "Grit", "Wards", "Frenzy", "Hordes", "Menace", "Return", "Fangs",
    "Scars", "Debt", "Shadow", "Forfeit", "Time", "Void", "Hubris", "Denial", "Rivals",
]
item_table_vows: Dict[str, ItemData] = {
    f"{vow} Vow Removal": ItemData(hades2_base_item_id + 36 + i, False, useful=True)
    for i, vow in enumerate(vow_names)
}

# --- Route-unlock progressives (lock_routes) ----------------------------------
item_table_routes: Dict[str, ItemData] = {
    "Progressive Underworld": ItemData(hades2_base_item_id + 53, True),
    "Progressive Surface": ItemData(hades2_base_item_id + 54, True),
    # Opens the Surface path (the AP version of the Witching-Wards incantation).
    "Surface Access": ItemData(hades2_base_item_id + 55, True),
    # Removes the Surface's lethal damage penalty (Unraveling a Fateful Bond).
    "Surface Penalty Cure": ItemData(hades2_base_item_id + 56, True),
    # Nightmare (opt-in third-party "Zagreus' Journey" route): mirrors Surface's shape -- its
    # own Access item gates the Crossroads Chaos Gate (no in-fiction damage penalty to cure),
    # plus the usual lock_routes progressive for zones 2-4.
    "Progressive Nightmare": ItemData(hades2_base_item_id + 244, True),
    "Nightmare Access": ItemData(hades2_base_item_id + 243, True),
}

# --- Weapon Aspects (aspectsanity) --------------------------------------------
# Items only (no check locations). "randomized" mode shuffles all 24 Aspects -- the 18
# alternates below plus each weapon's default Aspect of Melinoe, which weapons do NOT
# come with for free in that mode (see aspect_base_titles). Deity names are unique, so an
# alternate's item name is just the Aspect title. "progressive" mode uses one item per
# weapon ("Progressive <Weapon> Aspect"), copied 5x (1 unlock + 4 rank upgrades), and
# leaves the default Aspect of Melinoe unlocked as usual.
# Each randomized entry is (display title, weapon short-name); the Lua mod maps the
# title to the internal aspect id and the weapon. Order is fixed so item ids stay stable.
# The first randomized Aspect item you get for a weapon also unlocks it (see
# Rules._hades2_has_weapon / ItemManager.unlock_aspect), so these get promoted to
# progression at runtime (__init__._main_pool_item_names) instead of staying "useful" as
# below.
aspect_titles = [
    ("Aspect of Circe", "Staff"), ("Aspect of Momus", "Staff"), ("Aspect of Anubis", "Staff"),
    ("Aspect of Pan", "Blades"), ("Aspect of Artemis", "Blades"), ("Aspect of the Morrigan", "Blades"),
    ("Aspect of Medea", "Skull"), ("Aspect of Persephone", "Skull"), ("Aspect of Hel", "Skull"),
    ("Aspect of Eos", "Flames"), ("Aspect of Moros", "Flames"), ("Aspect of Supay", "Flames"),
    ("Aspect of Charon", "Axe"), ("Aspect of Thanatos", "Axe"), ("Aspect of Nergal", "Axe"),
    ("Aspect of Nyx", "Coat"), ("Aspect of Selene", "Coat"), ("Aspect of Shiva", "Coat"),
]
WEAPON_SHORT_NAMES = ["Staff", "Blades", "Skull", "Flames", "Axe", "Coat"]
# InitialWeapon option value (Options.py option_Staff=0..option_Coat=5) -> weapon short-name.
INITIAL_WEAPON_BY_VALUE = {0: "Staff", 1: "Blades", 2: "Flames", 3: "Axe", 4: "Skull", 5: "Coat"}
# The 6 default Aspects of Melinoe as randomized-mode items. All six share the same in-game
# title, so the item name is qualified by weapon to keep it unique. Same (title, weapon) shape
# as aspect_titles; the Lua mod maps these names via its ASPECT_BASE_ITEM_TO_ID.
aspect_base_titles = [(f"Aspect of Melinoe ({weapon})", weapon) for weapon in WEAPON_SHORT_NAMES]
ASPECT_BASE_TITLE_BY_WEAPON: Dict[str, str] = {w: t for t, w in aspect_base_titles}
# aspect_titles grouped by weapon, in the same fixed order as the Lua mod's ASPECTS_BY_WEAPON
# (e.g. Staff -> Circe, Momus, Anubis). Indexed by starting_aspect_index - 1: that option picks
# which of the starting weapon's 4 Aspects it begins the seed equipped with (0 = its default
# Aspect of Melinoe, 1-3 = these alternates) -- see __init__._main_pool_item_names.
ASPECT_TITLES_BY_WEAPON: Dict[str, List[str]] = {}
for _title, _weapon in aspect_titles:
    ASPECT_TITLES_BY_WEAPON.setdefault(_weapon, []).append(_title)
ASPECT_MAX_RANK = 5      # 1 unlock + 4 upgrades, so 5 progressive copies per weapon
KEEPSAKE_PROGRESSIVE_COUNT = 3   # 1 unlock + 2 level upgrades
FAMILIAR_PROGRESSIVE_COUNT = 4   # 1 unlock + 3 bond-tier upgrades


def included_aspect_alts(weapon: str, included_aspects: int) -> List[str]:
    """The alternate-Aspect titles (ASPECT_TITLES_BY_WEAPON's fixed order) accessible for
    `weapon` when IncludedAspects (Options.py) truncates each weapon to `included_aspects`
    (1-4) total Aspects. The default Aspect of Melinoe is always accessible on top of these
    (it's the weapon's first, "free" Aspect in every mode) -- this returns only the 0-3
    alternates on top of it, so callers building a weapon's full accessible-Aspect list
    should always prepend the base title themselves."""
    return ASPECT_TITLES_BY_WEAPON.get(weapon, [])[:max(0, included_aspects - 1)]

aspect_item_base = hades2_base_item_id + 57           # randomized alternates: +57..+74 (18)
aspect_base_item_base = hades2_base_item_id + 274     # randomized Aspects of Melinoe: +274..+279 (6)
item_table_aspects_randomized: Dict[str, ItemData] = {
    **{
        title: ItemData(aspect_item_base + i, False, useful=True)
        for i, (title, _weapon) in enumerate(aspect_titles)
    },
    **{
        title: ItemData(aspect_base_item_base + i, False, useful=True)
        for i, (title, _weapon) in enumerate(aspect_base_titles)
    },
}
aspect_prog_item_base = hades2_base_item_id + 75       # progressive: +75..+80 (6)
item_table_aspects_progressive: Dict[str, ItemData] = {
    f"Progressive {weapon} Aspect": ItemData(aspect_prog_item_base + i, False, useful=True)
    for i, weapon in enumerate(WEAPON_SHORT_NAMES)
}

# per_aspect mode: every one of the 24 Aspects (18 alternates above + each weapon's default
# "Aspect of Melinoe") gets its own 5-copy progressive item line. The first copy of ANY of
# a weapon's 4 aspect items also unlocks that weapon (see Rules._hades2_has_weapon).
# Marked progression unconditionally.
aspect_per_aspect_item_base = hades2_base_item_id + 219   # per_aspect: +219..+242 (24)
item_table_aspects_per_aspect_alt: Dict[str, ItemData] = {
    f"Progressive {title}": ItemData(aspect_per_aspect_item_base + i, True)
    for i, (title, _weapon) in enumerate(aspect_titles)
}
item_table_aspects_per_aspect_base: Dict[str, ItemData] = {
    f"Progressive {weapon} Base Aspect": ItemData(aspect_per_aspect_item_base + 18 + i, True)
    for i, weapon in enumerate(WEAPON_SHORT_NAMES)
}
item_table_aspects_per_aspect = {**item_table_aspects_per_aspect_alt, **item_table_aspects_per_aspect_base}

item_table_aspects = {
    **item_table_aspects_randomized,
    **item_table_aspects_progressive,
    **item_table_aspects_per_aspect,
}

# --- Keepsakes (keepsakesanity) -----------------------------------------------
# 33 keepsakes (randomized mode), named by their in-game title. Chronos's "Time Piece"
# is a findable item but has NO location. "progressive" mode adds 3 "Progressive
# Keepsake" copies instead. The Lua mod maps each title to its keepsake trait.
keepsake_titles = [
    "Engraved Pin", "Luckier Tooth", "Ghost Onion", "Evil Eye", "White Antler",
    "Moon Beam", "Gold Purse", "Knuckle Bones", "Silver Wheel", "Crystal Figurine",
    "Aromatic Phial", "Silken Sash", "Experimental Hammer", "Lion Fang", "Blackened Fleece",
    "Discordant Bell", "Metallic Droplet", "Concave Stone", "Transcendent Embryo", "Fig Leaf",
    "Gorgon Amulet", "Calling Card", "Jeweled Pom", "Time Piece", "Adamant Shard",
    "Cloud Bangle", "Barley Sheaf", "Beautiful Mirror", "Vivid Sea", "Harmonic Photon",
    "Everlasting Ember", "Sword Hilt", "Iridescent Fan",
    # Nightmare (Zagreus' Journey / zannc-SharedKeepsakePort integration). Appended at the end
    # so the auto-numbered item/location ids of the original 33 don't shift.
    "Shattered Shackle", "Evergreen Acorn", "Broken Spearpoint", "Distant Memory",
    "Skull Earring", "Pierced Butterfly", "Myrmidon Bracer",
]
# Keepsake title -> the NPC who gives it. Keepsake check locations are named
# "<NPC> Keepsake" (e.g. "Dora Keepsake"), which reads more clearly than the item name.
# Derived from each keepsake's GiftPresentation flag (DoraGift01, CharonGift01, ...).
KEEPSAKE_NPC: Dict[str, str] = {
    "Engraved Pin": "Moros",
    "Luckier Tooth": "Skelly",
    "Ghost Onion": "Dora",
    "Evil Eye": "Nemesis",
    "White Antler": "Artemis",
    "Moon Beam": "Selene",
    "Gold Purse": "Charon",
    "Knuckle Bones": "Odysseus",
    "Silver Wheel": "Hecate",
    "Crystal Figurine": "Circe",
    "Aromatic Phial": "Narcissus",
    "Silken Sash": "Arachne",
    "Experimental Hammer": "Icarus",
    "Lion Fang": "Heracles",
    "Blackened Fleece": "Medea",
    "Discordant Bell": "Eris",
    "Metallic Droplet": "Hermes",
    "Concave Stone": "Echo",
    "Transcendent Embryo": "Chaos",
    "Fig Leaf": "Dionysus",
    "Gorgon Amulet": "Athena",
    "Calling Card": "Zagreus",
    "Jeweled Pom": "Hades",
    "Time Piece": "Chronos",
    "Adamant Shard": "Hephaestus",
    "Cloud Bangle": "Zeus",
    "Barley Sheaf": "Demeter",
    "Beautiful Mirror": "Aphrodite",
    "Vivid Sea": "Poseidon",
    "Harmonic Photon": "Apollo",
    "Everlasting Ember": "Hestia",
    "Sword Hilt": "Ares",
    "Iridescent Fan": "Hera",
    # Nightmare keepsake-giving cast (zannc-SharedKeepsakePort). "Megaera" is also one of the
    # three random Furies fought in Tartarus (Routes.ROUTES[NIGHTMARE]["bosses"][0]).
    "Shattered Shackle": "Sisyphus",
    "Evergreen Acorn": "Eurydice",
    "Broken Spearpoint": "Patroclus",
    "Distant Memory": "Orpheus",
    "Skull Earring": "Megaera",
    "Pierced Butterfly": "Thanatos",
    "Myrmidon Bracer": "Achilles",
}
CHRONOS_KEEPSAKE = "Time Piece"  # item only, never a check location
# Keepsakes that exist as items but are NOT check locations, because they can't be
# reliably earned by gifting an NPC: Chronos's Time Piece, Zagreus's Calling Card, and
# Hades' Jeweled Pom (boss/story-granted). They behave like Time Piece: item-only.
# Megaera's Skull Earring stays here too -- her gift conditions in-game are still not
# understood well enough to gate a location reliably. The OTHER Nightmare keepsakes
# (Thanatos/Orpheus/Achilles) were re-added as locations July 16 once playtests confirmed
# gifting them via SharedKeepsakePort actually works -- see Routes.NPC_ROUTE_LOCK.
# MUST stay in sync with the Lua mod's own KEEPSAKE_NO_LOCATION (ItemManager.lua);
# tools/sync_check.py enforces that.
KEEPSAKE_NO_LOCATION = {"Time Piece", "Calling Card", "Jeweled Pom", "Skull Earring"}
# The original 33 keepsakes keep their historical ids (+90..+122). The 7 Nightmare keepsakes are
# assigned a SEPARATE, contiguous block at +267..+273 instead of continuing at +123..+129: that
# continuation collided with Rarity Increase (+125) and the first Progressive Arcana ids
# (+126..+129), so several distinct items shared a network id. Archipelago's id->name reverse
# lookup then resolved every colliding id to a single name, which is why received items showed up
# as duplicate "Myrmidon Bracer"s in-game. Both blocks are keyed by title, so the Lua mod (which
# receives item *names*, not ids) is unaffected by the relocation.
_KEEPSAKE_NIGHTMARE_COUNT = 7
# The 7 Nightmare keepsakes by title (the appended block of keepsake_titles). Their items
# only join the pool when the Nightmare route is active this seed (__init__.py) -- without
# Zagreus' Journey / SharedKeepsakePort in play the keepsake they unlock doesn't exist, so
# on other seeds they'd be dead items that still inflate the keepsake-count logic gates.
KEEPSAKE_NIGHTMARE_TITLES = set(keepsake_titles[-_KEEPSAKE_NIGHTMARE_COUNT:])
keepsake_item_base = hades2_base_item_id + 90              # original 33: +90..+122
keepsake_nightmare_item_base = hades2_base_item_id + 267     # Nightmare's 7: +267..+273
item_table_keepsakes_randomized: Dict[str, ItemData] = {
    **{
        title: ItemData(keepsake_item_base + i, False, useful=True)
        for i, title in enumerate(keepsake_titles[:-_KEEPSAKE_NIGHTMARE_COUNT])
    },
    **{
        title: ItemData(keepsake_nightmare_item_base + i, False, useful=True)
        for i, title in enumerate(keepsake_titles[-_KEEPSAKE_NIGHTMARE_COUNT:])
    },
}
# NOTE: id 123 (the old fixed slot for "Progressive Keepsake") is retired -- moved to +245.
# Ids +123..+129 (the old Nightmare keepsake continuation) are now retired too; do not reuse.
item_table_keepsakes_progressive: Dict[str, ItemData] = {
    "Progressive Keepsake": ItemData(hades2_base_item_id + 245, False, useful=True),
}
item_table_keepsakes = {**item_table_keepsakes_randomized, **item_table_keepsakes_progressive}

# --- Familiars / pets (petsanity) ---------------------------------------------
# Items only (no check locations). "randomized" mode = one item per familiar.
# "progressive" mode = "Progressive Familiar" copied 4x (1 unlock + 3 bond tiers).
familiar_names = ["Frinos", "Toula", "Raki", "Hecuba", "Gale"]
familiar_item_base = hades2_base_item_id + 81          # randomized: +81..+85 (5)
item_table_familiars_randomized: Dict[str, ItemData] = {
    name: ItemData(familiar_item_base + i, False, useful=True)
    for i, name in enumerate(familiar_names)
}
item_table_familiars_progressive: Dict[str, ItemData] = {
    "Progressive Familiar": ItemData(hades2_base_item_id + 86, False, useful=True),
}
item_table_familiars = {**item_table_familiars_randomized, **item_table_familiars_progressive}

# --- Boon gods (godsanity) -----------------------------------------------------
# Items only (no check locations of their own). The 9 gods who hand out boons through the
# normal reward-door roll (as opposed to Dionysus/Artemis/Athena/Hades/Chaos, who only appear
# via their own special encounters -- see StartingNpcGifts above). Order matches the Lua mod's
# existing Force<God>BoonKeepsake mapping (ItemManager.lua) for readability, not a functional
# requirement. When godsanity is not "unlocked", a god's boons can't spawn until its item is
# received; the Lua mod handles the 3 active modes (onions / no_waste_less_odds /
# no_waste_same_odds). Progression (not just useful): with godsanity active, Rules.py gates
# that god's "Met <God>"/"<God> Keepsake" locations on holding this item too (you can't meet a
# god, or gift their keepsake, before their boon can ever appear) -- the reachability sweep
# needs to see it as a real requirement, or generation could place something needed behind a
# location the sweep doesn't realize is conditional on it. Harmless when godsanity is
# "unlocked": these items never enter the pool in that mode (see __init__.create_items).
godsanity_gods = [
    "Hephaestus", "Zeus", "Demeter", "Aphrodite", "Poseidon", "Apollo", "Hestia", "Ares", "Hera",
]
godsanity_item_base = hades2_base_item_id + 295          # +295..+303 (9)
item_table_gods: Dict[str, ItemData] = {
    f"{god} Unlock": ItemData(godsanity_item_base + i, True)
    for i, god in enumerate(godsanity_gods)
}

# Hermes and Selene also hand out boons, but through their own dedicated "shop" reward-type
# entries (HermesUpgrade/SpellDrop) rather than competing in the per-god Boon selection above --
# so the Lua mod gates them differently (an existence-only check on their own native
# eligibility requirements, not the GetEligibleLootNames reroll/no_waste odds-scaling the 9
# gods above use). Same item shape and same Rules.py Met/Keepsake gating, though -- kept in a
# separate list only so the Lua-side Boon-odds-scaling denominator (fixed at 9) doesn't need to
# change.
godsanity_shop_gods = ["Hermes", "Selene"]
godsanity_shop_item_base = hades2_base_item_id + 314     # +314..+315 (2)
item_table_shop_gods: Dict[str, ItemData] = {
    f"{god} Unlock": ItemData(godsanity_shop_item_base + i, True)
    for i, god in enumerate(godsanity_shop_gods)
}

# --- Combined God Unlock + Keepsake (keepsakesanity=randomized AND godsanity active) -------
# When KeepsakeSanity is "randomized" (one item per keepsake) and GodSanity isn't "unlocked",
# the 11 GodSanity gods (the 9 boon-reward gods above plus Hermes/Selene) have their own
# "<God> Unlock" item and their keepsake item (e.g. Ares's Sword Hilt) fused into a single
# "<God> Unlock + Keepsake" item -- receiving it unlocks that god's boons AND makes their
# keepsake giftable at once, instead of needing both items separately. __init__.create_items
# swaps these in for both halves when the seed has both modes active (combine_god_keepsake);
# Rules.py checks the combined name in place of either half then. The Lua mod grants both
# effects from one item (ItemManager.lua's GOD_KEEPSAKE_COMBINED), reusing its existing
# unlock_god/unlock_shop_god/unlock_keepsake handlers. Progressive keepsakes (mode 2) have no
# per-NPC item to fuse, so this never applies then. Always progression, like the plain god
# items it replaces (both halves already were).
GOD_KEEPSAKE_COMBINED_GODS = godsanity_gods + godsanity_shop_gods
GOD_KEEPSAKE_TITLE: Dict[str, str] = {
    npc: title for title, npc in KEEPSAKE_NPC.items() if npc in GOD_KEEPSAKE_COMBINED_GODS
}
god_keepsake_combined_item_base = hades2_base_item_id + 322       # +322..+332 (11)
item_table_god_keepsake_combined: Dict[str, ItemData] = {
    f"{god} Unlock + Keepsake": ItemData(god_keepsake_combined_item_base + i, True)
    for i, god in enumerate(GOD_KEEPSAKE_COMBINED_GODS)
}

# --- Helper Room Sanity (story-room NPCs) ---------------------------------------
# Progression (not just useful): with helper_room_sanity on "items"/"items_random", Rules.py
# gates that NPC's "Met <NPC>"/"<NPC> Keepsake" locations on holding this item too (same
# reasoning/shape as godsanity above). Harmless when the mode is "unlocked"/"unlocked_random":
# these items never enter the pool then (see __init__._main_pool_item_names).
helper_story_npcs = ["Arachne", "Narcissus", "Echo", "Hades", "Medea", "Circe", "Dionysus"]
# Nightmare-route-only helpers; only added to the pool/rules when NIGHTMARE is an active route.
helper_story_npcs_nightmare = ["Sisyphus", "Eurydice", "Patroclus"]
helper_npc_item_base = hades2_base_item_id + 304          # +304..+313 (10)
item_table_helper_npcs: Dict[str, ItemData] = {
    f"{npc} Room": ItemData(helper_npc_item_base + i, True)
    for i, npc in enumerate(helper_story_npcs + helper_story_npcs_nightmare)
}

# --- Combat Helper Sanity (combat-assist NPCs) ----------------------------------
# Progression (not just useful): with combat_helper_sanity on "items"/"items_random",
# Rules.py gates that NPC's "Met <NPC>"/"<NPC> Keepsake" locations on holding this item too
# (same reasoning/shape as helper_room_sanity above) -- except Nemesis, who is always
# reachable at the Crossroads regardless (Rules.KEEPSAKE_FREE); her item still gates
# whether her combat encounter can fire in-game, just not her location. Harmless when the
# mode is "unlocked"/"unlocked_random": these items never enter the pool then (see
# __init__._main_pool_item_names).
combat_helper_npcs = COMBAT_HELPER_NPCS_ALL
combat_helper_item_base = hades2_base_item_id + 316          # +316..+321 (6)
item_table_combat_helpers: Dict[str, ItemData] = {
    f"{npc} Helper": ItemData(combat_helper_item_base + i, True)
    for i, npc in enumerate(combat_helper_npcs)
}

# --- Run-start boost items (New Filler Checks) ---------------------------------
# Rarity Increase is a filler item that boosts your chance of rarer boons; it joins
# the currency filler rotation.
item_table_extras: Dict[str, ItemData] = {
    # REMOVED: "Progressive Start" was superseded by the granular Starting Max Health /
    # Gold / Magick / Armor fillers below and was never placed in the pool.
    # Item id offset 124 retired; do not reuse. Lua handler is left dormant.
    # "Progressive Start": ItemData(hades2_base_item_id + 124, False, useful=True),
    "Rarity Increase": ItemData(hades2_base_item_id + 125, False),
    # Increased Odds of Major Finds: filler that biases exit-door rewards toward Major Finds
    # (boons, Daedalus hammers, Centaur Hearts) over Minor Finds (Ash/Bones/Nectar). A pure
    # odds-boost filler like Rarity Increase; joins the filler currency rotation.
    "Increased Odds of Major Finds": ItemData(hades2_base_item_id + 217, False),
    # REMOVED: Increased Help Odds filler stubbed out (no longer placed in the pool).
    # Item id 151 retired; do not reuse. Lua handler is left dormant.
    # "Increased Help Odds": ItemData(hades2_base_item_id + 151, False),
    # Single unlock (not filler): once received you start each run with a random Arachne armor.
    "Starting Arachne Armor": ItemData(hades2_base_item_id + 152, False, useful=True),
    # Same idea as Starting Arachne Armor, but drawn from another NPC's own personal gift-trait
    # pool (Medea's Curses, Icarus's Benefits, Circe's Blessings). Dionysus/Artemis/Athena/Hades
    # don't have a separate gift mechanic in-game -- their pick is just a random Boon from their
    # own signature pool -- see StartingNpcGifts in Options.py.
    "Starting Medea Curse": ItemData(hades2_base_item_id + 281, False, useful=True),
    "Starting Icarus Invention": ItemData(hades2_base_item_id + 282, False, useful=True),
    "Starting Circe Blessing": ItemData(hades2_base_item_id + 283, False, useful=True),
    "Starting Dionysus Boon": ItemData(hades2_base_item_id + 284, False, useful=True),
    "Starting Artemis Boon": ItemData(hades2_base_item_id + 285, False, useful=True),
    "Starting Athena Boon": ItemData(hades2_base_item_id + 286, False, useful=True),
    "Starting Hades Boon": ItemData(hades2_base_item_id + 287, False, useful=True),
    # Each grants a random Daedalus Hammer upgrade at the start of every run.
    "Daedalus Upgrade": ItemData(hades2_base_item_id + 210, False, useful=True),
    # Each raises the base level of every acquired boon that can be leveled (self-healing
    # top-up applied in the mod, not a gating item -- no location depends on it).
    "Progressive Boon Level": ItemData(hades2_base_item_id + 280, False, useful=True),
    # Empowered Zagreus mode only: steps his stat multiplier down (and eventually below)
    # vanilla strength. Progression: the Zagreus Victory location is gated on holding a
    # threshold share of these (see Rules._set_victory_rules), so the fill algorithm must
    # place enough of them somewhere reachable before that location.
    "Progressive Zagreus Weaken": ItemData(hades2_base_item_id + 218, True, useful=True),
}

# NPC name (as used by Options.StartingNpcGifts / the Lua NPC_GIFT_POOLS table) -> the
# "Starting <NPC> <Gift>" item name it places in the pool.
NPC_GIFT_ITEMS: Dict[str, str] = {
    "Arachne": "Starting Arachne Armor",
    "Medea": "Starting Medea Curse",
    "Icarus": "Starting Icarus Invention",
    "Circe": "Starting Circe Blessing",
    "Dionysus": "Starting Dionysus Boon",
    "Artemis": "Starting Artemis Boon",
    "Athena": "Starting Athena Boon",
    "Hades": "Starting Hades Boon",
}

# --- Progressive start-boost fillers ------------------------------------------
# Each of these permanently raises a starting stat by its configured "value". They join
# the filler currency rotation by their configured "percentage" (see build_filler_pool).
item_table_progressive_filler: Dict[str, ItemData] = {
    "Starting Max Health": ItemData(hades2_base_item_id + 206, False),
    "Starting Max Magick": ItemData(hades2_base_item_id + 207, False),
    "Starting Gold": ItemData(hades2_base_item_id + 208, False),
    "Starting Armor": ItemData(hades2_base_item_id + 209, False),
}

# --- Combined weapon + aspect progressives -------------------------------------
# With AspectSanity=progressive, these replace the per-weapon unlock items and Aspect
# items. The first "Progressive <Weapon>" unlocks that weapon and all of its Aspects;
# each later copy upgrades those Aspects.
# (AspectSanity=randomized/per_aspect handle their own combine cascade on their normal
# aspect items instead -- see item_table_aspects_randomized / item_table_aspects_per_aspect.)
item_table_weapon_combine: Dict[str, ItemData] = {
    f"Progressive {weapon}": ItemData(hades2_base_item_id + 211 + i, True)
    for i, weapon in enumerate(WEAPON_SHORT_NAMES)
}

# --- Incantations (Cauldron unlocks shuffled as items) ------------------------
# The Cauldron is blocked in-game, so these meta/QoL unlocks become AP items: collecting
# one grants its world-upgrade. No check locations (items-only, like aspects/familiars).
# The Lua mod maps each display name to its internal WorldUpgrade id. create_items gates
# them by route/keepsake mode. Five OTHER incantations are auto-granted at connect (not
# items): Consecration of Ashes, Aspects of Night and Darkness, Spreading of Ashes,
# Favored of All Keepsakes, Insight into Offerings.
incantation_always = [
    "Gathering of Ancient Bones", "Doomed Beckoning", "End to Deepest Slumber",
    "End to Dearest Slumber", "End to Dumbest Slumber", "Divination of the Elements",
    "Rite of Vapor-Cleansing", "Rite of Social Solidarity", "Rite of River-Fording",
    # NOTE: the three "End to ___ Slumber" entries above (WakeHypnos tiers) are excluded
    # from the pool below via _INCANTATION_RETIRED, not removed from this list -- doing it
    # that way keeps every other incantation's positional item id stable. Lua's mapping for
    # them (ItemManager.lua) is left dormant, same pattern as other retired items.
    "Empath's Intuition", "Rise of Stygian Wells", "Surge of Stygian Wells",
    "Cleansing of Fountain-Waters", "Purification of Fountain-Waters", "Kindred Keepsakes",
    "Propensity Toward Gold", "Necromantic Influence", "Eyes of Night and Darkness",
    "Summoning of Musical Rhapsody", "Path to Desired Blessings", "Shuffling of Noted Ballads",
    "Bones of Arcane Wisdom", "Gathering of Subterranean Riches", "Bounties of the Infinite Abyss",
    "Ashen Memories of Life", "Nectar of Godly Savor", "Augmentation of Bone Density",
    "Alteration of Familiar Forms",
]
incantation_underworld = [
    "Temporal Fluctuation", "Circles of the Moon", "Woodsy Lifespring", "Briny Lifespring",
    "Golden Lifespring", "Reviving a Mournful Husk", "Circles of Protection", "Exhumed Troves",
    "Surge of Desecrating Pools", "Revival of a Desecrating Pool",
]
incantation_surface = [
    "Surge of Fresh Air", "Summoning a Colony of Bats", "Rush of Fresh Air", "Sandy Lifespring",
    "Arisen Troves", "Frozen Lifespring", "Rage of the Elements",
]
incantation_keepsake_nonprog = ["Quickening of Sentimental Value"]
# Exhumed Troves lives in the underworld list, but is also wanted when the seed is
# surface-only (no underworld), so create_items adds it in that case too.
INCANTATION_SURFACE_ONLY_EXTRA = "Exhumed Troves"

_incantation_order = (incantation_always + incantation_underworld
                      + incantation_surface + incantation_keepsake_nonprog)
incantation_item_base = hades2_base_item_id + 160          # +160..+205 (46)
# Doomed Beckoning unlocks the Moros keepsake check (Rules.KEEPSAKE_ITEM_GATE), so it must
# be progression -- otherwise Archipelago's reachability sweep (progression items only) can
# never collect it and the Moros Keepsake location is flagged unreachable.
_INCANTATION_PROGRESSION = {"Doomed Beckoning"}
# Retired from the pool (see the NOTE by incantation_always): still occupy their positional
# item ids so nothing after them shifts, but create_items (__init__.py) filters them out of
# the actual pool via this set, and they're excluded from the table below too. July 19 cull
# added the 7 QoL/economy ones below: Rite of Vapor-Cleansing/Social Solidarity/River-Fording
# (hub room unlocks, no real gameplay stakes), Gathering of Ancient Bones/Subterranean Riches
# (unused-weapon Bones bonus -- nice but not worth a slot), Summoning of Musical
# Rhapsody/Shuffling of Noted Ballads (the jukebox -- pure cosmetic), Bounties of the Infinite
# Abyss (reward-stand spawn rate, same tier as the Bones ones).
INCANTATION_RETIRED = {"End to Deepest Slumber", "End to Dearest Slumber", "End to Dumbest Slumber",
                       "Augmentation of Bone Density",
                       "Rite of Vapor-Cleansing", "Rite of Social Solidarity", "Rite of River-Fording",
                       "Gathering of Ancient Bones", "Summoning of Musical Rhapsody",
                       "Shuffling of Noted Ballads", "Gathering of Subterranean Riches",
                       "Bounties of the Infinite Abyss"}
# Auto-granted at connect instead of shuffled (July 19 cull): real gameplay effect, but not
# exciting enough to be worth waiting on as a "find" -- same treatment as the 5 QoL
# incantations that were NEVER in the pool to begin with (see ItemManager.lua's
# INCANTATION_START_IDS). Names stay in their positional list (id stability, sync_check
# parity with Lua's INCANTATION_ITEM_TO_ID) but are excluded from the pool below. Route- or
# mode-scoped ones (Propensity Toward Gold, Temporal Fluctuation, Reviving a Mournful Husk,
# Rage of the Elements, Summoning a Colony of Bats, Quickening of Sentimental Value, Allow
# Orpheus to Spawn in Tartarus, Moon Monuments, Erebus Gates) are only actually force-granted
# in-game when their route/mode is active this seed -- see ItemManager.lua's
# apply_conditional_incantation_starts.
INCANTATION_AUTO_GRANTED = {
    "Divination of the Elements", "Empath's Intuition", "Propensity Toward Gold",
    "Path to Desired Blessings", "Alteration of Familiar Forms", "Temporal Fluctuation",
    "Reviving a Mournful Husk", "Rage of the Elements", "Summoning a Colony of Bats",
    "Quickening of Sentimental Value", "Allow Orpheus to Spawn in Tartarus",
    "Moon Monuments", "Erebus Gates",
}
# Folded into one of the 7 combined items below (July 19 simplification pass) instead of
# staying separately named -- same id-reservation/filter treatment as INCANTATION_RETIRED.
# See combined_incantation_counts() and item_table_incantation_combined for the replacements.
INCANTATION_COMBINED_AWAY = {
    # -> "Stygian Wells"
    "Rise of Stygian Wells", "Surge of Stygian Wells",
    "Well of Charon During Runs", "Well of Charon After Bosses",
    # -> "Lifespring/Fountain Rooms"
    "Woodsy Lifespring", "Briny Lifespring", "Golden Lifespring",
    "Sandy Lifespring", "Frozen Lifespring",
    "Tartarus Fountain Chamber", "Asphodel Fountain Chamber", "Elysium Fountain Chamber",
    # -> "Desecrating Pools"
    "Revival of a Desecrating Pool", "Surge of Desecrating Pools",
    "Sell Shops During Runs", "Sell Shops After Bosses",
    # -> "Shrine of Hermes"
    "Rush of Fresh Air", "Surge of Fresh Air",
    # -> "Troves"
    "Exhumed Troves", "Arisen Troves", "Infernal Troves",
    # -> "Keepsake Rack"
    "Kindred Keepsakes", "Post-Boss Keepsake Rack",
    # -> "Gold Urns"
    "Low-Value Gold Urns", "Medium-Value Gold Urns", "High-Value Gold Urns",
}
item_table_incantations: Dict[str, ItemData] = {
    name: ItemData(incantation_item_base + i, name in _INCANTATION_PROGRESSION,
                   useful=name not in _INCANTATION_PROGRESSION)
    for i, name in enumerate(_incantation_order)
    if name not in INCANTATION_RETIRED
    and name not in INCANTATION_AUTO_GRANTED
    and name not in INCANTATION_COMBINED_AWAY
}

# Nightmare incantations (Zagreus' Journey). Confirmed from the mod's own
# Scripts/WorldUpgradeData.lua header comment (22 total) -- excludes the purely cosmetic
# "Rename Bone Hydra to Lernie" (needs 20 boss defeats, no gameplay effect, not worth a
# shuffled-item slot). The first 3 are the mod's own "quest item" incantations (reunion
# questline beats) -- flagged in the design plan as higher-risk to force-grant than a normal
# WorldUpgrade flag flip; verify in-game they don't leave a half-finished scripted state.
incantation_nightmare = [
    "Reunite Orpheus and Eurydice", "Release Sisyphus", "Allow Orpheus to Spawn in Tartarus",
    "Post-Boss Keepsake Rack", "Well of Charon During Runs", "Well of Charon After Bosses",
    "Sell Shops During Runs", "Sell Shops After Bosses",
    "Tartarus Fountain Chamber", "Asphodel Fountain Chamber", "Elysium Fountain Chamber",
    "Low-Value Gold Urns", "Medium-Value Gold Urns", "High-Value Gold Urns",
    "Infernal Troves", "Moon Monuments", "Erebus Gates", "Hades Badges",
    "Orpheus' Lyre", "New Hades I Cosmetics", "New Music for the Music Maker",
]
# "Allow Orpheus to Spawn in Tartarus" USED TO gate the Orpheus keepsake check (Rules.py's
# KEEPSAKE_ITEM_GATE) and be progression for exactly that reason. July 19 cull moved it to
# INCANTATION_AUTO_GRANTED (force-granted whenever Nightmare is active, so Orpheus always
# spawns) -- Rules.py's KEEPSAKE_ITEM_GATE no longer has an "Orpheus" entry, so this set is
# now empty. Left in place (rather than deleted) in case a future incantation needs it.
_INCANTATION_NIGHTMARE_PROGRESSION = set()
# Retired from the pool (mirrors INCANTATION_RETIRED): still occupies its positional item id
# via enumerate so nothing after it shifts, but create_items (__init__.py) filters it out of
# the actual pool, and it's excluded from the table below too. July 19 cull added the 2 quest-
# beat incantations (Reunite Orpheus and Eurydice, Release Sisyphus) -- cosmetic-ish scripted
# story beats, no gameplay stakes, and the design plan already flagged force-granting them as
# higher-risk than a normal flag flip.
INCANTATION_NIGHTMARE_RETIRED = {"New Hades I Cosmetics",
                                 "Reunite Orpheus and Eurydice", "Release Sisyphus"}
incantation_nightmare_item_base = hades2_base_item_id + 246          # +246..+266 (21)
item_table_incantations_nightmare: Dict[str, ItemData] = {
    name: ItemData(incantation_nightmare_item_base + i, name in _INCANTATION_NIGHTMARE_PROGRESSION,
                   useful=name not in _INCANTATION_NIGHTMARE_PROGRESSION)
    for i, name in enumerate(incantation_nightmare)
    if name not in INCANTATION_NIGHTMARE_RETIRED
    and name not in INCANTATION_AUTO_GRANTED
    and name not in INCANTATION_COMBINED_AWAY
}

# --- Combined incantations (July 19 simplification pass) ----------------------------------
# Several same-shape incantations (one per zone/route/tier -- see INCANTATION_COMBINED_AWAY)
# collapse into a single item each: receiving it grants EVERY one of its underlying
# WorldUpgrade flags that's relevant to this seed's active routes, all at once (see
# ItemManager.lua's grant_combined_incantation) -- not a multi-copy progressive item.
# combined_incantation_counts() is really a presence check (1 = include this item this seed,
# 0 = none of its underlying unlocks apply, don't place it) rather than a copy count.
item_table_incantation_combined: Dict[str, ItemData] = {
    "Stygian Wells": ItemData(hades2_base_item_id + 288, False, useful=True),
    "Lifespring/Fountain Rooms": ItemData(hades2_base_item_id + 289, False, useful=True),
    "Desecrating Pools": ItemData(hades2_base_item_id + 290, False, useful=True),
    "Shrine of Hermes": ItemData(hades2_base_item_id + 291, False, useful=True),
    "Troves": ItemData(hades2_base_item_id + 292, False, useful=True),
    "Keepsake Rack": ItemData(hades2_base_item_id + 293, False, useful=True),
    "Gold Urns": ItemData(hades2_base_item_id + 294, False, useful=True),
}


def combined_incantation_counts(underworld_on: bool, surface_on: bool, nightmare_on: bool) -> Dict[str, int]:
    """Whether each of the 7 combined incantation items belongs in this seed's pool (1) or not
    (0) -- Stygian Wells and Keepsake Rack are always present (their base-list halves are
    seed-unconditional); the rest need at least one contributing route active. Each is a
    single item, not a copy count -- see the module note above."""
    return {
        "Stygian Wells": 1,
        "Lifespring/Fountain Rooms": 1 if (underworld_on or surface_on or nightmare_on) else 0,
        "Desecrating Pools": 1 if (underworld_on or nightmare_on) else 0,
        "Shrine of Hermes": 1 if surface_on else 0,
        "Troves": 1 if (underworld_on or surface_on or nightmare_on) else 0,
        "Keepsake Rack": 1,
        "Gold Urns": 1 if nightmare_on else 0,
    }


item_table_incantations = {**item_table_incantations, **item_table_incantations_nightmare,
                           **item_table_incantation_combined}


# --- Event items (boss victories, no real code) -------------------------------
# One "<Boss> Victory" event item per boss across both routes, plus Zagreus (the secret
# superboss -- not tied to either route's zone-boss list, see Rules.py's access rule).
items_table_event: Dict[str, ItemData] = {
    boss_victory(boss): ItemData(None, True, True)
    for route in ROUTE_NAMES for boss in ROUTES[route]["bosses"]
}
items_table_event[boss_victory("Zagreus")] = ItemData(None, True, True)


item_table = {
    **item_table_weapons,
    **item_table_filler,
    **item_table_grasp,
    **item_table_arcana,
    **item_table_arcana_progressive,
    **item_table_vows,
    **item_table_routes,
    **item_table_aspects,
    **item_table_keepsakes,
    **item_table_familiars,
    **item_table_gods,
    **item_table_shop_gods,
    **item_table_god_keepsake_combined,
    **item_table_helper_npcs,
    **item_table_combat_helpers,
    **item_table_extras,
    **item_table_progressive_filler,
    **item_table_weapon_combine,
    **item_table_incantations,
    **items_table_event,
}


# --- Item name groups (for yaml/plando convenience) ---------------------------
group_weapons = {"weapons": list(item_table_weapons) + list(item_table_weapon_combine)}
group_fillers = {"fillers": list(item_table_filler) + list(item_table_progressive_filler)}
group_arcana = {"arcana": list(item_table_arcana) + list(item_table_arcana_progressive)}
group_vows = {"vows": item_table_vows.keys()}
group_aspects = {"aspects": item_table_aspects.keys()}
group_keepsakes = {"keepsakes": item_table_keepsakes.keys()}
group_familiars = {"familiars": item_table_familiars.keys()}
group_incantations = {"incantations": item_table_incantations.keys()}
group_gods = {"gods": list(item_table_gods) + list(item_table_shop_gods)
                       + list(item_table_god_keepsake_combined)}
group_helper_npcs = {"helper_npcs": item_table_helper_npcs.keys()}
group_combat_helpers = {"combat_helpers": item_table_combat_helpers.keys()}

item_name_groups = {
    **group_weapons,
    **group_fillers,
    **group_arcana,
    **group_vows,
    **group_aspects,
    **group_keepsakes,
    **group_familiars,
    **group_incantations,
    **group_gods,
    **group_helper_npcs,
    **group_combat_helpers,
}


# --- Pairing of event locations with their event items ------------------------
# "Beat <Boss>" event location -> "<Boss> Victory" event item, both routes, plus Zagreus.
event_item_pairs: Dict[str, str] = {
    boss_event(boss): boss_victory(boss)
    for route in ROUTE_NAMES for boss in ROUTES[route]["bosses"]
}
event_item_pairs[boss_event("Zagreus")] = boss_victory("Zagreus")


class Hades2Item(Item):
    game = "Hades2Rogue"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        if item_data.progression:
            item_class = ItemClassification.progression
        elif item_data.trap:
            item_class = ItemClassification.trap
        elif item_data.useful:
            item_class = ItemClassification.useful
        else:
            item_class = ItemClassification.filler

        super(Hades2Item, self).__init__(
            name,
            item_class,
            item_data.code, player
        )
