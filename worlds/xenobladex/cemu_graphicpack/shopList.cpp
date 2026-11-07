#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);
void* __calloc (size_t num, size_t size);
size_t __strlen (const char * str);
char* __strcpy(char *dest, const char *src);
void __free (void* ptr);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

GetKnowledgePtr = 0x027fb934
GetBlueprintPtr = 0x027fbae4
#endif

char _formatShopText[] = "SH Id=%03x Tp=%01x:";

char ** _shopArmorNames;
char ** _shopWeaponNames;
char ** _shopDollArmorNames;
char ** _shopDollWeaponNames;
char ** _shopDollFrameNames;
char ** _shopAugmentNames;
char ** _shopDollAugmentNames;
char ** _shopBlueprintNames;

char* GetKnowledgePtr();
char* GetBlueprintPtr();

// Use https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_inner.html +
// https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_doll.html to match the ids
// use the embedded remaining bits of the "new" item in savedata
char* _postShopList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	for(int id = 1; id < 200; id++){
		// 0=disabled, 1=visible, 2=new, 3=crafted
		char* blueprintPtr = GetBlueprintPtr();
		int blueprintFlag = (int)*(blueprintPtr + id);

		if (blueprintFlag == 3)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x6);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
	}
	
	// Available until 4000 but unused last 50 reserved for the permanent storage of battle items
    for(int id = 1; id < 3950; id++){
		char* knowledgePtr = GetKnowledgePtr();
		int dollOffset = 0x4ba4;  // type 0x4d
		int groundOffset = 0x3c04; // type 0x4c
		int dollFlag = (int)*(knowledgePtr + dollOffset + id);
		int groundFlag = (int)*(knowledgePtr + groundOffset + id);
		// Augments 0x02
		int dollAugmentFlag = dollFlag & 0x02;
		int groundAugmentFlag = groundFlag & 0x02;
		// Weapons 0x04
		int dollWeaponFlag = dollFlag & 0x04;
		int groundWeaponFlag = groundFlag & 0x04;
		// Armor 0x08
		int dollArmorFlag = dollFlag & 0x08;
		int groundArmorFlag = groundFlag &= 0x8;
		// Frame 0x10
		int dollFrameFlag = dollFlag & 0x10;


		if (groundArmorFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x7);
		if (groundWeaponFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x8);
		if (groundAugmentFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x9);
		if (dollArmorFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xa);
		if (dollWeaponFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xb);
		if (dollAugmentFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xc);
		if (dollFrameFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xd);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}

void setKnowledgeBit(int id, int bit, int doll){
	char* knowledgePtr = GetKnowledgePtr();
	int dollOffset = 0x4ba4;  // type 0x4d
	int groundOffset = 0x3c04; // type 0x4c
	int offset = dollOffset;
	if (doll == 0)
		offset = groundOffset;
	char* valuePtr = knowledgePtr + offset + id;
	*valuePtr = *valuePtr | bit;
}
void setKnowledgeValue(int id, int value, int doll){
	char* knowledgePtr = GetKnowledgePtr();
	int dollOffset = 0x4ba4;  // type 0x4d
	int groundOffset = 0x3c04; // type 0x4c
	int offset = dollOffset;
	if (doll == 0)
		offset = groundOffset;
	char* valuePtr = knowledgePtr + offset + id;
	*valuePtr = (unsigned char)value;
}
int getKnowledgeBit(int id, int bit, int doll){
	char* knowledgePtr = GetKnowledgePtr();
	int dollOffset = 0x4ba4;  // type 0x4d
	int groundOffset = 0x3c04; // type 0x4c
	int offset = dollOffset;
	if (doll == 0)
		offset = groundOffset;
	char* valuePtr = knowledgePtr + offset + id;
	return *valuePtr & bit;
}

void _initShopCache(char*** shopPtrPtr, int size){
	if(*shopPtrPtr != nullptr) return;
	*shopPtrPtr = (char**)__calloc(size, 4);
}

void _copyShopName(char** shopPtr, int id, char* name, int len){
	if(shopPtr[id] != nullptr) return;
	shopPtr[id] = (char *)__calloc(len + 1, 1);
	__strcpy(shopPtr[id], name);
}

void _cacheShopItemName(int type, int id, char* name){
	int len = __strlen(name);
	if (len == 0) return;
	if(type == 6){
		_initShopCache(&_shopBlueprintNames, 200);
		_copyShopName(_shopBlueprintNames, id, name, len);
	}else if(type == 7){
		_initShopCache(&_shopArmorNames, 1700);
		_copyShopName(_shopArmorNames, id, name, len);
	}else if(type == 8){
		_initShopCache(&_shopWeaponNames, 1900);
		_copyShopName(_shopWeaponNames, id, name, len);
	}else if(type == 9){
		_initShopCache(&_shopAugmentNames, 3700);
		_copyShopName(_shopAugmentNames, id, name, len);
	}else if(type == 0xa){
		_initShopCache(&_shopDollArmorNames, 300);
		_copyShopName(_shopDollArmorNames, id, name, len);
	}else if(type == 0xb){
		_initShopCache(&_shopDollWeaponNames, 900);
		_copyShopName(_shopDollWeaponNames, id, name, len);
	}else if(type == 0xc){
		_initShopCache(&_shopDollAugmentNames, 3200);
		_copyShopName(_shopDollAugmentNames, id, name, len);
	}else if(type == 0xd){
		_initShopCache(&_shopDollFrameNames, 50);
		_copyShopName(_shopDollFrameNames, id, name, len);
	}
}