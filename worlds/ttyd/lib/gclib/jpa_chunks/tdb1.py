
from gclib import fs_helpers as fs
from gclib.jchunk import JPAChunk
from gclib.jpa_enums import JPACVersion

TDB1_ID_LIST_OFFSET = {
  JPACVersion.JPAC1_00: 0xC,
  JPACVersion.JPAC2_10: 0x8,
}

class TDB1(JPAChunk):
  # Texture ID database (list of texture IDs in this JPC file used by this particle)
  
  def read_chunk_specific_data(self):
    self.texture_ids = None # Can't read these yet, we need the number of textures from the particle header.
    self.texture_filenames = [] # Leave this list empty for now, it will be populated after the texture list is read.
  
  def read_texture_ids(self, num_texture_ids):
    self.texture_ids = []
    for texture_id_index in range(num_texture_ids):
      texture_id = fs.read_u16(self.data, TDB1_ID_LIST_OFFSET[self.version] + texture_id_index*2)
      self.texture_ids.append(texture_id)
  
  def save_chunk_specific_data(self):
    self.data.truncate(TDB1_ID_LIST_OFFSET[self.version])
    
    # Save the texture IDs (which were updated by the JPC's save function).
    for texture_id_index, texture_id in enumerate(self.texture_ids):
      fs.write_u16(self.data, TDB1_ID_LIST_OFFSET[self.version] + texture_id_index*2, texture_id)
