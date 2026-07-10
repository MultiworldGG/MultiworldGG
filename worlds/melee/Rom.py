import zipfile
from worlds.Files import APPlayerContainer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SSBMWorld

apworld_version = "2.0"

class MeleePlayerContainer(APPlayerContainer):
    game = "Super Smash Bros. Melee"
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".zip"

    def __init__(self, output_patch, output_file_path: str, player_name: str, player: int, patch_name,
        server: str = ""):
        self.output_patch = output_patch
        self.patch_name = patch_name
        super().__init__(output_file_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(f"{self.patch_name}.xml", self.output_patch)
        super().write_contents(opened_zipfile)


def apply_patch(world, basepatch, output):
    from jinja2 import Template
    template = Template(basepatch)
    if world.options.lottery_pool_mode:
        disable_class_upgrades = True
    else:
        disable_class_upgrades = False

    world_version_hex = apworld_version.encode("ascii").hex()
        
    result = template.render(
            PLAYER_NAME=world.player_name,
            VERSION_NUMBER=apworld_version,
            VERSION_NUM_ENCODED=world_version_hex,
            GAME_FILE_NAME=world.encoded_slot_name,
            SLOT_NUM=world.player,
            AUTH_ID=world.authentication_id,
            CSTICK_SMASH_SOLO=world.options.solo_cstick_smash,
            AUTO_L_CANCEL=world.options.automatic_l_cancel,
            DISABLE_TAP_JUMP=world.options.disable_tap_jump,
            TROPHYCLASS_IN_POOL=disable_class_upgrades)
    return result
    