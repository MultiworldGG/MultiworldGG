from collections.abc import MutableMapping
from dataclasses import dataclass


@dataclass(slots=True, eq=False)
class ModSlots(MutableMapping):
    mod_slot_one: bool = False
    mod_slot_two: bool = False
    mod_slot_three: bool = False

    def __getitem__(self, key):
        if key not in self.__slots__:
            raise KeyError(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key not in self.__slots__:
            raise KeyError(key)
        setattr(self, key, value)

    def __delitem__(self, key):
        self[key] = False

    def __iter__(self):
        return iter(self.__slots__)

    def __len__(self):
        return 3


@dataclass(slots=True)
class InventoryEntry:
    """Observed, granted, and transient state for one weapon or gadget."""

    name: str
    gadget: bool = False
    address: object | None = None
    owned: bool | None = None
    ap_owned: bool | None = None
    raw_owned: bool | None = None
    mods: ModSlots | None = None
    raw_mods: ModSlots | None = None
    raw_level: int | None = None
    previous_experience: int | None = None
    pinned_experience: int | None = None
    level_cap: int | None = None
    titan_purchased: bool | None = None


class EntryView(MutableMapping):
    """Compatibility access to a field stored on inventory entries."""

    def __init__(self, entries, field, gadget=False):
        self.entries, self.field, self.gadget = entries, field, gadget

    def __getitem__(self, name):
        entry = self.entries[name]
        value = getattr(entry, self.field)
        if entry.gadget != self.gadget or value is None:
            raise KeyError(name)
        return value

    def __setitem__(self, name, value):
        entry = self.entries.setdefault(name, InventoryEntry(name, self.gadget))
        if self.field in ("mods", "raw_mods") and not isinstance(value, ModSlots):
            value = ModSlots(**value)
        setattr(entry, self.field, value)

    def __delitem__(self, name):
        self[name]
        setattr(self.entries[name], self.field, None)

    def __iter__(self):
        return (
            name
            for name, entry in self.entries.items()
            if entry.gadget == self.gadget and getattr(entry, self.field) is not None
        )

    def __len__(self):
        return sum(1 for _ in self)

    def setdefault(self, name, default=None):
        if name not in self:
            self[name] = default
        return self[name]


class InventoryField:
    def __init__(self, field, gadget=False):
        self.field, self.gadget = field, gadget

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, "entries"):
            instance.entries = {}
        return EntryView(instance.entries, self.field, self.gadget)

    def __set__(self, instance, values):
        values = tuple(values.items())
        view = self.__get__(instance, type(instance))
        view.clear()
        view.update(values)
