import os
import shutil

folder_from = "/media/lofowl/My Passport/notebook_data/notebooks"
folder_to = "/media/lofowl/SL-E1/2019_Summer_Project/repo6"

jar = "/media/lofowl/SL-E1/2019_Summer_Project/lhdiff_2019.jar"

class connecter:

    def __init__(self,folder_from=folder_from,folder_to=folder_to,jar=jar):
        self.folder_from = folder_from
        self.folder_to = folder_to
        self.jar = jar

    def copy(self,name):
        shutil.copytree(self.folder_from+"/"+name,self.folder_to+"/"+name+"/"+name+".git")
        # shutil.copy(self.jar,self.folder_to+"/"+name)
        os.chdir(self.folder_to+"/"+name)
        os.system("git clone "+name+".git "+name)
        os.system("rm -rf "+name+".git")

    def getJarTool(self,path):
        shutil.copy(self.jar,path)

if __name__ == "__main__":
    Connect = connecter()
    Connect.copy("1373319")
