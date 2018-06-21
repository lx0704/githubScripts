import json
import gzip
import re
import os
import sys
import urllib
import requests
# parse after 2015
#curl -H "Authorization: token " -X GET https://api.github.com/rate_limit

def readtoken(tokenfile):
	tokens = []
	with open(tokenfile) as f:
		for line in f:
			tokens.append(line.strip())
	return tokens



year = sys.argv[1]
day = sys.argv[2]

tokenfile = "/media/disk2/xia/GithubProjects/2Parse/scripts/parse2015/" + day + ".txt"

tokens = readtoken(tokenfile)
print(tokens)

rootpath = "/media/disk2/xia/GithubProjects/1Archive/"
writepath = "/media/disk2/xia/GithubProjects/2Parse/rawdata/"
filepath = rootpath + year
allfiles = os.listdir(filepath)
tokenindex = 0
count = 0
filecount = 1
for file in allfiles:
    if day in file:
        print(str(filecount) + " files")
        filecount = filecount + 1
        urlandCommit = set()
        with gzip.open(filepath + "/" + file, "rb") as f:
            
            for line in f.readlines():
                d = json.loads(line.decode("utf-8")) 
                type = d["type"]
                        
                if type == "PushEvent":
                    commits = d["payload"]["commits"]
                    temCommits = []
                    fixing = "No"
                    for c in commits:
                        message = c["message"]
                        if re.search(r'^(?=.*(bug|issue|problem|error))(?=.*(fix|solve)).+$', message, re.IGNORECASE): 
                            temCommits.append(c["sha"])
                            fixing = "Yes"               
                    if fixing == "Yes":                        
                        apiurl = d["repo"]["url"]                      
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
                        if "clone_url" in apiinfor:
                            url = apiinfor["clone_url"]
                            language = apiinfor["language"]
                            if language == "Java":
                                for commit in temCommits:
                                    urlandCommit.add(url + " " + commit)                                 
            for commitN in urlandCommit:                        
                 with open(writepath + "/"  + day + ".txt", "a") as writefile:
                    writefile.write(commitN)
                    writefile.write("\n")              

        
