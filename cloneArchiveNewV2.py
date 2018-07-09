import sys
import util
import os
import requests
import subprocess
import time

reload(sys)
sys.setdefaultencoding("utf-8")

year = sys.argv[1]
partation = sys.argv[2]
tokenNumber = sys.argv[3]

tokenfile = "/home/Xia/XiaLi/GitHubProjects/3Clone/readtokens/" + tokenNumber + ".txt"
tokenKey = util.readComaretoken(tokenfile)
print(tokenKey)

archiveInfoPath = "/home/Xia/XiaLi/GitHubProjects/3Clone/" + year + "/" + partation
allfiles = os.listdir(archiveInfoPath)

tokenindex = 0
filecount = 0
count = 0
start_time = time.time()
for file in range(1, len(allfiles) + 1):
	eachPairPath = archiveInfoPath + "/" + str(file) + "/"
	downUrlPath =  eachPairPath + "fileDownloadUrl.txt"
	
	if (os.path.exists(downUrlPath)):
		buggyUrls,fixUrls = util.readDownUrl(downUrlPath)
		for i in range(0, len(buggyUrls)):			
			headers = {'Authorization': 'token ' + tokenKey}			
			remainingNumber = util.getRemaining(tokenKey)		
						
			if int(remainingNumber) < 5:			
				while int(remainingNumber) < 5000:					
					time.sleep(100)					
					remainingNumber = util.getRemaining(tokenKey)
					print ("remainig number is " + remainingNumber + "not enough limit, sleep a while")

			requestFrombuggy = requests.get(buggyUrls[i], headers = headers).json()
			requestFromfix = requests.get(fixUrls[i], headers = headers).json()					
			print("github key remaining rate limit " + remainingNumber)
			print(eachPairPath + " " + tokenNumber + "," + str(len(allfiles)) + " files")
			if "download_url" in requestFrombuggy and "download_url" in requestFromfix:
				if requestFrombuggy["download_url"] is not None:
				    buggyDownUrl = requestFrombuggy["download_url"]
				    fixDownUrl = requestFromfix["download_url"]
				    buggyversionPath = eachPairPath + "/buggy-version"
				    fixedversionPath = eachPairPath + "/fixed-version"
				    util.createPath(buggyversionPath)
				    util.createPath(fixedversionPath)
				    commonpath = buggyUrls[i].split("contents/")[1].split("?ref=")[0]
				    util.cdAndWget(buggyDownUrl,buggyversionPath,commonpath.replace("/","."))
				    util.cdAndWget(fixDownUrl,fixedversionPath,commonpath.replace("/","."))
print("Buggy and fixed versions DONE!!!!!")			
			


