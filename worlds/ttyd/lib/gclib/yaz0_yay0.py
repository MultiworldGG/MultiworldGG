
from io import BytesIO

from gclib import fs_helpers as fs

try:
  import pyfastyaz0yay0 # type: ignore
  PY_FAST_YAZ0_YAY0_INSTALLED = True
except ImportError:
  PY_FAST_YAZ0_YAY0_INSTALLED = False

class Yaz0Yay0:
  MAGIC_BYTES = None
  
  MAX_RUN_LENGTH = 0xFF + 0x12
  
  # How far back to search when compressing.
  # Can search as far back as 0x1000 bytes, but the farther back we search the slower it is.
  DEFAULT_SEARCH_DEPTH = 0x1000
  
  # Variables to hold the reserved next match across loops.
  next_num_bytes = 0
  next_match_pos = 0
  next_flag = False
  
  @classmethod
  def check_is_compressed(cls, data):
    if fs.data_len(data) < 4:
      return False
    if fs.read_bytes(data, 0, 4) != cls.MAGIC_BYTES:
      return False
    return True
  
  @classmethod
  def decompress(cls, comp_data: BytesIO) -> BytesIO:
    raise NotImplementedError
  
  @classmethod
  def compress(cls, uncomp_data: BytesIO, search_depth=DEFAULT_SEARCH_DEPTH, should_pad_data=False) -> BytesIO:
    raise NotImplementedError
  
  @classmethod
  def get_num_bytes_and_match_pos(cls, uncomp, uncomp_offset, search_depth=DEFAULT_SEARCH_DEPTH):
    num_bytes = 1
    
    if cls.next_flag:
      cls.next_flag = False
      return (cls.next_num_bytes, cls.next_match_pos)
    
    cls.next_flag = False
    num_bytes, match_pos = cls.simple_rle_encode(uncomp, uncomp_offset, search_depth=search_depth)
    
    if num_bytes >= 3:
      # Check if the next byte has a match that would compress better than the current byte.
      cls.next_num_bytes, cls.next_match_pos = cls.simple_rle_encode(uncomp, uncomp_offset+1, search_depth=search_depth)
      
      if cls.next_num_bytes >= num_bytes+2:
        # If it does, then only copy one byte for this match and reserve the next match for later so we save more space.
        num_bytes = 1
        match_pos = None
        cls.next_flag = True
    
    return (num_bytes, match_pos)
  
  @classmethod
  def simple_rle_encode(cls, uncomp, uncomp_offset, search_depth=DEFAULT_SEARCH_DEPTH):
    start_offset = uncomp_offset - search_depth
    if start_offset < 0:
      start_offset = 0
    
    num_bytes = 0
    match_pos = None
    max_num_bytes_to_check = len(uncomp) - uncomp_offset
    if max_num_bytes_to_check > cls.MAX_RUN_LENGTH:
      max_num_bytes_to_check = cls.MAX_RUN_LENGTH
    
    for possible_match_pos in range(start_offset, uncomp_offset):
      for index_in_match in range(max_num_bytes_to_check):
        if uncomp[possible_match_pos + index_in_match] != uncomp[uncomp_offset + index_in_match]:
          break
        
        num_bytes_matched = index_in_match + 1
        if num_bytes_matched > num_bytes:
          num_bytes = num_bytes_matched
          match_pos = possible_match_pos
    
    return (num_bytes, match_pos)

class Yaz0(Yaz0Yay0):
  MAGIC_BYTES = b"Yaz0"
  
  # Variables to hold the reserved next match across loops.
  next_num_bytes = 0
  next_match_pos = 0
  next_flag = False
  
  @classmethod
  def decompress(cls, comp_data):
    if not cls.check_is_compressed(comp_data):
      print("File is not compressed.")
      return comp_data
    
    if PY_FAST_YAZ0_YAY0_INSTALLED:
      comp_data = fs.read_all_bytes(comp_data)
      uncomp_data = pyfastyaz0yay0.decompress_yaz0(comp_data)
      uncomp_data = BytesIO(uncomp_data)
      return uncomp_data
    
    uncomp_size = fs.read_u32(comp_data, 4)
    
    comp = fs.read_all_bytes(comp_data)
    
    output = []
    output_len = 0
    src_offset = 0x10
    mask_bits_left = 0
    mask = 0
    while output_len < uncomp_size:
      if mask_bits_left == 0:
        mask = comp[src_offset]
        src_offset += 1
        mask_bits_left = 8
      
      if mask & 0x80 != 0:
        output.append(comp[src_offset])
        src_offset += 1
        output_len += 1
      else:
        byte1 = comp[src_offset]
        byte2 = comp[src_offset+1]
        src_offset += 2
        
        dist = ((byte1&0xF) << 8) | byte2
        copy_src_offset = output_len - (dist + 1)
        num_bytes = (byte1 >> 4)
        if num_bytes == 0:
          num_bytes = comp[src_offset] + 0x12
          src_offset += 1
        else:
          num_bytes += 2
        
        for i in range(0, num_bytes):
          output.append(output[copy_src_offset])
          output_len += 1
          copy_src_offset += 1
      
      mask = (mask << 1)
      mask_bits_left -= 1
    
    uncomp_data = bytes(output)
    
    return BytesIO(uncomp_data)
  
  @classmethod
  def compress(cls, uncomp_data, search_depth=Yaz0Yay0.DEFAULT_SEARCH_DEPTH, should_pad_data=False):
    if PY_FAST_YAZ0_YAY0_INSTALLED:
      uncomp_data = fs.read_all_bytes(uncomp_data)
      comp_data = pyfastyaz0yay0.compress_yaz0(uncomp_data, search_depth)
      comp_data = BytesIO(comp_data)
      if should_pad_data:
        fs.align_data_to_nearest(comp_data, 0x20, padding_bytes=b'\0')
      return comp_data
    
    comp_data = BytesIO()
    fs.write_magic_str(comp_data, 0, "Yaz0", 4)
    
    uncomp_size = fs.data_len(uncomp_data)
    fs.write_u32(comp_data, 4, uncomp_size)
    
    fs.write_u32(comp_data, 8, 0)
    fs.write_u32(comp_data, 0xC, 0)
    
    cls.next_num_bytes = 0
    cls.next_match_pos = None
    cls.next_flag = False
    
    uncomp_offset = 0
    uncomp = fs.read_all_bytes(uncomp_data)
    comp_offset = 0x10
    dst = []
    mask_bits_done = 0
    mask = 0
    while uncomp_offset < uncomp_size:
      num_bytes, match_pos = cls.get_num_bytes_and_match_pos(uncomp, uncomp_offset, search_depth=search_depth)
      
      if num_bytes < 3:
        # Copy the byte directly
        dst.append(uncomp[uncomp_offset])
        uncomp_offset += 1
        
        mask |= (0x80 >> mask_bits_done)
      else:
        dist = (uncomp_offset - match_pos - 1)
        
        if num_bytes >= 0x12:
          dst.append((dist & 0xFF00) >> 8)
          dst.append((dist & 0x00FF))
          
          if num_bytes > cls.MAX_RUN_LENGTH:
            num_bytes = cls.MAX_RUN_LENGTH
          dst.append(num_bytes - 0x12)
        else:
          byte = (((num_bytes - 2) << 4) | (dist >> 8) & 0x0F)
          dst.append(byte)
          dst.append(dist & 0xFF)
        
        uncomp_offset += num_bytes
      
      mask_bits_done += 1
      
      if mask_bits_done == 8:
        # Filled up the mask, so write this block.
        fs.write_u8(comp_data, comp_offset, mask)
        comp_offset += 1
        
        for byte in dst:
          fs.write_u8(comp_data, comp_offset, byte)
          comp_offset += 1
        
        mask = 0
        mask_bits_done = 0
        dst = []
    
    if mask_bits_done > 0:
      # Still some mask bits left over that weren't written yet, so write them now.
      fs.write_u8(comp_data, comp_offset, mask)
      comp_offset += 1
      
      for byte in dst:
        fs.write_u8(comp_data, comp_offset, byte)
        comp_offset += 1
    else:
      # If there are no mask bits left to flush, we instead write a single zero at the end for some reason.
      # I don't think it's necessary in practice, but we do it for maximum accuracy with the original algorithm.
      fs.write_u8(comp_data, comp_offset, 0)
      comp_offset += 1
    
    if should_pad_data:
      fs.align_data_to_nearest(comp_data, 0x20, padding_bytes=b'\0')
    
    return comp_data

class Yay0(Yaz0Yay0):
  MAGIC_BYTES = b"Yay0"
  
  # Variables to hold the reserved next match across loops.
  next_num_bytes = 0
  next_match_pos = 0
  next_flag = False
  
  @classmethod
  def decompress(cls, comp_data):
    if not cls.check_is_compressed(comp_data):
      print("File is not compressed.")
      return comp_data
    
    if PY_FAST_YAZ0_YAY0_INSTALLED:
      comp_data = fs.read_all_bytes(comp_data)
      uncomp_data = pyfastyaz0yay0.decompress_yay0(comp_data)
      uncomp_data = BytesIO(uncomp_data)
      return uncomp_data
    
    uncomp_size = fs.read_u32(comp_data, 4)
    link_offset = fs.read_u32(comp_data, 8)
    chunk_offset = fs.read_u32(comp_data, 0xC)
    mask_offset = 0x10
    
    output = []
    output_len = 0
    mask_bits_left = 0
    mask = 0
    while output_len < uncomp_size:
      if mask_bits_left == 0:
        mask = fs.read_u32(comp_data, mask_offset)
        mask_offset += 4
        mask_bits_left = 32
      
      if mask & 0x80000000 != 0:
        output.append(fs.read_u8(comp_data, chunk_offset))
        chunk_offset += 1
        output_len += 1
      else:
        link = fs.read_u16(comp_data, link_offset)
        link_offset += 2
        
        dist = link & 0x0FFF
        copy_src_offset = output_len - (dist + 1)
        num_bytes = (link >> 12)
        
        if num_bytes == 0:
          num_bytes = fs.read_u8(comp_data, chunk_offset) + 0x12
          chunk_offset += 1
        else:
          num_bytes += 2
        
        for i in range(num_bytes):
          output.append(output[copy_src_offset])
          output_len += 1
          copy_src_offset += 1
      
      mask <<= 1
      mask_bits_left -= 1
    
    uncomp_data = bytes(output)
    
    return BytesIO(uncomp_data)
  
  @classmethod
  def compress(cls, uncomp_data, search_depth=Yaz0Yay0.DEFAULT_SEARCH_DEPTH, should_pad_data=False):
    if PY_FAST_YAZ0_YAY0_INSTALLED:
      uncomp_data = fs.read_all_bytes(uncomp_data)
      comp_data = pyfastyaz0yay0.compress_yay0(uncomp_data, search_depth)
      comp_data = BytesIO(comp_data)
      if should_pad_data:
        fs.align_data_to_nearest(comp_data, 0x20, padding_bytes=b'\0')
      return comp_data
    
    uncomp_size = fs.data_len(uncomp_data)
    
    cls.next_num_bytes = 0
    cls.next_match_pos = None
    cls.next_flag = False
    
    mask_data = BytesIO()
    link_data = BytesIO()
    chunk_data = BytesIO()
    mask_offset = 0
    link_offset = 0
    chunk_offset = 0
    
    uncomp_offset = 0
    uncomp = fs.read_all_bytes(uncomp_data)
    curr_chunk = []
    mask_bits_done = 0
    mask = 0
    while uncomp_offset < uncomp_size:
      num_bytes, match_pos = cls.get_num_bytes_and_match_pos(uncomp, uncomp_offset, search_depth=search_depth)
      
      if num_bytes < 3:
        # Copy the byte directly
        curr_chunk.append(uncomp[uncomp_offset])
        uncomp_offset += 1
        
        mask |= (0x80000000 >> mask_bits_done)
      else:
        dist = (uncomp_offset - match_pos - 1)
        link = (dist & 0x0FFF)
        
        if num_bytes >= 0x12:
          if num_bytes > cls.MAX_RUN_LENGTH:
            num_bytes = cls.MAX_RUN_LENGTH
          curr_chunk.append(num_bytes - 0x12)
        else:
          link |= (num_bytes - 2) << 12
        
        fs.write_u16(link_data, link_offset, link)
        link_offset += 2
        
        uncomp_offset += num_bytes
      
      mask_bits_done += 1
      
      if mask_bits_done == 32:
        # Filled up the mask, so write this block.
        fs.write_u32(mask_data, mask_offset, mask)
        mask_offset += 4
        
        for byte in curr_chunk:
          fs.write_u8(chunk_data, chunk_offset, byte)
          chunk_offset += 1
        
        mask = 0
        mask_bits_done = 0
        curr_chunk = []
    
    if mask_bits_done > 0:
      # Still some mask bits left over that weren't written yet, so write them now.
      fs.write_u32(mask_data, mask_offset, mask)
      mask_offset += 4
      
      for byte in curr_chunk:
        fs.write_u8(chunk_data, chunk_offset, byte)
        chunk_offset += 1
    
    comp_data = BytesIO()
    fs.write_magic_str(comp_data, 0, "Yay0", 4)
    fs.write_u32(comp_data, 4, uncomp_size)
    
    mask_location = 0x10
    mask_bytes = fs.read_all_bytes(mask_data)
    fs.write_bytes(comp_data, mask_location, mask_bytes)
    
    link_location = mask_location + len(mask_bytes)
    link_bytes = fs.read_all_bytes(link_data)
    fs.write_bytes(comp_data, link_location, link_bytes)
    fs.write_u32(comp_data, 8, link_location)
    
    chunk_location = link_location + len(link_bytes)
    chunk_bytes = fs.read_all_bytes(chunk_data)
    fs.write_bytes(comp_data, chunk_location, chunk_bytes)
    fs.write_u32(comp_data, 0xC, chunk_location)
    
    if should_pad_data:
      fs.align_data_to_nearest(comp_data, 0x20, padding_bytes=b'\0')
    
    return comp_data
