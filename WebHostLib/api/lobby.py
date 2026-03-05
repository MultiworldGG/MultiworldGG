import io
import json
import os
import re
import zipfile

import yaml
from datetime import datetime, timedelta
from uuid import UUID

from flask import request, session, jsonify, send_file
from markupsafe import Markup
from pony.orm import commit, count, select, flush

from Utils import tuplize_version, Version
from WebHostLib.api import api_endpoints
from WebHostLib.check import get_yaml_data, roll_options
from WebHostLib.models import (
    Lobby, LobbyPlayer, LobbyMessage, LobbyYaml, LobbyApworld, Room,
    LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_CLOSED,
    Generation, Seed, uuid4,
)
from WebHostLib import app, limiter

APWORLD_MAX_SIZE = 60 * 1024 * 1024  # 60 MB — leaves headroom under 64 MB global limit

def _safe_zip_name(name: str) -> str:
    """Replace characters that are problematic in ZIP entry names."""
    return re.sub(r'[^\w\s.()\-]', '_', name).strip() or "unnamed"


_NAME_TEMPLATE_RE = re.compile(r'\{(player|PLAYER|number|NUMBER)\}')


def _has_name_template(name: str) -> bool:
    """Return True if the name contains a generation-time placeholder.
    Such names are guaranteed unique after generation and must be excluded
    from duplicate-name checks."""
    return bool(_NAME_TEMPLATE_RE.search(name))


def _delete_apworld_file(apworld: LobbyApworld) -> None:
    """Delete the apworld file from the filesystem, ignoring errors.
    Also removes the lobby subdirectory if it is now empty."""
    path = apworld.storage_path
    try:
        os.unlink(path)
    except OSError:
        pass
    try:
        os.rmdir(os.path.dirname(path))
    except OSError:
        pass  # not empty or already gone


def _cleanup_yaml_apworld(yaml_record: LobbyYaml) -> None:
    """Delete apworld file + record for a YAML before deleting the YAML itself."""
    if yaml_record.apworld:
        _delete_apworld_file(yaml_record.apworld)
        yaml_record.apworld.delete()


def _extract_game_info(content) -> tuple[str, str, str | None]:
    """Parse YAML content (bytes or str) and return (player_name, game, requires_game_version_json).

    requires_game_version_json is a JSON-encoded dict like {"min": "1.2.3"} or {"max": "1.2.3"},
    representing the version constraint from the YAML's requires.game section for the detected game.
    """
    from Utils import parse_yamls
    try:
        if isinstance(content, str):
            content = content.encode('utf-8')
        for yaml_data in parse_yamls(content):
            if yaml_data is None:
                continue
            game = yaml_data.get('game', '') or ''
            name = yaml_data.get('name', '') or ''
            if isinstance(game, dict):
                game = next(iter(game.keys()), '')
            if isinstance(name, dict):
                name = next(iter(name.keys()), '')
            game = str(game).strip()
            name = str(name).strip()

            # Extract requires.game version constraint for this specific game
            requires_version = None
            requires = yaml_data.get('requires', {})
            if requires and isinstance(requires, dict):
                games_req = requires.get('game', {})
                if games_req and isinstance(games_req, dict) and game in games_req:
                    constraint = games_req[game]
                    if isinstance(constraint, str):
                        # A bare version string means "designed for this exact version"
                        requires_version = json.dumps({"exact": constraint})
                    elif isinstance(constraint, dict):
                        # Explicit min/max dict from the YAML
                        requires_version = json.dumps(constraint)

            return name, game, requires_version
    except Exception:
        pass
    return '', '', None


def _version_mismatch_direction(requires_json: str, server_version: Version) -> str | None:
    """Return 'newer' if the YAML needs a newer world than the server has,
    'older' if it needs an older one, or None if the constraint is satisfied."""
    try:
        constraint = json.loads(requires_json)
        if "exact" in constraint:
            exact_ver = tuplize_version(str(constraint["exact"]))
            if exact_ver > server_version:
                return "newer"
            if exact_ver < server_version:
                return "older"
        if "min" in constraint:
            if tuplize_version(str(constraint["min"])) > server_version:
                return "newer"
        if "max" in constraint:
            if tuplize_version(str(constraint["max"])) < server_version:
                return "older"
    except Exception:
        pass
    return None


def _required_version_label(requires_json: str) -> str:
    """Return a readable version string from a constraint JSON blob."""
    try:
        c = json.loads(requires_json)
        if "exact" in c:
            return str(c["exact"])
        if "min" in c:
            return f"{c['min']}+"
        if "max" in c:
            return f"≤{c['max']}"
    except Exception:
        pass
    return "?"


def _check_version_constraint(requires_json: str | None, server_version: Version) -> str | None:
    """Return a human-readable warning string if the stored requires constraint is violated, else None."""
    if not requires_json:
        return None
    try:
        constraint = json.loads(requires_json)
        if "exact" in constraint:
            exact_ver = tuplize_version(str(constraint["exact"]))
            if exact_ver > server_version:
                return (f"designed for v{constraint['exact']}, "
                        f"server has v{server_version.as_simple_string()}")
            if exact_ver < server_version:
                return (f"designed for v{constraint['exact']}, server has "
                        f"v{server_version.as_simple_string()} — consider regenerating your YAML "
                        f"from the player options page.")
        if "min" in constraint:
            min_ver = tuplize_version(str(constraint["min"]))
            if min_ver > server_version:
                return f"requires v{constraint['min']}+, server has v{server_version.as_simple_string()}"
        if "max" in constraint:
            max_ver = tuplize_version(str(constraint["max"]))
            if max_ver < server_version:
                return (f"requires ≤v{constraint['max']}, server has "
                        f"v{server_version.as_simple_string()} — consider regenerating your YAML "
                        f"from the player options page.")
    except Exception:
        pass
    return None


def _expire_lobby_if_needed(lobby: Lobby) -> None:
    if lobby.state in (LOBBY_OPEN, LOBBY_GENERATING):
        if datetime.utcnow() - lobby.last_activity > timedelta(minutes=lobby.timeout_minutes):
            lobby.state = LOBBY_CLOSED


def _get_player_in_lobby(lobby: Lobby) -> LobbyPlayer | None:
    return LobbyPlayer.get(lobby=lobby, session_id=session["_id"])


@api_endpoints.route('/lobby/<suuid:lobby>/ping', methods=['GET'])
def lobby_ping(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    old_state = lobby.state
    _expire_lobby_if_needed(lobby)
    if lobby.state != old_state:
        commit()

    latest_msg_id = select(max(m.id) for m in LobbyMessage if m.lobby == lobby).first() or 0
    version = f"{int(lobby.last_activity.timestamp() * 1000)}-{latest_msg_id}"

    return jsonify({"state": lobby.state, "version": version})


@api_endpoints.route('/lobby/<suuid:lobby>/status', methods=['GET'])
def lobby_status(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    old_state = lobby.state
    _expire_lobby_if_needed(lobby)
    if lobby.state != old_state:
        commit()

    after_message_id = request.args.get('after_message', 0, type=int)

    player_rows = select(
        p for p in LobbyPlayer if p.lobby == lobby
    ).order_by(LobbyPlayer.joined_at)[:]

    from worlds.AutoWorld import AutoWorldRegister
    yamls_by_player: dict[int, list] = {}
    yaml_player_map = select(
        (y.id, y.filename, y.yaml_player_name, y.yaml_game, y.player.id, y.is_custom, y.requires_game_version)
        for y in LobbyYaml if y.lobby == lobby
    ).order_by(lambda i, f, n, g, p, ic, rv: i)[:]

    apworlds_list = select(a for a in LobbyApworld if a.lobby == lobby)[:]
    apworld_by_yaml_id = {}
    apworld_by_game: dict[str, dict] = {}
    for a in apworlds_list:
        entry = {"game_name": a.game_name, "filename": a.original_filename,
                 "file_size": a.file_size, "world_version": a.world_version}
        apworld_by_yaml_id[a.yaml.id] = entry
        apworld_by_game.setdefault(a.game_name, entry)

    has_custom = False
    for y_id, y_filename, y_pname, y_game, p_id, y_is_custom, y_requires_version in yaml_player_map:
        if y_is_custom:
            has_custom = True
        elif y_id in apworld_by_yaml_id:
            # Standard YAML with an upgrade apworld uploaded — also requires local generation
            has_custom = True
        yaml_info = {"id": y_id, "filename": y_filename, "is_custom": y_is_custom}
        if y_pname:
            yaml_info["player_name"] = y_pname
        if y_game:
            yaml_info["game"] = y_game
        # Mark apworld as present if directly linked OR if any apworld for this game exists
        if y_id in apworld_by_yaml_id:
            yaml_info["apworld"] = apworld_by_yaml_id[y_id]
        elif y_is_custom and y_game and y_game in apworld_by_game:
            yaml_info["apworld"] = apworld_by_game[y_game]
        # For standard worlds, include server-side world version and check requires constraint
        if y_game and not y_is_custom and y_game in AutoWorldRegister.world_types:
            server_wv = AutoWorldRegister.world_types[y_game].world_version
            if server_wv != Version(0, 0, 0):
                yaml_info["server_world_version"] = server_wv.as_simple_string()
            warning = _check_version_constraint(y_requires_version, server_wv)
            if warning:
                yaml_info["version_warning"] = warning
            # Offer optional apworld upgrade if YAML needs a newer version and none uploaded yet
            if (lobby.allow_custom_apworlds and y_requires_version
                    and _version_mismatch_direction(y_requires_version, server_wv) == "newer"
                    and y_id not in apworld_by_yaml_id):
                yaml_info["version_upgrade_available"] = True
        yamls_by_player.setdefault(p_id, []).append(yaml_info)

    players = []
    for p in player_rows:
        players.append({
            "id": p.id,
            "name": p.player_name,
            "is_owner": p.session_id == lobby.owner,
            "is_ready": p.is_ready,
            "yamls": yamls_by_player.get(p.id, []),
        })

    messages = select(
        m for m in LobbyMessage
        if m.lobby == lobby and m.id > after_message_id
    ).order_by(LobbyMessage.id)[:200]

    message_list = [{
        "id": m.id,
        "sender": m.sender_name,
        "content": m.content,
        "time": m.sent_at.isoformat() + "Z",
        "system": m.player is None,
    } for m in messages]

    total_yamls = len(yaml_player_map)

    latest_msg_id = select(max(m.id) for m in LobbyMessage if m.lobby == lobby).first() or 0
    version = f"{int(lobby.last_activity.timestamp() * 1000)}-{latest_msg_id}"

    meta = json.loads(lobby.meta)
    server_opts = meta.get("server_options", {})
    gen_opts = meta.get("generator_options", {})

    result = {
        "state": lobby.state,
        "title": lobby.title,
        "version": version,
        "player_count": len(players),
        "ready_count": sum(1 for p in player_rows if p.is_ready),
        "players": players,
        "messages": message_list,
        "total_yamls": total_yamls,
        "max_yamls_per_player": lobby.max_yamls_per_player,
        "max_players": lobby.max_players,
        "timeout_minutes": lobby.timeout_minutes,
        "allow_custom_apworlds": lobby.allow_custom_apworlds,
        "has_custom": has_custom,
        "server_opts": server_opts,
        "gen_opts": gen_opts,
        "apworlds": [
            {"yaml_id": a.yaml.id, "game_name": a.game_name,
             "filename": a.original_filename, "file_size": a.file_size,
             "world_version": a.world_version}
            for a in apworlds_list
        ],
    }

    if lobby.state == LOBBY_DONE:
        from WebHostLib import to_url
        if lobby.seed:
            result["seed_id"] = to_url(lobby.seed.id)
        if lobby.room:
            result["room_id"] = to_url(lobby.room.id)
        session_id = session.get("_id")
        is_member = session_id and any(p.session_id == session_id for p in player_rows)
        if is_member:
            pw = server_opts.get("server_password")
            if pw:
                result["server_password"] = pw

    if lobby.state == LOBBY_GENERATING and lobby.generation_id:
        gen_id = lobby.generation_id
        seed = Seed.get(id=gen_id)
        if seed:
            if lobby.state == LOBBY_GENERATING:
                lobby.seed = seed
                room = Room(seed=seed, owner=lobby.owner, tracker=uuid4())
                lobby.room = room
                lobby.state = LOBBY_DONE
                lobby.generation_id = None
                LobbyMessage(
                    lobby=lobby,
                    player=None,
                    sender_name="System",
                    content="Seed generated! Room is ready.",
                )
                try:
                    commit()
                except Exception:
                    return jsonify(result)
            from WebHostLib import to_url
            result["state"] = LOBBY_DONE
            if lobby.seed:
                result["seed_id"] = to_url(lobby.seed.id)
            if lobby.room:
                result["room_id"] = to_url(lobby.room.id)
        else:
            gen = Generation.get(id=gen_id)
            if gen and gen.state == -1:  # STATE_ERROR
                gen_meta = json.loads(gen.meta)
                error = gen_meta.get("error", "Unknown error")
                lobby.state = LOBBY_OPEN
                lobby.generation_id = None
                LobbyMessage(
                    lobby=lobby,
                    player=None,
                    sender_name="System",
                    content=f"Generation failed: {error}",
                )
                commit()
                result["state"] = LOBBY_OPEN
            elif gen is None:
                lobby.state = LOBBY_OPEN
                lobby.generation_id = None
                LobbyMessage(
                    lobby=lobby,
                    player=None,
                    sender_name="System",
                    content="Generation failed unexpectedly. Please try again.",
                )
                commit()
                result["state"] = LOBBY_OPEN

    return jsonify(result)


@api_endpoints.route('/lobby/<suuid:lobby>/upload', methods=['POST'])
@limiter.limit("20 per minute")
def lobby_upload_yaml(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    _expire_lobby_if_needed(lobby)
    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Lobby is not accepting uploads"}), 400

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    current_count = len(player.yamls)
    if current_count >= lobby.max_yamls_per_player:
        return jsonify({"error": f"Maximum {lobby.max_yamls_per_player} YAML(s) per player"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    files = request.files.getlist('file')
    if not files:
        return jsonify({"error": "No file provided"}), 400 
    remaining = lobby.max_yamls_per_player - current_count
    if len(files) > remaining:
        return jsonify({"error": f"You can only upload {remaining} more YAML(s)"}), 400

    # Validate using existing pipeline
    options = get_yaml_data(files)
    if isinstance(options, (str, Markup)):
        return jsonify({"error": str(options)}), 400

    from worlds.AutoWorld import AutoWorldRegister
    standard_options: dict[str, bytes] = {}
    custom_info: dict[str, tuple[str, str]] = {}  # filename -> (player_name, game)
    upgrade_info: dict[str, tuple[str, str]] = {}  # filename -> (player_name, game) for version upgrades
    requires_versions: dict[str, str | None] = {}  # filename -> requires_game_version JSON
    for filename, content in options.items():
        player_name, game, requires_version = _extract_game_info(content)
        requires_versions[filename] = requires_version

        if game and game not in AutoWorldRegister.world_types:
            # Completely unknown game — always requires custom APWorld
            if not lobby.allow_custom_apworlds:
                return jsonify({
                    "error": f"Game '{game}' is not supported on this server. "
                             f"The lobby owner must enable custom APWorlds to upload this file."
                }), 400
            if not player_name:
                return jsonify({"error": f"Could not find player name in '{filename}'"}), 400
            custom_info[filename] = (player_name, game)

        elif game and requires_version:
            # Known game but YAML declares a version requirement — check it
            server_wv = AutoWorldRegister.world_types[game].world_version
            direction = _version_mismatch_direction(requires_version, server_wv)

            if direction == "newer":
                # YAML needs a newer world than the server has
                if not lobby.allow_custom_apworlds:
                    req_label = _required_version_label(requires_version)
                    return jsonify({
                        "error": f"'{filename}' requires {game} v{req_label} but the server has "
                                 f"v{server_wv.as_simple_string()}. The lobby owner must enable "
                                 f"custom APWorlds so you can upload the matching world."
                    }), 400
                # Custom APWorlds enabled: skip validation to avoid the version exception.
                # Store in upgrade_info so it can be saved without validation.
                # The upgrade prompt will be shown by the status endpoint.
                if not player_name:
                    return jsonify({"error": f"Could not find player name in '{filename}'"}), 400
                upgrade_info[filename] = (player_name, game)

            elif direction == "older":
                # YAML was built for an older world than the server has — accept it either way,
                # the version_warning in status will surface the mismatch to the user.
                standard_options[filename] = content

            else:
                # Constraint satisfied
                standard_options[filename] = content

        else:
            standard_options[filename] = content

    meta = json.loads(lobby.meta)
    plando_options = set(meta.get("plando_options", []))
    new_names: dict[str, str] = {}
    new_games: dict[str, str] = {}
    new_custom: dict[str, bool] = {}
    new_requires: dict[str, str | None] = {}

    if standard_options:
        results, rolled = roll_options(standard_options, plando_options)
        errors = {k: v for k, v in results.items() if isinstance(v, str)}
        if errors:
            return jsonify({"error": "; ".join(errors.values())}), 400
        for filename, rolled_opts in rolled.items():
            name = getattr(rolled_opts, 'name', None) or os.path.splitext(filename)[0]
            new_names[filename] = name
            new_games[filename] = getattr(rolled_opts, 'game', '')
            new_custom[filename] = False
            new_requires[filename] = requires_versions.get(filename)

    for filename, (player_name, game) in custom_info.items():
        new_names[filename] = player_name
        new_games[filename] = game
        new_custom[filename] = True
        new_requires[filename] = requires_versions.get(filename)

    for filename, (player_name, game) in upgrade_info.items():
        new_names[filename] = player_name
        new_games[filename] = game
        new_custom[filename] = False  # Not truly custom, just needs version upgrade
        new_requires[filename] = requires_versions.get(filename)

    # Check for duplicates within the uploaded batch
    seen_names: dict[str, str] = {}
    for filename, name in new_names.items():
        if _has_name_template(name):
            continue
        if name in seen_names:
            return jsonify({
                "error": f"Duplicate player name '{name}' in uploaded files: "
                         f"'{seen_names[name]}' and '{filename}'"
            }), 400
        seen_names[name] = filename

    # Check against existing YAMLs in the lobby
    existing_names = set(select(
        y.yaml_player_name for y in LobbyYaml
        if y.lobby == lobby and y.yaml_player_name is not None
    )[:])
    for filename, name in new_names.items():
        if _has_name_template(name):
            continue
        if name in existing_names:
            return jsonify({
                "error": f"Player name '{name}' (from '{filename}') is already used by another YAML in this lobby."
            }), 400

    uploaded = []
    version_warnings: list[str] = []
    for filename, content in options.items():
        if isinstance(content, str):
            content = content.encode('utf-8')
        game = new_games.get(filename, '')
        is_custom = new_custom.get(filename, False)
        requires_json = new_requires.get(filename)

        # Check requires.game constraint against server's world version
        if requires_json and game and not is_custom and game in AutoWorldRegister.world_types:
            server_wv = AutoWorldRegister.world_types[game].world_version
            warning = _check_version_constraint(requires_json, server_wv)
            if warning:
                version_warnings.append(f"'{new_names.get(filename, filename)}' ({game}): {warning}")

        yaml_record = LobbyYaml(
            lobby=lobby,
            player=player,
            filename=filename,
            yaml_player_name=new_names.get(filename),
            yaml_game=game,
            is_custom=is_custom,
            requires_game_version=requires_json,
            content=content,
        )
        commit()
        uploaded.append({
            "id": yaml_record.id,
            "filename": filename,
            "is_custom": is_custom,
        })

    yaml_summaries = [
        f"{new_names.get(fn, fn)} ({new_games.get(fn, '?')})" for fn in options
    ]
    player.is_ready = False
    LobbyMessage(
        lobby=lobby,
        player=None,
        sender_name="System",
        content=f"{player.player_name} uploaded {len(uploaded)} YAML(s): {', '.join(yaml_summaries)}.",
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    result: dict = {"uploaded": uploaded}
    if version_warnings:
        result["version_warnings"] = version_warnings
    return jsonify(result), 201


@api_endpoints.route('/lobby/<suuid:lobby>/yaml/<int:yaml_id>', methods=['GET'])
def lobby_download_yaml(lobby: UUID, yaml_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    yaml_record = LobbyYaml.get(id=yaml_id)
    if not yaml_record or yaml_record.lobby != lobby:
        return jsonify({"error": "YAML not found"}), 404

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "Permission denied"}), 403

    content = yaml_record.content
    if isinstance(content, str):
        content = content.encode("utf-8")

    return send_file(
        io.BytesIO(content),
        download_name=yaml_record.filename,
        as_attachment=True,
        mimetype="application/x-yaml",
    )


@api_endpoints.route('/lobby/<suuid:lobby>/yaml/<int:yaml_id>', methods=['DELETE'])
def lobby_delete_yaml(lobby: UUID, yaml_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Cannot modify YAMLs in current lobby state"}), 400

    yaml_record = LobbyYaml.get(id=yaml_id)
    if not yaml_record or yaml_record.lobby != lobby:
        return jsonify({"error": "YAML not found"}), 404

    player = _get_player_in_lobby(lobby)
    is_owner = lobby.owner == session["_id"]

    # Only the YAML owner or lobby owner can delete
    if not player or (yaml_record.player != player and not is_owner):
        return jsonify({"error": "Permission denied"}), 403

    filename = yaml_record.filename
    yaml_owner = yaml_record.player
    owner_name = yaml_owner.player_name
    _cleanup_yaml_apworld(yaml_record)
    yaml_record.delete()
    yaml_owner.is_ready = False

    LobbyMessage(
        lobby=lobby,
        player=None,
        sender_name="System",
        content=f"{owner_name}'s YAML '{filename}' was removed.",
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/message/<int:message_id>', methods=['DELETE'])
@limiter.limit("30 per minute")
def lobby_delete_message(lobby: UUID, message_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can delete messages"}), 403

    msg = LobbyMessage.get(id=message_id)
    if not msg or msg.lobby != lobby:
        return jsonify({"error": "Message not found"}), 404

    if msg.player is None:
        return jsonify({"error": "Cannot delete system messages"}), 400

    owner_player = _get_player_in_lobby(lobby)
    owner_name = owner_player.player_name if owner_player else "Host"

    msg.player = None
    msg.sender_name = "System"
    msg.content = f"Message deleted by {owner_name}."
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({"content": msg.content})


@api_endpoints.route('/lobby/<suuid:lobby>/chat', methods=['POST'])
def lobby_chat(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    content = data.get('message', '').strip()
    if not content:
        return jsonify({"error": "Empty message"}), 400
    if len(content) > 500:
        return jsonify({"error": "Message too long (max 500 characters)"}), 400

    msg = LobbyMessage(
        lobby=lobby,
        player=player,
        sender_name=player.player_name,
        content=content,
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({
        "id": msg.id,
        "sender": msg.sender_name,
        "content": msg.content,
        "time": msg.sent_at.isoformat() + "Z",
        "system": False,
    }), 201


@api_endpoints.route('/lobby/<suuid:lobby>/ready', methods=['POST'])
@limiter.limit("20 per minute")
def lobby_toggle_ready(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Lobby is not open"}), 400

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    if not player.is_ready and not select(y for y in LobbyYaml if y.lobby == lobby and y.player == player).exists():
        return jsonify({"error": "Upload at least one YAML before marking ready"}), 400

    player.is_ready = not player.is_ready
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({"is_ready": player.is_ready})


@api_endpoints.route('/lobby/<suuid:lobby>/generate', methods=['POST'])
def lobby_generate(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can generate"}), 403

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Lobby is not in a state to generate"}), 400

    # Block generation when custom YAMLs are present, or when any YAML has an upgrade apworld
    custom_yamls = select(y for y in LobbyYaml if y.lobby == lobby and y.is_custom)[:]
    upgrade_apworlds = select(a for a in LobbyApworld if a.lobby == lobby and not a.yaml.is_custom)[:]
    if custom_yamls or upgrade_apworlds:
        return jsonify({
            "error": "Cannot generate: lobby contains custom APWorld YAMLs. "
                     "Use 'Download Package' to generate locally, then upload the result."
        }), 400

    all_yamls = select(y for y in LobbyYaml if y.lobby == lobby).order_by(LobbyYaml.id)[:]
    if not all_yamls:
        return jsonify({"error": "No YAMLs uploaded yet"}), 400

    if len(all_yamls) > app.config["MAX_ROLL"]:
        return jsonify({
            "error": f"Too many YAMLs ({len(all_yamls)}). Maximum is {app.config['MAX_ROLL']}."
        }), 400

    options = {}
    for yaml_record in all_yamls:
        unique_key = f"{yaml_record.player.player_name}_{yaml_record.id}_{yaml_record.filename}"
        options[unique_key] = yaml_record.content

    # Validate all options together
    meta = json.loads(lobby.meta)
    plando_options = set(meta.get("plando_options", []))
    results, gen_options = roll_options(options, plando_options)

    errors = {k: v for k, v in results.items() if isinstance(v, str)}
    if errors:
        error_msg = "; ".join(errors.values())
        LobbyMessage(
            lobby=lobby, player=None, sender_name="System",
            content=f"Generation validation failed: {error_msg}",
        )
        commit()
        return jsonify({"error": error_msg}), 400

    lobby.state = LOBBY_GENERATING
    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content="Seed generation started...",
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    from pickle import PicklingError
    from Utils import restricted_dumps
    try:
        gen = Generation(
            options=restricted_dumps({name: vars(opts) for name, opts in gen_options.items()}),
            meta=json.dumps(meta),
            state=0,  # STATE_QUEUED
            owner=session["_id"],
        )
        commit()
        lobby.generation_id = gen.id
        commit()
    except PicklingError as e:
        lobby.state = LOBBY_OPEN
        lobby.generation_id = None
        LobbyMessage(
            lobby=lobby, player=None, sender_name="System",
            content=f"Generation failed: {e}",
        )
        commit()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "generating"}), 202


@api_endpoints.route('/lobby/<suuid:lobby>/settings', methods=['PATCH'])
def lobby_update_settings(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can update settings"}), 403

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Cannot change settings after generation has started"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    newly_enabled_custom_apworlds = False

    if "title" in data:
        title = str(data["title"]).strip()
        if not title or len(title) > 48:
            return jsonify({"error": "Title must be 1–48 characters"}), 400
        lobby.title = title

    if "allow_custom_apworlds" in data:
        if data["allow_custom_apworlds"] and not lobby.allow_custom_apworlds:
            lobby.allow_custom_apworlds = True
            newly_enabled_custom_apworlds = True
        elif not data["allow_custom_apworlds"] and lobby.allow_custom_apworlds:
            return jsonify({"error": "Custom APWorlds cannot be disabled once enabled."}), 400

    if "max_yamls_per_player" in data:
        try:
            new_max_yamls = max(1, min(int(data["max_yamls_per_player"]), 20))
            counts = select(
                (y.player.id, count(y))
                for y in LobbyYaml if y.lobby == lobby and y.player is not None
            )[:]
            max_currently_held = max((c for _, c in counts), default=0)
            if new_max_yamls < max_currently_held:
                return jsonify({"error": f"Cannot lower max YAMLs below {max_currently_held} — a player already has that many."}), 400
            lobby.max_yamls_per_player = new_max_yamls
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid max_yamls_per_player"}), 400

    if "max_players" in data:
        try:
            new_max = max(0, min(int(data["max_players"]), 100))
            if new_max > 0:
                current_count = count(p for p in LobbyPlayer if p.lobby == lobby)
                if new_max < current_count:
                    return jsonify({"error": f"Cannot set max players to {new_max} — lobby already has {current_count} players."}), 400
            lobby.max_players = new_max
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid max_players"}), 400

    if "timeout_minutes" in data:
        try:
            lobby.timeout_minutes = max(1, min(int(data["timeout_minutes"]), 2880))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid timeout_minutes"}), 400

    meta = json.loads(lobby.meta)
    server_opts = meta.get("server_options", {})
    gen_opts = meta.get("generator_options", {})

    _release  = {"auto", "goal", "auto-enabled", "enabled", "disabled"}
    _collect  = {"auto", "goal", "auto-enabled", "enabled", "disabled"}
    _remaining = {"goal", "enabled", "disabled"}
    _countdown = {"auto", "disabled", "enabled"}
    _hint_mode = {"default", "own", "all"}

    if data.get("release_mode") in _release:
        server_opts["release_mode"] = data["release_mode"]
    if data.get("collect_mode") in _collect:
        server_opts["collect_mode"] = data["collect_mode"]
    if data.get("remaining_mode") in _remaining:
        if lobby.race:
            server_opts["remaining_mode"] = "disabled"
        else:
            server_opts["remaining_mode"] = data["remaining_mode"]
    if data.get("countdown_mode") in _countdown:
        server_opts["countdown_mode"] = data["countdown_mode"]
    if data.get("hint_mode") in _hint_mode:
        server_opts["hint_mode"] = data["hint_mode"]

    if "hint_cost" in data:
        try:
            server_opts["hint_cost"] = max(0, min(int(data["hint_cost"]), 105))
        except (ValueError, TypeError):
            pass

    if "item_cheat" in data:
        server_opts["item_cheat"] = False if lobby.race else bool(data["item_cheat"])

    if "spoiler" in data:
        try:
            gen_opts["spoiler"] = 0 if lobby.race else max(0, min(int(data["spoiler"]), 3))
        except (ValueError, TypeError):
            pass

    meta["server_options"] = server_opts
    meta["generator_options"] = gen_opts
    lobby.meta = json.dumps(meta)
    lobby.last_activity = datetime.utcnow()

    LobbyMessage(
        lobby=lobby,
        player=None,
        sender_name="System",
        content=(
            "Lobby settings were updated by the host. Custom APWorlds have been enabled."
            if newly_enabled_custom_apworlds else
            "Lobby settings were updated by the host."
        ),
    )
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/leave', methods=['POST'])
def lobby_leave(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 400

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Cannot leave after generation has started"}), 400

    # Owner cannot leave (they should close the lobby instead)
    if lobby.owner == session["_id"]:
        return jsonify({"error": "The lobby owner cannot leave. Close the lobby instead."}), 400

    name = player.player_name
    for m in player.messages:
        m.player = None
    for y in list(player.yamls):
        _cleanup_yaml_apworld(y)
        y.delete()
    player.delete()

    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content=f"{name} left the lobby.",
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/kick/<int:player_id>', methods=['POST'])
def lobby_kick(lobby: UUID, player_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can kick players"}), 403

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Cannot kick players in current state"}), 400

    target = LobbyPlayer.get(id=player_id)
    if not target or target.lobby != lobby:
        return jsonify({"error": "Player not found"}), 404

    if target.session_id == lobby.owner:
        return jsonify({"error": "Cannot kick the lobby owner"}), 400

    name = target.player_name
    for m in target.messages:
        m.player = None
    for y in list(target.yamls):
        _cleanup_yaml_apworld(y)
        y.delete()
    target.delete()

    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content=f"{name} was kicked from the lobby.",
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/close', methods=['POST'])
def lobby_close(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can close the lobby"}), 403

    if lobby.state == LOBBY_CLOSED:
        return jsonify({"error": "Lobby is already closed"}), 400

    lobby.state = LOBBY_CLOSED
    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content="The lobby was closed by the host.",
    )
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/apworld/<int:yaml_id>', methods=['POST'])
@limiter.limit("5 per minute")
def lobby_upload_apworld(lobby: UUID, yaml_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if not lobby.allow_custom_apworlds:
        return jsonify({"error": "This lobby does not allow custom APWorlds"}), 400

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Lobby is not accepting uploads"}), 400

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    yaml_record = LobbyYaml.get(id=yaml_id)
    if not yaml_record or yaml_record.lobby != lobby:
        return jsonify({"error": "YAML not found"}), 404

    if yaml_record.player != player:
        return jsonify({"error": "You can only upload an APWorld for your own YAML"}), 403

    if not yaml_record.is_custom:
        # Also allow apworld uploads for standard worlds where the YAML requires a newer version
        from worlds.AutoWorld import AutoWorldRegister as _AWR
        is_version_upgrade = (
            yaml_record.requires_game_version
            and yaml_record.yaml_game
            and yaml_record.yaml_game in _AWR.world_types
            and _version_mismatch_direction(
                yaml_record.requires_game_version,
                _AWR.world_types[yaml_record.yaml_game].world_version
            ) == "newer"
        )
        if not is_version_upgrade:
            return jsonify({"error": "This YAML does not require a custom APWorld"}), 400

    if not yaml_record.apworld:
        existing = select(
            a for a in LobbyApworld
            if a.lobby == lobby
            and a.game_name == yaml_record.yaml_game
            and a.yaml != yaml_record
        ).first()
        if existing:
            return jsonify({
                "error": f"An APWorld for '{yaml_record.yaml_game}' was already uploaded "
                         f"by another player and applies to your YAML automatically."
            }), 400

    content_length = request.content_length
    if content_length and content_length > APWORLD_MAX_SIZE:
        return jsonify({"error": f"APWorld file too large (max {APWORLD_MAX_SIZE // (1024*1024)} MB)"}), 413

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    f = request.files['file']
    if not f.filename or not f.filename.endswith('.apworld'):
        return jsonify({"error": "File must be a .apworld file"}), 400

    apworld_data = f.read(APWORLD_MAX_SIZE + 1)
    if len(apworld_data) > APWORLD_MAX_SIZE:
        return jsonify({"error": f"APWorld file too large (max {APWORLD_MAX_SIZE // (1024*1024)} MB)"}), 413

    if not zipfile.is_zipfile(io.BytesIO(apworld_data)):
        return jsonify({"error": "File is not a valid .apworld (must be a ZIP archive)"}), 400

    world_version = None
    try:
        with zipfile.ZipFile(io.BytesIO(apworld_data)) as apzip:
            manifest_path = next(
                (n for n in apzip.namelist() if n == "archipelago.json" or n.endswith("/archipelago.json")),
                None,
            )
            if manifest_path:
                manifest = json.loads(apzip.read(manifest_path))
                wv = manifest.get("world_version")
                if wv is not None:
                    world_version = str(wv)
    except Exception:
        pass

    # Upgrade apworlds must declare a world_version so we can display and validate the upgrade
    if not yaml_record.is_custom and world_version is None:
        return jsonify({"error": "Upgrade APWorlds must have a world_version defined in archipelago.json"}), 400

    apworld_dir = os.path.abspath(os.path.join(app.config["LOBBY_APWORLD_PATH"], str(lobby.id)))
    os.makedirs(apworld_dir, exist_ok=True)
    storage_path = os.path.abspath(os.path.join(apworld_dir, f"{yaml_id}.apworld"))
    if not storage_path.startswith(apworld_dir + os.sep):
        return jsonify({"error": "Invalid storage path"}), 400

    if yaml_record.apworld:
        _delete_apworld_file(yaml_record.apworld)
        yaml_record.apworld.delete()

    with open(storage_path, 'wb') as out:
        out.write(apworld_data)

    LobbyApworld(
        lobby=lobby,
        yaml=yaml_record,
        game_name=yaml_record.yaml_game,
        original_filename=f.filename,
        storage_path=storage_path,
        file_size=len(apworld_data),
        world_version=world_version,
    )
    lobby.last_activity = datetime.utcnow()
    commit()

    return jsonify({"success": True, "file_size": len(apworld_data)}), 201


@api_endpoints.route('/lobby/<suuid:lobby>/download-package', methods=['GET'])
def lobby_download_package(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You must be in this lobby to download the package"}), 403

    yaml_rows = select(
        (y.id, y.yaml_player_name, y.yaml_game, y.filename, y.content, y.player.player_name)
        for y in LobbyYaml if y.lobby == lobby
    ).order_by(lambda i, n, g, f, c, p: i)[:]
    apworlds = select(a for a in LobbyApworld if a.lobby == lobby)[:]

    meta = json.loads(lobby.meta)
    server_opts = meta.get("server_options", {})
    gen_opts = meta.get("generator_options", {})
    plando_opts = meta.get("plando_options", [])

    host_yaml = yaml.dump({
        "server_options": {
            "hint_cost": server_opts.get("hint_cost", 10),
            "release_mode": server_opts.get("release_mode", "auto"),
            "collect_mode": server_opts.get("collect_mode", "auto"),
            "remaining_mode": server_opts.get("remaining_mode", "goal"),
            "countdown_mode": server_opts.get("countdown_mode", "auto"),
            "hint_mode": server_opts.get("hint_mode", "default"),
            "disable_item_cheat": not server_opts.get("item_cheat", True),
            "server_password": server_opts.get("server_password") or None,
        },
        "generator": {
            "player_files_path": "Players",
            "spoiler": gen_opts.get("spoiler", 3),
            "race": 1 if gen_opts.get("race") else 0,
            "plando_options": ", ".join(sorted(plando_opts)),
        },
    }, default_flow_style=False, allow_unicode=True)

    zip_buffer = io.BytesIO()
    seen_apworld_games: set[str] = set()

    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("host.yaml", host_yaml)

        seen_yaml_names: set[str] = set()
        for y_id, y_player_name, y_game, y_filename, y_content, y_lobby_player_name in yaml_rows:
            player_name = _safe_zip_name(y_player_name or os.path.splitext(y_filename)[0])
            game = _safe_zip_name(y_game or "unknown")
            entry_name = f"Players/{player_name}_{game}.yaml"
            if entry_name in seen_yaml_names:
                lobby_player_name = _safe_zip_name(y_lobby_player_name)
                entry_name = f"Players/{lobby_player_name}_{game}.yaml"
            if entry_name in seen_yaml_names:
                entry_name = f"Players/{lobby_player_name}_{game}_{y_id}.yaml"
            seen_yaml_names.add(entry_name)
            if isinstance(y_content, (memoryview, bytearray)):
                y_content = bytes(y_content)
            zf.writestr(entry_name, y_content)

        for a in apworlds:
            if a.game_name in seen_apworld_games:
                continue
            seen_apworld_games.add(a.game_name)
            safe_filename = _safe_zip_name(a.original_filename)
            try:
                with open(a.storage_path, 'rb') as apf:
                    zf.writestr(f"custom_worlds/{safe_filename}", apf.read())
            except OSError:
                pass

    zip_buffer.seek(0)
    safe_title = _safe_zip_name(lobby.title)
    return send_file(
        zip_buffer,
        download_name=f"{safe_title}.zip",
        as_attachment=True,
        mimetype="application/zip",
    )


@api_endpoints.route('/lobby/<suuid:lobby>/upload-game', methods=['POST'])
def lobby_upload_game(lobby: UUID):
    from WebHostLib.upload import process_multidata, allowed_generation, upload_zip_to_db

    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can upload the game"}), 403

    if lobby.state != LOBBY_OPEN:
        return jsonify({"error": "Lobby is not in a state to accept a game file"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    f = request.files['file']
    if not f.filename or not allowed_generation(f.filename):
        return jsonify({"error": "Invalid file type. Expected .archipelago, .mwgg, or .zip"}), 400

    meta = json.loads(lobby.meta)

    try:
        file_bytes = f.read()
        if zipfile.is_zipfile(io.BytesIO(file_bytes)):
            with zipfile.ZipFile(io.BytesIO(file_bytes), 'r') as zf:
                seed = upload_zip_to_db(zf, owner=lobby.owner, meta=meta)
        else:
            slots, multidata = process_multidata(file_bytes)
            seed = Seed(multidata=multidata, slots=slots, owner=lobby.owner, meta=json.dumps(meta))
            flush()
            for slot in slots:
                slot.seed = seed
    except Exception as e:
        return jsonify({"error": f"Failed to process game file: {e}"}), 400

    if not seed:
        return jsonify({"error": "No multidata found in the uploaded file."}), 400

    room = Room(seed=seed, owner=lobby.owner, tracker=uuid4())
    lobby.seed = seed
    lobby.room = room
    lobby.state = LOBBY_DONE
    lobby.last_activity = datetime.utcnow()
    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content="Game uploaded! Room is ready.",
    )
    commit()

    from WebHostLib import to_url
    return jsonify({
        "success": True,
        "room_id": to_url(room.id),
        "seed_id": to_url(seed.id),
    })
