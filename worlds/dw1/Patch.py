import settings
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin


DW1_HASH = "8520edac0f7f1454f8a008ac5e599c1a"


class DW1Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Digimon World (USA) BIN image"""
        description = "Digimon World (USA) BIN file"
        copy_to = "Digimon World (USA).bin"
        md5s = [DW1_HASH]

    rom_file: RomFile = RomFile("Digimon World (USA).bin")


class DW1ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = DW1_HASH
    game = "Digimon World"
    patch_file_ending = ".apdw1"
    result_file_ending = ".bin"

    procedure = [
        ("apply_bsdiff4", ["dw1_base.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().dw1_settings.rom_file, "rb") as f:
            return f.read()
