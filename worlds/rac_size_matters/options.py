from dataclasses import dataclass

from Options import (
    Accessibility,
    Choice,
    DeathLink,
    DefaultOnToggle,
    ItemDict,
    OptionCounter,
    OptionGroup,
    PerGameCommonOptions,
    ProgressionBalancing,
    Range,
    StartInventoryPool,
    Toggle,
)

from .constants.options import Rac5Options
from .data.challenges import (
    CHALLENGE_GROUP_DERBY,
    CHALLENGE_GROUP_GADGETBOT,
    CHALLENGE_GROUP_GADGETBOT_TOSS,
    DEFAULT_CLANK_CHALLENGE_GROUPS,
)
from .data.traps import TRAP_DURATIONS
from .items import DEFAULT_ENABLED_WEAPONS, WEAPON_DISPLAY_TO_INTERNAL


class ClankPack(Toggle):
    """Start without Clank on Ratchet's back and add one Clank Pack item to the pool.
    Receiving it unlocks Clank's backpack abilities, including high and long jumps.
    The No Clank trap can still temporarily disable the pack after it is unlocked.
    Playable Clank sections are unaffected. Disabled by default."""

    display_name = "Clank Pack"


class ProgressiveWeapons(Choice):
    """Replace each weapon's individual unlock item with a single Progressive Weapon
    item per weapon: the first copy unlocks the weapon, each subsequent copy grants
    the next level upgrade.
    off: weapons are normal individual items with no level-up items (levels work as
    in vanilla).
    manual: leveling still happens by playing normally, but is capped at whatever
    level the Progressive Weapon items received so far allow — reaching that cap
    freezes further experience gain until the next copy arrives.
    automatic: level is set directly to match Progressive Weapon items received,
    with experience gain disabled entirely (no need to play to level up)."""

    display_name = "Progressive Weapons"
    option_off = 0
    option_manual = 1
    option_automatic = 2
    default = 0


class ProgressiveMods(Toggle):
    """Replace each weapon's individual mod items with a single Progressive Mod item
    per weapon: each copy grants the next mod slot in sequence. When off, each mod
    slot is its own individual item."""

    display_name = "Progressive Mods"


class ProgressiveArmour(Choice):
    """Controls how armour pieces are unlocked.
    off: each armour piece is its own individual item (vanilla-style, shuffled independently).
    per_set: each armour set has its own Progressive item (Progressive Wildfire, Progressive
    Sludge Mk9, etc.) — 4 copies of a set's item unlock that set's 4 pieces in order,
    independently of every other set.
    unified: a single "Progressive Armour" item replaces every per-set item. Copies grant
    pieces one set at a time, in a fixed order: Wildfire, Sludge Mk9, Crystallix,
    Electroshock, Mega Bomb, Hyperborean, Chameleon — so every Wildfire piece is granted
    before the first Sludge Mk9 piece, and so on."""

    display_name = "Progressive Armour"
    option_off = 0
    option_per_set = 1
    option_unified = 2
    default = 0


class EnabledWeapons(ItemDict):
    """Selects which weapons are included in generation at all. Set a weapon to 0 to
    remove it entirely: its own item(s) (including its Progressive Weapon/Mod items),
    its vendor/collectible location, its mod-vendor locations, and its Weapon Level
    Checks locations are all excluded from the pool, exactly as if the weapon didn't
    exist in this seed. Default 1 includes every weapon. At least one long-range
    projectile weapon must remain available after applying NG+ Items."""

    display_name = "Enabled Weapons"
    verify_item_name = False
    min = 0
    max = 1
    valid_keys = tuple(WEAPON_DISPLAY_TO_INTERNAL.keys())
    default = DEFAULT_ENABLED_WEAPONS


class ClankChallenges(Choice):
    """Controls how Clank challenge arenas are included as location checks.
    item_challenges: only the armour/gadget reward for each challenge arena (default).
    all: every individual challenge completion is a separate check."""

    display_name = "Clank Challenges"
    option_off = 0
    option_item_challenges = 1
    option_all = 2
    default = 1


class ClankChallengeGroups(ItemDict):
    """Selects which Clank Challenge groups (Metalis/Dayni Moon) are included
    as location checks, whenever Clank Challenges is on. Set a group to 0 to
    exclude all of its locations (both the item-reward and individual-
    completion tiers) from generation entirely — the challenge is still
    playable in-game, it just has no AP checks. Default 1 includes every
    group."""

    display_name = "Clank Challenge Groups"
    verify_item_name = False
    min = 0
    max = 1
    valid_keys = (CHALLENGE_GROUP_DERBY, CHALLENGE_GROUP_GADGETBOT_TOSS, CHALLENGE_GROUP_GADGETBOT)
    default = DEFAULT_CLANK_CHALLENGE_GROUPS


class SkyboardChallenges(Choice):
    """Controls whether Skyboard race challenges are included as location checks.
    all: every individual race completion is a separate check."""

    display_name = "Skyboard Challenges"
    option_off = 0
    option_all = 1
    default = 0


class ShrinkRayOptions(Choice):
    """Controls how Shrink Ray puzzles are handled.
    off: normal vanilla behavior — puzzles must be solved as usual, no checks.
    locations: include Shrink Ray puzzle completions as location checks.
    skip: unlock puzzle doors directly, without owning or activating the Shrink
    Ray. Puzzle completion checks are not included."""

    display_name = "Shrink Ray Options"
    option_off = 0
    option_locations = 1
    option_skip = 2
    default = 1


class AmmoLink(Toggle):
    """Share weapon ammo with every other connected player who also has
    AmmoLink enabled (and toggled on client-side, same as DeathLink):
    whenever your ammo for a weapon changes, everyone else linked for that
    weapon gets mirrored to the same count, and vice versa. Players don't
    need to own the same weapons for this to work — a weapon you don't
    have simply isn't affected."""

    display_name = "Ammo Link"


class BoltLink(Toggle):
    """Share your bolt count with every other connected player who also has
    Bolt Link enabled (and toggled on client-side, same as DeathLink): your
    bolt count mirrors everyone else's -- spend or collect bolts on any
    linked player and everyone else's balance matches."""

    display_name = "Bolt Link"


class GhostLink(Toggle):
    """See another connected player as a ghost clone whenever you're both on
    the same planet (and they also have Ghost Link enabled and toggled on
    client-side, same as DeathLink). Only one ghost can be rendered at a
    time -- if more than one linked player shares your planet, one is
    picked automatically."""

    display_name = "Ghost Link"


class GhostLinkUpdateInterval(Range):
    """How often (in seconds) your position is broadcast to other Ghost Link
    players while Ghost Link is enabled. 0 broadcasts as fast as possible
    (every poll tick, no throttling)."""

    display_name = "Ghost Link Update Interval"
    range_start = 0
    range_end = 100
    default = 5


class AllMissions(DefaultOnToggle):
    """Include story mission completions as location checks.
    Covers main narrative objectives on each planet."""

    display_name = "All Missions"


class AllCutscenes(Toggle):
    """Include cutscene and flag events as location checks.
    Covers encounter triggers and scripted events detected via flag bits."""

    display_name = "All Cutscenes"


class GiantClank(Toggle):
    """Include the Giant Clank Metalis and Giant Clank Challax sequences: their
    completion/armour-pickup location checks, and (with Skill Points on) their
    skill point checks.
    off (default): both sequences are locked out entirely — entering either one
    immediately forces a load back out, exactly like vanilla before this option
    existed. Nothing from them is ever checked or required.
    on: both sequences become playable; entering plays them start-to-finish with
    no AP items/notifications until their location(s) fire."""

    display_name = "Giant Clank"


class ArmourSetChecks(DefaultOnToggle):
    """Treat equipping a complete armour set as a location check. Adds 13 locations to the pool."""

    display_name = "Armour Set Checks"


class NgPlusItems(DefaultOnToggle):
    """Include RYNO and the Chameleon/Hyperborean armour sets in generation. These are New
    Game Plus exclusives in vanilla, so turning this off is intended for players doing a
    fresh (non-NG+) playthrough where those items would never actually be obtainable.
    off: RYNO and the Chameleon/Hyperborean armour pieces are removed from the item pool
    entirely. Also removes the RYNO Weapon Level checks, and the Chameleon/Hyperborean
    Armour Set checks along with Stalker/Ice II (both of which need a Chameleon or
    Hyperborean piece to complete)."""

    display_name = "NG+ Items"


class ChallengeMode(Range):
    """Max Challenge Mode tier (New Game Plus) and how far into it generation reaches.
    With Progressive Challenge Mode on, this is the maximum tier the Progressive
    Challenge Mode items can raise you to. Otherwise it is the Challenge Mode tier
    the game starts in, written to game memory at connect.
    0: vanilla — no Challenge Mode content.
    1: Challenge Mode 1 — adds the RYNO vendor purchase, 10 Challenge-Mode-only
    weapon mod purchases, and the 4 Hyperborean armour pieces as real pickups.
    2: Challenge Mode 2 — everything from tier 1, plus the 4 Chameleon armour
    pieces as real pickups.
    Every item this unlocks a location for is still governed by NG+ Items —
    with that option off, none of them are placed in the pool at all, so this
    option alone has no effect."""

    display_name = "Max Challenge Mode"
    range_start = 0
    range_end = 2
    default = 0


class ProgressiveChallengeMode(Toggle):
    """Gates Challenge Mode content behind a "Progressive Challenge Mode" item instead
    of it being unconditionally accessible as soon as the Max Challenge Mode option enables
    it. Max Challenge Mode still controls the ceiling — how many copies end up in the pool,
    and how far generation reaches — this only changes when that content becomes
    logically reachable.
    off (default): Challenge Mode content (RYNO, Titan variants, Challenge-Mode-only
    mods, Hyperborean/Chameleon pickups) is reachable as soon as its planet is, same as
    today.
    on: one "Progressive Challenge Mode" item per tier is added to the pool (so Max Challenge
    Mode 2 adds 2 copies); tier-1 content requires 1 copy received, tier-2 content
    requires 2. The in-game Challenge Mode tier itself now rises as copies come in,
    up to Max Challenge Mode, instead of being fixed at connect."""

    display_name = "Progressive Challenge Mode"


class SkillPoints(Choice):
    """Include skill point challenges as location checks.
    off: no skill point checks.
    easy: a curated set of easier skill points only.
    hard: also includes a curated set of harder skill points.
    Clank Challenge and Skyboard Challenge skill points are controlled separately
    by the Enable Clank Challenge Skill Points and Enable Skyboard Challenge Skill
    Points options below, regardless of this setting."""

    display_name = "Skill Points"
    option_off = 0
    option_easy = 1
    option_hard = 2
    default = 0


class EnableClankChallengeSkillPoints(Toggle):
    """Include skill points earned from Clank Challenge arenas as location checks,
    regardless of the Clank Challenges option."""

    display_name = "Enable Clank Challenge Skill Points"


class EnableSkyboardChallengeSkillPoints(Toggle):
    """Include skill points earned from Skyboard Challenges as location checks,
    regardless of the Skyboard Challenges option."""

    display_name = "Enable Skyboard Challenge Skill Points"


class StartingWeapons(Range):
    """Number of random weapons the player begins the game with, capped at the
    number of enabled weapons available with NG+ Items applied."""

    display_name = "Starting Weapons"
    range_start = 0
    range_end = 13
    default = 2


class StartingGadgets(Range):
    """Number of random gadgets the player begins the game with. Default of 1 grants the Hypershot."""

    display_name = "Starting Gadgets"
    range_start = 0
    range_end = 8
    default = 1


class RandomStartingPlanet(Choice):
    """Randomizes which two planets Ratchet starts with access to, instead of always
    starting on Pokitaru. Its infobot goes back into the normal item pool
    and two random planets' infobots are precollected in their place. Dreamtime,
    Inside Clank, and Quodrona are never candidates: the first two need extra gadgets
    beyond their own infobot to enter, and Quodrona is the goal planet.
    off: start on Pokitaru; Ryllus requires its separate infobot.
    weighted: candidate planets are weighted by how many locations they offer under the
    current options, so denser planets are more likely to be picked. Weapon/Gadget
    Vendor locations only count towards a planet's weight if Starting Weapons/Starting
    Gadgets is set above 0.
    unweighted: two of the 7 candidate planets are chosen completely at random, ignoring
    location counts entirely."""

    display_name = "Random Starting Planet"
    option_off = 0
    option_weighted = 1
    option_unweighted = 2
    default = 0


class DeathAmnesty(Range):
    """Number of deaths allowed before items are removed from the player's inventory on death.
    Higher values are more forgiving."""

    display_name = "Death Amnesty"
    range_start = 0
    range_end = 5
    default = 0


class StartingBolts(Range):
    """Number of bolts the player begins the game with."""

    display_name = "Starting Bolts"
    range_start = 0
    range_end = 100_000
    default = 45_000


class TrapChance(Range):
    """Percent chance for each filler item to be replaced with a trap instead of Bolts."""

    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeight(ItemDict):
    """Sets the relative weights of trap types in the filler pool. A higher value increases
    how often that trap is chosen over the others when a filler item rolls as a trap (see
    Trap Chance). Has no effect when Trap Chance is 0, or when every weight here is 0
    (Bolts fills in instead)."""

    display_name = "Trap Weight"
    min = 0
    max = 100
    valid_keys = TRAP_DURATIONS.keys()
    default = dict.fromkeys(TRAP_DURATIONS.keys(), 1)


class TrapDuration(OptionCounter):
    """How many seconds each trap type stays active once triggered."""

    display_name = "Trap Duration"
    min = 1
    max = 300
    valid_keys = TRAP_DURATIONS.keys()
    default = dict(TRAP_DURATIONS)


class WeaponExperienceMultiplier(Range):
    """Multiplies weapon experience gained each time the game grants it, speeding up
    weapon leveling. Stops applying once a weapon reaches level 4 (max level for
    every weapon). 0/1 = no boost."""

    display_name = "Weapon Experience Multiplier"
    range_start = 0
    range_end = 16
    default = 4


class BoltMultiplier(Range):
    """Multiplies bolts gained each time the game grants them (crates, enemies, etc.),
    speeding up bolt income. Does not affect one-off AP grants like starting bolts.
    0/1 = no boost."""

    display_name = "Bolt Multiplier"
    range_start = 0
    range_end = 16
    default = 4


class NanotechExperienceMultiplier(Range):
    """Multiplies Nanotech (health) experience gained each time the game grants it,
    speeding up Nanotech leveling. 0/1 = no boost."""

    display_name = "Nanotech Experience Multiplier"
    range_start = 0
    range_end = 16
    default = 4


class NanotechLevelInterval(Choice):
    """Include reaching Nanotech (health) Levels as location checks.
    off: no Nanotech Level checks.
    all: every single level is its own check, up to Nanotech Level Max.
    every_5/every_10/every_25: one check every N levels (e.g. every_5 checks levels
    10, 15, 20, ...), up to Nanotech Level Max. Levels above 20 require access to a
    good EXP planet."""

    display_name = "Nanotech Level Interval"
    option_off = 0
    option_all = 1
    option_every_5 = 5
    option_every_10 = 10
    option_every_25 = 25
    default = 0


class NanotechLevelMax(Range):
    """Highest Nanotech Level Nanotech Level Interval creates a check for — e.g.
    every_5 with this set to 25 checks only levels 10, 15, 20, 25. No effect while
    Nanotech Level Interval is off."""

    display_name = "Nanotech Level Max"
    range_start = 6
    range_end = 75
    default = 75


class WeaponLevelChecks(Choice):
    """Adds location checks for reaching weapon levels, in addition to whatever
    unlocks the weapon in the first place.
    off: no weapon level checks.
    level_4: one check per weapon, for reaching level 4 (vanilla max level).
    level_8: one check per weapon, for reaching level 8 (Challenge Mode Titan max
    level) — only meaningful with Challenge Mode 1+.
    level_4_and_8: both of the above.
    all: one check per weapon per level (2 through 8, Challenge Mode levels 5-8
    included when Challenge Mode is 1+)."""

    display_name = "Weapon Level Checks"
    option_off = 0
    option_level_4 = 1
    option_level_8 = 2
    option_level_4_and_8 = 3
    option_all = 4
    default = 0


class BalancePatch(Toggle):
    """Enable usernamecipher's Update 1.03 weapon and movement balance patch.
    Disabled by default."""

    display_name = "Balance Patch"
    default = 0


class ExperimentalSkins(Toggle):
    """Patches the thirteen red multiplayer skins into the single-player skin menu.
    Experimental. When off, the multiplayer skins aren't patched in at all, and
    Starting Skin can't be set to one of them."""

    display_name = "Experimental Skins"


class StartingSkin(Choice):
    """Cosmetic skin for Ratchet. Applied automatically on each planet load.
    Includes the thirteen red multiplayer skins (MP Ratchet onwards), which need
    Experimental Skins on; blue variants are excluded.
    All skins are unlocked in-game regardless of this choice."""

    display_name = "Starting Skin"
    option_default = 0
    option_pirate_ratchet = 1
    option_godzilla_ratchet = 2
    option_trash_ratchet = 3
    option_swim_ratchet = 4
    option_kanga_ratchet = 5
    option_hiro_ratchet = 6
    option_mp_ratchet = 7
    option_snowman = 8
    option_hotbot = 9
    option_qwark = 10
    option_ninja = 11
    option_training_bot = 12
    option_nurse = 13
    option_technomite = 14
    option_dan = 15
    option_low_rider_ratchet = 16
    option_samurai_ratchet = 17
    option_kangaroo_ratchet = 18
    option_tuxedo_ratchet = 19
    default = 0


class ApIcon(Choice):
    """Default Archipelago icon shown on vendor items. Can still be changed while
    playing with the /apicon client command."""

    display_name = "AP Icon"
    option_original = 0
    option_purple = 1
    option_grey = 2
    option_blue = 3
    default = 0


@dataclass
class RACSizeMatterOptions(PerGameCommonOptions):
    __annotations__ = {
        Rac5Options.START_INVENTORY_FROM_POOL: StartInventoryPool,
        Rac5Options.PROGRESSIVE_WEAPONS: ProgressiveWeapons,
        Rac5Options.CLANK_PACK: ClankPack,
        Rac5Options.PROGRESSIVE_MODS: ProgressiveMods,
        Rac5Options.PROGRESSIVE_ARMOUR: ProgressiveArmour,
        Rac5Options.ENABLED_WEAPONS: EnabledWeapons,
        Rac5Options.DEATH_LINK: DeathLink,
        Rac5Options.DEATH_AMNESTY: DeathAmnesty,
        Rac5Options.AMMO_LINK: AmmoLink,
        Rac5Options.BOLT_LINK: BoltLink,
        Rac5Options.GHOST_LINK: GhostLink,
        Rac5Options.GHOST_LINK_UPDATE_INTERVAL: GhostLinkUpdateInterval,
        Rac5Options.ALL_MISSIONS: AllMissions,
        Rac5Options.ALL_CUTSCENES: AllCutscenes,
        Rac5Options.GIANT_CLANK: GiantClank,
        Rac5Options.CLANK_CHALLENGES: ClankChallenges,
        Rac5Options.CLANK_CHALLENGE_GROUPS: ClankChallengeGroups,
        Rac5Options.ENABLE_CLANK_CHALLENGE_SKILL_POINTS: EnableClankChallengeSkillPoints,
        Rac5Options.SKYBOARD_CHALLENGES: SkyboardChallenges,
        Rac5Options.ENABLE_SKYBOARD_CHALLENGE_SKILL_POINTS: EnableSkyboardChallengeSkillPoints,
        Rac5Options.SHRINK_RAY_OPTIONS: ShrinkRayOptions,
        Rac5Options.ARMOUR_SET_CHECKS: ArmourSetChecks,
        Rac5Options.NG_PLUS_ITEMS: NgPlusItems,
        Rac5Options.PROGRESSIVE_CHALLENGE_MODE: ProgressiveChallengeMode,
        Rac5Options.CHALLENGE_MODE: ChallengeMode,
        Rac5Options.SKILL_POINTS: SkillPoints,
        Rac5Options.STARTING_WEAPONS: StartingWeapons,
        Rac5Options.STARTING_GADGETS: StartingGadgets,
        Rac5Options.RANDOM_STARTING_PLANET: RandomStartingPlanet,
        Rac5Options.STARTING_BOLTS: StartingBolts,
        Rac5Options.EXPERIMENTAL_SKINS: ExperimentalSkins,
        Rac5Options.BALANCE_PATCH: BalancePatch,
        Rac5Options.STARTING_SKIN: StartingSkin,
        Rac5Options.AP_ICON: ApIcon,
        Rac5Options.TRAP_CHANCE: TrapChance,
        Rac5Options.TRAP_WEIGHT: TrapWeight,
        Rac5Options.TRAP_DURATION: TrapDuration,
        Rac5Options.WEAPON_EXPERIENCE_MULTIPLIER: WeaponExperienceMultiplier,
        Rac5Options.BOLT_MULTIPLIER: BoltMultiplier,
        Rac5Options.NANOTECH_EXPERIENCE_MULTIPLIER: NanotechExperienceMultiplier,
        Rac5Options.WEAPON_LEVEL_CHECKS: WeaponLevelChecks,
        Rac5Options.NANOTECH_LEVEL_INTERVAL: NanotechLevelInterval,
        Rac5Options.NANOTECH_LEVEL_MAX: NanotechLevelMax,
    }


racsm_option_groups = [
    OptionGroup(
        "Generic Options",
        [
            ProgressionBalancing,
            Accessibility,
            BalancePatch,
        ],
    ),
    OptionGroup(
        "RACSM Game Links",
        [
            DeathLink,
            DeathAmnesty,
            AmmoLink,
            BoltLink,
            GhostLink,
            GhostLinkUpdateInterval,
        ],
    ),
    OptionGroup(
        "RACSM Item Options",
        [
            StartingWeapons,
            StartingGadgets,
            ClankPack,
            RandomStartingPlanet,
            StartingBolts,
            ProgressiveWeapons,
            ProgressiveMods,
            ProgressiveArmour,
            EnabledWeapons,
            TrapChance,
            TrapWeight,
            TrapDuration,
            WeaponExperienceMultiplier,
            BoltMultiplier,
            NanotechExperienceMultiplier,
        ],
    ),
    OptionGroup(
        "RACSM Challenges",
        [
            ClankChallenges,
            ClankChallengeGroups,
            EnableClankChallengeSkillPoints,
            SkyboardChallenges,
            EnableSkyboardChallengeSkillPoints,
            GiantClank,
        ],
    ),
    OptionGroup(
        "RACSM Location Options",
        [
            AllMissions,
            AllCutscenes,
            ShrinkRayOptions,
            SkillPoints,
            ArmourSetChecks,
            WeaponLevelChecks,
            NanotechLevelInterval,
            NanotechLevelMax,
            NgPlusItems,
            ProgressiveChallengeMode,
            ChallengeMode,
        ],
    ),
    OptionGroup(
        "RACSM Cosmetic Options",
        [
            ExperimentalSkins,
            StartingSkin,
            ApIcon,
        ],
    ),
]
