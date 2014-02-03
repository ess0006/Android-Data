'''
Created on Apr 14, 2012

@author: Billy Symon
'''
import os
import DBWriter
import re

dataDirectory = "C:\\Users\\Billy Symon\\Desktop\\Grad Research\\GRAD THESIS [BACKUP_DO_NOT_USE]\\Decompiled Files\\"
markets = ["appsforadam", "andapponline", "apptown"]

slideMeDirectory ="C:\\Users\\Billy Symon\\Desktop\\Grad Research\\GRAD THESIS [BACKUP_DO_NOT_USE]\\Decompiled Files\\slideme\\"
slideMeDirs = ["1","2","3","4","5"]

def extractLanguageLocData(location, market):
    path = location + market
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
        
extractLanguageLocData(slideMeDirectory, slideMeDirs[4])
 
