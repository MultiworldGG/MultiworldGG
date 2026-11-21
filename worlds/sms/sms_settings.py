import settings

class EmulatorExecutable(settings.UserFilePath):
    """
    Emulator executable path. Automatically starts rom upon patching completion.
    If using Flatpak, specify the path here.
    """
    is_exe = True
    description = "The path for emulator executable. If using Flatpak specify this path instead."

class EmulatorAdditionalArguments(list[str]):
    """ Additional arugments to be passed in when auto starting emulator. """
    args = []

class EmulatorSettings(settings.Group):
    path: EmulatorExecutable = EmulatorExecutable()
    additional_args: EmulatorAdditionalArguments = EmulatorAdditionalArguments([])
    auto_start: bool = True

class SuperMarioSunshineSettings(settings.Group):
    class ISOFile(settings.UserFilePath):
        description = "Super Mario Sunshine (USA) NTSC-U ISO File"
        copy_to = None

    class DolphinProcessName(str):
        """The name of the Dolphin process to connect to. Leave blank for system default."""

    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_settings: EmulatorSettings = EmulatorSettings()
    dolphin_process_name: DolphinProcessName = ""