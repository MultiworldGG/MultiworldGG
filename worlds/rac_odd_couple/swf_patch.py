"""
Patches the 6 scene navigation buttons in the vanilla odd_couple.swf with a
LoadVars-based API check, so the locally running backend (see client/backend.py)
can suppress/enable them per-item. This is a byte-for-byte port of the
standalone patch_swf.py script from the Odd Couple project, reworked to
operate on in-memory bytes instead of files so it can run as part of AP's
generate_output step.
"""
from __future__ import annotations

import struct

BUTTON_SCENES = {
    193: "stereo",
    194: "taxiDriver",
    195: "gimp",
    286: "phonecall1",
    294: "scissors",
    309: "tv",
}

API_BASE = "http://127.0.0.1:8000"


# ---------------------------------------------------------------------------
# AS1 bytecode helpers
# ---------------------------------------------------------------------------

def push_string(s: str) -> bytes:
    payload = b"\x00" + s.encode("latin-1") + b"\x00"  # type 0 = string
    return bytes([0x96]) + struct.pack("<H", len(payload)) + payload


def push_int(n: int) -> bytes:
    payload = b"\x07" + struct.pack("<I", n & 0xFFFFFFFF)  # type 7 = integer
    return bytes([0x96]) + struct.pack("<H", len(payload)) + payload


def build_press_bytecode(scene: str) -> bytes:
    """
    Compile the AS1 bytecode for the patched on(press) handler.
    Bytecode equivalent to:
        var lv = new LoadVars();
        lv.onLoad = function(ok) { if (ok) { _root.jumpScene(scene); } };
        lv.load(API_BASE + "/api/check?scene=" + scene);
    """
    check_url = f"{API_BASE}/api/check?scene={scene}"
    received_url = f"{API_BASE}/api/received?scene={scene}"

    # fire-and-forget second LoadVars to /api/received after jumpScene
    # ActionDefineLocal pops Value (top of stack) then Name, so the name must
    # be pushed *before* the value-producing sequence, not after it.
    notify_received = (
        push_string("lv2")
        + push_int(0)                 # num_args = 0
        + push_string("LoadVars")
        + bytes([0x40])             # ActionNewObject -> pushes new LoadVars() above "lv2"
        + bytes([0x3c])             # ActionDefineLocal: pops value(object), then name("lv2")
        + push_string(received_url)
        + push_int(1)               # num_args = 1
        + push_string("lv2")
        + bytes([0x1c])             # ActionGetVariable
        + push_string("load")
        + bytes([0x52])             # ActionCallMethod
        + bytes([0x17])             # ActionPop
    )

    # -- function body: if(ok){ _root.jumpScene(scene); lv2.load(received_url); } --
    jump_body = (
        push_string(scene)          # arg: scene name
        + push_int(1)               # num_args = 1
        + push_string("_root")
        + bytes([0x1c])             # ActionGetVariable  -> _root on stack
        + push_string("jumpScene")  # method name
        + bytes([0x52])             # ActionCallMethod
        + bytes([0x17])             # ActionPop
        + notify_received
    )

    # if (!ok) jump past jump_body
    if_header = (
        push_string("ok")
        + bytes([0x1c])             # ActionGetVariable  -> ok value on stack
        + bytes([0x12])             # ActionNot
        + bytes([0x9d])             # ActionIf
        + struct.pack("<H", 2)      # payload length = 2
        + struct.pack("<h", len(jump_body))  # signed offset
    )

    func_body = if_header + jump_body  # no ActionReturn needed; end of func

    # -- ActionDefineFunction("", ["ok"]) { func_body } --
    func_payload = (
        b"\x00"                     # function name = "" (empty)
        + struct.pack("<H", 1)      # num_params = 1
        + b"ok\x00"                 # param name
        + struct.pack("<H", len(func_body))  # body size
    )
    define_func = (
        bytes([0x9b])
        + struct.pack("<H", len(func_payload))
        + func_payload
        + func_body
    )

    # -- Step 1: var lv = new LoadVars() --
    # Same ordering requirement as notify_received above: name pushed first,
    # then the value (the new object) ends up on top for ActionDefineLocal.
    new_loadvars = (
        push_string("lv")
        + push_int(0)                 # num_args = 0
        + push_string("LoadVars")   # class name
        + bytes([0x40])             # ActionNewObject -> pushes new LoadVars() above "lv"
        + bytes([0x3c])             # ActionDefineLocal: pops value(object), then name("lv")
    )

    # -- Step 2: lv.onLoad = function(ok){...} --
    set_onload = (
        push_string("lv")
        + bytes([0x1c])             # ActionGetVariable  -> lv on stack
        + push_string("onLoad")     # member name
        + define_func               # function value
        + bytes([0x4f])             # ActionSetMember
    )

    # -- Step 3: lv.load(url) --
    call_load = (
        push_string(check_url)
        + push_int(1)               # num_args = 1
        + push_string("lv")
        + bytes([0x1c])             # ActionGetVariable
        + push_string("load")
        + bytes([0x52])             # ActionCallMethod
        + bytes([0x17])             # ActionPop
    )

    return new_loadvars + set_onload + call_load + bytes([0x00])  # ActionEnd


# ---------------------------------------------------------------------------
# SWF tag parsing / rebuilding
# ---------------------------------------------------------------------------

def skip_rect(data: bytes, pos: int) -> int:
    nbits = (data[pos] >> 3) & 0x1F
    total_bits = 5 + nbits * 4
    return pos + (total_bits + 7) // 8


def iter_tags(data: bytes, start: int):
    """Yield (tag_type, tag_data, header_start, data_start, long_form) for each tag."""
    pos = start
    while pos < len(data) - 1:
        hdr_start = pos
        header = struct.unpack_from("<H", data, pos)[0]
        tag_type = header >> 6
        tag_len = header & 0x3F
        pos += 2
        long_form = False
        if tag_len == 0x3F:
            tag_len = struct.unpack_from("<I", data, pos)[0]
            pos += 4
            long_form = True
        data_start = pos
        tag_data = data[pos: pos + tag_len]
        yield tag_type, tag_data, hdr_start, data_start, long_form
        if tag_type == 0:
            break
        pos += tag_len


def encode_tag(tag_type: int, tag_data: bytes) -> bytes:
    """Encode a SWF tag with correct (possibly long-form) header."""
    if len(tag_data) < 0x3F:
        header = (tag_type << 6) | len(tag_data)
        return struct.pack("<H", header) + tag_data
    else:
        header = (tag_type << 6) | 0x3F
        return struct.pack("<H", header) + struct.pack("<I", len(tag_data)) + tag_data


def parse_button2_actions(tag_data: bytes):
    """Return (button_id, flags, btn_records_bytes, list_of_(next_off, cond, action_bytes))."""
    btn_id = struct.unpack_from("<H", tag_data, 0)[0]
    flags = tag_data[2]
    first_offset = struct.unpack_from("<H", tag_data, 3)[0]

    btn_records_end = first_offset + 3  # first_offset is relative to byte 3
    btn_records = tag_data[5:btn_records_end]

    actions = []
    apos = btn_records_end
    while apos < len(tag_data):
        next_offset = struct.unpack_from("<H", tag_data, apos)[0]
        cond = struct.unpack_from("<H", tag_data, apos + 2)[0]
        if next_offset == 0:
            action_bytes = tag_data[apos + 4:]
        else:
            action_bytes = tag_data[apos + 4: apos + next_offset]
        actions.append((next_offset, cond, action_bytes))
        if next_offset == 0:
            break
        apos += next_offset

    return btn_id, flags, btn_records, actions


def rebuild_button2_tag(btn_id: int, flags: int, btn_records: bytes, actions) -> bytes:
    """Re-encode a DefineButton2 tag from its components (next_offset recomputed)."""
    rebuilt_bcas = []
    for i, (_, cond, action_bytes) in enumerate(actions):
        bca_size = 4 + len(action_bytes)
        next_off = bca_size if i < len(actions) - 1 else 0
        rebuilt_bcas.append(struct.pack("<H", next_off) + struct.pack("<H", cond) + action_bytes)

    action_area = b"".join(rebuilt_bcas)
    first_offset = 2 + len(btn_records)  # 2 = the first_offset field itself

    tag_body = (
        struct.pack("<H", btn_id)
        + bytes([flags])
        + struct.pack("<H", first_offset)
        + btn_records
        + action_area
    )
    return encode_tag(34, tag_body)  # 34 = DefineButton2


# ---------------------------------------------------------------------------
# Main patcher
# ---------------------------------------------------------------------------

def patch_swf_bytes(raw: bytes) -> bytes:
    """Patch the 6 scene navigation buttons in odd_couple.swf and return the new bytes."""
    sig = raw[:3]

    if sig not in (b"FWS", b"CWS"):
        raise ValueError(f"Not a recognised SWF file (sig={sig!r})")
    if sig == b"CWS":
        import zlib
        raw = raw[:8] + zlib.decompress(raw[8:])

    pos = skip_rect(raw, 8)
    pos += 4  # skip frame-rate + frame-count
    tags_start = pos

    output_parts: list[bytes] = []
    patched = 0

    for tag_type, tag_data, hdr_start, data_start, long_form in iter_tags(raw, tags_start):
        if tag_type == 34 and len(tag_data) >= 5:
            btn_id = struct.unpack_from("<H", tag_data, 0)[0]
            if btn_id in BUTTON_SCENES:
                scene = BUTTON_SCENES[btn_id]
                btn_id_parsed, flags, btn_records, actions = parse_button2_actions(tag_data)

                new_actions = []
                for next_off, cond, action_bytes in actions:
                    if cond == 0x0004:  # on(press)
                        new_actions.append((0, cond, build_press_bytecode(scene)))
                        patched += 1
                    else:
                        new_actions.append((next_off, cond, action_bytes))

                output_parts.append(rebuild_button2_tag(btn_id_parsed, flags, btn_records, new_actions))
                continue

        original_tag_bytes = raw[hdr_start:data_start + len(tag_data)]
        output_parts.append(original_tag_bytes)

    if patched != len(BUTTON_SCENES):
        raise ValueError(f"Expected to patch {len(BUTTON_SCENES)} buttons, only patched {patched}. "
                         f"Is this the correct base odd_couple.swf?")

    tags_blob = b"".join(output_parts)
    body = raw[8:tags_start] + tags_blob
    new_len = 8 + len(body)

    header = raw[:4] + struct.pack("<I", new_len)
    return header + body
