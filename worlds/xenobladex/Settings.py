import settings


class XenobladeXSettings(settings.Group):
    class Executable(settings.UserFilePath):
        is_exe = True

    class CemuSettings(settings.UserFilePath):
        pass

    class CemuMods(settings.UserFolderPath):
        pass

    executable: Executable = Executable("Cemu")
    cemu_settings: CemuSettings = CemuSettings("settings.xml")
    cemu_mods: CemuMods = CemuMods("Mods")
