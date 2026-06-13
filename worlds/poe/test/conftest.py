"""
pytest configuration for Path of Exile tests
"""
import sys
import os

def setup_paths():
    current_dir = os.path.dirname(__file__)
    poe_dir = os.path.dirname(current_dir)
    worlds_dir = os.path.dirname(poe_dir)
    archipelago_dir = os.path.dirname(worlds_dir)

    if archipelago_dir not in sys.path:
        sys.path.insert(0, archipelago_dir)

setup_paths()
