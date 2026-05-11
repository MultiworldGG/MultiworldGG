### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")

def count_in_list(e: T, ls: Iterable[T]):
    count = 0
    for el in ls:
        if el == e:
            count += 1
    return count

def format_list(
        ls: Iterable[T],
        ls_start: str = "[",
        ls_end: str = "]",
        sep: str = ",",
        enc_start: str = "",
        enc_end: str = ""
    ) -> str:
    res = ls_start
    first = True
    if ls:
        for item in ls:
            if not first:
                res += sep
            else:
                first = False
            res += f"{enc_start}{item!s}{enc_end}"
    res += ls_end
    return res

def scrub_list(a: list[T], b: Iterable[T], debug: bool = False) -> list[T]:
    newlist: list[T] = []
    for item in a:
        if item in b:
            newlist.append(item)
        elif debug:
            print(f"Excluding: {item}")
    return newlist
