from io import BytesIO

from gclib.yaz0_yay0 import Yaz0, Yay0

class GCLibFileEntry:
  data: BytesIO
  
  def __init__(self):
    self.data = BytesIO()
  
  def decompress_data_if_necessary(self) -> bool:
    if Yaz0.check_is_compressed(self.data):
      self.data = Yaz0.decompress(self.data)
      return True
    elif Yay0.check_is_compressed(self.data):
      self.data = Yay0.decompress(self.data)
      return True
    return False

class GCLibFile:
  """A generic parent class to handle initializing from multiple possible data sources.
  
  It can handle receiving binary data from a FileEntry (e.g. from inside of a RARC), from a BytesIO,
  reading from a given file path, or not receiving any initial data, instead creating a new file
  from scratch.
  
  It also automatically decompresses the data, if it detects it was compressed.
  """
  
  data: BytesIO
  file_entry: GCLibFileEntry | None
  
  def __init__(self, flexible_data: GCLibFileEntry | BytesIO | str | None = None):
    if isinstance(flexible_data, GCLibFileEntry):
      self.file_entry = flexible_data
      self.file_entry.decompress_data_if_necessary()
      self.data = self.file_entry.data
      return
    else:
      self.file_entry = None
    
    if isinstance(flexible_data, BytesIO):
      self.data = flexible_data
    elif isinstance(flexible_data, str):
      with open(flexible_data, "rb") as f:
        self.data = BytesIO(f.read())
    elif flexible_data is None:
      self.data = BytesIO()
    else:
      raise TypeError(f"Unsupported init argument type to GCLibFile: {type(flexible_data)}")
    
    if Yaz0.check_is_compressed(self.data):
      self.data = Yaz0.decompress(self.data)
    elif Yay0.check_is_compressed(self.data):
      self.data = Yay0.decompress(self.data)
