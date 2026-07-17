[Archipelago_locationList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07, 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.2U, 1.0.0E, 1.0.1E, 1.0.0E, 1.0.2U
.origin = codecave

_formatLocationText:
	.string "LC Id=%03x Fg=%01x Tp=%01x:"
_locationList_LC0:
	.string "FLD_Location"
_locationList_LC1:
	.string "Loc_type"
_locationList_LC2:
	.string "flg"
_postLocationList:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	stw r6,52(r31)
	lis r9,_locationList_LC0@ha
	addi r3,r9,_locationList_LC0@l
	bl getFP
	mr r9,r3
	stw r9,12(r31)
	lwz r3,12(r31)
	bl getIdTop
	mr r9,r3
	stw r9,16(r31)
	lwz r3,12(r31)
	bl getIdCount
	mr r9,r3
	stw r9,20(r31)
	lwz r9,16(r31)
	stw r9,8(r31)
	b _locationList_L2
_locationList_L4:
	li r6,1
	lwz r5,8(r31)
	lis r9,_locationList_LC1@ha
	addi r4,r9,_locationList_LC1@l
	lwz r3,12(r31)
	bl getValCheck
	mr r9,r3
	srawi r9,r9,24
	stw r9,24(r31)
	li r6,2
	lwz r5,8(r31)
	lis r9,_locationList_LC2@ha
	addi r4,r9,_locationList_LC2@l
	lwz r3,12(r31)
	bl getValCheck
	mr r9,r3
	srawi r9,r9,16
	stw r9,28(r31)
	lwz r4,28(r31)
	li r3,1
	bl getLocal
	mr r9,r3
	stw r9,28(r31)
	lwz r10,52(r31)
	lwz r8,24(r31)
	lwz r7,28(r31)
	lwz r6,8(r31)
	lis r9,_formatLocationText@ha
	addi r5,r9,_formatLocationText@l
	mr r4,r10
	lwz r3,44(r31)
	crxor 6,6,6
	lis r12,_after_locationList_1__sprintf_s@ha
	addi r12,r12,_after_locationList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_locationList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,44(r31)
	add r9,r9,r10
	stw r9,44(r31)
	lwz r10,44(r31)
	lwz r9,48(r31)
	cmplw cr0,r10,r9
	ble cr0,_locationList_L3
	lwz r3,40(r31)
	bl _postCurl
	lwz r9,40(r31)
	stw r9,44(r31)
_locationList_L3:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_locationList_L2:
	lwz r10,16(r31)
	lwz r9,20(r31)
	add r9,r10,r9
	lwz r10,8(r31)
	cmpw cr0,r10,r9
	blt cr0,_locationList_L4
	lwz r9,44(r31)
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_locationList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

getFP = 0x0229bd4c # ::GameBdat


[Archipelago_locationList_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

getIdTop = 0x029c23b4 # ::Bdat
getIdCount = 0x029c23ac # ::Bdat
getValCheck = 0x029c2630 # ::Bdat


[Archipelago_locationList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

getIdTop = 0x029c23a4 # ::Bdat
getIdCount = 0x029c239c # ::Bdat
getValCheck = 0x029c2620 # ::Bdat


