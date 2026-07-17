[Archipelago_equipList]
moduleMatches = 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.0E, 1.0.2U
.origin = codecave

_formatEquipText:
	.string "EQ CId=%03x Id=%03x Ix=%01x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:"
_postEquipList:
	stwu r1,-128(r1)
	mflr r0
	stw r0,132(r1)
	stw r31,124(r1)
	mr r31,r1
	stw r3,104(r31)
	stw r4,108(r31)
	stw r5,112(r31)
	stw r6,116(r31)
	li r9,0
	stw r9,40(r31)
	b _equipList_L2
_equipList_L7:
	lwz r3,40(r31)
	bl GetCharaDataPtr
	mr r9,r3
	stw r9,48(r31)
	li r9,0
	stw r9,44(r31)
	b _equipList_L3
_equipList_L6:
	lwz r4,44(r31)
	lwz r3,48(r31)
	bl getInnerEquipmentData
	mr r9,r3
	stw r9,52(r31)
	lwz r9,52(r31)
	lwz r9,0(r9)
	cmpwi cr0,r9,0
	beq cr0,_equipList_L9
	lwz r9,52(r31)
	lhz r9,0(r9)
	stw r9,56(r31)
	lwz r9,52(r31)
	addi r9,r9,2
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,60(r31)
	lwz r9,52(r31)
	addi r9,r9,4
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,64(r31)
	lwz r9,52(r31)
	addi r9,r9,6
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,68(r31)
	lwz r9,52(r31)
	addi r9,r9,2
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,72(r31)
	lwz r9,52(r31)
	addi r9,r9,4
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,76(r31)
	lwz r9,52(r31)
	addi r9,r9,6
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,80(r31)
	lwz r9,52(r31)
	addi r9,r9,8
	lhz r9,0(r9)
	stw r9,84(r31)
	lwz r9,52(r31)
	addi r9,r9,10
	lhz r9,0(r9)
	stw r9,88(r31)
	lwz r9,52(r31)
	addi r9,r9,12
	lhz r9,0(r9)
	stw r9,92(r31)
	lwz r4,116(r31)
	lwz r9,92(r31)
	stw r9,32(r1)
	lwz r9,88(r31)
	stw r9,28(r1)
	lwz r9,84(r31)
	stw r9,24(r1)
	lwz r9,80(r31)
	stw r9,20(r1)
	lwz r9,68(r31)
	stw r9,16(r1)
	lwz r9,76(r31)
	stw r9,12(r1)
	lwz r9,64(r31)
	stw r9,8(r1)
	lwz r10,72(r31)
	lwz r9,60(r31)
	lwz r8,44(r31)
	lwz r7,56(r31)
	lwz r6,40(r31)
	lis r5,_formatEquipText@ha
	addi r5,r5,_formatEquipText@l
	lwz r3,108(r31)
	crxor 6,6,6
	lis r12,_after_equipList_1__sprintf_s@ha
	addi r12,r12,_after_equipList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_equipList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,108(r31)
	add r9,r9,r10
	stw r9,108(r31)
	lwz r10,108(r31)
	lwz r9,112(r31)
	cmplw cr0,r10,r9
	ble cr0,_equipList_L5
	lwz r3,104(r31)
	bl _postCurl
	lwz r9,104(r31)
	stw r9,108(r31)
	b _equipList_L5
_equipList_L9:
	nop
_equipList_L5:
	lwz r9,44(r31)
	addi r9,r9,1
	stw r9,44(r31)
_equipList_L3:
	lwz r9,44(r31)
	cmpwi cr0,r9,11
	ble cr0,_equipList_L6
	lwz r9,40(r31)
	addi r9,r9,1
	stw r9,40(r31)
_equipList_L2:
	lwz r3,40(r31)
	bl GetCharaDataPtr
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	bne cr0,_equipList_L7
	lwz r9,108(r31)
	mr r3,r9
	addi r11,r31,128
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_equipList_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

getInnerEquipmentData = 0x02cc273c # ::menu::MenuEquipUtil::PCData


[Archipelago_equipList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

getInnerEquipmentData = 0x02cc26dc # ::menu::MenuEquipUtil::PCData


