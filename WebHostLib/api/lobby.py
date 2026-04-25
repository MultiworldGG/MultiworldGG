import io
import hashlib
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

from Utils import tuplize_version, Version, utcnow
from WebHostLib.api import api_endpoints
from WebHostLib.check import get_yaml_data, roll_options
from WebHostLib.models import (
    Lobby, LobbyPlayer, LobbyMessage, LobbyYaml, LobbyApworld, LobbyApworldRequest, Room,
    LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_CLOSED, LOBBY_LOCKED,
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


def _delete_pending_apworld_file(storage_path: str) -> None:
    try:
        os.unlink(storage_path)
    except OSError:
        pass
    try:
        os.rmdir(os.path.dirname(storage_path))
    except OSError:
        pass


def _lobby_system_message(lobby: Lobby, content: str) -> None:
    LobbyMessage(
        lobby=lobby,
        player=None,
        sender_name="System",
        content=content,
    )


def _cleanup_apworld_request(request_record: LobbyApworldRequest) -> None:
    _delete_pending_apworld_file(request_record.storage_path)
    request_record.delete()


def _cancel_pending_requests_for_yaml(yaml_record: LobbyYaml, reason: str) -> int:
    requests = select(r for r in LobbyApworldRequest if r.yaml == yaml_record)[:]
    if not requests:
        return 0
    lobby = yaml_record.lobby
    requester_names = sorted({r.requester.player_name for r in requests})
    for req in requests:
        _cleanup_apworld_request(req)
    _lobby_system_message(
        lobby,
        f"Cancelled {len(requests)} pending APWorld request(s) for "
        f"{yaml_record.player.player_name}'s YAML '{yaml_record.filename}' "
        f"({', '.join(requester_names)}): {reason}",
    )
    return len(requests)


def _cancel_pending_requests_for_game(lobby: Lobby, game_name: str, reason: str) -> int:
    requests = select(
        r for r in LobbyApworldRequest
        if r.lobby == lobby and r.game_name == game_name
    )[:]
    if not requests:
        return 0
    for req in requests:
        _cleanup_apworld_request(req)
    _lobby_system_message(
        lobby,
        f"Cancelled {len(requests)} pending APWorld request(s) for {game_name}: {reason}",
    )
    return len(requests)


def _cancel_all_pending_requests(lobby: Lobby, reason: str) -> int:
    requests = select(r for r in LobbyApworldRequest if r.lobby == lobby)[:]
    if not requests:
        return 0
    for req in requests:
        _cleanup_apworld_request(req)
    _lobby_system_message(
        lobby,
        f"Cancelled {len(requests)} pending APWorld request(s): {reason}",
    )
    return len(requests)


def _server_world_version_for_game(game_name: str) -> Version | None:
    from worlds.AutoWorld import AutoWorldRegister
    if game_name in AutoWorldRegister.world_types:
        return AutoWorldRegister.world_types[game_name].world_version
    return None


def _yaml_requires_newer_world(requires_json: str | None, world_version: Version) -> bool:
    if not requires_json:
        return False
    return _version_mismatch_direction(requires_json, world_version) == "newer"


def _delete_yaml_record(yaml_record: LobbyYaml, reason: str | None = None) -> None:
    current = LobbyYaml.get(id=yaml_record.id)
    if not current:
        return
    yaml_record = current
    owner = yaml_record.player
    lobby = yaml_record.lobby
    filename = yaml_record.filename
    owner_name = owner.player_name
    _cleanup_yaml_apworld(yaml_record)
    yaml_record.delete()
    owner.is_ready = False
    if reason:
        _lobby_system_message(
            lobby,
            f"{owner_name}'s YAML '{filename}' was removed: {reason}",
        )


def _handle_removed_active_apworld(yaml_record: LobbyYaml) -> None:
    active_apworld = yaml_record.apworld
    if not active_apworld:
        return

    lobby = yaml_record.lobby
    game_name = active_apworld.game_name
    removed_version = active_apworld.world_version

    same_game_yamls = select(
        y for y in LobbyYaml
        if y.lobby == lobby
        and y.yaml_game == game_name
        and y.id != yaml_record.id
    ).order_by(LobbyYaml.id)[:]
    server_world_version = _server_world_version_for_game(game_name)
    removed_by_name = yaml_record.player.player_name if yaml_record.player else "a player"
    remaining_players = sorted({
        y.player.player_name for y in same_game_yamls if y.player
    })

    _delete_apworld_file(active_apworld)
    active_apworld.delete()

    _cancel_pending_requests_for_game(
        lobby,
        game_name,
        "active APWorld changed",
    )

    if server_world_version is None:
        if len(remaining_players) == 1:
            _lobby_system_message(
                lobby,
                f"{remaining_players[0]}: the APWorld that replaced yours was removed "
                f"after {removed_by_name}'s YAML was deleted. You may upload another APWorld.",
            )
        elif remaining_players:
            _lobby_system_message(
                lobby,
                f"Custom APWorld for '{game_name}' was removed after {removed_by_name}'s YAML was deleted. "
                f"Players using this game can upload a replacement APWorld: {', '.join(remaining_players)}.",
            )
        else:
            _lobby_system_message(
                lobby,
                f"Custom APWorld for '{game_name}' was removed after {removed_by_name}'s YAML was deleted.",
            )
        return

    deleted_count = 0
    for y in list(same_game_yamls):
        if _yaml_requires_newer_world(y.requires_game_version, server_world_version):
            _delete_yaml_record(
                y,
                f"incompatible with server {game_name} world version "
                f"v{server_world_version.as_simple_string()}",
            )
            deleted_count += 1

    old_version_label = f"v{removed_version}" if removed_version else "custom"
    new_version_label = f"v{server_world_version.as_simple_string()}"
    summary = (
        f"APWorld for '{game_name}' reverted from {old_version_label} "
        f"to server {new_version_label}."
    )
    if deleted_count:
        summary += f" Removed {deleted_count} incompatible YAML(s)."
    _lobby_system_message(lobby, summary)
    if len(remaining_players) == 1:
        _lobby_system_message(
            lobby,
            f"{remaining_players[0]}: the APWorld that replaced yours was removed "
            f"after {removed_by_name}'s YAML was deleted. You can upload your APWorld again.",
        )


def _cleanup_yaml_apworld(yaml_record: LobbyYaml) -> None:
    """Delete dependent APWorld/APWorld-request data for a YAML before deleting the YAML itself."""
    _cancel_pending_requests_for_yaml(yaml_record, "requester YAML was removed")
    if yaml_record.apworld:
        _handle_removed_active_apworld(yaml_record)


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


def _split_yaml_documents(filename: str, content: bytes) -> dict[str, bytes]:
    """Split a multi-document YAML file into individual {filename: bytes} entries.

    If the file contains only one document, returns {filename: content} unchanged.
    For multi-document files (separated by '---' lines), returns one entry per
    document named '{base}_1{ext}', '{base}_2{ext}', etc.
    """
    from Utils import parse_yamls
    try:
        doc_count = sum(1 for _ in parse_yamls(content))
    except Exception:
        return {filename: content}

    if doc_count <= 1:
        return {filename: content}

    # Split the raw text on '---' document-separator lines to preserve formatting.
    text = content.decode('utf-8-sig', errors='replace')
    raw_parts = re.split(r'(?m)^---[ \t]*(?:\r?\n|$)', text)
    doc_texts = [p.strip() for p in raw_parts if p.strip()]

    # Sanity-check: if the regex split count doesn't match the parser's count,
    # fall back to re-dumping the parsed documents (loses comments/formatting).
    if len(doc_texts) != doc_count:
        from Utils import parse_yamls as _py
        doc_texts = [yaml.dump(d, allow_unicode=True) for d in _py(content) if d is not None]

    base, ext = os.path.splitext(filename)
    if not ext:
        ext = '.yaml'
    return {
        f"{base}_{i}{ext}": doc.encode('utf-8')
        for i, doc in enumerate(doc_texts, 1)
    }


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


def _manual_game_segment(game_name: str) -> str:
    """'Manual_GameName_Player' -> 'GameName', 'Manual_GameName' -> 'GameName'"""
    if not game_name.startswith("Manual_"):
        return ""
    rest = game_name[len("Manual_"):]
    return rest.split("_")[0]


def _is_manual_apworld(original_filename: str, apworld_data: bytes) -> bool:
    if not os.path.basename(original_filename).lower().startswith("manual_"):
        return False
    try:
        with zipfile.ZipFile(io.BytesIO(apworld_data)) as apzip:
            return any(
                n.lower().startswith("manual_") and n.lower().endswith("/game.py")
                for n in apzip.namelist()
            )
    except Exception:
        return False


def _parse_apworld_upload(apworld_data: bytes, original_filename: str = "") -> tuple[str, str | None]:
    if not zipfile.is_zipfile(io.BytesIO(apworld_data)):
        raise ValueError("File is not a valid .apworld (must be a ZIP archive)")

    with zipfile.ZipFile(io.BytesIO(apworld_data)) as apzip:
        names = apzip.namelist()
        manifest_path = next(
            (n for n in names if n == "archipelago.json" or n.endswith("/archipelago.json")),
            None,
        )
        if not manifest_path:
            if os.path.basename(original_filename).lower().startswith("manual_"):
                game_py_path = next(
                    (n for n in names if n.lower().startswith("manual_") and n.lower().endswith("/game.py")),
                    None,
                )
                if game_py_path:
                    module_prefix = game_py_path[:game_py_path.lower().index("/game.py")]
                    data_game_path = next(
                        (n for n in names if n.lower() == f"{module_prefix.lower()}/data/game.json"),
                        None,
                    )
                    if data_game_path:
                        try:
                            data_game = json.loads(apzip.read(data_game_path).decode("utf-8", errors="replace"))
                            game = str(data_game.get("game", "")).strip() if isinstance(data_game, dict) else str(data_game).strip()
                            if game:
                                return f"Manual_{game}", None
                        except Exception:
                            pass
            raise ValueError("APWorld must contain archipelago.json manifest")

        try:
            manifest = json.loads(apzip.read(manifest_path))
        except Exception as exc:
            raise ValueError("archipelago.json is not valid JSON") from exc

    if not isinstance(manifest, dict):
        raise ValueError("archipelago.json must contain a JSON object")

    game_name = str(manifest.get("game", "")).strip()
    if not game_name:
        raise ValueError("archipelago.json must include a non-empty 'game' field")

    world_version_value = manifest.get("world_version")
    world_version = None if world_version_value is None else str(world_version_value).strip()
    if world_version == "":
        world_version = None

    return game_name, world_version


def _active_apworld_for_game(lobby: Lobby, game_name: str) -> LobbyApworld | None:
    return select(
        a for a in LobbyApworld
        if a.lobby == lobby and a.game_name == game_name
    ).order_by(lambda a: a.id).first()


def _apworld_lobby_dir(lobby: Lobby) -> str:
    return os.path.abspath(os.path.join(app.config["LOBBY_APWORLD_PATH"], str(lobby.id)))


def _preview_apworld_dir(lobby: Lobby) -> str:
    return os.path.join(_apworld_lobby_dir(lobby), "preview")


def _safe_storage_path(base_dir: str, filename: str) -> str:
    os.makedirs(base_dir, exist_ok=True)
    storage_path = os.path.abspath(os.path.join(base_dir, filename))
    if not storage_path.startswith(base_dir + os.sep):
        raise ValueError("Invalid storage path")
    return storage_path


def _cleanup_preview_apworld(lobby: Lobby, preview_token: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{32}", preview_token):
        return
    preview_dir = _preview_apworld_dir(lobby)
    apworld_path = _safe_storage_path(preview_dir, f"{preview_token}.apworld")
    meta_path = _safe_storage_path(preview_dir, f"{preview_token}.json")
    for path in (apworld_path, meta_path):
        try:
            os.unlink(path)
        except OSError:
            pass


def _store_preview_apworld(
    lobby: Lobby,
    yaml_record: LobbyYaml,
    session_id: UUID,
    original_filename: str,
    apworld_data: bytes,
) -> str:
    preview_dir = _preview_apworld_dir(lobby)
    preview_token = uuid4().hex
    apworld_path = _safe_storage_path(preview_dir, f"{preview_token}.apworld")
    meta_path = _safe_storage_path(preview_dir, f"{preview_token}.json")
    with open(apworld_path, "wb") as out:
        out.write(apworld_data)
    with open(meta_path, "w", encoding="utf-8") as out:
        json.dump({
            "yaml_id": yaml_record.id,
            "session_id": str(session_id),
            "filename": original_filename,
        }, out, separators=(",", ":"))
    return preview_token


def _load_preview_apworld(
    lobby: Lobby,
    yaml_record: LobbyYaml,
    session_id: UUID,
    preview_token: str,
) -> tuple[bytes, str]:
    if not re.fullmatch(r"[0-9a-f]{32}", preview_token):
        raise ValueError("Invalid preview_token")

    preview_dir = _preview_apworld_dir(lobby)
    apworld_path = _safe_storage_path(preview_dir, f"{preview_token}.apworld")
    meta_path = _safe_storage_path(preview_dir, f"{preview_token}.json")
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except OSError as exc:
        raise ValueError("preview_token not found or expired") from exc
    except json.JSONDecodeError as exc:
        raise ValueError("preview_token metadata is invalid") from exc

    if not isinstance(meta, dict):
        raise ValueError("preview_token metadata is invalid")
    if meta.get("yaml_id") != yaml_record.id:
        raise PermissionError("preview_token does not match this YAML")
    if str(meta.get("session_id", "")) != str(session_id):
        raise PermissionError("preview_token does not belong to this session")

    try:
        with open(apworld_path, "rb") as f:
            apworld_data = f.read(APWORLD_MAX_SIZE + 1)
    except OSError as exc:
        raise ValueError("preview_token file is missing") from exc
    if len(apworld_data) > APWORLD_MAX_SIZE:
        raise ValueError(f"APWorld file too large (max {APWORLD_MAX_SIZE // (1024*1024)} MB)")

    original_filename = str(meta.get("filename") or f"{yaml_record.yaml_game or 'world'}.apworld")
    return apworld_data, original_filename


def _build_apworld_impact_preview(
    lobby: Lobby,
    yaml_record: LobbyYaml,
    world_version: str | None,
) -> tuple[dict, str, Version | None]:
    game_name = yaml_record.yaml_game or ""
    same_game_yamls = select(
        y for y in LobbyYaml
        if y.lobby == lobby and y.yaml_game == game_name
    ).order_by(LobbyYaml.id)[:]

    parsed_world_version = None
    if world_version is not None:
        try:
            parsed_world_version = tuplize_version(world_version)
        except Exception as exc:
            raise ValueError(f"Invalid world_version '{world_version}' in archipelago.json") from exc

    active_apworld = _active_apworld_for_game(lobby, game_name)
    server_world_version = _server_world_version_for_game(game_name)
    if active_apworld:
        active_source = "custom"
        active_world_version = active_apworld.world_version
    elif server_world_version is not None:
        active_source = "server"
        active_world_version = server_world_version.as_simple_string()
    else:
        active_source = "none"
        active_world_version = None

    other_player_yaml_ids = [
        y.id for y in same_game_yamls
        if y.player != yaml_record.player
    ]
    all_impacted_players = sorted({
        y.player.player_name
        for y in same_game_yamls
    })

    unverifiable_yaml_ids: list[int] = []
    would_delete_yamls: list[dict] = []
    would_delete_yaml_ids: list[int] = []
    if parsed_world_version is None:
        unverifiable_yaml_ids = [y.id for y in same_game_yamls if y.requires_game_version]
    else:
        for y in same_game_yamls:
            if _yaml_requires_newer_world(y.requires_game_version, parsed_world_version):
                would_delete_yaml_ids.append(y.id)
                would_delete_yamls.append({
                    "yaml_id": y.id,
                    "player_name": y.player.player_name,
                    "filename": y.filename,
                    "slot_name": y.yaml_player_name,
                    "required_version": _required_version_label(y.requires_game_version)
                    if y.requires_game_version else None,
                })

    preview = {
        "game_name": game_name,
        "target_yaml_id": yaml_record.id,
        "candidate_world_version": world_version,
        "active_source": active_source,
        "active_world_version": active_world_version,
        "affects_other_players": bool(other_player_yaml_ids),
        "impacted_players": all_impacted_players,
        "impacted_player_count": len(all_impacted_players),
        "impacted_yaml_ids": [y.id for y in same_game_yamls],
        "same_game_yaml_ids": [y.id for y in same_game_yamls],
        "would_delete_yaml_ids": would_delete_yaml_ids,
        "would_delete_yamls": would_delete_yamls,
        "unverifiable_yaml_ids": unverifiable_yaml_ids,
    }

    hash_payload = {
        "target_yaml_id": yaml_record.id,
        "game_name": game_name,
        "candidate_world_version": world_version,
        "active_apworld_id": active_apworld.id if active_apworld else None,
        "active_source": active_source,
        "same_game_yamls": [
            {
                "id": y.id,
                "player_id": y.player.id,
                "requires_game_version": y.requires_game_version,
            }
            for y in same_game_yamls
        ],
    }
    impact_hash = hashlib.sha256(
        json.dumps(hash_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return preview, impact_hash, parsed_world_version


def _replace_active_apworld(
    lobby: Lobby,
    yaml_record: LobbyYaml,
    original_filename: str,
    apworld_data: bytes,
    world_version: str | None,
    preview: dict,
) -> list[int]:
    game_name = yaml_record.yaml_game or ""
    apworld_dir = _apworld_lobby_dir(lobby)
    storage_path = _safe_storage_path(apworld_dir, f"{yaml_record.id}.apworld")

    existing_apworlds = select(
        a for a in LobbyApworld
        if a.lobby == lobby and a.game_name == game_name
    )[:]
    for existing in existing_apworlds:
        _delete_apworld_file(existing)
        existing.delete()

    with open(storage_path, "wb") as out:
        out.write(apworld_data)

    LobbyApworld(
        lobby=lobby,
        yaml=yaml_record,
        game_name=game_name,
        original_filename=original_filename,
        storage_path=storage_path,
        file_size=len(apworld_data),
        world_version=world_version,
    )

    deleted_yaml_ids: list[int] = []
    for victim_yaml_id in list(preview.get("would_delete_yaml_ids", [])):
        if victim_yaml_id == yaml_record.id:
            continue
        victim = LobbyYaml.get(id=victim_yaml_id)
        if victim and victim.lobby == lobby and victim.yaml_game == game_name:
            _delete_yaml_record(
                victim,
                f"incompatible with APWorld v{world_version}" if world_version else
                "incompatible with newly applied APWorld",
            )
            deleted_yaml_ids.append(victim_yaml_id)

    return deleted_yaml_ids


def _create_pending_apworld_request(
    lobby: Lobby,
    yaml_record: LobbyYaml,
    player: LobbyPlayer,
    original_filename: str,
    apworld_data: bytes,
    world_version: str | None,
) -> LobbyApworldRequest:
    pending_dir = os.path.join(_apworld_lobby_dir(lobby), "pending")
    temp_path = _safe_storage_path(pending_dir, f"tmp_{uuid4().hex}.apworld")
    with open(temp_path, "wb") as out:
        out.write(apworld_data)

    request_record = LobbyApworldRequest(
        lobby=lobby,
        yaml=yaml_record,
        requester=player,
        game_name=yaml_record.yaml_game or "",
        original_filename=original_filename,
        storage_path=temp_path,
        file_size=len(apworld_data),
        world_version=world_version,
    )
    flush()

    final_path = _safe_storage_path(pending_dir, f"{request_record.id}.apworld")
    if final_path != temp_path:
        os.replace(temp_path, final_path)
    request_record.storage_path = final_path
    return request_record


def _read_pending_apworld_data(request_record: LobbyApworldRequest) -> bytes:
    with open(request_record.storage_path, "rb") as f:
        return f.read()


def _serialize_apworld_request(request_record: LobbyApworldRequest) -> dict:
    has_file = os.path.exists(request_record.storage_path)
    try:
        preview, impact_hash, _ = _build_apworld_impact_preview(
            request_record.lobby,
            request_record.yaml,
            request_record.world_version,
        )
    except Exception:
        preview = {
            "game_name": request_record.game_name,
            "target_yaml_id": request_record.yaml.id,
            "candidate_world_version": request_record.world_version,
            "affects_other_players": False,
            "impacted_players": [],
            "impacted_player_count": 0,
            "impacted_yaml_ids": [],
            "would_delete_yaml_ids": [],
            "would_delete_yamls": [],
            "unverifiable_yaml_ids": [],
        }
        impact_hash = ""

    return {
        "id": request_record.id,
        "yaml_id": request_record.yaml.id,
        "game_name": request_record.game_name,
        "requester_name": request_record.requester.player_name,
        "filename": request_record.original_filename,
        "file_size": request_record.file_size,
        "world_version": request_record.world_version,
        "submitted_at": request_record.submitted_at.isoformat() + "Z",
        "impact_preview": preview,
        "impact_hash": impact_hash,
        "has_file": has_file,
    }


def _expire_lobby_if_needed(lobby: Lobby) -> None:
    if lobby.state in (LOBBY_OPEN, LOBBY_LOCKED, LOBBY_GENERATING):
        if utcnow() - lobby.last_activity > timedelta(minutes=lobby.timeout_minutes):
            _cancel_all_pending_requests(lobby, "lobby expired")
            lobby.state = LOBBY_CLOSED


def _get_player_in_lobby(lobby: Lobby) -> LobbyPlayer | None:
    return LobbyPlayer.get(lobby=lobby, session_id=session["_id"])


@api_endpoints.route('/lobbies/eligible', methods=['GET'])
def eligible_lobbies():
    """Return lobbies where the current session user can upload more YAMLs."""
    session_id = session.get("_id")
    if not session_id:
        return jsonify([])

    memberships = select(p for p in LobbyPlayer if p.session_id == session_id)[:]
    result = []
    expired_any = False
    for player in memberships:
        lobby = player.lobby
        old_state = lobby.state
        _expire_lobby_if_needed(lobby)
        if lobby.state != old_state:
            expired_any = True
        if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
            continue
        remaining = lobby.max_yamls_per_player - len(player.yamls)
        if remaining > 0:
            owner_player = LobbyPlayer.get(lobby=lobby, session_id=lobby.owner)
            owner_name = owner_player.player_name if owner_player else "Unknown"
            result.append({
                "id": str(lobby.id),
                "title": lobby.title,
                "remaining": remaining,
                "owner_name": owner_name,
            })
    if expired_any:
        commit()
    return jsonify(result)


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

    yaml_ids_with_pending_request = set(select(
        r.yaml.id for r in LobbyApworldRequest if r.lobby == lobby
    )[:])

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
        game_has_shared_apworld = y_game and y_game in apworld_by_game and y_id not in apworld_by_yaml_id
        if y_id in apworld_by_yaml_id:
            yaml_info["apworld"] = apworld_by_yaml_id[y_id]
            yaml_info["apworld_is_own"] = True
        elif y_game and y_game in apworld_by_game:
            yaml_info["apworld"] = apworld_by_game[y_game]
        if y_id in yaml_ids_with_pending_request:
            yaml_info["apworld_request_pending"] = True
        if y_requires_version:
            yaml_info["required_version"] = _required_version_label(y_requires_version)
        # For standard worlds, include server-side world version and check requires constraint
        if y_game and not y_is_custom and y_game in AutoWorldRegister.world_types:
            server_wv = AutoWorldRegister.world_types[y_game].world_version
            if server_wv != Version(0, 0, 0):
                yaml_info["server_world_version"] = server_wv.as_simple_string()
            if not game_has_shared_apworld:
                warning = _check_version_constraint(y_requires_version, server_wv)
                if warning:
                    yaml_info["version_warning"] = warning
            # Offer optional apworld upgrade if YAML needs a newer version and none uploaded yet
            if (lobby.allow_custom_apworlds and y_requires_version
                    and _version_mismatch_direction(y_requires_version, server_wv) == "newer"
                    and y_id not in apworld_by_yaml_id
                    and not game_has_shared_apworld):
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
    pending_request_count = count(r for r in LobbyApworldRequest if r.lobby == lobby)

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
        "race": lobby.race,
        "server_opts": server_opts,
        "gen_opts": gen_opts,
        "pending_request_count": pending_request_count,
        "last_activity": lobby.last_activity.isoformat() + "Z",
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
        is_owner = session_id == lobby.owner
        if is_owner:
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
                _cancel_all_pending_requests(lobby, "lobby finished generation")
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
                result["last_activity"] = lobby.last_activity.isoformat() + "Z"
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
                result["last_activity"] = lobby.last_activity.isoformat() + "Z"

    return jsonify(result)


@api_endpoints.route('/lobby/<suuid:lobby>/upload', methods=['POST'])
@limiter.limit("20 per minute")
def lobby_upload_yaml(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    _expire_lobby_if_needed(lobby)
    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
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

    # Reject zip files — zips are only accepted at the pregenerated-game upload step.
    for f in files:
        if f.filename.endswith(".zip"):
            return jsonify({"error": f"'{f.filename}' is a .zip file. "
                                     "Use the pregenerated game upload instead."}), 400

    # Validate using existing pipeline
    options = get_yaml_data(files)
    if isinstance(options, (str, Markup)):
        return jsonify({"error": str(options)}), 400

    expanded: dict[str, bytes] = {}
    for filename, content in options.items():
        expanded.update(_split_yaml_documents(filename, content))
    if len(expanded) > len(options):
        if len(expanded) > remaining:
            return jsonify({
                "error": f"Your combined YAML contains {len(expanded)} world(s), "
                         f"but you can only upload {remaining} more YAML(s). "
                         f"Please split the file or remove some entries."
            }), 400
    options = expanded

    force_custom_filenames = set(request.form.getlist("force_custom_file"))

    from worlds.AutoWorld import AutoWorldRegister
    standard_options: dict[str, bytes] = {}
    standard_info: dict[str, tuple[str, str]] = {}  # filename -> (player_name, game) for standard options
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
            if filename in force_custom_filenames:
                if not lobby.allow_custom_apworlds:
                    return jsonify({"error": "Custom APWorlds are not enabled for this lobby."}), 400
                if not player_name:
                    return jsonify({"error": f"Could not find player name in '{filename}'"}), 400
                custom_info[filename] = (player_name, game or os.path.splitext(filename)[0])
            else:
                standard_options[filename] = content
                standard_info[filename] = (player_name, game or "")

    meta = json.loads(lobby.meta)
    plando_options = set(meta.get("plando_options", []))
    new_names: dict[str, str] = {}
    new_games: dict[str, str] = {}
    new_custom: dict[str, bool] = {}
    new_requires: dict[str, str | None] = {}

    needs_confirmation: list[dict] = []
    if standard_options:
        results, rolled = roll_options(standard_options, plando_options)
        hard_errors: list[str] = []
        for fn, result in results.items():
            if isinstance(result, str):
                pn, gm = standard_info.get(fn, ("", ""))
                if gm and gm in AutoWorldRegister.world_types and lobby.allow_custom_apworlds:
                    needs_confirmation.append({
                        "filename": fn,
                        "error": result,
                        "player_name": pn or fn,
                        "game": gm,
                    })
                else:
                    hard_errors.append(result)
        if hard_errors:
            return jsonify({"error": "; ".join(hard_errors)}), 400
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
        new_custom[filename] = False
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

    active_apworld_games: dict[str, tuple[str, str | None]] = {}
    for a in select(a for a in LobbyApworld if a.lobby == lobby):
        server_ver = _server_world_version_for_game(a.game_name)
        server_label = f"v{server_ver.as_simple_string()}" if server_ver else None
        apworld_label = f"v{a.world_version}" if a.world_version else "custom"
        active_apworld_games[a.game_name] = (apworld_label, server_label)

    confirmation_filenames = {item["filename"] for item in needs_confirmation}

    uploaded = []
    version_warnings: list[str] = []
    upgrades_needed: list[dict] = []
    active_apworld_notices: list[str] = []
    noticed_apworld_games: set[str] = set()
    for filename, content in options.items():
        if filename in confirmation_filenames:
            continue
        if isinstance(content, str):
            content = content.encode('utf-8')
        game = new_games.get(filename, '')
        is_custom = new_custom.get(filename, False)
        requires_json = new_requires.get(filename)

        # Check requires.game constraint against server's world version.
        if filename in upgrade_info:
            upgrades_needed.append({
                "game": game,
                "required_version": _required_version_label(requires_json) if requires_json else "?",
            })
        elif requires_json and game and not is_custom and game in AutoWorldRegister.world_types:
            server_wv = AutoWorldRegister.world_types[game].world_version
            warning = _check_version_constraint(requires_json, server_wv)
            if warning:
                version_warnings.append(f"'{new_names.get(filename, filename)}' ({game}): {warning}")

        if game and game in active_apworld_games and game not in noticed_apworld_games:
            noticed_apworld_games.add(game)
            apworld_ver, server_ver = active_apworld_games[game]
            diff = f"{apworld_ver} (server: {server_ver})" if server_ver else apworld_ver
            active_apworld_notices.append(f"{game}: custom APWorld {diff}")

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
        entry: dict = {"id": yaml_record.id, "filename": filename, "is_custom": is_custom, "game": game}
        if requires_json:
            entry["required_version"] = _required_version_label(requires_json)
        uploaded.append(entry)

    yaml_summaries = [
        f"{new_names.get(fn, fn)} ({new_games.get(fn, '?')})"
        for fn in options if fn not in confirmation_filenames
    ]
    player.is_ready = False
    if uploaded:
        LobbyMessage(
            lobby=lobby,
            player=None,
            sender_name="System",
            content=f"{player.player_name} uploaded {len(uploaded)} YAML(s): {', '.join(yaml_summaries)}.",
        )
    lobby.last_activity = utcnow()
    commit()

    result: dict = {"uploaded": uploaded}
    if version_warnings:
        result["version_warnings"] = version_warnings
    if upgrades_needed:
        result["upgrades_needed"] = upgrades_needed
    if active_apworld_notices:
        result["active_apworld_notices"] = active_apworld_notices
    if needs_confirmation:
        result["needs_apworld_confirmation"] = needs_confirmation
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

    view_only = request.args.get("view") == "1"
    if view_only:
        return send_file(
            io.BytesIO(content),
            download_name=yaml_record.filename,
            as_attachment=False,
            mimetype="text/plain; charset=utf-8",
        )

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

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
        return jsonify({"error": "Cannot modify YAMLs in current lobby state"}), 400

    yaml_record = LobbyYaml.get(id=yaml_id)
    if not yaml_record or yaml_record.lobby != lobby:
        return jsonify({"error": "YAML not found"}), 404

    player = _get_player_in_lobby(lobby)
    is_owner = lobby.owner == session["_id"]

    # Only the YAML owner or lobby owner can delete
    if not player or (yaml_record.player != player and not is_owner):
        return jsonify({"error": "Permission denied"}), 403

    if yaml_record.player == player:
        delete_reason = "manually removed"
    else:
        deleter_name = player.player_name if player else "Host"
        delete_reason = f"removed by host {deleter_name}"

    _delete_yaml_record(yaml_record, delete_reason)
    lobby.last_activity = utcnow()
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
    lobby.last_activity = utcnow()
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
    lobby.last_activity = utcnow()
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

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
        return jsonify({"error": "Lobby is not open"}), 400

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    if not player.is_ready and not select(y for y in LobbyYaml if y.lobby == lobby and y.player == player).exists():
        return jsonify({"error": "Upload at least one YAML before marking ready"}), 400

    player.is_ready = not player.is_ready
    lobby.last_activity = utcnow()

    all_players = select(p for p in LobbyPlayer if p.lobby == lobby)[:]
    ready_count = sum(1 for p in all_players if p.is_ready)
    total_count = len(all_players)
    status = "ready" if player.is_ready else "not ready"
    LobbyMessage(
        lobby=lobby,
        player=None,
        sender_name="System",
        content=f"{player.player_name} is {status} ({ready_count}/{total_count})",
    )
    commit()

    return jsonify({"is_ready": player.is_ready})


@api_endpoints.route('/lobby/<suuid:lobby>/generate', methods=['POST'])
def lobby_generate(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can generate"}), 403

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
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

    pre_generate_state = lobby.state
    lobby.state = LOBBY_GENERATING
    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content="Seed generation started...",
    )
    lobby.last_activity = utcnow()
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
        lobby.state = pre_generate_state
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

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
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
            lobby.timeout_minutes = max(1, min(int(data["timeout_minutes"]), 40320))
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
    lobby.last_activity = utcnow()

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
        _delete_yaml_record(y, "player left the lobby")
    player.delete()

    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content=f"{name} left the lobby.",
    )
    lobby.last_activity = utcnow()
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/kick/<int:player_id>', methods=['POST'])
def lobby_kick(lobby: UUID, player_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can kick players"}), 403

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
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
        _delete_yaml_record(y, "player was kicked from the lobby")
    target.delete()

    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content=f"{name} was kicked from the lobby.",
    )
    lobby.last_activity = utcnow()
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

    _cancel_all_pending_requests(lobby, "lobby was closed")
    lobby.state = LOBBY_CLOSED
    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content="The lobby was abandoned by the host.",
    )
    commit()

    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/reopen', methods=['POST'])
def lobby_reopen(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can reopen the lobby"}), 403

    if lobby.state != LOBBY_DONE:
        return jsonify({"error": "Only finished lobbies can be reopened"}), 400

    room = lobby.room
    seed = lobby.seed
    lobby.room = None
    lobby.seed = None
    lobby.generation_id = None
    lobby.state = LOBBY_OPEN
    lobby.last_activity = utcnow()

    for player in select(p for p in LobbyPlayer if p.lobby == lobby):
        player.is_ready = False

    if room:
        room.delete()
    if seed and not seed.rooms and not seed.lobbies:
        for slot in list(seed.slots):
            slot.delete()
        seed.delete()

    LobbyMessage(
        lobby=lobby, player=None, sender_name="System",
        content="The lobby has been reopened by the host. Previous seed and room data were removed.",
    )
    commit()

    return jsonify({"success": True, "state": lobby.state})


@api_endpoints.route('/lobby/<suuid:lobby>/lock', methods=['POST'])
def lobby_lock(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can lock/unlock the lobby"}), 403

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
        return jsonify({"error": "Lobby cannot be locked in its current state"}), 400

    if lobby.state == LOBBY_OPEN:
        lobby.state = LOBBY_LOCKED
        LobbyMessage(
            lobby=lobby, player=None, sender_name="System",
            content="The lobby has been locked by the host. New players can no longer join.",
        )
    else:
        lobby.state = LOBBY_OPEN
        LobbyMessage(
            lobby=lobby, player=None, sender_name="System",
            content="The lobby has been unlocked by the host.",
        )

    lobby.last_activity = utcnow()
    commit()

    return jsonify({"success": True, "state": lobby.state})


@api_endpoints.route('/lobby/<suuid:lobby>/apworld/<int:yaml_id>', methods=['POST'])
@limiter.limit("5 per minute")
def lobby_upload_apworld(lobby: UUID, yaml_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if not lobby.allow_custom_apworlds:
        return jsonify({"error": "This lobby does not allow custom APWorlds"}), 400

    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
        return jsonify({"error": "Lobby is not accepting uploads"}), 400

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    yaml_record = LobbyYaml.get(id=yaml_id)
    if not yaml_record or yaml_record.lobby != lobby:
        return jsonify({"error": "YAML not found"}), 404

    if yaml_record.player != player:
        return jsonify({"error": "You can only upload an APWorld for your own YAML"}), 403

    content_length = request.content_length
    if content_length and content_length > APWORLD_MAX_SIZE:
        return jsonify({"error": f"APWorld file too large (max {APWORLD_MAX_SIZE // (1024*1024)} MB)"}), 413

    mode = (request.form.get("mode") or request.args.get("mode") or "apply").strip().lower()
    if mode not in {"preview", "apply"}:
        return jsonify({"error": "Invalid mode. Expected 'preview' or 'apply'."}), 400

    preview_token = ""
    used_preview_token = ""
    if 'file' in request.files:
        f = request.files['file']
        if not f.filename or not f.filename.endswith('.apworld'):
            return jsonify({"error": "File must be a .apworld file"}), 400

        original_filename = f.filename
        apworld_data = f.read(APWORLD_MAX_SIZE + 1)
        if len(apworld_data) > APWORLD_MAX_SIZE:
            return jsonify({"error": f"APWorld file too large (max {APWORLD_MAX_SIZE // (1024*1024)} MB)"}), 413
    elif mode == "apply":
        preview_token = (request.form.get("preview_token") or "").strip().lower()
        if not preview_token:
            return jsonify({"error": "No file provided. Apply mode requires either file or preview_token."}), 400
        try:
            apworld_data, original_filename = _load_preview_apworld(
                lobby=lobby,
                yaml_record=yaml_record,
                session_id=session["_id"],
                preview_token=preview_token,
            )
        except PermissionError as exc:
            return jsonify({"error": str(exc)}), 403
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        used_preview_token = preview_token
    else:
        return jsonify({"error": "No file provided"}), 400

    try:
        apworld_game, world_version = _parse_apworld_upload(apworld_data, original_filename)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if apworld_game != yaml_record.yaml_game:
        yaml_game = yaml_record.yaml_game or ""
        if not (
            _is_manual_apworld(original_filename, apworld_data)
            and _manual_game_segment(apworld_game) == _manual_game_segment(yaml_game)
            and _manual_game_segment(apworld_game)
        ):
            return jsonify({
                "error": f"APWorld is for '{apworld_game}', but this YAML is for '{yaml_game}'. "
                         f"Please upload the correct APWorld."
            }), 400

    if not yaml_record.is_custom and world_version is None and not _is_manual_apworld(original_filename, apworld_data):
        return jsonify({"error": "Upgrade APWorlds must have a world_version defined in archipelago.json"}), 400

    try:
        preview, current_hash, parsed_world_version = _build_apworld_impact_preview(
            lobby,
            yaml_record,
            world_version,
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if preview["unverifiable_yaml_ids"] and not _is_manual_apworld(original_filename, apworld_data):
        return jsonify({
            "error": "APWorld must define world_version in archipelago.json to validate YAML version requirements."
        }), 400

    if parsed_world_version is not None and _yaml_requires_newer_world(
        yaml_record.requires_game_version,
        parsed_world_version,
    ):
        req_label = _required_version_label(yaml_record.requires_game_version)
        return jsonify({
            "error": f"The uploaded APWorld is v{world_version}, but your YAML requires "
                     f"{yaml_record.yaml_game} v{req_label}. Please upload a newer version."
        }), 400

    if mode == "preview":
        try:
            preview_token = _store_preview_apworld(
                lobby=lobby,
                yaml_record=yaml_record,
                session_id=session["_id"],
                original_filename=original_filename,
                apworld_data=apworld_data,
            )
        except OSError:
            return jsonify({"error": "Could not store preview APWorld file"}), 500
        return jsonify({
            "impact_preview": preview,
            "impact_hash": current_hash,
            "preview_token": preview_token,
            "affects_other_players": preview["affects_other_players"],
            "would_delete_yaml_ids": preview["would_delete_yaml_ids"],
            "mode": "preview",
        }), 200

    impact_hash = (request.form.get("impact_hash") or "").strip()
    if not impact_hash:
        return jsonify({"error": "impact_hash is required in apply mode"}), 400
    if impact_hash != current_hash:
        return jsonify({
            "error": "Impact preview changed. Please review again before applying.",
            "impact_preview": preview,
            "impact_hash": current_hash,
            "affects_other_players": preview["affects_other_players"],
            "would_delete_yaml_ids": preview["would_delete_yaml_ids"],
            "mode": "preview",
        }), 409

    is_owner = lobby.owner == session["_id"]
    affects_other_players = bool(preview["affects_other_players"])
    confirm_impact = (request.form.get("confirm_impact") or "").strip().lower() in {"1", "true", "yes"}

    if is_owner and affects_other_players and not confirm_impact:
        return jsonify({
            "error": "Host confirmation required",
            "impact_preview": preview,
            "impact_hash": current_hash,
            "affects_other_players": True,
            "would_delete_yaml_ids": preview["would_delete_yaml_ids"],
            "mode": "preview",
        }), 412

    if not is_owner and affects_other_players:
        try:
            request_record = _create_pending_apworld_request(
                lobby=lobby,
                yaml_record=yaml_record,
                player=player,
                original_filename=original_filename,
                apworld_data=apworld_data,
                world_version=world_version,
            )
        except OSError:
            return jsonify({"error": "Could not store pending APWorld request file"}), 500
        _lobby_system_message(
            lobby,
            f"{player.player_name} submitted an APWorld replacement request for "
            f"'{yaml_record.yaml_game}' (file: {original_filename}).",
        )
        if used_preview_token:
            _cleanup_preview_apworld(lobby, used_preview_token)
        lobby.last_activity = utcnow()
        commit()
        return jsonify({
            "pending_approval": True,
            "request_id": request_record.id,
            "impact_preview": preview,
            "impact_hash": current_hash,
        }), 202

    try:
        deleted_yaml_ids = _replace_active_apworld(
            lobby=lobby,
            yaml_record=yaml_record,
            original_filename=original_filename,
            apworld_data=apworld_data,
            world_version=world_version,
            preview=preview,
        )
    except OSError:
        return jsonify({"error": "Could not store APWorld file"}), 500
    if used_preview_token:
        _cleanup_preview_apworld(lobby, used_preview_token)
    player.is_ready = False
    version_label = f"v{world_version}" if world_version else "custom"
    summary = (
        f"{player.player_name} applied APWorld {version_label} for '{yaml_record.yaml_game}'."
    )
    other_players = [n for n in preview.get("impacted_players", []) if n != player.player_name]
    if other_players:
        summary += f" Affected players: {', '.join(other_players)}."
    if deleted_yaml_ids:
        summary += f" Removed {len(deleted_yaml_ids)} incompatible YAML(s)."
    _lobby_system_message(lobby, summary)
    lobby.last_activity = utcnow()
    commit()

    return jsonify({
        "success": True,
        "file_size": len(apworld_data),
        "deleted_yaml_ids": deleted_yaml_ids,
        "impact_preview": preview,
    }), 201


@api_endpoints.route('/lobby/<suuid:lobby>/apworld-requests', methods=['GET'])
def lobby_apworld_requests(lobby: UUID):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    is_owner = lobby.owner == session["_id"]
    if is_owner:
        rows = select(
            r for r in LobbyApworldRequest if r.lobby == lobby
        ).order_by(LobbyApworldRequest.submitted_at)[:]
    else:
        rows = select(
            r for r in LobbyApworldRequest
            if r.lobby == lobby and r.requester == player
        ).order_by(LobbyApworldRequest.submitted_at)[:]

    return jsonify({
        "requests": [_serialize_apworld_request(r) for r in rows],
        "is_owner": is_owner,
    })


@api_endpoints.route('/lobby/<suuid:lobby>/apworld-request/<int:request_id>/approve', methods=['POST'])
def lobby_apworld_request_approve(lobby: UUID, request_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404
    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can approve requests"}), 403
    if lobby.state not in (LOBBY_OPEN, LOBBY_LOCKED):
        return jsonify({"error": "Lobby is not accepting APWorld changes"}), 400

    request_record = LobbyApworldRequest.get(id=request_id)
    if not request_record or request_record.lobby != lobby:
        return jsonify({"error": "Request not found"}), 404

    payload = request.get_json(silent=True) or {}
    impact_hash = str(payload.get("impact_hash", "")).strip()
    if not impact_hash:
        return jsonify({"error": "impact_hash is required"}), 400

    try:
        apworld_data = _read_pending_apworld_data(request_record)
    except OSError:
        _cleanup_apworld_request(request_record)
        commit()
        return jsonify({"error": "Request file is missing and was removed"}), 410

    yaml_record = request_record.yaml
    try:
        preview, current_hash, parsed_world_version = _build_apworld_impact_preview(
            lobby,
            yaml_record,
            request_record.world_version,
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if preview["unverifiable_yaml_ids"]:
        return jsonify({
            "error": "APWorld request cannot be approved because version constraints cannot be verified.",
            "impact_preview": preview,
            "impact_hash": current_hash,
        }), 400

    if parsed_world_version is not None and _yaml_requires_newer_world(
        yaml_record.requires_game_version,
        parsed_world_version,
    ):
        return jsonify({"error": "Request APWorld no longer satisfies requester YAML requirements."}), 400

    if impact_hash != current_hash:
        return jsonify({
            "error": "Impact preview changed. Please review and approve again.",
            "impact_preview": preview,
            "impact_hash": current_hash,
        }), 409

    try:
        deleted_yaml_ids = _replace_active_apworld(
            lobby=lobby,
            yaml_record=yaml_record,
            original_filename=request_record.original_filename,
            apworld_data=apworld_data,
            world_version=request_record.world_version,
            preview=preview,
        )
    except OSError:
        return jsonify({"error": "Could not store APWorld file"}), 500
    requester_name = request_record.requester.player_name
    request_world_version = request_record.world_version
    request_game_name = yaml_record.yaml_game
    request_record.requester.is_ready = False
    _cleanup_apworld_request(request_record)

    version_label = f"v{request_world_version}" if request_world_version else "custom"
    summary = (
        f"Host approved {requester_name}'s APWorld request for "
        f"'{request_game_name}' ({version_label})."
    )
    other_players = [n for n in preview.get("impacted_players", []) if n != requester_name]
    if other_players:
        summary += f" Affected players: {', '.join(other_players)}."
    if deleted_yaml_ids:
        summary += f" Removed {len(deleted_yaml_ids)} incompatible YAML(s)."
    _lobby_system_message(lobby, summary)
    lobby.last_activity = utcnow()
    commit()

    return jsonify({"success": True, "deleted_yaml_ids": deleted_yaml_ids})


@api_endpoints.route('/lobby/<suuid:lobby>/apworld-request/<int:request_id>/reject', methods=['POST'])
def lobby_apworld_request_reject(lobby: UUID, request_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404
    if lobby.owner != session["_id"]:
        return jsonify({"error": "Only the lobby owner can reject requests"}), 403

    request_record = LobbyApworldRequest.get(id=request_id)
    if not request_record or request_record.lobby != lobby:
        return jsonify({"error": "Request not found"}), 404

    requester_name = request_record.requester.player_name
    game_name = request_record.game_name
    _cleanup_apworld_request(request_record)
    _lobby_system_message(
        lobby,
        f"Host rejected {requester_name}'s APWorld request for '{game_name}'.",
    )
    lobby.last_activity = utcnow()
    commit()
    return jsonify({"success": True})


@api_endpoints.route('/lobby/<suuid:lobby>/apworld-request/<int:request_id>/cancel', methods=['POST'])
def lobby_apworld_request_cancel(lobby: UUID, request_id: int):
    lobby = Lobby.get(id=lobby)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    player = _get_player_in_lobby(lobby)
    if not player:
        return jsonify({"error": "You are not in this lobby"}), 403

    request_record = LobbyApworldRequest.get(id=request_id)
    if not request_record or request_record.lobby != lobby:
        return jsonify({"error": "Request not found"}), 404

    is_owner = lobby.owner == session["_id"]
    if not is_owner and request_record.requester != player:
        return jsonify({"error": "Permission denied"}), 403

    actor = player.player_name
    requester_name = request_record.requester.player_name
    game_name = request_record.game_name
    _cleanup_apworld_request(request_record)
    _lobby_system_message(
        lobby,
        f"{actor} cancelled APWorld request for '{game_name}' submitted by {requester_name}.",
    )
    lobby.last_activity = utcnow()
    commit()
    return jsonify({"success": True})


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
    _cancel_all_pending_requests(lobby, "lobby uploaded a finished game")
    lobby.state = LOBBY_DONE
    lobby.last_activity = utcnow()
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
