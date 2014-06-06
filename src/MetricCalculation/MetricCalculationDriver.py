'''
Created on Jan 22, 2014

@author: ess0006
'''
import os
import os.path
import xml.dom.minidom as minidom
import ManifestDataExtractor as mde
import SizeMetrics
import CKMetrics
import MVCMetrics
import OtherMetrics
import DBWriter
import sys
import traceback

ignoreFiles = ['BuildConfig.smali', 'R$attr.smali', 'R$dimen.smali', 'R$drawable.smali', 'R$id.smali',
'R$layout.smali','R$menu.smali','R$string.smali','R$style.smali','R.smali']


def getSourceCodeDirectoryPaths(root, packageName):
    os.chdir(root)
    dirNames = os.listdir(os.getcwd())
    firstIdentifier = packageName.split('.')[0]
    secondIdentifier = packageName.split('.')[1]
    dirPaths = []
    dirPaths.append(root + "\\" + firstIdentifier + "\\" + secondIdentifier)
    return dirPaths

def parseManifest(manifestDataExt,filePath):
    
        
    #EXTRACTING APP LABEL
    appLabel = manifestDataExt.extractAppLabel()
    try:
        print "App Label -> " + appLabel
    except:
        appLabel = "DATA NOT FOUND - INVALID ENCODING"
        print "App Label -> " + appLabel
                
    #EXTRACTING FULLY QUALIFIED APP NAME
    appFQName = manifestDataExt.extractFQName()
    print "Fully Qualified Name -> " + appFQName
    
    return appLabel, appFQName



decFolderPath =  'C:\\apks\\EmployeeListApp_dec'#'C:\\apks\\EmployeeListApp_dec'

def extractData(location, market):
    db = DBWriter.DBWriter()
    db.connect()
    
    path = location+market
    files = os.listdir(path)
    directorySize = len(files)
    errorFile = open(path+"_"+market+"_metric_errors.txt", "w")
    
    print "!"*150
    print "NOW EXTRACTING DATA FROM " + path
    print str(directorySize)+" APPS FOUND"
    print "!"*150
    
    i = 1
    for f in files:
        sourceCodePaths = []
        layoutFilePaths = []
        decFolderPath = path + "\\"+ f    
        filename = f + ".apk"
        #PRINTING HEADER
        print "*"*50
        print "EXTRACTING DATA FROM FILE "+ str(i) +" OF "+ str(directorySize)
        print "*"*50
        i += 1
        
        try:
            manifestDataExt = mde.ManifestDataExtractor(decFolderPath)
            
            #TODO: When in loop, need to check that manifest is valid
            if manifestDataExt.validateManifest():
                #get app name and package name from manifest
                appLabel, packageName = parseManifest(manifestDataExt,decFolderPath)
                
                #get path for each source code file that we will consider
                smaliPath = decFolderPath + '\\smali'
                dirPaths = getSourceCodeDirectoryPaths(smaliPath, packageName)
                #navigate using fully qualified packageName
                for codeDir in dirPaths:
                    for root, dirs, files in os.walk(codeDir):
                        for file in files:
                            if file not in ignoreFiles:
                                sourceCodePaths.append(os.path.join(root, file))
                                
                print sourceCodePaths
                
                if len(sourceCodePaths) == 0:
                    errorFile.write(f + ": No source code files\n")
                    continue
                
                layoutPath = decFolderPath + '\\res\\layout'
                for root, dirs, files in os.walk(layoutPath):
                    for file in files:
                        layoutFilePaths.append(os.path.join(root, file))
                        
                print layoutFilePaths
                
                #calculate size metrics
                sizeMetrics = SizeMetrics.SizeMetrics(sourceCodePaths)
                sizeMetrics.extractData()
                numInstructions = sizeMetrics.getNumInstructions()
                numMethods = sizeMetrics.getNumMethods()
                numClasses = sizeMetrics.getNumClasses()
                methodsPerClass = sizeMetrics.getMethodsPerClass()
                instrPerMethod = sizeMetrics.getInstructionsPerMethod()
                cyclomatic = sizeMetrics.getCyclomatic()
                wmc = sizeMetrics.getWMC()
                
                #calculate CK metrics
                ckMetrics = CKMetrics.CKMetrics(sourceCodePaths, packageName)
                ckMetrics.extractData()
                noc = ckMetrics.getNOC()
                dit = ckMetrics.getDIT()
                lcom = ckMetrics.getLCOM()
                cbo = ckMetrics.getCBO()
                ppiv = ckMetrics.getPPIV()
                apd = ckMetrics.getAPD()
                
                #calculate MVC metrics
                mvcMetrics =MVCMetrics.MVCMetrics(sourceCodePaths, layoutFilePaths)
                if appLabel == "3D Player":
                    print ""
                mvcMetrics.extractData()
                mvc = mvcMetrics.getSepVCScore()
                avgNumViewsInXML = mvcMetrics.getAvgNumViewsInXML()
                maxNumViewsInXML = mvcMetrics.getMaxNumViewsInXML()
                potBadToken = mvcMetrics.getPotentialBadTokenExceptions()
                
                #calculate other metrics
                otherMetrics = OtherMetrics.OtherMetrics(sourceCodePaths, layoutFilePaths)
                otherMetrics.extractData()
                uncheckedBundles = otherMetrics.getNumUncheckedBundles()
                
                db.writeAppTable(filename, appLabel, packageName, market)
                db.writeSizeMetricsTable(filename, numInstructions, numMethods, numClasses, methodsPerClass, instrPerMethod, cyclomatic, wmc)
                db.writeOOMetricsTable(filename, noc, dit, lcom, cbo, ppiv, apd)
                db.writeMVCMetricsTable(filename, mvc, avgNumViewsInXML, maxNumViewsInXML)
                db.writeOtherMetricsTable(filename, uncheckedBundles, potBadToken)
                
            else:
                print "ERROR FOUND WITH FILE AndroidManifest.xml"
                errorFile.write(f + ": ERROR FOUND WITH FILE AndroidManifest.xml\n")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            errorFile.write(f + ": " + ''.join('!! ' + line for line in lines) +"\n")
    errorFile.close()
        
if __name__ == "__main__":
    extractData("C:\\apks\\decompiled\\","slideme")
    extractData("C:\\apks\\decompiled\\","fdroid")
    extractData("C:\\apks\\decompiled\\","appsapk")