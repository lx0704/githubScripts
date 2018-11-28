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
JIRA_set = util.read_JIRAData("/media/disk2/Xia/GitHubProjectsJIRA/2Parse/jiraBug.txt")

def readtoken(tokenfile):
    with open(tokenfile) as f:
        token = ""
        for line in f:
            token = line.split(" ")[0]
    return token

rootpath = "/media/disk6TV1/Xia/GitHubProjects/1Archive/"
writepath = "/media/disk2/Xia/GitHubProjectsJIRA/2Parse/commitandmessage/"

year = sys.argv[1]  # 2011
month = sys.argv[2] # 03,04...
tokenNumber = sys.argv[3]

tokenfile = "/media/disk2/Xia/GitHubProjects/3Clone/readtokens/" + tokenNumber + ".txt"
tokenKey = readtoken(tokenfile)
print(tokenKey)

CurrentPath = writepath + year + '/' + month + '.txt'
CurrentData = util.readCurrent(CurrentPath)
print("CURRENT DATA SIZE:" + str(len(CurrentData)))
for i in CurrentData:
    print(i)
print("CURRENT DATA")


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
                        #if re.search(r'^(?=.*(bug|failure|issue|error|fault|defect|flaw|glitch))(?=.*(fix|solve|repair)).+$', message, re.IGNORECASE):                       
                        message_sets = message.replace("\n"," ").split(" ")
                        is_common = False
                        for m in message_sets:
                        	if m in JIRA_set:
                        		is_common = True
                        		break                        
                        if is_common:
                            print(message)
                            commitInfor = "" 
                            if "shas" in d["payload"]:
                                commitInfor = apiurl + "==>" + c[0] + " [" + message + "]"                                
                            else:
                                commitInfor = apiurl + "==>" + c["sha"]+ " [" + message + "]"
                            
                            if commitInfor.split("==>")[1] in CurrentData:
                                print("EXISTS")
                                print(commitInfor)
                            else:
                                temCommits.add(commitInfor)
commitMap = util.changeToMap(temCommits)
print("FINISH READ")        
for apiurl in commitMap:                                
    headers = {'Authorization': 'token ' + tokenKey}
    remainingNumber = util.getRemaining(tokenKey)                       
    if int(remainingNumber) < 5:            
        while int(remainingNumber) < 5000:                  
            time.sleep(100)                 
            remainingNumber = util.getRemaining(tokenKey)
            print ("remainig number is " + remainingNumber + "not enough limit, sleep a while")
    print("remaining rate limit is:" + remainingNumber + " for " + tokenNumber)

    notJavaurl = util.readNotJava(writepath + '/NonJavaURL/' + year + month + ".txt")
    if apiurl not in notJavaurl:
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
            else:
                with open(writepath + '/NonJavaURL/' + year + month + ".txt",'a') as nonJava:
                    nonJava.write(apiurl)
                    nonJava.write("\n")           
print(year + " " + month + " commit and message done!!")
        
