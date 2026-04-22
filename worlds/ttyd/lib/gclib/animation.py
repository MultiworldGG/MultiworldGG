from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr

class LoopMode(u8, Enum):
  ONCE = 0
  ONCE_AND_RESET = 1
  REPEAT = 2
  MIRRORED_ONCE = 3
  MIRRORED_REPEAT = 4

class TangentType(Enum):
  IN     =   0
  IN_OUT =   1

class AnimationKeyframe:
  def __init__(self, time, value, tangent_in, tangent_out):
    self.time = time
    self.value = value
    self.tangent_in = tangent_in
    self.tangent_out = tangent_out

class AnimationTrack:
  DATA_SIZE = 6
  
  def __init__(self):
    self.tangent_type = TangentType.IN_OUT
    self.keyframes = []
  
  def read(self, data, offset, track_data):
    self.count = fs.read_u16(data, offset+0)
    self.index = fs.read_u16(data, offset+2)
    self.tangent_type = TangentType(fs.read_u16(data, offset+4))
    
    self.keyframes = []
    if self.count == 1:
      keyframe = AnimationKeyframe(0, track_data[self.index], 0, 0)
      self.keyframes.append(keyframe)
    else:
      if self.tangent_type == TangentType.IN:
        for i in range(self.index, self.index + self.count*3, 3):
          keyframe = AnimationKeyframe(track_data[i+0], track_data[i+1], track_data[i+2], track_data[i+2])
          self.keyframes.append(keyframe)
      elif self.tangent_type == TangentType.IN_OUT:
        for i in range(self.index, self.index + self.count*4, 4):
          keyframe = AnimationKeyframe(track_data[i+0], track_data[i+1], track_data[i+2], track_data[i+3])
          self.keyframes.append(keyframe)
      else:
        raise Exception("Invalid tangent type")
  
  def save(self, data, offset, track_data):
    self.count = len(self.keyframes)
    
    this_track_data = []
    
    if self.count == 1:
      this_track_data.append(self.keyframes[0].value)
    else:
      if self.tangent_type == TangentType.IN:
        for keyframe in self.keyframes:
          this_track_data.append(keyframe.time)
          this_track_data.append(keyframe.value)
          this_track_data.append(keyframe.tangent_in)
      elif self.tangent_type == TangentType.IN_OUT:
        for keyframe in self.keyframes:
          this_track_data.append(keyframe.time)
          this_track_data.append(keyframe.value)
          this_track_data.append(keyframe.tangent_in)
          this_track_data.append(keyframe.tangent_out)
      else:
        raise Exception("Invalid tangent type")
    
    self.index = None
    # Try to find if this track's data is already in the full track list to avoid duplicating data.
    # Note: This deduplication is not entirely accurate to how the vanilla files deduplicated data.
    # Vanilla files did deduplicate data somewhat, but not all of it, resulting in repacked files being smaller than vanilla.
    # It's not currently known exactly how Nintendo's tools determined which data should be deduplicated.
    for i in range(len(track_data) - len(this_track_data) + 1):
      found_match = True
      
      for j in range(len(this_track_data)):
        if track_data[i+j] != this_track_data[j]:
          found_match = False
          break
      
      if found_match:
        self.index = i
        break
    
    if self.index is None:
      # If this data isn't already in the list, we append it to the end.
      self.index = len(track_data)
      track_data += this_track_data
    
    fs.write_u16(data, offset+0, self.count)
    fs.write_u16(data, offset+2, self.index)
    fs.write_u16(data, offset+4, self.tangent_type.value)

class Animation:
  def __init__(self):
    self.tracks = {}
  
  def read_track(self, track_name, data, offset, track_data):
    self.tracks[track_name] = AnimationTrack()
    self.tracks[track_name].read(data, offset, track_data)
    offset += AnimationTrack.DATA_SIZE
    return offset
  
  def save_track(self, track_name, data, offset, track_data):
    self.tracks[track_name].save(data, offset, track_data)
    offset += AnimationTrack.DATA_SIZE
    return offset
  
  def __getattr__(self, attr_name):
    if attr_name != "tracks" and attr_name in self.tracks:
      return self.tracks[attr_name]
    else:
      return super(self.__class__, self).__getattribute__(attr_name)
