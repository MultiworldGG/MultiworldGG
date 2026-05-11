### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import ClassVar

from . import CupheadTestBase


class DefaultTests(CupheadTestBase):
    should_run_default_tests: ClassVar[bool] = True

    def test_default(self): ...
