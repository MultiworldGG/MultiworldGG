from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
important_item_regions: List[Rule] = [
Rule("Menu"), Rule("Conners Comm Device", {Req("IMPIT: Conners Comm Device")}),
Rule("Menu"), Rule("Windshield Glass", {Req("IMPIT: Windshield Glass")}),
Rule("Menu"), Rule("Bobbys Watch", {Req("IMPIT: Bobbys Watch")}),
Rule("Menu"), Rule("Gnarlbranch Sap", {Req("IMPIT: Gnarlbranch Sap")}),
Rule("Menu"), Rule("Legen-dar", {Req("IMPIT: Legen-dar")}),
Rule("Menu"), Rule("Smelly Legen-dar", {Req("IMPIT: Smelly Legen-dar")}),
Rule("Menu"), Rule("Slice of Bread", {Req("IMPIT: Slice of Bread")}),
Rule("Menu"), Rule("Deep Blue Gem", {Req("IMPIT: Deep Blue Gem")}),
Rule("Menu"), Rule("Stuffed Lobster", {Req("IMPIT: Stuffed Lobster", 99)}),
Rule("Menu"), Rule("Gold Nopopotamus Card", {Req("IMPIT: Gold Nopopotamus Card")}),
Rule("Menu"), Rule("Natural Pearl", {Req("IMPIT: Natural Pearl", 10)}),
Rule("Menu"), Rule("White Gold Ore", {Req("IMPIT: White Gold Ore")}),
Rule("Menu"), Rule("Briggss Key", {Req("IMPIT: Briggss Key")}),
# Rule("Menu"), Rule("Fosdykes Key", {Req("IMPIT: Fosdykes Key")}), # after the celeste three
# Rule("Menu"), Rule("Moorehouses Key", {Req("IMPIT: Moorehouses Key")}), # after the celeste three
Rule("Menu"), Rule("Queggas Note", {Req("IMPIT: Queggas Note")}),
Rule("Menu"), Rule("Keycard Lakeside Getaway", {Req("IMPIT: Keycard - Lakeside Getaway")}),
Rule("Menu"), Rule("Ajoas ID Card", {Req("IMPIT: Ajoas ID Card")}),
Rule("Menu"), Rule("Ice Cream Cake", {Req("IMPIT: Ice Cream Cake")}),
Rule("Menu"), Rule("Malyteths Bottle", {Req("IMPIT: Malyteths Bottle")}),
Rule("Menu"), Rule("Nopon Contract", {Req("IMPIT: Nopon Contract", 4)}),
Rule("Menu"), Rule("Nopon Gemstone", {Req("IMPIT: Nopon Gemstone")}),
Rule("Menu"), Rule("Vi Sezhas Bracelet", {Req("IMPIT: Vi Sezhas Bracelet")}),
Rule("Menu"), Rule("Ge Jewhes Dagger", {Req("IMPIT: Ge Jewhes Dagger")}),
Rule("Menu"), Rule("Ringstone", {Req("IMPIT: Ringstone")}),
Rule("Menu"), Rule("Zazazans Package", {Req("IMPIT: Zazazans Package")}),
Rule("Menu"), Rule("Hazardous Container", {Req("IMPIT: Hazardous Container")}),
Rule("Menu"), Rule("Hazardous Fuel Cell", {Req("IMPIT: Hazardous Fuel Cell")}),
Rule("Menu"), Rule("Nios IOU", {Req("IMPIT: Nios IOU")}),
Rule("Menu"), Rule("Sapphire Ring", {Req("IMPIT: Sapphire Ring")}),
Rule("Menu"), Rule("Lumenoa Leaf", {Req("IMPIT: Lumenoa Leaf")}),
Rule("Menu"), Rule("Gorkwa", {Req("IMPIT: Gorkwa")}),
Rule("Menu"), Rule("Runtonams Right Arm", {Req("IMPIT: Runtonams Right Arm")}),
Rule("Menu"), Rule("Troylans Gorkwa Fake", {Req("IMPIT: Troylans Gorkwa Fake")}),
Rule("Menu"), Rule("White Whale Parts", {Req("IMPIT: White Whale Parts", 3)}),
Rule("Menu"), Rule("Ians ID Card", {Req("IMPIT: Ians ID Card")}),
Rule("Menu"), Rule("Nalus Present", {Req("IMPIT: Nalus Present")}),
Rule("Menu"), Rule("Dadapons Sunglasses", {Req("IMPIT: Dadapons Sunglasses")}),
Rule("Menu"), Rule("Dodonga Treaty", {Req("IMPIT: Dodonga Treaty")}),
Rule("Menu"), Rule("Dorian Treaty", {Req("IMPIT: Dorian Treaty")}),
Rule("Menu"), Rule("Wrothian Part", {Req("IMPIT: Wrothian Part", 3)}),
Rule("Menu"), Rule("Med Kit NLA", {Req("IMPIT: Med Kit NLA", 5)}),
Rule("Menu"), Rule("Internment Camp Key", {Req("IMPIT: Internment Camp Key")}),
# Rule("Menu"), Rule("Skell License", {Req("IMPIT: Skell License")}), # after the skell license
# Rule("Menu"), Rule("White Whale Parts_2", {Req("IMPIT: White Whale Parts_2")}), # probably unused
Rule("Menu"), Rule("L-002 Power Cable", {Req("IMPIT: L-002 Power Cable", 3)}),
Rule("Menu"), Rule("Skell License Certificate", {Req("IMPIT: Skell License Certificate", 8)}),
Rule("Menu"), Rule("Tissue Sample", {Req("IMPIT: Tissue Sample")}),
Rule("Menu"), Rule("Mias Comm Device", {Req("IMPIT: Mias Comm Device")}),
Rule("Menu"), Rule("Phosphorus-Tree Seed", {Req("IMPIT: Phosphorus-Tree Seed", 6)}),
Rule("Menu"), Rule("Container Key", {Req("IMPIT: Container Key")}),
Rule("Menu"), Rule("Grenade Pizza", {Req("IMPIT: Grenade Pizza")}),
Rule("Menu"), Rule("Frozen Pizza", {Req("IMPIT: Frozen Pizza")}),
Rule("Menu"), Rule("Ajibas Key", {Req("IMPIT: Ajibas Key")}),
Rule("Menu"), Rule("Mujibas Key", {Req("IMPIT: Mujibas Key")}),
Rule("Menu"), Rule("Dancers Clothes", {Req("IMPIT: Dancers Clothes")}),
Rule("Menu"), Rule("Crimson Tear", {Req("IMPIT: Crimson Tear")}),
Rule("Menu"), Rule("New Weapon Blueprint", {Req("IMPIT: New Weapon Blueprint")}),
Rule("Menu"), Rule("Summoning Goggles", {Req("IMPIT: Summoning Goggles")}),
Rule("Menu"), Rule("Senirapa Water", {Req("IMPIT: Senirapa Water")}),
Rule("Menu"), Rule("Zirtodiamond", {Req("IMPIT: Zirtodiamond")}),
Rule("Menu"), Rule("Golboggas Disk", {Req("IMPIT: Golboggas Disk")}),
Rule("Menu"), Rule("Tykki Sap", {Req("IMPIT: Tykki Sap")}),
Rule("Menu"), Rule("Gray Keycard", {Req("IMPIT: Gray Keycard")}),
Rule("Menu"), Rule("Rectangular Chest", {Req("IMPIT: Rectangular Chest")}),
Rule("Menu"), Rule("Kutas Cargo", {Req("IMPIT: Kutas Cargo")}),
Rule("Menu"), Rule("Aerozium", {Req("IMPIT: Aerozium")}),
Rule("Menu"), Rule("Guardian Etherscale", {Req("IMPIT: Guardian Etherscale")}),
Rule("Menu"), Rule("Mimeosome Left Arm", {Req("IMPIT: Mimeosome Left Arm")}), # affinity mission arms and the men
Rule("Menu"), Rule("L-002 Experimental Plant", {Req("IMPIT: L-002 Experimental Plant")}),
Rule("Menu"), Rule("Reverends Journal", {Req("IMPIT: Reverends Journal")}),
Rule("Menu"), Rule("Flemtide", {Req("IMPIT: Flemtide", 5)}),
Rule("Menu"), Rule("Floatstone Shard", {Req("IMPIT: Floatstone Shard")}),
Rule("Menu"), Rule("Blood-Soaked Beast Fur", {Req("IMPIT: Blood-Soaked Beast Fur")}),
Rule("Menu"), Rule("Laws Pendant", {Req("IMPIT: Laws Pendant")}),
Rule("Menu"), Rule("Three Swords", {Req("IMPIT: Three Swords")}),
Rule("Menu"), Rule("Data Unit FN093", {Req("IMPIT: Data Unit FN093")}),
Rule("Menu"), Rule("Repair Kit", {Req("IMPIT: Repair Kit")}),
Rule("Menu"), Rule("Aganeba Alloy", {Req("IMPIT: Aganeba Alloy")}),
Rule("Menu"), Rule("Cockpit Wreckage", {Req("IMPIT: Cockpit Wreckage")}),
Rule("Menu"), Rule("Engine Wreckage", {Req("IMPIT: Engine Wreckage")}),
Rule("Menu"), Rule("Zu Pharg Wreckage", {Req("IMPIT: Zu Pharg Wreckage", 3)}),
Rule("Menu"), Rule("Data Unit FN094", {Req("IMPIT: Data Unit FN094")}),
# Rule("Menu"), Rule("Mimeosome Head", {Req("IMPIT: Mimeosome Head")}), # obtainable after yelvs partner
# Rule("Menu"), Rule("Mimeosome Torso", {Req("IMPIT: Mimeosome Torso")}), # obtainable after yelvs partner
Rule("Menu"), Rule("Mimeosome Left Leg", {Req("IMPIT: Mimeosome Left Leg")}), # required for yelvs partner. obtainable after arms and the man
Rule("Menu"), Rule("Mimeosome Right Leg", {Req("IMPIT: Mimeosome Right Leg")}), # required for yelvs partner. obtainable after arms and the man
Rule("Menu"), Rule("First Barrier Key", {Req("IMPIT: First Barrier Key")}),
Rule("Menu"), Rule("Cleansing Moss", {Req("IMPIT: Cleansing Moss")}), # basic mission clean and green
Rule("Menu"), Rule("Locket", {Req("IMPIT: Locket")}), # basic mission lost memento
Rule("Menu"), Rule("Star Sand", {Req("IMPIT: Star Sand")}), # basic mission star sand seeker
Rule("Menu"), Rule("Violet Crystal", {Req("IMPIT: Violet Crystal")}), # basic mission a hard pill to swallow
Rule("Menu"), Rule("Emerian Relic", {Req("IMPIT: Emerian Relic")}), # basic mission the emerian battlegrounds
Rule("Menu"), Rule("Missing Drive", {Req("IMPIT: Missing Drive")}), # basic mission data recovery
Rule("Menu"), Rule("Broken Data Probe", {Req("IMPIT: Broken Data Probe")}), # basic mission a probing issue
Rule("Menu"), Rule("Heart Stone", {Req("IMPIT: Heart Stone")}), # basic mission straight from the heart
Rule("Menu"), Rule("Mount Mgando Stone", {Req("IMPIT: Mount Mgando Stone")}), # basic mission mount mgando mineralogy
Rule("Menu"), Rule("Jelly Weeds", {Req("IMPIT: Jelly Weeds")}), # basic mission in a jam
Rule("Menu"), Rule("New-Weapon Remains", {Req("IMPIT: New-Weapon Remains")}), # basic mission test data retrieval
Rule("Menu"), Rule("Sampling Bottle", {Req("IMPIT: Sampling Bottle")}),
Rule("Menu"), Rule("Solar Starship Map", {Req("IMPIT: Solar Starship Map")}), # required for proficiency exam 4, which itself is just a skell license certificate
Rule("Menu"), Rule("Hamburger", {Req("IMPIT: Hamburger")}),
Rule("Menu"), Rule("Hot Dog", {Req("IMPIT: Hot Dog")}),
Rule("Menu"), Rule("Data Unit FN095", {Req("IMPIT: Data Unit FN095")}),
Rule("Menu"), Rule("Data Unit FN096", {Req("IMPIT: Data Unit FN096")}),
Rule("Menu"), Rule("Data Unit FN097", {Req("IMPIT: Data Unit FN097")}),
Rule("Menu"), Rule("Practice Data Probe", {Req("IMPIT: Practice Data Probe")}),
Rule("Menu"), Rule("Toxic Chemical Bomb", {Req("IMPIT: Toxic Chemical Bomb")}),
Rule("Menu"), Rule("Med Kit Ganglion", {Req("IMPIT: Med Kit Ganglion", 5)}),
Rule("Menu"), Rule("Noble Silk", {Req("IMPIT: Noble Silk")}),
Rule("Menu"), Rule("Data Unit FN098", {Req("IMPIT: Data Unit FN098")}),
Rule("Menu"), Rule("Sword of Legendaryness", {Req("IMPIT: Sword of Legendaryness")}),
Rule("Menu"), Rule("Unbreakable Sword", {Req("IMPIT: Unbreakable Sword")}),
# Rule("Menu"), Rule("Voltant", {Req("IMPIT: Voltant")}), # probably not required for the good thief
Rule("Menu"), Rule("Keycard House of Cards", {Req("IMPIT: Keycard - House of Cards")}),
Rule("Menu"), Rule("Troylans Gorkwa", {Req("IMPIT: Troylans Gorkwa")}),
Rule("Menu"), Rule("Traditional Orphean Drug", {Req("IMPIT: Traditional Orphean Drug")}),
Rule("Menu"), Rule("Weapon Test Data", {Req("IMPIT: Weapon Test Data")}),
Rule("Menu"), Rule("Second Barrier Key", {Req("IMPIT: Second Barrier Key")}),
Rule("Menu"), Rule("Third Barrier Key", {Req("IMPIT: Third Barrier Key")}),
Rule("Menu"), Rule("Phogrium", {Req("IMPIT: Phogrium")}),
Rule("Menu"), Rule("Massive Ring Fragment", {Req("IMPIT: Massive Ring Fragment")}),
Rule("Menu"), Rule("Butte Ruin Fragments", {Req("IMPIT: Butte Ruin Fragments")}),
Rule("Menu"), Rule("North Coast Riddle Rock", {Req("IMPIT: North Coast Riddle Rock")}),
Rule("Menu"), Rule("Communication Data", {Req("IMPIT: Communication Data")}),
Rule("Menu"), Rule("Medical Data", {Req("IMPIT: Medical Data")}),
]