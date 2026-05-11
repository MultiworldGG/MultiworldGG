### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING

from . import levelrulecomp as lrc

if TYPE_CHECKING:
    from .... import CupheadWorld

def set_levelrules(world: "CupheadWorld"):
    lrc.LevelRuleComp(world).compile_levelrules()
