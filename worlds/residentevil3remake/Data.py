import json
import os
import pkgutil

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    data_directory = "data"
    fname = os.path.join(data_directory, *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata


class Data:
    item_table = []
    location_table = []
    enemy_table = []
    region_table = []
    region_connections_table = []

    item_name_groups = {}

    @staticmethod
    def load_data(character=None, scenario=None):
        """
        This apworld only supports Jill / Scenario A.
        `character` and `scenario` are accepted only for backwards compatibility with existing seeds
        """

        fixed_character = "jill"
        fixed_scenario = "a"
        character = fixed_character
        scenario = fixed_scenario

        character_offsets = {"jill": 0}
        scenario_offsets = {"a": 0}
        assisted_offset = 200  # put all assisted-only locations after standard location spots
        hardcore_offset = 400   # put all hardcore-only locations after assisted location spots
        nightmare_offset = 600  # put all nightmare-only locations after hardcore location spots
        inferno_offset = 800    # put all inferno-only locations in the last 100 location spots

        # Difficulty-only suffixes:
        # Standard: none
        # Hardcore/Nightmare/Inferno: (H)/(N)/(I)
        scenario_suffix = ""
        scenario_suffix_assisted = " (A)"
        scenario_suffix_hardcore = " (H)"
        scenario_suffix_nightmare = " (N)"
        scenario_suffix_inferno = " (I)"

        location_start = item_start = 3300000000 + character_offsets[character] + scenario_offsets[scenario]
        enemy_start = location_start + 1000000000
        enemy_remaining = enemy_start + 500

        ###
        # Add standard regions
        ###

        new_region_table = load_data_file(character, scenario, 'regions.json')
        Data.region_table.extend([
            {
                **reg,
                'name': reg['name'] + scenario_suffix if reg['name'] != 'Menu' else reg['name'], # add the scenario abbreviation so they're unique
                'character': character,
                'scenario': scenario
            }
            for reg in new_region_table
        ])

        ###
        # Add assisted regions, if applicable
        ###

        assisted_locations_table = load_data_file(character, scenario, 'locations_assisted.json')
        assisted_regions = set([loc['region'] for loc in assisted_locations_table])

        if len(assisted_regions) > 0:
            Data.region_table.extend([
                {
                    'name': reg + scenario_suffix_assisted,
                    'character': character,
                    'scenario': scenario,
                    'zone_id': [regular['zone_id'] for regular in new_region_table if regular['name'] == reg][0]
                }
                for reg in assisted_regions
            ])

        ###
        # Add hardcore regions, if applicable
        ###

        hardcore_locations_table = load_data_file(character, scenario, 'locations_hardcore.json')
        hardcore_regions = set([loc['region'] for loc in hardcore_locations_table])

        if len(hardcore_regions) > 0:
            Data.region_table.extend([
                {
                    'name': reg + scenario_suffix_hardcore, # add the scenario abbreviation so they're unique
                    'character': character,
                    'scenario': scenario,
                    'zone_id': [regular['zone_id'] for regular in new_region_table if regular['name'] == reg][0]
                }
                for reg in hardcore_regions
            ])

        ###
        # Add nightmare regions, if applicable
        ###

        nightmare_locations_table = load_data_file(character, scenario, "locations_nightmare.json")
        nightmare_regions = set([loc["region"] for loc in nightmare_locations_table])

        if len(nightmare_regions) > 0:
            Data.region_table.extend([
                {
                    "name": reg + scenario_suffix_nightmare,
                    "character": character,
                    "scenario": scenario,
                    "zone_id": [regular["zone_id"] for regular in new_region_table if regular["name"] == reg][0]
                }
                for reg in nightmare_regions
            ])

        ###
        # Add inferno regions, if applicable
        ###

        inferno_locations_table = load_data_file(character, scenario, "locations_inferno.json")
        inferno_regions = set([loc["region"] for loc in inferno_locations_table])

        if len(inferno_regions) > 0:
            Data.region_table.extend([
                {
                    "name": reg + scenario_suffix_inferno,
                    "character": character,
                    "scenario": scenario,
                    "zone_id": [regular["zone_id"] for regular in new_region_table if regular["name"] == reg][0]
                }
                for reg in inferno_regions
            ])

        ###
        # Add standard region connections
        ###

        new_region_connections_table = load_data_file(character, scenario, "region_connections.json")
        Data.region_connections_table.extend([
            {
                **conn,
                "from": conn["from"] + scenario_suffix if conn["from"] != "Menu" else conn["from"],
                "to": conn["to"] + scenario_suffix if conn["to"] != "Menu" else conn["to"],
                "character": character,
                "scenario": scenario
            }
            for conn in new_region_connections_table
        ])

        ###
        # Add assisted region connections
        ###

        if len(assisted_regions) > 0:
            for conn in new_region_connections_table:
                if conn["from"] in assisted_regions or conn["to"] in assisted_regions:
                    suffix_from = scenario_suffix_assisted if conn["from"] in assisted_regions else scenario_suffix
                    suffix_to = scenario_suffix_assisted if conn["to"] in assisted_regions else scenario_suffix

                    Data.region_connections_table.append({
                        **conn,
                        "from": conn["from"] + suffix_from,
                        "to": conn["to"] + suffix_to,
                        "character": character,
                        "scenario": scenario
                    })

        ###
        # Add hardcore region connections
        ###

        if len(hardcore_regions) > 0:
            for conn in new_region_connections_table:
                if conn["from"] in hardcore_regions or conn["to"] in hardcore_regions:
                    suffix_from = scenario_suffix_hardcore if conn["from"] in hardcore_regions else scenario_suffix
                    suffix_to = scenario_suffix_hardcore if conn["to"] in hardcore_regions else scenario_suffix

                    Data.region_connections_table.append({
                        **conn,
                        "from": conn["from"] + suffix_from,
                        "to": conn["to"] + suffix_to,
                        "character": character,
                        "scenario": scenario
                    })

        ###
        # Add nightmare region connections
        ###

        if len(nightmare_regions) > 0:
            for conn in new_region_connections_table:
                if conn["from"] in nightmare_regions or conn["to"] in nightmare_regions:
                    suffix_from = scenario_suffix_nightmare if conn["from"] in nightmare_regions else scenario_suffix
                    suffix_to = scenario_suffix_nightmare if conn["to"] in nightmare_regions else scenario_suffix

                    Data.region_connections_table.append({
                        **conn,
                        "from": conn["from"] + suffix_from,
                        "to": conn["to"] + suffix_to,
                        "character": character,
                        "scenario": scenario
                    })

        ###
        # Add inferno region connections
        ###

        if len(inferno_regions) > 0:
            for conn in new_region_connections_table:
                if conn["from"] in inferno_regions or conn["to"] in inferno_regions:
                    suffix_from = scenario_suffix_inferno if conn["from"] in inferno_regions else scenario_suffix
                    suffix_to = scenario_suffix_inferno if conn["to"] in inferno_regions else scenario_suffix

                    Data.region_connections_table.append({
                        **conn,
                        "from": conn["from"] + suffix_from,
                        "to": conn["to"] + suffix_to,
                        "character": character,
                        "scenario": scenario
                    })

        ###
        # Add item table (shared across difficulties)
        ###

        new_item_table = load_data_file(character, "items.json")
        Data.item_table.extend([
            {
                **item,
                "id": item["id"] if item.get("id") else item_start + key
            }
            for key, item in enumerate(new_item_table)
        ])

        # For the items that have groups, add them to the item group names
        new_items_with_groups = [item for item in new_item_table if "groups" in item.keys()]

        for item_with_group in new_items_with_groups:
            item_name = item_with_group["name"]
            group_names = item_with_group["groups"]

            for group_name in group_names:
                if group_name not in Data.item_name_groups.keys():
                    Data.item_name_groups[group_name] = []
                Data.item_name_groups[group_name].append(item_name)

        ###
        # Add standard locations
        ###

        new_location_table = load_data_file(character, scenario, "locations.json")
        Data.location_table.extend([
            {
                **loc,
                "id": loc["id"] if loc.get("id") else location_start + key,
                "region": loc["region"] + scenario_suffix,  # standard: no suffix
                "character": character,
                "scenario": scenario,
                "difficulty": None
            }
            for key, loc in enumerate(new_location_table)
        ])

        ###
        # Add assisted locations
        ###

        assisted_location_table = load_data_file(character, scenario, "locations_assisted.json")
        if len(assisted_location_table) > 0:
            Data.location_table.extend([
                {
                    **loc,
                    "id": loc["id"] if loc.get("id") else location_start + key + assisted_offset,
                    "region": loc["region"] + scenario_suffix_assisted,
                    "character": character,
                    "scenario": scenario,
                    "difficulty": "assisted"
                }
                for key, loc in enumerate(assisted_location_table)
            ])

        ###
        # Add hardcore locations
        ###

        hardcore_location_table = load_data_file(character, scenario, "locations_hardcore.json")
        if len(hardcore_location_table) > 0:
            Data.location_table.extend([
                {
                    **loc,
                    "id": loc["id"] if loc.get("id") else location_start + key + hardcore_offset,
                    "region": loc["region"] + scenario_suffix_hardcore,
                    "character": character,
                    "scenario": scenario,
                    "difficulty": "hardcore"
                }
                for key, loc in enumerate(hardcore_location_table)
            ])

        ###
        # Add nightmare locations
        ###

        nightmare_location_table = load_data_file(character, scenario, "locations_nightmare.json")
        if len(nightmare_location_table) > 0:
            Data.location_table.extend([
                {
                    **loc,
                    "id": loc["id"] if loc.get("id") else location_start + key + nightmare_offset,
                    "region": loc["region"] + scenario_suffix_nightmare,
                    "character": character,
                    "scenario": scenario,
                    "difficulty": "nightmare"
                }
                for key, loc in enumerate(nightmare_location_table)
            ])

        ###
        # Add inferno locations
        ###

        inferno_location_table = load_data_file(character, scenario, "locations_inferno.json")
        if len(inferno_location_table) > 0:
            Data.location_table.extend([
                {
                    **loc,
                    "id": loc["id"] if loc.get("id") else location_start + key + inferno_offset,
                    "region": loc["region"] + scenario_suffix_inferno,
                    "character": character,
                    "scenario": scenario,
                    "difficulty": "inferno"
                }
                for key, loc in enumerate(inferno_location_table)
            ])

        ###
        # Add enemy table
        ###

        enemy_table = load_data_file(character, scenario, "enemies.json")

        Data.enemy_table.extend([
            {
                **enemy,
                "id": enemy["id"] if enemy.get("id") else enemy_start + key,
                "region": enemy["region"] + scenario_suffix,
                "original_item": "__Enemy Kill Drop Placeholder__",
                "difficulty": "none"
            }
            for key, enemy in enumerate(enemy_table) if not enemy.get("excluded", 0)
        ])

        ###
        # Hardcore enemy kills
        ###

        enemy_table = load_data_file(character, scenario, "enemies.json")

        Data.enemy_table.extend([
            {
                **enemy,
                "id": enemy_start + hardcore_offset + key,
                "region": enemy["region"] + scenario_suffix_hardcore,
                "original_item": "__Enemy Kill Drop Placeholder__",
                "difficulty": "hardcore"
            }
            for key, enemy in enumerate(enemy_table) if not enemy.get("excluded", 0)
        ])

        ###
        # Nightmare enemy kills
        ###

        enemy_table = load_data_file(character, scenario, "enemies_extended.json")

        Data.enemy_table.extend([
            {
                **enemy,
                "id": enemy_start + nightmare_offset + key,
                "region": enemy["region"] + scenario_suffix_nightmare,
                "original_item": "__Enemy Kill Drop Placeholder__",
                "difficulty": "nightmare"
            }
            for key, enemy in enumerate(enemy_table) if not enemy.get("excluded", 0)
        ])

        ###
        # Inferno enemy kills
        ###

        enemy_table = load_data_file(character, scenario, "enemies_extended.json")

        Data.enemy_table.extend([
            {
                **enemy,
                "id": enemy_start + inferno_offset + key,
                "region": enemy["region"] + scenario_suffix_inferno,
                "original_item": "__Enemy Kill Drop Placeholder__",
                "difficulty": "inferno"
            }
            for key, enemy in enumerate(enemy_table) if not enemy.get("excluded", 0)
        ])
