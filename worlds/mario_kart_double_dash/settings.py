import settings

class MkddSettings(settings.Group):
    class DolphinProcessName(str):
        """The name of the Dolphin process to connect to. Leave blank for system default."""

    class DolphinPath(settings.UserFilePath):
        """Path to the Dolphin executable."""
        description = "Dolphin executable"
        is_exe = True

    class RomPath(settings.OptionalUserFilePath):
        """Path to the Mario Kart: Double Dash!! (USA) rom."""
        description = "Mario Kart: Double Dash!! (USA) rom"
    
    dolphin_process_name: DolphinProcessName = ""
    dolphin_path: DolphinPath = DolphinPath()
    rom_path: RomPath = RomPath()
