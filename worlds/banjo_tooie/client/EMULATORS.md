# Adding & debugging emulators in `emu_loader.py`

This doc is for maintainers who want to add support for a new N64 emulator,
or diagnose why an existing one stopped attaching.

---

## How the loader actually works

Every emulator we support is a single `EmulatorInfo(...)` entry in the
`EMULATOR_CONFIGS` dict. At startup, `BTEmuLoaderClient.connect()` walks
that dict in `Emulators` enum order and calls `attach()` on each entry
until one succeeds.

`attach()` runs in three phases:

1. **Process detection.** Walks `get_running_processes()` looking for any
   process whose name starts with `process_name`. If none match, it'll fail
   with `"Process '<name>' not running"`.
2. **RDRAM base discovery.** One of two strategies, chosen by the entry's
   flags (see below).
3. **Signature validation.** Reads a u32 at the candidate base + the
   BTHACK anchor offset (`0x00400000`), checks it's a valid `0x80xxxxxx`
   RDRAM pointer, then follows the pointer and confirms the version
   field's major is non-zero. If yes, it'll attach.

Once attached, all `read_u8/16/32` and `write_u8/16/32` calls compute the
host-process address by:
- Stripping the KSEG0 mask (`addr & 0x7FFFFFFF`).
- Rotating u8 / u16 addresses to account for Mupen64Plus-family
  byte-swap-within-word storage on LE hosts (`u8_addr` / `u16_addr`).
- Adding `connected_offset` (the RDRAM base in process memory).

The same logic works for *any* host-side N64 RDRAM as long as we
correctly find its base.

---

## `EmulatorInfo` Entries

```python
EmulatorInfo(
    emu_id,                       # Emulators.* enum value
    readable_name,                # human label
    process_name,                 # case-insensitive prefix match
    find_dll,                     # bool: use module-offset option
    dll_name,                     # Windows DLL name (None if find_dll=False)
    additional_lookup,            # bool: deref a pointer at dll_base+off?
    lower_offset_range,           # offset-scan start (relative to dll_base)
    upper_offset_range,           # offset-scan end
    range_step=16,                # offset-scan step
    extra_offset=0,               # added to RDRAM base after deref
    linux_dll_name=None,          # Linux .so name (find_dll=True only)
    scan_memory_for_signature=False,  # bool: use heap-scan option
    signature_alignment=0x10000,  # heap-scan stride
)
```

The fields fall into two clusters depending on which option you pick:

### Option A: module + offset range (`find_dll=True`, `scan_memory_for_signature=False`)

Used when the emulator stores RDRAM at a stable offset relative to
a known module. The loader resolves `dll_base` from `list_modules()` then
walks `dll_base + lower_offset_range … dll_base + upper_offset_range` in
`range_step` increments, validating each candidate.

If `additional_lookup=True`, each `dll_base + off` is treated as a
pointer to RDRAM rather than RDRAM itself — the loader reads a u64
there, adds `extra_offset`, and uses that as the candidate.

Example: RMG uses pointer indirection because mupen64plus.dll stores a
pointer-to-RDRAM at a stable struct offset, not RDRAM directly:

```python
Emulators.RMG: EmulatorInfo(
    Emulators.RMG, "Rosalie's Mupen GUI", "rmg",
    find_dll=True, dll_name="mupen64plus.dll", additional_lookup=True,
    lower_offset_range=0x29C15D8, upper_offset_range=0x2FC15D8,
    extra_offset=0x80000000, linux_dll_name="libmupen64plus.so",
),
```

### Option B: heap signature scan (`scan_memory_for_signature=True`)

Slow but version-agnostic. The loader walks every writable heap region
of the process (`list_writable_regions(min_size=0x800000)`), stepping by
`signature_alignment`, and validates each candidate by the same
signature check.

Use this when the emulator either:
- Doesn't expose a stable module base (Gopher64, ares — both standalone
  binaries with no helpful DLL).
- *Did* expose one but it shifts between releases.

Example:

```python
Emulators.BizHawk: EmulatorInfo(
    Emulators.BizHawk, "BizHawk", "emuhawk",
    find_dll=False, dll_name=None, additional_lookup=False,
    lower_offset_range=0, upper_offset_range=0,
    scan_memory_for_signature=True, signature_alignment=0x10000,
),
```

## Debugging: emulator-X won't attach

### 1. Reproduce with the standalone path

```
python3 worlds/banjo_tooie/client/emu_loader.py
```

This file no longer has a `main()`; instead just instrument a quick
shell:

```python
from worlds.banjo_tooie.client.emu_loader import (
    EMULATOR_CONFIGS, Emulators, BTEmuLoaderClient,
)
info = EMULATOR_CONFIGS[Emulators.<YourEmu>]
ok = info.attach()
print("attached:", ok, "error:", info.connection_error,
      "rdram_base:", hex(info.connected_offset) if info.connected_offset else None)
```

The `connection_error` string tells you which phase failed:

| Error substring | Meaning |
|---|---|
| `Process '<name>' not running` | `process_name` prefix doesn't match. Run `ps aux \| grep <name>` (Linux) or Task Manager and confirm. |
| `Module <names> not loaded` | `find_dll=True` but no module in `list_modules()` matched any `dll_name`/`linux_dll_name`. The DLL might be renamed in the new release. |
| `Could not read any data` | The loader did `read_longlong(dll_base + off)` repeatedly and got 0 for every offset. The module probably has the wrong base, or the offset range targets unmapped pages. |
| `BT signature not found` | The loader read data but never saw the BTHACK signature. Either the RDRAM base is outside the scanned range, or the patched ROM isn't loaded. |
| `attach failed: ...` | `ProcessMemory(...)` constructor raised. On Linux this is usually a ptrace permission issue — see [the ptrace_scope helper](emu_loader.py). |


### 2. Find the module-relative offset (for option A)

```python
from worlds.banjo_tooie.client.emu_loader import ProcessMemory, validate_bt_signature
pm = ProcessMemory("<process_name>")
# find the DLL base
for mod in pm.list_modules():
    if "mupen64plus" in mod.name.lower():
        print(mod.name, hex(mod.lpBaseOfDll))
# discover RDRAM base via heap scan, then subtract
```

The delta between `RDRAM_base - dll_base` gives you the offset to plug
into `lower_offset_range` (with some slack on either side).

---

## Adding a new emulator

### Step 1 — pick an option

Run the emulator with the BT-AP patched ROM:

```python
from worlds.banjo_tooie.client.emu_loader import (
    ProcessMemory, validate_bt_signature,
)
pm = ProcessMemory("<your_process_name>")
print("modules:", [m.name for m in pm.list_modules()
                   if "mupen" in m.name.lower() or "n64" in m.name.lower()])
# scan all heap regions for the signature:
for start, size in pm.list_writable_regions(min_size=0):
    if size < 0x400004: continue
    for base in range(0, size - 0x400004 + 1, 0x1000):
        if validate_bt_signature(pm, start + base):
            print(f"hit: process_offset=0x{start+base:x} region=(0x{start:x}+{size})")
```

- If a mupen-family module shows up *and* the hit address has a stable
  delta from that module base across runs -> **option A**.
- If no useful module name, or the delta wanders between runs -> **option B**.

### Step 2 — add the enum + config entry

In `Emulators`:

```python
class Emulators(IntEnum):
    Project64_v4 = auto()
    ...
    Ares = auto()
    YourEmu = auto()   # ← add at the end
```

In `EMULATOR_CONFIGS`:

```python
Emulators.YourEmu: EmulatorInfo(
    Emulators.YourEmu, "Your Emu (display name)", "your_process_prefix",
    find_dll=False, dll_name=None, additional_lookup=False,
    lower_offset_range=0, upper_offset_range=0,
    scan_memory_for_signature=True, signature_alignment=0x10000,
),
```

(Adjust the field cluster per your chosen option — see "Anatomy" above.)

The position in `Emulators` is the priority order
`connect_to_any_emulator()` will try them in. Heap-scan strategies are
slower; put them after offset-option entries that share a process name
to avoid wasting time scanning when a direct lookup will do.

### Step 3 — verify

1. Launch the emulator with the patched ROM.
2. Start the BT client.
3. Check the BT-client log for `Connected to Your Emu`.
4. Confirm `/writesettings` reports a real seed and the file-select
   screen flips to `BTCLIENT READY`.
5. Collect a known location, confirm the AP server receives the
   `LocationChecks`

If any of those fail, the loader attached to the wrong RDRAM region —
re-check the signature math in step 1.
