from enum import Enum
from io import BytesIO
import math
import numpy as np

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import BUNFOE, bunfoe, field
from gclib.bunfoe_types import RGBAu8
from gclib.jchunk import JChunk
import gclib.gx_enums as GX
from gclib.gx_enums import MDLCommandType, BPRegister, XFRegister
from gclib.j3d_chunks.mat3 import MAT3, Material, TexMatrix, TexMtxProjection
from gclib.j3d_chunks.tex1 import TEX1
import gclib.j3d_chunks.bp_command as BP
import gclib.j3d_chunks.xf_command as XF

@bunfoe
class MDLEntry(BUNFOE):
  bp_commands: list[BP.BPCommand] = field(default_factory=list)
  xf_commands: list[XF.XFCommand] = field(default_factory=list)
  
  def __post_init__(self):
    super().__post_init__()
    
    self.chan_color_subpacket_offset = None
    self.chan_control_subpacket_offset = None
    self.tex_gen_subpacket_offset = None
    self.texture_subpacket_offset = None
    self.tev_subpacket_offset = None
    self.pixel_subpacket_offset = None
    
    self.unknown_float_1 = 0.029761791229248
    self.unknown_float_2 = 0.025384426116943
    
    self.pixel_engine_mode = GX.PixelEngineMode.Opaque
  
  def read(self, offset: int, size: int) -> int:
    self.bp_commands.clear()
    self.xf_commands.clear()
    
    orig_offset = offset
    while offset < orig_offset+size:
      command_type = fs.read_u8(self.data, offset)
      if command_type == MDLCommandType.BP.value:
        register = BPRegister(fs.read_u8(self.data, offset+1))
        command = BP.BPCommand.new_from_register(register, self.data)
        offset = command.read(offset)
        self.bp_commands.append(command)
      elif command_type == MDLCommandType.XF.value:
        register = XFRegister(fs.read_u16(self.data, offset+3))
        command = XF.XFCommand.new_from_register(register, self.data)
        offset = command.read(offset)
        self.xf_commands.append(command)
      elif command_type == MDLCommandType.END_MARKER.value:
        break
      else:
        raise Exception("Invalid MDL3 command type: %02X" % command_type)
    
    return offset
  
  def save(self, offset: int):
    orig_offset = offset
    
    self.chan_color_subpacket_offset = None
    self.chan_control_subpacket_offset = None
    self.tex_gen_subpacket_offset = None
    self.texture_subpacket_offset = None # TODO
    self.tev_subpacket_offset = None
    self.pixel_subpacket_offset = None
    
    for command in self.bp_commands:
      if self.tev_subpacket_offset is None and (isinstance(command, BP.TEV_REGISTERL) or isinstance(command, BP.TEV_REGISTERH)):
        self.tev_subpacket_offset = offset - orig_offset
      if self.pixel_subpacket_offset is None and command.register in [BPRegister.TEV_FOG_PARAM_0, BPRegister.TEV_FOG_PARAM_1, BPRegister.TEV_FOG_PARAM_2, BPRegister.TEV_FOG_PARAM_3]:
        self.pixel_subpacket_offset = offset - orig_offset
      
      offset = command.save(offset)
    
    for command in self.xf_commands:
      if self.chan_color_subpacket_offset is None and command.register in [XFRegister.CHAN0_AMBCOLOR, XFRegister.CHAN0_MATCOLOR]:
        self.chan_color_subpacket_offset = offset - orig_offset
      if self.chan_control_subpacket_offset is None and command.register in [XFRegister.CHAN0_COLOR]:
        self.chan_control_subpacket_offset = offset - orig_offset
      if self.tex_gen_subpacket_offset is None and (isinstance(command, XF.TEXMTX) or command.register in [XFRegister.TEXMTXINFO]):
        self.tex_gen_subpacket_offset = offset - orig_offset
      
      offset = command.save(offset)
    
    if offset % 0x20 != 0:
      padding_bytes_needed = (0x20 - (offset % 0x20))
      padding = b"\0"*padding_bytes_needed
      fs.write_bytes(self.data, offset, padding)
      offset += padding_bytes_needed
    
    return offset
  
  def generate_from_material(self, mat: Material, tex1: TEX1):
    self.bp_commands.clear()
    self.xf_commands.clear()
    
    for i, texture_index in enumerate(mat.textures):
      if texture_index is None:
        continue
      tex = tex1.textures[texture_index]
      self.bp_commands.append(BP.TX_SETIMAGE3(
        reg_index=i,
        texture_index=texture_index,
      ))
      self.bp_commands.append(BP.TX_SETIMAGE0(
        reg_index=i,
        width_minus_1=tex.width-1,
        height_minus_1=tex.height-1,
        format=tex.image_format,
      ))
      mag_filter = tex.mag_filter
      if mag_filter != GX.FilterMode.Linear:
        mag_filter = GX.FilterMode.Nearest
      min_filter = BP.MDLFilterMode[tex.min_filter.name]
      lod_bias = int(tex.lod_bias * 0.01 * 32.0) & 0xFF
      self.bp_commands.append(BP.TX_SETMODE0(
        reg_index=i,
        wrap_s=tex.wrap_s, wrap_t=tex.wrap_t,
        mag_filter=mag_filter, min_filter=min_filter,
        diag_lod=True, # TODO: invert BTI field 0x11
        lod_bias=lod_bias,
        max_aniso=0, # TODO: BTI field 0x13
        lod_clamp=False, # TODO: BTI field 0x12
      ))
      self.bp_commands.append(BP.TX_SETMODE1(
        reg_index=i,
        min_lod=tex.min_lod*2, max_lod=tex.max_lod*2,
      ))
      
      tex = tex1.textures[texture_index]
      if not tex.needs_palettes():
        continue
      self.bp_commands.append(BP.BP_MASK(
        register=BPRegister.BP_MASK,
        mask=0xFFFF00,
      ))
      self.bp_commands.append(BP.IND_IMASK(
        register=BPRegister.IND_IMASK,
        mask=0,
      ))
      # https://github.com/dolphin-emu/dolphin/blob/6309aa00109f81a2e9f2281d1fced174eccef8f8/Source/Core/VideoCommon/BPStructs.cpp#L388
      # src << 5
      # tmem_addr << 9
      # tmem_line_count * 32
      # tmem_offset << 9
      self.bp_commands.append(BP.TEX_LOADTLUT0(
        register=BPRegister.TEX_LOADTLUT0,
        src=0, # This is the physical address of the TLUT in RAM. (i.e. The virtual address minus 0x80000000.)
      ))
      tmem_addr = (((i << 13) + 0xF0000 - 0x80000) >> 9)
      tmem_line_count = 1
      if tex.num_colors > 16:
        tmem_line_count = 16
      self.bp_commands.append(BP.TEX_LOADTLUT1(
        register=BPRegister.TEX_LOADTLUT1,
        tmem_addr=tmem_addr, tmem_line_count=tmem_line_count,
      ))
      self.bp_commands.append(BP.BP_MASK(
        register=BPRegister.BP_MASK,
        mask=0xFFFF00,
      ))
      self.bp_commands.append(BP.IND_IMASK(
        register=BPRegister.IND_IMASK,
        mask=0,
      ))
      self.bp_commands.append(BP.TX_LOADTLUT(
        reg_index=i,
        tmem_offset=tmem_addr, format=tex.palette_format, # TODO
      ))
    
    ras1_cmd = None
    cmds_for_order_pair = None
    either_order_exists = False
    for i, tev_order in enumerate(mat.tev_orders):
      if i % 2 == 0:
        ras1_cmd = BP.RAS1_TREF(
          reg_index=i//2,
          tex_map_0=GX.TexMapID.TEXMAP7, tex_map_1=GX.TexMapID.TEXMAP7,
          # This channel_id_1 value can different from the ones from the original game if the
          # material has an odd number of TEV orders. This is because the RAS1_TREF command includes
          # a pair of TEV orders, even if the second one doesn't actually exist, and a bug in the
          # code causes it to do an out-of-bounds read to get the next TEV order if the second one
          # doesn't actually exist. Known values that can appear here are:
          # 0x00 (COLOR0) and 0x07 (COLOR_ZERO)
          channel_id_0=BP.MDLColorChannelID.COLOR0, channel_id_1=BP.MDLColorChannelID.COLOR0,
        )
        cmds_for_order_pair = []
        either_order_exists = False
      
      if tev_order is None:
        tex_index = 7
        tex_width = 1
        tex_height = 1
      else:
        either_order_exists = True
        
        if tev_order.tex_coord_id == GX.TexCoordID.TEXCOORD_NULL:
          # TODO: not sure if this is correct or a hack
          tex_index = 7
          tex_width = 1
          tex_height = 1
        else:
          tex_index = tev_order.tex_coord_id.value
          tex = tex1.textures[mat.textures[tex_index]] # TODO unsure
          tex_width = tex.width
          tex_height = tex.height
        
        tex_map_id = GX.TexMapID(tev_order.tex_map_id & 0x07)
        enable = tev_order.tex_map_id != GX.TexMapID.TEXMAP_NULL and (tev_order.tex_map_id & 0x100) == 0
        if tev_order.tex_coord_id > GX.TexCoordID.TEXCOORD7:
          tex_coord_id = GX.TexCoordID.TEXCOORD0
        else:
          tex_coord_id = GX.TexCoordID(tev_order.tex_coord_id & 0x07)
        channel_id = BP.MDLColorChannelID[tev_order.channel_id.name]
        if i % 2 == 0:
          ras1_cmd.tex_map_0 = tex_map_id
          ras1_cmd.tex_coord_0 = tex_coord_id
          ras1_cmd.enable_0 = enable
          ras1_cmd.channel_id_0 = channel_id
        else:
          ras1_cmd.tex_map_1 = tex_map_id
          ras1_cmd.tex_coord_1 = tex_coord_id
          ras1_cmd.enable_1 = enable
          ras1_cmd.channel_id_1 = channel_id
      
      cmds_for_order_pair.append(BP.BP_MASK(
        register=BPRegister.BP_MASK,
        mask=0x03FFFF,
      ))
      cmds_for_order_pair.append(BP.SU_SSIZE(
        reg_index=tex_index,
        width_minus_1=tex_width-1,
      ))
      cmds_for_order_pair.append(BP.SU_TSIZE(
        reg_index=tex_index,
        height_minus_1=tex_height-1,
      ))
      
      if i % 2 == 1 and either_order_exists:
        self.bp_commands.append(ras1_cmd)
        self.bp_commands += cmds_for_order_pair
    
    for i, color in enumerate(mat.tev_colors):
      # TODO: what is with this i==3, i+1 stuff?
      if i == 3:
        continue
      self.bp_commands.append(BP.TEV_REGISTERL(
        reg_index=i+1,
        r=color.r&0x7FF, a=color.a&0x7FF, is_konst=False,
      ))
      self.bp_commands.append(BP.TEV_REGISTERH(
        reg_index=i+1,
        g=color.g&0x7FF, b=color.b&0x7FF, is_konst=False,
      ))
      self.bp_commands.append(self.bp_commands[-1].copy())
      self.bp_commands.append(self.bp_commands[-1].copy())
    
    for i, color in enumerate(mat.tev_konst_colors):
      self.bp_commands.append(BP.TEV_REGISTERL(
        reg_index=i,
        r=color.r, a=color.a, is_konst=True,
      ))
      self.bp_commands.append(BP.TEV_REGISTERH(
        reg_index=i,
        g=color.g, b=color.b, is_konst=True,
      ))
    
    for i, (tev_stage, swap_mode, ind_tev_stage) in enumerate(zip(mat.tev_stages, mat.tev_swap_modes, mat.tex_indirect.tev_stages)):
      if tev_stage is None or swap_mode is None:
        continue
      self.bp_commands.append(BP.TEV_COLOR_ENV(
        reg_index=i,
        color_in_a=tev_stage.color_in_a, color_in_b=tev_stage.color_in_b,
        color_in_c=tev_stage.color_in_c, color_in_d=tev_stage.color_in_d,
        color_op=GX.TevOp(tev_stage.color_op&0x01), color_bias=tev_stage.color_bias,
        color_scale=tev_stage.color_scale, color_clamp=tev_stage.color_clamp,
        color_reg_id=tev_stage.color_reg_id,
      ))
      self.bp_commands.append(BP.TEV_ALPHA_ENV(
        reg_index=i,
        alpha_in_a=tev_stage.alpha_in_a, alpha_in_b=tev_stage.alpha_in_b,
        alpha_in_c=tev_stage.alpha_in_c, alpha_in_d=tev_stage.alpha_in_d,
        alpha_op=GX.TevOp(tev_stage.alpha_op&0x01), alpha_bias=tev_stage.alpha_bias,
        alpha_scale=tev_stage.alpha_scale, alpha_clamp=tev_stage.alpha_clamp,
        alpha_reg_id=tev_stage.alpha_reg_id,
        ras_sel=swap_mode.ras_sel, tex_sel=swap_mode.tex_sel,
      ))
      self.bp_commands.append(BP.IND_CMD(
        reg_index=i,
        tev_stage=ind_tev_stage.tev_stage, format=ind_tev_stage.format,
        bias_sel=ind_tev_stage.bias_sel, alpha_sel=ind_tev_stage.alpha_sel,
        mtx_sel=ind_tev_stage.mtx_sel, wrap_s=ind_tev_stage.wrap_s, wrap_t=ind_tev_stage.wrap_t,
        utc_lod=ind_tev_stage.utc_lod, add_prev=ind_tev_stage.add_prev,
      ))
    
    ksel_cmds: list[BP.TEV_KSEL] = []
    for i, (color_sel, alpha_sel) in enumerate(zip(mat.tev_konst_color_sels, mat.tev_konst_alpha_sels)):
      if i % 2 == 0:
        ksel_cmd = BP.TEV_KSEL(reg_index=i//2)
        ksel_cmd.color_sel_0 = color_sel
        ksel_cmd.alpha_sel_0 = alpha_sel
        ksel_cmds.append(ksel_cmd)
      else:
        ksel_cmd = ksel_cmds[i//2]
        ksel_cmd.color_sel_1 = color_sel
        ksel_cmd.alpha_sel_1 = alpha_sel
    
    for i, swap_mode_table in enumerate(mat.tev_swap_mode_tables[:4]):
      ksel_cmd = ksel_cmds[i*2+0]
      if swap_mode_table is None:
        # Note: The original code read out of bounds in this case. We don't emulate this.
        ksel_cmd.r_or_b = 0
        ksel_cmd.g_or_a = 1
      else:
        ksel_cmd.r_or_b = swap_mode_table.r
        ksel_cmd.g_or_a = swap_mode_table.g
      self.bp_commands.append(ksel_cmd)
      ksel_cmd = ksel_cmds[i*2+1]
      if swap_mode_table is None:
        # Note: The original code read out of bounds in this case. We don't emulate this.
        ksel_cmd.r_or_b = 2
        ksel_cmd.g_or_a = 3
      else:
        ksel_cmd.r_or_b = swap_mode_table.b
        ksel_cmd.g_or_a = swap_mode_table.a
      self.bp_commands.append(ksel_cmd)
    
    if mat.tex_indirect.enable:
      assert mat.tex_indirect.num_ind_tex_stages >= 1
      assert mat.tex_indirect.num_ind_tex_stages <= len(mat.tex_indirect.tex_matrixes)
      for i in range(mat.tex_indirect.num_ind_tex_stages):
        ind_tex_mtx = mat.tex_indirect.tex_matrixes[i]
        ma = int(ind_tex_mtx.matrix.r0[0] * 1024.0) & 0x7FF
        mb = int(ind_tex_mtx.matrix.r1[0] * 1024.0) & 0x7FF
        mc = int(ind_tex_mtx.matrix.r0[1] * 1024.0) & 0x7FF
        md = int(ind_tex_mtx.matrix.r1[1] * 1024.0) & 0x7FF
        me = int(ind_tex_mtx.matrix.r0[2] * 1024.0) & 0x7FF
        mf = int(ind_tex_mtx.matrix.r1[2] * 1024.0) & 0x7FF
        scale_exp = ind_tex_mtx.scale_exponent + 17
        
        self.bp_commands.append(BP.IND_MTXA(
          reg_index=i,
          ma=ma, mb=mb, s0=(scale_exp >> 0) & 3,
        ))
        self.bp_commands.append(BP.IND_MTXB(
          reg_index=i,
          mc=mc, md=md, s1=(scale_exp >> 2) & 3,
        ))
        self.bp_commands.append(BP.IND_MTXC(
          reg_index=i,
          me=me, mf=mf, s2=(scale_exp >> 4) & 3,
        ))
    
    if mat.tex_indirect.enable:
      for i in range(0, mat.tex_indirect.num_ind_tex_stages, 2):
        ind_tex_scale_0 = mat.tex_indirect.scales[i+0]
        ind_tex_scale_1 = mat.tex_indirect.scales[i+1]
        self.bp_commands.append(BP.RAS1_SS0(
          reg_index=i//2,
          scale_s_0=ind_tex_scale_0.scale_s, scale_t_0=ind_tex_scale_0.scale_t,
          scale_s_1=ind_tex_scale_1.scale_s, scale_t_1=ind_tex_scale_1.scale_t,
        ))
    
    for i in range(4):
      self.bp_commands.append(BP.BP_MASK(
        register=BPRegister.BP_MASK,
        mask=0x03FFFF,
      ))
      
      tev_order = mat.tex_indirect.tev_orders[i]
      if tev_order.tex_coord_id == GX.TexCoordID.TEXCOORD_NULL:
        # Reproduces a bug in the original code.
        # The calculation for which registers to use work like this:
        # 0x30 + id * 2
        # 0x31 + id * 2
        # Where 0x30 is SU_SSIZE0 and 0x31 is SU_TSIZE0.
        # When the tex coord ID is NULL (0xFF), the calculation winds up like this:
        # 0x30 + 0xFF * 2 = 0x22E = (u8)0x2E = RAS1_TREF6
        # 0x31 + 0xFF * 2 = 0x22F = (u8)0x2F = RAS1_TREF7
        # So to emulate this, we add the bugged RAS1_TREF commands.
        self.bp_commands.append(BP.RAS1_TREF(
          reg_index=6,
          channel_id_0=BP.MDLColorChannelID.COLOR0, channel_id_1=BP.MDLColorChannelID.COLOR0,
        ))
        self.bp_commands.append(BP.RAS1_TREF(
          reg_index=7,
          channel_id_0=BP.MDLColorChannelID.COLOR0, channel_id_1=BP.MDLColorChannelID.COLOR0,
        ))
      else:
        tex_index = tev_order.tex_coord_id.value
        tex = tex1.textures[mat.textures[tex_index]] # TODO unsure
        tex_width = tex.width
        tex_height = tex.height
        
        self.bp_commands.append(BP.SU_SSIZE(
          reg_index=tev_order.tex_coord_id,
          width_minus_1=tex_width-1,
        ))
        self.bp_commands.append(BP.SU_TSIZE(
          reg_index=tev_order.tex_coord_id,
          height_minus_1=tex_height-1,
        ))
    
    tev_orders = mat.tex_indirect.tev_orders
    self.bp_commands.append(BP.RAS1_IREF(
      register=BPRegister.RAS1_IREF,
      tex_coord_id_0=GX.TexCoordID(tev_orders[0].tex_coord_id&0x07), tex_map_id_0=GX.TexMapID(tev_orders[0].tex_map_id&0x07),
      tex_coord_id_1=GX.TexCoordID(tev_orders[1].tex_coord_id&0x07), tex_map_id_1=GX.TexMapID(tev_orders[1].tex_map_id&0x07),
      tex_coord_id_2=GX.TexCoordID(tev_orders[2].tex_coord_id&0x07), tex_map_id_2=GX.TexMapID(tev_orders[2].tex_map_id&0x07),
      tex_coord_id_3=GX.TexCoordID(tev_orders[3].tex_coord_id&0x07), tex_map_id_3=GX.TexMapID(tev_orders[3].tex_map_id&0x07),
    ))
    mask = 0
    for i in range(mat.tex_indirect.num_ind_tex_stages):
      mask |= 1 << (tev_orders[i].tex_map_id & 0x07)
    self.bp_commands.append(BP.IND_IMASK(
      register=BPRegister.IND_IMASK,
      mask=mask,
    ))
    
    # Use 32-bit floats instead of Python's default of 64-bit floats in order to intentionally
    # reduce precision to what the original files used.
    start_z = np.float32(mat.fog_info.start_z)
    end_z   = np.float32(mat.fog_info.end_z)
    near_z  = np.float32(mat.fog_info.near_z)
    far_z   = np.float32(mat.fog_info.far_z)
    if far_z == near_z or end_z == start_z:
      # Avoid division by 0
      val_a = np.float32(0.0)
      val_b = np.float32(0.5)
      val_c = np.float32(0.0)
    else:
      val_a = (far_z * near_z) / ((far_z - near_z) * (end_z - start_z))
      val_b = far_z / (far_z - near_z)
      val_c = start_z / (end_z - start_z)
    
    mantissa = val_b
    exponent = 1
    while mantissa > 1.0:
      mantissa /= 2.0
      exponent += 1
    while mantissa > 0.0 and mantissa < 0.5:
      mantissa *= 2.0
      exponent -= 1
    
    integral_a = fs.bit_cast_float_to_int(val_a / (1 << exponent))
    integral_b = int(mantissa * 8388638.0)
    integral_c = fs.bit_cast_float_to_int(val_c)
    
    self.bp_commands.append(BP.TEV_FOG_PARAM_0(
      register=BPRegister.TEV_FOG_PARAM_0,
      mantissa=(integral_a >> 12 & 0x7FF), exponent=(integral_a >> 23 & 0xFF), sign=(integral_a >> 31 & 1),
    ))
    # print(val_a, val_b, val_c)
    # print(self.bp_commands[-1])
    self.bp_commands.append(BP.TEV_FOG_PARAM_1(
      register=BPRegister.TEV_FOG_PARAM_1,
      magnitude=integral_b,
    ))
    self.bp_commands.append(BP.TEV_FOG_PARAM_2(
      register=BPRegister.TEV_FOG_PARAM_2,
      shift=exponent,
    ))
    self.bp_commands.append(BP.TEV_FOG_PARAM_3(
      register=BPRegister.TEV_FOG_PARAM_3,
      mantissa=(integral_c >> 12 & 0x7FF), exponent=(integral_c >> 23 & 0xFF), sign=(integral_c >> 31 & 1),
      projection=GX.FogProjection.PERSPECTIVE, # TODO FogInfo.fog_type & 0x08 might be this? can't find examples in WW tho
      fog_type=mat.fog_info.fog_type,
    ))
    
    color = mat.fog_info.color
    self.bp_commands.append(BP.TEV_FOG_COLOR(
      register=BPRegister.TEV_FOG_COLOR,
      r=color.r, g=color.g, b=color.b,
    ))
    
    if mat.fog_info.enable:
      for i in range(5):
        self.bp_commands.append(BP.FOG_RANGE_ADJ(
          reg_index=i,
          hi=mat.fog_info.range_adjustments[i*2+0], lo=mat.fog_info.range_adjustments[i*2+1],
        ))
    self.bp_commands.append(BP.FOG_RANGE(
      register=BPRegister.FOG_RANGE,
      center=mat.fog_info.center+342, enabled=mat.fog_info.enable,
    ))
    
    self.bp_commands.append(BP.TEV_ALPHAFUNC(
      register=BPRegister.TEV_ALPHAFUNC,
      ref0=mat.alpha_compare.ref0, ref1=mat.alpha_compare.ref1,
      comp0=mat.alpha_compare.comp0, comp1=mat.alpha_compare.comp1,
      operation=mat.alpha_compare.operation,
    ))
    
    self.bp_commands.append(BP.BP_MASK(
      register=BPRegister.BP_MASK,
      mask=0x001FE7, # TODO: 0x001FE7 in WW, 0x00FFE7 in TP?
    ))
    cmode0_cmd = BP.PE_CMODE0(reg_index=0)
    if mat.blend_mode.mode == GX.BlendMode.Blend:
      cmode0_cmd.blend = True
    elif mat.blend_mode.mode == GX.BlendMode.Subtract:
      cmode0_cmd.blend = True
      cmode0_cmd.subtract = True
    elif mat.blend_mode.mode == GX.BlendMode.Logic:
      cmode0_cmd.logic = True
    cmode0_cmd.destination_factor = mat.blend_mode.destination_factor
    cmode0_cmd.source_factor = mat.blend_mode.source_factor
    cmode0_cmd.logic_op = mat.blend_mode.logic_op
    cmode0_cmd.dither = mat.dither
    self.bp_commands.append(cmode0_cmd)
    
    self.bp_commands.append(BP.PE_ZMODE(
      register=BPRegister.PE_ZMODE,
      depth_test=mat.z_mode.depth_test, depth_func=mat.z_mode.depth_func, depth_write=mat.z_mode.depth_write,
    ))
    
    self.bp_commands.append(BP.BP_MASK(
      register=BPRegister.BP_MASK,
      mask=0x000040,
    ))
    self.bp_commands.append(BP.PE_CONTROL(
      register=BPRegister.PE_CONTROL,
      z_compare=mat.z_compare,
    ))
    
    self.bp_commands.append(BP.BP_MASK(
      register=BPRegister.BP_MASK,
      mask=0x07FC3F,
    ))
    if mat.cull_mode == GX.CullMode.Cull_All:
      cull_mode = BP.MDLCullMode.Cull_None
    else:
      cull_mode = BP.MDLCullMode[mat.cull_mode.name]
    self.bp_commands.append(BP.GEN_MODE(
      register=BPRegister.GEN_MODE,
      num_tex_gens=mat.num_tex_gens, num_color_chans=mat.num_color_chans,
      num_tev_stages_minus_1=mat.num_tev_stages-1,
      cull_mode=cull_mode,
      num_ind_tex_stages=mat.tex_indirect.num_ind_tex_stages
    ))
    
    
    for i, tex_matrix in enumerate(mat.tex_matrixes):
      if tex_matrix is None:
        break
      
      # Only write the tex matrix if it's used by at least one tex coord gen.
      if not any(gen is not None and gen.tex_gen_matrix == GX.TexGenMatrix.TEXMTX0+i*3 for gen in mat.tex_coord_gens):
        continue
      
      tex_mtx_cmd = XF.TEXMTX(register=XF.TEXMTX.VALID_REGISTERS[i])
      
      trans_x  = np.float32(tex_matrix.translation.x)
      trans_y  = np.float32(tex_matrix.translation.y)
      scale_x  = np.float32(tex_matrix.scale.x)
      scale_y  = np.float32(tex_matrix.scale.y)
      tiling_x = np.float32(tex_matrix.center.x)
      tiling_y = np.float32(tex_matrix.center.y)
      angle    = np.float32(tex_matrix.rotation)
      
      sin = np.float32(math.sin(angle * math.pi / 0x8000))
      cos = np.float32(math.cos(angle * math.pi / 0x8000))
      
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(scale_x * cos)))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(-scale_x * sin)))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(0.0)))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(tiling_x + scale_x * (sin * (trans_y + tiling_y) - cos * (trans_x + tiling_x)))))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(scale_y * sin)))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(scale_y * cos)))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(0.0)))
      tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(tiling_y + -scale_y * (sin * (trans_x + tiling_x) + cos * (trans_y + tiling_y)))))
      
      if tex_matrix.projection == TexMtxProjection.MTX3x4:
        tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(0.0)))
        tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(0.0)))
        tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(0.0)))
        tex_mtx_cmd.args.append(XF.TEXMTX_Arg(value=float(1.0)))
      
      self.xf_commands.append(tex_mtx_cmd)
    
    tex_mtx_info_cmd = XF.TEXMTXINFO(register=XFRegister.TEXMTXINFO)
    pos_mtx_info_cmd = XF.POSMTXINFO(register=XFRegister.POSMTXINFO)
    any_tex_coord_gen_exists = False
    for i, coord_gen in enumerate(mat.tex_coord_gens):
      if coord_gen is None:
        continue
      any_tex_coord_gen_exists = True
      
      tex_arg = XF.TEXMTXINFO_Arg()
      tex_arg.tex_gen_type = XF.TexGenType.Regular
      tex_arg.source_row = XF.SourceRow.Geom
      if coord_gen.source in [GX.TexGenSrc.POS, GX.TexGenSrc.NRM, GX.TexGenSrc.BINRM, GX.TexGenSrc.TANGENT]:
        tex_arg.input_form = XF.TexInputForm.ABC1
      
      if GX.TexGenType.BUMP0 <= coord_gen.type_ <= GX.TexGenType.BUMP7:
        tex_arg.tex_gen_type = XF.TexGenType.EmbossMap
        tex_arg.source_row = XF.SourceRow.Tex0
        tex_arg.emboss_source_shift = coord_gen.source.value - GX.TexGenSrc.TEX0.value
        tex_arg.emboss_light_shift = coord_gen.type_.value - GX.TexGenType.BUMP0.value
      elif coord_gen.type_ == GX.TexGenType.SRTG:
        if coord_gen.source == GX.TexGenSrc.COLOR0:
          tex_arg.tex_gen_type = XF.TexGenType.Color0
        else:
          tex_arg.tex_gen_type = XF.TexGenType.Color1
        
        tex_arg.source_row = XF.SourceRow.Colors
      elif coord_gen.type_ in [GX.TexGenType.MTX2x4, GX.TexGenType.MTX3x4]:
        tex_arg.tex_gen_type = XF.TexGenType.Regular
        
        if coord_gen.source == GX.TexGenSrc.POS:
          tex_arg.source_row = XF.SourceRow.Geom
        elif coord_gen.source == GX.TexGenSrc.NRM:
          tex_arg.source_row = XF.SourceRow.Normal
        elif coord_gen.source >= GX.TexGenSrc.TEX0 and coord_gen.source <= GX.TexGenSrc.TEX7:
          tex_idx = coord_gen.source - GX.TexGenSrc.TEX0
          tex_arg.source_row = XF.SourceRow(XF.SourceRow.Tex0.value + tex_idx)
        else:
          raise NotImplementedError()
        
        if coord_gen.type_ == GX.TexGenType.MTX3x4:
          tex_arg.projection = XF.TexSize.STQ
      
      tex_mtx_info_cmd.args.append(tex_arg)
      
      tex_arg = XF.POSMTXINFO_Arg()
      pos_mtx_info_cmd.args.append(tex_arg)
    if any_tex_coord_gen_exists:
      self.xf_commands.append(tex_mtx_info_cmd)
      self.xf_commands.append(pos_mtx_info_cmd)
    
    mat_color_cmd = XF.CHAN0_MATCOLOR(register=XFRegister.CHAN0_MATCOLOR)
    for i, mat_color in enumerate(mat.material_colors):
      if mat_color is None:
        continue
      color_arg = XF.CHAN0_MATCOLOR_Arg(
        r=mat_color.r, g=mat_color.g, b=mat_color.b, a=mat_color.a,
      )
      mat_color_cmd.args.append(color_arg)
    self.xf_commands.append(mat_color_cmd)
    
    amb_color_cmd = XF.CHAN0_AMBCOLOR(register=XFRegister.CHAN0_AMBCOLOR)
    for i, amb_color in enumerate(mat.ambient_colors):
      if amb_color is None:
        continue
      color_arg = XF.CHAN0_AMBCOLOR_Arg(
        r=amb_color.r, g=amb_color.g, b=amb_color.b, a=amb_color.a,
      )
      amb_color_cmd.args.append(color_arg)
    self.xf_commands.append(amb_color_cmd)
    
    color_chan_cmd = XF.CHAN0_COLOR(register=XFRegister.CHAN0_COLOR)
    reordered_color_channels = [
      mat.color_channels[0],
      mat.color_channels[2],
      mat.color_channels[1],
      mat.color_channels[3],
    ]
    for i, color_chan in enumerate(reordered_color_channels):
      color_chan_arg = XF.CHAN0_COLOR_Arg()
      color_chan_arg.lighting_enabled = color_chan.lighting_enabled
      color_chan_arg.mat_color_src = color_chan.mat_color_src
      color_chan_arg.ambient_color_src = color_chan.ambient_color_src
      if color_chan.attenuation_function == GX.AttenuationFunction.Specular:
        color_chan_arg.attenuation_enabled = True
        color_chan_arg.use_spot_attenuation = False
        color_chan_arg.diffuse_function = GX.DiffuseFunction.None_
      elif color_chan.attenuation_function == GX.AttenuationFunction.Spot:
        color_chan_arg.attenuation_enabled = True
        color_chan_arg.use_spot_attenuation = True
        color_chan_arg.diffuse_function = color_chan.diffuse_function
      elif color_chan.attenuation_function == GX.AttenuationFunction.None_:
        color_chan_arg.attenuation_enabled = False
        color_chan_arg.use_spot_attenuation = True
        color_chan_arg.diffuse_function = color_chan.diffuse_function
      color_chan_arg.used_lights_0123 = color_chan.used_lights[0:4]
      color_chan_arg.used_lights_4567 = color_chan.used_lights[4:8]
      color_chan_cmd.args.append(color_chan_arg)
    self.xf_commands.append(color_chan_cmd)
    
    if mat.light_colors[0] is not None:
      # Light pos
      num_tex_gens_cmd = XF.LIGHT0_LPX(register=XFRegister.LIGHT0_LPX)
      color = mat.light_colors[0]
      num_tex_gens_cmd.args.append(XF.LIGHT0_LPX_Arg(value=0.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_LPX_Arg(value=0.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_LPX_Arg(value=0.0))
      self.xf_commands.append(num_tex_gens_cmd)
      
      # Light attenuation
      num_tex_gens_cmd = XF.LIGHT0_A0(register=XFRegister.LIGHT0_A0)
      num_tex_gens_cmd.args.append(XF.LIGHT0_A0_Arg(value=1.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_A0_Arg(value=0.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_A0_Arg(value=0.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_A0_Arg(value=1.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_A0_Arg(value=0.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_A0_Arg(value=0.0))
      self.xf_commands.append(num_tex_gens_cmd)
      
      # Light color
      # TODO: fn_body doesn't match? white/black
      num_tex_gens_cmd = XF.LIGHT0_COLOR(register=XFRegister.LIGHT0_COLOR)
      color = mat.light_colors[0]
      num_tex_gens_cmd.args.append(XF.LIGHT0_COLOR_Arg(color=color.r << 24 | color.g << 16 | color.b << 8 | color.a))
      self.xf_commands.append(num_tex_gens_cmd)
      
      # Light direction
      num_tex_gens_cmd = XF.LIGHT0_DHX(register=XFRegister.LIGHT0_DHX)
      num_tex_gens_cmd.args.append(XF.LIGHT0_DHX_Arg(value=0.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_DHX_Arg(value=-1.0))
      num_tex_gens_cmd.args.append(XF.LIGHT0_DHX_Arg(value=0.0))
      self.xf_commands.append(num_tex_gens_cmd)
    
    num_color_chans_cmd = XF.NUMCHAN(register=XFRegister.NUMCHAN)
    num_color_chans_cmd.args.append(XF.NUMCHAN_Arg(
      num_color_chans=mat.num_color_chans,
    ))
    self.xf_commands.append(num_color_chans_cmd)
    
    num_tex_gens_cmd = XF.NUMTEXGENS(register=XFRegister.NUMTEXGENS)
    num_tex_gens_cmd.args.append(XF.NUMTEXGENS_Arg(
      num_tex_gens=mat.num_tex_gens,
    ))
    self.xf_commands.append(num_tex_gens_cmd)
    
    
    # TODO: maybe do this when save() is called?
    for cmd in self.bp_commands:
      cmd.data = self.data
    for cmd in self.xf_commands:
      cmd.data = self.data
      for arg in cmd.args:
        arg.data = self.data

@bunfoe
class MDL3(JChunk):
  num_entries              : u16
  _padding_1               : u16 = 0xFFFF
  packets_offset           : u32
  subpackets_offset        : u32
  matrix_index_offset      : u32
  pixel_engine_modes_offset: u32
  indexes_offset           : u32
  mat_names_table_offset   : u32
  
  entries: list[MDLEntry] = field(ignore=True, default_factory=list)
  
  def read_chunk_specific_data(self):
    BUNFOE.read(self, 0)
    
    self.entries.clear()
    packet_offset = self.packets_offset
    for i in range(self.num_entries):
      entry_offset = packet_offset + fs.read_u32(self.data, packet_offset + 0x00)
      entry_size = fs.read_u32(self.data, packet_offset + 0x04)
      entry = MDLEntry(self.data)
      entry.read(entry_offset, entry_size)
      self.entries.append(entry)
      packet_offset += 8
    
    offset = self.matrix_index_offset
    for entry in self.entries:
      entry.unknown_float_1 = fs.read_and_unpack_bytes(self.data, offset+0x00, 4, ">f")[0]
      entry.unknown_float_2 = fs.read_and_unpack_bytes(self.data, offset+0x04, 4, "<f")[0]
      offset += 8
    
    offset = self.pixel_engine_modes_offset
    for entry in self.entries:
      pixel_engine_mode = GX.PixelEngineMode(fs.read_u8(self.data, offset))
      offset += 1
      entry.pixel_engine_mode = pixel_engine_mode
    
    self.string_table_offset = fs.read_u32(self.data, 0x20)
    self.mat_names = self.read_string_table(self.string_table_offset)
  
  def generate_from_mat3(self, mat3: MAT3, tex1: TEX1):
    for mat, entry in zip(mat3.materials, self.entries):
      entry.generate_from_material(mat, tex1)
    self.save()
  
  def save_chunk_specific_data(self):
    self.data.truncate(0x40)
    
    self.num_entries = len(self.entries)
    
    # Temporarily write placeholders for the packets.
    self.packets_offset = fs.data_len(self.data)
    packet_offset = self.packets_offset
    for entry in self.entries:
      fs.write_u32(self.data, packet_offset+0, 0)
      fs.write_u32(self.data, packet_offset+4, 0)
      packet_offset += 8
    entry_offset = fs.align_data_and_pad_offset(self.data, packet_offset, 0x20)
    
    # Write the entries as well as the actual packets.
    packet_offset = self.packets_offset
    for entry in self.entries:
      next_entry_offset = entry.save(entry_offset)
      entry_size = next_entry_offset - entry_offset
      fs.write_u32(self.data, packet_offset+0, entry_offset - packet_offset)
      fs.write_u32(self.data, packet_offset+4, entry_size)
      entry_offset = next_entry_offset
      packet_offset += 8
    offset = entry_offset
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    self.subpackets_offset = fs.data_len(self.data)
    for entry in self.entries:
      fs.write_u16(self.data, offset+0x00, entry.chan_color_subpacket_offset or 0)
      fs.write_u16(self.data, offset+0x02, entry.chan_control_subpacket_offset or 0)
      fs.write_u16(self.data, offset+0x04, entry.tex_gen_subpacket_offset or 0)
      fs.write_u16(self.data, offset+0x06, entry.texture_subpacket_offset or 0)
      fs.write_u16(self.data, offset+0x08, entry.tev_subpacket_offset or 0)
      fs.write_u16(self.data, offset+0x0A, entry.pixel_subpacket_offset or 0)
      fs.write_s32(self.data, offset+0x0C, -1) # Padding
      offset += 0x10
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    self.matrix_index_offset = fs.data_len(self.data)
    for entry in self.entries:
      # A big endian float followed by a little endian float. What these are exactly isn't known.
      # They're usually all the same value, but there are exceptions, such as Link's eyeL and eyeR materials.
      # TODO: could maybe be related to texmtx in some way? eyeL and eyeR have non-default texmtx
      fs.write_and_pack_bytes(self.data, offset+0x00, [entry.unknown_float_1], ">f")
      fs.write_and_pack_bytes(self.data, offset+0x04, [entry.unknown_float_2], "<f")
      offset += 8
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    self.pixel_engine_modes_offset = fs.data_len(self.data)
    for entry in self.entries:
      fs.write_u8(self.data, offset, entry.pixel_engine_mode.value)
      offset += 1
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    self.indexes_offset = fs.data_len(self.data)
    for entry_index, entry in enumerate(self.entries):
      fs.write_u16(self.data, offset, entry_index)
      offset += 2
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    # Write the material names.
    self.mat_names_table_offset = offset
    offset = self.write_string_table(self.mat_names_table_offset, self.mat_names)
    
    # Finally, save the new offsets to each list back to the header.
    BUNFOE.save(self, 0)
