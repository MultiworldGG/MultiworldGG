from typing import Any
import requests
import os
import sys
import re
import itertools

# Set working directory to file directory
os.chdir(sys.path[0])

modnames: dict[str, str] = {}
parameters: dict[str, set[str]] = {}

# Set mod name
for filename in (os.path.splitext(os.path.join(root, file))[0]  # noqa: C901
                 for root, _, files in os.walk(".")
                 for file in files if file.endswith("rules.txt")):
    dirname = os.path.dirname(filename)
    try:
        with open(f"{filename}.txt", "r") as f:
            rules = f.read()
    except Exception:
        raise Exception("No rules.txt file")
    match = re.search(r"^\s*[nN]ame\s*=\s*[\'\"]?(.*?)[\'\"]?\s*$", rules, re.M)
    if match is not None:
        modnames[dirname] = match.group(1)
    else:
        raise Exception("Rules.txt file contains no name")
    parameters[dirname] = set(re.findall(r"(?<=^\$)\w*(?=\s)", rules, re.M))

# Compile all *.cpp files, including those in subdirectories
for filename in (os.path.splitext(os.path.join(root, file))[0]  # noqa: C901
                 for root, _, files in os.walk(".")
                 for file in files if file.endswith(".cpp")):

    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)

    # Read file
    try:
        with open(f"{filename}.cpp", "r") as f:
            data = f.read()
    except Exception:
        raise Exception(f"Unable to read from {filename}.cpp")

    # Aquire assembly from https://godbolt.org/
    url = "https://godbolt.org/api/compiler/ppcg1320/compile"
    res = requests.post(url=url, json={"source": data}, headers={"Accept": "application/json"})
    try:
        res.raise_for_status()
    except Exception:
        raise Exception(f"Assembly for {filename}.cpp failed with {res.status_code}")
    jres: Any = res.json()

    # Print errors and warnings
    if jres["stderr"]:
        print("\n".join(re.sub(r"(?<=^\033\[01m\033\[K<)source(?=>)", f"{basename}.cpp", line["text"])
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
    content = re.sub(r"[.](LC?[0-9]+)", f"_{basename}_\\1", content)
    # Remove global label
    content = re.sub(r"\t\.global .*\n", "", content)
    # Remove all function brackets
    content = re.sub(r"[(](?!r?[1-3]?[0-9]).*?[)]", "", content)
    # Add register prefix to all easy numbers
    content = re.sub(r"(?<=[ ,(])([1-3]?[0-9])(?=[),])", "r\\1", content)
    # Add register prefix to all complex numbers
    content = re.sub(r"(\t(?:(?!i)\w)*(?: .*,|\s))([1-3]?[0-9])\n", "\\1r\\2\n", content)
    # Add register for divs
    content = re.sub(r"divw (r[0-9]+),(r[0-9]+),([0-9]+)", "divw \\1,\\2,r\\3", content)
    # Remove prefix from crxor
    content = re.sub(r"crxor r([0-9]+),r([0-9]+),r([0-9]+)", "crxor cr\\1,cr\\2,cr\\3", content)
    # Remove prefix from rlwinm
    content = re.sub(r"rlwinm (r[0-9]+),(r[0-9]+),r([0-9]+),r([0-9]+),([0-9]+)", "rlwinm \\1,\\2,\\3,\\4,\\5", content)
    # Fix simplified syntax most common ones
    content = re.sub(r"rlwinm (r[0-9]+),(r[0-9]+),r([0-9]+),0x[fF]{2}\n", "rlwinm \\1,\\2,\\3,24,31\n", content)
    content = re.sub(r"rlwinm (r[0-9]+),(r[0-9]+),r([0-9]+),0x[fF]{4}\n", "rlwinm \\1,\\2,\\3,16,31\n", content)
    # Restructure la instructions
    content = re.sub(r"la (r[1-3]?[0-9]),(.*)[(](r[1-3]?[0-9])[)]", "addi \\1,\\3,\\2", content)
    # Handle target out of range error for internal functions
    counter = itertools.count(1)

    def _generateAlternateCall(match: re.Match[str]) -> str:
        name = match.group(1)
        label = f"_after_{basename}_{next(counter)}{name}"
        return f"lis r12,{label}@ha\n\taddi r12,r12,{label}@l\n\tmtlr r12\n\tlis r12,{name}" \
               f"@ha\n\taddi r12,r12,{name}@l\n\tmtctr r12\n\tbctr\n{label}:"
    content = re.sub(r"bl (__.*)", _generateAlternateCall, content)
    # Change register to condition registers for cmpw/cmpwi/cmplw/cmplwi and beq/bne/blt/ble/bgt/bge
    content = re.sub(r"(cmpw|cmpwi|cmplw|cmplwi|beq|bne|blt|ble|bgt|bge) (r[0-7])", "\\1 c\\2", content)
    # Change register to floating point registers for fmr/lfs/stfs
    content = re.sub(r"(lfs|lfd|stfs|stfd) r([0-7])", "\\1 f\\2", content)
    content = re.sub(r"(fmr) r(\d+),r([\d+])", "\\1 f\\2,f\\3", content)
    # Change register to floating point registers for fctiwz/fmuls
    content = re.sub(r"(fctiwz) r(\d+),(\d+)", "\\1 f\\2,f\\3", content)
    content = re.sub(r"(fmuls) r(\d+),r(\d+),r(\d+)", "\\1 f\\2,f\\3,f\\4", content)
    # Change register to floating point registers for fcmpu
    content = re.sub(r"(fcmpu) r(\d+),r(\d+),r(\d+)", "\\1 cr\\2,f\\3,f\\4", content)
    # Change unsupported offset for symbols specifically for lis->addi and lis->lwz
    r = r"(lis (r\d+),.*?)\+(\d+)(@.*\n)(\t(?:addi|lwz) r\d+,r\d+,.*?)\+\d+(@.*)"
    content = re.sub(r, "\\1\\4\taddi \\2,\\2,\\3\n\\5\\6", content)
    # Add support for import with changed namespaces
    content = re.sub(r"(bl.*)", lambda _: re.sub(r"::", ".", str(_.group(1))), content)

    # Add Parameters from rules.txt file
    for parameter in parameters[dirname]:
        if parameter.endswith("Float"):
            content = re.sub(rf"({parameter}:\n\t\.)int(\s+)0", f"\\1float\\2${parameter}", content)
        else:
            content = re.sub(rf"({parameter}:\n\t\.int\s+)0", f"\\1${parameter}", content)

    # Prepare packages
    r = r"^#ifdef (?P<name>.*?)\nmoduleMatches *= *(?P<ids>.*?)" \
        r" *,? *[#;] *(?P<versions>.*?)\n(?P<content>.*?)^#endif *\n"
    packages = [match.groupdict() for match in re.compile(r, re.MULTILINE | re.DOTALL).finditer(data)]

    # Add cemu package information
    modules = f'{", ".join(package["ids"] for package in packages)} #' \
              f' {", ".join(package["versions"] for package in packages)}'
    content = f"[{modnames[dirname]}_{basename}]\nmoduleMatches = {modules}\n.origin = codecave\n\n{content}\n\n"

    # Add version specific addresses for symbols
    for package in packages:
        content += f'[{modnames[dirname]}_{basename}_{package["name"]}]\nmoduleMatches = {package["ids"]} ' \
                   f'# {package["versions"]}\n{package["content"]}\n\n'

    # Create file
    try:
        output_path = os.path.join(os.path.dirname(filename), f"patch_{basename}.asm")
        with open(output_path, "w") as f:
            f.write(content)
    except Exception:
        raise Exception(f"Unable to write to patch_{basename}.asm")
