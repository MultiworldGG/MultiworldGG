#include "ap_items.h"

#include "item_table.h"

extern item_row_t item_table[GI_RANDO_MAX];

_Static_assert(AP_FILLER_ITEM_ID > GI_AP_JUNK && AP_FILLER_ITEM_ID < GI_KOKIRI_EMERALD,
               "AP filler must fit in the reserved item-table gap");

void ap_items_init(void) {
    item_row_t* filler = &item_table[AP_FILLER_ITEM_ID];
    const item_row_t* collectible = &item_table[GI_RUPEE_GREEN];

    // Inherit the AP model, text and seed-configured chest appearance. Useful
    // and legacy items retain the original GI_AP_JUNK row and its dialog.
    *filler = item_table[GI_AP_JUNK];

    // Reuse a matching native collectible/action pair for the quick pickup
    // path. These items belong to another player, so dispatch sends them
    // without applying the local rupee action.
    filler->base_item_id = collectible->base_item_id;
    filler->action_id = collectible->action_id;
    filler->collectible = collectible->collectible;
    filler->effect = collectible->effect;
    filler->effect_arg1 = collectible->effect_arg1;
    filler->effect_arg2 = collectible->effect_arg2;
}
