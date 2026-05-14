import json
import os

if __name__ == "__main__":
    dir_name = os.path.dirname(__file__) + "../patching/asm"
    asm_files = []
    for filename in os.listdir(dir_name):
        if filename.endswith(".yaml"):
            asm_files.append(f"asm/{filename}")

    with open(dir_name + "/__init__.py", "w", encoding="utf-8") as f:
        f.write('ASM_FILES = ')
        f.write(json.dumps(asm_files, indent=4))