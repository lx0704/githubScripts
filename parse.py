import json
import gzip
import re
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
year = sys.argv[1]
rootpath = "/media/disk2/Xia/GitHubProjects/1Archive/"
writepath = "/media/disk2/Xia/GitHubProjects/2Parse/"
JIRA_set = util.read_JIRAData("/media/disk2/Xia/GitHubProjectsJIRA/2Parse/jiraBug.txt")
print(JIRA_set)

urlandCommit = set()

filecount = 1
     
filepath = rootpath + year
allfiles = os.listdir(filepath)
for file in allfiles:
    print("file count: " + str(filecount) + " files")
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
                                message = commit[2]
                                if re.search(r'^(?=.*(bug|failure|issue|error|fault|defect|flaw|glitch))(?=.*(fix|solve|repair)).+$', message, re.IGNORECASE):  
                                    urlcommit = url + " " + commit[0]                                
                                    if urlcommit not in urlandCommit:
                                        urlandCommit.add(urlcommit)
                                        with open(writepath + "/commitandmessage/" + year + ".txt", "a") as writefile:
                                            urlcommit = urlcommit.replace("//","//api.").replace(".com/",".com/repos/")
                                            writefile.write(urlcommit + " [" + message + "]")
                                            writefile.write("\n")
                

        
