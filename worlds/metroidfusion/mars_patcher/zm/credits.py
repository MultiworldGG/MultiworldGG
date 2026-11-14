from ..credits import CreditsLine, CreditsWriter, get_credits_size
from ..rom import Rom
from .auto_generated_types import MarsschemazmCreditsTextItem
from .constants.credits_lines import (
    MARS_CREDITS,
    RDV_CREDITS,
    ZM_STAFF_LINES,
)
from .constants.reserved_space import ReservedPointersZM


def write_credits(rom: Rom, data: list[MarsschemazmCreditsTextItem]) -> None:
    writer = CreditsWriter(rom)

    # Write MARS credits
    lines = [CreditsLine(*line) for line in MARS_CREDITS]
    writer.write_lines(lines)

    # Write RDV credits
    lines = [CreditsLine(*line) for line in RDV_CREDITS]
    writer.write_lines(lines)

    # Write custom credits
    lines = [CreditsLine.from_json(d) for d in data]
    writer.write_lines(lines)

    # Write Zero Mission staff credits
    lines = [CreditsLine(*line) for line in ZM_STAFF_LINES]
    writer.write_lines(lines)

    # Write to ROM
    credits_ptr = ReservedPointersZM.CREDITS_PTR.value
    credits_addr = rom.read_ptr(credits_ptr)
    credits_size = get_credits_size(rom, credits_addr)
    rom.write_repointable_data(credits_addr, credits_size, writer.data, [credits_ptr])
