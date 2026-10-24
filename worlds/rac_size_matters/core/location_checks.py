from ..constants import Rac5CutsceneLocations, Rac5Locations, Rac5SkyboardChallenges
from ..locations import ALL_LOCATIONS, WEAPON_LEVEL_LOOKUP
from ..locations.observation import LocationObservation
from ..options import Goal
from . import address_maps
from .armour import ARMOUR_PICKUPS
from .locations.challenge_locations import ALL_CLANK_ADDRESS_MAP
from .locations.skill_point_locations import TIERED_SKILL_POINTS

CLANK_CHALLENGE_NAMES = frozenset(ALL_CLANK_ADDRESS_MAP.values())


class LocationChecks:
    """Poll completion sources at the core's existing safe gameplay boundaries."""

    def __init__(self, core):
        self.core = core

    def events(self, names):
        observation = LocationObservation(events=frozenset(names))
        for name in names:
            definition = ALL_LOCATIONS[name]
            if definition.completed.source != "events" or definition.completed(observation):
                self.core.send_location(name)

    def goal(self):
        """Report victory once every selected goal is complete."""
        core = self.core
        if core._goal_reported:
            return
        conditions = {
            Goal.option_defeat_otto: self.otto_defeated,
            Goal.option_all_skill_points: lambda: self.all_in_seed(TIERED_SKILL_POINTS, core.skill_points.completed),
            Goal.option_all_clank_challenges: lambda: self.all_in_seed(CLANK_CHALLENGE_NAMES, core.clank.completed),
        }
        goals = core.options.goals
        if goals and all(conditions[goal]() for goal in goals):
            core.on_goal()
            core._goal_reported = True

    def otto_defeated(self):
        """Latch Otto's defeat before loader/menu gates can hide the ending transition."""
        core = self.core
        name = Rac5CutsceneLocations.QUODRONA_GOAL
        if name in core.missions.completed:
            return True
        # Only inspect live save flags after this session loaded gameplay.
        # Unlike ordinary pickups, victory must be observed during loading
        # and ending menus, before Continue/New Game can reset the flag.
        if not core._initial_load_done or not core._ap_inventory_ready:
            return False
        if not core.missions.get(name):
            return False
        core.missions.completed.add(name)
        core.send_location(name)
        return True

    def all_in_seed(self, names, completed):
        """True once every one of `names` in this seed's location pool is completed."""
        allowed = self.core.native.allowed_locations
        if allowed is None:
            return False
        required = allowed.intersection(names)
        return bool(required) and required <= completed

    def world(self):
        core = self.core
        observation = LocationObservation.read_bytes(
            core.pine, core.planet.planet_id, core.skill_points_enabled, core.clank_enabled, core.skyboard_enabled
        )
        self.events(core.bolts.check(observation.bolt_bits))
        if core.skill_points_enabled:
            self.events(core.skill_points.check(observation.skill_bits))
            self.all_skill_points()
        for name in core.missions.check(core.planet.planet_id, observation.missions):
            self.mission(name)
        if core.clank_enabled:
            self.events(
                core.clank.check(all_challenges=core.clank_all_challenges, raw_by_address=observation.challenges)
            )
        if core.skyboard_enabled:
            self.events(core.skyboard.check(observation.skyboard))
            # The rematch mission bit is not reliably set by the race. Its
            # actual completion flag also satisfies the story location, even
            # if the separate race location was already checked before reconnect.
            rematch = Rac5CutsceneLocations.OUTPOST_OMEGA_REMATCH
            interior = ALL_LOCATIONS[Rac5SkyboardChallenges.OUTPOST_OMEGA_INTERIOR]
            if rematch not in core.missions.completed and interior.completed(observation):
                core.missions.completed.add(rematch)
                self.mission(rematch)
        if core.shrink_ray_locations_enabled:
            self.events(core.shrink_ray.check(core.planet.planet_id))

    def all_skill_points(self):
        """Fires once every easy/hard skill point in this seed's pool is done; the server's location
        set already reflects the Skill Points tier and any weapon-gated skill points."""
        core = self.core
        allowed = core.native.allowed_locations
        if allowed is None or Rac5Locations.HIG_TREEHOUSE_ALL_SKILL_POINTS not in allowed:
            return
        if self.all_in_seed(TIERED_SKILL_POINTS, core.skill_points.completed):
            core.send_location(Rac5Locations.HIG_TREEHOUSE_ALL_SKILL_POINTS)

    def mission(self, name):
        core = self.core
        definition = ALL_LOCATIONS[name]
        gadget = definition.grants_location
        if gadget and not (core.native.pickup is not None and gadget == Rac5Locations.RYLLUS_SPROUT):
            self.events((gadget,))
        if name == Rac5CutsceneLocations.QUODRONA_GOAL:
            core.missions.completed.add(name)
            core.send_location(name)
            self.goal()
            return
        if definition.reload_planet is not None:
            core.pine.write_int32(address_maps.NEW_PLANET_START_LOAD_ADDR, definition.reload_planet)
        cutscene = "cutscene" in definition.categories
        if (cutscene and core.all_cutscenes_enabled) or (not cutscene and core.all_missions_enabled):
            core.send_location(name)

    def armour(self):
        core = self.core
        if not core._ap_inventory_ready:
            return
        collected = core.armour.check()
        observation = LocationObservation(armour=collected)
        for pickup in ARMOUR_PICKUPS:
            if ALL_LOCATIONS[pickup.name].completed(observation):
                core.send_location(pickup.name)

    def weapon_levels(self, levels):

        observation = LocationObservation(weapon_levels=frozenset(levels))
        for key in levels:
            name = WEAPON_LEVEL_LOOKUP.get(key)
            if name and ALL_LOCATIONS[name].completed(observation):
                self.core.send_location(name)

    def nanotech(self):
        planet = self.core.planet
        # Challenges can change HP before switching the active player pointer.
        # Keep gameplay guards, but determine earned levels from saved XP.
        if (
            not planet.is_ready
            or self.core.pine.read_int8(address_maps.CURRENT_PLANET_ADDRESS) != planet.planet_id
            or not planet.player.is_ratchet
        ):
            return
        names = self.core.player_health_exp.check_level()
        observation = LocationObservation(nanotech_levels=frozenset(ALL_LOCATIONS[name].level for name in names))
        for name in names:
            if ALL_LOCATIONS[name].completed(observation):
                self.core.send_location(name)
