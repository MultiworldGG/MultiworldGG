import json
import os

error_dlls_path = os.path.join(".","resources","app","meta","manifests","excluded_dlls.json")
if os.path.isfile(error_dlls_path):
    with open(error_dlls_path, "r") as error_dlls_file:
        error_dlls_json = json.load(error_dlls_file)
        if len(error_dlls_json) > 0 and error_dlls_json[0].strip() != "":
            print(error_dlls_json)
            # exit(1)
