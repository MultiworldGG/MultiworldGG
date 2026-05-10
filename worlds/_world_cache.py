"""
Cache helpers for world loading - launcher component/icon cache only.
"""

import logging


def prepare_for_worlds_load() -> None:
    """Remove launcher cache stubs before loading real world components."""
    try:
        from worlds import LauncherComponents
        LauncherComponents.prepare_for_worlds_load()
    except Exception as exc:
        logging.warning(f"Failed to prepare launcher components for world loading: {exc}")


def has_launcher_cache() -> bool:
    """Return True only if the cache file exists *and* passes validation."""
    try:
        from worlds.LauncherComponents import _load_launcher_cache
        return _load_launcher_cache() is not None
    except Exception:
        return False


def write_launcher_cache_if_missing(write_launcher_cache: bool = True) -> None:
    """Write launcher cache after world loading when requested and no valid cache exists."""
    if not write_launcher_cache or has_launcher_cache():
        return

    try:
        from worlds import LauncherComponents
        LauncherComponents.write_launcher_cache()
    except Exception as exc:
        logging.warning(f"Failed to write launcher cache: {exc}")


def rebuild_world_caches() -> None:
    """Rebuild launcher cache from current in-memory world state."""
    import worlds
    if not worlds._worlds_loaded:
        return

    worlds._build_network_data_packages()
    try:
        from worlds import LauncherComponents
        LauncherComponents.write_launcher_cache()
    except Exception as exc:
        logging.warning(f"Failed to write launcher cache during rebuild: {exc}")
