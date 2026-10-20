
from .bases import PokemonSnapTestBase
from ..client import _has_invalid_universal_tracker
from ..constants import MIN_UNIVERSAL_TRACKER_VERSION

class TestSparseLocationGeneration(PokemonSnapTestBase):

    def test_minimum_unit_version(self):

        invalid_versions = [ "v0.0.11.11","wre.121","five hundred", "3", "0.0.0", "v0.2.10"]
        valid_versions = [ "_v0.2.24.1" ,"v2.11.11", "v3.0.0", "0.25.120202"]

        for invalid_version in invalid_versions:
            if not _has_invalid_universal_tracker(invalid_version):
                self.fail(f"Incorrectly flagged version as valid: {invalid_version}")

        for valid_version in valid_versions:
            if _has_invalid_universal_tracker(valid_version):
                self.fail(f"Incorrectly flagged version as invalid: {valid_version}")

        current_version = '.'.join(map(str,MIN_UNIVERSAL_TRACKER_VERSION))
        if _has_invalid_universal_tracker(current_version):
            self.fail(f"Incorrectly flagged current minimum version as invalid: {current_version}. Check MIN_UNIVERSAL_TRACKER_VERSION.")