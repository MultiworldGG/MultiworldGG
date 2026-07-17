#include <cstddef>

int getLocal(int count, int position);

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E
#endif

char _formatCollecText[] = "CP Id=%03x Fg=%01x:";


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_CollectList.html to match the ids
char* _postCollepediaList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
  int collepediaOffset = 0x156b; // from getRatioCollepedia::collepedia
  for(int collecId = 1; collecId < 301; collecId++){
    int flag = getLocal(1, collecId + collepediaOffset);
    stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatCollecText, collecId, flag);

    // Reset buffer
    if(stringCurrentPtr > stringEndPtr){
      _postCurl(stringStartPtr);
      stringCurrentPtr = stringStartPtr;
    }
  }
  return stringCurrentPtr;
}