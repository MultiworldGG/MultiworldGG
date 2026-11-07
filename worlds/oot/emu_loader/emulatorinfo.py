"""Emulator configuration and attachment logic for EmuLoader."""

import json
import os
import ssl
import urllib.request
from importlib import resources
from typing import Any, Callable, Dict, List, Optional, Tuple

from .process import IS_LINUX, IS_MACOS, ProcessMemory, get_running_processes
from .retroarch_udp import RetroArchNetworkInfo
from .utils import sanitize_and_trim

try:
    from CommonClient import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


EMULATOR_CONFIGS_URL = "https://killklli.github.io/EmuLoader/emulators.json"
EMULATOR_CONFIGS_FILENAME = "emulators.json"

# Common CA bundle locations across distros
_CA_BUNDLE_CANDIDATES = (
    "/etc/ssl/certs/ca-certificates.crt",  # Debian, Ubuntu, Arch
    "/etc/pki/tls/certs/ca-bundle.crt",  # RHEL, CentOS, Fedora (legacy)
    "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",  # Fedora / newer RHEL
    "/etc/ssl/ca-bundle.pem",  # openSUSE
    "/etc/ssl/cert.pem",  # macOS, Alpine, FreeBSD
    "/usr/local/etc/openssl/cert.pem",  # macOS Homebrew OpenSSL
    "/usr/local/share/certs/ca-root-nss.crt",  # FreeBSD
    "/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt",  # NixOS
)


def _build_ssl_context() -> ssl.SSLContext:
    """Build an SSLContext that finds a CA bundle even in frozen Archipelago builds."""
    paths = ssl.get_default_verify_paths()
    if (paths.cafile and os.path.isfile(paths.cafile)) or (paths.capath and os.path.isdir(paths.capath)):
        return ssl.create_default_context()

    try:
        import certifi

        logger.debug("SSL: using certifi bundle")
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass

    for path in _CA_BUNDLE_CANDIDATES:
        if os.path.isfile(path):
            logger.debug(f"SSL: using system CA bundle {path}")
            return ssl.create_default_context(cafile=path)

    logger.debug("SSL: no CA bundle found; falling back to default context")
    return ssl.create_default_context()


class EmulatorInfo:
    """Class to store emulator information."""

    def __init__(
        self,
        id: str,
        readable_emulator_name: str,
        process_name: str,
        find_dll: bool,
        dll_name: Optional[str],
        additional_lookup: bool,
        lower_offset_range: int,
        upper_offset_range: int,
        range_step: int = 16,
        extra_offset: int = 0,
        linux_dll_name: Optional[str] = None,
        scan_memory_for_signature: bool = False,
        signature_alignment: int = 0x10000,
        signature_offset: int = 0x759290,
        signature_value: int = 0x52414D42,
        validation_func: Optional[Callable[["ProcessMemory", int], bool]] = None,
    ):
        """Initialize with given parameters."""
        self.id = id
        self.readable_emulator_name = readable_emulator_name
        self.process_name = process_name
        self.find_dll = find_dll
        self.dll_name = dll_name
        self.linux_dll_name = linux_dll_name
        self.additional_lookup = additional_lookup
        self.lower_offset_range = lower_offset_range
        self.upper_offset_range = upper_offset_range
        self.range_step = range_step
        self.extra_offset = extra_offset
        self.scan_memory_for_signature = scan_memory_for_signature
        self.signature_alignment = signature_alignment
        self.signature_offset = signature_offset
        self.signature_value = signature_value
        self.validation_func = validation_func
        self.connected_process: Optional[ProcessMemory] = None
        self.connected_offset: Optional[int] = None
        self.connection_error: Optional[str] = None
        self.runtime_error: Optional[str] = None

    def get_library_name(self) -> Optional[str]:
        """Get the appropriate library name for the current platform."""
        if IS_LINUX and self.linux_dll_name:
            return self.linux_dll_name
        if IS_MACOS and self.linux_dll_name:
            # Most mupen64plus dylibs share the same stem on macOS
            so = self.linux_dll_name
            return so.replace(".so", ".dylib") if so.endswith(".so") else so
        return self.dll_name

    def get_possible_library_names(self) -> List[str]:
        """Get a list of possible library names to search for."""
        names: List[str] = []
        primary_name = self.get_library_name()
        if primary_name:
            names.append(primary_name)

        if (IS_LINUX or IS_MACOS) and self.dll_name:
            ext = ".dylib" if IS_MACOS else ".so"
            if self.dll_name.endswith(".dll"):
                so_name = self.dll_name[:-4] + ext
                if so_name not in names:
                    names.append(so_name)

            if not self.dll_name.startswith("lib"):
                lib_name = "lib" + self.dll_name
                if lib_name not in names:
                    names.append(lib_name)
                if lib_name.endswith(".dll"):
                    lib_ext_name = lib_name[:-4] + ext
                    if lib_ext_name not in names:
                        names.append(lib_ext_name)

        return [name for name in names if name]

    def disconnect(self):
        """Disconnect emulator from process management."""
        if self.connected_process:
            self.connected_process.close()
        self.connected_offset = None
        self.connected_process = None

    def raiseError(self, msg: str):
        """Raise an error and log it."""
        logger.debug(msg)
        self.connection_error = msg

    def _scan_for_signature(self, pm: ProcessMemory) -> Optional[int]:
        """Scan anonymous heap regions for the ROM signature and return the RDRAM base."""
        signature = self.signature_value.to_bytes(4, "little")
        signature_offset = self.signature_offset
        alignment = self.signature_alignment or 0x10000  # 0 is invalid for range() step
        use_validator = self.validation_func is not None
        for region_start, region_size in pm.list_writable_regions():
            max_base = region_size - signature_offset - 4
            if max_base < 0:
                continue
            for base in range(0, max_base + 1, alignment):
                candidate = region_start + base
                try:
                    if use_validator:
                        if self.validation_func(pm, candidate):
                            return candidate
                    else:
                        if pm.read_bytes(candidate + signature_offset, 4) == signature:
                            return candidate
                except Exception:
                    continue
        return None

    def attach_to_emulator(self) -> Optional[Tuple[ProcessMemory, int]]:
        """Grab memory addresses of where emulated RDRAM is."""
        self.connected_process = None
        self.connected_offset = None
        # Find processes by name
        processes = get_running_processes()
        matching_procs = [p for p in processes if p["name"] and p["name"].lower().startswith(self.process_name.lower())]
        if not matching_procs:
            self.raiseError(f"Could not find process '{self.process_name}'")
            return None

        if self.scan_memory_for_signature:
            # Multiple processes may match (e.g. gopher64 launches a child for the actual emu).
            last_error: Optional[str] = None
            for proc in matching_procs:
                try:
                    pm = ProcessMemory(self.process_name, pid=proc["pid"])
                except Exception as e:
                    last_error = f"Failed to attach to process pid {proc['pid']}: {e}"
                    continue
                rdram_base = self._scan_for_signature(pm)
                if rdram_base is None:
                    pm.close()
                    continue
                self.connected_process = pm
                self.connected_offset = rdram_base
                return (pm, rdram_base)
            self.raiseError(last_error or f"Could not locate signature in any {self.readable_emulator_name} memory region")
            return None

        target_proc = matching_procs[0]
        try:
            pm = ProcessMemory(target_proc["name"])
        except Exception as e:
            self.raiseError(f"Failed to attach to process: {str(e)}")
            return None

        address_dll = 0
        if self.find_dll:
            possible_names = self.get_possible_library_names()
            for module in pm.list_modules():
                for lib_name in possible_names:
                    if module.name.lower() == lib_name.lower() and module.lpBaseOfDll:
                        address_dll = module.lpBaseOfDll
                        break
                if address_dll != 0:
                    break

            if address_dll == 0 and self.id == "BizHawk":
                address_dll = 2024407040  # fallback guess
            elif address_dll == 0:
                searched_names = ", ".join(possible_names)
                self.raiseError(f"Could not find any of [{searched_names}] in {self.readable_emulator_name}")
                return None

        has_seen_nonzero = False
        for pot_off in range(self.lower_offset_range, self.upper_offset_range, self.range_step):
            if self.additional_lookup:
                rom_addr_start = address_dll + pot_off
                try:
                    read_address = pm.read_longlong(rom_addr_start)
                except Exception:
                    continue
                if read_address != 0:
                    has_seen_nonzero = True
            else:
                read_address = address_dll + pot_off

            candidate_offset = read_address + self.extra_offset
            if self.validation_func is not None:
                try:
                    is_valid = self.validation_func(pm, candidate_offset)
                    has_seen_nonzero = True
                except Exception:
                    continue
            else:
                try:
                    test_value = pm.read_int(candidate_offset + self.signature_offset)
                except Exception:
                    continue
                if test_value != 0:
                    has_seen_nonzero = True
                is_valid = test_value == self.signature_value
            if is_valid:
                self.connected_process = pm
                self.connected_offset = candidate_offset
                return (pm, candidate_offset)

        if not has_seen_nonzero:
            self.raiseError(f"Could not read any data from {self.readable_emulator_name}")

        return None

    def readBytes(self, address: int, size: int) -> int:
        """Read a series of bytes and cast to an int with N64 address fixing."""
        if self.connected_process is None or self.connected_offset is None:
            self.runtime_error = "Not connected to a process, exiting"
            raise Exception(self.runtime_error)
        if address & 0x80000000:
            address &= 0x7FFFFFFF

        if size == 1:
            remainder = address % 4
            if remainder == 0:
                address += 3
            elif remainder == 1:
                address += 1
            elif remainder == 2:
                address -= 1
            elif remainder == 3:
                address -= 3
        elif size == 2:
            remainder = address % 4
            if remainder in (2, 3):
                address -= 2
            elif remainder in (0, 1):
                address += 2

        mem_address = self.connected_offset + address
        data = self.connected_process.read_bytes(mem_address, size)
        return int.from_bytes(data, "little")

    def writeBytes(self, address: int, size: int, value: int):
        """Write a series of bytes to memory with N64 address fixing."""
        if self.connected_process is None or self.connected_offset is None:
            self.runtime_error = "Not connected to a process, exiting"
            raise Exception(self.runtime_error)
        if address & 0x80000000:
            address &= 0x7FFFFFFF

        if size == 1:
            remainder = address % 4
            if remainder == 0:
                address += 3
            elif remainder == 1:
                address += 1
            elif remainder == 2:
                address -= 1
            elif remainder == 3:
                address -= 3
        elif size == 2:
            remainder = address % 4
            if remainder in (2, 3):
                address -= 2
            elif remainder in (0, 1):
                address += 2

        mem_address = self.connected_offset + address
        data = value.to_bytes(size, byteorder="little")
        self.connected_process.write_bytes(mem_address, data, size)

    def read_u8(self, address: int) -> int:
        """Read an 8-bit unsigned integer from memory."""
        return self.readBytes(address, 1)

    def read_u16(self, address: int) -> int:
        """Read a 16-bit unsigned integer from memory."""
        return self.readBytes(address, 2)

    def read_u32(self, address: int) -> int:
        """Read a 32-bit unsigned integer from memory."""
        return self.readBytes(address, 4)

    def write_u8(self, address: int, value: int):
        """Write an 8-bit unsigned integer to memory."""
        self.writeBytes(address, 1, value)

    def write_u16(self, address: int, value: int):
        """Write a 16-bit unsigned integer to memory."""
        self.writeBytes(address, 2, value)

    def write_u32(self, address: int, value: int):
        """Write a 32-bit unsigned integer to memory."""
        self.writeBytes(address, 4, value)

    def read_bytestring(self, address: int, length: int) -> str:
        """Read a bytestring from memory."""
        result = ""
        for i in range(length):
            byte_val = self.read_u8(address + i)
            if byte_val == 0:
                break
            result += chr(byte_val)
        return result

    def write_bytestring(self, address: int, data: str):
        """Write a bytestring to memory."""
        sanitized_data = sanitize_and_trim(data)
        for i, char in enumerate(sanitized_data):
            self.write_u8(address + i, ord(char))
        self.write_u8(address + len(sanitized_data), 0)


def _parse_emulator_configs(data: List[Dict[str, Any]]) -> Dict[str, EmulatorInfo]:
    """Parse a list of emulator config dicts into an EMULATOR_CONFIGS mapping."""
    configs: Dict[str, EmulatorInfo] = {}
    for entry in data:
        emu_id = entry["id"]
        configs[emu_id] = EmulatorInfo(
            id=emu_id,
            readable_emulator_name=entry["readable_emulator_name"],
            process_name=entry["process_name"],
            find_dll=entry["find_dll"],
            dll_name=entry.get("dll_name"),
            additional_lookup=entry["additional_lookup"],
            lower_offset_range=int(entry["lower_offset_range"], 16),
            upper_offset_range=int(entry["upper_offset_range"], 16),
            range_step=int(entry.get("range_step", "0x10"), 16),
            extra_offset=int(entry.get("extra_offset", "0x0"), 16),
            linux_dll_name=entry.get("linux_dll_name"),
            scan_memory_for_signature=entry.get("scan_memory_for_signature", False),
            signature_alignment=int(entry.get("signature_alignment", "0x10000"), 16),
        )
    return configs


def load_emulator_configs(pull_from_web: bool = True) -> Dict[str, EmulatorInfo]:
    """Load emulator configs from GitHub Pages (if pull_from_web=True) or the local JSON file."""
    if pull_from_web:
        try:
            ctx = _build_ssl_context()
            with urllib.request.urlopen(EMULATOR_CONFIGS_URL, timeout=5, context=ctx) as response:
                data = json.loads(response.read().decode("utf-8"))
            logger.info("Loaded emulator configs from web.")
            return _parse_emulator_configs(data)
        except Exception as e:
            logger.warning(f"Failed to fetch emulator configs from web ({e}), falling back to local file.")

    try:
        # Use importlib.resources so the JSON loads correctly whether the package
        # lives on the filesystem or inside a zip import (e.g. an .apworld).
        raw = resources.files(__package__).joinpath(EMULATOR_CONFIGS_FILENAME).read_text(encoding="utf-8")
        data = json.loads(raw)
        logger.info("Loaded emulator configs from local file.")
        return _parse_emulator_configs(data)
    except Exception as e:
        logger.error(f"Failed to load local emulator configs: {e}")
        return {}


def attachWrapper(emu: str, configs: Dict[str, EmulatorInfo]) -> EmulatorInfo:
    """Wrap function for attaching to an emulator."""
    configs[emu].attach_to_emulator()
    return configs[emu]


def connect_to_emulator(configs: Dict[str, EmulatorInfo]) -> Optional[Any]:
    """Try to connect to any available emulator and return the connected instance."""
    # On macOS, process-memory access is not supported; RetroArch UDP is the only option
    if IS_MACOS:
        logger.info("macOS detected: RetroArch Network Commands (UDP) is the only supported connection method.")
        retroarch_network = RetroArchNetworkInfo()
        if retroarch_network.attach_to_emulator():
            logger.info(f"Connected to {retroarch_network.readable_emulator_name}")
            return retroarch_network
        if retroarch_network.connection_error:
            logger.info(f"Failed to connect via RetroArch Network Commands: {retroarch_network.connection_error}")
        return None

    for emulator_info in configs.values():
        try:
            if emulator_info.attach_to_emulator():
                logger.info(f"Connected to {emulator_info.readable_emulator_name}")
                print(f"Connected to {emulator_info.readable_emulator_name}")
                return emulator_info
        except Exception as e:
            logger.info(f"Failed to connect to {emulator_info.readable_emulator_name}: {str(e)}")
            continue

    # Fall back to RetroArch UDP if no process-based emulator was found
    retroarch_network = RetroArchNetworkInfo()
    if retroarch_network.attach_to_emulator():
        logger.info(f"Connected to {retroarch_network.readable_emulator_name}")
        return retroarch_network

    return None
