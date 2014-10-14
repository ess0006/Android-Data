'''
This class counts the number of unchecked Intent Bundles per app.
Created on Jan 27, 2014

@author: ess0006
'''
import re
import fileinput
import AndroidViews

class UncheckedBundles(object):
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
        self.numBundles = 0
        self.numCheckedBundles = 0
        self.inTryCatch = False
        
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
        bundleAssignment = ".local (.*?):Landroid/os/Bundle;"
        bundleRegisters = []
        self.inTryCatch = False
        for line in fileinput.input([path]):
            if line.startswith(":try_start"):
                self.inTryCatch = True
            if line.startswith(":try_end"):
                self.inTryCatch = False
            matches = re.findall(bundleAssignment, line)
            if len(matches) > 0 and not ".end" in line:
                reg = matches[0][0:matches[0].find(",")]
                if not reg in bundleRegisters and not self.inTryCatch:
                    bundleRegisters.append(reg)
                self.numBundles = self.numBundles + 1
            else:
                if len(bundleRegisters) != 0:
                    nullCheck = "(if-nez|if-eqz) "
                    regName = ""
                    for reg in bundleRegisters:
                        matches = re.findall(nullCheck + reg, line)
                        if len(matches) > 0:
                            self.numCheckedBundles = self.numCheckedBundles + 1
                            regName = reg
                    if regName != "":
                        bundleRegisters.remove(regName)
           
    
    def extractLayoutFileData(self, path):
        fileinput.close()
        tempMax = 0
        viewRegex = "<" + AndroidViews.getAndroidViewsRegex()
        for line in fileinput.input([path]):
                numMatches = len(re.findall(viewRegex, line))
                
    def getNumCheckedBundles(self):
        return self.numCheckedBundles
    
    def getNumUncheckedBundles(self):
        return self.numBundles - self.numCheckedBundles
    
    def getObjectMap(self):
        return self.objMap
    
    def printData(self):
        print ""
            