from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.jchunk import JChunk
from gclib.bunfoe import bunfoe, field, BUNFOE

class INF1NodeType(u16, Enum):
  FINISH      = 0x00
  OPEN_CHILD  = 0x01
  CLOSE_CHILD = 0x02
  JOINT       = 0x10
  MATERIAL    = 0x11
  SHAPE       = 0x12

class INF1MatrixScalingRule(u8, Enum):
  BASIC     = 0x00
  SOFTIMAGE = 0x01
  MAYA      = 0x02

@bunfoe
class INF1Node(BUNFOE):
  DATA_SIZE = 4
  
  type: INF1NodeType
  index: u16
  
  parent: 'INF1Node' = field(default=None, repr=False, compare=False, ignore=True)
  children: list['INF1Node'] = field(default_factory=list, repr=False, compare=False, ignore=True)

@bunfoe
class INF1(JChunk):
  load_flags           : u16                   = field(bitfield=True)
  matrix_scaling_rule  : INF1MatrixScalingRule = field(bits=4)
  unknown_load_flags   : u16                   = field(bits=12)
  _padding             : u16
  mtx_group_count      : u32
  vertex_count         : u32
  hierarchy_data_offset: u32
  
  def read_chunk_specific_data(self):
    BUNFOE.read(self, 0)
    
    offset = self.hierarchy_data_offset
    self.flat_hierarchy: list[INF1Node] = []
    while True:
      if offset >= self.size:
        raise Exception("No INF1 end node found")
      
      node = INF1Node(self.data)
      node.read(offset)
      self.flat_hierarchy.append(node)
      offset += INF1Node.DATA_SIZE
      
      if node.type == INF1NodeType.FINISH:
        break
    
    self.build_scene_graph_recursive()
    # self.print_hierarchy_recursive([self.flat_hierarchy[0]])
  
  def build_scene_graph_recursive(self, parent_node: INF1Node = None, start_i: int = 0):
    if parent_node is not None:
      assert parent_node.type in [INF1NodeType.JOINT, INF1NodeType.MATERIAL, INF1NodeType.SHAPE]
    i = start_i
    prev_node = None
    while i < len(self.flat_hierarchy):
      node = self.flat_hierarchy[i]
      i += 1
      
      if node.type in [INF1NodeType.JOINT, INF1NodeType.MATERIAL, INF1NodeType.SHAPE]:
        prev_node = node
        if parent_node is not None:
          parent_node.children.append(node)
      elif node.type == INF1NodeType.OPEN_CHILD:
        assert prev_node is not None
        i = self.build_scene_graph_recursive(prev_node, i)
        if i == -1:
          return -1
      elif node.type == INF1NodeType.CLOSE_CHILD:
        return i
      elif node.type == INF1NodeType.FINISH:
        assert i == len(self.flat_hierarchy)
        return -1
    
    return i
  
  def print_hierarchy_recursive(self, nodes, indent=0):
    for node in nodes:
      print(("  "*indent) + "%s %X" % (node.type.name, node.index))
      self.print_hierarchy_recursive(node.children, indent=indent+1)
  
  def save_chunk_specific_data(self):
    BUNFOE.save(self, 0)
    
    offset = self.hierarchy_data_offset
    for node in self.flat_hierarchy:
      node.save(offset)
      offset += INF1Node.DATA_SIZE
