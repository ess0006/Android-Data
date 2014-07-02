'''
Created on Apr 14, 2012

@author: Billy Symon
'''
import os
import DBWriter
import re
import sys

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
    #languageData = []
    for f in files:
        languages = []
        resFilePath = path + "\\"+ f +'\\res'    
        #PRINTING HEADER
        print "*"*50
        print "EXTRACTING DATA FROM FILE "+ str(i) +" OF "+ str(directorySize)
        print "*"*50
        i += 1
        
        try:
            if os.path.exists(resFilePath):
                resContents = os.listdir(resFilePath)
                for content in resContents:
                    #if content[0:7]=="values-":
                    if (re.match("values-..$",content) or re.match("values-..-r.", content)):
                        languages.append(content[7:])
            filename =  f+".apk"
            if len(languages) > 0:
                for language in languages:
                    DBWriter.writeLanguageLocDataEntry(filename, language)
                print filename
                print languages
            else:
                print "No languages declared"
        except:
            e = sys.exc_info()[0]
            print e
        

#extractLanguageLocData(dataDirectory, markets[0])
#extractLanguageLocData(dataDirectory, markets[1])
extractLanguageLocData(dataDirectory, markets[2])
