#include "ap_filler_tint.h"

#define AP_FILLER_TINT_MAX_BYTES 4608
#define AP_FILLER_TINT_R 12
#define AP_FILLER_TINT_G 8
#define AP_FILLER_TINT_B 26

static uint8_t ap_filler_tint_buffers[AP_FILLER_TINT_SLOT_MAX][AP_FILLER_TINT_MAX_BYTES] __attribute__((aligned(16)));

static uint16_t ap_filler_tint_rgba16_pixel(uint16_t pixel) {
    uint16_t r = (pixel >> 11) & 0x1F;
    uint16_t g = (pixel >> 6) & 0x1F;
    uint16_t b = (pixel >> 1) & 0x1F;
    uint16_t a = pixel & 1;

    r = (r + AP_FILLER_TINT_R) >> 1;
    g = (g + AP_FILLER_TINT_G) >> 1;
    b = (b + AP_FILLER_TINT_B) >> 1;

    return (r << 11) | (g << 6) | (b << 1) | a;
}

void* ap_filler_resolve_texture(z64_game_t* game, z64_actor_t* actor, void* texture) {
    uint32_t addr = (uint32_t)texture;
    uint32_t segment = addr >> 24;
    uint32_t offset = addr & 0x00FFFFFF;

    if (segment == 0x05 && game->obj_ctxt.skeep_index < game->obj_ctxt.n_objects) {
        return ((uint8_t*)game->obj_ctxt.objects[game->obj_ctxt.skeep_index].data) + offset;
    }

    if (segment == 0x06 && actor != 0 && actor->alloc_index < game->obj_ctxt.n_objects) {
        return ((uint8_t*)game->obj_ctxt.objects[actor->alloc_index].data) + offset;
    }

    return texture;
}

void* ap_filler_tint_rgba16_texture(void* texture, ApFillerTintSlot slot, uint32_t bytes) {
    uint16_t* src = (uint16_t*)texture;
    uint16_t* dst = (uint16_t*)ap_filler_tint_buffers[slot];
    uint32_t pixels = bytes >> 1;
    uint32_t addr = (uint32_t)texture;

    if (texture == 0 || (addr >> 24) < 0x10 || bytes > AP_FILLER_TINT_MAX_BYTES) {
        return texture;
    }

    for (uint32_t i = 0; i < pixels; i++) {
        dst[i] = ap_filler_tint_rgba16_pixel(src[i]);
    }

    return dst;
}

void* ap_filler_tint_ci8_texture(void* texture, ApFillerTintSlot slot, uint32_t bytes, uint32_t palette_bytes) {
    uint8_t* src = (uint8_t*)texture;
    uint8_t* dst = ap_filler_tint_buffers[slot];
    uint32_t addr = (uint32_t)texture;

    if (texture == 0 || (addr >> 24) < 0x10 || bytes > AP_FILLER_TINT_MAX_BYTES || palette_bytes > bytes) {
        return texture;
    }

    for (uint32_t i = 0; i < bytes; i++) {
        dst[i] = src[i];
    }

    for (uint32_t i = 0; i < (palette_bytes >> 1); i++) {
        uint16_t* palette = (uint16_t*)dst;
        palette[i] = ap_filler_tint_rgba16_pixel(palette[i]);
    }

    return dst;
}
