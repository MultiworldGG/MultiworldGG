"""RetroArch Network Commands memory backend for EmuLoader."""

import socket
from typing import Optional

RETROARCH_COMMAND_HOST = "127.0.0.1"
RETROARCH_COMMAND_PORT = 55355
RETROARCH_COMMAND_TIMEOUT = 0.5
N64_KSEG1_BASE = 0xA0000000


class RetroArchNetworkInfo:
    """RetroArch Network Commands memory backend.

    Uses RetroArch's UDP network command interface to read/write emulated memory.
    This avoids process-memory attach entirely and is the only supported backend on macOS.
    """

    readable_emulator_name = "RetroArch Network Commands"

    def __init__(
        self,
        host: str = RETROARCH_COMMAND_HOST,
        port: int = RETROARCH_COMMAND_PORT,
        timeout: float = RETROARCH_COMMAND_TIMEOUT,
    ):
        """Initialize with host, port, and timeout for the RetroArch UDP command interface."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.connection_error: Optional[str] = None
        self.runtime_error: Optional[str] = None

    def attach_to_emulator(self) -> Optional["RetroArchNetworkInfo"]:
        """Connect to RetroArch Network Commands and verify it responds."""
        self.disconnect()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            self.socket = sock
            # Send a test read to verify the connection works
            self._read_word(0x00000000)
            return self
        except socket.timeout:
            self.connection_error = (
                f"RetroArch Network Commands did not respond. Enable Settings > Network > Network Commands "
                f"and leave the command port at {self.port}."
            )
        except OSError as exc:
            self.connection_error = (
                f"RetroArch Network Commands unavailable. Enable Settings > Network > Network Commands "
                f"and leave the command port at {self.port}. ({exc})"
            )
        except Exception as exc:
            self.connection_error = f"RetroArch Network Commands read failed: {exc}"
        self.disconnect()
        return None

    def disconnect(self):
        """Close the UDP socket."""
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
        return int.from_bytes(data, byteorder="little")

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

    def read_u8(self, address: int) -> int:
        """Read an 8-bit unsigned integer from N64 memory."""
        normalized = self._normalize_rdram_address(address)
        word = self._read_word(normalized & ~3)
        shift = (3 - (normalized & 3)) * 8
        return (word >> shift) & 0xFF

    def read_u16(self, address: int) -> int:
        """Read a 16-bit unsigned integer from N64 memory."""
        normalized = self._normalize_rdram_address(address)
        remainder = normalized & 3
        if remainder <= 2:
            word = self._read_word(normalized & ~3)
            shift = (2 - remainder) * 8
            return (word >> shift) & 0xFFFF
        return (self.read_u8(normalized) << 8) | self.read_u8(normalized + 1)

    def read_u32(self, address: int) -> int:
        """Read a 32-bit unsigned integer from N64 memory."""
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
        """Write an 8-bit unsigned integer to N64 memory."""
        normalized = self._normalize_rdram_address(address)
        word_address = normalized & ~3
        shift = (3 - (normalized & 3)) * 8
        word = self._read_word(word_address)
        word = (word & ~(0xFF << shift)) | ((value & 0xFF) << shift)
        self._write_word(word_address, word)

    def write_u16(self, address: int, value: int):
        """Write a 16-bit unsigned integer to N64 memory."""
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
        """Write a 32-bit unsigned integer to N64 memory."""
        normalized = self._normalize_rdram_address(address)
        if normalized & 3:
            self.write_u8(normalized, (value >> 24) & 0xFF)
            self.write_u8(normalized + 1, (value >> 16) & 0xFF)
            self.write_u8(normalized + 2, (value >> 8) & 0xFF)
            self.write_u8(normalized + 3, value & 0xFF)
            return
        self._write_word(normalized, value)
