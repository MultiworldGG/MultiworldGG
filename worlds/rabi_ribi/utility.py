"""
Utility used across the apworld
"""
import pkgutil, pkg_resources

rabi_ribi_base_id: int = 8350438193300

def get_rabi_ribi_base_id() -> int:
    return rabi_ribi_base_id

def load_text_file(path):
    data = pkgutil.get_data(__name__, path)
    if data is None:
        raise FileNotFoundError(f'{path!r} not found in {__name__}.')
    return data.decode()

def resource_listdir(path):
    return [f for f in pkg_resources.resource_listdir(__name__, path) if f != '']

def convert_existing_rando_name_to_ap_name(name):
    """
    Converts a name from the existing randomizer to AP.
    This converts from capitalized underscore seperation to Captialization with spaces.
    E.g. MY_ITEM_NAME -> My Item Name

    :string name: The name to convert
    """
    ap_name = name.split("_")
    ap_name = " ".join(word.capitalize() for word in ap_name)
    return ap_name

def convert_ap_name_to_existing_rando_name(name):
    """
    Converts a name from the existing randomizer to AP.
    This converts from capitalized underscore seperation to Captialization with spaces.
    E.g. My Item Name -> MY_ITEM_NAME

    :string name: The name to convert
    """
    existing_rando_name = name.split(" ")
    existing_rando_name = "_".join(existing_rando_name).upper()
    return existing_rando_name
