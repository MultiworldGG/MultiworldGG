"""EmuLoaderClient - high-level drop-in client for emulator memory access."""

import asyncio
from typing import Callable, Optional

from .emulatorinfo import EmulatorInfo, connect_to_emulator, load_emulator_configs
from .process import ProcessMemory

try:
    from CommonClient import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


class EmuLoaderClient:
    """Drop-in replacement client for PJ64Client using direct memory access."""

    def __init__(
        self,
        signature_offset: Optional[int] = None,
        signature_value: Optional[int] = None,
        validation_func: Optional[Callable[["ProcessMemory", int], bool]] = None,
        pull_from_web: bool = True,
    ):
        """Initialize the EmuLoaderClient and connect to an available emulator.

        A game must supply EITHER a (signature_offset, signature_value) pair OR a
        validation_func -- the client itself holds no game-specific defaults.

        Args:
            signature_offset: The offset from RDRAM base used to locate the signature value.
                              When given (with signature_value), the candidate RDRAM base is
                              confirmed by a fixed-value equality check.
            signature_value: The expected 32-bit value at signature_offset that confirms
                             the correct RDRAM base was found.
            validation_func: Optional callable that receives (ProcessMemory, candidate_offset)
                             and returns True if the candidate offset is the correct RDRAM base.
                             When provided, it replaces the (signature_offset, signature_value)
                             equality check -- use it for games whose RDRAM marker is a pointer
                             chain rather than a fixed constant (e.g. Banjo-Tooie).
            pull_from_web: If True, fetch emulator configs from the web before falling
                           back to the local bundled file. Defaults to True.

        Raises:
            ValueError: if neither a validation_func nor a complete
                        (signature_offset, signature_value) pair is supplied.
        """
        if validation_func is None and (signature_offset is None or signature_value is None):
            raise ValueError(
                "EmuLoaderClient requires a way to detect the RDRAM base: pass either a "
                "validation_func, or both signature_offset and signature_value."
            )
        self.emulator_info: Optional[EmulatorInfo] = None
        self.connected = False
        self._poll_task: Optional[asyncio.Task] = None
        self._not_connected_logged = False
        self.configs = load_emulator_configs(pull_from_web=pull_from_web)
        for emu in self.configs.values():
            if signature_offset is not None:
                emu.signature_offset = signature_offset
            if signature_value is not None:
                emu.signature_value = signature_value
            emu.validation_func = validation_func
        self.connect()

    def connect(self) -> bool:
        """Connect to an available emulator."""
        self.emulator_info = connect_to_emulator(configs=self.configs)
        self.connected = self.emulator_info is not None
        return self.connected

    def disconnect(self):
        """Disconnect from the emulator."""
        if self.emulator_info:
            self.emulator_info.disconnect()
        self.connected = False
        self.emulator_info = None

    def is_connected(self) -> bool:
        """Check if connected to an emulator.

        This serves as a safety check for the memory access methods below, so pyright ignore
        annotations have been added to them. Be careful if editing this method!
        """
        return self.connected and self.emulator_info is not None

    def _check_not_connected(self) -> bool:
        """Log a not-connected warning once. Returns True if NOT connected (caller should return early)."""
        if not self.is_connected():
            if not self._not_connected_logged:
                logger.warning("Not connected to emulator.")
                self._not_connected_logged = True
            return True
        return False

    # Direct memory access methods
    def read_u8(self, address: int) -> int:
        """Read an 8-bit unsigned integer from memory."""
        if self._check_not_connected():
            return 0
        return self.emulator_info.read_u8(address)  # pyright: ignore[reportOptionalMemberAccess]

    def read_u16(self, address: int) -> int:
        """Read a 16-bit unsigned integer from memory."""
        if self._check_not_connected():
            return 0
        return self.emulator_info.read_u16(address)  # pyright: ignore[reportOptionalMemberAccess]

    def read_u32(self, address: int) -> int:
        """Read a 32-bit unsigned integer from memory."""
        if self._check_not_connected():
            return 0
        return self.emulator_info.read_u32(address)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u8(self, address: int, value: int):
        """Write an 8-bit unsigned integer to memory."""
        if self._check_not_connected():
            return
        self.emulator_info.write_u8(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u16(self, address: int, value: int):
        """Write a 16-bit unsigned integer to memory."""
        if self._check_not_connected():
            return
        self.emulator_info.write_u16(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u32(self, address: int, value: int):
        """Write a 32-bit unsigned integer to memory."""
        if self._check_not_connected():
            return
        self.emulator_info.write_u32(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def read_bytestring(self, address: int, length: int) -> str:
        """Read a bytestring from memory."""
        if self._check_not_connected():
            return ""
        return self.emulator_info.read_bytestring(address, length)  # pyright: ignore[reportOptionalMemberAccess]

    def write_bytestring(self, address: int, data: str):
        """Write a bytestring to memory."""
        if self._check_not_connected():
            return
        self.emulator_info.write_bytestring(address, data)  # pyright: ignore[reportOptionalMemberAccess]

    async def wait_for_emulator(self, validate: Optional[Callable[["EmuLoaderClient"], bool]] = None):
        """Wait for emulator to connect and optionally validate a condition (e.g. ROM loaded).

        Runs as a background task, polling every second without blocking the UI.

        Args:
            validate: An optional callable that receives this client instance and returns True
                      when the emulator state is considered valid (e.g. the correct ROM is loaded).
                      If None, only the emulator connection is required.
        """
        logged_waiting_connection = False
        logged_waiting_valid = False

        if self._poll_task is not None and not self._poll_task.done():
            await self._poll_task
            return

        loop = asyncio.get_event_loop()

        async def _poll():
            nonlocal logged_waiting_connection, logged_waiting_valid
            while True:
                try:
                    if not self.is_connected():
                        if not logged_waiting_connection:
                            logger.info("Waiting on connection to emulator...")
                            logged_waiting_connection = True
                        await loop.run_in_executor(None, self.connect)
                        await asyncio.sleep(1.0)
                        continue

                    logged_waiting_connection = False

                    if validate is not None:
                        valid = await loop.run_in_executor(None, validate, self)
                        if not valid:
                            if not logged_waiting_valid:
                                logger.info("Waiting on valid state...")
                                logged_waiting_valid = True
                            await asyncio.sleep(1.0)
                            continue

                    logged_waiting_valid = False
                    self._not_connected_logged = False
                    logger.info("Emulator connected and ready!")
                    return
                except Exception as e:
                    logger.error(f"Error connecting to emulator, retrying... {str(e)}")
                    self.disconnect()
                    await asyncio.sleep(1.0)

        self._poll_task = asyncio.ensure_future(_poll())
        await self._poll_task
