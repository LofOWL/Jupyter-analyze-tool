import os
import threading
from threading import Timer
from subprocess import STDOUT, check_output
import subprocess

import json as js

#Setting: need lhdiff_2019.jar in the current folder

# input:
# current "/home/lofowl/Desktop"
# save "/97d7bf2dd641394f65b307bdec96db0698c74015#0.txt"
# parent "97d7bf2dd641394f65b307bdec96db0698c74015#0#p.txt"
# child "97d7bf2dd641394f65b307bdec96db0698c74015#0#c.txt"

# output:
# map files

class Diff:

    def __init__(self,**data):
        self.current = data["current"]

        self.element = data["element"]
        self.savePath = "/" + self.element.id
        self.parentPath = self.element.new_parent_path
        self.childPath = self.element.new_child_path

    def callJava(self):
        commond = "java -jar lhdiff_2020.jar child.txt parent.txt"
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


    def diff(self):

        os.chdir(self.current)

        isDiff = True
        diff = self.callJava()

        diff = diff.decode("utf-8").split("\n")
        diff = diff[1:]

        if len(diff) == 1:
            raise Exception('empty')

        parent = Diff.mapFile(self.parentPath)

        child = Diff.mapFile(self.childPath)

        diff = [ list(map(lambda x: x,x.split(","))) for x in diff if "," in x ]
        diff = [ [str(child.block(i[0])),str(parent.block(i[1])),str(i[2] if len(i) == 3 else 1)] for i in diff ]
        diff = [ [i[0],i[1], i[2] if i[1] != "_" else "0"] for i in diff]


        exist_list = []
        for i in diff:
            lin = Diff.line(i)
            lin.parent()
            if lin.exist:
                exist_list.append(lin.index)

        missing_index = [ i for i in range(1,parent.totalLength+1) if not(i in exist_list)]

        missing_data = [ "_,"+parent.block(i)+",0" for i in missing_index]

        missing_data = [i.split(",") for i in missing_data]

        diff = diff + missing_data
        diff.sort(key=lambda x: Diff.line(x).child())

        with open(self.current+self.savePath,"w") as text:
            for i in diff:
                text.write(",".join(i)+"\n")

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
            self.totalLength = sum([ i["linesLength"] for i in data])

        def block(self,index):
            if index == "_":
                return "_"
            else:
                data = [ (x,j[0]) for x,j in enumerate(self.interval) if j[0] <= int(index) and int(index) <= j[1] ]
                block = data[0][0]+1
                block_index = (int(index) - int(data[0][1]))+1
                return str(block)+"."+str(block_index)+"."+str(index)

    class line:

        def __init__(self,word):
            self.word = word
            self.data = None
            self.exist = None
            self.index = None

        def parent(self):
            self.data = self.word[1]
            self.exist = True if self.data != '_' else False
            self.index = int(self.data.split(".")[2]) if self.exist else -1
            return self.index

        def child(self):
            self.data = self.word[0]
            self.exist = True if self.data != '_' else False
            self.index = int(self.data.split(".")[2]) if self.exist else -1
            return self.index


if __name__ == "__main__":
    child = "97d7bf2dd641394f65b307bdec96db0698c74015#0#c.txt"
    parent = "97d7bf2dd641394f65b307bdec96db0698c74015#0#p.txt"
    current = "/home/lofowl/Desktop"
    save = "/97d7bf2dd641394f65b307bdec96db0698c74015#0.txt"
    diff = Diff(child=child,parent=parent,current=current,save=save)
    diff.diff()
