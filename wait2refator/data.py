import pandas as pd
import json as js
import git
import requests
import time


class Response:

    def __init__(self):
        self.url = ""
        self.tokens = {
                'Authorization': 'token 502a45ccde8b2df5b39e01743f8929a593b56e1d',
                "Accept": "application/vnd.github.mercy-preview+json",
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                }

    def setUrl(self,url):
        self.url = url

    def run(self):
        if self.more():
            time.sleep(180)
            self.run()
        webpage = js.loads(requests.get(self.url,headers=self.tokens).content)
        return webpage

    def more(self):
        data = js.loads(requests.get("https://api.github.com/rate_limit", headers=self.tokens, timeout=None).content)
        check = data["resources"]["core"]["remaining"] <= 10
        return check

class Data:

    def __init__(self,name):
        self.name = name
        self.path = "/media/lofowl/SL-E1/2019_Summer_Project/repo5/"+name.replace("/","#")
        self.repo = None
        self.response = Response()
        self.response.setUrl("https://api.github.com/repos/"+name)
        self.webpage = self.response.run()
        self.data = {}

    def setName(self):
        self.data["name"] = self.name

    def checkFound(self):
        try:
            if self.webpage["message"] == "Not Found":
                return False
            else:
                return True
        except:
            return True

    def getRepo(self):
        self.repo = git.Repo.init(path=self.path+"/"+str(name.split("/")[1]))

    def contributors(self):
        contributors = self.repo.git.log(all=True,full_history=True,pretty="%an")
        contributors = contributors.split("\n")
        contributors = list(set(contributors))
        self.data["contributors"] = len(contributors)

    def commits(self):
        commits = self.repo.git.log(all=True,full_history=True,pretty="%an")
        commits = commits.split("\n")
        self.data["commits"] = len(commits)

    def ipynb_commits(self):
        ipynb_commits = self.repo.git.log("*.ipynb",all=True,full_history=True,no_merges=True,follow=True,pretty="%H")
        ipynb_commits = ipynb_commits.split("\n")
        self.data["commits_ipynb"] = len(ipynb_commits)

    def topic(self):
        url = "https://api.github.com/repos/"+self.name+"/topics"
        # TODO: pacakge the response
        tokens = {
                'Authorization': '502a45ccde8b2df5b39e01743f8929a593b56e1d',
                "Accept": "application/vnd.github.mercy-preview+json",
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
        topic = js.loads(requests.get(url,headers=tokens).content)
        self.data["topics"] = topic["names"]

    def description(self):
        self.data["descriptioin"] = self.webpage["description"]

    def forks(self):
        self.data["forks"] = self.webpage["forks_count"]

    def watch(self):
        self.data["watch"] = self.webpage["subscribers_count"]

    def stars(self):
        self.data["stars"] = self.webpage["stargazers_count"]

    def languages(self):
        self.response.setUrl("https://api.github.com/repos/"+self.name+"/languages")
        self.data["languages"] = self.response.run()

    def run(self):
        self.commits()
        self.ipynb_commits()
        self.contributors()
        self.topic()
        self.description()
        self.forks()
        self.watch()
        self.stars()
        self.languages()

    def save(self):
        with open(self.path+"/data.txt","w") as file:
            js.dump(self.data,file)


if __name__ == "__main__":
    path = "/media/lofowl/SL-E1/2019_Summer_Project/repo5/rsouza#MMD"
    repo = git.Repo.init(path="/media/lofowl/SL-E1/2019_Summer_Project/repo5/rsouza#MMD/MMD")
    a = Data("rsouza/MMD")
    a.run()
    a.save()

    # json_data["commits_count"] = get_all_commits(repos)
    # json_data["commits_ipynb_count"] = get_all_ipynb_commits(repos)
    # data = js.loads(response(url).content)
    # json_data["branch"] = info[1]
    # json_data["release"] = info[2]
    # json_data["contributors"] = info[3]
    # json_data["description"] = data["description"]
    # top = js.loads(response(url_topics).content)
    # json_data["topics"] = top["names"]
    # json_data["forks"] = data["forks_count"]
    # json_data["watch"] = data["subscribers_count"]
    # json_data["stars"] = data["stargazers_count"]
    # json_data["languages"] = js.loads(response(url_languages).content)
    #
    # json_data["create_time"] = get_last_commits_time(repos,repo)
    #
    #
    # url = "https://api.github.com/repos/"+name
    # url_con = url+"/contributors?page="
    # url_topics = url+"/topics"
    # url_languages = url+"/languages"
    #
    # check = True
    # url_web = "https://www.github.com/"+name
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # if sys.platform == "darwin":
    #     path = "/Volumes/SL-E1/2019_Summer_Project/code/codes_3/chromedriver"
    # else:
    #     path = "chromedriver"
    # broswer = webdriver.Chrome(path,chrome_options = chrome_options)
    # broswer.get(url_web)
    # html = broswer.page_source
    # doc = pq(html)
    # get_url = doc('.numbers-summary').items()
    # for i in get_url:
    #     i = i.remove_namespaces()
    #     info = i('span').text()
    # info = info.split()
    # if len(info) != 4:
    #     data = response(url_web)
    #     doc = pq(data.content)
    #     get_url = doc('.numbers-summary').items()
    #     for i in get_url:
    #         i = i.remove_namespaces()
    #         info = i('span').text()
    #     info = info.split()
    # broswer.close()
    # print("%s %s"%(name,info))
