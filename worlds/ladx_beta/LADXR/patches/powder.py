from ..assembler import ASM


# remove calls to GiveInventoryItem(_trampoline)
def onlyGivePowderWhenHavePowder(rom):
    # trendy game
    rom.patch(0x04, 0x366B, ASM("call $3E6B"), b"", fill_nop=True)

    # floating powder
    rom.patch(0x06, 0x3BC1, ASM("call $3E6B"), b"", fill_nop=True)

    # standing powder
    rom.patch(0x03, 0x2356, ASM("call $6472"), b"", fill_nop=True)