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

ignoreFiles = ['BuildConfig.smali', 'R$attr.smali', 'R$dimen.smali', 'R$drawable.smali', 'R$id.smali',
'R$layout.smali','R$menu.smali','R$string.smali','R$style.smali','R.smali']

def getSourceCodeDirectoryPaths(root):
    os.chdir(root)
    dirNames = os.listdir(os.getcwd())
    if('android' in dirNames):
        dirNames.remove('android')
    dirPaths = []
    for name in dirNames:
        dirPaths.append(root + "\\" + name)
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
        #PRINTING HEADER
        print "*"*50
        print "EXTRACTING DATA FROM FILE "+ str(i) +" OF "+ str(directorySize)
        print "*"*50
        i += 1
        
        
        manifestDataExt = mde.ManifestDataExtractor(decFolderPath)
        
        #TODO: When in loop, need to check that manifest is valid
        if manifestDataExt.validateManifest():
            #get app name and package name from manifest
            ppName, packageName = parseManifest(manifestDataExt,decFolderPath)
            
            #get path for each source code file that we will consider
            smaliPath = decFolderPath + '\\smali'
            dirPaths = getSourceCodeDirectoryPaths(smaliPath)
            #navigate using fully qualified packageName
            for codeDir in dirPaths:
                for root, dirs, files in os.walk(codeDir):
                    for file in files:
                        if file not in ignoreFiles:
                            sourceCodePaths.append(os.path.join(root, file))
                            
            print sourceCodePaths
            
            layoutPath = decFolderPath + '\\res\\layout'
            for root, dirs, files in os.walk(layoutPath):
                for file in files:
                    layoutFilePaths.append(os.path.join(root, file))
                    
            print layoutFilePaths
            
            
            #calculate size metrics
            sizeMetrics = SizeMetrics.SizeMetrics(sourceCodePaths)
            sizeMetrics.extractData()
            
            #calculate CK metrics
            ckMetrics = CKMetrics.CKMetrics(sourceCodePaths, packageName)
            ckMetrics.extractData()
            
            mvcMetrics =MVCMetrics.MVCMetrics(sourceCodePaths, layoutFilePaths)
            mvcMetrics.extractData()
            
        else:
            print "ERROR FOUND WITH FILE AndroidManifest.xml"
            errorFile.write(f + ": ERROR FOUND WITH FILE AndroidManifest.xml")
    errorFile.close()
        
if __name__ == "__main__":
   extractData("C:\\apks\\decompiled\\","slideme")