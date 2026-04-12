import settings
import yaml

class EmulatorExecutable(settings.UserFilePath):
    """
    Emulator executable path. Automatically starts rom upon patching completion.
    If using Flatpak, specify the path here.
    """
    is_exe = True
    description = "The path for emulator executable. If using Flatpak, specify this path instead."

# Not a list[str] as apparently yaml cannot construct it or know how to infer it...
class EmulatorAdditionalArguments(list):
    """ Additional arugments to be passed in when auto starting emulator."""
    pass

class EmulatorSettings(settings.Group):
    """Various Emulator specific settings (such as Dolphin)"""
    path: EmulatorExecutable = EmulatorExecutable()
    additional_args: EmulatorAdditionalArguments = EmulatorAdditionalArguments()
    auto_start: bool = True

class ISOFile(settings.UserFilePath):
    """ Locate your Luigi's Mansion ISO """
    description = "Luigi's Mansion (NTSC-U) ISO"
    copy_to = None
    md5s = ["6e3d9ae0ed2fbd2f77fa1ca09a60c494"]

class DolphinProcessName(str):
    """The name of the Dolphin process to connect to. Leave blank for system default."""
    pass

class LuigisMansionSettings(settings.Group):
    """Various Luigi Mansion Settings"""
    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_settings: EmulatorSettings = EmulatorSettings()
    dolphin_process_name: DolphinProcessName = DolphinProcessName("")