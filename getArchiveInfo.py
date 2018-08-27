import subprocess
import os
import urllib
import sys
import requests
import util
import time

reload(sys)
sys.setdefaultencoding("utf-8")
   
def readtoken(tokenfile):
    with open(tokenfile) as f:
        for line in f:
            tokens = line.split(" ")[0]
    return tokens
def getInfoFromFixCommit(apiinfor,fixcommit,eachPairPath,apiurl):
    message = apiinfor["commit"]["message"]
    author = apiinfor["commit"]["author"]["name"]
    commiter = apiinfor["commit"]["committer"]["name"]
    date = apiinfor["commit"]["author"]["date"]
    bugcommits = apiinfor["parents"]
    bugs = bugcommits[0]        
    with open(eachPairPath + "/archiveInfo.txt",'a') as infoPath: 
        bugcommit = bugs["sha"]
        infoPath.write("Project url:" + apiurl + "\n")   
        infoPath.write("Buggy-version:" + bugcommit + "\n")
        infoPath.write("Fixed-version:" + fixcommit + "\n")
        infoPath.write("Fixed commit message:" + message + "\n")
        infoPath.write("Date:" + date + "\n")
        infoPath.write("Author:" + author + "\n")
        infoPath.write("Commiter:" + commiter + "\n")

            
            
partation = sys.argv[1]
tokenNumber = sys.argv[2]

tokenfile = "/media/disk2/Xia/GitHubProjects/3Clone/readtokens/" + tokenNumber + ".txt"
tokens = readtoken(tokenfile)
print(tokens)

bugPath = "/media/disk2/Xia/GitHubProjects/2Parse/partations/NewFull2011-2017/" + partation + ".txt"
clonerootPath = "/media/disk2/Xia/GitHubProjects/3Clone/NewFull2011-2017/" 
clonePath = clonerootPath + "/" + partation

path = bugPath
with open(path,'r') as file:
    count = 1 
    pairCount = 1     
    for line in file:           
        url = line.split(" ")[0]
        fixcommit = line.split(" ")[1].strip()
        apiurl = url + "/commits/" + fixcommit
        headers = {'Authorization': 'token ' + tokens}
        remainingNumber = util.getRemaining(tokens)   

        if int(remainingNumber) < 5:            
                while int(remainingNumber) < 5000:                  
                    time.sleep(100)                 
                    remainingNumber = util.getRemaining(tokens)
                    print ("remainig number is " + remainingNumber + "not enough limit, sleep a while")     
        login = requests.get(apiurl, headers = headers)
        apiinfor = login.json()
        count = count + 1
        if "url" in apiinfor:
            sys.stdout.write("token remaining:" + remainingNumber + " ") 
            print(partation + " pairCount " + str(pairCount) + " " + partation + " " + tokenNumber)           
            eachPairPath = clonePath + "/" + str(pairCount)           
            util.createPath(eachPairPath)
            getInfoFromFixCommit(apiinfor,fixcommit,eachPairPath,url)
            pairCount = pairCount + 1
        
print(partation + " archiveInfo.txt DONE!!!!")        


