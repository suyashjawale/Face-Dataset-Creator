import io
from PIL import Image
import base64
from unidecode import unidecode
import urllib.request
from selenium import webdriver	 
import json
import time
import os
# from win32com.client import Dispatch
from zipfile import ZipFile
from bs4 import BeautifulSoup
import requests

class GetDataSet:
    def __init__(self,target,limit):
        target=target.strip()
        self.target=target.replace(" ","+")
        self.limit=limit
        if os.path.isfile('chromedriver.zip'):
            self.browser = webdriver.Chrome()
            self.getimages()
        else:
            getdriver()
            self.browser = webdriver.Chrome()

    def getimages(self):
        self.browser.get(f'https://www.google.co.in/search?q={self.target}&source=lnms&tbm=isch')
        time.sleep(5)
        self.browser.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]').click()
        time.sleep(4)
        j=0

        data=[]

        try:
            while(j<self.limit):
                img=self.browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')
                data.append(img.get_attribute('src'))
                time.sleep(1)
                self.browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[1]/a[2]').click()
                print(j)
                j=j+1
        except Exception as e:
            print("Exception 2")

        data=list(set(data))
        newdict=dict()
        j=1
        for i in data:
            newdict[j]=i
            j+=1
        newdata= json.dumps(newdict, indent = 4)
        with open("allimageurls.json", "w") as outfile:
            outfile.write(newdata)
        time.sleep(5)
        self.browser.close()
        self.browser.quit()
        print("Completed Dowloading")


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

def getdriver():
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    print(f"You are using Chrome Browser version {version}")
    version=version[:3]
    print("Please wait while we are looking a suitable version of chromedriver..")
    page = requests.get('https://chromedriver.chromium.org/downloads')
    soup=BeautifulSoup(page.text,'html.parser')
    anchor=soup.find_all('a')
    for i in anchor:
        if f"ChromeDriver {version}" in i.text:
            version=i.text
            break
    print(f"We have found {version} which is suitable for your machine.\nDownloading it now...")
    version=version.replace("ChromeDriver ","")
    urllib.request.urlretrieve(f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip","chromedriver.zip")
    print("Extracting files..")
    with ZipFile("chromedriver.zip", 'r') as zip:
        zip.extractall()
    print("Setup is completed.")



GetDataSet("Rashmika Mandanna Beautiful",550)
