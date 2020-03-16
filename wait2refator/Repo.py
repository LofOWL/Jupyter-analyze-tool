import pandas as pd
import numpy as np
import os

from gitCom import git


import json as js

import subprocess
import ast

from shutil import copyfile

from multiprocessing import Process, Queue
import multiprocessing

import time

import threading

from threading import Timer

from subprocess import STDOUT, check_output

class Repo:

    def __init__(self,filePath,saveTo):
        self.repos = git(filePath)
        self.filePath = filePath
        self.savePath = saveTo

    def createFolder(self):
        os.chdir(self.savePath)
        os.mkdir("New")
        os.mkdir("Old")
        os.mkdir("Map")

    def createFolder_ipynb(self):
        os.chdir(self.savePath)
        os.mkdir("Old")

    def createFolder_map(self):
        os.chdir(self.savePath)
        try:
            os.mkdir("Map")
            os.mkdir("New")
        except:
            pass

    def havingM(self,commit):
        self.repos.set_commit_name_status(commit)
        check = self.repos.run(self.repos.commit_name_status)

        lists = []
        for i in check:
            i = i.split()
            lists.append(i[0])
        return "M" in lists

    def createList(self,commit):
        self.repos.set_commit_parent(commit)
        sha = self.repos.run(self.repos.commit_parent)

        parent_sha = ""
        for i in sha:
            if "parent" in i:
                i = i.split()
                parent_sha = i[1]
                break
        return [parent_sha,commit]

    def files(self,commit):
        self.repos.set_commit_name_status(commit[1])
        commit_details = self.repos.run(self.repos.commit_name_status)
        commit_list = [x.split("\t") for x in commit_details]
        filter_commit_files = [x[1] for x in commit_list if ".ipynb" in x[1] and "M" == x[0]]
        return filter_commit_files

    def getList(self):
        alist = self.repos.run(self.repos.ipynb_commit)
        commit_list = []
        for i in alist:
            if self.havingM(i):
                commit_list.append(self.createList(i))
        return commit_list


class Files:

    def __init__(self,fileName,index,currentIndex,parentIndex,path,savePath):
        self.fileName = fileName
        self.index = index
        self.currentIndex = currentIndex
        self.currentPath = ""
        self.currentMapPath = ""
        self.currentCheck = 0
        self.parentIndex = parentIndex
        self.parentPath = ""
        self.parentMapPath = ""
        self.parentCheck = 0
        self.path = path

        self.savePath = savePath

    def correct(self):
        if self.currentCheck == 1 and self.parentCheck == 1:
            return True
        else:
            return False

    def saveOriginalFile(self):
        child = self.saveChildFile()
        parent = self.saveParentFile()
        if self.correct():
            return True
        else:
            os.system("rm -rf "+self.savePath+"/Old/"+self.currentIndex+"#"+str(self.index)+"#c.ipynb")
            os.system("rm -rf "+self.savePath+"/Old/"+self.parentIndex+"#"+str(self.index)+"#p.ipynb")
            return False

    def saveNewMapfile(self):
        self.mapNewFile(self.currentPath,"c")
        self.mapNewFile(self.parentPath,"p")

    def createPath(self):
        self.currentPath = "/Old/"+self.currentIndex+"#"+str(self.index)+"#c.ipynb"
        self.parentPath = "/Old/"+self.currentIndex+"#"+str(self.index)+"#p.ipynb"

    def mapNewFile(self,files,types):
        with open(self.savePath+files) as text:
            data = js.loads(text.read())
        saveTo = self.savePath+"/New/"
        block = 0
        start = 0
        list_result = []
        if "cells" in data.keys():
            lines = data['cells']
        else:
            lines = data["worksheets"][0]["cells"]
        for i in lines:
            if "source" in i.keys():
                info = {}
                info["block"] = block
                block += 1
                info['type'] = i['cell_type']
                lines = i['source']
                linesLength = len(i['source'])
                info['linesLength'] = linesLength
                if start == 0:
                    info['startIndex'] = 0
                else:
                    info['startIndex'] = start
                start = start + linesLength
                info['lines'] = lines
                list_result.append(info)
        if types == "c":
            self.currentMapPath = self.savePath+"/New/"+self.currentIndex+"#"+str(self.index)+"#"+types+".txt"
        else:
            self.parentMapPath = self.savePath+"/New/"+self.currentIndex+"#"+str(self.index)+"#"+types+".txt"
        with open(saveTo+self.currentIndex+"#"+str(self.index)+"#"+types+".txt","w") as text:
            js.dump(list_result,text)

    def saveChildFile(self):
        os.chdir(self.path)
        os.system("git checkout %s"%self.currentIndex)
        src = self.path+"/"+self.fileName
        with open(src,"r") as text:
            try:
                a = js.loads(text.read())
                self.currentCheck = 1
                dst = self.savePath+"/Old/"+self.currentIndex+"#"+str(self.index)+"#c.ipynb"
                self.currentPath = "/Old/"+self.currentIndex+"#"+str(self.index)+"#c.ipynb"
                copyfile(src, dst)
                return True
            except:
                self.currentCheck = -1
                return False

    def saveParentFile(self):
        os.chdir(self.path)
        os.system("git checkout %s"%self.parentIndex)
        src = self.path+"/"+self.fileName
        with open(src,"r") as text:
            try:
                a = js.loads(text.read())
                self.parentCheck = 1
                dst = self.savePath+"/Old/"+self.currentIndex+"#"+str(self.index)+"#p.ipynb"
                self.parentPath = "/Old/"+self.currentIndex+"#"+str(self.index)+"#p.ipynb"
                copyfile(src, dst)
                return True
            except:
                self.parentCheck = -1
                return False

    def createParentFile(self):
        with open(self.savePath+self.parentPath,"r") as data:
            try:
                data = js.loads(data.read())
                self.createTxt(data,"parent.txt")
                return True
            except:
                return False

    def createCurrentFile(self):
        with open(self.savePath+self.currentPath,"r") as data:
            try:
                data = js.loads(data.read())
                self.createTxt(data,"child.txt")
                return True
            except:
                return False

    def createTxt(self,data,name):
        if 'cells' in data.keys():
            new_list_cells = [x['source'] for x in data['cells']]
        else:
            new_list_cells = [x['source'] for x in data["worksheets"][0]['cells'] if 'source' in x.keys()]
        new_index_dict = {x:len(new_list_cells[x]) for x in range(len(new_list_cells))}
        new_output = [y.replace("\n","") for x in new_list_cells for y in x ]
        with open(self.savePath+"/"+name,"w") as data:
            for i in new_output:
                data.write(i+"\n")


    def diff(self):

        class mapFile:

            def __init__(self,path):
                with open(path) as data:
                    data = js.loads(data.read())
                start = data[0]["startIndex"]
                result = []
                for i in data:
                    result.append([start+1,start+i["linesLength"]])
                    start = start+i["linesLength"]
                self.interval = result

            def block(self,index):
                if index == "_":
                    return "_"
                else:
                    data = [ (x,j[0]) for x,j in enumerate(self.interval) if j[0] <= int(index) and int(index) <= j[1] ]
                    block = data[0][0]+1
                    block_index = (int(index) - int(data[0][1]))+1
                    return str(block)+"."+str(block_index)+"."+str(index)

        def callJava():
            commond = "java -jar lhdiff_2019.jar child.txt parent.txt"
            env = dict(os.environ)
            env['JAVA_OPTS'] = 'foo'

            kill = lambda process: process.kill()
            ping = subprocess.Popen(commond.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,env=env)
            my_timer = Timer(3, kill, [ping])
            result = ""
            try:
                my_timer.start()
                a,b = ping.communicate()
                result = a
            finally:
                my_timer.cancel()
            return result


        self.createParentFile()
        self.createCurrentFile()
        os.chdir(self.savePath)

        isDiff = True
        diff = callJava()

        diff = diff.decode("utf-8").split("\n")
        diff = diff[1:]

        if len(diff) == 1:
            raise Exception('empty')

        parent = mapFile(self.parentMapPath)

        child = mapFile(self.currentMapPath)

        diff = [ list(map(lambda x: x,x.split(","))) for x in diff if "," in x ]

        diff = [ [str(child.block(i[0])),str(parent.block(i[1])),str(i[2] if len(i) == 3 else 1)] for i in diff ]

        diff = [ [i[0],i[1], i[2] if i[1] != "_" else "0"] for i in diff]

        with open(self.savePath+"/Map/"+self.currentIndex+"#"+str(self.index)+".txt","w") as text:
            for i in diff:
                text.write(",".join(i)+"\n")


if __name__ == "__main__":
    path = "/home/lofowl/Desktop/reasearch/MMD"
    repo = Repo("/home/lofowl/Desktop/reasearch/MMD")
    alist = repo.getList()
    result = []
    for i in alist:
        files = repo.files(i)
        index = 0
        for j in files:
            file = Files(j,index,i[1],i[0],"/home/lofowl/Desktop/reasearch/MMD")
            try:
                if file.saveOriginalFile():
                    try:
                        file.saveNewMapfile()
                        file.diff()
                        result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"success"])
                    except:
                        result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"no-cells"])
                else:
                    result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"conflict"])
            except:
                result.append([file.currentIndex+"#"+str(file.index),file.fileName,file.currentIndex,file.parentIndex,"files-not-found"])
            index += 1
    pa = pd.DataFrame(data=result,columns=["id","filename","current_commit","parent_commit","status"])
    pa.to_csv("/home/lofowl/Desktop/Data/result.csv",index=0)
