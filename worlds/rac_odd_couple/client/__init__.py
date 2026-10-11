"""
Launcher entry point for the Odd Couple client.

Two distinct actions live behind the one "Ratchet & Clank: The Odd Couple
Client" component (see the world package's __init__.py), depending on how
it's invoked:

- Opening a .apoddcouple patch file: patches the player's local vanilla swf
  with the Python patcher (patch.py/swf_patch.py) and installs the result.
  Nothing else - no server, no browser tab.
- Launching the client with no file: just opens the already-installed
  frontend in the browser. The page connects to the Archipelago server
  itself via archipelago.min.js; the only thing this process still runs is
  the small static/relay server the patched swf's own button-gating calls
  need (see backend.py) - there is no Archipelago protocol client here.
"""
from __future__ import annotations

import argparse
import logging
import webbrowser

import Patch
import Utils

from .backend import BASE_URL, OddCoupleServer, find_installed_patched_swf, install_patched_swf

logger = logging.getLogger("OddCoupleClient")


def launch(*launch_args: str) -> None:
    Utils.init_logging("OddCoupleClient", exception_logger="Client")

    parser = argparse.ArgumentParser()
    parser.add_argument("diff_file", default="", type=str, nargs="?",
                         help="Path to a .apoddcouple Archipelago patch file")
    args = parser.parse_args(launch_args)

    if args.diff_file:
        logger.info("Patch file was supplied - patching the local odd_couple.swf...")
        try:
            _meta, swf_path = Patch.create_rom_file(args.diff_file)
            install_patched_swf(swf_path)
        except Exception as ex:
            logger.exception("Failed to patch the local odd_couple.swf")
            Utils.messagebox("Ratchet & Clank: The Odd Couple", f"Failed to patch the game:\n{ex}", error=True)
            return
        logger.info(f"Wrote patched swf to {swf_path}")
        Utils.messagebox("Ratchet & Clank: The Odd Couple",
                          "Patched! You can now launch the Odd Couple client to play.")
        return

    if not find_installed_patched_swf():
        logger.warning("No patched swf installed yet - open a .apoddcouple file to generate one.")
        Utils.messagebox("Ratchet & Clank: The Odd Couple",
                          "No patched game found. Open your .apoddcouple patch file first, "
                          "then launch the client again.", error=True)
        return

    server = OddCoupleServer()
    server.start()
    webbrowser.open(BASE_URL)
    logger.info(f"Serving the Odd Couple client at {BASE_URL} - closing the browser tab will stop this too.")

    try:
        server.page_closed.wait()
    except KeyboardInterrupt:
        logger.info("Interrupted - shutting down.")
    finally:
        server.stop()
