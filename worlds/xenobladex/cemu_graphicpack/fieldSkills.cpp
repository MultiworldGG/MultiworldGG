#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

fieldSkillBasePtr = 0x1039c288 # from updateStatus::menu::MenuTotalSimpleStatus line 398
#endif

extern char* fieldSkillBasePtr;

char _formatFieldSkillText[] = "FS Id=%01x Lv=%01x:";
int _fieldSkillOffset = 0x48b19; // from updateStatus::menu::MenuTotalSimpleStatus line 413


// The ids follow the menu order
// 1 = Mechanical
// 2 = Biological
// 3 = Archeological
char* _postFieldSkillsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	char* fieldSkillOffset = fieldSkillBasePtr;
	fieldSkillOffset += _fieldSkillOffset - 1;
    for(int fieldSkill = 1; fieldSkill < 4; fieldSkill++){
		int rank = *fieldSkillOffset;
		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatFieldSkillText, fieldSkill, rank);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
		fieldSkillOffset += 0x1;
    }
	return stringCurrentPtr;
}