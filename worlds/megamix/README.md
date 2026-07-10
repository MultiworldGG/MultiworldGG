- **[What is this?](docs/en_Hatsune%20Miku%20Project%20Diva%20Mega%20Mix%2B.md)**
- **[Setup](docs/setup_en.md)**

This apworld is needed for seed and template generation and includes the JSON Generator for using mod songs.

The *game* requires the companion [mod](https://github.com/Cynichill/Diva-Archipelago-Mod) but players should source it from Setup linked above.

---

## Developing
A minimal development setup.

The `git clone` and relative path commands should be skipped and/or modified to match your setup, such as if using a GUI for git. 

```bash
# Optionally replace with your fork
git clone https://github.com/ArchipelagoMW/Archipelago
# Replace with your fork
git clone https://github.com/Cynichill/DivaAPworld

# Only retain required worlds files for PyCharm and Launcher performance
# Other worlds will not be available for code reference
# The Archipelago clone can be updated/branched as needed
cd Archipelago
git sparse-checkout set --no-cone "/*" "!/worlds/*/" "/worlds/apquest/" "/worlds/generic/"
cd ..

# Windows: Symlink apworld folder
mklink /J Archipelago\worlds\megamix DivaAPworld

# Linux: Symlink apworld folder
ln -rsv ./DivaAPworld ./Archipelago/worlds/megamix
```

- PyCharm
  - Open `Archipelago` as the project directory.
  - Develop within `Archipelago\worlds\megamix`.
  - Recommended run configurations:
    - `Launcher.py "Universal Tracker"` ([tracker apworld](github.com/FarisTheAncient/Archipelago/releases/latest))
    - `Launcher.py "Mega Mix JSON Generator"`
- Testing
  - pytest: `pytest test/general worlds/megamix`
  - [fuzzer](https://github.com/Eijebong/Archipelago-fuzzer): `fuzz.py -g megamix -r 500`
  - GitHub CI: [tests.yml](.github/workflows/tests.yml)