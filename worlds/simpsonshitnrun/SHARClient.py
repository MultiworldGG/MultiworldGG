import os
import sys
import zipfile
import subprocess
import asyncio
import tkinter as tk
from tkinter import filedialog
import Utils
from NetUtils import ClientStatus
from CommonClient import CommonContext, server_loop, gui_enabled
import ctypes
from ctypes import wintypes
from pathlib import Path
import worlds
from . import SimpsonsHitNRunWorld

try:
    from . import settings, SimpsonsHitNRunOptions
except ImportError:
    import settings

class SHARContext(CommonContext):
    game = "Simpsons Hit and Run"

    def __init__(self):
        super().__init__()
        self._initialized = False

    async def initialize(self):
        import ctypes
        from ctypes import wintypes
        from pathlib import Path


        def get_documents_folder() -> Path:
            CSIDL_PERSONAL = 0x0005  # My Documents
            SHGFP_TYPE_CURRENT = 0

            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            result = ctypes.windll.shell32.SHGetFolderPathW(
                None,  # hwndOwner
                CSIDL_PERSONAL,  # folder CSIDL
                None,  # hToken
                SHGFP_TYPE_CURRENT,  # dwFlags
                buf  # pszPath
            )
            if result != 0:  # S_OK = 0
                raise OSError(f"SHGetFolderPathW failed with code {result}")
            return Path(buf.value)

        """Async-safe initialization: load host options, paths, and tools."""
        if self._initialized:
            return
        print("[SHARClient] Initializing SHARContext asynchronously...")

        # Load options from host.yaml
        opts = SimpsonsHitNRunWorld.settings
        documents_path = get_documents_folder()

        # Default extraction path
        default_extract = (
            documents_path
            / "My Games"
            / "Lucas' Simpsons Hit & Run Mod Launcher"
            / "Saved Games"
            / "APSHARRandomizer"
        )

        # Use host options if set, otherwise default
        self.EXTRACT_DIR = default_extract
        print(f"[SHARClient] Using extraction path: {self.EXTRACT_DIR}")
        self.EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

        # Optional auto-launch executable paths
        self.SHARRandomizerExe = opts.sharrandomizer
        self.LucasLauncherExe = opts.lucas_launcher
        print(f"[SHARClient] SHARRandomizerExe: {self.SHARRandomizerExe}")
        print(f"[SHARClient] LucasLauncherExe: {self.LucasLauncherExe}")

        self._initialized = True

    def safe_extract(self, z: zipfile.ZipFile, path: Path):
        print(f"[SHARClient] Extracting ZIP to {path}...")
        for member in z.namelist():
            if member.endswith("SHAR.ini"):  # Only extract SHAR.ini
                dest = path / member
                if not str(dest.resolve()).startswith(str(path.resolve())):
                    raise ValueError("Blocked ZIP path traversal attempt.")
                z.extract(member, path)
                print(f"[SHARClient] Extracted {member}")
        print(f"[SHARClient] Extraction complete.")

    async def handle_apshar(self, file_path: Path):
        print(f"[SHARClient] handle_apshar called with: {file_path}")
        try:
            with zipfile.ZipFile(file_path, "r") as z:
                self.safe_extract(z, self.EXTRACT_DIR)

            self.gui_message(f"Extracted SHAR.ini into: {self.EXTRACT_DIR}")

        except Exception as e:
            self.gui_message(f"Error extracting .apshar: {e}")
            print(f"[SHARClient] Exception during extraction: {e}")
            return

        self.launch_external_tools()

    def launch_file(self, path: Path):
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def launch_external_tools(self):
        print("[SHARClient] Attempting to launch external tools...")

        exe_path = Path(self.SHARRandomizerExe)
        if exe_path.exists() and exe_path.name.lower() == "sharrandomizerfrontend.exe":
            self.gui_message(f"Launching SHARRandomizerFrontend.exe...")
            print(f"[SHARClient] Launching SHARRandomizerFrontend.exe at {self.SHARRandomizerExe}")
            subprocess.Popen([self.SHARRandomizerExe], cwd=Path(self.SHARRandomizerExe).parent, creationflags=subprocess.CREATE_NEW_CONSOLE )
        else:
            msg = "SHARRandomizerFrontend.exe not configured or missing."
            self.gui_message(msg)
            print(f"[SHARClient] {msg}")

        exe_path = Path(self.LucasLauncherExe)
        if exe_path.exists() and exe_path.name.lower() == "lucas simpsons hit & run mod launcher.exe":
            self.gui_message(f"Launching Lucas Mod Launcher.exe...")
            print(f"[SHARClient] Launching Lucas Launcher.exe at {self.LucasLauncherExe}")
            subprocess.Popen([self.LucasLauncherExe, "-enabledmod", "Archipelago Randomizer", "-launch"], cwd=Path(self.LucasLauncherExe).parent)
        else:
            msg = "Lucas's Mod Launcher.exe not configured or missing."
            self.gui_message(msg)
            print(f"[SHARClient] {msg}")


    def gui_message(self, message: str):
        print(f"[SHARClient][GUI] {message}")

    async def start(self):
        await self.initialize()

        # Check for drag-and-drop / command-line .apshar argument
        if len(sys.argv) > 1:
            file_path = Path(sys.argv[1])
            print(f"[SHARClient] Opening .apshar from argument: {file_path}")
            await self.handle_apshar(file_path)
            return

        # Prompt user to select a .apshar if Tkinter is available
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="Select a .apshar patch",
                filetypes=[("APSHAR files", "*.apshar")],
            )
            if file_path:
                await self.handle_apshar(Path(file_path))
                return
            else:
                print("[SHARClient] No .apshar selected. Starting server loop instead.")
        except ImportError:
            print("[SHARClient] Tkinter not available; pass .apshar as command-line argument.")

        # Fallback to normal server loop
        await server_loop(self)

# ---------------- Run Client Helper ----------------
def run_client(ap_url: str = None):
    """Entry point for Archipelago client component."""
    async def runner():
        ctx = SHARContext()
        await ctx.initialize()
        if ap_url:
            await ctx.handle_apshar(Path(ap_url))
        else:
            await ctx.start()

    asyncio.run(runner())
