'''
This class looks for method calls that are known to cause exceptions, based on the list presented in http://istlab.dmst.aueb.gr/~mkehagia/api-exceptions.pdf
Created on Jun 23, 2014

@author: Eric Shaw
'''
import re
import fileinput
import AndroidViews

class BadSmellMethodCalls(object):

    def __init__(self, sourceCodePaths, layoutPaths):
        '''
        Constructor
        '''
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.dismiss = 0
        self.show = 0
        self.setContentView = 0
        self.createScaledBitmap = 0
        self.onKeyDown = 0
        self.isPlaying = 0
        self.unregisterReceiver = 0
        self.onBackPressed = 0
        self.showDialog = 0
        self.create = 0
        
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
        for line in fileinput.input([path]):
            matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->dismiss\(", line)
            if len(matches) > 0:
                self. dismiss = self.dismiss + 1
            matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->show\(", line)
            if len(matches) > 0:
                self.show = self.show + 1
            matches = re.findall("invoke-virtual (.*?), (.*?);->setContentView\(", line)
            if len(matches) > 0:
                self.setContentView = self.setContentView + 1
            matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->createScaledBitmap\(", line)
            if len(matches) > 0:
                self. createScaledBitmap = self.createScaledBitmap + 1
            matches = re.findall("invoke-virtual (.*?), (.*?);->onKeyDown\(", line)
            if len(matches) > 0:
                self.onKeyDown = self.onKeyDown + 1
            matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->isPlaying\(", line)
            if len(matches) > 0:
                self.isPlaying = self.isPlaying + 1
            matches = re.findall("invoke-virtual (.*?), (.*?);->unregisterReceiver\(", line)
            if len(matches) > 0:
                self.unregisterReceiver = self.unregisterReceiver + 1
            matches = re.findall("invoke-virtual (.*?), (.*?);->onBackPressed\(", line)
            if len(matches) > 0:
                self. onBackPressed = self.onBackPressed + 1
            matches = re.findall("invoke-virtual (.*?), (.*?);->showDialog\(", line)
            if len(matches) > 0:
                self.showDialog = self.showDialog + 1
            matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->create\(", line)
            if len(matches) > 0:
                self.create = self.create + 1
                
    
    def extractLayoutFileData(self, path):
        fileinput.close()
        
                
    
    def getNumShowCalls(self):
        return self.show
    
    def getNumDismissCalls(self):
        return self.dismiss
    
    def getNumSetContentViewCalls(self):
        return self.setContentView
    
    def getNumCreateScaledBitmapCalls(self):
        return self.createScaledBitmap
    
    def getNumOnKeyDownCalls(self):
        return self.onKeyDown
    
    def getNumIsPlayingCalls(self):
        return self.isPlaying
    
    def getNumUnregisterRecieverCalls(self):
        return self.unregisterReceiver
    
    def getNumOnBackPressedCalls(self):
        return self.onBackPressed
    
    def getNumShowDialogCalls(self):
        return self.showDialog
    
    def getNumCreateCalls(self):
        return self.create
    
    def printData(self):
        print ""
            