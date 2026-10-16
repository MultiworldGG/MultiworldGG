from Options import OptionError

from .constants import NUM_WAVES
from .options import NumWaveCaps


def get_wave_cap_info(num_wave_caps_option: NumWaveCaps) -> tuple[int, dict[int, int]]:
    """Calculate information related to wave caps.

    Returns a tuple of:
        * The number of wave cap increase items needed.
        * A lookup of wave index to the number of wave cap increase items needed for that
          wave to be in logic.
    """
    num_wave_caps = _option_to_wave_cap_count(num_wave_caps_option)
    # The first cap is implicitly part of sphere 0, so it doesn't need an item to access
    num_items = num_wave_caps - 1

    # We could just hard-code these, but it makes us slightly more flexible if we add more
    # values down the road.
    wave_caps: list[int] = []
    wave_start = 1
    step_size = NUM_WAVES // num_wave_caps
    for _ in range(num_wave_caps):
        wave_caps.append(wave_start + step_size)
        wave_start += step_size

    cap_idx = 0
    current_cap = wave_caps[0]
    wave_access: dict[int, int] = {}
    for w in range(1, NUM_WAVES + 1):
        if w >= current_cap:
            cap_idx += 1
            current_cap = wave_caps[cap_idx]
        wave_access[w] = cap_idx

    return num_items, wave_access


def _option_to_wave_cap_count(num_wave_caps_option: NumWaveCaps) -> int:
    match num_wave_caps_option:
        case NumWaveCaps.option_one:
            return 1
        case NumWaveCaps.option_two:
            return 2
        case NumWaveCaps.option_four:
            return 4
        case NumWaveCaps.option_ten:
            return 10
        case NumWaveCaps.option_twenty:
            return 20
        case _:
            raise OptionError(f"Invalid value {num_wave_caps_option.value} for num_wave_caps option.")
