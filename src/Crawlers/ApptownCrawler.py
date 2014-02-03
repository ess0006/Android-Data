'''
Created on Jan 29, 2012

@author: Billy Symon
'''
import urllib
import re

#TODO
def getPageCount(url):
    numOfPagesExp = "&nbsp;<span class=\"nav-dots right-delimiter\">...</span>&nbsp;<a class=\"nav-page right-delimiter\" href=\"http://www.apptown.com/Android/\?page=(\d+)\""
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

def getDownloadLinks(html):
    downloadLinkExp = "<a href=\"./download_free_products.php\?id=(.*?)\">Download Now</a>"
    return re.findall(downloadLinkExp, html)

def downloadApp(url, path, appName):
    f = open(path+"apptown_"+appName+".apk", "wb")
    app = urllib.urlopen(url)
    f.write(app.read())
    f.close()
    app.close()


#############################################################################

domain = "http://www.apptown.com/android"
outputPath = "C:\\apks\\downloaded\\apptown\\"
appsDownloaded = 0




#this is where we will any errors we experience while downloading apps such as
#a problem with the formatting or if the app cost money to buy
errorFile = open(outputPath+"apptown_errors.txt", "w")

numOfPages = getPageCount(domain)

print "Downloading apps from "+str(numOfPages)+" pages . . ."
print "Scanning approximately "+str(numOfPages*13)+" apps for canidates . . ."

##for i in range(numOfPages+1):
for i in range(numOfPages+1):
    #set up the page url
    print "!!!!!!begining page #"+str(i)+" !!!!!!"
    currentPage = domain+"?page="+str(i)
    
    #get the html code
    try:
        html = getHTML(currentPage)
    
        downloadLinks = getDownloadLinks(html)
        for link in downloadLinks:
            try:
                downloadApp("http://www.apptown.com/download_free_products.php?id="+link, outputPath, link)
                appsDownloaded += 1
                if appsDownloaded % 5 == 0:
                    print "****** "+str(appsDownloaded) + " Apps downloaded ******"
            except:
                errorFile.write("Problem downloadig app at http://www.apptown.com/download_free_products.php?id="+link+"\n")
    except:
        errorFile.write("Problem geting html from "+currentPage+"\n")

errorFile.close()        

print str(appsDownloaded)+" apps downloaded"
 
