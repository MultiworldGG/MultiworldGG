def get_flag_val(input_bytes: bytes, flag_position: int):
    return input_bytes[flag_position // 8] & (1 << flag_position % 8)

def bit_flagger(input_byte: bytes, flag_position: int, bool_setting):
    bool_char = 1 if bool_setting else 0
    return input_byte | (bool_char << flag_position)
