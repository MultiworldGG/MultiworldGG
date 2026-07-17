[Archipelago_dollList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_formatDollText:
	.string "DL GIx=%02x Id=%03x Ix=%01x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x Na=%s:"
_postDollList:
	stwu r1,-496(r1)
	mflr r0
	stw r0,500(r1)
	stw r31,492(r1)
	mr r31,r1
	stw r3,472(r31)
	stw r4,476(r31)
	stw r5,480(r31)
	stw r6,484(r31)
	li r9,0
	stw r9,40(r31)
	b _dollList_L2
_dollList_L8:
	addi r9,r31,92
	mr r4,r9
	lwz r3,40(r31)
	bl GetGarageDollData
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_dollList_L3
	li r9,0
	stw r9,44(r31)
	b _dollList_L4
_dollList_L7:
	lwz r9,44(r31)
	mulli r9,r9,14
	addi r9,r9,36
	addi r10,r31,92
	add r9,r10,r9
	stw r9,48(r31)
	lwz r9,48(r31)
	lhz r9,0(r9)
	cmpwi cr0,r9,0
	beq cr0,_dollList_L10
	lwz r9,48(r31)
	lhz r9,0(r9)
	stw r9,52(r31)
	lwz r9,48(r31)
	addi r9,r9,2
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,56(r31)
	lwz r9,48(r31)
	addi r9,r9,4
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,60(r31)
	lwz r9,48(r31)
	addi r9,r9,6
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,64(r31)
	lwz r9,48(r31)
	addi r9,r9,2
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,68(r31)
	lwz r9,48(r31)
	addi r9,r9,4
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,72(r31)
	lwz r9,48(r31)
	addi r9,r9,6
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,76(r31)
	lwz r9,48(r31)
	addi r9,r9,8
	lhz r9,0(r9)
	stw r9,80(r31)
	lwz r9,48(r31)
	addi r9,r9,10
	lhz r9,0(r9)
	stw r9,84(r31)
	lwz r9,48(r31)
	addi r9,r9,12
	lhz r9,0(r9)
	stw r9,88(r31)
	lwz r4,484(r31)
	addi r9,r31,92
	stw r9,36(r1)
	lwz r9,88(r31)
	stw r9,32(r1)
	lwz r9,84(r31)
	stw r9,28(r1)
	lwz r9,80(r31)
	stw r9,24(r1)
	lwz r9,76(r31)
	stw r9,20(r1)
	lwz r9,64(r31)
	stw r9,16(r1)
	lwz r9,72(r31)
	stw r9,12(r1)
	lwz r9,60(r31)
	stw r9,8(r1)
	lwz r10,68(r31)
	lwz r9,56(r31)
	lwz r8,44(r31)
	lwz r7,52(r31)
	lwz r6,40(r31)
	lis r5,_formatDollText@ha
	addi r5,r5,_formatDollText@l
	lwz r3,476(r31)
	crxor 6,6,6
	lis r12,_after_dollList_1__sprintf_s@ha
	addi r12,r12,_after_dollList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_dollList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,476(r31)
	add r9,r9,r10
	stw r9,476(r31)
	lwz r10,476(r31)
	lwz r9,480(r31)
	cmplw cr0,r10,r9
	ble cr0,_dollList_L6
	lwz r3,472(r31)
	bl _postCurl
	lwz r9,472(r31)
	stw r9,476(r31)
	b _dollList_L6
_dollList_L10:
	nop
_dollList_L6:
	lwz r9,44(r31)
	addi r9,r9,1
	stw r9,44(r31)
_dollList_L4:
	lwz r9,44(r31)
	cmpwi cr0,r9,15
	ble cr0,_dollList_L7
_dollList_L3:
	lwz r9,40(r31)
	addi r9,r9,1
	stw r9,40(r31)
_dollList_L2:
	lwz r9,40(r31)
	cmpwi cr0,r9,59
	ble cr0,_dollList_L8
	lwz r9,476(r31)
	mr r3,r9
	addi r11,r31,496
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_dollList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

GetGarageDollData = 0x027f7104 # ::Util::DollData


