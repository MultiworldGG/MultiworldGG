from __future__ import annotations

import json
import logging
import multiprocessing
import os
import shutil
import typing
from datetime import timedelta, datetime
from threading import Event, Thread
from typing import Any
from uuid import UUID

from pony.orm import db_session, select, commit, PrimaryKey, desc

from Utils import restricted_loads, utcnow
from .locker import Locker, AlreadyRunningException

_stop_event = Event()


def stop() -> None:
    """Stops previously launched threads"""
    global _stop_event
    stop_event = _stop_event
    _stop_event = Event()  # new event for new threads
    stop_event.set()


# Track in-flight generations with their start time for stuck detection
_in_flight_generations: dict[UUID, datetime] = {}
_in_flight_lock = __import__('threading').Lock()


def _mark_generation_complete(gen_id: UUID) -> None:
    """Remove a generation from in-flight tracking when it completes."""
    with _in_flight_lock:
        _in_flight_generations.pop(gen_id, None)


def _mark_generation_started(gen_id: UUID) -> None:
    """Track when a generation starts for stuck detection."""
    with _in_flight_lock:
        _in_flight_generations[gen_id] = utcnow()


def _get_stuck_generations(threshold: timedelta) -> list[UUID]:
    """Return IDs of generations that have exceeded the stuck threshold."""
    now = utcnow()
    with _in_flight_lock:
        return [gid for gid, start_time in _in_flight_generations.items()
                if now - start_time > threshold]


def handle_generation_success(seed_id):
    if seed_id:
        _mark_generation_complete(seed_id)
    logging.info(f"Generation finished for seed {seed_id}")


def handle_generation_failure(result: BaseException):
    try:  # hacky way to get the full RemoteTraceback
        raise result
    except Exception as e:
        logging.exception(e)


def _get_lobby_apworld_root() -> str | None:
    from . import app as web_app
    root = web_app.config.get("LOBBY_APWORLD_PATH")
    if not root:
        return None
    return os.path.abspath(str(root))


def _cleanup_stale_preview_files(max_age: timedelta = timedelta(hours=1)) -> int:
    root = _get_lobby_apworld_root()
    if not root or not os.path.isdir(root):
        return 0

    cutoff = utcnow() - max_age
    removed_files = 0
    for lobby_entry in os.scandir(root):
        if not lobby_entry.is_dir():
            continue
        preview_dir = os.path.join(lobby_entry.path, "preview")
        if not os.path.isdir(preview_dir):
            continue
        for preview_file in os.scandir(preview_dir):
            if not preview_file.is_file():
                continue
            try:
                modified = datetime.utcfromtimestamp(preview_file.stat().st_mtime)
            except OSError:
                continue
            if modified < cutoff:
                try:
                    os.unlink(preview_file.path)
                    removed_files += 1
                except OSError:
                    pass
        try:
            if not any(os.scandir(preview_dir)):
                os.rmdir(preview_dir)
        except OSError:
            pass

    if removed_files:
        logging.info(f"Removed {removed_files} stale lobby APWorld preview file(s).")
    return removed_files


def _mp_gen_game(
    gen_options: dict,
    meta: dict[str, Any] | None = None,
    owner=None,
    sid=None,
    timeout: int|None = None,
) -> PrimaryKey | None:
    from setproctitle import setproctitle

    setproctitle(f"Generator ({sid})")
    try:
        return gen_game(gen_options, meta=meta, owner=owner, sid=sid, timeout=timeout)
    finally:
        setproctitle(f"Generator (idle)")


def launch_generator(pool: multiprocessing.pool.Pool, generation: Generation, timeout: int|None) -> None:
    try:
        meta = json.loads(generation.meta)
        options = restricted_loads(generation.options)
        logging.info(f"Generating {generation.id} for {len(options)} players")
        pool.apply_async(
            _mp_gen_game,
            (options,),
            {
                "meta": meta,
                "sid": generation.id,
                "owner": generation.owner,
                "timeout": timeout,
            },
            handle_generation_success,
            handle_generation_failure,
        )
    except Exception as e:
        generation.state = STATE_ERROR
        commit()
        logging.exception(e)
    else:
        generation.state = STATE_STARTED
        _mark_generation_started(generation.id)


def init_generator(config: dict[str, Any]) -> None:
    from setproctitle import setproctitle

    setproctitle("Generator (idle)")

    try:
        import resource
    except ModuleNotFoundError:
        pass  # unix only module
    else:
        # set soft limit for memory to from config (default 4GiB)
        soft_limit = config["GENERATOR_MEMORY_LIMIT"]
        old_limit, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
        if soft_limit != old_limit:
            resource.setrlimit(resource.RLIMIT_AS, (soft_limit, hard_limit))
            logging.debug(f"Changed AS mem limit {old_limit} -> {soft_limit}")
        del resource, soft_limit, hard_limit

    pony_config = config["PONY"]
    db.bind(**pony_config)
    db.generate_mapping()


def cleanup():
    """delete unowned user-content and expired lobbies"""
    with db_session:
        # >>> bool(uuid.UUID(int=0))
        # True
        rooms = Room.select(lambda room: room.owner == UUID(int=0)).delete(bulk=True)
        seeds = Seed.select(lambda seed: seed.owner == UUID(int=0) and not seed.rooms).delete(bulk=True)
        slots = Slot.select(lambda slot: not slot.seed).delete(bulk=True)
        # Command gets deleted by ponyorm Cascade Delete, as Room is Required
    if rooms or seeds or slots:
        logging.info(f"{rooms} Rooms, {seeds} Seeds and {slots} Slots have been deleted.")

    # Clean up expired lobbies (closed for > 1 hour) and done lobbies (> 3 days old)
    with db_session:
        now = utcnow()
        closed_cutoff = now - timedelta(hours=1)
        done_cutoff = now - timedelta(days=3)
        stale_lobbies = Lobby.select(
            lambda l: (l.state == LOBBY_CLOSED and l.last_activity < closed_cutoff) or
                      (l.state == LOBBY_DONE and l.last_activity < done_cutoff)
        )[:]
        lobby_apworld_root = _get_lobby_apworld_root()
        for lobby in stale_lobbies:
            request_paths = [r.storage_path for r in lobby.apworld_requests]
            apworld_paths = [a.storage_path for a in lobby.apworlds]

            for r in list(lobby.apworld_requests):
                r.delete()
            for a in list(lobby.apworlds):
                a.delete()

            lobby_apworld_dir = (
                os.path.join(lobby_apworld_root, str(lobby.id))
                if lobby_apworld_root else None
            )
            if lobby_apworld_dir:
                shutil.rmtree(lobby_apworld_dir, ignore_errors=True)
            else:
                for path in request_paths + apworld_paths:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
            # Clear player references on messages first, then delete in dependency order
            for m in lobby.messages:
                m.player = None
            for y in lobby.yamls:
                y.delete()
            for m in lobby.messages:
                m.delete()
            for p in lobby.players:
                p.delete()
            lobby.delete()
        if stale_lobbies:
            logging.info(f"{len(stale_lobbies)} stale lobbies cleaned up.")

    _cleanup_stale_preview_files()


def expire_lobbies():
    """Expire lobbies that have been inactive beyond their timeout."""
    with db_session:
        now = utcnow()
        stale_lobbies = Lobby.select(
            lambda l: l.state in (LOBBY_OPEN, LOBBY_LOCKED, LOBBY_GENERATING)
        )[:]
        expired_count = 0
        for lobby in stale_lobbies:
            if now - lobby.last_activity > timedelta(minutes=lobby.timeout_minutes):
                lobby.state = LOBBY_CLOSED
                expired_count += 1
        if expired_count:
            commit()
            logging.info(f"{expired_count} lobbies expired due to inactivity.")
    _cleanup_stale_preview_files()


def autohost(config: dict):
    def keep_running():
        stop_event = _stop_event
        try:
            with Locker("autohost"):
                cleanup()
                hosters = []
                for x in range(config["HOSTERS"]):
                    hoster = MultiworldInstance(config, x)
                    hosters.append(hoster)
                    hoster.start()

                last_lobby_check = utcnow()

                while not stop_event.wait(0.1):
                    with db_session:
                        rooms = select(
                            room for room in Room if
                            room.last_activity >= utcnow() - timedelta(
                                seconds=config["MAX_ROOM_TIMEOUT"])).order_by(desc(Room.last_port))
                        for room in rooms:
                            # we have to filter twice, as the per-room timeout can't currently be PonyORM transpiled.
                            if room.last_activity >= utcnow() - timedelta(seconds=room.timeout + 5):
                                hosters[room.id.int % len(hosters)].start_room(room.id)

                    # Check for expired lobbies every 5 minutes
                    now = utcnow()
                    if now - last_lobby_check > timedelta(minutes=5):
                        last_lobby_check = now
                        try:
                            expire_lobbies()
                        except Exception as e:
                            logging.exception(e)

        except AlreadyRunningException:
            logging.info("Autohost reports as already running, not starting another.")

    Thread(target=keep_running, name="AP_Autohost").start()


def autogen(config: dict):
    def keep_running():
        stop_event = _stop_event
        try:
            with Locker("autogen"):

                with multiprocessing.Pool(config["GENERATORS"], initializer=init_generator,
                                          initargs=(config,), maxtasksperchild=10) as generator_pool:
                    job_time = config["JOB_TIME"]
                    # Grace period: JOB_TIME * 3
                    # When worker is killed and neither the success nor error callback fires.
                    stuck_threshold = timedelta(seconds=(job_time * 3))
                    last_stuck_check = utcnow()

                    with db_session:
                        to_start = select(generation for generation in Generation if generation.state == STATE_STARTED)

                        if to_start:
                            logging.info("Resuming generation")
                            for generation in to_start:
                                sid = Seed.get(id=generation.id)
                                if sid:
                                    generation.delete()
                                else:
                                    launch_generator(generator_pool, generation, timeout=job_time)

                            commit()
                        select(generation for generation in Generation if generation.state == STATE_ERROR).delete()

                    while not stop_event.wait(0.1):
                        try:
                            now = utcnow()

                            # Check for stuck generations every 2 mins
                            if now - last_stuck_check > timedelta(seconds=120):
                                last_stuck_check = now
                                stuck_ids = _get_stuck_generations(stuck_threshold)
                                if stuck_ids:
                                    with db_session:
                                        for gid in stuck_ids:
                                            gen = Generation.get(id=gid)
                                            if gen is not None and gen.state == STATE_STARTED:
                                                # Worker died without completing - mark as error
                                                logging.warning(f"Generation {gid} appears stuck (worker may have died), marking as error")
                                                gen.state = STATE_ERROR
                                                meta = json.loads(gen.meta)
                                                meta["error"] = "Generation worker died unexpectedly. Please try again."
                                                gen.meta = json.dumps(meta)
                                            _mark_generation_complete(gid)
                                        commit()

                            with db_session:
                                # for update locks the database row(s) during transaction, preventing writes from elsewhere
                                to_start = select(
                                    generation for generation in Generation
                                    if generation.state == STATE_QUEUED).for_update()
                                for generation in to_start:
                                    launch_generator(generator_pool, generation, timeout=job_time)
                        except Exception as e:
                            logging.exception(e)
                            stop_event.wait(5)
        except AlreadyRunningException:
            logging.info("Autogen reports as already running, not starting another.")

    Thread(target=keep_running, name="AP_Autogen").start()


class MultiworldInstance():
    def __init__(self, config: dict, id: int):
        self.room_ids = set()
        self.process: typing.Optional[multiprocessing.Process] = None
        self.ponyconfig = config["PONY"]
        self.cert = config["SELFLAUNCHCERT"]
        self.key = config["SELFLAUNCHKEY"]
        self.host = config["HOST_ADDRESS"]
        self.rooms_to_start = multiprocessing.Queue()
        self.rooms_shutting_down = multiprocessing.Queue()
        self.name = f"MultiHoster{id}"
        self.process_start_time = None
        self.restart_interval = timedelta(hours=12)

    def start(self):
        if self.process and self.process.is_alive():
            return False

        process = multiprocessing.Process(group=None, target=run_server_process,
                                          args=(self.name, self.ponyconfig, get_static_server_data(),
                                                self.cert, self.key, self.host,
                                                self.rooms_to_start, self.rooms_shutting_down),
                                          name=self.name)
        process.start()
        self.process = process
        self.process_start_time = utcnow()

    def should_restart(self) -> bool:
        """Check if process should be restarted to reload fresh APWorld data"""
        if not self.process_start_time:
            return False
        
        time_for_restart = utcnow() - self.process_start_time > self.restart_interval
        is_idle = len(self.room_ids) == 0
        return time_for_restart and is_idle

    def start_room(self, room_id):
        while not self.rooms_shutting_down.empty():
            self.room_ids.remove(self.rooms_shutting_down.get(block=True, timeout=None))

        if self.should_restart():
            logging.info(f"{self.name} restarting to load fresh APWorld data (process was idle, no rooms were interrupted")
            self.stop(wait=True)  # Wait for old process to fully terminate before starting new one
            self.start()

        if room_id in self.room_ids:
            pass  # should already be hosted currently.
        else:
            self.room_ids.add(room_id)
            self.rooms_to_start.put(room_id)

    def stop(self, wait: bool = False):
        if self.process:
            self.process.terminate()
            if wait:
                self.process.join(timeout=5)
                if self.process.is_alive():
                    self.process.kill()
                    self.process.join(timeout=2)
            self.process = None
            self.process_start_time = None
            self.rooms_to_start = multiprocessing.Queue()
            self.rooms_shutting_down = multiprocessing.Queue()

    def done(self):
        return self.process and not self.process.is_alive()

    def collect(self):
        self.process.join()  # wait for process to finish
        self.process = None


from .models import Room, Generation, STATE_QUEUED, STATE_STARTED, STATE_ERROR, db, Seed, Slot, Lobby, LobbyApworld, LOBBY_OPEN, LOBBY_GENERATING, LOBBY_CLOSED, LOBBY_DONE, LOBBY_LOCKED
from .customserver import run_server_process, get_static_server_data
from .generate import gen_game
