import json
import gzip
import re
import os
import sys
import urllib
import requests
import util
import time
# parse 2011 and after 2015
#curl -H "Authorization: token " -X GET https://api.github.com/rate_limit
reload(sys)
sys.setdefaultencoding("utf-8")


def readtoken(tokenfile):
    with open(tokenfile) as f:
        token = ""
        for line in f:
            token = line.split(" ")[0]
    return token

rootpath = "/media/disk2/Xia/GitHubProjects/1Archive/"
writepath = "/media/disk2/Xia/GitHubProjects/2Parse/commitandmessage/"

year = sys.argv[1]  # 2011
month = sys.argv[2] # 03,04...
tokenNumber = sys.argv[3]

tokenfile = "/media/disk2/Xia/GitHubProjects/3Clone/readtokens/" + tokenNumber + ".txt"
tokenKey = readtoken(tokenfile)
print(tokenKey)

CurrentPath = writepath + year + '/' + month + '.txt'
CurrentData = util.readCurrent(CurrentPath)
print(len(CurrentData))


filepath = rootpath + year
allfiles = os.listdir(filepath)
filecount = 1
temCommits = set()
urlandCommit = set()
for file in allfiles:
    if year + "-" + month in file:        
        with gzip.open(filepath + "/" + file, "rb") as f:
           
            for line in f.readlines():
                d = json.loads(line.decode("utf-8")) 
                type = d["type"]
                        
                if type == "PushEvent":
                    apiurl = d["repo"]["url"].replace("github.dev","github.com")
                    commits = []
                    if "shas" in d["payload"]:
                        commits = d["payload"]["shas"]
                    else:
                        commits = d["payload"]["commits"]

                    for c in commits:
                        message = ""
                        if "shas" in d["payload"]:
                            if len(c) > 2:
                                message = c[2]
                        else:
                            if "message" in c:
                                message = c["message"]
                        if re.search(r'^(?=.*(bug|failure|issue|error|fault|defect|flaw|glitch))(?=.*(fix|solve|repair)).+$', message, re.IGNORECASE):
                        	commitInfor = "" 
                            if "shas" in d["payload"]:
                            	commitInfor = apiurl + "==>" + c[0] + " [" + message + "]"                                
                            else:
                            	commitInfor = apiurl + "==>" + c["sha"]+ " [" + message + "]"
                            print(commitInfor)
                            if commitInfor.replace("==>"," ") in CurrentData
                            	print("EXISTS")
                            else:
                            	print("NOTEXISTS store")
                            	temCommits.add(commitInfor)  
commitMap = util.changeToMap(temCommits)         
for apiurl in commitMap:                                
    headers = {'Authorization': 'token ' + tokenKey}
    remainingNumber = util.getRemaining(tokenKey)                       
    if int(remainingNumber) < 5:            
        while int(remainingNumber) < 5000:                  
            time.sleep(100)                 
            remainingNumber = util.getRemaining(tokenKey)
            print ("remainig number is " + remainingNumber + "not enough limit, sleep a while")
    print("remaining rate limit is:" + remainingNumber + " for " + tokenNumber)
    login = requests.get(apiurl, headers = headers)
    apiinfor = login.json()   
    if "clone_url" in apiinfor:
        url = apiinfor["clone_url"]
        language = apiinfor["language"]
        if language == "Java":
            for commitsha in commitMap[apiurl]:
                print(url + " " + commitsha)
                commitN = url.replace("//","//api.").replace(".com/",".com/repos/") + " " + commitsha                                                      
                with open(writepath + "/"  + year + "/" + month + ".txt", "a") as writefile:
                    writefile.write(commitN)
                    writefile.write("\n")              
print(year + " " + month + " commit and message done!!")
        
