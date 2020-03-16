import pandas as pd
import numpy as np
import os

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType

from pyquery import PyQuery as pq

from tqdm import tqdm

import time

from multiprocessing import Pool

from data import Data

class Broswer:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.broswer = webdriver.Chrome("chromedriver", chrome_options = chrome_options)
        # self.broswer = webdriver.Chrome("chromedriver")
        self.url = ""
        self.dict = {}
        self.isNotDoneL = True
        self.isNotDoneT = True

    def set(self,url):
        self.url = "https://www.github.com/"+url.split("/")[-2]+"/"+url.split("/")[-1]
        self.dict = {}
        self.dict["repo"] = self.url
        self.broswer.get(self.url)
        self.isNotDoneL = True
        self.isNotDoneT = True

    def getL(self):
        html = self.broswer.page_source
        doc = pq(html)
        get_url = doc('.numbers-summary').items()
        isTouch = False
        for i in get_url:
            i = i.remove_namespaces()
            info = i('a').text()
            isTouch = True
        if isTouch:
            info = info.split()
            self.isNotDoneL = True if "Fetching" in info else False
            if not(self.isNotDoneL):
                for i in range(0,len(info),2):
                    try:
                        self.dict[info[i+1]] = info[i]
                    except:
                        pass
        else:
            self.isNotDoneL = False

    def getT(self):
        html = self.broswer.page_source
        doc = pq(html)
        get_url = doc('.pagehead-actions').items()
        isTouch = False
        for i in get_url:
            i = i.remove_namespaces()
            info = i('a').text()
            isTouch = True
        if isTouch:
            info = info.split()
            self.isNotDoneT = True if "Fetching" in info else False
            if not(self.isNotDoneT):
                for i in range(0,len(info),2):
                    try:
                        self.dict[info[i]] = info[i+1]
                    except:
                        pass
        else:
            self.isNotDoneT = False

    def collect(self):
        self.getL()
        while self.isNotDoneL:
            self.getL()
            self.broswer.get(self.url)
        self.getT()
        while self.isNotDoneT:
            self.getT()
            self.broswer.get(self.url)

class Table:

    def __init__(self):
        self.data =  pd.read_csv("jupyter_notebook_projects_not_forked_not_deleted.csv")

    def divide(self):
        length = len(self.data["url"])
        division = int(len(self.data["url"]) / 5)
        division_list = []
        end = 0
        while end < length:
            child = []
            division_list.append([end,end+division-1])
            end = end+division

        result_list = []
        index = 0
        for i,j in division_list:
            child = []
            data = self.data.loc[i:j]
            result_list.append([data,index])
            index += 1

        return result_list

    def getList(self,data):
        url_list = list(data["url"])
        length = len(url_list)
        return length, url_list

    def save(self,result,index):
        table = pd.DataFrame(data=result)
        table.to_csv("result0_"+str(index)+".csv",index=0)

    def run(self,input):
        data = input[0]
        index = input[1]
        print(index)
        b = Broswer()
        length, url_list = self.getList(data)
        result_list = []
        for i in tqdm(range(length)):
            b.set(url_list[i])
            b.collect()
            result_list.append(b.dict)
            print("%s %s done"%(str(index),url_list[i]))
        self.save(result_list,index)

    def test(self,num):
        b = Broswer()
        length, url_list = self.getList()
        b.set(url_list[num])
        b.collect()
        print(b.dict)

if __name__ == "__main__":
    data = pd.read_csv("jupyter_notebooks_2_contributors_10_commits.csv")
    url = list(data["project_url"])
    result_list = []
    for i in tqdm(range(len(url))):
        a = Data(url[i])
        a.setName()
        if a.checkFound():
            a.stars()
            a.languages()
        result_list.append(a.data)
    table = pd.DataFrame(data=result_list)
    table.to_csv("result28.csv",index=0)
    print(table)
