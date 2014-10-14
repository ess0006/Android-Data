'''
This measures four metrics related to ANR, the use of each of the following on the main thread:
networking
file IO
SQL Lite
bitmaps

Created on July 14, 2014

@author: Eric Shaw
'''
import re
import fileinput

class ANRMetrics(object):
    '''
    classdocs
    '''
    
    def __init__(self, sourceCodePaths, layoutPaths):
        '''
        Constructor
        '''
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numNetworkOnMainThread = 0
        self.numSQLLiteOnMainThread = 0
        self.numFileIOOnMainThread = 0
        self.numBitmapOnMainThread = 0
        self.numNetworkOnBgThread = 0
        self.numSQLLiteOnBgThread = 0
        self.numFileIOOnBgThread = 0
        self.numBitmapOnBgThread = 0
        
    def getNumberofFiles(self):
        return self.numFiles
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        #for path in self.layoutPaths:
            #self.extractLayoutFileData(path)
        self.printData()
    
    def extractSrcFileData(self, path):
        fileinput.close()
        isActivity = False
        activityRegex = ".super Landroid/app/(.*?)Activity;" #since it is difficult to see how data is passed, consider only code in activities to be run on UI thread
        httpRequestRegex1 = "Landroid/net/http/AndroidHttpClient;->execute\("
        httpRequestRegex2 = "Lorg/apache/http/impl/client/DefaultHttpClient;->execute\("
        fileIORegex = "new-instance(.*?)Ljava/io/File"
        sqlLiteMethodRegex = "Landroid/database/sqlite/SQLiteDatabase;->(.*?)\("
        bitmapRegex = "Landroid/graphics/BitmapFactory;->decode(.*?)\("

        for line in fileinput.input([path]):
            
            matches = re.findall(activityRegex, line)
            if len(matches) > 0:
                isActivity = True
                
            if isActivity:
                matches1 = re.findall(httpRequestRegex1, line)
                matches2 = re.findall(httpRequestRegex2, line)
                if len(matches1) > 0 or len(matches2) > 0:
                    self.numNetworkOnMainThread = self.numNetworkOnMainThread + 1
                    
                matches = re.findall(sqlLiteMethodRegex, line)
                if len(matches) > 0:
                    self.numSQLLiteOnMainThread = self.numSQLLiteOnMainThread + 1
                    
                matches = re.findall(fileIORegex, line)
                if len(matches) > 0:
                    self.numFileIOOnMainThread = self.numFileIOOnMainThread + 1
                    
                matches = re.findall(bitmapRegex, line)
                if len(matches) > 0:
                    self.numBitmapOnMainThread = self.numBitmapOnMainThread + 1
                
            else:
                matches1 = re.findall(httpRequestRegex1, line)
                matches2 = re.findall(httpRequestRegex2, line)
                if len(matches1) > 0 or len(matches2) > 0:
                    self.numNetworkOnBgThread = self.numNetworkOnBgThread + 1
                    
                matches = re.findall(sqlLiteMethodRegex, line)
                if len(matches) > 0:
                    self.numSQLLiteOnBgThread = self.numSQLLiteOnBgThread + 1
                    
                matches = re.findall(fileIORegex, line)
                if len(matches) > 0:
                    self.numFileIOOnBgThread = self.numFileIOOnBgThread + 1
                    
                matches = re.findall(bitmapRegex, line)
                if len(matches) > 0:
                    self.numBitmapOnBgThread = self.numBitmapOnBgThread + 1
    
    def extractLayoutFileData(self, path):
        pass
                
    def getNumNetworkOnMainThread(self):
        return self.numNetworkOnMainThread
    
    def getNumSQLLiteOnMainThread(self):
        return self.numSQLLiteOnMainThread
    
    def getNumFileIOOnMainThread(self):
        return self.numFileIOOnMainThread
    
    def getNumBitmapOnMainThread(self):
        return self.numBitmapOnMainThread

    def getNumNetworkOnBgThread(self):
        return self.numNetworkOnBgThread
    
    def getNumSQLLiteOnBgThread(self):
        return self.numSQLLiteOnBgThread
    
    def getNumFileIOOnBgThread(self):
        return self.numFileIOOnBgThread
    
    def getNumBitmapOnBgThread(self):
        return self.numBitmapOnBgThread

    def printData(self):
        print ""
            