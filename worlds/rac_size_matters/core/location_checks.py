from ..constants import Rac5CutsceneLocations, Rac5Locations, Rac5SkyboardChallenges
from ..locations import ALL_LOCATIONS, WEAPON_LEVEL_LOOKUP
from ..locations.observation import LocationObservation
from . import address_maps
from .address_maps import NEW_PLANET_START_LOAD_ADDR
from .armour import ARMOUR_PICKUPS


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

    def world(self):
        core = self.core
        observation = LocationObservation.read_bytes(
            core.pine, core.planet.planet_id, core.skill_points_enabled, core.clank_enabled, core.skyboard_enabled
        )
        self.events(core.bolts.check(observation.bolt_bits))
        if core.skill_points_enabled:
            self.events(core.skill_points.check(observation.skill_bits))
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

    def mission(self, name):
        core = self.core
        definition = ALL_LOCATIONS[name]
        gadget = definition.grants_location
        if gadget and not (core.native.pickup is not None and gadget == Rac5Locations.RYLLUS_SPROUT):
            self.events((gadget,))
        if name == Rac5CutsceneLocations.QUODRONA_GOAL:
            core.on_goal()
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
        names = self.core.player_health_exp.check_level(self.core.planet.player.max_health)
        observation = LocationObservation(nanotech_levels=frozenset(ALL_LOCATIONS[name].level for name in names))
        for name in names:
            if ALL_LOCATIONS[name].completed(observation):
                self.core.send_location(name)
