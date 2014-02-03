'''
Created on Jan 26, 2012

@author: symonwi
'''
import urllib
import re

def getPageCount(url):
    applicationsPage = url+"/applications"
    numOfPagesExp = "<li class=\"pager-last last\"><a href=\"/applications\?page=(\d+)\""
   
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
    appPageExp = "<h2 class=\"title\"><a href=\"(/application/.*?)\""
    return re.findall(appPageExp, html)

def getDownloadLinks(html):
    downloadLinkExp = "<div class=\"download-button\"><a href=\"(.*?)\""
    return re.findall(downloadLinkExp, html)

def downloadApp(url, path, appName):
    f = open(path+"slideme_"+appName+".apk", "wb")
    app = urllib.urlopen(url)
    f.write(app.read())
    f.close()
    app.close()

def getAppName(html):
    appNameExp = "<div class=\"download-button\"><a href=\".*?\" title=\"(.+?)\""
    return re.findall(appNameExp, html)[0].translate(None, "<>:\"/\|?*")
   

#############################################################################

domain = "http://www.slideme.org"
outputPath = "C:\\apks\downloaded\\slideme\\"
appsExamined = 0
appsDownloaded = 0




#this is where we will any errors we experience while downloading apps such as
#a problem with the formatting or if the app cost money to buy
errorFile = open(outputPath+"slidme_errors.txt", "w")

numOfPages = getPageCount(domain)

print "Downloading apps from "+str(numOfPages)+" pages . . ."
print "Scanning approximately "+str(numOfPages*10)+" apps for canidates . . ."

##for i in range(numOfPages+1):
for i in range(873,numOfPages+1):
    #set up the page url
    print "!!!!!!begining page #"+str(i)+" !!!!!!"
    currentPage = domain+"/applications?page="+str(i)
   
    #get the html code
    html = getHTML(currentPage)
   
    #extract the links to the actual application pages
    applicationPages = getApplicationPageLinks(html)
   
    #for each page parse to see if it is a free app and if so download
    for page in applicationPages:
        #get the html code
        html = getHTML(domain+page)
        #extract the links
        downloadLinks = getDownloadLinks(html)
        appsExamined += 1
        #give status update for each 100 downloaded
        if appsExamined % 5 == 0:
            print "****** "+str(appsExamined) + " Apps examined ******"
       
        #if no links there is a formatting error with the page
        if len(downloadLinks) > 0:
            downloadLink = downloadLinks[0]
            #if it doesn't end with .apk it's a pay app
            if downloadLink[-4:] == ".apk":
                #print domain+downloadLink
                downloadApp(domain+downloadLink,outputPath,getAppName(html))
                appsDownloaded += 1
                if appsDownloaded % 5 == 0:
                    print "****** "+str(appsDownloaded) + " Apps downloaded ******"
            else:
                errorFile.write("$$$$$$ Pay app found at "+domain+page+" $$$$$$\n")
        else:
            errorFile.write("XXXXXX Formating Error with page "+domain+page+" XXXXXX\n")

errorFile.close()       
print str(appsExamined)+" apps examined"
print str(appsDownloaded)+" apps downloaded"
