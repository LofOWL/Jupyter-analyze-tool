import os
import subprocess

class git:

    def __init__(self,path):
        print(path)
        os.chdir(path)
        self.path = path
        self.ipynb_commit = "git log --pretty=%H --follow *.ipynb"
        self.commit_name_status = ""
        self.commit_parent = ""

    def set_commit_name_status(self,commit):
        self.commit_name_status = "git show "+str(commit)+" --name-status --pretty=\"\" "

    def set_commit_parent(self,commit):
        self.commit_parent = "git show "+str(commit)+" --name-status --pretty=\"raw\" "

    def run(self,commond):
        os.chdir(self.path)
        diff = subprocess.check_output(commond,shell=True)
        alist = diff.decode("utf-8").split("\n")
        return alist[:-1]
