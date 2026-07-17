#include <cstddef>

int getLocal(int count, int position);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int _hasPreciousItem(int id);
void _postCurl(char[]);
void _writeDebug(const char* output);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

fnetBasePtr = 0x1039c258 # from getFnetData::fnet::FnetDataAccessor

request = 0x023e0458 # CompoControl::CtrlRequesti
0x023ef190 = bl _notifyDead
#endif

extern int** fnetBasePtr;

int _charaHasDied;

int request(int* requestCtrlPtr, int code, int placeholder);


// Use https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PreciousList.html from [24:31] and [36:38]
char* _postKeyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    for(int keyId = 0; keyId < 16; keyId++){
		if(keyId == 0x9) keyId += 4;
		int flag = 0;

		// just for debugging purposes
		if(keyId == 0) flag = getLocal(0x10, 1);
		else if(keyId == 6){
			if (_charaHasDied) _charaHasDied = 0;
			else continue;
		}
		else 
			flag = _hasPreciousItem(24 + keyId - 1);

		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, "KY Id=%01x Fg=%01x:", keyId, flag);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}

int _notifyDead(int* requestCtrlPtr, int code, int placeholder){
	int* backupRequestCtrlPtr = requestCtrlPtr;
	asm("stw 29,24(31)");
	if(code == 0x2e && *requestCtrlPtr == 0x100){ 
		_charaHasDied = 1;
		_writeDebug("Sending Death");
	}
	return request(backupRequestCtrlPtr, code, placeholder);
}