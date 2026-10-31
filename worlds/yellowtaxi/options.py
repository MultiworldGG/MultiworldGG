import random
from dataclasses import dataclass

from Options import (Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, DeathLink, FreeText,
                     StartInventoryPool, TextChoice, OptionSet, OptionError, OptionCounter)
from .items import TRAPS

class Goal(Choice):
    """
    Which boss is your victory condition.
    """
    display_name = "Goal"

    option_bombeach_boss = 0
    option_tosla_offices_boss = 1
    option_help_maurizio = 2
    #option_moon_boss = 3
    #option_macguffin = 4

    default = option_tosla_offices_boss
    #alias_final_boss = option_moon_boss

class GoalPortalGearPercentage(Range):
    """
    Percentage of Gear items (based on accessible gear locations) needed to access the goal portal.
    """
    display_name = "Goal Portal Gear Percentage"
    range_start = 45
    range_end = 90
    default = 65

class ExtraGearPercentage(Range):
    """
    The percentage of the number of gears past the Goal Portal Gear Percentage that will be added to the item pool.
    Any gears not added will be replaced with random filler.

    If 100 gear locations are available in your seed, and your Goal Portal Gear Percentage is set to 60%:
    100% will add all 40 extra gears to the pool beyond the 60 required, for a total of 100.
    50% will add 20 extra gears to the pool beyond the 60 required, for a total of 80.
    0% will add 0 extra gears to the pool beyond the 60 required, for a total of 60.
    """
    display_name = "Extra Gear Percentage"
    range_start = 0
    range_end = 100
    default = 25

class RemoveGoalPortalLocations(Toggle):
    """
    If true, removes locations from within the goal portal from the pool.
    """

    display_name = "Remove Goal Portal Locations"

class RemovePostGoalPortals(Toggle):
    """
    If true, removes portals that are after your current goal portal.

    Note that the game does not currently support any portals after Morio's Mind, so these will always be removed.
    """

    display_name = "Remove Post-Goal Portals"

class ExpertLevel(Range):
    """
    Difficulty level for location access. Higher level means more difficult locations will get in logic earlier.

    Universal Tracker will by default display 1 expert level above your own as "glitched logic".
    You can increase the level shown by using "/manually_collect Additional Expert Logic Level".
    """
    display_name = "Expert Level"
    range_start = 0
    range_end = 3
    default = 0

class IncludeOutOfBounds(Choice):
    """
    Adds out-of-bounds logic.

    Barely: Adds coins that exist barely out-of-bounds but are collectable by bumping into certain floors/walls.
    Full: Adds logic to fully clip in/out of bounds in various places, depending on expert level. Same as Barely for Expert 0.
    """
    display_name = "Include Out-Of-Bounds"

    option_none = 0
    option_barely = 1
    option_full = 2

    alias_off = option_none
    alias_hidden_coins = option_barely
    alias_on = option_full

    default = option_none

class ExtraDemoCollectables(Toggle):
    """
    Adds demo-exclusive locations. Adds 5 additional gears and 2 additional bunnies.
    The corresponding Rocket level will require all available Morio's Lab Bunnies.
    """

    display_name = "Add Extra Demo Collectables"

class TimeTrialGears(Toggle):
    """
    Adds each individual gear in Time Attacks as a location, and adds the corresponding amount of gears to the pool.
    """

    display_name = "Add Time Attack Gears"

class OpenGrannysIsland(Toggle):
    """
    Opens up Granny's Island so that the main part of the island is available moveless.
    """
    display_name = "Open Granny's Island"

class LockedMoriosLab(Toggle):
    """
    Locks Morio's Lab and adds a "Lab Key" item into the multiworld. Adds a location for talking to Morio in Morio's Room.

    If "Open Granny's Island" is on, you will start outside the locked lab, and if it's off you will start inside the locked lab.
    """
    display_name = "Locked Morio's Lab"

class LockedMoriosWardrobe(Toggle):
    """
    Locks Morio's Wardrobe and adds a "Morio's Wardrobe" item into the multiworld.
    Adds a location for talking to the Mori-O-Tron in Morio's Wardrobe.

    If "Hatsanity" is not disabled, you will require logical access to the wardrobe in order to use hats.
    """
    display_name = "Locked Morio's Wardrobe"

class HatWorldMembership(Toggle):
    """
    Adds a "Hat World Membership" item needed to purchase any hats.
    """
    display_name = "Hat World Membership"

class GymGearsUnlockCondition(Choice):
    """
    How Gym Gears is unlocked.

    Open: Gym Gears entrance is always available in Granny's Island.
    Full Game: Gym Gears entrance will open after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Gym Membership: Gym Gears entrance will be unlocked after receiving "Gym Membership" from the multiworld. Adds a purchasable location from the Ultra Chad in Gym Gears.
    Exclude: Gym Gears entrance is always closed and Gym Gears will not be accessible
    """
    display_name = "Gym Gears Unlock Condition"

    option_open = 0
    option_full_game = 1
    option_shuffle_gym_membership = 2
    option_exclude = 3

    default = option_open
    alias_vanilla = option_open
    alias_unlocked = option_open
    alias_locked = option_shuffle_gym_membership

class FecalMattersUnlockCondition(Choice):
    """
    How Fecal Matters is unlocked.

    Vanilla: Talk to Doggo in Morio's Lab to unlock the house in Granny's Island.
    Open: The house in Granny's Island is always open.
    Full Game: The house in Granny's Island will open after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Doggo: The house in Granny's Island will be unlocked after receiving "Doggo" from the multiworld. Adds a location for talking to Doggo in Morio's Lab.
    Exclude: The house in Granny's Island is always closed and Fecal Matters will not be accessible
    """
    display_name = "Fecal Matters Unlock Condition"

    option_vanilla = -1
    option_open = 0
    option_full_game = 1
    option_shuffle_doggo = 2
    option_exclude = 3

    default = option_shuffle_doggo
    alias_unlocked = option_open
    alias_locked = option_shuffle_doggo

class FlushedAwayUnlockCondition(Choice):
    """
    How Flushed Away is unlocked.
    If set to anything other than "Exclude", an NPC will be added who will take you to the Sewer Island if you have no possible logical path to it.

    Open: The Sewer Entrance in Granny's Island is always open.
    Full Game: The Sewer Entrance in Granny's Island will open after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Sewer Key: The house in Granny's Island will be unlocked after receiving "Sewer Key" from the multiworld. Adds a location for talking to Michele in Flushed Away.
    Exclude: The Sewer Entrance in Granny's Island is always closed and Flushed Away will not be accessible
    """
    display_name = "Flushed Away Unlock Condition"

    option_open = 0
    option_full_game = 1
    option_shuffle_sewer_key = 2
    option_exclude = 3

    default = option_full_game
    alias_default = option_full_game
    alias_vanilla = option_full_game
    alias_unlocked = option_open
    alias_locked = option_shuffle_sewer_key

class PsychoTaxiUnlockCondition(Choice):
    """
    How Psycho Taxi is unlocked.
    At this time, the Psycho Taxi level contains no locations.

    Vanilla: Picking up the Psycho Taxi Cartridge in Arcade Panik will unlock Psycho Taxi.
             Same as Excluded if there's no logical access to Arcade Panik
    Open: Psycho Taxi will always be unlocked.
    Shuffle Cartridge: Adds the Psycho Taxi Cartridge into the item pool and adds a location for picking up the Cartridge in Arcade Panik.
                       If Arcade Panik is not an included level, talking to the Psycho Taxi Arcade Machine will be the location instead.
    Excluded: The Psycho Taxi Arcade Machine will never turn on.
    """

    display_name = "Psycho Taxi Unlock Condition"

    option_vanilla = -1
    option_open = 0
    option_shuffle_cartridge = 2
    option_exclude = 3

    default = option_shuffle_cartridge
    alias_unlocked = option_open
    alias_off = option_exclude

class DreamMachineUnlockCondition(Choice):
    """
    How Morio's Dream Machine is unlocked.
    If Morio's Password is not shuffled and Remove Post-Goal Portals has removed the Morio's Mind Portal, the dream machine will always be disabled.

    Open: The Dream Machine can be activated as soon as it is reached.
    Full Game: The Dream Machine can be activated after receiving Full Game Unlock. Same as Open if Shuffle Full Game is off.
    Shuffle Dream Machine: Adds the Dream Machine into the item pool and adds a location for talking to Morio in Morio's Mind if Morio's Mind is an included level.
    """
    display_name = "Dream Machine Unlock Condition"

    option_open = 0
    option_full_game = 1
    option_shuffle_dream_machine = 2
    #option_exclude = 3

    default = option_full_game
    alias_vanilla = option_full_game
    alias_unlocked = option_open
    alias_locked = option_shuffle_dream_machine

class MoskRocketUnlockCondition(Choice):
    """
    How Mosk's Rocket is unlocked.

    Open: Mosk's Rocket will always appear in Granny's Island
    Shuffle Rocket: Adds the Mosk's Rocket to the item pool and adds a location for defeating the final boss on the Moon.
                    If the Moon is not an included level, or is the goal and Remove Goal Portal locations is enabled, talking to Alien Mosk in Granny's Island will be the location instead.
    Exclude: Mosk's Rocket will never appear.
    """

    display_name = "Mosk's Rocket Unlock Condition"

    #option_default = -1
    option_open = 0
    option_shuffle_rocket = 2
    option_exclude = 3

    default = option_exclude
    #alias_vanilla = option_default
    alias_unlocked = option_open

class LockedTimeTrials(Choice):
    """
    Whether Time Attack TVs are locked behind an item.
    If set to anything but Open, will add locations for completing each Time Attack.

    Open: Time Attack TVs can always be accessed
    Single Item: Adds a "Time Attack Remote" item that is needed to access Time Attack TVs
    Split Items: Adds three specific Time Attack Remote items, each corresponding to an individual Time Attack.
    Progressive Items: Adds three "Progressive Time Attack Remote" items, each one allowing access to the next sequential Time Attack.
    """
    display_name = "Locked Time Attacks"

    option_open = 0
    option_single_item = 1
    option_split_items = 2
    option_progressive_items = 3

    default = option_open
    alias_vanilla = option_open
    alias_unlocked = option_open
    alias_disabled = option_open
    alias_off = option_open
    alias_enabled = option_single_item
    alias_on = option_single_item

class ShuffleGelaToni(DefaultOnToggle):
    """
    Adds the unlock for the Ice Cream Truck Entrance in Granny's Island into the item pool and adds a location for defeating Bomboss in Bombeach.

    If goal is Bomboss and Remove Goal Portal locations is enabled, the location will instead be talking to him in Granny's Island.
    """

    display_name = "Shuffle Gela-Toni"

class ShufflePizzaKing(DefaultOnToggle):
    """
    Adds the unlock for the Pizza Oven Entrance in Granny's Island into the item pool and adds a location for completing Pizza King's quest in Pizza Time.

    If Pizza Time is not an included level, the location will instead be talking to him in Granny's Island.
    """

    display_name = "Shuffle Pizza King"

class ShuffleOrangeSwitch(DefaultOnToggle):
    """
    Adds the Orange Switch into the item pool and adds a location for pressing the Orange Switch in Crash Test Industries.

    If Crash Test Industries is not an included level, talking to Ocra Taxi at the end of Crash again will be the location instead.
    """

    display_name = "Shuffle Orange Switch"

class ShuffleMoriosPassword(DefaultOnToggle):
    """
    Adds Morio's Password into the item pool and adds a location for obtaining the key in Morio's Mind.

    If Morio's Mind is not an included level, talking to Morio in the Dream Machine in Morio's Lab will be the location instead.
    """

    display_name = "Shuffle Morio's Password"

class ShuffleFullGame(DefaultOnToggle):
    """
    Starts the game in "Demo" mode, locking areas of Morio's Lab until a "Full Game Unlock" item is received.
    Adds a location for hitting the true demo wall in Morio's Lab.
    If the Full Game Unlock item is received, passing through where the wall used to be will send the location.

    The mod does not work in the actual demo, you are still required to purchase the full game to play!
    """

    display_name = "Shuffle Full Game Unlock"

class DemoPortalMode(Choice):
    """
    When the game is in the Demo state, which portals should appear. Has no effect if Shuffle Full Game is off.

    Basic: Matches current Steam demo, only containing the first two portals.
    Next Fest: Matches the Next Fest demo, which includes the first three portals.
    Influencers: Matches the demo given to certain influencers, containing the first four portals.
    Open: Portals will not be removed while in demo mode and will solely require gears to unlock.
    """

    display_name = "Demo Portal Mode"

    option_basic = 2
    option_next_fest = 3
    option_influencers = 4
    option_open = -1

    default = option_basic
    alias_vanilla = option_basic
    alias_default = option_basic
    alias_extra = option_next_fest
    alias_extra_influencers = option_influencers

class RandomizeHatPrices(Toggle):
    """
    Whether hat prices should be randomized.
    """
    display_name = "Randomize Hat Prices"

class SortRandomizedPricesBySphere(Toggle):
    """
    When enabled, randomized hat prices will be sorted lowest -> highest on a sphere-by-sphere basis.
    """
    display_name = "Sort Randomized Prices by Sphere"

class MinimumHatPrice(Range):
    """
    Minimum price for randomized hat prices.

    If greater than Maximum, they will be swapped.
    """
    display_name = "Minimum Randomized Hat Price"

    range_start = 0
    range_end = 5000
    default = 0

class MaximumHatPrice(Range):
    """
    Maximum price for randomized hat prices.

    If lower than Minimum, they will be swapped.
    """
    display_name = "Maximum Randomized Hat Price"

    range_start = 0
    range_end = 5000
    default = 1000

class Bunnysanity(Toggle):
    """
    Adds Golden Bunnies as items and locations.
    Items will only be added to the pool if Mosk's Rocket is an included level.
    """

    display_name = "Bunnysanity"

class BunnysanityIncludesAllBunnies(DefaultOnToggle):
    """
    Adds Golden Bunny items for all levels, even levels not included in the current seed.
    Has no effect unless Bunnysanity is enabled and Mosk's Rocket is an included level.
    Will remove filler (and gears if needed) from the pool to compensate for the additional Bunny items.
    """

    display_name = "Bunnysanity Includes All Bunnies"

class Hatsanity(Choice):
    """
    Shuffles Hats into the pool.

    Hatsanity makes one check per purchasable hat.
    Shopsanity makes any individual place a hat can be purchased into a check, including duplicates and "no hat" locations.
    In Shopsanity, extra hats will be added to the pool to compensate for the extra hat slots, regardless of the "Hatsanity Filler Hats" setting
    """
    display_name = "Hatsanity"

    option_disabled = 0
    option_hatsanity = 1
    option_shopsanity = 2

    alias_off = 0

class HatsanityFillerHats(DefaultOnToggle):
    """
    If Hatsanity is not set to disabled, add as many not-available hats as possible to the filler pool before doing random fill.
    """
    display_name = "Hatsanity Filler Hats"

class Checkpointsanity(Toggle):
    """
    Adds checkpoints as locations.
    """

    display_name = "Checkpointsanity"

class Safesanity(Toggle):
    """
    Adds freestanding safes as locations.
    """

    display_name = "Safesanity"

class Chestsanity(Toggle):
    """
    Adds freestanding chests as locations.
    """

    display_name = "Chestsanity"

class ChestsanityPercent(Range):
    """
    What percentage of individual chests will be made into locations if Chestsanity is enabled.
    """
    display_name = "Chestsanity Percent"
    range_start = 1
    range_end = 100
    default = 20

class Coinbagsanity(Toggle):
    """
    Adds freestanding coin bags as locations.
    """

    display_name = "Coinbagsanity"

class CoinbagsanityPercent(Range):
    """
    What percentage of individual coin bags will be made into locations if Coinbagsanity is enabled.
    """
    display_name = "Coinbagsanity Percent"
    range_start = 1
    range_end = 100
    default = 5

class Coinsanity(Toggle):
    """
    Adds freestanding individual coins as locations.
    """

    display_name = "Coinsanity"

class CoinsanityPercent(Range):
    """
    What percentage of individual coins will be made into locations if Coinsanity is enabled.

    In a multiworld, the following restriction is in place:
    If the value is higher than the "multiworld_coinsanity_percentage_cap" in the host.yaml (default: 100), it will be lowered to that value.
    """
    display_name = "Coinsanity Percent"
    range_start = 1
    range_end = 100
    default = 1

class CoinsanityNonFillerCap(Range):
    """
    What percentage of total available coins will be able to be anything other than filler items.

    If your Coinsanity Percent is set to 10 and this is set to 5, half of your rolled coin locations will be forced filler.
    If your Coinsanity Percent is lower than this number, all coins could potentially be progression.

    In a multiworld, the following restriction is in place:
    If the value is higher than the "multiworld_coinsanity_percentage_non_filler_cap" in the host.yaml (default: 5), it will be lowered to that value.
    """
    display_name = "Coinsanity Non-Filler Cap Percentage"
    range_start = 0
    range_end = 100
    default = 5

class Cheesesanity(Toggle):
    """
    Adds cheeses as locations.
    """

    display_name = "Cheesesanity"

class Pizzasanity(Toggle):
    """
    Adds the 5 Corrupted Pizza Slices as locations and items. Has no effect if Pizza Time isn't an included level.
    """

    display_name = "Pizzasanity"

class PizzasanityCount(Range):
    """
    How many Corrupted Pizza Slice items will be added to the multiworld if Pizzasanity is enabled.
    All of these items will be required in order to complete the Pizza King's Quest.
    """
    display_name = "Pizzasanity Count"
    range_start = 1
    range_end = 5
    default = 5

class EarlyMove(Toggle):
    """
    If Flip O' Will Shuffle is enabled, forces either a Progressive Boost or Progressive Jump to local sphere 0.

    Prevents an early BK depending on settings.

    If per-level Flip O' Will randomization is performed, this will be a Hub move.
    """

    display_name = "Early Move"

class ShuffleFlipOWill(Choice):
    """
    Shuffles the Flip O' Will into the item pool as 2 Progressive Boosts and 2 Progressive Jumps.
    Adds 4 corresponding locations by talking to NPCs, 3 PICIs in Morio's Lab and Morio in Morio's Island.

    If set to "Per Level", each level will have its own boost and jump items.
    No additional locations are added, so this will eat into the filler pool and, if needed, gear count.
    """

    display_name = "Flip O' Will Shuffle"

    option_off = 0
    #option_shuffle = 1
    #option_split = 2
    option_global = 3
    option_per_level = 4
    default = option_global
    alias_none = option_off
    alias_on = option_global
    alias_progressive_split = option_global # TODO: Swap alias with main option if adding more options

class AllowTopDownJumps(Toggle):
    """
    Allows you to interrupt the Flip O' Will in top-down sections where you usually aren't allowed to.
    This breaks the level design significantly, but logic will account for this!
    """

    display_name = "Allow Jumping in Top-Down Sections"

class ShuffleSpinAttack(Choice):
    """
    Shuffles the ability to attack using the Flip O' Will into the pool.
    This attack will knock back enemies and break blocks and oil pumps.

    Progressive adds a second spin attack item. When you have both you can break explosive blocks and destroy cars.
    """

    display_name = "Shuffle Spin Attack"

    option_off = 0
    option_shuffle = 1
    option_progressive = 2

    default = option_shuffle
    alias_none = option_off
    alias_false = option_off
    alias_true = option_shuffle
    alias_on = option_shuffle

class ShuffleGlide(Toggle):
    """
    Shuffles the ability to stall in midair by tapping the gas button into the item pool and adds a new location for talking to a PICI in Morio's Lab.

    This item is not logically required for any locations at this time, and as such will be considered "Useful"
    """

    display_name = "Shuffle Glide"

class ShuffleWorldMap(Toggle):
    """
    Shuffles the ability to use the World Map from the pause menu into the item pool and adds a new location for talking to a PICI in Morio's Lab.
    """

    display_name = "Shuffle World Map"

class ShuffleGoldenSpring(DefaultOnToggle):
    """
    Shuffles the Golden Spring into the item pool and adds a new location for defeating the Tosla's Offices boss.

    If Tosla's Offices is not an included level, talking to Morio near the Tosla's Offices Portal will be the location instead.
    """
    display_name = "Shuffle Golden Spring"

class ShuffleGoldenPropeller(DefaultOnToggle):
    """
    Shuffles the Golden Propeller into the item pool and adds a new location for talking to Morio in Ruined Observatory.

    If Ruined Observatory is not an included level, talking to Nick-O-Will near the top of Granny's Island will be the location instead.
    """
    display_name = "Shuffle Golden Propeller"

class ShuffleRat(Toggle):
    """
    Adds Michele the Rat into the item pool and adds a location for talking to Michele in Pizza Time.

    If Pizza Time is not an included level, Michele will instead be found in Granny's Island.
    """

    display_name = "Shuffle Michele the Rat"

class PizzaWheels(Choice):
    """
    Shuffles Pizza Wheels into the item pool and adds a new location for talking to MacPizza in Pizza Time.
    If Pizza Time is not an included level, talking to Chef Pepe in Morio's Lab will be the location instead.

    Pizza Wheels have three modes, corresponding to different item classifications:
    Progression: The cheese on the pizza protects your tires from spikes, allowing you to drive across them safely.
    Useful: Pizza Wheels can only protect you from spikes after receiving the Golden Spring Blueprints. No logic implications.
    Filler: Pizza Wheels are purely cosmetic, and have no effect on gameplay.
    """
    display_name = "Pizza Wheels"

    option_off = 0
    option_progression = 3
    option_useful = 2
    option_filler = 1
    default = option_off
    alias_disabled = option_off

class FunnyFaces(FreeText):
    """
    In your installation folder for Yellow Taxi Goes Vroom, there exists an "Extras" folder containing a "FunnyFaces" subfolder.

    Setting this option will load an image from this folder for both the TV Hat and coins, if available.
    If this is set to anything other than a blank string, you will start with the TV Hat.
    If Hatsanity is set to Shopsanity, a "No Hat" item will replace the TV Hat in the pool, and hats cannot be fully unequipped unless this is found.
    """
    display_name = "Funny Faces"
    default = ""

class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink.
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 5
    default = 1

class RingLink(Toggle):
    """
    Whether your coin gain/loss is linked to other players.
    """
    display_name = "Ring Link"

class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players.
    """
    display_name = "Trap Link"

class TrapLinkUsesWhitelist(Toggle):
    """
    If true, Trap Link will only receive traps that are weighted higher than 0.
    If false, Trap Link can receive any valid trap, including some that are exclusive to Trap Links from other games.
    """
    display_name = "Trap Link Uses Whitelist"

class PurchaseRebatePercent(Range):
    """
    When you die, the coins you lose are added to a secret counter that causes coin bags, chests, and safes to give more money until you are reimbursed.

    This setting allows any in-game purchases to also increment this counter by a % of the cost, allowing you to more easily regain spent coins.
    Note that the counter is saved per-session, restarting the game will result in it being reset to 0!
    """
    display_name = "Purchase Rebate %"
    range_start = 0
    range_end = 100
    default = 25

class EasyAlienMosk(Toggle):
    """
    When fighting Alien Mosk in Tosla's Offices, there are 4 different positions at which a Golden Spring will spawn.
    In all phases except the first, the fight will spawn one Golden Spring at the furthest position from the player.

    When this option is enabled, all four golden springs will spawn on all boss phases instead.
    """

    display_name = "Easy Alien Mosk"

class MoriosMindLaserBehavior(Choice):
    """
    How Morio's Mind Laser behaves.

    The Hat options will disable the laser as long as you are wearing the relevant hat.
    """
    display_name = "Morio's Mind Laser Behavior"
    option_enabled = 0
    option_disabled = 1
    option_morios_brain_hat = 2
    option_inception_top_hat = 3
    option_morios_brain_or_inception_top_hat = 4

    default = option_enabled

class QuickPickups(Toggle):
    """
    When enabled, all collectables will use the quick pickup animation, rather than freezing the player in place.
    """

    display_name = "Quick Pickups"

class TrapFillPercent(Range):
    """
    What percentage of filler items will be replaced by traps.
    """
    display_name = "Trap Fill Percent"
    range_start = 0
    range_end = 100
    default = 0

class TrapDistribution(OptionCounter):
    """
    Specify the weighted chance of rolling individual traps.
    You can use a weight of "0" to disable a trap entirely.
    """
    display_name = "Trap Distribution"
    min = 0
    max = 1000
    valid_keys = frozenset(sorted(TRAPS))
    default = {
        trap: 100
        for trap in sorted(TRAPS)
    }

class ShopHints(Choice):
    """
    When backing out of a shop without purchasing, should a hint be generated and, if so, for what item types?
    """
    display_name = "Shop Hints"

    option_none = 0
    option_progression_only = 3
    option_progression_and_useful = 2
    option_all = 1
    default = option_progression_only
    alias_disabled = option_none
    alias_off = option_none
    alias_progression = option_progression_only
    alias_useful = option_progression_and_useful
    alias_proguseful = option_progression_and_useful
    alias_any = option_all
    alias_on = option_all

class UseSeparateEntrancePools(Toggle):
    """
    If enabled, shuffled levels will be split up into separate pools, and will only be at an entrance from that pool.
    If disabled, any shuffled level can be at any shuffled entrance.
    """
    display_name = "Use Separate Entrance Pools"

class AllowShufflingRemovedLevels(Choice):
    """
    When on, allows levels to be shuffled when they would normally not be included in the game.
    These levels will potentially replace shuffled levels that would normally be included by your settings.
    Note that Time Attacks, Psycho Taxi, and Mosk's Rocket are unaffected by this setting,
    and will be shuffled into the pool if their shuffle settings are enabled regardless of being excluded or not.

    None: Only shuffle levels that would be included by your non-ER options
    Portal Levels Only: Only the Portal levels in Morio's Lab will be potentially shuffled in if not normally included.
    Any: Portal Levels and the three Granny's Island levels will be potentially shuffled in if not normally included.
    """
    display_name = "Allow Shuffling Removed Levels"

    option_none = 0
    option_portal_levels_only = 1
    option_any = 2

    default = option_portal_levels_only

class PortalOrder(Choice):
    """
    Which order portals will appear.

    Vanilla: The default portal level order.
    Internal: Follows the code level #s. Changes the first 4 levels to: Bombeach, Pizza Time, Morio's Home, Arcade Panik
              This order puts more moveless locations early!
    Shuffle: Shuffles portal levels. If "Use Separate Entrance Pools" is true, these will be in their own unique pool.
    """
    display_name = "Portal Order"
    option_vanilla = 0
    option_internal = 1
    option_shuffle = 2

    default = option_vanilla

class ShuffleGrannysLevels(Toggle):
    """
    Whether the three Granny's Island Levels (Gym Gears, Fecal Matters, and Flushed Away) should be shuffled.

    If "Use Separate Entrance Pools" is true, these will be in their own unique pool.
    """
    display_name = "Shuffle Granny's Island Levels"

class ShuffleTimeTrialsEntrances(Toggle):
    """
    Whether the three Time Attacks should have their entrances be shuffled.

    If "Use Separate Entrance Pools" is true, these will be in the "Miscellaneous" pool.
    """
    display_name = "Shuffle Time Attack Entrances"

class ShuffleRocketEntrance(Toggle):
    """
    Whether Mosk's Rocket should have its entrance shuffled.
    If "Mosk's Rocket Unlock Condition" is set to "Exclude", will shuffle the level into the pool, but not the entrance.

    If "Use Separate Entrance Pools" is true, it will be in the "Miscellaneous" pool.
    """
    display_name = "Shuffle Rocket Entrance"

class ShufflePsychoTaxiEntrance(Toggle):
    """
    Whether Psycho Taxi should have its entrance shuffled.
    If "Psycho Taxi Unlock Condition" is set to "Exclude" or to "Default" when Arcade Panik is not an included level,
    will shuffle the level into the pool, but not the entrance.

    If "Use Separate Entrance Pools" is true, it will be in the "Miscellaneous" pool.
    """
    display_name = "Shuffle Psycho Taxi Entrance"

class TaxiSkin(Choice):
    """
    Default taxi skin.

    Custom will load "{FunnyFaces}Taxi.png" from the FunnyFaces Folder, where {FunnyFaces} is the string set for the Funny Faces setting.
    The first time you load into a game, it will export the base taxi texture to this folder as "TestTaxi.png" for copying and editing.
    If the custom taxi skin does not exist, the base skin will be used.
    """
    display_name = "Taxi Skin"
    option_default_yellow = 0
    option_default_green = 1
    option_default_blue = 2
    option_default_purple = 3
    option_default_red = 4
    option_default_random_every_load = 9
    option_default_random_every_flip = 1009

    option_skeleton = 10
    option_skeleton_green = 11
    option_skeleton_blue = 12
    option_skeleton_purple = 13
    option_skeleton_pink = 14
    option_skeleton_light = 15
    option_skeleton_random_every_load = 19
    option_skeleton_random_every_flip = 1019

    option_golden = 20
    option_golden_bright_yellow = 21
    option_golden_blurry = 22
    option_golden_light = 23
    option_golden_orange = 24
    option_golden_random_every_load = 29
    option_golden_random_every_flip = 1029

    option_prototype = 30
    option_prototype_yellow = 31
    option_prototype_green = 32
    option_prototype_blue = 33
    option_prototype_pink = 34
    option_prototype_red = 35
    option_prototype_random_every_load = 39
    option_prototype_random_every_flip = 1039

    option_car_blue = 40
    option_car_green = 41
    option_car_orange = 42
    option_car_pink = 43
    option_car_red = 44
    option_car_white = 45
    option_car_random_every_load = 49
    option_car_random_every_flip = 1049

    option_corrupted_car = 50

    option_grannys_car = 60
    option_grannys_car_corrupted = 61
    option_stars_and_stripes = 62

    option_pink_flames = 70
    option_pink_flames_corrupted = 71

    option_police_car = 80
    option_police_car_corrupted = 81

    option_city_taxi = 90

    option_destroyed = 100

    option_custom = 1000

    option_random_every_load = 999
    option_random_every_flip = 1999

    default = option_default_yellow
    alias_yellow = option_default_yellow
    alias_default = option_default_yellow
    alias_green = option_default_green
    alias_blue = option_default_blue
    alias_purple = option_default_purple
    alias_red = option_default_red
    alias_corrupted = option_corrupted_car
    alias_random_per_load = option_random_every_load
    alias_fully_random = option_random_every_load
    alias_chaos = option_random_every_flip

class GlitchedTaxiSkinColor(TextChoice):
    """
    Sets the color used for the Glitched Taxi Skin.
    Can also be set to a hex color code (e.g. '#FF00DC') for a custom color.
    """
    display_name = "Glitched Taxi Skin Color"
    option_vanilla_orange = "vanilla_orange"
    option_time_attack_green = "time_attack_green"
    #option_time_attack_gold = "time_attack_gold" # Too similar to vanilla to be listed. Can still be inputted though.
    option_red = "red"
    option_cyan = "cyan"
    option_blue = "blue"
    option_darkblue = "darkblue"
    option_lightblue = "lightblue"
    option_purple = "purple"
    option_yellow = "yellow"
    #option_lime = "lime" # Too similar to time attack green to be listed. Can still be inputted though.
    option_fuchsia = "fuchsia"
    option_white = "white"
    option_silver = "silver"
    option_grey = "grey"
    option_black = "black"
    #option_orange = "orange" # Too similar to vanilla to be listed. Can still be inputted though.
    option_brown = "brown"
    option_maroon = "maroon"
    option_green = "green"
    option_olive = "olive"
    option_navy = "navy"
    option_teal = "teal"
    option_aqua = "aqua"
    option_magenta = "magenta"

    default = option_vanilla_orange

    @classmethod
    def from_text(cls, text: str) -> TextChoice:
        # Special Values and HTML colors supported by Unity
        # https://docs.unity3d.com/2020.3/Documentation/ScriptReference/ColorUtility.TryParseHtmlString.html
        if text.lower() in ["red", "cyan", "blue", "darkblue", "lightblue", "purple", "yellow", "lime", "fuchsia",
                            "white", "silver", "grey", "black", "orange", "brown", "maroon", "green", "olive", "navy",
                            "teal", "aqua", "magenta", "vanilla_orange", "time_attack_green", "time_attack_gold"]:
            return cls(text.lower())
        # Interpret "random" as a completely random hex code
        if text.lower() == "random":
            return cls(f"#{random.randbytes(3).hex().upper()}")
        # Check hex color for validity. Allow with or without leading #
        cleaned = text.strip().lstrip("#")
        if len(cleaned) == 6:
            try:
                int(cleaned, 16)
                return cls("#" + cleaned.upper())
            except ValueError:
                pass
        raise OptionError(text + " is not a valid color")

class GearType(Choice):
    """
    Change the appearance of uncollected gears.
    Default will use either Standard or Time Attack depending on if the level is a Time Attack level.
    Inverse will use the opposite (either standard or time attack) as it would in vanilla
    """
    display_name = "Gear Type"
    option_default = 0
    option_inverse = 1
    option_standard = 2
    option_time_attack = 3

class StandardGearColor(TextChoice):
    """
    Sets the color used for uncollected standard gears.
    Default will use either the standard or colorblind material depending on in-game settings.
    Can also be set to a hex color code (e.g. '#E91E63') for a custom color.
    """
    display_name = "Gear Color"
    option_default = "default"
    option_vanilla_green = "vanilla_green"
    option_vanilla_colorblind_blue = "vanilla_colorblind_blue"
    option_red = "red"
    option_cyan = "cyan"
    option_blue = "blue"
    option_darkblue = "darkblue"
    option_lightblue = "lightblue"
    option_purple = "purple"
    option_yellow = "yellow"
    option_lime = "lime"
    option_fuchsia = "fuchsia"
    option_white = "white"
    option_silver = "silver"
    option_grey = "grey"
    option_black = "black"
    option_orange = "orange"
    option_brown = "brown"
    option_maroon = "maroon"
    option_green = "green"
    option_olive = "olive"
    option_navy = "navy"
    option_teal = "teal"
    option_aqua = "aqua"
    option_magenta = "magenta"

    default = option_default

    @classmethod
    def from_text(cls, text: str) -> TextChoice:
        # Special Values and HTML colors supported by Unity
        # https://docs.unity3d.com/2020.3/Documentation/ScriptReference/ColorUtility.TryParseHtmlString.html
        if text.lower() in ["red", "cyan", "blue", "darkblue", "lightblue", "purple", "yellow", "lime", "fuchsia",
                            "white", "silver", "grey", "black", "orange", "brown", "maroon", "green", "olive", "navy",
                            "teal", "aqua", "magenta", "default", "vanilla_green", "vanilla_colorblind_blue"]:
            return cls(text.lower())
        # Interpret "random" as a completely random hex code
        if text.lower() == "random":
            return cls(f"#{random.randbytes(3).hex().upper()}")
        # Check hex color for validity. Allow with or without leading #
        cleaned = text.strip().lstrip("#")
        if len(cleaned) == 6:
            try:
                int(cleaned, 16)
                return cls("#" + cleaned.upper())
            except ValueError:
                pass
        raise OptionError(text + " is not a valid color")

class TimeAttackGearColor(TextChoice):
    """
    Sets the color used for uncollected time attack gears.
    Can also be set to a hex color code (e.g. '#E91E63') for a custom color.
    """
    display_name = "Time Attack Gear Color"
    option_vanilla_green = "vanilla_green"
    option_gold = "gold"
    option_red = "red"
    option_cyan = "cyan"
    option_blue = "blue"
    option_darkblue = "darkblue"
    option_lightblue = "lightblue"
    option_purple = "purple"
    option_yellow = "yellow"
    #option_lime = "lime" # Too similar to standard green to be listed. Can still be inputted though.
    option_fuchsia = "fuchsia"
    option_white = "white"
    option_silver = "silver"
    option_grey = "grey"
    option_black = "black"
    option_orange = "orange"
    option_brown = "brown"
    option_maroon = "maroon"
    option_green = "green"
    option_olive = "olive"
    option_navy = "navy"
    option_teal = "teal"
    option_aqua = "aqua"
    option_magenta = "magenta"

    default = option_vanilla_green

    @classmethod
    def from_text(cls, text: str) -> TextChoice:
        # Special Values and HTML colors supported by Unity
        # https://docs.unity3d.com/2020.3/Documentation/ScriptReference/ColorUtility.TryParseHtmlString.html
        if text.lower() in ["red", "cyan", "blue", "darkblue", "lightblue", "purple", "yellow", "lime", "fuchsia",
                            "white", "silver", "grey", "black", "orange", "brown", "maroon", "green", "olive", "navy",
                            "teal", "aqua", "magenta", "vanilla_green", "gold"]:
            return cls(text.lower())
        # Interpret "random" as a completely random hex code
        if text.lower() == "random":
            return cls(f"#{random.randbytes(3).hex().upper()}")
        # Check hex color for validity. Allow with or without leading #
        cleaned = text.strip().lstrip("#")
        if len(cleaned) == 6:
            try:
                int(cleaned, 16)
                return cls("#" + cleaned.upper())
            except ValueError:
                pass
        raise OptionError(text + " is not a valid color")

class MorioCostume(Choice):
    """
    What costume Morio will wear in the lab.
    Default will wear the relevant seasonal costume he would wear in vanilla as applicable.
    """
    display_name = "Morio Costume"
    option_default = -1
    option_no_costume = 0
    option_halloween = 1
    option_christmas = 2
    option_valentines_day = 3
    option_random_costume_every_load = -2
    option_random_costume_parts_every_load = -3

    default = option_default
    alias_none = option_no_costume
    alias_pumpkin = option_halloween
    alias_santa = option_christmas
    alias_cupid = option_valentines_day
    alias_valentines = option_valentines_day
    alias_random_per_load = option_random_costume_every_load
    alias_fully_random = option_random_costume_parts_every_load

class RandomizeMusic(Choice):
    """
    Whether (and how) music will be randomized.

    Consistent: Shuffles music, everywhere that plays the same song in vanilla will remain consistent with each other.
    Random Every Load: Every time a load happens, the music will be determined at complete random.
    Radio: Songs will play until their loop point, at which point the song will change to a valid random one.
    """
    display_name = "Randomize Music"

    option_off = 0
    option_consistent = 1
    option_random_every_load = 2
    #option_singularity = 3
    option_radio = -1

    alias_random_per_load = option_random_every_load
    alias_fully_random = option_random_every_load

class IncludeTitleAndCreditsMusic(Toggle):
    """
    Whether Randomize Music will include the Title and Credits themes as possible songs.

    Has no effect if Randomize Music is off.
    """
    display_name = "Include Title and Credits Music"

class SeparateBossMusic(Toggle):
    """
    If enabled, bosses will only play boss themes, and no boss themes will play elsewhere.

    Has no effect if Randomize Music is off.
    """
    display_name = "Separate Boss Music"

class RandomizeSkyboxes(Choice):
    """
    Whether (and how) skyboxes will be randomized.

    Consistent: Shuffles skyboxes, everywhere with the same skybox in vanilla will remain consistent with each other.
    Random Every Load: Every time a load happens, the skybox will be determined at complete random.
    """
    display_name = "Randomize Skyboxes"

    option_off = 0
    option_consistent = 1
    option_random_every_load = 2
    #option_singularity = 3

    alias_random_per_load = option_random_every_load
    alias_fully_random = option_random_every_load

class ExcludeBoringSkyboxes(Toggle):
    """
    If enabled, Skyboxes consisting of a single color will not be included in the randomization.

    Has no effect if Randomize Skyboxes is off.
    """
    display_name = "Exclude Boring Skyboxes"

@dataclass
class YellowTaxiOptions(PerGameCommonOptions):
    goal: Goal
    goal_portal_gear_percentage: GoalPortalGearPercentage
    extra_gear_percentage: ExtraGearPercentage
    remove_goal_portal_locations : RemoveGoalPortalLocations
    remove_post_goal_portals : RemovePostGoalPortals
    expert_level: ExpertLevel
    include_out_of_bounds: IncludeOutOfBounds
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty
    ring_link: RingLink
    trap_link: TrapLink
    trap_link_uses_whitelist: TrapLinkUsesWhitelist
    purchase_rebate_percent: PurchaseRebatePercent
    open_grannys_island: OpenGrannysIsland
    locked_morios_lab: LockedMoriosLab
    locked_morios_wardrobe: LockedMoriosWardrobe
    locked_time_trials: LockedTimeTrials
    psycho_taxi_unlock_condition: PsychoTaxiUnlockCondition
    dream_machine_unlock_condition: DreamMachineUnlockCondition
    gym_gears_unlock_condition: GymGearsUnlockCondition
    fecal_matters_unlock_condition: FecalMattersUnlockCondition
    flushed_away_unlock_condition: FlushedAwayUnlockCondition
    rocket_unlock_condition: MoskRocketUnlockCondition
    shuffle_gela_toni: ShuffleGelaToni
    shuffle_pizza_king: ShufflePizzaKing
    shuffle_orange_switch: ShuffleOrangeSwitch
    shuffle_morios_password: ShuffleMoriosPassword
    shuffle_full_game: ShuffleFullGame
    demo_portal_mode: DemoPortalMode
    hat_world_membership: HatWorldMembership
    randomize_hat_prices: RandomizeHatPrices
    sort_randomized_prices_by_sphere: SortRandomizedPricesBySphere
    minimum_hat_price: MinimumHatPrice
    maximum_hat_price: MaximumHatPrice
    bunnysanity: Bunnysanity
    bunnysanity_includes_all_bunnies: BunnysanityIncludesAllBunnies
    hatsanity: Hatsanity
    hatsanity_filler_hats: HatsanityFillerHats
    checkpointsanity: Checkpointsanity
    safesanity: Safesanity
    chestsanity: Chestsanity
    chestsanity_percent: ChestsanityPercent
    coinbagsanity: Coinbagsanity
    coinbagsanity_percent: CoinbagsanityPercent
    coinsanity: Coinsanity
    coinsanity_percent: CoinsanityPercent
    coinsanity_non_filler_cap: CoinsanityNonFillerCap
    cheesesanity: Cheesesanity
    pizzasanity: Pizzasanity
    pizzasanity_count: PizzasanityCount
    early_move: EarlyMove
    shuffle_flip_o_will: ShuffleFlipOWill
    allow_top_down_jumps: AllowTopDownJumps
    shuffle_spin_attack: ShuffleSpinAttack
    shuffle_glide: ShuffleGlide
    shuffle_world_map: ShuffleWorldMap
    shuffle_golden_spring: ShuffleGoldenSpring
    shuffle_golden_propeller: ShuffleGoldenPropeller
    shuffle_rat: ShuffleRat
    pizza_wheels: PizzaWheels
    extra_demo_collectables: ExtraDemoCollectables
    time_trial_gears: TimeTrialGears
    funny_faces: FunnyFaces
    easy_alien_mosk: EasyAlienMosk
    morios_mind_laser_behavior: MoriosMindLaserBehavior
    quick_pickups: QuickPickups
    start_inventory_from_pool: StartInventoryPool
    trap_fill_percent: TrapFillPercent
    trap_distribution: TrapDistribution
    shop_hints: ShopHints
    use_separate_entrance_pools: UseSeparateEntrancePools
    allow_shuffling_removed_levels: AllowShufflingRemovedLevels
    portal_order: PortalOrder
    shuffle_grannys_levels: ShuffleGrannysLevels
    shuffle_time_trial_entrances: ShuffleTimeTrialsEntrances
    shuffle_rocket_entrance: ShuffleRocketEntrance
    shuffle_psycho_taxi_entrance: ShufflePsychoTaxiEntrance
    taxi_skin: TaxiSkin
    glitched_taxi_skin_color: GlitchedTaxiSkinColor
    gear_type: GearType
    standard_gear_color: StandardGearColor
    time_attack_gear_color: TimeAttackGearColor
    morio_costume: MorioCostume
    randomize_music: RandomizeMusic
    include_title_and_credits_music: IncludeTitleAndCreditsMusic
    separate_boss_music: SeparateBossMusic
    randomize_skyboxes: RandomizeSkyboxes
    exclude_boring_skyboxes: ExcludeBoringSkyboxes

# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Location Options",
        [
            ExtraDemoCollectables,
            TimeTrialGears,
            Bunnysanity,
            BunnysanityIncludesAllBunnies,
            Hatsanity,
            HatsanityFillerHats,
            Checkpointsanity,
            Safesanity,
            Chestsanity,
            ChestsanityPercent,
            Coinbagsanity,
            CoinbagsanityPercent,
            Coinsanity,
            CoinsanityPercent,
            Cheesesanity,
            Pizzasanity,
            PizzasanityCount,
        ],
    ),
    OptionGroup(
        "World Options",
        [
            OpenGrannysIsland,
            LockedMoriosLab,
            LockedMoriosWardrobe,
            LockedTimeTrials,
            PsychoTaxiUnlockCondition,
            DreamMachineUnlockCondition,
            GymGearsUnlockCondition,
            FecalMattersUnlockCondition,
            FlushedAwayUnlockCondition,
            MoskRocketUnlockCondition,
            ShuffleGelaToni,
            ShufflePizzaKing,
            ShuffleOrangeSwitch,
            ShuffleMoriosPassword,
            ShuffleFullGame,
            DemoPortalMode,
            HatWorldMembership,
            RandomizeHatPrices,
            SortRandomizedPricesBySphere,
            MinimumHatPrice,
            MaximumHatPrice,
        ],
    ),
    OptionGroup(
        "Ability Randomizer Options",
        [
            EarlyMove,
            ShuffleFlipOWill,
            AllowTopDownJumps,
            ShuffleSpinAttack,
            ShuffleGlide,
            ShuffleGoldenSpring,
            ShuffleGoldenPropeller,
            PizzaWheels,
            ShuffleRat,
            ShuffleWorldMap,
        ],
    ),
    OptionGroup(
        "Entrance Randomization Options",
        [
            UseSeparateEntrancePools,
            AllowShufflingRemovedLevels,
            PortalOrder,
            ShuffleGrannysLevels,
            ShuffleTimeTrialsEntrances,
            ShuffleRocketEntrance,
            ShufflePsychoTaxiEntrance,
        ]
    ),
    OptionGroup(
        "Quality of Life Options",
        [
            QuickPickups,
            ShopHints,
            PurchaseRebatePercent,
            EasyAlienMosk,
            MoriosMindLaserBehavior,
        ],
    ),
    OptionGroup(
        "Trap Options",
        [
            TrapLink,
            TrapLinkUsesWhitelist,
            TrapFillPercent,
            TrapDistribution,
        ],
    ),
    OptionGroup(
        "Cosmetic Options",
        [
            TaxiSkin,
            GlitchedTaxiSkinColor,
            FunnyFaces,
            GearType,
            StandardGearColor,
            TimeAttackGearColor,
            RandomizeMusic,
            IncludeTitleAndCreditsMusic,
            SeparateBossMusic,
            RandomizeSkyboxes,
            ExcludeBoringSkyboxes,
            MorioCostume,
        ],
    ),
    OptionGroup(
        "Advanced Options",
        [
            CoinsanityNonFillerCap,
        ],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    # TODO: Make option presets
}
