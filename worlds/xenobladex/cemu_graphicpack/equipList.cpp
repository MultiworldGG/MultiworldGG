#include <cstddef>

int * GetCharaDataPtr(int charaId);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

getInnerEquipmentData = 0x02cc273c # ::menu::MenuEquipUtil::PCData
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

getInnerEquipmentData = 0x02cc26dc # ::menu::MenuEquipUtil::PCData
#endif

char _formatEquipText[]="EQ CId=%03x Id=%03x Ix=%01x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:";

int * getInnerEquipmentData(char* characterPtr, int equipPosition);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/TWN_FriendRank.html to match the ids
// Ix=0 Ranged Weapon
// Ix=1 Melee Weapon
// Ix=2 Armor Head
// Ix=3 Armor Torso
// Ix=4 Armor Left Arm
// Ix=5 Armor Right Arm
// Ix=6 Armor Legs
char* _postEquipList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    for(int characterId = 0; GetCharaDataPtr(characterId) != 0; characterId++){
		char* characterPtr = (char*)GetCharaDataPtr(characterId);
		 
		for(int equipPosition = 0; equipPosition < 0xc; equipPosition++){
			unsigned int* equipPtr = (unsigned int*)getInnerEquipmentData(characterPtr, equipPosition);
			if(*equipPtr == 0) continue;
			unsigned int itemId =  ((unsigned short*)equipPtr)[0];

			unsigned int skillId1 = ((unsigned short*)equipPtr)[1] >> 4;
			unsigned int skillId2 = ((unsigned short*)equipPtr)[2] >> 4;
			unsigned int skillId3 = ((unsigned short*)equipPtr)[3] >> 4;

			unsigned int upgradeCount1 = ((unsigned short*)equipPtr)[1] << 0x1C >> 0x1C;
			unsigned int upgradeCount2 = ((unsigned short*)equipPtr)[2] << 0x1C >> 0x1C;
			unsigned int upgradeCount3 = ((unsigned short*)equipPtr)[3] << 0x1C >> 0x1C;

			unsigned int augmentId1 = ((unsigned short*)equipPtr)[4];
			unsigned int augmentId2 = ((unsigned short*)equipPtr)[5];
			unsigned int augmentId3 = ((unsigned short*)equipPtr)[6];

			// Be careful you need to rename the after label in the .asm
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatEquipText, characterId, itemId, equipPosition,
				skillId1, upgradeCount1, skillId2, upgradeCount2, skillId3, upgradeCount3, augmentId1, augmentId2, augmentId3);

			if(stringCurrentPtr > stringEndPtr){
				_postCurl(stringStartPtr);
				stringCurrentPtr = stringStartPtr;
			}
		}
    }
	return stringCurrentPtr;
}