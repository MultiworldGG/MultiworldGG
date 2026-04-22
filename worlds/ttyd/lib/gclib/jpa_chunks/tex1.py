
from gclib import fs_helpers as fs
from io import BytesIO
from gclib.jchunk import JPAChunk
from gclib.bti import BTI

class TEX1(JPAChunk):
  def read_chunk_specific_data(self):
    # This string is 0x14 bytes long, but sometimes there are random garbage bytes after the null byte.
    self.filename = fs.read_str_until_null_character(self.data, 0xC)
    
    bti_data = BytesIO(fs.read_bytes(self.data, 0x20, self.size - 0x20))
    self.bti = BTI(bti_data)
  
  def save_chunk_specific_data(self):
    self.data.seek(0x20)
    self.bti.save_header_changes()
    header_bytes = fs.read_bytes(self.bti.data, self.bti.header_offset, 0x20)
    self.data.write(header_bytes)
    
    self.bti.image_data.seek(0)
    self.data.write(self.bti.image_data.read())
    
    if self.bti.needs_palettes():
      self.bti.palette_data.seek(0)
      self.data.write(self.bti.palette_data.read())
