[Archipelago_friendList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_formatFriendText:
	.string "FD Id=%02x Lv=%02x Ch=%s:"
_postFriendList:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	stw r6,36(r31)
	li r9,1
	stw r9,8(r31)
	b _friendList_L2
_friendList_L4:
	lwz r3,8(r31)
	bl GetCharaDataPtr
	mr r9,r3
	stw r9,12(r31)
	lwz r3,8(r31)
	bl GetFriendRank
	mr r9,r3
	stw r9,16(r31)
	lwz r10,36(r31)
	lwz r8,12(r31)
	lwz r7,16(r31)
	lwz r6,8(r31)
	lis r9,_formatFriendText@ha
	addi r5,r9,_formatFriendText@l
	mr r4,r10
	lwz r3,28(r31)
	crxor 6,6,6
	lis r12,_after_friendList_1__sprintf_s@ha
	addi r12,r12,_after_friendList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_friendList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,28(r31)
	add r9,r9,r10
	stw r9,28(r31)
	lwz r10,28(r31)
	lwz r9,32(r31)
	cmplw cr0,r10,r9
	ble cr0,_friendList_L3
	lwz r3,24(r31)
	bl _postCurl
	lwz r9,24(r31)
	stw r9,28(r31)
_friendList_L3:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_friendList_L2:
	lwz r3,8(r31)
	bl GetCharaDataPtr
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	bne cr0,_friendList_L4
	lwz r9,28(r31)
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_friendList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

GetFriendRank = 0x027fb0a0 # ::Util


