[Archipelago_shopList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_formatShopText:
	.string "SH Id=%03x Tp=%01x:"
_shopArmorNames:
	.int    0
_shopWeaponNames:
	.int    0
_shopDollArmorNames:
	.int    0
_shopDollWeaponNames:
	.int    0
_shopDollFrameNames:
	.int    0
_shopAugmentNames:
	.int    0
_shopDollAugmentNames:
	.int    0
_shopBlueprintNames:
	.int    0
_postShopList:
	stwu r1,-96(r1)
	mflr r0
	stw r0,100(r1)
	stw r31,92(r1)
	mr r31,r1
	stw r3,72(r31)
	stw r4,76(r31)
	stw r5,80(r31)
	stw r6,84(r31)
	li r9,1
	stw r9,8(r31)
	b _shopList_L2
_shopList_L5:
	bl GetBlueprintPtr
	mr r9,r3
	stw r9,64(r31)
	lwz r9,8(r31)
	lwz r10,64(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,68(r31)
	lwz r9,68(r31)
	cmpwi cr0,r9,3
	bne cr0,_shopList_L3
	lwz r10,84(r31)
	li r7,6
	lwz r6,8(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_1__sprintf_s@ha
	addi r12,r12,_after_shopList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L3:
	lwz r10,76(r31)
	lwz r9,80(r31)
	cmplw cr0,r10,r9
	ble cr0,_shopList_L4
	lwz r3,72(r31)
	bl _postCurl
	lwz r9,72(r31)
	stw r9,76(r31)
_shopList_L4:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_shopList_L2:
	lwz r9,8(r31)
	cmpwi cr0,r9,199
	ble cr0,_shopList_L5
	li r9,1
	stw r9,12(r31)
	b _shopList_L6
_shopList_L15:
	bl GetKnowledgePtr
	mr r9,r3
	stw r9,16(r31)
	li r9,19364
	stw r9,20(r31)
	li r9,15364
	stw r9,24(r31)
	lwz r10,20(r31)
	lwz r9,12(r31)
	add r9,r10,r9
	lwz r10,16(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,28(r31)
	lwz r10,24(r31)
	lwz r9,12(r31)
	add r9,r10,r9
	lwz r10,16(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,32(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,30,30
	stw r9,36(r31)
	lwz r9,32(r31)
	rlwinm r9,r9,0,30,30
	stw r9,40(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,29,29
	stw r9,44(r31)
	lwz r9,32(r31)
	rlwinm r9,r9,0,29,29
	stw r9,48(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,28,28
	stw r9,52(r31)
	lwz r9,32(r31)
	rlwinm r9,r9,0,28,28
	stw r9,32(r31)
	lwz r9,32(r31)
	stw r9,56(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,27,27
	stw r9,60(r31)
	lwz r9,56(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L7
	lwz r10,84(r31)
	li r7,7
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_2__sprintf_s@ha
	addi r12,r12,_after_shopList_2__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_2__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L7:
	lwz r9,48(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L8
	lwz r10,84(r31)
	li r7,8
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_3__sprintf_s@ha
	addi r12,r12,_after_shopList_3__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_3__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L8:
	lwz r9,40(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L9
	lwz r10,84(r31)
	li r7,9
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_4__sprintf_s@ha
	addi r12,r12,_after_shopList_4__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_4__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L9:
	lwz r9,52(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L10
	lwz r10,84(r31)
	li r7,10
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_5__sprintf_s@ha
	addi r12,r12,_after_shopList_5__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_5__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L10:
	lwz r9,44(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L11
	lwz r10,84(r31)
	li r7,11
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_6__sprintf_s@ha
	addi r12,r12,_after_shopList_6__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_6__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L11:
	lwz r9,36(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L12
	lwz r10,84(r31)
	li r7,12
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_7__sprintf_s@ha
	addi r12,r12,_after_shopList_7__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_7__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L12:
	lwz r9,60(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L13
	lwz r10,84(r31)
	li r7,13
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_8__sprintf_s@ha
	addi r12,r12,_after_shopList_8__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_8__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L13:
	lwz r10,76(r31)
	lwz r9,80(r31)
	cmplw cr0,r10,r9
	ble cr0,_shopList_L14
	lwz r3,72(r31)
	bl _postCurl
	lwz r9,72(r31)
	stw r9,76(r31)
_shopList_L14:
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
_shopList_L6:
	lwz r9,12(r31)
	cmpwi cr0,r9,3949
	ble cr0,_shopList_L15
	lwz r9,76(r31)
	mr r3,r9
	addi r11,r31,96
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
setKnowledgeBit:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	bl GetKnowledgePtr
	mr r9,r3
	stw r9,12(r31)
	li r9,19364
	stw r9,16(r31)
	li r9,15364
	stw r9,20(r31)
	lwz r9,16(r31)
	stw r9,8(r31)
	lwz r9,48(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopList_L18
	lwz r9,20(r31)
	stw r9,8(r31)
_shopList_L18:
	lwz r10,8(r31)
	lwz r9,40(r31)
	add r9,r10,r9
	lwz r10,12(r31)
	add r9,r10,r9
	stw r9,24(r31)
	lwz r9,24(r31)
	lbz r9,0(r9)
	mr r10,r9
	lwz r9,44(r31)
	or r9,r10,r9
	mr r10,r9
	lwz r9,24(r31)
	stb r10,0(r9)
	nop
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
setKnowledgeValue:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	bl GetKnowledgePtr
	mr r9,r3
	stw r9,12(r31)
	li r9,19364
	stw r9,16(r31)
	li r9,15364
	stw r9,20(r31)
	lwz r9,16(r31)
	stw r9,8(r31)
	lwz r9,48(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopList_L20
	lwz r9,20(r31)
	stw r9,8(r31)
_shopList_L20:
	lwz r10,8(r31)
	lwz r9,40(r31)
	add r9,r10,r9
	lwz r10,12(r31)
	add r9,r10,r9
	stw r9,24(r31)
	lwz r9,44(r31)
	mr r10,r9
	lwz r9,24(r31)
	stb r10,0(r9)
	nop
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
getKnowledgeBit:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	bl GetKnowledgePtr
	mr r9,r3
	stw r9,12(r31)
	li r9,19364
	stw r9,16(r31)
	li r9,15364
	stw r9,20(r31)
	lwz r9,16(r31)
	stw r9,8(r31)
	lwz r9,48(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopList_L22
	lwz r9,20(r31)
	stw r9,8(r31)
_shopList_L22:
	lwz r10,8(r31)
	lwz r9,40(r31)
	add r9,r10,r9
	lwz r10,12(r31)
	add r9,r10,r9
	stw r9,24(r31)
	lwz r9,24(r31)
	lbz r9,0(r9)
	rlwinm r10,r9,0,24,31
	lwz r9,44(r31)
	and r9,r10,r9
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_initShopCache:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	lwz r9,8(r31)
	lwz r9,0(r9)
	cmpwi cr0,r9,0
	bne cr0,_shopList_L27
	lwz r9,12(r31)
	li r4,4
	mr r3,r9
	lis r12,_after_shopList_9__calloc@ha
	addi r12,r12,_after_shopList_9__calloc@l
	mtlr r12
	lis r12,__calloc@ha
	addi r12,r12,__calloc@l
	mtctr r12
	bctr
_after_shopList_9__calloc:
	mr r10,r3
	lwz r9,8(r31)
	stw r10,0(r9)
	b _shopList_L24
_shopList_L27:
	nop
_shopList_L24:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_copyShopName:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r30,24(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	stw r6,20(r31)
	lwz r9,12(r31)
	slwi r9,r9,2
	lwz r10,8(r31)
	add r9,r10,r9
	lwz r9,0(r9)
	cmpwi cr0,r9,0
	bne cr0,_shopList_L31
	lwz r9,20(r31)
	addi r9,r9,1
	mr r8,r9
	lwz r9,12(r31)
	slwi r9,r9,2
	lwz r10,8(r31)
	add r30,r10,r9
	li r4,1
	mr r3,r8
	lis r12,_after_shopList_10__calloc@ha
	addi r12,r12,_after_shopList_10__calloc@l
	mtlr r12
	lis r12,__calloc@ha
	addi r12,r12,__calloc@l
	mtctr r12
	bctr
_after_shopList_10__calloc:
	mr r9,r3
	stw r9,0(r30)
	lwz r9,12(r31)
	slwi r9,r9,2
	lwz r10,8(r31)
	add r9,r10,r9
	lwz r9,0(r9)
	lwz r4,16(r31)
	mr r3,r9
	lis r12,_after_shopList_11__strcpy@ha
	addi r12,r12,_after_shopList_11__strcpy@l
	mtlr r12
	lis r12,__strcpy@ha
	addi r12,r12,__strcpy@l
	mtctr r12
	bctr
_after_shopList_11__strcpy:
	b _shopList_L28
_shopList_L31:
	nop
_shopList_L28:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_cacheShopItemName:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lwz r3,32(r31)
	lis r12,_after_shopList_12__strlen@ha
	addi r12,r12,_after_shopList_12__strlen@l
	mtlr r12
	lis r12,__strlen@ha
	addi r12,r12,__strlen@l
	mtctr r12
	bctr
_after_shopList_12__strlen:
	mr r9,r3
	stw r9,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L42
	lwz r9,24(r31)
	cmpwi cr0,r9,6
	bne cr0,_shopList_L35
	li r4,200
	lis r9,_shopBlueprintNames@ha
	addi r3,r9,_shopBlueprintNames@l
	bl _initShopCache
	lis r9,_shopBlueprintNames@ha
	lwz r9,_shopBlueprintNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L35:
	lwz r9,24(r31)
	cmpwi cr0,r9,7
	bne cr0,_shopList_L36
	li r4,1700
	lis r9,_shopArmorNames@ha
	addi r3,r9,_shopArmorNames@l
	bl _initShopCache
	lis r9,_shopArmorNames@ha
	lwz r9,_shopArmorNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L36:
	lwz r9,24(r31)
	cmpwi cr0,r9,8
	bne cr0,_shopList_L37
	li r4,1900
	lis r9,_shopWeaponNames@ha
	addi r3,r9,_shopWeaponNames@l
	bl _initShopCache
	lis r9,_shopWeaponNames@ha
	lwz r9,_shopWeaponNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L37:
	lwz r9,24(r31)
	cmpwi cr0,r9,9
	bne cr0,_shopList_L38
	li r4,3700
	lis r9,_shopAugmentNames@ha
	addi r3,r9,_shopAugmentNames@l
	bl _initShopCache
	lis r9,_shopAugmentNames@ha
	lwz r9,_shopAugmentNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L38:
	lwz r9,24(r31)
	cmpwi cr0,r9,10
	bne cr0,_shopList_L39
	li r4,300
	lis r9,_shopDollArmorNames@ha
	addi r3,r9,_shopDollArmorNames@l
	bl _initShopCache
	lis r9,_shopDollArmorNames@ha
	lwz r9,_shopDollArmorNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L39:
	lwz r9,24(r31)
	cmpwi cr0,r9,11
	bne cr0,_shopList_L40
	li r4,900
	lis r9,_shopDollWeaponNames@ha
	addi r3,r9,_shopDollWeaponNames@l
	bl _initShopCache
	lis r9,_shopDollWeaponNames@ha
	lwz r9,_shopDollWeaponNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L40:
	lwz r9,24(r31)
	cmpwi cr0,r9,12
	bne cr0,_shopList_L41
	li r4,3200
	lis r9,_shopDollAugmentNames@ha
	addi r3,r9,_shopDollAugmentNames@l
	bl _initShopCache
	lis r9,_shopDollAugmentNames@ha
	lwz r9,_shopDollAugmentNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L41:
	lwz r9,24(r31)
	cmpwi cr0,r9,13
	bne cr0,_shopList_L32
	li r4,50
	lis r9,_shopDollFrameNames@ha
	addi r3,r9,_shopDollFrameNames@l
	bl _initShopCache
	lis r9,_shopDollFrameNames@ha
	lwz r9,_shopDollFrameNames@l(r9)
	lwz r6,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	mr r3,r9
	bl _copyShopName
	b _shopList_L32
_shopList_L42:
	nop
_shopList_L32:
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_shopList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

GetKnowledgePtr = 0x027fb934
GetBlueprintPtr = 0x027fbae4


