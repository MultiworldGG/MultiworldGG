"""Reversible vendor cosmetics; native row identities and prices stay intact."""
import struct
from importlib.resources import files

from .patches.asm import packed
from .patches.plan import supported_game_id

_ICON_ROOT = files(__package__.rsplit(".", 1)[0]).joinpath("images", "icons")
ICON_STYLES = ("original", "purple", "blue", "grey")
_icon_style = "original"
_icon_cache: dict[str, tuple[bytes, bytes]] = {}


def _load_icon(style):
    cached = _icon_cache.get(style)
    if cached is None:
        folder = _ICON_ROOT.joinpath(style)
        indices = folder.joinpath("archipelago-icon.indices").read_bytes()
        clut = folder.joinpath("archipelago-icon.clut").read_bytes()
        if len(indices) != 1024 or len(clut) != 1024:
            raise RuntimeError(f"AP icon style {style!r} requires 32x32 indices and 256 RGBA palette entries")
        _icon_cache[style] = cached = (indices, clut)
    return cached


def get_icon_style() -> str:
    return _icon_style


def set_icon_style(style: str) -> None:
    global _icon_style
    style = next((s for s in ICON_STYLES if s.lower() == style.lower()), None) or style
    if style not in ICON_STYLES:
        raise ValueError(f"Unknown icon style {style!r}; choices: {', '.join(ICON_STYLES)}")
    _load_icon(style)
    _icon_style = style

RENDER_SIGNATURE = packed(0x27BDFC80, 0x3C04FFFF, 0xFFB00320, 0x3484FFFF, 0xFFB10328)
# The Titan title path formats the level-four name with a native Titan prefix.
# Scouted offers must instead draw the localized title replaced by _text.
TITAN_TITLE_BRANCH_OFFSET = 0x784
TITAN_TITLE_BRANCH = packed(0x10400020)  # beq v0, zero, ordinary_title
SCOUTED_TITLE_BRANCH = packed(0x10000020)  # beq zero, zero, ordinary_title


def prepare(pine, code_start, code):
    hits = [i for i in range(0, len(code) - len(RENDER_SIGNATURE), 4)
            if code[i:i + len(RENDER_SIGNATURE)] == RENDER_SIGNATURE]
    if len(hits) != 1:
        raise RuntimeError("Vendor renderer signature changed")
    render = code_start + hits[0]
    def word(address):
        offset = address - code_start
        if not 0 <= offset <= len(code) - 4:
            raise RuntimeError("Vendor presentation code outside module")
        return struct.unpack_from("<I", code, offset)[0]
    def target(address):
        w = word(address)
        if w >> 26 != 3:
            raise RuntimeError("Vendor presentation call changed")
        return (w & 0x3FFFFFF) << 2
    def pair(upper, lower, hi, lo):
        a, b = word(upper), word(lower)
        if a & 0xFFFF0000 != hi or b & 0xFFFF0000 != lo:
            raise RuntimeError("Vendor presentation address signature changed")
        return ((a & 65535) << 16) + struct.unpack("<h", packed(b)[:2])[0]
    header = pair(render + 0x14, render + 0x5C, 0x3C100000, 0x26040000)
    strings = target(render + 0x27C)
    string_state = pair(strings + 0x1C, strings + 0x20, 0x3C030000, 0x24700000)
    spec = target(render + 0x6B8)
    equipment = pair(spec + 0x28, spec + 0x2C, 0x3C040000, 0x24840000)
    draw_list = target(render + 0x35C)
    draw_icon = target(draw_list + 0xC8)
    icons = pair(draw_icon + 4, draw_icon + 16, 0x3C020000, 0x24420000)
    area = target(draw_icon + 24)
    rect = target(area + 28)
    dimensions = target(rect + 72)
    textures = pair(dimensions + 4, dimensions + 16, 0x3C020000, 0x24420000)
    return VendorPresentation(pine, render, header, string_state, equipment, icons, textures)


class VendorPresentation:
    def __init__(self, pine, render, header, string_state, equipment, icons, textures):
        self.pine = pine
        self.game_id = supported_game_id(pine)
        self.render, self.header, self.string_state = render, header, string_state
        self.equipment, self.icons, self.textures = equipment, icons, textures
        self.text_changes = []
        self.icon_changes = []
        self.row_changes = {}
        self.selected_key = None
        self.string_entries = None
        self.icon_id = None

    def validate(self):
        if (self.pine.get_game_id() != self.game_id
                or self.pine.read_bytes(self.render, len(RENDER_SIGNATURE)) != RENDER_SIGNATURE):
            raise RuntimeError("Vendor presentation module changed")

    @staticmethod
    def _pointer(address, size=4):
        if not 0x100000 <= address <= 0x2000000 - size:
            raise RuntimeError("Invalid vendor presentation pointer")
        return address

    def _rows(self):
        pointer, count, columns, selected = struct.unpack("<4I", self.pine.read_bytes(self.header, 16))
        if count == 0:
            return []
        if not 0 < count <= 64 or selected >= count or pointer % 4:
            raise RuntimeError("Invalid native vendor rows")
        self._pointer(pointer, count * 28)
        raw = self.pine.read_bytes(pointer, count * 28)
        return [(pointer + i * 28, struct.unpack_from("<7I", raw, i * 28), i == selected)
                for i in range(count)]

    def _strings(self):
        p = self.pine
        state = p.read_bytes(self.string_state, 24)
        pointer, count = struct.unpack_from("<I", state)[0], struct.unpack_from("<I", state, 16)[0]
        if not state[8] or not 0 < count < 20000 or state[20] not in (0, 1) or state[21] not in (0, 1):
            raise RuntimeError("Invalid localization table")
        stride = 8 + state[20] * 4 + state[21] * 4
        start = self._pointer(pointer + state[20] * 4, count * stride)
        raw = p.read_bytes(start, count * stride)
        self.string_entries = {struct.unpack_from("<I", raw, i * stride)[0]: start + i * stride + 4
                               for i in range(count)}

    def _change(self, changes, address, replacement):
        original = self.pine.read_bytes(address, len(replacement))
        if original != replacement:
            try:
                self.pine.write_bytes(address, replacement)
                if self.pine.read_bytes(address, len(replacement)) != replacement:
                    raise RuntimeError("Vendor cosmetic write failed verification")
            except Exception:
                self.pine.write_bytes(address, original)
                raise
            changes.append((address, original, bytes(replacement)))

    def _restore(self, changes):
        for address, original, replacement in reversed(changes):
            if self.pine.read_bytes(address, len(replacement)) != replacement:
                raise RuntimeError("Vendor cosmetic memory changed; refusing stale restore")
            self.pine.write_bytes(address, original)
        changes.clear()

    def _text(self, row, reward):
        if self.string_entries is None:
            self._strings()
        native_id = row[5]
        if not 2 <= native_id < 25:
            return
        data = self.equipment + native_id * 0x58
        level = self.pine.read_int32(data + 0x3C)
        if level > 9:
            raise RuntimeError("Invalid vendor weapon level")
        spec = self._pointer(self.pine.read_int32(data + 0x10 + level * 4), 24)
        title_id, desc_id = struct.unpack("<2I", self.pine.read_bytes(spec + 16, 8))
        title_entry, desc_entry = self.string_entries.get(title_id), self.string_entries.get(desc_id)
        if title_entry is None or desc_entry is None or title_entry == desc_entry:
            return
        desc = self._pointer(self.pine.read_int32(desc_entry), 2048)
        original = self.pine.read_bytes(desc, 2048)
        end = original.find(b"\0")
        if end < 24:
            return
        capacity = end + 1
        clean = lambda text: "".join(c if 32 <= ord(c) < 127 else "?" for c in text).encode("ascii")
        title = clean(reward.item_name)
        recipient = b"For " + clean(reward.recipient_name)
        title_limit = min(96, capacity - min(len(recipient) + 1, 48) - 5)
        title = title[:max(1, title_limit)]
        title = bytes((0x90, reward.title_color)) + title + b"\x90\x01\0"
        recipient = recipient[:capacity - len(title) - 1] + b"\0"
        payload = (title + recipient).ljust(capacity, b"\0")
        if row[6] == 2:
            branch = self.render + TITAN_TITLE_BRANCH_OFFSET
            if self.pine.read_bytes(branch, 4) != TITAN_TITLE_BRANCH:
                raise RuntimeError("Vendor Titan title branch changed")
            self._change(self.text_changes, branch, SCOUTED_TITLE_BRANCH)
        self._change(self.text_changes, desc, payload)
        self._change(self.text_changes, title_entry, packed(desc))
        self._change(self.text_changes, desc_entry, packed(desc + len(title)))

    def _icon(self, rows):
        used = {row[1] for _, row, _ in rows} | {row[2] for _, row, _ in rows}
        p = self.pine
        for icon in range(1, 100):
            if icon in used:
                continue
            resource = p.read_int32(self.icons + icon * 4)
            if resource >= 2048:
                continue
            entry = self.textures + resource * 100
            image, palette = struct.unpack("<2I", p.read_bytes(entry + 12, 8))
            if not (0x100000 <= image < 0x1FFFFC0 and 0x100000 <= palette < 0x1FFFFC0):
                continue
            ih, ph = p.read_bytes(image, 64), p.read_bytes(palette, 64)
            if (struct.unpack_from("<3H", ih, 4) != (5, 0, 32)
                    or struct.unpack_from("<H", ih, 10)[0] != 32
                    or struct.unpack_from("<H", ph, 8)[0] != 256):
                continue
            pixels = self._pointer(struct.unpack_from("<I", ih, 48)[0], 1024)
            colors = self._pointer(struct.unpack_from("<I", ph, 48)[0], 1024)
            indices, clut = _load_icon(_icon_style)
            self._change(self.icon_changes, pixels, indices)
            self._change(self.icon_changes, colors, clut)
            self.icon_id = icon
            return
        raise RuntimeError("No compatible unused vendor icon texture")

    def tick(self, active, scouts):
        self.validate()
        if not active or scouts is None:
            self.close()
            return
        rows = self._rows()
        rewards = [(address, row, selected, scouts.for_purchase(row[6], row[5]))
                   for address, row, selected in rows]
        selected = next(((address, row, reward) for address, row, flag, reward in rewards if flag), None)
        key = (selected[0], selected[1][5:], selected[2]) if selected else None
        if key != self.selected_key:
            self._restore(self.text_changes)
            self.selected_key = None
            if selected and selected[2] is not None:
                self._text(selected[1], selected[2])
            self.selected_key = key
        if self.icon_id is None and any(reward is not None for _, _, _, reward in rewards):
            self._icon(rows)
        for address, row, _, reward in rewards:
            if reward is None or self.icon_id is None:
                continue
            identity = row[3:]
            previous = self.row_changes.get(address)
            if previous is None or previous[0] != identity:
                self.row_changes[address] = (identity, row[1])
            if row[1] != self.icon_id:
                p = self.pine
                if p.read_bytes(address + 12, 16) == packed(*identity):
                    p.write_int32(address + 4, self.icon_id)

    def close(self):
        self.validate()
        self._restore(self.text_changes)
        for address, (identity, icon) in self.row_changes.items():
            if (self.pine.read_bytes(address + 12, 16) == packed(*identity)
                    and self.pine.read_int32(address + 4) == self.icon_id):
                self.pine.write_int32(address + 4, icon)
        self.row_changes.clear()
        self._restore(self.icon_changes)
        self.selected_key = self.icon_id = None
