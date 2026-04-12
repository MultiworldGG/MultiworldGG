from __future__ import annotations
from typing import Union # type: ignore
import os
import settings

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
            256: Visualize Regions generated for Universal Tracker
            512: Debug even in tests
            1024: Debug Tests
        """

        if "PYTEST_CURRENT_TEST" in os.environ and (int(self.debug) & 512) == 0:
            return False
        return (int(self.debug) & bit) == bit
