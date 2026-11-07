[Archipelago_shopNames]
moduleMatches = 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.0E, 1.0.2U
.origin = codecave

_getShopName:
	stwu r1,-32(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	lwz r9,16(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L2
	li r9,0
	b _shopNames_L3
_shopNames_L2:
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopNames_L4
	lwz r9,12(r31)
	slwi r9,r9,2
	lwz r10,8(r31)
	add r9,r10,r9
	lwz r9,0(r9)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L5
_shopNames_L4:
	li r9,0
	b _shopNames_L3
_shopNames_L5:
	lwz r9,12(r31)
	slwi r9,r9,2
	lwz r10,8(r31)
	add r9,r10,r9
	lwz r9,0(r9)
_shopNames_L3:
	mr r3,r9
	addi r11,r31,32
	lwz r31,-4(r11)
	mr r1,r11
	blr
_shopNames_LC0:
	.string "SHP_AmrPC"
_getShopArmorName:
	stwu r1,-80(r1)
	mflr r0
	stw r0,84(r1)
	stw r22,40(r1)
	stw r30,72(r1)
	stw r31,76(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lis r9,_shopArmorNames@ha
	lwz r30,_shopArmorNames@l(r9)
	mr r9,r22
	li r5,0
	mr r4,r9
	lis r9,_shopNames_LC0@ha
	addi r3,r9,_shopNames_LC0@l
	bl _getShopIdx
	mr r10,r3
	lis r9,includeShopArmor@ha
	lwz r9,includeShopArmor@l(r9)
	mr r5,r9
	mr r4,r10
	mr r3,r30
	bl _getShopName
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L7
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L8
_shopNames_L7:
	lwz r9,8(r31)
_shopNames_L8:
	mr r3,r9
	addi r11,r31,80
	lwz r0,4(r11)
	mtlr r0
	lwz r22,-40(r11)
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_shopNames_LC1:
	.string "SHP_WpnPC"
_getShopWeaponName:
	stwu r1,-80(r1)
	mflr r0
	stw r0,84(r1)
	stw r23,44(r1)
	stw r30,72(r1)
	stw r31,76(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lis r9,_shopWeaponNames@ha
	lwz r30,_shopWeaponNames@l(r9)
	mr r9,r23
	li r5,1
	mr r4,r9
	lis r9,_shopNames_LC1@ha
	addi r3,r9,_shopNames_LC1@l
	bl _getShopIdx
	mr r10,r3
	lis r9,includeShopWeapons@ha
	lwz r9,includeShopWeapons@l(r9)
	mr r5,r9
	mr r4,r10
	mr r3,r30
	bl _getShopName
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L10
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L11
_shopNames_L10:
	lwz r9,8(r31)
_shopNames_L11:
	mr r3,r9
	addi r11,r31,80
	lwz r0,4(r11)
	mtlr r0
	lwz r23,-36(r11)
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getShopDollFrameName:
	stwu r1,-96(r1)
	mflr r0
	stw r0,100(r1)
	stw r20,48(r1)
	stw r31,92(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lis r9,_shopDollFrameNames@ha
	lwz r10,_shopDollFrameNames@l(r9)
	mr r8,r20
	lis r9,includeShopSkellFrames@ha
	lwz r9,includeShopSkellFrames@l(r9)
	mr r5,r9
	mr r4,r8
	mr r3,r10
	bl _getShopName
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L13
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L14
_shopNames_L13:
	lwz r9,8(r31)
_shopNames_L14:
	mr r3,r9
	addi r11,r31,96
	lwz r0,4(r11)
	mtlr r0
	lwz r20,-48(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getShopAugmentName:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lwz r6,44(r1)
	li r9,0
	stw r9,8(r31)
	lis r9,_augmentMenuType@ha
	lwz r9,_augmentMenuType@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L16
	lis r9,_shopAugmentNames@ha
	lwz r10,_shopAugmentNames@l(r9)
	mr r8,r6
	lis r9,includeShopAugments@ha
	lwz r9,includeShopAugments@l(r9)
	mr r5,r9
	mr r4,r8
	mr r3,r10
	bl _getShopName
	stw r3,8(r31)
_shopNames_L16:
	lis r9,_augmentMenuType@ha
	lwz r9,_augmentMenuType@l(r9)
	cmpwi cr0,r9,1
	bne cr0,_shopNames_L17
	lis r9,_shopDollAugmentNames@ha
	lwz r10,_shopDollAugmentNames@l(r9)
	mr r8,r6
	lis r9,includeShopSkellAugments@ha
	lwz r9,includeShopSkellAugments@l(r9)
	mr r5,r9
	mr r4,r8
	mr r3,r10
	bl _getShopName
	stw r3,8(r31)
_shopNames_L17:
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L18
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L19
_shopNames_L18:
	lwz r9,8(r31)
_shopNames_L19:
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_shopNames_LC2:
	.string "SHP_AmrDL"
_getShopDollArmorName:
	stwu r1,-96(r1)
	mflr r0
	stw r0,100(r1)
	stw r21,52(r1)
	stw r30,88(r1)
	stw r31,92(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lis r9,_shopDollArmorNames@ha
	lwz r30,_shopDollArmorNames@l(r9)
	mr r9,r21
	li r5,0
	mr r4,r9
	lis r9,_shopNames_LC2@ha
	addi r3,r9,_shopNames_LC2@l
	bl _getShopIdx
	mr r10,r3
	lis r9,includeShopSkellArmor@ha
	lwz r9,includeShopSkellArmor@l(r9)
	mr r5,r9
	mr r4,r10
	mr r3,r30
	bl _getShopName
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L21
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L22
_shopNames_L21:
	lwz r9,8(r31)
_shopNames_L22:
	mr r3,r9
	addi r11,r31,96
	lwz r0,4(r11)
	mtlr r0
	lwz r21,-44(r11)
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_shopNames_LC3:
	.string "SHP_WpnDL"
_getShopDollWeaponName:
	stwu r1,-80(r1)
	mflr r0
	stw r0,84(r1)
	stw r25,52(r1)
	stw r30,72(r1)
	stw r31,76(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lis r9,_shopDollWeaponNames@ha
	lwz r30,_shopDollWeaponNames@l(r9)
	mr r9,r25
	li r5,0
	mr r4,r9
	lis r9,_shopNames_LC3@ha
	addi r3,r9,_shopNames_LC3@l
	bl _getShopIdx
	mr r10,r3
	lis r9,includeShopSkellWeapons@ha
	lwz r9,includeShopSkellWeapons@l(r9)
	mr r5,r9
	mr r4,r10
	mr r3,r30
	bl _getShopName
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L24
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L25
_shopNames_L24:
	lwz r9,8(r31)
_shopNames_L25:
	mr r3,r9
	addi r11,r31,80
	lwz r0,4(r11)
	mtlr r0
	lwz r25,-28(r11)
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getShopBlueprintName:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r28,48(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	lis r9,_shopBlueprintNames@ha
	lwz r10,_shopBlueprintNames@l(r9)
	mr r8,r28
	lis r9,includeShopBlueprints@ha
	lwz r9,includeShopBlueprints@l(r9)
	mr r5,r9
	mr r4,r8
	mr r3,r10
	bl _getShopName
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopNames_L27
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	b _shopNames_L28
_shopNames_L27:
	lwz r9,8(r31)
_shopNames_L28:
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r28,-16(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_shopNames_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

0x02a2d2c8 = bl _getShopWeaponName
0x02a2e260 = bl _getShopArmorName
0x02a2f8f0 = bl _getShopDollArmorName
0x02a2eef8 = bl _getShopDollWeaponName
0x02a304e0 = bl _getShopDollFrameName
0x02a81cdc = bl _getShopAugmentName
0x02a81da4 = bl _getShopAugmentName
0x02a81e88 = bl _getShopAugmentName
0x02a7b2d4 = bl _getShopBlueprintName  # gear
0x02a7b35c = bl _getShopBlueprintName  # dolls


[Archipelago_shopNames_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

0x02a2d2b8 = bl _getShopWeaponName
0x02a2e250 = bl _getShopArmorName
0x02a2f8e0 = bl _getShopDollArmorName
0x02a2eee8 = bl _getShopDollWeaponName
0x02a304d0 = bl _getShopDollFrameName
0x02a81ccc = bl _getShopAugmentName
0x02a81d94 = bl _getShopAugmentName
0x02a81e78 = bl _getShopAugmentName
0x02a7b2c4 = bl _getShopBlueprintName  # gear
0x02a7b34c = bl _getShopBlueprintName  # dolls


