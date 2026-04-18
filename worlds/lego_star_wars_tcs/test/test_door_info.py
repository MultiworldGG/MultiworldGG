import itertools
from typing import Iterable
from unittest import TestCase

from ..client.game_state_modifiers import locked_cantina_door_display as door_display

ALL_DOORS: list[Iterable[door_display.Coordinates]] = [
    door_display.MAIN_ROOM_DOORS.values(),
    door_display.EPISODE_2_DOORS.values(),
    door_display.EPISODE_3_DOORS.values(),
]


class TestDoorInfo(TestCase):
    MIN_DOOR_DISTANCE = door_display.ACTIVATION_DISTANCE

    def test_distances_between_doors(self):
        for doors_dict in door_display.RELEVANT_ROOMS_TO_DOORS.values():
            door1: door_display.Coordinates
            door2: door_display.Coordinates
            for door1, door2 in itertools.combinations(doors_dict.values(), r=2):
                # No overlap.
                self.assertGreater(door1.xz_distance(door2), self.MIN_DOOR_DISTANCE * 2)
