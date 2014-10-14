'''
This class collects app ratings and other metadata about the slideme apps.
Created on Jan 28, 2014

@author: Eric
'''
import urllib
import re
import os
import ManifestDataExtractor as mde
import sys
import DBWriter

def getHTML(url):
    site = urllib.urlopen(url)
    html = site.read()
    site.close()
    return html

def parseManifest(manifestDataExt, filePath):
    
        
    # EXTRACTING APP LABEL
    appLabel = manifestDataExt.extractAppLabel()
    try:
        print "App Label -> " + appLabel
    except:
        appLabel = "DATA NOT FOUND - INVALID ENCODING"
        print "App Label -> " + appLabel
                
    # EXTRACTING FULLY QUALIFIED APP NAME
    appFQName = manifestDataExt.extractFQName()
    print "Fully Qualified Name -> " + appFQName
    
    return appLabel, appFQName

if __name__ == '__main__':
    pass


path = "C:\\apks\\decompiled\\slideme"
files = os.listdir(path)
directorySize = len(files)
errorFile = open(path + "_ratings_errors.txt", "w")
    
print "!"*150
print "NOW EXTRACTING DATA FROM " + path
print str(directorySize) + " APPS FOUND"
print "!"*150

db = DBWriter.DBWriter()
db.connect()

i = 1
for f in files:
    
    try:
        filename = f + ".apk"
        
        decFolderPath = "C:\\apks\\decompiled\\slideme" + "\\" + f
        manifestDataExt = mde.ManifestDataExtractor(decFolderPath)
        
        # TODO: When in loop, need to check that manifest is valid
        if manifestDataExt.validateManifest():
            # get app name and package name from manifest
            appname, packageName = parseManifest(manifestDataExt, decFolderPath)
            appname = appname.replace(' ', '-').lower()
            
            
            url = "http://slideme.org/application/" + appname
            html = getHTML(url)
            ratingExp = "average-rating\">Average: <span>(\d+\.\d*|\d+)"
            appRating = float(re.findall(ratingExp, html)[0])
            
            numRatingsExp = "total-votes\">\(<span>(\d+)"
            numRatings = int(re.findall(numRatingsExp, html)[0])
            
            numDownloadsExp = "downloads\">(\d+)"
            numDownloads = int(re.findall(numDownloadsExp, html)[0])
            
            db.writeRatingsTable(filename, appRating, numRatings, numDownloads)
            
            print appname
            print 'Rating: ' + str(appRating)
            print 'Num Ratings: ' + str(numRatings)
            print 'Num Downloads: ' + str(numDownloads)
            
            i += 1
    except:
            e = sys.exc_info()[0]
            errorFile.write(f + ": " + str(e) + "\n")
print str(i) + " apps examined"
