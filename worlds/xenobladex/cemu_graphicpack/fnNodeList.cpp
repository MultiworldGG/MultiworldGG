#include <cstddef>

extern int* segmentBasePtr;

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

checkDP = 0x027d346c # ::fnet::FnetDataAccesor
#endif

char _formatFnNodeText[] = "FN Id=%03x Fg=%01x:";

int checkDP(short id);


// Use https://xenoblade.github.io/xbx/bdat/common_local_us/FnetVeinList.html
char* _postFnNodeList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    for(int nodeId = 1; nodeId < 110; nodeId++){
        int flag = checkDP(nodeId);

        stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatFnNodeText, nodeId, flag);

        // Reset buffer
        if(stringCurrentPtr > stringEndPtr){
            _postCurl(stringStartPtr);
            stringCurrentPtr = stringStartPtr;
        }
    }

    return stringCurrentPtr;
}