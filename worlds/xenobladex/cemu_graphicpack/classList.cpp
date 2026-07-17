#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

getClassLv = 0x02c9560c # ::Menu::MenuDataUtil
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

getClassLv = 0x02c955ac # ::Menu::MenuDataUtil
#endif

char _formatClassText[] = "CL Id=%02x Lv=%01x:";

int getClassLv(int classId);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_ClassInfo.html to match the ids
char* _postClassList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	// Do this only for main character for now
    for(int classId = 1; classId < 0x11; classId++){
		int flag = getClassLv(classId);
		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatClassText, classId, flag);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}