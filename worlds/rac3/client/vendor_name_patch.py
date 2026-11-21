"""Saved pointers for a randomized vendor name."""

from dataclasses import dataclass


@dataclass
class VendorNamePatch:
    address: int
    original: int
    replacement: int
