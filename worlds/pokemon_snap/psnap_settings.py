import settings

class UseProject64(settings.Bool):
    description = ("Whether to use Project64 as the default emulator or not. By having this enabled, "
        "extra setup is required to enable communication between AP and PJ64.")

class Project64Executable(settings.UserFilePath):
    """ The path for Project64 executable. If using Flatpak, specify this path instead. """
    description = "Project64 executable path"
    is_exe = True

class EmulatorSettings(settings.Group):
    """Various Emulator specific settings (such as Project64, BizHawk)"""
    path: Project64Executable = Project64Executable(None)
    auto_start: bool = True

class SnapRomPath(settings.UserFilePath):
    """ Locate your Pokemon Snap ROM path """
    description = "Pokemon Snap ROM path"

class PokemonSnapSettings(settings.Group):
    """Various Pokemon Snap Settings"""
    rom_path: SnapRomPath = SnapRomPath(None)
    use_pj64: UseProject64 | bool = True
    emulator_settings: EmulatorSettings = EmulatorSettings()