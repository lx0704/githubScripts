import urllib2
import sys
start = sys.argv[1]
print("start:" + str(start))
contents = urllib2.urlopen("https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-rss/temp/SearchRequest.xml?jqlQuery=issuetype+%3D+Bug+AND+status+in+%28Resolved%2C+Closed%2C+Done%29+AND+resolution+in+%28Fixed%2C+Implemented%2C+Done%2C+Resolved%2C+Delivered%29+&tempMax=1000&pager/start=" + str(start))

lines = contents.readlines()

for line in lines:
    if "<title>[" in line:
        bugid = line.split("<title>[")[1].split("] ")[0]
        with open('jiraBug.txt','a') as w:
        	w.write(bugid)
        	w.write("\n")


#292056

