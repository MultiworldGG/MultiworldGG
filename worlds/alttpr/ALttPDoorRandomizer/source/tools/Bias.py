# Demo script showing bias in VT and ER boss shuffle algorithms, with proposed fixes.

import random

boss_location_list = [
    'GT_top',
    'GT_mid',
    'TH',
    'SW',
    'EP',
    'DP',
    'PD',
    'SP',
    'TT',
    'IP',
    'MM',
    'TR',
    'GT_bot'
]

entrance_rando_boss_location_list = [
    'GT_top',
    'TH',
    'SW',
    'GT_mid',
    'EP',
    'DP',
    'PD',
    'SP',
    'TT',
    'IP',
    'MM',
    'TR',
    'GT_bot'
]

boss_list = [
    'Armos',
    'Lanmo',
    'Moldorm',
    'Helma',
    'Arrghus',
    'Moth',
    'Blind',
    'Khold',
    'Vitty',
    'Trinexx'
]

results_dict = {
    'GT_top': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'GT_mid': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'TH': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'SW': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'EP': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'DP': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'PD': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'SP': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'TT': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'IP': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'MM': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'TR': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0},
    'GT_bot': {'Armos': 0, 'Lanmo': 0, 'Moldorm': 0, 'Helma': 0, 'Arrghus': 0, 'Moth': 0, 'Blind': 0, 'Khold': 0, 'Vitty': 0, 'Trinexx': 0}
}

def can_place_boss(boss:str, dungeon_name: str) -> bool:
    if (dungeon_name == 'GT_top'):
        if boss in {'Armos', 'Arrghus', 'Blind', 'Trinexx', 'Lanmo'}:
            return False
    elif (dungeon_name == 'GT_mid'):
        if boss == 'Blind':
            return False
    elif (dungeon_name == 'TH'):
        if boss in {'Armos', 'Arrghus', 'Blind', 'Trinexx', 'Lanmo'}:
            return False
    elif (dungeon_name == 'SW'):
        if boss == 'Trinexx':
            return False
    return True

def resetresults():
    for boss_location in boss_location_list:
        for boss in boss_list:
            results_dict[boss_location][boss] = 0

def printresults(iterations):
    for boss_location in boss_location_list:
        print("Location: " + boss_location.ljust(6) + ' ', end='')
        for boss in boss_list:
            percentagestr = "{0:.2%}".format(results_dict[boss_location][boss] / iterations)
            print(boss + ": " + percentagestr.rjust(6) + ' ', end='')
        restrictive_count = results_dict[boss_location]['Armos'] + results_dict[boss_location]['Arrghus'] + results_dict[boss_location]['Blind'] + results_dict[boss_location]['Trinexx'] + results_dict[boss_location]['Lanmo']
        restrictive_pct = "{0:.2%}".format(restrictive_count / iterations)
        nonrestrictive_count = results_dict[boss_location]['Moldorm'] + results_dict[boss_location]['Helma'] + results_dict[boss_location]['Moth'] + results_dict[boss_location]['Khold'] + results_dict[boss_location]['Vitty']
        nonrestrictive_pct = "{0:.2%}".format(nonrestrictive_count / iterations)
        print("Restrictive: " + restrictive_pct.rjust(7) + " Non-restrictive: " + nonrestrictive_pct.rjust(7))

# Demonstration of reshuffle algorithm at:
# https://github.com/sporchia/alttp_vt_randomizer/blob/master/app/Randomizer.php#L399
def vt(reshuffle):
    for i in range(iterations):
        dupes = random.sample(boss_list, 3)
        temp_full_boss_list = boss_list + dupes
        shuffled_boss_list = temp_full_boss_list.copy()
        random.shuffle(shuffled_boss_list)
        for boss_location in boss_location_list:
            boss = shuffled_boss_list.pop(0)
            while (not can_place_boss(boss, boss_location)):
                shuffled_boss_list.append(boss)

                # Proposed fix
                if reshuffle:
                    random.shuffle(shuffled_boss_list)

                boss = shuffled_boss_list.pop(0)
            results_dict[boss_location][boss] = results_dict[boss_location][boss] + 1

# Demonstration of reshuffle algorithm at:
# https://github.com/KevinCathcart/ALttPEntranceRandomizer/blob/Dev/Bosses.py#L203
def er(reshuffle):
    for i in range(iterations):
        dupes = random.sample(boss_list, 3)
        temp_full_boss_list = boss_list + dupes
        shuffled_boss_list = temp_full_boss_list.copy()
        random.shuffle(shuffled_boss_list)
        for boss_location in entrance_rando_boss_location_list:
            boss = next((b for b in shuffled_boss_list if can_place_boss(b, boss_location)), None)
            shuffled_boss_list.remove(boss)
            results_dict[boss_location][boss] = results_dict[boss_location][boss] + 1

            # Proposed fix
            if reshuffle:
                random.shuffle(shuffled_boss_list)

def er_unique():
    for i in range(iterations):
        temp_full_boss_list = boss_list
        moldorm2 = random.choice([b for b in boss_list
                                  if b not in ["Armos", "Arrghus", "Blind", "Trinexx", "Lanmo"]])
        lanmo2 = random.choice([b for b in boss_list
                                if b not in [moldorm2, "Blind"]])
        armos2 = random.choice([b for b in boss_list if b not in [moldorm2, lanmo2]])
        gt_bosses = [moldorm2, lanmo2, armos2]

        shuffled_boss_list = temp_full_boss_list.copy()
        for boss_location in entrance_rando_boss_location_list:
            if '_' in boss_location:
                boss = random.choice([b for b in gt_bosses if can_place_boss(b, boss_location)])
                gt_bosses.remove(boss)
            else:
                boss = random.choice([b for b in shuffled_boss_list if can_place_boss(b, boss_location)])
                shuffled_boss_list.remove(boss)
            results_dict[boss_location][boss] += 1

def er_unique_chaos():
    for i in range(iterations):
        temp_full_boss_list = boss_list

        shuffled_boss_list = temp_full_boss_list.copy()
        for boss_location in entrance_rando_boss_location_list:
            if '_' in boss_location:
                boss = random.choice(b for b in boss_list if can_place_boss(b, boss_location))
            else:
                boss = random.choice(b for b in shuffled_boss_list if can_place_boss(b, boss_location))
                shuffled_boss_list.remove(boss)
            results_dict[boss_location][boss] += 1


if __name__ == '__main__':

    iterations = 100000
    # reshuffle = False
    #
    # vt(reshuffle)
    #
    # print("Original results:")
    #
    # printresults(iterations)
    # resetresults()
    #
    # reshuffle = True
    #
    # vt(reshuffle)
    #
    # print("")
    # print("Reshuffled results:")
    #
    # printresults(iterations)
    # resetresults()
    #
    # #ER
    # reshuffle = False
    # er(reshuffle)
    #
    # print("")
    # print("ER Original results:")
    #
    # printresults(iterations)
    # resetresults()
    #
    # reshuffle = True
    # er(reshuffle)
    #
    # print("")
    # print("ER Reshuffled results:")
    #
    # printresults(iterations)
    # resetresults()

    er_unique()

    print("")
    print("ER Unique results:")

    printresults(iterations)
    resetresults()

    er_unique_chaos()

    print("")
    print("ER Chaos results:")

    printresults(iterations)

# Results:
#Original results:
#Location: GT_top Armos:  0.00% Lanmo:  0.00% Moldorm: 20.00% Helma: 19.89% Arrghus:  0.00% Moth: 20.01% Blind:  0.00% Khold: 20.14% Vitty: 19.96% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: GT_mid Armos: 11.05% Lanmo: 11.16% Moldorm: 11.00% Helma: 11.35% Arrghus: 11.07% Moth: 11.00% Blind:  0.00% Khold: 11.01% Vitty: 11.20% Trinexx: 11.15% Restrictive:  44.43% Non-restrictive:  55.57%
#Location: TH     Armos:  0.00% Lanmo:  0.00% Moldorm: 20.06% Helma: 19.95% Arrghus:  0.00% Moth: 20.07% Blind:  0.00% Khold: 19.88% Vitty: 20.05% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: SW     Armos: 11.30% Lanmo: 11.04% Moldorm: 11.30% Helma: 10.95% Arrghus: 11.09% Moth: 11.04% Blind: 11.15% Khold: 11.15% Vitty: 10.98% Trinexx:  0.00% Restrictive:  44.59% Non-restrictive:  55.42%
#Location: EP     Armos:  9.89% Lanmo:  9.90% Moldorm: 10.02% Helma:  9.97% Arrghus: 10.17% Moth:  9.98% Blind:  9.95% Khold: 10.16% Vitty:  9.90% Trinexx: 10.07% Restrictive:  49.97% Non-restrictive:  50.03%
#Location: DP     Armos:  9.98% Lanmo: 10.09% Moldorm:  9.97% Helma:  9.95% Arrghus: 10.17% Moth: 10.01% Blind:  9.87% Khold: 10.02% Vitty:  9.88% Trinexx: 10.04% Restrictive:  50.16% Non-restrictive:  49.84%
#Location: PD     Armos: 10.12% Lanmo:  9.96% Moldorm:  9.85% Helma:  9.90% Arrghus: 10.31% Moth:  9.91% Blind:  9.96% Khold:  9.87% Vitty:  9.94% Trinexx: 10.17% Restrictive:  50.52% Non-restrictive:  49.48%
#Location: SP     Armos: 10.41% Lanmo: 10.35% Moldorm:  9.61% Helma:  9.66% Arrghus: 10.29% Moth:  9.60% Blind: 10.47% Khold:  9.67% Vitty:  9.53% Trinexx: 10.42% Restrictive:  51.93% Non-restrictive:  48.07%
#Location: TT     Armos: 11.04% Lanmo: 10.98% Moldorm:  8.86% Helma:  8.95% Arrghus: 10.98% Moth:  9.12% Blind: 11.18% Khold:  8.98% Vitty:  9.03% Trinexx: 10.89% Restrictive:  55.06% Non-restrictive:  44.94%
#Location: IP     Armos: 12.10% Lanmo: 11.89% Moldorm:  7.81% Helma:  7.83% Arrghus: 11.94% Moth:  7.89% Blind: 12.84% Khold:  7.87% Vitty:  7.99% Trinexx: 11.84% Restrictive:  60.62% Non-restrictive:  39.38%
#Location: MM     Armos: 13.67% Lanmo: 13.66% Moldorm:  6.00% Helma:  6.17% Arrghus: 13.48% Moth:  6.18% Blind: 15.06% Khold:  6.25% Vitty:  6.14% Trinexx: 13.41% Restrictive:  69.28% Non-restrictive:  30.72%
#Location: TR     Armos: 15.35% Lanmo: 15.49% Moldorm:  3.87% Helma:  3.90% Arrghus: 15.31% Moth:  3.78% Blind: 19.06% Khold:  3.89% Vitty:  3.82% Trinexx: 15.53% Restrictive:  80.74% Non-restrictive:  19.26%
#Location: GT_bot Armos: 15.24% Lanmo: 15.24% Moldorm:  1.54% Helma:  1.51% Arrghus: 15.22% Moth:  1.52% Blind: 20.44% Khold:  1.51% Vitty:  1.53% Trinexx: 26.25% Restrictive:  92.38% Non-restrictive:   7.62%
#
#Reshuffled results:
#Location: GT_top Armos:  0.00% Lanmo:  0.00% Moldorm: 20.02% Helma: 19.97% Arrghus:  0.00% Moth: 20.02% Blind:  0.00% Khold: 20.07% Vitty: 19.92% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: GT_mid Armos: 12.23% Lanmo: 12.05% Moldorm: 10.23% Helma: 10.24% Arrghus: 12.11% Moth: 10.31% Blind:  0.00% Khold: 10.36% Vitty: 10.33% Trinexx: 12.13% Restrictive:  48.52% Non-restrictive:  51.48%
#Location: TH     Armos:  0.00% Lanmo:  0.00% Moldorm: 19.86% Helma: 20.09% Arrghus:  0.00% Moth: 20.23% Blind:  0.00% Khold: 19.83% Vitty: 19.99% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: SW     Armos: 13.23% Lanmo: 13.34% Moldorm:  9.05% Helma:  9.02% Arrghus: 13.37% Moth:  9.10% Blind: 14.97% Khold:  8.98% Vitty:  8.93% Trinexx:  0.00% Restrictive:  54.92% Non-restrictive:  45.08%
#Location: EP     Armos: 11.54% Lanmo: 11.50% Moldorm:  7.96% Helma:  7.82% Arrghus: 11.76% Moth:  7.81% Blind: 12.84% Khold:  7.79% Vitty:  8.03% Trinexx: 12.95% Restrictive:  60.59% Non-restrictive:  39.41%
#Location: DP     Armos: 11.55% Lanmo: 11.49% Moldorm:  7.93% Helma:  7.85% Arrghus: 11.72% Moth:  7.69% Blind: 12.80% Khold:  7.99% Vitty:  7.74% Trinexx: 13.25% Restrictive:  60.80% Non-restrictive:  39.20%
#Location: PD     Armos: 11.79% Lanmo: 11.47% Moldorm:  7.81% Helma:  7.78% Arrghus: 11.61% Moth:  7.91% Blind: 12.81% Khold:  7.78% Vitty:  8.00% Trinexx: 13.02% Restrictive:  60.71% Non-restrictive:  39.29%
#Location: SP     Armos: 11.59% Lanmo: 11.56% Moldorm:  7.90% Helma:  7.75% Arrghus: 11.52% Moth:  8.02% Blind: 12.67% Khold:  7.92% Vitty:  7.85% Trinexx: 13.23% Restrictive:  60.57% Non-restrictive:  39.43%
#Location: TT     Armos: 11.64% Lanmo: 11.64% Moldorm:  7.77% Helma:  7.73% Arrghus: 11.70% Moth:  7.67% Blind: 12.89% Khold:  8.05% Vitty:  7.85% Trinexx: 13.07% Restrictive:  60.93% Non-restrictive:  39.07%
#Location: IP     Armos: 11.54% Lanmo: 11.77% Moldorm:  7.95% Helma:  7.97% Arrghus: 11.49% Moth:  7.80% Blind: 12.64% Khold:  7.87% Vitty:  7.89% Trinexx: 13.10% Restrictive:  60.54% Non-restrictive:  39.47%
#Location: MM     Armos: 11.69% Lanmo: 11.65% Moldorm:  7.91% Helma:  7.88% Arrghus: 11.59% Moth:  7.78% Blind: 12.80% Khold:  7.73% Vitty:  7.92% Trinexx: 13.04% Restrictive:  60.77% Non-restrictive:  39.23%
#Location: TR     Armos: 11.58% Lanmo: 11.82% Moldorm:  7.75% Helma:  7.83% Arrghus: 11.62% Moth:  7.79% Blind: 12.76% Khold:  7.90% Vitty:  7.76% Trinexx: 13.19% Restrictive:  60.97% Non-restrictive:  39.03%
#Location: GT_bot Armos: 11.54% Lanmo: 11.60% Moldorm:  7.91% Helma:  7.87% Arrghus: 11.62% Moth:  7.90% Blind: 12.78% Khold:  7.82% Vitty:  7.86% Trinexx: 13.10% Restrictive:  60.65% Non-restrictive:  39.35%
#
#ER Original results:
#Location: GT_top Armos:  0.00% Lanmo:  0.00% Moldorm: 19.94% Helma: 19.87% Arrghus:  0.00% Moth: 19.98% Blind:  0.00% Khold: 20.31% Vitty: 19.90% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: GT_mid Armos: 14.15% Lanmo: 14.33% Moldorm:  4.51% Helma:  4.53% Arrghus: 14.19% Moth:  4.56% Blind:  0.00% Khold:  4.61% Vitty:  4.49% Trinexx: 34.62% Restrictive:  77.30% Non-restrictive:  22.70%
#Location: TH     Armos:  0.00% Lanmo:  0.00% Moldorm: 19.93% Helma: 19.98% Arrghus:  0.00% Moth: 20.10% Blind:  0.00% Khold: 19.75% Vitty: 20.24% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: SW     Armos: 21.52% Lanmo: 21.56% Moldorm:  2.76% Helma:  2.80% Arrghus: 21.50% Moth:  2.82% Blind: 21.48% Khold:  2.81% Vitty:  2.75% Trinexx:  0.00% Restrictive:  86.05% Non-restrictive:  13.95%
#Location: EP     Armos: 11.39% Lanmo: 11.33% Moldorm:  5.89% Helma:  5.69% Arrghus: 11.32% Moth:  5.83% Blind: 24.71% Khold:  5.82% Vitty:  5.76% Trinexx: 12.27% Restrictive:  71.01% Non-restrictive:  28.99%
#Location: DP     Armos: 11.62% Lanmo: 11.66% Moldorm:  8.05% Helma:  8.32% Arrghus: 11.75% Moth:  8.13% Blind: 12.46% Khold:  8.10% Vitty:  8.18% Trinexx: 11.73% Restrictive:  59.22% Non-restrictive:  40.78%
#Location: PD     Armos: 11.01% Lanmo: 10.77% Moldorm:  9.18% Helma:  9.20% Arrghus: 10.89% Moth:  9.03% Blind: 10.83% Khold:  9.13% Vitty:  9.17% Trinexx: 10.79% Restrictive:  54.29% Non-restrictive:  45.71%
#Location: SP     Armos: 10.26% Lanmo: 10.17% Moldorm:  9.73% Helma:  9.61% Arrghus: 10.33% Moth:  9.69% Blind: 10.31% Khold:  9.84% Vitty:  9.61% Trinexx: 10.45% Restrictive:  51.52% Non-restrictive:  48.48%
#Location: TT     Armos: 10.12% Lanmo: 10.01% Moldorm: 10.07% Helma:  9.97% Arrghus: 10.16% Moth:  9.92% Blind:  9.95% Khold:  9.73% Vitty:  9.96% Trinexx: 10.11% Restrictive:  50.35% Non-restrictive:  49.65%
#Location: IP     Armos: 10.03% Lanmo: 10.01% Moldorm: 10.00% Helma: 10.10% Arrghus:  9.89% Moth:  9.93% Blind: 10.13% Khold:  9.99% Vitty:  9.80% Trinexx: 10.13% Restrictive:  50.18% Non-restrictive:  49.82%
#Location: MM     Armos:  9.89% Lanmo:  9.99% Moldorm: 10.09% Helma: 10.10% Arrghus: 10.02% Moth:  9.93% Blind: 10.03% Khold: 10.00% Vitty: 10.06% Trinexx:  9.89% Restrictive:  49.81% Non-restrictive:  50.19%
#Location: TR     Armos: 10.03% Lanmo: 10.10% Moldorm: 10.01% Helma:  9.92% Arrghus:  9.94% Moth: 10.01% Blind: 10.04% Khold:  9.95% Vitty:  9.92% Trinexx: 10.08% Restrictive:  50.19% Non-restrictive:  49.81%
#Location: GT_bot Armos:  9.90% Lanmo: 10.04% Moldorm:  9.88% Helma:  9.85% Arrghus: 10.00% Moth: 10.04% Blind: 10.09% Khold: 10.09% Vitty: 10.11% Trinexx: 10.01% Restrictive:  50.03% Non-restrictive:  49.97%
#
#ER Reshuffled results:
#Location: GT_top Armos:  0.00% Lanmo:  0.00% Moldorm: 20.11% Helma: 19.81% Arrghus:  0.00% Moth: 20.22% Blind:  0.00% Khold: 20.08% Vitty: 19.78% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: GT_mid Armos: 13.17% Lanmo: 13.37% Moldorm:  9.05% Helma:  9.14% Arrghus: 13.23% Moth:  9.29% Blind:  0.00% Khold:  8.96% Vitty:  9.11% Trinexx: 14.69% Restrictive:  54.45% Non-restrictive:  45.55%
#Location: TH     Armos:  0.00% Lanmo:  0.00% Moldorm: 20.03% Helma: 19.72% Arrghus:  0.00% Moth: 20.17% Blind:  0.00% Khold: 19.86% Vitty: 20.23% Trinexx:  0.00% Restrictive:   0.00% Non-restrictive: 100.00%
#Location: SW     Armos: 13.38% Lanmo: 13.41% Moldorm:  9.27% Helma:  9.33% Arrghus: 13.41% Moth:  9.27% Blind: 13.48% Khold:  9.28% Vitty:  9.17% Trinexx:  0.00% Restrictive:  53.69% Non-restrictive:  46.31%
#Location: EP     Armos: 11.50% Lanmo: 11.56% Moldorm:  7.90% Helma:  8.06% Arrghus: 11.58% Moth:  8.11% Blind: 12.72% Khold:  7.93% Vitty:  7.93% Trinexx: 12.70% Restrictive:  60.06% Non-restrictive:  39.94%
#Location: DP     Armos: 11.66% Lanmo: 11.51% Moldorm:  8.05% Helma:  7.96% Arrghus: 11.43% Moth:  7.83% Blind: 12.94% Khold:  7.89% Vitty:  7.88% Trinexx: 12.87% Restrictive:  60.40% Non-restrictive:  39.60%
#Location: PD     Armos: 11.36% Lanmo: 11.53% Moldorm:  7.89% Helma:  7.96% Arrghus: 11.46% Moth:  7.72% Blind: 13.12% Khold:  8.07% Vitty:  8.02% Trinexx: 12.87% Restrictive:  60.34% Non-restrictive:  39.66%
#Location: SP     Armos: 11.27% Lanmo: 11.38% Moldorm:  7.89% Helma:  7.98% Arrghus: 11.56% Moth:  7.89% Blind: 13.10% Khold:  8.17% Vitty:  8.08% Trinexx: 12.68% Restrictive:  59.99% Non-restrictive:  40.01%
#Location: TT     Armos: 11.32% Lanmo: 11.49% Moldorm:  7.91% Helma:  8.16% Arrghus: 11.44% Moth:  7.97% Blind: 12.93% Khold:  8.05% Vitty:  7.97% Trinexx: 12.77% Restrictive:  59.94% Non-restrictive:  40.06%
#Location: IP     Armos: 11.69% Lanmo: 11.74% Moldorm:  7.91% Helma:  8.00% Arrghus: 11.34% Moth:  7.87% Blind: 12.80% Khold:  7.82% Vitty:  7.95% Trinexx: 12.88% Restrictive:  60.44% Non-restrictive:  39.56%
#Location: MM     Armos: 11.57% Lanmo: 11.31% Moldorm:  8.13% Helma:  7.90% Arrghus: 11.32% Moth:  7.91% Blind: 13.15% Khold:  7.97% Vitty:  7.82% Trinexx: 12.91% Restrictive:  60.26% Non-restrictive:  39.74%
#Location: TR     Armos: 11.44% Lanmo: 11.30% Moldorm:  8.04% Helma:  8.13% Arrghus: 11.47% Moth:  7.90% Blind: 12.82% Khold:  8.09% Vitty:  7.96% Trinexx: 12.84% Restrictive:  59.87% Non-restrictive:  40.13%
#Location: GT_bot Armos: 11.36% Lanmo: 11.53% Moldorm:  7.87% Helma:  7.99% Arrghus: 11.49% Moth:  7.96% Blind: 13.01% Khold:  7.98% Vitty:  8.00% Trinexx: 12.80% Restrictive:  60.19% Non-restrictive:  39.81