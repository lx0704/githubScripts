import json
import gzip
import re
import os
import sys
import urllib
import requests
import util
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

rootpath = "/home/Xia/XiaLi/GitHubProjects/1Archive/"
writepath = "/home/Xia/XiaLi/GitHubProjects/2Parse/commitandmessage/"

year = sys.argv[1]  # 2011
month = sys.argv[2] # 03,04...
tokenNumber = sys.argv[3]

tokenfile = "/home/Xia/XiaLi/GitHubProjects/3Clone/readtokens/" + tokenNumber + ".txt"
tokenKey = readtoken(tokenfile)
print(tokenKey)


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
                    if year == "2011":
                        commits = d["payload"]["shas"]
                    else:
                        commits = d["payload"]["commits"]

                    for c in commits:
                        message = ""
                        if year == "2011":
                            message = c[2]
                        else:
                            message = c["message"]
                        if re.search(r'^(?=.*(bug|issue|problem|error))(?=.*(fix|solve)).+$', message, re.IGNORECASE): 
                            if year == "2011":
                                temCommits.add(apiurl + "==>" + c[0] + " [" + message + "]")
                            else:
                                temCommits.add(apiurl + "==>" + c["sha"]+ " [" + message + "]")
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

        
