#ifndef AP_FILLER_TINT_H
#define AP_FILLER_TINT_H

#include "z64.h"

typedef enum {
    AP_FILLER_TINT_CHEST_FRONT,
    AP_FILLER_TINT_CHEST_BASE,
    AP_FILLER_TINT_POT_SIDE,
    AP_FILLER_TINT_POT_TOP,
    AP_FILLER_TINT_SMALLCRATE,
    AP_FILLER_TINT_CRATE,
    AP_FILLER_TINT_SLOT_MAX,
} ApFillerTintSlot;

void* ap_filler_resolve_texture(z64_game_t* game, z64_actor_t* actor, void* texture);
void* ap_filler_tint_rgba16_texture(void* texture, ApFillerTintSlot slot, uint32_t bytes);
void* ap_filler_tint_ci8_texture(void* texture, ApFillerTintSlot slot, uint32_t bytes, uint32_t palette_bytes);

#endif
