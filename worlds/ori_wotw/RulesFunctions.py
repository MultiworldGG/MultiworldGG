from math import ceil, floor
from .Refills import refills
from worlds.AutoWorld import LogicMixin
from .Options import LogicDifficulty, StartingLocation

from typing import TYPE_CHECKING, cast, Any
if TYPE_CHECKING:
    from BaseClasses import CollectionState, MultiWorld
    from .Options import WotWOptions


class WotWLogic(LogicMixin):
    """
    Class to store the max health/energy, refill values and defeatable enemies.

    All methods and variables should start with `wotw_`.
    """
    wotw_max_resources: dict[int, tuple[int, float]]  # Max health and energy
    wotw_refill_amount: dict[int, tuple[int, float]]  # Refill amounts for health and energy
    wotw_enemies: dict[int, dict[str, float]]  # Energy cost to defeat each enemy
    wotw_resource_stale: dict[int, bool]  # Indicate if resource and refills have to be recomputed
    wotw_enemies_stale_collect: dict[int, bool]  # Indicate if combat has to be recomputed from collect
    wotw_enemies_stale_remove: dict[int, bool]  # Indicate if combat has to be recomputed from remove

    def init_mixin(self, mw: "MultiWorld") -> None:
        self.wotw_max_resources = {player: (30, 3.0) for player in mw.get_game_players("Ori and the Will of the Wisps")}
        self.wotw_refill_amount = {player: (30, 1.0) for player in mw.get_game_players("Ori and the Will of the Wisps")}
        self.wotw_enemies = {}
        for player in mw.get_game_players("Ori and the Will of the Wisps"):
            self.wotw_enemies.setdefault(player, {enemy: IMPOSSIBLE_COST for enemy in enemy_data.keys()})
        self.wotw_resource_stale = {player: True for player in mw.get_game_players("Ori and the Will of the Wisps")}
        self.wotw_enemies_stale_collect = {
            player: True for player in mw.get_game_players("Ori and the Will of the Wisps")
        }
        self.wotw_enemies_stale_remove = {
            player: True for player in mw.get_game_players("Ori and the Will of the Wisps")
        }

    def copy_mixin(self, new_state: "CollectionState") -> "CollectionState":
        new_state.wotw_max_resources = self.wotw_max_resources.copy()
        new_state.wotw_refill_amount = self.wotw_refill_amount.copy()
        new_state.wotw_enemies = {player: enemies.copy() for player, enemies in self.wotw_enemies.items()}
        new_state.wotw_enemies_stale_collect = self.wotw_enemies_stale_collect.copy()
        new_state.wotw_enemies_stale_remove = self.wotw_enemies_stale_remove.copy()
        return new_state

# Rules for some glitches
def can_wavedash(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Dash", "Regenerate"), player)

def can_hammerjump(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Double Jump", "Hammer"), player)

def can_swordjump(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Double Jump", "Sword"), player)

def can_glidehammerjump(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Glide", "Hammer"), player)

def can_glidebashchain(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Glide", "Bash"), player)

def can_doublejumpbashchain(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Glide", "Bash"), player)

def can_launchbashchain(state: "CollectionState", player: int) -> bool:
    return state.has_all(("Launch", "Bash"), player)

def can_pausefloat(state: "CollectionState", player: int) -> bool:
    return True

IMPOSSIBLE_COST = 1000.0  # Extremely high energy cost, used when a requirement is not met
# The value is arbitrary value, but it must be higher than 20 (which is the max energy that you can get)


weapon_data: dict[str, tuple[int, float]] = {  # The tuple contains the damage per use, and the energy cost
    "Grenade": (13, 1),  # Can be 17 damage if charged
    "Shuriken": (7, 0.5),
    "Bow": (4, 0.25),
    "Flash": (12, 1),
    "Sentry": (8, 1),  # 8.8 damage, rounded down here
    "Spear": (20, 2),
    "Blaze": (13, 1),  # 13.8 damage, rounded down here
    "SentryJump": (8, 1),  # Same as Sentry values
    "SwordSJump": (8, 1),
    "HammerSJump": (8, 1),
    }

enemy_data: dict[str, tuple[int, list[str]]] = {  # For each enemy: HP and combat tags required
    "Mantis": (32, []),
    "Slug": (13, []),
    "WeakSlug": (12, []),
    "BombSlug": (1, ["Combat.Ranged"]),
    "CorruptSlug": (1, ["Combat.Ranged"]),
    "SneezeSlug": (32, ["Combat.Dangerous"]),
    "ShieldSlug": (24, []),
    "Lizard": (24, []),
    "Bat": (32, ["Combat.Bat", "Combat.Aerial", "Combat.Ranged"]),
    "Hornbug": (40, ["Combat.Dangerous", "Combat.Shielded"]),
    "Skeeto": (20, ["Combat.Aerial"]),
    "SmallSkeeto": (8, ["Combat.Aerial"]),
    "Bee": (24, ["Combat.Aerial"]),
    "Nest": (25, ["Combat.Aerial"]),
    "Fish": (10, []),
    "Waterworm": (20, []),
    "Crab": (32, ["Combat.Dangerous"]),
    "SpinCrab": (32, ["Combat.Dangerous"]),
    "Tentacle": (40, ["Combat.Ranged"]),
    "Balloon": (1, []),
    "Miner": (40, ["Combat.Dangerous"]),
    "MaceMiner": (60, ["Combat.Dangerous"]),
    "ShieldMiner": (60, ["Combat.Dangerous", "Combat.Shielded"]),
    "CrystalMiner": (80, ["Combat.Dangerous"]),
    "ShieldCrystalMiner": (50, ["Combat.Dangerous", "Combat.Shielded"]),
    "Sandworm": (20, ["Combat.Sand"]),
    "Spiderling": (12, []),
}


def get_max(state: "CollectionState", player: int) -> tuple[int, float]:
    """Return the current max health and energy."""
    wisps = state.count_from_list(("EastHollow.ForestsVoice", "LowerReach.ForestsMemory", "UpperDepths.ForestsEyes",
                                  "WestPools.ForestsStrength", "WindtornRuins.Seir"), player)
    return (30 + state.count("Health Fragment", player)*5 + 10*wisps,
            3 + state.count("Energy Fragment", player)*0.5 + wisps)


def get_refill(state: "CollectionState", player: int) -> tuple[int, int]:
    """Return the refill values."""
    max_h, max_e = state.wotw_max_resources[player]
    refill_h = min((4 + floor(max_h/50/0.6685)) * 10, max_h)
    refill_e = floor(max_e/5+1)
    return refill_h, refill_e


def get_enemy_cost(enemy: str, state: "CollectionState", player: int, options: "WotWOptions") -> float:
    """Return the energy cost to defeat the enemy (or IMPOSSIBLE_COST if the tags are not fulfilled)."""
    data = enemy_data[enemy]
    if not state.has_all(data[1], player):  # Check the tags
        return IMPOSSIBLE_COST

    if state.has_any(("Sword", "Hammer"), player):
        return 0

    if options.difficulty.value == LogicDifficulty.option_moki:
        possible_weapons = []  # Only use Sword or Hammer in Moki
    elif options.difficulty.value == LogicDifficulty.option_unsafe:
        possible_weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze", "Flash"]
    else:
        possible_weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]

    cost = IMPOSSIBLE_COST
    for weapon in possible_weapons:
        if state.has(weapon, player):
            cost = min(cost, weapon_data[weapon][1] * ceil(data[0] / weapon_data[weapon][0]))
    return cost


def has_enough_max_health(state: "CollectionState", player: int, options: "WotWOptions", value: int) -> bool:
    """Check if the player has enough max health to solve the region requirement."""
    if state.wotw_resource_stale[player]:  # Update the resources and refill values if needed
        state.wotw_max_resources[player] = get_max(state, player)
        state.wotw_refill_amount[player] = get_refill(state, player)
        state.wotw_resource_stale[player] = False

    if options.hard_mode:
        return state.wotw_max_resources[player][0] > 2 * value
    return state.wotw_max_resources[player][0] > value


def can_buy_map(state: "CollectionState", player: int) -> bool:
    """Maps are logically required after collecting 1200 SL from 200 SL items."""
    return state.count("200 Spirit Light", player) >= 6


def can_buy_shop(state: "CollectionState", player: int) -> bool:
    """Shops are logically required after collecting 1200 SL from 200 SL items."""
    return state.count("200 Spirit Light", player) >= 6


def can_open_door(door_name: str, state: "CollectionState", player: int, spawn: int) -> bool:
    """
    Return if the door can be opened. The keystone (KS) costs are arbitrary.

    10 KS for early game doors that only require 2 KS to open.
    14 KS are mid-game doors that cost 2 KS (these doors are relevant early with random spawn).
    22 KS for mid-game doors at 4 KS.
    34 KS (enough KS to open everything) for doors that can be avoided or only lock a few items (and no trees).
    Depending on the spawn, some doors are made accessible very early, to avoid a fill error when teleporters are not
    in the pool (this concern doors that you need to cross to get access to most of the map).
    """
    required_ks: int
    # Early game doors: 10 KS (or less if spawning nearby).
    if door_name == "MarshSpawn.KeystoneDoor":
        required_ks = 2 if spawn == StartingLocation.option_marsh else 10
    elif door_name == "HowlsDen.KeystoneDoor":
        required_ks = 2 if spawn == StartingLocation.option_howlsden else 10
    elif door_name == "MarshPastOpher.EyestoneDoor":
        required_ks = 10
    # Midgame doors that lock access to some areas: 14 KS (or less if spawning nearby)
    elif door_name == "WoodsEntry.KeystoneDoor":
        required_ks = 2 if spawn == StartingLocation.option_westwoods else 14
    elif door_name == "WoodsMain.KeystoneDoor":
        required_ks = 6 if spawn in (StartingLocation.option_westwoods,
                                     StartingLocation.option_eastwoods,
                                     StartingLocation.option_westwastes) else 14
    elif door_name == "UpperDepths.EntryKeystoneDoor":
        required_ks = 2 if spawn == StartingLocation.option_depths else 14
    elif door_name == "UpperWastes.KeystoneDoor":
        required_ks = 2 if spawn in (StartingLocation.option_outerruins,
                                     StartingLocation.option_innerruins,
                                     StartingLocation.option_eastwastes) else 14
    # Midgame doors that are less critical, but usually required for completion: 22 KS
    elif door_name in ("UpperReach.KeystoneDoor", "UpperPools.KeystoneDoor"):
        required_ks = 22
    # Misc doors that are rarely used: 34 KS (which is enough to open every door)
    elif door_name in ("MidnightBurrows.KeystoneDoor", "UpperDepths.CentralKeystoneDoor", "LowerReach.KeystoneDoor"):
        required_ks = 34
    else:
        raise ValueError(f"Unknown keystone door: {door_name}.")
    return state.count("Keystone", player) >= required_ks


def has_enough_resources(requirements_all: list[tuple[str, Any]],
                         requirements_any: list[tuple[str, Any]],
                         region: str,
                         state: "CollectionState",
                         player: int,
                         options: "WotWOptions",
                         is_moki: bool) -> bool:
    """
    Check if the player has enough energy/health to use the path.

    :param requirements_all: List of requirements, the tuples contain a key (str) and a data object.
                             All of them must be satisfied from the same initial health/energy pool.
    :param requirements_any: List of requirements, at least one must be valid.
                             The health/energy pool is reset each time, from what remains after the all part.
    :param region: The starting region of the path.
    :param state: The CollectionState object.
    :param player: The player int.
    :param options: The WotWOptions object.
    :param is_moki: Whether the path is moki (lowest difficulty).
    """
    if state.wotw_resource_stale[player]:  # Update the resources and refill values if needed
        state.wotw_max_resources[player] = get_max(state, player)
        state.wotw_refill_amount[player] = get_refill(state, player)
        state.wotw_resource_stale[player] = False

    max_h, max_e = state.wotw_max_resources[player]
    health, energy = 10, 1.0  # Minimal values, can lead to softlocks in specific situations
    refill_e, refill_h, refill_type = refills[region]

    # Apply the refills
    if is_moki:  # Moki has no damage boost and barely requires energy, so this is fine.
        health, energy = max_h, max_e
    else:
        if refill_type == 2 and state.has("F." + region, player):  # Full refill
            health, energy = max_h, max_e
        else:
            if refill_type == 1 and state.has("C." + region, player):  # Checkpoint
                health, energy = state.wotw_refill_amount[player]
            if refill_h != 0 and state.has("H." + region, player):  # Health plant
                health += refill_h*10
            if refill_e != 0 and state.has("E." + region, player):  # Energy crystal
                energy += refill_e
        health, energy = min(max_h, health), min(max_e, energy)  # Make sure that it does not go over the maximum

    energy_cost: float
    # Compute the requirements
    for i, (req_type, data) in enumerate(requirements_all + requirements_any):
        if req_type == "db":  # Damage boost
            cast(int, data)
            health, energy_cost = compute_dboost(data, health, max_h, state, player, bool(options.hard_mode))
            # Remark: the health is not reset in the `any` part, but it is fine since there is at most one damage boost
            # in requirements_any, and health does not affect the other types of requirements.
        elif req_type == "combat":
            cast(str, data)
            energy_cost = compute_combat(data, state, player, options)
        elif req_type == "wall":
            cast(tuple[str, int], data)
            energy_cost = compute_wall(data, state, player, options)
        else:  # req_type == "energy"
            cast(tuple[str, int], data)
            energy_cost = compute_energy(data, state, player)
        if i < len(requirements_all):  # This means that it is parsing the `all` part
            energy -= energy_cost
            if energy < 0:  # Not enough energy, or a required skill is missing
                return False
        elif energy >= energy_cost:  # Currently parsing the `any` part, and this path is valid
            return True
    if requirements_any:  # There is at least one requirement from `any`, and no requirement can be fulfilled: invalid
        return False
    return True  # `All` requirements parsed, and not out of energy: path is valid


def compute_dboost(damage: int,
                   health: int,
                   max_health:int,
                   state: "CollectionState",
                   player: int,
                   is_hard: bool) -> tuple[int, float]:
    """Return the new health and the energy cost after the damage boost."""
    n_regen = 0.0  # Number of Regenerate used, i.e. the energy cost
    if is_hard:  # Hard difficulty doubles the damage taken
        damage *= 2
    health -= damage
    if health <= 0:  # Not enough health, Regenerate must be used beforehand
        if state.has("Regenerate", player) and damage < max_health:
            n_regen = ceil((-health + 1) / 30)  # Amount of regenerate needed
            health = health + 30 * n_regen
        else:
            n_regen = IMPOSSIBLE_COST
    return health, n_regen


def compute_combat(defeat_enemy: str,
                   state: "CollectionState",
                   player: int,
                   options: "WotWOptions") -> float:
    """Return the energy cost to defeat the enemy."""
    # Update the energy cost for combat if required
    if state.wotw_enemies_stale_collect[player] or state.wotw_enemies_stale_remove[player]:
        for enemy in state.wotw_enemies[player].keys():
            if ((state.wotw_enemies[player][enemy] != 0
                     or state.wotw_enemies_stale_remove[player])
                and (state.wotw_enemies[player][enemy] != IMPOSSIBLE_COST
                     or state.wotw_enemies_stale_collect[player])):
                # No need to recheck the cost when it is 0 and no release happened
                # And same when the enemy cannot be defeated and no collect happened
                state.wotw_enemies[player][enemy] = get_enemy_cost(enemy, state, player, options)
        state.wotw_enemies_stale_collect[player] = False
        state.wotw_enemies_stale_remove[player] = False

    # Return the energy cost for the enemy that the rule require to defeat
    return state.wotw_enemies[player][defeat_enemy]


def compute_wall(data: tuple[str, int],
                 state: "CollectionState",
                 player: int,
                 options: "WotWOptions") -> float:
    """Return the energy cost for breaking a wall (or killing a boss)."""
    break_type, damage = data
    if state.has_any(("Sword", "Hammer"), player) and break_type in ("BreakWall", "Boss"):
        return 0

    if break_type in ("BreakWall", "Boss"):
        weapons = ["Grenade", "Bow", "Shuriken", "Sentry", "Spear", "Blaze"]
    elif break_type == "shuriken":
        weapons = ["Shuriken"]
        if options.difficulty.value == LogicDifficulty.option_unsafe:
            damage *= 2
        else:
            damage *= 3
    else:  # break_type == "sentry"
        weapons = ["Sentry"]
        damage *= 6
    cost = IMPOSSIBLE_COST
    for weapon in weapons:
        if state.has(weapon, player):
            cost = min(cost, weapon_data[weapon][1] * ceil(damage / weapon_data[weapon][0]))
    return cost


def compute_energy(data: tuple[str, int],
                   state: "CollectionState",
                   player: int) -> float:
    """Return the energy cost for using the energy weapons."""
    weapon, times = data
    # Check for the non-energy requirements for sentry jumps
    if weapon == "SentryJump" and not state.has_any(("Sword", "Hammer"), player):
        return IMPOSSIBLE_COST
    elif weapon == "SwordSJump" and not state.has("Sword", player):
        return IMPOSSIBLE_COST
    elif weapon == "HammerSJump" and not state.has("Hammer", player):
        return IMPOSSIBLE_COST
    # In any cases, check for the energy cost (and if the energy weapon is there)
    if not state.has(weapon, player):
        return IMPOSSIBLE_COST
    return weapon_data[weapon][1] * times
