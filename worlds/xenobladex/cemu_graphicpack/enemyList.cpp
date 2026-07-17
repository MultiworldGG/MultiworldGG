#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

GetEnBookDefeat = 0x027fcb70 # ::Util
GetEnBookDiscovery = 0x027fcab4 # ::Util
#endif

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

getVal = 0x029c2120 # ::bdat
getFlagVal = 0x029c254c # ::bdat
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

getVal = 0x029c2110 # ::bdat
getFlagVal = 0x029c253c # ::bdat
#endif

// Parameter from rules.txt
int enemyBookThreshold;

char _formatEnemyText[] = "EN Id=%03x Fg=%01x:";

int GetEnBookDefeat(int id);
int GetEnBookDiscovery(int id);

int* getFP(const char* bdat);
int getVal(int* bdatPtr, const char* columnName, int id);
int getValCheck(int* bdatPtr, const char* columnName, int id, int offset);
int getFlagVal(int* bdatPtr, const char* flagName, int id, const char* columnName);

// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_EnBook.html to match the ids
// Defeat: Number of enemies you defeated
char* _postEnemyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	int enemyThreshold = enemyBookThreshold;
	int enemyCount = 1404;
	int* chrBdatPtr = getFP("CHR_EnList");
	int* btlBdatPtr = getFP("BTL_EnBook");
    for(int enemyId = 1; enemyId < enemyCount; enemyId++){
		int flag = 0;
		if(enemyThreshold > 0){
			int defeat = GetEnBookDefeat(enemyId);
			if (defeat >= 1){
				int enemyBaseId = getVal(btlBdatPtr, "BaseEnemyID", enemyId) >> 0x10;
				int isBoss = getFlagVal(chrBdatPtr, "Flag", enemyBaseId, "mBoss");
				int isNamed = getFlagVal(chrBdatPtr, "Flag", enemyBaseId, "Named");
				int enBook = getFlagVal(chrBdatPtr, "Flag", enemyBaseId, "enBook");
				if(defeat >= enemyThreshold || isBoss || isNamed || enBook) flag = 1;  // exactly what game does in getOpenType
			} 
		}
		else {
			int discovery = GetEnBookDiscovery(enemyId);
			if(discovery >= 1) flag = 1;
		}

		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatEnemyText, enemyId, flag);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}