import math
from typing import TYPE_CHECKING
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule
from .Routes import ROUTES, UNDERWORLD, SURFACE, NIGHTMARE, boss_event, boss_victory, \
    active_routes, NPC_ROUTE_LOCK, NPC_RANDOMIZED_HELPERS, NPC_RANDOMIZED_ZONE_INDEX, \
    GOAL_BOSSES, ALL_SELECTED, goal_includes, COMBAT_HELPER_NPCS, combat_helper_native_fallback
from .Items import WEAPON_SHORT_NAMES, arcana_titles, keepsake_titles, aspect_titles, \
    ASPECT_BASE_TITLE_BY_WEAPON, vow_names, ASPECT_MAX_RANK, godsanity_gods, godsanity_shop_gods, \
    helper_story_npcs, helper_story_npcs_nightmare, GOD_KEEPSAKE_COMBINED_GODS, GOD_KEEPSAKE_TITLE, \
    KEEPSAKE_PROGRESSIVE_COUNT
from .Locations import combine_active, _score_count_for, _combined_room_count, \
    _combined_score_count, COMBINED_SCORE_PREFIX, _zone_bounds, SHARED_ENEMY_ZONES, \
    ENEMY_BY_ZONE, MINIBOSS_ENEMY_NAMES, MINIBOSS_ZONE_OVERRIDE, \
    ZAGREUS_MET_LOCATION, ZAGREUS_DEFEATED_LOCATION, NPC_INTRO

if TYPE_CHECKING:
    from . import Hades2World

# Weapons required to beat each of a route's 4 bosses (index 0..2), and to beat the 4th/final
# boss (FINAL_WEAPONS). These gate the BOSS ITSELF (see BOSS_TIER_PERCENT below), not just the
# zone-exit that follows it -- see the July 17 tightening pass. Trimmed July 17 (later same day,
# generation-failure pass): the July 17 tightening left the ramp at 2/3/5/6 -- landing on 5 and
# then 6 back-to-back for the last two bosses forced almost the entire weapon pool in hand before
# the 3rd boss, well before the fill algorithm has placed enough progression items. Smoothed to a
# steady 2/3/4/5 ramp; still requires real weapon variety without demanding literally the whole
# 6-weapon pool.
ZONE_WEAPON_GATES = [2, 3, 4]
FINAL_WEAPONS = 5

# Location-system option values (match Options.LocationSystem / Locations.py).
POINT_BASED = 0
ROOM_BASED = 1
PER_WEAPON_ROOM_BASED = 2

# --- Keepsakes (July 17 stricter tiers) ---------------------------------------
# Keepsake check locations are named "<NPC> Keepsake" (see Locations.location_keepsakes), and
# "Met <NPC>" carries the identical rule (see _set_keepsake_rules). Every threshold below is a
# percentage of the full keepsake pool (_keepsake_pool_size) -- all keepsake_titles actually in
# play are shuffled items even the 4 with no check location (Time Piece/Calling Card/Jeweled Pom/
# Skull Earring still count toward _hades2_keepsake_count), so this is a stable denominator
# regardless of KeepsakeSanity mode.
_KEEPSAKE_NIGHTMARE_TITLE_COUNT = 7  # keep in sync with Items._KEEPSAKE_NIGHTMARE_COUNT


def _keepsake_pool_size(options) -> int:
    """40 keepsake titles normally; 33 when IncludeZagreusJourney is off, since the 7
    Nightmare-cast keepsakes (Items.KEEPSAKE_NIGHTMARE_TITLES) never enter the pool then."""
    if getattr(options, "include_zagreus_journey", True):
        return 40
    return 40 - _KEEPSAKE_NIGHTMARE_TITLE_COUNT

# Free tier: no rule at all -- reachable at the Crossroads from the very first run.
KEEPSAKE_FREE = {"Hecate", "Nemesis", "Odysseus", "Dora", "Hypnos", "Skelly"}

# The 12 boon-giving Olympians (all the old soft tiers' gods, now unified into one tier) open
# together once you've earned 25% of the keepsake pool.
KEEPSAKE_BOON_GODS = {
    "Aphrodite", "Apollo", "Ares", "Demeter", "Hephaestus", "Hera",
    "Hestia", "Poseidon", "Zeus", "Hermes", "Chaos", "Selene",
}
KEEPSAKE_BOON_GODS_PCT = 0.25

# Charon isn't route-locked (no area gate, like the boon gods above), but isn't a boon god
# either -- put in Tier 1 (10%, KEEPSAKE_HARD_TIER_PCT[1]) per user request rather than left
# ungated or folded into the 25% bucket.
KEEPSAKE_FLAT_TIER1 = {"Charon"}

# Hard keepsakes: (route, area index, tier) - require reaching that route's area AND owning
# enough keepsakes for the tier (KEEPSAKE_HARD_TIER_PCT below).
# July 18: most of these NPCs are now RANDOMIZED HELPERS (Routes.NPC_RANDOMIZED_HELPERS) --
# the story-room / combat-assist randomizer dependencies can produce them on any active
# route, so for them the (route, area) columns here are DOCUMENTATION of their native home
# only: _set_keepsake_rules ignores both and gates on "any active route's earliest hosting
# zone reachable" (NPC_RANDOMIZED_EARLIEST_ZONE) instead. Only the tier column still applies
# to everyone. The non-randomized entries (Eris, Orpheus, Achilles -- still in
# NPC_ROUTE_LOCK) keep the full native (route, area) gate, and their location is dropped
# entirely when their route isn't in the seed (Locations._route_locked_out).
# Tiers 1-4 preserve the original relative ordering of each NPC's old flat threshold (0/4/8/10
# mapped onto tiers 1/2/3/4 in the same order) -- only the actual counts got stricter.
KEEPSAKE_HARD = {
    "Arachne":   (UNDERWORLD, 0, 1),
    "Artemis":   (UNDERWORLD, 0, 2),
    "Narcissus": (UNDERWORLD, 1, 2),
    "Echo":      (UNDERWORLD, 2, 3),
    "Heracles":  (SURFACE, 0, 3),
    "Medea":     (SURFACE, 0, 3),
    "Circe":     (SURFACE, 1, 4),
    "Icarus":    (SURFACE, 1, 4),
    "Eris":      (SURFACE, 1, 2),
    "Athena":    (SURFACE, 2, 4),
    "Dionysus":  (SURFACE, 2, 4),
    # Nightmare cast, zones corrected July 16 against the mods' actual spawn data (each
    # verified in the installed Zagreus' Journey source): Sisyphus's story room A_Story01 is
    # TARTARUS (zone 0 -- was wrongly Asphodel), Eurydice's X_Story01 is Asphodel (1),
    # Patroclus's Y_Story01 is Elysium (2). Thanatos's contest encounters run in all three
    # of Tartarus/Asphodel/Elysium with their rollout gates stripped from run 1
    # (ItemManager.apply_nightmare_helpers_unlock), so his earliest reach is zone 0.
    # Orpheus spawns in ZJ's Tartarus rooms (zone 0); "Allow Orpheus to Spawn in Tartarus" used
    # to gate that behind an item (see the old KEEPSAKE_ITEM_GATE note), but it's auto-granted
    # now (Items.INCANTATION_AUTO_GRANTED), so he's simply reachable from zone 0 like everyone
    # else here. Achilles appears alongside Patroclus's Elysium content (NPC_Achilles_01), so he
    # mirrors Patroclus's gate.
    # Megaera isn't here because her keepsake (Skull Earring) is item-only, no keepsake
    # location to gate (Locations.KEEPSAKE_NO_LOCATION) -- her "Met Megaera" location is a
    # separate NPC_BOSS_MEET entry gated by zone reachability, not this table.
    "Sisyphus":  (NIGHTMARE, 0, 2),
    "Eurydice":  (NIGHTMARE, 1, 2),
    "Patroclus": (NIGHTMARE, 2, 3),
    "Thanatos":  (NIGHTMARE, 0, 2),
    "Orpheus":   (NIGHTMARE, 0, 2),
    "Achilles":  (NIGHTMARE, 2, 3),
    # Hades: no "<NPC> Keepsake" location (Jeweled Pom is item-only, KEEPSAKE_NO_LOCATION),
    # so this entry only rules "Met Hades". He used to be the lone multi-route NPC (his own
    # _set_hades_met_rule, Underworld/Nightmare zone 3); now his I_Story01 shuffles across
    # routes like every other story room, so he's a randomized helper with a tier-3 count
    # for pacing parity with the other deep story NPCs (Patroclus/Achilles).
    "Hades":     (UNDERWORLD, 3, 3),
}
KEEPSAKE_HARD_TIER_PCT = {1: 0.10, 2: 0.30, 3: 0.50, 4: 0.75}
# NPCs who need a specific incantation item held before they'll show up: Moros needs
# Doomed Beckoning (base game), which is progression in Items.py for this reason. Orpheus
# used to need "Allow Orpheus to Spawn in Tartarus" here too, but the July 19 cull moved that
# incantation to Items.INCANTATION_AUTO_GRANTED -- it's force-granted whenever Nightmare is
# active (ItemManager.lua's apply_conditional_incantation_starts) instead of being a shuffled
# item, so Orpheus always spawns from the start of a Nightmare seed and no longer needs a gate
# here (an item-based rule for an item that no longer exists in the pool would never resolve).
KEEPSAKE_ITEM_GATE = {
    "Moros": "Doomed Beckoning",
}
# Athena's keepsake item -- holding it is an alternate way to "meet" her (see
# _set_keepsake_rules), which also makes her reachable on Underworld-only seeds.
ATHENA_KEEPSAKE_ITEM = "Gorgon Amulet"

# Without the Surface Penalty Cure you can only reach a sliver of the Surface: in-game the
# curse walls you off after room 3 (the cure is locked behind meeting Athena), so the cure
# must turn up in that early sphere -- the first 3 surface rooms, a Crossroads NPC/god "Met"
# check, or an early keepsake -- all of which stay ungated below. Score systems keep the same
# proportion the original 5-room cap had (5 rooms <-> 6%), so 3 rooms <-> 3.6%. Room/score
# checks can be banked cumulatively across many separate run attempts, so "reachable" here
# means "reachable over time", not "survivable in one continuous curse-laden run" -- that
# stricter, single-run bar is what actually matters for enemy "Defeated" checks instead (see
# SURFACE_NO_CURE_ENEMY_ZONE_DEPTH below: verified against Content/Scripts/EncounterData_Opening.lua
# that the curse trait itself isn't granted until AFTER the first room's encounter resolves).
SURFACE_NO_CURE_ROOM_DEPTH = 3
SURFACE_NO_CURE_SCORE_FRACTION = 0.036

# Item-name lists for the arcana/keepsake counters.
_ARCANA_ITEMS = [f"{title} Arcana" for title in arcana_titles]
_ARCANA_PROG_ITEMS = [f"Progressive {title} Arcana" for title in arcana_titles]

# --- Boss-tier gates (weapons / grasp / arcana / vow weight / void vow weight /
# progressive weapons / gods) ---
# Second tightening pass (July 17): a zone's own boss is the ONLY thing that gates the zone
# behind it (see set_rules) -- reaching a zone's rooms/score checks no longer implies its boss
# is beatable, and a boss's own weapon count now applies directly to ITS "Beat" event (not just
# the zone-exit that follows). Each of a route's 4 bosses additionally needs a growing
# percentage of whichever resource pools are actually active this seed: 30% for the 1st boss,
# 50% the 2nd, 75% the 3rd, 100% the 4th (final). Grasp is deliberately percentage-of-cap
# (rather than a flat count) since players can freely change how many Progressive Grasp items
# exist (GraspCount); Arcana/vow-weight/void-vow-weight/progressive-weapon/gods-unlocked share
# the same percentages for consistency. GodSanity (added July 21) is a resource pool the same
# way: while it's active, boons from a locked god can never be picked up, so a boss tier
# assuming you've accumulated boon-derived power needs its own share of the 11 "<God> Unlock"
# items too, not just grasp/arcana -- otherwise a seed could demand 75% arcana off boon-fueled
# runs while GodSanity still had 10 of 11 gods locked. Each piece only gates when its mode is
# actually in play this seed (mirrors _hades2_grasp_count/_hades2_arcana_count's "return a
# large number when off" pass-through pattern). Re-tightened July 24: now that every resource
# above is guaranteed progression (no longer a mix of progression/useful), _tier_requirement_met
# requires ALL active pools to individually clear each tier (not just a majority) -- see that
# function's docstring. The Void vow also got its own dedicated pool (_hades2_void_vow_state),
# separate from the combined vow-weight pool, so a seed can't clear the vow gate by stripping
# only the cheaper vows while leaving Void untouched.
BOSS_TIER_PERCENT = [0.30, 0.50, 0.75, 1.00]

# Real per-rank "shrine point" weight of each Vow, read directly from the game's own
# Ranks tables (Content/Scripts/MetaUpgradeData.lua) -- the same weight the vanilla
# Pact of Punishment uses for its own difficulty scoring, so a vow's "weight" here
# matches how heavy the game itself considers that rank. List index i = rank (i+1)'s
# own point cost (not cumulative); lengths match each Vow's range_end in Options.py.
VOW_LEVEL_POINTS = {
    "Pain": [1, 2, 2], "Grit": [1, 1, 1], "Wards": [1, 1], "Frenzy": [3, 3],
    "Hordes": [1, 1, 1], "Menace": [1, 2], "Return": [1, 1], "Fangs": [2, 3],
    "Scars": [1, 1, 2], "Debt": [1, 1], "Shadow": [2], "Forfeit": [3],
    "Time": [1, 2, 3], "Void": [1, 1, 1, 2], "Hubris": [1, 1], "Denial": [2],
    "Rivals": [2, 3, 3, 4],
}

# Total "Progressive <Weapon>" copies across all 6 weapons -- only meaningful when
# aspectsanity=progressive (the one mode where that item is how weapons unlock at all --
# see _progressive_weapon_active below). Superseded by _progressive_weapon_pool_size below
# (IncludedWeapons, Options.py, means not every seed has all 6); kept as the max-universe
# constant other modules might still want.
PROGRESSIVE_WEAPON_POOL_SIZE = len(WEAPON_SHORT_NAMES) * ASPECT_MAX_RANK


def _weapon_cap(options) -> int:
    """How many weapons actually exist this seed (IncludedWeapons, Options.py). The boss
    weapon-count gates and the progressive-weapon pool size must scale to this instead of
    always assuming 6, or a seed with fewer included weapons could demand more weapon variety
    than can ever exist -- making a boss (or the goal itself) permanently unreachable."""
    return len(options.included_weapons.value)


def _zone_weapon_gate(z: int, options) -> int:
    """Weapons needed to beat a route's zone-z (0..2) boss, clamped to this seed's actual
    weapon count."""
    return min(ZONE_WEAPON_GATES[z], _weapon_cap(options))


def _final_weapon_gate(options) -> int:
    """Weapons needed to beat a route's final (4th) boss / the Zagreus Defeated check,
    clamped to this seed's actual weapon count."""
    return min(FINAL_WEAPONS, _weapon_cap(options))


def _progressive_weapon_pool_size(options) -> int:
    """Total "Progressive <Weapon>" copies that actually exist this seed -- only meaningful
    when aspectsanity=progressive (see _progressive_weapon_active). Scales with
    IncludedWeapons instead of assuming all 6, same reasoning as _zone_weapon_gate."""
    return _weapon_cap(options) * ASPECT_MAX_RANK


def _arcana_cap(options) -> int:
    """Total Arcana items that actually exist this seed, for scaling the boss-tier
    fractions. A large number when ArcanaSanity is off (cards are bought normally, so
    this gate never binds) -- mirrors _grasp_cap's sentinel."""
    if options.arcanasanity.value == 0:
        return 99
    return len(arcana_titles)


# Reverse of Items.GOD_KEEPSAKE_TITLE (god -> title): title -> god, for _hades2_keepsake_count.
_GOD_BY_KEEPSAKE_TITLE = {title: god for god, title in GOD_KEEPSAKE_TITLE.items()}


def _god_keepsake_combined(options) -> bool:
    """Whether GodSanity's 11 "<God> Unlock" items are fused with their KeepsakeSanity
    keepsake item into a single "<God> Unlock + Keepsake" item this seed (see Items.py's
    GOD_KEEPSAKE_COMBINED_GODS) -- only when KeepsakeSanity is "randomized" (one item per
    keepsake, mode 1) AND GodSanity is active. Progressive keepsakes (mode 2) have no
    per-NPC item to fuse, so this is always False then."""
    return options.keepsakesanity.value == 1 and options.godsanity.value != 0


def _god_unlock_item(god: str, options) -> str:
    """The actual item name that unlocks `god`'s boons this seed: the combined
    "<God> Unlock + Keepsake" item when _god_keepsake_combined, else the plain
    "<God> Unlock" item."""
    if _god_keepsake_combined(options):
        return f"{god} Unlock + Keepsake"
    return f"{god} Unlock"


def _god_cap(options) -> int:
    """Total "<God> Unlock" items that actually exist this seed, for scaling the boss-tier
    fractions. A large number when GodSanity is "unlocked" (0) -- boons aren't gated behind
    an item at all then, so this pool never binds -- mirrors _grasp_cap/_arcana_cap's
    sentinel. All 11 GodSanity items count (the 9 boon-reward gods plus Hermes/Selene):
    GodSanity restricts what CAN spawn in a boon-reward slot regardless of which of the 11
    it is, so the boss-tier gate treats "gods unlocked" as one pool the same way grasp/arcana
    are, rather than trying to split boon-slot vs. shop-eligibility gods apart."""
    if options.godsanity.value == 0:
        return 99
    return len(godsanity_gods) + len(godsanity_shop_gods)


def _progressive_weapon_active(options) -> bool:
    """Whether "Progressive <Weapon>" items are this seed's weapon-unlock mechanism
    (aspectsanity=progressive) -- the only mode where the boss-tier progressive-weapon
    gate means anything."""
    return options.aspectsanity.value == 2


class Hades2Logic(LogicMixin):
    def _hades2_has_weapon(self, weapon_subfix: str, player: int, options) -> bool:
        # Weapons are always shuffled (the WeaponSanity toggle was removed): you have a
        # weapon if it's your starting weapon or you've received its unlock item.
        mapping = {
            "Staff": (0, "Staff Weapon Unlock Item"),
            "Blades": (1, "Blades Weapon Unlock Item"),
            "Flames": (2, "Flames Weapon Unlock Item"),
            "Axe": (3, "Axe Weapon Unlock Item"),
            "Skull": (4, "Skull Weapon Unlock Item"),
            "Coat": (5, "Coat Weapon Unlock Item"),
        }
        initial, item = mapping[weapon_subfix]
        # Progressive mode replaces the unlock item with "Progressive <Weapon>" (the first
        # copy unlocks the weapon), so accept either form.
        if (options.initial_weapon == initial) or self.has(item, player) \
                or self.has("Progressive " + weapon_subfix, player):
            return True
        asp = options.aspectsanity.value
        # Randomized mode: the first of this weapon's 4 Aspect items (its default Aspect of
        # Melinoe or one of its 3 alternates -- all 4 are shuffled in this mode) also
        # unlocks the weapon (ItemManager.unlock_aspect).
        if asp == 1:
            names = [ASPECT_BASE_TITLE_BY_WEAPON[weapon_subfix]] + \
                [title for title, w in aspect_titles if w == weapon_subfix]
            return any(self.has(name, player) for name in names)
        # per_aspect: the first copy of ANY of this weapon's 4 aspect items (its default
        # Base Aspect or one of its 3 alternates) unlocks the weapon.
        if asp == 3:
            names = [f"Progressive {weapon_subfix} Base Aspect"] + \
                [f"Progressive {title}" for title, w in aspect_titles if w == weapon_subfix]
            return any(self.has(name, player) for name in names)
        return False

    def _hades2_has_enough_weapons(self, player: int, options, amount: int) -> bool:
        count = 0
        for weapon in ("Staff", "Blades", "Flames", "Axe", "Skull", "Coat"):
            if self._hades2_has_weapon(weapon, player, options):
                count += 1
        return count >= amount

    def _hades2_arcana_count(self, player: int, options) -> int:
        """How many distinct Arcana cards are unlocked. Returns a large number when
        ArcanaSanity is off (cards are bought normally, so they don't gate anything)."""
        mode = options.arcanasanity.value
        if mode == 1:  # Arcana: one unlock item per card
            return sum(1 for name in _ARCANA_ITEMS if self.has(name, player))
        if mode == 2:  # Progressive_Arcana: first "Progressive <Card>" copy unlocks it
            return sum(1 for name in _ARCANA_PROG_ITEMS if self.has(name, player))
        return 99

    def _hades2_grasp_count(self, player: int, options) -> int:
        """How many Progressive Grasp items are owned. Returns a large number when grasp
        isn't a real resource (0 grasp per item), so grasp gates pass."""
        if int(options.grasp_intervals) <= 0:
            return 99
        return self.count("Progressive Grasp", player)

    def _hades2_god_count(self, player: int, options) -> int:
        """How many of the 11 "<God> Unlock" items are held. Returns a large number when
        GodSanity is "unlocked" (0), since boons aren't gated behind an item then."""
        if options.godsanity.value == 0:
            return 99
        return sum(1 for god in godsanity_gods + godsanity_shop_gods
                    if self.has(_god_unlock_item(god, options), player))

    def _hades2_keepsake_count(self, player: int, options) -> int:
        """How many keepsakes have effectively been earned, for the Logic.txt thresholds.
        Randomized: count distinct keepsake items. Progressive: copy 1 clears the tier 1
        threshold, copy 2 clears tier 2, and holding all KEEPSAKE_PROGRESSIVE_COUNT copies
        clears the whole pool (tier 3/4 and the boon-god threshold included). Previously a
        flat "* 4" per copy, which topped out at 12 (3 copies) -- short of the tier 3 (20)
        and tier 4 (30) thresholds against the 40-title pool, so KEEPSAKE_HARD's tier-3/4
        NPCs (Echo/Heracles/Medea/Circe/Icarus/Athena/Dionysus/Patroclus/Hades/Achilles)
        had a permanently-unreachable Met+Keepsake rule under keepsakesanity=progressive
        whenever a progression item landed there (generation-breaking, fixed 7/22). Normal
        keepsakes have no check locations, so this is never consulted there."""
        mode = options.keepsakesanity.value
        if mode == 2:
            copies = self.count("Progressive Keepsake", player)
            if copies >= KEEPSAKE_PROGRESSIVE_COUNT:
                return _keepsake_pool_size(options)
            return math.ceil(KEEPSAKE_HARD_TIER_PCT.get(copies, 0) * _keepsake_pool_size(options))
        if mode == 1:
            if _god_keepsake_combined(options):
                # The 11 GodSanity gods' titles are fused into "<God> Unlock + Keepsake"
                # items (see Items.GOD_KEEPSAKE_TITLE) -- check those instead of the bare
                # title, which was never placed in the pool this seed.
                def owned(title):
                    god = _GOD_BY_KEEPSAKE_TITLE.get(title)
                    name = f"{god} Unlock + Keepsake" if god else title
                    return self.has(name, player)
                return sum(1 for title in keepsake_titles if owned(title))
            return sum(1 for title in keepsake_titles if self.has(title, player))
        return 99

    def _hades2_vow_weight_state(self, player: int, options) -> tuple:
        """(total starting vow weight, weight removed so far), using the real per-rank
        Points in VOW_LEVEL_POINTS. (0, 0) when vows aren't in play this seed (reverse_vow
        off, or every vow_X happens to be 0) -- callers treat a 0 total as "gate passes"."""
        if not options.reverse_vow:
            return 0, 0
        total = 0
        removed = 0
        for vow in vow_names:
            start_level = int(getattr(options, "vow_" + vow.lower()))
            if start_level <= 0:
                continue
            points = VOW_LEVEL_POINTS[vow]
            total += sum(points[:start_level])
            owned = min(self.count(f"{vow} Vow Removal", player), start_level)
            # Removal peels from the top (most severe) rank down, so the weight removed
            # is the top `owned` ranks' points, not the bottom ones.
            removed += sum(points[start_level - owned:start_level])
        return total, removed

    def _hades2_void_vow_state(self, player: int, options) -> tuple:
        """Same shape as _hades2_vow_weight_state, scoped to just the Void vow -- gives the
        boss-tier gate its own dedicated Void pool (see BOSS_TIER_PERCENT's July 24 note)
        distinct from the combined vow-weight pool, so removing weight from cheaper vows
        can't stand in for actually peeling down Void. (0, 0) when Void isn't in play this
        seed (reverse_vow off, or vow_void's starting level is 0)."""
        if not options.reverse_vow:
            return 0, 0
        start_level = int(getattr(options, "vow_void", 0))
        if start_level <= 0:
            return 0, 0
        points = VOW_LEVEL_POINTS["Void"]
        total = sum(points[:start_level])
        owned = min(self.count("Void Vow Removal", player), start_level)
        removed = sum(points[start_level - owned:start_level])
        return total, removed

    def _hades2_progressive_weapon_count(self, player: int) -> int:
        """Total copies of any "Progressive <Weapon>" item owned, summed across all 6
        weapons -- only meaningful when _progressive_weapon_active(options) is true."""
        return sum(self.count(f"Progressive {w}", player) for w in WEAPON_SHORT_NAMES)

    def _hades2_can_get_victory(self, player: int, options) -> bool:
        # Route bosses (chronos/typhon/hades) each need the configured weapon-clear variety;
        # zagreus (secret superboss, no route) doesn't -- a single clear with any weapon
        # satisfies his part of the goal.
        weapons = options.weapons_clears_needed.value
        achieved = {}
        for boss in GOAL_BOSSES:
            has_victory = self.has(f"{boss.capitalize()} Victory", player)
            if boss == "zagreus":
                achieved[boss] = has_victory
            else:
                achieved[boss] = has_victory and self._hades2_has_enough_weapons(
                    player, options, weapons)

        bosses = [b for b in GOAL_BOSSES if goal_includes(options, b)]
        if not bosses:
            return False    # misconfigured (no goal boss toggled on) -- never completable
        if options.goal_mode.value == ALL_SELECTED:
            return all(achieved[b] for b in bosses)
        return any(achieved[b] for b in bosses)


# -----------------------------------------------------------------------------


def _grasp_cap(options) -> int:
    """How many Progressive Grasp exist, for clamping grasp requirements. A large number
    when grasp isn't a real resource (so grasp gates never bind)."""
    if int(options.grasp_intervals) <= 0:
        return 99
    return int(options.grasp_count)


def _tier_requirement_met(state, player: int, options, percent: float, grasp_cap: int,
                          arcana_cap: int, weapon_active: bool, god_cap: int = 99) -> bool:
    """Whether `state` clears the given tier's percentage across EVERY resource pool that is
    actually active this seed (grasp/arcana/progressive-weapon-count/vow-weight-removed/
    void-vow-weight-removed/gods-unlocked). Shared by every boss's own tier gate and by the
    Zagreus checks (see set_rules).

    Re-tightened July 24 back to a strict AND across every active pool (each of BOSS_TIER_PERCENT's
    now-guaranteed-progression resources must individually clear the tier -- no pool can be
    ignored by leaning on the others). This was loosened to a majority on July 17 when the tiers
    ran up to 90% and stacked pools could demand "almost the entire item pool" at once; the July 24
    pass lowered the ceiling back to 100% only at the final boss (30/50/75/100 ramp) and the vow
    pool was split so Void has its own dedicated gate (_hades2_void_vow_state) distinct from the
    combined vow-weight one -- with the ramp gentler and each pool's own fill correspondingly
    easier to satisfy, requiring all of them together is deliberate this time, not an oversight to
    relax again."""
    checks = []
    if grasp_cap < 99:
        checks.append(state._hades2_grasp_count(player, options) >= math.ceil(percent * grasp_cap))
    if arcana_cap < 99:
        checks.append(state._hades2_arcana_count(player, options) >= math.ceil(percent * arcana_cap))
    if weapon_active:
        checks.append(state._hades2_progressive_weapon_count(player) >=
                       math.ceil(percent * _progressive_weapon_pool_size(options)))
    if options.reverse_vow:
        total, removed = state._hades2_vow_weight_state(player, options)
        if total > 0:
            checks.append(removed >= math.ceil(percent * total))
        void_total, void_removed = state._hades2_void_vow_state(player, options)
        if void_total > 0:
            checks.append(void_removed >= math.ceil(percent * void_total))
    if god_cap < 99:
        checks.append(state._hades2_god_count(player, options) >= math.ceil(percent * god_cap))
    if not checks:
        return True
    return all(checks)


def set_rules(world: "Hades2World", player: int, options, route_offsets: dict,
              surface_access_via_progressive: bool = False,
              nightmare_access_via_progressive: bool = False) -> None:
    locked = bool(options.lock_routes)
    routes = active_routes(options)
    system = options.location_system.value
    grasp_cap = _grasp_cap(options)
    arcana_cap = _arcana_cap(options)
    weapon_active = _progressive_weapon_active(options)
    god_cap = _god_cap(options)

    # (route, zone-index) -> (zone name, predicate(state)) for that zone's own boss, so the
    # enemy gates (point 6) and the Zagreus checks (point 7) below can reuse the exact same
    # "is this boss beatable" test instead of re-deriving it.
    route_boss_conditions: dict = {}

    for route in routes:
        zones = ROUTES[route]["zones"]
        bosses = ROUTES[route]["bosses"]
        prog = ROUTES[route]["progressive"]
        offset = route_offsets[route]

        # Entering the route's first zone: needs `offset` route-progressives when locked.
        if locked:
            add_rule(world.get_entrance("Descend " + route, player),
                     lambda state, p=prog, o=offset: state.count(p, player) >= o)

        # Each of a route's 4 bosses is now the ONLY thing gating the zone behind it -- a
        # zone's rooms/score checks are no longer treated as "beatable" just because the zone
        # itself is reachable (July 17 tightening). A boss's own weapon count + tier
        # percentage (BOSS_TIER_PERCENT) gates ITS OWN "Beat <boss>" event directly; leaving
        # the zone then just needs that boss's Victory item (which encodes everything above)
        # plus, when locked, enough route-progressives.
        for z, boss in enumerate(bosses):
            weapons_needed = _final_weapon_gate(options) if z == len(bosses) - 1 \
                else _zone_weapon_gate(z, options)
            percent = BOSS_TIER_PERCENT[z]

            def _boss_beatable(state, w=weapons_needed, pct=percent):
                return state._hades2_has_enough_weapons(player, options, w) \
                    and _tier_requirement_met(state, player, options, pct, grasp_cap,
                                              arcana_cap, weapon_active, god_cap)

            add_rule(world.get_location(boss_event(boss), player), _boss_beatable)
            route_boss_conditions[(route, z)] = (zones[z], _boss_beatable)

        for i in range(len(zones) - 1):
            add_rule(world.get_entrance("Exit " + zones[i], player),
                     lambda state, b=bosses[i]: state.has(boss_victory(b), player))
            if locked:
                add_rule(world.get_entrance("Exit " + zones[i], player),
                         lambda state, p=prog, need=i + 1 + offset: state.count(p, player) >= need)

    # combine_pools: the shared pools live in their own region rather than the per-route zone
    # regions, so their reachability is set here instead of coming from the zone chain.
    # Rooms ("Room NNNN") are gated by depth only, score ("Score NNNN") by its check index --
    # each reachable once the matching zone is reachable on ANY route (plus the weapon, for
    # per_weapon rooms). This is the SAME zone-ladder as above (now much stricter), so
    # split_pools' score/room checks (gated purely by the region they live in -- see
    # Locations.py/Regions.py) and combine_pools' shared checks both inherit it identically:
    # there is no separate, softer percentile ramp for point_based any more (see set_rules'
    # July 17 history -- SCORE_POWER_TIERS/_set_score_power_rules were removed).
    if combine_active(options):
        if system in (ROOM_BASED, PER_WEAPON_ROOM_BASED):
            _set_combined_room_rules(world, player, options, routes)
        else:
            _set_combined_score_rules(world, player, options, routes)
    # per_weapon_room_based (split_pools): each "<Room prefix> NNNN <Weapon>" check
    # additionally needs that specific weapon in hand.
    elif system == PER_WEAPON_ROOM_BASED:
        _set_per_weapon_rules(world, player, options, routes)

    # Enemy "Defeated" checks (point 6, narrowed): ONLY mini-boss enemies (MINIBOSS_ENEMY_NAMES
    # -- real secondary mini-bosses plus the handful that are the same fight as the zone's own
    # boss) require that boss to be beatable. Every other (regular/trash) enemy in the zone
    # keeps its original rule: just the zone being reachable, same as before the July 17 pass.
    # MINIBOSS_ZONE_OVERRIDE lets a specific mini-boss borrow a LATER zone's (harder) tier
    # instead of its own zone's, while still living in its own zone's region (Alecto/Tisiphone).
    # NOTE (found July 18 while investigating the Surface curse): MINIBOSS_ENEMY_NAMES/
    # MINIBOSS_ZONE_OVERRIDE store bare creature names, but every enemy check name here has
    # " Defeated" appended -- a direct membership test against either table always missed, so
    # this whole boss-tier gate (and the identical one in _set_shared_enemy_rules below) had
    # silently never applied to ANY route. Fixed via _is_miniboss_location / stripping the
    # suffix before the MINIBOSS_ZONE_OVERRIDE lookup.
    for (route, z), (zone, pred) in route_boss_conditions.items():
        for name in ENEMY_BY_ZONE.get((route, zone), []):
            if not _is_miniboss_location(name):
                continue
            try:
                location = world.get_location(name, player)
            except KeyError:
                continue
            bare = name[:-len(" Defeated")] if name.endswith(" Defeated") else name
            override = MINIBOSS_ZONE_OVERRIDE.get(bare)
            use_pred = route_boss_conditions[override][1] if override in route_boss_conditions else pred
            add_rule(location, use_pred)
    _set_shared_enemy_rules(world, player, routes, route_boss_conditions)

    # The Surface route needs the Surface Access item to open the door. The Surface
    # Penalty Cure no longer gates entry: per Logic.txt you can play the early Surface
    # without it, but it's needed to push past the first few rooms (handled per-location).
    if SURFACE in routes:
        if surface_access_via_progressive:
            # No separate "Surface Access" item: the first Progressive Surface opens the door
            # (Test Run 5 #14), so entering the Surface needs 1 Progressive Surface.
            prog = ROUTES[SURFACE]["progressive"]
            add_rule(world.get_entrance("Descend Surface", player),
                     lambda state, p=prog: state.count(p, player) >= 1)
        else:
            add_rule(world.get_entrance("Descend Surface", player),
                     lambda state: state.has("Surface Access", player))
        _set_surface_cure_rules(world, player, options)
        _set_surface_enemy_cure_rules(world, player)

    # Nightmare needs its own Access item to open the Crossroads Chaos Gate -- same shape as
    # Surface. This is on top of (not instead of) the generic Progressive-offset mechanism
    # above: Underworld has no in-fiction entry gate of its own, so the offset alone locks its
    # door, while Surface/Nightmare layer their Access-item/first-Progressive door check on
    # top of the same offset -- all three still cost 4 total copies when non-starting, 3 when
    # starting.
    if NIGHTMARE in routes:
        if nightmare_access_via_progressive:
            prog = ROUTES[NIGHTMARE]["progressive"]
            add_rule(world.get_entrance("Descend " + NIGHTMARE, player),
                     lambda state, p=prog: state.count(p, player) >= 1)
        else:
            add_rule(world.get_entrance("Descend " + NIGHTMARE, player),
                     lambda state: state.has("Nightmare Access", player))

    # Keepsake unlock checks gate on keepsake count and (hard ones) area access. This also
    # covers "Met Hades" -- previously a separate _set_hades_met_rule; his entry now lives
    # in KEEPSAKE_HARD as a randomized helper (July 18).
    _set_keepsake_rules(world, player, options, routes)

    # Zagreus (secret superboss): not tied to either route's zone-boss list, so it's placed
    # in Crossroads (see Regions.py) with its own access rule instead of a zone entrance
    # chain. In-fiction the contract only becomes available once you've proven yourself
    # against a route's own final boss, so gate reachability on any active route being
    # fully accessible (its last zone reachable) rather than just an early zone. In
    # Empowered mode, also require a threshold share of Progressive Zagreus Weaken so the
    # fight isn't attemptable while he's still at full empowered strength.
    zagreus_final_zones = [ROUTES[route]["zones"][-1] for route in routes]
    weaken_needed = -(-(options.zagreus_weaken_tiers.value * 3) // 5) \
        if options.zagreus_encounter_mode.value == 1 and goal_includes(options, "zagreus") \
        else 0   # ceil(0.6 * tiers), Empowered only, and only when the pool has Weaken items
    add_rule(world.get_location(boss_event("Zagreus"), player),
             lambda state, zones=zagreus_final_zones, need=weaken_needed:
                 any(state.can_reach(z, "Region", player) for z in zones)
                 and state.count("Progressive Zagreus Weaken", player) >= need)

    # "Met Chronos" (user request): moved into zone 0 (Erebus) in Locations.py so its region
    # is reachable from the start of the Underworld route, same as Hecate's -- but region
    # reachability alone would make it available immediately, which is looser than "when
    # defeating Hecate is accessible". So it also gets Hecate's own _boss_beatable predicate
    # (weapons + tier %) directly, matching the exact condition on "Beat Hecate" itself.
    if (UNDERWORLD, 0) in route_boss_conditions:
        hecate_pred = route_boss_conditions[(UNDERWORLD, 0)][1]
        try:
            met_chronos = world.get_location("Met Chronos", player)
        except KeyError:
            pass
        else:
            add_rule(met_chronos, hecate_pred)

        # SHUSH Homer / Find Hecate 1-3 (user request): these are Hecate's own hide-and-seek
        # flashback beats, so they should open at the exact same moment defeating Hecate does
        # -- not just be free Crossroads checks the instant the Underworld route exists. Unlike
        # "Met Chronos" (which lives IN the Erebus region, so lock_routes/entrance reachability
        # is already enforced by the region graph), these four live in the always-reachable
        # Crossroads region (see Regions.py), so hecate_pred alone isn't enough -- it only
        # checks weapons/tier%, not whether the Underworld route is actually enterable yet. Also
        # require the Erebus zone itself be reachable, same pattern as _set_shared_enemy_rules.
        erebus_zone = route_boss_conditions[(UNDERWORLD, 0)][0]
        for _intro_name in NPC_INTRO:
            try:
                _intro_loc = world.get_location(_intro_name, player)
            except KeyError:
                continue
            add_rule(_intro_loc,
                     lambda state, z=erebus_zone, pred=hecate_pred:
                         state.can_reach(z, "Region", player) and pred(state))

    # "Met Zagreus" / "Zagreus Defeated" (point 7): two REAL checks, distinct from the "Beat
    # Zagreus" goal event above. Met opens up as soon as ANY route's 1st ("tier 1",
    # BOSS_TIER_PERCENT[0] = 30%) boss is beatable -- an early, cheap gate, since this is
    # meant to just be a first sighting. EXCEPT in Final Challenge mode (user request, July 22):
    # there the Zagreus contract only ever spawns after defeating a route's FINAL boss (see
    # boss_event("Zagreus") above / the ItemManager hook), so "meeting" him can't happen any
    # earlier than that in that mode -- gate on any route's final-tier boss being beatable
    # instead of its 1st-tier one.
    # Defeated needs the FULL (100%) share of every active resource pool -- same bar as the
    # 4th/final boss tier now that BOSS_TIER_PERCENT[3] is itself 100% -- plus all 6 weapons,
    # any route's final zone, and (in Empowered mode) the full Weaken-tier count rather than the
    # 60% the goal event uses.
    tier1_preds = [pred for (route, z), (zone, pred) in route_boss_conditions.items() if z == 0]
    final_preds = [pred for (route, z), (zone, pred) in route_boss_conditions.items()
                   if z == len(ROUTES[route]["zones"]) - 1]
    try:
        met_zagreus = world.get_location(ZAGREUS_MET_LOCATION, player)
    except KeyError:
        pass
    else:
        if options.zagreus_encounter_mode.value == 2 and goal_includes(options, "zagreus"):
            add_rule(met_zagreus, lambda state, preds=final_preds: any(pred(state) for pred in preds))
        else:
            add_rule(met_zagreus, lambda state, preds=tier1_preds: any(pred(state) for pred in preds))

    # Bug fix (generation-failure pass): this used to check only zagreus_encounter_mode, not
    # whether Zagreus is actually part of the goal -- but the item pool only adds "Progressive
    # Zagreus Weaken" copies when goal_includes(options, "zagreus") is true (see __init__.py's
    # create_items). On any seed with Empowered mode but Zagreus NOT in the goal, this location
    # demanded copies of an item that was never placed in the pool, making it permanently
    # unreachable and failing generation outright. Now mirrors the "Beat Zagreus" goal event's
    # own guard just above.
    defeat_weaken_needed = options.zagreus_weaken_tiers.value \
        if options.zagreus_encounter_mode.value == 1 and goal_includes(options, "zagreus") else 0
    try:
        zagreus_defeated = world.get_location(ZAGREUS_DEFEATED_LOCATION, player)
    except KeyError:
        pass
    else:
        add_rule(zagreus_defeated,
                 lambda state, zones=zagreus_final_zones, need=defeat_weaken_needed,
                     w=_final_weapon_gate(options):
                     any(state.can_reach(z, "Region", player) for z in zones)
                     and state._hades2_has_enough_weapons(player, options, w)
                     and _tier_requirement_met(state, player, options, 1.0, grasp_cap,
                                               arcana_cap, weapon_active, god_cap)
                     and state.count("Progressive Zagreus Weaken", player) >= need)

    world.completion_condition[player] = lambda state: state._hades2_can_get_victory(player, options)


def _is_miniboss_location(location_name: str) -> bool:
    """MINIBOSS_ENEMY_NAMES holds bare creature names ("Erymanthian Boar"), but every enemy
    "Defeated" check/location name has " Defeated" appended (see Locations.py's ENEMY_BY_ZONE/
    SHARED_ENEMY_ZONES construction) -- strip it before comparing so the miniboss boss-tier gate
    (below and in _set_shared_enemy_rules) actually matches instead of silently never firing."""
    bare = location_name[:-len(" Defeated")] if location_name.endswith(" Defeated") else location_name
    return bare in MINIBOSS_ENEMY_NAMES


def _room_depth(name: str, prefix: str) -> int:
    """Depth of a room/score check from its name: '<prefix> NNNN [Weapon]' -> NNNN."""
    return int(name[len(prefix) + 1:].split(" ")[0])


def _set_surface_cure_rules(world: "Hades2World", player: int, options) -> None:
    """Without the Surface Penalty Cure the Surface curse limits you to its earliest
    checks (Logic.txt): rooms up to depth 3, or the first 3.6% of score checks."""
    system = options.location_system.value
    if system == POINT_BASED:
        prefix = ROUTES[SURFACE]["score_prefix"]
        count = _score_count_for(SURFACE, options)
    else:
        prefix = ROUTES[SURFACE]["room_prefix"]
        count = 0
    for zone in ROUTES[SURFACE]["zones"]:
        for location in world.get_region(zone, player).locations:
            name = location.name
            if not name.startswith(prefix + " "):
                continue
            depth = _room_depth(name, prefix)
            if system == POINT_BASED:
                gated = count > 0 and (depth / count) > SURFACE_NO_CURE_SCORE_FRACTION
            else:
                gated = depth > SURFACE_NO_CURE_ROOM_DEPTH
            if gated:
                add_rule(location, lambda state: state.has("Surface Penalty Cure", player))


def _set_surface_enemy_cure_rules(world: "Hades2World", player: int) -> None:
    """Enemy "Defeated" checks need a stricter bar than room/score checks: those can be banked
    cumulatively across many separate run attempts (each one only needs to reach a little
    farther than the last), but a "Defeated" check needs one live encounter with that specific
    species, which -- past the zone's own opening room -- means surviving the curse's escalating
    DoT for however long it takes to reach it (see SURFACE_NO_CURE_ROOM_DEPTH's comment: the
    curse trait itself isn't granted until AFTER City of Ephyra's first encounter resolves, so
    that first encounter's own roster is the one exception).

    City of Ephyra's regular (non-mini-boss) roster IS that first-encounter pool
    (Locations.ENEMY_LAYERS[SURFACE][0]), so those stay reachable on just zone access, same as
    before. Everything else on the Surface needs the cure on top of its existing gate:
      - City of Ephyra's own mini-boss/boss-identical fights (Erymanthian Boar, The Cyclops
        Polyphemus) sit deep in the zone, not in that opening pool.
      - Every enemy in the three zones past it (Rift of Thessaly, Mount Olympus, The Summit) is
        only reachable at all by having already survived that whole curse-laden stretch.
    """
    zones = ROUTES[SURFACE]["zones"]
    for zi, zone in enumerate(zones):
        for name in ENEMY_BY_ZONE.get((SURFACE, zone), []):
            if zi == 0 and not _is_miniboss_location(name):
                continue    # City of Ephyra trash: reachable in its own pre-curse opening pool
            try:
                location = world.get_location(name, player)
            except KeyError:
                continue
            add_rule(location, lambda state: state.has("Surface Penalty Cure", player))


def _set_keepsake_rules(world: "Hades2World", player: int, options, routes: list) -> None:
    """Gate each "<NPC> Keepsake" check: free tier gets no rule at all, the boon gods open
    together at KEEPSAKE_BOON_GODS_PCT, and hard keepsakes need area access + a tier count
    (KEEPSAKE_HARD_TIER_PCT) -- all thresholds are a percentage of _keepsake_pool_size(options)
    (40, or 33 when IncludeZagreusJourney is off).
    Moros (and Orpheus) additionally need their gating incantation item. Per Known Bugs/
    "Logic is all out of whack", meeting an NPC and being able to gift them a keepsake happen
    at the same point, so the matching "Met <NPC>" location (when one exists) gets the
    identical rule -- that also fixes NPCs like Icarus/Dionysus who were previously always
    reachable regardless of route."""
    def npc_locations(npc: str) -> list:
        found = []
        for name in (f"{npc} Keepsake", f"Met {npc}"):
            try:
                found.append(world.get_location(name, player))
            except KeyError:
                pass
        return found

    keepsakes_active = options.keepsakesanity.value != 0

    # KEEPSAKE_FREE gets no rule at all -- reachable at the Crossroads from the start.

    # Boon gods: one flat keepsake-count threshold shared by all 12. (Only meaningful with
    # keepsakesanity on, since that's the only mode with "<NPC> Keepsake" check locations;
    # the "Met <NPC>" locations exist regardless, but these NPCs have no route restriction.)
    pool_size = _keepsake_pool_size(options)
    if keepsakes_active:
        threshold = math.ceil(KEEPSAKE_BOON_GODS_PCT * pool_size)
        for npc in KEEPSAKE_BOON_GODS:
            for location in npc_locations(npc):
                add_rule(location,
                         lambda state, t=threshold: state._hades2_keepsake_count(player, options) >= t)

        tier1_threshold = math.ceil(KEEPSAKE_HARD_TIER_PCT[1] * pool_size)
        for npc in KEEPSAKE_FLAT_TIER1:
            for location in npc_locations(npc):
                add_rule(location,
                         lambda state, t=tier1_threshold: state._hades2_keepsake_count(player, options) >= t)

    # Incantation-gated NPCs (Moros/Doomed Beckoning, Orpheus/Allow Orpheus to Spawn in
    # Tartarus): the NPC doesn't show up until the item is held, so this gates their "Met"
    # location too -- and those exist whenever npc_locations is on, NOT just under
    # keepsakesanity, so this deliberately sits outside the keepsakes_active branch (it used
    # to be inside, leaving "Met Moros" ungated when keepsakesanity was off).
    for npc, item_name in KEEPSAKE_ITEM_GATE.items():
        for location in npc_locations(npc):
            add_rule(location, lambda state, i=item_name: state.has(i, player))

    # GodSanity: when active (not "unlocked"), the mod won't let a god's boon ever spawn
    # until its own "<God> Unlock" item is received (ItemManager.god_eligible /
    # SpawnRoomReward wrap), so meeting them -- and thus gifting their keepsake -- is
    # impossible before then. Same "gated behind an item" shape as KEEPSAKE_ITEM_GATE above,
    # applied unconditionally (not just under keepsakesanity) since "Met <God>" exists either
    # way. Sits outside keepsakes_active for the same reason KEEPSAKE_ITEM_GATE does.
    if options.godsanity.value != 0:
        # Hermes/Selene (godsanity_shop_gods) are gated in Lua by a different mechanism
        # (existence-only check on their own eligibility requirements, not the per-god Boon
        # reroll the other 9 use), but the same Met/Keepsake location rule applies either way.
        for god in godsanity_gods + godsanity_shop_gods:
            item_name = _god_unlock_item(god, options)
            for location in npc_locations(god):
                add_rule(location, lambda state, i=item_name: state.has(i, player))

    # Helper Room Sanity: on "items"/"items_random" (1/3), the mod won't let a helper NPC's
    # dialogue/buff (or the Met check itself) fire until their own "<NPC> Room" item is
    # received (ItemManager.helper_npc_eligible / the UseNPC gate), so meeting them -- and
    # thus gifting their keepsake -- is impossible before then. Same shape as GodSanity above.
    # Sits outside keepsakes_active for the same reason KEEPSAKE_ITEM_GATE does.
    if options.helper_room_sanity.value in (1, 3):
        # July 22: item-gate the Nightmare-cast trio whenever IncludeZagreusJourney is on, not
        # just when Nightmare itself is in `routes` -- they can be swapped into another active
        # route's story slot regardless (see Locations._route_locked_out's docstring), so the
        # item must exist to gate them whenever their location does.
        zj_on = bool(getattr(options, "include_zagreus_journey", True))
        helper_npcs = helper_story_npcs + (helper_story_npcs_nightmare if zj_on else [])
        for npc in helper_npcs:
            item_name = f"{npc} Room"
            for location in npc_locations(npc):
                add_rule(location, lambda state, i=item_name: state.has(i, player))

    # Combat Helper Sanity: on "items"/"items_random" (1/3), the mod won't let a combat-
    # assist NPC's encounter fire (native OR foreign zone) until their own "<NPC> Helper"
    # item is received (ItemManager.combat_helper_eligible / the Handle<God>Spawn wraps),
    # so meeting them -- and thus gifting their keepsake -- is impossible before then. Same
    # shape as GodSanity/Helper Room Sanity above. Nemesis is EXCLUDED here on purpose: she's
    # KEEPSAKE_FREE (met at the Crossroads from the start) regardless of this option, so her
    # location never gets this rule -- her item still gates her combat encounter in Lua, it
    # just doesn't gate her (separately, always-reachable) location.
    chs_mode = options.combat_helper_sanity.value
    if chs_mode in (1, 3):
        for npc in COMBAT_HELPER_NPCS:
            item_name = f"{npc} Helper"
            for location in npc_locations(npc):
                add_rule(location, lambda state, i=item_name: state.has(i, player))

    # Hard keepsakes: an area gate AND own enough keepsakes for the NPC's tier. These gate
    # "Met <NPC>" even when keepsakesanity is off, since that's what stops off-route NPCs
    # from being unconditionally reachable. The area gate comes in two shapes (July 18):
    #  - Randomized helpers (Routes.NPC_RANDOMIZED_HELPERS): the story-room / combat-assist
    #    randomizers reroll WHO appears every run, on every route -- so the NPC is reachable
    #    (over repeated runs) once ANY active route's earliest hosting zone is reachable
    #    (zone 0, except the NPC_RANDOMIZED_EARLIEST_ZONE overrides).
    #  - Everyone else: their own native route's area, when that route is in the seed
    #    (when it isn't, the location doesn't exist at all -- Locations._route_locked_out).
    for npc, (route, area, tier) in KEEPSAKE_HARD.items():
        locations = npc_locations(npc)
        if not locations:
            continue
        # Combat Helper Sanity, native-only modes (0/1): these 5 NPCs can no longer spawn
        # anywhere but their own native zone (ItemManager.apply_combat_helper_random turns
        # the "any location" config flags off in Lua), so the random-helper "any active
        # route's final zone" rule below would be too generous -- fall through to the
        # `elif route in routes` branch instead, which already does exactly the native
        # (route, area) rule needed. Locations._route_locked_out already dropped the
        # location entirely when that native route isn't in the seed at all, so `route in
        # routes` is guaranteed true by the time we get here.
        # EXCEPTION (Thanatos/IncludeZagreusJourney, July 22): Routes.combat_helper_native_fallback
        # -- when his native route (Nightmare) isn't in the seed but IncludeZagreusJourney is
        # still on, ItemManager.apply_combat_helper_random forces his foreign-zone flags on
        # regardless of mode (mod side), so he's reachable via whichever OTHER routes are active
        # instead of native-locked -- treat him as a normal randomized helper here too.
        combat_native_only = npc in COMBAT_HELPER_NPCS and chs_mode in (0, 1) \
            and not combat_helper_native_fallback(npc, options, routes)
        if npc in NPC_RANDOMIZED_HELPERS and not combat_native_only:
            # Reachable once at least ceil(len(routes)/2) of the active routes have their
            # OWN final zone (index 3) reachable -- see Routes.NPC_RANDOMIZED_ZONE_INDEX.
            final_zones = tuple(ROUTES[r]["zones"][NPC_RANDOMIZED_ZONE_INDEX] for r in routes)
            need = -(-len(final_zones) // 2)  # ceil(n/2): 1->1, 2->1, 3->2
            for location in locations:
                add_rule(location,
                         lambda state, zones=final_zones, need=need: sum(
                             1 for z in zones if state.can_reach(z, "Region", player)) >= need)
        elif route in routes:
            region = ROUTES[route]["zones"][area]
            for location in locations:
                add_rule(location, lambda state, r=region: state.can_reach(r, "Region", player))
        if keepsakes_active:
            threshold = math.ceil(KEEPSAKE_HARD_TIER_PCT[tier] * pool_size)
            for location in locations:
                add_rule(location,
                         lambda state, t=threshold: state._hades2_keepsake_count(player, options) >= t)

    # Athena: a randomized helper like the rest as of July 18 (zerp-Extended gives her
    # encounters in every route's zones), so she no longer needs the Surface Penalty Cure
    # rule her deep-Surface home zone used to justify. Already holding her keepsake item
    # remains an alternate way for her to "show up", relaxing the area+count gate above
    # (kept from the original design -- it's how Underworld-only seeds reached her before).
    # July 22: this backdoor only holds when Combat Helper Sanity ISN'T item-gating her --
    # in modes 1/3, ItemManager.combat_helper_eligible("Athena") blocks HandleAthenaSpawn
    # outright until the separate "Athena Helper" item is received, with no exception for
    # holding the keepsake item itself, so both "Met Athena" and "Athena Keepsake" (which
    # only fire from her actually spawning/being gifted in-game) stay impossible without
    # it -- ORing the keepsake item in unconditionally would mark the location reachable
    # when it can never actually be triggered.
    if chs_mode not in (1, 3):
        for location in npc_locations("Athena"):
            add_rule(location, lambda state: state.has(ATHENA_KEEPSAKE_ITEM, player), combine="or")


def _set_shared_enemy_rules(world: "Hades2World", player: int, routes: list,
                            route_boss_conditions: dict) -> None:
    """Gate the 13 enemy names Nightmare shares with the existing Underworld roster (see
    Locations.SHARED_ENEMY_ZONES): these live in the Crossroads region (always reachable),
    not their original zone, precisely so their reachability can't be locked to one specific
    region -- see the comment on SHARED_ENEMY_ZONES for why an access_rule alone can't widen
    reachability across regions. July 18 (user ruling): these 13 only EXIST when the
    Nightmare route is in the seed, and only their NIGHTMARE zone counts for logic -- their
    Underworld-side spawns (Asphodel-anomaly detours etc.) are too rare/inconsistent to be
    load-bearing, though the mod still accepts an Underworld kill opportunistically. Only
    "King Vermin" (the one mini-boss among these 13 -- see MINIBOSS_ENEMY_NAMES) additionally
    needs that zone's own boss beaten, matching the per-zone enemy gate in set_rules. See the
    July 18 note there re: _is_miniboss_location -- same suffix-mismatch bug applied here too."""
    for name, zones in SHARED_ENEMY_ZONES.items():
        try:
            location = world.get_location(name, player)
        except KeyError:
            continue    # Nightmare excluded this seed -- location doesn't exist at all
        pairs = []
        for route, zi in zones:
            if route != NIGHTMARE or route not in routes or (route, zi) not in route_boss_conditions:
                continue
            zone_name, pred = route_boss_conditions[(route, zi)]
            pairs.append((zone_name, pred))
        if _is_miniboss_location(name):
            add_rule(location,
                     lambda state, pairs=pairs: any(
                         state.can_reach(zone, "Region", player) and pred(state)
                         for zone, pred in pairs))
        else:
            add_rule(location,
                     lambda state, pairs=pairs: any(
                         state.can_reach(zone, "Region", player) for zone, pred in pairs))


def _set_per_weapon_rules(world: "Hades2World", player: int, options, routes: list) -> None:
    """Gate each per-weapon room check behind owning the matching weapon."""
    for route in routes:
        prefix = ROUTES[route]["room_prefix"]
        for region_name in ROUTES[route]["zones"]:
            region = world.get_region(region_name, player)
            for location in region.locations:
                name = location.name
                if not name.startswith(prefix + " "):
                    continue
                weapon = name.rsplit(" ", 1)[-1]
                if weapon in WEAPON_SHORT_NAMES:
                    add_rule(location,
                             lambda state, w=weapon: state._hades2_has_weapon(w, player, options))


def _set_combined_score_rules(world: "Hades2World", player: int, options, routes: list) -> None:
    """combine_pools + point_based: gate each shared "Score NNNN" check. Points from EVERY
    active route bank into this one pool, so a check only needs SOME route to be able to reach
    the depth that funds it -- the whole pool is earnable on a single route. Mirrors
    _set_combined_room_rules: check N sits in the zone its index falls in (_zone_bounds over
    the pool size, exactly how fill_score_checks assigns per-route score checks to zones), and
    is reachable once that zone is reachable on ANY active route.

    The Surface branch carries the same caveat as the combined room pool: without the Penalty
    Cure the surface curse walls you off past its earliest checks
    (SURFACE_NO_CURE_SCORE_FRACTION, per Logic.txt), so funding a deeper check *via the
    Surface* also needs the cure. Any other route reaches the same depth uncapped."""
    try:
        region = world.get_region("Combined Score", player)
    except KeyError:
        return
    count = _combined_score_count(options)
    if count <= 0:
        return
    bounds = _zone_bounds(count)   # check n (1..count) lives in zone z where bounds[z] < n <= bounds[z+1]

    def zone_of(n: int) -> int:
        for z in range(4):
            if bounds[z] < n <= bounds[z + 1]:
                return z
        return 3

    for location in region.locations:
        n = _room_depth(location.name, COMBINED_SCORE_PREFIX)
        zi = zone_of(n)
        capped = (n / count) > SURFACE_NO_CURE_SCORE_FRACTION
        surface_zone = ROUTES[SURFACE]["zones"][zi] if SURFACE in routes else None
        other_zones = [ROUTES[route]["zones"][zi] for route in routes if route != SURFACE]
        add_rule(location,
                 lambda state, sz=surface_zone, others=other_zones, capped=capped:
                     any(state.can_reach(reg, "Region", player) for reg in others)
                     or (sz is not None
                         and state.can_reach(sz, "Region", player)
                         and (not capped
                              or state.has("Surface Penalty Cure", player))))


def _set_combined_room_rules(world: "Hades2World", player: int, options, routes: list) -> None:
    """combine_pools: gate each shared "Room NNNN" / "Room NNNN <Weapon>" check by depth.
    A check at depth d is reachable once depth d's zone is reachable on ANY active route
    (so the easier route satisfies it); per_weapon checks also need the matching weapon."""
    try:
        region = world.get_region("Combined Rooms", player)
    except KeyError:
        return
    count = _combined_room_count()
    bounds = _zone_bounds(count)   # depth d (1..count) lives in zone z where bounds[z] < d <= bounds[z+1]

    def zone_of(depth: int) -> int:
        for z in range(4):
            if bounds[z] < depth <= bounds[z + 1]:
                return z
        return 3

    for location in region.locations:
        # name: "Room NNNN", "Room NNNN <Weapon>", or with a " +k" scaling slot token
        # between the depth and the (optional, always-last) weapon.
        parts = location.name.split(" ")
        depth = int(parts[1])
        weapon = parts[-1] if parts[-1] in WEAPON_SHORT_NAMES else None
        zi = zone_of(depth)
        # A combined "Room N" check is reachable once depth N's zone is reachable on ANY
        # active route. The Surface branch is special: the surface curse walls you off past
        # room 3 without the Penalty Cure, so reaching a deeper combined room *via the
        # Surface* also needs the cure. The Underworld reaches the same depth with no such
        # cap. Together that's exactly the surface-only-start case: past room 3 you need
        # either a Progressive Underworld (to open the uncapped Underworld branch) or the
        # cure -- and fill keeps one of those in the early ungated sphere (rooms 1-3 / NPC
        # meets). The cure is always precollected, so the cure clause is trivially satisfied
        # and this collapses back to "any route's zone is reachable".
        capped = depth > SURFACE_NO_CURE_ROOM_DEPTH
        surface_zone = ROUTES[SURFACE]["zones"][zi] if SURFACE in routes else None
        other_zones = [ROUTES[route]["zones"][zi] for route in routes if route != SURFACE]
        add_rule(location,
                 lambda state, sz=surface_zone, others=other_zones, capped=capped:
                     any(state.can_reach(reg, "Region", player) for reg in others)
                     or (sz is not None
                         and state.can_reach(sz, "Region", player)
                         and (not capped
                              or state.has("Surface Penalty Cure", player))))
        if weapon:
            add_rule(location,
                     lambda state, w=weapon: state._hades2_has_weapon(w, player, options))
