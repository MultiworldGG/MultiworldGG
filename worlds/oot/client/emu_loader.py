"""N64 emulator memory access layer for OoT AP bridge.

Adapted from DK64 - thanks to the DK64 team for the baseline implementation.
"""

import ctypes
import glob
import os
import platform
import socket
import subprocess
import time
from enum import IntEnum, auto
from typing import Any, Dict, List, Optional, Tuple

from .ptrace import check_and_fix_ptrace_scope

try:
    from CommonClient import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# OoT AP ROM validation constants
# COOP_CONTEXT starts at N64 virtual 0x80400020 (RDRAM offset 0x00400020).
# COOP_VERSION is the first word (.word 7) and identifies a patched OoT AP ROM.
OOT_COOP_VERSION_ADDR = 0x00400020
OOT_COOP_VERSION_EXPECTED = 7
OOT_COSMETIC_FORMAT_VERSION_ADDR = 0x00400C44
OOT_COSMETIC_FORMAT_VERSION_EXPECTED = 0x1F073FE2
CONNECT_STATUS_LOG_INTERVAL = 30.0
RETROARCH_COMMAND_HOST = "127.0.0.1"
RETROARCH_COMMAND_PORT = 55355
RETROARCH_COMMAND_TIMEOUT = 0.5
N64_KSEG1_BASE = 0xA0000000

_last_connect_status: Optional[str] = None
_last_connect_status_time = 0.0

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX   = platform.system() == "Linux"
IS_MACOS   = platform.system() == "Darwin"

if IS_WINDOWS:
    import ctypes.wintypes

    PROCESS_VM_READ            = 0x0010
    PROCESS_VM_WRITE           = 0x0020
    PROCESS_VM_OPERATION       = 0x0008
    PROCESS_QUERY_INFORMATION  = 0x0400
    TH32CS_SNAPMODULE          = 0x00000008
    TH32CS_SNAPMODULE32        = 0x00000010
    TH32CS_SNAPPROCESS         = 0x00000002
    MAX_PATH                   = 260

    class MODULEENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize",        ctypes.wintypes.DWORD),
            ("th32ModuleID",  ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("GlblcntUsage",  ctypes.wintypes.DWORD),
            ("ProccntUsage",  ctypes.wintypes.DWORD),
            ("modBaseAddr",   ctypes.POINTER(ctypes.wintypes.BYTE)),
            ("modBaseSize",   ctypes.wintypes.DWORD),
            ("hModule",       ctypes.wintypes.HMODULE),
            ("szModule",      ctypes.c_char * 256),
            ("szExePath",     ctypes.c_char * 260),
        ]

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize",              ctypes.wintypes.DWORD),
            ("cntUsage",            ctypes.wintypes.DWORD),
            ("th32ProcessID",       ctypes.wintypes.DWORD),
            ("th32DefaultHeapID",   ctypes.POINTER(ctypes.wintypes.ULONG)),
            ("th32ModuleID",        ctypes.wintypes.DWORD),
            ("cntThreads",          ctypes.wintypes.DWORD),
            ("th32ParentProcessID", ctypes.wintypes.DWORD),
            ("pcPriClassBase",      ctypes.wintypes.LONG),
            ("dwFlags",             ctypes.wintypes.DWORD),
            ("szExeFile",           ctypes.c_char * MAX_PATH),
        ]

    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BaseAddress", ctypes.c_void_p),
            ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", ctypes.wintypes.DWORD),
            ("RegionSize", ctypes.c_size_t),
            ("State", ctypes.wintypes.DWORD),
            ("Protect", ctypes.wintypes.DWORD),
            ("Type", ctypes.wintypes.DWORD),
        ]

    MEM_COMMIT                = 0x1000
    MEM_PRIVATE               = 0x20000
    PAGE_NOACCESS             = 0x01
    PAGE_READWRITE            = 0x04
    PAGE_EXECUTE_READWRITE    = 0x40
    PAGE_GUARD                = 0x100

    def _get_windows_processes() -> List[Dict[str, Any]]:
        processes: List[Dict[str, Any]] = []
        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot == -1:
            return processes
        try:
            pe32 = PROCESSENTRY32()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
            if ctypes.windll.kernel32.Process32First(snapshot, ctypes.byref(pe32)):
                while True:
                    try:
                        processes.append({"name": pe32.szExeFile.decode("utf-8"), "pid": pe32.th32ProcessID})
                    except UnicodeDecodeError:
                        pass
                    if not ctypes.windll.kernel32.Process32Next(snapshot, ctypes.byref(pe32)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)
        return processes


def _get_linux_processes() -> List[Dict[str, Any]]:
    processes: List[Dict[str, Any]] = []
    try:
        for pid_dir in glob.glob("/proc/[0-9]*"):
            try:
                pid = int(os.path.basename(pid_dir))
                comm_path = os.path.join(pid_dir, "comm")
                if os.path.exists(comm_path):
                    with open(comm_path, "r") as f:
                        processes.append({"name": f.read().strip(), "pid": pid})
            except (ValueError, OSError, IOError):
                continue
    except OSError:
        pass
    return processes


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
    if IS_WINDOWS:
        return _get_windows_processes()
    if IS_LINUX:
        return _get_linux_processes()
    if IS_MACOS:
        return _get_macos_processes()
    return []


def _is_process_running(processes: List[Dict[str, Any]], process_name: str) -> bool:
    expected = process_name.lower()
    return any(
        proc["name"] and proc["name"].lower().startswith(expected)
        for proc in processes
    )


class ModuleInfo:
    name: str
    lpBaseOfDll: Optional[int]

    def __init__(self, name: str, lpBaseOfDll: Optional[int]):
        self.name        = name
        self.lpBaseOfDll = lpBaseOfDll


class ProcessMemory:
    def __init__(self, process_name: str, pid: Optional[int] = None):
        self.process_name   = process_name
        self.process_handle = None
        self.process_id     = None
        self.mem_fd         = None   # Linux /proc/pid/mem
        self._attach_to_process(pid)

    def _attach_to_process(self, target_pid: Optional[int] = None):
        processes = get_running_processes()
        for proc in processes:
            if target_pid is not None:
                matches = proc["pid"] == target_pid
            else:
                matches = bool(proc["name"]) and proc["name"].lower().startswith(self.process_name.lower())
            if matches:
                self.process_id = proc["pid"]
                if IS_WINDOWS:
                    self._attach_windows()
                elif IS_LINUX:
                    self._attach_linux()
                return
        raise Exception(f"Process {self.process_name} not found")

    def _attach_windows(self):
        self.process_handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION,
            False, self.process_id,
        )
        if not self.process_handle:
            raise Exception(f"Failed to open process {self.process_name}")

    def _attach_linux(self):
        check_and_fix_ptrace_scope()
        try:
            self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
        except (OSError, IOError) as e:
            if e.errno in (1, 13):
                if check_and_fix_ptrace_scope():
                    try:
                        self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                        return
                    except (OSError, IOError) as retry_e:
                        raise Exception(f"Failed to open memory after fixing ptrace: {retry_e}")
                raise Exception(
                    f"Failed to open memory for {self.process_name}: {e}. "
                    "Ptrace restrictions may be blocking access."
                )
            raise Exception(f"Failed to open memory for {self.process_name}: {e}")

    def list_modules(self) -> List[ModuleInfo]:
        if IS_WINDOWS:
            return self._list_modules_windows()
        if IS_LINUX:
            return self._list_modules_linux()
        return []

    def _list_modules_windows(self) -> List[ModuleInfo]:
        modules: List[ModuleInfo] = []
        if not self.process_handle or not self.process_id:
            return modules
        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(
            TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, self.process_id
        )
        if snapshot == -1:
            return modules
        try:
            me32 = MODULEENTRY32()
            me32.dwSize = ctypes.sizeof(MODULEENTRY32)
            if ctypes.windll.kernel32.Module32First(snapshot, ctypes.byref(me32)):
                while True:
                    modules.append(ModuleInfo(
                        name=me32.szModule.decode("utf-8"),
                        lpBaseOfDll=ctypes.cast(me32.modBaseAddr, ctypes.c_void_p).value,
                    ))
                    if not ctypes.windll.kernel32.Module32Next(snapshot, ctypes.byref(me32)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)
        return modules

    def _list_modules_linux(self) -> List[ModuleInfo]:
        modules: List[ModuleInfo] = []
        if not self.process_id:
            return modules
        try:
            with open(f"/proc/{self.process_id}/maps", "r") as maps_file:
                seen: set = set()
                for line in maps_file:
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        permissions = parts[1]
                        pathname    = parts[5]
                        if "x" in permissions and pathname and not pathname.startswith("["):
                            name = os.path.basename(pathname)
                            if name not in seen:
                                start = int(parts[0].split("-")[0], 16)
                                modules.append(ModuleInfo(name=name, lpBaseOfDll=start))
                                seen.add(name)
        except (OSError, IOError):
            pass
        return modules

    def list_writable_regions(self, min_size: int = 0x800000) -> List[Tuple[int, int]]:
        if IS_WINDOWS:
            return self._list_writable_regions_windows(min_size)
        if IS_LINUX:
            return self._list_writable_regions_linux(min_size)
        return []

    def _list_writable_regions_linux(self, min_size: int) -> List[Tuple[int, int]]:
        regions: List[Tuple[int, int]] = []
        if not self.process_id:
            return regions

        try:
            with open(f"/proc/{self.process_id}/maps", "r") as maps_file:
                for line in maps_file:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    permissions = parts[1]
                    pathname = parts[5] if len(parts) > 5 else ""
                    if "r" not in permissions or "w" not in permissions:
                        continue
                    if pathname and pathname != "[heap]" and not pathname.startswith("[anon"):
                        continue

                    try:
                        start_str, end_str = parts[0].split("-")
                        start_addr = int(start_str, 16)
                        end_addr = int(end_str, 16)
                    except ValueError:
                        continue

                    size = end_addr - start_addr
                    if size >= min_size:
                        regions.append((start_addr, size))
        except (OSError, IOError):
            pass

        return regions

    def _list_writable_regions_windows(self, min_size: int) -> List[Tuple[int, int]]:
        regions: List[Tuple[int, int]] = []
        if not self.process_handle:
            return regions

        VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
        VirtualQueryEx.argtypes = [
            ctypes.wintypes.HANDLE,
            ctypes.c_void_p,
            ctypes.POINTER(MEMORY_BASIC_INFORMATION),
            ctypes.c_size_t,
        ]
        VirtualQueryEx.restype = ctypes.c_size_t

        mbi = MEMORY_BASIC_INFORMATION()
        mbi_size = ctypes.sizeof(MEMORY_BASIC_INFORMATION)
        max_address = 0x7FFFFFFFFFFF if ctypes.sizeof(ctypes.c_void_p) == 8 else 0x7FFFFFFF
        writable_mask = PAGE_READWRITE | PAGE_EXECUTE_READWRITE

        address = 0
        while address < max_address:
            if VirtualQueryEx(self.process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), mbi_size) == 0:
                break

            base = mbi.BaseAddress or 0
            size = mbi.RegionSize
            if size == 0:
                break

            protect = mbi.Protect
            if (
                mbi.State == MEM_COMMIT
                and mbi.Type == MEM_PRIVATE
                and not (protect & PAGE_GUARD)
                and not (protect & PAGE_NOACCESS)
                and (protect & writable_mask)
                and size >= min_size
            ):
                regions.append((base, size))

            address = base + size

        return regions

    def read_bytes(self, address: int, size: int) -> bytes:
        if IS_WINDOWS:
            return self._read_bytes_windows(address, size)
        if IS_LINUX:
            return self._read_bytes_linux(address, size)
        raise Exception("Unsupported operating system")

    def _read_bytes_windows(self, address: int, size: int) -> bytes:
        if not self.process_handle:
            raise Exception("Process not attached")
        buffer     = ctypes.create_string_buffer(size)
        bytes_read = ctypes.wintypes.DWORD(0)
        result = ctypes.windll.kernel32.ReadProcessMemory(
            self.process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read)
        )
        if not result:
            raise Exception(f"Failed to read memory at 0x{address:08x}")
        return buffer.raw[: bytes_read.value]

    def _read_bytes_linux(self, address: int, size: int) -> bytes:
        if self.mem_fd is None:
            raise Exception("Process not attached")
        try:
            data = os.pread(self.mem_fd, size, address)
            if len(data) != size:
                raise Exception(f"Short read at 0x{address:08x}")
            return data
        except (OSError, IOError) as e:
            raise Exception(f"Failed to read memory at 0x{address:08x}: {e}")

    def write_bytes(self, address: int, data: bytes, size: int):
        if IS_WINDOWS:
            self._write_bytes_windows(address, data, size)
        elif IS_LINUX:
            self._write_bytes_linux(address, data, size)
        else:
            raise Exception("Unsupported operating system")

    def _write_bytes_windows(self, address: int, data: bytes, size: int):
        if not self.process_handle:
            raise Exception("Process not attached")
        bytes_written = ctypes.wintypes.DWORD(0)
        result = ctypes.windll.kernel32.WriteProcessMemory(
            self.process_handle, ctypes.c_void_p(address), data, size, ctypes.byref(bytes_written)
        )
        if not result:
            error_code = ctypes.windll.kernel32.GetLastError()
            raise Exception(f"WriteProcessMemory failed at 0x{address:08x}, error: {error_code}")

    def _write_bytes_linux(self, address: int, data: bytes, size: int):
        if self.mem_fd is None:
            raise Exception("Process not attached")
        try:
            written = os.pwrite(self.mem_fd, data[:size], address)
            if written != size:
                raise Exception(f"Short write at 0x{address:08x}")
        except (OSError, IOError) as e:
            raise Exception(f"Failed to write memory at 0x{address:08x}: {e}")

    def read_int(self, address: int) -> int:
        data = self.read_bytes(address, 4)
        return int.from_bytes(data, "little")

    def read_longlong(self, address: int) -> int:
        data = self.read_bytes(address, 8)
        return int.from_bytes(data, "little")

    def close(self):
        if IS_WINDOWS and self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
        elif IS_LINUX and self.mem_fd is not None:
            os.close(self.mem_fd)
            self.mem_fd = None


class Emulators(IntEnum):
    Project64Scan  = auto()
    Project64_EM   = auto()
    Project64      = auto()
    BizHawk        = auto()
    Project64_v4   = auto()
    RMG            = auto()
    Simple64       = auto()
    ParallelLauncher    = auto()
    ParallelLauncher903 = auto()
    RetroArch      = auto()
    Gopher64       = auto()
    Ares           = auto()


class EmulatorInfo:
    def __init__(
        self,
        id: Emulators,
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
    ):
        self.id                    = id
        self.readable_emulator_name = readable_emulator_name
        self.process_name          = process_name
        self.find_dll              = find_dll
        self.dll_name              = dll_name
        self.linux_dll_name        = linux_dll_name
        self.additional_lookup     = additional_lookup
        self.lower_offset_range    = lower_offset_range
        self.upper_offset_range    = upper_offset_range
        self.range_step            = range_step
        self.extra_offset          = extra_offset
        self.scan_memory_for_signature = scan_memory_for_signature
        self.signature_alignment   = signature_alignment
        self.connected_process: Optional[ProcessMemory] = None
        self.connected_offset: Optional[int] = None
        self.connection_error: Optional[str] = None
        self.runtime_error: Optional[str]    = None

    def get_library_name(self) -> Optional[str]:
        if IS_LINUX and self.linux_dll_name:
            return self.linux_dll_name
        if IS_MACOS and self.linux_dll_name:
            # Most mupen64plus dylibs share the same stem on macOS
            so = self.linux_dll_name
            return so.replace(".so", ".dylib") if so.endswith(".so") else so
        return self.dll_name

    def get_possible_library_names(self) -> List[str]:
        names: List[str] = []
        primary = self.get_library_name()
        if primary:
            names.append(primary)

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
                    lib_ext = lib_name[:-4] + ext
                    if lib_ext not in names:
                        names.append(lib_ext)

        return [n for n in names if n]

    def disconnect(self):
        if self.connected_process:
            self.connected_process.close()
        self.connected_offset  = None
        self.connected_process = None

    def raiseError(self, msg: str):
        self.connection_error = msg

    def _is_oot_ap_rom_base(self, pm: ProcessMemory, rdram_base: int) -> bool:
        try:
            coop_version = pm.read_int(rdram_base + OOT_COOP_VERSION_ADDR)
            cosmetic_version = pm.read_int(rdram_base + OOT_COSMETIC_FORMAT_VERSION_ADDR)
        except Exception:
            return False
        return (
            coop_version == OOT_COOP_VERSION_EXPECTED
            and cosmetic_version == OOT_COSMETIC_FORMAT_VERSION_EXPECTED
        )

    def _scan_for_signature(self, pm: ProcessMemory) -> Optional[int]:
        """Scan anonymous heap regions for an OoT AP ROM and return the RDRAM base."""
        signature = OOT_COOP_VERSION_EXPECTED.to_bytes(4, "little")
        signature_offset = OOT_COOP_VERSION_ADDR
        alignment = self.signature_alignment

        for region_start, region_size in pm.list_writable_regions():
            max_base = region_size - signature_offset - 4
            if max_base < 0:
                continue
            for base in range(0, max_base + 1, alignment):
                try:
                    sample = pm.read_bytes(region_start + base + signature_offset, 4)
                except Exception:
                    continue
                if sample != signature:
                    continue

                candidate_base = region_start + base
                if self._is_oot_ap_rom_base(pm, candidate_base):
                    return region_start + base
        return None

    def attach_to_emulator(self) -> Optional[Tuple["ProcessMemory", int]]:
        """Find the emulator process and locate the N64 RDRAM base in host memory.

        The RDRAM base is identified by reading the OoT AP COOP_VERSION and
        COSMETIC_FORMAT_VERSION marker words.
        """
        self.connected_process = None
        self.connected_offset  = None

        processes = get_running_processes()
        matching_procs = [
            proc for proc in processes
            if proc["name"] and proc["name"].lower().startswith(self.process_name.lower())
        ]
        if not matching_procs:
            self.raiseError(f"Could not find process '{self.process_name}'")
            return None

        if self.scan_memory_for_signature:
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
                self.connected_offset  = rdram_base
                return (pm, rdram_base)

            self.raiseError(
                last_error
                or f"Could not locate an OoT AP ROM in any {self.readable_emulator_name} memory region"
            )
            return None

        target_proc = matching_procs[0]
        try:
            pm = ProcessMemory(self.process_name, pid=target_proc["pid"])
        except Exception as e:
            self.raiseError(f"Failed to attach to process: {e}")
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

            if address_dll == 0 and self.id == Emulators.BizHawk:
                address_dll = 2024407040  # fallback
            elif address_dll == 0:
                searched = ", ".join(possible_names)
                self.raiseError(f"Could not find [{searched}] in {self.readable_emulator_name}")
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

            candidate_base = read_address + self.extra_offset
            try:
                coop_version = pm.read_int(candidate_base + OOT_COOP_VERSION_ADDR)
                cosmetic_version = pm.read_int(candidate_base + OOT_COSMETIC_FORMAT_VERSION_ADDR)
            except Exception:
                continue

            if coop_version != 0 or cosmetic_version != 0:
                has_seen_nonzero = True
            if (
                coop_version == OOT_COOP_VERSION_EXPECTED
                and cosmetic_version == OOT_COSMETIC_FORMAT_VERSION_EXPECTED
            ):
                self.connected_process = pm
                self.connected_offset  = candidate_base
                return (pm, candidate_base)

        if not has_seen_nonzero:
            self.raiseError(f"Could not read any data from {self.readable_emulator_name}")

        return None


    def _fix_address(self, address: int, size: int) -> int:
        """Remap an N64 address to the host address for byte-lane-swapped RDRAM."""
        if size == 1:
            remainder = address % 4
            if   remainder == 0: address += 3
            elif remainder == 1: address += 1
            elif remainder == 2: address -= 1
            elif remainder == 3: address -= 3
        elif size == 2:
            remainder = address % 4
            if   remainder in (2, 3): address -= 2
            elif remainder in (0, 1): address += 2
        return address

    def readBytes(self, address: int, size: int) -> int:
        if self.connected_process is None or self.connected_offset is None:
            self.runtime_error = "Not connected to a process"
            raise Exception(self.runtime_error)
        if address & 0x80000000:
            address &= 0x7FFFFFFF
        address    = self._fix_address(address, size)
        mem_address = self.connected_offset + address
        data = self.connected_process.read_bytes(mem_address, size)
        return int.from_bytes(data, "little")

    def writeBytes(self, address: int, size: int, value: int):
        if self.connected_process is None or self.connected_offset is None:
            self.runtime_error = "Not connected to a process"
            raise Exception(self.runtime_error)
        if address & 0x80000000:
            address &= 0x7FFFFFFF
        address    = self._fix_address(address, size)
        mem_address = self.connected_offset + address
        data = value.to_bytes(size, byteorder="little")
        self.connected_process.write_bytes(mem_address, data, size)

    def read_u8(self, address: int) -> int:
        return self.readBytes(address, 1)

    def read_u16(self, address: int) -> int:
        return self.readBytes(address, 2)

    def read_u32(self, address: int) -> int:
        return self.readBytes(address, 4)

    def write_u8(self, address: int, value: int):
        self.writeBytes(address, 1, value)

    def write_u16(self, address: int, value: int):
        self.writeBytes(address, 2, value)

    def write_u32(self, address: int, value: int):
        self.writeBytes(address, 4, value)

    def validate_rom(self) -> bool:
        """Return True if an OoT AP patched ROM is loaded."""
        try:
            return (
                self.read_u32(OOT_COOP_VERSION_ADDR) == OOT_COOP_VERSION_EXPECTED
                and self.read_u32(OOT_COSMETIC_FORMAT_VERSION_ADDR) == OOT_COSMETIC_FORMAT_VERSION_EXPECTED
            )
        except Exception:
            return False


class RetroArchNetworkInfo:
    """RetroArch Network Commands memory backend.

    This avoids process-memory attach entirely.
    """

    readable_emulator_name = "RetroArch Network Commands"

    def __init__(
        self,
        host: str = RETROARCH_COMMAND_HOST,
        port: int = RETROARCH_COMMAND_PORT,
        timeout: float = RETROARCH_COMMAND_TIMEOUT,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.connection_error: Optional[str] = None
        self.runtime_error: Optional[str] = None
        self._word_cache: Optional[Dict[int, int]] = None

    def attach_to_emulator(self) -> Optional["RetroArchNetworkInfo"]:
        self.disconnect()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            self.socket = sock
            coop_version = self.read_u32(OOT_COOP_VERSION_ADDR)
            cosmetic_version = self.read_u32(OOT_COSMETIC_FORMAT_VERSION_ADDR)
            if (
                coop_version == OOT_COOP_VERSION_EXPECTED
                and cosmetic_version == OOT_COSMETIC_FORMAT_VERSION_EXPECTED
            ):
                return self
            self.connection_error = (
                "RetroArch Network Commands responded, but ROM markers did not match "
                f"(COOP_VERSION={coop_version}, COSMETIC_FORMAT_VERSION=0x{cosmetic_version:08X}). "
                "Load the patched OoT AP ROM."
            )
        except socket.timeout:
            self.connection_error = (
                "RetroArch Network Commands did not respond. Enable Settings > Network > Network Commands "
                f"and leave the command port at {self.port}."
            )
        except OSError as exc:
            self.connection_error = (
                "RetroArch Network Commands unavailable. Enable Settings > Network > Network Commands "
                f"and leave the command port at {self.port}. ({exc})"
            )
        except Exception as exc:
            self.connection_error = f"RetroArch Network Commands read failed: {exc}"

        self.disconnect()
        return None

    def disconnect(self):
        if self.socket is not None:
            try:
                self.socket.close()
            except OSError:
                pass
        self.socket = None

    def _normalize_rdram_address(self, address: int) -> int:
        if 0x80000000 <= address < 0x80800000:
            return address - 0x80000000
        if 0xA0000000 <= address < 0xA0800000:
            return address - 0xA0000000
        if address & 0x80000000:
            return address & 0x7FFFFFFF
        return address

    def _to_retroarch_address(self, address: int) -> int:
        # RetroArch exposes N64 core memory through the system memory map.
        # Reading/writing whole words at KSEG1 addresses gives us the stable
        # little-endian host representation of N64 big-endian words.
        return N64_KSEG1_BASE + self._normalize_rdram_address(address)

    def _send_command(self, command: str) -> str:
        if self.socket is None:
            self.runtime_error = "RetroArch Network Commands is not connected"
            raise Exception(self.runtime_error)
        self.socket.send(command.encode("ascii"))
        return self.socket.recv(4096).decode("ascii", errors="replace").strip()

    def _read_word(self, address: int) -> int:
        normalized_address = self._normalize_rdram_address(address)
        if self._word_cache is not None and normalized_address in self._word_cache:
            return self._word_cache[normalized_address]

        command_address = self._to_retroarch_address(normalized_address)
        response = self._send_command(f"READ_CORE_MEMORY {command_address:08X} 4")
        parts = response.split()
        if len(parts) < 3 or parts[0] != "READ_CORE_MEMORY":
            raise Exception(f"Unexpected RetroArch read response: {response}")
        if parts[2] == "-1":
            error = " ".join(parts[3:]) or "unknown error"
            raise Exception(f"RetroArch read failed at 0x{command_address:08X}: {error}")
        data = bytes(int(part, 16) for part in parts[2:])
        if len(data) != 4:
            raise Exception(f"RetroArch read returned {len(data)} bytes, expected 4: {response}")
        value = int.from_bytes(data, byteorder="little")
        if self._word_cache is not None:
            self._word_cache[normalized_address] = value
        return value

    def _write_word(self, address: int, value: int):
        normalized_address = self._normalize_rdram_address(address)
        command_address = self._to_retroarch_address(normalized_address)
        data = (value & 0xFFFFFFFF).to_bytes(4, byteorder="little")
        data_text = " ".join(f"{byte:02X}" for byte in data)
        response = self._send_command(f"WRITE_CORE_MEMORY {command_address:08X} {data_text}")
        parts = response.split()
        if len(parts) < 3 or parts[0] != "WRITE_CORE_MEMORY":
            raise Exception(f"Unexpected RetroArch write response: {response}")
        if parts[2] == "-1":
            error = " ".join(parts[3:]) or "unknown error"
            raise Exception(f"RetroArch write failed at 0x{command_address:08X}: {error}")
        try:
            written = int(parts[2])
        except ValueError as exc:
            raise Exception(f"Unexpected RetroArch write response: {response}") from exc
        if written != 4:
            raise Exception(f"RetroArch wrote {written} bytes, expected 4: {response}")
        if self._word_cache is not None:
            self._word_cache[normalized_address] = value & 0xFFFFFFFF

    def begin_batch(self):
        self._word_cache = {}

    def end_batch(self):
        self._word_cache = None

    def read_u8(self, address: int) -> int:
        normalized = self._normalize_rdram_address(address)
        word = self._read_word(normalized & ~3)
        shift = (3 - (normalized & 3)) * 8
        return (word >> shift) & 0xFF

    def read_u16(self, address: int) -> int:
        normalized = self._normalize_rdram_address(address)
        remainder = normalized & 3
        if remainder <= 2:
            word = self._read_word(normalized & ~3)
            shift = (2 - remainder) * 8
            return (word >> shift) & 0xFFFF
        return (self.read_u8(normalized) << 8) | self.read_u8(normalized + 1)

    def read_u32(self, address: int) -> int:
        normalized = self._normalize_rdram_address(address)
        if normalized & 3:
            return (
                (self.read_u8(normalized) << 24)
                | (self.read_u8(normalized + 1) << 16)
                | (self.read_u8(normalized + 2) << 8)
                | self.read_u8(normalized + 3)
            )
        return self._read_word(normalized)

    def write_u8(self, address: int, value: int):
        normalized = self._normalize_rdram_address(address)
        word_address = normalized & ~3
        shift = (3 - (normalized & 3)) * 8
        word = self._read_word(word_address)
        word = (word & ~(0xFF << shift)) | ((value & 0xFF) << shift)
        self._write_word(word_address, word)

    def write_u16(self, address: int, value: int):
        normalized = self._normalize_rdram_address(address)
        remainder = normalized & 3
        if remainder <= 2:
            word_address = normalized & ~3
            shift = (2 - remainder) * 8
            word = self._read_word(word_address)
            word = (word & ~(0xFFFF << shift)) | ((value & 0xFFFF) << shift)
            self._write_word(word_address, word)
            return
        self.write_u8(normalized, (value >> 8) & 0xFF)
        self.write_u8(normalized + 1, value & 0xFF)

    def write_u32(self, address: int, value: int):
        normalized = self._normalize_rdram_address(address)
        if normalized & 3:
            self.write_u8(normalized, (value >> 24) & 0xFF)
            self.write_u8(normalized + 1, (value >> 16) & 0xFF)
            self.write_u8(normalized + 2, (value >> 8) & 0xFF)
            self.write_u8(normalized + 3, value & 0xFF)
            return
        self._write_word(normalized, value)

    def validate_rom(self) -> bool:
        try:
            return (
                self.read_u32(OOT_COOP_VERSION_ADDR) == OOT_COOP_VERSION_EXPECTED
                and self.read_u32(OOT_COSMETIC_FORMAT_VERSION_ADDR) == OOT_COSMETIC_FORMAT_VERSION_EXPECTED
            )
        except Exception:
            return False


EMULATOR_CONFIGS: Dict[Emulators, EmulatorInfo] = {
    Emulators.Project64Scan: EmulatorInfo(
        Emulators.Project64Scan, "Project64-compatible", "project64",
        False, None, False, 0x00000000, 0x80000000, range_step=0x10000,
    ),
    Emulators.Project64_EM: EmulatorInfo(
        Emulators.Project64_EM, "Project64-EM (PJ64 3.0.1)", "project64-em",
        False, None, False, 0, 0, scan_memory_for_signature=True,
    ),
    Emulators.Project64_v4: EmulatorInfo(
        Emulators.Project64_v4, "Project64 4.0", "project64",
        False, None, False, 0xFDD00000, 0xFE1FFFFF,
    ),
    Emulators.BizHawk: EmulatorInfo(
        Emulators.BizHawk, "BizHawk", "emuhawk",
        True, "mupen64plus.dll", False, 0x5A000, 0x5658DF,
        linux_dll_name="libmupen64plus.so",
    ),
    Emulators.RMG: EmulatorInfo(
        Emulators.RMG, "Rosalie's Mupen GUI", "rmg",
        True, "mupen64plus.dll", True, 0x29C15D8, 0x2FC15D8,
        extra_offset=0x80000000, linux_dll_name="libmupen64plus.so",
    ),
    Emulators.Simple64: EmulatorInfo(
        Emulators.Simple64, "simple64", "simple64-gui",
        True, "libmupen64plus.dll", True, 0x1380000, 0x29C95D8,
        linux_dll_name="libmupen64plus.so",
    ),
    Emulators.ParallelLauncher: EmulatorInfo(
        Emulators.ParallelLauncher, "Parallel Launcher", "retroarch",
        True, "parallel_n64_next_libretro.dll", True, 0x845000, 0xD56000,
        linux_dll_name="parallel_n64_next_libretro.so",
    ),
    Emulators.ParallelLauncher903: EmulatorInfo(
        Emulators.ParallelLauncher903, "Parallel Launcher (9.0.3+)", "retroarch",
        True, "parallel_n64_next_libretro.dll", True, 0x1400000, 0x1800000,
        linux_dll_name="parallel_n64_next_libretro.so",
    ),
    Emulators.RetroArch: EmulatorInfo(
        Emulators.RetroArch, "RetroArch", "retroarch",
        True, "mupen64plus_next_libretro.dll", True, 0, 0xFFFFFF,
        range_step=4, linux_dll_name="mupen64plus_next_libretro.so",
    ),
    Emulators.Project64: EmulatorInfo(
        Emulators.Project64, "Project64", "project64",
        False, None, False, 0xDFD00000, 0xE01FFFFF,
    ),
    Emulators.Gopher64: EmulatorInfo(
        Emulators.Gopher64, "Gopher64", "gopher64",
        False, None, False, 0, 0, scan_memory_for_signature=True,
    ),
    Emulators.Ares: EmulatorInfo(
        Emulators.Ares, "ares", "ares",
        False, None, False, 0, 0, scan_memory_for_signature=True, signature_alignment=0x1000,
    ),
}


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


def connect_to_emulator() -> Optional[Any]:
    """Try each emulator profile and return the first one that attaches successfully."""
    global _last_connect_status, _last_connect_status_time

    errors: List[Tuple[str, str]] = []
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
    if IS_MACOS:
        _log_connect_status(errors)
        return None

    for emu in Emulators:
        info = EMULATOR_CONFIGS[emu]
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
    _log_connect_status(errors)
    return None


class EmuLoaderClient:
    def __init__(self):
        self.emulator_info: Optional[Any] = None
        self.connected = False

    def connect(self) -> bool:
        self.emulator_info = connect_to_emulator()
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
        return self.emulator_info.validate_rom()  # pyright: ignore[reportOptionalMemberAccess]
