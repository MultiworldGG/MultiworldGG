[Archipelago_artsList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_formatArtsText:
	.string "AT Id=%02x Lv=%01x:"
_postArtsList:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	stw r6,52(r31)
	li r9,888
	stw r9,16(r31)
	li r9,0
	stw r9,8(r31)
	b _artsList_L2
_artsList_L6:
	lwz r3,8(r31)
	bl GetCharaDataPtr
	mr r9,r3
	stw r9,20(r31)
	li r9,1
	stw r9,12(r31)
	b _artsList_L3
_artsList_L5:
	lwz r10,12(r31)
	lwz r9,16(r31)
	add r9,r10,r9
	lwz r10,20(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	stw r9,24(r31)
	lwz r10,52(r31)
	lwz r7,24(r31)
	lwz r6,12(r31)
	lis r9,_formatArtsText@ha
	addi r5,r9,_formatArtsText@l
	mr r4,r10
	lwz r3,44(r31)
	crxor 6,6,6
	lis r12,_after_artsList_1__sprintf_s@ha
	addi r12,r12,_after_artsList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_artsList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,44(r31)
	add r9,r9,r10
	stw r9,44(r31)
	lwz r10,44(r31)
	lwz r9,48(r31)
	cmplw cr0,r10,r9
	ble cr0,_artsList_L4
	lwz r3,40(r31)
	bl _postCurl
	lwz r9,40(r31)
	stw r9,44(r31)
_artsList_L4:
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
_artsList_L3:
	lwz r9,12(r31)
	cmpwi cr0,r9,157
	ble cr0,_artsList_L5
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_artsList_L2:
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	ble cr0,_artsList_L6
	lwz r9,44(r31)
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_artsList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E


