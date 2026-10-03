import logging
import time
from typing import TYPE_CHECKING, Any, Dict, Optional

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from . import Data
from .Items import item_table, progressive_weapon_names, weapon_chains, weapon_names
from .Locations import location_data_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

WRAM = "Combined WRAM"

ROM_NAME_ADDR = 0x0A0
EXPECTED_ROM_NAME = "MEGAMANZERO3"

SAVE_ADDR = 0x370FC
SAVE_DISK_ADDR = SAVE_ADDR + 0x0BC    # save.disk, 4 disks per byte, low nibble means found.
UNUSED_240_ADDR = SAVE_ADDR + 0x240   # save.unused_240, hijacked to store AP related progress
TAKEN_FLAGS_ADDR = UNUSED_240_ADDR + Data.AP_TAKEN_BYTE

SUBTANK_TAKEN_BITS = {
    Data.AP_LOC_SUBTANK_1: Data.AP_TAKEN_SUBTANK1,
    Data.AP_LOC_SUBTANK_2: Data.AP_TAKEN_SUBTANK2,
}

# The four Sunken Library data files, left out as they are used in level logic.
SKIP_DISK_RESTORE = frozenset({10, 16, 17, 18})

FINAL_STAGE_LOCATION = location_data_table["Complete Abandoned Research Laboratory"].address
STORY_PROGRESS_ITEM_CODE = item_table["Story Progress"]
PROGRESSIVE_WEAPONS = {
    item_table[progressive]: (index, len(weapon_chains[weapon]))
    for index, (weapon, progressive) in enumerate(zip(weapon_names, progressive_weapon_names))
}


class MMZero3Client(BizHawkClient):
    """Talks to gAp, the AP mailbox. See the ROM source code!"""

    game = "Mega Man Zero 3"
    system = "GBA"
    patch_suffix = ".apmmzero3"

    def __init__(self):
        super().__init__()

        self.version_mismatch = False
        self.ap_handshake_logged = False
        self.locations_reported = set()  # location IDs already forwarded to the server

        # Options, overwritten from slot data
        self.options_set = False
        self.starting_weapons = None 

        # DeathLink
        self.death_link = False
        self.pending_death_link = False
        self.death_count_seen = None    # last gAp.deathCount; None until the mailbox is live

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_name = (await bizhawk.read(ctx.bizhawk_ctx, [(ROM_NAME_ADDR, 12, "ROM")]))[0]
        except bizhawk.RequestFailedError:
            return False
        if rom_name.decode("ascii", "replace") != EXPECTED_ROM_NAME:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """If you are searching through the code to understand how it works, I would start here!
        Runs every second or so and processes most of the logic. Interacts with the gAP fields,
        which you can find in the Rom's codebase as ap.c and ap.h"""
        try:
            self.read_slot_data(ctx)
            if self.death_link:
                await ctx.update_death_link(True)

            mailbox = await self.read_mailbox(ctx)
            if mailbox is not None:
                await self.handle_checked_locations(ctx)
                await self.handle_server_checked(ctx)
                await self.handle_received_items(ctx, mailbox)
                await self.handle_death_link(ctx, mailbox)
                await self.handle_goal(ctx)

            await self.handle_collected_pickups(ctx)
        except bizhawk.RequestFailedError:
            pass

    def read_slot_data(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.slot_data or self.options_set:
            return
        self.death_link = bool(ctx.slot_data.get("death_link", 0))
        self.starting_weapons = set(ctx.slot_data.get("starting_weapons", ()))
        self.options_set = True

    async def read_mailbox(self, ctx: "BizHawkClientContext") -> Optional[Dict[str, int]]:
        """One read of gAp. None means the ROM isn't ready.

        ApInit runs on the first Process_Game(), so the ready value not matching means the game is still booting or in the starting menu.
        """
        if self.version_mismatch or ctx.slot is None or not ctx.server_locations:
            return None

        mailbox_bytes = await bizhawk.read(ctx.bizhawk_ctx, [
            (Data.READY, 4, WRAM),
            (Data.VERSION, 2, WRAM),
            (Data.INBOX_WRITE_INDEX, 1, WRAM),
            (Data.INBOX_READ_INDEX, 1, WRAM),
            (Data.ITEMS_APPLIED, 2, WRAM),
            (Data.DISKS_OWNED, 2, WRAM),
            (Data.DEATH_COUNT, 2, WRAM),
            (Data.CAN_ACCEPT_ITEMS, 1, WRAM),
        ])

        (ready, version, inbox_write_index, inbox_read_index,
         items_applied, disks_owned, death_count, can_accept_items) = mailbox_bytes

        if int.from_bytes(ready, "little") != Data.AP_READY:
            return None

        rom_version = int.from_bytes(version, "little")
        if rom_version != Data.AP_VERSION:
            self.version_mismatch = True
            message = (f"ROM/client version mismatch: the ROM is version "
                       f"{rom_version}, this apworld is version {Data.AP_VERSION}. "
                       f"Please generate a new game/ROM!")
            logger.error("MMZero3: %s", message)
            await ctx.send_msgs([{"cmd": "Say", "text": f"[MMZ3] {message}"}])
            return None

        if not self.ap_handshake_logged:
            logger.info("MMZero3: Archipelago Connected!")
            self.ap_handshake_logged = True

        return {
            "inbox_write_index": inbox_write_index[0],
            "inbox_read_index": inbox_read_index[0],
            "items_applied": int.from_bytes(items_applied, "little"),
            "disks_owned": int.from_bytes(disks_owned, "little"),
            "death_count": int.from_bytes(death_count, "little"),
            "can_accept_items": can_accept_items[0] != 0,
        }

    async def handle_checked_locations(self, ctx: "BizHawkClientContext") -> None:
        """Forward every newly set bit of gAp.checkedLocations to the server.

        Game -> client only: one bit per location ID, set by the ROM and never cleared.
        """
        checked_bits = (await bizhawk.read(ctx.bizhawk_ctx, [
            (Data.CHECKED_LOCATIONS, Data.CHECKED_LOCATIONS_COUNT, WRAM),
        ]))[0]

        newly_checked_locations = []
        for location_id in range(len(checked_bits) * 8):
            # 8 locations per byte: >> 3 picks the byte, & 7 the bit inside it. Each bit is one location found in theg ame.
            if not checked_bits[location_id >> 3] & (1 << (location_id & 7)):
                continue
            if location_id in self.locations_reported:
                continue
            self.locations_reported.add(location_id)
            if location_id in ctx.server_locations:
                newly_checked_locations.append(location_id)
            else:
                logger.warning("MMZero3: ROM reported unknown location id %d.", location_id)

        if newly_checked_locations:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": newly_checked_locations}])
            logger.debug("MMZero3: reported %d locations: %s", len(newly_checked_locations), newly_checked_locations)

    async def handle_server_checked(self, ctx: "BizHawkClientContext") -> None:
        """
        Lets the game know which locations have been checked. So that certain items can render the effect
        for when they haven't been picked up yet. (For pickup sanity)
        """
        payload = bytearray(Data.SERVER_CHECKED_COUNT)
        for location_id in ctx.checked_locations:
            if 0 <= location_id < Data.SERVER_CHECKED_COUNT * 8:
                payload[location_id >> 3] |= 1 << (location_id & 7)
        await bizhawk.write(ctx.bizhawk_ctx, [(Data.SERVER_CHECKED, list(payload), WRAM)])

    async def handle_received_items(self, ctx: "BizHawkClientContext", mailbox: Dict[str, int]) -> None:
        """Hand received items to the game through the itemInbox"""
        if not mailbox["can_accept_items"]:
            return
        if self.starting_weapons is None:
            return

        # Both are positions in the 16-slot ring buffer, not counts of items.
        next_slot_to_write = mailbox["inbox_write_index"]
        next_slot_the_game_will_read = mailbox["inbox_read_index"]

        items_sitting_in_inbox = next_slot_to_write - next_slot_the_game_will_read
        if items_sitting_in_inbox < 0:
            items_sitting_in_inbox += Data.ITEM_INBOX_COUNT

        # The client keeps no counter of its own; it reads its position back out of the game.
        items_the_game_already_has = mailbox["items_applied"] + items_sitting_in_inbox

        # One slot is always left free, so equal indices can only mean empty.
        free_inbox_slots = Data.ITEM_INBOX_COUNT - 1 - items_sitting_in_inbox

        first_item_to_send = items_the_game_already_has
        items_not_yet_sent = len(ctx.items_received) - first_item_to_send
        items_to_send_now = min(items_not_yet_sent, free_inbox_slots)
        if items_to_send_now <= 0:
            return

        pending_writes = []
        for offset in range(items_to_send_now):
            item_index = first_item_to_send + offset
            item_code = self.game_item_code(ctx, item_index)
            slot_address = Data.ITEM_INBOX + next_slot_to_write * Data.ITEM_INBOX_ELEMENT_SIZE
            item_code_bytes = item_code.to_bytes(Data.ITEM_INBOX_ELEMENT_SIZE, "little")
            pending_writes.append((slot_address, list(item_code_bytes), WRAM))

            next_slot_to_write += 1
            if next_slot_to_write == Data.ITEM_INBOX_COUNT:
                next_slot_to_write = 0

        pending_writes.append((Data.INBOX_WRITE_INDEX, [next_slot_to_write], WRAM))
        await bizhawk.write(ctx.bizhawk_ctx, pending_writes)

        items_still_waiting = items_not_yet_sent - items_to_send_now
        logger.debug("MMZero3: pushed %d items to the game, %d total still waiting.", items_to_send_now, items_still_waiting)

    def game_item_code(self, ctx: "BizHawkClientContext", item_index: int) -> int:
        """The ROM item code to send for ctx.items_received[item_index].

        Used for any progressive item (weapons and story progress).
        """
        ap_item_code = int(ctx.items_received[item_index].item)

        if ap_item_code == STORY_PROGRESS_ITEM_CODE:
            # First copy becomes ROM code 229, second copy 230.
            if self.copies_received(ctx, item_index) == 1:
                return Data.AP_ITEM_STORY_MID
            return Data.AP_ITEM_STORY_LATE

        if ap_item_code in PROGRESSIVE_WEAPONS:
            weapon_index, max_level = PROGRESSIVE_WEAPONS[ap_item_code]
            level = self.copies_received(ctx, item_index)

            if weapon_names[weapon_index] in self.starting_weapons:
                level += 1

            if level > max_level:
                level = max_level

            return (Data.AP_ITEM_WEAPON_LEVEL_FIRST
                    + weapon_index * Data.AP_ITEM_CODES_PER_WEAPON
                    + level)

        return ap_item_code

    @staticmethod
    def copies_received(ctx: "BizHawkClientContext", item_index: int) -> int:
        this_item = ctx.items_received[item_index].item
        history_so_far = ctx.items_received[:item_index + 1]

        copies = 0
        for earlier_item in history_so_far:
            if earlier_item.item == this_item:
                copies += 1
        return copies

    async def handle_death_link(self, ctx: "BizHawkClientContext",
                                mailbox: Dict[str, int]) -> None:
        death_count = mailbox["death_count"]
        if self.death_count_seen is None:
            self.death_count_seen = death_count
        elif death_count > self.death_count_seen:
            self.death_count_seen = death_count
            if "DeathLink" in ctx.tags:
                await self.send_deathlink(ctx)
        elif death_count < self.death_count_seen:
            self.death_count_seen = death_count

        if self.pending_death_link:
            self.pending_death_link = False
            await bizhawk.write(ctx.bizhawk_ctx, [
                (Data.KILL_REQUEST, [Data.AP_KILL_REQUESTED], WRAM),
            ])

    async def handle_goal(self, ctx: "BizHawkClientContext") -> None:
        """
        Check if final stage is cleared.
        """
        if ctx.finished_game:
            return
        if FINAL_STAGE_LOCATION not in self.locations_reported:
            return

        await ctx.send_msgs([
            {"cmd": "Say", "text": "Final stage cleared! Game completed!"},
            {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL},
        ])
        ctx.finished_game = True

    async def handle_collected_pickups(self, ctx: "BizHawkClientContext") -> None:
        """Keep the game's RAM synced with the locations the server says are checked.

        Stops pickups from respawning
        """
        collected_disks, taken_byte = await bizhawk.read(ctx.bizhawk_ctx, [
            (SAVE_DISK_ADDR, Data.AP_DISK_BYTES, WRAM),
            (TAKEN_FLAGS_ADDR, 1, WRAM),
        ])
        repaired_disks = bytearray(collected_disks)
        repaired_taken = taken_byte[0]
        for location_id in ctx.checked_locations:
            if location_id in SKIP_DISK_RESTORE:
                continue
            if Data.AP_ITEM_DISK_FIRST <= location_id <= Data.AP_ITEM_DISK_LAST:
                disk_index = location_id - 1
                repaired_disks[disk_index // 4] |= 1 << (disk_index % 4)
            elif location_id in SUBTANK_TAKEN_BITS:
                repaired_taken |= SUBTANK_TAKEN_BITS[location_id]

        writes = []
        if repaired_disks != collected_disks:
            writes.append((SAVE_DISK_ADDR, list(repaired_disks), WRAM))
        if repaired_taken != taken_byte[0]:
            writes.append((TAKEN_FLAGS_ADDR, [repaired_taken], WRAM))
        if writes:
            await bizhawk.write(ctx.bizhawk_ctx, writes)

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        await ctx.send_death("Zero was destroyed.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced" and "tags" in args:
            if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                self.on_deathlink(ctx)
