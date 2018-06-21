import json
import gzip
import re
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
#years = ["2012","2013","2014","2015","2016","2017"]
#year = sys.argv[1]
years = ["2012","2013","2014"]
rootpath = "/disk2/Xia/GitHubProjects/1Archive/"
writepath = "/disk2/Xia/GitHubProjects/2Parse/"
urlandCommit = set()

filecount = 1
for year in years:      
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
                                            with open(writepath + "/commitandmessage/" + "2012-2014.txt", "a") as writefile:
                                                urlcommit = urlcommit.replace("//","//api.").replace(".com/",".com/repos/")
                                                writefile.write(urlcommit + " [" + message + "]")
                                                writefile.write("\n")
                

        
