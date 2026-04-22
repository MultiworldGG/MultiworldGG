
from io import BytesIO
from enum import Enum

from gclib import fs_helpers as fs
from gclib import texture_utils
from gclib.gclib_file import GCLibFile, GCLibFileEntry
from gclib.texture_utils import ImageFormat, PaletteFormat
from gclib.texture_utils import BLOCK_WIDTHS, BLOCK_HEIGHTS, BLOCK_DATA_SIZES
from gclib.texture_utils import IMAGE_FORMATS_THAT_USE_PALETTES, GREYSCALE_IMAGE_FORMATS, GREYSCALE_PALETTE_FORMATS
from gclib.gx_enums import WrapMode, FilterMode

class BTI(GCLibFile):
  def __init__(self, flexible_data = None, header_offset=0):
    if isinstance(flexible_data, GCLibFileEntry) or isinstance(flexible_data, str):
      assert header_offset == 0
    super().__init__(flexible_data)
    
    self.header_offset = header_offset
    
    self.read_header(self.data, header_offset=header_offset)
    
    assert self.mipmap_count > 0, "Mipmap count must not be zero"
    
    # The size of all mipmap image data combined is equal to the offset of the next mipmap after the last one.
    image_data_total_size, _, _, _ = self.get_mipmap_offset_and_size(self.mipmap_count)
    
    self.image_data = BytesIO(fs.read_bytes(self.data, header_offset+self.image_data_offset, image_data_total_size))
    
    palette_data_size = self.num_colors*2
    self.palette_data = BytesIO(fs.read_bytes(self.data, header_offset+self.palette_data_offset, palette_data_size))
  
  def read_header(self, data, header_offset=0):
    self.image_format = ImageFormat(fs.read_u8(data, header_offset+0))
    
    self.alpha_setting = fs.read_u8(data, header_offset+1)
    self.width = fs.read_u16(data, header_offset+2)
    self.height = fs.read_u16(data, header_offset+4)
    
    self.wrap_s = WrapMode(fs.read_u8(data, header_offset+6))
    self.wrap_t = WrapMode(fs.read_u8(data, header_offset+7))
    
    self.palettes_enabled = bool(fs.read_u8(data, header_offset+8))
    self.palette_format = PaletteFormat(fs.read_u8(data, header_offset+9))
    self.num_colors = fs.read_u16(data, header_offset+0xA)
    self.palette_data_offset = fs.read_u32(data, header_offset+0xC)
    
    self.min_filter = FilterMode(fs.read_u8(data, header_offset+0x14))
    self.mag_filter = FilterMode(fs.read_u8(data, header_offset+0x15))
    
    self.min_lod = fs.read_u8(data, header_offset+0x16)
    self.max_lod = fs.read_u8(data, header_offset+0x17)
    self.mipmap_count = fs.read_u8(data, header_offset+0x18)
    self.unknown_3 = fs.read_u8(data, header_offset+0x19)
    self.lod_bias = fs.read_s16(data, header_offset+0x1A)
    
    self.image_data_offset = fs.read_u32(data, header_offset+0x1C)
    
    if self.mipmap_count == 0:
      self.mipmap_count = 1
  
  def save_header_changes(self):
    fs.write_u8(self.data, self.header_offset+0, self.image_format.value)
    
    fs.write_u8(self.data, self.header_offset+1, self.alpha_setting)
    fs.write_u16(self.data, self.header_offset+2, self.width)
    fs.write_u16(self.data, self.header_offset+4, self.height)
    
    fs.write_u8(self.data, self.header_offset+6, self.wrap_s.value)
    fs.write_u8(self.data, self.header_offset+7, self.wrap_t.value)
    
    self.palettes_enabled = self.needs_palettes()
    fs.write_u8(self.data, self.header_offset+8, int(self.palettes_enabled))
    fs.write_u8(self.data, self.header_offset+9, self.palette_format.value)
    fs.write_u16(self.data, self.header_offset+0xA, self.num_colors)
    fs.write_u32(self.data, self.header_offset+0xC, self.palette_data_offset)
    
    fs.write_u8(self.data, self.header_offset+0x14, self.min_filter.value)
    fs.write_u8(self.data, self.header_offset+0x15, self.mag_filter.value)
    
    assert self.mipmap_count <= self.get_max_valid_mipmap_count()
    self.max_lod = min(0xFF, max(0, (self.mipmap_count-1)*8))
    fs.write_u8(self.data, self.header_offset+0x16, self.min_lod)
    fs.write_u8(self.data, self.header_offset+0x17, self.max_lod)
    fs.write_u8(self.data, self.header_offset+0x18, self.mipmap_count)
    fs.write_u8(self.data, self.header_offset+0x19, self.unknown_3)
    fs.write_s16(self.data, self.header_offset+0x1A, self.lod_bias)
    
    fs.write_u32(self.data, self.header_offset+0x1C, self.image_data_offset)
  
  # Note: This function is for standalone .bti files only (as opposed to textures embedded inside
  # J3D models/animations).
  def save_changes(self):
    # Cut off the image and palette data first since we're replacing this data entirely.
    self.data.truncate(0x20)
    self.data.seek(0x20)
    
    self.image_data_offset = 0x20
    self.image_data.seek(0)
    self.data.write(self.image_data.read())
    
    if self.needs_palettes():
      self.palette_data_offset = 0x20 + fs.data_len(self.image_data)
      self.palette_data.seek(0)
      self.data.write(self.palette_data.read())
    else:
      self.palette_data_offset = 0
    
    self.save_header_changes()
  
  @property
  def block_width(self):
    return BLOCK_WIDTHS[self.image_format]
  
  @property
  def block_height(self):
    return BLOCK_HEIGHTS[self.image_format]
  
  @property
  def block_data_size(self):
    return BLOCK_DATA_SIZES[self.image_format]
  
  def needs_palettes(self):
    return self.image_format in IMAGE_FORMATS_THAT_USE_PALETTES
  
  def is_greyscale(self):
    if self.needs_palettes():
      return self.palette_format in GREYSCALE_PALETTE_FORMATS
    else:
      return self.image_format in GREYSCALE_IMAGE_FORMATS
  
  @staticmethod
  def round_to_block(num, block_size):
    return (num + (block_size-1)) // block_size
  
  def get_mipmap_offset_and_size(self, mipmap_index):
    blocks_wide = self.round_to_block(self.width, self.block_width)
    blocks_tall = self.round_to_block(self.height, self.block_height)
    curr_mipmap_size = blocks_wide*blocks_tall*self.block_data_size
    remaining_mipmaps = mipmap_index
    image_data_offset = 0
    width = self.width
    height = self.height
    while remaining_mipmaps > 0:
      image_data_offset += curr_mipmap_size
      width //= 2
      height //= 2
      blocks_wide = self.round_to_block(width, self.block_width)
      blocks_tall = self.round_to_block(height, self.block_height)
      curr_mipmap_size = blocks_wide*blocks_tall*self.block_data_size
      remaining_mipmaps -= 1
    return image_data_offset, curr_mipmap_size, width, height
  
  def get_max_valid_mipmap_count(self):
    mipmap_index = 0
    width = self.width
    height = self.height
    for i in range(0xFF+1):
      width //= 2
      height //= 2
      if width <= 0 or height <= 0:
        break
      mipmap_index += 1
    return mipmap_index
  
  def render(self):
    return self.render_mipmap(0)
  
  def render_mipmap(self, mipmap_index):
    image_data_offset, curr_mipmap_size, width, height = self.get_mipmap_offset_and_size(mipmap_index)
    image_data = fs.read_sub_data(self.image_data, image_data_offset, curr_mipmap_size)
    
    image = texture_utils.decode_image(
      image_data, self.palette_data,
      self.image_format, self.palette_format,
      self.num_colors,
      width, height
    )
    return image
  
  def render_palette(self):
    colors = texture_utils.decode_palettes(
      self.palette_data, self.palette_format,
      self.num_colors, self.image_format
    )
    return colors
  
  def replace_image_from_path(self, new_image_file_path):
    self.image_data, self.palette_data, encoded_colors, self.width, self.height = texture_utils.encode_image_from_path(
      new_image_file_path, self.image_format, self.palette_format,
      mipmap_count=self.mipmap_count
    )
    self.num_colors = len(encoded_colors)
  
  def replace_image(self, new_image):
    self.image_data, self.palette_data, encoded_colors = texture_utils.encode_image(
      new_image, self.image_format, self.palette_format,
      mipmap_count=self.mipmap_count
    )
    self.num_colors = len(encoded_colors)
    self.width = new_image.width
    self.height = new_image.height
  
  def replace_mipmap(self, mipmap_index, new_image):
    image_data_offset, curr_mipmap_size, width, height = self.get_mipmap_offset_and_size(mipmap_index)
    
    images = []
    for other_mipmap_index in range(self.mipmap_count):
      if other_mipmap_index == mipmap_index:
        images.append(new_image)
      else:
        images.append(self.render_mipmap(other_mipmap_index))
    
    encoded_colors, colors_to_color_indexes = texture_utils.generate_new_palettes_from_images(images, self.image_format, self.palette_format)
    
    mipmap_image_data = texture_utils.encode_mipmap_image(
      new_image, self.image_format,
      colors_to_color_indexes,
      width, height
    )
    assert fs.data_len(mipmap_image_data) == curr_mipmap_size
    fs.write_bytes(self.image_data, image_data_offset, fs.read_all_bytes(mipmap_image_data))
    self.palette_data = texture_utils.encode_palette(encoded_colors, self.palette_format, self.image_format)
    self.num_colors = len(encoded_colors)
  
  def replace_palette(self, new_colors):
    encoded_colors = texture_utils.generate_new_palettes_from_colors(new_colors, self.palette_format)
    self.palette_data = texture_utils.encode_palette(encoded_colors, self.palette_format, self.image_format)
    self.num_colors = len(encoded_colors)
  
  def is_visually_equal_to(self, other):
    # Checks if a BTI would result in the exact same rendered PNG image data as another BTI, without actually rendering them both in order to improve performance.
    
    if not isinstance(other, BTI):
      return False
    
    if self.image_format != other.image_format:
      return False
    if self.palette_format != other.palette_format:
      return False
    if self.num_colors != other.num_colors:
      return False
    if self.width != other.width:
      return False
    if self.height != other.height:
      return False
    if fs.read_all_bytes(self.image_data) != fs.read_all_bytes(other.image_data):
      return False
    if fs.read_all_bytes(self.palette_data) != fs.read_all_bytes(other.palette_data):
      return False
    
    return True
