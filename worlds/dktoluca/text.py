from .client import TextMemory, DKC3_TEXT_DATA, DKC3_TEXT_OFFSETS
from worlds.AutoSNIClient import SnesData

def extract_text(text_memory: SnesData[TextMemory]):
    current_text: list[bytearray] = []

    text_offset_data = bytearray(text_memory.get(TextMemory.text_offsets))
    text_data = bytearray(text_memory.get(TextMemory.text_data))
    idx = 0
    previous_offset = 0
    current_offset = int.from_bytes(text_offset_data[idx:idx+2], "little")
    while current_offset != 0x0000:
        #print (f"{previous_offset:04X} | {current_offset+1:04X} | {idx:04X}")
        data = text_data[previous_offset:current_offset]
        #print (len(data), data)
        current_text.append(data)
        idx += 2
        previous_offset = current_offset
        current_offset = int.from_bytes(text_offset_data[idx:idx+2], "little")

    return current_text

    