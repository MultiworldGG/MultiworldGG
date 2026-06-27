from pathlib import Path

import settings

class Sims4Settings(settings.Group):
    class ModsFolder(settings.UserFolderPath):
        """Path to the Sims 4 Mods folder"""
        description = "the folder your Sims 4 mods are installed to"

    mods_folder: ModsFolder = ModsFolder(Path.home() / "Documents" / "Electronic Arts" / "The Sims 4" / "Mods")