import json as js


class Old2New:

    def __init__(self,**data):
        self.old_path = data["old_path"]
        self.new_path = data["new_path"]
        self.__init_load_old_data()

    def __init_load_old_data(self):
        with open(self.old_path) as text:
            self.old_data = js.loads(text.read())


    def map(self):
        block = 0
        start = 0
        list_result = []
        if "cells" in self.old_data.keys():
            lines = self.old_data['cells']
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
        else:
            lines = self.old_data["worksheets"][0]["cells"]
            for i in lines:
                if "input" in i.keys():
                    info = {}
                    info["block"] = block
                    block += 1
                    info['type'] = i['cell_type']
                    lines = i['input']
                    linesLength = len(i['input'])
                    info['linesLength'] = linesLength
                    if start == 0:
                        info['startIndex'] = 0
                    else:
                        info['startIndex'] = start
                    start = start + linesLength
                    info['lines'] = lines
                    list_result.append(info)
        with open(self.new_path,"w") as text:
            js.dump(list_result,text)

if __name__ == "__main__":
    old_path = "/home/lofowl/Desktop/10118245_0/Old/9e54faf891f9c2fea00673c6d5d5cb25d4986c7e#0#c.ipynb"
    new_path = "/home/lofowl/Desktop/test/test.txt"
    test = Old2New(old_path=old_path,new_path=new_path)
    test.map()
