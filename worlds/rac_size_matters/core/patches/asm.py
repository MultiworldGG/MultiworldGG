"""Shared low-level MIPS/patch-record primitives -- word packing, jump/branch encoding, and the Patch record every patches/*.py plan builder produces."""

import struct
from dataclasses import dataclass


def packed(*words: int) -> bytes:
    return struct.pack(f"<{len(words)}I", *words)


def jump(address: int) -> int:
    return 0x0C000000 | (address >> 2)


def j(address: int) -> int:
    """Plain (non-linking) MIPS J -- jump() above always emits JAL."""
    return 0x08000000 | (address >> 2)


def branch(source: int, target: int) -> int:
    displacement = (target - source - 4) // 4
    if source % 4 or target % 4 or not -32768 <= displacement <= 32767:
        raise ValueError("Invalid native branch")
    return 0x10000000 | (displacement & 0xFFFF)


@dataclass(frozen=True)
class Patch:
    address: int
    original: bytes
    replacement: bytes
    enabled: bool = True


ZERO, AT, V0, V1, A0, A1, A2, A3 = range(8)
T0, T1, T2, T3, T4, T5, T6, T7 = range(8, 16)
S0, S1, S2, S3, S4, S5, S6, S7 = range(16, 24)
T8, T9, K0, K1, GP, SP, FP, RA = range(24, 32)

# Coprocessor 1 (FPU) registers -- PS2's EE core has single-precision float
# hardware only (no SDC1/LDC1 double support), so only swc1/lwc1 exist here.
F0, F1, F2, F3, F4, F5, F6, F7 = range(8)
F8, F9, F10, F11, F12, F13, F14, F15 = range(8, 16)
F16, F17, F18, F19, F20, F21, F22, F23 = range(16, 24)
F24, F25, F26, F27, F28, F29, F30, F31 = range(24, 32)

NOP = 0

_OP_ORI = 0x0D
_OP_ADDIU = 0x09
_OP_SLTIU = 0x0B
_OP_LBU = 0x24
_OP_LW = 0x23
_OP_SB = 0x28
_OP_SW = 0x2B
_OP_LD = 0x37  # MIPS-III 64-bit load -- the EE core's GPRs are 64-bit
_OP_SD = 0x3F  # MIPS-III 64-bit store, same reason
_OP_LWC1 = 0x31
_OP_SWC1 = 0x39
_OP_BEQ = 0x04
_OP_BNE = 0x05
_OP_LUI = 0x0F
_OP_ANDI = 0x0C
_OP_XORI = 0x0E
_FUNCT_ADDU = 0x21
_FUNCT_SUBU = 0x23
_FUNCT_OR = 0x25
_FUNCT_AND = 0x24
_FUNCT_JR = 0x08
_FUNCT_JALR = 0x09
_FUNCT_SLL = 0x00
_FUNCT_SRL = 0x02
_FUNCT_SLTU = 0x2B
_FUNCT_DADDU = 0x2D  # MIPS-III 64-bit ADDU; with rt=ZERO this is the EE
# toolchain's 64-bit register-move idiom (see dmove()).


def _itype(opcode, rs, rt, imm):
    return (opcode << 26) | (rs << 21) | (rt << 16) | (imm & 0xFFFF)


def _rtype(rs, rt, rd, funct, shamt=0):
    return (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct


def lui(rt, imm16):
    return _itype(_OP_LUI, 0, rt, imm16)


def ori(rt, rs, imm16):
    return _itype(_OP_ORI, rs, rt, imm16)


def li32(rt, value):
    """lui+ori pair loading a full 32-bit constant into rt."""
    return [lui(rt, value >> 16), ori(rt, rt, value & 0xFFFF)]


def addiu(rt, rs, imm16):
    return _itype(_OP_ADDIU, rs, rt, imm16)


def addu(rd, rs, rt):
    return _rtype(rs, rt, rd, _FUNCT_ADDU)


def sltiu(rt, rs, imm16):
    return _itype(_OP_SLTIU, rs, rt, imm16)


def lbu(rt, offset, base):
    return _itype(_OP_LBU, base, rt, offset)


def sb(rt, offset, base):
    return _itype(_OP_SB, base, rt, offset)


def sw(rt, offset, base):
    return _itype(_OP_SW, base, rt, offset)


def beq(rs, rt, offset):
    return _itype(_OP_BEQ, rs, rt, offset)


def bne(rs, rt, offset):
    return _itype(_OP_BNE, rs, rt, offset)


def jr(rs):
    return _rtype(rs, 0, 0, _FUNCT_JR)


def jalr(rs, rd=RA):
    return _rtype(rs, 0, rd, _FUNCT_JALR)


def lw(rt, offset, base):
    return _itype(_OP_LW, base, rt, offset)


def sub_(rd, rs, rt):
    return _rtype(rs, rt, rd, _FUNCT_SUBU)


def or_(rd, rs, rt):
    return _rtype(rs, rt, rd, _FUNCT_OR)


def and_(rd, rs, rt):
    return _rtype(rs, rt, rd, _FUNCT_AND)


def sll(rd, rt, shamt):
    return _rtype(0, rt, rd, _FUNCT_SLL, shamt)


def srl(rd, rt, shamt):
    return _rtype(0, rt, rd, _FUNCT_SRL, shamt)


def andi(rt, rs, imm16):
    return _itype(_OP_ANDI, rs, rt, imm16)


def xori(rt, rs, imm16):
    return _itype(_OP_XORI, rs, rt, imm16)


def move(rd, rs):
    """Pseudo-op: OR rd, rs, ZERO."""
    return or_(rd, rs, ZERO)


def sltu(rd, rs, rt):
    return _rtype(rs, rt, rd, _FUNCT_SLTU)


def ld(rt, offset, base):
    """MIPS-III 64-bit load -- the EE core's GPRs are 64-bit."""
    return _itype(_OP_LD, base, rt, offset)


def sd(rt, offset, base):
    """MIPS-III 64-bit store, same reason."""
    return _itype(_OP_SD, base, rt, offset)


def lwc1(ft, offset, base):
    return _itype(_OP_LWC1, base, ft, offset)


def swc1(ft, offset, base):
    return _itype(_OP_SWC1, base, ft, offset)


def daddu(rd, rs, rt):
    return _rtype(rs, rt, rd, _FUNCT_DADDU)


def dmove(rd, rs):
    """Pseudo-op: DADDU rd, rs, ZERO -- the EE toolchain's 64-bit register move, seen instead of plain move()/OR in some compiled functions."""
    return daddu(rd, rs, ZERO)
