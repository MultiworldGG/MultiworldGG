import os
import time
import logging

try:
    import bps.apply
    import bps.io
except ImportError:
    raise Exception('Could not load BPS module')

from .Utils import output_path
from .Rom import LocalRom, apply_rom_settings
from .source.tools.BPS import bps_read_vlv


def adjust(args):
    start = time.process_time()
    logger = logging.getLogger('')
    logger.info('Patching ROM.')

    outfilebase = os.path.basename(args.rom)[:-4] + '_adjusted'

    if os.stat(args.rom).st_size in (0x200000, 0x400000) and os.path.splitext(args.rom)[-1].lower() == '.sfc':
        rom = LocalRom(args.rom, False)
        if os.path.isfile(args.baserom):
            baserom = LocalRom(args.baserom, True)
            rom.orig_buffer = baserom.orig_buffer
    else:
        raise RuntimeError('Provided Rom is not a valid Link to the Past Randomizer Rom. Please provide one for adjusting.')

    if not hasattr(args,"sprite"):
        args.sprite = None
    if not hasattr(args,"triforce_gfx"):
        args.triforce_gfx = None

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic,
                       args.sprite, args.triforce_gfx, args.ow_palettes, args.uw_palettes, args.reduce_flashing, args.shuffle_sfx,
                       args.shuffle_sfxinstruments, args.shuffle_songinstruments, args.msu_resume)

    output_path.cached_path = args.outputpath
    rom.write_to_file(output_path('%s.sfc' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.process_time() - start)

    return args


def patch(args):
    start = time.process_time()
    logger = logging.getLogger('')
    logger.info('Patching ROM.')

    outfile_base = os.path.basename(args.patch)[:-4]

    rom = LocalRom(args.baserom, False)
    if os.path.isfile(args.baserom):
        rom.verify_base_rom()
    orig_buffer = rom.buffer.copy()
    with open(args.patch, 'rb') as stream:
        stream.seek(4)  # skip BPS1
        bps_read_vlv(stream)  # skip source size
        target_length = bps_read_vlv(stream)
        rom.buffer.extend(bytearray([0x00] * (target_length - len(rom.buffer))))
        stream.seek(0)
        bps.apply.apply_to_bytearrays(bps.io.read_bps(stream), orig_buffer, rom.buffer)

    if not hasattr(args, "sprite"):
        args.sprite = None
    if not hasattr(args, "triforce_gfx"):
        args.triforce_gfx = None

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic,
                       args.sprite, args.triforce_gfx, args.ow_palettes, args.uw_palettes, args.reduce_flashing,
                       args.shuffle_sfx, args.shuffle_sfxinstruments, args.shuffle_songinstruments, args.msu_resume)

    output_path.cached_path = args.outputpath
    rom.write_to_file(output_path('%s.sfc' % outfile_base))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.process_time() - start)

    return args
