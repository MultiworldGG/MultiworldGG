from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.jchunk import JChunk
from gclib.animation import LoopMode
from gclib.bunfoe import bunfoe, field, BUNFOE

@bunfoe
class ANF1(JChunk):
  loop_mode:                LoopMode
  rotation_frac:            u8
  duration:                 u16
  anims_count:              u16
  scale_table_count:        u16
  rotation_table_count:     u16
  translation_table_count:  u16
  anims_offset:             u32
  scale_table_offset:       u32
  rotation_table_offset:    u32
  translation_table_offset: u32
  
  def read_chunk_specific_data(self):
    BUNFOE.read(self, 0)
  
  def save_chunk_specific_data(self):
    BUNFOE.save(self, 0)
