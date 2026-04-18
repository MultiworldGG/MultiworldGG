saveBufferOffset = 0x207700

filesPtr = [0x207700, 0x207770, 0x2077E0, 0x207850]
currFilePtr = 0x32DDF4
hpPtr = 0x33B21E
igtPtr = 0x32D580

starCountAPPtr1 = 0x245000 + 0x35040
starCountAPPtr2 = 0x245000 + 0x35074
flagAPPtr = 0x245000 + 0x35198
cannonAPPtr = 0x245000 + 0x35344
capAPPtr = 0x245000 + 0x61FAC
keyAPPtr1 = 0x245000 + 0x34DB0
keyAPPtr2 = 0x245000 + 0x34DD4
toad1APPtr = 0x245000 + 0x319B0
toad2APPtr = 0x245000 + 0x319E4
toad3APPtr = 0x245000 + 0x31A18
moatAPPtr = 0x245000 + 0x751B0

marioActionPtr = 0x33B17C
marioFloorPtr = 0x33B1D8
marioYPosPtr = 0x33B1B0
marioFloorHeightPtr = 0x33B1E0
marioSquishPtr = 0x33B224

starsCountPtr = 0x33B21B

marioObjectPtr = 0x361158

objectListPtr = 0x33D488
objectListSize = 240
levelPtr = 0x32DDF9
areaPtr = 0x33B24A

trapPatchPtr = 0x29D4B8
choirPatchPtr = 0x27FF00
choirHookPtr = 0x3191E0
starPatchPtr = 0x279C88
moveHookPtr = 0x252CFC
movePatchPtr = 0x1F1100

burningHookPtr = 0x24EC1C
treeHookPtr1 = 0x25E64C
treeHookPtr2 = 0x25E2BC
punchHookPtr = 0x275398
movingPunchHookPtr = 0x2665FC
shellHookPtr = 0x24F6E0
slopeFixHookPtr = 0x268010
wallkickHookPtr1 = 0x26D34C
wallkickHookPtr2 = 0x26D9D4

bank13RamStartPtr = 0x33B400 + 4 * 0x13

coinPtr = 0x33B218
coinVisualPtr = 0x33B262

livesPtr = 0x33B21C
stevePtr = 0x1F1000

level_index = { #sm64's internal level ids are different than the ones used in save data
    16:8, #overworld
    6:8,
    26:8,
    9:12, #course 1-15
    24:13,
    12:14,
    5:15,
    4:16,
    7:17,
    22:18,
    8:19,
    23:20,
    10:21,
    11:22,
    36:23,
    13:24,
    14:25,
    15:26,
    17:27, #bowser 1/fight
    30:27,
    19:28, #bowser 2/fight
    33:28,
    21:29, #bowser 3/fight
    34:29,
    27:30, #slide
    28:31, #metal cap
    29:32, #wing cap
    18:33, #vanish cap
    31:34, #secrets 1-3
    20:35,
    25:36
}

courseIndex = {
    8:  "Overworld",
    12: "Course 1" ,
    13: "Course 2" ,
    14: "Course 3" ,
    15: "Course 4" ,
    16: "Course 5" ,
    17: "Course 6" ,
    18: "Course 7" ,
    19: "Course 8" ,
    20: "Course 9" ,
    21: "Course 10" ,
    22: "Course 11" ,
    23: "Course 12" ,
    24: "Course 13" ,
    25: "Course 14" ,
    26: "Course 15" ,
    27: "Bowser 1" ,
    28: "Bowser 2" ,
    29: "Bowser 3" ,
    30: "Slide" ,
    31: "Metal Cap" ,
    32: "Wing Cap" ,
    33: "Vanish Cap" ,
    34: "Secret 1" ,
    35: "Secret 2" ,
    36: "Secret 3"
}

causeStrings = [
    "this is not supposed to show up",
    "slot fell into something which acts like quicksand.",
    "slot really likes spinning around!",
    "slot became a tasty meal.",
    "slot couldn't find clean air.",
    "slot tried to breathe water.",
    "slot is not a good conductor of electricity.",
    "slot doesn't like extreme temperatures.",
    "slot fell into a deep abyss.",
    "The wind wasn't enough to save slot.",
    "slot died."
]

badge_dict = {
    0x80: "Triple Jump Badge",
    0x40: "Lava Badge",
    0x20: "Ultra Badge",
    0x10: "Super Badge",
    0x08: "Wall Badge"
}

moves = (
    "Progressive Jump",
    "Wallkick",
    "Backflip",
    "Sideflip",
    "Long Jump",
    "Dive",
    "Ground Pound",
    "Kick",
    "Punch",
    "Slidekick",
    "Shell"
)

jump_names = (
    "Jump",
    "Double Jump",
    "Triple Jump"
)


# these are for v0.4 client compatibility
legacy_location_name_to_id = {'Course 1 Star 1': 40693, 'Course 1 Star 2': 40694, 'Course 1 Star 3': 40695, 'Course 1 Star 4': 40696, 'Course 1 Star 5': 40697, 'Course 1 Star 6': 40698, 'Course 1 Star 7': 40699, 'Course 1 Star 8': 40700, 'Course 1 Cannon': 40701, 'Course 1 Troll Star': 40702, 'Course 2 Star 1': 40703, 'Course 2 Star 2': 40704, 'Course 2 Star 3': 40705, 'Course 2 Star 4': 40706, 'Course 2 Star 5': 40707, 'Course 2 Star 6': 40708, 'Course 2 Star 7': 40709, 'Course 2 Star 8': 40710, 'Course 2 Cannon': 40711, 'Course 2 Troll Star': 40712, 'Course 3 Star 1': 40713, 'Course 3 Star 2': 40714, 'Course 3 Star 3': 40715, 'Course 3 Star 4': 40716, 'Course 3 Star 5': 40717, 'Course 3 Star 6': 40718, 'Course 3 Star 7': 40719, 'Course 3 Star 8': 40720, 'Course 3 Cannon': 40721, 'Course 3 Troll Star': 40722, 'Course 4 Star 1': 40723, 'Course 4 Star 2': 40724, 'Course 4 Star 3': 40725, 'Course 4 Star 4': 40726, 'Course 4 Star 5': 40727, 'Course 4 Star 6': 40728, 'Course 4 Star 7': 40729, 'Course 4 Star 8': 40730, 'Course 4 Cannon': 40731, 'Course 4 Troll Star': 40732, 'Course 5 Star 1': 40733, 'Course 5 Star 2': 40734, 'Course 5 Star 3': 40735, 'Course 5 Star 4': 40736, 'Course 5 Star 5': 40737, 'Course 5 Star 6': 40738, 'Course 5 Star 7': 40739, 'Course 5 Star 8': 40740, 'Course 5 Cannon': 40741, 'Course 5 Troll Star': 40742, 'Course 6 Star 1': 40743, 'Course 6 Star 2': 40744, 'Course 6 Star 3': 40745, 'Course 6 Star 4': 40746, 'Course 6 Star 5': 40747, 'Course 6 Star 6': 40748, 'Course 6 Star 7': 40749, 'Course 6 Star 8': 40750, 'Course 6 Cannon': 40751, 'Course 6 Troll Star': 40752, 'Course 7 Star 1': 40753, 'Course 7 Star 2': 40754, 'Course 7 Star 3': 40755, 'Course 7 Star 4': 40756, 'Course 7 Star 5': 40757, 'Course 7 Star 6': 40758, 'Course 7 Star 7': 40759, 'Course 7 Star 8': 40760, 'Course 7 Cannon': 40761, 'Course 7 Troll Star': 40762, 'Course 8 Star 1': 40763, 'Course 8 Star 2': 40764, 'Course 8 Star 3': 40765, 'Course 8 Star 4': 40766, 'Course 8 Star 5': 40767, 'Course 8 Star 6': 40768, 'Course 8 Star 7': 40769, 'Course 8 Star 8': 40770, 'Course 8 Cannon': 40771, 'Course 8 Troll Star': 40772, 'Course 9 Star 1': 40773, 'Course 9 Star 2': 40774, 'Course 9 Star 3': 40775, 'Course 9 Star 4': 40776, 'Course 9 Star 5': 40777, 'Course 9 Star 6': 40778, 'Course 9 Star 7': 40779, 'Course 9 Star 8': 40780, 'Course 9 Cannon': 40781, 'Course 9 Troll Star': 40782, 'Course 10 Star 1': 40783, 'Course 10 Star 2': 40784, 'Course 10 Star 3': 40785, 'Course 10 Star 4': 40786, 'Course 10 Star 5': 40787, 'Course 10 Star 6': 40788, 'Course 10 Star 7': 40789, 'Course 10 Star 8': 40790, 'Course 10 Cannon': 40791, 'Course 10 Troll Star': 40792, 'Course 11 Star 1': 40793, 'Course 11 Star 2': 40794, 'Course 11 Star 3': 40795, 'Course 11 Star 4': 40796, 'Course 11 Star 5': 40797, 'Course 11 Star 6': 40798, 'Course 11 Star 7': 40799, 'Course 11 Star 8': 40800, 'Course 11 Cannon': 40801, 'Course 11 Troll Star': 40802, 'Course 12 Star 1': 40803, 'Course 12 Star 2': 40804, 'Course 12 Star 3': 40805, 'Course 12 Star 4': 40806, 'Course 12 Star 5': 40807, 'Course 12 Star 6': 40808, 'Course 12 Star 7': 40809, 'Course 12 Star 8': 40810, 'Course 12 Cannon': 40811, 'Course 12 Troll Star': 40812, 'Course 13 Star 1': 40813, 'Course 13 Star 2': 40814, 'Course 13 Star 3': 40815, 'Course 13 Star 4': 40816, 'Course 13 Star 5': 40817, 'Course 13 Star 6': 40818, 'Course 13 Star 7': 40819, 'Course 13 Star 8': 40820, 'Course 13 Cannon': 40821, 'Course 13 Troll Star': 40822, 'Course 14 Star 1': 40823, 'Course 14 Star 2': 40824, 'Course 14 Star 3': 40825, 'Course 14 Star 4': 40826, 'Course 14 Star 5': 40827, 'Course 14 Star 6': 40828, 'Course 14 Star 7': 40829, 'Course 14 Star 8': 40830, 'Course 14 Cannon': 40831, 'Course 14 Troll Star': 40832, 'Course 15 Star 1': 40833, 'Course 15 Star 2': 40834, 'Course 15 Star 3': 40835, 'Course 15 Star 4': 40836, 'Course 15 Star 5': 40837, 'Course 15 Star 6': 40838, 'Course 15 Star 7': 40839, 'Course 15 Star 8': 40840, 'Course 15 Cannon': 40841, 'Course 15 Troll Star': 40842, 'Bowser 1 Star 1': 40843, 'Bowser 1 Star 2': 40844, 'Bowser 1 Star 3': 40845, 'Bowser 1 Star 4': 40846, 'Bowser 1 Star 5': 40847, 'Bowser 1 Star 6': 40848, 'Bowser 1 Star 7': 40849, 'Bowser 1 Star 8': 40850, 'Bowser 1 Cannon': 40851, 'Bowser 1 Troll Star': 40852, 'Bowser 2 Star 1': 40853, 'Bowser 2 Star 2': 40854, 'Bowser 2 Star 3': 40855, 'Bowser 2 Star 4': 40856, 'Bowser 2 Star 5': 40857, 'Bowser 2 Star 6': 40858, 'Bowser 2 Star 7': 40859, 'Bowser 2 Star 8': 40860, 'Bowser 2 Cannon': 40861, 'Bowser 2 Troll Star': 40862, 'Bowser 3 Star 1': 40863, 'Bowser 3 Star 2': 40864, 'Bowser 3 Star 3': 40865, 'Bowser 3 Star 4': 40866, 'Bowser 3 Star 5': 40867, 'Bowser 3 Star 6': 40868, 'Bowser 3 Star 7': 40869, 'Bowser 3 Star 8': 40870, 'Bowser 3 Cannon': 40871, 'Bowser 3 Troll Star': 40872, 'Slide Star 1': 40873, 'Slide Star 2': 40874, 'Slide Star 3': 40875, 'Slide Star 4': 40876, 'Slide Star 5': 40877, 'Slide Star 6': 40878, 'Slide Star 7': 40879, 'Slide Star 8': 40880, 'Slide Cannon': 40881, 'Slide Troll Star': 40882, 'Secret 1 Star 1': 40883, 'Secret 1 Star 2': 40884, 'Secret 1 Star 3': 40885, 'Secret 1 Star 4': 40886, 'Secret 1 Star 5': 40887, 'Secret 1 Star 6': 40888, 'Secret 1 Star 7': 40889, 'Secret 1 Star 8': 40890, 'Secret 1 Cannon': 40891, 'Secret 1 Troll Star': 40892, 'Secret 2 Star 1': 40893, 'Secret 2 Star 2': 40894, 'Secret 2 Star 3': 40895, 'Secret 2 Star 4': 40896, 'Secret 2 Star 5': 40897, 'Secret 2 Star 6': 40898, 'Secret 2 Star 7': 40899, 'Secret 2 Star 8': 40900, 'Secret 2 Cannon': 40901, 'Secret 2 Troll Star': 40902, 'Secret 3 Star 1': 40903, 'Secret 3 Star 2': 40904, 'Secret 3 Star 3': 40905, 'Secret 3 Star 4': 40906, 'Secret 3 Star 5': 40907, 'Secret 3 Star 6': 40908, 'Secret 3 Star 7': 40909, 'Secret 3 Star 8': 40910, 'Secret 3 Cannon': 40911, 'Secret 3 Troll Star': 40912, 'Metal Cap Star 1': 40913, 'Metal Cap Star 2': 40914, 'Metal Cap Star 3': 40915, 'Metal Cap Star 4': 40916, 'Metal Cap Star 5': 40917, 'Metal Cap Star 6': 40918, 'Metal Cap Star 7': 40919, 'Metal Cap Star 8': 40920, 'Metal Cap Cannon': 40921, 'Metal Cap Troll Star': 40922, 'Wing Cap Star 1': 40923, 'Wing Cap Star 2': 40924, 'Wing Cap Star 3': 40925, 'Wing Cap Star 4': 40926, 'Wing Cap Star 5': 40927, 'Wing Cap Star 6': 40928, 'Wing Cap Star 7': 40929, 'Wing Cap Star 8': 40930, 'Wing Cap Cannon': 40931, 'Wing Cap Troll Star': 40932, 'Vanish Cap Star 1': 40933, 'Vanish Cap Star 2': 40934, 'Vanish Cap Star 3': 40935, 'Vanish Cap Star 4': 40936, 'Vanish Cap Star 5': 40937, 'Vanish Cap Star 6': 40938, 'Vanish Cap Star 7': 40939, 'Vanish Cap Star 8': 40940, 'Vanish Cap Cannon': 40941, 'Vanish Cap Troll Star': 40942, 'Overworld Star 1': 40943, 'Overworld Star 2': 40944, 'Overworld Star 3': 40945, 'Overworld Star 4': 40946, 'Overworld Star 5': 40947, 'Overworld Star 6': 40948, 'Overworld Star 7': 40949, 'Overworld Star 8': 40950, 'Overworld Cannon': 40951, 'Overworld Troll Star': 40952, 'Key 1': 40953, 'Super Badge': 40954, 'Key 2': 40955, 'Ultra Badge': 40956, 'Wing Cap': 40957, 'Wall Badge': 40958, 'Vanish Cap': 40959, 'Triple Jump Badge': 40960, 'Metal Cap': 40961, 'Lava Badge': 40962, 'Black Switch': 40963, 'Yellow Switch': 40964, 'Bowser Fight Reds': 40965, 'Star 210': 40966, 'Toursome Trouble RT Star 1': 40967, 'Toursome Trouble RT Star 2': 40968, 'Toursome Trouble RT Star 3': 40969, 'Toursome Trouble RT Star 4': 40970, 'Toursome Trouble RT Star 5': 40971, 'Toursome Trouble RT Star 6': 40972, 'Castle Moat': 40973}
legacy_item_names = ['Key 1', 'Key 2', 'Wing Cap', 'Vanish Cap', 'Metal Cap', 'Power Star', 'Progressive Key', 'Course 1 Cannon', 'Course 2 Cannon', 'Course 3 Cannon', 'Course 4 Cannon', 'Course 5 Cannon', 'Course 6 Cannon', 'Course 7 Cannon', 'Course 8 Cannon', 'Course 9 Cannon', 'Course 10 Cannon', 'Course 11 Cannon', 'Course 12 Cannon', 'Course 13 Cannon', 'Course 14 Cannon', 'Course 15 Cannon', 'Bowser 1 Cannon', 'Bowser 2 Cannon', 'Bowser 3 Cannon', 'Slide Cannon', 'Secret 1 Cannon', 'Secret 2 Cannon', 'Secret 3 Cannon', 'Metal Cap Cannon', 'Wing Cap Cannon', 'Vanish Cap Cannon', 'Overworld Cannon', 'Progressive Stomp Badge', 'Wall Badge', 'Triple Jump Badge', 'Lava Badge', 'Overworld Cannon Star', 'Bowser 2 Cannon Star', 'Yellow Switch', 'Black Switch', 'Coin', 'Green Demon Trap', 'Mario Choir', 'Heave-Ho Trap', 'Squish Trap', 'Castle Moat']

#in format ram address: asm code originally in place (to restore your moves when you get them back)

move_rando_asm = { #most of these are just changing B address after calls to set_mario_action to BNEZ V0, address
    0x25315C: "00000000", # dont set return in set_jumping_action
    0x261E18: "14400051", # backflip
    0x2625C4: "1440001E",
    0x2626E4: "1440001E",
    0x268210: "14400045", # long jump
    0x268260: "14400031", # slidekick
    0x266B5C: "14400076", # sideflip
    0x266DAC: "14400022",
    0x268284: "14400028", # breakdance
    0x261F34: "1440000A",
    0x2655F8: "14400005", # move punching
    0x266EE0: "14400034", 
    0x260A54: "14400011", # stationary punching
    0x261CB0: "1440000A",
    0x262270: "14400016",
    0x262D40: "14400005",
    0x26A468: "14400005", # kicking/dive
    0x266620: "1440003F",
    0x2763BC: "14400027",
    0x26F370: "144000A3", # dive; act_flying_triple_jump
    0x26B874: "14400021", # act_triple_jump
    0x26B9E4: "1440002F", #act_freefall
    0x26BCF4: "14400031", #act_sideflip
    0x26BE00: "14400019", #act_wall_kick_air
    0x26C8B8: "1440004B", #act_steep_jump
    0x26F87C: "14400061", #act_special_triple_jump - there is no world where this matters in literally any game unless someone is playing disaster quest pi or some casual talks to yoshi in vanilla for some fucking reason
    0x2655DC: "1440000C", #check_ground_dive_or_punch
    0x26F394: "1440009A", #ground pound; act_flying_triple_jump
    0x26BE30: "1440000D", #act_wall_kick_air
    0x26F8AC: "14400055", #act_special_triple_jump
    0x26B6EC: "14400010", #act_jump
    0x26B7BC: "14400011", #act_double_jump
    0x26B8A4: "14400015", #act_triple_jump
    0x26B940: "14400016", #act_backflip
    0x26BA14: "14400023", #act_freefall
    0x26BB64: "1440000F", #act_hold_jump
    0x26BC84: "1440000A", #act_hold_freefall
    0x26BD24: "14400025", #act_side_flip
    0x26EC7C: "14400131", #act_flying
    0x25F00C: "14400025", #act_start_hanging
    0x25F14C: "14400021", #act_hanging
    0x25F248: "1440004A", #act_hang_moving
    0x253080: "00000000", #dont set return in set_jump_from_landing
    0x262CCC: "14400022", #single jump, check_common_landing_cancels
    0x2663E0: "1440006F", #act_walking -> set_jump_from_landing
    0x26703C: "1440007B", #act_decelerating -> set_jump_from_landing
    0x25324C: "14400028", #check_common_action_exits
    0x253334: "14400027", #check_common_hold_action_exits
    0x2677B8: "14400063", #act_crawling
    0x2682B4: "1440001C", #act_crouch_slide
    0x26095C: "1440004F", #check_common_idle_cancels
    0x266830: "14400055", #act_hold_walking
    0x267310: "14400077", #act_hold_decelerating
    0x260B98: "14400042", #check_common_hold_idle_cancels
    0x26437C: "1440001F", #set_triple_jump_action
    0x264384: "14400019", #set_triple_jump_action
    0x2643C0: "1440000E", #set_triple_jump_action
    0x2643C8: "14400008", #set_triple_jump_action
}
slope_fix_ptr = 0x267FE0
no_slope_fix_asm = { #aglabs slope fix modifies the code in the common_slide_action_with_jump function so i need to account for both slope fix and non-slope fix since its a popular patch (for good reason)
    0x267FF4: "1440001B"
}

#decades later
starCountDLPtr1 = 0x279BE0
starCountDLPtr2 = 0x279BFC
starCountDLPtr3 = 0x279C14
starDisplayPtr = 0x1D19F0
prePlayTransitionPtr = 0x1D09A4
actSelectPathPtr = 0x1D0A30
blueStarBoxPtr = 0x1CFA60
afterStarInitPtr = 0x1D03A4
requiredStarsArrPtr = 0x4051E0
blueStarActHook = 0x1D0A60
blueStarActPatchPtr = 0x1E1000

#new traps
tempoPtr = 0x222622
rollPtr = 0x33C74C

#buffs
hundredCoinStarPtr1 = 0x24DBB2
hundredCoinStarPtr2 = 0x24DBBE
vanishCapTimerPtr = 0x24FBF2
metalCapTimerPtr = 0x24FC0A
wingCapTimerPtr= 0x24FC22

wallkickFramePtr = 0x26DA52
wallkickFramePtr2 = 0x26DABA