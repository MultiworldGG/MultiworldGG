[Archipelago_util]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

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


[Archipelago_util_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu


