import subprocess
import os
import urllib
import sys
import requests
import util
from os.path import exists

reload(sys)
sys.setdefaultencoding("utf-8")


def readComaretoken(tokenfile):
    tokens = []
    with open(tokenfile) as f:
        for line in f:
            tokens.append(line.split(" ")[0].strip())
    return tokens

def cdAndWget(Dowurl, pairpath, pathName):   
    os.system("wget -q -O " + pairpath  + "/" + pathName + " " + Dowurl)
def readArchiveInfo(path):
    bugcommit = ""
    fixcommit = ""
    apicrl = ""
    with open(path) as archive:
        info = archive.read()
        bugcommit = info.split("Buggy-version:")[1].split("\n")[0]
        fixcommit = info.split("Fixed-version:")[1].split("\n")[0]
        apiurl = info.split("Project url:")[1].split("\n")[0]
    return bugcommit,fixcommit,apiurl



partation = sys.argv[1]

archiveInfoPath = "/media/disk2/Xia/GitHubProjects/3Clone/NewFull2011-2017/%s"%partation
allfiles = os.listdir(archiveInfoPath)
tokenindex = 0
filecount = 0
count = 0
for file in allfiles:
    eachPairPath = archiveInfoPath + "/" + file + "/"
    archiveInfoFile = eachPairPath + "archiveInfo.txt" 
    alreadyFix = eachPairPath + "buggy-version"
    if exists(archiveInfoFile):
        print(eachPairPath)
        filecount = filecount + 1
        print(str(filecount) + " files")     
       
        bugcommit,fixcommit,apiurl = readArchiveInfo(eachPairPath + "archiveInfo.txt")

        compareCommit = bugcommit + "..." + fixcommit
        
        diffUrl = apiurl.replace("api.","").replace("repos/","") + "/compare/" + compareCommit + ".diff"
        response = urllib.urlopen(diffUrl)
        for line in response:
            if "diff --git " in line and ".java" in line and "test" not in line and "Test" not in line:
                path = line.split("diff --git ")[1].split(" ")[0]
                path = path[2:]
                commonFileUrl = apiurl + "/contents/" + path + "?ref="
                buggyFileUrl = commonFileUrl + bugcommit
                fixFileUrl = commonFileUrl + fixcommit
                with open(eachPairPath + "fileDownloadUrl.txt",'a') as otherInfo:
                	otherInfo.write("bug file url:" + buggyFileUrl)
                	otherInfo.write("\n")
                	otherInfo.write("fix file url:" + fixFileUrl)
                	otherInfo.write("\n")
print("Write fileDownloadUrl DONE!!!!!!")