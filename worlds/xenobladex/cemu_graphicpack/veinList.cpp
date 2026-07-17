#include <cstddef>

extern int** fnetBasePtr;

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

getBeacon = 0x027d00f8 # ::fnet::FnetData
#endif

char _formatVeinsText[] = "VN Id=%02x Bc=%02x:";

int getBeacon(int* fnetBasePtr, int id);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/FnetVeinList.html to match the ids
char* _postVeinList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	for(int veinId = 1; veinId < 110; veinId++){

		int beaconId = getBeacon(fnetBasePtr[2], veinId); // from setBeacon::fnet::FnetTask in line 20
		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatVeinsText, veinId, beaconId);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
	}

	return stringCurrentPtr;
}