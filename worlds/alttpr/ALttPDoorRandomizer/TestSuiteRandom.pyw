import subprocess
import sys
import multiprocessing
import concurrent.futures
import argparse
import sqlite3
from collections import OrderedDict
from datetime import datetime

cpu_threads = multiprocessing.cpu_count()
py_version = f"{sys.version_info.major}.{sys.version_info.minor}"


def main(args=None):
    successes = []
    errors = []
    task_mapping = []
    tests = OrderedDict()

    max_attempts = 1 #args and args.count if args.count is not None else 1
    print(f"Testing Random OWR with {max_attempts} Tests")

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=cpu_threads)
    dead_or_alive = 0
    alive = 0

    
    basecommand = f'py Mystery.py --suppress_rom --suppress_meta --spoiler full --outputpath L:/_Work/Zelda/ROMs/Bug/Automate/{datetime.now().strftime("%y%m%d")} --weights L:/_Work/Zelda/ROMs/Bug/Automate/_test.yml'
        
    def gen_seed():
        return subprocess.run(basecommand, capture_output=True, shell=True, text=True)

    for x in range(1, max_attempts + 1):
        task = pool.submit(gen_seed)
        task.success = False
        task.name = "OWR Random Test"
        task.mode = ""
        task.cmd = basecommand
        task_mapping.append(task)
    
    from tqdm import tqdm
    with tqdm(concurrent.futures.as_completed(task_mapping),
              total=len(task_mapping), unit="seed(s)",
              desc=f"Success rate: 0.00%") as progressbar:
        #with open("L:/_Work/Zelda/ROMs/Bug/Automate/_error_.txt", "a") as ff:
        #    ff.write("seed")
        for task in progressbar:
            dead_or_alive += 1
            try:
                result = task.result()
                if result.returncode:
                    errors.append([datetime.now(), result.stderr])
                    #print(result.stderr)
                    #print(result.stdout)
                else:
                    alive += 1
                    successes.append([datetime.now(), result.stderr])
                    task.success = True
            except Exception as e:
                with open("L:/_Work/Zelda/ROMs/Bug/Automate" + datetime.now().strftime("%y%m%d") + "/_error_.txt", "a") as ff:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    ff.write(exc_type)
                    ff.write(exc_tb.tb_lineno)
                raise e

            progressbar.set_description(f"Success rate: {(alive/dead_or_alive)*100:.2f}% - {task.name}{task.mode}")

    def get_results(testname: str):
        result = ""
        dead_or_alive = [task.success for task in task_mapping]
        alive = [x for x in dead_or_alive if x]
        success = f"Rate: {(len(alive) / len(dead_or_alive)) * 100:.2f}%"
        #successes.append(success)
        #print(success)
        result += f"{(len(alive)/len(dead_or_alive))*100:.2f}%\t"
        return result.strip()

    results = []
    results.append(get_results(""))

    #for result in results:
        #print(result)
        #successes.append(result)

    return successes, errors


if __name__ == "__main__":
    successes = []

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--count', default=1, type=lambda value: max(int(value), 1))
    parser.add_argument('--cpu_threads', default=cpu_threads, type=lambda value: max(int(value), 1))
    parser.add_argument('--help', default=False, action='store_true')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        exit(0)

    cpu_threads = args.cpu_threads

    args = argparse.Namespace()
    successes, errors = main(args=args)
    # if successes:
    #     successes += [""] * 2
    # successes += s
    # print()


    if errors:
        with open(f"L:/_Work/Zelda/ROMs/Bug/Automate/{datetime.now().strftime('%y%m%d')}/_error_{datetime.now().strftime('%y%m%d')}.txt", 'a') as stream:
            for error in errors:
                stream.write("Run at: " + error[0].strftime("%Y-%m-%d %H:%M:%S") + "\n")
                stream.write(error[1] + "\n\n")
                stream.write("----------------------------------------------------\n")

    if successes:
        with open(f"L:/_Work/Zelda/ROMs/Bug/Automate/{datetime.now().strftime('%y%m%d')}/_success_{datetime.now().strftime('%y%m%d')}.txt", 'a') as stream:
            for success in successes:
                stream.write("Run at: " + success[0].strftime("%Y-%m-%d %H:%M:%S") + "\n")
                stream.write(success[1] + "\n\n")
                stream.write("----------------------------------------------------\n")

    # with open(f"L:\\_Work\\Zelda\\ROMs\\Bug\\Automate\\{datetime.now().strftime('%y%m%d')}\\_success.txt", "w") as stream:
    #     stream.write(str.join("\n", successes))


    #conn = sqlite3.connect(f"L:/_Work/Zelda/ROMs/Bug/Automate/{datetime.now().strftime('%y%m%d')}/log.db")
    # conn.execute('''CREATE TABLE SEEDGEN
    #      (SEED           INT NOT NULL,
    #      MYSTERY        CHAR(10),
    #      SETTINGSCODE   CHAR(20) NOT NULL,
    #      VERSION        CHAR(10) NOT NULL,
    #      TIMESTAMP      INT NOT NULL,
    #      SUCCESS        INT,
    #      LOG            TEXT);''')

    #input("Press enter to continue")
    
    #conn.close()

    exit(0)
