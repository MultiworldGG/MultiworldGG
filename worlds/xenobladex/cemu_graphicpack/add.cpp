#include <cstddef>

extern int itemListBase;
extern int* fnetBasePtr;
extern char* fieldSkillBasePtr;
extern int _fieldSkillOffset;

unsigned int** getItemTypeInfo(int*, int);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

reqMenuAddItemFromId = 0x0234f1a8 # ::CmdReq
reqMenuAddItemFromInfo = 0x0234f5ec # ::CmdReq
reqMenuSetArtsLevel = 0x02347c1c # ::CmdReq
reqMenuSetSkillLevel = 0x02348b0c # ::CmdReq
SetFriendRank = 0x027faee0 # ::Util
GetClassDataPtr = 0x027fa7a0 # ::Util

_reqForceDamagePlayerTargetGoner = 0x021a88e4
getCharaHandle = 0x02373b9c

GetCharaDataPtr = 0x027f70ac # ::Util
setLocal = 0x0228f008 # ::GameFlag
changeScenarioFlag = 0x027d5638 # ::FNet
addGarage = 0x0234c620 # ::CmdCommon::SceneCmdPrm
#endif

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

SetDead = 0x0298f2f0
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

SetDead = 0x0298f2e0
#endif

int _collepediaFlag = 0x1286; // from funcCollepedia
int _bladeFlag = 0x1288; // from updataStatus::MenuTotalSimpleStatus

void reqMenuAddItemFromId(int type, int id, int count);
void reqMenuAddItemFromInfo(unsigned short* item, int count);
void reqMenuSetArtsLevel(char* characterBasePtr, int id, int lvl, int filler);
void reqMenuSetSkillLevel(char* characterBasePtr, int id, int lvl, int filler);
void SetFriendRank(int id, int lvl);
char* GetClassDataPtr(int id);

void _reqForceDamagePlayerTargetGoner(int player);
void SetDead(int unused, char* charaHandle);
void getCharaHandle(char* charaHandle, int partyIndex);

int * GetCharaDataPtr(int charaId);
void setLocal(int width, int position, int value);
void changeScenarioFlag(int* basePtr, int flag);
void addGarage(int* idPtr);

void* __malloc (size_t size);
void __free (void* ptr);


// 1 = Ground Armor Head			https://xenoblade.github.io/xbx/bdat/common_local_us/AMR_PcList.html
// 2 = Ground Armor Body
// 3 = Ground Armor Arm R
// 4 = Ground Armor Arm L
// 5 = Ground Armor Legs
// 6 = Ground Weapon Ranged			https://xenoblade.github.io/xbx/bdat/common_local_us/WPN_PcList.html
// 7 = Ground Weapon Melee
// 8 = Probably Avatar Creation 	// Don't use
// 9 = Skell Frame					https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_DlList.html (FrameId) => https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_DlList.html
// a = Skell Armor Head				https://xenoblade.github.io/xbx/bdat/common_local_us/AMR_DlList.html
// b = Skell Armor Torso
// c = Skell Armor Arm R
// d = Skell Armor Arm L
// e = Skell Armor Legs
// f = Skell Weapon Back			https://xenoblade.github.io/xbx/bdat/common_local_us/WPN_DlList.html
// 10 = Skell Weapon Shoulder
// 11 = Skell Weapon Shield
// 12 = Skell Weapon Sidearm
// 13 = Skell Weapon Spare
// 14 = Augment Ground Weapon		https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_inner.html
// 15 = Augment Ground Armor
// 16 = Augment Skell Frame			https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_doll.html
// 17 = Augment Skell Weapon
// 18 = Augment Skell Armor
// 19 = Precious Ressources			https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_RareRscList.html
// 1a = Materials					https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_MaterialList.html
// 1b = Collectable					https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_CollectList.html
// 1c = Data Probes					https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_BeaconList.html
// 1d = Important Items				https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PreciousList.html
// 1e = Appendage Fragments			https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PieceList.html
// 1f = Consumeable Items			https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_BattleItem.html
// 41 = Blueprints                  https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_Blueprint.html
void _addItem(int type, int id){
	if(type != 9){
		reqMenuAddItemFromId(type, id, 1);
	} else {
		addGarage(&id);
	}
}

short _gearItem[8] = { 0 };
void _addGear(int type, int id, int affixId1, int affixId2, int affixId3, int slotCount){

	unsigned short* _gearItem = (unsigned short*)__malloc(8 * sizeof(unsigned short));
	*(int*)_gearItem = (id << 19) + (type << 13) + (1 << 3);
	_gearItem[6] = affixId1 << 4;
	_gearItem[7] = affixId2 << 4;
	_gearItem[8] = affixId3 << 4;
	for(int i = 0; i < 3; i++){
		if (i < slotCount) _gearItem[9+i] = 0x0;
		else _gearItem[9+i] = 0xFFFF;
	}
	reqMenuAddItemFromInfo(_gearItem, 1);
	__free(_gearItem);
}

int _hasPreciousItem(int id){
	int * basePtr = &itemListBase;
	unsigned int* itemListPtr = *getItemTypeInfo(basePtr, 0x1d);
	for(int idx = 0; idx < 300; idx++){
		unsigned int itemType = itemListPtr[0] << 13 >> 26;
		if(itemType != 0x1d) break;
		unsigned int itemId = itemListPtr[0] >> 19;
		if(id == itemId) return 1;
		itemListPtr += 3;
	}
	return 0;
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ArtsList.html
void _addArt(int id, int lv){
	for (int charId = 0; charId < 0x13; charId++)
		reqMenuSetArtsLevel((char*)GetCharaDataPtr(charId), id, lv, 0);
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_SkillClass.html
void _addSkill(int id, int lv){
	for (int charId = 0; charId < 0x13; charId++)
		reqMenuSetSkillLevel((char*)GetCharaDataPtr(charId), id, lv, 0);
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_PcList.html
void _addFriend(int id, int lv){
	SetFriendRank(id, lv);
}

// 1 = Mechanical, 2 = Biological, 3 = Archeological
void _addFieldSkill(int id, int lv){
	char* fieldSkillOffset = fieldSkillBasePtr;
	fieldSkillOffset += _fieldSkillOffset - 1;
	fieldSkillOffset += id - 1;
	*fieldSkillOffset = (char)lv;
}

// 1 = Skell License, 2 = Flight Module, 3 = Overdrive, 4 = FNet, 5=Blade
// Some important unlocks are tied to the scenario flag, which is not desired
// Replace all functions with a call to our own for these items
// To anchor them in the savedata we use unused items from the "Important Items" Category
// Specifically 24-31 from https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PreciousList.html
void _addKey(int id, int flag){

	// 4: FNET
	// from initialize::fnet::FnetTask where param_1 + 0xe must be 2
	// to accomplish this you need to set the scenerio flag to at least 3001=0xbb9
	// https://xenoblade.github.io/xbx/bdat/common_local_us/FnetVeinConfig.html value at idx 8
	// the game is unable to unload during runtime so you need to save and restart to unset
	// the game unlocks the fnet in two stages at the start of chapter 2 it unlocks the grid view only
	// after you completed chapter 2 you get access to fast travel and the game manually unlocks each fn-node

	// 5: BLADE
	// there is not really a check in the game for the blade license
	// it only really checks if you are at least in chapter 3 via scenario flag 3002
	// the overriden check for the terminals can be found in keyChanges
	// but the blade rank exp is unlocked seperately at the start of chapter 3
	// get setLocal from id from there by trial and error

	if(id == 6){
		char charaHandle[8];
		getCharaHandle(charaHandle, 0);
		SetDead(0, charaHandle);
	}
	else if(id == 13) _reqForceDamagePlayerTargetGoner(0);
	
	// Only for testing
	else if(id == 0x20) setLocal(0x10, 1, flag);
	else if(id == 0x21) changeScenarioFlag(fnetBasePtr, flag);
	else if(id == 0x22) setLocal(1, flag, 1);

	else _addItem(0x1d, 24 + id - 1);
	
	int skellLicenseFlag = 0x5e5b; // IsDollLicense
	int flightModuleFlag = 0x7610; // getFlightUnitFlag
	int overdriveFlag = 0x6bc3; // IsPermit

	if(id == 1) setLocal(1, skellLicenseFlag, flag);
	else if(id == 2) setLocal(1, flightModuleFlag, flag);
	else if(id == 3) setLocal(1, overdriveFlag, flag);
	else if(id == 4) changeScenarioFlag(fnetBasePtr, flag*3001);
	else if(id == 5){
		setLocal(2, _collepediaFlag, 3);
		setLocal(2, _bladeFlag, 3);
	}
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_ClassInfo.html
void _addClass(int id, int lv){
	*GetClassDataPtr(id) = (char)lv;
}
