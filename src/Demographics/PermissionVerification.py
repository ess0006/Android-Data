'''
Created on May 1, 2014

@author: ess0006
'''

import os
import re
        
if __name__ == '__main__':
    dataDirectory = "C:\\apks\\decompiled"
    markets = ["appsapk", "fdroid", "slideme"]
    
    def extractData(location, market):
        count = 0
        numRead = 0
        
        path = location+'\\'+market
        files = os.listdir(path)
        
        for f in files:
            if count % 50 == 0:
                print "current count: " + str(count)
            
            filePath = path + "\\"+ f 
        
            if os.path.exists(filePath+"\\AndroidManifest.xml"):
                ins = open( filePath+"\\AndroidManifest.xml", "r" )
                numRead = numRead + 1
                
                #regex = "<uses-permission(.*?)android.permission.INTERNET(.*?)>"
                regex = "uses-sdk"
                for line in ins:
                    matches = re.findall(regex, line)
                    if(len(matches) > 0):
                        count = count + 1
                        break
                        
        print count
        print numRead
        return count
  
    totalCount = extractData(dataDirectory,markets[0])
    totalCount = totalCount + extractData(dataDirectory,markets[1])
    totalCount = totalCount + extractData(dataDirectory,markets[2])
    print totalCount
    print "DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"