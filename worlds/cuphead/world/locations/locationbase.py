### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import NamedTuple

from BaseClasses import LocationProgressType


class LocationData(NamedTuple):
    id: int | None
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    event: bool = False

    def with_progress_type(self, progress_type: LocationProgressType) -> "LocationData":
        return LocationData(self.id, progress_type, self.event)
