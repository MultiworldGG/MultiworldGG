import subprocess
import sys
import multiprocessing
import concurrent.futures
import argparse
from collections import OrderedDict
import csv

cpu_threads = multiprocessing.cpu_count()
py_version = f"{sys.version_info.major}.{sys.version_info.minor}"


ALL_SETTINGS = {
    'mode': ['open', 'standard', 'inverted'],
    'goal': ['ganon', 'pedestal', 'triforcehunt', 'trinity', 'crystals', 'dungeons'],
    'swords': ['random', 'swordless', 'assured'],
    'shuffle': ['vanilla','simple','restricted','full','dungeonssimple','dungeonsfull','lite','lean','district','swapped','crossed','insanity'],
    'shufflelinks': [True, False],
    'shuffleganon': [True, False],
    'door_shuffle': ['vanilla', 'basic', 'crossed'],
    'intensity': ['1','2','3'],
    'ow_shuffle': ['vanilla', 'parallel', 'full'],
    'ow_fluteshuffle': ['vanilla', 'balanced', 'random'],
    'ow_keepsimilar': [True, False],
    'ow_mixed': [True, False],
    'ow_crossed': [True, False],
    'accessibility': [True, False],
    'difficulty': [True, False],
    'shufflepots': [True, False],
    'keydropshuffle': [True, False],
    'keysanity': [True, False],
    'retro': [True, False],
    'bombbag': [True, False],
    'shopsanity': [True, False]
}

SETTINGS = {
    'mode': ['standard', 'open', 'inverted'],
    'goal': ['ganon'],
    'swords': ['random'],
    'shuffle': ['vanilla', 
        'dungeonssimple', 'dungeonsfull', 'simple', 'restricted', 'full', 'lite', 'lean', 'district', 'swapped', 'crossed', 'insanity'
        ],
    'shufflelinks': [True, False],
    'shuffleganon': [True, False],
    'door_shuffle': ['vanilla', 'crossed'],
    'intensity': ['2'],
    'ow_shuffle': ['vanilla', 'parallel', 'full'],
    'ow_fluteshuffle': ['balanced'],
    'ow_keepsimilar': [True, False],
    'ow_mixed': [True, False],
    'ow_crossed': ['none', 'polar', 'grouped', 'unrestricted'],
    'accessibility': [True],
    'difficulty': [False],
    'shufflepots': [False],
    'keydropshuffle': [False],
    'keysanity': [False],
    'retro': [True, False],
    'bombbag': [False],
    'shopsanity': [True, False]
}

optionsList = []
for sett,options in SETTINGS.items():
    for option in options:
        if isinstance(option, str):
            optionsList.append(f'{option}')
        else:
            optionsList.append('{}-{}'.format(sett,str(option)))

headerList = list(SETTINGS.keys())

def main(args=None):
    successes = []
    errors = []
    task_mapping = []
    tests = OrderedDict()

    successes.append(f"Testing {args.ow} with {args.count} Tests" + (f" (intensity={args.tense})" if args.ow in ['basic', 'crossed'] else ""))
    print(successes[0])

    max_attempts = args.count
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=cpu_threads)
    dead_or_alive = 0
    alive = 0

    def test(testname: list, command: str):
        tests[' '.join(testname)] = [command]
        basecommand = f"py DungeonRandomizer.py --shuffle {args.ow} --suppress_rom --suppress_spoiler"

        def gen_seed():
            taskcommand = basecommand + ' ' + command
            return subprocess.run(taskcommand, capture_output=True, shell=True, text=True)

        for _ in range(1, max_attempts + 1):
            task = pool.submit(gen_seed)
            task.success = False
            task.name = ' '.join(testname)
            task.settings = testname
            task.cmd = basecommand + ' ' + command
            task_mapping.append(task)

    for mode in SETTINGS['mode']:
        for goal in SETTINGS['goal']:
            for swords in SETTINGS['swords']:
                #for shuffle in SETTINGS['shuffle']:
                for ow_shuffle in SETTINGS['ow_shuffle']:
                    for shufflelinks in SETTINGS['shufflelinks']:
                        for shuffleganon in SETTINGS['shuffleganon']:
                            for door_shuffle in SETTINGS['door_shuffle']:
                                for intensity in SETTINGS['intensity']:
                                    for ow_fluteshuffle in SETTINGS['ow_fluteshuffle']:
                                        for ow_keepsimilar in SETTINGS['ow_keepsimilar']:
                                            for ow_mixed in SETTINGS['ow_mixed']:
                                                for ow_crossed in SETTINGS['ow_crossed']:
                                                    for difficulty in SETTINGS['difficulty']:
                                                        for shufflepots in SETTINGS['shufflepots']:
                                                            for accessibility in SETTINGS['accessibility']:
                                                                for keydropshuffle in SETTINGS['keydropshuffle']:
                                                                    for keysanity in SETTINGS['keysanity']:
                                                                        for retro in SETTINGS['retro']:
                                                                            for bombbag in SETTINGS['bombbag']:
                                                                                for shopsanity in SETTINGS['shopsanity']:
                                                                                    commands = ''
                                                                                    name = []
                                                                                    commands = commands + f' --mode {mode}'
                                                                                    name.append(mode)
                                                                                    commands = commands + f' --goal {goal}'
                                                                                    name.append(goal)
                                                                                    commands = commands + f' --swords {swords}'
                                                                                    name.append(swords)
                                                                                    # if shuffle != 'vanilla': #since this is the output is grouped on this, we only want one of these in the loop
                                                                                    #     continue
                                                                                    # commands = commands + f' --shuffle {shuffle}'
                                                                                    # name.append(f'ER{shuffle}')
                                                                                    commands = commands + f' --ow_shuffle {ow_shuffle}'
                                                                                    name.append(ow_shuffle)
                                                                                    if shufflelinks:
                                                                                        commands = commands + f' --shufflelinks'
                                                                                        name.append('shufflelinks-True')
                                                                                    else:
                                                                                        name.append('shufflelinks-False')
                                                                                    if shuffleganon:
                                                                                        commands = commands + f' --shuffleganon'
                                                                                        name.append('shuffleganon-True')
                                                                                    else:
                                                                                        name.append('shuffleganon-False')
                                                                                    commands = commands + f' --door_shuffle {door_shuffle}'
                                                                                    name.append(door_shuffle)
                                                                                    if intensity == '3' and door_shuffle == 'vanilla':
                                                                                        continue
                                                                                    commands = commands + f' --intensity {intensity}'
                                                                                    name.append(intensity)
                                                                                    commands = commands + f' --ow_fluteshuffle {ow_fluteshuffle}'
                                                                                    name.append(ow_fluteshuffle)
                                                                                    if difficulty:
                                                                                        commands = commands + f' --difficulty expert'
                                                                                        commands = commands + f' --item_functionality expert'
                                                                                        name.append('difficulty-True')
                                                                                    else:
                                                                                        name.append('difficulty-False')
                                                                                    if ow_keepsimilar:
                                                                                        commands = commands + f' --ow_keepsimilar'
                                                                                        name.append('ow_keepsimilar-True')
                                                                                    else:
                                                                                        if ow_crossed in ['none', 'polar', 'grouped']:
                                                                                            continue
                                                                                        name.append('ow_keepsimilar-False')
                                                                                    if ow_mixed:
                                                                                        commands = commands + f' --ow_mixed'
                                                                                        name.append('ow_mixed-True')
                                                                                    else:
                                                                                        if ow_crossed == 'polar':
                                                                                            continue
                                                                                        name.append('ow_mixed-False')
                                                                                    commands = commands + f' --ow_crossed {ow_crossed}'
                                                                                    name.append(ow_crossed)
                                                                                    if shufflepots:
                                                                                        commands = commands + f' --shufflepots'
                                                                                        name.append('shufflepots-True')
                                                                                    else:
                                                                                        name.append('shufflepots-False')
                                                                                    if not accessibility:
                                                                                        commands = commands + f' --accessibility none'
                                                                                        name.append('accessibility-False')
                                                                                    else:
                                                                                        name.append('accessibility-True')
                                                                                    if keydropshuffle:
                                                                                        commands = commands + f' --keydropshuffle'
                                                                                        name.append('keydropshuffle-True')
                                                                                    else:
                                                                                        name.append('keydropshuffle-False')
                                                                                    if keysanity:
                                                                                        commands = commands + f' --keysanity'
                                                                                        name.append('keysanity-True')
                                                                                    else:
                                                                                        name.append('keysanity-False')
                                                                                    if retro:
                                                                                        commands = commands + f' --retro'
                                                                                        name.append('retro-True')
                                                                                    else:
                                                                                        name.append('retro-False')
                                                                                    if bombbag:
                                                                                        commands = commands + f' --bombbag'
                                                                                        name.append('bombbag-True')
                                                                                    else:
                                                                                        name.append('bombbag-False')
                                                                                    if shopsanity:
                                                                                        commands = commands + f' --shopsanity'
                                                                                        name.append('shopsanity-True')
                                                                                    else:
                                                                                        name.append('shopsanity-False')
                                                                                    test(name, commands)

#    test("Vanilla   ", "--futuro --shuffle vanilla")
#    test("Basic     ", "--futuro --retro --shuffle vanilla")
#    test("Keysanity ", "--futuro --shuffle vanilla --keydropshuffle --keysanity")
#    test("Simple    ", "--futuro --shuffle simple")
#    test("Crossed   ", "--futuro --shuffle crossed")
#    test("Insanity   ", "--futuro --shuffle insanity")
#    test("CrossKeys  ", "--futuro --shuffle crossed --keydropshuffle --keysanity")

    from tqdm import tqdm
    with tqdm(concurrent.futures.as_completed(task_mapping),
              total=len(task_mapping), unit="seed(s)",
              desc=f"Success rate: 0.00%") as progressbar:
        for task in progressbar:
            dead_or_alive += 1
            try:
                result = task.result()
                if result.returncode:
                    errors.append([task.name, task.cmd, result.stderr])
                else:
                    alive += 1
                    task.success = True
            except Exception as e:
                raise e

            progressbar.set_description(f"Success rate: {(alive/dead_or_alive)*100:.2f}% - {task.name}")

    def get_results(option: str):
        result = ""
        dead_or_alive = [task.success for task in task_mapping if option in task.settings]
        if len(dead_or_alive):
            alive = [x for x in dead_or_alive if x]
            success = f"{option} Rate: {(len(alive) / len(dead_or_alive)) * 100:.1f}%"
            successes.append(success)
            print(success)
            result += f"{(len(alive)/len(dead_or_alive))*100:.2f}%\t"
        else:
            success = f"{option} Rate: NULL%"
            print(success)
            result += f"NULL%\t"
        return result.strip()
    
    results = []
    for option in optionsList:
        results.append(get_results(option))

    for result in results:
        successes.append(result)

    tabresultsfile = './output/' + args.ow + '.tsv'
    with open(tabresultsfile, 'w+', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        header = headerList.copy()
        header.append('Success')
        writer.writerow(header)
        for task in task_mapping:
            settings = []
            for option in headerList:
                if option in task.settings:
                    settings.append(1)
                elif str(option + '-True') in task.settings:
                    settings.append(1)
                else:
                    settings.append(0)
            if task.success:
                settings.append(1)
            else:
                settings.append(0)
            writer.writerow(settings)

    return successes, errors


if __name__ == "__main__":
    successes = []

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--count', default=0, type=lambda value: max(int(value), 0))
    parser.add_argument('--cpu_threads', default=cpu_threads, type=lambda value: max(int(value), 1))
    parser.add_argument('--help', default=False, action='store_true')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        exit(0)

    cpu_threads = args.cpu_threads

#    for ow in [['full', args.count if args.count else 2, 1]]:
    # for ow in [['vanilla', args.count if args.count else 2, 1],
    #            ['parallel', args.count if args.count else 5, 1],
    #            ['full', args.count if args.count else 10, 1]]:
    count = args.count if args.count else 1
    for ow in SETTINGS['shuffle']:
        for tense in range(1, 2): #ow[2] + 1): #unnecessary when DR is not the root setting
            args = argparse.Namespace()
            args.ow = ow #ow[0]
            args.tense = tense
            args.count = count #ow[1]
            s, errors = main(args=args)
            if successes:
                successes += [""] * 2
            successes += s
            print()

            if errors:
                with open(f"./output/{ow[0]}{(f'-{tense}' if ow in ['parallel', 'full'] else '')}-errors.txt", 'w+') as stream:
                    for error in errors:
                        stream.write(error[0] + "\n")
                        stream.write(error[1] + "\n")
                        stream.write(error[2] + "\n\n")

    with open("./output/success.txt", "w+") as stream:
        stream.write(str.join("\n", successes))

    input("Press enter to continue")
