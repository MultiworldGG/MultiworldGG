"""Unified TTYD runtime: ghost peer pipeline (publish, render, hits,
spin tracking, SFX).
and the 60 Hz ghost-sync orchestrator.

TTYDClient.py owns AP wiring, the items/locations sync task, and all
user-facing /commands. Helpers in this module that need ROOM /
read_string from TTYDClient go through the lazy accessors below to
avoid a load-time import cycle.
"""

import asyncio
import struct
import typing
import uuid

from CommonClient import logger
from .TTYDPatcher import dolphin
from NetUtils import SlotType

from . import Ghosts


def _client_read_string(addr: int, length: int) -> str:
    """Lazy import of TTYDClient.read_string. Called from inside
    runtime functions that need to read a NUL-terminated string
    from Dolphin RAM (e.g. the current map name)."""
    from . import TTYDClient
    return TTYDClient.read_string(addr, length)


def _client_ROOM() -> int:
    """Lazy accessor for the ROOM register address constant."""
    from . import TTYDClient
    return TTYDClient.ROOM




MARIO_PTR_ADDR = 0x8041E900

ANIM_WP_ADDR = 0x803D9470
ANIM_POSE_STRIDE = 0x170
ANIM_POSE_FRAME_OFFSET = 0x20

SFX_RING_CAPACITY    = 32

SFX_EVENT_BYTES      = 4

HIT_KIND_HAMMER = 1

def _resolve_ghost_addresses(ctx) -> bool:
    """Read APSettings.ghostStatePtr and populate ctx._ghost_addrs.

    Re-reads the pointer every call and recomputes the address table only
    when it CHANGES. Caching it for the whole client-process lifetime was a
    corruption bug: on an in-place game reset (recovering from a crash screen
    without closing Dolphin) DME stays hooked, the mod's Init() re-allocates
    GhostState at a possibly different address, but the stale cached address
    kept receiving the peer block + scratch every frame.

    Returns False ("skip this tick") until the pointer is valid."""
    try:
        ptr = int.from_bytes(
            dolphin.read_bytes(Ghosts.APSETTINGS_GHOST_STATE_PTR, 4), "big"
        )
    except Exception:
        return False
    # Treat zero as "not yet published". The mod writes a non-zero
    # pointer in mod::ghosts::Init() at boot.
    if ptr == 0:
        ctx._ghost_addrs = None
        ctx._ghost_state_ptr = 0
        return False
    if (getattr(ctx, "_ghost_addrs", None) is not None
            and getattr(ctx, "_ghost_state_ptr", 0) == ptr):
        return True
    try:
        ctx._ghost_addrs = Ghosts.compute_ghost_state_addresses(ptr)
        ctx._ghost_state_ptr = ptr
    except ValueError as e:
        # Pointer out of plausible range; usually means the game just
        # hasn't booted far enough yet. Try again next tick.
        logger.debug(f"ghost-state pointer not yet valid: {e}")
        ctx._ghost_addrs = None
        ctx._ghost_state_ptr = 0
        return False
    return True

def _read_pose_frame(pose_id: int) -> float | None:
    if pose_id < 0:
        return None
    try:
        arr = int.from_bytes(
            dolphin.read_bytes(ANIM_WP_ADDR + 0x10, 4), "big"
        )
        if not (0x80000000 <= arr < 0x81800000):
            return None
        addr = arr + pose_id * ANIM_POSE_STRIDE + ANIM_POSE_FRAME_OFFSET
        (frame,) = struct.unpack(">f", dolphin.read_bytes(addr, 4))
        return frame
    except Exception:
        return None


def _read_self_state(ctx) -> dict | None:
    """Read the local Player struct in ONE IPC call and parse offsets
    locally. Doing this as 9 separate dolphin.read_bytes calls (the old
    way) caused visible jitter: the game advances frames between reads
    so the resulting state mixed values from different frames.

    The Player struct is contiguous; we read the first 0x1B0 bytes which
    covers all the offsets we need (largest is wPlayerDirectionCurrent at
    0x1AC). The struct read isn't truly atomic against the running game
    (Dolphin's read happens while the GameCube CPU is also writing) but
    it's near-instantaneous and dramatically tighter than 9 separate
    round-trips through asyncio + IPC.

    Takes ctx so it can resolve the GhostState container address (for
    reading the self-paper-AGB scratch field). If addresses haven't
    been resolved yet, falls back to leaving paper_agb empty rather
    than failing the whole read."""
    try:
        player_ptr = int.from_bytes(
            dolphin.read_bytes(MARIO_PTR_ADDR, 4), "big"
        )
        if not (0x80000000 <= player_ptr < 0x81800000):
            return None

        buf = dolphin.read_bytes(player_ptr, 0x2D4)

        (flags2,) = struct.unpack_from(">I", buf, 0x4)
        (flags3,) = struct.unpack_from(">I", buf, 0xC)
        anim_ptr  = int.from_bytes(buf[0x18:0x1C], "big")

        paper_anim_ptr = int.from_bytes(buf[0x1C:0x20], "big")
        (motion_timer,) = struct.unpack_from(">H", buf, 0x28)

        (motion_id,) = struct.unpack_from(">H", buf, 0x2E)

        (color_raw,) = struct.unpack_from(">b", buf, 0x3D)  # marioGetColor byte; -1 sentinel
        color_index = color_raw if 0 <= color_raw <= 3 else 0

        (base_x,  base_y,  base_z)  = struct.unpack_from(">fff", buf, 0x8C)
        (ofs1_x,  ofs1_y,  ofs1_z)  = struct.unpack_from(">fff", buf, 0x98)
        (ofs2_x,  ofs2_y,  ofs2_z)  = struct.unpack_from(">fff", buf, 0xA4)
        x = base_x + ofs1_x + ofs2_x
        y = base_y + ofs1_y + ofs2_y
        z = base_z + ofs1_z + ofs2_z
        (camera_angle,) = struct.unpack_from(">f", buf, 0x19C)
        (rot_y,) = struct.unpack_from(">f", buf, 0x1AC)

        (rot_x,) = struct.unpack_from(">f", buf, 0xBC)
        (rot_z,) = struct.unpack_from(">f", buf, 0xC4)

        (pivot_x, pivot_y, pivot_z) = struct.unpack_from(">fff", buf, 0xB0)

        (scale_x, scale_y, scale_z) = struct.unpack_from(">fff", buf, 0xC8)

        (flags1,) = struct.unpack_from(">I", buf, 0x0)
        if flags1 & 0x01000000:
            (stretch_y,) = struct.unpack_from(">f", buf, 0x130)
        else:
            stretch_y = 1.0

        anim_name = ""
        if 0x80000000 <= anim_ptr < 0x81800000:
            raw = dolphin.read_bytes(anim_ptr, 16)
            anim_name = raw.split(b"\x00", 1)[0].decode("ascii", errors="replace")

        paper_anim = ""
        if 0x80000000 <= paper_anim_ptr < 0x81800000:
            raw = dolphin.read_bytes(paper_anim_ptr, 16)
            paper_anim = raw.split(b"\x00", 1)[0].decode("ascii", errors="replace")

        paper_agb = ""
        try:
            addrs = getattr(ctx, "_ghost_addrs", None) if ctx else None
            agb_addr = addrs.get("self_paper_agb") if addrs else None
            if agb_addr is not None:
                agb_raw = dolphin.read_bytes(agb_addr, Ghosts.SELF_PAPER_AGB_LEN)
                paper_agb = agb_raw.split(b"\x00", 1)[0].decode(
                    "ascii", errors="replace")
        except Exception:

            pass

        paper_local_time = -1.0
        if motion_id == 0x13 and paper_anim == "P_H_1A":
            (spin_charge,) = struct.unpack_from(">f", buf, 0x2C8)
            paper_local_time = spin_charge / 6.0
        elif motion_id == 0x14 and anim_name == "M_W_6":

            (mp_2d3,) = struct.unpack_from(">b", buf, 0x2D3)
            paper_local_time = float(mp_2d3)
        elif anim_name == "M_B_3" or paper_anim == "PM_B_1":
            # Vivian Veil: the engine scrubs the paper pose (mp+0x240)
            # playhead every frame for both sink and rise. Read that
            # pose's live frame position directly so receivers match
            # exactly, instead of reconstructing it from phase bytes.
            (paper_pose_id,) = struct.unpack_from(">i", buf, 0x240)
            pf = _read_pose_frame(paper_pose_id)
            if pf is not None:
                paper_local_time = pf
    except Exception:
        return None

    map_name = _client_read_string(_client_ROOM(), 16)
    if not map_name:
        return None

    return {
        "map": map_name,
        "anim": anim_name,
        "x": x,
        "y": y,
        "z": z,
        "rot_y": rot_y,
        "rot_x": rot_x,
        "rot_z": rot_z,
        "rot_pivot_x": pivot_x,
        "rot_pivot_y": pivot_y,
        "rot_pivot_z": pivot_z,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "scale_z": scale_z,
        "stretch_y": stretch_y,
        "flags1": flags1,
        "flags2": flags2,
        "flags3": flags3,
        "motion_timer": motion_timer,
        "motion_id": motion_id,
        "color_index": color_index,
        "camera_angle": camera_angle,
        "paper_agb": paper_agb,
        "paper_anim": paper_anim,
        "paper_local_time": paper_local_time,
    }

def _write_peer_block(ctx) -> None:
    if ctx.team is None or ctx.slot is None:
        return
    if not _resolve_ghost_addresses(ctx):
        return
    peer_block_addr = ctx._ghost_addrs["peer_block"]
    peers = getattr(ctx, "_ghost_peers", {})

    try:
        payload = Ghosts.pack_peer_block(peers)
        dolphin.write_bytes(peer_block_addr, payload)
    except Exception as e:
        logger.warning(f"Failed to write ghost block to Dolphin: {e}")

async def _drain_sfx_ring(ctx) -> list:
    if not _resolve_ghost_addresses(ctx):
        return []
    addrs = ctx._ghost_addrs
    head_addr   = addrs["sfx_ring_head"]
    tail_addr   = addrs["sfx_ring_tail"]
    events_addr = addrs["sfx_ring_events"]
    try:
        head_b = dolphin.read_bytes(head_addr, 1)
        tail_b = dolphin.read_bytes(tail_addr, 1)
    except Exception:
        return []
    if not head_b or not tail_b:
        return []

    head = head_b[0]
    tail = tail_b[0]
    if head == tail:
        return []

    available = (head - tail) & 0xFF
    if available > SFX_RING_CAPACITY:
        available = SFX_RING_CAPACITY

    events = []
    cur = tail
    for _ in range(available):
        try:
            raw = dolphin.read_bytes(
                events_addr + cur * SFX_EVENT_BYTES,
                SFX_EVENT_BYTES)
        except Exception:
            break
        if not raw or len(raw) < SFX_EVENT_BYTES:
            break
        sfx_id = (raw[0] << 8) | raw[1]
        seq    = raw[2]
        flags  = raw[3]
        events.append({"sfx_id": sfx_id, "seq": seq, "flags": flags})
        cur = (cur + 1) % SFX_RING_CAPACITY

    try:
        dolphin.write_bytes(tail_addr, bytes([head]))
    except Exception:
        pass

    if len(events) > Ghosts.SFX_EVENTS_PER_SLOT:
        events = events[-Ghosts.SFX_EVENTS_PER_SLOT:]
    return events






def _publish_ghost_state_scratch(ctx):
    addrs = ctx._ghost_addrs if _resolve_ghost_addresses(ctx) else None

    team_id = int(getattr(ctx, "_ghost_team_id", Ghosts.TEAM_NONE)) & 0xFF
    friendly_fire = 0  # FF command removed; default off (same-team hits filtered)

    if addrs is not None:
        try:
            dolphin.write_bytes(addrs["self_team_id"], bytes([team_id]))
            dolphin.write_bytes(addrs["self_friendly_fire"], bytes([friendly_fire]))
        except Exception:
            pass

    return addrs, team_id


def _on_ghost_disconnect(ctx) -> None:
    ctx._ghost_subscribed = False
    ctx._ghost_peers = {}
    ctx._vlink = None
    addrs = getattr(ctx, "_ghost_addrs", None)
    if addrs is not None:
        try:
            dolphin.write_bytes(addrs["peer_block"], Ghosts.CLEAR_MAGIC)
        except Exception:
            pass

def _peer_index_to_ap_slot(ctx, peer_index: int) -> typing.Optional[int]:
    peers = getattr(ctx, "_ghost_peers", None) or {}
    sorted_keys = sorted(peers.keys())
    if peer_index < 0 or peer_index >= len(sorted_keys):
        return None
    try:
        return Ghosts.slot_from_key(sorted_keys[peer_index])
    except (ValueError, IndexError):
        return None


def _peer_index_to_cid(ctx, peer_index: int) -> typing.Optional[int]:
    peers = getattr(ctx, "_ghost_peers", None) or {}
    sorted_keys = sorted(peers.keys())
    if peer_index < 0 or peer_index >= len(sorted_keys):
        return None
    try:
        return Ghosts.cid_from_key(sorted_keys[peer_index])
    except (ValueError, IndexError):
        return None

async def _drain_outbound_hits(ctx) -> None:
    if ctx.team is None or ctx.slot is None:
        return
    if not _resolve_ghost_addresses(ctx):
        return
    outbound_addr = ctx._ghost_addrs["outbound_hit"]
    try:
        word = dolphin.read_word(outbound_addr)
    except Exception:
        return
    if word == 0:
        return

    kind = (word >> 24) & 0xFF
    peer_index = (word >> 16) & 0xFF

    try:
        dolphin.write_word(outbound_addr, 0)
    except Exception:
        pass

    if kind != HIT_KIND_HAMMER:

        return

    target_slot = _peer_index_to_ap_slot(ctx, peer_index)
    target_cid = _peer_index_to_cid(ctx, peer_index)
    if target_slot is None:

        logger.debug(
            f"hit peer index {peer_index} doesn't resolve to an AP slot; "
            f"playing local stagger as a single-client loopback"
        )
        _on_inbound_hit(ctx, {"ttyd_hit": True, "kind": "hammer", "from": ctx.slot})
        return

    my_cid = _vlink_state(ctx)["cid"]
    try:
        await ctx.send_msgs([{
            "cmd":   "Bounce",
            "slots": [target_slot],
            "data":  {
                "ttyd_hit": True,
                "from":     ctx.slot,
                "from_cid": my_cid,
                "to_cid":   target_cid,
                "kind":     "hammer",
            },
        }])
    except Exception:
        logger.exception("failed to send hammer hit Bounce")

def _on_inbound_hit(ctx, data: dict) -> None:
    if not getattr(ctx, "_ghost_multiplayer", True):
        return
    if getattr(ctx, "_ghost_hammer_optout", False):
        return

    to_cid = data.get("to_cid")
    if to_cid is not None and to_cid != _vlink_state(ctx)["cid"]:
        return

    kind = data.get("kind")
    if kind == "hammer":
        kind_code = HIT_KIND_HAMMER
    else:
        return

    if not _resolve_ghost_addresses(ctx):
        logger.debug("inbound hit dropped: ghost-state container not yet resolved")
        return

    try:
        dolphin.write_word(ctx._ghost_addrs["pending_hit"], (kind_code & 0xFF) << 24)
    except Exception:
        logger.exception("failed to write inbound hit to mod scratch")

GHOST_RENDER_INTERVAL_S = 1.0 / 60.0


def _read_self_active_loops(ctx) -> list:
    addrs = getattr(ctx, "_ghost_addrs", None)
    if addrs is None:
        if not _resolve_ghost_addresses(ctx):
            return []
        addrs = ctx._ghost_addrs

    try:
        count_b = dolphin.read_bytes(addrs["self_active_loop_count"], 1)
        if not count_b:
            return []
        count = count_b[0]
        if count > Ghosts.ACTIVE_LOOPS_PER_PEER:
            count = Ghosts.ACTIVE_LOOPS_PER_PEER
        if count == 0:
            return []
        entries_b = dolphin.read_bytes(
            addrs["self_active_loops"],
            Ghosts.ACTIVE_LOOPS_PER_PEER * 2)
        if not entries_b or len(entries_b) < count * 2:
            return []
        loops = []
        for i in range(count):
            sid = (entries_b[i*2] << 8) | entries_b[i*2 + 1]
            if sid != 0:
                loops.append(sid)
        return loops
    except Exception:
        return []


VL_SAMPLE_INTERVAL_S    = 1.0 / 20.0
VL_MOVE_INTERVAL_S      = 0.20
VL_PRESENCE_KEEPALIVE_S = 5.0
VL_INTERP_DELAY_S       = 0.20
VL_EXTRAP_CAP_S         = 0.0
VL_PLAYBACK_BUFFER_S    = 1.5
VL_HISTORY_S            = 1.5
VL_PRESENCE_TIMEOUT_S   = 13.0
VL_OVERLAP_SAMPLES      = 2


def _vlink_state(ctx):
    s = getattr(ctx, "_vlink", None)
    if s is None:
        s = {
            "cid": uuid.uuid4().int & 0xFFFFFFFFFFFFFFFF,
            "samples": [],
            "sent_t": -1.0,
            "last_sample_t": 0.0,
            "last_move_t": 0.0,
            "last_presence_t": 0.0,
            "last_room": None,
            "force_presence": False,
            "pending_sfx": [],
            "last_loops": None,
            "last_discrete": None,
            "peers": {},
            "known": set(),
        }
        ctx._vlink = s
    return s


def _vlink_player_slots(ctx) -> list:
    out = []
    for slot_id, info in (ctx.slot_info or {}).items():
        if slot_id == 0 or slot_id == ctx.slot:
            continue
        if info.type != SlotType.player:
            continue
        out.append(slot_id)
    return out


def _vlink_discrete(ctx, state: dict, team_id: int, active_loops: list, sfx_events: list) -> dict:
    own_name = ""
    try:
        own_name = (ctx.player_names.get(ctx.slot, "") or "")[:16]
    except Exception:
        pass
    override = getattr(ctx, "_ghost_display_name", None)
    if override:
        own_name = override[:16]
    optout = 1 if getattr(ctx, "_ghost_hammer_optout", False) else 0
    grace = 0
    addrs = getattr(ctx, "_ghost_addrs", None)
    if addrs is not None:
        try:
            gb = dolphin.read_bytes(addrs["hit_grace"], 1)
            if gb and gb[0] != 0:
                grace = 1
        except Exception:
            pass
    d = {
        "anim": state.get("anim", ""),
        "flags1": int(state.get("flags1", 1)),
        "flags2": int(state.get("flags2", 0)),
        "flags3": int(state.get("flags3", 0)),
        "motion_id": int(state.get("motion_id", 0)),
        "color_index": int(state.get("color_index", 0)),
        "motion_timer": int(state.get("motion_timer", 0)),
        "camera_angle": round(float(state.get("camera_angle", 0.0)), 2),
        "rot_pivot_x": round(float(state.get("rot_pivot_x", 0.0)), 2),
        "rot_pivot_y": round(float(state.get("rot_pivot_y", 0.0)), 2),
        "rot_pivot_z": round(float(state.get("rot_pivot_z", 0.0)), 2),
        "scale_x": round(float(state.get("scale_x", 1.0)), 3),
        "scale_y": round(float(state.get("scale_y", 1.0)), 3),
        "scale_z": round(float(state.get("scale_z", 1.0)), 3),
        "stretch_y": round(float(state.get("stretch_y", 1.0)), 3),
        "paper_agb": state.get("paper_agb", ""),
        "paper_anim": state.get("paper_anim", ""),
        "paper_local_time": round(float(state.get("paper_local_time", -1.0)), 3),
        "slot_name": own_name,
        "show_name": 1 if getattr(ctx, "_ghost_names_hidden", False) else 0,
        "hammerable": 1 if (optout or grace) else 0,
        "team_id": int(team_id),
        "active_loops": active_loops or [],
    }
    if sfx_events:
        d["sfx_events"] = sfx_events
    return d


def _vlink_discrete_signature(d: dict) -> tuple:
    return (
        d.get("anim", ""),
        d.get("flags1", 0), d.get("flags2", 0), d.get("flags3", 0),
        d.get("motion_id", 0),
        d.get("color_index", 0),
        d.get("scale_x", 1.0), d.get("scale_y", 1.0), d.get("scale_z", 1.0),
        d.get("stretch_y", 1.0),
        d.get("rot_pivot_x", 0.0), d.get("rot_pivot_y", 0.0), d.get("rot_pivot_z", 0.0),
        d.get("paper_agb", ""), d.get("paper_anim", ""),
        d.get("paper_local_time", -1.0),
        d.get("hammerable", 0), d.get("team_id", 0),
        d.get("show_name", 0), d.get("slot_name", ""),
    )


def _vlink_sample(ctx, state: dict, now: float) -> None:
    s = _vlink_state(ctx)
    smp = Ghosts.make_sample(now, state["x"], state["y"], state["z"],
                             state["rot_y"], state["rot_x"], state["rot_z"])
    buf = s["samples"]
    if buf and not Ghosts.samples_differ(smp, buf[-1]):
        return
    buf.append(smp)
    cutoff = now - VL_HISTORY_S
    while len(buf) > 2 and buf[1][0] < cutoff:
        buf.pop(0)


def _vlink_colocated_slots(ctx, my_map: str, now: float) -> list:
    if not my_map:
        return []
    s = _vlink_state(ctx)
    out = set()
    for cid, p in s["peers"].items():
        if (now - p.get("last_seen", 0.0)) > VL_PRESENCE_TIMEOUT_S:
            continue
        if p.get("map", "") == my_map:
            out.add(int(p.get("slot", 0)))
    return list(out)


async def _vlink_send_presence(ctx, state: dict, team_id: int, now: float) -> None:
    name = ""
    try:
        name = (ctx.player_names.get(ctx.slot, "") or "")[:16]
    except Exception:
        pass
    override = getattr(ctx, "_ghost_display_name", None)
    if override:
        name = override[:16]
    d = _vlink_discrete(ctx, state, team_id, _read_self_active_loops(ctx), [])
    payload = Ghosts.build_presence(ctx.slot, team_id, state.get("map", ""), name, d["hammerable"],
                                    _vlink_state(ctx)["cid"])
    payload["x"] = round(float(state["x"]), 2)
    payload["y"] = round(float(state["y"]), 2)
    payload["z"] = round(float(state["z"]), 2)
    payload["ry"] = round(float(state["rot_y"]), 1)
    payload["rx"] = round(float(state["rot_x"]), 1)
    payload["rz"] = round(float(state["rot_z"]), 1)
    payload["d"] = d
    try:
        await ctx.send_msgs([{"cmd": "Bounce", "tags": [Ghosts.VLINK_TAG], "data": payload}])
    except Exception:
        logger.exception("vlink presence send failed")


async def _vlink_send_part(ctx) -> None:
    if getattr(ctx, "slot", None) is None:
        return
    if not getattr(ctx, "_ghost_multiplayer", True):
        return
    try:
        await ctx.send_msgs([{"cmd": "Bounce", "tags": [Ghosts.VLINK_TAG],
                              "data": Ghosts.build_part(ctx.slot, _vlink_state(ctx)["cid"])}])
    except Exception:
        logger.debug("vlink part send failed (socket likely closed)")


async def _vlink_send_move(ctx, state: dict, team_id: int, targets: list, now: float) -> None:
    s = _vlink_state(ctx)
    buf = s["samples"]
    if not buf or not targets:
        return
    sent_t = s["sent_t"]
    new = [smp for smp in buf if smp[0] > sent_t]
    loops = _read_self_active_loops(ctx)
    loops_changed = (loops != s.get("last_loops"))

    d = _vlink_discrete(ctx, state, team_id, loops, [])
    sig = _vlink_discrete_signature(d)
    discrete_changed = (sig != s.get("last_discrete"))

    if not new and not s["pending_sfx"] and not loops_changed and not discrete_changed:
        return
    overlap = [smp for smp in buf if smp[0] <= sent_t][-VL_OVERLAP_SAMPLES:]
    batch = overlap + new
    if not batch:
        return
    sfx = s["pending_sfx"][:Ghosts.SFX_EVENTS_PER_SLOT]
    s["pending_sfx"] = s["pending_sfx"][Ghosts.SFX_EVENTS_PER_SLOT:]
    if sfx:
        d["sfx_events"] = sfx
    payload = Ghosts.build_move(ctx.slot, state.get("map", ""), d, batch, s["cid"])
    if new:
        s["sent_t"] = new[-1][0]
    s["last_loops"] = list(loops)
    s["last_discrete"] = sig
    try:
        await ctx.send_msgs([{"cmd": "Bounce", "slots": list(targets), "data": payload}])
    except Exception:
        logger.exception("vlink move send failed")


def vlink_force_presence(ctx) -> None:
    """Request an immediate presence broadcast on the next sync tick.
    Used by commands that change team / name visibility / hammerable so
    peers see the change without waiting for the keepalive."""
    _vlink_state(ctx)["force_presence"] = True


def _vlink_on_bounce(ctx, data: dict) -> None:
    """Dispatch an inbound VisionLink Bounce (presence or move) into the
    per-peer playback state. Safe to call for any Bounce; returns
    immediately if the payload isn't ours."""
    kind = data.get(Ghosts.VLINK_KIND)
    if kind is None:
        return
    try:
        slot = int(data.get("s"))
        cid = int(data.get("c", 0))
    except (TypeError, ValueError):
        return
    s = _vlink_state(ctx)
    if cid == s["cid"]:
        return
    if kind == Ghosts.VLINK_PART:
        s["peers"].pop(cid, None)
        s["known"].discard(cid)
        return
    now = asyncio.get_event_loop().time()
    peer = s["peers"].get(cid)
    if peer is None:
        peer = {"pb": Ghosts.PlaybackBuffer(VL_PLAYBACK_BUFFER_S),
                "discrete": {}, "map": "", "name": "", "team": 0,
                "slot": slot, "hammerable": 0, "last_seen": now}
        s["peers"][cid] = peer
    peer["slot"] = slot
    peer["last_seen"] = now

    if kind == Ghosts.VLINK_PRESENCE:
        peer["map"] = data.get("mp", "")
        peer["name"] = data.get("nm", "")
        peer["team"] = int(data.get("tm", 0))
        peer["hammerable"] = int(data.get("hm", 0))
        d = data.get("d") or {}
        if d:
            peer["discrete"] = d
        x = data.get("x")
        if x is not None:
            peer["pb"].append([Ghosts.make_sample(
                now, x, data.get("y", 0.0), data.get("z", 0.0),
                data.get("ry", 0.0), data.get("rx", 0.0), data.get("rz", 0.0))], now)
        if cid not in s["known"]:
            s["known"].add(cid)
            s["force_presence"] = True   # reply with our presence next tick
    elif kind == Ghosts.VLINK_MOVE:
        if data.get("mp"):
            peer["map"] = data.get("mp")
        d = data.get("d") or {}
        if d:
            peer["discrete"] = d
            peer["team"] = int(d.get("team_id", peer.get("team", 0)))
            peer["hammerable"] = int(d.get("hammerable", peer.get("hammerable", 0)))
        sm = data.get("sm") or []
        if sm:
            peer["pb"].append(sm, now)


def _vlink_playback(ctx, now: float) -> None:
    s = _vlink_state(ctx)
    render_time = now - VL_INTERP_DELAY_S
    out = {}
    dead = []
    for cid, peer in s["peers"].items():
        if (now - peer.get("last_seen", 0.0)) > VL_PRESENCE_TIMEOUT_S:
            dead.append(cid)
            continue
        pose = peer["pb"].sample(render_time, VL_EXTRAP_CAP_S)
        if pose is None:
            continue
        entry = dict(peer.get("discrete") or {})
        entry["map"] = peer.get("map", "")
        entry["x"], entry["y"], entry["z"] = pose[0], pose[1], pose[2]
        entry["rot_y"], entry["rot_x"], entry["rot_z"] = pose[3], pose[4], pose[5]
        entry.setdefault("team_id", peer.get("team", 0))
        entry.setdefault("hammerable", peer.get("hammerable", 0))
        if not entry.get("slot_name"):
            entry["slot_name"] = peer.get("name", "")
        Ghosts.stamp_peer(entry)
        out[Ghosts.ghost_key(peer.get("team", 0), peer.get("slot", 0), cid)] = entry
    for cid in dead:
        s["peers"].pop(cid, None)
        s["known"].discard(cid)
    ctx._ghost_peers = out


GHOST_TEST_CID = 0x7E57
GHOST_TEST_OFFSET = 100.0


def _inject_ghost_test(ctx, state: dict, team_id: int) -> None:
    if not getattr(ctx, "_ghost_test", False) or state is None:
        return
    entry = _vlink_discrete(ctx, state, team_id, _read_self_active_loops(ctx), [])
    entry["map"] = state.get("map", "")
    entry["x"] = float(state.get("x", 0.0)) + GHOST_TEST_OFFSET
    entry["y"] = float(state.get("y", 0.0))
    entry["z"] = float(state.get("z", 0.0))
    entry["rot_y"] = float(state.get("rot_y", 0.0))
    entry["rot_x"] = float(state.get("rot_x", 0.0))
    entry["rot_z"] = float(state.get("rot_z", 0.0))
    entry["team_id"] = int(team_id)
    if not entry.get("slot_name"):
        entry["slot_name"] = "TEST"
    Ghosts.stamp_peer(entry)
    peers = getattr(ctx, "_ghost_peers", None)
    if peers is None:
        peers = {}
        ctx._ghost_peers = peers
    peers[Ghosts.ghost_key(team_id, ctx.slot or 0, GHOST_TEST_CID)] = entry


async def ttyd_ghost_sync_task(ctx):
    while not ctx.exit_event.is_set():
        await asyncio.sleep(GHOST_RENDER_INTERVAL_S)

        if not (dolphin.is_hooked() and ctx.dolphin_connected):
            continue
        if ctx.team is None or ctx.slot is None:
            continue
        try:
            in_game = ctx.save_loaded()
        except Exception:
            in_game = False
        if not in_game:
            continue

        if not getattr(ctx, "_ghost_multiplayer", True):
            continue

        try:
            await _drain_outbound_hits(ctx)
        except Exception:
            logger.exception("ghost outbound-hit drain error")

        _, team_id = _publish_ghost_state_scratch(ctx)
        now = asyncio.get_event_loop().time()
        s = _vlink_state(ctx)

        state = _read_self_state(ctx)
        if state is not None:
            if now - s["last_sample_t"] >= VL_SAMPLE_INTERVAL_S:
                s["last_sample_t"] = now
                _vlink_sample(ctx, state, now)

            my_map = state.get("map", "")

            try:
                ring = await _drain_sfx_ring(ctx)
            except Exception:
                ring = []
            if ring and _vlink_colocated_slots(ctx, my_map, now):
                s["pending_sfx"].extend(ring)
                _cap = Ghosts.SFX_EVENTS_PER_SLOT * 8
                if len(s["pending_sfx"]) > _cap:
                    s["pending_sfx"] = s["pending_sfx"][-_cap:]

            room_changed = (my_map != s["last_room"])
            if (room_changed or s.get("force_presence")
                    or now - s["last_presence_t"] >= VL_PRESENCE_KEEPALIVE_S):
                s["last_presence_t"] = now
                s["last_room"] = my_map
                s["force_presence"] = False
                try:
                    await _vlink_send_presence(ctx, state, team_id, now)
                except Exception:
                    logger.exception("vlink presence error")

            if now - s["last_move_t"] >= VL_MOVE_INTERVAL_S:
                s["last_move_t"] = now
                colo = _vlink_colocated_slots(ctx, my_map, now)
                if colo:
                    try:
                        await _vlink_send_move(ctx, state, team_id, colo, now)
                    except Exception:
                        logger.exception("vlink move error")

        _vlink_playback(ctx, now)
        _inject_ghost_test(ctx, state, team_id)

        try:
            _write_peer_block(ctx)
        except Exception:
            logger.exception("ghost render tick error")
