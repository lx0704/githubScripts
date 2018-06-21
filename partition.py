import os
import sys

year = sys.argv[1]
partationSize = 8000
orifile = "/disk2/Xia/GitHubProjects/2Parse/commitandmessage/" + year + ".txt"
partionpath = "/disk2/Xia/GitHubProjects/2Parse/partations/" + year

with open(orifile) as originfile:
	count = 1       
	fileNumber = 1   
	for line in originfile:
		filename = partionpath + "/V" + str(fileNumber) + ".txt"
		with open(filename,"a") as writefile:
			writefile.write(line.strip())
			writefile.write("\n")
			if count < partationSize:				
				count = count + 1
			else:
				fileNumber = fileNumber + 1
				count = 1

		