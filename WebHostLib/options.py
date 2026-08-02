import collections.abc
import json
import os
from textwrap import dedent
from typing import Dict, Union
from docutils.core import publish_parts

import yaml
from flask import redirect, render_template, request, Response, abort, session, jsonify
from schema import And, Optional as SchemaOptional, Or, Schema, Use
from urllib.parse import quote
from pony.orm import commit, select

import Options
from Utils import local_path, utcnow
from worlds.AutoWorld import AutoWorldRegister
from . import app, cache, limiter
from .generate import get_meta
from .misc import get_world_theme


def create() -> None:
    target_folder = local_path("WebHostLib", "static", "generated")
    yaml_folder = os.path.join(target_folder, "configs")

    Options.generate_yaml_templates(yaml_folder)


def get_option_counter_keys(option: type[Options.OptionCounter]) -> list[str]:
    """Return counter keys that can be safely offered as autocomplete suggestions."""
    keys: list[str] = []

    valid_keys = getattr(option, "valid_keys", ())
    keys.extend(sorted(key for key in valid_keys if isinstance(key, str)))

    schema = getattr(option, "schema", None)
    schema_definition = getattr(schema, "schema", getattr(schema, "_schema", schema))
    if isinstance(schema_definition, dict):
        for schema_key in schema_definition:
            key = getattr(schema_key, "schema", getattr(schema_key, "_schema", schema_key))
            if isinstance(key, str):
                keys.append(key)

    default = getattr(option, "default", {})
    if isinstance(default, dict):
        keys.extend(key for key in default if isinstance(key, str))

    return list(dict.fromkeys(keys))


def _get_scalar_schema_descriptor(schema_rule) -> dict | None:
    if isinstance(schema_rule, Schema):
        return _get_scalar_schema_descriptor(schema_rule._schema)

    if schema_rule is bool:
        return {"type": "boolean"}
    if schema_rule is int:
        return {"type": "integer"}
    if schema_rule is float:
        return {"type": "number"}
    if schema_rule is str:
        return {"type": "string"}

    if isinstance(schema_rule, Use):
        return _get_scalar_schema_descriptor(schema_rule._callable)

    if isinstance(schema_rule, Or):
        descriptors = [_get_scalar_schema_descriptor(rule) for rule in schema_rule._args]
        if any(descriptor is None for descriptor in descriptors):
            return None
        assert all(descriptor is not None for descriptor in descriptors)
        if len({descriptor["type"] for descriptor in descriptors}) != 1:
            return None
        if all("choices" in descriptor for descriptor in descriptors):
            choices = list(dict.fromkeys(
                choice
                for descriptor in descriptors
                for choice in descriptor["choices"]
            ))
            return {"type": descriptors[0]["type"], "choices": choices}
        return {"type": descriptors[0]["type"]}

    if isinstance(schema_rule, And):
        descriptors = [
            descriptor
            for rule in schema_rule._args
            if (descriptor := _get_scalar_schema_descriptor(rule)) is not None
        ]
        if not descriptors or len({descriptor["type"] for descriptor in descriptors}) != 1:
            return None
        choices = [descriptor["choices"] for descriptor in descriptors if "choices" in descriptor]
        return {
            "type": descriptors[0]["type"],
            **({"choices": choices[0]} if choices else {}),
        }

    if isinstance(schema_rule, bool):
        return {"type": "boolean", "choices": [schema_rule]}
    if type(schema_rule) is int:
        return {"type": "integer", "choices": [schema_rule]}
    if type(schema_rule) is float:
        return {"type": "number", "choices": [schema_rule]}
    if isinstance(schema_rule, str):
        return {"type": "string", "choices": [schema_rule]}

    return None


def _get_dict_key_schema(schema_rule) -> tuple[str, list[str]] | None:
    if isinstance(schema_rule, SchemaOptional):
        return _get_dict_key_schema(schema_rule._schema)
    if isinstance(schema_rule, Schema):
        return _get_dict_key_schema(schema_rule._schema)
    if schema_rule is str:
        return "additional", []
    if isinstance(schema_rule, str):
        return "fixed", [schema_rule]
    if isinstance(schema_rule, Or):
        if all(isinstance(rule, str) for rule in schema_rule._args):
            return "fixed", list(dict.fromkeys(schema_rule._args))
        return None
    if isinstance(schema_rule, And):
        key_descriptors = [
            descriptor
            for rule in schema_rule._args
            if (descriptor := _get_dict_key_schema(rule)) is not None
        ]
        if not key_descriptors:
            return None
        fixed_keys = [key for kind, keys in key_descriptors if kind == "fixed" for key in keys]
        if fixed_keys:
            return "fixed", list(dict.fromkeys(fixed_keys))
        return "additional", []
    return None


def get_option_dict_schema(option: type[Options.OptionDict]) -> dict | None:
    """Describe flat, scalar OptionDict schemas that the player-options UI can render safely."""
    for option_class in option.__mro__:
        if option_class is Options.OptionDict:
            break
        initializer = option_class.__dict__.get("__init__")
        if initializer is not None and initializer.__name__ != "meta__init__":
            return None

    schema = getattr(option, "schema", None)
    schema_definition = getattr(schema, "_schema", schema)
    if not isinstance(schema_definition, dict) or not schema_definition:
        return None

    fixed_keys: dict[str, dict] = {}
    additional_value = None
    for key_rule, value_rule in schema_definition.items():
        key_descriptor = _get_dict_key_schema(key_rule)
        value_descriptor = _get_scalar_schema_descriptor(value_rule)
        if key_descriptor is None or value_descriptor is None:
            return None

        key_type, keys = key_descriptor
        if key_type == "additional":
            if additional_value is not None and additional_value != value_descriptor:
                return None
            additional_value = value_descriptor
        else:
            for key in keys:
                fixed_keys[key] = value_descriptor

    default = getattr(option, "default", {})
    if not isinstance(default, dict):
        return None
    if any(key not in fixed_keys and additional_value is None for key in default):
        return None

    return {"keys": fixed_keys, "additional": additional_value}


def render_options_page(template: str, world_name: str, is_complex: bool = False) -> Union[Response, str]:
    world = AutoWorldRegister.world_types[world_name]
    if world.hidden or world.web.options_page is False or world_name in app.config["HIDDEN_WEBWORLDS"]:
        return redirect("games")
    visibility_flag = Options.Visibility.complex_ui if is_complex else Options.Visibility.simple_ui

    start_collapsed = {"Game Options": False}
    for group in world.web.option_groups:
        start_collapsed[group.name] = group.start_collapsed

    return render_template(
        template,
        world_name=world_name,
        world=world,
        option_groups=Options.get_option_groups(world, visibility_level=visibility_flag),
        start_collapsed=start_collapsed,
        issubclass=issubclass,
        Options=Options,
        option_counter_keys=get_option_counter_keys,
        option_dict_schema=get_option_dict_schema,
        theme=get_world_theme(world_name),
    )


def generate_game(options: Dict[str, Union[dict, str]]) -> Union[Response, str]:
    from .generate import start_generation
    return start_generation(options, get_meta({}))


def send_yaml(player_name: str, formatted_options: dict) -> Response:
    response = Response(yaml.dump(formatted_options, sort_keys=False))
    response.headers["Content-Type"] = "text/yaml"
    response.headers["Content-Disposition"] = f"attachment; filename={player_name}.yaml"
    return response


@app.template_filter("dedent")
def filter_dedent(text: str) -> str:
    return dedent(text).strip("\n ")

@app.template_filter('encodeURIComponent')
def encodeURIComponent_filter(s):
    return quote(str(s), safe='~()*!.\'')  

@app.template_filter("rst_to_html")
def filter_rst_to_html(text: str) -> str:
    """Converts reStructuredText (such as a Python docstring) to HTML."""
    if text.startswith(" ") or text.startswith("\t"):
        text = dedent(text)
    elif "\n" in text:
        lines = text.splitlines()
        text = lines[0] + "\n" + dedent("\n".join(lines[1:]))

    return publish_parts(text, writer_name='html', settings=None, settings_overrides={
        'raw_enable': False,
        'file_insertion_enabled': False,
        'output_encoding': 'unicode'
    })['body']


@app.template_test("ordered")
def test_ordered(obj):
    return isinstance(obj, collections.abc.Sequence)


@app.route("/games/<string:game>/option-presets", methods=["GET"])
@cache.cached()
def option_presets(game: str) -> Response:
    world = AutoWorldRegister.world_types[game]

    presets = {}
    for preset_name, preset in world.web.options_presets.items():
        presets[preset_name] = {}
        for preset_option_name, preset_option in preset.items():
            if preset_option == "random":
                presets[preset_name][preset_option_name] = preset_option
                continue

            option = world.options_dataclass.type_hints[preset_option_name].from_any(preset_option)
            if isinstance(option, Options.NamedRange) and isinstance(preset_option, str):
                assert preset_option in option.special_range_names, \
                    f"Invalid preset value '{preset_option}' for '{preset_option_name}' in '{preset_name}'. " \
                    f"Expected {option.special_range_names.keys()} or {option.range_start}-{option.range_end}."

                presets[preset_name][preset_option_name] = option.value
            elif isinstance(option, (Options.Range, Options.OptionSet, Options.OptionList, Options.OptionCounter)):
                presets[preset_name][preset_option_name] = option.value
            elif isinstance(preset_option, str):
                # Ensure the option value is valid for Choice and Toggle options
                assert option.name_lookup[option.value] == preset_option, \
                    f"Invalid option value '{preset_option}' for '{preset_option_name}' in preset '{preset_name}'. " \
                    f"Values must not be resolved to a different option via option.from_text (or an alias)."
                # Use the name of the option
                presets[preset_name][preset_option_name] = option.current_key
            else:
                # Use the name of the option
                presets[preset_name][preset_option_name] = option.current_key

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            from collections.abc import Set
            if isinstance(obj, Set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    json_data = json.dumps(presets, cls=SetEncoder)
    response = Response(json_data)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/weighted-options")
def weighted_options_old():
    return redirect("games", 301)


@app.route("/games/<string:game>/weighted-options")
@cache.cached()
def weighted_options(game: str):
    try:
        return render_options_page("weightedOptions/weightedOptions.html", game, is_complex=True)
    except KeyError:
        return abort(404)


@app.route("/games/<string:game>/generate-weighted-yaml", methods=["POST"])
def generate_weighted_yaml(game: str):
    if request.method == "POST":
        intent_generate = False
        options = {}

        for key, val in request.form.items():
            if val == "_ensure-empty-list":
                options[key] = {}
            elif "||" not in key:
                if len(str(val)) == 0:
                    continue

                options[key] = val
            else:
                if int(val) == 0:
                    continue

                [option, setting] = key.split("||")
                options.setdefault(option, {})[setting] = int(val)

        # Error checking
        if "name" not in options:
            return "Player name is required."

        # Remove POST data irrelevant to YAML
        if "intent-generate" in options:
            intent_generate = True
            del options["intent-generate"]
        if "intent-export" in options:
            del options["intent-export"]

        # Properly format YAML output
        player_name = options["name"]
        del options["name"]

        formatted_options = {
            "name": player_name,
            "game": game,
            "description": f"Generated by MultiworldGG for {game}",
            game: options,
        }

        if intent_generate:
            return generate_game({player_name: formatted_options})

        else:
            return send_yaml(player_name, formatted_options)


# Player options pages
@app.route("/games/<string:game>/player-options")
@cache.cached()
def player_options(game: str):
    try:
        return render_options_page("playerOptions/playerOptions.html", game, is_complex=False)
    except KeyError:
        return abort(404)


# Alias for player-options
@app.route("/games/<string:game>/player-settings")
def player_settings(game: str):
    return redirect(f"/games/{game}/player-options", code=301)


def _parse_player_options_form(game: str) -> tuple[str, dict, bool]:
    """Parse POST form data into (player_name, formatted_options, intent_generate).

    Raises ValueError on validation failure.
    """
    options = {}
    intent_generate = False

    for key, val in request.form.items(multi=True):
        if val == "_ensure-empty-list" and not key.endswith("||free-list"):
            options[key] = []
        elif key in options:
            if not isinstance(options[key], list):
                options[key] = [options[key]]
            options[key].append(val)
        else:
            options[key] = val

    free_lists: dict[str, list[str]] = {}
    free_counters: dict[str, dict[str, dict[str, str]]] = {}
    free_dicts: dict[str, dict[str, dict[str, str]]] = {}
    for key, val in options.copy().items():
        if key.endswith("||free-list-marker"):
            option_name = key.removesuffix("||free-list-marker")
            free_lists.setdefault(option_name, [])
            del options[key]
            continue

        if key.endswith("||free-list"):
            option_name = key.removesuffix("||free-list")
            values = val if isinstance(val, list) else [val]
            free_lists.setdefault(option_name, []).extend(value for value in values if value != "")
            del options[key]
            continue

        key_parts = key.rsplit("||", 2)
        if len(key_parts) == 2 and key_parts[-1] == "free-counter":
            free_counters.setdefault(key_parts[0], {})
            del options[key]
        elif len(key_parts) == 2 and key_parts[-1] == "free-dict":
            free_dicts.setdefault(key_parts[0], {})
            del options[key]
        elif len(key_parts) == 3 and key_parts[-2] in {"counter-key", "counter-value"}:
            option_name, field_type, row_id = key_parts
            field_name = "key" if field_type == "counter-key" else "value"
            free_counters.setdefault(option_name, {}).setdefault(row_id, {})[field_name] = val
            del options[key]
        elif len(key_parts) == 3 and (key_parts[-2] == "dict-key" or key_parts[-2].startswith("dict-value-")):
            option_name, field_type, row_id = key_parts
            row = free_dicts.setdefault(option_name, {}).setdefault(row_id, {})
            if field_type == "dict-key":
                row["key"] = val
            else:
                row["value"] = val
                row["type"] = field_type.removeprefix("dict-value-")
            del options[key]
        elif key_parts[-1] == "qty":
            if key_parts[0] not in options:
                options[key_parts[0]] = {}
            if val and val != "0":
                options[key_parts[0]][key_parts[1]] = int(val)
            del options[key]
        elif key_parts[-1].endswith("-custom"):
            if val:
                options[key_parts[-1][:-7]] = val
            del options[key]
        elif key_parts[-1].endswith("-range"):
            if options[key_parts[-1][:-6]] == "custom":
                options[key_parts[-1][:-6]] = val
            del options[key]

    options.update(free_lists)

    for option_name, rows in free_counters.items():
        counter = options[option_name] = {}
        for row in rows.values():
            entry_key = row.get("key", "").strip()
            entry_value = row.get("value", "")
            if entry_key and entry_value:
                value = int(entry_value)
                if value == 0:
                    counter.pop(entry_key, None)
                else:
                    counter[entry_key] = value

    for option_name, rows in free_dicts.items():
        option_dict = options[option_name] = {}
        for row in rows.values():
            entry_key = row.get("key", "").strip()
            entry_value = row.get("value")
            value_type = row.get("type")
            if not entry_key or entry_value is None:
                continue
            if value_type == "integer":
                if entry_value == "":
                    continue
                value = int(entry_value)
            elif value_type == "number":
                if entry_value == "":
                    continue
                value = float(entry_value)
            elif value_type == "boolean":
                if entry_value not in {"true", "false"}:
                    raise ValueError(f"Invalid boolean value for {option_name}: {entry_value}")
                value = entry_value == "true"
            elif value_type == "string":
                value = entry_value
            else:
                raise ValueError(f"Unsupported dictionary value type for {option_name}: {value_type}")
            option_dict[entry_key] = value

    for key, val in options.copy().items():
        if key.startswith("random-"):
            options[key.removeprefix("random-")] = "random"
            del options[key]

    if not options.get("name"):
        raise ValueError("Player name is required.")

    preset_name = 'default'
    if "intent-generate" in options:
        intent_generate = True
        del options["intent-generate"]
    if "intent-export" in options:
        del options["intent-export"]
    if "lobby-id" in options:
        del options["lobby-id"]
    if "game-options-preset" in options:
        preset_name = options["game-options-preset"]
        del options["game-options-preset"]

    player_name = options["name"]
    del options["name"]

    description = f"Generated by MultiworldGG for {game}"
    if preset_name != 'default' and preset_name != 'custom':
        description += f" using {preset_name} preset"

    formatted_options = {
        "name": player_name,
        "game": game,
        "description": description,
        game: options,
    }

    return player_name, formatted_options, intent_generate


# YAML generator for player-options
@app.route("/games/<string:game>/generate-yaml", methods=["POST"])
def generate_yaml(game: str):
    if request.method == "POST":
        try:
            player_name, formatted_options, intent_generate = _parse_player_options_form(game)
        except ValueError as e:
            return str(e)

        if intent_generate:
            return generate_game({player_name: formatted_options})
        else:
            return send_yaml(player_name, formatted_options)


@app.route("/games/<string:game>/add-to-lobby", methods=["POST"])
@limiter.limit("20 per minute")
def add_to_lobby(game: str):
    from uuid import UUID as _UUID
    from WebHostLib.models import (
        Lobby, LobbyPlayer, LobbyMessage, LobbyYaml,
        LOBBY_OPEN, LOBBY_LOCKED,
    )
    from WebHostLib.api.lobby import _expire_lobby_if_needed, _extract_game_info, _has_name_template
    from WebHostLib.check import roll_options
    from WebHostLib import to_url

    try:
        player_name, formatted_options, _ = _parse_player_options_form(game)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    lobby_id = request.form.get("lobby-id")
    if not lobby_id:
        return jsonify({"error": "No lobby selected"}), 400

    try:
        lobby_uuid = _UUID(lobby_id)
    except (ValueError, AttributeError):
        return jsonify({"error": "Invalid lobby ID"}), 400

    lobby = Lobby.get(id=lobby_uuid)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    _expire_lobby_if_needed(lobby)
    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
        return jsonify({"error": "Lobby is not accepting uploads"}), 400

    session_id = session.get("_id")
    if not session_id:
        return jsonify({"error": "No active session"}), 403

    player = LobbyPlayer.get(lobby=lobby, session_id=session_id)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    current_count = len(player.yamls)
    if current_count >= lobby.max_yamls_per_player:
        return jsonify({"error": f"Maximum {lobby.max_yamls_per_player} YAML(s) per player"}), 400

    yaml_content = yaml.dump(formatted_options, sort_keys=False).encode('utf-8')
    filename = f"{player_name}.yaml"

    yaml_player_name, yaml_game, requires_version = _extract_game_info(yaml_content)

    # Validate via roll_options, respecting lobby plando settings
    meta = json.loads(lobby.meta)
    plando_options = set(meta.get("plando_options", []))
    results, _ = roll_options({filename: yaml_content}, plando_options)
    errors = {k: v for k, v in results.items() if isinstance(v, str)}
    if errors:
        return jsonify({"error": "; ".join(errors.values())}), 400

    # Check for duplicate player names
    if not _has_name_template(yaml_player_name):
        existing_names = set(select(
            y.yaml_player_name for y in LobbyYaml
            if y.lobby == lobby and y.yaml_player_name is not None
        )[:])
        if yaml_player_name in existing_names:
            return jsonify({
                "error": f"Player name '{yaml_player_name}' is already used by another YAML in this lobby."
            }), 400

    LobbyYaml(
        lobby=lobby,
        player=player,
        filename=filename,
        yaml_player_name=yaml_player_name,
        yaml_game=yaml_game,
        is_custom=False,
        requires_game_version=requires_version,
        content=yaml_content,
    )
    commit()

    player.is_ready = False
    LobbyMessage(
        lobby=lobby,
        player=None,
        sender_name="System",
        content=f"{player.player_name} uploaded YAML: {yaml_player_name} ({yaml_game}).",
    )
    lobby.last_activity = utcnow()
    commit()

    return jsonify({"success": True, "lobby_url": f"/lobby/{to_url(lobby.id)}"})
