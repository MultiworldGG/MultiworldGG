[Archipelago_curl]
moduleMatches = 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.0E, 1.0.2U
.origin = codecave

curlPort:
	.int    $curlPort
_uploadHandle:
	.int    0
_uploadMultiHandle:
	.int    0
_downloadHandle:
	.int    0
_downloadMultiHandle:
	.int    0
_curl_LC0:
	.string "http://localhost:%d/locations"
_curl_LC1:
	.string "http://localhost:%d/items"
_initCurl:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	li r9,10002
	stw r9,8(r31)
	lis r9,curlPort@ha
	lwz r9,curlPort@l(r9)
	stw r9,12(r31)
	bl import.nlibcurl.curl_easy_init
	mr r10,r3
	lis r9,_uploadHandle@ha
	stw r10,_uploadHandle@l(r9)
	addi r10,r31,16
	lwz r6,12(r31)
	lis r9,_curl_LC0@ha
	addi r5,r9,_curl_LC0@l
	li r4,40
	mr r3,r10
	crxor 6,6,6
	lis r12,_after_curl_1__sprintf_s@ha
	addi r12,r12,_after_curl_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_curl_1__sprintf_s:
	lis r9,_uploadHandle@ha
	lwz r9,_uploadHandle@l(r9)
	addi r10,r31,16
	mr r5,r10
	lwz r4,8(r31)
	mr r3,r9
	crxor 6,6,6
	bl import.nlibcurl.curl_easy_setopt
	bl import.nlibcurl.curl_multi_init
	mr r10,r3
	lis r9,_uploadMultiHandle@ha
	stw r10,_uploadMultiHandle@l(r9)
	bl import.nlibcurl.curl_easy_init
	mr r10,r3
	lis r9,_downloadHandle@ha
	stw r10,_downloadHandle@l(r9)
	addi r10,r31,16
	lwz r6,12(r31)
	lis r9,_curl_LC1@ha
	addi r5,r9,_curl_LC1@l
	li r4,40
	mr r3,r10
	crxor 6,6,6
	lis r12,_after_curl_2__sprintf_s@ha
	addi r12,r12,_after_curl_2__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_curl_2__sprintf_s:
	lis r9,_downloadHandle@ha
	lwz r9,_downloadHandle@l(r9)
	addi r10,r31,16
	mr r5,r10
	lwz r4,8(r31)
	mr r3,r9
	crxor 6,6,6
	bl import.nlibcurl.curl_easy_setopt
	bl import.nlibcurl.curl_multi_init
	mr r10,r3
	lis r9,_downloadMultiHandle@ha
	stw r10,_downloadMultiHandle@l(r9)
	nop
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_postCurl:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	li r9,10015
	stw r9,8(r31)
	li r9,47
	stw r9,12(r31)
	li r9,1
	stw r9,16(r31)
	lis r9,_uploadMultiHandle@ha
	lwz r10,_uploadMultiHandle@l(r9)
	lis r9,_uploadHandle@ha
	lwz r9,_uploadHandle@l(r9)
	mr r4,r9
	mr r3,r10
	bl import.nlibcurl.curl_multi_add_handle
	lis r9,_uploadHandle@ha
	lwz r9,_uploadHandle@l(r9)
	lwz r5,24(r31)
	lwz r4,8(r31)
	mr r3,r9
	crxor 6,6,6
	bl import.nlibcurl.curl_easy_setopt
	lis r9,_uploadHandle@ha
	lwz r9,_uploadHandle@l(r9)
	li r5,1
	lwz r4,12(r31)
	mr r3,r9
	crxor 6,6,6
	bl import.nlibcurl.curl_easy_setopt
_curl_L3:
	lis r9,_uploadMultiHandle@ha
	lwz r9,_uploadMultiHandle@l(r9)
	addi r10,r31,16
	mr r4,r10
	mr r3,r9
	bl import.nlibcurl.curl_multi_perform
	lwz r9,16(r31)
	cmpwi cr0,r9,0
	bne cr0,_curl_L3
	lis r9,_uploadMultiHandle@ha
	lwz r10,_uploadMultiHandle@l(r9)
	lis r9,_uploadHandle@ha
	lwz r9,_uploadHandle@l(r9)
	mr r4,r9
	mr r3,r10
	bl import.nlibcurl.curl_multi_remove_handle
	nop
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_WriteCallback:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	stw r6,36(r31)
	lwz r10,28(r31)
	lwz r9,32(r31)
	mullw r9,r10,r9
	stw r9,8(r31)
	lwz r9,36(r31)
	stw r9,12(r31)
	lwz r9,12(r31)
	lwz r8,0(r9)
	lwz r9,12(r31)
	lwz r10,4(r9)
	lwz r9,8(r31)
	add r9,r10,r9
	addi r9,r9,1
	mr r4,r9
	mr r3,r8
	lis r12,_after_curl_3__realloc@ha
	addi r12,r12,_after_curl_3__realloc@l
	mtlr r12
	lis r12,__realloc@ha
	addi r12,r12,__realloc@l
	mtctr r12
	bctr
_after_curl_3__realloc:
	mr r9,r3
	stw r9,16(r31)
	lwz r9,12(r31)
	lwz r10,16(r31)
	stw r10,0(r9)
	lwz r9,12(r31)
	lwz r10,0(r9)
	lwz r9,12(r31)
	lwz r9,4(r9)
	add r9,r10,r9
	lwz r5,8(r31)
	lwz r4,24(r31)
	mr r3,r9
	bl import.coreinit.memcpy
	lwz r9,12(r31)
	lwz r10,4(r9)
	lwz r9,8(r31)
	add r10,r10,r9
	lwz r9,12(r31)
	stw r10,4(r9)
	lwz r9,12(r31)
	lwz r10,0(r9)
	lwz r9,12(r31)
	lwz r9,4(r9)
	add r9,r10,r9
	li r10,0
	stb r10,0(r9)
	lwz r9,8(r31)
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getCurl:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	li r9,0
	stw r9,16(r31)
	li r9,0
	stw r9,20(r31)
	li r9,1
	stw r9,24(r31)
	li r9,20011
	stw r9,8(r31)
	li r9,10001
	stw r9,12(r31)
	lis r9,_downloadMultiHandle@ha
	lwz r10,_downloadMultiHandle@l(r9)
	lis r9,_downloadHandle@ha
	lwz r9,_downloadHandle@l(r9)
	mr r4,r9
	mr r3,r10
	bl import.nlibcurl.curl_multi_add_handle
	lis r9,_downloadHandle@ha
	lwz r10,_downloadHandle@l(r9)
	lis r9,_WriteCallback@ha
	addi r5,r9,_WriteCallback@l
	lwz r4,8(r31)
	mr r3,r10
	crxor 6,6,6
	bl import.nlibcurl.curl_easy_setopt
	lis r9,_downloadHandle@ha
	lwz r9,_downloadHandle@l(r9)
	addi r10,r31,16
	mr r5,r10
	lwz r4,12(r31)
	mr r3,r9
	crxor 6,6,6
	bl import.nlibcurl.curl_easy_setopt
_curl_L7:
	lis r9,_downloadMultiHandle@ha
	lwz r9,_downloadMultiHandle@l(r9)
	addi r10,r31,24
	mr r4,r10
	mr r3,r9
	bl import.nlibcurl.curl_multi_perform
	lwz r9,24(r31)
	cmpwi cr0,r9,0
	bne cr0,_curl_L7
	lis r9,_downloadMultiHandle@ha
	lwz r10,_downloadMultiHandle@l(r9)
	lis r9,_downloadHandle@ha
	lwz r9,_downloadHandle@l(r9)
	mr r4,r9
	mr r3,r10
	bl import.nlibcurl.curl_multi_remove_handle
	lwz r9,16(r31)
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_cleanupCurl:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	lis r9,_uploadHandle@ha
	lwz r9,_uploadHandle@l(r9)
	mr r3,r9
	bl import.nlibcurl.curl_easy_cleanup
	lis r9,_uploadMultiHandle@ha
	lwz r9,_uploadMultiHandle@l(r9)
	mr r3,r9
	bl import.nlibcurl.curl_multi_cleanup
	lis r9,_downloadHandle@ha
	lwz r9,_downloadHandle@l(r9)
	mr r3,r9
	bl import.nlibcurl.curl_easy_cleanup
	lis r9,_downloadMultiHandle@ha
	lwz r9,_downloadMultiHandle@l(r9)
	mr r3,r9
	bl import.nlibcurl.curl_multi_cleanup
	lis r9,_uploadHandle@ha
	li r10,0
	stw r10,_uploadHandle@l(r9)
	lis r9,_uploadMultiHandle@ha
	li r10,0
	stw r10,_uploadMultiHandle@l(r9)
	lis r9,_downloadHandle@ha
	li r10,0
	stw r10,_downloadHandle@l(r9)
	lis r9,_downloadMultiHandle@ha
	li r10,0
	stw r10,_downloadMultiHandle@l(r9)
	nop
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_curl_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

__realloc = 0x03b1af20


[Archipelago_curl_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

__realloc = 0x03b1aea0


