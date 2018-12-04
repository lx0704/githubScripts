import os
from os import listdir
from os.path import isfile, join
import shutil

rootPath = "/disk2/Xia/GitHubProjects/3Clone/"
years = ["NewDown2011-2017/","NewDown2018/"]
archiveInfor = "archiveInfo.txt"

print(years)
commitByYear = dict()
totalmeargeCount = 0
for year in years:
	yearPath = rootPath + year    # "/disk2/Xia/GitHubProjects/3Clone/NewDown2018"
	partations = os.listdir(yearPath)
	for partation in partations:			# "/disk2/Xia/GitHubProjects/3Clone/NewDown2018/V11"
		partationPath = yearPath + partation + "/"
		commitFolders = os.listdir(partationPath)
		for commits in commitFolders:          
			commitYear = "'"
			commitPath = partationPath + commits + "/"  # "/disk2/Xia/GitHubProjects/3Clone/NewDown2018/V11/111"
			commitInforFile = commitPath + archiveInfor
			ifIncludeJava = 0
			if isfile(commitInforFile):
				with open(commitInforFile) as inforFile:
					mergeCount = 0					
					if os.path.isdir(commitPath + "buggy-version"):						
						for line in inforFile:
							if "Date:" in line:
								commitYear = line.split("Date:")[1].strip().split("-")[0]
								mergeCount = mergeCount + 1
						allBuggyFiles = os.listdir(commitPath + "buggy-version")
						#print(allBuggyFiles)
						if mergeCount > 1:
							#print(commitPath)
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
print(commitByYear)				
