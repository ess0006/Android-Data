'''
Created on Mar 21, 2012

@author: Billy Symon
'''
import os
import re

appNameExp = "<string name=\"app_name\">(.*?)</string>"
manifestNameExp = "<application android:label=\"(.*?)\""

filepath = "C:\\Users\\Billy Symon\\Desktop\\Grad Research\\GRAD THESIS [BACKUP_DO_NOT_USE]\\Decompiled Files\\"
market = "appsforadam\\"

dirs = os.listdir(filepath+market)
numFiles = len(dirs)

def getSize(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def getAppName(appDirectory):
    #print filepath+market+dir+"\\res\\values\\strings.xml"
    if os.path.exists(filepath+market+dir+"\\res\\values\\strings.xml"):
        stringsXML = open(filepath+market+dir+"\\res\\values\\strings.xml")
        XML = stringsXML.read()
        stringsXML.close()
        appName = re.findall(appNameExp, XML)
        if len(appName)>0:
            return appName[0]
    if os.path.exists(filepath+market+dir+"\\AndroidManifest.xml"):    
        manifestFile = open(filepath+market+dir+"\\AndroidManifest.xml")
        manifest = manifestFile.read()
        manifestFile.close()
        appName = re.findall(manifestNameExp,manifest)
        if len(appName)>0:
            return appName[0]
        else:
            return "NO NAME MENTION IN MANIFEST FILE"     
    return "NAME NOT FOUND"  

i = 1
for dir in dirs:
    print "****************************"
    print "-------App "+str(i)+" of "+str(numFiles)+"-------"
    marketName = market[:-1]
    print "Market Name -> " + marketName
    fileName = dir
    print "File Name/Key -> " + fileName
    try:
        size = getSize(filepath+market+dir)
    except:
        size = "UNKNOWN"
    print "Size in bytes -> " + str(size)
    appName = getAppName(filepath+market+dir)
    print "App name -> "+ appName
    i += 1
    print "****************************"

