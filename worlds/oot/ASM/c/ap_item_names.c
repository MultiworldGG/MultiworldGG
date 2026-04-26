#include "ap_item_names.h"

#include "item_table.h"

uint16_t AP_ITEM_NAME_OFFSETS[AP_ITEM_NAME_TABLE_SIZE] = { 0 };
uint8_t AP_ITEM_NAME_TEXT[AP_ITEM_NAME_TEXT_SIZE] = { 0 };
uint16_t AP_ITEM_NAME_COUNT = 0;
uint8_t AP_ITEM_NAME_CONTROL_CODE_VERSION = 2;
char ACTIVE_AP_ITEM_NAME[AP_ACTIVE_ITEM_NAME_SIZE] = { 0 };

static char AP_IMPORTANT_ITEM_FALLBACK[] = "important MWGG item";
static char AP_FILLER_ITEM_FALLBACK[] = "filler MWGG item";
static char AP_ITEM_FALLBACK[] = "MWGG item";

static char* ap_item_names_fallback(uint16_t item_id) {
    if (item_id == GI_AP_PROGRESSION) {
        return AP_IMPORTANT_ITEM_FALLBACK;
    }
    if (item_id == GI_AP_JUNK) {
        return AP_FILLER_ITEM_FALLBACK;
    }
    return AP_ITEM_FALLBACK;
}

static void ap_item_names_copy(char* dst, char* src, uint32_t max_len) {
    uint32_t i = 0;
    while (i + 1 < max_len && src[i] != 0) {
        dst[i] = src[i];
        i++;
    }
    dst[i] = 0;
}

void ap_item_names_set_active_from_override(override_t* override) {
    uint16_t item_id = override->value.base.item_id;
    uint16_t name_id = override->value.ap_item_name_id;
    char* fallback = ap_item_names_fallback(item_id);

    if (name_id > 0 && name_id <= AP_ITEM_NAME_COUNT && name_id < AP_ITEM_NAME_TABLE_SIZE) {
        uint16_t offset = AP_ITEM_NAME_OFFSETS[name_id];
        if (offset < AP_ITEM_NAME_TEXT_SIZE && AP_ITEM_NAME_TEXT[offset] != 0) {
            ap_item_names_copy(ACTIVE_AP_ITEM_NAME, (char*)&AP_ITEM_NAME_TEXT[offset], AP_ACTIVE_ITEM_NAME_SIZE);
            return;
        }
    }

    ap_item_names_copy(ACTIVE_AP_ITEM_NAME, fallback, AP_ACTIVE_ITEM_NAME_SIZE);
}

char* ap_item_names_get_active_name(void) {
    if (ACTIVE_AP_ITEM_NAME[0] == 0) {
        return AP_ITEM_FALLBACK;
    }
    return ACTIVE_AP_ITEM_NAME;
}

char* ap_item_names_get_active_article(void) {
    char first_char = ap_item_names_get_active_name()[0];
    if (first_char >= 'A' && first_char <= 'Z') {
        first_char += 'a' - 'A';
    }
    switch (first_char) {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
            return "an";
        default:
            return "a";
    }
}
