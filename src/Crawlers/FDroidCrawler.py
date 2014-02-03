'''
Created on Jan 26, 2012

@author: symonwi
@author: Eric Shaw
@version: 1/19/2014
'''
import urllib
import re

def getPageCount(url):
    applicationsPage = url+"/repository/browse/"
    numOfPagesExp = "Page 1 of (\d+)"
   
    site = urllib.urlopen(applicationsPage)
    html = site.read()
    site.close()
   
    numOfPages = int(re.findall(numOfPagesExp, html)[0])
    return numOfPages

def getHTML(url):
    site = urllib.urlopen(url)
    html = site.read()
    site.close()
    return html

def getApplicationPageLinks(html):
    appPageExp ="https://f-droid.org/repository/browse/\?fdid=(.*?)\""
    #appPageExp = "<h2 class=\"title\"><a href=\"(/application/.*?)\""
    return re.findall(appPageExp, html)

def getDownloadLinks(html):
    downloadLinkExp = "<a href=\"(.*?).apk"
    ret = re.findall(downloadLinkExp, html)
    return ret

def downloadApp(url, path, appName):
    f = open(path+"fdroid_"+appName+".apk", "wb")
    app = urllib.urlopen(url)
    f.write(app.read())
    f.close()
    app.close()

def getAppName(html):
    appNameExp = "<span style=\"font-size:20px\">(.*?)</span>"
    return re.findall(appNameExp, html)[0].translate(None, "<>:\"/\|?*")
   

#############################################################################

domain = "https://f-droid.org"
outputPath = "C:\\apks\\downloaded\\fdroid\\"
appsExamined = 0
appsDownloaded = 0




#this is where we will any errors we experience while downloading apps such as
#a problem with the formatting or if the app cost money to buy
errorFile = open(outputPath+"fdroid_errors.txt", "w")

numOfPages = getPageCount(domain)

print "Downloading apps from "+str(numOfPages)+" pages . . ."
print "Scanning approximately "+str(numOfPages*30)+" apps for candidates . . ."

start = 1 #change to recover from an error and start where you left off
for i in range(start,numOfPages+1):
    #set up the page url
    print "!!!!!!beginning page #"+str(i)+" !!!!!!"
    currentPage = domain+"/repository/browse/?fdpage="+str(i)
   
    #get the html code
    html = getHTML(currentPage)
   
    #extract the links to the actual application pages
    applicationPages = getApplicationPageLinks(html)
   
    #for each page parse to see if it is a free app and if so download
    for page in applicationPages:
        #get the html code
        html = getHTML(domain+ '/repository/browse/?fdid=' + page)
        #extract the links
        downloadLinks = getDownloadLinks(html)
        appsExamined += 1
        #give status update for each 100 downloaded
        if appsExamined % 5 == 0:
            print "****** "+str(appsExamined) + " Apps examined ******"
       
        #if no links there is a formatting error with the page
        if len(downloadLinks) > 1:
            downloadLink = downloadLinks[1]
            
            #print domain+downloadLink
            downloadApp(downloadLink + '.apk',outputPath,getAppName(html))
            appsDownloaded += 1
            if appsDownloaded % 5 == 0:
                print "****** "+str(appsDownloaded) + " Apps downloaded ******"
           
        else:
            errorFile.write("XXXXXX Formating Error with page "+domain+page+" XXXXXX\n")

errorFile.close()       
print str(appsExamined)+" apps examined"
print str(appsDownloaded)+" apps downloaded"
