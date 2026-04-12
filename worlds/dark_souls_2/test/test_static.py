import unittest
from typing import List

from ..items import item_list
from ..locations import locations_by_region
from ..regions import region_list
from ..rules import connection_rules, location_rules

from BaseClasses import ItemClassification

class TestStatic(unittest.TestCase):

    # check for location names with same id but different location description (on same version)

    location_list = [ location for locations in locations_by_region.values() for location in locations]

    def test_no_duplicate_location_names(self):
        seen = set()
        duplicates = set()

        for location in self.location_list:
            if location.name in seen:
                duplicates.add(location.name)
            else:
                seen.add(location.name)

        if duplicates:
            self.fail(
                "\n" + "\n".join(
                    f"Location name '{name}' appears more than once"
                    for name in duplicates
                )
            )

    def test_all_location_original_items_exist(self):
        location_items = {location.original_item_name for location in self.location_list if not location.is_event}
        item_names = {item.name for item in item_list}
        wrong = {item for item in location_items if item not in item_names}

        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Item '{name}' does not exist in the list of items"
                    for name in wrong
                )
            )

    def test_all_location_regions_exist(self):
        location_regions = [region for region in locations_by_region]
        region_names = [region.name for region in region_list]
        extra = [region for region in location_regions if region not in region_names]

        if extra:
            self.fail(
                "\n" + "\n".join(
                    f"Region '{name}' from the location list does not exist in the list of regions"
                    for name in extra
                )
            )

    def test_all_regions_appear_in_location_list(self):
        location_regions = [region for region in locations_by_region]
        region_names = [region.name for region in region_list]
        missing = [region for region in region_names if region not in location_regions]

        if missing:
            self.fail(
                "\n" + "\n".join(
                    f"Region '{name}' does not appear in the location list"
                    for name in missing
                )
            )

    def test_connections_are_real_locations(self):
        region_names = {region.name for region in region_list}
        connection_names = {connection for region in region_list for connection in region.connections}
        wrong = {connection for connection in connection_names if connection not in region_names}

        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Connection '{name}' is not in the region list"
                    for name in wrong
                )
            )

    def test_connection_rule_regions_exist(self):
        region_names = {region.name for region in region_list}
        rule_regions = []
        for rule_data in connection_rules:
            self.assertTrue(" -> " in rule_data.spot, f"Connection rule spot \"{rule_data.spot}\" is invalid")
            rule_regions.extend(rule_data.spot.split(" -> "))
        wrong = {region for region in rule_regions if region not in region_names}

        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Region '{name}' from a connection rule is not in the region list"
                    for name in wrong
                )
            )

    def test_location_rule_locations_exist(self):
        location_names = {location.name for location in self.location_list}
        rule_locations = []
        for rule_data in location_rules:
            rule_locations.append(rule_data.spot)
        wrong = {location for location in rule_locations if location not in location_names}

        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Location '{name}' from a location rule is not in the location list"
                    for name in wrong
                )
            )

    def test_rule_items_exist(self):
        item_names = {item.name for item in item_list}
        event_items = { location.name for locations in locations_by_region.values() for location in locations if location.is_event }
        item_names = item_names | event_items
        
        rule_items = []
        for rule_data in connection_rules + location_rules:
            if callable(rule_data.rule):
                pass  # TODO
            if isinstance(rule_data.rule, str):
                rule_items.append(rule_data.rule)
            if isinstance(rule_data.rule, List):
                rule_items.extend(rule_data.rule)

        wrong = {item for item in rule_items if item not in item_names}

        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Item '{name}' from a rule is not in the item list"
                    for name in wrong
                )
            )

    def test_rule_items_are_progression(self):
        prog_items = {item.name for item in item_list if item.classification == ItemClassification.progression or ItemClassification == ItemClassification.progression_skip_balancing}
        event_items = { location.name for locations in locations_by_region.values() for location in locations if location.is_event }
        item_names = prog_items | event_items
        
        rule_items = []
        for rule_data in connection_rules + location_rules:
            if callable(rule_data.rule):
                pass  # TODO
            if isinstance(rule_data.rule, str):
                rule_items.append(rule_data.rule)
            if isinstance(rule_data.rule, List):
                rule_items.extend(rule_data.rule)
                
        wrong = {item for item in rule_items if item not in item_names}

        if wrong:
            self.fail(
                "\n" + "\n".join(
                    f"Item '{name}' from a rule is not a progression item"
                    for name in wrong
                )
            )

    def test_all_progression_items_have_rules(self):
        progression_items = [item.name for item in item_list if item.classification == ItemClassification.progression]
        rule_items = []

        for rule_data in connection_rules + location_rules:
            if callable(rule_data.rule):
                pass  # TODO
            if isinstance(rule_data.rule, str):
                rule_items.append(rule_data.rule)
            if isinstance(rule_data.rule, List):
                rule_items.extend(rule_data.rule)

        missing = {progression_item for progression_item in progression_items if progression_item not in rule_items}

        if missing:
            self.fail(
                "\n" + "\n".join(
                    f"Progression Item '{name}' is not currently part of a rule"
                    for name in missing
                )
            )

    # TODO check if connection in rule actually exists
