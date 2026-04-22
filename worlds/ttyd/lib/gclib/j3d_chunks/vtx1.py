from enum import IntEnum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.jchunk import JChunk
from gclib.bunfoe import bunfoe, field, BUNFOE
import gclib.gx_enums as GX

class VTX1DataOffsetIndex(IntEnum):
  PositionData  = 0x0
  NormalData    = 0x1
  NBTData       = 0x2
  Color0Data    = 0x3
  Color1Data    = 0x4
  TexCoord0Data = 0x5
  TexCoord1Data = 0x6
  TexCoord2Data = 0x7
  TexCoord3Data = 0x8
  TexCoord4Data = 0x9
  TexCoord5Data = 0xA
  TexCoord6Data = 0xB
  TexCoord7Data = 0xC

GXAttr_TO_VTX1DataOffsetIndex = {
  GX.Attr.Position: VTX1DataOffsetIndex.PositionData,
  GX.Attr.Normal  : VTX1DataOffsetIndex.NormalData,
  GX.Attr.Color0  : VTX1DataOffsetIndex.Color0Data,
  GX.Attr.Color1  : VTX1DataOffsetIndex.Color1Data,
  GX.Attr.Tex0    : VTX1DataOffsetIndex.TexCoord0Data,
  GX.Attr.Tex1    : VTX1DataOffsetIndex.TexCoord1Data,
  GX.Attr.Tex2    : VTX1DataOffsetIndex.TexCoord2Data,
  GX.Attr.Tex3    : VTX1DataOffsetIndex.TexCoord3Data,
  GX.Attr.Tex4    : VTX1DataOffsetIndex.TexCoord4Data,
  GX.Attr.Tex5    : VTX1DataOffsetIndex.TexCoord5Data,
  GX.Attr.Tex6    : VTX1DataOffsetIndex.TexCoord6Data,
  GX.Attr.Tex7    : VTX1DataOffsetIndex.TexCoord7Data,
}

GXComponentType_TO_NUMBER_COMPONENT_BYTE_SIZE = {
  GX.ComponentType.Unsigned8 : 1,
  GX.ComponentType.Signed8   : 1,
  GX.ComponentType.Unsigned16: 2,
  GX.ComponentType.Signed16  : 2,
  GX.ComponentType.Float32   : 4,
}

GXComponentType_TO_COLOR_COMPONENT_BYTE_SIZE = {
  GX.ComponentType.RGB565: 2,
  GX.ComponentType.RGB8  : 1,
  GX.ComponentType.RGBX8 : 1,
  GX.ComponentType.RGBA4 : 2,
  GX.ComponentType.RGBA6 : 1,
  GX.ComponentType.RGBA8 : 1,
}

@bunfoe
class VertexFormat(BUNFOE):
  DATA_SIZE = 0x10
  
  attribute_type      : GX.Attr           = GX.Attr.NULL
  component_count_type: GX.ComponentCount = GX.ComponentCount.Position_XYZ
  component_type      : GX.ComponentType  = GX.ComponentType.Unsigned8
  component_shift     : u8                = 0
  _padding            : u24               = 0xFFFFFF
  
  @property
  def data_offset_index(self):
    return GXAttr_TO_VTX1DataOffsetIndex[self.attribute_type]
  
  @property
  def is_color_attr(self):
    return self.attribute_type in [GX.Attr.Color0, GX.Attr.Color1]
  
  @property
  def component_count(self):
    if self.is_color_attr:
      if self.component_type in [GX.ComponentType.RGB565, GX.ComponentType.RGBA4]:
        return 1
      elif self.component_type in [GX.ComponentType.RGB8, GX.ComponentType.RGBX8, GX.ComponentType.RGBA6, GX.ComponentType.RGBA8]:
        return 4
      else:
        raise NotImplementedError
    
    if self.attribute_type == GX.Attr.Position:
      if self.component_count_type == GX.ComponentCount.Position_XY:
        return 2
      elif self.component_count_type == GX.ComponentCount.Position_XYZ:
        return 3
    elif self.attribute_type == GX.Attr.Normal:
      if self.component_count_type == GX.ComponentCount.Normal_XYZ:
        return 3
    elif self.attribute_type in [
      GX.Attr.Tex0,
      GX.Attr.Tex1,
      GX.Attr.Tex2,
      GX.Attr.Tex3,
      GX.Attr.Tex4,
      GX.Attr.Tex5,
      GX.Attr.Tex6,
      GX.Attr.Tex7,
    ]:
      if self.component_count_type == GX.ComponentCount.TexCoord_S:
        return 1
      elif self.component_count_type == GX.ComponentCount.TexCoord_ST:
        return 2
    
    raise NotImplementedError
  
  @property
  def component_size(self):
    if self.is_color_attr:
      return GXComponentType_TO_COLOR_COMPONENT_BYTE_SIZE[self.component_type]
    else:
      return GXComponentType_TO_NUMBER_COMPONENT_BYTE_SIZE[self.component_type]

class VTX1(JChunk):
  def read_chunk_specific_data(self):
    self.vertex_formats_start_offset = fs.read_u32(self.data, 0x08)
    
    self.vertex_data_offsets = []
    for i in range(13):
      vertex_data_offset = fs.read_u32(self.data, 0x0C+i*4)
      self.vertex_data_offsets.append(vertex_data_offset)
    
    self.vertex_formats: list[VertexFormat] = []
    current_vertex_format_offset = self.vertex_formats_start_offset
    while True:
      vertex_format = VertexFormat(self.data)
      vertex_format.read(current_vertex_format_offset)
      current_vertex_format_offset += VertexFormat.DATA_SIZE
      self.vertex_formats.append(vertex_format)
      if vertex_format.attribute_type == GX.Attr.NULL:
        break
    
    self.attributes: dict[GX.Attr, list] = {}
    for vertex_format in self.vertex_formats:
      if vertex_format.attribute_type == GX.Attr.NULL:
        break
      
      self.load_attribute_data(vertex_format)
  
  def get_attribute_data_count(self, offset_index, component_count, component_size):
    """Attempts to guess at the number of entries this VTX1 section has for a particular attribute."""
    
    entry_size = component_count * component_size
    
    data_start_offset = self.vertex_data_offsets[offset_index]
    
    data_end_offset_index = offset_index + 1
    data_end_offset = 0
    while data_end_offset == 0:
      if data_end_offset_index == len(self.vertex_data_offsets):
        data_end_offset = self.size
        break
      data_end_offset = self.vertex_data_offsets[data_end_offset_index]
      data_end_offset_index += 1
    
    data_size = (data_end_offset - data_start_offset)
    
    # Floor-divide to remove any bytes at the end that can't possibly be data and must be padding.
    data_count = data_size // entry_size
    
    if entry_size <= 0x10:
      # Attempt to remove more bytes that are very likely to be padding by checking if they match known padding strings.
      # If each entry in the list is half the padding size (0x20) or less, there's a possible problem that can occur.
      # We can't tell for sure if the data_count we currently have is accurate or if the padding at the end is giving
      # the illusion that there are more entries than there really are.
      # For example, if each entry is 0xC bytes, and the total data size is 0x40, we don't know if that means the number
      # of entries is 3, 4, or 5, as all of those would pad up to 0x40 bytes.
      # So we check all of the possible entry counts we're unsure of to see if the data from that point to the end
      # happens to match the padding bytes. If it does, it is extremely likely (though not 100% certain) to be padding.
      # In testing, this results in all VTX1 sections in vanilla Wind Waker repacking correctly (including padding).
      KNOWN_PADDING_BYTES = [b"This is padding data to alignme", b"Model made with SuperBMD by Gamma."]
      first_unsure_index = ((data_size-0x20) // entry_size) + 1
      for i in range(first_unsure_index, data_count):
        check_offset = data_start_offset + i*entry_size
        maybe_pad = fs.read_bytes(self.data, check_offset, data_end_offset-check_offset)
        if maybe_pad is None:
          continue
        if any(padding_bytes.startswith(maybe_pad) for padding_bytes in KNOWN_PADDING_BYTES):
          data_size = (check_offset - data_start_offset)
          data_count = data_size // entry_size
          break
    
    return data_count
  
  def load_attribute_data(self, vtxfmt: VertexFormat):
    self.attributes[vtxfmt.attribute_type] = self.load_attribute_list(vtxfmt)
  
  def load_attribute_list(self, vtxfmt: VertexFormat):
    data_offset = self.vertex_data_offsets[vtxfmt.data_offset_index]
    attrib_count = self.get_attribute_data_count(vtxfmt.data_offset_index, vtxfmt.component_count, vtxfmt.component_size)
    attr_data = []
    for i in range(0, attrib_count):
      components = self.read_components(vtxfmt, data_offset)
      attr_data.append(components)
      data_offset += vtxfmt.component_count * vtxfmt.component_size
    return attr_data
  
  def read_components(self, vtxfmt: VertexFormat, data_offset):
    divisor = (1 << vtxfmt.component_shift)
    components = []
    for i in range(vtxfmt.component_count):
      if vtxfmt.is_color_attr:
        component = self.read_color_component(vtxfmt.component_type, data_offset, divisor)
      else:
        component = self.read_number_component(vtxfmt.component_type, data_offset, divisor)
      components.append(component)
      data_offset += vtxfmt.component_size
    return tuple(components)
  
  def read_number_component(self, comp_type: GX.ComponentType, data_offset, divisor):
    match comp_type:
      case GX.ComponentType.Unsigned8:
        return fs.read_u8(self.data, data_offset) / divisor
      case GX.ComponentType.Signed8:
        return fs.read_s8(self.data, data_offset) / divisor
      case GX.ComponentType.Unsigned16:
        return fs.read_u16(self.data, data_offset) / divisor
      case GX.ComponentType.Signed16:
        return fs.read_s16(self.data, data_offset) / divisor
      case GX.ComponentType.Float32:
        return fs.read_float(self.data, data_offset) / divisor
      case _:
        raise NotImplementedError
  
  def read_color_component(self, comp_type: GX.ComponentType, data_offset, divisor):
    match comp_type:
      case GX.ComponentType.RGBA8:
        return fs.read_u8(self.data, data_offset) / 255
      case _:
        raise NotImplementedError
  
  def save_chunk_specific_data(self):
    # Cut off all the data, we're rewriting it entirely.
    self.data.truncate(0)
    
    # Placeholder for the header.
    self.data.seek(0)
    self.data.write(b"\0"*0x40)
    
    offset = self.data.tell()
    self.vertex_formats_start_offset = offset
    
    for vertex_format in self.vertex_formats:
      vertex_format.save(offset)
      offset += VertexFormat.DATA_SIZE
    fs.align_data_to_nearest(self.data, 0x20)
    offset = self.data.tell()
    
    self.vertex_data_offsets = [0]*13
    
    for vertex_format in self.vertex_formats:
      if vertex_format.attribute_type == GX.Attr.NULL:
        break
      
      offset = self.save_attribute_data(vertex_format, offset)
      fs.align_data_to_nearest(self.data, 0x20)
      offset = fs.data_len(self.data)
    
    # Write the header.
    fs.write_magic_str(self.data, 0, "VTX1", 4)
    
    fs.write_u32(self.data, 0x08, self.vertex_formats_start_offset)
    for i, vertex_data_offset in enumerate(self.vertex_data_offsets):
      fs.write_u32(self.data, 0x0C+i*4, vertex_data_offset)
  
  def save_attribute_data(self, vertex_format: VertexFormat, data_offset):
    self.vertex_data_offsets[vertex_format.data_offset_index] = data_offset
    data_offset = self.save_attribute_list(
      self.attributes[vertex_format.attribute_type],
      vertex_format,
      data_offset,
    )
    return data_offset
  
  def save_attribute_list(self, attr_data, vtxfmt: VertexFormat, data_offset):
    for components in attr_data:
      assert len(components) == vtxfmt.component_count
      data_offset = self.save_components(vtxfmt, components, data_offset)
    return data_offset
  
  def save_components(self, vtxfmt: VertexFormat, components, data_offset):
    divisor = (1 << vtxfmt.component_shift)
    for component in components:
      if vtxfmt.is_color_attr:
        self.save_color_component(vtxfmt.component_type, component, data_offset, divisor)
      else:
        self.save_number_component(vtxfmt.component_type, component, data_offset, divisor)
      data_offset += vtxfmt.component_size
    return data_offset
  
  def save_number_component(self, comp_type: GX.ComponentType, component, data_offset, divisor):
    match comp_type:
      case GX.ComponentType.Unsigned8:
        fs.write_u8(self.data, data_offset, round(component*divisor))
      case GX.ComponentType.Signed8:
        fs.write_s8(self.data, data_offset, round(component*divisor))
      case GX.ComponentType.Unsigned16:
        fs.write_u16(self.data, data_offset, round(component*divisor))
      case GX.ComponentType.Signed16:
        fs.write_s16(self.data, data_offset, round(component*divisor))
      case GX.ComponentType.Float32:
        fs.write_float(self.data, data_offset, component*divisor)
      case _:
        raise NotImplementedError
  
  def save_color_component(self, comp_type: GX.ComponentType, component, data_offset, divisor):
    match comp_type:
      case GX.ComponentType.RGBA8:
        fs.write_u8(self.data, data_offset, round(component*255))
      case _:
        raise NotImplementedError
