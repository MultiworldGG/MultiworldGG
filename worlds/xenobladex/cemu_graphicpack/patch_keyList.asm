[Archipelago_keyList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_charaHasDied:
	.int    0
_keyList_LC0:
	.string "KY Id=%01x Fg=%01x:"
_postKeyList:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	stw r6,36(r31)
	li r9,0
	stw r9,8(r31)
	b _keyList_L2
_keyList_L9:
	lwz r9,8(r31)
	cmpwi cr0,r9,9
	bne cr0,_keyList_L3
	lwz r9,8(r31)
	addi r9,r9,4
	stw r9,8(r31)
_keyList_L3:
	li r9,0
	stw r9,12(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_keyList_L4
	li r4,1
	li r3,16
	bl getLocal
	mr r9,r3
	stw r9,12(r31)
	b _keyList_L5
_keyList_L4:
	lwz r9,8(r31)
	cmpwi cr0,r9,6
	bne cr0,_keyList_L6
	lis r9,_charaHasDied@ha
	lwz r9,_charaHasDied@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyList_L11
	lis r9,_charaHasDied@ha
	li r10,0
	stw r10,_charaHasDied@l(r9)
	b _keyList_L5
_keyList_L6:
	lwz r9,8(r31)
	addi r9,r9,23
	mr r3,r9
	bl _hasPreciousItem
	mr r9,r3
	stw r9,12(r31)
_keyList_L5:
	lwz r10,36(r31)
	lwz r7,12(r31)
	lwz r6,8(r31)
	lis r9,_keyList_LC0@ha
	addi r5,r9,_keyList_LC0@l
	mr r4,r10
	lwz r3,28(r31)
	crxor 6,6,6
	lis r12,_after_keyList_1__sprintf_s@ha
	addi r12,r12,_after_keyList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_keyList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,28(r31)
	add r9,r9,r10
	stw r9,28(r31)
	lwz r10,28(r31)
	lwz r9,32(r31)
	cmplw cr0,r10,r9
	ble cr0,_keyList_L8
	lwz r3,24(r31)
	bl _postCurl
	lwz r9,24(r31)
	stw r9,28(r31)
	b _keyList_L8
_keyList_L11:
	nop
_keyList_L8:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_keyList_L2:
	lwz r9,8(r31)
	cmpwi cr0,r9,15
	ble cr0,_keyList_L9
	lwz r9,28(r31)
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyList_LC1:
	.string "Sending Death"
_notifyDead:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lwz r9,24(r31)
	stw r9,8(r31)
	stw r29,24(r31)
	lwz r9,28(r31)
	cmpwi cr0,r9,46
	bne cr0,_keyList_L13
	lwz r9,24(r31)
	lwz r9,0(r9)
	cmpwi cr0,r9,256
	bne cr0,_keyList_L13
	lis r9,_charaHasDied@ha
	li r10,1
	stw r10,_charaHasDied@l(r9)
	lis r9,_keyList_LC1@ha
	addi r3,r9,_keyList_LC1@l
	bl _writeDebug
_keyList_L13:
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,8(r31)
	bl request
	mr r9,r3
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_keyList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

fnetBasePtr = 0x1039c258 # from getFnetData::fnet::FnetDataAccessor

request = 0x023e0458 # CompoControl::CtrlRequesti
0x023ef190 = bl _notifyDead


