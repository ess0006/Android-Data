'''
Created on Jan 26, 2012

@author: symonwi
@author: Eric Shaw
@version: 1/21/2014
'''
import urllib
import re

def getPageCount(url):
    applicationsPage = url+"/android/all-apps/page/1"
    numOfPagesExp = "http://www.appsapk.com/android/all-apps/page/(\d+)/"
   
    site = urllib.urlopen(applicationsPage)
    html = site.read()
    site.close()
   
    list = re.findall(numOfPagesExp, html)
    numOfPages = int(list[-1])
    return numOfPages

def getHTML(url):
    site = urllib.urlopen(url)
    html = site.read()
    site.close()
    return html

def getApplicationPageLinks(html):
    htmlsub = html[html.index("<h1 class=\"page-title\">All Apps</h1>"):html.index("class=\"pagenav clearfix\">")]
    appPageExp ="href=\"(.*?)\" title"
    #appPageExp = "<h2 class=\"title\"><a href=\"(/application/.*?)\""
    return re.findall(appPageExp, htmlsub)

def getDownloadLinks(html):
    downloadLinkExp = "href=\"(.*?)\.apk"
    ret = re.findall(downloadLinkExp, html)
    return ret

def downloadApp(url, path, appName):
    f = open(path+"appsapk_"+appName+".apk", "wb")
    app = urllib.urlopen(url)
    f.write(app.read())
    f.close()
    app.close()

def getAppName(link):
    appNameExp = "http://www.appsapk.com/(.*?)/"
    list = re.findall(appNameExp, link)
    return list[-1].translate(None, "<>:\"/\|?*")
   

#############################################################################

domain = "http://www.appsapk.com/"
outputPath = "C:\\apks\\downloaded\\appsapk\\"
appsExamined = 0
appsDownloaded = 0




#this is where we will any errors we experience while downloading apps such as
#a problem with the formatting or if the app cost money to buy
errorFile = open(outputPath+"appsapk_errors.txt", "w")

numOfPages = getPageCount(domain)

print "Downloading apps from "+str(numOfPages)+" pages . . ."
print "Scanning approximately "+str(numOfPages*7)+" apps for candidates . . ."

start = 1
for i in range(start,numOfPages+1):
    #set up the page url
    print "!!!!!!beginning page #"+str(i)+" !!!!!!"
    currentPage = domain+"/android/all-apps/page/"+str(i)
   
    #get the html code
    html = getHTML(currentPage)
   
    #extract the links to the actual application pages
    applicationPages = getApplicationPageLinks(html)
   
    #for each page parse to see if it is a free app and if so download
    for page in applicationPages:
        #get the html code
        html = getHTML(page)
        #extract the links
        downloadLinks = getDownloadLinks(html)
        appsExamined += 1
        #give status update for each 100 downloaded
        if appsExamined % 5 == 0:
            print "****** "+str(appsExamined) + " Apps examined ******"
       
        #if no links there is a formatting error with the page
        if len(downloadLinks) > 0:
            downloadLink = downloadLinks[0]
            
            #print domain+downloadLink
            downloadApp(downloadLink + '.apk',outputPath,getAppName(page))
            appsDownloaded += 1
            if appsDownloaded % 5 == 0:
                print "****** "+str(appsDownloaded) + " Apps downloaded ******"
           
        else:
            errorFile.write("XXXXXX Formating Error with page "+page+" XXXXXX\n")

errorFile.close()       
print str(appsExamined)+" apps examined"
print str(appsDownloaded)+" apps downloaded"
