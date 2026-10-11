from .items import SongData, ExtraSongData
from .datagen import extractModDataToJson
from typing import Dict, List, Set
from copy import deepcopy
from collections import ChainMap
from BaseClasses import logging
import traceback

class RotNCollections:
    DIAMOND_NAME: str = "Diamond"
    DIAMOND_CODE: int = 1
    logger = logging.getLogger("RotN")

    # Current ID reservations
    # 1 - 59 Diamonds + filler/traps
    # 50 - 999 Rhythm Rifts (Supports max 474 Songs)
    # 1050 - 1999 Remix Rifts
    # 2000 - 2099 Minigames
    # 2100 - 2199 Boss Battles

    SONG_DATA: Dict[str, SongData] = {
        # Base
        "Disco Disaster": SongData(50, "TrackName_DiscoDisaster", "Dove", 1, 4, 9, 19),
        "Elusional": SongData(51, "TrackName_Elusional", "Dove", 1, 6, 10, 18),
        "Visualize Yourself": SongData(52, "TrackName_VisualizeYourself", "Dove", 2, 6, 12, 21),
        "Spookhouse Pop": SongData(53, "TrackName_SpookhousePop", "Dove", 3, 7, 14, 24),
        "Om and On": SongData(54, "TrackName_OmAndOn", "Dove", 3, 7, 14, 24),
        "Morning Dove": SongData(55, "TrackName_MorningDove", "Dove", 3, 6, 13, 25),
        "Heph's Mess": SongData(56, "TrackName_HephsMess", "Heph & Merlin", 2, 5, 15, 24),
        "Amalgamaniac": SongData(57, "TrackName_Amalgamaniac", "Heph & Merlin", 4, 6, 13, 23),
        "Hang Ten Heph": SongData(58, "TrackName_HangTenHeph", "Heph & Merlin", 4, 8, 15, 23),
        "Count Funkula": SongData(59, "TrackName_CountFunkula", "Heph & Merlin", 4, 9, 17, 24),
        "Overthinker": SongData(60, "TrackName_Overthinker", "Heph & Merlin", 3, 8, 14, 27),
        "Cryp2que": SongData(61, "TrackName_Cryp2que", "Nocturna", 3, 11, 15, 25),
        "Nocturning": SongData(62, "TrackName_Nocturning", "Nocturna", 3, 9, 14, 21),
        "Glass Cages (feat. Sarah Hubbard)": SongData(63, "TrackName_GlassCages", "Nocturna", 5, 9, 14, 24),
        "Hallow Queen": SongData(64, "TrackName_HallowQueen", "Nocturna", 4, 11, 15, 17),
        "Progenitor": SongData(65, "TrackName_Progenitor", "Nocturna", 2, 10, 15, 28),
        "Matriarch": SongData(66, "TrackName_Matriarch", "Nocturna", 6, 11, 17, 23),
        "Under the Thunder": SongData(67, "TrackName_Thunder", "Suzu", 3, 12, 16, 27),
        "Eldritch House": SongData(68, "TrackName_EldritchHouse", "Suzu", 5, 10, 13, 24),
        "RAVEVENGE (feat. Aram Zero)": SongData(69, "TrackName_RAVEvenge", "Suzu", 6, 10, 13, 26),
        "Rift Within": SongData(70, "TrackName_RiftWithin", "Suzu", 4, 10, 15, 25),
        "Suzu's Quest": SongData(71, "TrackName_SuzusQuest", "Suzu", 5, 11, 16, 20),
        "Necropolis": SongData(72, "TrackName_Necropolis", "Suzu", 4, 11, 16, 19),
        "Baboosh": SongData(73, "TrackName_Baboosh", "Necrodancer", 6, 12, 17, 27),
        "Necro Sonatica": SongData(74, "TrackName_NecroSonatica", "Necrodancer", 7, 15, 18, 28),
        "She Banned": SongData(75, "TrackName_SheBanned", "Boss Tracks", 4, 11, 17, 20),
        "King's Ruse": SongData(76, "TrackName_KingsRuse", "Boss Tracks", 4, 10, 13, 26),
        "What's in the Box": SongData(77, "TrackName_WhatsInTheBox", "Boss Tracks", 4, 12, 18, 27),
        "Brave the Harvester": SongData(78, "TrackName_BravetheHarvester", "Boss Tracks", 4, 12, 18, 27),
        "Final Fugue": SongData(79, "TrackName_FinalFugue", "Boss Tracks", 7, 13, 19, 26),
        "Twombtorial": SongData(80, "TrackName_Twombtorial", "Boss Tracks", 4, 12, 19, 26),
        "Portamello": SongData(81, "TrackName_Portamello", "Boss Tracks", 4, 9, 16, 19),
        #Meat Boy
        "Slugger's Refrain": SongData(82, "TrackName_DLC_Apricot01", "MeatBoy", 6, 13, 20, 28),
        "Got Danged": SongData(83, "TrackName_DLC_Apricot02", "MeatBoy", 7, 12, 20, 27),
        "Bootus Bleez": SongData(84, "TrackName_DLC_Apricot03", "MeatBoy", 5, 11, 19, 27),
        #Celeste
        "Resurrections (dannyBstyle Remix)": SongData(85, "TrackName_DLC_Banana01", "Celeste", 5, 12, 17, 24),
        "Scattered and Lost": SongData(86, "Scattered and Lost", "Celeste", 4, 8, 16, 25),
        "Reach for the Summit": SongData(87, "Reach for the Summit", "Celeste", 7, 11, 18, 30),
        "Confronting Myself": SongData(88, "Confronting Myself", "Celeste", 6, 9, 17, 26),
        "Resurrections": SongData(89, "Resurrections", "Celeste", 6, 10, 17, 23),
        #Anniversary
        "Crypteque": SongData(90, "Crypteque", "Anniversary", 5, 8, 13, 22),
        "Power Cords": SongData(91, "Power Cords", "Anniversary", 2, 6, 11, 21),
        "Fungal Funk": SongData(92, "Fungal Funk", "Anniversary", 4, 12, 16, 22),
        #Pizza Tower
        "It's Pizza Time!": SongData(93, "It's Pizza Time!", "Pizza Tower", 6, 12, 18, 22),
        "The Death That I Deservioli": SongData(94, "The Death That I Deservioli", "Pizza Tower", 6, 10, 17, 24),
        "Unexpectancy, Pt. 3": SongData(95, "Unexpectancy, Pt. 3", "Pizza Tower", 7, 15, 20, 27),
        "World Wide Noise": SongData(96, "World Wide Noise", "Pizza Tower", 5, 9, 18, 26),
        #Miku
        "Too Real": SongData(97, "Too Real", "Hatsune Miku", 4, 8, 15, 23),
        "M@GICAL☆CURE! LOVE ♥ SHOT!": SongData(98, "M@GICAL☆CURE! LOVE ♥ SHOT!", "Hatsune Miku", 5, 10, 17, 24),
        "Intergalactic Bound": SongData(99, "Intergalactic Bound", "Hatsune Miku", 3, 7, 14, 21),
        "Just 1dB Louder": SongData(100, "Just 1dB Louder", "Hatsune Miku", 4, 10, 17, 24),
        "MikuFiesta": SongData(101, "MikuFiesta", "Hatsune Miku", 3, 8, 15, 22),
        "Radiant Revival": SongData(102, "Radiant Revival", "Hatsune Miku", 4, 6, 15, 21),
        #Hololive
        "REFLECT": SongData(103, "REFLECT", "Hololive", 6, 11, 16, 21),
        "BIBBIDIBA": SongData(104, "BIBBIDIBA", "Hololive", 4, 8, 17, 22),
        "Play Dice!": SongData(105, "Play Dice!", "Hololive", 7, 12, 18, 23),
        "Ahoy!! 我ら宝鐘海賊団☆": SongData(106, "Ahoy!! 我ら宝鐘海賊団☆", "Hololive", 6, 13, 19, 28),
        "Carbonated Love": SongData(107, "Carbonated Love", "Hololive", 5, 9, 14, 21),
        #Everhood
        "Powers Of Destruction": SongData(108, "Powers of Destruction", "Everhood", 6, 10, 13, 19),
        "The Final Battle": SongData(109, "The Final Battle", "Everhood", 5, 9, 15, 20),
        "Feisty Flowers": SongData(110, "Feisty Flowers", "Everhood", 5, 11, 19, 27),
        "Revenge": SongData(111, "Revenge", "Everhood", 5, 11, 19, 27),
        "Why Oh You Are LOVE": SongData(112, "Why Oh You Are LOVE", "Everhood", 5, 14, 20, 28),
        #Monstercat
        "Crab Rave": SongData(113, "Crab Rave", "Monstercat", 5, 9, 16, 24),
        "Final Boss": SongData(114, "Final Boss", "Monstercat", 2, 8, 16, 22),
        "New Game": SongData(115, "New Game", "Monstercat", 5, 10, 17, 23),
        "PLAY": SongData(116, "PLAY", "Monstercat", 5, 10, 15, 25),
        "Waiting For You (feat. Joanna Jones)": SongData(117, "Waiting for you (feat. Joanna Jones)", "Monstercat", 5, 9, 15, 20),
        #Shovel Knight
        "Main Theme": SongData(118, "Main Theme", "Shovel Knight", 4, 9, 17, 24),
        "La Danse Macabre (Lich Yard)": SongData(119, "La Danse Macabre (Lich Yard)", "Shovel Knight", 5, 7, 20, 27),
        "Strike the Earth! (Plains of Passage)": SongData(120, "Strike the Earth! (Plains of Passage)", "Shovel Knight", 2, 8, 16, 27),
        "In the Halls of the Usurper (Pridemoor Keep)": SongData(121, "In the Halls of the Usurper (Pridemoor Keep)", "Shovel Knight", 5, 9, 17, 22),
        "High Above the Land (The Flying Machine)": SongData(122, "High Above the Land (The Flying Machine)", "Shovel Knight", 4, 7, 16, 21),
        "An Underlying Problem (The Lost City)": SongData(123, "An Underlying Problem (The Lost City)", "Shovel Knight", 4, 11, 18, 23),
        #Friday Night Funkin'
        "Dad Battle": SongData(124, "Dad Battle", "Friday Night Funkin'", 4, 10, 16, 21),
        "Blammed": SongData(125, "Blammed", "Friday Night Funkin'", 7, 12, 18, 25),
        "Stress": SongData(126, "Stress", "Friday Night Funkin'", 7, 15, 21, 28),
        "Darnell": SongData(127, "Darnell", "Friday Night Funkin'", 6, 10, 19, 27),
        "Ugh": SongData(128, "Ugh", "Friday Night Funkin'", 5, 12, 17, 24),
        "Senpai": SongData(129, "Senpai", "Friday Night Funkin'", 2, 10, 16, 24),
        #Unbeatable
        "WORN OUT TAPES [tally-ho version]": SongData(130, "WORN OUT TAPES [tally-ho version]", "Free DLC", 5, 12, 16, 25),
        #Rift Anniversary
        "Portabellohead": SongData(131, "Portabellohead", "Anniversary", 3, 8, 13, 18),
        "March of the Profane": SongData(132, "March of the Profane", "Anniversary", 5, 12, 17, 24),
        #Spin Rhythm
        "The Magician": SongData(133, "The Magician", "Free DLC", 4, 12, 17, 25),
        #VA-11 HALL-A
        "Digital Drive": SongData(134, "Digital Drive", "VA-11 HALL-A", 3, 6, 18, 24),
        "Every Day is Night": SongData(135, "Every Day is Night", "VA-11 HALL-A", 3, 8, 14, 22),
        "Drive Me Wild": SongData(136, "Drive Me Wild", "VA-11 HALL-A", 5, 11, 15, 20),
        "YLIAD": SongData(137, "YLIAD", "VA-11 HALL-A", 4, 8, 14, 20),
        "Welcome to VA-11 HALL-A": SongData(138, "Welcome to VA-11 HALL-A", "VA-11 HALL-A", 2, 8, 13, 21),
        #Undertale
        "Spider Dance": SongData(139, "Spider Dance", "Undertale", 2, 6, 13, 18),
        "Hopes and Dreams": SongData(140, "Hopes and Dreams", "Undertale", 3, 9, 15, 19),
        "Death by Glamour": SongData(141, "Death by Glamour", "Undertale", 5, 13, 16, 24),
        "Bergentrückung / Asgore": SongData(142, "Bergentrückung / Asgore", "Undertale", 4, 10, 15, 21),
        "Battle Against a True Hero": SongData(143, "Battle Against a True Hero", "Undertale", 5, 11, 17, 26),
        "MEGALOVANIA": SongData(144, "MEGALOVANIA", "Undertale", 5, 11, 17, 25),
        #Vol 2
        "A Banj After Midnight (feat. M Gewehr)": SongData(145, "A Banj After Midnight (feat. M Gewehr)", "Volume 2", 5, 11, 18, 24),
        "Goo": SongData(146, "Goo", "Volume 2", 4, 11, 17, 23),
        "Phantom Funk (feat. Lawrence Ravagnan)": SongData(147, "Phantom Funk (feat. Lawrence Ravagnan)", "Volume 2", 5, 11, 16, 25),
        "The Showdown Throwdown": SongData(148, "The Showdown Throwdown", "Volume 2", 6, 12, 20, 29),
        "Ultra Creepy": SongData(149, "Ultra Creepy", "Volume 2", 5, 10, 15, 26),
        "Inside": SongData(150, "Inside", "Volume 2", 4, 12, 16, 24),
        #K/DA
        "POP/STARS": SongData(151, "POP/STARS", "K/DA", 4, 11, 17, 24),
        "More": SongData(152, "More", "K/DA", 5, 11, 16, 24),
        "Villain": SongData(153, "Villain", "K/DA", 4, 10, 15, 23),
        "The Baddest": SongData(154, "The Baddest", "K/DA", 5, 10, 19, 25),
        #Among Us
        "Sought (Among Us - Seek Remix)": SongData(155, "Sought (Among Us - Seek Remix)", "Free DLC", 4, 9, 15, 24),
        #Omega Strikers
        "The Girl Who Glitched (Ai.Mi's Theme)": SongData(156, "The Girl Who Glitched (Ai.Mi's Theme)", "Omega Strikers", 3, 11, 16, 23),
        "Thousand Absolutes (Octavia's Theme)": SongData(157, "Thousand Absolutes (Octavia's Theme)", "Omega Strikers", 7, 13, 19, 26),
        "Curtain Call (Finii's Theme)": SongData(158, "Curtain Call (Finii's Theme)", "Omega Strikers", 5, 11, 18, 25),
        "Go Strike! (Juliette's Theme)": SongData(159, "Go Strike! (Juliette's Theme)", "Omega Strikers", 6, 12, 17, 21),
        "Methods of Madness (Kazan's Theme)": SongData(160, "Methods of Madness (Kazan's Theme)", "Omega Strikers", 6, 11, 17, 27),
        # Miku 2
        "Highlight": SongData(161, "Highlight", "Hatsune Miku 2", 5, 11, 17, 23),
        "CONNECT:COMMUNE": SongData(162, "CONNECT:COMMUNE", "Hatsune Miku 2", 6, 12, 17, 23),
        "Artifact": SongData(163, "Artifact", "Hatsune Miku 2", 7, 13, 17, 26),
        "Hello Builder": SongData(164, "Hello Builder", "Hatsune Miku 2", 7, 14, 20, 27),
        "Wonder Style": SongData(165, "Wonder Style", "Hatsune Miku 2", 5, 11, 16, 25),
        "My One and Oni": SongData(166, "My One and Oni", "Hatsune Miku 2", 6, 11, 17, 23),
    }

    EXTRA_DATA: Dict[str, ExtraSongData] = {
        #Minigames
        "A Bit of a Stretch": ExtraSongData(2000, "Minigame", 0),
        "Lunch Rush": ExtraSongData(2003, "Minigame", 0),
        "Voguelike": ExtraSongData(2006, "Minigame", 0),
        "Show Time!": ExtraSongData(2009, "Minigame", 0),
        "Take a Breather": ExtraSongData(2012, "Minigame", 0),
        #Bosses
        "Harmonie": ExtraSongData(2100, "Boss", 0),
        "Deep Blues": ExtraSongData(2103, "Boss", 0),
        "Matron": ExtraSongData(2106, "Boss", 0),
        "Reaper": ExtraSongData(2109, "Boss", 0),
        "The NecroDancer": ExtraSongData(2112, "Boss", 0),
    }

    FREE_SONGS: List[str] = [
        "Resurrections (dannyBstyle Remix)",
        "Too Real",
        "REFLECT",
        "Powers Of Destruction",
        "Main Theme",
        "Dad Battle",
        "YLIAD",
        "Spider Dance",
        "Ultra Creepy",
        "The Girl Who Glitched (Ai.Mi's Theme)",
        "My One and Oni",
    ]

    FREE_PACKS: List[str] = [
        "Dove",
        "Heph & Merlin",
        "Nocturna",
        "Suzu",
        "Necrodancer",
        "Boss Tracks",
        "MeatBoy",
        "Anniversary",
        "Free DLC",
        "Minigame",
        "Boss",
        "Workshop",
        "Local"
    ]

    DLC_PACKS: List[str] = [
        "All",
        "Celeste",
        "Pizza Tower",
        "Hatsune Miku",
        "Hololive",
        "Everhood",
        "Monstercat",
        "Shovel Knight",
        "Friday Night Funkin'",
        "VA-11 HALL-A",
        "Undertale",
        "Volume 2",
        "K/DA",
        "Omega Strikers",
        "Hatsune Miku 2",
    ]

    DLC_SONGS: List[str] = []
    for name, data in SONG_DATA.items():
        if data.DLC not in FREE_PACKS:
            DLC_SONGS.append(name)

    DLC: List[str] = [*DLC_PACKS, *DLC_SONGS]

    song_locations: Dict[str, int] = {}
    song_items: Dict[str, SongData] = {}

    filler_items: Dict[str, int] = {
        "Apple": 2,
        "Cheese": 3,
        "Chicken": 4,
        "Ham": 5,
        "Vibe Charge": 6,
    }

    filler_weights: Dict[str, int] = {
        "Apple": 10,
        "Cheese": 7,
        "Chicken": 4,
        "Ham": 1,
        "Vibe Charge": 5,
    }

    item_names_to_id: ChainMap = ChainMap({}, filler_items)
    location_names_to_id: ChainMap = ChainMap(song_locations)

    modId_to_name: Dict[str, str] = {}

    def __init__(self) -> None:
        self.item_names_to_id[self.DIAMOND_NAME] = self.DIAMOND_CODE

        mod_data = extractModDataToJson()

        self.mod_remaps: dict[int, dict[str, list]] = {}

        if mod_data:
            seen_mod_song_ids = set()
            seen_mod_item_ids = set()

            for slot_index, data_dict in enumerate(mod_data):
                for song_name, dict_data in data_dict.items():
                    try:
                        data = SongData(int(dict_data["code"]), dict_data["song_id"], dict_data["DLC"], int(dict_data["diff_easy"]) if dict_data["diff_easy"] else None, int(dict_data["diff_medium"]) if dict_data["diff_medium"] else  None, 
                                        int(dict_data["diff_hard"]) if dict_data["diff_hard"] else  None, int(dict_data["diff_impossible"]) if dict_data["diff_impossible"] else  None, "Custom")
                        if not isinstance(song_name, str) or not isinstance(data, SongData):
                            self.logger.warning(f"Skipping {song_name}")
                            continue

                        if data.DLC == "Local":
                            new_code = data.code + 5000 + (1000 * slot_index)
                            data = SongData(new_code, data.song_id, data.DLC, data.diff_easy, data.diff_medium, data.diff_hard, data.diff_impossible, "Custom")
                            self.mod_remaps[data.song_id] = {}
                            self.mod_remaps[data.song_id][song_name] = [new_code, new_code + 1]

                        if song_name in self.song_items:
                            self.logger.warning(f"{song_name} previously mapped to base ID, skipping")
                            continue

                        song_id = data.song_id

                        if song_id in seen_mod_song_ids:
                            if song_id in self.mod_remaps and song_name in self.mod_remaps[song_id]:
                                self.logger.warning(f"{song_name} already remapped to {self.mod_remaps[song_id][song_name]}")
                                continue

                            resolve = {i for i in range(song_id + 2, song_id + 10)}
                            resolve -= seen_mod_song_ids
                            new_slots = sorted(resolve)[0:2]

                            if len(new_slots) != 2:
                                raise Exception(f"Could not remap conflict of {song_name} (out of slots)\n"
                                                    f"{self.mod_remaps[song_id]}")
                            self.logger.warning(f"Remapped {song_name} to {new_slots}")

                            data.code = new_slots[0]
                            seen_mod_item_ids.update(new_slots)

                            self.mod_remaps.setdefault(song_id, {})
                            self.mod_remaps[song_id] = {}
                            self.mod_remaps[song_id][song_name] = new_slots

                        seen_mod_song_ids.add(data.code)
                        seen_mod_song_ids.add(data.code + 1)

                        self.song_items[song_name] = data
                        self.song_locations[f"{song_name}-0"] = data.code
                        self.song_locations[f"{song_name}-1"] = data.code + 1
                        self.modId_to_name[song_id] = song_name
                    except Exception as e:
                        self.logger.error(f"RotN Song Import Error: {song_name} is invalid, skipping song.\n{traceback.format_exc()}")

        for key, data in self.SONG_DATA.items():
            self.song_items[key] = data
            self.song_items[key + " (Remix)"] = SongData(data.code + 1000, data.song_id, data.DLC, data.diff_easy, data.diff_medium, data.diff_hard, data.diff_impossible, "Remix")

        for key, data in self.EXTRA_DATA.items():
            self.song_items[key] = SongData(data.code, key, data.DLC, 1, 0, 0, 0, data.DLC)
            self.song_items[key + " (Medium)"] = SongData(data.code + 1, key, data.DLC, 0, 1, 0, 0, data.DLC)
            self.song_items[key + " (Hard)"] = SongData(data.code + 2, key, data.DLC, 0, 0, 1, 0, data.DLC)

        self.item_names_to_id.update({name: data.code for name, data in self.song_items.items()})

        location_id_index = 1
        for name in self.SONG_DATA.keys():
            self.song_locations[f"{name}-0"] = location_id_index 
            self.song_locations[f"{name}-1"] = location_id_index + 1
            self.song_locations[f"{name} (Remix)-0"] = location_id_index + 1000
            self.song_locations[f"{name} (Remix)-1"] = location_id_index + 1001
            location_id_index += 2

        location_id_index = 2000
        for name in self.EXTRA_DATA.keys():
            self.song_locations[f"{name}-0"] = location_id_index 
            self.song_locations[f"{name}-1"] = location_id_index + 1
            self.song_locations[f"{name} (Medium)-0"] = location_id_index + 2
            self.song_locations[f"{name} (Medium)-1"] = location_id_index + 3
            self.song_locations[f"{name} (Hard)-0"] = location_id_index + 4
            self.song_locations[f"{name} (Hard)-1"] = location_id_index + 5
            location_id_index += 6

    def getSongsWithSettings(self, options, diff_lower: int, diff_higher:int, mod_data: Dict) -> List[str]:
        dlc_songs = options.dlc_songs
        filtered_list = []

        for key, data in self.song_items.items():
            if data.DLC == "Minigame":
                if options.include_minigames == 1 and data.diff_easy == 1:
                    filtered_list.append(key)
                elif options.include_minigames == 2 and data.diff_easy == 0:
                    filtered_list.append(key)
                continue

            if data.DLC == "Boss":
                if options.include_boss_battle == 1 and data.diff_easy == 1:
                    filtered_list.append(key)
                elif options.include_boss_battle == 2 and data.diff_easy == 0:
                    filtered_list.append(key)
                continue
            
            if data.type == "Remix" and not options.include_remix:
                continue

            # Skip modded songs not meant for current player
            if (data.DLC == "Workshop" or data.DLC == "Local") and key not in mod_data.keys():
                continue

            if not self.songMatchesDlcFilter(data, dlc_songs):
                continue

            if data.diff_easy != None and "Easy" in options.difficulty_option and diff_lower <= data.diff_easy <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_medium != None and "Medium" in options.difficulty_option and diff_lower <= data.diff_medium <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_hard != None and "Hard" in options.difficulty_option and diff_lower <= data.diff_hard <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_impossible != None and "Impossible" in options.difficulty_option and diff_lower <= data.diff_impossible <= diff_higher:
                filtered_list.append(key)
                continue

        return filtered_list
    
    def songMatchesDlcFilter(self, song: SongData, dlc_songs: Set[str]) -> bool:
        if "All" in dlc_songs:
            return True

        if song.DLC in self.FREE_PACKS:
            return True

        if song.DLC in dlc_songs or song.song_id in dlc_songs:
            return True

        return False

    groups = {
        "Rhythm Rift": [],
        "Remix Rift": [],
        "Minigame": [],
        "Boss Battle": [],
        "Vanilla": [],
        "Workshop": [],
        "Local": [],
        "Base Songs": [],
    }

    base_dlc = ["Dove", "Heph & Merlin", "Nocturna", "Suzu", "Necrodancer", "Boss Tracks"]

    for group in FREE_PACKS:
        if group == "Boss":
            continue
        groups[group] = []

    for group in DLC_PACKS:
        if group == "All":
            continue
        groups[group] = []
    
    def getItemNameGroups(self) -> Dict[str, str]:
        newGroup = deepcopy(self.groups)
        
        for name, data in self.song_items.items():
            if data.type == "Rift":
                newGroup["Rhythm Rift"].append(name)
            elif data.type == "Remix":
                newGroup["Remix Rift"].append(name)
            elif data.type == "Minigame":
                newGroup["Minigame"].append(name)
                continue
            elif data.type == "Boss":
                newGroup["Boss Battle"].append(name)
                continue

            if data.type == "Local":
                newGroup["Local"].append(name)
            elif data.type == "Workshop":
                newGroup["Workshop"].append(name)
            else:
                newGroup["Vanilla"].append(name)

            if name in self.FREE_SONGS:
                newGroup["Free DLC"].append(name)

            if data.DLC in self.base_dlc:
                newGroup["Base Songs"].append(name)

            newGroup[data.DLC].append(name)

        return newGroup

    def getLocationNameGroups(self) -> Dict[str, str]:
        newGroup = deepcopy(self.groups)

        for name, _ in self.song_locations.items():
            data = self.song_items[name[:len(name)-2]]

            if data.type == "Rift":
                newGroup["Rhythm Rift"].append(name)
            elif data.type == "Remix":
                newGroup["Remix Rift"].append(name)
            elif data.type == "Minigame":
                newGroup["Minigame"].append(name)
                continue
            elif data.type == "Boss":
                newGroup["Boss Battle"].append(name)
                continue

            if data.type == "Local":
                newGroup["Local"].append(name)
            elif data.type == "Workshop":
                newGroup["Workshop"].append(name)
            else:
                newGroup["Vanilla"].append(name)

            if name in self.FREE_SONGS:
                newGroup["Free DLC"].append(name)

            if data.DLC in self.base_dlc:
                newGroup["Base Songs"].append(name)

            newGroup[data.DLC].append(name)

        return newGroup