int GetGarageDollData(int idx, char* result);
int SetGarageDollData(int idx, char* result);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E
dollGarageBasePtr = 0x1039c288
0x0234ccd0 = bl _convertSkellToGhost # replace EraceGarageDollData
SetGarageDollData = 0x027f88a0 # ::Util::DollData
reqMenuRemoveItem = 0x0234fba4 # ::CmdReq::ItemInfo
#endif

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

0x02b79884 = bl _convertItemToGhost # replace reqMenuRemoveItem
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

0x02b79874 = bl _convertItemToGhost # replace reqMenuRemoveItem
#endif

extern char* dollGarageBasePtr;

void reqMenuRemoveItem(int* itemPtr, int removeCount);


// Ghost Items are the same item, but they have a different type, but they are part of the same item type list, 
// this hides them from the menus, but makes it possible to check for it in the memory
// the only use for those is to avoid giving duplicate items, because once you received an item 
// you will never lose the ghost item
// when you sell an item, the item should turn into a ghost item instead of vanishing
int _convertSkellToGhost(int idx){
	char* base = dollGarageBasePtr;
	char* dollData = base + 0x6f40 + idx * 0x174;
	// Add arbitrary value
	// game is only checking for 0x6
	// hopefully there are no reprecussions
	dollData[0x16c] += 0x20; 
	return 1;
}

void _convertItemToGhost(int* itemPtr, int removeCount){
	unsigned int itemType = itemPtr[0] << 13 >> 26;
	if(itemType < 0x19){
		itemPtr[0] += 0x20 << 13;
	}
	else reqMenuRemoveItem(itemPtr, removeCount);
}