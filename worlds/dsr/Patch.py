from pathlib import Path

from Utils import messagebox
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components

PATCH_MD5 = "df10b4ec0fb03b922585318e8dce4664"
VANILLA_ASSET_MD5 = "d0f534a0c181055d1ac94ea1aae784ea"
PATCHED_ASSET_MD5 = "345668f031755f3f3b03a9fec7110e2f"

def check_hash(path: Path | str, hash: str) -> bool:
  from hashlib import md5

  with open(path, "rb") as f:
    file_hash = md5(f.read()).hexdigest()
  return file_hash == hash

def patch(*args: list[str]) -> None:
  from . import DSRWorld
  import shutil

  try:
    game_exe: str = DSRWorld.settings.exe_path
  except:
    messagebox("Invalid Game", "Selected file did not match known Dark Souls Remastered executable.")
    return

  asset_path = Path(game_exe).parent.joinpath('menu', 'menu_0.tpf.dcx')
  backup_path = Path(game_exe).parent.joinpath('menu', 'menu_0.tpf.dcx.apbak')

  if len(args) == 1:
    # Patching
    import bsdiff4

    patch_path = args[0]

    if not check_hash(patch_path, PATCH_MD5):
      messagebox("Invalid Patch", "Not a recognized patch file for Dark Souls Remastered.", True)
      return

    if check_hash(asset_path, PATCHED_ASSET_MD5):
      messagebox("Nothing to do", "The game has already been patched.")
      return

    if not check_hash(asset_path, VANILLA_ASSET_MD5):
      messagebox("Unable to patch", 
                 """
                 The assets had been modified by an external source.
                 
                 Patching is not possible.
                 Consider restoring the vanilla game files via 'Properties -> Installed Files -> Verify integrity of game files' on Steam.
                 """, True)
      return

    if not backup_path.exists() or not check_hash(backup_path, VANILLA_ASSET_MD5):
      shutil.copyfile(asset_path, backup_path)

    bsdiff4.file_patch_inplace(asset_path, patch_path)

    messagebox("Success", "Dark Souls Remastered has been patched succesfully!")
    
  else:
    # Reverting
    import os

    if check_hash(asset_path, VANILLA_ASSET_MD5):
      messagebox("Nothing to revert", "The game has not been patched yet.")
      return

    if not backup_path.exists() or not check_hash(backup_path, VANILLA_ASSET_MD5):
      messagebox("Unable to revert patch", 
                  """
                  The backup is not present and/or corrupted.
                  
                  Restore the vanilla game files via 'Properties -> Installed Files -> Verify integrity of game files' on Steam instead.
                  """, True)
      return
    
    shutil.copyfile(backup_path, asset_path)
    os.remove(backup_path)

    messagebox("Success", "The Dark Souls Remastered patch has been reverted.")


components.append(
    Component(
        "Revert DSR Patch",
        func=patch,
        game_name="Dark Souls Remastered",
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apdsr")
    )
)
