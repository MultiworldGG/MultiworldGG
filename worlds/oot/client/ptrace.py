"""Helper module for managing Linux ptrace scope permissions."""

import os
import platform
import subprocess

IS_LINUX = platform.system() == "Linux"

try:
    from CommonClient import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


def check_and_fix_ptrace_scope() -> bool:
    """Check if ptrace scope is restrictive and attempt to fix it."""
    if not IS_LINUX:
        return True

    ptrace_scope_path = "/proc/sys/kernel/yama/ptrace_scope"

    if not os.path.exists(ptrace_scope_path):
        return True

    try:
        with open(ptrace_scope_path, "r") as f:
            scope = int(f.read().strip())

        if scope == 0:
            return True

        logger.info(f"Detected restrictive ptrace scope ({scope}). Attempting to enable memory access...")
        logger.info("You may be prompted for your sudo password.")

        try:
            result = subprocess.run(["sudo", "tee", ptrace_scope_path], input=b"0\n", timeout=30)
            if result.returncode == 0:
                logger.info("Successfully enabled ptrace access.")
                return True
            else:
                logger.warning("Failed to set ptrace scope. You may need to run manually:")
                logger.warning(f"  echo 0 | sudo tee {ptrace_scope_path}")
                return False
        except subprocess.TimeoutExpired:
            logger.warning("Sudo prompt timed out.")
            return False
        except Exception as e:
            logger.warning(f"Failed to set ptrace scope: {e}")
            logger.warning(f"You may need to run manually: echo 0 | sudo tee {ptrace_scope_path}")
            return False

    except Exception as e:
        logger.warning(f"Could not check ptrace scope: {e}")
        return True
