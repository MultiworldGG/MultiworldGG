from typing import Optional
from io import BytesIO

from gclib import fs_helpers as fs
from gclib.jchunk import JPAChunk
from gclib.jpa_enums import JPACVersion
from gclib.jpa_chunks.bsp1 import BSP1
from gclib.jpa_chunks.ssp1 import SSP1, SSP1_JPC100, SSP1_JPC210
from gclib.jpa_chunks.tdb1 import TDB1

PARTICLE_HEADER_SIZE = {
  JPACVersion.JPAC1_00: 0x20,
  JPACVersion.JPAC2_10: 0x8,
}

class JParticle:
  # bem1: BEM1
  bsp1: BSP1
  # esp1: Optional[ESP1]
  # etx1: Optional[ETX1]
  ssp1: Optional[SSP1]
  # fld1: list[FLD1] # TODO: properly handle lists of fields
  # kfa1: list[KFA1]
  tdb1: Optional[TDB1]
  
  CHUNK_TYPES = {
    chunk_class.__name__: chunk_class
    for chunk_class in [
      chunk_class.__args__[0] if chunk_class.__name__ == "Optional" else chunk_class
      for chunk_class in __annotations__.values()
    ]
  }
  
  def __init__(self, jpc_data, particle_offset, jpac_version: JPACVersion):
    self.bsp1 = None
    self.ssp1 = None
    self.tdb1 = None
    
    self.version = jpac_version
    
    if self.version == JPACVersion.JPAC1_00:
      self.read_header_jpc100(jpc_data, particle_offset)
    elif self.version == JPACVersion.JPAC2_10:
      self.read_header_jpc210(jpc_data, particle_offset)
    true_size = self.read_chunks(jpc_data, particle_offset)
    
    jpc_data.seek(particle_offset)
    self.data = BytesIO(jpc_data.read(true_size))
  
  def read_header_jpc100(self, jpc_data, particle_offset):
    self.magic = fs.read_str(jpc_data, particle_offset, 8)
    assert self.magic == "JEFFjpa1"
    
    self.unknown_1 = fs.read_u32(jpc_data, particle_offset+8)
    self.num_chunks = fs.read_u32(jpc_data, particle_offset+0xC)
    self.size = fs.read_u32(jpc_data, particle_offset+0x10) # Not accurate in some rare cases
    
    self.num_kfa1_chunks = fs.read_u8(jpc_data, particle_offset+0x14)
    self.num_fld1_chunks = fs.read_u8(jpc_data, particle_offset+0x15)
    self.num_textures = fs.read_u8(jpc_data, particle_offset+0x16)
    self.unknown_5 = fs.read_u8(jpc_data, particle_offset+0x17)
    
    self.particle_id = fs.read_u16(jpc_data, particle_offset+0x18)
    
    self.unknown_6 = fs.read_bytes(jpc_data, particle_offset+0x1A, 6)
  
  def read_header_jpc210(self, jpc_data, particle_offset):
    self.particle_id = fs.read_u16(jpc_data, particle_offset + 0x0)
    self.num_chunks = fs.read_u16(jpc_data, particle_offset + 0x2)
    self.num_fld1_chunks = fs.read_u8(jpc_data, particle_offset + 0x4)
    self.num_kfa1_chunks = fs.read_u8(jpc_data, particle_offset + 0x5)
    self.num_textures = fs.read_u8(jpc_data, particle_offset + 0x6)
    self.unknown_7 = fs.read_u8(jpc_data, particle_offset + 0x7)
  
  def read_chunks(self, jpc_data, particle_offset):
    self.chunks: list[JPAChunk] = []
    self.chunk_by_type: dict[str, JPAChunk] = {}
    chunk_offset = particle_offset + PARTICLE_HEADER_SIZE[self.version]
    for chunk_index in range(0, self.num_chunks):
      chunk_magic = fs.read_str(jpc_data, chunk_offset, 4)
      chunk_class = self.CHUNK_TYPES.get(chunk_magic, JPAChunk)
      
      size = fs.read_u32(jpc_data, chunk_offset+4)
      chunk_data = fs.read_sub_data(jpc_data, chunk_offset, size)
      chunk = chunk_class(chunk_data, self.version)
      chunk.read(0)
      
      self.chunks.append(chunk)
      self.chunk_by_type[chunk.magic] = chunk
      
      if chunk.magic in self.CHUNK_TYPES:
        setattr(self, chunk.magic.lower(), chunk)
      
      chunk_offset += chunk.size
    
    self.tdb1.read_texture_ids(self.num_textures)
  
    # self.verify_valid_chunks()
    
    true_size = (chunk_offset - particle_offset)
    return true_size
  
  def verify_valid_chunks(self):
    class_attrs = type(self).__annotations__
    for chunk_magic, chunk_class in self.CHUNK_TYPES.items():
      chunk_attr = chunk_magic.lower()
      if chunk_attr in class_attrs:
        if class_attrs[chunk_attr] == chunk_class:
          assert getattr(self, chunk_attr) is not None
  
  def save(self):
    # Cut off the chunk data first since we're replacing this data entirely.
    self.data.truncate(PARTICLE_HEADER_SIZE[self.version])
    self.data.seek(PARTICLE_HEADER_SIZE[self.version])
    
    self.num_textures = len(self.tdb1.texture_ids)
    
    for chunk in self.chunks:
      chunk.save()
      
      chunk.data.seek(0)
      chunk_data = chunk.data.read()
      self.data.write(chunk_data)
    
    if self.version == JPACVersion.JPAC1_00:
      # We don't recalculate this size field, since this is inaccurate anyway. It's probably not even used.
      #self.size = fs.data_len(self.data)
      
      fs.write_magic_str(self.data, 0, self.magic, 8)
      fs.write_u32(self.data, 0x10, self.size)
      
      # TODO: write back all header changes.

class JParticle100(JParticle):
  # bem1: BEM1
  bsp1: BSP1
  # esp1: Optional[ESP1]
  # etx1: Optional[ETX1]
  ssp1: Optional[SSP1_JPC100]
  # fld1: list[FLD1]
  # kfa1: list[KFA1]
  tdb1: Optional[TDB1]

class JParticle210:
  # bem1: BEM1
  bsp1: BSP1
  # esp1: Optional[ESP1]
  # etx1: Optional[ETX1]
  ssp1: Optional[SSP1_JPC210]
  # fld1: list[FLD1]
  # kfa1: list[KFA1]
  tdb1: Optional[TDB1]
