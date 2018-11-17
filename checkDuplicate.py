import os
import sys

def listfiles(partationpath,years):
    newCommits = dict()
    count = 0
    for yearFile in years:
        oldfiles = os.listdir(partationpath + yearFile)
        for file in oldfiles:
            File2Path = partationpath + yearFile + "/" + file
            with open(File2Path) as newf:
                for line in newf:
                    url = line.split(" ")[0]
                    shaAndCommit = line.split(url + " ")[1].strip()
                    newCommits[shaAndCommit] = line.strip().replace(".git "," ")
                    count = count + 1

    print(count)
    return newCommits


partationpath = "/media/disk2/Xia/GitHubProjects/2Parse/commitandmessage/"
years = ["2012-2014/","2011/","2015/","2017/","2016/"]
BigCommits = listfiles(partationpath,years)
print(len(BigCommits))


path2018 = "/media/disk2/Xia/GitHubProjects/2Parse/commitandmessage/"
years2018 = ["2018"]
Commits2018 = listfiles(path2018,years2018)
print(len(Commits2018))

# partationSize = 10000
# partionpath = "/media/disk2/Xia/GitHubProjects/2Parse/partations/NewFull2011-2017"


# count = 1       
# fileNumber = 1  
# uniqueCount = 0

# for key in BigCommits:
#     uniqueCount = uniqueCount + 1
#     filename = partionpath + "/V" + str(fileNumber) + ".txt"
#     with open(filename,"a") as writefile:
#         writefile.write(BigCommits[key].strip())
#         writefile.write("\n")
#         if count < partationSize:               
#             count = count + 1
#         else:
#             fileNumber = fileNumber + 1
#             count = 1
# print(uniqueCount)

        





