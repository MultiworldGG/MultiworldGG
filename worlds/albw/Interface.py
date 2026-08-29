from typing import Optional
import enum
import socket
import struct
import asyncio

class ConnectionError(Exception):
    pass

class RequestType(enum.IntEnum):
    Ping = 0
    Read = 1
    Write = 2
    ProcessList = 3
    SetGetProcess = 4

class N3DSInterface:
    PACKET_VERSION: int = 1
    HEADER_SIZE: int = 0x10
    MAX_PACKET_SIZE: int = 0x410
    TIMEOUT: float = 1.0

    sock: socket.socket
    max_request_size: int
    id: int

    def __init__(self):
        self.id = 0
        self.max_request_size = 32
    
    def _max_read_size(self) -> int:
        return self.max_request_size
    
    def _max_write_size(self) -> int:
        return self.max_request_size - 8
    
    async def _send_packet(self, request_type: RequestType, request_data: bytes, response_size: Optional[int] = None, retry: bool = True) -> bytes:
        loop = asyncio.get_running_loop()
        tries = 4 if retry else 1
        for _ in range(tries):
            try:
                request_id = self.id
                self.id = (self.id + 1) & 0xffffffff
                request = struct.pack("=IIII", self.PACKET_VERSION, request_id, request_type, len(request_data))
                request += request_data
                await asyncio.wait_for(loop.sock_sendall(self.sock, request), self.TIMEOUT)
                for _ in range(16):
                    response = await asyncio.wait_for(loop.sock_recv(self.sock, self.MAX_PACKET_SIZE), self.TIMEOUT)
                    if not response or len(response) < self.HEADER_SIZE:
                        break
                    version, id, response_type, size = struct.unpack("=IIII", response[:self.HEADER_SIZE])
                    if version == self.PACKET_VERSION and id == request_id and response_type == request_type:
                        return response[self.HEADER_SIZE:]
            except Exception as e:
                continue
        raise ConnectionError("Lost connection to game")

    async def _set_process(self, title: int) -> bool:
        start_process = 0
        while True:
            request_data = struct.pack("=II", start_process, 0x7fffffff)
            try:
                response = await self._send_packet(RequestType.ProcessList, request_data, retry=False)
                if len(response) < 4:
                    self.max_request_size = 32
                    return True
                count = struct.unpack("=I", response[0:4])[0]
                if count == 0:
                    return False
                start_process += count
                for i in range(count):
                    proc_id, title_id = struct.unpack("=IQ", response[i * 0x14 + 4 : i * 0x14 + 0x10])
                    if title_id == title:
                        request_data = struct.pack("=II", 1, proc_id)
                        await self._send_packet(RequestType.SetGetProcess, request_data, 0)
                        self.max_request_size = 1024
                        return True
            except ConnectionError:
                # if no response, assume we are on an older version
                self.max_request_size = 32
                return True

    async def connect(self, address: str, title: int) -> bool:
        self.disconnect()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((address, 45987))
        self.sock.setblocking(False)
        try:
            await self._send_packet(RequestType.Ping, b"", 0)
            return await self._set_process(title)
        except ConnectionError:
            return False

    def disconnect(self):
        if hasattr(self, 'sock'):
            self.sock.close()

    async def read(self, address: int, size: int) -> bytes:
        mem = b""
        while size > 0:
            request_size = min(size, self._max_read_size())
            request_data = struct.pack("=II", address, request_size)
            mem += await self._send_packet(RequestType.Read, request_data, request_size)
            address += request_size
            size -= request_size
        return mem

    async def write(self, address: int, data: bytes) -> None:
        start = 0
        while start < len(data):
            end = min(start + self._max_write_size(), len(data))
            request_data = struct.pack("=II", address + start, end - start)
            request_data += data[start:end]
            await self._send_packet(RequestType.Write, request_data, 0, retry=False)
            start += self._max_write_size()

    async def read_u8(self, address: int) -> int:
        return int.from_bytes(await self.read(address, 1), "little")

    async def read_u32(self, address: int) -> int:
        return int.from_bytes(await self.read(address, 4), "little")
    
    async def write_u32(self, address: int, value: int) -> None:
        await self.write(address, value.to_bytes(4, "little"))
