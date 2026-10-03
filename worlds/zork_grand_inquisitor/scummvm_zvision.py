from typing import Dict, List, Optional, Sequence, Tuple

import ctypes
import math
import struct
import time
import zlib

import pymem.process
import pymem.ressources.kernel32
import pymem.ressources.structure

from pymem import Pymem


SCUMMVM_SIZE_OF_IMAGE: int = 0xC5A6000
SCUMMVM_FUNCTION_FINGERPRINT: int = 0xC9E020AC

SCUMMVM_FUNCTION_RVAS: Dict[str, int] = {
    "ManagedSurface::transBlitFrom": 0x388D650,
    "MenuZGI::process": 0x3556970,
    "RenderManager::setBackgroundPosition": 0x3550150,
    "RenderTable::generateRenderTable": 0x35558A0,
    "RenderTable::setPanoramaFoV": 0x3555C70,
    "RenderTable::setPanoramaReverse": 0x3555CF0,
    "RenderTable::setPanoramaScale": 0x3555CB0,
    "Screen::update": 0x38B1240,
    "ScriptManager::ChangeLocationReal": 0x3544950,
    "ScriptManager::changeLocation": 0x3543CC0,
    "ScriptManager::checkPuzzleCriteria": 0x3544440,
    "ScriptManager::getStateFlag": 0x3544000,
    "ScriptManager::getStateValue": 0x3543C30,
    "ScriptManager::inventoryDrop": 0x3556330,
    "ScriptManager::killSideFx": 0x3542640,
    "ScriptManager::queuePuzzles": 0x3543950,
    "ScriptManager::serialize": 0x35440A0,
    "ScriptManager::setStateFlag": 0x3543AB0,
    "ScriptManager::setStateValue": 0x3543BC0,
    "ScriptManager::unsetStateFlag": 0x3544360,
    "Surface::create": 0x38B5420,
    "Surface::fillRect": 0x38B5CF0,
    "TextRenderer::drawTextWithWordWrapping": 0x355F4D0,
}

SCUMMVM_FUNCTION_SIZES: Dict[str, int] = {
    "ScriptManager::serialize": 0x2B5,
}

SCUMMVM_GLOBAL_RVAS: Dict[str, int] = {
    "g_engine": 0x6F01718,
}

SCUMMVM_VIRTUAL_TABLE_RVAS: Dict[str, int] = {
    "MenuZGI": 0x6450C30,
}

SCUMMVM_VIRTUAL_TABLE_OFFSETS: Dict[str, int] = {
    "MenuManager::process": 0x28,
    "ResultAction::execute": 0x10,
}

ZVISION_ACTIONS: Dict[str, Tuple[int, int]] = {
    "add": (0x6450D80, 0x35637D0),
    "animplay": (0x6450910, 0x35640A0),
    "animpreload": (0x6450A30, 0x3564000),
    "animunload": (0x64509D0, 0x3564720),
    "assign": (0x644FE70, 0x3563820),
    "attenuate": (0x6450620, 0x35638B0),
    "change_location": (0x6450940, 0x3563A10),
    "crossfade": (0x6450650, 0x3563940),
    "cursor": (0x644FEA0, 0x35646D0),
    "delay_render": (0x6450760, 0x3563A50),
    "disable_control": (0x6450970, 0x3563A90),
    "display_message": (0x64509A0, 0x3563AB0),
    "dissolve": (0x64503D0, 0x3563880),
    "distort": (0x64500D0, 0x35643D0),
    "enable_control": (0x64508B0, 0x3563D00),
    "flush_mouse_events": (0x6450A00, 0x3563D20),
    "inventory": (0x6450680, 0x3563D50),
    "kill": (0x644F860, 0x3564490),
    "menu_bar_enable": (0x64508E0, 0x3563E30),
    "music": (0x644FB50, 0x3563E60),
    "pan_track": (0x6450400, 0x35644F0),
    "playpreload": (0x6450A90, 0x3564170),
    "preferences": (0x6450790, 0x3563F70),
    "quit": (0x644F890, 0x35641D0),
    "random": (0x644FED0, 0x35641F0),
    "region": (0x644FF00, 0x3565060),
    "restore_game": (0x64507C0, 0x3564240),
    "rotate_to": (0x6450430, 0x3564280),
    "set_partial_screen": (0x6450A60, 0x35642B0),
    "set_screen": (0x64506B0, 0x3564360),
    "stop": (0x644F8C0, 0x3564390),
    "streamvideo": (0x64507F0, 0x35649B0),
    "syncsound": (0x64506E0, 0x3564770),
    "timer": (0x644FB80, 0x35645C0),
    "ttytext": (0x6450100, 0x3564640),
    "universe_music": (0x644FB50, 0x3563E60),
}

SCUMMVM_DETOUR_PROLOGUES: Dict[str, bytes] = {
    "ScriptManager::checkPuzzleCriteria": bytes.fromhex("4157415641554154555756534883ec38"),
    "ScriptManager::queuePuzzles": bytes.fromhex("4154555756534883ec20448b9168020000"),
    "ScriptManager::setStateValue": bytes.fromhex("41554154534883ec204989cc89542448"),
    "ScriptManager::ChangeLocationReal": bytes.fromhex("4157415641554154555756534881ecd8000000"),
    "ScriptManager::getStateFlag": bytes.fromhex("534883ec20448b91280100004c8b8920010000"),
    "ScriptManager::getStateValue": bytes.fromhex("534883ec20448b91900000004c8b8988000000"),
    "Screen::update": bytes.fromhex("41554154555756534883ec48488d7170"),
}

ZVISION_MEMBER_OFFSETS: Dict[str, int] = {
    "MenuManager::_engine": 0x18,
    "RenderManager::_renderTable": 0x3F8,
    "RenderManager::_screen": 0x98,
    "RenderTable::_panoramaOptions.linearScale": 0x3C,
    "RenderTable::_panoramaOptions.reverse": 0x40,
    "RenderTable::_panoramaOptions.verticalFOV": 0x38,
    "RenderTable::_renderState": 0x28,
    "ScriptManager::_currentLocation": 0x400,
    "ScriptManager::_engine": 0x0,
    "ScriptManager::_nextLocation": 0x408,
    "ZVision::_renderManager": 0xC0,
    "ZVision::_resourcePixelFormat": 0x98,
    "ZVision::_scriptManager": 0xB8,
    "ZVision::_textRenderer": 0xD8,
    "ZVision::_videoIsPlaying": 0x1A2,
    "ZVision::_widescreen": 0x1A1,
}

ZVISION_STRUCTURE_OFFSETS: Dict[str, int] = {
    "ManagedSurface::w": 0x50,
}

ACTION_CLASSES: List[Tuple[int, int, Tuple[str, ...]]] = [
    (virtual_table, execute, tuple(name for name in sorted(ZVISION_ACTIONS) if ZVISION_ACTIONS[name][0] == virtual_table))
    for virtual_table, execute in sorted(set(ZVISION_ACTIONS.values()))
]

PUMP_CODE_OFFSET: int = 0x0000
COPY_CODE_OFFSET: int = 0x00C0
SNAPSHOT_CODE_OFFSET: int = 0x00D0
STATE_CHANGE_LOGGER_CODE_OFFSET: int = 0x0120
STATE_OVERRIDE_CODE_OFFSET: int = 0x01A0
LOCATION_CHANGE_CODE_OFFSET: int = 0x0220
CURRENT_PUZZLE_CODE_OFFSET: int = 0x0300
CURRENT_PUZZLE_TRAMPOLINE_OFFSET: int = 0x0340
ACTION_FILTER_CODE_OFFSET: int = 0x0360
FLAG_OVERRIDE_CODE_OFFSET: int = 0x03B0
FLAG_OVERRIDE_TRAMPOLINE_OFFSET: int = 0x0430
READ_OVERRIDE_CODE_OFFSET: int = 0x0460
READ_OVERRIDE_TRAMPOLINE_OFFSET: int = 0x04C0
OVERLAY_CODE_OFFSET: int = 0x04F0
ACTION_THUNKS_OFFSET: int = 0x0860
PATCH_STAGING_OFFSET: int = 0x0CC0
MAILBOX_OFFSET: int = 0x0CE0
STATE_CHANGE_DATA_OFFSET: int = 0x1100
ARRIVAL_DATA_OFFSET: int = 0x1110
STRING_REFERENCE_COUNT_OFFSET: int = 0x1120
ACTION_DATA_OFFSET: int = 0x1130
STATE_OVERRIDE_DATA_OFFSET: int = 0x1340
STATE_VALUE_REMAP_DATA_OFFSET: int = 0x1550
READ_OVERRIDE_DATA_OFFSET: int = 0x1650
LOCATION_REDIRECT_DATA_OFFSET: int = 0x1860
OVERLAY_DATA_OFFSET: int = 0x2070
OVERLAY_GAP_DATA_OFFSET: int = 0x2370
ARRIVAL_LOG_OFFSET: int = 0x2460
FLAG_OVERRIDE_DISABLED_OFFSET: int = 0x3460
FLAG_OVERRIDE_ENABLED_OFFSET: int = 0x4460
SNAPSHOT_KEYS_OFFSET: int = 0x5460
SNAPSHOT_VALUES_OFFSET: int = 0x9460
STATE_CHANGE_LOG_OFFSET: int = 0xD460
OVERLAY_TEXT_OFFSET: int = 0x2D460
CAVE_SIZE: int = 0x39460

CALL_RECORD_CAPACITY: int = 16
STATE_CHANGE_LOG_CAPACITY: int = 16384
STATE_OVERRIDE_CAPACITY: int = 64
STATE_VALUE_REMAP_CAPACITY: int = 15
FLAG_OVERRIDE_BITMAP_SIZE: int = 0x1000
READ_OVERRIDE_CAPACITY: int = 32
LOCATION_REDIRECT_CAPACITY: int = 128
ARRIVAL_LOG_CAPACITY: int = 256
SNAPSHOT_CAPACITY: int = 4096
ACTION_BLOCK_CAPACITY: int = 64
ACTION_THUNK_SIZE: int = 0x20
OVERLAY_CAPACITY: int = 6
OVERLAY_LAYER_SIZE: int = 0x80
OVERLAY_TEXT_LENGTH: int = 2047
OVERLAY_SCREEN_WIDTH: int = 640
OVERLAY_TRANSPARENT_COLOR: int = 0xFFFF

MAILBOX_MAGIC: int = 0x0D53495656505A41
MAILBOX_STATE_IDLE: int = 0
MAILBOX_STATE_PENDING: int = 1
MAILBOX_STATE_DONE: int = 2
MAILBOX_STATE_RUNNING: int = 3

THIS_SCRIPT_MANAGER: int = 1

DETOURS: List[Tuple[str, int]] = [
    ("ScriptManager::checkPuzzleCriteria", CURRENT_PUZZLE_CODE_OFFSET),
    ("ScriptManager::queuePuzzles", STATE_CHANGE_LOGGER_CODE_OFFSET),
    ("ScriptManager::setStateValue", STATE_OVERRIDE_CODE_OFFSET),
    ("ScriptManager::ChangeLocationReal", LOCATION_CHANGE_CODE_OFFSET),
    ("ScriptManager::getStateFlag", FLAG_OVERRIDE_CODE_OFFSET),
    ("ScriptManager::getStateValue", READ_OVERRIDE_CODE_OFFSET),
    ("Screen::update", OVERLAY_CODE_OFFSET),
]


def assemble(parts: Sequence) -> bytes:
    label_positions: Dict[str, int] = dict()
    position: int = 0

    part: object
    for part in parts:
        if isinstance(part, bytes):
            position += len(part)
        elif part[0] == "label":
            label_positions[part[1]] = position
        elif part[0] == "jump":
            position += len(part[1]) + 1
        elif part[0] == "near_jump":
            position += len(part[1]) + 4

    code: bytes = bytes()

    for part in parts:
        if isinstance(part, bytes):
            code += part
        elif part[0] == "jump":
            code += part[1] + struct.pack("<b", label_positions[part[2]] - (len(code) + len(part[1]) + 1))
        elif part[0] == "near_jump":
            code += part[1] + struct.pack("<i", label_positions[part[2]] - (len(code) + len(part[1]) + 4))

    return code


def absolute_jump(address: int) -> bytes:
    return b"\xFF\x25\x00\x00\x00\x00" + struct.pack("<Q", address)  # jmp [rip + 0] ; address


def build_pump_code(cave_address: int, module_base: int) -> bytes:
    return assemble([
        b"\x41\x54",  # push r12
        b"\x53",  # push rbx
        b"\x56",  # push rsi
        b"\x57",  # push rdi
        b"\x48\x83\xEC\x38",  # sub rsp, 0x38
        b"\x48\x89\xCB",  # mov rbx, rcx  ; menu
        b"\x48\x89\x54\x24\x30",  # mov [rsp + 0x30], rdx  ; delta time
        b"\x48\xBE" + struct.pack("<Q", cave_address + MAILBOX_OFFSET),  # mov rsi, mailbox

        b"\x48\x8B\x83" + struct.pack("<i", ZVISION_MEMBER_OFFSETS["MenuManager::_engine"]),  # mov rax, [rbx + engine]
        b"\x48\x8B\x80" + struct.pack("<i", ZVISION_MEMBER_OFFSETS["ZVision::_scriptManager"]),  # mov rax, [rax + script manager]
        b"\x48\x89\x46\x18",  # mov [rsi + 0x18], rax  ; live script manager
        b"\x48\xFF\x46\x10",  # inc qword [rsi + 0x10]  ; frame count

        b"\x83\x3E" + struct.pack("<b", MAILBOX_STATE_PENDING),  # cmp dword [rsi], pending
        ("near_jump", b"\x0F\x85", "done"),  # jne done

        b"\xC7\x06" + struct.pack("<i", MAILBOX_STATE_RUNNING),  # mov dword [rsi], running
        b"\x44\x8B\x66\x04",  # mov r12d, [rsi + 0x04]  ; call count
        b"\x48\x8D\x7E\x20",  # lea rdi, [rsi + 0x20]  ; first call record

        ("label", "next_call"),
        b"\x45\x85\xE4",  # test r12d, r12d
        ("jump", b"\x74", "finished"),  # je finished
        b"\x48\x8B\x4F\x08",  # mov rcx, [rdi + 0x08]  ; this
        b"\x48\x83\xF9" + struct.pack("<b", THIS_SCRIPT_MANAGER),  # cmp rcx, script manager sentinel
        ("jump", b"\x75", "not_script_manager"),  # jne not_script_manager
        b"\x48\x8B\x4E\x18",  # mov rcx, [rsi + 0x18]  ; live script manager
        ("label", "not_script_manager"),
        b"\x48\x8B\x57\x10",  # mov rdx, [rdi + 0x10]  ; argument 1
        b"\x4C\x8B\x47\x18",  # mov r8, [rdi + 0x18]  ; argument 2
        b"\x4C\x8B\x4F\x20",  # mov r9, [rdi + 0x20]  ; argument 3
        b"\x66\x48\x0F\x6E\xCA",  # movq xmm1, rdx  ; argument 1 as float
        b"\x66\x49\x0F\x6E\xD0",  # movq xmm2, r8  ; argument 2 as float
        b"\x66\x49\x0F\x6E\xD9",  # movq xmm3, r9  ; argument 3 as float
        b"\x48\x8B\x47\x28",  # mov rax, [rdi + 0x28]
        b"\x48\x89\x44\x24\x20",  # mov [rsp + 0x20], rax  ; argument 4
        b"\x48\x8B\x47\x30",  # mov rax, [rdi + 0x30]
        b"\x48\x89\x44\x24\x28",  # mov [rsp + 0x28], rax  ; argument 5
        b"\xFF\x17",  # call [rdi]  ; function
        b"\x48\x89\x47\x38",  # mov [rdi + 0x38], rax  ; result
        b"\x48\x83\xC7\x40",  # add rdi, 0x40  ; next call record
        b"\x41\xFF\xCC",  # dec r12d
        ("jump", b"\xEB", "next_call"),  # jmp next_call

        ("label", "finished"),
        b"\xC7\x06" + struct.pack("<i", MAILBOX_STATE_DONE),  # mov dword [rsi], done

        ("label", "done"),
        b"\x48\x89\xD9",  # mov rcx, rbx  ; menu
        b"\x48\x8B\x54\x24\x30",  # mov rdx, [rsp + 0x30]  ; delta time
        b"\x48\xB8" + struct.pack("<Q", module_base + SCUMMVM_FUNCTION_RVAS["MenuZGI::process"]),  # mov rax, original MenuZGI::process
        b"\x48\x83\xC4\x38",  # add rsp, 0x38
        b"\x5F",  # pop rdi
        b"\x5E",  # pop rsi
        b"\x5B",  # pop rbx
        b"\x41\x5C",  # pop r12
        b"\xFF\xE0",  # jmp rax
    ])


def build_copy_code() -> bytes:
    return assemble([
        b"\x56",  # push rsi
        b"\x57",  # push rdi
        b"\x48\x89\xCF",  # mov rdi, rcx  ; destination
        b"\x48\x89\xD6",  # mov rsi, rdx  ; source
        b"\x4C\x89\xC1",  # mov rcx, r8  ; length
        b"\xF3\xA4",  # rep movsb
        b"\x5F",  # pop rdi
        b"\x5E",  # pop rsi
        b"\xC3",  # ret
    ])


def build_snapshot_code() -> bytes:
    return assemble([
        b"\x41\x54",  # push r12
        b"\x41\x55",  # push r13
        b"\x41\x56",  # push r14
        b"\x41\x57",  # push r15
        b"\x53",  # push rbx
        b"\x48\x8B\x44\x24\x50",  # mov rax, [rsp + 0x50]  ; getter
        b"\x48\x83\xEC\x20",  # sub rsp, 0x20
        b"\x48\x89\xCB",  # mov rbx, rcx  ; script manager
        b"\x49\x89\xD4",  # mov r12, rdx  ; keys
        b"\x4D\x89\xC5",  # mov r13, r8  ; count
        b"\x4D\x89\xCE",  # mov r14, r9  ; values
        b"\x49\x89\xC7",  # mov r15, rax  ; getter

        ("label", "next_key"),
        b"\x4D\x85\xED",  # test r13, r13
        ("jump", b"\x74", "done"),  # je done
        b"\x48\x89\xD9",  # mov rcx, rbx  ; script manager
        b"\x41\x8B\x14\x24",  # mov edx, [r12]  ; key
        b"\x41\xFF\xD7",  # call r15  ; getter
        b"\x41\x89\x06",  # mov [r14], eax  ; value
        b"\x49\x83\xC4\x04",  # add r12, 4
        b"\x49\x83\xC6\x04",  # add r14, 4
        b"\x49\xFF\xCD",  # dec r13
        ("jump", b"\xEB", "next_key"),  # jmp next_key

        ("label", "done"),
        b"\x48\x83\xC4\x20",  # add rsp, 0x20
        b"\x5B",  # pop rbx
        b"\x41\x5F",  # pop r15
        b"\x41\x5E",  # pop r14
        b"\x41\x5D",  # pop r13
        b"\x41\x5C",  # pop r12
        b"\xC3",  # ret
    ])


def build_state_change_logger_code(cave_address: int, module_base: int) -> bytes:
    return assemble([
        b"\x51",  # push rcx  ; script manager
        b"\x52",  # push rdx  ; key
        b"\x41\x50",  # push r8
        b"\x41\x51",  # push r9
        b"\x48\x83\xEC\x28",  # sub rsp, 0x28
        b"\x48\xB8" + struct.pack("<Q", module_base + SCUMMVM_FUNCTION_RVAS["ScriptManager::getStateValue"]),  # mov rax, getStateValue
        b"\xFF\xD0",  # call rax  ; value
        b"\x8B\x54\x24\x38",  # mov edx, [rsp + 0x38]  ; key
        b"\x49\xBA" + struct.pack("<Q", cave_address + STATE_CHANGE_DATA_OFFSET),  # mov r10, state change data
        b"\x45\x8B\x1A",  # mov r11d, [r10]  ; log count
        b"\x44\x89\xD9",  # mov ecx, r11d
        b"\x81\xE1" + struct.pack("<i", STATE_CHANGE_LOG_CAPACITY - 1),  # and ecx, log capacity - 1
        b"\x49\xB9" + struct.pack("<Q", cave_address + STATE_CHANGE_LOG_OFFSET),  # mov r9, state change log
        b"\x41\x89\x14\xC9",  # mov [r9 + rcx*8], edx  ; key
        b"\x41\x89\x44\xC9\x04",  # mov [r9 + rcx*8 + 4], eax  ; value
        b"\x41\xFF\xC3",  # inc r11d
        b"\x45\x89\x1A",  # mov [r10], r11d  ; log count
        b"\x48\x83\xC4\x28",  # add rsp, 0x28
        b"\x41\x59",  # pop r9
        b"\x41\x58",  # pop r8
        b"\x5A",  # pop rdx
        b"\x59",  # pop rcx
        SCUMMVM_DETOUR_PROLOGUES["ScriptManager::queuePuzzles"],  # original prologue
        absolute_jump(module_base + SCUMMVM_FUNCTION_RVAS["ScriptManager::queuePuzzles"] + len(SCUMMVM_DETOUR_PROLOGUES["ScriptManager::queuePuzzles"])),
    ])


def build_state_override_code(cave_address: int, module_base: int) -> bytes:
    return assemble([
        b"\x49\xBA" + struct.pack("<Q", cave_address + STATE_OVERRIDE_DATA_OFFSET),  # mov r10, state override data
        b"\x45\x8B\x1A",  # mov r11d, [r10]  ; override count
        b"\x31\xC0",  # xor eax, eax

        ("label", "next_override"),
        b"\x44\x39\xD8",  # cmp eax, r11d
        ("jump", b"\x7D", "overrides_done"),  # jge overrides_done
        b"\x41\x3B\x54\xC2\x08",  # cmp edx, [r10 + rax*8 + 0x08]  ; overridden key
        ("jump", b"\x75", "skip"),  # jne skip
        b"\x45\x8B\x44\xC2\x0C",  # mov r8d, [r10 + rax*8 + 0x0C]  ; forced value
        ("jump", b"\xEB", "overrides_done"),  # jmp overrides_done

        ("label", "skip"),
        b"\xFF\xC0",  # inc eax
        ("jump", b"\xEB", "next_override"),  # jmp next_override

        ("label", "overrides_done"),
        b"\x49\xBA" + struct.pack("<Q", cave_address + STATE_VALUE_REMAP_DATA_OFFSET),  # mov r10, state value remap data
        b"\x45\x8B\x1A",  # mov r11d, [r10]  ; remap count
        b"\x41\xC1\xE3\x04",  # shl r11d, 4  ; remap table size
        b"\x31\xC0",  # xor eax, eax

        ("label", "next_remap"),
        b"\x44\x39\xD8",  # cmp eax, r11d
        ("jump", b"\x7D", "done"),  # jge done
        b"\x41\x3B\x54\x02\x08",  # cmp edx, [r10 + rax + 0x08]  ; first key
        ("jump", b"\x7C", "skip_remap"),  # jl skip_remap
        b"\x41\x3B\x54\x02\x0C",  # cmp edx, [r10 + rax + 0x0C]  ; last key
        ("jump", b"\x7F", "skip_remap"),  # jg skip_remap
        b"\x45\x3B\x44\x02\x10",  # cmp r8d, [r10 + rax + 0x10]  ; original value
        ("jump", b"\x75", "skip_remap"),  # jne skip_remap
        b"\x45\x8B\x44\x02\x14",  # mov r8d, [r10 + rax + 0x14]  ; replacement value
        ("jump", b"\xEB", "done"),  # jmp done

        ("label", "skip_remap"),
        b"\x83\xC0\x10",  # add eax, 0x10
        ("jump", b"\xEB", "next_remap"),  # jmp next_remap

        ("label", "done"),
        SCUMMVM_DETOUR_PROLOGUES["ScriptManager::setStateValue"],  # original prologue
        absolute_jump(module_base + SCUMMVM_FUNCTION_RVAS["ScriptManager::setStateValue"] + len(SCUMMVM_DETOUR_PROLOGUES["ScriptManager::setStateValue"])),
    ])


def build_flag_override_code(cave_address: int, module_base: int) -> bytes:
    return assemble([
        b"\x48\x8B\x04\x24",  # mov rax, [rsp]  ; return address
        b"\x49\xBA" + struct.pack("<Q", module_base + SCUMMVM_FUNCTION_RVAS["ScriptManager::serialize"]),  # mov r10, serialize
        b"\x4C\x39\xD0",  # cmp rax, r10
        ("jump", b"\x72", "override"),  # jb override
        b"\x49\x81\xC2" + struct.pack("<i", SCUMMVM_FUNCTION_SIZES["ScriptManager::serialize"]),  # add r10, serialize size
        b"\x4C\x39\xD0",  # cmp rax, r10
        ("jump", b"\x72", "pass_through"),  # jb pass_through

        ("label", "override"),
        b"\x48\x83\xEC\x28",  # sub rsp, 0x28
        b"\x89\x54\x24\x20",  # mov [rsp + 0x20], edx  ; key
        b"\x48\xB8" + struct.pack("<Q", cave_address + FLAG_OVERRIDE_TRAMPOLINE_OFFSET),  # mov rax, original getStateFlag
        b"\xFF\xD0",  # call rax
        b"\x8B\x54\x24\x20",  # mov edx, [rsp + 0x20]
        b"\x48\x83\xC4\x28",  # add rsp, 0x28
        b"\x81\xFA" + struct.pack("<i", 8 * FLAG_OVERRIDE_BITMAP_SIZE),  # cmp edx, bitmap bits
        ("jump", b"\x73", "done"),  # jae done
        b"\x49\xBA" + struct.pack("<Q", cave_address + FLAG_OVERRIDE_DISABLED_OFFSET),  # mov r10, forced disabled bitmap
        b"\x41\x0F\xA3\x12",  # bt [r10], edx
        ("jump", b"\x73", "check_enabled"),  # jnc check_enabled
        b"\x83\xC8\x02",  # or eax, 2  ; DISABLED
        b"\xC3",  # ret

        ("label", "check_enabled"),
        b"\x49\xBA" + struct.pack("<Q", cave_address + FLAG_OVERRIDE_ENABLED_OFFSET),  # mov r10, forced enabled bitmap
        b"\x41\x0F\xA3\x12",  # bt [r10], edx
        ("jump", b"\x73", "done"),  # jnc done
        b"\x83\xE0\xFD",  # and eax, ~2  ; not DISABLED

        ("label", "done"),
        b"\xC3",  # ret

        ("label", "pass_through"),
        b"\x48\xB8" + struct.pack("<Q", cave_address + FLAG_OVERRIDE_TRAMPOLINE_OFFSET),  # mov rax, original getStateFlag
        b"\xFF\xE0",  # jmp rax
    ])


def build_location_change_code(cave_address: int, module_base: int) -> bytes:
    current_location: int = ZVISION_MEMBER_OFFSETS["ScriptManager::_currentLocation"]
    next_location: int = ZVISION_MEMBER_OFFSETS["ScriptManager::_nextLocation"]

    return assemble([
        b"\x49\xBA" + struct.pack("<Q", cave_address + LOCATION_REDIRECT_DATA_OFFSET),  # mov r10, location redirect data
        b"\x8B\x81" + struct.pack("<i", next_location),  # mov eax, [rcx + next location]
        b"\x84\xD2",  # test dl, dl  ; is loading
        ("near_jump", b"\x0F\x85", "log"),  # jne log

        b"\x53",  # push rbx
        b"\x56",  # push rsi
        b"\x45\x8B\x1A",  # mov r11d, [r10]  ; redirect count
        b"\x8B\xB1" + struct.pack("<i", current_location),  # mov esi, [rcx + current location]
        b"\x31\xDB",  # xor ebx, ebx

        ("label", "next_redirect"),
        b"\x44\x39\xDB",  # cmp ebx, r11d
        ("jump", b"\x7D", "restore"),  # jge restore
        b"\x41\x89\xD8",  # mov r8d, ebx
        b"\x41\xC1\xE0\x04",  # shl r8d, 4  ; redirect entry size
        b"\x43\x3B\x44\x02\x0C",  # cmp eax, [r10 + r8 + 0x0C]  ; redirected destination
        ("jump", b"\x75", "skip"),  # jne skip
        b"\x47\x8B\x4C\x02\x08",  # mov r9d, [r10 + r8 + 0x08]  ; required origin
        b"\x45\x85\xC9",  # test r9d, r9d
        ("jump", b"\x74", "redirect"),  # je redirect  ; any origin
        b"\x41\x39\xF1",  # cmp r9d, esi
        ("jump", b"\x75", "skip"),  # jne skip

        ("label", "redirect"),
        b"\x47\x8B\x4C\x02\x10",  # mov r9d, [r10 + r8 + 0x10]  ; new destination
        b"\x44\x89\x89" + struct.pack("<i", next_location),  # mov [rcx + next location], r9d
        b"\x47\x8B\x4C\x02\x14",  # mov r9d, [r10 + r8 + 0x14]  ; new offset
        b"\x44\x89\x89" + struct.pack("<i", next_location + 4),  # mov [rcx + next location offset], r9d
        b"\x8B\x81" + struct.pack("<i", next_location),  # mov eax, [rcx + next location]
        ("jump", b"\xEB", "restore"),  # jmp restore

        ("label", "skip"),
        b"\xFF\xC3",  # inc ebx
        ("jump", b"\xEB", "next_redirect"),  # jmp next_redirect

        ("label", "restore"),
        b"\x5E",  # pop rsi
        b"\x5B",  # pop rbx

        ("label", "log"),
        b"\x49\xBA" + struct.pack("<Q", cave_address + ARRIVAL_DATA_OFFSET),  # mov r10, arrival data
        b"\x45\x8B\x1A",  # mov r11d, [r10]  ; log count
        b"\x45\x89\xD8",  # mov r8d, r11d
        b"\x41\x81\xE0" + struct.pack("<i", ARRIVAL_LOG_CAPACITY - 1),  # and r8d, log capacity - 1
        b"\x41\xC1\xE0\x04",  # shl r8d, 4  ; arrival entry size
        b"\x49\xB9" + struct.pack("<Q", cave_address + ARRIVAL_LOG_OFFSET),  # mov r9, arrival log
        b"\x43\x89\x44\x01\x04",  # mov [r9 + r8 + 0x04], eax  ; destination
        b"\x8B\x81" + struct.pack("<i", current_location),  # mov eax, [rcx + current location]
        b"\x43\x89\x04\x01",  # mov [r9 + r8], eax  ; origin
        b"\x8B\x81" + struct.pack("<i", next_location + 4),  # mov eax, [rcx + next location offset]
        b"\x43\x89\x44\x01\x08",  # mov [r9 + r8 + 0x08], eax  ; offset
        b"\x0F\xB6\xC2",  # movzx eax, dl
        b"\x43\x89\x44\x01\x0C",  # mov [r9 + r8 + 0x0C], eax  ; is loading
        b"\x41\xFF\xC3",  # inc r11d
        b"\x45\x89\x1A",  # mov [r10], r11d  ; log count
        SCUMMVM_DETOUR_PROLOGUES["ScriptManager::ChangeLocationReal"],  # original prologue
        absolute_jump(module_base + SCUMMVM_FUNCTION_RVAS["ScriptManager::ChangeLocationReal"] + len(SCUMMVM_DETOUR_PROLOGUES["ScriptManager::ChangeLocationReal"])),
    ])


def build_current_puzzle_code(cave_address: int) -> bytes:
    return assemble([
        b"\x53",  # push rbx
        b"\x48\x83\xEC\x20",  # sub rsp, 0x20
        b"\x49\xBA" + struct.pack("<Q", cave_address + ACTION_DATA_OFFSET),  # mov r10, action data
        b"\x49\x8B\x1A",  # mov rbx, [r10]  ; enclosing puzzle
        b"\x49\x89\x12",  # mov [r10], rdx  ; puzzle being checked
        b"\x48\xB8" + struct.pack("<Q", cave_address + CURRENT_PUZZLE_TRAMPOLINE_OFFSET),  # mov rax, original checkPuzzleCriteria
        b"\xFF\xD0",  # call rax
        b"\x49\xBA" + struct.pack("<Q", cave_address + ACTION_DATA_OFFSET),  # mov r10, action data
        b"\x49\x89\x1A",  # mov [r10], rbx  ; back to the enclosing puzzle
        b"\x48\x83\xC4\x20",  # add rsp, 0x20
        b"\x5B",  # pop rbx
        b"\xC3",  # ret
    ])


def build_read_override_code(cave_address: int) -> bytes:
    return assemble([
        b"\x49\xBA" + struct.pack("<Q", cave_address + READ_OVERRIDE_DATA_OFFSET),  # mov r10, read override data
        b"\x45\x8B\x1A",  # mov r11d, [r10]  ; override count
        b"\x45\x85\xDB",  # test r11d, r11d
        ("jump", b"\x74", "pass_through"),  # je pass_through
        b"\x48\xB8" + struct.pack("<Q", cave_address + ACTION_DATA_OFFSET),  # mov rax, action data
        b"\x48\x8B\x00",  # mov rax, [rax]  ; puzzle being checked
        b"\x48\x85\xC0",  # test rax, rax
        ("jump", b"\x74", "pass_through"),  # je pass_through
        b"\x44\x8B\x00",  # mov r8d, [rax]  ; puzzle key
        b"\x41\xC1\xE3\x04",  # shl r11d, 4  ; override table size
        b"\x31\xC0",  # xor eax, eax

        ("label", "next_override"),
        b"\x44\x39\xD8",  # cmp eax, r11d
        ("jump", b"\x7D", "pass_through"),  # jge pass_through
        b"\x41\x3B\x54\x02\x08",  # cmp edx, [r10 + rax + 0x08]  ; state key
        ("jump", b"\x75", "skip"),  # jne skip
        b"\x45\x3B\x44\x02\x0C",  # cmp r8d, [r10 + rax + 0x0C]  ; puzzle key
        ("jump", b"\x75", "skip"),  # jne skip
        b"\x41\x8B\x44\x02\x10",  # mov eax, [r10 + rax + 0x10]  ; value read by that puzzle
        b"\xC3",  # ret

        ("label", "skip"),
        b"\x83\xC0\x10",  # add eax, 0x10
        ("jump", b"\xEB", "next_override"),  # jmp next_override

        ("label", "pass_through"),
        b"\x48\xB8" + struct.pack("<Q", cave_address + READ_OVERRIDE_TRAMPOLINE_OFFSET),  # mov rax, original getStateValue
        b"\xFF\xE0",  # jmp rax
    ])


def build_action_thunk_code(cave_address: int, class_index: int, original_execute: int) -> bytes:
    return assemble([
        b"\xB8" + struct.pack("<i", class_index),  # mov eax, action class
        b"\x49\xBA" + struct.pack("<Q", original_execute),  # mov r10, original execute
        absolute_jump(cave_address + ACTION_FILTER_CODE_OFFSET),
    ])


def build_action_filter_code(cave_address: int) -> bytes:
    return assemble([
        b"\x49\xBB" + struct.pack("<Q", cave_address + ACTION_DATA_OFFSET),  # mov r11, action data
        b"\x49\x8B\x13",  # mov rdx, [r11]  ; puzzle being checked
        b"\x45\x31\xC0",  # xor r8d, r8d
        b"\x48\x85\xD2",  # test rdx, rdx
        ("jump", b"\x74", "have_puzzle_key"),  # je have_puzzle_key
        b"\x44\x8B\x02",  # mov r8d, [rdx]  ; puzzle key

        ("label", "have_puzzle_key"),
        b"\x31\xD2",  # xor edx, edx

        ("label", "next_block"),
        b"\x41\x3B\x53\x08",  # cmp edx, [r11 + 0x08]  ; block count
        ("jump", b"\x7D", "not_blocked"),  # jge not_blocked
        b"\x45\x39\x44\xD3\x10",  # cmp [r11 + rdx*8 + 0x10], r8d  ; blocked puzzle
        ("jump", b"\x74", "puzzle_matches"),  # je puzzle_matches
        b"\x41\x83\x7C\xD3\x10\xFF",  # cmp dword [r11 + rdx*8 + 0x10], -1  ; any puzzle
        ("jump", b"\x75", "skip"),  # jne skip

        ("label", "puzzle_matches"),
        b"\x41\x39\x44\xD3\x14",  # cmp [r11 + rdx*8 + 0x14], eax  ; blocked action class
        ("jump", b"\x74", "blocked"),  # je blocked
        b"\x41\x83\x7C\xD3\x14\xFF",  # cmp dword [r11 + rdx*8 + 0x14], -1  ; any action class
        ("jump", b"\x74", "blocked"),  # je blocked

        ("label", "skip"),
        b"\xFF\xC2",  # inc edx
        ("jump", b"\xEB", "next_block"),  # jmp next_block

        ("label", "not_blocked"),
        b"\x41\xFF\xE2",  # jmp r10  ; original execute

        ("label", "blocked"),
        b"\xB8\x01\x00\x00\x00",  # mov eax, 1
        b"\xC3",  # ret
    ])


def build_overlay_code(cave_address: int, module_base: int) -> bytes:
    parts: List = [
        b"\x51",  # push rcx  ; screen
        b"\x52",  # push rdx
        b"\x48\x83\xEC\x58",  # sub rsp, 0x58
    ]

    layer: int
    for layer in range(OVERLAY_CAPACITY):
        parts.extend([
            b"\x48\x8B\x4C\x24\x60",  # mov rcx, [rsp + 0x60]  ; screen
            b"\x49\xBA" + struct.pack("<Q", cave_address + OVERLAY_DATA_OFFSET + layer * OVERLAY_LAYER_SIZE),  # mov r10, overlay layer
            b"\x41\x83\x3A\x00",  # cmp dword [r10], 0  ; is shown
            ("jump", b"\x74", f"skip_{layer}"),  # je skip
            b"\x49\x3B\x4A\x08",  # cmp rcx, [r10 + 0x08]  ; screen the layer was made for
            ("jump", b"\x75", f"skip_{layer}"),  # jne skip
            b"\x48\x8B\x41" + struct.pack("<b", ZVISION_STRUCTURE_OFFSETS["ManagedSurface::w"]),  # mov rax, [rcx + width reference]
            b"\x66\x81\x38" + struct.pack("<H", OVERLAY_SCREEN_WIDTH),  # cmp word [rax], screen width
            ("jump", b"\x75", f"skip_{layer}"),  # jne skip
            b"\x49\x8D\x52\x10",  # lea rdx, [r10 + 0x10]  ; surface
            b"\x4D\x8D\x42\x30",  # lea r8, [r10 + 0x30]  ; source rectangle
            b"\x4D\x8D\x4A\x38",  # lea r9, [r10 + 0x38]  ; destination rectangle
            b"\xC7\x44\x24\x20" + struct.pack("<I", OVERLAY_TRANSPARENT_COLOR),  # mov dword [rsp + 0x20], transparent color
            b"\xC7\x44\x24\x28\x00\x00\x00\x00",  # mov dword [rsp + 0x28], 0  ; not flipped
            b"\x41\x8B\x42\x04",  # mov eax, [r10 + 0x04]  ; alpha
            b"\x3D\xFF\x00\x00\x00",  # cmp eax, 0xFF
            ("jump", b"\x74", f"alpha_{layer}"),  # je alpha
            b"\x49\xBB" + struct.pack("<Q", module_base + SCUMMVM_GLOBAL_RVAS["g_engine"]),  # mov r11, g_engine
            b"\x4D\x8B\x1B",  # mov r11, [r11]  ; engine
            b"\x41\x80\xBB" + struct.pack("<i", ZVISION_MEMBER_OFFSETS["ZVision::_videoIsPlaying"]) + b"\x00",  # cmp byte [r11 + video is playing], 0
            ("jump", b"\x74", f"alpha_{layer}"),  # je alpha
            b"\xB8\xFF\x00\x00\x00",  # mov eax, 0xFF
            ("label", f"alpha_{layer}"),
            b"\x89\x44\x24\x30",  # mov [rsp + 0x30], eax
            b"\x48\xC7\x44\x24\x38\x00\x00\x00\x00",  # mov qword [rsp + 0x38], 0  ; no palette
            b"\x48\xC7\x44\x24\x40\x00\x00\x00\x00",  # mov qword [rsp + 0x40], 0
            b"\x48\xB8" + struct.pack("<Q", module_base + SCUMMVM_FUNCTION_RVAS["ManagedSurface::transBlitFrom"]),  # mov rax, transBlitFrom
            b"\xFF\xD0",  # call rax
            ("label", f"skip_{layer}"),
        ])

    parts.extend([
        b"\x48\x83\xC4\x58",  # add rsp, 0x58
        b"\x5A",  # pop rdx
        b"\x59",  # pop rcx
        SCUMMVM_DETOUR_PROLOGUES["Screen::update"],  # original prologue
        absolute_jump(module_base + SCUMMVM_FUNCTION_RVAS["Screen::update"] + len(SCUMMVM_DETOUR_PROLOGUES["Screen::update"])),
    ])

    return assemble(parts)


class ScummVMZVisionProcess:
    process: Pymem
    module_base: int

    cave_address: Optional[int]
    last_frame_count: Optional[int]
    state_change_log_cursor: Optional[int]
    arrival_log_cursor: Optional[int]
    call_timeout_seconds: float

    def __init__(self, process: Pymem, module_name: str) -> None:
        self.process = process
        module: pymem.ressources.structure.MODULEINFO = pymem.process.module_from_name(self.process.process_handle, module_name)
        self.module_base = module.lpBaseOfDll

        if module.SizeOfImage != SCUMMVM_SIZE_OF_IMAGE:
            raise RuntimeError(f"{module_name} is not ScummVM 2026.3.0 (win64)")

        fingerprint: int = zlib.crc32(bytes().join(
            self.process.read_bytes(self.module_base + SCUMMVM_FUNCTION_RVAS[name], 16)
            for name in sorted(SCUMMVM_FUNCTION_RVAS)
            if name not in SCUMMVM_DETOUR_PROLOGUES
        ))

        if fingerprint != SCUMMVM_FUNCTION_FINGERPRINT:
            raise RuntimeError(f"{module_name} does not have the expected ZVision functions")

        self.cave_address = None
        self.last_frame_count = None
        self.state_change_log_cursor = None
        self.arrival_log_cursor = None
        self.call_timeout_seconds = 5.0

    def install_hooks(self) -> None:
        pump_slot_address: int = self._get_virtual_slot_address(SCUMMVM_VIRTUAL_TABLE_RVAS["MenuZGI"], "MenuManager::process")
        pump_function: int = self._read_pointer(pump_slot_address)

        if pump_function == self._get_function_address("MenuZGI::process"):
            self._install_cave(pump_slot_address)
        else:
            try:
                magic: int = self.process.read_ulonglong(pump_function - PUMP_CODE_OFFSET + MAILBOX_OFFSET + 0x08)
            except Exception:
                magic = 0

            if magic != MAILBOX_MAGIC:
                raise RuntimeError("MenuZGI::process is already hooked by something else; restart ScummVM")

            self.cave_address = pump_function - PUMP_CODE_OFFSET

            if self.process.read_uint(self.cave_address + MAILBOX_OFFSET) != MAILBOX_STATE_PENDING:
                self.process.write_uint(self.cave_address + MAILBOX_OFFSET, MAILBOX_STATE_IDLE)

        self._install_detours()

    def is_hooked(self) -> bool:
        if self.cave_address is None:
            return False

        name: str
        code_offset: int
        for name, code_offset in DETOURS:
            if self.process.read_bytes(self._get_function_address(name), 14) != absolute_jump(self.cave_address + code_offset):
                return False

        class_index: int
        virtual_table: int
        for class_index, (virtual_table, _, _) in enumerate(ACTION_CLASSES):
            if self._read_pointer(self._get_virtual_slot_address(virtual_table, "ResultAction::execute")) != self.cave_address + ACTION_THUNKS_OFFSET + class_index * ACTION_THUNK_SIZE:
                return False

        return True

    def read_frame_count(self) -> int:
        return self.process.read_ulonglong(self._require_cave() + MAILBOX_OFFSET + 0x10)

    def is_game_running(self) -> bool:
        frame_count: int = self.read_frame_count()
        is_running: bool = self.last_frame_count is not None and frame_count != self.last_frame_count

        self.last_frame_count = frame_count

        return is_running

    def is_zvision_running(self) -> bool:
        engine: int = self._read_pointer(self.module_base + SCUMMVM_GLOBAL_RVAS["g_engine"])

        if engine == 0:
            return False

        try:
            script_manager: int = self._read_pointer(engine + ZVISION_MEMBER_OFFSETS["ZVision::_scriptManager"])

            return script_manager != 0 and self._read_pointer(script_manager + ZVISION_MEMBER_OFFSETS["ScriptManager::_engine"]) == engine
        except Exception:
            return False

    def is_widescreen(self) -> bool:
        return bool(self.process.read_uchar(self.read_engine_address() + ZVISION_MEMBER_OFFSETS["ZVision::_widescreen"]))

    def read_engine_address(self) -> int:
        if not self.is_zvision_running():
            raise RuntimeError("No ZVision game is running")

        return self._read_pointer(self.module_base + SCUMMVM_GLOBAL_RVAS["g_engine"])

    def call_on_main_thread(self, calls: Sequence[Tuple[int, ...]], timeout_seconds: Optional[float] = None) -> List[int]:
        cave_address: int = self._require_cave()

        if len(calls) > CALL_RECORD_CAPACITY:
            raise RuntimeError(f"Too many calls queued at once ({len(calls)})")

        if timeout_seconds is None:
            timeout_seconds = self.call_timeout_seconds

        deadline: float = time.perf_counter() + timeout_seconds
        mailbox_address: int = cave_address + MAILBOX_OFFSET

        while self.process.read_uint(mailbox_address) == MAILBOX_STATE_RUNNING:
            if time.perf_counter() > deadline:
                raise RuntimeError("The main thread is still running an earlier call queue")

            time.sleep(0.005)

        records: bytes = bytes().join(
            struct.pack("<Qqqqqqqq", *(tuple(call) + (0,) * (8 - len(call))))
            for call in calls
        )

        self.process.write_bytes(mailbox_address + 0x20, records, len(records))
        self.process.write_uint(mailbox_address + 0x04, len(calls))
        self.process.write_uint(mailbox_address, MAILBOX_STATE_PENDING)

        while self.process.read_uint(mailbox_address) != MAILBOX_STATE_DONE:
            if time.perf_counter() > deadline:
                if self.process.read_uint(mailbox_address) == MAILBOX_STATE_PENDING:
                    self.process.write_uint(mailbox_address, MAILBOX_STATE_IDLE)

                raise RuntimeError("Main thread did not service the call queue in time; is Zork Grand Inquisitor running?")

            time.sleep(0.005)

        self.process.write_uint(mailbox_address, MAILBOX_STATE_IDLE)

        results: bytes = self.process.read_bytes(mailbox_address + 0x20, len(records))

        return [struct.unpack_from("<i", results, record_index * 0x40 + 0x38)[0] for record_index in range(len(calls))]

    def read_state_values(self, keys: Sequence[int]) -> Dict[int, int]:
        cave_address: int = self._require_cave()
        values: Dict[int, int] = dict()

        index: int
        for index in range(0, len(keys), SNAPSHOT_CAPACITY):
            batch: Sequence[int] = keys[index:index + SNAPSHOT_CAPACITY]

            self._write_cave(SNAPSHOT_KEYS_OFFSET, struct.pack(f"<{len(batch)}I", *batch))
            self.call_on_main_thread([(
                cave_address + SNAPSHOT_CODE_OFFSET,
                THIS_SCRIPT_MANAGER,
                cave_address + SNAPSHOT_KEYS_OFFSET,
                len(batch),
                cave_address + SNAPSHOT_VALUES_OFFSET,
                self._get_function_address("ScriptManager::getStateValue"),
            )])

            values.update(zip(batch, struct.unpack(f"<{len(batch)}i", self.process.read_bytes(cave_address + SNAPSHOT_VALUES_OFFSET, len(batch) * 4))))

        return values

    def write_state_values(self, values: Dict[int, int]) -> None:
        set_state_value: int = self._get_function_address("ScriptManager::setStateValue")

        calls: List[Tuple[int, ...]] = [(set_state_value, THIS_SCRIPT_MANAGER, key, value) for key, value in values.items()]

        index: int
        for index in range(0, len(calls), CALL_RECORD_CAPACITY):
            self.call_on_main_thread(calls[index:index + CALL_RECORD_CAPACITY])

    def write_state_flags(self, flags: Sequence[Tuple[int, int, bool]]) -> None:
        set_state_flag: int = self._get_function_address("ScriptManager::setStateFlag")
        unset_state_flag: int = self._get_function_address("ScriptManager::unsetStateFlag")

        calls: List[Tuple[int, ...]] = [
            (set_state_flag if is_set else unset_state_flag, THIS_SCRIPT_MANAGER, key, flag)
            for key, flag, is_set in flags
        ]

        index: int
        for index in range(0, len(calls), CALL_RECORD_CAPACITY):
            self.call_on_main_thread(calls[index:index + CALL_RECORD_CAPACITY])

    def set_state_value_overrides(self, overrides: Dict[int, int]) -> None:
        cave_address: int = self._require_cave()

        if len(overrides) > STATE_OVERRIDE_CAPACITY:
            raise RuntimeError(f"At most {STATE_OVERRIDE_CAPACITY} state values can be overridden")

        entries: List[int] = [number for key, value in overrides.items() for number in (key, value)]
        padded_entries: List[int] = entries + [0] * (2 * STATE_OVERRIDE_CAPACITY - len(entries))

        self.process.write_uint(cave_address + STATE_OVERRIDE_DATA_OFFSET, 0)
        self.process.write_bytes(
            cave_address + STATE_OVERRIDE_DATA_OFFSET + 0x08,
            struct.pack(f"<{2 * STATE_OVERRIDE_CAPACITY}i", *padded_entries),
            8 * STATE_OVERRIDE_CAPACITY,
        )
        self.process.write_uint(cave_address + STATE_OVERRIDE_DATA_OFFSET, len(overrides))

    def set_state_flag_overrides(self, overrides: Dict[int, bool]) -> None:
        cave_address: int = self._require_cave()

        offset: int
        is_disabled: bool
        for offset, is_disabled in ((FLAG_OVERRIDE_DISABLED_OFFSET, True), (FLAG_OVERRIDE_ENABLED_OFFSET, False)):
            bitmap: bytearray = bytearray(FLAG_OVERRIDE_BITMAP_SIZE)

            key: int
            for key in [key for key, is_key_disabled in overrides.items() if is_key_disabled == is_disabled]:
                if not 0 <= key < 8 * FLAG_OVERRIDE_BITMAP_SIZE:
                    raise RuntimeError(f"State flag {key} is outside the overridable range")

                bitmap[key >> 3] |= 1 << (key & 7)

            self.process.write_bytes(cave_address + offset, bytes(bitmap), FLAG_OVERRIDE_BITMAP_SIZE)

    def set_state_value_read_overrides(self, overrides: Sequence[Tuple[int, int, int]]) -> None:
        cave_address: int = self._require_cave()

        if len(overrides) > READ_OVERRIDE_CAPACITY:
            raise RuntimeError(f"At most {READ_OVERRIDE_CAPACITY} state value read overrides can be set")

        entries: List[int] = [number for key, puzzle_key, value in overrides for number in (key, puzzle_key, value, 0)]
        padded_entries: List[int] = entries + [0] * (4 * READ_OVERRIDE_CAPACITY - len(entries))

        self.process.write_uint(cave_address + READ_OVERRIDE_DATA_OFFSET, 0)
        self.process.write_bytes(
            cave_address + READ_OVERRIDE_DATA_OFFSET + 0x08,
            struct.pack(f"<{4 * READ_OVERRIDE_CAPACITY}i", *padded_entries),
            16 * READ_OVERRIDE_CAPACITY,
        )
        self.process.write_uint(cave_address + READ_OVERRIDE_DATA_OFFSET, len(overrides))

    def set_state_value_remaps(self, remaps: Sequence[Tuple[int, int, int, int]]) -> None:
        cave_address: int = self._require_cave()

        if len(remaps) > STATE_VALUE_REMAP_CAPACITY:
            raise RuntimeError(f"At most {STATE_VALUE_REMAP_CAPACITY} state value remaps can be set")

        entries: List[int] = [number for remap in remaps for number in remap]
        padded_entries: List[int] = entries + [0] * (4 * STATE_VALUE_REMAP_CAPACITY - len(entries))

        self.process.write_uint(cave_address + STATE_VALUE_REMAP_DATA_OFFSET, 0)
        self.process.write_bytes(
            cave_address + STATE_VALUE_REMAP_DATA_OFFSET + 0x08,
            struct.pack(f"<{4 * STATE_VALUE_REMAP_CAPACITY}i", *padded_entries),
            16 * STATE_VALUE_REMAP_CAPACITY,
        )
        self.process.write_uint(cave_address + STATE_VALUE_REMAP_DATA_OFFSET, len(remaps))

    def read_new_state_changes(self) -> Tuple[List[Tuple[int, int]], bool]:
        cave_address: int = self._require_cave()
        count: int = self.process.read_uint(cave_address + STATE_CHANGE_DATA_OFFSET)

        if self.state_change_log_cursor is None or self.state_change_log_cursor > count:
            self.state_change_log_cursor = count

        first: int = max(self.state_change_log_cursor, count - STATE_CHANGE_LOG_CAPACITY)
        log: Tuple[int, ...] = struct.unpack(
            f"<{2 * STATE_CHANGE_LOG_CAPACITY}i",
            self.process.read_bytes(cave_address + STATE_CHANGE_LOG_OFFSET, STATE_CHANGE_LOG_CAPACITY * 8),
        )
        is_complete: bool = first == self.state_change_log_cursor and self.process.read_uint(cave_address + STATE_CHANGE_DATA_OFFSET) - first <= STATE_CHANGE_LOG_CAPACITY

        self.state_change_log_cursor = count

        changes: List[Tuple[int, int]] = list()

        index: int
        for index in range(first, count):
            slot: int = index % STATE_CHANGE_LOG_CAPACITY

            changes.append((log[slot * 2], log[slot * 2 + 1]))

        return changes, is_complete

    def read_current_location(self) -> Tuple[str, int]:
        script_manager: int = self._read_pointer(self.read_engine_address() + ZVISION_MEMBER_OFFSETS["ZVision::_scriptManager"])
        location_address: int = script_manager + ZVISION_MEMBER_OFFSETS["ScriptManager::_currentLocation"]
        packed, offset = struct.unpack("<II", self.process.read_bytes(location_address, 8))

        return struct.pack("<I", packed).decode("ascii", errors="replace").rstrip("\x00"), offset

    def change_location(self, location: str, offset: int) -> None:
        self.call_on_main_thread([
            (self._get_function_address("ScriptManager::changeLocation"), THIS_SCRIPT_MANAGER, *location.encode("ascii"), offset),
        ])

    def set_location_redirects(self, redirects: Sequence[Tuple[str, str, str, int]]) -> None:
        cave_address: int = self._require_cave()

        if len(redirects) > LOCATION_REDIRECT_CAPACITY:
            raise RuntimeError(f"At most {LOCATION_REDIRECT_CAPACITY} location redirects can be set")

        entries: List[int] = [
            number
            for origin, destination, new_destination, new_offset in redirects
            for number in (
                struct.unpack("<I", origin.encode("ascii"))[0] if origin else 0,
                struct.unpack("<I", destination.encode("ascii"))[0],
                struct.unpack("<I", new_destination.encode("ascii"))[0],
                new_offset,
            )
        ]
        padded_entries: List[int] = entries + [0] * (4 * LOCATION_REDIRECT_CAPACITY - len(entries))

        self.process.write_uint(cave_address + LOCATION_REDIRECT_DATA_OFFSET, 0)
        self.process.write_bytes(
            cave_address + LOCATION_REDIRECT_DATA_OFFSET + 0x08,
            struct.pack(f"<{4 * LOCATION_REDIRECT_CAPACITY}I", *padded_entries),
            16 * LOCATION_REDIRECT_CAPACITY,
        )
        self.process.write_uint(cave_address + LOCATION_REDIRECT_DATA_OFFSET, len(redirects))

    def read_new_arrivals(self) -> Tuple[List[Tuple[str, str, int, bool]], bool]:
        cave_address: int = self._require_cave()
        count: int = self.process.read_uint(cave_address + ARRIVAL_DATA_OFFSET)

        if self.arrival_log_cursor is None or self.arrival_log_cursor > count:
            self.arrival_log_cursor = count

        first: int = max(self.arrival_log_cursor, count - ARRIVAL_LOG_CAPACITY)
        log: Tuple[int, ...] = struct.unpack(
            f"<{4 * ARRIVAL_LOG_CAPACITY}I",
            self.process.read_bytes(cave_address + ARRIVAL_LOG_OFFSET, ARRIVAL_LOG_CAPACITY * 16),
        )
        is_complete: bool = first == self.arrival_log_cursor and self.process.read_uint(cave_address + ARRIVAL_DATA_OFFSET) - first <= ARRIVAL_LOG_CAPACITY

        self.arrival_log_cursor = count

        arrivals: List[Tuple[str, str, int, bool]] = list()

        index: int
        for index in range(first, count):
            slot: int = index % ARRIVAL_LOG_CAPACITY

            arrivals.append((
                struct.pack("<I", log[slot * 4]).decode("ascii", errors="replace").rstrip("\x00"),
                struct.pack("<I", log[slot * 4 + 1]).decode("ascii", errors="replace").rstrip("\x00"),
                log[slot * 4 + 2],
                bool(log[slot * 4 + 3]),
            ))

        return arrivals, is_complete

    def block_actions(self, blocks: Sequence[Tuple[Optional[int], Optional[str]]]) -> None:
        cave_address: int = self._require_cave()

        if len(blocks) > ACTION_BLOCK_CAPACITY:
            raise RuntimeError(f"At most {ACTION_BLOCK_CAPACITY} action blocks can be set")

        class_indexes: Dict[str, int] = {name: class_index for class_index, (_, _, names) in enumerate(ACTION_CLASSES) for name in names}
        entries: List[int] = [
            number
            for puzzle_key, action_name in blocks
            for number in (
                0xFFFFFFFF if puzzle_key is None else puzzle_key,
                0xFFFFFFFF if action_name is None else class_indexes[action_name],
            )
        ]
        padded_entries: List[int] = entries + [0] * (2 * ACTION_BLOCK_CAPACITY - len(entries))

        self.process.write_uint(cave_address + ACTION_DATA_OFFSET + 0x08, 0)
        self.process.write_bytes(
            cave_address + ACTION_DATA_OFFSET + 0x10,
            struct.pack(f"<{2 * ACTION_BLOCK_CAPACITY}I", *padded_entries),
            8 * ACTION_BLOCK_CAPACITY,
        )
        self.process.write_uint(cave_address + ACTION_DATA_OFFSET + 0x08, len(blocks))

    def kill_side_effect(self, key: int) -> None:
        self.call_on_main_thread([(self._get_function_address("ScriptManager::killSideFx"), THIS_SCRIPT_MANAGER, key)])

    def inventory_drop(self, item: int) -> None:
        self.call_on_main_thread([(self._get_function_address("ScriptManager::inventoryDrop"), THIS_SCRIPT_MANAGER, item)])

    def show_overlays(self, overlays: Sequence[Tuple[int, str, int, int, int, int, int, bool, int, Optional[Tuple[int, int, int]]]]) -> None:
        cave_address: int = self._require_cave()
        engine: int = self.read_engine_address()
        screen: int = self._read_pointer(engine + ZVISION_MEMBER_OFFSETS["ZVision::_renderManager"]) + ZVISION_MEMBER_OFFSETS["RenderManager::_screen"]
        text_renderer: int = self._read_pointer(engine + ZVISION_MEMBER_OFFSETS["ZVision::_textRenderer"])
        copy_address: int = cave_address + COPY_CODE_OFFSET
        calls: List[Tuple[int, ...]] = list()

        layer: int
        text: str
        x: int
        y: int
        width: int
        height: int
        fill_color: int
        has_black_frame: bool
        alpha: int
        line_gaps: Optional[Tuple[int, int, int]]
        for layer, text, x, y, width, height, fill_color, has_black_frame, alpha, line_gaps in overlays:
            layer_address: int = cave_address + OVERLAY_DATA_OFFSET + layer * OVERLAY_LAYER_SIZE
            text_address: int = cave_address + OVERLAY_TEXT_OFFSET + layer * 4 * (OVERLAY_TEXT_LENGTH + 1)
            encoded: bytes = text[:OVERLAY_TEXT_LENGTH].encode("utf-32-le")

            self.process.write_bytes(text_address, encoded + b"\x00" * 4, len(encoded) + 4)
            self.process.write_bytes(
                layer_address + 0x40,
                struct.pack("<IIQQI4x", len(encoded) // 4, 0, text_address, cave_address + STRING_REFERENCE_COUNT_OFFSET, OVERLAY_TEXT_LENGTH + 1),
                0x20,
            )
            self.process.write_bytes(
                layer_address + 0x60,
                struct.pack("<IIQ8h", 1, alpha, screen, 0, 0, height, width, y, x, y + height, x + width),
                0x20,
            )

            calls.extend([
                (self._get_function_address("Surface::create"), layer_address + 0x10, width, height, engine + ZVISION_MEMBER_OFFSETS["ZVision::_resourcePixelFormat"]),
                (self._get_function_address("Surface::fillRect"), layer_address + 0x10, (width << 48) | (height << 32), fill_color),
                (self._get_function_address("TextRenderer::drawTextWithWordWrapping"), text_renderer, layer_address + 0x40, layer_address + 0x10, int(has_black_frame)),
            ])

            if line_gaps is not None:
                first_row: int
                line_height: int
                line_count: int
                first_row, line_height, line_count = line_gaps

                gap_address: int = cave_address + OVERLAY_GAP_DATA_OFFSET + layer * 0x28
                left: int = width * first_row

                self.process.write_bytes(gap_address + 0x20, struct.pack("<hhh2x", left + width, line_count, width * 2 * line_height), 8)

                calls.extend([
                    (copy_address, gap_address, layer_address + 0x10, 0x20),
                    (copy_address, gap_address, gap_address + 0x20, 8),
                    (self._get_function_address("Surface::fillRect"), gap_address, ((left + width) << 48) | (line_count << 32) | (left << 16), fill_color),
                ])

            calls.extend([
                (copy_address, layer_address, layer_address + 0x60, 0x10),
                (copy_address, layer_address + 0x30, layer_address + 0x70, 0x10),
            ])

        self.call_on_main_thread(calls)

    def read_render_table(self) -> Dict[str, object]:
        render_manager: int = self._read_pointer(self.read_engine_address() + ZVISION_MEMBER_OFFSETS["ZVision::_renderManager"])
        render_table: int = render_manager + ZVISION_MEMBER_OFFSETS["RenderManager::_renderTable"]

        return {
            "render_state": ("panorama", "tilt", "flat")[self.process.read_int(render_table + ZVISION_MEMBER_OFFSETS["RenderTable::_renderState"])],
            "panorama_vertical_fov": math.degrees(self.process.read_float(render_table + ZVISION_MEMBER_OFFSETS["RenderTable::_panoramaOptions.verticalFOV"])),
            "panorama_linear_scale": self.process.read_float(render_table + ZVISION_MEMBER_OFFSETS["RenderTable::_panoramaOptions.linearScale"]),
            "panorama_reverse": bool(self.process.read_uchar(render_table + ZVISION_MEMBER_OFFSETS["RenderTable::_panoramaOptions.reverse"])),
        }

    def set_view_options(self, vertical_fov: Optional[float] = None, linear_scale: Optional[float] = None, reverse: Optional[bool] = None) -> None:
        if (vertical_fov is not None and vertical_fov <= 0.0) or (linear_scale is not None and linear_scale <= 0.0):
            raise ValueError("The vertical field of view and the linear scale must be positive")

        render_manager: int = self._read_pointer(self.read_engine_address() + ZVISION_MEMBER_OFFSETS["ZVision::_renderManager"])
        render_table: int = render_manager + ZVISION_MEMBER_OFFSETS["RenderManager::_renderTable"]
        calls: List[Tuple[int, ...]] = list()

        if vertical_fov is not None:
            calls.append((self._get_function_address("RenderTable::setPanoramaFoV"), render_table, struct.unpack("<I", struct.pack("<f", vertical_fov))[0]))

        if linear_scale is not None:
            calls.append((self._get_function_address("RenderTable::setPanoramaScale"), render_table, struct.unpack("<I", struct.pack("<f", linear_scale))[0]))

        if reverse is not None:
            calls.append((self._get_function_address("RenderTable::setPanoramaReverse"), render_table, int(reverse)))

        calls.append((self._get_function_address("RenderTable::generateRenderTable"), render_table))

        view_position: int = self.read_state_values([7])[7]

        calls.append((self._get_function_address("RenderManager::setBackgroundPosition"), render_manager, view_position + 1))
        calls.append((self._get_function_address("RenderManager::setBackgroundPosition"), render_manager, view_position))

        self.call_on_main_thread(calls)

    def _install_cave(self, pump_slot_address: int) -> None:
        name: str
        for name in SCUMMVM_DETOUR_PROLOGUES:
            if self.process.read_bytes(self._get_function_address(name), len(SCUMMVM_DETOUR_PROLOGUES[name])) != SCUMMVM_DETOUR_PROLOGUES[name]:
                raise RuntimeError(f"{name} is already patched by something else; restart ScummVM")

        virtual_table: int
        execute: int
        names: Tuple[str, ...]
        for virtual_table, execute, names in ACTION_CLASSES:
            if self._read_pointer(self._get_virtual_slot_address(virtual_table, "ResultAction::execute")) != self.module_base + execute:
                raise RuntimeError(f"Action {names[0]} is already hooked by something else; restart ScummVM")

        self.cave_address = self.process.allocate(CAVE_SIZE)

        self._write_cave(PUMP_CODE_OFFSET, build_pump_code(self.cave_address, self.module_base))
        self._write_cave(COPY_CODE_OFFSET, build_copy_code())
        self._write_cave(SNAPSHOT_CODE_OFFSET, build_snapshot_code())
        self._write_cave(STATE_CHANGE_LOGGER_CODE_OFFSET, build_state_change_logger_code(self.cave_address, self.module_base))
        self._write_cave(STATE_OVERRIDE_CODE_OFFSET, build_state_override_code(self.cave_address, self.module_base))
        self._write_cave(LOCATION_CHANGE_CODE_OFFSET, build_location_change_code(self.cave_address, self.module_base))
        self._write_cave(CURRENT_PUZZLE_CODE_OFFSET, build_current_puzzle_code(self.cave_address))
        self._write_cave(ACTION_FILTER_CODE_OFFSET, build_action_filter_code(self.cave_address))
        self._write_cave(FLAG_OVERRIDE_CODE_OFFSET, build_flag_override_code(self.cave_address, self.module_base))
        self._write_cave(READ_OVERRIDE_CODE_OFFSET, build_read_override_code(self.cave_address))
        self._write_cave(OVERLAY_CODE_OFFSET, build_overlay_code(self.cave_address, self.module_base))

        trampoline_offset: int
        for name, trampoline_offset in (
            ("ScriptManager::checkPuzzleCriteria", CURRENT_PUZZLE_TRAMPOLINE_OFFSET),
            ("ScriptManager::getStateFlag", FLAG_OVERRIDE_TRAMPOLINE_OFFSET),
            ("ScriptManager::getStateValue", READ_OVERRIDE_TRAMPOLINE_OFFSET),
        ):
            self._write_cave(trampoline_offset, SCUMMVM_DETOUR_PROLOGUES[name] + absolute_jump(self._get_function_address(name) + len(SCUMMVM_DETOUR_PROLOGUES[name])))

        class_index: int
        for class_index, (virtual_table, execute, names) in enumerate(ACTION_CLASSES):
            self._write_cave(ACTION_THUNKS_OFFSET + class_index * ACTION_THUNK_SIZE, build_action_thunk_code(self.cave_address, class_index, self.module_base + execute))

        self._write_cave(MAILBOX_OFFSET, struct.pack("<IIQQQ", MAILBOX_STATE_IDLE, 0, MAILBOX_MAGIC, 0, 0))
        self._write_cave(STRING_REFERENCE_COUNT_OFFSET, struct.pack("<i", 0x40000000))

        for class_index, (virtual_table, _, _) in enumerate(ACTION_CLASSES):
            self._write_protected_pointer(self._get_virtual_slot_address(virtual_table, "ResultAction::execute"), self.cave_address + ACTION_THUNKS_OFFSET + class_index * ACTION_THUNK_SIZE)

        self._write_protected_pointer(pump_slot_address, self.cave_address + PUMP_CODE_OFFSET)

    def _install_detours(self) -> None:
        cave_address: int = self._require_cave()
        copy_address: int = cave_address + COPY_CODE_OFFSET

        name: str
        code_offset: int
        for name, code_offset in DETOURS:
            function_address: int = self._get_function_address(name)
            prologue: bytes = SCUMMVM_DETOUR_PROLOGUES[name]
            patch: bytes = absolute_jump(cave_address + code_offset)
            patch += b"\xCC" * (len(prologue) - len(patch))
            current: bytes = self.process.read_bytes(function_address, len(prologue))

            if current == patch:
                continue

            if current != prologue:
                raise RuntimeError(f"{name} is already patched by something else; restart ScummVM")

            self._write_cave(PATCH_STAGING_OFFSET, patch)

            previous_protection: ctypes.c_ulong = ctypes.c_ulong(0)

            if not pymem.ressources.kernel32.VirtualProtectEx(self.process.process_handle, ctypes.c_void_p(function_address), len(patch), 0x40, ctypes.byref(previous_protection)):
                raise RuntimeError(f"Could not make {name} writable")

            try:
                self.call_on_main_thread([(copy_address, function_address, cave_address + PATCH_STAGING_OFFSET, len(patch))])
            finally:
                pymem.ressources.kernel32.VirtualProtectEx(self.process.process_handle, ctypes.c_void_p(function_address), len(patch), previous_protection.value, ctypes.byref(previous_protection))
                ctypes.windll.kernel32.FlushInstructionCache(ctypes.c_void_p(self.process.process_handle), ctypes.c_void_p(function_address), ctypes.c_size_t(len(patch)))

    def _require_cave(self) -> int:
        if self.cave_address is None:
            raise RuntimeError("Hooks are not installed")

        return self.cave_address

    def _write_cave(self, offset: int, data: bytes) -> None:
        self.process.write_bytes(self._require_cave() + offset, data, len(data))

    def _write_protected_pointer(self, address: int, value: int) -> None:
        previous_protection: ctypes.c_ulong = ctypes.c_ulong(0)

        if not pymem.ressources.kernel32.VirtualProtectEx(self.process.process_handle, ctypes.c_void_p(address), 8, 0x40, ctypes.byref(previous_protection)):
            raise RuntimeError(f"Could not make {address:#x} writable")

        self.process.write_ulonglong(address, value)

        pymem.ressources.kernel32.VirtualProtectEx(self.process.process_handle, ctypes.c_void_p(address), 8, previous_protection.value, ctypes.byref(previous_protection))

    def _read_pointer(self, address: int) -> int:
        return self.process.read_ulonglong(address)

    def _get_function_address(self, name: str) -> int:
        return self.module_base + SCUMMVM_FUNCTION_RVAS[name]

    def _get_virtual_slot_address(self, virtual_table_rva: int, function_name: str) -> int:
        return self.module_base + virtual_table_rva + SCUMMVM_VIRTUAL_TABLE_OFFSETS[function_name]
