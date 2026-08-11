import os as _os
import sys as _sys

if _sys.platform == "win32" and hasattr(_os, "add_dll_directory"):
    _os.add_dll_directory(_os.path.dirname(__file__))

from ._dolphin_memory_engine import (
    MemWatch,
    assert_hooked,
    follow_pointers,
    get_status,
    hook,
    is_hooked,
    read_byte,
    read_bytes,
    read_double,
    read_float,
    read_word,
    un_hook,
    write_byte,
    write_bytes,
    write_double,
    write_float,
    write_word,
)

__all__ = [
    "MemWatch",
    "assert_hooked",
    "follow_pointers",
    "hook",
    "un_hook",
    "is_hooked",
    "get_status",
    "read_byte",
    "read_bytes",
    "read_double",
    "read_float",
    "read_word",
    "write_byte",
    "write_bytes",
    "write_double",
    "write_float",
    "write_word",
]