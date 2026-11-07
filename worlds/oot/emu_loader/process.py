"""Process and memory access utilities for EmuLoader."""

import ctypes
import glob
import os
import platform
from typing import Any, Dict, List, Optional, Set, Tuple

from .ptrace import check_and_fix_ptrace_scope

# Detect operating system
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

# Windows API constants and structures
if IS_WINDOWS:
    import ctypes.wintypes

    PROCESS_VM_READ = 0x0010
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    TH32CS_SNAPMODULE = 0x00000008
    TH32CS_SNAPMODULE32 = 0x00000010
    TH32CS_SNAPPROCESS = 0x00000002
    MAX_PATH = 260

    class MODULEENTRY32(ctypes.Structure):
        """Module entry structure for Windows API."""

        _fields_ = [
            ("dwSize", ctypes.wintypes.DWORD),
            ("th32ModuleID", ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("GlblcntUsage", ctypes.wintypes.DWORD),
            ("ProccntUsage", ctypes.wintypes.DWORD),
            ("modBaseAddr", ctypes.POINTER(ctypes.wintypes.BYTE)),
            ("modBaseSize", ctypes.wintypes.DWORD),
            ("hModule", ctypes.wintypes.HMODULE),
            ("szModule", ctypes.c_char * 256),
            ("szExePath", ctypes.c_char * 260),
        ]

    class PROCESSENTRY32(ctypes.Structure):
        """Process entry structure for Windows API."""

        _fields_ = [
            ("dwSize", ctypes.wintypes.DWORD),
            ("cntUsage", ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.wintypes.ULONG)),
            ("th32ModuleID", ctypes.wintypes.DWORD),
            ("cntThreads", ctypes.wintypes.DWORD),
            ("th32ParentProcessID", ctypes.wintypes.DWORD),
            ("pcPriClassBase", ctypes.wintypes.LONG),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("szExeFile", ctypes.c_char * MAX_PATH),
        ]

    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        """Memory region descriptor returned by VirtualQueryEx."""

        _fields_ = [
            ("BaseAddress", ctypes.c_void_p),
            ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", ctypes.wintypes.DWORD),
            ("RegionSize", ctypes.c_size_t),
            ("State", ctypes.wintypes.DWORD),
            ("Protect", ctypes.wintypes.DWORD),
            ("Type", ctypes.wintypes.DWORD),
        ]

    MEM_COMMIT = 0x1000
    MEM_PRIVATE = 0x20000
    PAGE_NOACCESS = 0x01
    PAGE_READWRITE = 0x04
    PAGE_EXECUTE_READWRITE = 0x40
    PAGE_GUARD = 0x100

    def _get_windows_processes() -> List[Dict[str, Any]]:
        """Get running processes on Windows using native API."""
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
                        process_name = pe32.szExeFile.decode("utf-8")
                        processes.append({"name": process_name, "pid": pe32.th32ProcessID})
                    except UnicodeDecodeError:
                        pass

                    if not ctypes.windll.kernel32.Process32Next(snapshot, ctypes.byref(pe32)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)

        return processes


def _get_linux_processes() -> List[Dict[str, Any]]:
    """Get running processes on Linux by reading /proc."""
    processes: List[Dict[str, Any]] = []

    try:
        for pid_dir in glob.glob("/proc/[0-9]*"):
            try:
                pid = int(os.path.basename(pid_dir))
                comm_path = os.path.join(pid_dir, "comm")
                if os.path.exists(comm_path):
                    with open(comm_path, "r") as f:
                        process_name = f.read().strip()
                        processes.append({"name": process_name, "pid": pid})
            except (ValueError, OSError, IOError):
                continue
    except OSError:
        pass

    return processes


def get_running_processes() -> List[Dict[str, Any]]:
    """Get list of running processes using native OS methods."""
    if IS_WINDOWS:
        return _get_windows_processes()
    elif IS_LINUX:
        return _get_linux_processes()
    return []


class ModuleInfo:
    """Info relating to a module in the process."""

    name: str
    lpBaseOfDll: Optional[int]

    def __init__(self, name: str, lpBaseOfDll: Optional[int]):
        """Initialize with the module name and base address."""
        self.name = name
        self.lpBaseOfDll = lpBaseOfDll


class ProcessMemory:
    """Class to handle process memory operations using ctypes on Windows and Linux."""

    def __init__(self, process_name: str, pid: Optional[int] = None):
        """Initialize with the process name. If pid is provided, attach to that specific PID instead of the first match by name."""
        self.process_name = process_name
        self.process_handle = None
        self.process_id = None
        self.mem_fd = None  # File descriptor for Linux /proc/pid/mem
        self._attach_to_process(pid)

    def _attach_to_process(self, target_pid: Optional[int] = None):
        """Attach to the process by name, or by specific pid when provided."""
        processes = get_running_processes()

        for proc in processes:
            if target_pid is not None:
                matches = proc["pid"] == target_pid
            else:
                matches = bool(proc["name"]) and proc["name"].lower().startswith(self.process_name.lower())
            if matches:
                self.process_id = proc["pid"]

                if IS_WINDOWS:
                    self.process_handle = ctypes.windll.kernel32.OpenProcess(
                        PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION,
                        False,
                        self.process_id,
                    )
                    if not self.process_handle:
                        raise Exception(f"Failed to open process {self.process_name}")
                elif IS_LINUX:
                    check_and_fix_ptrace_scope()
                    try:
                        self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                    except (OSError, IOError) as e:
                        if e.errno in (1, 13):
                            if check_and_fix_ptrace_scope():
                                try:
                                    self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                                except (OSError, IOError) as retry_e:
                                    raise Exception(
                                        f"Failed to open memory file for process {self.process_name} after fixing ptrace: {retry_e}"
                                    )
                            else:
                                raise Exception(
                                    f"Failed to open memory file for process {self.process_name}: {e}. Ptrace restrictions may be blocking access."
                                )
                        else:
                            raise Exception(f"Failed to open memory file for process {self.process_name}: {e}")
                return
        raise Exception(f"Process {self.process_name} not found")

    def list_modules(self) -> List[ModuleInfo]:
        """List modules in the process."""
        if IS_WINDOWS:
            return self._list_modules_windows()
        elif IS_LINUX:
            return self._list_modules_linux()
        return []

    def _list_modules_windows(self) -> List[ModuleInfo]:
        """List modules on Windows."""
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
                    module_info = ModuleInfo(
                        name=me32.szModule.decode("utf-8"),
                        lpBaseOfDll=ctypes.cast(me32.modBaseAddr, ctypes.c_void_p).value,
                    )
                    modules.append(module_info)

                    if not ctypes.windll.kernel32.Module32Next(snapshot, ctypes.byref(me32)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)

        return modules

    def _list_modules_linux(self) -> List[ModuleInfo]:
        """List modules on Linux by reading /proc/pid/maps."""
        modules: List[ModuleInfo] = []
        if not self.process_id:
            return modules

        try:
            with open(f"/proc/{self.process_id}/maps", "r") as maps_file:
                seen_modules: Set[str] = set()
                for line in maps_file:
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        address_range = parts[0]
                        permissions = parts[1]
                        pathname = parts[5] if len(parts) > 5 else ""

                        if "x" in permissions and pathname and pathname != "[vdso]" and not pathname.startswith("["):
                            module_name = os.path.basename(pathname)
                            if module_name not in seen_modules:
                                start_addr = int(address_range.split("-")[0], 16)
                                modules.append(ModuleInfo(name=module_name, lpBaseOfDll=start_addr))
                                seen_modules.add(module_name)
        except (OSError, IOError):
            pass

        return modules

    def list_writable_regions(self, min_size: int = 0x800000) -> List[Tuple[int, int]]:
        """List anonymous read/write memory regions of at least min_size bytes."""
        if IS_WINDOWS:
            return self._list_writable_regions_windows(min_size)
        elif IS_LINUX:
            return self._list_writable_regions_linux(min_size)
        return []

    def _list_writable_regions_linux(self, min_size: int) -> List[Tuple[int, int]]:
        """Walk /proc/pid/maps for anonymous (heap-like) read/write mappings."""
        regions: List[Tuple[int, int]] = []
        if not self.process_id:
            return regions

        try:
            with open(f"/proc/{self.process_id}/maps", "r") as maps_file:
                for line in maps_file:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    address_range = parts[0]
                    permissions = parts[1]
                    pathname = parts[5] if len(parts) > 5 else ""

                    if "r" not in permissions or "w" not in permissions:
                        continue
                    # Keep anonymous mappings, [heap], and [anon:*]; skip file-backed and [stack]/[vdso]/etc.
                    if pathname and pathname != "[heap]" and not pathname.startswith("[anon"):
                        continue

                    try:
                        start_str, end_str = address_range.split("-")
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
        """Walk address space via VirtualQueryEx for committed private read/write regions."""
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
        """Read bytes from process memory."""
        if IS_WINDOWS:
            return self._read_bytes_windows(address, size)
        elif IS_LINUX:
            return self._read_bytes_linux(address, size)
        else:
            raise Exception("Unsupported operating system")

    def _read_bytes_windows(self, address: int, size: int) -> bytes:
        """Read bytes from process memory on Windows."""
        if not self.process_handle:
            raise Exception("Process not attached")

        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.wintypes.DWORD(0)

        result = ctypes.windll.kernel32.ReadProcessMemory(
            self.process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read)
        )

        if not result:
            raise Exception(f"Failed to read memory at address 0x{address:08x}")

        return buffer.raw[: bytes_read.value]

    def _read_bytes_linux(self, address: int, size: int) -> bytes:
        """Read bytes from process memory on Linux."""
        if self.mem_fd is None:
            raise Exception("Process not attached")

        try:
            data = os.pread(self.mem_fd, size, address)
            if len(data) != size:
                raise Exception(f"Failed to read {size} bytes at address 0x{address:08x}")
            return data
        except (OSError, IOError) as e:
            raise Exception(f"Failed to read memory at address 0x{address:08x}: {e}")

    def write_bytes(self, address: int, data: bytes, size: int):
        """Write bytes to process memory."""
        if IS_WINDOWS:
            self._write_bytes_windows(address, data, size)
        elif IS_LINUX:
            self._write_bytes_linux(address, data, size)
        else:
            raise Exception("Unsupported operating system")

    def _write_bytes_windows(self, address: int, data: bytes, size: int):
        """Write bytes to process memory on Windows."""
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
        """Write bytes to process memory on Linux."""
        if self.mem_fd is None:
            raise Exception("Process not attached")

        try:
            written = os.pwrite(self.mem_fd, data[:size], address)
            if written != size:
                raise Exception(f"Failed to write {size} bytes at address 0x{address:08x}")
        except (OSError, IOError) as e:
            raise Exception(f"Failed to write memory at address 0x{address:08x}: {e}")

    def read_int(self, address: int) -> int:
        """Read a 4-byte integer from memory."""
        data = self.read_bytes(address, 4)
        return int.from_bytes(data, "little")

    def read_longlong(self, address: int) -> int:
        """Read an 8-byte long long from memory."""
        data = self.read_bytes(address, 8)
        return int.from_bytes(data, "little")

    def close(self):
        """Close the process handle or file."""
        if IS_WINDOWS and self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
        elif IS_LINUX and self.mem_fd is not None:
            os.close(self.mem_fd)
            self.mem_fd = None
