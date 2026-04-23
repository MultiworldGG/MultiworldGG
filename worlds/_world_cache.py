"""
Cache helpers for world loading - launcher component/icon cache only.
"""

import logging


def has_launcher_cache() -> bool:
    """Return True only if the cache file exists *and* passes validation."""
    try:
        from worlds.LauncherComponents import _load_launcher_cache
        return _load_launcher_cache() is not None
    except Exception:
        return False


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
