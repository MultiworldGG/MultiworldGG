# HITMAN Worlds of Assassination

## What is considered a location check in HITMAN?

The Completion of each Level, as well as the completion of each Level with a rating of "Silent Assassin", "Suit Only" and "Silent Assassin, Suit Only" can each be configured to give a check.

Each target being eliminated can be enabled to give one check.

"Itemsanity" can be enabled to give one check for each different Item picked up while ingame. Only Items that go into the inventory and can be dropped give checks (i.e. Crowbar, Screwdriver), items like keys and collectable information do not. Itemsanity can be set to give one check per item (one check for "Itempickup - Crowbar") or split into one check per item per level ("Itempickup - Paris - Crowbar", "Itempickup - Miami - Crowbar", "Itempickup - Marrakesh - Crowbar" etc.).

"Disguisesanity" can be enabled to give one check for each different Disguise 47 can wear in each level.

## What HITMAN items can appear in other players' worlds?

Every level needs to be unlocked by collecting a corresponding item. 

Any item that can be equipped in the planning screen of a mission is randomised away. This includes all Weapons, Gear, Starting Locations (except the first one in each mission), Agency Pickup Locations (except the first one in each Hitman 1 mission) and Suits.

Players can also choose to shuffle "Item Packages" into the itempool. There is one Item Package for each type of eqquipment (i.e "Poison, Explosive, Tool, Pistol etc.), which when equipped in the Planning screen will add all already recieved items of that type to 47s inventory.

If there are more location checks then items, some items will be added into the itempool multiple times. Using equipment that was recieved multiple times adds that multiple instances of the equippment to 47s inventory, using weapons that were recieved multiple times adds only one weapon but multiple times the ammunition to 47s inventory.  

## What goals can be set for HITMAN
 - **Level Completion**: Chose one level to be the goal level and beat it with a chosen rating (Any, Suit Only, Silent Assassin, Silent assassin - Suit Only, Sniper Assassin)
 - **Contract Collection**: Shuffles a number of "Contract Piece" items into the item pool. They act as McGuffins with no gameplay function, but if a number of them are collected, the slot instantly goals. You can also add more Contract Pieces to the item pool than required.
 - **Contract Collection - Level Completion**: Same as Contract Collection, but if all Contract Pieces are collected, the goal level is unlocked, which has to be beaten with the selected rating.
 - **Number of Completions**: Same as Contract Collection, but all Contract Pieces are placed on Level Completions with a specified rating. 

## FAQ
- Is Deathlink available?
  - Deathlink is not supported for HITMAN because the modding framework that is currently used is not able to make any changes to the gameplay in the level. It can only modify the menus, inventory and contract-setup.
  - There are also no Traps currently for the same reason.
- What locations are included in each option of "Disable Annoying Sanitychecks"?
  - *skip_locations_with_wait_time*
    - Itempickup - Hawks Bay - Wristwatch Alarm
    - Itempickup - Whittleton Creek - Beak Staff
    - Itempickup - Whittleton Creek - Package
    - Itempickup - Whittleton Creek - Remote CX Demo Block
    - Disguise - Mendoza - 47's Signature Suit with Gloves
  - *skip_locations_with_extra_steps*
    - Itempickup - Hawks Bay - Shovel
    - Itempickup - Santa Fortuna - Sacrificial Knife
    - Itempickup - Santa Fortuna - "El Matador"
    - Itempickup - Whittleton Creek - Battle Axe
    - Itempickup - Ambrose Island - Doubloon
    - Itempickup - Ambrose Island - Makeshift Explosive
    - Itempickup - Ambrose Island - Emetic Gas Grenade
    - Itempickup - Ambrose Island - Lethal Poison Vial
    - Itempickup - Isle of Sgail - Sacrificial Knife
    - Itempickup - New York - Goldbar
    - Itempickup - New York - Golden Sawed Off Bartoli 12G
    - Itempickup - Mendoza - 1945 Grand Paladin
    - Itempickup - Mendoza - Hackl 9S Covert
    - Disguise - Mendoza - 47's Signature Suit with Gloves
  - *skip_locations_carried_by_npcs*
    - Itempickup - Paris - Lethal Poison Pill Jar
    - Itempickup - Miami - Cocaine Brick
    - Itempickup - Santa Fortuna - Golden Idol
    - Itempickup - Santa Fortuna - Sacrificial Knife
    - Itempickup - Santa Fortuna - "El Matador"
    - Itempickup - Isle of Sgail - Flash Grenade
    - Itempickup - Isle of Sgail - Botulinum Toxin
    - Itempickup - Isle of Sgail - Bartoli 75S
    - Itempickup - New York - Small Gold Bar
    - Itempickup - New York - Toy Tank
    - Itempickup - New York - Letterbomb Parcel
    - Itempickup - New York - Burial Dagger
    - Itempickup - New York - Imperial Filigree Egg
    - Itempickup - New York - Antique Carved Knife
    - Itempickup - New York - DAK X2
    - Itempickup - New York - Folding Knife
    - Itempickup - New York - Goldbar
    - Itempickup - New York - Golden Sawed Off Bartoli 12G
    - Itempickup - Dubai - Folding Knife
    - Itempickup - Dubai - Lethal Poison Pill Jar
    - Itempickup - Dubai - Hackl 9S Covert
    - Itempickup - Berlin - Lethal Pills
    - Itempickup - Berlin - Modern Lethal Syringe
    - Itempickup - Berlin - Concealable Knife
    - Itempickup - Berlin - ICA Remote Audio Distraction Mk III
  - *skip_locations_requiring_other_items*
    - Itempickup - Miami - Car Bomb
    - Itempickup - Miami - Modern Lethal Syringe
    - Itempickup - Santa Fortuna - Cocaine Souvenir
    - Itempickup - Whittleton Creek - Cigar Box
    - Itempickup - Whittleton Creek - Hatchet
    - Itempickup - Whittleton Creek - Expired Can of Spaghetti Sauce
    - Itempickup - Ambrose Island - Cigar box
    - Itempickup - Ambrose Island - Jarl's Pirate Saber
    - Itempickup - Ambrose Island - Doubloon
    - Itempickup - Ambrose Island - Makeshift Explosives
    - Itempickup - Ambrose Island - Emetic Gas Grenade
    - Itempickup - Ambrose Island - Lethal Poison Vial
    - Itempickup - Isle of Sgail - Hackl 9S Covert
    - Itempickup - Isle of Sgail - Sacrificial Knife
    - Itempickup - Isle of Sgail - Bartoli 75S
    - Itempickup - New York - Small Gold Bar
    - Itempickup - New York - Toy Tank
    - Itempickup - New York - Letterbomb Parcel
    - Itempickup - New York - Burial Dagger
    - Itempickup - New York - Imperial Filigree Egg
    - Itempickup - New York - Antique Carved Knife
    - Itempickup - New York - Gold Idol
    - Itempickup - Haven Island - Folding Knife
    - Itempickup - Haven Island - Jarl's Pirate Saber
    - Itempickup - Haven Island - Doubloon
    - Itempickup - Dartmoor - Banana
    - Itempickup - Mendoza - Sieger AR552 Tactical
    - Itempickup - Mendoza - Cocaine Brick
    - Itempickup - Mendoza - Grapevine
    - Disguise - Mendoza - 47's Signature Suit with Gloves
  - *skip_buried_locations*
    - Itempickup - Whittleton Creek - Cigar Box
    - Itempickup - Whittleton Creek - Hatchet
    - Itempickup - Whittleton Creek - Expired Can of Spaghetti Sauce
    - Itempickup - Ambrose Island - Cigar box
    - Itempickup - Ambrose Island - Jarl's Pirate Saber
    - Itempickup - Ambrose Island - Doubloon
    - Itempickup - Isle of Sgail - Hackl 9S Covert
    - Itempickup - Haven Island - Jarl's Pirate Saber
    - Itempickup - Haven Island - Doubloon
