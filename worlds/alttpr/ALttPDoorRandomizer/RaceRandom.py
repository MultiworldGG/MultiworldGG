import random as _random
from functools import update_wrapper

__all__ = ["use_secure"]

_prng_inst = _random.Random()
_cprng_inst = _random.SystemRandom()

_mode = "prng"

def use_secure(secure=True):
    # pylint: disable=global-statement
    global _mode
    _mode = "cprng" if secure else "prng"

def _wrap(name):
    def somefunc(*args, **kwargs):
        return getattr(_cprng_inst if _mode == "cprng" else _prng_inst, name)(*args, **kwargs)
    update_wrapper(somefunc, getattr(_prng_inst, name))

    return somefunc

# These are for intellisense purposes only, and will be overwritten below
choice = _prng_inst.choice
choices = _prng_inst.choices
gauss = _prng_inst.gauss
getrandbits = _prng_inst.getrandbits
randint = _prng_inst.randint
random = _prng_inst.random
randrange = _prng_inst.randrange
sample = _prng_inst.sample
seed = _prng_inst.seed
shuffle = _prng_inst.shuffle
uniform = _prng_inst.uniform

def init_race_random(multiworld_random):
    global _prng_inst, _cprng_inst
    _prng_inst = multiworld_random
    _cprng_inst = multiworld_random  # AP doesn't use system random

    for func_name in dir(multiworld_random):
        if not callable(getattr(multiworld_random, func_name)):
            continue
        if not callable(getattr(_prng_inst, func_name, None)):
            continue
        if func_name.startswith('_'):
            continue

        globals()[func_name] = _wrap(func_name)
        __all__.append(func_name)
