[Archipelago_sell]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07, 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.2U, 1.0.0E, 1.0.1E, 1.0.0E, 1.0.2U
.origin = codecave

_convertSkellToGhost:
	stwu r1,-48(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	lis r9,dollGarageBasePtr@ha
	lwz r9,dollGarageBasePtr@l(r9)
	stw r9,8(r31)
	lwz r9,24(r31)
	mulli r9,r9,372
	addi r9,r9,28480
	lwz r10,8(r31)
	add r9,r10,r9
	stw r9,12(r31)
	lwz r9,12(r31)
	addi r9,r9,364
	lbz r10,0(r9)
	lwz r9,12(r31)
	addi r9,r9,364
	addi r10,r10,32
	stb r10,0(r9)
	li r9,1
	mr r3,r9
	addi r11,r31,48
	lwz r31,-4(r11)
	mr r1,r11
	blr
_convertItemToGhost:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	lwz r9,24(r31)
	lwz r9,0(r9)
	slwi r9,r9,13
	srawi r9,r9,26
	stw r9,8(r31)
	lwz r9,8(r31)
	cmplwi cr0,r9,24
	bgt cr0,_sell_L4
	lwz r9,24(r31)
	lwz r9,0(r9)
	addis r10,r9,0x4
	lwz r9,24(r31)
	stw r10,0(r9)
	b _sell_L6
_sell_L4:
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl reqMenuRemoveItem
_sell_L6:
	nop
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_sell_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
dollGarageBasePtr = 0x1039c288
0x0234ccd0 = bl _convertSkellToGhost # replace EraceGarageDollData
SetGarageDollData = 0x027f88a0 # ::Util::DollData
reqMenuRemoveItem = 0x0234fba4 # ::CmdReq::ItemInfo


[Archipelago_sell_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

0x02b79884 = bl _convertItemToGhost # replace reqMenuRemoveItem


[Archipelago_sell_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

0x02b79874 = bl _convertItemToGhost # replace reqMenuRemoveItem


