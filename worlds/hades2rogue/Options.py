from dataclasses import dataclass
from typing import Dict, Any
from Options import Range, DeathLink, Choice, StartInventoryPool, PerGameCommonOptions, \
    OptionGroup, DefaultOnToggle, Toggle, OptionSet


# ----------------------- Gameplay decisions -----------------------------------


class IncludedWeapons(OptionSet):
    """
    Which weapons to include in the run. Removing any of these will remove their
    and their aspects items from the item pool, and any locations requiring that
    weapon will or it's aspects will be removed.
    """
    display_name = "Included Weapons"
    valid_keys = frozenset({"Staff", "Blades", "Flames", "Axe", "Skull", "Coat"})
    default = frozenset({"Staff", "Blades", "Flames", "Axe", "Skull", "Coat"})


class InitialWeapon(Choice):
    """Which weapon will you have at the beginning of the run."""
    display_name = "Weapon"
    option_Staff = 0   # Witch's Staff
    option_Blades = 1  # Sister Blades
    option_Flames = 2  # Umbral Flames
    option_Axe = 3     # Moonstone Axe
    option_Skull = 4   # Argent Skull
    option_Coat = 5    # Black Coat
    default = "random"


class AspectSanity(Choice):
    """
    How you'll get the various weapon aspects.
    unlocked: every Aspect is available from the start, fully upgraded.
    randomized: all 24 Aspects are shuffled - the 18 alternates and each weapon's Aspect of
    Melinoe. Each is its own item, granted at max level.
    Your starting weapon begins on a random one of its 4 Aspects, but only at
    level 1. It's leveled to max when you find it's item.
    progressive: you start with only one weapon with Melinoe's Aspect. Each weapon gets "Progressive
    <Weapon>" items; the first unlocks all aspects at level one, the rest level all aspects up.
    per_aspect: all 24 Aspects level independently, each with its own "Progressive
    <Aspect>" item. 5 copies apiece (1 unlock + 4 rank upgrades), 120 items total. Your
    starting weapon begins with a random one of its 4 Aspects at rank 1. The first aspect
    item you receive for a weapon also unlocks that weapon.
    """
    display_name = "AspectSanity"
    option_unlocked = 0
    option_randomized = 1
    option_progressive = 2
    option_per_aspect = 3
    default = 2


class IncludedAspects(Range):
    """
    If aspectsanity is set to randomized or per_aspect
    How many of each weapons aspects should be accessible.
    Any locations requiring any removed aspects will be removed.
    """
    display_name = "Included Aspects"
    range_start = 1
    range_end = 4
    default = 4


class LocationSystem(Choice):
    """
    How to handle base locations.
    Room_based: Each location is the first time you clear that many rooms/encounters in one
    run. For example; Room Check 9 sends the first time you clear 9 encounters in one run.
    Point_based: Each location is a point total you must accumulate, you get points equal
    to a room's depth when you clear it. Use this for much longer APs, and it will likely
    be quite repetitive.
    Per_Weapon_Room_Based: Like room_based, but there are separate pools for each weapon.
    """
    display_name = "Location System"
    option_point_based = 0
    option_room_based = 1
    option_per_weapon_room_based = 2
    default = 1


class ScoreRewardsAmount(Range):
    """
    Point_based only. How many score locations are there? If you set each route to have
    it's own pool later, each route will have a pool this big. If there aren't enough
    locations to fulfill the minimum item pool, this will be increased accordingly. More
    locations means more filler items, which are beneficial, but not required.
    """
    display_name = "Score Rewards Amount"
    range_start = 40
    range_end = 1000
    default = 100


class SeparateChecks(Choice):
    """
    When you've included more than one route: does each route get its own full set of
    checks, or do they share one pool?
    separate_pools: Every route gets their own locations, meaning you'll have to
    thoroughly explore each of your routes.
    combine_pools: the routes share one pool. Score checks stop being route-specific:
    there are 200 of them total, every route's rooms bank into the same points pool, and
    you could earn all 200 without ever leaving one route. Each room check is likewise
    earned the first time you clear that depth on ANY route.
    """
    display_name = "Separate Checks"
    option_separate_pools = 0
    option_combine_pools = 1
    default = 0


class EnemyLocations(DefaultOnToggle):
    """Add locations for the first time you defeat each enemy type."""
    display_name = "Enemy Locations"


class NpcLocations(DefaultOnToggle):
    """Add locations for the first time you speak to each NPC."""
    display_name = "NPC Locations"


class GraspCount(Range):
    """How many Progressive Grasp items in the item pool."""
    display_name = "Grasp Count"
    range_start = 1
    range_end = 30
    default = 6


class GraspIntervals(Range):
    """How much each Progressive Grasp raises your maximum Grasp."""
    display_name = "Grasp Intervals"
    range_start = 0
    range_end = 10
    default = 5


class ArcanaSanity(Choice):
    """
    How Arcana Cards are obtained.
    arcana: each card is unlocked by an item at max level and can't be purchased.
    progressive_arcana: each card gets multiple progressive items - the first unlocks it,
    the rest upgrade it. Cards can't be upgraded any other way.
    """
    display_name = "ArcanaSanity"
    option_Arcana = 1
    option_Progressive_Arcana = 2
    default = 2


class KeepsakeSanity(Choice):
    """
    How Keepsakes are handled.
    false: unchanged from the base game.
    randomized: Adds a location for earning each keepsake, and adds each keepsake to the item pool.
    progressive: Adds a location for earning each keepsake, and adds 3 "Progressive
    Keepsake" items. The first unlocks all keepsakes at level one, the next two level
    them up. Normal keepsake leveling is blocked.
    """
    display_name = "KeepsakeSanity"
    option_false = 0
    option_randomized = 1
    option_progressive = 2
    default = 1


class PetSanity(Choice):
    """
    How Familiars (pets: Frinos, Toula, Raki, Hecuba, Gale) are handled. Items only - no new check locations.
    unlocked: every familiar is available from the start.
    randomized: each familiar becomes its own item; you start with none and unlock each
    at maximum bond when you receive its item.
    progressive: a Progressive Familiar item is added - the first unlocks all familiars,
    the rest upgrade their bonds. Normal familiar unlocking/bonding is blocked.
    """
    display_name = "PetSanity"
    option_unlocked = 0
    option_randomized = 1
    option_progressive = 2
    default = 1


class HelperRoomSanity(Choice):
    """
    How helper NPC story rooms (Arachne, Narcissus, Echo, Hades, Medea, Circe, Dionysus,
    and on Nightmare: Sisyphus, Eurydice, Patroclus) are handled.
    unlocked: all helpers are unlocked from the start and appear only in their normal rooms.
    items: helpers are unlocked via items in the item pool; they appear only in their normal rooms.
    unlocked_random: same as unlocked, but they can appear in any of the other helpers' rooms too.
    items_random: same as items, but they can appear in any of the other helpers' rooms too.
    """
    display_name = "Helper Room Sanity"
    option_unlocked = 0
    option_items = 1
    option_unlocked_random = 2
    option_items_random = 3
    default = 2


class CombatHelperSanity(Choice):
    """
    How to handle the various helper NPCs that assist in combat mid-run (Artemis, Nemesis,
    Heracles, Icarus, Athena, Thanatos).
    unlocked: all NPC helpers are automatically unlocked from the beginning, and show up
    where they're supposed to.
    items: all NPC helpers are unlocked via items in the item pool, and they show up where
    they're supposed to.
    unlocked_random: same as unlocked, but they can all show up in different places than
    they normally can.
    items_random: same as items, but they can all show up in different places than they
    normally can.
    """
    display_name = "Combat Helper Sanity"
    option_unlocked = 0
    option_items = 1
    option_unlocked_random = 2
    option_items_random = 3
    default = 2


class GodSanity(Choice):
    """
    Locks each god's boons behind a check, so until you get the "Zeus" item, boons from him
    will never spawn.
    unlocked: All gods are available from the beginning. Logically all are available at the
    same time, which could lead to some unlucky missed items.
    onions: Anytime a boon would spawn from a god you haven't unlocked, it is replaced with
    an Onion. This means that even once you've unlocked some gods, there will be runs where
    you don't see any of them.
    no_waste_less_odds: Each time a god is unlocked, the % chance of a boon spawning
    increases, but every boon that spawns will always be from a god you've unlocked.
    no_waste_same_odds: Boons spawn at the normal rate no matter how many gods are unlocked,
    but every one is still guaranteed to be from a god you've unlocked - this makes you very
    strong early on, since it's easy to get only boons that work very well together.
    """
    display_name = "GodSanity"
    option_unlocked = 0
    option_onions = 1
    option_no_waste_less_odds = 2
    option_no_waste_same_odds = 3
    default = 0


class Hades2DeathLink(DeathLink):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    default = 1


class DeathLinkPercent(Range):
    """
    When you receive a DeathLink, how much of your health you'll lose, as a percentage of
    your maximum health. Or, set to 0 to end the run regardless of available death defiances.
    """
    display_name = "DeathLink Damage Percent"
    range_start = 0
    range_end = 100
    default = 100


class DeathLinkAmnesty(Range):
    """
    How many times you die in a row before it sends a Deathlink to everyone else. 0
    means you'll never send, only receive
    """
    display_name = "DeathLink Deaths To Send"
    range_start = 0
    range_end = 5
    default = 1


# -------------------- Reverse Vow (Oath of the Unseen) ------------------------


class ReverseVow(DefaultOnToggle):
    """
    Start each run with the vows below already active (raising difficulty); each is then
    removed, one at a time, by items found in the multiworld.
    """
    display_name = "Reverse Vow"


class _VowRange(Range):
    range_start = 0
    range_end = 3
    default = 1


class VowPain(_VowRange):
    """How many levels of Vow of Pain to start with (foes deal more damage)."""
    display_name = "Vow of Pain"
    range_end = 3


class VowGrit(_VowRange):
    """How many levels of Vow of Grit to start with (foes have more health)."""
    display_name = "Vow of Grit"
    range_end = 3


class VowWards(_VowRange):
    """How many levels of Vow of Wards to start with (foes gain Barrier)."""
    display_name = "Vow of Wards"
    range_end = 2


class VowFrenzy(_VowRange):
    """How many levels of Vow of Frenzy to start with (foes are faster)."""
    display_name = "Vow of Frenzy"
    range_end = 2


class VowHordes(_VowRange):
    """How many levels of Vow of Hordes to start with (more foes)."""
    display_name = "Vow of Hordes"
    range_end = 3


class VowMenace(_VowRange):
    """How many levels of Vow of Menace to start with (foes from the next region)."""
    display_name = "Vow of Menace"
    range_end = 2


class VowReturn(_VowRange):
    """How many levels of Vow of Return to start with (slain foes may revive)."""
    display_name = "Vow of Return"
    range_end = 2


class VowFangs(_VowRange):
    """How many levels of Vow of Fangs to start with (armored foes gain perks)."""
    display_name = "Vow of Fangs"
    range_end = 2


class VowScars(_VowRange):
    """How many levels of Vow of Scars to start with (healing is less effective)."""
    display_name = "Vow of Scars"
    range_end = 3


class VowDebt(_VowRange):
    """How many levels of Vow of Debt to start with (Higher gold costs)."""
    display_name = "Vow of Debt"
    range_end = 2


class VowShadow(_VowRange):
    """How many levels of Vow of Shadow to start with (Shadow Servants)."""
    display_name = "Vow of Shadow"
    range_end = 1
    default = 0


class VowForfeit(_VowRange):
    """How many levels of Vow of Forfeit to start with (first Boon becomes Red Onion)."""
    display_name = "Vow of Forfeit"
    range_end = 1
    default = 0


class VowTime(_VowRange):
    """How many levels of Vow of Time to start with (time limit per region)."""
    display_name = "Vow of Time"
    range_end = 3


class VowVoid(_VowRange):
    """How many levels of Vow of Void to start with (less Grasp for Arcana)."""
    display_name = "Vow of Void"
    range_end = 4
    default = 2


class VowHubris(_VowRange):
    """How many levels of Vow of Hubris to start with (Primes Magick after Boons)."""
    display_name = "Vow of Hubris"
    range_end = 2


class VowDenial(_VowRange):
    """How many levels of Vow of Denial to start with (unpicked blessings vanish)."""
    display_name = "Vow of Denial"
    range_end = 1
    default = 0


class VowRivals(_VowRange):
    """How many levels of Vow of Rivals to start with (Guardians are stronger)."""
    display_name = "Vow of Rivals"
    range_end = 4
    default = 2


class ReverseRivals(DefaultOnToggle):
    """
    Reverse which Guardians the Vow of Rivals strengthens: this makes Chronos and Typhon
    the last boss to return to normal.
    """
    display_name = "Reverse Rivals"


# -------------------- Routes & Endgame settings -------------------------------


class GoalsRequired(OptionSet):
    """
    Which routes' final bosses should be included in the goal (Chronos for Underworld,
    Typhon for Surface, Hades for Nightmare -- Zagreus is separate, see Goal Requires
    Zagreus below). Nightmare requires the "Zagreus Journey" mod by NikkelM, which is a
    dependency of the Archipelago mod, but will only work if Hades 1 is installed.
    Meaning don't include Nightmare unless you have Hades 1 installed/available to be
    installed.
    Valid options are: Underworld, Surface, and Nightmare.
    """
    display_name = "Goals Required"
    valid_keys = frozenset({"Underworld", "Surface", "Nightmare"})
    default = frozenset({"Underworld", "Surface"})


class GoalRequiresZagreus(Toggle):
    """Whether defeating Zagreus is part of your Goal."""
    display_name = "Goal Requires Zagreus"


class GoalMode(Choice):
    """
    How the toggled-on Goal bosses above combine.
    all_selected: every toggled-on boss must be defeated.
    any_selected: defeating any one of the toggled-on bosses is enough.
    """
    display_name = "Goal Mode"
    option_all_selected = 0
    option_any_selected = 1
    default = 1


class ZagreusEncounterMode(Choice):
    """How Zagreus fights appear (only matters if Zagreus is part of your Goal):
    Vanilla: Zagreus fights appear how they normally do in the late game.
    Empowered: Zagreus fights appear how they normally do, but Zagreus starts heavily
    empowered. Progressive Zagreus Weaken items are added to the multiworld that weaken him
    back down to, and eventually below, his normal strength.
    Final Challenge: Defeating any route's final boss spawns a contract to go fight Zagreus
    instead of ending the run."""
    display_name = "Zagreus Encounter Mode"
    option_vanilla = 0
    option_empowered = 1
    option_final_challenge = 2
    default = 1


class ZagreusWeakenTiers(Range):
    """
    If Zagreus Encounter Mode is set to Empowered, how many "Progressive Zagreus Weaken"
    items exist to weaken him. Setting more will not make him weaker, just weaken him in smaller
    chunks
    """
    display_name = "Zagreus Weaken Tiers"
    range_start = 1
    range_end = 10
    default = 5


class ZagreusDefeatsNeeded(Range):
    """How many times you must defeat Zagreus to satisfy the Zagreus part of the goal."""
    display_name = "Zagreus Defeats Needed"
    range_start = 1
    range_end = 20
    default = 1


class IncludeRegions(OptionSet):
    """
    Which routes will be included: Underworld (Erebus/Oceanus/Fields of Mourning/Tartarus),
    Surface (City of Ephyra/Rift of Thessaly/Mount Olympus/The Summit), and Nightmare (the
    original Hades 1 route -- Tartarus/Asphodel/Elysium/Styx).
    Nightmare requires the "Zagreus Journey" mod by NikkelM, which is a dependency of
    the Archipelago mod, but will only work if Hades 1 is installed.
    Meaning don't include Nightmare unless you have Hades 1 installed/available to be installed.

    Valid options are: Underworld, Surface, and Nightmare.
    """
    display_name = "Include Regions"
    valid_keys = frozenset({"Underworld", "Surface", "Nightmare"})
    default = frozenset({"Underworld", "Surface"})


class IncludeZagreusJourney(Toggle):
    """
    Whether to include any content from NikkelM's Zagreus' Journey mod.
    When off: Nightmare is removed as a playable route/goal
    regardless of what Include Regions/Goals Required select, its 7 keepsakes (Sisyphus/
    Eurydice/Patroclus/Orpheus/Megaera/Thanatos/Achilles) never enter the item pool, and
    none of Sisyphus/Eurydice/Patroclus/Thanatos can be randomized into other routes' rooms
    either.
    """
    display_name = "Include Zagreus Journey"


class LockRoutes(DefaultOnToggle):
    """
    Lock each route's regions behind its progressive route items (Progressive Underworld
    / Progressive Surface / Progressive Nightmare).
    """
    display_name = "Lock Routes"


class StartingRoute(Choice):
    """
    If lock_routes is on, which route is open from the start.
    Picking a route you didn't include will result in a random route you did include.
    """
    display_name = "Starting Route"
    option_random_1_route = 0
    option_underworld = 1
    option_surface = 2
    option_all = 3
    option_nightmare = 4
    default = 0


class UnderworldWinsNeeded(Range):
    """How many times you must win an Underworld run to mark the goal as complete."""
    display_name = "Underworld Wins Needed"
    range_start = 1
    range_end = 20
    default = 1


class SurfaceWinsNeeded(Range):
    """How many times you must win a Surface run to mark the goal as complete."""
    display_name = "Surface Wins Needed"
    range_start = 1
    range_end = 20
    default = 1


class NightmareWinsNeeded(Range):
    """How many times you must win a Nightmare run to mark the goal as complete."""
    display_name = "Nightmare Wins Needed"
    range_start = 1
    range_end = 20
    default = 1


class WeaponsClearsNeeded(Range):
    """
    How many different weapons you must use to defeat any boss. Meaning defeating Chronos
    with the axe and Typhon with the blades would count as 2 weapons.
    """
    display_name = "Weapons Clears Needed"
    range_start = 1
    range_end = 6
    default = 1


# ----------------------- Filler item proportions ------------------------------
# The 4 meta-progression currencies. Each currency has a "value" (how much you
# receive per item) and a "percentage" (its share of the filler pool). If the
# percentages don't sum to 100 they are treated as proportions.


class NectarPackValue(Range):
    """Amount of Nectar granted per Nectar item."""
    display_name = "Nectar Pack Value"
    range_start = 0
    range_end = 50
    default = 2


class NectarPackPercentage(Range):
    """Share of the filler pool that is Nectar."""
    display_name = "Nectar Pack Percentage"
    range_start = 0
    range_end = 100
    default = 5


class StartingHealthValue(Range):
    """How much max health each Starting Max Health item grants."""
    display_name = "Starting Health Value"
    range_start = 0
    range_end = 50
    default = 20


class StartingHealthPercentage(Range):
    """Share of the filler pool that is Max Health."""
    display_name = "Starting Health Percentage"
    range_start = 0
    range_end = 100
    default = 15


class StartingMagickValue(Range):
    """How much max Magick each Starting Max Magick item grants."""
    display_name = "Starting Magick Value"
    range_start = 0
    range_end = 50
    default = 2


class StartingMagickPercentage(Range):
    """Share of the filler pool that is Max Magick."""
    display_name = "Starting Magick Percentage"
    range_start = 0
    range_end = 100
    default = 15


class StartingGoldValue(Range):
    """How much run-start gold each Starting Gold item grants."""
    display_name = "Starting Gold Value"
    range_start = 1
    range_end = 100
    default = 10


class StartingGoldPercentage(Range):
    """Share of the filler pool that is Starting Gold."""
    display_name = "Starting Gold Percentage"
    range_start = 0
    range_end = 100
    default = 15


class StartingArmorValue(Range):
    """How much run-start armor each Starting Armor item grants."""
    display_name = "Starting Armor Value"
    range_start = 1
    range_end = 100
    default = 10


class StartingArmorPercentage(Range):
    """Share of the filler pool that is Starting Armor."""
    display_name = "Starting Armor Percentage"
    range_start = 0
    range_end = 100
    default = 15


class RarityIncreasePercentage(Range):
    """
    Share of the filler pool that is Rarity Increase. Each one permanently raises your
    odds of higher-rarity boons.
    """
    display_name = "Rarity Increase Percentage"
    range_start = 0
    range_end = 100
    default = 15


class MajorFindsPercentage(Range):
    """
    Share of the filler pool that is Increased Odds of Major Finds. Each one nudges door
    rewards toward Major Finds (Boons, Daedalus Hammers, Centaur Hearts) and away from
    Minor Finds (Bones, Ash, Nectar).
    """
    display_name = "Major Finds Percentage"
    range_start = 0
    range_end = 100
    default = 10


# REMOVED: Increased Help Odds filler did not pan out as a meaningful mechanic.
# Option stubbed out (kept for reference / possible revival). See also Items.py and __init__.py.
# class HelpOddsPercentage(Range):
#     """Share of the filler pool that is Increased Help Odds (more chance an NPC, e.g. Artemis, shows up to help during a run). 0 = none."""
#     display_name = "Increased Help Odds Percentage"
#     range_start = 0
#     range_end = 100
#     default = 10


# REMOVED: Ashes filler stubbed out. Item id offset retired; do not reuse. See also
# Items.py and __init__.py.
# class AshesPackValue(Range):
#     """Amount of Ashes granted per Ashes item."""
#     display_name = "Ashes Pack Value"
#     range_start = 0
#     range_end = 1000
#     default = 100
#
#
# class AshesPackPercentage(Range):
#     """Share of the filler pool that is Ashes. I don't recommend this if Arcanasanity is on."""
#     display_name = "Ashes Pack Percentage"
#     range_start = 0
#     range_end = 100
#     default = 0


# REMOVED: Psyche filler stubbed out. GraspSanity is always on now, and Psyche has no sink
# in this mod once it is (its only spend, raising the Grasp cap, is fully item-gated), so it
# was always force-dropped from the filler pool regardless of these settings -- the options
# did nothing. Item id offset retired; do not reuse. See also Items.py and __init__.py.
# class PsychePackValue(Range):
#     """Amount of Psyche granted per Psyche item."""
#     display_name = "Psyche Pack Value"
#     range_start = 0
#     range_end = 500
#     default = 20
#
#
# class PsychePackPercentage(Range):
#     """Share of the filler pool that is Psyche."""
#     display_name = "Psyche Pack Percentage"
#     range_start = 0
#     range_end = 100
#     default = 0


# REMOVED: Bones filler stubbed out. Bones has no sink in this mod (its only spend,
# Cauldron incantations, is blocked entirely), so it was always force-dropped from the
# filler pool regardless of these settings -- the options did nothing. Item id offsets
# retired; do not reuse. See also Items.py and __init__.py.
# class BonesPackValue(Range):
#     """Amount of Bones granted per Bones item."""
#     display_name = "Bones Pack Value"
#     range_start = 0
#     range_end = 500
#     default = 20
#
#
# class BonesPackPercentage(Range):
#     """Share of the filler pool that is Bones."""
#     display_name = "Bones Pack Percentage"
#     range_start = 0
#     range_end = 100
#     default = 0


# REMOVED: Moon Dust filler stubbed out. Item id offset retired; do not reuse. See also
# Items.py and __init__.py.
# class MoonDustPackValue(Range):
#     """Amount of Moon dust granted per Moon dust item."""
#     display_name = "Moon Dust Pack Value"
#     range_start = 0
#     range_end = 50
#     default = 2
#
#
# class MoonDustPackPercentage(Range):
#     """Share of the filler pool that is Moon Dust. I don't recommend this if Arcanasanity is progressive_arcana."""
#     display_name = "Moon Dust Pack Percentage"
#     range_start = 0
#     range_end = 100
#     default = 0


class StartingNpcGifts(OptionSet):
    """
    For each NPC you add, it adds an item to the item pool that grants you a random one of the
    boons they would normally give you if you ran into them during a run
    Valid options are: Arachne, Artemis, Athena, Circe, Dionysus, Hades, Icarus, and Medea.
    All but Medea are defaulted, as some of Medea's curses can negatively impact your runs.
    """
    display_name = "Starting NPC Gifts"
    valid_keys = frozenset({
        "Arachne", "Medea", "Icarus", "Circe", "Dionysus", "Artemis", "Athena", "Hades",
    })
    default = frozenset({"Arachne", "Artemis", "Athena", "Circe", "Dionysus", "Hades", "Icarus"})


class DaedalusUpgrade(Range):
    """
    Adds this many Daedalus Upgrade items to the pool. Each one grants a random Daedalus
    Hammer upgrade for your equipped weapon at the start of each run.
    """
    display_name = "Daedalus Upgrade"
    range_start = 0
    range_end = 5
    default = 3


class ProgressiveBoonLevel(Range):
    """
    Adds this many Progressive Boon Level items to the pool. Each one raises the base level
    of all acquired boons that can be leveled (most Common/Rare/Epic/Heroic boons; Duo and
    Legendary boons can't level and are unaffected). 0 removes the item from the pool.
    """
    display_name = "Progressive Boon Level"
    range_start = 0
    range_end = 10
    default = 3


# ------------------------------ Options dataclass -----------------------------


@dataclass
class Hades2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    # Weapon Options
    included_weapons: IncludedWeapons
    initial_weapon: InitialWeapon
    aspectsanity: AspectSanity
    included_aspects: IncludedAspects
    # Location Options
    location_system: LocationSystem
    score_rewards_amount: ScoreRewardsAmount
    separate_checks: SeparateChecks
    enemy_locations: EnemyLocations
    npc_locations: NpcLocations
    # Item Options
    grasp_count: GraspCount
    grasp_intervals: GraspIntervals
    arcanasanity: ArcanaSanity
    keepsakesanity: KeepsakeSanity
    petsanity: PetSanity
    helper_room_sanity: HelperRoomSanity
    combat_helper_sanity: CombatHelperSanity
    godsanity: GodSanity
    # Deathlink
    deathlink: Hades2DeathLink
    deathlink_percent: DeathLinkPercent
    deathlink_amnesty: DeathLinkAmnesty
    # Vow Options
    reverse_vow: ReverseVow
    vow_pain: VowPain
    vow_grit: VowGrit
    vow_wards: VowWards
    vow_frenzy: VowFrenzy
    vow_hordes: VowHordes
    vow_menace: VowMenace
    vow_return: VowReturn
    vow_fangs: VowFangs
    vow_scars: VowScars
    vow_debt: VowDebt
    vow_shadow: VowShadow
    vow_forfeit: VowForfeit
    vow_time: VowTime
    vow_void: VowVoid
    vow_hubris: VowHubris
    vow_denial: VowDenial
    vow_rivals: VowRivals
    reverse_rivals: ReverseRivals
    # Goal & Route Options
    goals_required: GoalsRequired
    goal_requires_zagreus: GoalRequiresZagreus
    goal_mode: GoalMode
    zagreus_encounter_mode: ZagreusEncounterMode
    zagreus_weaken_tiers: ZagreusWeakenTiers
    include_regions: IncludeRegions
    include_zagreus_journey: IncludeZagreusJourney
    lock_routes: LockRoutes
    starting_route: StartingRoute
    underworld_wins_needed: UnderworldWinsNeeded
    surface_wins_needed: SurfaceWinsNeeded
    nightmare_wins_needed: NightmareWinsNeeded
    zagreus_defeats_needed: ZagreusDefeatsNeeded
    weapons_clears_needed: WeaponsClearsNeeded
    # Misc Options
    starting_npc_gifts: StartingNpcGifts
    daedalus_upgrade: DaedalusUpgrade
    progressive_boon_level: ProgressiveBoonLevel
    # Filler Options
    nectar_pack_value: NectarPackValue
    nectar_pack_percentage: NectarPackPercentage
    starting_health_value: StartingHealthValue
    starting_health_percentage: StartingHealthPercentage
    starting_magick_value: StartingMagickValue
    starting_magick_percentage: StartingMagickPercentage
    starting_gold_value: StartingGoldValue
    starting_gold_percentage: StartingGoldPercentage
    starting_armor_value: StartingArmorValue
    starting_armor_percentage: StartingArmorPercentage
    rarity_increase_percentage: RarityIncreasePercentage
    major_finds_percentage: MajorFindsPercentage
    # help_odds_percentage: HelpOddsPercentage  # REMOVED: Increased Help Odds stubbed out
    # ashes_pack_value / ashes_pack_percentage: REMOVED, see Options.py comment above
    # psyche_pack_value / psyche_pack_percentage: REMOVED, see Options.py comment above
    # bones_pack_value / bones_pack_percentage: REMOVED, see Options.py comment above
    # moon_dust_pack_value / moon_dust_pack_percentage: REMOVED, see Options.py comment above


# ------------------------------ Option groups ---------------------------------
# Group names double as the section headers in the generated template; the leading/
# trailing spaces in " Item Options " are intentional (they centre the title in its box).


hades2_option_groups = [
    OptionGroup("Weapon Options", [
        IncludedWeapons,
        InitialWeapon,
        AspectSanity,
        IncludedAspects,
    ]),
    OptionGroup("Location Options", [
        LocationSystem,
        ScoreRewardsAmount,
        SeparateChecks,
        EnemyLocations,
        NpcLocations,
    ]),
    OptionGroup(" Item Options ", [
        GraspCount,
        GraspIntervals,
        ArcanaSanity,
        KeepsakeSanity,
        PetSanity,
        HelperRoomSanity,
        CombatHelperSanity,
        GodSanity,
    ]),
    OptionGroup("Deathlink", [
        Hades2DeathLink,
        DeathLinkPercent,
        DeathLinkAmnesty,
    ]),
    OptionGroup("Vow Options", [
        ReverseVow,
        VowPain, VowGrit, VowWards, VowFrenzy, VowHordes, VowMenace, VowReturn,
        VowFangs, VowScars, VowDebt, VowShadow, VowForfeit, VowTime, VowVoid,
        VowHubris, VowDenial, VowRivals,
        ReverseRivals,
    ]),
    OptionGroup("Goal & Route Options", [
        GoalsRequired,
        GoalRequiresZagreus,
        GoalMode,
        ZagreusEncounterMode,
        ZagreusWeakenTiers,
        IncludeRegions,
        IncludeZagreusJourney,
        LockRoutes,
        StartingRoute,
        UnderworldWinsNeeded,
        SurfaceWinsNeeded,
        NightmareWinsNeeded,
        ZagreusDefeatsNeeded,
        WeaponsClearsNeeded,
    ]),
    OptionGroup("Misc Options", [
        StartingNpcGifts,
        DaedalusUpgrade,
        ProgressiveBoonLevel,
    ]),
    OptionGroup("Filler Options", [
        NectarPackValue,
        NectarPackPercentage,
        StartingHealthValue,
        StartingHealthPercentage,
        StartingMagickValue,
        StartingMagickPercentage,
        StartingGoldValue,
        StartingGoldPercentage,
        StartingArmorValue,
        StartingArmorPercentage,
        RarityIncreasePercentage,
        MajorFindsPercentage,
        # HelpOddsPercentage,  # REMOVED: Increased Help Odds stubbed out
        # AshesPackValue, AshesPackPercentage,  # REMOVED: Ashes filler stubbed out
        # PsychePackValue, PsychePackPercentage,  # REMOVED: Psyche filler stubbed out
        # BonesPackValue, BonesPackPercentage,  # REMOVED: Bones filler stubbed out
        # MoonDustPackValue, MoonDustPackPercentage,  # REMOVED: Moon Dust filler stubbed out
    ]),
]


# ------------------------------ Presets ---------------------------------------

hades2_option_presets: Dict[str, Dict[str, Any]] = {
    "Standard": {
        "score_rewards_amount": 100,
        "underworld_wins_needed": 1,
        "weapons_clears_needed": 1,
    },
}
