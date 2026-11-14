#include "z64.h"
#include "ap_player.h"
#include "ap_item_names.h"

// Separate from the eight-character save-name table and its fixed client offsets.
uint8_t AP_DISPLAY_NAMES[AP_PLAYER_TABLE_SIZE][AP_DISPLAY_NAME_SIZE] = { 0 };
uint32_t AP_MESSAGE_CHAR_WIDTHS[256] = { 0 }; // populated from TextBox.py
extern uint16_t PLAYER_ID;
extern uint16_t PLAYER_NAME_ID;
extern char FILENAME_ENCODING[256];

#define RAW_SIZE 1280
#define EXPANDED_SIZE 2048
#define LINE_WIDTH 1801800
#define ICON_LINE_WIDTH 1441440
static uint8_t expanded[EXPANDED_SIZE];
static uint8_t formatted[RAW_SIZE];

static uint32_t code_size(uint8_t c) {
    switch (c) {
        case 0x05: case 0x06: case 0x0C: case 0x0E: case 0x13:
        case 0x14: case 0x1E: case 0xF0: case 0xF1: return 2;
        case 0x07: case 0x12: return 3;
        case 0x15: return 4;
        default: return 1;
    }
}

static uint32_t append_string(uint32_t pos, const uint8_t* text, uint32_t max) {
    for (uint32_t i = 0; i < max && text[i] && pos < EXPANDED_SIZE - 1; i++) {
        expanded[pos++] = text[i];
    }
    return pos;
}

static uint32_t append_save_name(uint32_t pos) {
    int end = 8;
    while (end > 0 && (uint8_t)z64_file.file_name[end - 1] == 0xDF) end--;
    for (int i = 0; i < end && pos < EXPANDED_SIZE - 1; i++) {
        expanded[pos++] = FILENAME_ENCODING[(uint8_t)z64_file.file_name[i]];
    }
    return pos;
}

static uint32_t append_owner(uint32_t pos) {
    if (PLAYER_NAME_ID == PLAYER_ID) return append_save_name(pos);
    uint16_t player = PLAYER_NAME_ID <= AP_MAX_PLAYER_ID ? PLAYER_NAME_ID : 0;
    return append_string(pos, AP_DISPLAY_NAMES[player], AP_DISPLAY_NAME_LENGTH);
}

static uint32_t expand_message(const uint8_t* raw, uint32_t length) {
    uint32_t out = 0;
    uint8_t outgoing_acquisition = 0, hide_description = 0;
    for (uint32_t i = 0; i < length && out < EXPANDED_SIZE - 5;) {
        uint8_t c = raw[i];
        uint32_t size = code_size(c);
        if (c == 0x02 || i + size > length) break;
        // Keep textbox endings (including event, fade and ocarina controls),
        // but omit follow-up effects and instructions for somebody else's item.
        if (hide_description && c != 0x07 && c != 0x09 && c != 0x0A
                && c != 0x0B && c != 0x0E && c != 0x10) {
            i += size;
            continue;
        }
        if (c == 0x0F) {
            out = append_save_name(out);
        } else if (c == 0xF2) {
            out = append_owner(out);
        } else if (c == 0xF7) {
            if (PLAYER_NAME_ID != PLAYER_ID) {
                out = append_string(out, (uint8_t*)" for ", 5);
                out = append_owner(out);
                outgoing_acquisition = 1;
            }
        } else if (c == 0xF0 && raw[i + 1] == 0xFF) {
            out = append_string(out, (uint8_t*)ap_item_names_get_active_name(), AP_ACTIVE_ITEM_NAME_SIZE - 1);
        } else if (c == 0xF0 && raw[i + 1] == 0xFE) {
            out = append_string(out, (uint8_t*)ap_item_names_get_active_article(), 2);
        } else {
            for (uint32_t j = 0; j < size; j++) expanded[out++] = raw[i + j];
        }
        // F7 is inserted immediately before the acquisition sentence's final
        // punctuation. Names are expanded above, so punctuation in them is safe.
        if (outgoing_acquisition && (c == '!' || c == '.')) hide_description = 1;
        i += size;
    }
    expanded[out++] = 0x02;
    return out;
}

// Unexpanded numeric controls need room for their maximum displayed width.
static uint32_t glyph_count(uint8_t c) {
    switch (c) {
        case 0x16: case 0x17: return 8;
        case 0x18: case 0x1E: return 5;
        case 0x19: case 0xF0: case 0xF1: return 3;
        case 0x1D: return 2;
        case 0x1F: return 5;
        default: return c >= 0x20 && c < 0xF0 ? 1 : 0;
    }
}

static uint32_t token_width(uint8_t c) {
    uint32_t count = glyph_count(c);
    return count == 1 ? AP_MESSAGE_CHAR_WIDTHS[c] : count * AP_MESSAGE_CHAR_WIDTHS['0'];
}

static uint32_t word_width(uint32_t start, uint32_t length) {
    uint32_t width = 0;
    for (uint32_t i = start; i < length;) {
        uint8_t c = expanded[i];
        if (c == ' ' || c == 0x01 || c == 0x04 || c == 0x0C || c == 0x02) break;
        width += token_width(c);
        i += code_size(c);
    }
    return width;
}

typedef struct {
    uint32_t pos, width, line, glyphs, decoded;
    int icon;
    uint8_t color;
    uint8_t instant;
} layout_t;

static void line_break(layout_t* s) {
    if (s->line == 3 || s->glyphs >= 110 || s->decoded >= 176) {
        formatted[s->pos++] = 0x04;
        if (s->instant) formatted[s->pos++] = 0x08;
        s->line = s->glyphs = s->decoded = 0;
        if (s->icon >= 0) {
            formatted[s->pos++] = 0x13;
            formatted[s->pos++] = s->icon;
            s->decoded += 2;
        }
        formatted[s->pos++] = 0x05;
        formatted[s->pos++] = s->color;
        s->decoded += 2;
    } else {
        formatted[s->pos++] = 0x01;
        s->line++;
        s->decoded++;
    }
    s->width = 0;
}

static uint32_t wrap_message(uint32_t length) {
    layout_t s = { 0, 0, 0, 0, 0, -1, 0x40, 0 };
    uint8_t space = 0, start_word = 1;
    for (uint32_t i = 0; i < length && s.pos < RAW_SIZE - 24;) {
        uint8_t c = expanded[i];
        uint32_t size = code_size(c);
        if (c == 0x02) break;
        if (c == ' ') {
            space = s.width != 0;
            start_word = 1;
            i++;
            continue;
        }
        if (c == 0x01) {
            line_break(&s);
            space = 0;
            start_word = 1;
            i++;
            continue;
        }
        if (c == 0x04 || c == 0x0C) {
            for (uint32_t j = 0; j < size; j++) formatted[s.pos++] = expanded[i + j];
            s.width = s.line = s.glyphs = s.decoded = 0;
            space = 0;
            start_word = 1;
            i += size;
            continue;
        }
        if (c == 0x13) s.icon = expanded[i + 1];
        if (c == 0x05) s.color = expanded[i + 1];
        if (c == 0x08 || c == 0x09) s.instant = c == 0x08;
        uint32_t limit = s.icon >= 0 ? ICON_LINE_WIDTH : LINE_WIDTH;
        uint32_t width = token_width(c);
        uint32_t glyphs = glyph_count(c);
        if (glyphs) {
            if (start_word && s.width && s.width + (space ? AP_MESSAGE_CHAR_WIDTHS[' '] : 0)
                    + word_width(i, length) > limit) {
                line_break(&s);
                space = 0;
            }
            start_word = 0;
            if (s.width + (space ? AP_MESSAGE_CHAR_WIDTHS[' '] : 0) + width > limit
                    || s.glyphs + glyphs > 110 || s.decoded + size + glyphs + 4 > 180) {
                // Split names without spaces, too. Respect both the four-line
                // limit and the native decoded-text/glyph texture buffers.
                line_break(&s);
                space = 0;
            }
            if (space) {
                formatted[s.pos++] = ' ';
                s.width += AP_MESSAGE_CHAR_WIDTHS[' '];
                s.decoded++;
                space = 0;
            }
            s.width += width;
            s.glyphs += glyphs;
        }
        if (c == 0x06) s.width += expanded[i + 1] * 8580;
        for (uint32_t j = 0; j < size; j++) formatted[s.pos++] = expanded[i + j];
        s.decoded += size + (glyphs > 1 ? glyphs - 1 : 0);
        i += size;
    }
    formatted[s.pos++] = 0x02;
    return s.pos;
}

// Called by the AP assembly hook after Message_OpenText has loaded the raw
// buffer, before vanilla decoding. Ordinary dialogue is left byte-for-byte intact.
void ap_format_item_message(z64_game_t* play) {
    MessageContext* ctx = &play->msgContext;
    uint8_t* raw = (uint8_t*)ctx->font.msgBuf;
    uint32_t length = ctx->font.msgLength;
    if (length > RAW_SIZE) length = RAW_SIZE;
    uint8_t has_ap_text = 0;
    for (uint32_t i = 0; i < length;) {
        uint8_t c = raw[i];
        uint32_t size = code_size(c);
        if (c == 0x02 || i + size > length) break;
        if (c == 0xF2 || c == 0xF7
                || (c == 0xF0 && (raw[i + 1] == 0xFE || raw[i + 1] == 0xFF))) {
            has_ap_text = 1;
            break;
        }
        i += size;
    }
    if (!has_ap_text) return;
    length = wrap_message(expand_message(raw, length));
    for (uint32_t i = 0; i < length; i++) raw[i] = formatted[i];
    ctx->font.msgLength = ctx->msgLength = length;
}
