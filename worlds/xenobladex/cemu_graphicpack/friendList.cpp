#include <cstddef>

int * GetCharaDataPtr(int charaId);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

GetFriendRank = 0x027fb0a0 # ::Util
#endif

char _formatFriendText[] = "FD Id=%02x Lv=%02x Ch=%s:";

int GetFriendRank(int friendId);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/TWN_FriendRank.html to match the ids
// Ranges from 0 to 50, but 32 is already 5 hearts???
char* _postFriendList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	// Do this only for main character for now
    for(int friendId = 1; GetCharaDataPtr(friendId) != 0; friendId++){
		char* name = (char*)GetCharaDataPtr(friendId);
		int rank = GetFriendRank(friendId);
		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatFriendText, friendId, rank, name);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}