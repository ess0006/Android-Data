'''
Created on Apr 14, 2012

@author: Billy Symon
'''
import os
import DBWriter
import re

dataDirectory = "C:\\apks\\decompiled"
markets = ["appsapk", "fdroid", "slideme"]


def extractLanguageLocData(location, market):
    path = location+'\\'+market
    files = os.listdir(path)
    directorySize = len(files)
    
    print "!"*150
    print "NOW EXTRACTING DATA FROM " + path
    print str(directorySize)+" APPS FOUND"
    print "!"*150
    
    i = 1
    for f in files[14001:14418]:
        layouts = []
        drawable = []
        resFilePath = path + "\\"+ f +'\\res'    
        #PRINTING HEADER
        print "*"*50
        print "EXTRACTING DATA FROM FILE "+ str(i) +" OF "+ str(directorySize)
        print "*"*50
        i += 1
        
        if os.path.exists(resFilePath):
            resContents = os.listdir(resFilePath)
            for content in resContents:
                #if content[0:7]=="values-":
                if re.match("layout-",content):
                    layouts.append(content[7:])
                if re.match("drawable-", content):
                    drawable.append(content[9:])
        filename =  f+".apk"
        print filename
        if len(layouts) > 0:
            for layout in layouts:
                DBWriter.writeLayoutLocDataEntry(filename, layout)
            print "layouts"
            print layouts
        if len(drawable) > 0:
            for draw in drawable:
                DBWriter.writeDrawableLocDataEntry(filename, draw)
            print "drawable"
            print drawable   

#extractLanguageLocData(dataDirectory, markets[0])
#extractLanguageLocData(dataDirectory, markets[1])
extractLanguageLocData(dataDirectory, markets[2])