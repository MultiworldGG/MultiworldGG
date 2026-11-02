from typing import Optional, NamedTuple
import base64, os, re, time, asyncio, sys, json, uuid
from collections import defaultdict
from datetime import datetime, timezone

import Utils
from CommonClient import logger, server_loop, get_base_parser, gui_enabled
from NetUtils import ClientStatus
from worlds.AutoWorld import AutoWorldRegister

from .pj64_connector import PJ64Context, pj64connect, pj64disconnect, pj64_read_memory, pj64_write_memory
from .constants import *
from .locations import wonderful_id as wdfl_id, multiple_id as mult_id, special_pose_id, regular_pose_id as pose_id, secret_exit_id, sign_id, bonus_id, oak_reward_id, OAK_REWARDS, POKEMON_TO_SLOTS, POKEMON_IN_MULTIPLE_LEVELS
from .update_pj64_config import safe_load_pj64_config
from .items import item_dictionary, SIGN_PIC_NAMES, POKEMON_PIC_NAMES, fragment, unfragment
from .options import PhotoScoring, PressLToStop, PhotoBonusChecks
from . import addresses as addr

_code_to_name = {data.ps_code: name for name, data in item_dictionary.items()}

_tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (TrackerGameContext as CommonContext,
        TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION)
    _tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor

class PokemonSnapReportScore(NamedTuple):
    special_bonus: int
    pose_score: int
    last_pose_id: int
    size_score: int
    technique_score: int
    same_pokemon_score: int
    special_pose_bits: int
    total_score: int

class PokemonSnapRawScore(NamedTuple):
    frame: int
    species_slot: int
    special_pose_id: int
    size_score: int
    pose_id: int
    pose_score: int
    is_wonderful: int
    multiple_score: int
    total_score: int
    level_id: int


class PokemonSnapRunEvent(NamedTuple):
    frame: int
    type: int


SPECIES_DATA_SIZE = len(PokemonSnapReportScore._fields)
RAW_SCORE_SIZE = len(PokemonSnapRawScore._fields)
RUN_LOG_SIZE = len(PokemonSnapRunEvent._fields)

NUM_ROLL_PHOTOS = 60
MAX_RUN_EVENTS = 256
RUN_EVENT_NAMES = ["food", "flute", "pester", "dash_on", "dash_off"]

SLOT_TO_LOCATION = {
    slot: course(name, POKEMON_IN_MULTIPLE_LEVELS[name][i]) if name in POKEMON_IN_MULTIPLE_LEVELS else name
    for name, slots in POKEMON_TO_SLOTS.items()
    for i, slot in enumerate(slots)
}

# Bit in gCanUseMask -> item name (Pokemon Food and Apple share bit 0)
CAN_USE_BIT_NAMES: dict[int, str] = {}
for _name, _bit in addr.CAN_USE_BITS.items():
    CAN_USE_BIT_NAMES.setdefault(_bit, _name)


def run_event_name(event_type: int) -> str | int:
    return RUN_EVENT_NAMES[event_type] if 0 <= event_type < len(RUN_EVENT_NAMES) else event_type


def photo_record(roll_index: int, raw_score: PokemonSnapRawScore, run_log: list[PokemonSnapRunEvent]) -> dict:
    # Frames since each event type last happened before this photo (None = hadn't happened yet this course).
    # The run log is in chronological order, so the last match wins.
    frames_since = {f"last_{name}": None for name in RUN_EVENT_NAMES}
    for event in run_log:
        if event.frame <= raw_score.frame and 0 <= event.type < len(RUN_EVENT_NAMES):
            frames_since[f"last_{RUN_EVENT_NAMES[event.type]}"] = raw_score.frame - event.frame

    return {
        "roll_index": roll_index,
        "frame": raw_score.frame,
        "location": SLOT_TO_LOCATION.get(raw_score.species_slot),
        "species_slot": raw_score.species_slot,
        "special_pose_id": raw_score.special_pose_id,
        "size_score": raw_score.size_score,
        "pose_id": raw_score.pose_id,
        "pose_score": raw_score.pose_score,
        "is_wonderful": raw_score.is_wonderful,
        "multiple_score": raw_score.multiple_score,
        "total_score": raw_score.total_score,
        **frames_since,
    }

class PokemonSnapCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

    def _cmd_pj64_status(self):
        """Gets the current status of the Project 64 connection."""
        if isinstance(self.ctx, PokemonSnapContext):
            logger.info(f"Project64 Status: {self.ctx.pj64_status}")

    def _cmd_photo_log(self):
        """Gets the path to the photo log."""
        if isinstance(self.ctx, PokemonSnapContext):
            logger.info(self.ctx.photo_log_path)

class PokemonSnapContext(CommonContext, PJ64Context):
    command_processor = PokemonSnapCommandProcessor
    game = "Pokemon Snap"
    items_handling = 0b111
    tracker_enabled: bool = False
    instance_id: float | None
    pj64_sync_task: Optional[asyncio.Task[None]] = None
    pj64_status: str
    finished_game: bool = False
    should_play_cloud_dialog: bool = True
    current_level_id: int = -1
    photo_log_session: str
    photo_log_path: str | None = None
    photo_rolls_logged: int = 0

    OAK_REWARD_CHECK_FUNCTIONS = {
        POKEMON_TOTAL_6:  (lambda slot_data, count, _: count >= 6  and slot_data["report_photo_count"]),
        POKEMON_TOTAL_22: (lambda slot_data, count, _: count >= 22 and slot_data["report_photo_count"]),
        POKEMON_TOTAL_40: (lambda slot_data, count, _: count >= 40 and slot_data["report_photo_count"]),

        REPORT_SCORE_24_000:  (lambda slot_data, _, score: score >= 24_000  and slot_data["report_score_total"]),
        REPORT_SCORE_72_500:  (lambda slot_data, _, score: score >= 72_500  and slot_data["report_score_total"]),
        REPORT_SCORE_130_000: (lambda slot_data, _, score: score >= 130_000 and slot_data["report_score_total"]),
    }

    def __init__(self, server_address, password, ap_port):
        """
        Initialize the Pokemon Snap Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        CommonContext.__init__(self, server_address, password)
        PJ64Context.__init__(self, ap_port)
        self.instance_id = None
        self.tracker_enabled = _tracker_loaded
        self.pj64_status = INITIAL_STATUS
        self.ap_port = ap_port
        self.slot_data = {}
        self.goal_type = DEFAULT_GOAL_TYPE
        self.signs_required = DEFAULT_SIGN_REQUIREMENT
        self.pokemon_required = DEFAULT_POKEMON_REQUIREMENT
        self.photo_log_session = str(uuid.uuid4())
        self.photo_log_path = Utils.user_path("pokemon_snap", f"photo_scores_{self.photo_log_session}.jsonl")

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        CommonContext.on_package(self, cmd, args)
        match cmd:
            case "PrintJSON":
                if args.get("type", "") == "Countdown" and len(list(args.get("data", []))) > 0 and \
                        "starting countdown of " in args["data"][0]["text"].lower():
                    countdown_var: int = int(re.search(r"\d+", args["data"][0]["text"]).group())
                    print(str(countdown_var))

            case "Connected":  # On Connect
                self.slot_data = args.get("slot_data", {})
                self.goal_type = self.slot_data["goal_type"]
                self.signs_required = self.slot_data["signs_required"]
                self.pokemon_required = self.slot_data["pokemon_required"]

            case "Bounced":
                if "tags" not in args:
                    return
                if not hasattr(self, "instance_id"):
                    self.instance_id = time.time()


    def _main(self):
        if self.tracker_enabled:
            self.run_generator()
            self.tags.remove("Tracker")
        else:
            logger.warning("Could not find Universal Tracker.")

    def make_gui(self):
        if _tracker_loaded and _has_invalid_universal_tracker(UT_VERSION):
            Utils.messagebox("Universal Tracker needs updated",
            f"Please update your Universal Tracker. The version currently installed is {UT_VERSION}.", error=True)
            raise ImportError(f"Need to update universal tracker version to at least v{'.'.join(map(str,MIN_UNIVERSAL_TRACKER_VERSION))}.")

        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from kvui import GameManager
        ui: type[GameManager] = CommonContext.make_gui(self)
        class UniversalWrapper(ui):
            base_title: str = "Pokemon Snap Client"

            def build(self):
                container = super().build()
                if _tracker_loaded:
                    self.base_title += f" | Universal Tracker {UT_VERSION}"
                return container

        return UniversalWrapper
    
    def append_photo_log(self, record: dict) -> None:
        if self.photo_log_path is None: return
        os.makedirs(os.path.dirname(self.photo_log_path), exist_ok=True)
        with open(self.photo_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")

    def build_roll_record(self, raw_scores: list[PokemonSnapRawScore], run_log: list[PokemonSnapRunEvent]) -> dict:
        level_id = raw_scores[0].level_id if raw_scores else -1

        world = AutoWorldRegister.world_types.get(self.game)
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "session": self.photo_log_session,
            "roll": self.photo_rolls_logged,
            "apworld_version": world.world_version.as_simple_string() if world else None,
            "seed_name": self.seed_name,
            "slot": self.slot,
            "level_id": level_id,
            "photo_scoring": self.slot_data.get("photo_scoring"),
            "hard_logic": self.slot_data.get("hard_logic"),
            "events": [{"frame": event.frame, "type": run_event_name(event.type)} for event in run_log],
            "photos": [photo_record(i, raw_score, run_log) for i, raw_score in enumerate(raw_scores) if raw_score.species_slot > 0],
        }

    async def log_photo_roll(self):
        photo_count = min((await pj64_read_memory(self, "u32", addr.PHOTO_COUNT, 4))[0], NUM_ROLL_PHOTOS)
        raw_scores = []
        if photo_count > 0:
            raw_score_ints = await pj64_read_memory(self, "u16", addr.RAW_SCORES, photo_count * RAW_SCORE_SIZE * 2)
            raw_scores = [PokemonSnapRawScore(*raw_score_ints[i:i+RAW_SCORE_SIZE]) for i in range(0, photo_count * RAW_SCORE_SIZE, RAW_SCORE_SIZE)]

        event_count = min((await pj64_read_memory(self, "u32", addr.RUN_EVENT_COUNT, 4))[0], MAX_RUN_EVENTS)
        run_log = []
        if event_count > 0:
            run_log_ints = await pj64_read_memory(self, "u16", addr.RUN_EVENTS, event_count * RUN_LOG_SIZE * 2)
            run_log = [PokemonSnapRunEvent(*run_log_ints[i:i+RUN_LOG_SIZE]) for i in range(0, event_count * RUN_LOG_SIZE, RUN_LOG_SIZE)]

        try:
            self.photo_rolls_logged += 1
            self.append_photo_log(self.build_roll_record(raw_scores, run_log))
        except Exception as ex:
            logger.error(f"Failed to write to the photo log: {ex}")

        await pj64_write_memory(self, "u32", addr.ROLL_COUNT, [0])

    async def _expansion_loaded(self) -> bool:
        magic = (await pj64_read_memory(self, "u32", addr.EXPANSION_MAGIC, 4))[0]
        return magic == addr.EXPANSION_LOADED

    async def _read_auth_token(self):
        """Read the per-seed auth token from the ROM as base64, or None."""
        try:
            if self.streams is None or not await self._expansion_loaded():
                return None
            raw = bytes(await pj64_read_memory(self, "u8", addr.AUTH_ADDR, addr.AUTH_LEN))
            if not raw or raw == addr.UNPATCHED_AUTH:
                return None
            return base64.b64encode(raw).decode("ascii")
        except Exception:
            return None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        notified = False
        while not self.auth and not self.exit_event.is_set():
            token = await self._read_auth_token()
            if token:
                self.auth = token
                break
            if not notified:
                logger.info("Waiting to read the connect token from a patched, running Pokemon Snap ROM...")
                notified = True
            await asyncio.sleep(3)

        if not self.auth:
            return

        await self.send_connect()

    async def check_snap_locations(self):
        if not self.slot or not await self._expansion_loaded():
            return

        # TODO: condense into one read and split based on addresses
        level_id = (await pj64_read_memory(self, "s32", addr.LEVEL_ID, 4))[0]
        report_scores = await pj64_read_memory(self, "u16", addr.SPECIES_SCORES, addr.NUM_SPECIES_SCORES * SPECIES_DATA_SIZE * 2)
        sign_flags = await pj64_read_memory(self, "u8", addr.SIGN_FLAGS, addr.NUM_SIGNS)
        secret_exit_flags = (await pj64_read_memory(self, "u8", addr.SECRET_EXIT_FLAGS, 1))[0]

        if (await pj64_read_memory(self, "u32", addr.ROLL_COUNT, 4))[0] != 0:
            await self.log_photo_roll()

        if level_id != self.current_level_id:
            self.current_level_id = level_id
            await self.send_msgs([{
                "cmd": "Bounce",
                "slots": [self.slot],
                "data": {
                    "type": "MapUpdate",
                    "mapId": level_id
                }
            }])

        all_checks = set()

        scores = [PokemonSnapReportScore(*report_scores[i:i+SPECIES_DATA_SIZE]) 
                  for i in range(0, addr.NUM_SPECIES_SCORES * SPECIES_DATA_SIZE, SPECIES_DATA_SIZE)]
        for slot, report in enumerate(scores):
            if report.total_score == 0: continue

            pokemon_id = slot + 1
            all_checks.add(pokemon_id)
            if report.technique_score > 0:    all_checks.add(wdfl_id(pokemon_id))
            if report.same_pokemon_score > 0: all_checks.add(mult_id(pokemon_id))
            if report.last_pose_id > 0:       all_checks.add(pose_id(report.last_pose_id, pokemon_id))

            poses_seen_ids = [i+1 for i in range(12) if ((1 << i) & report.special_pose_bits) != 0]
            all_checks |= {special_pose_id(pose_id) for pose_id in poses_seen_ids}
        
        all_checks |= {sign_id(i) for i, f in enumerate(sign_flags) if f != 0}
        all_checks |= {secret_exit_id(i) for i in range(6) if (secret_exit_flags & (1 << i)) != 0}
        all_checks |= {bonus_id(id) for id in all_checks}

        all_checks |= await self.do_oak_reward_checks(scores)

        # CommonClient.check_locations filters locations to just those missing 
        # from the server, so we can send every check we find every time.
        self.checked_locations |= all_checks
        await self.check_locations(all_checks)


    async def do_oak_reward_checks(self, scores):
        # TODO: holy, we gotta clean this up
        REPORT_KEY = f'POKEMON_SNAP_PKMN_REPORT_{self.team}_{self.slot}'
        REWARD_FLAGS_KEY = f'POKEMON_SNAP_OAK_REWARD_KEYS_{self.team}_{self.slot}'

        if REPORT_KEY not in self.stored_data or len(self.stored_data[REPORT_KEY]) == 0 or \
           REWARD_FLAGS_KEY not in self.stored_data or len(self.stored_data[REWARD_FLAGS_KEY]) == 0:
            # Gate updating here to make sure we restore after disconnect
            await self.send_msgs([
                {
                    "cmd": "Set",
                    "key": REPORT_KEY,
                    "default": {pokemon_name: 0 for pokemon_name in ALL_INGAME_POKEMON},
                    "want_reply": True,
                    "operations": []
                },
                {
                    "cmd": "Set",
                    "key": REWARD_FLAGS_KEY,
                    "default": {x: [False, False] for x in OAK_REWARDS},
                    "want_reply": True,
                    "operations": []
                }])
            return set() # Return nothing

        # Update the report on the server
        prev_report = self.stored_data[REPORT_KEY]
        pkmn_report = {
            pokemon_name: max(
                prev_report.get(pokemon_name, 0), 
                max(scores[slot-1].total_score for slot in POKEMON_TO_SLOTS[pokemon_name])
            )
            for pokemon_name in ALL_INGAME_POKEMON
        }

        if pkmn_report != prev_report:
            await self.send_msgs([{
                "cmd": "Set",
                "key": REPORT_KEY,
                "default": {pokemon_name: 0 for pokemon_name in ALL_INGAME_POKEMON},
                "want_reply": True,
                "operations": [{"operation": "update", "value": pkmn_report}]
            }])
        
        prev_dialog_flags = self.stored_data[REWARD_FLAGS_KEY]
        dialog_flags = {x: flags[:] for x, flags in prev_dialog_flags.items()}

        # Trigger dialog and update trigger flags
        pokemon_count = sum(1 for value in pkmn_report.values() if value > 0)
        report_score = sum(value for value in pkmn_report.values())

        # Update what flags have been marked as played
        dialog_request_flags = 0
        dialog_played_flags = (await pj64_read_memory(self, "u32", addr.DIALOG_PLAYED_FLAGS, 4))[0]
        for reward, flags in dialog_flags.items():
            # if dialog triggered and flag cleared
            if flags[0] and (dialog_played_flags & (1 << OAK_REWARDS[reward])) != 0:
                flags[1] = True # mark dialog as played

        oak_checks = set()
        for oak_reward, reward_index in OAK_REWARDS.items():
            reward_check_func = self.OAK_REWARD_CHECK_FUNCTIONS[oak_reward]
            if not reward_check_func(self.slot_data, pokemon_count, report_score): continue
            
            triggered, played = dialog_flags[oak_reward]
            if not triggered:
                dialog_request_flags |= (1 << reward_index)
                dialog_flags[oak_reward][0] = True
            if triggered and played:
                oak_checks.add(oak_reward_id(reward_index))

        if dialog_flags != prev_dialog_flags:
            await self.send_msgs([{
                "cmd": "Set",
                "key": REWARD_FLAGS_KEY,
                "default": {x: [False, False] for x in OAK_REWARDS},
                "want_reply": True,
                "operations": [{"operation": "update", "value": dialog_flags}]
            }])

        stored_request_flags = (await pj64_read_memory(self, "u32", addr.DIALOG_REQUEST_FLAGS, 4))[0]
        await pj64_write_memory(self, "u32", addr.DIALOG_REQUEST_FLAGS, [dialog_request_flags | stored_request_flags])
        
        return oak_checks


    async def receive_snap_items(self):
        if not self.slot or not await self._expansion_loaded():
            return

        await pj64_write_memory(self, "u32", addr.CAN_USE_OVERRIDE, [0])
        await pj64_write_memory(self, "u32", addr.COURSE_OVERRIDE, [0])

        can_use_mask = 0
        can_use_per_course_mask = [0] * len(ALL_LEVELS)
        course_mask = 0
        film = self.slot_data['starting_film']
        sign_pic_count = 0
        pokemon_pic_count = 0
        prog_scoring_count = 0
        map_fragments = defaultdict(int)
        for net_item in self.items_received:
            if not self.finished_game and net_item.item == VICTORY_ITEM_ID:
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                self.finished_game = True
                await pj64_write_memory(self, "u32", addr.DIALOG_REQUEST_FLAGS, [0x80])
                if self.slot_data['good_technique_mew_photo'] and self.slot_data['photo_bonuses'] != PhotoBonusChecks.option_none:
                    logger.info("Mew photographed with good technique - goal complete!")
                else:
                    logger.info("Mew photographed - goal complete!")

            name = _code_to_name.get(net_item.item)
            if name is None:
                continue
            if name in addr.CAN_USE_FLAGS:
                can_use_mask |= addr.CAN_USE_FLAGS[name]
            elif name in addr.CAN_USE_PER_COURSE_FLAGS:
                i, flag = addr.CAN_USE_PER_COURSE_FLAGS[name]
                can_use_per_course_mask[i] |= flag
            elif name in addr.COURSE_IDS:
                course_mask |= 1 << addr.COURSE_IDS[name]
            elif name in map(fragment, ALL_MAIN_LEVELS):
                map_fragments[name] += 1
                if map_fragments[name] >= self.slot_data['map_fragments']:
                    course_mask |= (1 << addr.COURSE_IDS[unfragment(name)])
            elif name == FILM_UPGRADE:
                film = min(film + self.slot_data['film_upgrade_amount'], self.slot_data['maximum_film'])
            elif name in SIGN_PIC_NAMES:
                sign_pic_count += 1
            elif name in POKEMON_PIC_NAMES:
                pokemon_pic_count += 1
            elif name == PROG_SCORING:
                prog_scoring_count += 1

        met_sign_goal = self.goal_type == GOAL_SIGN_PICS and sign_pic_count >= self.signs_required
        met_pokemon_goal = self.goal_type == GOAL_POKEMON_PICS and pokemon_pic_count >= self.pokemon_required

        if met_sign_goal or met_pokemon_goal:
            course_mask |= 1 << addr.COURSE_IDS[LVL_CLOUD]
            if self.should_play_cloud_dialog:
                self.should_play_cloud_dialog = False
                stored_request_flags = (await pj64_read_memory(self, "u32", addr.DIALOG_REQUEST_FLAGS, 4))[0]
                await pj64_write_memory(self, "u32", addr.DIALOG_REQUEST_FLAGS, [stored_request_flags | 1])

        if self.slot_data['left_bumper_to_start_stop'] == PressLToStop.option_start_with:
            can_use_mask |= addr.CAN_USE_FLAGS[L_TO_STOP]
        
        # Check wonderful/multiple scoring unlocks
        scoring_type = self.slot_data['photo_scoring']
        if scoring_type == PhotoScoring.option_vanilla:
            can_use_mask |= addr.CAN_USE_FLAGS[WDFL_SCORING] | addr.CAN_USE_FLAGS[MULT_SCORING]
        elif scoring_type == PhotoScoring.option_separate:
            can_use_mask |= addr.CAN_USE_FLAGS[WDFL_SCORING] | addr.CAN_USE_FLAGS[MULT_SCORING] | addr.CAN_USE_FLAGS[MULT_WO_WDFL]
        elif self.slot_data['photo_scoring'] == PhotoScoring.option_progressive_unlocks:
            if prog_scoring_count >= 1: can_use_mask |= addr.CAN_USE_FLAGS[WDFL_SCORING]
            if prog_scoring_count >= 2: can_use_mask |= addr.CAN_USE_FLAGS[MULT_SCORING]
        elif self.slot_data['photo_scoring'] == PhotoScoring.option_separate_unlocks:
            can_use_mask |= addr.CAN_USE_FLAGS[MULT_WO_WDFL]

        await pj64_write_memory(self, "u32", addr.CAN_USE_MASK, [can_use_mask])
        await pj64_write_memory(self, "u32", addr.CAN_USE_PER_COURSE_MASK, can_use_per_course_mask)
        await pj64_write_memory(self, "u32", addr.COURSE_UNLOCK_MASK, [course_mask])
        await pj64_write_memory(self, "u32", addr.MAX_FILM, [film])
        await pj64_write_memory(self, "u32", addr.CAMERA_INVERSION, [self.slot_data['camera_inversion'] | 0x02]) # 0x02 is the "performed write" flag

    async def wait_for_next_loop(self, time_to_wait: float):
        await asyncio.sleep(time_to_wait)

    async def pj64_sync_main_task(self):
        logger.info(f"Using {CLIENT_NAME}...")
        logger.info("Starting Project64 connector. Use /pj64_status for status information.")

        try:
            while not self.exit_event.is_set():
                try:
                    if not self.pj64_status == CONNECTED_STATUS:
                        if not self.pj64_status == CONNECTING_STATUS:
                            if not await pj64connect(self):
                                self.pj64_status = DISCONNECTED_STATUS
                                logger.info(self.pj64_status)
                                await self.wait_for_next_loop(5)
                                continue
                            self.pj64_status = CONNECTING_STATUS
                            logger.info(self.pj64_status)

                        # Wait for AP login and the patched ROM to be running.
                        if not self.slot or not await self._expansion_loaded():
                            await self.wait_for_next_loop(1)
                            continue

                        self.pj64_status = CONNECTED_STATUS
                        logger.info(self.pj64_status)

                    await self.check_snap_locations()
                    await self.receive_snap_items()
                    await self.wait_for_next_loop(0.125)

                except Exception as ex:
                    logger.error(f"Project64 connection lost: {ex}")
                    pj64disconnect(self)
                    self.pj64_status = DISCONNECTED_STATUS
                    logger.info(DISCONNECTED_STATUS)
                    await self.wait_for_next_loop(5)
                    continue
        except Exception as threadEx:
            logger.error("Something went horribly wrong with the Pokemon Snap client. Details: " + str(threadEx))


def _has_invalid_universal_tracker(universal_tracker_version) -> bool:
    delimiter = "."

    version_split = universal_tracker_version.split(delimiter)
    if len(version_split) < 3:
        return True

    clean_version_split = version_split.copy()
    for i, version in enumerate(version_split):
        clean_version_split[i]  = "".join([ele for ele in version if ele.isdigit()]) # Clean everything but digits from each part of the split

    tracker_version = tuple(int(ele) for ele in clean_version_split)
    if tracker_version < MIN_UNIVERSAL_TRACKER_VERSION:
        return True

    return False

def _patch_and_launch(patch_file: str) -> str:
    """Turn a dragged-in .apsnap patch into a ROM and start the emulator on it.

    Returns the Archipelago server address embedded in the patch (set when the
    patch was downloaded from a room), or an empty string if none.
    """
    from .rom import PokemonSnapProcedurePatch

    rom_path = os.path.splitext(patch_file)[0] + ".z64"
    server = ""
    try:
        patch = PokemonSnapProcedurePatch(patch_file)
        patch.read()
        server = patch.server or ""
        if not os.path.exists(rom_path):
            patch.patch(rom_path)
            logger.info(f"Patched ROM created at {rom_path}")
        else:
            logger.info(f"Using existing patched ROM at {rom_path}")
    except Exception as ex:
        logger.error(f"Failed to create the patched ROM: {ex}")
        Utils.messagebox(f"{CLIENT_NAME} Patch Error", str(ex), True)
        return server

    try:
        safe_load_pj64_config()
    except Exception as ex:
        logger.warning(f"Could not update the Project64 config automatically: {ex}")

    from settings import get_settings
    emu = get_settings()["pokemon_snap_options"]["emulator_settings"]
    if not emu["auto_start"]:
        logger.info(f"Auto-start is off; open this ROM in your emulator: {rom_path}")
        return server

    exe = str(emu["path"])
    if not os.path.exists(exe):
        exe = Utils.user_path(exe)
    if not os.path.exists(exe):
        logger.info(f"No emulator configured; open this ROM in Project64: {rom_path}")
        return server

    # PJ64 3.0 finds Scripts/ and Config/ relative to the cwd, so run it from there.
    import subprocess
    exe = os.path.abspath(exe)
    subprocess.Popen([exe, os.path.abspath(rom_path)], cwd=os.path.dirname(exe))
    logger.info(f"Launched {exe} with {rom_path}")
    logger.info("If the client doesn't connect, start ap_psnap_pj64_adapter_30.js via "
                "Debugger -> Scripts in Project64.")
    return server


def main(*launch_args: str):
    import colorama

    Utils.init_logging(CLIENT_NAME)
    logger.info(f"Starting {CLIENT_NAME}...")

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?",
                        help="Path to an .apsnap patch file to apply and launch.")
    args = parser.parse_args(launch_args)

    server_address: str = args.connect or ""
    if args.patch_file:
        patch_server = _patch_and_launch(args.patch_file)
        # --connect wins; else use the patch's embedded room address.
        if patch_server and not args.connect:
            server_address = patch_server
            logger.info(f"Connecting to the server address from the patch: {server_address}")

    async def _main(connect, password):
        try:
            ap_port = safe_load_pj64_config()
            ctx = PokemonSnapContext(connect, password, ap_port)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

            ctx.pj64_sync_task = asyncio.create_task(ctx.pj64_sync_main_task(), name="PokemonSnap_PJ64Sync")

            # Runs Universal Tracker's internal generator
            ctx._main()

            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            await ctx.wait_for_next_loop(5)

            await ctx.exit_event.wait()
            await ctx.shutdown()

            if ctx.pj64_sync_task:
                await ctx.pj64_sync_task
        except Exception as clientEx:
            client_msg: str = (f"An unknown error occurred while running Pokemon Snap's client.\n" +
                f"Additional details:\n") + str(clientEx)
            logger.error(client_msg)
            Utils.messagebox(f"{CLIENT_NAME} Client Issue", client_msg, True)
            raise clientEx

    colorama.just_fix_windows_console()
    asyncio.run(_main(server_address, args.password))
    colorama.deinit()

if __name__ == "__main__":
    Utils.init_logging(CLIENT_NAME, exception_logger="Client")
    main(*sys.argv[1:])
