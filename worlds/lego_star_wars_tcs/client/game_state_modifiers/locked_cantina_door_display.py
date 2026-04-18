import math
from dataclasses import dataclass, field
from typing import Self

from . import ClientComponent
from .text_replacer import TextId
from ..common import NuVecField, StaticFloat, StaticInt, StaticUint, UShortField, TCSContext
from ..common_addresses import CantinaRoom, player_character_entity_iter
from ..events import subscribe_event, OnGameWatcherTickEvent, OnLevelChangeEvent, OnReceiveSlotDataEvent
from ...levels import SHORT_NAME_TO_CHAPTER_AREA, EPISODE_TO_CHAPTER_AREAS


LEVEL_ID_CANTINA = 325


# Technically this is the feet position
CHARACTER_POSITION_VECTOR = NuVecField(0x5c)
"""Feet position of a character (GameObject_s)."""

HUB_EPISODE_TIME = StaticFloat(0x879574)
"""Timer float for the Cantina episode door on-screen text. If this is set by the game, then the on-screen text for
an episode door is currently being displayed. Setting this above zero do *not* cause the on-screen text to display."""

HUB_AREA_TIME = StaticFloat(0x879508)
"""
Timer float for the Cantina area door on-screen text. Setting this above zero causes the on-screen text to display
according to the Area ID that the value at HUB_AREA is set to.
"""

HUB_AREA = StaticInt(0x879B00)
"""Area ID for the Cantina level door on-screen text."""

A_DATA_LIST_PTR = StaticUint(0x951354)
"""Pointer to the start of the AREADATA_s array _ADataList."""

AREA_DATA_SIZE = 0x9c
"""sizeof(AREADATA_s)"""

AREA_DATA_NAME_ID = UShortField(0x78)
""".NameId of AREADATA_s, the localisation text ID of the area."""

EPISODE_1_ENDING_AREA_ID = 7
AREA_ID_TO_USE = EPISODE_1_ENDING_AREA_ID


@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float
    z: float
    as_tuple: tuple[float, float, float] = field(init=False)
    as_xz_tuple: tuple[float, float] = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "as_tuple", (self.x, self.y, self.z))
        object.__setattr__(self, "as_xz_tuple", (self.x, self.z))

    def distance(self, other: Self):
        return math.dist(self.as_tuple, other.as_tuple)

    def xz_distance(self, other: Self):
        return math.dist(self.as_xz_tuple, other.as_xz_tuple)

    # Normally, squared distance would be faster to calculate, but math.dist is accelerated using C, and outperforms
    # calculating squared distance in Python, by multiple times.
    # def distance_squared(self, other: Self):
    #     return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
    #
    # def xz_distance_squared(self, other: Self):
    #     return (self.x - other.x) ** 2 + (self.z - other.z) ** 2


ACTIVATION_DISTANCE = 0.30734664296783093
# EPISODE_1_DOOR_ACTIVATION_FURTHEST_ACTIVATION = Coordinates(-23.21241951, 0.001831591129, -51.91680908)

# These coordinates were recorded by standing against the locked door, roughly in the middle.
# The bonus doors were already open on the file I used, so I stood within the doorframe instead.
MAIN_ROOM_DOORS = {
    "1": Coordinates(-22.9132, 0.0013, -51.9870),
    "2": Coordinates(-23.2557, 0.0013, -52.9901),
    "3": Coordinates(-23.7055, 0.0013, -53.9667),
    "4": Coordinates(-24.3302, 0.0013, -54.8765),
    "5": Coordinates(-25.2044, 0.0014, -55.5948),
    "6": Coordinates(-26.2368, 0.0014, -56.1084),
    # "arcade": Coordinates(-22.4908, 0.0022, -49.889),
    # "bonus": Coordinates(-28.2893, 0.0015, -57.1381),
    # "junkyard": Coordinates(-27.9784, 0.1109, -46.8383),
}
EPISODE_1_DOORS = {
    "1": Coordinates(-13.7371, 0.0013, -55.6437),
    "2": Coordinates(-13.5916, 0.0013, -54.0831),
    "3": Coordinates(-12.8858, 0.0013, -52.9075),
    "4": Coordinates(-11.6144, 0.0013, -52.2382),
    "5": Coordinates(-9.9517, 0.0013, -51.9606),
    "6": Coordinates(-8.4534, 0.0013, -52.4315),
    # "bonus": Coordinates(-6.4901, 0.0015, -53.8392),
}
EPISODE_2_DOORS = {
    "1": Coordinates(-12.2607, 0.0013, -64.5745),
    "2": Coordinates(-10.8183, 0.0013, -64.5931),
    "3": Coordinates(-9.4126, 0.0013, -64.3750),
    "4": Coordinates(-7.9266, 0.0013, -63.7392),
    "5": Coordinates(-6.7660, 0.0013, -64.6734),
    "6": Coordinates(-6.6051, 0.0013, -66.0659),
    # "bonus": Coordinates(-5.7765, 0.0015, -68.8038),
}
EPISODE_3_DOORS = {
    "1": Coordinates(-7.4674, 0.0013, -74.3870),
    "2": Coordinates(-7.4676, 0.0013, -75.5595),
    "3": Coordinates(-7.3477, 0.0013, -76.6879),
    "4": Coordinates(-7.1177, 0.0013, -78.0387),
    "5": Coordinates(-7.2158, 0.0013, -79.3340),
    "6": Coordinates(-7.8197, 0.0013, -80.4848),
    # "bonus": Coordinates(-10.0878, 0.0013, -81.1680),
}
EPISODE_4_DOORS = {
    "1": Coordinates(-11.9416, 0.0013, -90.8385),
    "2": Coordinates(-10.8066, 0.0013, -90.8385),
    "3": Coordinates(-9.6827, 0.0013, -90.9004),
    "4": Coordinates(-7.1865, 0.0013, -93.2124),
    "5": Coordinates(-7.1753, 0.0013, -94.3230),
    "6": Coordinates(-7.1465, 0.0013, -95.4684),
    # "bonus": Coordinates(-7.0653, 0.0013, -98.1796),
}
EPISODE_5_DOORS = {
    "1": Coordinates(-13.3404, 0.0013, -108.3106),
    "2": Coordinates(-12.3556, 0.0013, -106.8501),
    "3": Coordinates(-10.7851, 0.0013, -106.1567),
    "4": Coordinates(-9.4099, 0.0013, -105.9008),
    "5": Coordinates(-7.8177, 0.0013, -106.4374),
    "6": Coordinates(-7.0013, 0.0013, -107.5948),
    # "bonus": Coordinates(-5.7996, 0.0013, -110.5100),
}
EPISODE_6_DOORS = {
    "1": Coordinates(-10.2091, 0.0013, -120.9750),
    "2": Coordinates(-9.2976, 0.0013, -120.0989),
    "3": Coordinates(-8.1642, 0.0013, -119.6590),
    "4": Coordinates(-6.9686, 0.0013, -119.8224),
    "5": Coordinates(-5.9117, 0.0013, -120.4271),
    "6": Coordinates(-5.1751, 0.0013, -121.4412),
    # "bonus": Coordinates(-4.1028, 0.0015, -125.8803),
}
# JUNKYARD_DOORS = {
#     "cantina": Coordinates(-30.6921, 0.04027, -35.0349),
#     "missions": Coordinates(-33.2018, -0.0048, -29.2741),
# }
# MISSIONS_DOORS = {
#     "junkyard": Coordinates(-31.8879, 0.1481, -72.2756),
# }

RELEVANT_ROOMS_TO_DOORS: dict[CantinaRoom, dict[str, Coordinates]] = {
    CantinaRoom.SHOP_ROOM: MAIN_ROOM_DOORS,
    CantinaRoom.EPISODE_1: EPISODE_1_DOORS,
    CantinaRoom.EPISODE_2: EPISODE_2_DOORS,
    CantinaRoom.EPISODE_3: EPISODE_3_DOORS,
    CantinaRoom.EPISODE_4: EPISODE_4_DOORS,
    CantinaRoom.EPISODE_5: EPISODE_5_DOORS,
    CantinaRoom.EPISODE_6: EPISODE_6_DOORS,
}


class LockedCantinaDoorDisplay(ClientComponent):
    active: bool = False
    is_drawing: bool = False
    # TODO: Add some way to cycle through the locked chapters within a locked episode, so that each chapter's unlock
    #  requirements can be seen.
    #_episode_door_chapter_cycle: int = 0

    @subscribe_event
    def on_receive_slot_data(self, event: OnReceiveSlotDataEvent):
        if event.first_time_setup:
            # Set the Episode 1 Ending Area's localised Text ID to something we can overwrite. In this case, one of the
            # Wii Motion Control hints.
            # The Episode 1 Ending Area is picked because Episode endings are not levels that can be accessed directly
            # from the Cantina, so do not have a localised Text ID assigned to their name in vanilla, meaning it can be
            # freely overridden as needed.
            a_data_list_addr = A_DATA_LIST_PTR.get(event.context)
            episode_1_ending_area_data_addr = a_data_list_addr + AREA_DATA_SIZE * AREA_ID_TO_USE
            AREA_DATA_NAME_ID.set(event.context, episode_1_ending_area_data_addr, TextId.WII_MOTION_CONTROL_HINT_1)
            pass

        # Initialise active state based on the current level ID.
        self.active = event.context.current_level_id == LEVEL_ID_CANTINA

    @subscribe_event
    def on_level_change(self, event: OnLevelChangeEvent):
        self.active = event.new_level_id == LEVEL_ID_CANTINA

    @staticmethod
    def _write_text(ctx: TCSContext, text: str):
        ctx.text_replacer.write_custom_string(TextId.WII_MOTION_CONTROL_HINT_1, text)

    def _draw_episode_info(self, ctx: TCSContext, episode: int) -> bool:
        chapter_manager = ctx.unlocked_chapter_manager
        if not chapter_manager.is_episode_enabled(episode):
            self._write_text(ctx, f"Episode {episode} is not enabled")
            return True

        if chapter_manager.is_episode_unlocked(episode):
            # The Episode is already unlocked, and should be displaying the vanilla Episode door info (with text
            # potentially modified by other parts of the client)
            return False

        enabled_chapters = [chapter for chapter in EPISODE_TO_CHAPTER_AREAS[episode]
                            if chapter_manager.is_chapter_enabled(chapter)]
        if len(enabled_chapters) == 0:
            self._write_text(ctx, f"Error: Episode {episode} is locked, but no enabled Chapters in the Episode"
                                  f" were found.")
        elif len(enabled_chapters) == 1:
            self._write_text(ctx, chapter_manager.format_locked_chapter_requirements(enabled_chapters[0]))
        elif len(enabled_chapters) == 2:
            self._write_text(ctx, f"Unlock either {enabled_chapters[0].name} or {enabled_chapters[1].name}")
        else:
            names = [chapter.name for chapter in enabled_chapters]
            self._write_text(ctx, f"Unlock any of {', '.join(names[:-1])} or {names[-1]}")
        return True

    def _draw_chapter_info(self, ctx: TCSContext, short_name: str) -> bool:
        chapter = SHORT_NAME_TO_CHAPTER_AREA[short_name]
        chapter_manager = ctx.unlocked_chapter_manager
        if not chapter_manager.is_chapter_enabled(chapter):
            self._write_text(ctx, f"{chapter.name} ({chapter.short_name}) is not enabled")
            return True

        if chapter_manager.is_chapter_unlocked(chapter):
            # The chapter is already unlocked, and should be displaying the vanilla Chapter door info (with text
            # potentially modified by other parts of the client).
            return False

        to_write = chapter_manager.format_locked_chapter_requirements(chapter)
        if to_write:
            self._write_text(ctx, to_write)
            return True
        else:
            self._write_text(ctx, f"Error: {chapter.name} is locked, but its requirements could not be found")
            return False

    def _draw_info(self, ctx: TCSContext, room_id: CantinaRoom, door_name: str) -> None:
        room = room_id.value
        if room == 0:
            if len(door_name) == 1 and ("1" <= door_name <= "6"):
                has_drawn = self._draw_episode_info(ctx, int(door_name))
            else:
                has_drawn = False
        else:
            episode = room
            if len(door_name) == 1 and ("1" <= door_name <= "6"):
                short_name = f"{episode}-{door_name}"
                has_drawn = self._draw_chapter_info(ctx, short_name)
            else:
                has_drawn = False
        if has_drawn:
            # Set the area ID used by the game to display
            HUB_AREA.set(ctx, AREA_ID_TO_USE)
            # Set/refresh the timer.
            HUB_AREA_TIME.set(ctx, 1.1)
            self.is_drawing = True

    async def _draw_locked_door_info(self, event: OnGameWatcherTickEvent):
        # When not drawing, check roughly twice per second, offset by 2 ticks.
        if not self.is_drawing and ((event.tick_count + 2) % 5 != 0):
            return
        # Assume we are no longer needing to draw anything.
        was_drawing = self.is_drawing
        self.is_drawing = False
        ctx = event.context
        current_room = ctx.current_cantina_room
        if current_room not in RELEVANT_ROOMS_TO_DOORS:
            # The player is in a room we don't care about.
            return

        current_doors = RELEVANT_ROOMS_TO_DOORS[current_room]

        if HUB_EPISODE_TIME.get(ctx) > 0:
            # Episode door text is currently on-screen.
            if was_drawing:
                # Ensure the Area text is hidden if Episode text is currently being displayed. They overlap otherwise.
                HUB_AREA_TIME.set(ctx, 0.0)
            return

        if HUB_AREA.get(ctx) not in (-1, AREA_ID_TO_USE):
            # Area door text other than our own is currently on-screen.
            return

        # Find if a player is within ACTIVATION_DISTANCE of a relevant door within this room.
        for _player_number, player_address in player_character_entity_iter(ctx):
            player_pos = Coordinates(*CHARACTER_POSITION_VECTOR.get(ctx, player_address))
            for door_name, door_pos in current_doors.items():
                if player_pos.distance(door_pos) < ACTIVATION_DISTANCE:
                    self._draw_info(ctx, current_room, door_name)
                    return

    @staticmethod
    async def _force_open_episode_doors(event: OnGameWatcherTickEvent):
        # Check roughly once per second, offset by 3 ticks.
        if ((event.tick_count + 3) % 10) != 0:
            return
        # The player is not in the main room with the shop and the doors to each Episode area, so don't bother doing
        # anything.
        if event.context.current_cantina_room != CantinaRoom.SHOP_ROOM:
            return

        # I haven't yet figured out the proper pointer path to the array of transformation matrices of the 'special
        # objects' in the current level (most objects within a level that can move). Fortunately, there are some static
        # Cantina splines which seem to have a fixed offset from the array, so use one of those static splines to get to
        # the array.
        # I'm guessing this works because each level defines maximum numbers of each level object type, and the game
        # probably allocates the maximum space required for each type, so, within an individual level, the offset, from
        # the splines array to the 'special objects''s matrices array, is a constant value.
        hub_minikitviewer_camspl_p_addr = 0x879b3c
        ctx = event.context
        hub_minikitviewer_camspl_addr = ctx.read_uint(hub_minikitviewer_camspl_p_addr)
        # +0x4ec to get to the start of the array.
        # Each transformation matrix is 64 bytes (4x4 of float32).
        # The Episode 1 door is the 164th element in this array, so +64 bytes * 164 = +10496 bytes
        # The matrix is an affine transformation matrix with memory arranged in columns first. The third element of the
        # fourth column gives the Y position. Each column is 4x float32, so skip 3 columns +4*4*3, then, skip the first
        # float32 in that column, +4.
        episode_1_door_y_addr = hub_minikitviewer_camspl_addr + 11808
        # The transformation matrices of each Episode door are conveniently in sequence in memory (the order appears to,
        # be determined by the order they are in the level file, as seen in BrickBench), so an offset of 64 bytes gets
        # to the matrix for the next door object.
        for i in range(6):
            # Force open the door if the episode is enabled.
            if ctx.unlocked_chapter_manager.is_episode_enabled(i + 1):
                # Forcefully open the door by writing a y position that moves the door out of the way.
                ctx.write_float(episode_1_door_y_addr + i * 64, 0.63, raw=True)

    @subscribe_event
    async def on_tick(self, event: OnGameWatcherTickEvent):
        if not self.active:
            return
        await self._draw_locked_door_info(event)
        await self._force_open_episode_doors(event)




