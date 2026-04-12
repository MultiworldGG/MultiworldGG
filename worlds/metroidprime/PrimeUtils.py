import os
import pkgutil
import platform


def get_apworld_version():
    # Get version from ./version.txt
    # detect if on windows since pathing is handled differently from linux
    if platform.system() == "Windows":
        path = os.path.join(os.path.dirname(__file__), "version.txt")
    else:
        path = "version.txt"
    version = pkgutil.get_data(__name__, path).decode().strip()
    return version
