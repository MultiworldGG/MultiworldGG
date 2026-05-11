# Path of Exile Archipelago - Changelog

## v2.0.0

### New Feature: Area Locations
- New option **Area visits as location checks** (`add_area_locations_to_location_pool`, default: on) — reaching zones counts as location checks
- 612 area entries added; towns/encampments skipped
- Area location IDs start at 42000 to avoid conflicts with base-item, level, and boss ID ranges
- Only areas in acts ≤ goal act are included
- `existing_char` preset has area locations disabled by default

### New Feature: YAML Generation
- `generate_poe_options_data.py` now outputs `options_data.json` to all three client locations simultaneously
- Location order in generated YAML now follows AP ID order (base items → level locations → bosses) instead of alphabetical

### Client
- Electron frontend extracted to separate repository: [Path-of-Exile-Archipelago-Client](https://github.com/stubob/Path-of-Exile-Archipelago-Client)
- Added as git submodule alongside `pathofexile_ap`
- Fixed deathlink
- Fixed Linux path separator
- Removed OS-level focus detection from `client.txt` output monitoring

### Internal
- `total_gear_upgrades` added to slot data
- `areaLocationsAsLocations` flag added to slot data
- `scrape_act_areas.py` added (scraper used to generate area location data)
