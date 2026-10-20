"""
A module for interacting with Project64 through an embedded JavaScript TCP server.

Based heavily on the BizHawk implementation details.
"""

import asyncio
import enum
import json
from typing import Any, Union

class ConnectionStatus(enum.IntEnum):
    NOT_CONNECTED = 1
    TENTATIVE = 2
    CONNECTED = 3

class NotConnectedError(Exception):
    """Raised when an operation is attempted before a connection is established."""
    pass

class RequestFailedError(Exception):
    """Raised when the Project64 script does not respond or times out."""
    pass

class ConnectorError(Exception):
    """Raised when the emulator script explicitly returns an error message."""
    pass


class PJ64Context:
    streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None
    connection_status: ConnectionStatus
    _lock: asyncio.Lock
    _port: int | None
    _message_id_counter: int
    ap_port: int

    def __init__(self, ap_port) -> None:
        self.streams = None
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        self._lock = asyncio.Lock()
        self._port = None
        self._message_id_counter = 0
        self.ap_port = ap_port

    def _get_next_message_id(self) -> int:
        self._message_id_counter = (self._message_id_counter + 1) & 0xFFFF
        return self._message_id_counter

    async def _send_raw_command(self, command_string: str) -> str:
        """Frames the command with a message ID, sends it, and awaits the response."""
        async with self._lock:
            if self.streams is None:
                raise NotConnectedError("You tried to send a request before a connection to Project64 was made.")

            msg_id = self._get_next_message_id()
            full_payload = f"{msg_id}:{command_string}\n"

            try:
                reader, writer = self.streams
                writer.write(full_payload.encode("utf-8"))
                await asyncio.wait_for(writer.drain(), timeout=5)

                res_bytes = await asyncio.wait_for(reader.readline(), timeout=5)

                if res_bytes == b"":
                    writer.close()
                    self.streams = None
                    self.connection_status = ConnectionStatus.NOT_CONNECTED
                    raise RequestFailedError("Connection closed by Project64 server.")

                if self.connection_status == ConnectionStatus.TENTATIVE:
                    self.connection_status = ConnectionStatus.CONNECTED

                response_str = res_bytes.decode("utf-8").strip()

                if response_str.startswith("ERR:"):
                    raise ConnectorError(response_str)

                parts = response_str.split(":", 1)
                if len(parts) < 2:
                    raise RequestFailedError(f"Malformed tracking frame received: {response_str}")

                resp_id, payload = parts[0].strip(), parts[1].strip()
                if int(resp_id) != msg_id:
                    raise RequestFailedError(f"Sync error: Sent ID {msg_id}, got response ID {resp_id}")

                elif payload.startswith("Invalid") or payload.startswith("Unknown"):
                    raise ConnectorError(f"PJ64 Script Error: {payload}")

                return payload

            except asyncio.TimeoutError as exc:
                writer.close()
                self.streams = None
                self.connection_status = ConnectionStatus.NOT_CONNECTED
                raise RequestFailedError("Connection timed out waiting for response.") from exc
            except ConnectionResetError as exc:
                writer.close()
                self.streams = None
                self.connection_status = ConnectionStatus.NOT_CONNECTED
                raise RequestFailedError("Connection reset by remote host.") from exc

async def pj64connect(ctx: PJ64Context) -> bool:
    """Attempts to establish a TCP connection with the Project64 server."""
    try:
        ctx.streams = await asyncio.open_connection("127.0.0.1", ctx.ap_port)
        ctx.connection_status = ConnectionStatus.TENTATIVE
        ctx._port = ctx.ap_port
        return True
    except (TimeoutError, ConnectionRefusedError):
        pass

    ctx.streams = None
    ctx.connection_status = ConnectionStatus.NOT_CONNECTED
    return False

def pj64disconnect(ctx: PJ64Context) -> None:
    """Closes the connection to the Project64 script server."""
    if ctx.streams is not None:
        try:
            ctx.streams[1].close()
        except Exception:
            pass
        ctx.streams = None
    ctx.connection_status = ConnectionStatus.NOT_CONNECTED

async def pj64_get_rom_info(ctx: PJ64Context) -> dict[str, Any]:
    """Gets meta-information about the currently running N64 game."""
    response = await ctx._send_raw_command("romInfo")
    return json.loads(response)

async def pj64_read_memory(ctx: PJ64Context, data_type: str, address: int, size: int) -> Union[str, list[int]]:
    """Reads a block of data from emulated memory.

    data_type can be: 'u8', 'u16', 'u32', or 'bytestring'
    """
    # Format address as a hex string match for JavaScript's parseInt(..., 16)
    hex_addr = hex(address)
    cmd = f"read {data_type} {hex_addr} {size}"
    response = await ctx._send_raw_command(cmd)

    if data_type == "bytestring":
        return response

    return json.loads(response)

async def pj64_read_dictionary(ctx: PJ64Context, lookup_dict: dict[str, Any]) -> dict[str, list[int]]:
    """Performs a highly optimized batch lookup using a mapping schema dictionary.

    Example input:
       {"health": {"type": "u8", "adr": 0x80001234, "size": 1}}
    """
    json_payload = json.dumps(lookup_dict)
    cmd = f"dict {json_payload}"
    response = await ctx._send_raw_command(cmd)
    return json.loads(response)

async def pj64_write_memory(ctx: PJ64Context, data_type: str, address: int, value: Union[str, list[int]]) -> bool:
    """Writes structured array values or a bytestring to an emulated memory block.

    data_type can be: 'u8', 'u16', 'u32', or 'bytestring'
    """
    hex_addr = hex(address)

    if data_type == "bytestring":
        if not isinstance(value, str):
            raise ValueError("Value must be a string when using 'bytestring' type.")
        payload = value
    else:
        if not isinstance(value, list):
            raise ValueError("Value must be a list of integers for numeric types.")
        payload = json.dumps(value)

    cmd = f"write {data_type} {hex_addr} {payload}"
    response = await ctx._send_raw_command(cmd)

    return "successful" in response
