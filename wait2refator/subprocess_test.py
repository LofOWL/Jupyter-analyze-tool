import subprocess
from threading import Thread, Event

import os

def kill_on_timeout(done, timeout, proc):
    if not done.wait(timeout):
        proc.kill()

def exec_command(command, timeout):

    done = Event()
    os.chdir("/home/lofowl/Desktop/test/")
    print(os.listdir())
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    watcher = Thread(target=kill_on_timeout, args=(done, timeout, proc))
    watcher.daemon = True
    watcher.start()

    data, stderr = proc.communicate()
    done.set()

    return data, stderr, proc.returncode

if __name__ == "__main__":
    os.chdir("/home/lofowl/Desktop/test/")
    commond = "java -jar lhdiff_2019.jar child.txt parent.txt"
    try:
        data = subprocess.call(commond, timeout=3, shell=True)
        print(data)
    except:
        print("d")
