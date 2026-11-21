import itertools
from typing import Iterable
from unittest import TestCase

from ..client.game_state_modifiers import locked_cantina_door_display as door_display

# noinspection PyProtectedMember
ALL_DOORS: list[Iterable[door_display._Coordinates]] = [
    door_display._MAIN_ROOM_DOORS.values(),
    door_display._EPISODE_1_DOORS.values(),
    door_display._EPISODE_2_DOORS.values(),
    door_display._EPISODE_3_DOORS.values(),
    door_display._EPISODE_4_DOORS.values(),
    door_display._EPISODE_5_DOORS.values(),
    door_display._EPISODE_6_DOORS.values(),
]


class TestDoorInfo(TestCase):
    MIN_DOOR_DISTANCE = door_display._ACTIVATION_DISTANCE

    def test_distances_between_doors(self):
        for doors_dict in door_display._RELEVANT_ROOMS_TO_DOORS.values():
            door1: door_display._Coordinates
            door2: door_display._Coordinates
            for door1, door2 in itertools.combinations(doors_dict.values(), r=2):
                # No overlap.
                self.assertGreater(door1.xz_distance(door2), self.MIN_DOOR_DISTANCE * 2)
