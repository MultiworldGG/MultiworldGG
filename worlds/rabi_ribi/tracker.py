from functools import cached_property
from typing import Any, Optional, override
from BaseClasses import CollectionState, Entrance, Location, Region
from NetUtils import JSONMessagePart
from Options import Option
from Utils import get_fuzzy_results, get_intended_text
from worlds.AutoWorld import World
from .rule_builder.glitched_rules import evaluate_rule, get_logic_color, rule_to_json
from .bases import RabiRibiWorldBase
from .constants import BASE_ID
from .rule_builder.custom_rules import Macro
from .data import data
from .items import item_data_table
from .locations import all_locations
from .names import ItemName


def should_regenerate_seed_for_universal_tracker(world: World):
    """
    If true, this world has information from Universal Tracker that should be used when generating the seed.
    This ensures that the world state matches the seed used by the connected server.
    """
    return hasattr(world.multiworld, "re_gen_passthrough") and world.game in world.multiworld.re_gen_passthrough  # type: ignore


def map_page_index(data: Any) -> int:
    """
    Maps Rabi-Ribi area IDs to map IDs used by Poptracker.
    """
    if type(data) != int:
        return 0
    return data


MAP_OFFSETS = [
    (1, 1),  # Southern Woodland
    (1, 2),  # Western Coast
    (3, 2),  # Island Core
    (2, 1),  # Northern Tundra
    (1, 1),  # Eastern Highlands
    (2, -1), # Rabi Rabi Town
    (1, 1),  # Plurkwood
    (1, 1),  # Subterranean Area
    (0, 4),  # Warp Destination
    (1, 1),  # System Interior
]


def location_icon_coords(index: int, coords: tuple[int, int]) -> Optional[tuple[int, int, str]]:
    """
    Maps a Rabi-Ribi room to coordinates on the Poptracker map.
    """
    if not coords or coords == (-1, -1):
        return None

    room_x, room_y = coords
    dx, dy = MAP_OFFSETS[index]
    x = ((room_x + dx) * 32) - 16
    y = ((room_y + dy) * 32) - 16
    return x, y, f"images/items/erina_badge.png"


# Maps AP location IDs to the respective names used by Poptracker
poptracker_name_mapping: dict[str, int] = {
    location.poptracker_name: BASE_ID + location.id for location in data.locations}


class RabiRibiUTWorld(RabiRibiWorldBase):
    tracker_world = {
        "map_page_maps": ["maps/maps.jsonc"],
        "map_page_locations": ["locations/locations.jsonc"],
        "map_page_setting_key": "{player}_{team}_rabi_ribi_area_id",
        "map_page_index": map_page_index,
        "external_pack_key": "ut_pack_path",
        "location_setting_key": "{player}_{team}_rabi_ribi_coords",
        "location_icon_coords": location_icon_coords,
        "poptracker_name_mapping": poptracker_name_mapping
    }
    ut_can_gen_without_yaml = True
    glitches_item_name = ItemName.glitched_logic

    @cached_property
    def is_ut(self) -> bool:
        return getattr(self.multiworld, "generation_is_fake", False)

    @override
    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            slot_options: dict[str, Any] = slot_data.get("options", {})

            # Set all your options here instead of getting them from the YAML
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))

            self.picked_templates = slot_data["picked_templates"]
            self.map_transition_shuffle_order = slot_data["map_transition_shuffle_order"]
            self.start_location = slot_data["start_location"]
        super().generate_early()

    def get_logical_path(self, dest_name: str, state: CollectionState, *_: Any, **__: Any) -> list[JSONMessagePart]:
        if not dest_name:
            return [{"type": "text", "text": "Provide a location or region to route to using /get_logical_path [name]"}]

        goal_location: Location | None = None
        goal_region: Region | None = None
        region_name = ""
        location_name, usable, response = get_intended_text(
            dest_name, [loc.name for loc in self.get_locations()])
        if usable:
            try:
                goal_location = self.get_location(location_name)
            except KeyError:
                return [{"type": "text", "text": f"Location {location_name} not found in this multiworld"}]
            goal_region = goal_location.parent_region
            if not goal_region:
                return [{"type": "text", "text": f"Location {location_name} has no parent region"}]
        else:
            region_name, usable, _resp = get_intended_text(
                dest_name,
                [reg.name for reg in self.get_regions()],
            )
            if usable:
                goal_region = self.get_region(region_name)
            else:
                return [{"type": "text", "text": response}]

        in_logic = True
        glitched_state = state.copy()
        glitched_state.collect(self.create_item(self.glitches_item_name))
        if (goal_location and not goal_location.can_reach(state)) or (
            goal_region not in state.path and goal_region.name != self.origin_region_name
        ):
            in_logic = False

        if goal_location and not goal_location.can_reach(glitched_state):
            return [{"type": "text", "text": f"Location {goal_location.name} cannot be reached"}]
        if goal_region not in glitched_state.path and goal_region.name != self.origin_region_name:
            return [{"type": "text", "text": f"Region {goal_region.name} cannot be reached"}]

        messages: list[JSONMessagePart] = [
            {"type": "color", "color": "slateblue",
                "text": f"Start -> {self.origin_region_name}\n"},
        ]
        if goal_region.name != self.origin_region_name:
            path: list[Entrance] = []
            name, connection = state.path[goal_region] if in_logic else glitched_state.path[goal_region]
            while connection is not None:
                name, connection = connection
                if "->" in name or name.endswith(" Portal"):
                    path.append(self.get_entrance(name))

            path.reverse()
            for p in path:
                rule_json = rule_to_json(
                    p.access_rule, state, glitched_state, 1)
                messages.extend(
                    [
                        {"type": "entrance_name", "text": p.name,
                            "player": self.player},
                        {"type": "text", "text": "\n"},
                    ]
                )
                if len(rule_json) > 0:
                    messages.extend(
                        [
                            *rule_json,
                            {"type": "text", "text": "\n"},
                        ]
                    )

        if goal_location:
            rule_json = rule_to_json(
                goal_location.access_rule, state, glitched_state, 1)
            messages.extend(
                [
                    {"type": "text", "text": "-> "},
                    {
                        "type": "color",
                        "color": "green" if in_logic else "yellow",
                        "text": goal_location.name,
                    },
                ]
            )
            if len(rule_json) > 0:
                messages.extend(
                    [
                        {"type": "text", "text": "\n"},
                        *rule_json,
                    ]
                )

        return messages

    def explain_rule(self, dest_name: str, state: CollectionState, *_: Any, **__: Any) -> list[JSONMessagePart]:
        if not dest_name:
            return [{"type": "text", "text": "Enter a macro, location, region, item, or acronym to get an explanation"}]

        types_to_try = {
            "macro": self._explain_macro,
            "region": self._explain_region,
            "location": self._explain_location,
            "item": self._explain_item,
        }

        glitched_state = state.copy()
        glitched_state.collect(self.create_item(self.glitches_item_name))

        attempts = list(types_to_try.keys())
        parts = dest_name.split(maxsplit=1)
        if len(parts) == 2:
            first_word = parts[0].lower()
            for label in types_to_try.keys():
                if first_word == label:
                    attempts = [label]
                    break

        result = []
        usable = False
        best_guess = []
        max_confidence = 0
        confidence = 0
        for classification in attempts:
            result, usable, confidence = types_to_try[classification](
                dest_name, state, glitched_state)
            if usable:
                return result
            if confidence > max_confidence:
                best_guess = result
                max_confidence = confidence

        return best_guess

    def _explain_location(self, location_name: str, state: CollectionState, glitched_state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
        all_location_names = set(
            self.multiworld.regions.location_cache[self.player])
        guess, usable, response = get_intended_text(
            location_name, all_location_names)
        if not usable:
            picks = get_fuzzy_results(
                location_name, all_location_names, limit=1)
            confidence = picks[0][1]
            return [{"type": "text", "text": response}], False, confidence

        location_name = guess
        location = self.get_location(location_name)
        if location.can_reach(state):
            color = "green"
        elif location.can_reach(glitched_state):
            color = "yellow"
        else:
            color = "salmon"
        messages: list[JSONMessagePart] = [
            {"type": "text", "text": "Location "},
            {"type": "color", "color": color, "text": location_name},
        ]

        messages.extend(
            [
                {"type": "text", "text": "\nLogic: "},
                *rule_to_json(location.access_rule, state, glitched_state),
            ]
        )
        return messages, True, 100

    def _explain_region(self, region_name: str, state: CollectionState, glitched_state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
        all_region_names = set(
            self.multiworld.regions.region_cache[self.player])
        guess, usable, response = get_intended_text(
            region_name, all_region_names)
        if not usable:
            picks = get_fuzzy_results(region_name, all_region_names, limit=1)
            confidence = picks[0][1]
            return [{"type": "text", "text": response}], False, confidence

        region_name = guess
        region = self.get_region(region_name)
        if region.can_reach(state):
            color = "green"
        elif region.can_reach(glitched_state):
            color = "yellow"
        else:
            color = "salmon"
        messages: list[JSONMessagePart] = [
            {"type": "text", "text": "Region "},
            {"type": "color", "color": color, "text": region_name},
        ]
        if region.entrances:
            messages.append({"type": "text", "text": "\nEntrances:"})
            for entrance in region.entrances:
                rule_json = rule_to_json(
                    entrance.access_rule, state, glitched_state, 1)
                messages.extend(
                    [
                        {
                            "type": "text",
                            "text": f"\n  {entrance.parent_region.name if entrance.parent_region else entrance.name}",
                        },
                    ]
                )
                if len(rule_json) > 0:
                    messages.extend(
                        [
                            {"type": "text", "text": "\n"},
                            *rule_json,
                        ]
                    )
        return messages, True, 100

    def _explain_item(self, item_name: str, state: CollectionState, glitched_state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
        all_item_names = set(self.item_name_to_id.keys())
        guess, usable, response = get_intended_text(item_name, all_item_names)
        if not usable:
            picks = get_fuzzy_results(item_name, all_item_names, limit=1)
            confidence = picks[0][1]
            return [{"type": "text", "text": response}], False, confidence

        item_name = guess
        item_data = item_data_table[item_name]
        classification = (
            item_data.classification(self.options) if callable(
                item_data.classification) else item_data.classification
        )
        messages: list[JSONMessagePart] = [
            {"type": "text", "text": "Item "},
            {
                "type": "item_id",
                "flags": int(classification),
                "player": self.player,
                "text": str(self.item_name_to_id[item_name]),
            },
        ]
        count = state.count(item_name, self.player)
        messages.extend(
            [
                {"type": "text", "text": "\nCount: "},
                {"type": "color", "color": "green" if count else "salmon",
                    "text": str(count)},
            ]
        )
        return messages, True, 100

    def _explain_macro(self, macro_name: str, state: CollectionState, glitched_state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
        all_macro_names = set(self.rule_macros.keys())
        if len(all_macro_names) == 0:
            return [{"type": "text", "text": "No macros found!"}], False, 0

        guess, usable, response = get_intended_text(
            macro_name, all_macro_names)
        if not usable:
            picks = get_fuzzy_results(macro_name, all_macro_names, limit=1)
            confidence = picks[0][1]
            return [{"type": "text", "text": response}], False, confidence

        macro_name = guess
        macro = self.rule_macros[macro_name]
        result = evaluate_rule(macro, state, glitched_state)
        assert isinstance(macro, Macro.Resolved)
        messages: list[JSONMessagePart] = [
            {"type": "text", "text": "Macro "},
            {"type": "color", "color": get_logic_color(
                result), "text": macro.name},
        ]
        if macro.description:
            messages.append({"type": "text", "text": f"\n{macro.description}"})
        messages.extend(
            [
                {"type": "text", "text": "\nLogic: "},
                *rule_to_json(macro.child, state, glitched_state, 0),
            ]
        )
        return messages, True, 100
