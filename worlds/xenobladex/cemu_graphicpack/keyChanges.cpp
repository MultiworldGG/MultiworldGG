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

# disable affinity quest arts reward
0x029c7dc0 = li r3,0

0x02814cf4 = b _prepareBladeTerminal # in loadEnd::ScriptManager

# reconfigure rentalCharTerminal to LShop
0x028eacc8 = bl _prepareRentalCharTerminal
beginScript = 0x028cb70c # ::Gimmick::GimmickMapObj

# overwrite setLocal for blade flag
0x0228f018 = bl _setLocal

addItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::Type::ItemHandle
getItem = 0x021ab180 # ::ItemDrop::ItemDropManager
getItemNum = 0x021ab164 # ::ItemDrop::ItemDropManager
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

# required quest items from equipment disallow sell
0x02b73a20 = bl _getFlagValAdjusted

# filter enemy rewards
0x02b07540 = bl _getItemNumAdjusted
0x02b076d4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07584
_itemLoopEnd = 0x02b076e8

__strcmp = 0x03b16c50

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604
shopTerminalScenarioFlagPtr = 0x20343634

# mandatory disable shops
0x02a32770 = nop # skell frame
0x02a69954 = nop # augment menu
0x02a69968 = nop # develop menu
# optional shops # need paramaterization
0x02a326d0 = nop # ground weapon
0x02a326f8 = nop # ground armor
0x02a32720 = nop # skell weapon
0x02a32748 = nop # skell armor

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
# need further testing
bladeTerminalScenarioFlagPtr = 0x20343604-0xB821D
shopTerminalScenarioFlagPtr = 0x20343634-0xB821D

# mandatory disable shops
0x02a32760 = nop # skell frame
0x02a69944 = nop # augment menu
0x02a69958 = nop # develop menu
# optional shops # need paramaterization
0x02a326c0 = nop # ground weapon
0x02a326e8 = nop # ground armor
0x02a32710 = nop # skell weapon
0x02a32738 = nop # skell armor

openHudTelop = 0x02c91edc # ::MenuTask
chkLv = 0x02af8e6c # ::menu::MenuDollGarage
#endif

// Parameters from rules.txt
int disableGroundArmor, disableGroundWeapons, disableSkellArmor, disableSkellWeapons, disableGroundAugments, disableSkellAugments, disableImportantItems, disableBlueprints;

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

void openHudTelop(int* menuBasePtr, int errorIdx);
int chkLv(int p1, int p2);

int addItemEquipment(int type, int id, int* data, int flag);
int addNum(int* ptr, int type, int* data, int flag);
int addItem(int type, int id, int* item);

int* getItem(int* ptr, int enemies, int boxes, int items);
int getItemNum(int* ptr, int enemies, int boxes);

int getFlagVal(int* bdatPtr, const char* flagName, int id, const char* columnName);

int beginScript(int** scriptPtr);


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

int _prepareRentalCharTerminal(int** scriptPtr){
	int* fldConsoleParamPtr = scriptPtr[0x29];
	if(__strcmp((char*)fldConsoleParamPtr,"fld_console.sb")) return beginScript(scriptPtr);
	int fldConsoleScriptId = fldConsoleParamPtr[9];
	if(fldConsoleScriptId == 2){
		if(_hasPreciousItem(24 + 5 - 1)) return beginScript(scriptPtr + 0x98);
		else {
			openHudTelop(menuBasePtr, 52);
			return 0; // does not matter
		}
	} 
	if(fldConsoleScriptId == 0xb) return beginScript(scriptPtr - 0x98);
	return beginScript(scriptPtr);
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
