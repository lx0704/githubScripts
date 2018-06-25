import os
import subprocess

def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        os.chdir(path)
def readComaretoken(tokenfile):
    with open(tokenfile) as f:
        tokenkey = f.read().split(" ")[0].strip()
    return tokenkey
def readDownUrl(UrlFile):
    buggyUrls = set()
    fixUrls = set()
    with open(UrlFile) as f:
        for line in f:
            if "bug file url:" in line:
                buggyUrls.add(line.split("bug file url:")[1].strip())
            if "fix file url:" in line:
                fixUrls.add(line.split("fix file url:")[1].strip())
    return list(buggyUrls),list(fixUrls)
def cdAndWget(Dowurl, pairpath, pathName):   
    os.system("wget -q -O " + pairpath  + "/" + pathName + " " + Dowurl)

def getRemaining(tokenKey):
    command = "curl -H" + "\"Authorization: token " + tokenKey + "\" -X GET https://api.github.com/rate_limit"
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    remainingNumber = output.split("remaining\": ")[1].split(",\n")[0]  
    return remainingNumber
def changeToMap(tempCommits):
    commitMap = dict()
    for commit in tempCommits:                                
        url = commit.split("==>")[0]
        commitsha = commit.split("==>")[1]
        if url not in commitMap:
            commits = set()
            commits.add(commitsha)
            commitMap[url] = commits
        else:
            commitMap[url].add(commitsha)
    return commitMap



