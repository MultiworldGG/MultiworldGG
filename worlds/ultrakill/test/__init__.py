from test.bases import WorldTestBase
from .. import UltrakillWorld


class UltrakillTestBase(WorldTestBase):
    game = "ULTRAKILL"
    world: UltrakillWorld
