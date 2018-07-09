import os
import sys

def listfiles(partationpath,years):
    newCommits = set()
    count = 0
    for yearFile in years:
        oldfiles = os.listdir(partationpath + yearFile)

        for file in oldfiles:
            File2Path = partationpath + yearFile + "/" + file
            with open(File2Path) as newf:
                for line in newf:
                    urlCommit = line.split(" [")[0].strip().replace(".git "," ")
                    newCommits.add(urlCommit)
                    count = count + 1

    print(count)
    print(len(newCommits))
    return newCommits


partationpath = "/home/Xia/XiaLi/GitHubProjects/2Parse/partations/"
years = ["2012-2014/","2011/","2015/","2017/","2016/"]
BigCommits = listfiles(partationpath,years)
print(list(BigCommits)[0])


# path2016 = "/home/Xia/XiaLi/GitHubProjects/2Parse/commitandmessage/"
# years2016 = ["2016"]
# Commits2016 = listfiles(path2016,years2016)
# print(list(Commits2016)[0])

# partationSize = 8000
# partionpath = "/home/Xia/XiaLi/GitHubProjects/2Parse/partations/2016/"


# count = 1       
# fileNumber = 1  
# uniqueCount = 0
# for c in Commits2016:
#     if c not in BigCommits:
#         uniqueCount = uniqueCount + 1
#         filename = partionpath + "/V" + str(fileNumber) + ".txt"
#         with open(filename,"a") as writefile:
#             writefile.write(c.strip())
#             writefile.write("\n")
#             if count < partationSize:               
#                 count = count + 1
#             else:
#                 fileNumber = fileNumber + 1
#                 count = 1
# print(uniqueCount)

        





