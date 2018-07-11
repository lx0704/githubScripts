import os
from os import listdir
from os.path import isfile, join

rootPath = "/home/Xia/XiaLi/GitHubProjects/3Clone/"
#years = ["2012-2014/","2011/","2015/","2017/","2016/"]
years = ["2011/"]
archiveInfor = "archiveInfo.txt"


commitDic = dict()
for year in years:
	yearPath = rootPath + year
	partations = os.listdir(yearPath)
	for partation in partations:
		partationPath = yearPath + partation + "/"
		commitFolders = os.listdir(partationPath)
		for commits in commitFolders:
			commitPath = partationPath + commits + "/"
			commitInforFile = commitPath + archiveInfor
			if isfile(commitInforFile):
				with open(commitInforFile) as inforFile:
					fixedCommit = ""
					fixedMessage = ""
					for line in inforFile:
						if "Fixed-version:" in line:
							fixedCommit = line.split("Fixed-version:")[1].strip()
						if "Fixed commit message:" in line:
							fixedMessage = line.split("Fixed commit message:")[1].strip()
					fixedCommitAndMessage = fixedCommit + fixedMessage
					if fixedCommitAndMessage not in commitDic:
						files = []
						files.append(commitInforFile)
						commitDic[fixedCommitAndMessage] = files
					else:
						commitDic[fixedCommitAndMessage].append(commitInforFile)
for key in commitDic.keys():
	length = len(commitDic[key])
	if length>1:
		for i in range(1,length):
			print(key)
			print(commitDic[key])
			os.rename(commitDic[key] + "buggy-version", commitDic[key] + "buggy-versionDUPLICATE")
			os.rename(commitDic[key] + "fixed-version", commitDic[key] + "fixed-versionDUPLICATE")
		

		
