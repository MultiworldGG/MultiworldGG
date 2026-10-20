# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_actor_stats.py
from ..data.actor_data import actor_attr_table, actor_param_table, get_actor_attr_key
from ..options import EnemyDifficulty


def get_shuffled_chapter_difficulty(
    enemy_difficulty: int,
    starting_chapter: int,
    random
):
    # Load and reorganize actor param data into different format
    # format example:
    # "00_Goomba": {
    #     "Level": [5,8,10,13,15,18,20,23],
    #     "HP": [2,3,4,5,6,7,8],
    #     "DamageA": [1,2,2,3,3,4,4,5]
    #     "NativeChapter": 1
    # }
    all_enemy_stats = {}

    shuffle_chapter_difficulty = (
        enemy_difficulty == EnemyDifficulty.option_Shuffle_Chapter_Difficulty
    )
    progressive_scaling = (
        enemy_difficulty == EnemyDifficulty.option_Progressive_Scaling
    )

    for param_key, param_value in actor_param_table.items():
        actor_name = param_value[0]
        actor_native_chapter = param_value[3]
        actor_stat_name = param_value[1]
        actor_stat_values = [
            param_value[4],
            param_value[5],
            param_value[6],
            param_value[7],
            param_value[8],
            param_value[9],
            param_value[10],
            param_value[11],
        ]

        if actor_name not in all_enemy_stats:
            all_enemy_stats[actor_name] = {}
        all_enemy_stats[actor_name]["NativeChapter"] = actor_native_chapter
        all_enemy_stats[actor_name][actor_stat_name] = actor_stat_values

    # Randomize chapter order
    chapters_to_shuffle = [1, 2, 3, 4, 5, 6, 7]
    if shuffle_chapter_difficulty:
        random.shuffle(chapters_to_shuffle)

    chapter_dict = {}
    for (old_chapter_number, new_chapter_number) in enumerate(chapters_to_shuffle):
        chapter_dict[old_chapter_number + 1] = new_chapter_number
    # Chapter 8 is never shuffled
    chapter_dict[8] = 8

    if (    starting_chapter != 0
        and chapter_dict[starting_chapter] > 3
    ):
        # Chapter we are starting in is too high of a level: adjust it
        original_chapters = list(chapter_dict.keys())
        random.shuffle(original_chapters)
        for original_chapter in original_chapters:
            if chapter_dict[original_chapter] <= 3:
                swap_chapter = chapter_dict[starting_chapter]
                chapter_dict[starting_chapter] = chapter_dict[original_chapter]
                chapter_dict[original_chapter] = swap_chapter
                break

    new_enemy_stats = []

    for attr_id, attr_value in actor_attr_table.items():
        dbkey = get_actor_attr_key(attr_id)
        actor_name = attr_value[3]
        actor_stat_name = attr_value[4]
        if (  actor_name not in all_enemy_stats
            or actor_stat_name not in all_enemy_stats[actor_name]
            or (    not progressive_scaling
                and not shuffle_chapter_difficulty)
        ):
            # not supposed to be random, so write defaults
            value = attr_value[5]
        else:
            native_chapter = all_enemy_stats[actor_name]["NativeChapter"]
            if native_chapter == -1:
                # Special case for Dojo / Kent
                native_chapter = 1
            value = int(
                all_enemy_stats[actor_name][actor_stat_name][chapter_dict.get(native_chapter) - 1]
            )

        new_enemy_stats.append((dbkey, value))

    return new_enemy_stats, chapter_dict
