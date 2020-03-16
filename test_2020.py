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

        def create_new_parent_data_txt(self):
            data = self.get_new_parent_data()
            new_list_cells = [x['lines'] for x in data]
            new_index_dict = {x:len(new_list_cells[x]) for x in range(len(new_list_cells))}
            new_output = [y.replace("\n","") for x in new_list_cells for y in x ]
            with open("parent.txt","w") as data:
                for i in new_output:
                    data.write(i+"\n")


        def get_new_child_data(self):
            with open(self.new_child_path,"r") as data:
                return js.loads(data.read())

        def create_new_child_data_txt(self):
            data = self.get_new_child_data()
            new_list_cells = [x['lines'] for x in data]
            new_index_dict = {x:len(new_list_cells[x]) for x in range(len(new_list_cells))}
            new_output = [y.replace("\n","") for x in new_list_cells for y in x ]
            with open("child.txt","w") as data:
                for i in new_output:
                    data.write(i+"\n")

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
    filter_list = repo.transfer_data[repo.transfer_data["status"] != "success"]

    id = list(filter_list["id"])
    n_id = [ repo.createElement(i) for i in id]

    index = int(sys.argv[1])
    element = n_id[index]
    element.create_new_parent_data_txt()
    element.create_new_child_data_txt()

    len_child = len(element.get_new_child_data())
    len_parent = len(element.get_new_parent_data())
    print(f"child: {len_child} parent: {len_parent}")

    current = "/home/lofowl/Desktop/Jupyter-project-tool"
    diff = Diff(element=element,current=current)
    diff.diff()
