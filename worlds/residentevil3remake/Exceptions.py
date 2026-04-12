from Options import OptionError

class RE3ROptionError(OptionError):
    def __init__(self, msg):
        msg = f"There was a problem with your RE3R YAML options. {msg}"

        super().__init__(msg)

