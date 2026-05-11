### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable

from . import itemnames, locationnames, regionnames

_ITEM_NAME_MAP = {iname: getattr(itemnames, iname) for iname in dir(itemnames)}
_LOC_NAME_MAP = {lname: getattr(locationnames, lname) for lname in dir(locationnames)}
_REGION_NAME_MAP = {rname: getattr(regionnames, rname) for rname in dir(regionnames)}

def item_name_exists(key: str) -> bool:
    return key in _ITEM_NAME_MAP

def location_name_exists(key: str) -> bool:
    return key in _LOC_NAME_MAP

def region_name_exists(key: str) -> bool:
    return key in _REGION_NAME_MAP

def get_item_fields() -> Iterable[str]:
    return _ITEM_NAME_MAP.keys()

def get_location_fields() -> Iterable[str]:
    return _LOC_NAME_MAP.keys()

def get_region_fields() -> Iterable[str]:
    return _REGION_NAME_MAP.keys()

def get_item_name(key: str) -> str:
    return _ITEM_NAME_MAP[key]

def get_location_name(key: str) -> str:
    return _LOC_NAME_MAP[key]

def get_region_name(key: str) -> str:
    return _REGION_NAME_MAP[key]
