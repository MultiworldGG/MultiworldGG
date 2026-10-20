from ..data.actor_data import actor_table
from ..data.formations_meta import (
    front_row_enemies,
    chapter_battle_mapping,
    dont_randomize_formations,
    dont_randomize_enemies,
    special_random_formations,
    random_actor_vars,
    gulpit_rocks,
    flying_enemies,
    battlestage_ceilings,
    battlestage_ceiling_formations,
    ceiling_enemies,
)


def _get_random_formationsize(
    chapter_difficulty:int,
    do_progressive_scaling:bool,
    random,
):
    """
    Choose the size of the formation from 1-4. This is a function of
    chapter difficulty, with later chapters having a higher likelihood for
    more enemies.
    """

    # Setup formation size chances:
    # formations in vanilla game
    #              enemy count
    #                   1       2       3       4
    # chapter  0        25%     60%     15%     0%
    # chapter  1        15%     55%     20%     10%
    # chapter  2        10%     45%     30%     15%
    # chapter  3        10%     35%     35%     20%
    # chapter  4        5%      35%     35%     25%
    # chapter  5        0%      35%     40%     25%
    # chapter  6        0%      25%     45%     30%
    # chapter  7        0%      15%     55%     30%
    # chapter  8        0%      10%     50%     40%
    if do_progressive_scaling:
        # during prog scaling always do 3/4 enemies, since the rom itself
        # deletes an enemy if scale is low, resulting in 2/3
        size_chances = {
            0: [ 0, 0, 60, 40],
            1: [ 0, 0, 60, 40],
            2: [ 0, 0, 60, 40],
            3: [ 0, 0, 60, 40],
            4: [ 0, 0, 60, 40],
            5: [ 0, 0, 60, 40],
            6: [ 0, 0, 60, 40],
            7: [ 0, 0, 60, 40],
            8: [ 0, 0, 60, 40],
        }
    else:
        size_chances = {
            0: [25, 60, 15,  0],
            1: [15, 55, 20, 10],
            2: [10, 45, 30, 15],
            3: [10, 35, 35, 20],
            4: [ 5, 35, 35, 25],
            5: [ 0, 35, 40, 25],
            6: [ 0, 25, 45, 30],
            7: [ 0, 15, 55, 30],
            8: [ 0, 10, 50, 40],
        }

    rnd_value = random.random() * 100
    probability_count = 0
    for (size, size_probability) in enumerate(size_chances[chapter_difficulty]):
        probability_count += size_probability
        if rnd_value <= probability_count:
            rnd_number_of_enemies = size + 1
            break

    return rnd_number_of_enemies


def _get_new_formation(
    actor_pointers:dict,
    area_id:str,
    formation_id:str,
    enemylist:list,
    random
):
    formation = []

    int_area_id = int(area_id, 16)
    int_formation_id = int(formation_id, 16)

    # Setup enemy formation file occupancy:
    # The number of enemies determines the 'shape' of the formation -- which
    # of the four files are occupied by an enemy.
    #              file a  file b  file c  file d
    # # enemies  1                   x
    #            2           x       x
    #            3           x       x       x
    #            4   x       x       x       x
    enemycount_occupancy_map = {
        1: [2],
        2: [1,2],
        3: [1,2,3],
        4: [0,1,2,3]
    }

    gulpit_in_formation = ("1D_Gulpit" in enemylist)

    if gulpit_in_formation:
        cur_turn_order = 0x14
    else:
        cur_turn_order = 0x0A

    for (i, enemy_pos) in enumerate(enemycount_occupancy_map[len(enemylist)]):
        # formation setup on example:
        # -> 0000010A 8021B0AC 00000000 00000000
        # word 1:
        # battleID:position:turn order
        # 0000     01       0A
        # word 2:
        # enemy pointer:
        # 8021B0AC
        # word 3:
        # posX:poxY
        # 0000 0000
        # word 4:
        # posZ:var0:var1
        # 0000 00   00
        current_enemy = enemylist[i]

        enemy_on_ceiling = False
        battle_string = f"{area_id}-{formation_id}"
        if current_enemy in ceiling_enemies:
            for stage, battle_list in battlestage_ceiling_formations.items():
                if battle_string in battle_list:
                    # If enemy can be stuck to ceiling, do so
                    enemy_on_ceiling = True
                    cur_stage = stage
                    break

        # Each enemy has four home positions (one in each file), usually
        # either 0/1/2/3 (ground) or 4/5/6/7 (flying), but certain
        # enemies on certain stages can be attached to the ceiling instead.
        actual_enemy_pos = enemy_pos
        if enemy_on_ceiling:
            actual_enemy_pos = 0xFF
        elif current_enemy in flying_enemies:
            actual_enemy_pos += 4

        formation_word_1 = (
            (int_area_id << 24)
            | (int_formation_id << 16)
            | (actual_enemy_pos << 8)
            | cur_turn_order
        )
        formation.append(formation_word_1)

        formation_word_2 = actor_pointers.get(current_enemy)
        formation.append(formation_word_2)

        # If the current battle map has a usable ceiling and we have enemies
        # that can roost on the ceiling, put them there
        formation_word_3 = 0
        xpos = 0
        ypos = 0
        zpos = 0
        if enemy_on_ceiling:
            xpos_per_file = [0xF, 0x37, 0x5F, 0x87] # static 15, 55, 95, 135
            xpos = xpos_per_file[enemy_pos]

            ypos = battlestage_ceilings.get(cur_stage)

            zpos = 0xFFDB # static -25

            formation_word_3 = (xpos << 16) | ypos
        formation.append(formation_word_3)

        # Choose actor vars if applicable.
        # (certain enemies may have randomized initial values for their
        # actor values (ex: spear guy holding spear upward or forward))
        actor_var0 = 0
        actor_var1 = 0
        if current_enemy in random_actor_vars:
            if "Var0" in random_actor_vars[current_enemy]:
                if current_enemy == "0B_BuzzyBeetle":
                    if enemy_on_ceiling:
                        actor_var0 = 1
                else:
                    actor_var0 = random.choice(random_actor_vars[current_enemy]["Var0"])
            if "Var1" in random_actor_vars[current_enemy]:
                actor_var1 = random.choice(random_actor_vars[current_enemy]["Var1"])
        elif current_enemy == "14_SpearGuy":
            # first spearguy points spear forward, all others up
            actor_var0 = 0 if i == 0 else 1
        formation_word_4 = (zpos << 16) | (actor_var0 << 8) | actor_var1
        formation.append(formation_word_4)

        cur_turn_order -= 1

    # And if an enemy is a Gulpit, spawn a bunch of rocks in too.
    # They always have the same number and positions.
    if gulpit_in_formation:
        for i, rocks_hex in enumerate(gulpit_rocks):
            updated_rocks_hex = rocks_hex
            # Insert area id and battle id into each rock's first word
            if i % 4 == 0:
                updated_rocks_hex = (
                    (int_area_id << 24)
                    | (int_formation_id << 16)
                    | rocks_hex
                )
            formation.append(updated_rocks_hex)

    return formation


def _get_new_special_formation(
    actor_pointers:dict,
    area_id:str,
    formation_id:str,
    chapter_difficulty:int,
    do_progressive_scaling:bool,
    available_enemies:list,
    random
):
    special_formation = []

    battle_id = f"{area_id}-{formation_id}"

    if battle_id == "06-17":
        # Billblaster x3 -> add one extra random enemy
        cur_enemylist = ["06_BillBlaster", "06_BillBlaster", "06_BillBlaster"]
        max_number_of_enemies = 4
    elif battle_id == "0B-07":
        # StoneChomp x2 -> add one extra random enemy
        cur_enemylist = ["0B_StoneChomp", "0B_StoneChomp"]
        available_enemies.remove("0B_Swooper")
        max_number_of_enemies = 3
    elif battle_id == "18-1C":
        # AmazyDayzee -> add one extra random enemy
        cur_enemylist = ["18_AmazyDayzee"]
        max_number_of_enemies = 2
    elif battle_id == "25-02":
        # BombshellBlaster x2 -> add one extra random enemy
        cur_enemylist = ["25_BombshellBlaster", "25_BombshellBlaster"]
        max_number_of_enemies = 3
    elif battle_id == "25-03":
        # BombshellBlaster x2 + Koopatrol -> replace Koopatrol with random enemy
        cur_enemylist = ["25_BombshellBlaster", "25_BombshellBlaster"]
        max_number_of_enemies = 3
    elif battle_id == "25-04":
        # BombshellBlaster x2 + MagiKoopa-> replace Koopatrol with random enemy
        cur_enemylist = ["25_BombshellBlaster", "25_BombshellBlaster"]
        max_number_of_enemies = 3
    else:
        raise(KeyError)

    base_number_of_enemies = len(cur_enemylist)
    while True:
        if battle_id == "18-1C":
            rnd_number_of_enemies = 2
        rnd_number_of_enemies = _get_random_formationsize(
            chapter_difficulty,
            do_progressive_scaling,
            random
        )
        if rnd_number_of_enemies >= base_number_of_enemies:
            break
    if rnd_number_of_enemies > max_number_of_enemies:
        rnd_number_of_enemies = max_number_of_enemies
    while rnd_number_of_enemies > len(cur_enemylist):
        cur_enemylist.append(random.choice(available_enemies))

    special_formation = _get_new_formation(
        actor_pointers,
        area_id,
        formation_id,
        cur_enemylist,
        random
    )

    return special_formation


def get_random_formations(
    chapter_changes:dict,
    do_progressive_scaling:bool,
    random
):
    battle_formations = []

    unused_mediguys = [
        "14_MediGuy",
        "16_MediGuy",
        "18_MediGuy",
    ]

    # Fetch dict of actors and their ROM pointers
    actor_pointers = actor_table.copy()
    actor_areas = {}
    for name, pointer in actor_pointers.items():
        # Build list of areas the formations fall into. This requires the actor
        # names to be prefixed by the area byte, i.e. "06_KoopaTroopa"
        area_id = name[:2]
        if not area_id in actor_areas:
            actor_areas[area_id] = []
        if not name in actor_areas[area_id]:
            # Only allow unused MediGuys during ProgressiveScaling
            if (   do_progressive_scaling
                or not name in unused_mediguys
            ):
                actor_areas[area_id].append(name)

    # Loop over all battle formation to be randomized
    for battle, front_row_enemy in front_row_enemies.items():
        #NYI if formation in vanilla_used_battles:
        area_id = battle[:2]
        formation_id = battle[3:]

        do_randomize_battle = True
        for forbidden_formation in dont_randomize_formations:
            if (    forbidden_formation[:2] == area_id
                and forbidden_formation[3:] in [formation_id, "XX"]
            ):
                do_randomize_battle = False
                break

        if do_randomize_battle:
            # Choose the size of the formation depending on chapter difficulty
            for cur_chapter in chapter_battle_mapping:
                if area_id in chapter_battle_mapping.get(cur_chapter):
                    if cur_chapter == 0:
                        battle_homechapter = 1
                    else:
                        battle_homechapter = cur_chapter
                    break
            chapter_difficulty = chapter_changes.get(battle_homechapter)
            rnd_number_of_enemies = _get_random_formationsize(
                chapter_difficulty,
                do_progressive_scaling,
                random
            )

            available_enemies = [
                enemy for enemy in actor_areas.get(area_id) if enemy not in dont_randomize_enemies
            ]

            if battle not in special_random_formations:
                # Select an enemy at random for each occupied file
                current_enemylist = []
                placed_healer = False

                for i in range(1, rnd_number_of_enemies + 1):
                    force_matching_firstfile = True
                    if i == 1 and force_matching_firstfile:
                        # Match the first enemy in the formation to the enemy
                        # appearing in the field, so first strikes don't get
                        # weird
                        current_enemylist.append(front_row_enemy)
                    else:
                        while True:
                            new_enemy = random.choice(available_enemies)
                            # In case of bat, check if battle stage has ceiling.
                            # If not, pick other enemy
                            if "Swoop" in new_enemy:
                                for stage in battlestage_ceiling_formations.keys():
                                    if battle in battlestage_ceiling_formations.get(stage):
                                        current_enemylist.append(new_enemy)
                                        break
                                else:
                                    continue
                                break
                            else:
                                if (   "WMagikoopa" in new_enemy
                                    or "MediGuy" in new_enemy
                                ):
                                    if placed_healer:
                                        # We do not want more than one healing
                                        # enemy in a formation
                                        continue
                                    placed_healer = True
                                current_enemylist.append(new_enemy)
                                break

                # Build new formation for current battle with chosen enemies
                new_formation = _get_new_formation(
                    actor_pointers,
                    area_id,
                    formation_id,
                    current_enemylist,
                    random
                )

                battle_formations.append(new_formation)

            else:
                # Randomize a certain set of special battles in individual ways
                new_special_formation = _get_new_special_formation(
                    actor_pointers,
                    area_id,
                    formation_id,
                    chapter_difficulty,
                    do_progressive_scaling,
                    available_enemies,
                    random
                )

                battle_formations.append(new_special_formation)

    # Write test formation
    #battle_formations.append([
    #    0x0000010A,
    #    0x802196EC,
    #    0x00000000,
    #    0x00000000,
    #    0x00000209,
    #    0x8021B0AC,
    #    0x00000000,
    #    0x00000000,
    #    0x0001010A,
    #    0x8021B0AC,
    #    0x00000000,
    #    0x00000000,
    #    0x00010209,
    #    0x8021B0AC,
    #    0x00000000,
    #    0x00000000,
    #])

    return battle_formations
