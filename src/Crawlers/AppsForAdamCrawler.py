'''
Created on Jan 30, 2012

@author: Billy Symon
'''

import urllib
import re

#TODO
def getPageCount(url):
    numOfPagesExp = "class=\"pagination_last\">(\d+)</a>"
    site = urllib.urlopen(url)
    html = site.read()
    site.close()
    
    numOfPages = int(re.findall(numOfPagesExp, html)[0])
    return numOfPages

def getHTML(url):
    site = urllib.urlopen(url)
    html = site.read()
    site.close()
    return html

def getDownloadLinksAndNames(html):
    downloadLinkExp = "<a href=\"(http://appsforadam.tk/apps/(.*?))\" target=\"_blank\">Download</a></span></span><br />"
    return re.findall(downloadLinkExp, html)

def getAppPageLinks(html):
    applinkexp = "App: <a href=\"(.*?)\">"
    return re.findall(applinkexp, html)

def downloadApp(url, path, appName):
    f = open(path+"appsforadam_"+appName, "wb")
    app = urllib.urlopen(url)
    f.write(app.read())
    f.close()
    app.close()


#############################################################################

domain = "http://appsforadam.tk/search.php?action=results&sid=2d988417050b102d5c3a54d3028e7b61&sortby=dateline&order=desc&uid="
outputPath = "C:\\apks\\downloaded\\appsforadam\\"
appsDownloaded = 0




#this is where we will any errors we experience while downloading apps such as
#a problem with the formatting or if the app cost money to buy
errorFile = open(outputPath+"appsforadam_errors.txt", "w")

numOfPages = getPageCount(domain)

print "Downloading apps from "+str(numOfPages)+" pages . . ."
print "Scanning approximately "+str(numOfPages*20)+" apps for canidates . . ."

##for i in range(numOfPages+1):
for i in range(numOfPages+1):
    #set up the page url
    print "!!!!!!begining page #"+str(i)+" !!!!!!"
    currentPage = domain+"&page="+str(i)
    
    #get the html code
    try:
        html = getHTML(currentPage)
        appPages = getAppPageLinks(html)
        try:
            for page in appPages:
                downloadLinks = getDownloadLinksAndNames(html)
                for link in downloadLinks:
                    try:
                        downloadApp(link[0], outputPath, link[1])
                        appsDownloaded += 1
                        if appsDownloaded % 5 == 0:
                            print "****** "+str(appsDownloaded) + " Apps downloaded ******"
                    except:
                        errorFile.write("Problem downloadig app at "+link[0]+"\n")
        except:
            errorFile.write("Problem getting download links from "+page+"\n")
    except:
        errorFile.write("Problem geting html from "+currentPage+"\n")

errorFile.close()        

print str(appsDownloaded)+" apps downloaded"
 
