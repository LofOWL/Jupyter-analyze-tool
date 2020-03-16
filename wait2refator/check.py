from run import run
import os
from tqdm import tqdm

from multiprocessing import Pool
import multiprocessing


def process(name,Connect):
    Connect.copy(name)
    path = "/media/lofowl/SL-E1/2019_Summer_Project/repo6/"+name+"/"+name
    saveTo = "/media/lofowl/SL-E1/2019_Summer_Project/repo6/"+name
    repo = run(path,saveTo)
    try:
        # repo.run()
        repo.collectIpynb()
    except:
        os.system("rm -r "+path)
        os.system("rm -f "+saveTo+"/lhdiff_2019.jar")


def map(l,q,i):
    isNotFinish = True
    while isNotFinish:
        l.acquire()
        try:
            name = q.get(False)
        finally:
            l.release()
        try:
            path = "/media/lofowl/SL-E1/2019_Summer_Project/repo6/"+name
            saveTo = "/media/lofowl/SL-E1/2019_Summer_Project/repo6/"+name
            repo = run(path,saveTo)
            try:
                repo.processIpynb()
                print("done "+path+" on Process "+str(i))
            except:
                pass
        except:
            pass

        if isNotFinish:
            l.acquire()
            try:
                isNotFinish = False if q.qsize() == 0 else True
            finally:
                l.release()


if __name__ == "__main__":
    path = "/media/lofowl/SL-E1/2019_Summer_Project/repo6/"
    all_list = os.listdir(path)
    not_done_list = [ i for i in all_list if len(os.listdir(path+i)) > 4]

    manager = multiprocessing.Manager()
    q = manager.Queue()
    l = manager.Lock()
    [ q.put(i) for i in not_done_list]

    p = Pool(5)
    #multiprocessing.cpu_count()
    for i in range(5):
        p.apply_async(map, args=(l, q, i,))
    p.close()
    p.join()
