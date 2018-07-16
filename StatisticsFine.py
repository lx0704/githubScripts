import os
from os import listdir
from os.path import isfile, join
import shutil

FineResult = "/disk2/Xia/GitHubProjects/4gumtree/Statistics/SparkResults/FineGrained/part-00000"
writePath = "/disk2/Xia/GitHubProjects/4gumtree/Statistics/Excels/"
PatternCount = "/disk2/Xia/GitHubProjects/4gumtree/Statistics/SparkResults/GeneralPattern/GeneralPattern.csv"
generalDic = dict()
with open(PatternCount) as PC:
	for line in PC:
		pa = line.split(",")[0].replace("=>","TO")
		count = line.split(",")[1].strip()
		generalDic[pa] = count
#print(generalDic)
count = 0
with open(FineResult) as resultFile:
	for line in resultFile:
		firstSemi = line.index(",")
		generalPattern = line[2:firstSemi].replace("=>","TO")
		lastIndex = line.rindex("),")
		finedPattern = line[firstSemi + 1 : lastIndex]
		frequency = line[lastIndex + 2:-2]
		writeFile = writePath + generalPattern + ".csv"
		with open(writeFile,'a') as wf:
			if int(frequency) > 1:
				wf.write(finedPattern + "," + frequency + "," + str(float(frequency)/int(generalDic[generalPattern])))
				wf.write("\n")
print(count)