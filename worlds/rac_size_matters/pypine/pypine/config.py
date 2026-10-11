from configparser import ConfigParser
from pathlib import Path

DEFAULT_PINE_PORT = 28011

class PineConfig:

    config: ConfigParser
    port: int
    memcard_name: str

    def __init__(self, config_path: Path, port: int = DEFAULT_PINE_PORT, memcard_name: str = "memcard.ps2"):
        self.config_file_path = config_path
        self.config = ConfigParser(delimiters=('='))
        self.config.optionxform = str
        self.port = port
        self.memcard_name = memcard_name

    def setup_config(self):
        self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.config_file_path.exists():
            self.config.read(self.config_file_path)
        self._verify_config()
        self._write_config()

    def _write_config(self):
        try:
            with self.config_file_path.open('w') as configfile:
                self.config.write(configfile)
        except OSError as e:
            print(f"Error writing config file: {e}")

    def _verify_config(self):
        self._normalize_keys('EmuCore', {'enablepine': 'EnablePINE', 'pineslot': 'PINESlot'})
        self.config['EmuCore'] = {
            **self.config['EmuCore'],
            'EnablePINE': 'true',
            'PINESlot': str(self.port),
        }
        if not self.config.has_section('Memcard'):
            self.config.add_section('Memcard')
        self.config['Memcard'] = {
            **self.config['Memcard'],
            'Slot1_Enable': 'true',
            'Slot2_Enable': 'false',
            'Slot1_Filename': self.memcard_name,
        }

    def _normalize_keys(self, section, renames):
        if not self.config.has_section(section):
            self.config.add_section(section)
            return
        for key in list(self.config[section]):
            canonical = renames.get(key.lower())
            if canonical and key != canonical:
                self.config[section][canonical] = self.config[section].pop(key)