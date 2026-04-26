#ifndef AP_ITEM_NAMES_H
#define AP_ITEM_NAMES_H

#include <stdint.h>

#include "override.h"

#define AP_ITEM_NAME_TABLE_SIZE 2201
#define AP_ITEM_NAME_TEXT_SIZE 0xFFFF
#define AP_ACTIVE_ITEM_NAME_SIZE 49

void ap_item_names_set_active_from_override(override_t* override);
char* ap_item_names_get_active_name(void);
char* ap_item_names_get_active_article(void);

#endif
