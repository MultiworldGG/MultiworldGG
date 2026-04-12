from typing import ClassVar

from test.bases import WorldTestBase


class RabiRibiTestBase(WorldTestBase):
    game = "Rabi-Ribi"
    player: ClassVar[int] = 1
