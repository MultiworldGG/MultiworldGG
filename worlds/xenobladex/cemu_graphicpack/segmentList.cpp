#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

segmentBasePtr = 0x104524bc # From line 10 in completeSegment::UIManager
getLocal = 0x0228ed34 # ::GameFlag
#endif

extern int* segmentBasePtr;

char _formatSegmentText[] = "SG Id=%03x Fg=%01x AId=%02x:";

int getLocal(int count, int position);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/SEG_NormalList.html to match the ids
char* _postSegmentList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    int* areaOffset = segmentBasePtr;
    for(int areaId = 0; areaId < 0x15; areaId++){
        // from existNewSegmentInfo: 0x1f18
        int nodeCount = *(areaOffset + 0x7c6);
        // from existNewSegmentInfo: 0x1428
        int* segmentOffset = areaOffset + 0x50a;
        for(int nodeIdx = 0; nodeIdx < nodeCount; nodeIdx++){
            int flag = getLocal(2 /* maybe 1*/, segmentOffset[2] >> 0x10);
            int segmentId = segmentOffset[3];
            stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatSegmentText, segmentId, flag, areaId);

            // Reset buffer
            if(stringCurrentPtr > stringEndPtr){
                _postCurl(stringStartPtr);
                stringCurrentPtr = stringStartPtr;
            }

            // from existNewSegmentInfo: 0x1c
            segmentOffset += 0x7;
        }
        areaOffset += 0x7f7; // from existNewSegmentInfo: 0x1fdc
    }
    return stringCurrentPtr;
}