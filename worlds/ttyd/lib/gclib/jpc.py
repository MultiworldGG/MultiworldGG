from io import BytesIO
import os
import glob

from gclib import fs_helpers as fs
from gclib.jpa_enums import JPACVersion
from gclib.jpa import JParticle, JParticle100, JParticle210
from gclib.jpa_chunks.tex1 import TEX1

PARTICLE_LIST_OFFSET = {
  JPACVersion.JPAC1_00: 0x20,
  JPACVersion.JPAC2_10: 0x10,
}

class JPC:
  tex1: TEX1
  
  version: JPACVersion
  particles: list[JParticle]
  particles_by_id: dict[int, JParticle]
  textures: list[TEX1]
  textures_by_filename: dict[str, TEX1]
  
  def __init__(self, data):
    self.particles = []
    self.particles_by_id = {}
    self.textures = []
    self.textures_by_filename = {}
    
    self.data = data
    self.read()
  
  def read(self):
    self.magic = fs.read_str(self.data, 0, 8)
    self.version = JPACVersion(self.magic)
    self.num_particles = fs.read_u16(self.data, 8)
    self.num_textures = fs.read_u16(self.data, 0xA)
    if self.version == JPACVersion.JPAC2_10:
      self.tex_offset = fs.read_u32(self.data, 0xC)
    
    self.particles.clear()
    self.particles_by_id.clear()
    offset = PARTICLE_LIST_OFFSET[self.version]
    for particle_index in range(self.num_particles):
      particle = JParticle(self.data, offset, self.version)
      self.particles.append(particle)
      
      if particle.particle_id in self.particles_by_id:
        raise Exception("Duplicate particle ID: %04X" % particle.particle_id)
      self.particles_by_id[particle.particle_id] = particle
      
      # The particle's size field is inaccurate in some rare cases.
      # So we instead add the size of the data the particle read, because that is done in an accurate way.
      offset += fs.data_len(particle.data)
    
    self.textures.clear()
    self.textures_by_filename.clear()
    if self.version == JPACVersion.JPAC2_10:
      offset = self.tex_offset
    for texture_index in range(self.num_textures):
      chunk_magic = fs.read_str(self.data, offset, 4)
      assert chunk_magic == "TEX1"
      
      size = fs.read_u32(self.data, offset+4)
      chunk_data = fs.read_sub_data(self.data, offset, size)
      texture = TEX1(chunk_data, self.version)
      texture.read(0)
      
      self.textures.append(texture)
      
      if texture.filename in self.textures_by_filename:
        raise Exception("Duplicate texture filename: %s" % texture.filename)
      self.textures_by_filename[texture.filename] = texture
      
      offset += texture.size
    
    # Populate the particle TDB1 texture filename lists.
    for particle in self.particles:
      for texture_id in particle.tdb1.texture_ids:
        texture = self.textures[texture_id]
        particle.tdb1.texture_filenames.append(texture.filename)
  
  def add_particle(self, particle):
    if particle.particle_id in self.particles_by_id:
      raise Exception("Cannot add a particle with the same name as an existing one: %04X" % particle.particle_id)
    self.particles.append(particle)
    self.particles_by_id[particle.particle_id] = particle
  
  def replace_particle(self, particle):
    if particle.particle_id not in self.particles_by_id:
      raise Exception("Cannot replace a particle that does not already exist: %04X" % particle.particle_id)
    existing_particle = self.particles_by_id[particle.particle_id]
    particle_index = self.particles.index(existing_particle)
    self.particles[particle_index] = particle
    self.particles_by_id[particle.particle_id] = particle
  
  def add_texture(self, texture):
    if texture.filename in self.textures_by_filename:
      raise Exception("Cannot add a texture with the same name as an existing one: %s" % texture.filename)
    self.textures.append(texture)
    self.textures_by_filename[texture.filename] = texture
  
  def replace_texture(self, texture):
    if texture.filename not in self.textures_by_filename:
      raise Exception("Cannot replace a texture that does not already exist: %s" % texture.filename)
    texture_id = [tex.filename for tex in self.textures].index(texture.filename)
    self.textures[texture_id] = texture
    self.textures_by_filename[texture.filename] = texture
  
  def extract_all_particles_to_disk(self, output_directory):
    if not os.path.isdir(output_directory):
      os.mkdir(output_directory)
    
    for particle in self.particles:
      file_name = "%04X.jpa" % particle.particle_id
      particle_path = os.path.join(output_directory, file_name)
      with open(particle_path, "wb") as f:
        particle.data.seek(0)
        f.write(particle.data.read())
        
        for texture_id in particle.tdb1.texture_ids:
          texture = self.textures[texture_id]
          texture.data.seek(0)
          f.write(texture.data.read())
  
  def import_particles_from_disk(self, input_directory):
    all_jpa_file_paths = glob.glob(glob.escape(input_directory) + "/*.jpa")
    new_particles = []
    new_textures = []
    new_textures_for_particle_id = {}
    for jpa_path in all_jpa_file_paths:
      # Read the particle itself.
      with open(jpa_path, "rb") as f:
        jpa_data = BytesIO(f.read())
      particle = JParticle(jpa_data, 0, self.version)
      new_particles.append(particle)
      new_textures_for_particle_id[particle.particle_id] = []
      
      # Read the textures.
      offset = fs.data_len(particle.data)
      while True:
        if offset == fs.data_len(jpa_data):
          break
        size = fs.read_u32(jpa_data, offset+4)
        chunk_data = fs.read_sub_data(jpa_data, offset, size)
        texture = TEX1(chunk_data, self.version)
        texture.read(0)
        new_textures.append(texture)
        new_textures_for_particle_id[particle.particle_id].append(texture)
        offset += texture.size
    
    num_particles_added = 0
    num_particles_overwritten = 0
    num_textures_added = 0
    num_textures_overwritten = 0
    
    for particle in new_particles:
      if particle.particle_id in self.particles_by_id:
        self.replace_particle(particle)
        num_particles_overwritten += 1
      else:
        num_particles_added += 1
        self.add_particle(particle)
      
      # Populate the particle's TDB1 texture filename list.
      particle.tdb1.texture_filenames = []
      for texture in new_textures_for_particle_id[particle.particle_id]:
        particle.tdb1.texture_filenames.append(texture.filename)
    
    for texture in new_textures:
      if texture.filename in self.textures_by_filename:
        self.replace_texture(texture)
        num_textures_overwritten += 1
      else:
        self.add_texture(texture)
        num_textures_added += 1
    
    return (num_particles_added, num_particles_overwritten, num_textures_added, num_textures_overwritten)
  
  def save(self):
    self.num_particles = len(self.particles)
    self.num_textures = len(self.textures)
    fs.write_magic_str(self.data, 0, self.magic, 8)
    fs.write_u16(self.data, 8, self.num_particles)
    fs.write_u16(self.data, 0xA, self.num_textures)
    if self.version == JPACVersion.JPAC2_10:
      fs.write_u32(self.data, 0xC, self.tex_offset)
    
    # Cut off the particle list and texture list since we're replacing this data entirely.
    self.data.truncate(PARTICLE_LIST_OFFSET[self.version])
    self.data.seek(PARTICLE_LIST_OFFSET[self.version])
    
    for particle in self.particles:
      # First regenerate this particle's TDB1 texture ID list based off the filenames.
      particle.tdb1.texture_ids = []
      for texture_filename in particle.tdb1.texture_filenames:
        texture_id = [tex.filename for tex in self.textures].index(texture_filename)
        particle.tdb1.texture_ids.append(texture_id)
      
      particle.save()
      
      particle.data.seek(0)
      particle_data = particle.data.read()
      self.data.write(particle_data)
    
    fs.align_data_to_nearest(self.data, 0x20, padding_bytes=b'\0')
    
    for texture in self.textures:
      texture.save()
      
      texture.data.seek(0)
      texture_data = texture.data.read()
      self.data.write(texture_data)
    
    fs.align_data_to_nearest(self.data, 0x20, padding_bytes=b'\0')

class JPC100(JPC):
  particles: list[JParticle100]
  particles_by_id: dict[int, JParticle100]

class JPC210(JPC):
  particles: list[JParticle210]
  particles_by_id: dict[int, JParticle210]
