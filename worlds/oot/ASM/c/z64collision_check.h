#ifndef Z_COLLISION_CHECK_H
#define Z_COLLISION_CHECK_H

#define COLLISION_CHECK_AT_MAX 50
#define COLLISION_CHECK_AC_MAX 60
#define COLLISION_CHECK_OC_MAX 50
#define COLLISION_CHECK_OC_LINE_MAX 3

#include "stdint.h"
#include "z64_math.h"
// From z64.h
struct z64_actor_t;

typedef struct {
    /* 0x0000 */ int16_t radius;
    /* 0x0002 */ int16_t height;
    /* 0x0004 */ int16_t yShift;
    /* 0x0006 */ z64_xyz_t pos;
} Cylinder16; // size = 0x0C

typedef struct {
    /* 0x00 */ struct z64_actor_t* actor; // Attached actor
    /* 0x04 */ struct z64_actor_t* at; // Actor attached to what it collided with as an AT collider.
    /* 0x08 */ struct z64_actor_t* ac; // Actor attached to what it collided with as an AC collider.
    /* 0x0C */ struct z64_actor_t* oc; // Actor attached to what it collided with as an OC collider.
    /* 0x10 */ uint8_t atFlags; // Information flags for AT collisions.
    /* 0x11 */ uint8_t acFlags; // Information flags for AC collisions.
    /* 0x12 */ uint8_t ocFlags1; // Information flags for OC collisions.
    /* 0x13 */ uint8_t ocFlags2;  // Flags related to which colliders it can OC collide with.
    /* 0x14 */ uint8_t colType; // Determines hitmarks and sound effects during AC collisions.
    /* 0x15 */ uint8_t shape; // JntSph, Cylinder, Tris, or Quad
} Collider; // size = 0x18

typedef struct {
    /* 0x00 */ uint8_t colType; // Determines hitmarks and sound effects during AC collisions.
    /* 0x01 */ uint8_t atFlags; // Information flags for AT collisions.
    /* 0x02 */ uint8_t acFlags; // Information flags for OC collisions.
    /* 0x03 */ uint8_t ocFlags1; // Information flags for OC collisions.
    /* 0x04 */ uint8_t ocFlags2; // Flags related to which colliders it can OC collide with.
    /* 0x05 */ uint8_t shape; // JntSph, Cylinder, Tris, or Quad
} ColliderInit; // size = 0x06

typedef struct {
    /* 0x00 */ uint8_t colType; // Determines hitmarks and sound effects during AC collisions.
    /* 0x01 */ uint8_t atFlags; // Information flags for AT collisions.
    /* 0x02 */ uint8_t acFlags; // Information flags for AC collisions.
    /* 0x03 */ uint8_t ocFlags1; // Information flags for OC collisions.
    /* 0x04 */ uint8_t shape; // JntSph, Cylinder, Tris, or Quad
} ColliderInitType1; // size = 0x05

typedef struct {
    /* 0x00 */ struct z64_actor_t* actor;
    /* 0x04 */ uint8_t atFlags; // Information flags for AT collisions.
    /* 0x05 */ uint8_t acFlags; // Information flags for AC collisions.
    /* 0x06 */ uint8_t ocFlags1; // Information flags for OC collisions.
    /* 0x07 */ uint8_t shape;   // JntSph, Cylinder, Tris, or Quad
} ColliderInitToActor; // size = 0x08

typedef struct {
    /* 0x00 */ uint32_t dmgFlags; // Toucher damage type flags.
    /* 0x04 */ uint8_t effect; // Damage Effect (Knockback, Fire, etc.)
    /* 0x05 */ uint8_t damage; // Damage or Stun Timer
} ColliderTouch; // size = 0x08

typedef struct {
    /* 0x00 */ uint32_t dmgFlags;  // Bumper damage type flags.
    /* 0x04 */ uint8_t effect;  // Damage Effect (Knockback, Fire, etc.)
    /* 0x05 */ uint8_t defense; // Damage Resistance
    /* 0x06 */ z64_xyz_t hitPos; // Point of contact
} ColliderBump; // size = 0x0C

typedef struct {
    /* 0x00 */ uint32_t dmgFlags; // Bumper exclusion mask
    /* 0x04 */ uint8_t effect; // Damage Effect (Knockback, Fire, etc.)
    /* 0x05 */ uint8_t defense; // Damage Resistance
} ColliderBumpInit; // size = 0x08

typedef struct ColliderInfo {
    /* 0x00 */ ColliderTouch toucher; // Damage properties when acting as an AT collider
    /* 0x08 */ ColliderBump bumper; // Damage properties when acting as an AC collider
    /* 0x14 */ uint8_t elemType; // Affects sfx reaction when attacked by Link and hookability. Full purpose unknown.
    /* 0x15 */ uint8_t toucherFlags; // Information flags for AT collisions
    /* 0x16 */ uint8_t bumperFlags; // Information flags for AC collisions
    /* 0x17 */ uint8_t ocElemFlags; // Information flags for OC collisions
    /* 0x18 */ Collider* atHit;                // object touching this element's AT collider
    /* 0x1C */ Collider* acHit;                // object touching this element's AC collider
    /* 0x20 */ struct ColliderInfo* atHitInfo; // element that hit the AT collider
    /* 0x24 */ struct ColliderInfo* acHitInfo; // element that hit the AC collider
} ColliderInfo; // size = 0x28

typedef struct {
    /* 0x00 */ uint8_t elemType; // Affects sfx reaction when attacked by Link and hookability. Full purpose unknown.
    /* 0x04 */ ColliderTouch toucher; // Damage properties when acting as an AT collider
    /* 0x0C */ ColliderBumpInit bumper; // Damage properties when acting as an AC collider
    /* 0x14 */ uint8_t toucherFlags; // Information flags for AT collisions
    /* 0x15 */ uint8_t bumperFlags;  // Information flags for AC collisions
    /* 0x16 */ uint8_t ocElemFlags; // Information flags for OC collisions
} ColliderInfoInit; // size = 0x18

typedef struct {
    /* 0x00 */ Collider base;
    /* 0x18 */ ColliderInfo info;
    /* 0x40 */ Cylinder16 dim;
} ColliderCylinder; // size = 0x4C

typedef struct {
    /* 0x00 */ ColliderInit base;
    /* 0x08 */ ColliderInfoInit info;
    /* 0x20 */ Cylinder16 dim;
} ColliderCylinderInit; // size = 0x2C

typedef struct {
    /* 0x00 */ ColliderInitType1 base;
    /* 0x08 */ ColliderInfoInit info;
    /* 0x20 */ Cylinder16 dim;
} ColliderCylinderInitType1; // size = 0x2C

typedef struct {
    /* 0x00 */ ColliderInitToActor base;
    /* 0x08 */ ColliderInfoInit info;
    /* 0x20 */ Cylinder16 dim;
} ColliderCylinderInitToActor; // size = 0x2C

typedef struct {
    /* 0x00 */ z64_xyzf_t quad[4];
    /* 0x30 */ z64_xyz_t dcMid; // midpoint of vectors d, c
    /* 0x36 */ z64_xyz_t baMid; // midpoint of vectors b, a
    /* 0x3C */ float acDist; // distance to nearest AC collision this frame.
} ColliderQuadDim; // size = 0x40

typedef struct {
    /* 0x00 */ z64_xyzf_t quad[4];
} ColliderQuadDimInit; // size = 0x30

typedef struct {
    /* 0x00 */ ColliderInfo info;
    /* 0x24 */ ColliderQuadDim dim;
} ColliderQuadElement; // size = 0x68

typedef struct {
    /* 0x00 */ Collider base;
    /* 0x18 */ ColliderInfo info;
    /* 0x40 */ ColliderQuadDim dim;
} ColliderQuad; // size = 0x80

typedef struct {
    /* 0x00 */ ColliderInit base;
    /* 0x08 */ ColliderInfoInit info;
    /* 0x20 */ ColliderQuadDimInit dim;
} ColliderQuadInit; // size = 0x50

typedef struct {
    /* 0x00 */ ColliderInitType1 base;
    /* 0x08 */ ColliderInfoInit info;
    /* 0x20 */ ColliderQuadDimInit dim;
} ColliderQuadInitType1; // size = 0x50

typedef enum {
    /* 0  */ COLTYPE_HIT0, // Blue blood, white hitmark
    /* 1  */ COLTYPE_HIT1, // No blood, dust hitmark
    /* 2  */ COLTYPE_HIT2, // Green blood, dust hitmark
    /* 3  */ COLTYPE_HIT3, // No blood, white hitmark
    /* 4  */ COLTYPE_HIT4, // Water burst, no hitmark
    /* 5  */ COLTYPE_HIT5, // No blood, red hitmark
    /* 6  */ COLTYPE_HIT6, // Green blood, white hitmark
    /* 7  */ COLTYPE_HIT7, // Red blood, white hitmark
    /* 8  */ COLTYPE_HIT8, // Blue blood, red hitmark
    /* 9  */ COLTYPE_METAL,
    /* 10 */ COLTYPE_NONE,
    /* 11 */ COLTYPE_WOOD,
    /* 12 */ COLTYPE_HARD,
    /* 13 */ COLTYPE_TREE
} ColliderType;

typedef enum {
    /* 0 */ COLSHAPE_JNTSPH,
    /* 1 */ COLSHAPE_CYLINDER,
    /* 2 */ COLSHAPE_TRIS,
    /* 3 */ COLSHAPE_QUAD,
    /* 4 */ COLSHAPE_INVALID
} ColliderShape;

/**
 * Affects the sound Link's sword makes when hitting it, hookability,
 * and possibly other things. It's definitely not flags, as all checks
 * are == or !=. Will probably need more actors decomped to truly
 * understand what this is.
 */
typedef enum {
    /* 0 */ ELEMTYPE_UNK0,
    /* 1 */ ELEMTYPE_UNK1,
    /* 2 */ ELEMTYPE_UNK2,
    /* 3 */ ELEMTYPE_UNK3,
    /* 4 */ ELEMTYPE_UNK4,
    /* 5 */ ELEMTYPE_UNK5,
    /* 6 */ ELEMTYPE_UNK6,
    /* 7 */ ELEMTYPE_UNK7
} ElementType;

#define AT_NONE 0 // No flags set. Cannot have AT collisions when set as AT
#define AT_ON (1 << 0) // Can have AT collisions when set as AT
#define AT_HIT (1 << 1) // Had an AT collision
#define AT_BOUNCED (1 << 2) // Had an AT collision with an AC_HARD collider
#define AT_TYPE_PLAYER (1 << 3) // Has player-aligned damage
#define AT_TYPE_ENEMY (1 << 4) // Has enemy-aligned damage
#define AT_TYPE_OTHER (1 << 5) // Has non-aligned damage
#define AT_SELF (1 << 6) // Can have AT collisions with colliders attached to the same actor
#define AT_TYPE_ALL (AT_TYPE_PLAYER | AT_TYPE_ENEMY | AT_TYPE_OTHER) // Has all three damage alignments

#define AC_NONE 0 // No flags set. Cannot have AC collisions when set as AC
#define AC_ON (1 << 0) // Can have AC collisions when set as AC
#define AC_HIT (1 << 1) // Had an AC collision
#define AC_HARD (1 << 2) // Causes AT colliders to bounce off it
#define AC_TYPE_PLAYER AT_TYPE_PLAYER // Takes player-aligned damage
#define AC_TYPE_ENEMY AT_TYPE_ENEMY // Takes enemy-aligned damage
#define AC_TYPE_OTHER AT_TYPE_OTHER // Takes non-aligned damage
#define AC_NO_DAMAGE (1 << 6) // Collider does not take damage
#define AC_BOUNCED (1 << 7) // Caused an AT collider to bounce off it
#define AC_TYPE_ALL (AC_TYPE_PLAYER | AC_TYPE_ENEMY | AC_TYPE_OTHER) // Takes damage from all three alignments

#define OC1_NONE 0 // No flags set. Cannot have OC collisions when set as OC
#define OC1_ON (1 << 0) // Can have OC collisions when set as OC
#define OC1_HIT (1 << 1) // Had an OC collision
#define OC1_NO_PUSH (1 << 2) // Does not push other colliders away during OC collisions
#define OC1_TYPE_PLAYER (1 << 3) // Can have OC collisions with OC type player
#define OC1_TYPE_1 (1 << 4) // Can have OC collisions with OC type 1
#define OC1_TYPE_2 (1 << 5) // Can have OC collisions with OC type 2
#define OC1_TYPE_ALL (OC1_TYPE_PLAYER | OC1_TYPE_1 | OC1_TYPE_2) // Can have collisions with all three OC types

#define OC2_NONE 0 // No flags set. Has no OC type
#define OC2_HIT_PLAYER (1 << 0) // Had an OC collision with OC type player
#define OC2_UNK1 (1 << 1) // Prevents OC collisions with OC2_UNK2. Some horses and toki_sword have it.
#define OC2_UNK2 (1 << 2) // Prevents OC collisions with OC2_UNK1. Nothing has it.
#define OC2_TYPE_PLAYER OC1_TYPE_PLAYER // Has OC type player
#define OC2_TYPE_1 OC1_TYPE_1 // Has OC type 1
#define OC2_TYPE_2 OC1_TYPE_2 // Has OC type 2
#define OC2_FIRST_ONLY (1 << 6) // Skips AC checks on elements after the first collision. Only used by Ganon

#define TOUCH_NONE 0 // No flags set. Cannot have AT collisions
#define TOUCH_ON (1 << 0) // Can have AT collisions
#define TOUCH_HIT (1 << 1) // Had an AT collision
#define TOUCH_NEAREST (1 << 2) // If a Quad, only collides with the closest bumper
#define TOUCH_SFX_NORMAL (0 << 3) // Hit sound effect based on AC collider's type
#define TOUCH_SFX_HARD (1 << 3) // Always uses hard deflection sound
#define TOUCH_SFX_WOOD (2 << 3) // Always uses wood deflection sound
#define TOUCH_SFX_NONE (3 << 3) // No hit sound effect
#define TOUCH_AT_HITMARK (1 << 5) // Draw hitmarks for every AT collision
#define TOUCH_DREW_HITMARK (1 << 6) // Already drew hitmark for this frame
#define TOUCH_UNK7 (1 << 7) // Unknown purpose. Used by some enemy quads

#define BUMP_NONE 0 // No flags set. Cannot have AC collisions
#define BUMP_ON (1 << 0) // Can have AC collisions
#define BUMP_HIT (1 << 1) // Had an AC collision
#define BUMP_HOOKABLE (1 << 2) // Can be hooked if actor has hookability flags set.
#define BUMP_NO_AT_INFO (1 << 3) // Does not give its info to the AT collider that hit it.
#define BUMP_NO_DAMAGE (1 << 4) // Does not take damage.
#define BUMP_NO_SWORD_SFX (1 << 5) // Does not have a sound when hit by player-attached AT colliders.
#define BUMP_NO_HITMARK (1 << 6) // Skips hit effects.
#define BUMP_DRAW_HITMARK (1 << 7) // Draw hitmark for AC collision this frame.

#define OCELEM_NONE 0 // No flags set. Cannot have OC collisions
#define OCELEM_ON (1 << 0) // Can have OC collisions
#define OCELEM_HIT (1 << 1) // Had an OC collision
#define OCELEM_UNK3 (1 << 3) // Unknown purpose. Used by Dead Hand element 0 and Dodongo element 5

#define OCLINE_NONE 0 // Did not have an OcLine collision
#define OCLINE_HIT (1 << 0) // Had an OcLine collision

#define DMG_ENTRY(damage, effect) ((damage) | ((effect) << 4))

// These flags are not to be used in code until we figure out how we want to format them. They are only here for reference
#define DMG_DEKU_NUT     (1 << 0x00)
#define DMG_DEKU_STICK   (1 << 0x01)
#define DMG_SLINGSHOT    (1 << 0x02)
#define DMG_EXPLOSIVE    (1 << 0x03)
#define DMG_BOOMERANG    (1 << 0x04)
#define DMG_ARROW_NORMAL (1 << 0x05)
#define DMG_HAMMER_SWING (1 << 0x06)
#define DMG_HOOKSHOT     (1 << 0x07)
#define DMG_SLASH_KOKIRI (1 << 0x08)
#define DMG_SLASH_MASTER (1 << 0x09)
#define DMG_SLASH_GIANT  (1 << 0x0A)
#define DMG_ARROW_FIRE   (1 << 0x0B)
#define DMG_ARROW_ICE    (1 << 0x0C)
#define DMG_ARROW_LIGHT  (1 << 0x0D)
#define DMG_ARROW_UNK1   (1 << 0x0E)
#define DMG_ARROW_UNK2   (1 << 0x0F)
#define DMG_ARROW_UNK3   (1 << 0x10)
#define DMG_MAGIC_FIRE   (1 << 0x11)
#define DMG_MAGIC_ICE    (1 << 0x12)
#define DMG_MAGIC_LIGHT  (1 << 0x13)
#define DMG_SHIELD       (1 << 0x14)
#define DMG_MIR_RAY      (1 << 0x15)
#define DMG_SPIN_KOKIRI  (1 << 0x16)
#define DMG_SPIN_GIANT   (1 << 0x17)
#define DMG_SPIN_MASTER  (1 << 0x18)
#define DMG_JUMP_KOKIRI  (1 << 0x19)
#define DMG_JUMP_GIANT   (1 << 0x1A)
#define DMG_JUMP_MASTER  (1 << 0x1B)
#define DMG_UNKNOWN_1    (1 << 0x1C)
#define DMG_UNBLOCKABLE  (1 << 0x1D)
#define DMG_HAMMER_JUMP  (1 << 0x1E)
#define DMG_UNKNOWN_2    (1 << 0x1F)

#define DMG_SLASH (DMG_SLASH_KOKIRI | DMG_SLASH_MASTER | DMG_SLASH_GIANT)
#define DMG_SPIN_ATTACK (DMG_SPIN_KOKIRI | DMG_SPIN_MASTER | DMG_SPIN_GIANT)
#define DMG_JUMP_SLASH (DMG_JUMP_KOKIRI | DMG_JUMP_MASTER | DMG_JUMP_GIANT)
#define DMG_SWORD (DMG_SLASH | DMG_SPIN_ATTACK | DMG_JUMP_SLASH)
#define DMG_HAMMER (DMG_HAMMER_SWING | DMG_HAMMER_JUMP)
#define DMG_FIRE (DMG_ARROW_FIRE | DMG_MAGIC_FIRE)
#define DMG_ARROW (DMG_ARROW_NORMAL | DMG_ARROW_FIRE | DMG_ARROW_ICE | DMG_ARROW_LIGHT | DMG_ARROW_UNK1 | DMG_ARROW_UNK2 | DMG_ARROW_UNK3)
#define DMG_RANGED (DMG_ARROW | DMG_HOOKSHOT | DMG_SLINGSHOT)
#define DMG_DEFAULT ~(DMG_SHIELD | DMG_MIR_RAY)

#endif
