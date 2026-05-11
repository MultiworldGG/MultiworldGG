### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import ClassVar

from typing_extensions import override

from test.bases import WorldTestBase

from .. import CupheadWorld, varis

varis.testing = True
print("---- Cuphead APWorld Test Mode ----")

class CupheadTestBase(WorldTestBase):
    game: ClassVar[str] = CupheadWorld.GAME_NAME
    should_run_default_tests: ClassVar[bool] = False

    @property
    @override
    def run_default_tests(self) -> bool:
        return super().run_default_tests if self.should_run_default_tests else False
