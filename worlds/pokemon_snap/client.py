from typing import NamedTuple
import json, os, uuid
from collections import defaultdict
from datetime import datetime, timezone

import Utils
from NetUtils import ClientStatus
from CommonClient import logger, CommonContext
from worlds.AutoWorld import AutoWorldRegister

from .constants import *
from .locations import wonderful_id as wdfl_id, multiple_id as mult_id, special_pose_id, regular_pose_id as pose_id, secret_exit_id, sign_id, bonus_id, oak_reward_id, OAK_REWARDS, POKEMON_TO_SLOTS, POKEMON_IN_MULTIPLE_LEVELS
from .items import item_dictionary, SIGN_PIC_NAMES, POKEMON_PIC_NAMES, fragment, unfragment
from .options import PhotoScoring, PressLToStop, PhotoBonusChecks, GoalType
from . import addresses as addr

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


_code_to_name = {data.ps_code: name for name, data in item_dictionary.items()}

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

class PokemonSnapClient:
    should_play_cloud_dialog: bool = True
    camera_inversion: int | None = None
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

    def __init__(self):
        self.photo_log_session = str(uuid.uuid4())
        self.photo_log_path = Utils.user_path("pokemon_snap", f"photo_scores_{self.photo_log_session}.jsonl")

    async def check_snap_locations(self, emu: "PokemonSnapGenericEmuClient", ctx: CommonContext):
        ((level_id, ), report_scores, sign_flags, (secret_exit_flags, ), (photo_roll_count, )) = await emu.read(ctx, [
            (addr.LEVEL_ID, 4, 's32'),
            (addr.SPECIES_SCORES, addr.NUM_SPECIES_SCORES * SPECIES_DATA_SIZE * 2, 'u16'),
            (addr.SIGN_FLAGS, addr.NUM_SIGNS, 'u8'),
            (addr.SECRET_EXIT_FLAGS, 1, 'u8'),
            (addr.ROLL_COUNT, 4, "u32"),
        ])

        if photo_roll_count != 0:
            await self.log_photo_roll(emu, ctx)

        if level_id != self.current_level_id:
            self.current_level_id = level_id
            data = { "type": "MapUpdate", "mapId": self.current_level_id }
            await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot], "data": data}])

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

        all_checks |= await self.do_oak_reward_checks(scores, emu, ctx)

        await ctx.check_locations(all_checks)

    async def do_oak_reward_checks(self, scores, emu: "PokemonSnapGenericEmuClient", ctx: CommonContext):
        # TODO: holy, we gotta clean this up
        REPORT_KEY = f'POKEMON_SNAP_PKMN_REPORT_{ctx.team}_{ctx.slot}'
        REWARD_FLAGS_KEY = f'POKEMON_SNAP_OAK_REWARD_KEYS_{ctx.team}_{ctx.slot}'

        if REPORT_KEY not in ctx.stored_data or len(ctx.stored_data[REPORT_KEY]) == 0 or \
            REWARD_FLAGS_KEY not in ctx.stored_data or len(ctx.stored_data[REWARD_FLAGS_KEY]) == 0:
            # Gate updating here to make sure we restore after disconnect
            await ctx.send_msgs([
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
        prev_report = ctx.stored_data[REPORT_KEY]
        pkmn_report = {
            pokemon_name: max(
                prev_report.get(pokemon_name, 0), 
                max(scores[slot-1].total_score for slot in POKEMON_TO_SLOTS[pokemon_name])
            )
            for pokemon_name in ALL_INGAME_POKEMON
        }

        if pkmn_report != prev_report:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": REPORT_KEY,
                "default": {pokemon_name: 0 for pokemon_name in ALL_INGAME_POKEMON},
                "want_reply": True,
                "operations": [{"operation": "update", "value": pkmn_report}]
            }])
        
        prev_dialog_flags = ctx.stored_data[REWARD_FLAGS_KEY]
        dialog_flags = {x: flags[:] for x, flags in prev_dialog_flags.items()}

        # Trigger dialog and update trigger flags
        pokemon_count = sum(1 for value in pkmn_report.values() if value > 0)
        report_score = sum(value for value in pkmn_report.values())

        # Update what flags have been marked as played
        dialog_request_flags = 0
        dialog_played_flags = (await emu.read(ctx, [(addr.DIALOG_PLAYED_FLAGS, 4, "u32")]))[0][0]
        for reward, flags in dialog_flags.items():
            # if dialog triggered and flag cleared
            if flags[0] and (dialog_played_flags & (1 << OAK_REWARDS[reward])) != 0:
                flags[1] = True # mark dialog as played

        oak_checks = set()
        for oak_reward, reward_index in OAK_REWARDS.items():
            reward_check_func = self.OAK_REWARD_CHECK_FUNCTIONS[oak_reward]
            if not reward_check_func(ctx.slot_data, pokemon_count, report_score): continue
            
            triggered, played = dialog_flags[oak_reward]
            if not triggered:
                dialog_request_flags |= (1 << reward_index)
                dialog_flags[oak_reward][0] = True
            if triggered and played:
                oak_checks.add(oak_reward_id(reward_index))

        if dialog_flags != prev_dialog_flags:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": REWARD_FLAGS_KEY,
                "default": {x: [False, False] for x in OAK_REWARDS},
                "want_reply": True,
                "operations": [{"operation": "update", "value": dialog_flags}]
            }])

        stored_request_flags = (await emu.read(ctx, [(addr.DIALOG_REQUEST_FLAGS, 4, "u32")]))[0][0]
        await emu.write(ctx, [(addr.DIALOG_REQUEST_FLAGS, [dialog_request_flags | stored_request_flags], "u32")])
        
        return oak_checks

    async def receive_snap_items(self, emu: "PokemonSnapGenericEmuClient", ctx: CommonContext):
        await emu.write(ctx, [
            (addr.CAN_USE_OVERRIDE, [0], "u32"),
            (addr.COURSE_OVERRIDE, [0], "u32")
        ])

        can_use_mask = 0
        can_use_per_course_mask = [0] * len(ALL_LEVELS)
        course_mask = 0
        film = ctx.slot_data['starting_film']
        sign_pic_count = 0
        pokemon_pic_count = 0
        prog_scoring_count = 0
        map_fragments = defaultdict(int)
        for net_item in ctx.items_received:
            if not ctx.finished_game and net_item.item == VICTORY_ITEM_ID:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
                await emu.write(ctx, [(addr.DIALOG_REQUEST_FLAGS, [0x80], "u32")])
                if ctx.slot_data['good_technique_mew_photo'] and ctx.slot_data['photo_bonuses'] != PhotoBonusChecks.option_none:
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
                if map_fragments[name] >= ctx.slot_data['map_fragments']:
                    course_mask |= (1 << addr.COURSE_IDS[unfragment(name)])
            elif name == FILM_UPGRADE:
                film = min(film + ctx.slot_data['film_upgrade_amount'], ctx.slot_data['maximum_film'])
            elif name in SIGN_PIC_NAMES:
                sign_pic_count += 1
            elif name in POKEMON_PIC_NAMES:
                pokemon_pic_count += 1
            elif name == PROG_SCORING:
                prog_scoring_count += 1

        met_sign_goal    = ctx.slot_data["goal_type"] == GoalType.option_signs            and sign_pic_count >= ctx.slot_data["signs_required"]
        met_pokemon_goal = ctx.slot_data["goal_type"] == GoalType.option_pokemon_pictures and pokemon_pic_count >= ctx.slot_data["pokemon_required"]

        if met_sign_goal or met_pokemon_goal:
            course_mask |= 1 << addr.COURSE_IDS[LVL_CLOUD]
            if self.should_play_cloud_dialog:
                self.should_play_cloud_dialog = False
                stored_request_flags = (await emu.read(ctx, [(addr.DIALOG_REQUEST_FLAGS, 4, "u32")]))[0][0]
                await emu.write(ctx, [(addr.DIALOG_REQUEST_FLAGS, [stored_request_flags | 1], "u32")])

        if ctx.slot_data['left_bumper_to_start_stop'] == PressLToStop.option_start_with:
            can_use_mask |= addr.CAN_USE_FLAGS[L_TO_STOP]
        
        # Check wonderful/multiple scoring unlocks
        scoring_type = ctx.slot_data['photo_scoring']
        if scoring_type == PhotoScoring.option_vanilla:
            can_use_mask |= addr.CAN_USE_FLAGS[WDFL_SCORING] | addr.CAN_USE_FLAGS[MULT_SCORING]
        elif scoring_type == PhotoScoring.option_separate:
            can_use_mask |= addr.CAN_USE_FLAGS[WDFL_SCORING] | addr.CAN_USE_FLAGS[MULT_SCORING] | addr.CAN_USE_FLAGS[MULT_WO_WDFL]
        elif ctx.slot_data['photo_scoring'] == PhotoScoring.option_progressive_unlocks:
            if prog_scoring_count >= 1: can_use_mask |= addr.CAN_USE_FLAGS[WDFL_SCORING]
            if prog_scoring_count >= 2: can_use_mask |= addr.CAN_USE_FLAGS[MULT_SCORING]
        elif ctx.slot_data['photo_scoring'] == PhotoScoring.option_separate_unlocks:
            can_use_mask |= addr.CAN_USE_FLAGS[MULT_WO_WDFL]

        if self.camera_inversion is None:
            self.camera_inversion = 1 if ctx.slot_data['camera_inversion'] else 0

        camera_inversion_flags = (await emu.read(ctx, [(addr.CAMERA_INVERSION, 4, 'u32')]))[0][0]
        change_pending = camera_inversion_flags & addr.CAMERA_INVERSION_REQUEST_FLAG
        change_acked = camera_inversion_flags & addr.CAMERA_INVERSION_ACK_FLAG
        if not change_pending and (not change_acked or (camera_inversion_flags & 0x01) != self.camera_inversion):
            camera_inversion_flags = self.camera_inversion | addr.CAMERA_INVERSION_REQUEST_FLAG

        await emu.write(ctx, [
            (addr.CAN_USE_MASK, [can_use_mask], "u32"),
            (addr.CAN_USE_PER_COURSE_MASK, can_use_per_course_mask, "u32"),
            (addr.COURSE_UNLOCK_MASK, [course_mask], "u32"),
            (addr.MAX_FILM, [film], "u32"),
            (addr.CAMERA_INVERSION, [camera_inversion_flags], "u32"),
        ])
    
    def append_photo_log(self, record: dict) -> None:
        if self.photo_log_path is None: return
        os.makedirs(os.path.dirname(self.photo_log_path), exist_ok=True)
        with open(self.photo_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")

    def build_roll_record(self, raw_scores: list[PokemonSnapRawScore], run_log: list[PokemonSnapRunEvent], ctx: CommonContext) -> dict:
        level_id = raw_scores[0].level_id if raw_scores else -1

        world = AutoWorldRegister.world_types.get(ctx.game)
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "session": self.photo_log_session,
            "roll": self.photo_rolls_logged,
            "apworld_version": world.world_version.as_simple_string() if world else None,
            "seed_name": ctx.seed_name,
            "slot": ctx.slot,
            "level_id": level_id,
            "photo_scoring": ctx.slot_data.get("photo_scoring"),
            "hard_logic": ctx.slot_data.get("hard_logic"),
            "events": [{"frame": event.frame, "type": run_event_name(event.type)} for event in run_log],
            "photos": [photo_record(i, raw_score, run_log) for i, raw_score in enumerate(raw_scores) if raw_score.species_slot > 0],
        }

    async def log_photo_roll(self, emu: "PokemonSnapGenericEmuClient", ctx: CommonContext):
        photo_count = min((await emu.read(ctx, [(addr.PHOTO_COUNT, 4, 'u32')]))[0][0], NUM_ROLL_PHOTOS)
        raw_scores = []
        if photo_count > 0:
            raw_score_ints = (await emu.read(ctx, [(addr.RAW_SCORES, photo_count * RAW_SCORE_SIZE * 2, "u16")]))[0]
            raw_scores = [PokemonSnapRawScore(*raw_score_ints[i:i+RAW_SCORE_SIZE]) for i in range(0, photo_count * RAW_SCORE_SIZE, RAW_SCORE_SIZE)]

        event_count = min((await emu.read(ctx, [(addr.RUN_EVENT_COUNT, 4, 'u32')]))[0][0], MAX_RUN_EVENTS)
        run_log = []
        if event_count > 0:
            run_log_ints = (await emu.read(ctx, [(addr.RUN_EVENTS, event_count * RUN_LOG_SIZE * 2, "u16")]))[0]
            run_log = [PokemonSnapRunEvent(*run_log_ints[i:i+RUN_LOG_SIZE]) for i in range(0, event_count * RUN_LOG_SIZE, RUN_LOG_SIZE)]

        try:
            self.photo_rolls_logged += 1
            self.append_photo_log(self.build_roll_record(raw_scores, run_log, ctx))
        except Exception as ex:
            logger.error(f"Failed to write to the photo log: {ex}")

        await emu.write(ctx, [(addr.ROLL_COUNT, [0], "u32")])
