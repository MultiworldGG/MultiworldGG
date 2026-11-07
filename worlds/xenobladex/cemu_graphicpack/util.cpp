#include <cstddef>

extern int* menuBasePtr;

void writeSystemLog(int* menuBasePtr, const char* str1, const char* str2);
size_t __strlen (const char * str);
int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

namespace import{
	namespace coreinit{
		void OSConsoleWrite(const char* strPtr, int length);
	}
}

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

requestSoundCreate = 0x02418344

menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu
#endif

void getInnerHandle(unsigned int* handle, int partyId);
void requestSoundCreate(int* soundPtr, int id, int flag);


void _writeConsole(const char* output){
	import::coreinit::OSConsoleWrite(output, __strlen(output));
}

void _writeDebug(const char* output){
	writeSystemLog(menuBasePtr, "Debug Message", output);
}

void _playSound(int id){
		int partyId = 0;
		unsigned int innerHandle = 0;
		getInnerHandle(&innerHandle, partyId);
		// from addInnerExpChara
		int*** base = (int***)0x10367664;
		int idx = innerHandle >> 0x13 & 0xfff;
		int*** base_offset = base + idx * 3;
		int* soundPtr = (*base_offset)[0x7a];
		requestSoundCreate(soundPtr, id, 1);
}