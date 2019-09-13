import requests
import json
from bs4 import BeautifulSoup
import urllib.request
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

begin = input("Begin at: (issue)")
ind = 1
for i in range(int(begin), 4974):
    print("Downloading issue:%s" %i)
    resp = None
    data = None
    jsonSuccess = False
    while not jsonSuccess:
        try:
            resp = requests.get("https://www.akuankka.fi/api/v2/issues/%s?stories-full=1" %i)
            data = json.loads(resp.text)
            jsonSuccess = True
        except:
            print("JSON Error in issue %s" %i)
    for story in data["stories"]:
        author = None
        authorSuccess = False
        try:
            author = story['artists'][0]['name']
            authorSuccess = True
        except:
            print("Skipped author")
        if authorSuccess:
            if(author == "Carl Barks" or author == "Don Rosa"):
                authorDir = dir_path + r'\Aku Ankka - ' + author
                if not os.path.exists(authorDir):
                    os.makedirs(authorDir)
                title = str(ind) + story["title"]
                dir = r'\AKU ' + title.translate({ord('"'): None}).translate({ord('?'): None})
                if not os.path.exists(authorDir + dir):
                    os.makedirs(authorDir + dir)
                for index, page in enumerate(story["pages"]):
                    name = title + " "+ str(index)
                    print("Downloading " + name)
                    print(dir + "\\" + name + ".jpg")
                    success = False
                    failCounter = 0
                    while not success and failCounter < 15:
                        try:
                            urllib.request.urlretrieve("https://akuankka.fi" + page["images"]["default"]["url"], authorDir + dir + "\\" + name + ".jpg")
                            print("Sucessfully fetched " + name + "\n" + "------------\n")
                            success = True
                        except:
                            print("Failed to download %s" %i)
                            failCounter = failCounter + 1
    print("Downloaded issue:%s" %i)