from Repo import Repo,Files
import pandas as pd
import numpy as np
import os
from connecter import connecter
from tqdm import tqdm

class run:

    def __init__(self,path,saveTo):
        self.path = path
        self.saveTo = saveTo


    def processIpynb(self):
        pa = pd.read_csv(self.path+"/result.csv")
        pa = pa[pa["status"] == "success"]
        pa = np.array(pa)
        repo = Repo(self.path,self.saveTo)
        repo.createFolder_map()
        c = connecter()
        c.getJarTool(self.saveTo)
        result = []
        for i in tqdm(pa):
            index = i[0].split("#")[1]
            file = Files(i[1],index,i[2],i[3],self.path,self.saveTo)
            file.createPath()
            try:
                file.saveNewMapfile()
                try:
                    file.diff()
                    result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"success"])
                except:
                    result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"diff-error"])
            except:
                result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"no-cells"])

        # remove old files
        os.chdir(self.saveTo)
        os.system("rm -r Old")
        os.system("rm -f lhdiff_2019.jar")
        os.system("rm -f child.txt")
        os.system("rm -f parent.txt")

        pa = pd.DataFrame(data=result,columns=["id","filename","current_commit","parent_commit","status"])
        pa.to_csv(self.saveTo+"/result1.csv",index=0)

    def collectIpynb(self):
        repo = Repo(self.path,self.saveTo)
        repo.createFolder_ipynb()
        alist = repo.getList()
        result = []
        for i in alist:
            files = repo.files(i)
            index = 0
            for j in files:
                file = Files(j,index,i[0],i[1],self.path,self.saveTo)
                try:
                    if file.saveOriginalFile():
                        result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"success"])
                    else:
                        result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"conflict"])
                except:
                    result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"files-not-found"])
                index += 1
        pa = pd.DataFrame(data=result,columns=["id","filename","current_commit","parent_commit","status"])
        pa.to_csv(self.saveTo+"/result.csv",index=0)
        os.system("rm -r "+self.path)

    def run(self):
        repo = Repo(self.path,self.saveTo)
        repo.createFolder()
        alist = repo.getList()
        result = []
        for i in alist:
            files = repo.files(i)
            index = 0
            for j in files:
                file = Files(j,index,i[0],i[1],self.path,self.saveTo)
                try:
                    if file.saveOriginalFile():
                        try:
                            file.saveNewMapfile()
                            try:
                                file.diff()
                                result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"success"])
                            except:
                                result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"diff-error"])
                        except:
                            result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"no-cells"])
                    else:
                        result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"conflict"])
                except:
                    result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"files-not-found"])
                index += 1
        pa = pd.DataFrame(data=result,columns=["id","filename","current_commit","parent_commit","status"])
        pa.to_csv(self.saveTo+"/result.csv",index=0)

        os.chdir(self.saveTo)
        os.system("rm -f lhdiff_2019.jar")
        os.system("rm -f parent.txt")
        os.system("rm -f child.txt")
        os.system("rm -r "+self.path)
