from collections import defaultdict
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Entrance
from rule_builder.rules import Rule, Has, HasAll, HasAny, HasFromListUnique, True_, False_, And, Or, \
    CanReachRegion, CanReachLocation
from worlds.generic.Rules import add_rule as _ap_add_rule, CollectionRule
from .battle_tower_data import BATTLE_TOWER_NUM_TIERS, BATTLE_TOWER_UBERS_TIER
from .logic_rules import HasNPokemon, HasDexCount, HasSpeciesDex, HasRequestSlot, HasTradeRequest, GlitchedLogic, \
    CanUseHM, CanUseFieldMove, HasHMBadge, HasBadges, HasGyms, ResolvedRule
from .data import data, EvolutionType, EvolutionData, FishingRodType, EncounterKey, LogicalAccess, EncounterType, \
    FishTimeOfDay
from .evolution import evolution_location_name
from .fly import get_fly_regions
from .items import item_const_name_to_label
from .options import Goal, JohtoOnly, Route32Condition, UndergroundsRequirePower, Route2Access, \
    BlackthornDarkCaveAccess, NationalParkAccess, Route22AccessRequirement, Route3Access, BreedingMethodsRequired, \
    MtSilverRequirement, FreeFlyLocation, HMBadgeRequirements, VictoryRoadRequirement, EliteFourRequirement, \
    RedRequirement, \
    Route44AccessRequirement, RandomizeBadges, RadioTowerRequirement, PokemonCrystalOptions, Shopsanity, \
    RequireItemfinder, Route42Access, RedGyaradosAccess, PhoneCallMode, Route30Access, \
    SouthKantoCondition, RemoveBadgeRequirement, WildEncounterMethodsRequired, SaffronGatehouseTea, \
    VanillaEventChains, Route12Access
from .pokemon import add_hm_compatibility, get_chamber_event_for_unown
from .pokemon_data import ALL_UNOWN, SWARM_REGISTRATIONS
from .rematch_trainer_data import REMATCH_TRAINERS, SCALING_SUFFIX, rematch_location_name
from .utils import get_mart_slot_location_name

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

DARK_AREA_REGIONS: dict[str, list[str]] = {
    "Dark Cave": [
        "REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST",
        "REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTHEAST",
        "REGION_DARK_CAVE_VIOLET_ENTRANCE:SOUTHEAST",
        "REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTH",
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHEAST",
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHEAST",
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST",
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHWEST",
    ],
    "Union Cave": [
        "REGION_UNION_CAVE_1F",
        "REGION_UNION_CAVE_1F:SOUTH",
        "REGION_UNION_CAVE_B1F:NORTH",
        "REGION_UNION_CAVE_B1F:STRENGTH",
        "REGION_UNION_CAVE_B1F:CENTER",
        "REGION_UNION_CAVE_B1F:SOUTHWEST",
        "REGION_UNION_CAVE_B1F:SOUTHEAST",
        "REGION_UNION_CAVE_B2F:NORTH",
        "REGION_UNION_CAVE_B2F:SURF",
    ],
    "Slowpoke Well": [
        "REGION_SLOWPOKE_WELL_B1F:ENTRANCE",
        "REGION_SLOWPOKE_WELL_B1F",
        "REGION_SLOWPOKE_WELL_B1F:WEST",
        "REGION_SLOWPOKE_WELL_B1F:CENTER",
        "REGION_SLOWPOKE_WELL_B2F:CENTER",
        "REGION_SLOWPOKE_WELL_B2F:ISLANDS",
    ],
    "Ilex Forest": [
        "REGION_ILEX_FOREST:NORTH",
        "REGION_ILEX_FOREST:SOUTH",
    ],
    "Goldenrod Underground": [
        "REGION_GOLDENROD_UNDERGROUND",
        "REGION_GOLDENROD_UNDERGROUND:BASEMENT_LANDING",
    ],
    "Burned Tower": [
        "REGION_BURNED_TOWER_1F",
        "REGION_BURNED_TOWER_B1F",
    ],
    "Olivine Lighthouse": [
        "REGION_OLIVINE_LIGHTHOUSE_1F",
        "REGION_OLIVINE_LIGHTHOUSE_2F",
        "REGION_OLIVINE_LIGHTHOUSE_2F:POWER",
        "REGION_OLIVINE_LIGHTHOUSE_2F:HOLE",
        "REGION_OLIVINE_LIGHTHOUSE_3F",
        "REGION_OLIVINE_LIGHTHOUSE_3F:NORTH",
        "REGION_OLIVINE_LIGHTHOUSE_3F:HOLE",
        "REGION_OLIVINE_LIGHTHOUSE_4F",
        "REGION_OLIVINE_LIGHTHOUSE_4F:CENTER",
        "REGION_OLIVINE_LIGHTHOUSE_4F:NORTH_HOLE",
        "REGION_OLIVINE_LIGHTHOUSE_4F:HOLE",
        "REGION_OLIVINE_LIGHTHOUSE_5F",
        "REGION_OLIVINE_LIGHTHOUSE_5F:CENTER",
        "REGION_OLIVINE_LIGHTHOUSE_5F:HOLE",
        "REGION_OLIVINE_LIGHTHOUSE_6F",
    ],
    "Whirl Islands": [
        "REGION_WHIRL_ISLAND_NW:NORTH",
        "REGION_WHIRL_ISLAND_NW:SOUTH",
        "REGION_WHIRL_ISLAND_NE:WEST",
        "REGION_WHIRL_ISLAND_NE:CENTER",
        "REGION_WHIRL_ISLAND_NE:SOUTHEAST",
        "REGION_WHIRL_ISLAND_NE:NORTHEAST",
        "REGION_WHIRL_ISLAND_SW:NORTHWEST",
        "REGION_WHIRL_ISLAND_SW:NORTHEAST",
        "REGION_WHIRL_ISLAND_SW:SOUTHWEST",
        "REGION_WHIRL_ISLAND_SW:SOUTHEAST",
        "REGION_WHIRL_ISLAND_SE",
        "REGION_WHIRL_ISLAND_B1F:NORTH",
        "REGION_WHIRL_ISLAND_B1F:NORTHEAST",
        "REGION_WHIRL_ISLAND_B1F:SOUTHWEST",
        "REGION_WHIRL_ISLAND_B1F:SOUTHEAST",
        "REGION_WHIRL_ISLAND_B1F:LEDGE",
        "REGION_WHIRL_ISLAND_B2F:NORTH",
        "REGION_WHIRL_ISLAND_B2F:CENTER",
        "REGION_WHIRL_ISLAND_B2F:LUGIA_CHAMBER_ENTRANCE",
        "REGION_WHIRL_ISLAND_B2F:SOUTH",
        "REGION_WHIRL_ISLAND_CAVE",
        "REGION_WHIRL_ISLAND_LUGIA_CHAMBER",
        "REGION_WHIRL_ISLAND_LUGIA_CHAMBER:WATER",
    ],
    "Mount Mortar": [
        "REGION_MOUNT_MORTAR_1F_INSIDE",
        "REGION_MOUNT_MORTAR_1F_INSIDE:NORTH",
        "REGION_MOUNT_MORTAR_1F_INSIDE:SOUTH",
        "REGION_MOUNT_MORTAR_2F_INSIDE",
        "REGION_MOUNT_MORTAR_2F_INSIDE:SOUTH",
        "REGION_MOUNT_MORTAR_2F_INSIDE:SOUTHWEST",
        "REGION_MOUNT_MORTAR_2F_INSIDE:NORTH",
        "REGION_MOUNT_MORTAR_B1F",
        "REGION_MOUNT_MORTAR_B1F:SOUTH",
        "REGION_MOUNT_MORTAR_B1F:NORTHWEST",
    ],
    "Ice Path": [
        "REGION_ICE_PATH_1F:WEST",
        "REGION_ICE_PATH_1F:EAST",
        "REGION_ICE_PATH_B1F:NORTH",
        "REGION_ICE_PATH_B1F:SOUTH",
        "REGION_ICE_PATH_B2F_BLACKTHORN_SIDE",
        "REGION_ICE_PATH_B2F_MAHOGANY_SIDE",
        "REGION_ICE_PATH_B2F_MAHOGANY_SIDE:MIDDLE",
        "REGION_ICE_PATH_B3F",
    ],
    "Dragons Den": [
        "REGION_DRAGONS_DEN_1F:UPPER",
        "REGION_DRAGONS_DEN_1F:LOWER",
        "REGION_DRAGONS_DEN_B1F:NORTH",
        "REGION_DRAGONS_DEN_B1F:CENTER",
        "REGION_DRAGONS_DEN_B1F:WEST",
        "REGION_DRAGONS_DEN_B1F:SOUTH",
        "REGION_DRAGONS_DEN_B1F:SOUTHEAST",
    ],
    "Tohjo Falls": [
        "REGION_TOHJO_FALLS:WEST",
        "REGION_TOHJO_FALLS:EAST",
    ],
    "Victory Road": [
        "REGION_VICTORY_ROAD:1F:ENTRANCE",
        "REGION_VICTORY_ROAD:1F",
        "REGION_VICTORY_ROAD:2F",
        "REGION_VICTORY_ROAD:2F:NORTHEAST",
        "REGION_VICTORY_ROAD:2F:NORTHWEST",
        "REGION_VICTORY_ROAD:3F",
        "REGION_VICTORY_ROAD:3F:SOUTHEAST",
    ],
    "Silver Cave": [
        "REGION_SILVER_CAVE_ROOM_1",
    ],
    "Digletts Cave": [
        "REGION_DIGLETTS_CAVE",
        "REGION_DIGLETTS_CAVE:SOUTH_ENTRANCE",
        "REGION_DIGLETTS_CAVE:NORTH_ENTRANCE",
    ],
    "Mount Moon": [
        "REGION_MOUNT_MOON",
        "REGION_MOUNT_MOON:LEDGE",
        "REGION_MOUNT_MOON:NORTH_ENTRANCE",
        "REGION_MOUNT_MOON:SOUTH_ENTRANCE",
    ],
    "Rock Tunnel": [
        "REGION_ROCK_TUNNEL_1F:SOUTH",
        "REGION_ROCK_TUNNEL_1F:NORTHEAST",
        "REGION_ROCK_TUNNEL_1F:NORTHWEST",
        "REGION_ROCK_TUNNEL_B1F:WEST",
        "REGION_ROCK_TUNNEL_B1F:EAST",
    ],
    "Flooded Mine": [
        "REGION_FLOODED_MINE",
        "REGION_FLOODED_MINE:NORTH_ENTRANCE",
        "REGION_FLOODED_MINE:SOUTH_ENTRANCE",
    ],
}

KANTO_DARK_AREAS = {"Digletts Cave", "Mount Moon", "Rock Tunnel"}

CYCLING_ROAD_REGIONS: list[str] = [
    "REGION_ROUTE_16:CYCLING_ROAD",
    "REGION_ROUTE_17",
]

# (hm, johto_badge, kanto_badge, remove_key, regional_splits) for hm_badge_requirements.
# regional_splits=False keeps both badges in both regions under the "regional" option (Fly only).
_HM_BADGE_REQUIREMENTS = (
    ("CUT", "hive", "cascade", RemoveBadgeRequirement.CUT, True),
    ("FLY", "storm", "thunder", RemoveBadgeRequirement.FLY, False),
    ("SURF", "fog", "soul", RemoveBadgeRequirement.SURF, True),
    ("STRENGTH", "plain", "rainbow", RemoveBadgeRequirement.STRENGTH, True),
    ("FLASH", "zephyr", "boulder", RemoveBadgeRequirement.FLASH, True),
    ("WHIRLPOOL", "glacier", "volcano", RemoveBadgeRequirement.WHIRLPOOL, True),
    ("WATERFALL", "rising", "earth", RemoveBadgeRequirement.WATERFALL, True),
)


class PokemonCrystalLogic:
    all_pokemon: set[str]
    evolution: dict[str, list[tuple[EvolutionData, LogicalAccess]]]
    breeding: dict[str, list[tuple[str, LogicalAccess, bool]]]
    wild_regions: dict[EncounterKey, LogicalAccess]
    guaranteed_hm_access: bool

    pokemon_hm_use: dict[str, list[str]]
    compatible_hm_pokemon: dict[str, list[str]]

    badge_items: dict[str, str]
    hm_badge_requirements_johto: dict[str, tuple]
    hm_badge_requirements_kanto: dict[str, tuple]
    gym_events: dict[str, str]

    map_card_fly_unlocks: tuple
    expn_components: tuple

    fishing_rod_rules: dict[FishingRodType, Rule]

    player: int
    options: PokemonCrystalOptions

    def __init__(self, world: "PokemonCrystalWorld"):
        self.all_pokemon = set(world.generated_pokemon.keys())
        self.evolution = defaultdict(list)
        self.breeding = defaultdict(list)
        self.wild_regions = defaultdict(lambda: LogicalAccess.Inaccessible)
        self.compatible_hm_pokemon = defaultdict(list)
        self.guaranteed_hm_access = False

        self.hm_badge_requirements_johto = {}
        self.hm_badge_requirements_kanto = {}
        self.pokemon_hm_use = {}

        self.player = world.player
        self.options = world.options

        if self.options.randomize_badges == RandomizeBadges.option_vanilla:
            self.badge_items = {
                "zephyr": "EVENT_ZEPHYR_BADGE_FROM_FALKNER",
                "hive": "EVENT_HIVE_BADGE_FROM_BUGSY",
                "plain": "EVENT_PLAIN_BADGE_FROM_WHITNEY",
                "fog": "EVENT_FOG_BADGE_FROM_MORTY",
                "mineral": "EVENT_MINERAL_BADGE_FROM_JASMINE",
                "storm": "EVENT_STORM_BADGE_FROM_CHUCK",
                "glacier": "EVENT_GLACIER_BADGE_FROM_PRYCE",
                "rising": "EVENT_RISING_BADGE_FROM_CLAIR" if VanillaEventChains.CLAIR in world.options.vanilla_event_chains.value else "EVENT_RISING_BADGE_FROM_CLAIR_GYM",

                "boulder": "EVENT_BOULDER_BADGE_FROM_BROCK",
                "cascade": "EVENT_CASCADE_BADGE_FROM_MISTY",
                "thunder": "EVENT_THUNDER_BADGE_FROM_LTSURGE",
                "rainbow": "EVENT_RAINBOW_BADGE_FROM_ERIKA",
                "soul": "EVENT_SOUL_BADGE_FROM_JANINE",
                "marsh": "EVENT_MARSH_BADGE_FROM_SABRINA",
                "volcano": "EVENT_VOLCANO_BADGE_FROM_BLAINE",
                "earth": "EVENT_EARTH_BADGE_FROM_BLUE"
            }
        else:
            self.badge_items = {
                "zephyr": "Zephyr Badge",
                "hive": "Hive Badge",
                "plain": "Plain Badge",
                "fog": "Fog Badge",
                "mineral": "Mineral Badge",
                "storm": "Storm Badge",
                "glacier": "Glacier Badge",
                "rising": "Rising Badge",

                "boulder": "Boulder Badge",
                "cascade": "Cascade Badge",
                "thunder": "Thunder Badge",
                "rainbow": "Rainbow Badge",
                "soul": "Soul Badge",
                "marsh": "Marsh Badge",
                "volcano": "Volcano Badge",
                "earth": "Earth Badge"
            }

        self.gym_events = {
            "falkner": "EVENT_BEAT_FALKNER",
            "bugsy": "EVENT_BEAT_BUGSY",
            "whitney": "EVENT_BEAT_WHITNEY",
            "morty": "EVENT_BEAT_MORTY",
            "jasmine": "EVENT_BEAT_JASMINE",
            "chuck": "EVENT_BEAT_CHUCK",
            "pryce": "EVENT_BEAT_PRYCE",
            "clair": "EVENT_BEAT_CLAIR",

            "brock": "EVENT_BEAT_BROCK",
            "misty": "EVENT_BEAT_MISTY",
            "ltsurge": "EVENT_BEAT_LTSURGE",
            "erika": "EVENT_BEAT_ERIKA",
            "janine": "EVENT_BEAT_JANINE",
            "sabrina": "EVENT_BEAT_SABRINA",
            "blaine": "EVENT_BEAT_BLAINE",
            "blue": "EVENT_BEAT_BLUE"
        }

        if world.options.hm_badge_requirements != HMBadgeRequirements.option_no_badges:
            badge_mode = world.options.hm_badge_requirements
            for hm, johto_badge, kanto_badge, remove_key, regional_splits in _HM_BADGE_REQUIREMENTS:
                if remove_key in world.options.remove_badge_requirement:
                    continue
                if badge_mode == HMBadgeRequirements.option_vanilla:
                    johto = kanto = (johto_badge,)
                elif badge_mode == HMBadgeRequirements.option_add_kanto or not regional_splits:
                    johto = kanto = (johto_badge, kanto_badge)
                else:  # option_regional
                    johto, kanto = (johto_badge,), (kanto_badge,)
                self.hm_badge_requirements_johto[hm] = johto
                self.hm_badge_requirements_kanto[hm] = kanto

        if world.options.randomize_pokegear:
            self.map_card_fly_unlocks = ("Map Card", "Pokegear")
            self.expn_components = ("Pokegear", "Radio Card", "EXPN Card")
            if world.options.phone_call_mode == PhoneCallMode.option_simple:
                self.phone_call_components = ("Pokegear", "Phone Card")
            else:
                self.phone_call_components = ("Pokegear", "Phone Card", "EVENT_CHANGE_DST")
        else:
            self.map_card_fly_unlocks = ("EVENT_GOT_MAP_CARD", "EVENT_GOT_POKEGEAR")
            self.expn_components = ("EVENT_GOT_POKEGEAR", "EVENT_GOT_RADIO_CARD", "EVENT_GOT_EXPN_CARD")
            if world.options.phone_call_mode == PhoneCallMode.option_simple:
                self.phone_call_components = ("EVENT_GOT_POKEGEAR", "EVENT_GOT_PHONE_CARD")
            else:
                self.phone_call_components = ("EVENT_GOT_POKEGEAR", "EVENT_GOT_PHONE_CARD", "EVENT_CHANGE_DST")

        if world.options.randomize_pokedex:
            self.pokedex = "Pokedex"
        else:
            self.pokedex = "EVENT_GOT_POKEDEX"

        if world.options.progressive_rods:
            self.fishing_rod_rules = {
                FishingRodType.Old: Has("Progressive Rod"),
                FishingRodType.Good: Has("Progressive Rod", 2),
                FishingRodType.Super: Has("Progressive Rod", 3),
            }
        else:
            self.fishing_rod_rules = {
                FishingRodType.Old: Has("Old Rod"),
                FishingRodType.Good: Has("Good Rod"),
                FishingRodType.Super: Has("Super Rod"),
            }

    def can_phone_call(self) -> Rule:
        return HasAll(*self.phone_call_components)

    def can_fish(self) -> Rule:
        return Or(*self.fishing_rod_rules.values())

    def can_phone_call_power(self) -> Rule:
        return Has("EVENT_RESTORED_POWER_TO_KANTO") & self.can_phone_call()

    def ship_rule(self) -> Rule:
        rule: Rule = Has("S.S. Ticket")
        if self.options.ss_aqua_access:
            rule = rule & Has("EVENT_JASMINE_RETURNED_TO_GYM")
        return rule

    def magnet_train_rule(self) -> Rule:
        rule: Rule = Has("Pass")
        if self.options.magnet_train_access:
            rule = rule & Has("EVENT_RESTORED_POWER_TO_KANTO")
        return rule

    def _badges_or_gyms(self, badges: bool, count: int) -> Rule:
        return HasBadges(count) if badges else HasGyms(count)

    def has_rockets_requirement(self) -> Rule:
        return self._badges_or_gyms(
            self.options.radio_tower_requirement == RadioTowerRequirement.option_badges,
            self.options.radio_tower_count.value)

    def has_route_44_access(self) -> Rule:
        return self._badges_or_gyms(
            self.options.route_44_access_requirement == Route44AccessRequirement.option_badges,
            self.options.route_44_access_count.value)

    def has_victory_road_requirement(self) -> Rule:
        count = self.options.victory_road_count.value
        if self.options.victory_road_requirement == VictoryRoadRequirement.option_gyms:
            return self._badges_or_gyms(False, count)
        elif self.options.victory_road_requirement == VictoryRoadRequirement.option_badges:
            return self._badges_or_gyms(True, count)
        else:
            return HasBadges(count, johto_only=True)

    def has_elite_four_requirement(self) -> Rule:
        count = self.options.elite_four_count.value
        if self.options.elite_four_requirement == EliteFourRequirement.option_gyms:
            return self._badges_or_gyms(False, count)
        elif self.options.elite_four_requirement == EliteFourRequirement.option_badges:
            return self._badges_or_gyms(True, count)
        else:
            return HasBadges(count, johto_only=True)

    def has_red_requirement(self) -> Rule:
        return self._badges_or_gyms(
            self.options.red_requirement != RedRequirement.option_gyms,
            self.options.red_count.value)

    def has_mt_silver_requirement(self) -> Rule:
        return self._badges_or_gyms(
            self.options.mt_silver_requirement != MtSilverRequirement.option_gyms,
            self.options.mt_silver_count.value)

    def has_route_22_access_requirement(self) -> Rule:
        if self.options.route_22_access_requirement == Route22AccessRequirement.option_wake_snorlax:
            return Has("EVENT_FOUGHT_SNORLAX")
        elif self.options.route_22_access_requirement == Route22AccessRequirement.option_badges:
            return self._badges_or_gyms(True, self.options.route_22_access_count.value)
        elif self.options.route_22_access_requirement == Route22AccessRequirement.option_gyms:
            return self._badges_or_gyms(False, self.options.route_22_access_count.value)
        else:
            return Has("EVENT_BEAT_ELITE_FOUR")

    def has_route_32_condition(self) -> Rule:
        if self.options.route_32_condition == Route32Condition.option_egg_from_aide:
            return Has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE")
        elif self.options.route_32_condition == Route32Condition.option_any_badge:
            return self._badges_or_gyms(True, 1)
        elif self.options.route_32_condition == Route32Condition.option_any_gym:
            return self._badges_or_gyms(False, 1)
        elif self.options.route_32_condition == Route32Condition.option_zephyr_badge:
            return Has(self.badge_items["zephyr"])
        else:
            return True_()

    def set_hm_compatible_pokemon(self, world: "PokemonCrystalWorld"):
        hms = ("CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH")
        for hm in hms:
            for pokemon_id, pokemon_data in world.generated_pokemon.items():
                if hm in pokemon_data.tm_hm:
                    self.compatible_hm_pokemon[hm].append(pokemon_id)

        pokemon_hm_use = defaultdict(list)
        for hm, species_list in self.compatible_hm_pokemon.items():
            for species in species_list:
                pokemon_hm_use[species].append(f"Teach {hm}")
        self.pokemon_hm_use = pokemon_hm_use

    def add_hm_compatible_pokemon(self, hm: str, pokemon_id: str):
        self.compatible_hm_pokemon[hm].append(pokemon_id)
        self.pokemon_hm_use.setdefault(pokemon_id, []).append(f"Teach {hm}")


def set_rules(world: "PokemonCrystalWorld") -> None:
    def set_rule(spot, rule):
        world.set_rule(spot, rule)

    def add_rule(spot, rule, combine="and"):
        if isinstance(rule, Rule):
            old = spot.access_rule
            if isinstance(old, Rule.Resolved):
                # Recombine through And/Or so the merged rule is flattened and deduped.
                nested = And if combine == "and" else Or
                world.set_rule(spot, nested(ResolvedRule(old), rule))
                return
            rule = rule.resolve(world)
            world.register_rule_dependencies(rule)
            if isinstance(spot, Entrance):
                world._register_rule_indirects(rule, spot)
        _ap_add_rule(spot, rule, combine)

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    def get_location(location: str):
        if location in data.locations:
            location = data.locations[location].label

        return world.get_location(location)

    def safe_set_location_rule(spot: str, rule: CollectionRule | Rule) -> None:
        try:
            location = get_location(spot)
        except KeyError:
            return
        set_rule(location, rule)

    def set_static_rule(name: str, rule: CollectionRule | Rule):
        if world.options.level_scaling:
            set_rule(get_location(name), rule)
        if world.options.static_pokemon_required or world.is_universal_tracker:
            set_rule(get_location(f"Static_{name}_1"), rule)

    def hidden():
        return world.options.randomize_hidden_items.value

    def johto_only():
        return world.options.johto_only.value

    world.refresh_source_sets()

    if world.options.momsanity:
        mom_available_gyms = 16 if world.options.johto_only == JohtoOnly.option_off else 8
        for i in range(10):
            gyms = min(i, mom_available_gyms)
            set_rule(get_location(f"MOM_SAVINGS_{i + 1}"),
                     (Has("EVENT_GAVE_MYSTERY_EGG_TO_ELM") | Has("EVENT_TALKED_TO_MOM_AFTER_MYSTERY_EGG_QUEST"))
                     & HasGyms(gyms))

    can_surf_and_whirlpool = CanUseHM(CanUseHM.SURF) & CanUseHM(CanUseHM.WHIRLPOOL)
    can_surf_and_waterfall = CanUseHM(CanUseHM.SURF) & CanUseHM(CanUseHM.WATERFALL)

    lock_kanto_gyms = world.options.lock_kanto_gyms or world.options.kinda_early_surf
    kanto_gym_lock = HasAny("EVENT_SILVER_CAVE_ACCESS", "EVENT_FOUGHT_SNORLAX", "EVENT_FOUGHT_LUGIA",
                            "EVENT_FOUGHT_HO_OH", "EVENT_FOUGHT_SUICUNE", "EVENT_VICTORY_ROAD_ACCESS")
    if world.options.lock_kanto_gyms and world.options.kinda_early_surf:
        kanto_gyms_access = kanto_gym_lock & CanUseHM(CanUseHM.SURF, kanto=True)
    elif world.options.kinda_early_surf:
        kanto_gyms_access = CanUseHM(CanUseHM.SURF, kanto=True)
    else:
        kanto_gyms_access = kanto_gym_lock

    # Goal
    goal_events = []
    if Goal.ELITE_FOUR in world.options.goal:
        goal_events.append("EVENT_BEAT_ELITE_FOUR")
    if Goal.RED in world.options.goal:
        goal_events.append("EVENT_BEAT_RED")
    if Goal.DIPLOMA in world.options.goal:
        goal_events.append("EVENT_OBTAINED_DIPLOMA")
    if Goal.RIVAL in world.options.goal:
        goal_events.extend([
            "EVENT_BEAT_CHERRYGROVE_RIVAL",
            "EVENT_BEAT_AZALEA_RIVAL",
            "EVENT_RIVAL_BURNED_TOWER",
            "EVENT_BEAT_GOLDENROD_UNDERGROUND_RIVAL",
            "EVENT_BEAT_VICTORY_ROAD_RIVAL",
        ])
        if world.options.johto_only == JohtoOnly.option_off:
            goal_events.extend([
                "EVENT_BEAT_RIVAL_IN_MT_MOON",
                "EVENT_BEAT_RIVAL_IN_INDIGO_PLATEAU"
            ])
    if Goal.DEFEAT_TEAM_ROCKET in world.options.goal:
        goal_events.extend([
            "EVENT_CLEARED_SLOWPOKE_WELL",
            "EVENT_CLEARED_ROCKET_HIDEOUT",
            "EVENT_BEAT_ROCKET_EXECUTIVEM_3",
            "EVENT_CLEARED_RADIO_TOWER",
        ])
        if world.options.johto_only == JohtoOnly.option_off:
            goal_events.append("EVENT_DEFEATED_ROUTE_24_ROCKET")
    if Goal.UNOWN_HUNT in world.options.goal:
        goal_events.append("EVENT_GOT_ALL_UNOWN")
    if Goal.BATTLE_TOWER in world.options.goal:
        goal_events.append("EVENT_BEAT_ALL_BATTLE_TOWER_TIERS")
    world.set_completion_rule(HasAll(*goal_events))

    # Free Fly
    set_rule(get_entrance("Fly"), CanUseHM(CanUseHM.FLY))
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        from .regions import _get_fly_dest_region
        map_card_dest = _get_fly_dest_region(world, world.map_card_fly_location)
        add_rule(get_entrance(f"Free Fly {map_card_dest}"), HasAll(*world.logic.map_card_fly_unlocks))

    def fly_unlock_rule(fr, flypoint):
        items = [f"Fly {data.fly_regions[flypoint - 1].name}", f"Fly Unlock {flypoint}"]
        if not world.options.randomize_fly_unlocks:
            items.append(f"EVENT_VISITED_{fr.base_identifier}")
        return HasAny(*items)

    # Fly Unlocks
    if world.options.randomize_fly_destinations:
        for i, fly_region in enumerate(get_fly_regions(world), start=1):
            set_rule(get_entrance(f"Fly Destination {i}"), fly_unlock_rule(fly_region, i))
    else:
        for fly_region in get_fly_regions(world):
            set_rule(get_entrance(f"REGION_FLY -> {fly_region.exit_region}"), fly_unlock_rule(fly_region, fly_region.id))

    # New Bark Town
    set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_27:WEST"), CanUseHM(CanUseHM.SURF))
    set_rule(get_location("EVENT_GAVE_MYSTERY_EGG_TO_ELM"), Has("Mystery Egg"))
    set_rule(get_location("Elm's Lab - Everstone from Elm"), Has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE"))
    set_rule(get_location("Elm's Lab - Gift from Aide after returning Mystery Egg"), Has("Mystery Egg"))
    set_rule(get_location("Elm's Lab - Master Ball from Elm"), Has(world.logic.badge_items["rising"]))
    set_rule(get_location("Elm's Lab - S.S. Ticket from Elm"), Has("EVENT_BEAT_ELITE_FOUR"))

    # Route 29
    set_rule(get_location("Route 29 - Pink Bow from Tuscany"), Has(world.logic.badge_items["zephyr"]))

    # Route 30
    if world.options.route_30_access == Route30Access.option_mr_pokemon:
        route_30_rule = Has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON") | CanUseHM(CanUseHM.CUT)
    else:
        route_30_rule = Has("EVENT_GAVE_MYSTERY_EGG_TO_ELM") | CanUseHM(CanUseHM.CUT)

    if world.options.route_30_battle:
        set_rule(get_entrance("REGION_ROUTE_30:NORTHWEST -> REGION_ROUTE_30"), route_30_rule)

    set_rule(get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_30:NORTHWEST"), route_30_rule)
    if world.options.route_30_access == Route30Access.option_mr_pokemon:
        route_30_unblock = "EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON"
    else:
        route_30_unblock = "EVENT_GAVE_MYSTERY_EGG_TO_ELM"

    set_rule(get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_30:POST_MYSTERY_EGG"), Has(route_30_unblock))

    set_rule(get_location("Route 30 - Exp Share from Mr Pokemon"), Has("Red Scale"))

    if world.options.rematchsanity or world.options.randomize_phone_call_items:
        for trainer in REMATCH_TRAINERS.values():
            for gate in trainer.tier_gates:
                safe_set_location_rule(f"{trainer.trainer_const}_{SCALING_SUFFIX[gate]}", HasAll(gate))

    if world.options.rematchsanity:
        for trainer in REMATCH_TRAINERS.values():
            for i in range(trainer.num_rematches):
                tier_rule = HasAll(*trainer.tier_gates[:i + 1])
                if trainer.pokemon_request_slot is not None:
                    slot = trainer.pokemon_request_slot
                    rule = tier_rule & world.logic.can_phone_call() & HasRequestSlot(slot) & Has(world.logic.pokedex)
                else:
                    rule = tier_rule & world.logic.can_phone_call()
                safe_set_location_rule(rematch_location_name(trainer, i), rule)

    if world.options.randomize_phone_call_items:
        if world.options.rematchsanity:
            joey_gates = tuple(REMATCH_TRAINERS["JOEY"].tier_gates)
            set_rule(get_location("Route 30 - HP Up from Joey"), world.logic.can_phone_call() & HasAll(*joey_gates))
        else:
            set_rule(get_location("Route 30 - HP Up from Joey"),
                     world.logic.can_phone_call() & Has("EVENT_BEAT_ELITE_FOUR"))

    # Cherrygrove
    set_rule(get_location("Cherrygrove City - Mystic Water from Island Man"), CanUseHM(CanUseHM.SURF))

    safe_set_location_rule("Cherrygrove City - Rival", Has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON"))
    set_rule(get_location("EVENT_BEAT_CHERRYGROVE_RIVAL"), Has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON"))

    # Route 31
    set_rule(get_location("EVENT_GAVE_KENYA"), Has("EVENT_GOT_KENYA"))
    set_rule(get_location("Route 31 - TM50 for delivering Kenya"), Has("EVENT_GOT_KENYA"))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 31 - Berry from Wade"), world.logic.can_phone_call())

    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTHEAST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST"),
             CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTHEAST"),
             CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTHEAST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:SOUTHEAST"),
             CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:SOUTHEAST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTHEAST"),
             CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))

    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTH -> REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST"),
             CanUseHM(CanUseHM.SURF))

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        rule = can_surf_and_waterfall
    else:
        rule = CanUseHM(CanUseHM.SURF)
    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST -> REGION_DARK_CAVE_VIOLET_ENTRANCE:NORTH"), rule)

    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHEAST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHEAST"),
        CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHEAST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHEAST"),
        CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHEAST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST"),
        CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance(
        "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHEAST"),
        CanUseHM(CanUseHM.SURF))

    # Violet City
    if hidden():
        set_rule(get_location("Violet City - Hidden Item behind Cut Tree"), CanUseHM(CanUseHM.CUT))
    set_rule(get_location("Violet City - Northwest Item across Water"), CanUseHM(CanUseHM.SURF))
    set_rule(get_location("Violet City - Northeast Item across Water"), CanUseHM(CanUseHM.SURF))

    set_rule(get_location("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE"), Has(world.logic.gym_events["falkner"]))
    set_static_rule("EggTogepi", Has(world.logic.gym_events["falkner"]))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE -> REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OUTSIDE:SOUTH -> REGION_RUINS_OF_ALPH_OUTSIDE"),
             CanUseHM(CanUseHM.SURF))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_KABUTO_CHAMBER -> REGION_RUINS_OF_ALPH_KABUTO_ITEM_ROOM"),
             Has("EVENT_MART_ESCAPE_ROPE"))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_OMANYTE_CHAMBER -> REGION_RUINS_OF_ALPH_OMANYTE_ITEM_ROOM"),
             Has("Water Stone"))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_AERODACTYL_CHAMBER -> REGION_RUINS_OF_ALPH_AERODACTYL_ITEM_ROOM"),
             CanUseHM(CanUseHM.FLASH, allow_ool=False))

    set_rule(get_entrance("REGION_RUINS_OF_ALPH_HO_OH_CHAMBER -> REGION_RUINS_OF_ALPH_HO_OH_ITEM_ROOM"),
             Has("Rainbow Wing"))

    if Goal.UNOWN_HUNT in world.options.goal:
        set_rule(get_location("EVENT_GOT_ALL_UNOWN"), HasAll(*ALL_UNOWN))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_A_TO_K"), Has("Kabuto Tile", 16))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_L_TO_R"), Has("Omanyte Tile", 16))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_S_TO_W"), Has("Aerodactyl Tile", 16))
        set_rule(get_location("ENGINE_UNLOCKED_UNOWNS_X_TO_Z"), Has("Ho-Oh Tile", 16))

        set_rule(get_entrance("REGION_RUINS_OF_ALPH_KABUTO_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 Has("Kabuto Tile", 16))
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_AERODACTYL_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 Has("Aerodactyl Tile", 16))
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_OMANYTE_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 Has("Omanyte Tile", 16))
        set_rule(get_entrance("REGION_RUINS_OF_ALPH_HO_OH_CHAMBER -> REGION_RUINS_OF_ALPH_INNER_CHAMBER"),
                 Has("Ho-Oh Tile", 16))

    # Route 32
    route_32_access_rule = world.logic.has_route_32_condition()
    set_rule(get_entrance("REGION_ROUTE_32:NORTH -> REGION_ROUTE_32:SOUTH"), route_32_access_rule)
    set_rule(get_entrance("REGION_ROUTE_32:SOUTH -> REGION_ROUTE_32:NORTH"), route_32_access_rule)

    set_rule(get_location("Route 32 - Miracle Seed from Man in North"), Has(world.logic.badge_items["zephyr"]))
    set_rule(get_location("Route 32 - TM05 from Roar Guy"), CanUseHM(CanUseHM.CUT))

    # Union Cave
    # 1F internal
    set_rule(get_entrance("REGION_UNION_CAVE_1F -> REGION_UNION_CAVE_1F:SOUTH"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_UNION_CAVE_1F:SOUTH -> REGION_UNION_CAVE_1F"), CanUseHM(CanUseHM.SURF))
    # B1F internal
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:NORTH -> REGION_UNION_CAVE_B1F:STRENGTH"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:STRENGTH -> REGION_UNION_CAVE_B1F:NORTH"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:NORTH -> REGION_UNION_CAVE_B1F:CENTER"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:CENTER -> REGION_UNION_CAVE_B1F:NORTH"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:SOUTHWEST -> REGION_UNION_CAVE_B1F:SOUTHEAST"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_UNION_CAVE_B1F:SOUTHEAST -> REGION_UNION_CAVE_B1F:SOUTHWEST"),
             CanUseHM(CanUseHM.SURF))
    # B2F internal
    set_rule(get_entrance("REGION_UNION_CAVE_B2F:NORTH -> REGION_UNION_CAVE_B2F:SURF"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_UNION_CAVE_B2F:SURF -> REGION_UNION_CAVE_B2F:NORTH"), CanUseHM(CanUseHM.SURF))

    if world.options.route_23_restored:
        set_rule(get_entrance("REGION_ROUTE_23_RESTORED:SOUTH -> REGION_ROUTE_23_RESTORED:SURF"),
                 CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_ROUTE_23_RESTORED:NORTH -> REGION_ROUTE_23_RESTORED:SURF"),
                 CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_ROUTE_23_RESTORED:SURF -> REGION_ROUTE_23_RESTORED:SOUTH"),
                 CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_ROUTE_23_RESTORED:SURF -> REGION_ROUTE_23_RESTORED:NORTH"),
                 CanUseHM(CanUseHM.SURF))

    if world.options.flooded_mine:
        set_rule(get_entrance("REGION_CHERRYGROVE_CITY -> REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE"),
                 CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE -> REGION_CHERRYGROVE_CITY"),
                 CanUseHM(CanUseHM.SURF))


    # Route 33
    # Azalea Town
    set_rule(get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_TOWN:WELL"), Has("EVENT_MET_KURT"))
    set_rule(get_entrance("REGION_AZALEA_TOWN:WELL -> REGION_AZALEA_TOWN"), Has("EVENT_MET_KURT"))

    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F:ENTRANCE -> REGION_SLOWPOKE_WELL_B1F"), Has("EVENT_MET_KURT"))
    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F -> REGION_SLOWPOKE_WELL_B1F:ENTRANCE"), Has("EVENT_MET_KURT"))

    slowpoke_well_west_rule = CanUseHM(CanUseHM.STRENGTH) & Has("EVENT_CLEARED_SLOWPOKE_WELL")
    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F -> REGION_SLOWPOKE_WELL_B1F:WEST"), slowpoke_well_west_rule)
    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F:WEST -> REGION_SLOWPOKE_WELL_B1F"), slowpoke_well_west_rule)

    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F:WEST -> REGION_SLOWPOKE_WELL_B1F:CENTER"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B1F:CENTER -> REGION_SLOWPOKE_WELL_B1F:WEST"), CanUseHM(CanUseHM.SURF))

    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B2F:CENTER -> REGION_SLOWPOKE_WELL_B2F:ISLANDS"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_SLOWPOKE_WELL_B2F:ISLANDS -> REGION_SLOWPOKE_WELL_B2F:CENTER"),
             CanUseHM(CanUseHM.SURF))

    set_rule(get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))

    safe_set_location_rule("Azalea Town - Rival", Has("EVENT_CLEARED_SLOWPOKE_WELL"))
    set_rule(get_location("EVENT_BEAT_AZALEA_RIVAL"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))

    set_rule(get_location("Azalea Town - Lure Ball from Kurt"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))

    if Shopsanity.APRICORNS in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_KURTS_HOUSE -> REGION_MART_KURTS_BALLS"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))

        for color in ("Red", "Grn", "Blu", "Ylw", "Blk", "Wht", "Pnk"):
            required = f"{color} Apricorn" if world.options.randomize_berry_trees else f"EVENT_{color.upper()}_APRICORN"
            set_rule(get_location(f"Azalea Town - Kurt's Ball Shop - {color} Apricorn"), Has(required))

    set_rule(get_location("Charcoal Kiln - Charcoal"), Has("EVENT_HERDED_FARFETCHD"))

    if world.options.level_scaling:
        set_rule(get_location("RIVAL_BAYLEEF_AZALEA"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))
        set_rule(get_location("RIVAL_CROCONAW_AZALEA"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))
        set_rule(get_location("RIVAL_QUILAVA_AZALEA"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))

    # Ilex Forest

    if not world.options.remove_ilex_cut_tree:
        set_rule(get_entrance("REGION_ILEX_FOREST:NORTH -> REGION_ILEX_FOREST:SOUTH"), CanUseHM(CanUseHM.CUT))
        set_rule(get_entrance("REGION_ILEX_FOREST:SOUTH -> REGION_ILEX_FOREST:NORTH"), CanUseHM(CanUseHM.CUT))

    celebi_rule = Has("GS Ball") & Has("EVENT_CLEARED_SLOWPOKE_WELL") & Has("EVENT_BEAT_AZALEA_RIVAL")
    if world.options.require_flash and "Ilex Forest" in world.options.dark_areas:
        # Kurt refuses the GS Ball without Flash, even when Flash is only logically required
        celebi_rule = celebi_rule & CanUseHM(CanUseHM.FLASH, allow_ool=False)
    set_static_rule("Celebi", celebi_rule)

    set_rule(get_location("EVENT_HERDED_FARFETCHD"), Has("EVENT_CLEARED_SLOWPOKE_WELL"))

    set_rule(get_location("Ilex Forest - HM01 from Farfetch'd Guy"), Has("EVENT_HERDED_FARFETCHD"))

    # Route 34
    set_rule(get_entrance("REGION_ROUTE_34 -> REGION_ROUTE_34:WATER"), CanUseHM(CanUseHM.SURF))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 34 - Leaf Stone from Gina"), world.logic.can_phone_call())

    # Goldenrod City
    set_rule(get_location("Goldenrod City - Squirtbottle from Flower Shop"), Has(world.logic.badge_items["plain"]))
    set_rule(get_location("Goldenrod City - Post-E4 GS Ball from Trade Corner Receptionist"),
             Has("EVENT_BEAT_ELITE_FOUR"))
    set_static_rule("Eevee", Has("EVENT_MET_BILL"))

    if Shopsanity.JOHTO_MARTS in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_ROOF -> REGION_MART_ROOFTOP_SALE"),
                 Has("EVENT_BEAT_ELITE_FOUR"))

    if not johto_only():
        set_rule(get_entrance("REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
                 world.logic.magnet_train_rule())

    set_rule(get_location("Goldenrod City - Exchange Eon Mail in Pokecenter"), Has("EVENT_GOT_EON_MAIL_FROM_EUSINE"))

    # Underground
    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND -> REGION_GOLDENROD_UNDERGROUND:BASEMENT_LANDING"),
             Has("Basement Key"))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F -> REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE"),
             Has("Card Key"))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE -> REGION_GOLDENROD_DEPT_STORE_B1F"),
             Has("Card Key"))

    has_rockets_requirement = world.logic.has_rockets_requirement()

    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND_WAREHOUSE -> REGION_GOLDENROD_UNDERGROUND_WAREHOUSE:TAKEOVER"),
             has_rockets_requirement)

    set_rule(get_entrance(
        "REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES -> REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES:TAKEOVER"),
        has_rockets_requirement)

    if Shopsanity.GAME_CORNERS in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_GOLDENROD_GAME_CORNER -> REGION_MART_GOLDENROD_GAME_CORNER"), Has("Coin Case"))

    set_static_rule("GoldenrodGameCorner1", Has("Coin Case"))
    set_static_rule("GoldenrodGameCorner2", Has("Coin Case"))
    set_static_rule("GoldenrodGameCorner3", Has("Coin Case"))

    # Radio Tower
    set_rule(get_entrance("REGION_RADIO_TOWER_1F -> REGION_RADIO_TOWER_1F:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_2F:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_3F"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_3F -> REGION_RADIO_TOWER_3F:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_3F -> REGION_RADIO_TOWER_3F:EAST"), Has("Card Key"))
    set_rule(get_entrance("REGION_RADIO_TOWER_3F:EAST -> REGION_RADIO_TOWER_3F"),
             Has("EVENT_USED_THE_CARD_KEY_IN_THE_RADIO_TOWER"))
    set_rule(get_entrance("REGION_RADIO_TOWER_3F:EAST -> REGION_RADIO_TOWER_3F:EAST:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_4F:WEST -> REGION_RADIO_TOWER_4F:WEST:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_4F:EAST -> REGION_RADIO_TOWER_4F:EAST:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_5F:WEST -> REGION_RADIO_TOWER_5F:WEST:TAKEOVER"), has_rockets_requirement)
    set_rule(get_entrance("REGION_RADIO_TOWER_5F:EAST -> REGION_RADIO_TOWER_5F:EAST:TAKEOVER"), has_rockets_requirement)

    set_rule(get_location("Radio Tower 3F - TM11 from Woman"), Has("EVENT_CLEARED_RADIO_TOWER"))
    set_rule(get_location("Radio Tower 4F - Pink Bow from Mary"), Has("EVENT_CLEARED_RADIO_TOWER"))

    set_rule(get_location("EVENT_USED_THE_CARD_KEY_IN_THE_RADIO_TOWER"), Has("Card Key"))

    if Shopsanity.BLUE_CARD in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_MART_BLUE_CARD"), Has("Blue Card"))

        blue_card_points = (2, 2, 3, 3, 5, 5, 5, 5, 5)

        for i, points in enumerate(blue_card_points):
            slot_name = get_mart_slot_location_name("MART_BLUE_CARD", i)
            set_rule(get_location(f"Radio Tower 2F - Blue Card Shop - {slot_name}"), Has("Blue Card Point", points))

    # Route 35
    set_rule(get_location("Route 35 - HP Up after delivering Kenya"), Has("EVENT_GAVE_KENYA"))
    set_rule(get_entrance("REGION_ROUTE_35 -> REGION_ROUTE_35:FRUITTREE"), CanUseHM(CanUseHM.SURF))

    # National Park
    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        set_rule(get_entrance("REGION_ROUTE_35_NATIONAL_PARK_GATE -> REGION_ROUTE_35_NATIONAL_PARK_GATE:BIKE"),
                 Has("Bicycle"))
        set_rule(get_entrance("REGION_ROUTE_36_NATIONAL_PARK_GATE -> REGION_NATIONAL_PARK"), Has("Bicycle"))
        set_rule(get_entrance("REGION_ROUTE_36_NATIONAL_PARK_GATE -> REGION_NATIONAL_PARK:CONTEST"), Has("Bicycle"))

    if world.options.randomize_phone_call_items and world.options.randomize_pokemon_requests:
        set_rule(get_location("National Park - Nugget from Beverly"),
                 world.logic.can_phone_call() & HasRequestSlot(5) & Has(world.logic.pokedex))

    if WildEncounterMethodsRequired.BUG_CATCHING_CONTEST not in world.options.wild_encounter_methods_required and world.is_universal_tracker:
        for i in range(len(world.generated_contest)):
            set_rule(get_location(f"Bug Catching Contest Slot {i + 1}"), GlitchedLogic())

    # Sudowoodo
    has_squirtbottle = Has("Squirtbottle")
    set_rule(get_entrance("REGION_ROUTE_36:EAST -> REGION_ROUTE_37"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_36:EAST -> REGION_ROUTE_36:WEST"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_36:EAST"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_37"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_37 -> REGION_ROUTE_36:EAST"), has_squirtbottle)
    set_rule(get_entrance("REGION_ROUTE_37 -> REGION_ROUTE_36:WEST"), has_squirtbottle)

    set_static_rule("Sudowoodo", has_squirtbottle)

    # Route 36
    set_rule(get_entrance("REGION_ROUTE_35 -> REGION_ROUTE_36:WEST"), CanUseHM(CanUseHM.CUT))
    set_rule(get_entrance("REGION_ROUTE_36:WEST -> REGION_ROUTE_35"), CanUseHM(CanUseHM.CUT))

    set_rule(get_location("EVENT_SAW_SUICUNE_ON_ROUTE_36"), Has("EVENT_RELEASED_THE_BEASTS"))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 36 - Fire Stone from Alan"), world.logic.can_phone_call())

    set_rule(get_location("Route 36 - TM08 from Rock Smash Guy"), has_squirtbottle)

    # Ecruteak City
    set_rule(get_entrance("REGION_ECRUTEAK_GYM -> REGION_ECRUTEAK_GYM:INTERIOR"), Has("EVENT_BURNED_TOWER_MORTY"))
    set_rule(get_entrance("REGION_ECRUTEAK_GYM -> REGION_ECRUTEAK_CITY"), Has("EVENT_BURNED_TOWER_MORTY"))

    set_rule(get_location("Burned Tower 1F - Item"), CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
    set_rule(get_location("Burned Tower B1F - Item"), CanUseHM(CanUseHM.STRENGTH))

    set_rule(get_entrance("REGION_ECRUTEAK_TIN_TOWER_ENTRANCE -> REGION_ECRUTEAK_TIN_TOWER_ENTRANCE:BEHIND_SAGE"),
             Has("Clear Bell"))

    set_rule(get_location("Tin Tower 1F - Rainbow Wing"), Has("EVENT_BEAT_ELITE_FOUR"))

    set_rule(get_location("EVENT_GOT_EON_MAIL_FROM_EUSINE"), HasAll(
        "EVENT_SAW_SUICUNE_ON_ROUTE_36", "EVENT_SAW_SUICUNE_ON_ROUTE_42", "EVENT_SAW_SUICUNE_AT_CIANWOOD_CITY"))

    set_rule(get_entrance("REGION_TIN_TOWER_1F -> REGION_TIN_TOWER_2F"), Has("Rainbow Wing"))

    # Clear Bell gate on Tin Tower 1F itself (sage blocks entry in ER)
    tin_tower_1f = world.get_region("REGION_TIN_TOWER_1F")
    for exit_ in tin_tower_1f.exits:
        add_rule(exit_, Has("Clear Bell"))
    for location in tin_tower_1f.locations:
        add_rule(location, Has("Clear Bell"))

    set_rule(get_location("EVENT_FOUGHT_HO_OH"), Has("Rainbow Wing"))
    set_static_rule("Ho_Oh", Has("Rainbow Wing"))

    # Route 38
    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 38 - Thunderstone from Dana"), world.logic.can_phone_call())

    # Route 39
    if world.options.randomize_phone_call_items and world.options.randomize_pokemon_requests:
        set_rule(get_location("Route 39 - Nugget from Derek"),
                 world.logic.can_phone_call() & HasRequestSlot(6) & Has(world.logic.pokedex))

    # Route 39 Moomoo Farm - items require healing Miltank in the barn first
    healed_moomoo_rule = Has("EVENT_HEALED_MOOMOO")
    set_rule(get_location("Moomoo Farm - Moomoo Milk after feeding Moomoo"), healed_moomoo_rule)
    set_rule(get_location("Moomoo Farm - TM13 after feeding Moomoo"), healed_moomoo_rule)

    # Olivine City
    set_rule(get_location("EVENT_JASMINE_RETURNED_TO_GYM"), Has("Secretpotion"))

    if VanillaEventChains.JASMINE in world.options.vanilla_event_chains.value:
        add_rule(get_location("SECRETPOTION_FROM_PHARMACY"), Has("EVENT_JASMINE_EXPLAINED_AMPHYS_SICKNESS"))

    if not world.options.johto_only and world.options.randomize_phone_call_items:
        set_rule(get_entrance("REGION_OLIVINE_LIGHTHOUSE_2F -> REGION_OLIVINE_LIGHTHOUSE_2F:POWER"),
                 world.logic.can_phone_call_power())
        if world.options.rematchsanity:
            set_rule(get_location("Olivine Lighthouse 2F - Protein from Huey"),
                     world.logic.can_phone_call()
                     & HasAll("EVENT_CLEARED_RADIO_TOWER", "EVENT_BEAT_ELITE_FOUR", "EVENT_RESTORED_POWER_TO_KANTO"))

    if not johto_only():
        set_rule(get_entrance("REGION_OLIVINE_PORT -> REGION_OLIVINE_PORT:TICKET"), world.logic.ship_rule())
        set_rule(get_entrance("REGION_FAST_SHIP_1F -> REGION_OLIVINE_PORT:TICKET"), Has("EVENT_FAST_SHIP_LAZY_SAILOR"))

        for trainer in ("PSYCHIC_RODNEY", "SUPER_NERD_SHAWN", "BEAUTY_CASSIE", "COOLTRAINERM_SEAN",
                        "COOLTRAINERF_CAROL", "GENTLEMAN_EDWARD", "SAILOR_GARRETT", "FISHER_JONAH", "BLACKBELT_WAI",
                        "POKEFANM_JEREMY", "POKEFANF_GEORGIA", "BUG_CATCHER_KEN", "GUITARIST_CLYDE",
                        "POKEMANIAC_ETHAN", "BURGLAR_COREY", "SAILOR_KENNETH", "TEACHER_SHIRLEY", "SCHOOLBOY_NATE",
                        "SCHOOLBOY_RICKY"):
            safe_set_location_rule(f"ITEM_FROM_{trainer}", Has("EVENT_FAST_SHIP_LAZY_SAILOR"))
            if world.options.level_scaling:
                safe_set_location_rule(trainer, Has("EVENT_FAST_SHIP_LAZY_SAILOR"))

        if hidden():
            set_rule(get_location("Olivine Port - Hidden Item in Buoy"), CanUseHM(CanUseHM.SURF))

    set_rule(get_entrance("REGION_OLIVINE_GYM -> REGION_OLIVINE_GYM:JASMINE"), Has("EVENT_JASMINE_RETURNED_TO_GYM"))

    # Route 40
    set_rule(get_entrance("REGION_ROUTE_40 -> REGION_ROUTE_40:WATER"), CanUseHM(CanUseHM.SURF))

    if hidden():
        set_rule(get_location("Route 40 - Hidden Item in Rock"), CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))

    # Route 41
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_ROUTE_41:NW_ISLAND"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41:NW_ISLAND -> REGION_ROUTE_41"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_ROUTE_41:NE_ISLAND"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41:NE_ISLAND -> REGION_ROUTE_41"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_ROUTE_41:SW_ISLAND"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41:SW_ISLAND -> REGION_ROUTE_41"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_ROUTE_41:SE_ISLAND"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41:SE_ISLAND -> REGION_ROUTE_41"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_41:SW_ISLAND -> REGION_ROUTE_41:SW_ISLAND:ITEM"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_ROUTE_41:SW_ISLAND:ITEM -> REGION_ROUTE_41:SW_ISLAND"), CanUseHM(CanUseHM.SURF))

    # Whirl Islands internal
    # B1F one-way + strength
    set_rule(get_entrance("REGION_WHIRL_ISLAND_B1F:SOUTHEAST -> REGION_WHIRL_ISLAND_B1F:SOUTHWEST"),
             CanUseHM(CanUseHM.STRENGTH))
    # SW surf connections
    set_rule(get_entrance("REGION_WHIRL_ISLAND_SW:NORTHWEST -> REGION_WHIRL_ISLAND_SW:NORTHEAST"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_WHIRL_ISLAND_SW:NORTHEAST -> REGION_WHIRL_ISLAND_SW:NORTHWEST"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_WHIRL_ISLAND_SW:SOUTHWEST -> REGION_WHIRL_ISLAND_SW:SOUTHEAST"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_WHIRL_ISLAND_SW:SOUTHEAST -> REGION_WHIRL_ISLAND_SW:SOUTHWEST"),
             CanUseHM(CanUseHM.SURF))
    # B2F connections
    set_rule(get_entrance("REGION_WHIRL_ISLAND_B2F:NORTH -> REGION_WHIRL_ISLAND_B2F:SOUTH"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_WHIRL_ISLAND_B2F:SOUTH -> REGION_WHIRL_ISLAND_B2F:NORTH"), can_surf_and_waterfall)
    set_rule(get_entrance("REGION_WHIRL_ISLAND_B2F:SOUTH -> REGION_WHIRL_ISLAND_B2F:LUGIA_CHAMBER_ENTRANCE"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_WHIRL_ISLAND_B2F:LUGIA_CHAMBER_ENTRANCE -> REGION_WHIRL_ISLAND_B2F:SOUTH"),
             CanUseHM(CanUseHM.SURF))
    # Lugia sits across open water; surf the chamber to reach it
    set_rule(get_entrance("REGION_WHIRL_ISLAND_LUGIA_CHAMBER -> REGION_WHIRL_ISLAND_LUGIA_CHAMBER:WATER"),
             CanUseHM(CanUseHM.SURF))

    set_rule(get_location("EVENT_FOUGHT_LUGIA"), Has("Silver Wing"))
    set_static_rule("Lugia", Has("Silver Wing"))

    # Cianwood
    set_rule(get_entrance("REGION_CIANWOOD_CITY -> REGION_ROUTE_41"), CanUseHM(CanUseHM.SURF))
    if hidden():
        set_rule(get_location("Cianwood City - Hidden Item in West Rock"), CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
        set_rule(get_location("Cianwood City - Hidden Item in North Rock"), CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))

    set_rule(get_location("Cianwood City - HM02 from Chuck's Wife"), Has(world.logic.gym_events["chuck"]))

    set_rule(get_entrance("REGION_CIANWOOD_GYM -> REGION_CIANWOOD_GYM:STRENGTH"), CanUseHM(CanUseHM.STRENGTH))

    safe_set_location_rule("Cianwood City - Mysticalman Eusine", Has("EVENT_RELEASED_THE_BEASTS"))

    if world.options.level_scaling:
        set_rule(get_location("MYSTICALMAN_EUSINE"), Has("EVENT_RELEASED_THE_BEASTS"))

    set_rule(get_location("EVENT_SAW_SUICUNE_AT_CIANWOOD_CITY"), Has("EVENT_RELEASED_THE_BEASTS"))

    # Route 42
    if world.options.route_42_access.value == Route42Access.option_vanilla:
        set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER"), CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST"), CanUseHM(CanUseHM.SURF))

        set_rule(get_entrance("REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER"), CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST"), CanUseHM(CanUseHM.SURF))
    elif world.options.route_42_access.requires_whirlpool:
        set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER"), can_surf_and_whirlpool)
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST"), can_surf_and_whirlpool)

        set_rule(get_entrance("REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER"), can_surf_and_whirlpool)
        set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST"), can_surf_and_whirlpool)
    # else: blocked -> connection doesn't even exist

    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:CENTERFRUIT"), CanUseHM(CanUseHM.CUT))

    # set_rule auto-registers the indirect connection for CanReachRegion rules.
    set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:HEADBUTT"),
             CanReachRegion("REGION_ROUTE_42:CENTERFRUIT"))

    set_rule(get_entrance("REGION_ROUTE_42:CENTERFRUIT -> REGION_ROUTE_42:HEADBUTT"),
             CanReachRegion("REGION_ROUTE_42:WEST"))

    set_rule(get_location("EVENT_SAW_SUICUNE_ON_ROUTE_42"), Has("EVENT_RELEASED_THE_BEASTS"))

    if hidden():
        set_rule(get_location("Route 42 - Hidden Item in Pond Rock"), CanUseHM(CanUseHM.SURF))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 42 - Water Stone from Tully"), world.logic.can_phone_call())

    # Mt Mortar
    # 1F Outside
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTH -> REGION_MOUNT_MORTAR_1F_OUTSIDE:NORTH"),
             can_surf_and_waterfall)
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:NORTH -> REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTH"),
             CanUseHM(CanUseHM.SURF))

    # 1F Outside WATERFALL_ISLAND (conditional on route_42_access)
    if world.options.route_42_access.opens_mortar_connection:
        set_rule(
            get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTH -> REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND"),
            CanUseHM(CanUseHM.SURF))
        set_rule(
            get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND -> REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTH"),
            CanUseHM(CanUseHM.SURF))

    # 1F Outside rock smash (conditional)
    if world.options.mount_mortar_access:
        set_rule(get_entrance(
            "REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHWEST:ENTRANCE -> REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHWEST"),
            CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
        set_rule(get_entrance(
            "REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHWEST -> REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHWEST:ENTRANCE"),
            CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
        set_rule(get_entrance(
            "REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHEAST:ENTRANCE -> REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHEAST"),
            CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))
        set_rule(get_entrance(
            "REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHEAST -> REGION_MOUNT_MORTAR_1F_OUTSIDE:SOUTHEAST:ENTRANCE"),
            CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))

    # 1F Inside
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_INSIDE:SOUTH -> REGION_MOUNT_MORTAR_1F_INSIDE"),
             CanUseHM(CanUseHM.STRENGTH))

    # 2F Inside (all surf)
    set_rule(get_entrance("REGION_MOUNT_MORTAR_2F_INSIDE:SOUTH -> REGION_MOUNT_MORTAR_2F_INSIDE:SOUTHWEST"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_2F_INSIDE:SOUTHWEST -> REGION_MOUNT_MORTAR_2F_INSIDE:SOUTH"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_2F_INSIDE:SOUTH -> REGION_MOUNT_MORTAR_2F_INSIDE"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_2F_INSIDE -> REGION_MOUNT_MORTAR_2F_INSIDE:SOUTH"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_2F_INSIDE -> REGION_MOUNT_MORTAR_2F_INSIDE:NORTH"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_2F_INSIDE:NORTH -> REGION_MOUNT_MORTAR_2F_INSIDE"),
             CanUseHM(CanUseHM.SURF))

    # B1F
    set_rule(get_entrance("REGION_MOUNT_MORTAR_B1F:SOUTH -> REGION_MOUNT_MORTAR_B1F"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_B1F -> REGION_MOUNT_MORTAR_B1F:SOUTH"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_MOUNT_MORTAR_B1F:NORTHWEST -> REGION_MOUNT_MORTAR_B1F"),
             CanUseHM(CanUseHM.STRENGTH) & CanUseHM(CanUseHM.SURF))

    # Mahogany Town
    if Shopsanity.JOHTO_MARTS in world.options.shopsanity.value:
        set_rule(get_entrance("REGION_MAHOGANY_MART_1F -> REGION_MART_MAHOGANY_2"), Has("EVENT_CLEARED_RADIO_TOWER"))

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_GYM"), Has("EVENT_CLEARED_ROCKET_HIDEOUT"))

    set_rule(get_entrance("REGION_MAHOGANY_MART_1F -> REGION_TEAM_ROCKET_BASE_B1F"), Has("EVENT_DECIDED_TO_HELP_LANCE"))

    set_rule(get_entrance("REGION_TEAM_ROCKET_BASE_B3F:WEST -> REGION_TEAM_ROCKET_BASE_B3F:CENTER"),
             Has("EVENT_BEAT_ROCKET_GRUNTF_5") & Has("EVENT_BEAT_ROCKET_GRUNTM_28"))

    set_rule(get_entrance("REGION_TEAM_ROCKET_BASE_B2F:SOUTH -> REGION_TEAM_ROCKET_BASE_B2F:CENTER"),
             Has("EVENT_LEARNED_HAIL_GIOVANNI"))

    has_route_44_access = world.logic.has_route_44_access()

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_TOWN:EAST"), has_route_44_access)
    set_rule(get_entrance("REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_TOWN"), has_route_44_access)

    if not world.options.johto_only and world.options.randomize_phone_call_items:
        set_rule(get_entrance("REGION_ROUTE_44 -> REGION_ROUTE_44:POWER"), world.logic.can_phone_call_power())

    # Route 43
    set_rule(get_entrance("REGION_ROUTE_43 -> REGION_ROUTE_43:FRUITTREE"),
             CanUseHM(CanUseHM.CUT) & CanUseHM(CanUseHM.SURF))

    set_rule(get_location("Route 43 - TM36 from Guard in Gate"), Has("EVENT_CLEARED_ROCKET_HIDEOUT"))

    if world.options.randomize_phone_call_items and world.options.randomize_pokemon_requests:
        set_rule(get_location("Route 43 - Pink Bow from Tiffany"),
                 world.logic.can_phone_call() & HasRequestSlot(7) & Has(world.logic.pokedex))

    # Lake of Rage
    if world.options.red_gyarados_access == RedGyaradosAccess.option_whirlpool:
        set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:GYARADOS"), can_surf_and_whirlpool)
    elif world.options.red_gyarados_access == RedGyaradosAccess.option_vanilla:
        set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:GYARADOS"), CanUseHM(CanUseHM.SURF))

    set_rule(get_location("EVENT_DECIDED_TO_HELP_LANCE"), CanReachLocation("Lake of Rage - Red Scale from Gyarados"))

    set_rule(get_entrance("REGION_LAKE_OF_RAGE -> REGION_LAKE_OF_RAGE:CUT"), CanUseHM(CanUseHM.CUT))

    set_rule(get_entrance("REGION_LAKE_OF_RAGE:HIDDEN_POWER_HOUSE -> REGION_LAKE_OF_RAGE:CUT"), CanUseHM(CanUseHM.CUT))
    set_rule(get_entrance("REGION_LAKE_OF_RAGE:CUT -> REGION_LAKE_OF_RAGE:HIDDEN_POWER_HOUSE"), CanUseHM(CanUseHM.CUT))

    if world.options.randomize_pokemon_requests:
        set_rule(get_location("Lake of Rage - Magikarp Prize"),
                 Has("MAGIKARP") & Has("EVENT_CLEARED_ROCKET_HIDEOUT") & Has(world.logic.pokedex))

    # Route 44
    set_rule(get_entrance("REGION_ROUTE_44 -> REGION_ROUTE_44:WATER"), CanUseHM(CanUseHM.SURF))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 44 - Poke Ball from Wilton"), world.logic.can_phone_call())
        if not world.options.johto_only:
            if world.options.rematchsanity:
                set_rule(get_location("Route 44 - Carbos from Vance"),
                         world.logic.can_phone_call()
                         & HasAll("EVENT_BEAT_ELITE_FOUR", "EVENT_RESTORED_POWER_TO_KANTO"))
            else:
                set_rule(get_location("Route 44 - Carbos from Vance"), world.logic.can_phone_call_power())

    # Ice Path

    set_rule(get_entrance("REGION_ICE_PATH_B1F:NORTH -> REGION_ICE_PATH_B1F:NORTH:STRENGTH"),
             CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_entrance("REGION_ICE_PATH_B1F:NORTH:STRENGTH -> REGION_ICE_PATH_B1F:NORTH"),
             CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_location("EVENT_BOULDER_IN_ICE_PATH_1A"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_location("EVENT_BOULDER_IN_ICE_PATH_2A"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_location("EVENT_BOULDER_IN_ICE_PATH_3A"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_location("EVENT_BOULDER_IN_ICE_PATH_4A"), CanUseHM(CanUseHM.STRENGTH))
    ice_path_boulders = ["EVENT_BOULDER_IN_ICE_PATH_1A", "EVENT_BOULDER_IN_ICE_PATH_2A",
                         "EVENT_BOULDER_IN_ICE_PATH_3A", "EVENT_BOULDER_IN_ICE_PATH_4A"]
    set_rule(get_entrance("REGION_ICE_PATH_B2F_MAHOGANY_SIDE -> REGION_ICE_PATH_B2F_MAHOGANY_SIDE:MIDDLE"),
             HasAll(*ice_path_boulders))

    # Blackthorn
    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_BLACKTHORN_GYM_1F"), Has("EVENT_CLEARED_RADIO_TOWER"))
    set_rule(get_location("EVENT_BOULDER_IN_BLACKTHORN_GYM_1"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_location("EVENT_BOULDER_IN_BLACKTHORN_GYM_3"), CanUseHM(CanUseHM.STRENGTH))
    set_rule(get_entrance("REGION_BLACKTHORN_GYM_1F:MIDDLE -> REGION_BLACKTHORN_GYM_1F:LOLA"),
             Has("EVENT_BOULDER_IN_BLACKTHORN_GYM_3"))
    set_rule(get_entrance("REGION_BLACKTHORN_GYM_1F:LOLA -> REGION_BLACKTHORN_GYM_1F:CLAIR"),
             Has("EVENT_BOULDER_IN_BLACKTHORN_GYM_1"))
    set_rule(get_entrance("REGION_BLACKTHORN_GYM_2F -> REGION_BLACKTHORN_GYM_1F:HOLE_3"), CanUseHM(CanUseHM.STRENGTH))

    set_rule(get_entrance("REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE -> REGION_DRAGONS_DEN_1F:UPPER"),
             Has(world.logic.gym_events["clair"]))
    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE"),
             CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE -> REGION_BLACKTHORN_CITY"),
             CanUseHM(CanUseHM.SURF))

    # Dragons Den B1F
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:NORTH -> REGION_DRAGONS_DEN_B1F:CENTER"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:CENTER -> REGION_DRAGONS_DEN_B1F:NORTH"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:NORTH -> REGION_DRAGONS_DEN_B1F:WEST"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:WEST -> REGION_DRAGONS_DEN_B1F:NORTH"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:WEST -> REGION_DRAGONS_DEN_B1F:SOUTH"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:SOUTH -> REGION_DRAGONS_DEN_B1F:WEST"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:SOUTH -> REGION_DRAGONS_DEN_B1F:SOUTHEAST"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_DRAGONS_DEN_B1F:SOUTHEAST -> REGION_DRAGONS_DEN_B1F:SOUTH"), CanUseHM(CanUseHM.SURF))

    # Dragon Shrine - elder kicks you out if you haven't beaten Clair
    beaten_clair = Has(world.logic.gym_events["clair"])
    set_rule(get_entrance("REGION_DRAGON_SHRINE:ENTRANCE -> REGION_DRAGONS_DEN_B1F:SOUTH"), beaten_clair)
    set_rule(get_entrance("REGION_DRAGON_SHRINE:ENTRANCE -> REGION_DRAGON_SHRINE"), beaten_clair)

    # Route 45
    if hidden():
        set_rule(get_location("Route 45 - Hidden Item in Southeast Pond"), CanUseHM(CanUseHM.SURF))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 45 - PP Up from Kenji"), world.logic.can_phone_call())

        if not world.options.johto_only:
            set_rule(get_entrance("REGION_ROUTE_45 -> REGION_ROUTE_45:POWER"), world.logic.can_phone_call_power())
            if world.options.rematchsanity:
                set_rule(get_location("Route 45 - Iron from Parry"),
                         world.logic.can_phone_call()
                         & HasAll("EVENT_BEAT_ELITE_FOUR", "EVENT_RESTORED_POWER_TO_KANTO"))
            else:
                set_rule(get_location("Route 45 - Iron from Parry"), world.logic.can_phone_call_power())

    # Route 46
    if world.options.randomize_phone_call_items and not world.options.johto_only:
        if world.options.rematchsanity:
            set_rule(get_location("Route 46 - Calcium from Erin"),
                     world.logic.can_phone_call()
                     & HasAll("EVENT_BEAT_ELITE_FOUR", "EVENT_RESTORED_POWER_TO_KANTO"))
        else:
            set_rule(get_location("Route 46 - Calcium from Erin"), world.logic.can_phone_call_power())

    if not world.options.johto_only and world.options.randomize_phone_call_items:
        set_rule(get_entrance("REGION_ROUTE_45 -> REGION_ROUTE_45:POWER"), world.logic.can_phone_call_power())

    # Route 27
    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_NEW_BARK_TOWN"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_ROUTE_27:WESTWATER"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_ROUTE_27:CENTER -> REGION_ROUTE_27:EAST"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:CENTER"), CanUseHM(CanUseHM.SURF))
    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:EASTWHIRLPOOL"), can_surf_and_whirlpool)
    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_ROUTE_27:WESTSURFTREES"), CanUseHM(CanUseHM.SURF))
    set_rule(get_location("Route 27 - West Item across Water"), CanUseHM(CanUseHM.SURF))

    if world.options.randomize_phone_call_items:
        set_rule(get_location("Route 27 - Star Piece from Jose"), world.logic.can_phone_call())

    set_rule(get_location("Tohjo Falls - Item"), CanUseHM(CanUseHM.SURF))

    set_rule(get_entrance("REGION_TOHJO_FALLS:WEST -> REGION_TOHJO_FALLS:EAST"), can_surf_and_waterfall)
    set_rule(get_entrance("REGION_TOHJO_FALLS:EAST -> REGION_TOHJO_FALLS:WEST"), can_surf_and_waterfall)

    # Victory Road Gate
    has_victory_road_requirement = world.logic.has_victory_road_requirement()
    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_VICTORY_ROAD_GATE:NORTH"), has_victory_road_requirement)
    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE:NORTH -> REGION_VICTORY_ROAD_GATE"), has_victory_road_requirement)

    # Indigo Plateau Pokemon Center Elite Four roadblock
    if world.options.elite_four_count.value > 0:
        has_elite_four_requirement = world.logic.has_elite_four_requirement()
        set_rule(get_entrance(
            "REGION_INDIGO_PLATEAU_POKECENTER_1F -> REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE"),
            has_elite_four_requirement)
        set_rule(get_entrance(
            "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_INDIGO_PLATEAU_POKECENTER_1F"),
            has_elite_four_requirement)

    if world.options.lance_requires_elite_four:
        beat_elite_four = HasAll("EVENT_BEAT_ELITE_4_WILL", "EVENT_BEAT_ELITE_4_KOGA",
                                 "EVENT_BEAT_ELITE_4_BRUNO", "EVENT_BEAT_ELITE_4_KAREN")

        lances_room = world.get_region("REGION_LANCES_ROOM")
        for location in lances_room.locations:
            add_rule(location, beat_elite_four)
        for lances_exit in lances_room.exits:
            add_rule(lances_exit, beat_elite_four)

    # Victory Road
    if world.options.victory_road_strength:
        set_rule(get_entrance("REGION_VICTORY_ROAD:1F:ENTRANCE -> REGION_VICTORY_ROAD:1F"), CanUseHM(CanUseHM.STRENGTH))

    if johto_only() != JohtoOnly.option_on:
        has_mt_silver_requirement = world.logic.has_mt_silver_requirement()
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_VICTORY_ROAD_GATE:WEST"), has_mt_silver_requirement)
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE:WEST -> REGION_VICTORY_ROAD_GATE"), has_mt_silver_requirement)
        set_rule(get_location("EVENT_OPENED_MT_SILVER"), has_mt_silver_requirement)

        set_rule(get_location("EVENT_BEAT_RED"), world.logic.has_red_requirement())
        # set_rule(get_location("RED_1"), has_red_requirement)

        # Beating Red warps you outside Silver Cave Pokemon Center
        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_3 -> REGION_SILVER_CAVE_OUTSIDE"), Has("EVENT_BEAT_RED"))

        # Route 28
        set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE -> REGION_ROUTE_28:CUT"), CanUseHM(CanUseHM.CUT))
        set_rule(get_entrance("REGION_ROUTE_28:CUT -> REGION_SILVER_CAVE_OUTSIDE"), CanUseHM(CanUseHM.CUT))

        # Silver Cave
        set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE -> REGION_SILVER_CAVE_OUTSIDE:SURF"), CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE:SURF -> REGION_SILVER_CAVE_OUTSIDE"), CanUseHM(CanUseHM.SURF))

        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2 -> REGION_SILVER_CAVE_ROOM_2:WEST"), can_surf_and_waterfall)
        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2 -> REGION_SILVER_CAVE_ROOM_2:EAST"), can_surf_and_waterfall)
        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2:WEST -> REGION_SILVER_CAVE_ROOM_2"), CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2:EAST -> REGION_SILVER_CAVE_ROOM_2"), CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2:WEST -> REGION_SILVER_CAVE_ROOM_2:WEST_ITEM"),
                 CanUseHM(CanUseHM.SURF))
        set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2:WEST_ITEM -> REGION_SILVER_CAVE_ROOM_2:WEST"),
                 CanUseHM(CanUseHM.SURF))

    if not johto_only():

        route_22_access = world.logic.has_route_22_access_requirement()
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_VICTORY_ROAD_GATE:EAST"), route_22_access)
        set_rule(get_entrance("REGION_VICTORY_ROAD_GATE:EAST -> REGION_VICTORY_ROAD_GATE"), route_22_access)

        set_rule(get_entrance(
            "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_INDIGO_PLATEAU_POKECENTER_1F:RIVAL"),
            Has("EVENT_BEAT_RIVAL_IN_MT_MOON") & world.logic.has_elite_four_requirement())

        # Viridian
        set_rule(get_location("Viridian City - TM42 from Sleepy Guy"),
                 CanUseHM(CanUseHM.SURF, kanto=True) | CanUseHM(CanUseHM.CUT, kanto=True))

        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_VIRIDIAN_CITY -> REGION_VIRIDIAN_GYM"), kanto_gyms_access)
            set_rule(get_entrance("REGION_TRAINER_HOUSE_B1F -> REGION_TRAINER_HOUSE_B1F:CAL"), kanto_gyms_access)

        set_rule(get_entrance("REGION_VIRIDIAN_GYM -> REGION_VIRIDIAN_GYM:BLUE"), Has("EVENT_VIRIDIAN_GYM_BLUE"))

        # Route 2
        if world.options.route_2_access.value != Route2Access.option_open:
            set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:NORTHEAST"),
                     CanUseHM(CanUseHM.CUT, kanto=True))
        if world.options.route_2_access.value == Route2Access.option_vanilla:
            set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:WEST"),
                     CanUseHM(CanUseHM.CUT, kanto=True))

        set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:SOUTHEAST"), CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:WEST"), CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:CENTEREAST"),
                 CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_2:CENTEREAST -> REGION_ROUTE_2:NORTHEAST"),
                 CanUseHM(CanUseHM.CUT, kanto=True))

        # Pewter City
        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_PEWTER_CITY -> REGION_PEWTER_GYM"), kanto_gyms_access)

        # Route 3
        if world.options.route_3_access.value == Route3Access.option_boulder_badge:
            set_rule(get_entrance("REGION_PEWTER_CITY -> REGION_ROUTE_3"), Has(world.logic.badge_items["boulder"]))
            set_rule(get_entrance("REGION_ROUTE_3 -> REGION_PEWTER_CITY"), Has(world.logic.badge_items["boulder"]))

        if hidden():
            set_rule(get_location("Mount Moon Square - Hidden Item under Rock"),
                     CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))

        set_rule(get_entrance("REGION_ROUTE_4:WEST -> REGION_ROUTE_4:EAST"), Has("EVENT_CLEARED_ROUTE_4"))

        if lock_kanto_gyms:
            add_rule(get_entrance("REGION_ROUTE_3 -> REGION_MOUNT_MOON"), kanto_gyms_access)
            add_rule(get_entrance("REGION_ROUTE_4:WEST -> REGION_MOUNT_MOON"), kanto_gyms_access)
            add_rule(get_entrance("REGION_MOUNT_MOON_SQUARE -> REGION_MOUNT_MOON:NORTH_ENTRANCE"), kanto_gyms_access)
            add_rule(get_entrance("REGION_MOUNT_MOON_SQUARE -> REGION_MOUNT_MOON:SOUTH_ENTRANCE"), kanto_gyms_access)

        # Cerulean
        set_rule(get_entrance("REGION_ROUTE_24 -> REGION_CERULEAN_CITY:SURF"), CanUseHM(CanUseHM.SURF, kanto=True))
        if VanillaEventChains.MISTY in world.options.vanilla_event_chains.value:
            safe_set_location_rule("Route 24 - Grunt", Has("EVENT_MET_ROCKET_GRUNT_AT_CERULEAN_GYM"))

        set_rule(get_entrance("REGION_CERULEAN_CITY -> REGION_ROUTE_9"), CanUseHM(CanUseHM.CUT, kanto=True))

        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_CERULEAN_CITY -> REGION_CERULEAN_GYM"), kanto_gyms_access)

        if VanillaEventChains.MISTY in world.options.vanilla_event_chains.value:
            set_rule(get_entrance("REGION_CERULEAN_GYM -> REGION_CERULEAN_GYM:ROCKET"),
                     Has("EVENT_MET_MANAGER_AT_POWER_PLANT"))
            set_rule(get_entrance("REGION_CERULEAN_GYM -> REGION_CERULEAN_GYM:MISTY"),
                     Has("EVENT_ROUTE_25_MISTY_DATE"))
            set_rule(get_entrance("REGION_ROUTE_24 -> REGION_ROUTE_24:ROCKET"),
                     Has("EVENT_MET_ROCKET_GRUNT_AT_CERULEAN_GYM"))

        set_rule(get_entrance("REGION_ROUTE_9 -> REGION_CERULEAN_CITY"), CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_9 -> REGION_ROUTE_10_NORTH:SURF"), CanUseHM(CanUseHM.SURF, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_10_NORTH:SURF -> REGION_ROUTE_9"), CanUseHM(CanUseHM.SURF, kanto=True))

        # Route 25
        set_rule(get_location("Route 25 - Item behind Cut Tree"), CanUseHM(CanUseHM.CUT, kanto=True))

        if VanillaEventChains.MISTY in world.options.vanilla_event_chains.value:
            set_rule(get_entrance("REGION_ROUTE_25 -> REGION_ROUTE_25:MISTY_DATE"),
                     Has("EVENT_MET_ROCKET_GRUNT_AT_CERULEAN_GYM"))

        # Power Plant
        set_rule(get_location("EVENT_RESTORED_POWER_TO_KANTO"), Has("Machine Part"))
        set_rule(get_location("Power Plant - TM07 from Manager"), Has("EVENT_RESTORED_POWER_TO_KANTO"))

        # Lavender
        if world.options.randomize_pokegear or world.options.remote_items:
            set_rule(get_location("Lavender Radio Tower - EXPN Card"), Has("EVENT_RESTORED_POWER_TO_KANTO"))
        set_rule(get_location("EVENT_GOT_EXPN_CARD"), Has("EVENT_RESTORED_POWER_TO_KANTO"))

        # Route 12
        if world.options.route_12_access:
            r12_rule = Has("Squirtbottle")
            if world.options.route_12_access.value == Route12Access.option_weird_tree:
                r12_rule |= CanUseHM(CanUseHM.SURF, kanto=True)
            set_rule(get_entrance("REGION_ROUTE_12:NORTH -> REGION_ROUTE_12:SOUTH"), r12_rule)
            set_rule(get_entrance("REGION_ROUTE_12:SOUTH -> REGION_ROUTE_12:NORTH"), r12_rule)

        set_rule(get_location("Route 12 - Item behind North Cut Tree"), CanUseHM(CanUseHM.CUT, kanto=True))

        set_rule(get_location("Route 12 - Item behind South Cut Tree across Water"),
                 CanUseHM(CanUseHM.CUT, kanto=True) & CanUseHM(CanUseHM.SURF, kanto=True))

        if hidden():
            set_rule(get_location("Route 12 - Hidden Item on Island"), CanUseHM(CanUseHM.SURF, kanto=True))

        # Route 13
        set_rule(get_entrance("REGION_ROUTE_13 -> REGION_ROUTE_13:CUT"), CanUseHM(CanUseHM.CUT, kanto=True))

        # Route 14
        set_rule(get_entrance("REGION_ROUTE_14 -> REGION_ROUTE_14:CUT"), CanUseHM(CanUseHM.CUT, kanto=True))

        # Vermilion
        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_CITY:GYM_ENTRANCE"),
                 CanUseHM(CanUseHM.CUT, kanto=True) | CanUseHM(CanUseHM.SURF, kanto=True))
        set_rule(get_entrance("REGION_VERMILION_CITY:GYM_ENTRANCE -> REGION_VERMILION_CITY"),
                 CanUseHM(CanUseHM.CUT, kanto=True) | CanUseHM(CanUseHM.SURF, kanto=True))
        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_VERMILION_CITY:GYM_ENTRANCE -> REGION_VERMILION_GYM"), kanto_gyms_access)

        kanto_badges = list(world.logic.badge_items.values())[8:]
        set_rule(get_location("Vermilion City - HP Up from Man nowhere near PokeCenter"), HasAll(*kanto_badges))

        set_rule(get_location("Vermilion City - Lost Item from Guy in Fan Club"), Has("EVENT_RESTORED_POWER_TO_KANTO"))

        if VanillaEventChains.COPYCAT in world.options.vanilla_event_chains.value:
            add_rule(get_location("Vermilion City - Lost Item from Guy in Fan Club"),
                     Has("EVENT_MET_COPYCAT_FOUND_OUT_ABOUT_LOST_ITEM"))

        has_expn = HasAll(*world.logic.expn_components)
        set_rule(get_location("EVENT_FOUGHT_SNORLAX"), has_expn)
        set_static_rule("Snorlax", has_expn)

        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_ROUTE_11"), has_expn)
        set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE"), has_expn)

        set_rule(get_entrance("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_VERMILION_CITY"), has_expn)
        set_rule(get_entrance("REGION_ROUTE_11 -> REGION_VERMILION_CITY"), has_expn)
        set_rule(get_entrance("REGION_VERMILION_PORT -> REGION_VERMILION_PORT:TICKET"), world.logic.ship_rule())

        if hidden():
            set_rule(get_location("Vermilion Port - Hidden Item in Buoy"), CanUseHM(CanUseHM.SURF, kanto=True))

        set_rule(get_entrance("REGION_FAST_SHIP_1F -> REGION_VERMILION_PORT:TICKET"),
                 Has("EVENT_FAST_SHIP_LAZY_SAILOR"))

        # Saffron
        set_rule(get_location("Copycat's House - Pass from Copycat"), Has("Lost Item"))
        set_rule(get_location("EVENT_MET_COPYCAT_FOUND_OUT_ABOUT_LOST_ITEM"), Has("EVENT_RESTORED_POWER_TO_KANTO"))

        set_rule(get_entrance("REGION_SAFFRON_MAGNET_TRAIN_STATION -> REGION_GOLDENROD_MAGNET_TRAIN_STATION"),
                 world.logic.magnet_train_rule())

        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_SAFFRON_CITY -> REGION_SAFFRON_GYM:ENTRANCE"), kanto_gyms_access)

        if SaffronGatehouseTea.NORTH in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_ROUTE_5_SAFFRON_GATE:NORTH -> REGION_ROUTE_5_SAFFRON_GATE:SOUTH"), Has("Tea"))
            set_rule(get_entrance("REGION_ROUTE_5_SAFFRON_GATE:SOUTH -> REGION_ROUTE_5_SAFFRON_GATE:NORTH"), Has("Tea"))

        if SaffronGatehouseTea.EAST in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_ROUTE_8_SAFFRON_GATE:WEST -> REGION_ROUTE_8_SAFFRON_GATE:EAST"), Has("Tea"))
            set_rule(get_entrance("REGION_ROUTE_8_SAFFRON_GATE:EAST -> REGION_ROUTE_8_SAFFRON_GATE:WEST"), Has("Tea"))

        if SaffronGatehouseTea.SOUTH in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_ROUTE_6_SAFFRON_GATE:NORTH -> REGION_ROUTE_6_SAFFRON_GATE:SOUTH"), Has("Tea"))
            set_rule(get_entrance("REGION_ROUTE_6_SAFFRON_GATE:SOUTH -> REGION_ROUTE_6_SAFFRON_GATE:NORTH"), Has("Tea"))

        if SaffronGatehouseTea.WEST in world.options.saffron_gatehouse_tea.value:
            set_rule(get_entrance("REGION_ROUTE_7_SAFFRON_GATE:WEST -> REGION_ROUTE_7_SAFFRON_GATE:EAST"), Has("Tea"))
            set_rule(get_entrance("REGION_ROUTE_7_SAFFRON_GATE:EAST -> REGION_ROUTE_7_SAFFRON_GATE:WEST"), Has("Tea"))

        # Underground Paths
        if world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_north_south,
                                                              UndergroundsRequirePower.option_both):
            set_rule(get_entrance("REGION_ROUTE_5 -> REGION_ROUTE_5_UNDERGROUND_PATH_ENTRANCE"),
                     Has("EVENT_RESTORED_POWER_TO_KANTO"))

            set_rule(get_entrance("REGION_ROUTE_6 -> REGION_ROUTE_6_UNDERGROUND_PATH_ENTRANCE"),
                     Has("EVENT_RESTORED_POWER_TO_KANTO"))

        if (world.options.east_west_underground
                and world.options.undergrounds_require_power.value in (
                        UndergroundsRequirePower.option_east_west,
                        UndergroundsRequirePower.option_both)):
            set_rule(get_entrance("REGION_ROUTE_7 -> REGION_ROUTE_7_UNDERGROUND_PATH_ENTRANCE"),
                     Has("EVENT_RESTORED_POWER_TO_KANTO"))

            set_rule(get_entrance("REGION_ROUTE_8 -> REGION_ROUTE_8_UNDERGROUND_PATH_ENTRANCE"),
                     Has("EVENT_RESTORED_POWER_TO_KANTO"))

        # Route 8
        set_rule(get_entrance("REGION_ROUTE_8 -> REGION_ROUTE_8:CUT"), CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_8:CUT -> REGION_ROUTE_8"), CanUseHM(CanUseHM.CUT, kanto=True))

        # Celadon
        set_rule(get_entrance("REGION_CELADON_CITY -> REGION_CELADON_CITY:GYM_ENTRANCE"),
                 CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_CELADON_CITY:GYM_ENTRANCE -> REGION_CELADON_CITY"),
                 CanUseHM(CanUseHM.CUT, kanto=True))

        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_CELADON_CITY:GYM_ENTRANCE -> REGION_CELADON_GYM"), kanto_gyms_access)

        if Shopsanity.GAME_CORNERS in world.options.shopsanity.value:
            set_rule(
                get_entrance("REGION_CELADON_GAME_CORNER_PRIZE_ROOM -> REGION_MART_CELADON_GAME_CORNER_PRIZE_ROOM"),
                Has("Coin Case"))

        set_static_rule("CeladonGameCornerPrizeRoom1", Has("Coin Case"))
        set_static_rule("CeladonGameCornerPrizeRoom2", Has("Coin Case"))
        set_static_rule("CeladonGameCornerPrizeRoom3", Has("Coin Case"))

        set_rule(get_location("EVENT_OBTAINED_DIPLOMA"), HasNPokemon(world.pokemon_pool.diploma_count))

        # Route 16
        set_rule(get_entrance("REGION_ROUTE_16 -> REGION_ROUTE_16:NORTH"), CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_16:NORTH -> REGION_ROUTE_16"), CanUseHM(CanUseHM.CUT, kanto=True))

        # Cycling Road - bike required to traverse gatehouses
        set_rule(get_entrance("REGION_ROUTE_16_GATE:EAST -> REGION_ROUTE_16_GATE:WEST"), Has("Bicycle"))
        set_rule(get_entrance("REGION_ROUTE_16_GATE:WEST -> REGION_ROUTE_16_GATE:EAST"), Has("Bicycle"))
        set_rule(get_entrance("REGION_ROUTE_17_ROUTE_18_GATE:EAST -> REGION_ROUTE_17_ROUTE_18_GATE:WEST"),
                 Has("Bicycle"))
        set_rule(get_entrance("REGION_ROUTE_17_ROUTE_18_GATE:WEST -> REGION_ROUTE_17_ROUTE_18_GATE:EAST"),
                 Has("Bicycle"))

        # Route 15
        set_rule(get_location("Route 15 - Item"), CanUseHM(CanUseHM.CUT, kanto=True))

        # Fuchsia City
        set_rule(get_entrance("REGION_FUCHSIA_CITY -> REGION_FUCHSIA_CITY:CUT"), CanUseHM(CanUseHM.CUT, kanto=True))
        set_rule(get_entrance("REGION_FUCHSIA_CITY:CUT -> REGION_FUCHSIA_CITY"), CanUseHM(CanUseHM.CUT, kanto=True))

        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_FUCHSIA_CITY -> REGION_FUCHSIA_GYM"), kanto_gyms_access)

        if world.options.south_kanto_condition == SouthKantoCondition.option_enter_south_kanto:
            south_kanto_condition = Has("EVENT_CINNABAR_ROCKS_CLEARED")
        else:
            south_kanto_condition = Has("EVENT_RESTORED_POWER_TO_KANTO")

        if world.options.south_kanto_access.blocks_route_19:
            set_rule(get_entrance("REGION_ROUTE_19:GATE_ENTRANCE -> REGION_ROUTE_19:SHORE"), south_kanto_condition)
            if world.options.south_kanto_condition != SouthKantoCondition.option_enter_south_kanto:
                set_rule(get_entrance("REGION_ROUTE_19:SHORE -> REGION_ROUTE_19:GATE_ENTRANCE"), south_kanto_condition)
        if world.options.south_kanto_access.blocks_route_21:
            set_rule(get_entrance("REGION_ROUTE_21:NORTH -> REGION_ROUTE_21:SOUTH"), south_kanto_condition)
            if world.options.south_kanto_condition != SouthKantoCondition.option_enter_south_kanto:
                set_rule(get_entrance("REGION_ROUTE_21:SOUTH -> REGION_ROUTE_21:NORTH"), south_kanto_condition)

        add_rule(get_entrance("REGION_ROUTE_19:SHORE -> REGION_ROUTE_19"), CanUseHM(CanUseHM.SURF, kanto=True))

        # Cinnabar
        set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_20"), CanUseHM(CanUseHM.SURF, kanto=True))
        set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_21:SOUTH"), CanUseHM(CanUseHM.SURF, kanto=True))
        set_rule(get_entrance("REGION_PALLET_TOWN -> REGION_ROUTE_21:NORTH"), CanUseHM(CanUseHM.SURF, kanto=True))
        set_rule(get_entrance("REGION_ROUTE_20:SEAFOAM -> REGION_ROUTE_20"), CanUseHM(CanUseHM.SURF, kanto=True))

        if lock_kanto_gyms:
            set_rule(get_entrance("REGION_ROUTE_20:SEAFOAM -> REGION_SEAFOAM_GYM"), kanto_gyms_access)

        if world.options.randomize_pokemon_requests:
            bills_grandpa_locations = (
                "Bill's House - Everstone from Bill's Grandpa",
                "Bill's House - Leaf Stone from Bill's Grandpa",
                "Bill's House - Water Stone from Bill's Grandpa",
                "Bill's House - Fire Stone from Bill's Grandpa",
                "Bill's House - Thunderstone from Bill's Grandpa"
            )

            for i, location in enumerate(bills_grandpa_locations):
                set_rule(get_location(location),
                         And(*[HasRequestSlot(j) for j in range(i + 1)], Has(world.logic.pokedex)))

    if Goal.UNOWN_HUNT in world.options.goal:
        for location, unown in world.generated_unown_signs.items():
            chamber_event = get_chamber_event_for_unown(unown)
            set_rule(get_location(location), Has(chamber_event))
            set_rule(get_location(f"{location}_Encounter"), Has(chamber_event))

    trade_gate: Rule = True_() if world.options.trades_required else GlitchedLogic()
    for trade_id in world.generated_trades:
        safe_set_location_rule(trade_id, HasTradeRequest(trade_id) & Has(world.logic.pokedex) & trade_gate)

    if world.options.randomize_lucky_number_show:
        prize_labels = ["Radio Tower 1F - Lucky Number Show 1st Prize",
                        "Radio Tower 1F - Lucky Number Show 2nd Prize",
                        "Radio Tower 1F - Lucky Number Show 3rd Prize"]
        for i, trade_id in enumerate(world.generated_lucky_number_trades):
            # Trade-access event lives in the trade's region (region reach is free); gate it on the species.
            safe_set_location_rule(
                f"Lucky Number Trade {i + 1}", HasTradeRequest(trade_id) & Has(world.logic.pokedex))
            # Prize requires winning the corresponding trade-access event.
            safe_set_location_rule(prize_labels[i], Has(f"Lucky Number Trade {i + 1}"))

    if world.options.require_itemfinder:
        rule = Has("Itemfinder")
        if world.options.require_itemfinder == RequireItemfinder.option_logically_required:
            rule = rule | GlitchedLogic()

        for location in world.multiworld.get_locations(world.player):
            if "Hidden" in location.tags:
                add_rule(location, rule)

    if world.options.grasssanity:
        for region in world.get_regions():
            if region.name in data.grass_tiles:
                rule = CanUseHM(CanUseHM.CUT, region=region.name)
                add_rule(get_entrance(f"{region.name} -> {region.name}:GRASS"), rule)

    if world.options.dexsanity or world.options.dexcountsanity:
        set_rule(get_entrance("Menu -> Pokedex"), Has(world.logic.pokedex))

    for pokemon_id in world.generated_dexsanity:
        pokemon_data = world.generated_pokemon[pokemon_id]
        set_rule(get_location(f"Pokedex - {pokemon_data.friendly_name}"), HasSpeciesDex(pokemon_id))

    leniency = world.options.dexcountsanity_leniency.value

    def _dex_rule(target: int) -> Rule:
        return HasDexCount(min(world.pokemon_pool.dexcountsanity_total, target + leniency))

    for dexcountsanity_count in world.generated_dexcountsanity[:-1]:
        set_rule(get_location(f"Pokedex - Catch {dexcountsanity_count} Pokemon"), _dex_rule(dexcountsanity_count))

    if world.generated_dexcountsanity:
        set_rule(get_location("Pokedex - Final Catch"), _dex_rule(world.generated_dexcountsanity[-1]))

    bt_active = world.options.battle_tower_sanity or Goal.BATTLE_TOWER in world.options.goal
    if bt_active:
        milestones = [
            "EVENT_BEAT_FALKNER", "EVENT_BEAT_BUGSY", "EVENT_BEAT_WHITNEY", "EVENT_BEAT_MORTY",
            "EVENT_BEAT_JASMINE", "EVENT_BEAT_CHUCK", "EVENT_BEAT_PRYCE", "EVENT_BEAT_CLAIR",
            "EVENT_BEAT_ELITE_FOUR",
        ]
        if world.options.johto_only == JohtoOnly.option_off:
            milestones.extend([
                "EVENT_BEAT_BROCK", "EVENT_BEAT_MISTY", "EVENT_BEAT_LTSURGE", "EVENT_BEAT_ERIKA",
                "EVENT_BEAT_JANINE", "EVENT_BEAT_SABRINA", "EVENT_BEAT_BLAINE", "EVENT_BEAT_BLUE",
            ])
        if world.options.johto_only != JohtoOnly.option_on:
            milestones.append("EVENT_BEAT_RED")
        pool_size = len(milestones)
        progressive = world.options.battle_tower_progressive_tier_unlocks

        sub_uber_species = [name for name, pkmn in world.generated_pokemon.items() if pkmn.bst < 600]

        set_rule(get_entrance("REGION_BATTLE_TOWER_1F -> Battle Tower"),
                 Has("Battle Tower Ubers Pass") | HasFromListUnique(*sub_uber_species, count=3))

        # Per-tier rules live on the parent → tier-N sub-region entrance, so the
        # sanity location and the logical event in that sub-region share access.
        for tier_idx in range(BATTLE_TOWER_NUM_TIERS):
            required = min(tier_idx + 1, pool_size)
            rule = HasFromListUnique(*milestones, count=required)
            if tier_idx + 1 >= BATTLE_TOWER_UBERS_TIER:
                rule = rule & (Has("Battle Tower Ubers Pass") | GlitchedLogic())
            set_rule(get_entrance(f"Battle Tower -> Battle Tower Tier {tier_idx + 1}"), rule)
        if progressive:
            for tier_idx in range(BATTLE_TOWER_NUM_TIERS):
                add_rule(get_entrance(f"Battle Tower -> Battle Tower Tier {tier_idx + 1}"),
                         Has("Progressive Battle Tower Tier Unlock", tier_idx + 1))

        if Goal.BATTLE_TOWER in world.options.goal:
            tier_events = [f"EVENT_BATTLE_TOWER_TIER_{n}_BEATEN" for n in range(1, BATTLE_TOWER_NUM_TIERS + 1)]
            set_rule(get_location("EVENT_BEAT_ALL_BATTLE_TOWER_TIERS"), HasAll(*tier_events))

    precollected_tod = world.precollected_tod
    pokegear_name = "Pokegear" if world.options.randomize_pokegear else "EVENT_GOT_POKEGEAR"

    def has_tod(tod_item: str) -> Rule:
        if tod_item == precollected_tod:
            return Has(tod_item)
        return Has(tod_item) & Has(pokegear_name)

    def time_of_day_rule(encounter_key: EncounterKey) -> Rule | None:
        if not world.options.unlockable_time_of_day or encounter_key.time_of_day is None:
            return None
        if encounter_key.encounter_type is EncounterType.Grass:
            return has_tod(encounter_key.time_of_day.name)
        if encounter_key.encounter_type is EncounterType.Fish:
            # the game uses the day fishing group during morn as well
            if encounter_key.time_of_day is FishTimeOfDay.Day:
                return Or(has_tod("Morn"), has_tod("Day"))
            return has_tod(encounter_key.time_of_day.name)
        return None

    def swarm_rule(encounter_key: EncounterKey) -> Rule:
        cfg = SWARM_REGISTRATIONS[encounter_key.region_id]
        rule = world.logic.can_phone_call() & Has(cfg["registration_event"])
        if cfg["fishing_region"] is not None:
            rule = rule & world.logic.can_fish()
        return rule

    for location in world.multiworld.get_locations(world.player):
        if "wilds scaling" not in location.tags:
            continue
        encounter_key = location.encounter_key

        if encounter_key.encounter_type is EncounterType.Water:
            add_rule(location, CanUseHM(CanUseHM.SURF, region=location.parent_region.name))
        elif encounter_key.encounter_type is EncounterType.Fish:
            add_rule(location, world.logic.fishing_rod_rules[encounter_key.fishing_rod])
        elif encounter_key.encounter_type is EncounterType.Tree:
            add_rule(location, CanUseFieldMove(CanUseFieldMove.HEADBUTT))
        elif encounter_key.encounter_type is EncounterType.RockSmash:
            add_rule(location, CanUseFieldMove(CanUseFieldMove.ROCK_SMASH))

        if encounter_key.is_swarm:
            add_rule(location, swarm_rule(encounter_key))

        tod_rule = time_of_day_rule(encounter_key)
        # a Day fish key's shared slots are reachable at any time; scale from the earliest slot
        if tod_rule is not None and not (encounter_key.encounter_type is EncounterType.Fish
                                         and encounter_key.time_of_day is FishTimeOfDay.Day):
            add_rule(location, tod_rule)

    for encounter_key, encounter_access in world.logic.wild_regions.items():

        if encounter_access is LogicalAccess.Inaccessible: continue
        if encounter_access is LogicalAccess.OutOfLogic and not world.is_universal_tracker: continue

        rule = None

        if encounter_key.encounter_type is EncounterType.Water:
            region = world.get_region(encounter_key.region_name())
            parent_region = region.entrances[0].parent_region
            rule = CanUseHM(CanUseHM.SURF, region=parent_region.name)
        elif encounter_key.encounter_type is EncounterType.Fish:
            rule = world.logic.fishing_rod_rules[encounter_key.fishing_rod]
        elif encounter_key.encounter_type is EncounterType.Tree:
            rule = CanUseFieldMove(CanUseFieldMove.HEADBUTT)
        elif encounter_key.encounter_type is EncounterType.RockSmash:
            rule = CanUseFieldMove(CanUseFieldMove.ROCK_SMASH)
        elif encounter_key.encounter_type is EncounterType.Static:
            if not world.is_universal_tracker: continue

            location = get_location(f"{encounter_key.region_name()}_1")
            if encounter_access is LogicalAccess.OutOfLogic:
                add_rule(location, GlitchedLogic())
            continue

        region_name = encounter_key.region_name()
        tod_rule = time_of_day_rule(encounter_key)
        key_swarm_rule = swarm_rule(encounter_key) if encounter_key.is_swarm else None

        # shared fish slots are served at all times of day; only the time-varying slots are Day-gated
        day_time_slot_indexes = None
        if (encounter_key.encounter_type is EncounterType.Fish
                and encounter_key.time_of_day is FishTimeOfDay.Day):
            day_time_slot_indexes = {
                slot_index for slot_index, _ in
                data.fish_time_slots[(encounter_key.region_id, encounter_key.fishing_rod)]}

        # Unown gating is added by fill_wild_encounter_locations, once starter swaps have settled species.
        for i in range(len(world.generated_wild[encounter_key])):
            location = get_location(f"{region_name}_{i + 1}")

            if rule is not None:
                set_rule(location, rule)

            if key_swarm_rule is not None:
                add_rule(location, key_swarm_rule)

            if tod_rule is not None and (day_time_slot_indexes is None or i in day_time_slot_indexes):
                add_rule(location, tod_rule)

            if encounter_access is LogicalAccess.OutOfLogic:
                add_rule(location, GlitchedLogic())

    def evolution_rule(evolved_from: str,
                       evolutions: list[tuple[EvolutionData, LogicalAccess, str | None]]) -> Rule:
        options: list[Rule] = []
        for evo, access, item_label in evolutions:
            ool = access is LogicalAccess.OutOfLogic
            gate: Rule = GlitchedLogic() if ool else True_()
            if evo.evo_type in (EvolutionType.Level, EvolutionType.Stats):
                gyms = ((evo.level - 1) // world.options.evolution_gym_levels) + 1
                inner = True_() if ool else HasGyms(gyms)
            elif evo.evo_type is EvolutionType.Item:
                inner = Has(item_label)
            elif evo.evo_type is EvolutionType.Trade:
                inner = Has("Link Cable") & Has(item_label)
            elif evo.evo_type is EvolutionType.Happiness:
                inner = True_() if ool else HasAny("EVENT_DAISY_GROOMING", "EVENT_HAIRCUT_BROTHERS")
            else:
                continue
            options.append(gate & inner)
        return Has(evolved_from) & (Or(*options) if options else False_())

    locations_to_evolutions = defaultdict[str, list[tuple[EvolutionData, LogicalAccess, str | None]]](list)
    locations_to_pokemon = dict[str, str]()

    for evolvee, evolutions in world.logic.evolution.items():
        for evolution, logical_access in evolutions:
            if not world.is_universal_tracker and logical_access is LogicalAccess.OutOfLogic: continue
            location_name = evolution_location_name(world, evolvee, evolution.pokemon)
            locations_to_pokemon[location_name] = evolvee
            item_label = (item_const_name_to_label(evolution.condition)
                          if evolution.evo_type in (EvolutionType.Item, EvolutionType.Trade) else None)
            locations_to_evolutions[location_name].append((evolution, logical_access, item_label))

    for location_name, evo_data in locations_to_evolutions.items():
        evolves_from = locations_to_pokemon[location_name]
        set_rule(get_location(location_name), evolution_rule(evolves_from, evo_data))

    def breeding_rule(breeders_access: list[tuple[str, LogicalAccess, bool]]) -> Rule:
        options: list[Rule] = []
        for breeder, access, requires_ditto in breeders_access:
            if access is LogicalAccess.InLogic:
                gate: Rule = True_()
            elif access is LogicalAccess.OutOfLogic:
                gate = GlitchedLogic()
            else:
                continue
            ditto: Rule = Has("DITTO") if requires_ditto else True_()
            options.append(Has(breeder) & ditto & gate)
        return Or(*options) if options else False_()

    if world.options.breeding_methods_required or world.is_universal_tracker:
        set_rule(get_entrance("Menu -> Breeding"),
                 HasAll("EVENT_UNLOCKED_DAY_CARE", "EVENT_UNLOCKED_DAY_CARE_YARD"))

        if world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto:
            add_rule(get_entrance("Menu -> Breeding"), Has("DITTO") | GlitchedLogic())

    for base_form_id, breeders in world.logic.breeding.items():
        logical_access = [access for _, access, _ in breeders]
        if not world.is_universal_tracker and (LogicalAccess.InLogic not in logical_access): continue
        set_rule(get_location(f"Hatch {world.generated_pokemon[base_form_id].friendly_name}"), breeding_rule(breeders))

    for dark_area, region_names in DARK_AREA_REGIONS.items():
        if dark_area not in world.options.dark_areas:
            continue
        flash_fn = CanUseHM(CanUseHM.FLASH, kanto=True) if dark_area in KANTO_DARK_AREAS else CanUseHM(CanUseHM.FLASH)
        for region_name in region_names:
            try:
                region = world.get_region(region_name)
            except KeyError:
                continue
            for exit_ in region.exits:
                add_rule(exit_, flash_fn)
            for location in region.locations:
                add_rule(location, flash_fn)

    for region_name in CYCLING_ROAD_REGIONS:
        try:
            region = world.get_region(region_name)
        except KeyError:
            continue
        for exit_ in region.exits:
            add_rule(exit_, Has("Bicycle"))
        for location in region.locations:
            add_rule(location, Has("Bicycle"))

    if world.options.kinda_early_surf:
        add_rule(get_entrance("REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
                 CanUseHM(CanUseHM.SURF))
        add_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_TOWN:EAST"), CanUseHM(CanUseHM.SURF))
        add_rule(get_location("EVENT_JASMINE_RETURNED_TO_GYM"), CanUseHM(CanUseHM.SURF))
        add_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_2F:TAKEOVER"), CanUseHM(CanUseHM.SURF))

        def safe_add_location_rule(name: str, rule: CollectionRule | Rule):
            try:
                loc = world.get_location(name)
            except KeyError:
                return
            add_rule(loc, rule)

        safe_add_location_rule("Radio Tower 1F - Grunt", CanUseHM(CanUseHM.SURF))
        if world.options.level_scaling:
            safe_add_location_rule("GRUNTM_3", CanUseHM(CanUseHM.SURF))
        add_rule(get_entrance("REGION_ECRUTEAK_TIN_TOWER_ENTRANCE -> REGION_ECRUTEAK_TIN_TOWER_ENTRANCE:BEHIND_SAGE"),
                 CanUseHM(CanUseHM.SURF))
        add_rule(get_location("EVENT_FOUGHT_SNORLAX"), CanUseHM(CanUseHM.SURF, kanto=True))
        add_rule(get_entrance("REGION_VERMILION_CITY -> REGION_ROUTE_11"), CanUseHM(CanUseHM.SURF, kanto=True))
        add_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE"),
                 CanUseHM(CanUseHM.SURF, kanto=True))
        if world.options.level_scaling:
            add_rule(get_location("Snorlax"), CanUseHM(CanUseHM.SURF, kanto=True))
        if world.options.static_pokemon_required or world.is_universal_tracker:
            add_rule(get_location("Static_Snorlax_1"), CanUseHM(CanUseHM.SURF, kanto=True))


def verify_hm_accessibility(world: "PokemonCrystalWorld") -> None:
    if world.options.field_moves_always_usable: return

    logic = world.logic

    hm_rules: dict[str, CollectionRule] = {
        "CUT": (CanUseHM(CanUseHM.CUT) | CanUseHM(CanUseHM.CUT, kanto=True)).resolve(world),
        "FLY": CanUseHM(CanUseHM.FLY).resolve(world),
        "SURF": (CanUseHM(CanUseHM.SURF) | CanUseHM(CanUseHM.SURF, kanto=True)).resolve(world),
        "STRENGTH": (CanUseHM(CanUseHM.STRENGTH) | CanUseHM(CanUseHM.STRENGTH, kanto=True)).resolve(world),
        "FLASH": (CanUseHM(CanUseHM.FLASH, allow_ool=False)
                  | CanUseHM(CanUseHM.FLASH, True, allow_ool=False)).resolve(world),
        "WHIRLPOOL": (CanUseHM(CanUseHM.WHIRLPOOL) | CanUseHM(CanUseHM.WHIRLPOOL, kanto=True)).resolve(world),
        "WATERFALL": (CanUseHM(CanUseHM.WATERFALL) | CanUseHM(CanUseHM.WATERFALL, kanto=True)).resolve(world),
        "HEADBUTT": CanUseFieldMove(CanUseFieldMove.HEADBUTT).resolve(world),
        "ROCK_SMASH": CanUseFieldMove(CanUseFieldMove.ROCK_SMASH).resolve(world),
    }

    def can_use_hm(state: CollectionState, hm: str) -> bool:
        rule = hm_rules.get(hm)
        return rule(state) if rule is not None else False

    def do_verify(hms: list[str]):
        hms_to_verify = hms.copy()
        unverified_hms = []
        last_hm = None

        while hms_to_verify:
            state = world.get_world_collection_state()
            hm_to_verify = hms_to_verify[0]
            if not can_use_hm(state, hm_to_verify):

                if last_hm == hm_to_verify:
                    unverified_hms.append(hms_to_verify.pop(0))
                    continue

                last_hm = hm_to_verify
                logical_pokemon = sorted(world.pokemon_pool.all_available)
                world.random.shuffle(logical_pokemon)
                valid_pokemon = [mon for mon in logical_pokemon if state.has(mon, world.player)
                                 and mon not in logic.compatible_hm_pokemon[hm_to_verify]]
                if valid_pokemon:
                    pokemon = world.random.choice(valid_pokemon)
                    add_hm_compatibility(world, pokemon, hm_to_verify)
            else:
                hms_to_verify.pop(0)

        if unverified_hms and unverified_hms == hms:
            state = world.get_world_collection_state()
            if any((HasHMBadge(hm) | HasHMBadge(hm, True)).resolve(world)(state) for hm in unverified_hms):
                unverified_hms_list = ",".join(unverified_hms)
                raise Exception(f"Failed to ensure access to {unverified_hms_list} for player {world.player}")
        elif unverified_hms:
            unverified_hms.reverse()
            do_verify(unverified_hms)

    hms = ["CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH"]
    world.random.shuffle(hms)
    do_verify(hms)
