#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

getItemTypeInfo = 0x02361830
itemListBase = 0x10399be8
#endif

extern int itemListBase; // be especially careful here

char _formatAugmentText[] = "IT Id=%03x Tp=%02x:";
char _formatItemText[] = "IT Id=%03x Tp=%02x Cn=%03x:";
char _formatItemGearText[]="IT Id=%03x Tp=%02x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:";
int _itemTypes[] = {1, 6, 7, 0xa, 0xf, 0x14, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f};

unsigned int** getItemTypeInfo(int*, int);


char* _postItemList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    for(int type : _itemTypes){
        int * basePtr = &itemListBase;
        unsigned int* itemListPtr = *getItemTypeInfo(basePtr, type);
        int size = 999;
        if(type == 0x19 || type == 0x1c || type == 0x1f) size = 50;
        else if(type == 0x1a) size = 800;
        else if(type == 0x1b) size = 500;
        else if(type == 0x1d) size = 300;
        else if(type == 0x1e) size = 0xe;
        for(int idx = 0; idx < size; idx++){
            bool isEquip = type < 0x14;
            bool isAugment = type < 0x19;
            if(*itemListPtr != 0){
                unsigned int itemType = itemListPtr[0] << 13 >> 26;
                // Check for GhostItems
                if(itemType > 0x20) itemType -= 0x20;
                if(type > 0x18 && type != itemType) break;
                unsigned int itemId = itemListPtr[0] >> 19;
                unsigned int itemCount = itemListPtr[0] << 19 >> 22;
                if(isEquip){

                    unsigned int skillId1 = ((unsigned short*)itemListPtr)[6] >> 4;
                    unsigned int skillId2 = ((unsigned short*)itemListPtr)[7] >> 4;
                    unsigned int skillId3 = ((unsigned short*)itemListPtr)[8] >> 4;

                    unsigned int upgradeCount1 = ((unsigned short*)itemListPtr)[6] << 0x1C >> 0x1C;
                    unsigned int upgradeCount2 = ((unsigned short*)itemListPtr)[7] << 0x1C >> 0x1C;
                    unsigned int upgradeCount3 = ((unsigned short*)itemListPtr)[8] << 0x1C >> 0x1C;

                    unsigned int augmentId1 = ((unsigned short*)itemListPtr)[9];
                    unsigned int augmentId2 = ((unsigned short*)itemListPtr)[10];
                    unsigned int augmentId3 = ((unsigned short*)itemListPtr)[11];

                    stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatItemGearText, itemId, itemType,
                        skillId1, upgradeCount1, skillId2, upgradeCount2, skillId3, upgradeCount3, augmentId1, augmentId2, augmentId3);
                } else if(isAugment) {
                    stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatAugmentText, itemId, itemType);
                } else {
                    stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatItemText, itemId, itemType, itemCount);
                }
            }

            if(isEquip) itemListPtr += 0x6;
            else itemListPtr += 0x3;
            
            if(stringCurrentPtr > stringEndPtr){
                _postCurl(stringStartPtr);
                stringCurrentPtr = stringStartPtr;
            }
        }

    }
    return stringCurrentPtr;
}