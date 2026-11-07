"""
Upstream owns process access, emulator profiles and the RetroArch protocol.
This adapter keeps ROM validation, explicit connections and UDP read batches.
"""

import os
import platform
import subprocess
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..emu_loader import EmulatorInfo, ProcessMemory, load_emulator_configs
from ..emu_loader import RetroArchNetworkInfo as VendorRetroArchNetworkInfo
from ..emu_loader.process import get_running_processes as _get_running_processes

try:
    from CommonClient import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# OoT AP ROM validation constants
# COOP_CONTEXT starts at N64 virtual 0x80400020 (RDRAM offset 0x00400020).
# COOP_VERSION is the first word (.word 8) and identifies a patched OoT AP ROM.
OOT_COOP_VERSION_ADDR = 0x00400020
OOT_COOP_VERSION_EXPECTED = 8
OOT_COSMETIC_FORMAT_VERSION_ADDR = 0x00403054
OOT_COSMETIC_FORMAT_VERSION_EXPECTED = 0x1F073FE2
CONNECT_STATUS_LOG_INTERVAL = 30.0
# A 256-byte read produces an ASCII reply under 1 KiB, fitting one UDP packet.
RETROARCH_READ_BLOCK_SIZE = 256

_last_connect_status: Optional[str] = None
_last_connect_status_time = 0.0

IS_MACOS = platform.system() == "Darwin"


def _get_macos_processes() -> List[Dict[str, Any]]:
    processes: List[Dict[str, Any]] = []
    try:
        output = subprocess.check_output(
            ["ps", "-axo", "pid=,comm="],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return processes

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        pid_text, _, command = line.partition(" ")
        try:
            pid = int(pid_text)
        except ValueError:
            continue
        name = os.path.basename(command.strip())
        if name:
            processes.append({"name": name, "pid": pid})
    return processes


def get_running_processes() -> List[Dict[str, Any]]:
    if IS_MACOS:
        return _get_macos_processes()
    return _get_running_processes()


def _is_process_running(processes: List[Dict[str, Any]], process_name: str) -> bool:
    expected = process_name.lower()
    return any(
        proc["name"] and proc["name"].lower().startswith(expected)
        for proc in processes
    )


def _validate_rom(read_u32: Callable[[int], int]) -> bool:
    try:
        return (
            read_u32(OOT_COOP_VERSION_ADDR) == OOT_COOP_VERSION_EXPECTED
            and read_u32(OOT_COSMETIC_FORMAT_VERSION_ADDR) == OOT_COSMETIC_FORMAT_VERSION_EXPECTED
        )
    except Exception:
        return False


def _validate_process_rom(process: ProcessMemory, base: int) -> bool:
    return _validate_rom(lambda address: process.read_int(base + address))


def _load_configs() -> Dict[str, EmulatorInfo]:
    configs = load_emulator_configs(pull_from_web=False)
    for info in configs.values():
        # The scanner uses this offset to bound candidate addresses even when
        # validation_func is supplied. Do not retain upstream's DK64 offset.
        info.signature_offset = OOT_COOP_VERSION_ADDR
        info.signature_value = OOT_COOP_VERSION_EXPECTED
        info.validation_func = _validate_process_rom
    return configs


class RetroArchNetworkInfo(VendorRetroArchNetworkInfo):
    """Add OoT validation and scoped block caching to upstream's UDP backend."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._word_cache: Optional[Dict[int, int]] = None

    def attach_to_emulator(self) -> Optional["RetroArchNetworkInfo"]:
        self.connection_error = None
        if super().attach_to_emulator() is None:
            return None
        if self.validate_rom():
            return self
        self.connection_error = (
            "RetroArch Network Commands responded, but OoT ROM markers could not be validated. "
            "Load the patched OoT AP ROM."
        )
        self.disconnect()
        return None

    def disconnect(self):
        self._word_cache = None
        super().disconnect()

    def _read_word(self, address: int) -> int:
        normalized_address = self._normalize_rdram_address(address)
        if self._word_cache is not None and normalized_address in self._word_cache:
            return self._word_cache[normalized_address]

        # Only explicit batches use read-ahead. Delivery/counter checks outside a
        # batch must always see fresh memory, including repeated word reads.
        if self._word_cache is not None and 0 <= normalized_address < 0x00800000:
            block_address = normalized_address & ~(RETROARCH_READ_BLOCK_SIZE - 1)
            data = self._read_memory(block_address, RETROARCH_READ_BLOCK_SIZE)
            for offset in range(0, len(data), 4):
                self._word_cache[block_address + offset] = int.from_bytes(data[offset:offset + 4], "little")
            return self._word_cache[normalized_address]

        return int.from_bytes(self._read_memory(normalized_address, 4), "little")

    def _read_memory(self, address: int, size: int) -> bytes:
        command_address = self._to_retroarch_address(address)
        response = self._send_command(f"READ_CORE_MEMORY {command_address:08X} {size}")
        parts = response.split()
        if len(parts) < 3 or parts[0] != "READ_CORE_MEMORY":
            raise Exception(f"Unexpected RetroArch read response: {response}")
        if int(parts[1], 16) != command_address:
            raise Exception(f"RetroArch read response address mismatch: {response}")
        if parts[2] == "-1":
            error = " ".join(parts[3:]) or "unknown error"
            raise Exception(f"RetroArch read failed at 0x{command_address:08X}: {error}")
        data = bytes(int(part, 16) for part in parts[2:])
        if len(data) != size:
            raise Exception(f"RetroArch read returned {len(data)} bytes, expected {size}: {response}")
        return data

    def _write_word(self, address: int, value: int):
        super()._write_word(address, value)
        if self._word_cache is not None:
            self._word_cache[self._normalize_rdram_address(address)] = value & 0xFFFFFFFF

    def begin_batch(self):
        self._word_cache = {}

    def end_batch(self):
        self._word_cache = None

    def validate_rom(self) -> bool:
        return _validate_rom(self.read_u32)


def _log_connect_status(errors: List[Tuple[str, str]]) -> None:
    """Log a compact, throttled summary of emulator attach failures."""
    global _last_connect_status, _last_connect_status_time

    actionable_errors = []
    seen_actionable_errors = set()
    for name, error in errors:
        if (
            "Failed to attach" in error
            or "RetroArch Network Commands" in error
            or "Could not find [" in error
            or "Could not find any of [" in error
            or "Could not locate signature" in error
            or "Could not locate an OoT AP ROM" in error
            or "Could not read any data" in error
        ):
            text = f"{name}: {error}"
            if error not in seen_actionable_errors:
                actionable_errors.append(text)
                seen_actionable_errors.add(error)
    if actionable_errors:
        summary = "OoT Bridge: emulator attach blocked; " + "; ".join(actionable_errors)
    else:
        summary = "OoT Bridge: waiting for supported emulator process"

    now = time.monotonic()
    if summary == _last_connect_status and now - _last_connect_status_time < CONNECT_STATUS_LOG_INTERVAL:
        return

    _last_connect_status = summary
    _last_connect_status_time = now
    logger.info(summary)


def connect_to_emulator(configs: Dict[str, EmulatorInfo]) -> Optional[Any]:
    """Prefer process memory on Windows/Linux; use UDP as fallback or on macOS."""
    global _last_connect_status, _last_connect_status_time

    errors: List[Tuple[str, str]] = []
    if not IS_MACOS:
        for info in configs.values():
            info.connection_error = None
            try:
                if info.attach_to_emulator():
                    logger.info(f"OoT Bridge: connected to {info.readable_emulator_name}")
                    _last_connect_status = None
                    _last_connect_status_time = 0.0
                    return info
                if info.connection_error:
                    errors.append((info.readable_emulator_name, info.connection_error))
            except Exception as e:
                errors.append((info.readable_emulator_name, str(e)))
                continue

    processes = get_running_processes()
    retroarch_network = RetroArchNetworkInfo()
    if retroarch_network.attach_to_emulator():
        logger.info(f"OoT Bridge: connected to {retroarch_network.readable_emulator_name}")
        _last_connect_status = None
        _last_connect_status_time = 0.0
        return retroarch_network
    if (
        retroarch_network.connection_error
        and (
            _is_process_running(processes, "retroarch")
            or "responded" in retroarch_network.connection_error
            or (
                "read failed" in retroarch_network.connection_error
                and "no memory map defined" not in retroarch_network.connection_error
            )
        )
    ):
        errors.append((retroarch_network.readable_emulator_name, retroarch_network.connection_error))
    _log_connect_status(errors)
    return None


class EmuLoaderClient:
    def __init__(self):
        self.emulator_info: Optional[Any] = None
        self.connected = False
        self._configs: Optional[Dict[str, EmulatorInfo]] = None

    def connect(self) -> bool:
        self.disconnect()
        if self._configs is None:
            self._configs = _load_configs()
        self.emulator_info = connect_to_emulator(self._configs)
        self.connected     = self.emulator_info is not None
        return self.connected

    def disconnect(self):
        if self.emulator_info:
            self.emulator_info.disconnect()
        self.connected     = False
        self.emulator_info = None

    def is_connected(self) -> bool:
        return self.connected and self.emulator_info is not None

    def read_u8(self, address: int) -> int:
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_u8(address)  # pyright: ignore[reportOptionalMemberAccess]

    def read_u16(self, address: int) -> int:
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_u16(address)  # pyright: ignore[reportOptionalMemberAccess]

    def read_u32(self, address: int) -> int:
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_u32(address)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u8(self, address: int, value: int):
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_u8(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u16(self, address: int, value: int):
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_u16(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u32(self, address: int, value: int):
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_u32(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def validate_rom(self) -> bool:
        if not self.is_connected():
            return False
        return _validate_rom(self.read_u32)
