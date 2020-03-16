import os

class Map:

    def __init__(self,path):

        class line:
            def __init__(self,word):
                self.data = word.split(",")[1]
                self.exist = True if self.data != '_' else False
                self.index = int(self.data.split(".")[2]) if self.exist else -1

        self.data = []

        with open(path,'r') as file:
            data = file.read()
            data = data.split("\n")[:-1]
            for i in data:
                a = line(i)
                if a.exist:
                    self.data.append(a.index)

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
    path = "/home/lofowl/Desktop/Map/0af84bb3744eaf6833eed5e0ded555e2d7331757#0.txt"
    a = Map(path)
