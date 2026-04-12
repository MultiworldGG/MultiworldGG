import io
import json
import os
import shutil
import tempfile
import zipfile
from uuid import uuid4

from pony.orm import db_session, flush

from WebHostLib import to_url
from WebHostLib.models import (
    Lobby,
    LobbyApworld,
    LobbyApworldRequest,
    LobbyMessage,
    LobbyPlayer,
    LobbyYaml,
    Room,
    LOBBY_DONE,
    LOBBY_GENERATING,
    LOBBY_OPEN,
    Seed,
)

from . import TestBase


def _make_apworld_bytes(game_name: str, world_version: str = "1.2.3") -> bytes:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "archipelago.json",
            json.dumps({"game": game_name, "world_version": world_version}),
        )
    return payload.getvalue()


class TestLobbyApworldQueue(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.host_client = self.client
        self.other_client = self.app.test_client()
        self.third_client = self.app.test_client()

        self.host_session = uuid4()
        self.other_session = uuid4()
        self.third_session = uuid4()

        with self.host_client.session_transaction() as s:
            s["_id"] = self.host_session
        with self.other_client.session_transaction() as s:
            s["_id"] = self.other_session
        with self.third_client.session_transaction() as s:
            s["_id"] = self.third_session

        self.prev_apworld_path = self.app.config["LOBBY_APWORLD_PATH"]
        self.temp_apworld_dir = tempfile.mkdtemp(prefix="apworld-queue-test-")
        self.app.config["LOBBY_APWORLD_PATH"] = self.temp_apworld_dir

    def tearDown(self) -> None:
        self.app.config["LOBBY_APWORLD_PATH"] = self.prev_apworld_path
        shutil.rmtree(self.temp_apworld_dir, ignore_errors=True)

    def _create_open_lobby(self, include_third_yaml: bool = False) -> dict:
        with db_session:
            lobby = Lobby(
                title="Queue Test Lobby",
                owner=self.host_session,
                password_hash="",
                timeout_minutes=60,
                max_yamls_per_player=3,
                race=False,
                meta="{}",
                state=LOBBY_OPEN,
                max_players=0,
                allow_custom_apworlds=True,
            )
            host_player = LobbyPlayer(lobby=lobby, session_id=self.host_session, player_name="Host")
            other_player = LobbyPlayer(lobby=lobby, session_id=self.other_session, player_name="Other")
            third_player = LobbyPlayer(lobby=lobby, session_id=self.third_session, player_name="Third")

            host_yaml = LobbyYaml(
                lobby=lobby,
                player=host_player,
                filename="host.yaml",
                yaml_player_name="HostSlot",
                yaml_game="GameX",
                is_custom=True,
                requires_game_version=None,
                content=b"game: GameX\nname: HostSlot\n",
            )
            other_yaml = LobbyYaml(
                lobby=lobby,
                player=other_player,
                filename="other.yaml",
                yaml_player_name="OtherSlot",
                yaml_game="GameX",
                is_custom=True,
                requires_game_version=None,
                content=b"game: GameX\nname: OtherSlot\n",
            )
            third_yaml = None
            if include_third_yaml:
                third_yaml = LobbyYaml(
                    lobby=lobby,
                    player=third_player,
                    filename="third.yaml",
                    yaml_player_name="ThirdSlot",
                    yaml_game="GameX",
                    is_custom=True,
                    requires_game_version=None,
                    content=b"game: GameX\nname: ThirdSlot\n",
                )

            flush()
            return {
                "lobby_id": lobby.id,
                "host_yaml_id": host_yaml.id,
                "other_yaml_id": other_yaml.id,
                "third_player_id": third_player.id,
                "third_yaml_id": third_yaml.id if third_yaml else None,
            }

    def _preview(self, client, lobby_suuid: str, yaml_id: int, apworld_bytes: bytes):
        return client.post(
            f"/api/lobby/{lobby_suuid}/apworld/{yaml_id}",
            data={
                "mode": "preview",
                "file": (io.BytesIO(apworld_bytes), "replace.apworld"),
            },
            content_type="multipart/form-data",
        )

    def _apply(self, client, lobby_suuid: str, yaml_id: int, apworld_bytes: bytes, impact_hash: str, confirm: bool):
        return client.post(
            f"/api/lobby/{lobby_suuid}/apworld/{yaml_id}",
            data={
                "mode": "apply",
                "impact_hash": impact_hash,
                "confirm_impact": "1" if confirm else "0",
                "file": (io.BytesIO(apworld_bytes), "replace.apworld"),
            },
            content_type="multipart/form-data",
        )

    def _apply_with_preview_token(
        self,
        client,
        lobby_suuid: str,
        yaml_id: int,
        impact_hash: str,
        preview_token: str,
        confirm: bool,
    ):
        return client.post(
            f"/api/lobby/{lobby_suuid}/apworld/{yaml_id}",
            data={
                "mode": "apply",
                "impact_hash": impact_hash,
                "preview_token": preview_token,
                "confirm_impact": "1" if confirm else "0",
            },
            content_type="multipart/form-data",
        )

    def test_host_preview_requires_confirmation_before_impacting_apply(self) -> None:
        ids = self._create_open_lobby()
        lobby_suuid = to_url(ids["lobby_id"])
        apworld_bytes = _make_apworld_bytes("GameX", "2.0.0")

        preview = self._preview(self.host_client, lobby_suuid, ids["host_yaml_id"], apworld_bytes)
        self.assertEqual(preview.status_code, 200, preview.get_data(as_text=True))
        preview_data = preview.get_json()
        self.assertTrue(preview_data["affects_other_players"])

        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertEqual(LobbyApworld.select(lambda a: a.lobby == lobby).count(), 0)

        apply_without_confirm = self._apply(
            self.host_client,
            lobby_suuid,
            ids["host_yaml_id"],
            apworld_bytes,
            preview_data["impact_hash"],
            confirm=False,
        )
        self.assertEqual(apply_without_confirm.status_code, 412, apply_without_confirm.get_data(as_text=True))
        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            confirmation_msgs = [
                m for m in LobbyMessage.select(lambda m: m.lobby == lobby and m.player is None)
                if "Host confirmation is required before applying" in m.content
            ]
            self.assertEqual(len(confirmation_msgs), 0)

        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertEqual(LobbyApworld.select(lambda a: a.lobby == lobby).count(), 0)

        apply_with_confirm = self._apply(
            self.host_client,
            lobby_suuid,
            ids["host_yaml_id"],
            apworld_bytes,
            preview_data["impact_hash"],
            confirm=True,
        )
        self.assertEqual(apply_with_confirm.status_code, 201, apply_with_confirm.get_data(as_text=True))
        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertEqual(LobbyApworld.select(lambda a: a.lobby == lobby).count(), 1)

    def test_apply_mode_accepts_preview_token_without_second_file_upload(self) -> None:
        ids = self._create_open_lobby()
        lobby_suuid = to_url(ids["lobby_id"])
        apworld_bytes = _make_apworld_bytes("GameX", "2.0.0")

        preview = self._preview(self.host_client, lobby_suuid, ids["host_yaml_id"], apworld_bytes)
        self.assertEqual(preview.status_code, 200, preview.get_data(as_text=True))
        preview_data = preview.get_json()
        preview_token = preview_data.get("preview_token")
        self.assertTrue(preview_token)

        apply_with_token = self._apply_with_preview_token(
            self.host_client,
            lobby_suuid,
            ids["host_yaml_id"],
            preview_data["impact_hash"],
            preview_token,
            confirm=True,
        )
        self.assertEqual(apply_with_token.status_code, 201, apply_with_token.get_data(as_text=True))
        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertEqual(LobbyApworld.select(lambda a: a.lobby == lobby).count(), 1)

    def test_hash_drift_returns_409_with_refreshed_preview(self) -> None:
        ids = self._create_open_lobby()
        lobby_suuid = to_url(ids["lobby_id"])
        apworld_bytes = _make_apworld_bytes("GameX", "2.0.0")

        preview = self._preview(self.host_client, lobby_suuid, ids["host_yaml_id"], apworld_bytes)
        self.assertEqual(preview.status_code, 200)
        old_hash = preview.get_json()["impact_hash"]

        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            third_player = LobbyPlayer.get(session_id=self.third_session, lobby=lobby)
            LobbyYaml(
                lobby=lobby,
                player=third_player,
                filename="late.yaml",
                yaml_player_name="LateSlot",
                yaml_game="GameX",
                is_custom=True,
                requires_game_version=None,
                content=b"game: GameX\nname: LateSlot\n",
            )

        stale_apply = self._apply(
            self.host_client,
            lobby_suuid,
            ids["host_yaml_id"],
            apworld_bytes,
            old_hash,
            confirm=True,
        )
        self.assertEqual(stale_apply.status_code, 409, stale_apply.get_data(as_text=True))
        stale_json = stale_apply.get_json()
        self.assertIn("impact_hash", stale_json)
        self.assertNotEqual(stale_json["impact_hash"], old_hash)

    def test_non_host_impacted_apply_creates_pending_and_close_cleans_requests(self) -> None:
        ids = self._create_open_lobby()
        lobby_suuid = to_url(ids["lobby_id"])
        apworld_bytes = _make_apworld_bytes("GameX", "2.0.0")

        preview = self._preview(self.other_client, lobby_suuid, ids["other_yaml_id"], apworld_bytes)
        self.assertEqual(preview.status_code, 200)
        preview_json = preview.get_json()
        self.assertTrue(preview_json["affects_other_players"])

        apply_response = self._apply(
            self.other_client,
            lobby_suuid,
            ids["other_yaml_id"],
            apworld_bytes,
            preview_json["impact_hash"],
            confirm=False,
        )
        self.assertEqual(apply_response.status_code, 202, apply_response.get_data(as_text=True))
        pending_json = apply_response.get_json()
        self.assertTrue(pending_json["pending_approval"])
        request_id = pending_json["request_id"]

        status_response = self.host_client.get(f"/api/lobby/{lobby_suuid}/status")
        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.get_json().get("pending_request_count"), 1)

        with db_session:
            req = LobbyApworldRequest.get(id=request_id)
            self.assertIsNotNone(req)
            self.assertTrue(os.path.exists(req.storage_path))
            pending_path = req.storage_path

        close_response = self.host_client.post(f"/api/lobby/{lobby_suuid}/close")
        self.assertEqual(close_response.status_code, 200, close_response.get_data(as_text=True))

        with db_session:
            self.assertIsNone(LobbyApworldRequest.get(id=request_id))
        self.assertFalse(os.path.exists(pending_path))

    def test_deleting_new_owner_yaml_removes_custom_apworld_and_notifies_remaining_player(self) -> None:
        ids = self._create_open_lobby()
        lobby_suuid = to_url(ids["lobby_id"])

        # Host applies an initial custom APWorld.
        apworld_v1 = _make_apworld_bytes("GameX", "1.0.0")
        host_preview = self._preview(self.host_client, lobby_suuid, ids["host_yaml_id"], apworld_v1)
        self.assertEqual(host_preview.status_code, 200, host_preview.get_data(as_text=True))
        host_apply = self._apply(
            self.host_client,
            lobby_suuid,
            ids["host_yaml_id"],
            apworld_v1,
            host_preview.get_json()["impact_hash"],
            confirm=True,
        )
        self.assertEqual(host_apply.status_code, 201, host_apply.get_data(as_text=True))

        # Other player requests and host approves a replacement APWorld.
        apworld_v2 = _make_apworld_bytes("GameX", "2.0.0")
        other_preview = self._preview(self.other_client, lobby_suuid, ids["other_yaml_id"], apworld_v2)
        self.assertEqual(other_preview.status_code, 200, other_preview.get_data(as_text=True))
        other_apply = self._apply(
            self.other_client,
            lobby_suuid,
            ids["other_yaml_id"],
            apworld_v2,
            other_preview.get_json()["impact_hash"],
            confirm=False,
        )
        self.assertEqual(other_apply.status_code, 202, other_apply.get_data(as_text=True))
        pending_json = other_apply.get_json()
        request_id = pending_json["request_id"]

        approve = self.host_client.post(
            f"/api/lobby/{lobby_suuid}/apworld-request/{request_id}/approve",
            json={"impact_hash": pending_json["impact_hash"]},
        )
        self.assertEqual(approve.status_code, 200, approve.get_data(as_text=True))

        # Deleting the YAML that currently owns the APWorld removes it for custom-only games.
        delete_other_yaml = self.other_client.delete(f"/api/lobby/{lobby_suuid}/yaml/{ids['other_yaml_id']}")
        self.assertEqual(delete_other_yaml.status_code, 200, delete_other_yaml.get_data(as_text=True))

        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertIsNone(LobbyYaml.get(id=ids["other_yaml_id"]))

            apworlds = LobbyApworld.select(lambda a: a.lobby == lobby and a.game_name == "GameX")[:]
            self.assertEqual(len(apworlds), 0)

            system_messages = [
                m.content for m in LobbyMessage.select(lambda m: m.lobby == lobby and m.player is None)
            ]
            self.assertTrue(
                any(
                    "Host: the APWorld that replaced yours was removed" in content
                    and "You can upload your APWorld again." in content
                    for content in system_messages
                )
            )

        status_response = self.host_client.get(f"/api/lobby/{lobby_suuid}/status")
        self.assertEqual(status_response.status_code, 200, status_response.get_data(as_text=True))
        game_apworld = next(
            (entry for entry in status_response.get_json()["apworlds"] if entry["game_name"] == "GameX"),
            None,
        )
        self.assertIsNone(game_apworld)

    def test_pending_requests_cleanup_on_done_transition(self) -> None:
        ids = self._create_open_lobby()
        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            host_player = LobbyPlayer.get(session_id=self.host_session, lobby=lobby)
            host_yaml = LobbyYaml.get(id=ids["host_yaml_id"])
            seed = Seed(multidata=b"", owner=self.host_session, meta='{"race": false}')
            lobby.state = LOBBY_GENERATING
            lobby.generation_id = seed.id

            pending_dir = os.path.join(self.temp_apworld_dir, str(lobby.id), "pending")
            os.makedirs(pending_dir, exist_ok=True)
            pending_path = os.path.join(pending_dir, "manual_pending.apworld")
            with open(pending_path, "wb") as f:
                f.write(_make_apworld_bytes("GameX", "2.0.0"))

            req = LobbyApworldRequest(
                lobby=lobby,
                yaml=host_yaml,
                requester=host_player,
                game_name="GameX",
                original_filename="manual.apworld",
                storage_path=pending_path,
                file_size=os.path.getsize(pending_path),
                world_version="2.0.0",
            )
            request_id = req.id

        lobby_suuid = to_url(ids["lobby_id"])
        status_response = self.host_client.get(f"/api/lobby/{lobby_suuid}/status")
        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.get_json()["state"], 2)

        with db_session:
            self.assertIsNone(LobbyApworldRequest.get(id=request_id))
        self.assertFalse(os.path.exists(pending_path))

    def test_reopen_done_lobby_preserves_players_files_and_settings(self) -> None:
        ids = self._create_open_lobby()
        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            lobby.meta = json.dumps({
                "server_options": {"hint_cost": 7},
                "generator_options": {"spoiler": 1},
            })
            for player in lobby.players:
                player.is_ready = True

            seed = Seed(multidata=b"done-seed", owner=self.host_session, meta='{"race": false}')
            room = Room(seed=seed, owner=self.host_session, tracker=uuid4())
            lobby.seed = seed
            lobby.room = room
            lobby.state = LOBBY_DONE

            host_yaml = LobbyYaml.get(id=ids["host_yaml_id"])
            apworld_dir = os.path.join(self.temp_apworld_dir, str(lobby.id))
            os.makedirs(apworld_dir, exist_ok=True)
            apworld_path = os.path.join(apworld_dir, "host.apworld")
            apworld_bytes = _make_apworld_bytes("GameX", "2.0.0")
            with open(apworld_path, "wb") as apworld_file:
                apworld_file.write(apworld_bytes)

            apworld = LobbyApworld(
                lobby=lobby,
                yaml=host_yaml,
                game_name="GameX",
                original_filename="host.apworld",
                storage_path=apworld_path,
                file_size=len(apworld_bytes),
                world_version="2.0.0",
            )
            seed_id = seed.id
            room_id = room.id
            flush()
            apworld_id = apworld.id

        lobby_suuid = to_url(ids["lobby_id"])
        reopen_response = self.host_client.post(f"/api/lobby/{lobby_suuid}/reopen")
        self.assertEqual(reopen_response.status_code, 200, reopen_response.get_data(as_text=True))
        self.assertEqual(reopen_response.get_json()["state"], LOBBY_OPEN)

        status_response = self.host_client.get(f"/api/lobby/{lobby_suuid}/status")
        self.assertEqual(status_response.status_code, 200)
        status_json = status_response.get_json()
        self.assertEqual(status_json["state"], LOBBY_OPEN)
        self.assertNotIn("seed_id", status_json)
        self.assertNotIn("room_id", status_json)

        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertEqual(lobby.state, LOBBY_OPEN)
            self.assertIsNone(lobby.seed)
            self.assertIsNone(lobby.room)
            self.assertEqual(len(lobby.players), 3)
            self.assertEqual(len(lobby.yamls), 2)
            self.assertEqual(len(lobby.apworlds), 1)
            self.assertEqual(json.loads(lobby.meta)["server_options"]["hint_cost"], 7)
            self.assertTrue(all(not player.is_ready for player in lobby.players))
            self.assertIsNone(Seed.get(id=seed_id))
            self.assertIsNone(Room.get(id=room_id))
            self.assertIsNotNone(LobbyApworld.get(id=apworld_id))
            self.assertTrue(os.path.exists(apworld_path))

    def test_reopen_requires_owner(self) -> None:
        ids = self._create_open_lobby()
        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            seed = Seed(multidata=b"done-seed", owner=self.host_session, meta='{"race": false}')
            room = Room(seed=seed, owner=self.host_session, tracker=uuid4())
            lobby.seed = seed
            lobby.room = room
            lobby.state = LOBBY_DONE
            seed_id = seed.id
            room_id = room.id

        lobby_suuid = to_url(ids["lobby_id"])
        reopen_response = self.other_client.post(f"/api/lobby/{lobby_suuid}/reopen")
        self.assertEqual(reopen_response.status_code, 403, reopen_response.get_data(as_text=True))

        with db_session:
            lobby = Lobby.get(id=ids["lobby_id"])
            self.assertEqual(lobby.state, LOBBY_DONE)
            self.assertIsNotNone(lobby.seed)
            self.assertIsNotNone(lobby.room)
            self.assertIsNotNone(Seed.get(id=seed_id))
            self.assertIsNotNone(Room.get(id=room_id))

    def test_reopen_rejects_non_done_state(self) -> None:
        ids = self._create_open_lobby()
        lobby_suuid = to_url(ids["lobby_id"])
        reopen_response = self.host_client.post(f"/api/lobby/{lobby_suuid}/reopen")
        self.assertEqual(reopen_response.status_code, 400, reopen_response.get_data(as_text=True))
        self.assertIn("finished lobbies", reopen_response.get_json()["error"])
