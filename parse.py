import json
import gzip
import re
import os
import sys
import util

reload(sys)
sys.setdefaultencoding("utf-8")
year = sys.argv[1]
rootpath = "/media/disk6TV1/Xia/GitHubProjects/1Archive/"
writepath = "/media/disk2/Xia/GitHubProjectsJIRA/2Parse/"
JIRA_set = util.read_JIRAData("/media/disk2/Xia/GitHubProjectsJIRA/2Parse/jiraBug.txt")

urlandCommit = set()

filecount = 1
     
filepath = rootpath + year
allfiles = os.listdir(filepath)
for file in allfiles:
    print(file)
    filecount = filecount + 1       
    with gzip.open(filepath + "/" + file, "rb") as f:
        for line in f.readlines():
            d = json.loads(line.decode("utf-8"))        
            if "repository" in d:
                if "language" in d["repository"] and d["repository"]["language"] == "Java":
                        url =  d["repository"]["url"]                           
                        if "payload" in d and "shas" in d["payload"]:
                            commits = d["payload"]["shas"]                
                            for commit in commits:
                                message = commit[2].replace("\n"," ")
                                #if re.search(r'^(?=.*(bug|failure|issue|error|fault|defect|flaw|glitch))(?=.*(fix|solve|repair)).+$', message, re.IGNORECASE):  
                                for bug_id in JIRA_set:
                                    if message.startswith(bug_id + " "):
                                        print(bug_id)
                                        urlcommit = url + " " + commit[0]                                
                                        if urlcommit not in urlandCommit:
                                            urlandCommit.add(urlcommit)
                                            with open(writepath + "/commitandmessage/" + year + ".txt", "a") as writefile:
                                                urlcommit = urlcommit.replace("//","//api.").replace(".com/",".com/repos/")
                                                writefile.write(urlcommit + " [" + message + "]")
                                                writefile.write("\n")
                

        
