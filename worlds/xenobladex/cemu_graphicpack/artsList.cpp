#include <cstddef>

int * GetCharaDataPtr(int charaId);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E
#endif

char _formatArtsText[] = "AT Id=%02x Lv=%01x:";


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ArtsList.html to match the ids
char* _postArtsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	int artsOffset = 0x378; // from GetArtsLevel::Menu::MenuArtsSet
	// Do this only for main character for now
    for(int characterId = 0; characterId < 0x1; characterId++){
		char* characterBasePtr = (char*)GetCharaDataPtr(characterId);

		for(int artId = 1; artId < 158; artId++){

			int level = *(characterBasePtr + artId + artsOffset); 
			// option to log character name with characterBasePtr and %s in format string
			// option to log character id with characterId and %02x in format string
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatArtsText, artId, level);

			// Reset buffer
			if(stringCurrentPtr > stringEndPtr){
				_postCurl(stringStartPtr);
				stringCurrentPtr = stringStartPtr;
			}
		}
    }
	return stringCurrentPtr;
}