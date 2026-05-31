import io, re, json
import os
import pkgutil
import shutil
import subprocess
import tempfile
import zipfile
from functools import lru_cache

OOT_PLAYER_NAME_LENGTH = 8
OOT_PLAYER_NAME_PAD = 0xDF
OOT_PLAYER_NAME_CHARACTERS = {
    **{str(i): i for i in range(10)},
    **{chr(c): c + 0x6A for c in range(ord('A'), ord('Z') + 1)},
    **{chr(c): c + 0x64 for c in range(ord('a'), ord('z') + 1)},
    '.': 0xEA,
    '-': 0xE4,
    ' ': OOT_PLAYER_NAME_PAD,
}


def encode_oot_player_name(name: str, max_length: int = OOT_PLAYER_NAME_LENGTH) -> bytearray:
    encoded = bytearray()
    for c in name:
        value = OOT_PLAYER_NAME_CHARACTERS.get(c)
        if value is None:
            continue
        encoded.append(value)
        if len(encoded) >= max_length:
            break

    if not encoded:
        return encode_oot_player_name("Player", max_length)

    encoded.extend([OOT_PLAYER_NAME_PAD] * (max_length - len(encoded)))
    return encoded


def _is_apworld_archive(path):
    return path and path.lower().endswith(".apworld")


def _apworld_archive_path():
    archive = getattr(globals().get("__loader__"), "archive", None)
    if _is_apworld_archive(archive):
        return os.path.abspath(archive)

    module_path = os.path.abspath(__file__)
    while True:
        if _is_apworld_archive(module_path):
            return module_path
        parent = os.path.dirname(module_path)
        if parent == module_path:
            return None
        module_path = parent


_version_data = pkgutil.get_data(__name__, "archipelago.json")
if _version_data is None:
    raise FileNotFoundError("archipelago.json")
_version_info = json.loads(_version_data.decode('utf-8'))
__version__: str = _version_info['world_version']
__version_full__: str = _version_info['world_version_full']

def _restore_executable_mode(path):
    if os.path.basename(path).startswith(('Compress', 'Decompress')):
        try:
            os.chmod(path, 0o755) # nosec
        except OSError:
            pass


@lru_cache(maxsize=1)
def _data_root():
    apworld_path = _apworld_archive_path()
    if not apworld_path:
        return os.path.join(os.path.dirname(__file__), 'data')

    stat = os.stat(apworld_path)
    temp_root = os.path.join(
        tempfile.gettempdir(), f"oot_apworld_data_{__version__}_{stat.st_mtime_ns}_{stat.st_size}")
    data_root = os.path.join(temp_root, "data")
    marker_path = os.path.join(temp_root, ".extracted")
    if os.path.exists(marker_path) and os.path.isdir(data_root):
        return data_root

    os.makedirs(data_root, exist_ok=True)
    prefix = "oot/data/"
    data_root_abs = os.path.abspath(data_root)
    with zipfile.ZipFile(apworld_path, 'r') as apworld:
        for info in apworld.infolist():
            if info.is_dir() or not info.filename.startswith(prefix):
                continue
            relative_path = info.filename[len(prefix):]
            target_path = os.path.abspath(os.path.join(data_root, *relative_path.split('/')))
            if os.path.commonpath([data_root_abs, target_path]) != data_root_abs:
                raise RuntimeError(f"Unexpected path in OOT apworld: {info.filename}")

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with apworld.open(info, 'r') as source, open(target_path, 'wb') as target:
                shutil.copyfileobj(source, target)
            _restore_executable_mode(target_path)

    with open(marker_path, 'w', encoding='utf-8') as marker:
        marker.write(apworld_path)
    return data_root


def data_path(*args):
    return os.path.join(_data_root(), *args)


@lru_cache
def read_json(file_path):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos - 35:error.pos + 35] + "\n" + \
                        "                                   ^^\n")


# From the pyinstaller Wiki: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
# Create a set of arguments which make a ``subprocess.Popen`` (and
# variants) call work with or without Pyinstaller, ``--noconsole`` or
# not, on Windows and Linux. Typical use::
#   subprocess.call(['program_to_run', 'arg_1'], **subprocess_args())
def subprocess_args(include_stdout=True):
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env})
    return ret


def get_version_bytes(a):
    version_bytes = [0x00, 0x00, 0x00]
    if not a:
        return version_bytes
    sa = a.replace('v', '').replace(' ', '.').split('.')

    for i in range(0, 3):
        try:
            version_byte = int(sa[i])
        except ValueError:
            break
        version_bytes[i] = version_byte

    return version_bytes


def compare_version(a, b):
    if not a and not b:
        return 0
    elif a and not b:
        return 1
    elif not a and b:
        return -1

    sa = get_version_bytes(a)
    sb = get_version_bytes(b)

    for i in range(0, 3):
        if sa[i] > sb[i]:
            return 1
        if sa[i] < sb[i]:
            return -1
    return 0

# https://stackoverflow.com/a/23146126
def find_last(source_list, sought_element):
    for reverse_index, element in enumerate(reversed(source_list)):
        if element == sought_element:
            return len(source_list) - 1 - reverse_index
