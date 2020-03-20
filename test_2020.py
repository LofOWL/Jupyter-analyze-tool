import os
import pandas as pd
import numpy as np
import json as js

import sys


from Diff import Diff

class Folder:

    def __init__(self, path):
        self.path = path
        self.__init_transfer_data()
        self.__init_download_data()

    def __init_transfer_data(self):
        pa = pd.read_csv(self.path+"/result1.csv")
        self.transfer_data = pa

    def __init_download_data(self):
        pa = pd.read_csv(self.path+"/result.csv")
        self.download_data = pa

    def createElement(self,id):
        return Folder.Element(self,id)


    class Element:

        def __init__(self,parent,id):
            self.path = parent.path
            self.id = id
            self.__init_new_path()
            self.__init_old_path()

        def __init_new_path(self):
            self.new_parent_path = self.path + "/New/" + self.id +"#p.txt"
            self.new_child_path = self.path + "/New/" + self.id +"#c.txt"

        def __init_old_path(self):
            self.old_parent_path = self.path + "/Old/" + self.id +"#p.ipynb"
            self.old_child_path = self.path + "/Old/" + self.id + "#c.ipynb"

        def get_new_parent_data(self):
            with open(self.new_parent_path,"r") as data:
                return js.loads(data.read())

        def create_new_parent_data_txt(self,savePath):
            data = self.get_new_parent_data()
            new_list_cells = [x['lines'] for x in data]
            new_index_dict = {x:len(new_list_cells[x]) for x in range(len(new_list_cells))}
            new_output = [y.replace("\n","") for x in new_list_cells for y in x ]
            with open(savePath+"/parent.txt","w") as data:
                for i in new_output:
                    data.write(i+"\n")

            self.java_tool_path = savePath
            self.parent_txt = savePath + "/parent.txt"


        def get_new_child_data(self):
            with open(self.new_child_path,"r") as data:
                return js.loads(data.read())

        def create_new_child_data_txt(self,savePath):
            data = self.get_new_child_data()
            new_list_cells = [x['lines'] for x in data]
            new_index_dict = {x:len(new_list_cells[x]) for x in range(len(new_list_cells))}
            new_output = [y.replace("\n","") for x in new_list_cells for y in x ]
            with open(savePath+"/child.txt","w") as data:
                for i in new_output:
                    data.write(i+"\n")

            self.java_tool_path = savePath
            self.child_txt = savePath + "/child.txt"

        def get_old_parent_data(self):
            with open(self.old_parent_path,"r") as data:
                return data.read()

        def get_old_child_data(self):
            with open(self.old_child_path,"r") as data:
                return data.read()


        def __str__(self):
            return f'''folder path: {self.path}
id: {self.id}
new_parent_path: {self.new_parent_path}
new_child_path: {self.new_child_path}
old_parent_path: {self.old_parent_path}
old_child_path: {self.old_child_path}'''


if __name__ == "__main__":
    repo = Folder("/home/lofowl/Desktop/10118245_0")
    test = repo.transfer_data
    test = test[test["id"] == "aa247965158316f7560f990ee5c9f8a73d4e628a#0"]
    print(test)
    filter_list = repo.transfer_data[repo.transfer_data["status"] == "diff-error"]

    id = list(filter_list["id"])
    n_id = [ repo.createElement(i) for i in id]

    select_n = [ i for i in n_id if i.id == '9e54faf891f9c2fea00673c6d5d5cb25d4986c7e#0']

    error_n = select_n[0]
    print(error_n.get_new_child_data())
    print(error_n.get_old_child_data())
    current = "/home/lofowl/Desktop/Jupyter-analyze-tool"

    error_n.create_new_parent_data_txt(current)
    error_n.create_new_child_data_txt(current)

    diff = Diff(error_n)
    diff.diff()

    # index = int(sys.argv[1])
    # element = n_id[index]

    # current = "/home/lofowl/Desktop/Jupyter-analyze-tool"
    # for element in n_id:
    #     print(element)
    #     element.create_new_parent_data_txt(current)
    #     element.create_new_child_data_txt(current)
    #
    #     len_child = len(element.get_new_child_data())
    #     len_parent = len(element.get_new_parent_data())
    #     print(f"child: {len_child} parent: {len_parent}")
    #
    #     diff = Diff(element)
    #     diff.diff(save_path="/home/lofowl/Desktop/Jupyter-analyze-tool/test")
