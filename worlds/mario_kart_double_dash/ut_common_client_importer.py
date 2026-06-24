tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (
            TrackerCommandProcessor as ClientCommandProcessor,
            TrackerGameContext as CommonContext,
            UT_VERSION)
    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext
    UT_VERSION = ""
