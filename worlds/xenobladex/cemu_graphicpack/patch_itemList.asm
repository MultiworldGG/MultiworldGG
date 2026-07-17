[Archipelago_itemList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_formatAugmentText:
	.string "IT Id=%03x Tp=%02x:"
_formatItemText:
	.string "IT Id=%03x Tp=%02x Cn=%03x:"
_formatItemGearText:
	.string "IT Id=%03x Tp=%02x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:"
_itemTypes:
	.long   1
	.long   6
	.long   7
	.long   10
	.long   15
	.long   20
	.long   25
	.long   26
	.long   27
	.long   28
	.long   29
	.long   30
	.long   31
_postItemList:
	stwu r1,-160(r1)
	mflr r0
	stw r0,164(r1)
	stw r31,156(r1)
	mr r31,r1
	stw r3,128(r31)
	stw r4,132(r31)
	stw r5,136(r31)
	stw r6,140(r31)
	lis r9,_itemTypes@ha
	addi r9,r9,_itemTypes@l
	stw r9,52(r31)
	lis r9,_itemTypes@ha
	addi r9,r9,_itemTypes@l
	stw r9,32(r31)
	lis r9,_itemTypes@ha
	addi r9,r9,52
	addi r9,r9,_itemTypes@l
	stw r9,56(r31)
	b _itemList_L2
_itemList_L20:
	lwz r9,32(r31)
	lwz r9,0(r9)
	stw r9,60(r31)
	lis r9,itemListBase@ha
	addi r9,r9,itemListBase@l
	stw r9,64(r31)
	lwz r4,60(r31)
	lwz r3,64(r31)
	bl getItemTypeInfo
	mr r9,r3
	lwz r9,0(r9)
	stw r9,36(r31)
	li r9,999
	stw r9,40(r31)
	lwz r9,60(r31)
	cmpwi cr0,r9,25
	beq cr0,_itemList_L3
	lwz r9,60(r31)
	cmpwi cr0,r9,28
	beq cr0,_itemList_L3
	lwz r9,60(r31)
	cmpwi cr0,r9,31
	bne cr0,_itemList_L4
_itemList_L3:
	li r9,50
	stw r9,40(r31)
	b _itemList_L5
_itemList_L4:
	lwz r9,60(r31)
	cmpwi cr0,r9,26
	bne cr0,_itemList_L6
	li r9,800
	stw r9,40(r31)
	b _itemList_L5
_itemList_L6:
	lwz r9,60(r31)
	cmpwi cr0,r9,27
	bne cr0,_itemList_L7
	li r9,500
	stw r9,40(r31)
	b _itemList_L5
_itemList_L7:
	lwz r9,60(r31)
	cmpwi cr0,r9,29
	bne cr0,_itemList_L8
	li r9,300
	stw r9,40(r31)
	b _itemList_L5
_itemList_L8:
	lwz r9,60(r31)
	cmpwi cr0,r9,30
	bne cr0,_itemList_L5
	li r9,14
	stw r9,40(r31)
_itemList_L5:
	li r9,0
	stw r9,44(r31)
	b _itemList_L9
_itemList_L19:
	lwz r9,60(r31)
	addi r10,r9,-20
	or r9,r9,r10
	srwi r9,r9,31
	stb r9,68(r31)
	lwz r9,60(r31)
	addi r10,r9,-25
	or r9,r9,r10
	srwi r9,r9,31
	stb r9,69(r31)
	lwz r9,36(r31)
	lwz r9,0(r9)
	cmpwi cr0,r9,0
	beq cr0,_itemList_L10
	lwz r9,36(r31)
	lwz r9,0(r9)
	slwi r9,r9,13
	srwi r9,r9,26
	stw r9,48(r31)
	lwz r9,48(r31)
	cmplwi cr0,r9,32
	ble cr0,_itemList_L11
	lwz r9,48(r31)
	addi r9,r9,-32
	stw r9,48(r31)
_itemList_L11:
	lwz r9,60(r31)
	cmpwi cr0,r9,24
	ble cr0,_itemList_L12
	lwz r9,60(r31)
	lwz r10,48(r31)
	cmpw cr0,r10,r9
	bne cr0,_itemList_L22
_itemList_L12:
	lwz r9,36(r31)
	lwz r9,0(r9)
	srwi r9,r9,19
	stw r9,72(r31)
	lwz r9,36(r31)
	lwz r9,0(r9)
	slwi r9,r9,19
	srwi r9,r9,22
	stw r9,76(r31)
	lbz r9,68(r31)
	cmpwi cr0,r9,0
	beq cr0,_itemList_L14
	lwz r9,36(r31)
	addi r9,r9,12
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,80(r31)
	lwz r9,36(r31)
	addi r9,r9,14
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,84(r31)
	lwz r9,36(r31)
	addi r9,r9,16
	lhz r9,0(r9)
	srwi r9,r9,4
	stw r9,88(r31)
	lwz r9,36(r31)
	addi r9,r9,12
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,92(r31)
	lwz r9,36(r31)
	addi r9,r9,14
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,96(r31)
	lwz r9,36(r31)
	addi r9,r9,16
	lhz r9,0(r9)
	slwi r9,r9,28
	srawi r9,r9,28
	stw r9,100(r31)
	lwz r9,36(r31)
	addi r9,r9,18
	lhz r9,0(r9)
	stw r9,104(r31)
	lwz r9,36(r31)
	addi r9,r9,20
	lhz r9,0(r9)
	stw r9,108(r31)
	lwz r9,36(r31)
	addi r9,r9,22
	lhz r9,0(r9)
	stw r9,112(r31)
	lwz r4,140(r31)
	lwz r9,112(r31)
	stw r9,28(r1)
	lwz r9,108(r31)
	stw r9,24(r1)
	lwz r9,104(r31)
	stw r9,20(r1)
	lwz r9,100(r31)
	stw r9,16(r1)
	lwz r9,88(r31)
	stw r9,12(r1)
	lwz r9,96(r31)
	stw r9,8(r1)
	lwz r10,84(r31)
	lwz r9,92(r31)
	lwz r8,80(r31)
	lwz r7,48(r31)
	lwz r6,72(r31)
	lis r5,_formatItemGearText@ha
	addi r5,r5,_formatItemGearText@l
	lwz r3,132(r31)
	crxor 6,6,6
	lis r12,_after_itemList_1__sprintf_s@ha
	addi r12,r12,_after_itemList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_itemList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,132(r31)
	add r9,r9,r10
	stw r9,132(r31)
	b _itemList_L10
_itemList_L14:
	lbz r9,69(r31)
	cmpwi cr0,r9,0
	beq cr0,_itemList_L15
	lwz r10,140(r31)
	lwz r7,48(r31)
	lwz r6,72(r31)
	lis r9,_formatAugmentText@ha
	addi r5,r9,_formatAugmentText@l
	mr r4,r10
	lwz r3,132(r31)
	crxor 6,6,6
	lis r12,_after_itemList_2__sprintf_s@ha
	addi r12,r12,_after_itemList_2__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_itemList_2__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,132(r31)
	add r9,r9,r10
	stw r9,132(r31)
	b _itemList_L10
_itemList_L15:
	lwz r10,140(r31)
	lwz r8,76(r31)
	lwz r7,48(r31)
	lwz r6,72(r31)
	lis r9,_formatItemText@ha
	addi r5,r9,_formatItemText@l
	mr r4,r10
	lwz r3,132(r31)
	crxor 6,6,6
	lis r12,_after_itemList_3__sprintf_s@ha
	addi r12,r12,_after_itemList_3__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_itemList_3__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,132(r31)
	add r9,r9,r10
	stw r9,132(r31)
_itemList_L10:
	lbz r9,68(r31)
	cmpwi cr0,r9,0
	beq cr0,_itemList_L16
	lwz r9,36(r31)
	addi r9,r9,24
	stw r9,36(r31)
	b _itemList_L17
_itemList_L16:
	lwz r9,36(r31)
	addi r9,r9,12
	stw r9,36(r31)
_itemList_L17:
	lwz r10,132(r31)
	lwz r9,136(r31)
	cmplw cr0,r10,r9
	ble cr0,_itemList_L18
	lwz r3,128(r31)
	bl _postCurl
	lwz r9,128(r31)
	stw r9,132(r31)
_itemList_L18:
	lwz r9,44(r31)
	addi r9,r9,1
	stw r9,44(r31)
_itemList_L9:
	lwz r10,44(r31)
	lwz r9,40(r31)
	cmpw cr0,r10,r9
	blt cr0,_itemList_L19
	b _itemList_L13
_itemList_L22:
	nop
_itemList_L13:
	lwz r9,32(r31)
	addi r9,r9,4
	stw r9,32(r31)
_itemList_L2:
	lwz r10,32(r31)
	lwz r9,56(r31)
	cmpw cr0,r10,r9
	bne cr0,_itemList_L20
	lwz r9,132(r31)
	mr r3,r9
	addi r11,r31,160
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_itemList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

getItemTypeInfo = 0x02361830
itemListBase = 0x10399be8


