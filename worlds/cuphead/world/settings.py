### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import Union  # type: ignore

import settings

from .. import varis


class CupheadSettings(settings.Group):
    class Debug(int):
        """Debug mode."""

    ## A bitwise integer that sets specific debug flags.
    debug: Union[Debug, int] = 0 # type: ignore

    def is_debug_bit_on(self, bit: int) -> bool:
        """
        Checks if a certain bit in the debug setting is enabled.

        Args:
            bit (int): the bit(s) to check for.

        Returns:
            bool: True if the bit(s) are enabled in settings.

        Known bits:
            1: Verbose
            2: Print Regions
            4: Visualize Regions (generates PUML)
            8: Visualize Regions highlight reachable
            16: Debug hint_dict
            32: Debug aux
            64: Debug options + slot_data
            128: Debug levelrules
            256: Debug rulereg
            512: Visualize Regions generated for Universal Tracker
            1024: Debug even in tests
            2048: Debug Tests
        """

        #print(f"debug_bit_test {bit:f}")

        if varis.testing and (int(self.debug) & 1024) == 0:
            return False
        return (int(self.debug) & bit) == bit
