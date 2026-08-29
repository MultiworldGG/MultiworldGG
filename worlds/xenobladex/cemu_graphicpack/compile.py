from typing import Any
import requests
import os
import sys
import re
import itertools

# Set working directory to file directory
os.chdir(sys.path[0])

# Set mod name
try:
    with open("rules.txt", "r") as f:
        rules = f.read()
except Exception:
    raise Exception("No rules.txt file")
match = re.search(r"^\s*[nN]ame\s*=\s*[\'\"]?(.*?)[\'\"]?\s*$", rules, re.M)
if match is not None:
    modname = match.group(1)
else:
    raise Exception("Rules.txt file contains no name")
parameters = set(re.findall(r"(?<=^\$)\w*(?=\s)", rules, re.M))

# Compile all *.cpp files
for filename in (os.path.splitext(file)[0] for file in os.listdir() if file.endswith(".cpp")):

    # Read file
    try:
        with open(f"{filename}.cpp", "r") as f:
            data = f.read()
    except Exception:
        raise Exception(f"Unable to read from {filename}.cpp")

    # Aquire assembly from https://godbolt.org/
    url = "https://godbolt.org/api/compiler/ppcg1320/compile"
    res = requests.post(url=url, data=data, headers={"Accept": "application/json"})
    try:
        res.raise_for_status()
    except Exception:
        raise Exception(f"Assembly for {filename}.cpp failed with {res.status_code}")
    jres: Any = res.json()

    # Print errors and warnings
    if jres["stderr"]:
        print("\n".join(re.sub(r"(?<=^\033\[01m\033\[K<)source(?=>)", f"{filename}.cpp", line["text"])
                        for line in jres["stderr"]))
    if jres["code"] != 0:
        continue

    content = "\n".join(line["text"] for line in jres["asm"]) + "\n"

    # Fix assembly formatting
    # Replace spaces with tabs
    content = re.sub(r" {4,12}", "\t", content)

    # Replace .zero initializers
    def _generateInitializer(match: re.Match[str]) -> str:
        match match.group(1):
            case "1":
                return ".byte   0"
            case "2":
                return ".short  0"
            case "8":
                return ".double 0"
            case _:
                return ".int    0"
    content = re.sub(r"\.zero\s*(\d)", _generateInitializer, content)
    # Replace invalid Labels
    content = re.sub(r"[.](LC?[0-9]+)", f"_{filename}_\\1", content)
    # Remove global label
    content = re.sub(r"\t\.global .*\n", "", content)
    # Remove all function brackets
    content = re.sub(r"[(](?!r?[1-3]?[0-9]).*?[)]", "", content)
    # Add register prefix to all easy numbers
    content = re.sub(r"(?<=[ ,(])([1-3]?[0-9])(?=[),])", "r\\1", content)
    # Add register prefix to all complex numbers
    content = re.sub(r"(\t(?:(?!i)\w)*(?: .*,|\s))([1-3]?[0-9])\n", "\\1r\\2\n", content)
    # Remove prefix from crxor
    content = re.sub(r"crxor r([0-9]+),r([0-9]+),r([0-9]+)", "crxor \\1,\\2,\\3", content)
    # Restructure la instructions
    content = re.sub(r"la (r[1-3]?[0-9]),(.*)[(](r[1-3]?[0-9])[)]", "addi \\1,\\3,\\2", content)
    # Handle target out of range error for internal functions
    counter = itertools.count(1)

    def _generateAlternateCall(match: re.Match[str]) -> str:
        name = match.group(1)
        label = f"_after_{filename}_{next(counter)}{name}"
        return f"lis r12,{label}@ha\n\taddi r12,r12,{label}@l\n\tmtlr r12\n\tlis r12,{name}" \
               f"@ha\n\taddi r12,r12,{name}@l\n\tmtctr r12\n\tbctr\n{label}:"
    content = re.sub(r"bl (__.*)", _generateAlternateCall, content)
    # Change register to condition registers for cmpw/cmpwi/cmplw/cmplwi and beq/bne/blt/ble/bgt/bge
    content = re.sub(r"(cmpw|cmpwi|cmplw|cmplwi|beq|bne|blt|ble|bgt|bge) (r[0-7])", "\\1 c\\2", content)
    # Change unsupported offset for symbols specifically for lis->addi and lis->lwz
    r = r"(lis (r\d+),.*?)\+(\d+)(@.*\n)(\t(?:addi|lwz) r\d+,r\d+,.*?)\+\d+(@.*)"
    content = re.sub(r, "\\1\\4\taddi \\2,\\2,\\3\n\\5\\6", content)
    # Remove rlwinm, this could lead to errors, but i found no usage for this
    content = re.sub(r".*rlwinm .*[\n]", "", content)
    # Add support for import with changed namespaces
    content = re.sub(r"(bl.*)", lambda _: re.sub(r"::", ".", str(_.group(1))), content)

    # Add Parameters from rules.txt file
    for parameter in parameters:
        content = re.sub(rf"({parameter}:\n\t\.int\s+)0", f"\\1${parameter}", content)

    # Prepare packages
    r = r"^#ifdef (?P<name>.*?)\nmoduleMatches *= *(?P<ids>.*?)" \
        r" *,? *[#;] *(?P<versions>.*?)\n(?P<content>.*?)^#endif *\n"
    packages = [match.groupdict() for match in re.compile(r, re.MULTILINE | re.DOTALL).finditer(data)]

    # Add cemu package information
    modules = f'{", ".join(package["ids"] for package in packages)} #' \
              f' {", ".join(package["versions"] for package in packages)}'
    content = f"[{modname}_{filename}]\nmoduleMatches = {modules}\n.origin = codecave\n\n{content}\n\n"

    # Add version specific addresses for symbols
    for package in packages:
        content += f'[{modname}_{filename}_{package["name"]}]\nmoduleMatches = {package["ids"]} ' \
                   f'# {package["versions"]}\n{package["content"]}\n\n'

    # Create file
    try:
        with open(f"patch_{filename}.asm", "w") as f:
            f.write(content)
    except Exception:
        raise Exception(f"Unable to write to patch_{filename}.asm")
