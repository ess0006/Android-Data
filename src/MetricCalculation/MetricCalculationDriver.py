'''
This is the driver program for the collection of quality related metrics on a set of reverse engineered .apk files.
Before running, the user should set up his database to match the expected schemas.  I would recommend commenting out
the db.write methods at first to ensure the program runs properly.  Once the DB is set up, only the extractData method
needs to be changed to hold the correct paths to your apps.
Created on Jan 22, 2014

@author: Eric Shaw
'''
import os
import os.path
import xml.dom.minidom as minidom
import ManifestDataExtractor as mde
import SizeMetrics
import CKMetrics
import MVCMetrics
import OtherMetrics
import BadSmellMethodCalls
import UncheckedBadSmellMethodCalls
import BatteryMetrics
import BlackHole
import NetworkTimeout
import ANRMetrics
import IntentLaunchMetrics
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
                    #errorFile.write(f + ": No source code files\n")
                    continue
                
                layoutPath = decFolderPath + '\\res\\layout'
                for root, dirs, files in os.walk(layoutPath):
                    for file in files:
                        layoutFilePaths.append(os.path.join(root, file))
                        
                print layoutFilePaths
                
                """
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
                mvcMetrics.extractData()
                mvc = mvcMetrics.getSepVCScore()
                avgNumViewsInXML = mvcMetrics.getAvgNumViewsInXML()
                maxNumViewsInXML = mvcMetrics.getMaxNumViewsInXML()
                potBadToken = mvcMetrics.getPotentialBadTokenExceptions()
                numFragments = mvcMetrics.getNumFragments()
                
                
                #calculate other metrics
                otherMetrics = OtherMetrics.OtherMetrics(sourceCodePaths, layoutFilePaths)
                otherMetrics.extractData()
                uncheckedBundles = otherMetrics.getNumUncheckedBundles()
                objMap = otherMetrics.getObjectMap()"""
                
                #bad smell methods
                bsmc = BadSmellMethodCalls.BadSmellMethodCalls(sourceCodePaths, layoutFilePaths)
                bsmc.extractData()
                show = bsmc.getNumShowCalls()
                dismiss = bsmc.getNumDismissCalls()
                setContentView = bsmc.getNumSetContentViewCalls()
                createScaledBitmap = bsmc.getNumCreateScaledBitmapCalls()
                onKeyDown = bsmc.getNumOnKeyDownCalls()
                isPlaying = bsmc.getNumIsPlayingCalls()
                unregisterReceiver = bsmc.getNumUnregisterRecieverCalls()
                onBackPressed = bsmc.getNumOnBackPressedCalls()
                showDialog = bsmc.getNumShowDialogCalls()
                create = bsmc.getNumCreateCalls()
                
                #checked bad smell methods
                cbsmc = UncheckedBadSmellMethodCalls.UncheckedBadSmellMethodCalls(sourceCodePaths, layoutFilePaths)
                cbsmc.extractData()
                cshow = cbsmc.getNumShowCalls()
                cdismiss = cbsmc.getNumDismissCalls()
                csetContentView = cbsmc.getNumSetContentViewCalls()
                ccreateScaledBitmap = cbsmc.getNumCreateScaledBitmapCalls()
                conKeyDown = cbsmc.getNumOnKeyDownCalls()
                cisPlaying = cbsmc.getNumIsPlayingCalls()
                cunregisterReceiver = cbsmc.getNumUnregisterRecieverCalls()
                conBackPressed = cbsmc.getNumOnBackPressedCalls()
                cshowDialog = cbsmc.getNumShowDialogCalls()
                ccreate = cbsmc.getNumCreateCalls()
                
                """
                #Battery Life metrics
                batteryMetrics = BatteryMetrics.BatteryMetrics(sourceCodePaths, layoutFilePaths)
                batteryMetrics.extractData()
                noTimeoutWakeLocks = batteryMetrics.getNumNoTimeoutWakeLocks()
                locListeners = batteryMetrics.getNumLocationListeners()
                gpsUses = batteryMetrics.getNumGpsUses()
                domParsers = batteryMetrics.getNumDomParsers()
                saxParsers = batteryMetrics.getNumSaxParsers()
                xmlPullParsers = batteryMetrics.getNumXMLPullParsers()
                
                #network timeout metrics
                networkTimeout = NetworkTimeout.NetworkTimeout(sourceCodePaths, layoutFilePaths)
                networkTimeout.extractData()
                httpClients = networkTimeout.getNumHttpClients()
                numConTimeouts = networkTimeout.getNumConTimeouts()
                numSoTimeouts = networkTimeout.getNumSoTimeouts()
                numNoConTimeouts = networkTimeout.getNumNoConTimeout()
                numNoSoTimeouts = networkTimeout.getNumNoSoTimeout()
                
                #black hole exception handling
                blackHole = BlackHole.BlackHole(sourceCodePaths, layoutFilePaths)
                blackHole.extractData()
                numCatchBlocks = blackHole.getNumCatchBlocks()
                numLogOnly = blackHole.getNumLogOnly()
                numNoAction = blackHole.getNumNoAction()
                
                #ANR Metrics
                anrMetrics = ANRMetrics.ANRMetrics(sourceCodePaths, layoutFilePaths)
                anrMetrics.extractData()
                network = anrMetrics.getNumNetworkOnMainThread()
                sqlLite = anrMetrics.getNumSQLLiteOnMainThread()
                fileIO = anrMetrics.getNumFileIOOnMainThread()
                bitmap = anrMetrics.getNumBitmapOnMainThread()
                networkBg = anrMetrics.getNumNetworkOnBgThread()
                sqlLiteBg = anrMetrics.getNumSQLLiteOnBgThread()
                fileIOBg = anrMetrics.getNumFileIOOnBgThread()
                bitmapBg = anrMetrics.getNumBitmapOnBgThread()
                
                #intent launch metrics
                intentLaunchMetrics = IntentLaunchMetrics.IntentLaunchMetrics(sourceCodePaths, layoutFilePaths, packageName)
                intentLaunchMetrics.extractData()
                startActivities = intentLaunchMetrics.getNumStartActivities()
                startActivity = intentLaunchMetrics.getNumStartActivity()
                startInstrumentation = intentLaunchMetrics.getNumStartInstrumentation()
                startIntentSender = intentLaunchMetrics.getNumStartIntentSender()
                startService = intentLaunchMetrics.getNumStartService()
                startActionMode = intentLaunchMetrics.getNumStartActionMode()
                startActivityForResult = intentLaunchMetrics.getNumStartActivityForResult()
                startActivityFromChild = intentLaunchMetrics.getNumStartActivityFromChild()
                startActivityFromFragment = intentLaunchMetrics.getNumStartActivityFromFragment()
                startActivityIfNeeded = intentLaunchMetrics.getNumStartActivityIfNeeded()
                startIntentSenderForResult = intentLaunchMetrics.getNumStartIntentSenderForResult()
                startIntentSenderFromChild = intentLaunchMetrics.getNumStartIntentSenderFromChild()
                startNextMatchingActivity = intentLaunchMetrics.getNumStartNextMatchingActivity()
                startSearch = intentLaunchMetrics.getNumStartSearch()
                
                db.writeAppTable(filename, appLabel, packageName, market)
                db.writeSizeMetricsTable(filename, numInstructions, numMethods, numClasses, methodsPerClass, instrPerMethod, cyclomatic, wmc)
                db.writeOOMetricsTable(filename, noc, dit, lcom, cbo, ppiv, apd)
                db.writeMVCMetricsTable(filename, mvc, avgNumViewsInXML, maxNumViewsInXML)
                db.writeOtherMetricsTable(filename, uncheckedBundles, potBadToken)
                db.updateNumFragments(filename,numFragments)
                db.writeAndroidObjectsTable(filename, objMap)
                db.writeBadSmellMethodCallsTable(filename, show, dismiss, setContentView, createScaledBitmap, onKeyDown, isPlaying, unregisterReceiver, onBackPressed, showDialog, create)
                db.writeUncheckedBadSmellMethodCallsTable(filename, cshow, cdismiss, csetContentView, ccreateScaledBitmap, conKeyDown, cisPlaying, cunregisterReceiver, conBackPressed, cshowDialog, ccreate)
                db.writeBatteryMetrics(filename, noTimeoutWakeLocks, locListeners, gpsUses, domParsers, saxParsers, xmlPullParsers)
                db.writeNetworkTimeoutMetrics(filename, httpClients, numConTimeouts, numSoTimeouts, numNoConTimeouts, numNoSoTimeouts)
                db.writeBlackHole(filename, numCatchBlocks, numLogOnly, numNoAction)
                db.writeANRMetrics(filename, network, sqlLite, fileIO, bitmap, networkBg, sqlLiteBg, fileIOBg, bitmapBg)
                db.writeIntentLaunchMetrics(filename, startActivities, startActivity, startInstrumentation, startIntentSender, startService, startActionMode, startActivityForResult, startActivityFromChild, startActivityFromFragment, startActivityIfNeeded, startIntentSenderForResult, startIntentSenderFromChild, startNextMatchingActivity, startSearch)"""
                db.updateCreateScaledBitmap(filename, ccreateScaledBitmap)
            else:
                print "ERROR FOUND WITH FILE AndroidManifest.xml"
                #errorFile.write(f + ": ERROR FOUND WITH FILE AndroidManifest.xml\n")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            #errorFile.write(f + ": " + ''.join('!! ' + line for line in lines) +"\n")
    errorFile.close()
        
if __name__ == "__main__":
    extractData("C:\\apks\\decompiled\\","slideme")
    extractData("C:\\apks\\decompiled\\","fdroid")
    extractData("C:\\apks\\decompiled\\","appsapk")