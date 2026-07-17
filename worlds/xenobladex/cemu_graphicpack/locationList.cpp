#include <cstddef>

char* getSegmentBdat(int areaId);
int getLocal(int count, int position);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

getFP = 0x0229bd4c # ::GameBdat
#endif

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

getIdTop = 0x029c23b4 # ::Bdat
getIdCount = 0x029c23ac # ::Bdat
getValCheck = 0x029c2630 # ::Bdat
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

getIdTop = 0x029c23a4 # ::Bdat
getIdCount = 0x029c239c # ::Bdat
getValCheck = 0x029c2620 # ::Bdat
#endif

char _formatLocationText[] = "LC Id=%03x Fg=%01x Tp=%01x:";

int* getFP(const char* areaName);
int getIdTop(int* bdatPtr);
int getIdCount(int* bdatPtr);
int getValCheck(int* bdatPtr, const char* columnName, int id, int offset);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/FLD_Location.html to match the ids
// Fg: Flag
// Tp: Type
char* _postLocationList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	int* bdatPtr = getFP("FLD_Location");
	int locationIdStart = getIdTop(bdatPtr);
	int segmentIdCount = getIdCount(bdatPtr);

	for(int locationId = locationIdStart; locationId < locationIdStart + segmentIdCount; locationId++){
		int type = getValCheck(bdatPtr,"Loc_type",locationId,1) >> 0x18;
		int flag = getValCheck(bdatPtr,"flg",locationId,2) >> 0x10;
		flag = getLocal(1, flag);
		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatLocationText, locationId, flag, type);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
	}
	return stringCurrentPtr;
}