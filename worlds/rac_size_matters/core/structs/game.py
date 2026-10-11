from __future__ import annotations

import ctypes

from ..address_maps import Address
from .base import MemoryStruct


class PlanetProgressStruct(MemoryStruct):

    BASE_ADDRESS = Address("PLANET_PROGRESS_BASE")
    _pack_ = 1
    _fields_ = [
        ("pokitaru",      ctypes.c_uint8),
        ("ryllus",        ctypes.c_uint8),
        ("kalidon",       ctypes.c_uint8),
        ("metalis",       ctypes.c_uint8),
        ("dreamtime",     ctypes.c_uint8),
        ("outpost_omega", ctypes.c_uint8),
        ("challax",       ctypes.c_uint8),
        ("dayni_moon",    ctypes.c_uint8),
        ("inside_clank",  ctypes.c_uint8),
        ("quodrona",      ctypes.c_uint8),
    ]

    PLANET_ORDER: tuple[str, ...] = (
        "pokitaru", "ryllus", "kalidon", "metalis", "dreamtime",
        "outpost_omega", "challax", "dayni_moon", "inside_clank", "quodrona",
    )
    PLANET_NAME_ORDER: tuple[str, ...] = tuple(n.upper() for n in PLANET_ORDER)


class QuickSelectStruct(MemoryStruct):
    BASE_ADDRESS = Address("QUICK_SELECT_BASE")
    _pack_ = 1
    _fields_ = [
        ("right",         ctypes.c_uint32),
        ("top_right",     ctypes.c_uint32),
        ("top_middle",    ctypes.c_uint32),
        ("top_left",      ctypes.c_uint32),
        ("left",          ctypes.c_uint32),
        ("bottom_left",   ctypes.c_uint32),
        ("bottom_middle", ctypes.c_uint32),
        ("bottom_right",  ctypes.c_uint32),
    ]

    SLOT_ORDER: tuple[str, ...] = (
        "right", "top_right", "top_middle", "top_left",
        "left", "bottom_left", "bottom_middle", "bottom_right",
    )


class SkinStruct(MemoryStruct):
    BASE_ADDRESS = Address("SKIN_BASE")
    _pack_ = 1
    _fields_ = [
        ("unlocked", ctypes.c_uint8),
        ("equipped", ctypes.c_uint8),
    ]


class ChallengeModeStruct(MemoryStruct):
    BASE_ADDRESS = Address("CHALLENGE_MODE_BASE")
    _pack_ = 1
    _fields_ = [("tier", ctypes.c_uint8)]


class VendorVisibilityStruct(MemoryStruct):

    BASE_ADDRESS = 0
    _pack_ = 1
    _fields_ = [("visibility", ctypes.c_int16)]

TRANSITION_GATE_IDLE:    int = 0x000000FF
TRANSITION_GATE_ARRIVED: int = 0x00000100


class TransitionGateStruct(MemoryStruct):
    BASE_ADDRESS = Address("TRANSITION_GATE_ADDRESS")
    _pack_ = 1
    _fields_ = [("value", ctypes.c_uint32)]


class LoadingPlanetStruct(MemoryStruct):
    BASE_ADDRESS = Address("LOADING_PLANET_ADDRESS")
    _pack_ = 1
    _fields_ = [("value", ctypes.c_uint32)]
