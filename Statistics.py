import os
from os import listdir
from os.path import isfile, join
import shutil

rootPath = "/disk2/Xia/GitHubProjects/3Clone/"
years = ["2012-2014/","2011/","2015/","2017/","2016/","2018/"]
#years = ["2012-2014/"]
archiveInfor = "archiveInfo.txt"

print(years)
commitByYear = dict()
totalmeargeCount = 0
for year in years:
	yearPath = rootPath + year
	partations = os.listdir(yearPath)
	for partation in partations:
		partationPath = yearPath + partation + "/"
		commitFolders = os.listdir(partationPath)
		for commits in commitFolders:
			commitYear = "'"
			commitPath = partationPath + commits + "/"
			commitInforFile = commitPath + archiveInfor
			ifIncludeJava = 0
			if isfile(commitInforFile):
				with open(commitInforFile) as inforFile:
					fixedCommit = ""
					fixedMessage = ""
					mergeCount = 0					
					if os.path.isdir(commitPath + "buggy-version"):						
						for line in inforFile:
							if "Date:" in line:
								commitYear = line.split("Date:")[1].strip().split("-")[0]
								mergeCount = mergeCount + 1
						allBuggyFiles = os.listdir(commitPath + "buggy-version")
						#print(allBuggyFiles)
						if mergeCount > 1:
							print(commitPath)
							totalmeargeCount = totalmeargeCount + 1
						for file in allBuggyFiles:
							if file.endswith(".java"):
								ifIncludeJava = 1
								break
			if ifIncludeJava == 1:
				if commitYear not in commitByYear:
					commitByYear[commitYear] = 1
				else:
					commitByYear[commitYear] = commitByYear[commitYear] + 1
print(totalmeargeCount)				
