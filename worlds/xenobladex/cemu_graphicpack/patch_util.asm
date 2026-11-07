[Archipelago_util]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_writeConsole:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lwz r3,8(r31)
	lis r12,_after_util_1__strlen@ha
	addi r12,r12,_after_util_1__strlen@l
	mtlr r12
	lis r12,__strlen@ha
	addi r12,r12,__strlen@l
	mtctr r12
	bctr
_after_util_1__strlen:
	mr r9,r3
	mr r4,r9
	lwz r3,8(r31)
	bl import.coreinit.OSConsoleWrite
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_util_LC0:
	.string "Debug Message"
_writeDebug:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,menuBasePtr@ha
	lwz r10,menuBasePtr@l(r9)
	lwz r5,8(r31)
	lis r9,_util_LC0@ha
	addi r4,r9,_util_LC0@l
	mr r3,r10
	bl writeSystemLog
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_playSound:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	li r9,0
	stw r9,8(r31)
	li r9,0
	stw r9,28(r31)
	addi r9,r31,28
	lwz r4,8(r31)
	mr r3,r9
	bl getInnerHandle
	lis r9,0x1036
	ori r9,r9,0x7664
	stw r9,12(r31)
	lwz r9,28(r31)
	srwi r9,r9,19
	rlwinm r9,r9,0,20,31
	stw r9,16(r31)
	lwz r9,16(r31)
	mulli r9,r9,12
	lwz r10,12(r31)
	add r9,r10,r9
	stw r9,20(r31)
	lwz r9,20(r31)
	lwz r9,0(r9)
	lwz r9,488(r9)
	stw r9,24(r31)
	li r5,1
	lwz r4,40(r31)
	lwz r3,24(r31)
	bl requestSoundCreate
	nop
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_util_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

requestSoundCreate = 0x02418344

menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu


