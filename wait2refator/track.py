import pandas as pd
import numpy as np
import os
import json as js

import subprocess
import ast

class TrackTool:

    def __init__(self,new,old):
        with open(new,"r") as data:
            self.newIpynb = js.loads(data.read())

        with open(old,"r") as data:
            self.oldIpynb = js.loads(data.read())

        self.isNew = 0
        self.isOld = 1

        self.newIpynbIndex = None
        self.oldIpynbIndex = None
        self.diff = None

        self.oldInterval = None
        self.newInterval = None
        self.mapInterval = None

        self.moveList = None
        self.mergeList = None

    def create(self):
        def toTxt(data,name,type):
            def interval_list(alist):
                def getIndex(index_dict,index):
                    lastIndex = sum([index_dict[x] for x in range(index+1)])
                    firstIndex = lastIndex - index_dict[index] + 1
                    return [firstIndex,lastIndex]
                return [ [x for x in range(getIndex(alist,index)[0],getIndex(alist,index)[1]+1)] for index,values in alist.items() if values != 0]

            list_cells = [x['source'] for x in data['cells']]
            if type == self.isNew:
                self.newIpynbIndex = {x:len(list_cells[x]) for x in range(len(list_cells))}
                self.newInterval = interval_list(self.newIpynbIndex)
            else:
                self.oldIpynbIndex = {x:len(list_cells[x]) for x in range(len(list_cells))}
                self.oldInterval = interval_list(self.oldIpynbIndex)

            output = [y.replace("\n","") for x in list_cells for y in x ]
            with open("/home/lofowl/Desktop/Tool/"+name,"w") as data:
                for i in output:
                    data.write(i+"\n")
        toTxt(self.newIpynb,"new.txt",self.isNew)
        toTxt(self.oldIpynb,"old.txt",self.isOld)

    def createMove(self):
        def function_map(x):
            return self.diff[x-1][1]
        def math_find(map_interval,new_interval):
            def math_cell(a,b):
                a = set(a)
                b = set(b)
                if (a & b):
                    return True
                else:
                    return False

            move_list = []
            for i in range(len(map_interval)):
                child_list = []
                target_cell = map_interval[i]
                math = [ math_cell(target_cell,x) for x in new_interval]
                math_index = [ i+1 for i,e in enumerate(math) if e==True]
                move_list.append([i+1,math_index])
            return move_list
        map_interval = [ list(map(lambda x: function_map(x),x)) for x in self.oldInterval ]
        new_interval = [ list(map(lambda x: str(x),x)) for x in self.newInterval]
        self.moveList = math_find(map_interval,new_interval)

    def mapping(self):
        os.chdir("/home/lofowl/Desktop/Tool")
        commond = "java -jar lhdiff.jar old.txt new.txt"
        diff = subprocess.check_output(commond,shell=True)
        diff = diff.decode("utf-8").split("\n")
        self.diff = [ list(map(lambda x: x,x.split(","))) for x in diff if "," in x ]

    def createMerge(self):
        cell_list = [str(x[1]) for x in self.moveList]
        merge_list = []

        for i in list(set(cell_list)):
            child_list = [e[0] for e in self.moveList if str(e[1]) == i]
            if len(child_list) >= 2:
                merge_list.append([child_list,ast.literal_eval(i)])
        self.mergeList = merge_list

    def run(self):
        self.create()
        self.mapping()
        self.createMove()
        self.createMerge()

    def saveMove(self,path):
        with open(path,"w") as data:
            for i in self.moveList:
                data.write(str(i[0])+"-"+",".join([str(j) for j in i[1]])+"\n")

    def saveMerge(self,path):
        with open(path,"w") as data:
            for i in self.mergeList:
                if i[1] != []:
                    data.write(",".join([str(j) for j in i[0]])+"-"+str(i[1][0])+"\n")

if __name__ == "__main__":
    t = TrackTool("/home/lofowl/Desktop/reasearch/new.ipynb","/home/lofowl/Desktop/reasearch/old.ipynb")
    t.run()
    t.saveMove("/home/lofowl/Desktop/move1.txt")
    t.saveMerge("/home/lofowl/Desktop/merge1.txt")
