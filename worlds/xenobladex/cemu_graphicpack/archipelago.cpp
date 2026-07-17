#include <cstddef>

extern int* menuBasePtr;

void _initCurl();
void _postCurl(char[]);
char* _getCurl();
void _cleanupCurl();

void _addItem(int type, int id);
void _addGear(int type, int id, int affixId1, int affixId2, int affixId3, int slotCount);
void _addArt(int id, int lv);
void _addSkill(int id, int lv);
void _addFriend(int id, int lv);
void _addFieldSkill(int id, int lv);
void _addKey(int id, int flag);
void _addClass(int id, int lv);

char* _postArtsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postClassList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postCollepediaList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postEnemyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postFieldSkillsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postFnNodeList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postFriendList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postItemList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postLocationList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postSegmentList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postSkillsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postKeyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postEquipList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postDollList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postVeinList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

changeTime = 0x022b36f4 #::GameManager

0x022b3bbc = bl _mainArchipelago # replace bl changeTime
#endif

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

writeSystemLog = 0x02c74290 #::MenuTask

__sprintf_s = 0x03133354
__malloc = 0x03b1aeb0
__free = 0x03b1afe8
__strtol = 0x03b1b27c
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

writeSystemLog = 0x02c74230 #::MenuTask

__sprintf_s = 0x031332d4
__malloc = 0x03b1ae30
__free = 0x03b1af68
__strtol = 0x03b1b1fc
#endif

#ifdef Unsupported
moduleMatches = 0x7672271D, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.2J, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

# Error Box for bad game versions
Unsupported_Game_Version:
	.int	$Unsupported_Game_Version
#endif

int Unsupported_Game_Version;

int changeTime(int hour, int minute);
void writeSystemLog(int* menuBasePtr, char* str1, char* str2);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);
void* __malloc (size_t size);
void __free (void* ptr);
long int __strtol (const char* str, char** endptr, int base);


void _postArchipelago(){
	int allocBufferSize = 0xFFFF;
	int maxEntrySize = 0x100;

    char* stringStartPtr = (char*)__malloc(allocBufferSize);
    char* stringCurrentPtr = stringStartPtr;
	char* stringEndPtr = stringStartPtr + allocBufferSize - maxEntrySize;

	stringCurrentPtr[0] = '^';
	stringCurrentPtr++;

	stringCurrentPtr = _postArtsList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postClassList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postCollepediaList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postEnemyList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postFieldSkillsList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postFnNodeList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postFriendList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postItemList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postLocationList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postSegmentList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postSkillsList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postKeyList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postEquipList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postDollList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postVeinList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);

	stringCurrentPtr[0] = '$';
	stringCurrentPtr[1] = 0;

	_postCurl(stringStartPtr);

    __free(stringStartPtr);
}

void _getArchipelago(){
	char* outputPtr = _getCurl();
	if (outputPtr == nullptr) return;

	char* outputCurrentPtr = outputPtr;
	while(*outputCurrentPtr != 0){
		switch(*outputCurrentPtr){
			case 'I': // Item
			// Identification Character + Prefix + Type + Prefix + Id
			{
				outputCurrentPtr += 1 + 4;
				int itemType = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int itemId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addItem(itemType, itemId);
			}
			break;

			case 'G': // Gear with Affixes
			// Identification Character + Prefix + Type + Prefix + Id + 3*(prefix + affixId) + prefix + slotCount
			{
				outputCurrentPtr += 1 + 4;
				int itemType = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int itemId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int affixId1 = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int affixId2 = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int affixId3 = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int slotCount = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addGear(itemType, itemId, affixId1, affixId2, affixId3, slotCount);
			}
			break;

			case 'A': // Art
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int artId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int artLv = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addArt(artId, artLv);
			}
			break;

			case 'S': // Skill
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int skillId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int skillLv = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addSkill(skillId, skillLv);
			}
			break;

			case 'F': // Friend
			// Identification Character + Prefix + Id + Prefix + Rank
			{
				outputCurrentPtr += 1 + 4; 
				int friendId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int friendRk = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addFriend(friendId, friendRk);
			}
			break;

			case 'D': // Debris Skill (Field Skill)
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int fieldSkillId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int fieldSkillLv = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addFieldSkill(fieldSkillId, fieldSkillLv);
			}
			break;

			case 'K': // Key Items
			// Identification Character + Prefix + Id + Prefix + Flag
			{
				outputCurrentPtr += 1 + 4; 
				int keyId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int keyFlag = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addKey(keyId, keyFlag);
			}
			break;

			case 'C': // Class
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int classId = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8 + 4;
				int classLv = (int)__strtol(outputCurrentPtr, nullptr, 16);
				outputCurrentPtr += 8;
				_addClass(classId, classLv);
			}
			break;

			case 'M': // Message
			// Identification Character + Message Heading + \r + Message Body 
			{
				outputCurrentPtr += 1 + 1;
				char* messageHead = outputCurrentPtr;
				while(*outputCurrentPtr != '\r') outputCurrentPtr++;
				*outputCurrentPtr = 0;
				outputCurrentPtr++;
				char* messageBody = outputCurrentPtr;
				while(*outputCurrentPtr != '\n') outputCurrentPtr++;
				*outputCurrentPtr = 0;
				outputCurrentPtr++;
				writeSystemLog(menuBasePtr, messageHead, messageBody);
			}
			break;

			case '\n':
			outputCurrentPtr++;
			break;

			default:
			__free(outputPtr);
			return;
		}
	}
	__free(outputPtr);
}

unsigned int _networkCounter = 0;
int _mainArchipelago(int hour, int minute) {
	// if(minute % 3 != 0) return changeTime(hour, minute);
	
	_initCurl();

	_networkCounter = _networkCounter << 31;
	_networkCounter = _networkCounter >> 31;
	if(_networkCounter == 0) _getArchipelago();
	else _postArchipelago();
	_networkCounter = _networkCounter + 1;

    _cleanupCurl();

	return changeTime(hour, minute);
}