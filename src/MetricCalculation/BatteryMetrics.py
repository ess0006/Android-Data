'''
Metrics gleaned from Google I/O presentation http://www.youtube.com/watch?v=OUemfrKe65c&feature=player_embedded
Created on Jun 27, 2014

@author: Eric Shaw
'''
import fileinput
import re

class BatteryMetrics(object):


    def __init__(self, sourceCodePaths, layoutPaths):
        '''
        Constructor
        '''
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numNoTimeoutWakeLocks = 0
        self.numLocListeners = 0
        self.numGpsUses = 0
        self.numXMLPullParser = 0
        self.numSaxParser = 0
        self.numDomParser = 0
        
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        for path in self.layoutPaths:
            self.extractLayoutFileData(path)
        
    def extractSrcFileData(self, path):
        fileinput.close()
        isLocListener = False
        wakeLockAcqRegex = "invoke-virtual(.*?)Landroid/os/PowerManager$WakeLock;->acquire()"
        domRegex = "invoke-virtual(.*?)Ljavax/xml/parsers/DocumentBuilderFactory;->newDocumentBuilder()"
        saxRegex = "invoke-virtual(.*?)Ljavax/xml/parsers/SAXParserFactory;->newSAXParser()"
        xmlppRegex = "invoke-static(.*?)Landroid/util/Xml;->newPullParser()"
        for line in fileinput.input([path]):
            matches = re.findall(wakeLockAcqRegex, line)
            if len(matches) > 0:
                self.numNoTimeoutWakeLocks = self.numNoTimeoutWakeLocks + 1
            if line.startswith(".implements Landroid/location/LocationListener;"):
                self.numLocListeners = self.numLocListeners + 1
                isLocListener = True
            if isLocListener:
                if "\"gps\"" in line:
                    self.numGpsUses = self. numGpsUses + 1
            matches = re.findall(domRegex, line)
            if len(matches) > 0:
                self.numDomParser = self.numDomParser + 1
            matches = re.findall(saxRegex, line)
            if len(matches) > 0:
                self.numSaxParser = self.numSaxParser + 1
            matches = re.findall(xmlppRegex, line)
            if len(matches) > 0:
                self.numXMLPullParser = self.numXMLPullParser + 1
                
    def extractLayoutFileData(self, path):
        pass
    
    def getNumNoTimeoutWakeLocks(self):
        return self.numNoTimeoutWakeLocks
    
    def getNumLocationListeners(self):
        return self.numLocListeners
    
    def getNumGpsUses(self):
        return self.numGpsUses
    
    def getNumDomParsers(self):
        return self.numDomParser
    
    def getNumSaxParsers(self):
        return self.numSaxParser
    
    def getNumXMLPullParsers(self):
        return self.numXMLPullParser
        