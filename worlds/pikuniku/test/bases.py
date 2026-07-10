from test.bases import WorldTestBase

from ..world import PikunikuWorld


class PikunikuTestBase(WorldTestBase):
    game = "Pikuniku"
    world: PikunikuWorld
