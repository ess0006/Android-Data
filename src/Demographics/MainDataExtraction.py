import os
import xml.dom.minidom as minidom
import DBWriter
import sys

dataDirectory = "C:\\apks\\decompiled"
markets = ["appsapk", "fdroid", "slideme"]

#slideMeDirectory ="C:\\Users\\Billy Symon\\Desktop\\Grad Research\\GRAD THESIS [BACKUP_DO_NOT_USE]\\Decompiled Files\\slideme\\"
#slideMeDirs = ["1","2","3","4","5"]


def extractData(location, market):
    path = location+'\\'+market
    files = os.listdir(path)
    directorySize = len(files)
    
    print "!"*150
    print "NOW EXTRACTING DATA FROM " + path
    print str(directorySize)+" APPS FOUND"
    print "!"*150
    
    i = 1
    for f in files:
        try:
            filePath = path + "\\"+ f    
            #PRINTING HEADER
            print "*"*50
            print "EXTRACTING DATA FROM FILE "+ str(i) +" OF "+ str(directorySize)
            print "*"*50
            i += 1
            
            if validateManifest(filePath):
                #EXTRACTING FILENAME
                fileName = f + ".apk"
                print "File Name -> " + fileName
            
                #EXTRACTING MARKET
                #market = "slideme"
                print "Market -> " + market
            
                #EXTRACTING FILE SIZE
                try:
                    fileSize = getFileSize(filePath)
                except:
                    fileSize = 0
                    writeError("?????"+filePath, "Error when gathering file size data")
                print "File Size -> " + str(fileSize) +" bytes"
            
                ####THE REMAINING EXTRACTED INFORMATION COMES FROM THE MANIFEST.XML FILE#####
                if os.path.exists(filePath+"\\AndroidManifest.xml"):
                    manifest = minidom.parse(filePath+"\\AndroidManifest.xml")
            
                #EXTRACTING APP LABEL
                appLabel = extractAppLabel(manifest,filePath)
                try:
                    print "App Label -> " + appLabel
                except:
                    appLabel = "DATA NOT FOUND - INVALID ENCODING"
                    print "App Label -> " + appLabel
                
                #EXTRACTING FULLY QUALIFIED APP NAME
                appFQName = extractFQName(manifest)
                print "Fully Qualified Name -> " + appFQName
              
                #EXTRACTING MIN SDK LEVEL
                minSDKLevel = extractMinSDKLevel(manifest)
                print "Minimum SDK Level -> " + minSDKLevel
                
                #EXTRACTING PERMISSIONS USED
                permissionsUsed = extractPermissionsUsed(manifest)
                numPermissionsUsed = len(permissionsUsed)
                print "Number of Permissions Requested -> " + str(numPermissionsUsed)
                if numPermissionsUsed > 0:
                    for permission in permissionsUsed:
                        try:
                            print "Permission Requested -> " + permission
                        except:
                            pass
                else:
                    print "No Permissions Requested"
                
                #EXTRACTING PERMISSIONS SET UP BY THE APP
                permissionsSetUp = extractPermissionsSetUp(manifest)
                numPermissionsSetUp = len(permissionsSetUp)
                print "Number of Permissions Set Up -> " + str(numPermissionsSetUp)
                if numPermissionsSetUp > 0:
                    for permission in permissionsSetUp:
                        print "Permission Set Up By App -> " + permission
                else:
                    print "No Permissions Set Up By App"
                
                #EXTRACTING PERMISSIONS REQUIRED TO INTERACT
                permissionsRequired = extractPermissionsRequired(manifest)
                numPremissionsRequired = len(permissionsRequired)
                print "Number of Permissions Required -> " + str(numPremissionsRequired)
                if numPremissionsRequired > 0:
                    for permission in permissionsRequired:
                        print "Permission Required to Interact with App -> " + permission
                else:
                    print "No Permissions Required to Interact with App"
                
                #EXTRACTING ACTIVITIES
                activities = extractActivities(manifest)
                numActivities = len(activities)
                print "Number of Activities -> " + str(numActivities)
                if numActivities > 0:
                    for activity in activities:
                        print "Activity -> " + activity
                else:
                    print "No Activities Declared"
                
                #EXTRACTING SERVICES
                services = extractServices(manifest)
                numServices = len(services)
                print "Number of Services -> " + str(numServices)
                if numServices > 0:
                    for service in services:
                        print "Service -> " + service
                else:
                    print "No Services Declared"
                
                #EXTRACTING RECEIVERS
                receivers = extractReceivers(manifest)
                numReceivers = len(receivers)
                print "Number of Receivers -> " + str(numReceivers)
                if numReceivers > 0:
                    for receiver in receivers:
                        print "Receiver -> " + receiver
                else:
                    print "No Receivers Declared"
                
                #EXTRACTING PROVIDERS
                providers = extractProviders(manifest)
                numProviders = len(providers)
                print "Number of Providers -> " + str(numProviders)
                if numProviders > 0:
                    for provider in providers:
                        print "Provider -> " + provider
                else:
                    print "No Providers Declared"
                
                #EXTRACTING LIBRARIES USED
                libraries = extractLibraries(manifest)
                numLibraries = len(libraries)
                print "Number of Libraries Used -> " + str(numLibraries)
                if numLibraries > 0:
                    for library in libraries:
                        print "Library -> " + library
                else:
                    print "No External Libraries Used"
                
                #EXTRACTING NUMBER OF LAYOUTS
                numLayouts = extractNumLayouts(filePath)
                print "Number of Layouts -> " + str(numLayouts)
                if numLayouts != 0:
                    altLayouts = checkAltLayouts(filePath)
                else:
                    altLayouts = "No"
                print "Alternative Layouts Provided -> " + altLayouts
                
                #EXTRACTING NUMBER OF STRINGS IN STRING.XML
                numStrings = extractNumStrings(filePath)
                print "Number of Strings -> " + str(numStrings)
                if numStrings > 0:
                    altStrings = checkAltStrings(filePath)
                else:
                    altStrings = "No"
                print "Alternative Strings Provided -> " + altStrings
                
                #WRITE DATA GATHERED OUT TO DATABASE
                ####################################
                #######VARABILES AVAILABLE##########
                ####################################
                #fileName -> name of the file including .apk extension [string]
                #market -> the name of the market from which the app came [string]
                #fileSize -> the size of the file in bytes [int]
                #appLabel -> the label displayed on the device for the application [string]
                #appFQName -> the fully qualified name of the app [string]
                #minSDKLevel -> the minimum sdk level needed to run the app [string]
                #numPermissionsUsed -> the number of permissions requested by the app [int]
                #permissionsUsed -> a list containing the names of the permissions used [list of strings]
                #numPermissionsSetUp -> the number of permissions set up by the app [int]
                #permissionsSetUp -> a list containing the names of the permissions set up by the app [list of strings]
                #numPremissionsRequired -> the number of permissions required to interact with the app [int]
                #permissionsRequired -> a list containing the names of the permissions required to interact app [list of strings]
                #numActivities -> the number of activities set up by the app [int]
                #activities -> a list containing all of the activities set up by the app [list of strings]
                #numServices -> the number of services set up by the app [int]
                #services -> a list containing all of the services set up by the app [list of strings]
                #numReceivers -> the number of receivers set up by the app [int]
                #receivers -> a list containing all of the receivers set up by the app [list of strings]
                #numProviders -> the number of providers set up by the app [int]
                #providers -> a list containing all of the providers set up by the app [list of strings]
                #numLibraries -> the number of external libraries used by the app [int]
                #libraries -> a list containing all of the libraries set up by the app [list of strings]
                #numLayouts -> the number of layouts present in the directory /res/layout [int]
                #altLayouts -> a string stating if alternative layouts are provided for the app [string (yes|no)]
                #numStrings -> the number of strings present in the file /res/value/strings.xml [int]
                #altStrings -> a string stating if alternative strings are provided for the app [string (yes|no)]
                
                
                #Printing DB Write Header
                print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "WRITING GATHERED DATA TO DATABASE..."
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                
                print fileName
                print market
                print fileSize
                print permissionsUsed
                DBWriter.writeAppInfoTableEnrty(fileName, market, fileSize, appLabel, appFQName)
                DBWriter.writePermissionsInfoTableEnrty(fileName, numPermissionsUsed, numPermissionsSetUp, numPremissionsRequired)
                DBWriter.writePermissionsRequestedTableEnrty(fileName, permissionsUsed)
                DBWriter.writePermissionsSetUpTableEnrty(fileName, permissionsSetUp)
                DBWriter.writePermissionsRequiredTableEnrty(fileName, permissionsRequired)
                DBWriter.writeIntentsTableEnrty(fileName, numActivities, numServices, numReceivers, numProviders)
                DBWriter.writeActivitiesTableEnrty(fileName, activities)
                DBWriter.writeServicesTableEnrty(fileName, services)
                DBWriter.writeReceiversTableEnrty(fileName, receivers)
                DBWriter.writeProvidersTableEnrty(fileName, providers)
                DBWriter.writeAditionalInfoTableEnrty(fileName, numLibraries, numLayouts, numStrings, minSDKLevel, altLayouts, altStrings)
                DBWriter.writeLibrariesTableEnrty(fileName, libraries)
                DBWriter.writeMasterEntry(fileName, market, fileSize, appLabel, appFQName, numPermissionsUsed, numPermissionsSetUp, numPremissionsRequired, numActivities, numServices, numReceivers, numProviders, numLibraries, numLayouts, numStrings, minSDKLevel, altLayouts, altStrings)
                
                print ""  
                                       
            else:
                print "DATA NOT FOUND - ERROR FOUND WITH FILE AndroidManifest.xml"
                print ""
                
        except:
            e = sys.exc_info()[0]
            writeError("XXXXX"+filePath, "Eror in driver body")
        
def getFileSize(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def extractNumStrings(path):
    if os.path.exists(path+"\\res\\values\\strings.xml"):
        try:
            xmlFile = minidom.parse(path+"\\res\\values\\strings.xml")
            strings = xmlFile.getElementsByTagName("string")
            return len(strings)
        except:
            writeError("OOOOO"+path+"\\res\\values\\strings.xml", "Error parsing strings.xlm in resources")
            return 0
    else:
        return 0        

def checkAltStrings(path):
    if os.path.exists(path+"\\res"):
        contents = os.listdir(path+"\\res")
        count = 0;
        for content in contents:
            if content[0:6] == "values":
                dirContents = os.listdir(path+"\\res\\"+content)
                if dirContents.count("strings.xml") > 0:
                    count += 1
        if count > 1:
            return "Yes"
    return "No"
    
def extractNumLayouts(path):
    if os.path.exists(path+"\\res\\layout"):
        return  len(os.listdir(path+"\\res\\layout"))
    else:
        return 0

def checkAltLayouts(path):
    if os.path.exists(path+"\\res"):
        contents = os.listdir(path+"\\res")
        count = 0;
        for content in contents:
            if content[0:6] == "layout":
                count += 1
        if count > 1:
            return "Yes"
    return "No"

def extractLibraries(manifest):
    libraries = []
    tags = manifest.getElementsByTagName("uses-library")
    for tag in tags:
        library = tag.getAttribute("android:name")
        libraries.append(library)
    return libraries

def extractProviders(manifest):
    providers = []
    tags = manifest.getElementsByTagName("provider")
    for tag in tags:
        provider = tag.getAttribute("android:name")
        providers.append(provider)
    return providers

def extractReceivers(manifest):
    receivers = []
    tags = manifest.getElementsByTagName("receiver")
    for tag in tags:
        receiver = tag.getAttribute("android:name")
        receivers.append(receiver)
    return receivers

def extractServices(manifest):
    services = []
    tags = manifest.getElementsByTagName("service")
    for tag in tags:
        service = tag.getAttribute("android:name")
        services.append(service)
    return services

def extractActivities(manifest):
    activities = []
    tags = manifest.getElementsByTagName("activity")
    for tag in tags:
        activity = tag.getAttribute("android:name")
        activities.append(activity)
    return activities
    
def extractPermissionsRequired(manifest):
    permissionsRequired = []
    tags = manifest.getElementsByTagName("application")
    for tag in tags:
        permission = tag.getAttribute("android:permission")
        if permission != "":
            permissionsRequired.append(permission)
    return permissionsRequired

def extractPermissionsSetUp(manifest):
    permissionsSetUp = []
    tags = manifest.getElementsByTagName("permission")
    for tag in tags:
        permission = tag.getAttribute("android:name")
        permissionsSetUp.append(permission)
    return permissionsSetUp
    
def extractPermissionsUsed(manifest):
    permissionsUsed = []
    tags = manifest.getElementsByTagName("uses-permission")
    for tag in tags:
        permission = tag.getAttribute("android:name")
        permissionsUsed.append(permission)
    return permissionsUsed

def extractMinSDKLevel(manifest):
    tag = manifest.getElementsByTagName("uses-sdk")
    if len(tag) > 0:
        for item in tag:
            sdkLevel = item.getAttribute("android:minSdkVersion")
            return sdkLevel
    else:
        return "UNKNOWN"

def extractFQName(manifest):
    tag = manifest.getElementsByTagName("manifest")
    for item in tag:
        fQName = item.getAttribute("package")
        return fQName

def extractAppLabel(manifest,path):
    tag = manifest.getElementsByTagName("application")
    for item in tag:
        appName = item.getAttribute("android:label")
        if len(appName) > 0:    
            if appName[0] == "@":
                return getResource(path, appName)
            else:
                return appName
        else:
            return "DATA NOT FOUND"
    
def validateManifest(filePath):
    if os.path.exists(filePath+"\\AndroidManifest.xml"):
        return True
    else:
        writeError("XXXXX"+filePath, "Unable to find AndroidManifest.xml")
        
def writeError(filePath, message):
    f = open("Extraction_error_log.txt", 'a')
    f.write(filePath + " -> " + message+"\n")
    f.close()
    
def getResource(path, appName):
    if os.path.exists(path+"\\res\\values\\strings.xml"):
        try:
            strings = minidom.parse(path+"\\res\\values\\strings.xml")
        except:
            return "DATA NOT FOUND - ERROR PARSING XML FILE"
        elements = strings.getElementsByTagName("string")
        for tag in elements:
            if tag.getAttribute("name") == appName[8:]:
                return tag.firstChild.nodeValue
        return "DATA NOT FOUND - No STRINGS.XML"
    else:
        return "DATA NOT FOUND - NO STRINGS.XML"
      
extractData(dataDirectory,markets[0])
extractData(dataDirectory,markets[1])
extractData(dataDirectory,markets[2])
#extractData(slideMeDirectory, slideMeDirs[0])
#extractData(slideMeDirectory, slideMeDirs[1])
#extractData(slideMeDirectory, slideMeDirs[2])
#extractData(slideMeDirectory, slideMeDirs[3])
#extractData(slideMeDirectory, slideMeDirs[4])
