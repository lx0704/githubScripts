import subprocess
import os
import urllib
import sys
import requests
import util

reload(sys)
sys.setdefaultencoding("utf-8")
   
def readtoken(tokenfile):
    tokens = []
    with open(tokenfile) as f:
        for line in f:
            tokens.append(line.strip())
    return tokens
def getInfoFromFixCommit(apiinfor,fixcommit,eachPairPath,apiurl):
    message = apiinfor["commit"]["message"]
    author = apiinfor["commit"]["author"]["name"]
    commiter = apiinfor["commit"]["committer"]["name"]
    date = apiinfor["commit"]["author"]["date"]
    bugcommits = apiinfor["parents"]
    for bugs in bugcommits:        
        with open(eachPairPath + "/archiveInfo.txt",'a') as infoPath: 
            bugcommit = bugs["sha"]
            infoPath.write("Project url:" + apiurl + "\n")   
            infoPath.write("Buggy-version:" + bugcommit + "\n")
            infoPath.write("Fixed-version:" + fixcommit + "\n")
            infoPath.write("Fixed commit message:" + message + "\n")
            infoPath.write("Date:" + date + "\n")
            infoPath.write("Author:" + author + "\n")
            infoPath.write("Commiter:" + commiter + "\n")

            
            
year = sys.argv[1]
partation = sys.argv[2]
tokenNumber = sys.argv[3]

tokenfile = "/home/Xia/XiaLi/GitHubProjects/3Clone/" + tokenNumber + ".txt"
tokens = readtoken(tokenfile)
print(tokens)

bugPath = "/home/Xia/XiaLi/GitHubProjects/2Parse/partations/"+ year + "/" + partation + ".txt"
clonerootPath = "/home/Xia/XiaLi/GitHubProjects/3Clone/" 
clonePath = clonerootPath + year + "/" + partation

path = bugPath
with open(path,'r') as file:
    count = 1
    tokenindex = 0  
    pairCount = 1     
    for line in file:         
        #print(year + " " + partation + " is processing")       
        url = line.split(" ")[0]
        fixcommit = line.split(" ")[1]
        apiurl = url + "/commits/" + fixcommit
        
        headers = {'Authorization': 'token ' + tokens[tokenindex]}
        if count > 20:
            if tokenindex == len(tokens) - 1:
                tokenindex = 0
            else:
                tokenindex = tokenindex + 1
            headers = {'Authorization': 'token ' + tokens[tokenindex]}
            count = 1
        login = requests.get(apiurl, headers = headers)
        apiinfor = login.json()
        count = count + 1
        if "url" in apiinfor:
            print("pairCount " + str(pairCount) + " " + partation + " " + tokenNumber)           
            eachPairPath = clonePath + "/" + str(pairCount)           
            util.createPath(eachPairPath)
            getInfoFromFixCommit(apiinfor,fixcommit,eachPairPath,url)
            pairCount = pairCount + 1
        
        


