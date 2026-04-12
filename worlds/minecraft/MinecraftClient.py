import argparse
from base64 import b64encode, b64decode
import zipfile
import json
import os
import sys
import re
import shutil
from subprocess import Popen
from time import strftime
import logging

import requests
import subprocess

import Utils
from Utils import is_windows
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components
from settings import get_settings


# 1 or more digits followed by m or g, then optional b
max_heap_re = re.compile(r"^\d+[mMgG][bB]?$")


def try_auto_launch_minecraft():
    """
    Launch Minecraft using the 'mc_launch' host.yaml setting if provided.
    """
    settings = get_settings()
    mc_settings = settings.minecraft_options

    mc_launch = mc_settings.mc_launch

    if not mc_launch:
        return

    # Pass the entire command as a string to Popen with shell=True
    try:
        print(f"Executing: {mc_launch}")
        subprocess.Popen(mc_launch, shell=True)
        print(f"[Minecraft Client] Auto-launched Minecraft: {mc_launch}")
    except Exception as e:
        print(f"[Minecraft Client] Failed to auto-launch Minecraft: {e}")

def prompt_yes_no(prompt):
    yes_inputs = {'yes', 'ye', 'y'}
    no_inputs = {'no', 'n'}
    while True:
        choice = input(prompt + " [y/n] ").lower()
        if choice in yes_inputs:
            return True
        elif choice in no_inputs:
            return False
        else:
            print('Please respond with "y" or "n".')


def show_java_prompt_simple(java_version):
    """Show Java installation prompt using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        result = messagebox.askyesno(
            "Java Required",
            f"Java {java_version} was not found on your system.\n\n"
            "To continue, you need to install Java.\n\n"
            "1. Click 'Yes' to proceed with install\n"
            "2. Or click 'No' to cancel setup"
        )

        root.destroy()
        return result

    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"Java {java_version} not found. Please install Java from https://adoptium.net/")
        return prompt_yes_no("Download and install Java now?")


def show_forge_prompt_simple(forge_version):
    """Show Forge installation prompt using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        result = messagebox.askyesno(
            "Forge Installation Required",
            f"Minecraft Forge {forge_version} was not found on your system.\n\n"
            "To continue, you need to install Forge.\n\n"
            "1. Click 'Yes' to continue with the install.\n"
            "2. Or click 'No' to cancel setup"
        )

        root.destroy()
        return result

    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"Forge {forge_version} not found.")
        return prompt_yes_no(f"Download and install forge version {forge_version} now?")


def show_yes_no_simple(title, message):
    """Show a simple yes/no dialog using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        result = messagebox.askyesno(title, message)

        root.destroy()
        return result

    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"{title}: {message}")
        return prompt_yes_no("Continue?")


def show_progress_dialog(title, message):
    """Show a progress dialog with a message"""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Show info dialog (non-blocking)
        messagebox.showinfo(title, message)

        root.destroy()

    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"{title}: {message}")


class ProgressWindow:
    """A tkinter window that shows installation progress with live console output"""
    def __init__(self, title, message, allow_close=False):
        self.tk = None
        self.root = None
        self.console = None
        self.active = False
        self.allow_close = allow_close

        try:
            import tkinter as tk
            from tkinter import scrolledtext

            self.tk = tk

            self.root = tk.Tk()
            self.root.title(title)
            self.root.geometry("600x400")

            # Make window stay on top initially
            self.root.attributes('-topmost', True)
            # After a moment, remove topmost so it doesn't cover Minecraft
            self.root.after(3000, lambda: self.root.attributes('-topmost', False))

            # Message label at top
            self.label = tk.Label(self.root, text=message, font=('TkDefaultFont', 10, 'bold'), pady=10, wraplength=580)
            self.label.pack(fill=tk.X)

            # Scrolled text widget for console output
            self.console = scrolledtext.ScrolledText(
                self.root,
                wrap=tk.WORD,
                width=90,
                height=25,
                bg='black',
                fg="#C300FF",
                font=('monospace', 10)
            )
            self.console.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            self.console.config(state=tk.DISABLED)  # Make read-only initially

            self.active = True
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        except ImportError:
            self.root = None
            self.active = False
            print(f"{title}: {message}")

    def append_text(self, text):
        """Append text to the console output"""
        if self.root and self.active and self.console and self.tk:
            self.console.config(state=self.tk.NORMAL)
            self.console.insert(self.tk.END, text + '\n')
            self.console.see(self.tk.END)  # Auto-scroll to bottom
            self.console.config(state=self.tk.DISABLED)
            self.root.update()  # Force update the UI
        else:
            print(text)

    def on_close(self):
        """Handle window close button"""
        if self.allow_close:
            self.close()
        else:
            pass

    def close(self):
        """Close the progress window"""
        if self.root and self.active:
            self.active = False
            self.root.destroy()

    def update(self):
        """Update the window to process events"""
        if self.root and self.active:
            self.root.update()


class ServerConsoleWindow:
    """A tkinter window that shows the Minecraft server console with player instructions"""
    def __init__(self):
        self.tk = None
        self.root = None
        self.console = None
        self.active = False
        self.server_process = None

        try:
            import tkinter as tk
            from tkinter import scrolledtext

            self.tk = tk

            self.root = tk.Tk()
            self.root.title("Minecraft Server Console")
            self.root.geometry("700x500")

            instructions = (
                "Minecraft Server is starting!\n\n"
                "1. Open Minecraft Java Edition (v1.20.4)\n"
                "2. Once server is ready, connect to 'localhost' in Multiplayer\n"
                "3. In-game, enter in chat: /connect multiworld.gg room_port\n"
                "4. Chat /start when ready\n\n"
                "Don't close this window until you're done playing!\n"
                "The server will stop once you close this window."
            )

            self.label = tk.Label(
                self.root,
                text=instructions,
                pady=10,
                wraplength=680,
                justify=tk.LEFT,
                bg='#f0f0f0',
                relief=tk.RIDGE,
                borderwidth=2
            )
            self.label.pack(fill=tk.X, padx=5, pady=5)

            # Add console label
            console_label = tk.Label(self.root, text="Server Console Output:", font=('TkDefaultFont', 9, 'bold'))
            console_label.pack(anchor=tk.W, padx=10)

            # Scrolled text widget for console output
            self.console = scrolledtext.ScrolledText(
                self.root,
                wrap=tk.WORD,
                width=90,
                height=25,
                bg='black',
                fg='#C300FF',
                font=('monospace', 10)
            )
            self.console.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))
            self.console.config(state=tk.DISABLED)  # Make read-only initially

            self.active = True
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        except ImportError:
            self.root = None
            self.active = False
            print("Minecraft Server Console - Press Ctrl+C to stop the server")

    def append_text(self, text):
        """Append text to the console output"""
        if self.root and self.active and self.console and self.tk:
            try:
                self.console.config(state=self.tk.NORMAL)
                self.console.insert(self.tk.END, text + '\n')
                self.console.see(self.tk.END)  # Auto-scroll to bottom
                self.console.config(state=self.tk.DISABLED)
                self.root.update()  # Force update the UI
            except:
                pass  # Window might be closing
        else:
            print(text)

    def on_close(self):
        """Handle window close button"""
        if self.tk and self.active:
            result = self.tk.messagebox.askyesno(
                "Stop Server?",
                "Are you sure you want to stop the Minecraft server?\n\nThis will end your session."
            )
            if result:
                self.close()

    def close(self):
        """Close the server console window"""
        if self.root and self.active:
            self.active = False
            if self.server_process and self.server_process.poll() is None:
                # Terminate the server process
                self.server_process.terminate()
                try:
                    self.server_process.wait(timeout=5)
                except:
                    self.server_process.kill()
            self.root.destroy()

    def set_server_process(self, process):
        """Set the server process so we can terminate it on close"""
        self.server_process = process

    def update(self):
        """Update the window to process events"""
        if self.root and self.active:
            try:
                self.root.update()
            except:
                pass  # Window might be closing

    def is_active(self):
        """Check if the window is still active"""
        return self.active


def find_ap_randomizer_jar(forge_dir):
    """Create mods folder if needed; find AP randomizer jar; return None if not found."""
    mods_dir = os.path.join(forge_dir, 'mods')
    if os.path.isdir(mods_dir):
        for entry in os.scandir(mods_dir):
            if entry.name.startswith("aprandomizer") and entry.name.endswith(".jar"):
                logging.info(f"Found AP randomizer mod: {entry.name}")
                return entry.name
        return None
    else:
        os.mkdir(mods_dir)
        logging.info(f"Created mods folder in {forge_dir}")
        return None


def convert_apmc_to_base64(input_path: str, output_path: str) -> None:
    """
    Converts an APMC file into a base64-encoded JSON text file.
    Supports BOTH:
    - New-format ZIP-based .apmc (with data.json)
    - Old-format base64 JSON .apmc (already encoded)
    """

    # Case 1: NEW FORMAT (ZIP PROCEDURE PATCH)
    if zipfile.is_zipfile(input_path):
        with zipfile.ZipFile(input_path, 'r') as zf:
            if "data.json" not in zf.namelist():
                raise ValueError("ZIP .apmc missing data.json!")

            raw_json = zf.read("data.json").decode("utf-8")
            encoded = b64encode(raw_json.encode("utf-8")).decode("utf-8")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encoded)

        print(f"[APMC] Converted ZIP {input_path} → base64 JSON {output_path}")
        return

    # Case 2: OLD FORMAT (BASE64 JSON)
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Validate it's actually base64
        try:
            decoded = b64decode(content).decode('utf-8')
            json.loads(decoded)  # ensure it is valid JSON
        except Exception as e:
            raise ValueError(f"Invalid old-format .apmc file: {input_path}") from e

        # Just copy it — it’s already base64
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[APMC] Passed through old-format base64 file: {input_path} → {output_path}")
        return


def replace_apmc_files(forge_dir: str, zip_apmc_path: str) -> None:
    """
    Takes the AP-generated ZIP-style .apmc file and converts it into
    a Forge-compatible base64 .apmc file inside the server directory.
    """

    # Where Forge expects the final base64 file
    target_apdata = os.path.join(forge_dir, "APData")
    os.makedirs(target_apdata, exist_ok=True)

    # Remove any existing .apmc files (keep folder clean)
    for entry in os.scandir(target_apdata):
        if entry.name.endswith(".apmc"):
            os.remove(entry.path)
            print(f"Removed old patch: {entry.name}")

    # Forge expects the same name but base64 contents
    file_name = os.path.basename(zip_apmc_path)
    base64_apmc_path = os.path.join(target_apdata, file_name)

    # Convert ZIP → base64 JSON text
    convert_apmc_to_base64(zip_apmc_path, base64_apmc_path)

    print(f"Converted {zip_apmc_path} → Forge base64 {base64_apmc_path}")


def read_apmc_file(apmc_path: str):
    """
    Reads either:
    - NEW FORMAT: ZIP containing data.json
    - OLD FORMAT: base64 JSON text
    """
    if not os.path.isfile(apmc_path):
        raise FileNotFoundError(f"APMC file not found: {apmc_path}")

    # NEW format: ZIP procedure patch
    if zipfile.is_zipfile(apmc_path):
        with zipfile.ZipFile(apmc_path, 'r') as zf:
            if "data.json" not in zf.namelist():
                raise ValueError("APMC ZIP missing data.json")
            raw = zf.read("data.json").decode("utf-8")
            return json.loads(raw)

    # OLD format: base64 JSON text
    with open(apmc_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    try:
        decoded = b64decode(content).decode("utf-8")
        return json.loads(decoded)
    except Exception:
        raise ValueError("APMC file is neither ZIP nor valid base64 JSON")


def update_mod(forge_dir, url: str):
    """Check mod version, download new mod from GitHub releases page if needed. """
    ap_randomizer = find_ap_randomizer_jar(forge_dir)
    os.path.basename(url)
    if ap_randomizer is not None:
        logging.info(f"Your current mod is {ap_randomizer}.")
    else:
        logging.info(f"You do not have the AP randomizer mod installed.")

    if ap_randomizer != os.path.basename(url):
        logging.info(f"A new release of the Minecraft AP randomizer mod was found: "
                     f"{os.path.basename(url)}")
        if show_yes_no_simple("Mod Update Available", f"A new release of the Minecraft AP randomizer mod was found:\n{os.path.basename(url)}\n\nWould you like to update?"):
            old_ap_mod = os.path.join(forge_dir, 'mods', ap_randomizer) if ap_randomizer is not None else None
            new_ap_mod = os.path.join(forge_dir, 'mods', os.path.basename(url))
            logging.info("Downloading AP randomizer mod. This may take a moment...")
            apmod_resp = requests.get(url)
            if apmod_resp.status_code == 200:
                with open(new_ap_mod, 'wb') as f:
                    f.write(apmod_resp.content)
                    logging.info(f"Wrote new mod file to {new_ap_mod}")
                if old_ap_mod is not None:
                    os.remove(old_ap_mod)
                    logging.info(f"Removed old mod file from {old_ap_mod}")
            else:
                logging.error(f"Error retrieving the randomizer mod (status code {apmod_resp.status_code}).")
                logging.error(f"Please report this issue on the Unofficial AP Discord server.")
                sys.exit(1)


def check_eula(forge_dir):
    """Check if the EULA is agreed to, and prompt the user to read and agree if necessary."""
    eula_path = os.path.join(forge_dir, "eula.txt")
    if not os.path.isfile(eula_path):
        # Create eula.txt
        with open(eula_path, 'w') as f:
            f.write("#By changing the setting below to TRUE you are indicating your agreement to the Minecraft EULA (https://www.minecraft.net/en-us/eula).\n")
            f.write(f"#{strftime('%a %b %d %X %Z %Y')}\n")
            f.write("eula=false\n")
    with open(eula_path, 'r+') as f:
        text = f.read()
        if 'false' in text:
            # Prompt user to agree to the EULA
            logging.info("You need to agree to the Minecraft EULA in order to run the server.")
            logging.info("The EULA can be found at https://www.minecraft.net/en-us/eula")
            if show_yes_no_simple("EULA Agreement", "Do you agree to the Minecraft EULA?\n\nBy clicking 'Yes', you agree to the terms."):
                f.seek(0)
                f.write(text.replace('eula=false', 'eula=true'))
                f.truncate()
                logging.info(f"Set {eula_path} to true")
            else:
                logging.error("EULA not agreed to. Cannot continue.")
                sys.exit(0)


def find_jdk_dir(version: str) -> str | None:
    """get the specified versions jdk directory"""
    for entry in os.listdir():
        if os.path.isdir(entry) and entry.startswith(f"jdk{version}"):
            return os.path.abspath(entry)


def find_jdk(version: str) -> str:
    """get the java exe location"""
    if is_windows:
        jdk = find_jdk_dir(version)
        if jdk:
            jdk_exe = os.path.join(jdk, "bin", "java.exe")
            if os.path.isfile(jdk_exe):
                return jdk_exe
        return "java"  # fallback
    else:
        settings = get_settings()
        java_cmd = settings.minecraft_options.java or "java"
        jdk_exe = shutil.which(java_cmd)
        if not jdk_exe:
            raise Exception("Could not find Java. Is Java installed on the system?")
        return jdk_exe


def download_java(java: str):
    """Download Corretto (Amazon JDK)"""

    jdk = find_jdk_dir(java)
    if jdk is not None:
        print(f"Removing old JDK...")
        from shutil import rmtree
        rmtree(jdk)

    print(f"Downloading Java...")

    # Create progress window
    progress = ProgressWindow("Java Installation", "Downloading and extracting Java...\nThis may take several minutes.")

    jdk_url = f"https://corretto.aws/downloads/latest/amazon-corretto-{java}-x64-windows-jdk.zip"
    progress.append_text(f"Downloading Java {java} from AWS Corretto...")
    progress.append_text(f"URL: {jdk_url}")

    resp = requests.get(jdk_url)
    if resp.status_code == 200:  # OK
        progress.append_text(f"Download complete! ({len(resp.content) // (1024*1024)} MB)")
        progress.append_text("Extracting Java files...")

        import zipfile
        from io import BytesIO

        # Show progress during extraction
        with zipfile.ZipFile(BytesIO(resp.content)) as zf:
            total_files = len(zf.namelist())
            progress.append_text(f"Found {total_files} files to extract...")

            for i, file_info in enumerate(zf.infolist(), 1):
                if i % 100 == 0 or i == total_files:  # Show progress every 100 files
                    progress.append_text(f"Extracting... {i}/{total_files} files ({(i/total_files)*100:.1f}%)")
                zf.extract(file_info)

        progress.append_text("Java extraction completed successfully!")
        progress.append_text("\nYou can close this window.")
        print("Java extraction completed!")

        # Keep window open for a moment so user can see completion
        import time
        time.sleep(2)
        progress.close()
    else:
        progress.append_text(f"ERROR: Download failed with status code {resp.status_code}")
        progress.close()
        print(f"Error downloading Java (status code {resp.status_code}).")
        print(f"If this was not expected, please report this issue on the Unofficial AP Discord server.")
        if not show_yes_no_simple("Download Error", f"Error downloading Java (status code {resp.status_code}).\n\nContinue anyways?"):
            sys.exit(0)


def install_forge(directory, forge_version, java_version):
    """download and install forge"""

    java_exe = find_jdk(java_version)
    if java_exe is not None:
        print(f"Downloading Forge {forge_version}...")

        # Create progress window
        progress = ProgressWindow("Forge Installation", "Installing Minecraft Forge...\nThis may take several minutes.")

        forge_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forge_version}/forge-{forge_version}-installer.jar"
        progress.append_text(f"Downloading Forge {forge_version}...")
        progress.append_text(f"URL: {forge_url}")

        resp = requests.get(forge_url)
        if resp.status_code == 200:  # OK
            forge_install_jar = os.path.join(directory, "forge_install.jar")
            if not os.path.exists(directory):
                os.mkdir(directory)
            with open(forge_install_jar, 'wb') as f:
                f.write(resp.content)

            progress.append_text(f"Download complete! ({len(resp.content) // (1024*1024)} MB)")
            progress.append_text("Running Forge installer...")
            progress.append_text("Please wait while Forge downloads and installs all required files...")
            progress.append_text("")

            # Run the installer with progress indication
            install_process = subprocess.Popen(
                [java_exe, "-jar", forge_install_jar, "--installServer", directory],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Show ALL installer output in the progress window
            while True:
                output = install_process.stdout.readline()
                if output == '' and install_process.poll() is not None:
                    break
                if output:
                    progress.append_text(output.strip())
                    if any(keyword in output.lower() for keyword in ['downloading', 'installing', 'extracting', 'copying', 'creating', 'error', 'failed']):
                        print(f"Forge installer: {output.strip()}")

            return_code = install_process.wait()
            progress.append_text("")
            if return_code == 0:
                progress.append_text("Forge installation completed successfully!")
                print("Forge installation completed successfully!")
            else:
                progress.append_text(f"### Forge installation exited with return code: {return_code}")
                print(f"Forge installation exited with return code: {return_code}")

            progress.append_text("\nYou can close this window.")

            # Keep window open for a moment so user can see completion
            import time
            time.sleep(2)
            progress.close()

            # Clean up installer
            os.remove(forge_install_jar)


def run_forge_server(forge_dir: str, java_version: str, heap_arg: str, forge_version) -> Popen:
    """Run the Forge server."""

    java_exe = find_jdk(java_version)
    if not os.path.isfile(java_exe):
        java_exe = "java"  # try to fall back on java in the PATH

    heap_arg = max_heap_re.match(heap_arg).group()
    if heap_arg[-1] in ['b', 'B']:
        heap_arg = heap_arg[:-1]
    heap_arg = "-Xmx" + heap_arg

    os_args = "win_args.txt" if is_windows else "unix_args.txt"
    args_file = os.path.join(forge_dir, "libraries", "net", "minecraftforge", "forge", forge_version, os_args)
    forge_args = []
    with open(args_file) as argfile:
        for line in argfile:
            forge_args.extend(line.strip().split(" "))

    args = [java_exe, heap_arg, *forge_args, "-nogui"]
    logging.info(f"Running Forge server: {args}")
    os.chdir(forge_dir)
    # Pipe stdout and stderr so we can display it in the console window
    return Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)


def get_minecraft_versions(version, release_channel="release"):
    version_file_endpoint = "https://raw.githubusercontent.com/cjmang/Minecraft_AP_Randomizer/refs/heads/master/versions/minecraft_versions.json"
    resp = requests.get(version_file_endpoint)
    local = False
    if resp.status_code == 200:  # OK
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            logging.warning(f"Unable to fetch version update file, using local version. (status code {resp.status_code}).")
            local = True
    else:
        logging.warning(f"Unable to fetch version update file, using local version. (status code {resp.status_code}).")
        local = True

    if local:
        with open(Utils.user_path("minecraft_versions.json"), 'r') as f:
            data = json.load(f)
    else:
        with open(Utils.user_path("minecraft_versions.json"), 'w') as f:
            json.dump(data, f)

    try:
        if version:
            return next(filter(lambda entry: entry["version"] == version, data[release_channel]))
        else:
            return resp.json()[release_channel][0]
    except (StopIteration, KeyError):
        logging.error(f"No compatible mod version found for client version {version} on \"{release_channel}\" channel.")
        if release_channel != "release":
            logging.error("Consider switching \"release_channel\" to \"release\" in your Host.yaml file")
        else:
            logging.error("No suitable mod found on the \"release\" channel. Please Contact us on discord to report this error.")
        sys.exit(0)


def is_correct_forge(forge_dir, forge_version) -> bool:
    if os.path.isdir(os.path.join(forge_dir, "libraries", "net", "minecraftforge", "forge", forge_version)):
        return True
    return False

def add_to_launcher_components():
    component = Component(
        "Minecraft Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apmc"),
        cli=True
    )
    components.append(component)


def run_client(*args):
    Utils.init_logging("MinecraftClient")
    parser = argparse.ArgumentParser()
    parser.add_argument("apmc_file", default=None, nargs='?', help="Path to an Archipelago Minecraft data file (.apmc)")
    parser.add_argument('--install', '-i', dest='install', default=False, action='store_true',
                        help="Download and install Java and the Forge server. Does not launch the client afterwards.")
    parser.add_argument('--release_channel', '-r', dest="channel", type=str, action='store',
                        help="Specify release channel to use.")
    parser.add_argument('--java', '-j', metavar='17', dest='java', type=str, default=False, action='store',
                        help="specify java version.")
    parser.add_argument('--forge', '-f', metavar='1.18.2-40.1.0', dest='forge', type=str, default=False, action='store',
                        help="specify forge version. (Minecraft Version-Forge Version)")
    parser.add_argument('--version', '-v', metavar='9', dest='data_version', type=int, action='store',
                        help="specify Mod data version to download.")

    args = parser.parse_args(args)
    apmc_file = os.path.abspath(args.apmc_file) if args.apmc_file else None

    # Change to executable's working directory
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

    settings = get_settings()
    mc_settings = settings.minecraft_options
    forge_dir = os.path.expanduser(str(mc_settings.forge_directory))
    max_heap  = mc_settings.max_heap_size

    channel = args.channel or mc_settings.release_channel

    apmc_data = None
    data_version = args.data_version or None

    if apmc_file is None and not args.install:
        apmc_file = Utils.open_filename('Select APMC file', (('APMC File', ('.apmc',)),))

    if apmc_file is not None and data_version is None:
        apmc_data = read_apmc_file(apmc_file)
        data_version = apmc_data.get('client_version', '')

    versions = get_minecraft_versions(data_version, channel)

    forge_version = args.forge or versions["forge"]
    java_version  = args.java or versions["java"]
    mod_url       = versions["url"]
    java_dir      = find_jdk_dir(java_version)

    if args.install:
        if is_windows:
            print("Installing Java")
            download_java(java_version)
        if not is_correct_forge(forge_dir, forge_version):
            print("Installing Minecraft Forge")
            install_forge(forge_dir, forge_version, java_version)
        else:
            print("Correct Forge version already found, skipping install.")
        sys.exit(0)

    if apmc_data is None:
        raise FileNotFoundError(f"APMC file does not exist or is inaccessible at the given location ({apmc_file})")

    if is_windows:
        if java_dir is None or not os.path.isdir(java_dir):
            if show_java_prompt_simple(java_version):
                download_java(java_version)
                java_dir = find_jdk_dir(java_version)
            if java_dir is None or not os.path.isdir(java_dir):
                raise NotADirectoryError(f"Path {java_dir} does not exist or could not be accessed.")

    if not is_correct_forge(forge_dir, forge_version):
        if show_forge_prompt_simple(forge_version):
            install_forge(forge_dir, forge_version, java_version)
        if not os.path.isdir(forge_dir):
            raise NotADirectoryError(f"Path {forge_dir} does not exist or could not be accessed.")

    if not max_heap_re.match(max_heap):
        raise Exception(f"Max heap size {max_heap} in incorrect format. Use a number followed by M or G, e.g. 512M or 2G.")

    update_mod(forge_dir, mod_url)
    replace_apmc_files(forge_dir, apmc_file)
    check_eula(forge_dir)

    # Create server console window
    console = ServerConsoleWindow()
    console.append_text("Starting Minecraft Forge server...")
    console.append_text(f"Server directory: {forge_dir}")
    console.append_text("")

    # Start the server
    server_process = run_forge_server(forge_dir, java_version, max_heap, forge_version)
    console.set_server_process(server_process)

    # Stream server output to console window
    server_ready = False
    minecraft_launched = False

    import threading
    import queue

    # Create a queue for server output
    output_queue = queue.Queue()

    def read_output(process, queue):
        """Read server output in a separate thread"""
        try:
            for line in iter(process.stdout.readline, ''):
                if line:
                    queue.put(line.rstrip())
        except:
            pass

    # Start thread to read server output
    output_thread = threading.Thread(target=read_output, args=(server_process, output_queue), daemon=True)
    output_thread.start()

    # Process server output and update console
    while console.is_active() and (server_process.poll() is None or not output_queue.empty()):
        try:
            # Get output from queue with timeout
            line = output_queue.get(timeout=0.1)

            # Display in console window
            console.append_text(line)

            # Check if server is ready
            if not server_ready and "Done (" in line and ")! For help, type \"help\"" in line:
                server_ready = True
                console.append_text("")
                console.append_text("#" * 20)
                console.append_text("SERVER IS READY!")
                console.append_text("#" * 20)
                console.append_text("")

                # Auto-launch Minecraft after server is ready
                if not minecraft_launched:
                    minecraft_launched = True
                    try_auto_launch_minecraft()

        except queue.Empty:
            # No output available, just update the window
            console.update()
            continue
        except:
            # Window might be closing
            break

    # Clean up
    if server_process.poll() is None:
        console.append_text("")
        console.append_text("Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
            console.append_text("Server stopped.")
        except:
            server_process.kill()
            console.append_text("Server forcefully terminated.")

    console.close()
