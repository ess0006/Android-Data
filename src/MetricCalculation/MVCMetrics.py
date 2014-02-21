'''
Created on Jan 27, 2014

@author: ess0006
'''
import re
import fileinput
import AndroidViews

class MVCMetrics(object):
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
        self.numViewsInController = 0
        self.numViewsNotInController = 0
        self.sepVCScore = 0.0
        
    def getNumberofFiles(self):
        return self.numFiles
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        for path in self.layoutPaths:
            self.extractLayoutFileData(path)
        self.sepVCScore = self.calculateSepVCScore()
        self.printData()
    
    def extractSrcFileData(self, path):
        fileinput.close()
        viewInitRegex = "new-instance(.*?)Landroid/widget/" + AndroidViews.getAndroidViewsRegex()
        isController = False
        for line in fileinput.input([path]):
            if line.startswith('.super '):
                matches = re.findall("Landroid/app/(.*?)Activity", line)
                isController = (len(matches) > 0)
            else:
                matches = re.findall(viewInitRegex, line)
                if(len(matches) > 0):
                    if(isController):
                        self.numViewsInController = self.numViewsInController + 1
                    else:
                        self.numViewsNotInController = self.numViewsNotInController + 1
    
    def extractLayoutFileData(self, path):
        fileinput.close()
        viewRegex = "<" + AndroidViews.getAndroidViewsRegex()
        for line in fileinput.input([path]):
                numMatches = len(re.findall(viewRegex, line))
                self.numViewsNotInController = self.numViewsNotInController + numMatches
                
    def calculateSepVCScore(self):
        if(self.numViewsNotInController + self.numViewsInController == 0):
            return 0
        return self.numViewsNotInController / float(self.numViewsNotInController + self.numViewsInController) * 100
    
    def getNumViewsInController(self):
        return self.numViewsInController
    
    def getNumViewsNotInController(self):
        return self.numViewsNotInController
    
    def getSepVCScore(self):
        return self.sepVCScore
    
    def printData(self):
        print "Num views in controllers: " + str(self.numViewsInController)
        print "Num views not in controllers: " + str(self.numViewsNotInController)
        print "Percentage of Views Defined Outside of Controllers: " + str(self.sepVCScore) + "%"
            