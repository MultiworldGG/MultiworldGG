#include <cstddef>

extern int _collepediaFlag;
extern int _bladeFlag;

int _hasPreciousItem(int id);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E
0x021b70bc = bl _IsPermit # replace getLocal inside IsPermit with new check
0x022e9920 = nop # restructure online skell flight module check to always use this one
0x022e9934 = bl _loadSkyUnit # replace online skell flight module call with own
0x027d6da0 = bl _loadFNet # replace getScenarioFlag for initial load
0x027d5748 = blr # return original call to changeScenarioFlag Fnet

# doll overdrive
IsReady = 0x021ccdec
0x024bf00c = bl _IsReadyAdjusted

# affinity quests no longer lock you out of other quests
0x022ce6c4 = li r3,0

# disable lock party from affinity quests
0x02296518 = nop
0x02290ca4 = nop
# disable lock for elma on new game
0x027c5004 = li r4,0

# max out fuel for doll with one refill
0x025ce838 = nop

# division points disable until KEY Blade license
0x02847ef8 = bl _isUnlock
0x02847fbc = bl _isUnlock
# join division only if you get blade license, otherwise not
EntryUnion = 0x0288e3f4
getMyUnionNo = 0x0288d380
0x0288e418 = nop

0x022e2c24 = nop # dont set all the arts/skills/classes if you change your Class
0x020c48c4 = blr # disable Class exp
0x020c63d8 = blr # disable friend exp
# disable character exp
addInnerExp = 0x020c395c
0x022953b4 = b _addInnerExpAdjusted
0x02562504 = bl _addInnerExpAdjusted

# remove all equipment for new playable characters
0x027e43d0 = nop # replace setupPcArmor
0x027e4474 = nop 
0x027e44e8 = bl _getDefaultWeapon
0x027e4558 = bl _getDefaultWeapon

# remove arts/skills for new playable characters
0x026a52e8 = blr # disable OpenArts::CharacterData
0x026a5308 = blr # disable OpenSkills::CharacterData
0x027e41f8 = b 0x027e4334 # disable automatic skill asignment
# remove reequip of assault hammer and flame granade for drifter
0x022736ec = lis r3, 0
0x02273734 = lis r3, 0
# set drifter weapon types
Create_DataInit = 0x27e2388
0x027e4768 = bl _Create_DataInit_Adjusted

# remove all equipment for new skells
# replace setupDollArmor
0x027ea5f0 = nop
0x027ea664 = nop
0x027ea6d8 = nop
0x027ea74c = nop
0x027ea7c0 = nop
# replace setupDollWeapon
0x027ea834 = bl _getDefaultSkellWeapon
0x027ea8ac = bl _getDefaultSkellWeapon
0x027ea94c = nop
0x027ea9c4 = nop
0x027eaa3c = nop

# filter quest rewards
addNum = 0x02779870
0x0229572c = bl _addRewardItemEquipment
0x022957c4 = bl _addRewardItemEquipment
0x0229585c = bl _addRewardItemEquipment
0x022958f4 = bl _addRewardItemEquipment
# filter treasure box rewards
0x022d8d50 = bl _addRewardItemEquipment
# disable itembox full message for the above
0x022d8dc4 = nop
# filter mission event rewards
# important items
0x027a3f28 = bl _addNumAdjusted 
0x027a3fb8 = bl _addNumAdjusted
# pop items
addItem = 0x02365934
0x02389ef0 = bl _addItemAdjusted
# collectables
# 0x027a4008 = bl _addNumAdjusted
# 0x027a4098 = bl _addNumAdjusted
# materials
# 0x027a40e8 = bl _addNumAdjusted
# 0x027a4178 = bl _addNumAdjusted
# 0x42 unkown probably info
# 0x027a41c8 = bl _addNumAdjusted
# 0x027a4258 = bl _addNumAdjusted
# data probes
0x027a42a8 = bl _addNumAdjusted
0x027a4338 = bl _addNumAdjusted
# ground weapons
0x027a4410 = bl _addNumAdjusted
# 0x44 unkown
# 0x027a45ac = bl _addNumAdjusted
# 0x027a463c = bl _addNumAdjusted

# disable field skills
0x0238e138 = nop

0x02814cf4 = b _prepareBladeTerminal # in loadEnd::ScriptManager

# overwrite setLocal for blade flag
0x0228f018 = bl _setLocal

# add new run speed
0x0264332c = bl _setRunSpeed
0x0240ab90 = stw r0, +0x14(r1) # swap order with following instruction
0x0240ab94 = bl _ToggleSuperRunningState
0x025051ec = bl _UpdateRunningState
0x02646808 = bl _setFasterSwimSpeed

# set movement variables
setValueFloat = 0x02003148
setValueBool = 0x02003178
setValueInt = 0x0200a5d0
getMappedId = 0x02007f90
getValueName = 0x020030e0
0x0263b660 = bl _initImplCharaAdjusted # innerChara
initImpl_EventCharacter = 0x02635b80
0x02617f04 = bl _initImplDollAdjusted # doll
initImpl_UnitCharacter = 0x02612524
0x0246eecc = bl _initDollActParam # doll act param
# remove original hardcoded values
0x02622110 = nop # just sets to 1.0 on entering run doll
0x0261fed8 = nop # on entering walk doll


addItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::Type::ItemHandle
getItem = 0x021ab180 # ::ItemDrop::ItemDropManager
getItemNum = 0x021ab164 # ::ItemDrop::ItemDropManager

# Temporary Debug Functions
# 0x0200a634 = bl setValueFloatTemporary
#endif

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

0x02b051a4 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051c4 = nop # remove original error message

# join division only if you get blade license
0x02c20118 = nop

# disable getting skell after skell license quest in doll_present
0x029cc078 = nop # disable doll creation
0x029cc088 = nop # disable doll assign

# bdat changes at startup
getMember = 0x029c1ddc

# required quest items from equipment disallow sell
0x02b73a20 = bl _getFlagValAdjusted

# filter enemy rewards
0x02b07540 = bl _getItemNumAdjusted
0x02b076d4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07584
_itemLoopEnd = 0x02b076e8

# disable affinity quest arts reward
0x029c7dc0 = li r3,0

__strcmp = 0x03b16c50

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604
shopTerminalScenarioFlagPtr = 0x20343634

# mandatory disable shops
0x02a79100 = bl _filterDevices  # blueprints + augments
0x02a7ced4 = nop  # doll blueprints
# optional shops # need paramaterization
makeWpnItemList = 0x02a2ca6c
0x02a326d0 = bl makeWpnItemListAdjusted
makeAmrItemList = 0x02a2da48
0x02a326f8 = bl makeAmrItemListAdjusted
makeDlWpnItemList = 0x02a2e608
0x02a32720 = bl makeDlWpnItemListAdjusted
makeDlAmrItemList = 0x02a2f088
0x02a32748 = bl makeDlAmrItemListAdjusted
makeDollItemList = 0x02a2fc78
0x02a32770 = bl makeDollItemListAdjusted
# shop equip no longer upgrades but rather adds the new tiers
0x02a2ca08 = nop  # ground
0x02a2e5a4 = nop  # doll
# shop buy equip no longer has an equip option
0x02a4422c = li r4, 0xa  # use menu 10 instead of 4
0x02a44234 = addi r5, r5, 0x3f4  # use the corresponding buy function
# unlist items you already bought from shop
isSellItemByMaker = 0x02a2c928
isSellDollItemByMaker = 0x02a2e4c4
isSellDollAssetItemByMaker = 0x02a2fb58
# armor
0x02a2db08 = bl isSellItemByMakerArmorPreAdjusted
0x02a2db7c = bl isSellItemByMakerArmorPreAdjusted
0x02a2dbf0 = bl isSellItemByMakerArmorPreAdjusted
0x02a2dc64 = bl isSellItemByMakerArmorPreAdjusted
0x02a2dcf8 = bl isSellItemByMakerArmorPreAdjusted
0x02a2dea8 = bl isSellItemByMakerArmorAdjusted
# weapons
0x02a2cb2c = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cba0 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cc14 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cc88 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cd24 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cedc = bl isSellItemByMakerWeaponAdjusted
# doll armor
0x02a2f148 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f1bc = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f230 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f2a4 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f338 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f4e8 = bl isSellItemByMakerDollArmorAdjusted
# doll weapons
0x02a2e6c8 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e73c = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e7b0 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e824 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e8b8 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2ea54 = bl isSellItemByMakerDollWeaponAdjusted
# doll frames
0x02a2fda0 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2fe18 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2fe90 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2ff08 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2ffa8 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a30124 = bl isSellDollAssetItemByMakerDollFrameAdjusted
# augments change text color to indicate already done
writeText = 0x02c9c9c4
0x02a82168 = bl writeTextAdjusted
0x02a8207c = bl writeTextAdjusted

# mark shop locations
0x02a8334c = bl reqMenuAddAugmentFromIdAdjusted
0x02a7ccfc = bl reqMenuAddBlueprintFromIdAdjusted
0x02a40c00 = bl BuyDollAdjusted  # doll frame shop
0x02a402a4 = bl reqMenuAddShopItemFromIdAdjusted

# disable items from collepedia
0x02a0acf4 = nop

# miranium get not decreased after lshop upgrade
0x02a40ecc = nop

# extend system log duration
0x02c04440 = li r9, 0xff

openHudTelop = 0x02c91f3c # ::MenuTask
chkLv = 0x02af8e7c # ::menu::MenuDollGarage
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

0x02b05194 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051b4 = nop # remove original error message

# join divison only if blade license
0x02c20124 = nop

# disable getting skell after skell license quest in doll_present
0x029cc068 = nop # disable doll creation
0x029cc078 = nop # disable doll assign

# bdat changes at startup
getMember = 0x029c1dcc

# required quest items from equipment disallow sell
0x02b73a10 = bl _getFlagValAdjusted

# filter enemy rewards
0x02b07530 = bl _getItemNumAdjusted
0x02b076c4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07574
_itemLoopEnd = 0x02b076d8

# disable affinity quest arts reward
0x029c7db0 = li r3,0

__strcmp = 0x03b16bd0

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604-0xB821D
shopTerminalScenarioFlagPtr = 0x20343634-0xB821D

# mandatory disable shops
0x02a790f0 = bl _filterDevices
0x02a7cec4 = nop  # doll blueprints
# optional shops # need paramaterization
makeWpnItemList = 0x02a2ca5c
0x02a326c0 = bl makeWpnItemListAdjusted
makeAmrItemList = 0x02a2da38
0x02a326e8 = bl makeAmrItemListAdjusted
makeDlWpnItemList = 0x02a2e5f8
0x02a32710 = bl makeDlWpnItemListAdjusted
makeDlAmrItemList = 0x02a2f078
0x02a32738 = bl makeDlAmrItemListAdjusted
makeDollItemList = 0x02a2fc68
0x02a32760 = bl makeDollItemListAdjusted
# shop equip no longer upgrades but rather adds the new tiers
0x02a2c9f8 = nop  # ground
0x02a2e594 = nop  # doll
# shop buy equip no longer has an equip option
0x02a4421c = li r4, 0xa  # use menu 10 instead of 4
0x02a44224 = addi r5, r5, 0x3e4  # use the corresponding buy function
# unlist items you already bought from shop
isSellItemByMaker = 0x02a2c918
isSellDollItemByMaker = 0x02a2e4b4
isSellDollAssetItemByMaker = 0x02a2fb48
# armor
0x02a2daf8 = bl isSellItemByMakerArmorPreAdjusted
0x02a2db6c = bl isSellItemByMakerArmorPreAdjusted
0x02a2dbe0 = bl isSellItemByMakerArmorPreAdjusted
0x02a2dc54 = bl isSellItemByMakerArmorPreAdjusted
0x02a2dce8 = bl isSellItemByMakerArmorPreAdjusted
0x02a2de98 = bl isSellItemByMakerArmorAdjusted
# weapons
0x02a2cb1c = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cb90 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cc04 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cc78 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cd14 = bl isSellItemByMakerWeaponPreAdjusted
0x02a2cecc = bl isSellItemByMakerWeaponAdjusted
# doll armor
0x02a2f138 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f1ac = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f220 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f294 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f328 = bl isSellItemByMakerDollArmorPreAdjusted
0x02a2f4d8 = bl isSellItemByMakerDollArmorAdjusted
# doll weapons
0x02a2e6b8 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e72c = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e7a0 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e814 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2e8a8 = bl isSellItemByMakerDollWeaponPreAdjusted
0x02a2ea44 = bl isSellItemByMakerDollWeaponAdjusted
# doll frames
0x02a2fd90 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2fe08 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2fe80 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2fef8 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a2ff98 = bl isSellDollAssetItemByMakerDollFramePreAdjusted
0x02a30114 = bl isSellDollAssetItemByMakerDollFrameAdjusted
# augments change text color to indicate already done
writeText = 0x02c9c964
0x02a82158 = bl writeTextAdjusted
0x02a8206c = bl writeTextAdjusted

# mark shop locations
0x02a8333c = bl reqMenuAddAugmentFromIdAdjusted
0x02a7ccec = bl reqMenuAddBlueprintFromIdAdjusted
0x02a40bf0 = bl BuyDollAdjusted  # doll frame shop
0x02a40294 = bl reqMenuAddShopItemFromIdAdjusted

# disable items from collepedia
0x02a0ace4 = nop

# miranium get not decreased after lshop upgrade
0x02a40ebc = nop

# extend system log duration
0x02c04430 = li r9, 0xff

openHudTelop = 0x02c91edc # ::MenuTask
chkLv = 0x02af8e6c # ::menu::MenuDollGarage
#endif

// Parameters from rules.txt
int disableGroundArmor, disableGroundWeapons, disableSkellArmor, disableSkellWeapons, disableGroundAugments, disableSkellAugments, disableImportantItems, disableBlueprints, drifterRangedWeapon, drifterMeleeWeapon, includeShopBlueprints,
includeShopArmor, includeShopWeapons, includeShopAugments, includeShopSkellArmor, includeShopSkellWeapons, includeShopSkellAugments, includeShopSkellFrames;
float fastWalkSpeedFloat, fastRunSpeedFloat, fasterRunSpeedFloat;
int fastRunningState = 0, fasterRunPlaySound = 0, fasterRunningState = 0;
int _augmentMenuType = 0;

extern int characterLevel;

extern int* menuBasePtr;
extern int bladeTerminalScenarioFlagPtr, shopTerminalScenarioFlagPtr;
extern void* _itemLoopStart;
extern void* _itemLoopEnd;

int __strcmp (const char* str1, const char* str2);
int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int IsReady(int value);
int getMyUnionNo(int* ptr);
int EntryUnion(int* ptr, int union_id);

int* getFP(const char* bdat);
int getValCheck(int* bdatPtr, const char* columnName, int id, int offset);

void Create_DataInit();
int* getMember(int* bdatPtr, const char* columnName);

void openHudTelop(int* menuBasePtr, int errorIdx);
int chkLv(int p1, int p2);

int addItemEquipment(int type, int id, int* data, int flag);
int addNum(int* ptr, int type, int* data, int flag);
int addItem(int type, int id, int* item);
void addInnerExp(int* ptr, int exp, int value);

int* getItem(int* ptr, int enemies, int boxes, int items);
int getItemNum(int* ptr, int enemies, int boxes);

int getFlagVal(int* bdatPtr, const char* flagName, int id, const char* columnName);

void _playSound(int id);

char* getValueName(int* ptr, int id);
int getMappedId(int* ptr, int zero, int id);
void setValueFloat(float value, int* ptr, int mapId);
void initImpl_EventCharacter(int** ptr, int* ptr2);
void initImpl_UnitCharacter(int** ptr, int* ptr2);

void makeWpnItemList(int* cshop);
void makeAmrItemList(int* cshop);
void makeDlWpnItemList(int* cshop);
void makeDlAmrItemList(int* cshop);
void makeDollItemList(int* cshop);

int isSellItemByMaker(int* cshop, int makerId, int makerLvl);
int isSellDollItemByMaker(int* cshop, int makerId, int makerLvl);
int isSellDollAssetItemByMaker(int* cshop, int makerId, int makerLvl);

void setKnowledgeBit(int id, int bit, int doll);
int getKnowledgeBit(int id, int bit, int doll);
void reqMenuAddItemFromId(int type, int id, int count);
void _getArchipelagoShop();

void _writeConsole(char* output);

void writeText(int* ptr, int* ptr2, char* text, int color, int glow, int v1, int v2);

void _filterDevices(){
	register int selectedOption asm("r6");
	register int errorMessage asm("r4");
	register char* menuPtr asm("r30");
	int backup = errorMessage;
	if(menuPtr[0x1ac] == 4){
		if(selectedOption >= 0 && selectedOption <= 1)
			if(!includeShopAugments && !disableGroundAugments)
				backup = 485;
			else{
				_augmentMenuType = 0;
				_getArchipelagoShop();
			}
		if(selectedOption >= 2 && selectedOption <= 4)
			if(!includeShopSkellAugments && !disableSkellAugments)
				backup = 485;
			else {
				_augmentMenuType = 1;
				_getArchipelagoShop();
			}
	}
	else if(menuPtr[0x1ac] == 3){
		if(!includeShopBlueprints)
			backup = 485;
		else
			_getArchipelagoShop();
	}
	
	errorMessage = backup;
	asm("cmpwi cr0, r4, 0");
}

void makeWpnItemListAdjusted(int* cshop){
	if(!includeShopWeapons && !disableGroundWeapons)
		return;
	_getArchipelagoShop();
	makeWpnItemList(cshop);
}
void makeAmrItemListAdjusted(int* cshop){
	if(!includeShopArmor && !disableGroundArmor)
		return;
	_getArchipelagoShop();
	makeAmrItemList(cshop);
}
void makeDlWpnItemListAdjusted(int* cshop){
	if(!includeShopSkellWeapons && !disableSkellWeapons)
		return;
	_getArchipelagoShop();
	makeDlWpnItemList(cshop);
}
void makeDlAmrItemListAdjusted(int* cshop){
	if(!includeShopSkellArmor && !disableSkellArmor)
		return;
	_getArchipelagoShop();
	makeDlAmrItemList(cshop);
}
void makeDollItemListAdjusted(int* cshop){
	if(!includeShopSkellFrames)
		return;
	_getArchipelagoShop();
	makeDollItemList(cshop);
}

void reqMenuAddAugmentFromIdAdjusted(int type, int id, int count){
	if((type == 0x14 || type == 0x15) && includeShopAugments)
		setKnowledgeBit(id, 0x02, 0);
	else if(type >= 0x16 && type <= 0x18 && includeShopSkellAugments)
		setKnowledgeBit(id, 0x02, 1);
	else
		reqMenuAddItemFromId(type, id, count);
}
void reqMenuAddBlueprintFromIdAdjusted(int type, int id, int count){
	if(!includeShopBlueprints)
		reqMenuAddItemFromId(type, id, count);
}
int _getShopIdx(const char* bdat_name, int itemId, bool dropLastColumn = false){
	int* shpPtr = getFP(bdat_name);
	int value;
	int baseOffset = (int)((short*)shpPtr)[0x7];
	// rowSize is dependant on alignment each row start on aligned 0x4 bytes
	int rowSize = (int)((short*)shpPtr)[0x4] >> 1;
	int realRowSize = rowSize - 1;
	if(dropLastColumn)
		realRowSize -= 1;
	for(int row = 0; true; row++){
		for(int column = 0; column < realRowSize; column++){
			value = (int)((short*)((char*)shpPtr + baseOffset))[row * rowSize + column];
			if(itemId == value)
				return row * realRowSize + column + 1;
		}
	}
}
void reqMenuAddShopItemFromIdAdjusted(int type, int id, int count){
	if(type >= 1 && type <= 5 && includeShopArmor)
		setKnowledgeBit(_getShopIdx("SHP_AmrPC", id), 0x08, 0);
	else if(type >= 6 && type <= 7 && includeShopWeapons)
		setKnowledgeBit(_getShopIdx("SHP_WpnPC", id, true), 0x04, 0);
	else if(type >= 0xa && type <= 0xe && includeShopSkellArmor)
		setKnowledgeBit(_getShopIdx("SHP_AmrDL", id), 0x08, 1);
	else if(type >= 0xf && type <= 0x13 && includeShopSkellWeapons)
		setKnowledgeBit(_getShopIdx("SHP_WpnDL", id), 0x04, 1);
	else
		reqMenuAddItemFromId(type, id, count);
}
void BuyDollAdjusted(int id){
	if(includeShopSkellFrames)
		setKnowledgeBit(id, 0x10, 1);
}

int isSellItemByMakerArmorPreAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r20");
	if(includeShopArmor && getKnowledgeBit(_getShopIdx("SHP_AmrPC", itemId), 0x08, 0) != 0)
		return 0;
	else
		return isSellItemByMaker(cshop, makerId, makerLvl);
}
int isSellItemByMakerArmorAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r22");
	if(includeShopArmor && getKnowledgeBit(_getShopIdx("SHP_AmrPC", itemId), 0x08, 0) != 0)
		return 0;
	else
		return isSellItemByMaker(cshop, makerId, makerLvl);
}

int isSellItemByMakerWeaponPreAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r20");
	if(includeShopWeapons && getKnowledgeBit(_getShopIdx("SHP_WpnPC", itemId, true), 0x04, 0) != 0)
		return 0;
	else
		return isSellItemByMaker(cshop, makerId, makerLvl);
}
int isSellItemByMakerWeaponAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r23");
	if(includeShopWeapons && getKnowledgeBit(_getShopIdx("SHP_WpnPC", itemId, true), 0x04, 0) != 0)
		return 0;
	else
		return isSellItemByMaker(cshop, makerId, makerLvl);
}

int isSellItemByMakerDollArmorPreAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r20");
	if(includeShopSkellArmor && getKnowledgeBit(_getShopIdx("SHP_AmrDL", itemId), 0x08, 1) != 0)
		return 0;
	else
		return isSellDollItemByMaker(cshop, makerId, makerLvl);
}
int isSellItemByMakerDollArmorAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r21");
	if(includeShopSkellArmor && getKnowledgeBit(_getShopIdx("SHP_AmrDL", itemId), 0x08, 1) != 0)
		return 0;
	else
		return isSellDollItemByMaker(cshop, makerId, makerLvl);
}

int isSellItemByMakerDollWeaponPreAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r20");
	if(includeShopSkellWeapons && getKnowledgeBit(_getShopIdx("SHP_WpnDL", itemId), 0x04, 1) != 0)
		return 0;
	else
		return isSellDollItemByMaker(cshop, makerId, makerLvl);
}
int isSellItemByMakerDollWeaponAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r25");
	if(includeShopSkellWeapons && getKnowledgeBit(_getShopIdx("SHP_WpnDL", itemId), 0x04, 1) != 0)
		return 0;
	else
		return isSellDollItemByMaker(cshop, makerId, makerLvl);
}

int isSellDollAssetItemByMakerDollFramePreAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemIdx asm("r23");
	if(includeShopSkellFrames && getKnowledgeBit(itemIdx, 0x10, 1) != 0)
		return 0;
	else
		return isSellDollAssetItemByMaker(cshop, makerId, makerLvl);
}
int isSellDollAssetItemByMakerDollFrameAdjusted(int* cshop, int makerId, int makerLvl){
	register int itemId asm("r20");
	if(includeShopSkellFrames && getKnowledgeBit(itemId, 0x10, 1) != 0)
		return 0;
	else
		return isSellDollAssetItemByMaker(cshop, makerId, makerLvl);
}

void writeTextAdjusted(int* ptr, int* ptr2, char* text, int color, int glow, int v1, int v2){
	register int idx asm("r29");
	register char* basePtr asm("r23");
	int id = (int)*(unsigned short*)(basePtr + idx * 0xc + 0x8);
	int purpleColor = 0x18;
	if(includeShopSkellAugments && _augmentMenuType == 1 && getKnowledgeBit(id, 0x2, 1) != 0){
		writeText(ptr, ptr2, text, purpleColor, 0, v1, v2);
	}else if(includeShopAugments && _augmentMenuType == 0 && getKnowledgeBit(id, 0x2, 0) != 0){
		writeText(ptr, ptr2, text, purpleColor, 0, v1, v2);
	}else{
		writeText(ptr, ptr2, text, color, glow, v1, v2);
	}
}

int _IsPermit(){
	return _hasPreciousItem(24 + 3 - 1);
}

int _IsReadyAdjusted(int value){
	if(_hasPreciousItem(24 + 3 - 1)) return IsReady(value);
	return 0;
}

int _assignDollCheck(int p1, int p2){
	if(!_hasPreciousItem(24 + 1 - 1)){
		// display error message for missing skell license
		// check https://xenoblade.github.io/xbx/bdat/common_local_us/MNU_CommonTelop.html
		// -> https://xenoblade.github.io/xbx/bdat/common_ms/MNU_CommonTelop_ms.html
		openHudTelop(menuBasePtr, 12);
		return 0;
	}
	if(chkLv(p1,p2) == 0){	
		openHudTelop(menuBasePtr, 0x1ae);
		return 0;
	}
	return 1;
}

// overwrite starting weapon with default weapon
// from https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_PcList.html for Weapon calls
// take class instead and match https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_ClassInfo.html#30
// to get default weapon
int _getDefaultWeapon(int* DEF_PcList_bdat, char weaponColumn[], int charId, int offset){
	int* bdatPtr = getFP("CHR_ClassInfo");
	int classId = getValCheck(DEF_PcList_bdat, "ClassType", charId, 1) >> 0x18;
	// convert DefWpnFar -> FarWeapon
	char newWeaponColumn[0x20];
	char* weaponType = weaponColumn + 6; 
	__sprintf_s(newWeaponColumn, 0x20, "%sWeapon", weaponType);
	return getValCheck(bdatPtr, newWeaponColumn, classId, 1) >> 0x8;
}

// overwrite starting skell weapon with default weapon
// from https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_PcList.html for Weapon calls
// offset is the index
// weaponColumn is "WPN" with https://xenoblade.github.io/xbx/bdat/common_local_us/WPN_DlList.html
// returns id of part shifted left by 0x10
int _getDefaultSkellWeapon(int* DEF_DlList_bdat, char weaponColumn[], int skellId, int offset){
	// Left 
	if (offset == 0) return 0x20000;
	if (offset == 1) return 0x10000;
	return 0;
}

void _setRunSpeed(){
	register float value asm("fr1");
	value = fastRunSpeedFloat;
	if (fastRunningState == 1 && fasterRunningState == 1){
		// Load float value
		value = fasterRunSpeedFloat;
		if (fasterRunPlaySound == 1){
			fasterRunPlaySound = 0;
			_playSound(0x2d4);
		}
	}
}

void _UpdateRunningState(int* ptr, int newRunningState){
	int backup;
	register int original asm("r26");
	backup = original;

	fastRunningState = original;
	if(fastRunningState == 1)
		fasterRunningState = 0;

	original = backup;
	asm("cmpwi cr0, r26, 0");
}

void _ToggleSuperRunningState(){
	int backup;
	register int original asm("r3");
	backup = original;
	if(fasterRunningState == 0){
		fasterRunningState = 1;
		fasterRunPlaySound = 1;
	}else if(fasterRunningState == 1)
		fasterRunningState = 0;
	// Restore condition register
	original = backup;
	asm("cmpwi cr0, r3, 0");
}

int _FindSystemVariableByName(int* valuePtr, char* name){
	for (int id = 0; true; id++){
		if(__strcmp(name, getValueName(valuePtr + 3, id)) == 0)
			return id;
	}
}

int** _setFasterSwimSpeed(int** ptr){
	char* name = (char*)"VF_MoveSpeedSwimDash";
	float value = fastRunSpeedFloat;
	if (fastRunningState == 1 && fasterRunningState == 1){
		// Load float value
		value = fasterRunSpeedFloat;
		if (fasterRunPlaySound == 1){
			fasterRunPlaySound = 0;
			_playSound(0x2d4);
		}
	}
	int* valuePtr = ptr[1];
	setValueFloat(value, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));

	// original instruction
	asm("li r4,2");
	return ptr;
}

float getValueFloatDirect(float** handle, int mapId){
	return handle[0xa7][mapId * 3 + 2];
}

// Temporary Debug Function
void setValueFloatTemporary(float value, int* ptr, int mapId){
	char buffer[200];
	int newValue = value * 1000;
	// if(mapId == 0x79) asm("nop");
	__sprintf_s(buffer, 200, "Name: %s, Id: %d, Value: %d.%03d\n", getValueName(ptr, mapId), mapId, newValue / 1000, newValue % 1000);
	_writeConsole(buffer);
	return setValueFloat(value, ptr, mapId);
}

void _InitCharaSystemVariables(int ** ptr, int* ptr2){
	int* valuePtr = ptr[1];

	// Addional functions for debugging id mapping
	// int mapId = getMappedId(valuePtr, 0, id);
	char* name = (char*)"VF_MoveSpeedSwimRun";
	setValueFloat(fastWalkSpeedFloat, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));
	name = (char*)"VF_MoveSpeedSwimDash";
	setValueFloat(fastRunSpeedFloat, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));

	name = (char*)"VF_MoveSpeedRun";
	setValueFloat(fastRunSpeedFloat, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));

	// Available
	// setValueBool(valuePtr + 3, mapId, true); // Start with VB_
	// setValueInt(valuePtr + 3, id, newValueInt); // Start with VI_
}

void _initImplCharaAdjusted(int ** ptr, int* ptr2){
	_InitCharaSystemVariables(ptr, ptr2);
	initImpl_EventCharacter(ptr, ptr2);
}

float dollMaxVelocity = 1.0;
void _InitDollSystemVariables(int ** ptr){
	int* valuePtr = ptr[1];

	char* name = (char*)"VF_CarDashMaxVelocity";
	float value = getValueFloatDirect((float**)valuePtr, _FindSystemVariableByName(valuePtr, name));
	if(value != dollMaxVelocity){
		value *= fastRunSpeedFloat;
		dollMaxVelocity = value;
	}
	setValueFloat(value, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));

	name = (char*)"VF_MoveSpeedFieldMove";
	setValueFloat(fastWalkSpeedFloat, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));
	name = (char*)"VF_MoveSpeedHoverDash";
	setValueFloat(fastRunSpeedFloat, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));
	name = (char*)"VF_MoveSpeedRun";
	setValueFloat(fastRunSpeedFloat, valuePtr + 3, _FindSystemVariableByName(valuePtr, name));
}

void _initImplDollAdjusted(int ** ptr, int* ptr2){
	_InitDollSystemVariables(ptr);
	initImpl_UnitCharacter(ptr, ptr2);
}

// from https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_DlActParam.html
void _initDollActParam(){
	register int*** self asm("r30");
	_InitDollSystemVariables(self[5]);

	// original instruction
	asm("or r3,r26,r26");
}


void _SetBdatValue(const char* bdatName, const char* columnName, int rowId, int newValue, int valueSize){
	int* bdat = getFP(bdatName);
	int* columnPtr = getMember(bdat, columnName);
	short columnOffsetBase = *(short*)(columnPtr);
	// ignore value check for simplicity
	// char* valCheckPtr = getValCheckSub(bdat, getMember(bdat, columnName), valueSize);
	int baseOffset = *(short*)((char*)bdat + 0xe);
	int rowOffset = (*(short*)((char*)bdat + 0x8)) * (rowId - 1);
	int columnOffset = *(short*)((char*)bdat + 0x2 + columnOffsetBase);
	char* valPtr = (char*)bdat + baseOffset + rowOffset + columnOffset;
	if (valueSize == 1)
		*valPtr = newValue;
	else if (valueSize == 2)
		*(short*)valPtr = newValue;
	else if (valueSize == 4)
		*(int*)valPtr = newValue;
}

void _Create_DataInit_Adjusted(){
	_SetBdatValue("CHR_ClassInfo", "NearWeapon", 1, drifterMeleeWeapon, 1);
	_SetBdatValue("CHR_ClassInfo", "FarWeapon", 1, drifterRangedWeapon, 1);
	_SetBdatValue("CHR_ClassInfo", "defNear", 1, drifterMeleeWeapon, 2);
	_SetBdatValue("CHR_ClassInfo", "defFar", 1, drifterRangedWeapon, 2);

	// from 0x02a3d604
	int purchaseTitleNameOffset = 0xdf72;
	_SetBdatValue("menu_program_ms", "name", 4439, purchaseTitleNameOffset, 4);

	Create_DataInit();
}

// Unlock Blade Lvl
int _isUnlock(int* ptr, int value2){
	// join division if you havent
	if(getMyUnionNo(ptr) == 0) EntryUnion(ptr, 1);
	return _hasPreciousItem(24 + 5 - 1);
}

// keep in mind that you need to reload your skell to trigger this
// best way is to go into active members and press confirm once
int _loadSkyUnit(){
	return _hasPreciousItem(24 + 2 - 1);
}

int _loadFNet(){
	return _hasPreciousItem(24 + 4 - 1) * 3001;
}

int _checkType(int type){
	if(type >= 0x1 && type <= 0x5) return disableGroundArmor;
	if(type >= 0x6 && type <= 0x7) return disableGroundWeapons;
	if(type >= 0xa && type <= 0xe) return disableSkellArmor;
	if(type >= 0xf && type <= 0x13) return disableSkellWeapons;
	if(type >= 0x14 && type <= 0x15) return disableGroundAugments;
	if(type >= 0x16 && type <= 0x18) return disableSkellAugments;
	if(type == 0x1d) return disableImportantItems;
	if(type == 0x41) return disableBlueprints;
	if(type >= 0x18 && type != 0x1c) return 1;
	return 0;
}

int _addRewardItemEquipment(int type, int id, int* data, int flag){
	if(_checkType(type)){
		return addItemEquipment(type, id, data, flag);
	}
	return 0;
}

void _addNumAdjusted(int* ptr, int type, int* data, int flag){
	if(_checkType(type)){
		addNum(ptr, type, data, flag);
	}
	return;
}

int _addItemAdjusted(int type, int id, int* item){
	if(_checkType(type)){
		return addItem(type, id, item);
	}
	return 0;
}

void _addInnerExpAdjusted(int* ptr, int exp, int value){
	if(!characterLevel){
		addInnerExp(ptr, exp, value);
	}
}

int _getFlagValAdjusted(int* bdatPtr, const char* flagName, int id, const char* columnName){
	register int type asm("r30");
	// AMR: Combat Bodywear 1-3
	if(type == 0x2 && (id == 246 || id == 251 || id == 256)) return 1;
	// WPN: Iron Sword
	if(type == 0x7 && (id == 26 || id == 27 || id == 28)) return 1;
	// WPN: Chrome Sword
	if(type == 0x7 && (id == 32 || id == 33 || id == 34)) return 1;
	// WPN: Iron Blades
	if(type == 0x7 && (id == 287 || id == 288 || id == 289)) return 1;
	// WPN: Chrome Knife
	if(type == 0x7 && (id == 550 || id == 551 || id == 552)) return 1;
	// WPN: Titanium Shield
	if(type == 0x7 && (id == 810 || id == 811 || id == 812)) return 1;
	// WPN: Soldier Assault Rifle
	if(type == 0x6 && (id == 1587 || id == 1588 || id == 1589)) return 1;
	// WPN: Warrior Assault Rifle
	if(type == 0x6 && (id == 1590 || id == 1591 || id == 1592)) return 1;
	return getFlagVal(bdatPtr, flagName, id, columnName);
}

int _getItemNumAdjusted(int* ptr, int enemies, int boxes){
	int count = 0;
	int num = getItemNum(ptr, enemies, boxes);
	for(int i = 0; i < num; i++){
		int itemType = *(char*)getItem(ptr, enemies, boxes, i);
		if(_checkType(itemType)) count++;
	}
	return count;
}
int _itemLoopAdjustment(int* ptr, int enemies, int boxes, int idx, int offset){
	int type = *(char*)getItem(ptr, enemies, boxes, idx);
	if(_checkType(type)) offset += 0x1c;
	return offset;
}
int _itemLoopContinue(int* ptr, int enemies, int boxes, int idx){
	int num = getItemNum(ptr, enemies, boxes);
	if(idx < num) return 1;
	return 0;
}

void _prepareBladeTerminal(){
	if(bladeTerminalScenarioFlagPtr == 3001){
		if(_hasPreciousItem(24 + 5 - 1)) bladeTerminalScenarioFlagPtr = 0;
		else bladeTerminalScenarioFlagPtr = 0x7fffff;
	}
	if(shopTerminalScenarioFlagPtr == 2001){
		if(_hasPreciousItem(24 + 5 - 1)) shopTerminalScenarioFlagPtr = 0;
		else shopTerminalScenarioFlagPtr = 0x7fffff;
	}
}

// Do not call this function directly, but rather call the first label
// Intellisense works only properly with g++ as a compiler 
// https://code.visualstudio.com/docs/cpp/configure-intellisense-crosscompilation#_compiler-path
void _preItemLoopAdjustmentWrapper(){
	asm(".global _preItemLoopAdjustment:");
	asm ("_preItemLoopAdjustment:");
    register int boxNum asm("r22");
    register int dropNum asm("r20");
    register int idx asm("r18");
    register int* ptr asm("r31");
    register int offset asm("r23");
	offset = _itemLoopAdjustment(ptr, boxNum, dropNum, idx, offset);
	int value = _itemLoopContinue(ptr, boxNum, dropNum, idx);
	idx++;
	if(value == 0) goto *&_itemLoopEnd;
	goto *&_itemLoopStart;
}

// Overwrite the unlock BladeLvl flag from add.cpp
void _setLocal(const int width, const int position){
	register int value asm("r5");
	if(width == 2 && value == 1){
		if((position == _collepediaFlag || position == _bladeFlag) && !_hasPreciousItem(24 + 5 - 1))
			value = 0;
	}

	// original instruction from 0x0228f018
	asm("lis r9, 0x103a");
	return;
}
