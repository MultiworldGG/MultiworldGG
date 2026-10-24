import sys

from . import run_client

# Guarded: the spawned PCSX2 worker re-imports this module as __mp_main__.
if __name__ == "__main__":
    run_client(*sys.argv[1:])
