from enum import Enum
from ctypes import c_short as short, c_ushort as ushort, c_byte as sbyte, c_ubyte as byte, c_byte, c_ubyte
from math import trunc
from typing import Any

class PacketType(Enum):
    Unknown : short = 0
    Init : short = 1
    PlayerInfo : short = 2
    HackCapInfo : short = 3
    GameInfo : short = 4
    TagInfo : short = 5
    Connect : short = 6
    Disconnect : short = 7
    CostumeInfo : short = 8
    Check : short = 9
    CaptureInfo : short = 10
    ChangeStage : short = 11
    Command : short = 12
    ArchipelagoChat : short = 13
    SlotData : short = 14
    DeathLink : short = 16
    ShineChecks : short = 17
    ApInfo : short = 18
    ShopReplace : short = 19
    ShineReplace : short = 20
    ShineColor : short = 21
    ShineHint : short = 22
    #UDPInit : short = 26
    #HolePunch : short = 27

class ConnectionType(Enum):
    Connect = 0
    Reconnect = 1

class ItemType(Enum):
    Coins = -2
    Moon = -1
    Clothes = 0
    Cap = 1
    Souvenir = 2
    Sticker = 3
    RegionalCoin = 4
    Capture = 5


#region Check Packets

class CheckPacket:
    OBJ_ID_SIZE = 0x10
    STAGE_NAME_SIZE = 0x30
    location_id : int
    # Shop Items
    item_type : ItemType
    # Prevent Repeat Filler ETC
    index : int
    # OBJ ID
    obj_id : str
    # Stage
    stage : str
    # Coins
    amount : int
    SIZE : short = 16 + 0x10 + 0x30

    def __init__(self, packet_bytes : bytearray = None, location_id : int = None, item_type : int = None, index : int = None, obj_id : str = None, stage : str = None, amount : int = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.location_id = location_id
            self.item_type = ItemType(item_type)
            self.index = index
            self.obj_id = obj_id
            self.stage = stage
            self.amount = amount

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.location_id.to_bytes(4, "little", signed=True)
        data += self.item_type.value.to_bytes(4, "little", signed=True)
        data += self.index.to_bytes(4, "little", signed=True)
        data += self.obj_id.encode()
        while len(data) < 12 + self.OBJ_ID_SIZE:
            data += b"\x00"
        data += self.stage.encode()
        while len(data) < 12 + self.OBJ_ID_SIZE + self.STAGE_NAME_SIZE:
            data += b"\x00"
        data += self.amount.to_bytes(4, "little", signed=True)
        if len(data) != self.SIZE:
            raise f"CheckPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset = 0
        self.location_id  = int.from_bytes(data[offset:offset + 4], "little")
        offset += 4
        self.item_type  = ItemType(int.from_bytes(data[offset:offset + 4], "little",signed=True))
        offset += 4
        self.index  = int.from_bytes(data[offset:offset + 4], "little",signed=True)
        offset += 4
        self.obj_id = data[offset:offset + self.OBJ_ID_SIZE].decode()
        offset += self.OBJ_ID_SIZE
        self.stage = data[offset:offset + self.STAGE_NAME_SIZE].decode()
        offset += self.STAGE_NAME_SIZE
        self.amount  = int.from_bytes(data[offset:offset + 4], "little")
        offset += 4


class ShineChecksPacket:
    checks : list[int]
    SIZE : short = 200

    def __init__(self, packet_bytes : bytearray = None, checks : list[int] = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.checks = checks

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        for i in range(100):
            if i < len(self.checks):
                data += self.checks[i].to_bytes(length=2, byteorder="little", signed=True)

            else:
                filler = 0
                data += filler.to_bytes(length=2, byteorder="little", signed=True)


        if len(data) != self.SIZE:
            raise f"ShineChecksPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        # Shouldn't be necessary

#endregion

#region Server Packets

class ChatMessagePacket:
    MESSAGE_SIZE : int = 0x4B
    messages : list[str]
    SIZE : short = 0x4B * 3

    def __init__(self, packet_bytes : bytearray = None, messages : list[str] = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.messages = messages

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        size : int = 0
        for index in range(len(self.messages)):
            for char in self.messages[index]:
                if size < self.MESSAGE_SIZE:
                    data += char.encode()
                else:
                    raise "Message too long exception"

            while len(data) < self.MESSAGE_SIZE * (index + 1):
                data += b"\x00"
        if len(data) != self.SIZE:
            raise f"ChatMessagePacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data


    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

        offset = 0
        self.messages.append(data[offset:offset + self.MESSAGE_SIZE].decode("utf8"))
        offset += self.MESSAGE_SIZE
        self.messages.append(data[offset:offset + self.MESSAGE_SIZE].decode("utf8"))
        offset += self.MESSAGE_SIZE
        self.messages.append(data[offset:offset + self.MESSAGE_SIZE].decode("utf8"))


class SlotDataPacket:
    cascade : ushort
    sand : ushort
    wooded : ushort
    lake : ushort
    lost : ushort
    metro : ushort
    seaside : ushort
    snow : ushort
    luncheon : ushort
    ruined : ushort
    bowser : ushort
    dark : ushort
    darker : ushort
    regionals : bool
    captures : bool
    SIZE : short = 28

    def __init__(self, packet_bytes : bytearray = None, cascade : int = None, sand : int = None, wooded : int = None, lake : int = None, lost : int = None, metro : int = None, seaside : int = None, snow : int = None, luncheon : int = None, ruined : int = None, bowser : int = None, dark : int = None, darker : int = None,  regionals : bool = None, captures : bool = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.cascade = short(cascade)
            self.sand = short(sand)
            self.wooded = short(wooded)
            self.lake = short(lake)
            self.lost = short(lost)
            self.metro = short(metro)
            self.seaside = short(seaside)
            self.snow = short(snow)
            self.luncheon = short(luncheon)
            self.ruined = short(ruined)
            self.bowser = short(bowser)
            self.dark = short(dark)
            self.darker = short(darker)
            self.regionals = regionals
            self.captures = captures

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        int_value : int = self.cascade.value
        data += int_value.to_bytes(2, "little")
        int_value = self.sand.value
        data += int_value.to_bytes(2, "little")
        int_value = self.wooded.value
        data += int_value.to_bytes(2, "little")
        int_value = self.lake.value
        data += int_value.to_bytes(2, "little")
        int_value = self.lost.value
        data += int_value.to_bytes(2, "little")
        int_value = self.metro.value
        data += int_value.to_bytes(2, "little")
        int_value = self.seaside.value
        data += int_value.to_bytes(2, "little")
        int_value = self.snow.value
        data += int_value.to_bytes(2, "little")
        int_value = self.luncheon.value
        data += int_value.to_bytes(2, "little")
        int_value = self.ruined.value
        data += int_value.to_bytes(2, "little")
        int_value = self.bowser.value
        data += int_value.to_bytes(2, "little")
        int_value = self.dark.value
        data += int_value.to_bytes(2, "little")
        int_value = self.darker.value
        data += int_value.to_bytes(2, "little")
        data += self.regionals.to_bytes(1, "little")
        data += self.captures.to_bytes(1, "little")
        if len(data) != self.SIZE:
            raise f"CountsPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset = 0
        self.cascade = ushort(int.from_bytes(data[offset:2], "little"))
        offset += 2
        self.sand = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.wooded = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.lake = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.lost = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.metro = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.seaside = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.snow = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.luncheon = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.ruined = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.bowser = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.dark = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.darker = ushort(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.regionals = bool.from_bytes(data[offset:offset + 1], "little")
        offset += 1
        self.captures = bool.from_bytes(data[offset:offset + 1], "little")





#endregion

class ChangeStagePacket:
    ID_SIZE : int  = 0x10
    STAGE_SIZE : int = 0x30
    stage : str
    stage_id : str
    scenario : sbyte
    sub_scenario_type : byte
    SIZE : short = 0x42

    def __init__(self, packet_bytes = None , stage : str = "", stage_id : str = "", scenario : int = -1, sub_scenario_type : int = 0):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.stage = stage
            self.stage_id = stage_id
            self.scenario = c_byte(int(scenario))
            self.sub_scenario_type = c_ubyte(sub_scenario_type)

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.stage.encode()
        while len(data) < self.STAGE_SIZE:
            data += b"\x00"
        data += self.stage_id.encode()
        while len(data) < self.STAGE_SIZE + self.ID_SIZE:
            data += b"\x00"
        int_value : int = self.scenario.value
        data += int_value.to_bytes(1, "little", signed=True)
        int_value2 : int = self.sub_scenario_type.value
        data += int_value2.to_bytes(1, "little", signed=False)
        if len(data) != self.SIZE:
            raise f"ChangeStagePacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.stage = data[offset:self.STAGE_SIZE].decode()
        offset += self.STAGE_SIZE
        self.stage_id = data[offset:offset + self.ID_SIZE].decode()
        offset += self.ID_SIZE
        self.scenario = sbyte(int.from_bytes(data[offset:offset + 1], "little"))
        offset += 1
        self.sub_scenario_type = byte(int.from_bytes(data[offset:offset + 1], "little"))

class ApInfoPacket:
    INFO_SIZE : int = 40
    info_type : int = -1
    index1 : int = -1
    index2 : int = -1
    index3 : int = -1
    info : list[str] = []

    SIZE : short = 128

    def __init__(self, info_type: int, index1 : int, index2 : int, index3 : int, info : list[str]):
        self.info_type = info_type
        self.index1 = index1
        self.index2 = index2
        self.index3 = index3
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.info_type.to_bytes(2,"little")
        data += self.index1.to_bytes(2,"little")
        data += self.index2.to_bytes(2,"little")
        data += self.index3.to_bytes(2,"little")
        # print(self.info_type)
        # print(self.index1)
        # print(self.index2)
        # print(self.index3)
        # print(self.info)

        for i in range(3):
            if i < len(self.info):
                if len(self.info[i]) > 40:
                    data += self.info[i][:40].encode()
                else:
                    data += self.info[i].encode()

            while len(data) < 8 + self.INFO_SIZE * (i + 1):
                data += b"\x00"

        if len(data) != self.SIZE:
            raise f"ApInfoPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.info_type = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.index1 = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.index2 = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.index3 = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.info.append(data[offset:offset + self.INFO_SIZE].decode("utf-16"))
        offset += self.INFO_SIZE
        self.info.append(data[offset:offset + self.INFO_SIZE].decode("utf-16"))
        offset += self.INFO_SIZE
        self.info.append(data[offset:offset + self.INFO_SIZE].decode("utf-16"))

class ShopReplace:
    info_type : int = 255
    info : list[list[int]] = []

    SIZE : short = 177

    def __init__(self, info_type: int, info : list[list[int]]):
        self.info_type = info_type
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.info_type.to_bytes(1,"little", signed=False)

        for i in range(44):
            if i < len(self.info):
                for value in self.info[i]:
                    data += value.to_bytes(1,"little", signed=False)

            else:
                filler = 255
                data += filler.to_bytes(1,"little", signed=False)
                data += filler.to_bytes(1,"little", signed=False)
                data += filler.to_bytes(1,"little", signed=False)
                data += filler.to_bytes(1,"little", signed=False)

        if len(data) != self.SIZE:
            raise f"ShopReplace failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.info_type = data[offset]
        offset += 1
        for i in range(11):
            self.info.append([data[offset], data[offset+1], data[offset+2], data[offset+3]])
            offset += 4

class ShineReplace:
    info : dict[str | list[int]] = []

    SIZE : short = 200

    def __init__(self, info : dict[str | list[int]]):
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()

        for i in range(100):
            if i < len(self.info):
                data += self.info[str(i)][0].to_bytes(1,"little", signed=True)
                data += self.info[str(i)][1].to_bytes(1,"little", signed=False)

            else:
                filler = 127
                data += filler.to_bytes(1,"little", signed=True)
                filler = 255
                data += filler.to_bytes(1,"little", signed=False)

        if len(data) != self.SIZE:
            raise f"ShineReplace failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        for i in range(100):
            self.info[str(i)] = [data[offset], data[offset+1]]
            offset += 2

class ShineColor:
    info : list[list[int]] = []

    SIZE : short = 51*3

    def __init__(self, info : list[list[int]]):
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()

        for i in range(51):
            if i < len(self.info):
                data += self.info[i][0].to_bytes(2,"little")
                data += self.info[i][1].to_bytes(1,"little", signed=True)

            else:
                filler = 0
                data += filler.to_bytes(2,"little")
                data += filler.to_bytes(1,"little", signed=True)

        if len(data) != self.SIZE:
            print(len(data))
            raise f"ShineColor failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.info = []
        print(int.from_bytes(data[offset:offset+2], "little"))
        print(int.from_bytes(data[offset:offset+2], "little", signed=True))
        for i in range(83):
            self.info.append([int.from_bytes(data[offset:offset+2],"little", signed=True), data[offset+3]])
            offset += 3

class ShineHint:
    hints : dict[str | list[int]] = []

    SIZE : short = 200

    def __init__(self, shine : int):
        self.shine = shine

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()

        for i in range(100):
            if i < len(self.hints):
                data += self.info[str(i)][0].to_bytes(1,"little", signed=True)
                data += self.info[str(i)][1].to_bytes(1,"little", signed=False)

            else:
                filler = 127
                data += filler.to_bytes(1,"little", signed=True)
                filler = 255
                data += filler.to_bytes(1,"little", signed=False)

        if len(data) != self.SIZE:
            raise f"ShineReplace failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        for i in range(100):
            self.hints[str(i)] = [data[offset], data[offset+1]]
            offset += 2


class DeathLinkPacket:
    SIZE : short = 0x0

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

#region Connection Packets

class ConnectPacket:
    SIZE : short = 4
    connection_type : ConnectionType

    def __init__(self, packet_bytes : bytearray = None , connection_type : ConnectionType = ConnectionType.Connect):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.connection_type = connection_type

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        value = self.connection_type.value
        data += value.to_bytes(4,"little")
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

        self.connection_type = ConnectionType(int.from_bytes(data[0:4],"little"))

class DisconnectPacket:
    # Empty Packet just to signal disconnect
    SIZE : short = 0

class InitPacket:
    max_players : ushort = ushort(4)
    SIZE : short = 2

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        as_integer : int = self.max_players.value
        data += as_integer.to_bytes(2, "little")
        if len(data) != self.SIZE:
            raise f"InitPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data


    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        self.max_players = ushort(int.from_bytes(data[0:self.SIZE], "little"))

#endregion

class PacketHeader:
    GUID_SIZE : int = 16
    guid : bytearray
    packet_type : PacketType
    packet_size : short
    SIZE : short = 16 + 4

    def __init__(self, header_bytes : bytearray = None, guid : bytearray = None,  packet_type : PacketType = PacketType.Init):
        if header_bytes:
            self.deserialize(header_bytes)
        else:
            self.guid = guid
            self.packet_type = packet_type

    def serialize(self) -> bytearray:
        data: bytearray = bytearray()
        data += self.guid

        while len(data) < self.GUID_SIZE:
            data += b"\x00"
        int_value: int = self.packet_type.value
        data += int_value.to_bytes(2, "little")
        int_value2 : int = self.packet_size
        data += int_value2.to_bytes(2, "little")
        if len(data) != self.SIZE:
            raise f"PacketHeader failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset = 0
        self.guid = data[offset:self.GUID_SIZE]
        offset += self.GUID_SIZE
        self.packet_type = PacketType(int.from_bytes(data[offset:offset + 2], "little"))
        offset += 2
        self.packet_size = short(int.from_bytes(data[offset:offset + 2], "little"))

class Packet:
    header : PacketHeader
    packet : Any
    max_size : int = 256 # max size without header

    def __init__(self, guid : bytearray, header_bytes : bytearray = None, packet_type : PacketType = PacketType.Connect, packet_data : list = None):
        if header_bytes:
            self.header = PacketHeader(header_bytes=header_bytes)
        else:
            self.header = PacketHeader(guid=guid, packet_type=packet_type)
            match packet_type:
                case PacketType.Connect:
                    self.packet = ConnectPacket()
                case PacketType.Init:
                    self.packet = InitPacket()
                case PacketType.ChangeStage:
                    self.packet = ChangeStagePacket(stage=packet_data[0], scenario=packet_data[1])
                case PacketType.SlotData:
                    self.packet = SlotDataPacket(cascade=packet_data[0], sand=packet_data[1], wooded=packet_data[2],
                        lake=packet_data[3], lost =packet_data[4], metro=packet_data[5], seaside=packet_data[6],
                        snow=packet_data[7], luncheon=packet_data[8], ruined=packet_data[9], bowser=packet_data[10],
                        dark=packet_data[11], darker=packet_data[12], regionals=packet_data[13], captures=packet_data[14])
                case PacketType.ArchipelagoChat:
                    self.packet = ChatMessagePacket(messages=packet_data[0])
                case PacketType.Check:
                    self.packet = CheckPacket(location_id=packet_data[0], item_type=packet_data[1], index=packet_data[2], obj_id=packet_data[3], stage=packet_data[4], amount=packet_data[5])
                case PacketType.DeathLink:
                    self.packet = DeathLinkPacket()
                case PacketType.ShineChecks:
                    self.packet = ShineChecksPacket(checks=packet_data[0])
                case PacketType.ApInfo:
                    self.packet = ApInfoPacket(info_type=packet_data[0], index1=packet_data[1], index2=packet_data[2], index3=packet_data[3], info=packet_data[4])
                case PacketType.ShopReplace:
                    self.packet = ShopReplace(info_type=packet_data[0], info=packet_data[1])
                case PacketType.ShineReplace:
                    self.packet = ShineReplace(info=packet_data[0])
                case PacketType.ShineColor:
                    self.packet = ShineColor(info=packet_data[0])
                case PacketType.ShineHint:
                    self.packet = ShineHint(shine=packet_data[0])

    def serialize(self) -> bytearray:
        self.header.packet_size = self.packet.SIZE
        data : bytearray = bytearray()
        data += self.header.serialize()
        data += self.packet.serialize()
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        match self.header.packet_type:
            case PacketType.Connect:
                self.packet = ConnectPacket()
            # case PacketType.Command:
            #     self.packet = CommandP()
            case PacketType.Check:
                self.packet = CheckPacket(packet_bytes=data)
            case PacketType.ArchipelagoChat:
                self.packet = ChatMessagePacket()
            case PacketType.SlotData:
                self.packet = SlotDataPacket(packet_bytes=data)
            case PacketType.DeathLink:
                self.packet = DeathLinkPacket()
            case PacketType.ShineChecks:
                self.packet = ShineChecksPacket(packet_bytes=data)
            case PacketType.ChangeStage:
                self.packet = ChangeStagePacket(packet_bytes=data)
