from ..constants import MIN_UNIVERSAL_TRACKER_VERSION

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor, UT_VERSION
    universal_tracker_loaded = True
except ImportError:
    TrackerGameContext = None
    TrackerCommandProcessor = None
    UT_VERSION = MIN_UNIVERSAL_TRACKER_VERSION
    universal_tracker_loaded = False

def has_invalid_universal_tracker(ut_version: str) -> bool:
    delimiter = "."

    version_split = ut_version.split(delimiter)
    if len(version_split) < 3:
        return True

    clean_version_split = version_split.copy()
    for i, version in enumerate(version_split):
        clean_version_split[i]  = "".join([ele for ele in version if ele.isdigit()]) # Clean everything but digits from each part of the split

    tracker_version = tuple(int(ele) for ele in clean_version_split)
    if tracker_version < MIN_UNIVERSAL_TRACKER_VERSION:
        return True

    return False

if universal_tracker_loaded and has_invalid_universal_tracker(UT_VERSION):
    raise ImportError(f"Need to update universal tracker version to at least v{'.'.join(map(str, MIN_UNIVERSAL_TRACKER_VERSION))}.")