
'''
DBWriter
Created on Mar 29, 2012

@author: Billy Symon
'''
import MySQLdb as mdb
import sys

def connect():
    host, username, password, db = readFile('C:\\apks\\db\\dem_db.txt')
    return mdb.connect(host, username, password, db);

def readFile(filePath):
    lines = tuple(open(filePath, 'r'))
    return lines[0].replace("\n", ""), lines[1].replace("\n", ""), lines[2].replace("\n", ""), lines[3].replace("\n", "")
    
def writeError(message):
    f = open("DB_write_error_log.txt", 'a')
    f.write(message+"\n")
    f.close()

def executeDBCommand(command):
    con = connect()
    try:
        with con:
            cur = con.cursor()
            cur.execute(command)
    except mdb.Error, e:
        writeError(command + "Resulted in Error %d: %s" % (e.args[0],e.args[1]))
    except:
        writeError ("!!!!! Unexpected error:" + str(sys.exc_info()[0]) + " When Executing Command "+command)
    finally:
        if con:
            con.close()
            
def writeAppInfoTableEnrty(fileName, market, fileSize, appLabel, appFQName):

    command = "INSERT INTO appinfo VALUES(\""+fileName+"\",\" "+market+"\", \""+str(fileSize)+"\", \""+ appLabel+"\", \""+appFQName+"\")"
    executeDBCommand(command);

def writePermissionsInfoTableEnrty(fileName, numPermissionsUsed, numPermissionsSetUp, numPremissionsRequired):
    command = "INSERT INTO permissionsinfo VALUES(\""+fileName+"\",\" "+str(numPermissionsUsed)+"\", \""+str(numPermissionsSetUp)+"\",\""+str(numPremissionsRequired)+"\")"
    executeDBCommand(command);

def writePermissionsRequestedTableEnrty(fileName, permissionsUsed):
    for permission in permissionsUsed:
        command = "INSERT INTO permissions_requested VALUES(\""+fileName+"\",\" "+permission+"\")"
        executeDBCommand(command);

def writePermissionsSetUpTableEnrty(fileName, permissionsSetUp):
    for permission in permissionsSetUp:
        command = "INSERT INTO permissions_setup VALUES(\""+fileName+"\",\" "+permission+"\")"
        executeDBCommand(command);

def writePermissionsRequiredTableEnrty(fileName, permissionsRequired):
    for permission in permissionsRequired:
        command = "INSERT INTO permissions_required VALUES(\""+fileName+"\",\" "+permission+"\")"
        executeDBCommand(command);

def writeIntentsTableEnrty(fileName, numActivities, numServices, numReceivers, numProviders):
    command = "INSERT INTO intents VALUES(\""+fileName+"\",\" "+str(numActivities)+"\", \""+str(numServices)+"\", \""+str(numReceivers)+"\", \""+str(numProviders)+"\")"
    executeDBCommand(command);

def writeActivitiesTableEnrty(fileName, activities):
    for activity in activities:
        command = "INSERT INTO activities VALUES(\""+fileName+"\",\" "+activity+"\")"
        executeDBCommand(command);

def writeServicesTableEnrty(fileName, services):
    for service in services:
        command = "INSERT INTO services VALUES(\""+fileName+"\",\" "+service+"\")"
        executeDBCommand(command);
        
def writeReceiversTableEnrty(fileName, receivers):
    for receiver in receivers:
        command = "INSERT INTO receivers VALUES(\""+fileName+"\",\" "+receiver+"\")"
        executeDBCommand(command);

def writeProvidersTableEnrty(fileName, providers):
    for provider in providers:
        command = "INSERT INTO providers VALUES(\""+fileName+"\",\" "+provider+"\")"
        executeDBCommand(command);
        
def writeAditionalInfoTableEnrty(fileName, numLibraries, numLayouts, numStrings, minSDKLevel, altLayouts, altStrings):
    command = "INSERT INTO additional_info VALUES(\""+fileName+"\",\" "+str(numLibraries)+"\", \""+str(numLayouts)+"\", \""+str(numStrings)+"\", \""+minSDKLevel+"\", \""+altLayouts+"\", \""+altStrings+"\")"
    executeDBCommand(command);

def writeLibrariesTableEnrty(fileName, libraries):
    for library in libraries:
        command = "INSERT INTO libraries VALUES(\""+fileName+"\",\" "+library+"\")"
        executeDBCommand(command);

def writeMasterEntry(fileName, market, fileSize, appLabel, appFQName, numPermissionsUsed, numPermissionsSetUp, numPremissionsRequired, numActivities, numServices, numReceivers, numProviders, numLibraries, numLayouts, numStrings, minSDKLevel, altLayouts, altStrings):
        command = "INSERT INTO master VALUES(\""+fileName+"\",\" "+market+"\", \""+str(fileSize)+"\", \""+ appLabel+"\", \""+appFQName+"\",\" "+str(numPermissionsUsed)+"\", \""+str(numPermissionsSetUp)+"\",\""+str(numPremissionsRequired)+"\",\" "+str(numActivities)+"\", \""+str(numServices)+"\", \""+str(numReceivers)+"\", \""+str(numProviders)+"\",\" "+str(numLibraries)+"\", \""+str(numLayouts)+"\", \""+str(numStrings)+"\", \""+minSDKLevel+"\", \""+altLayouts+"\", \""+altStrings+"\")"
        executeDBCommand(command);
        
def writeLanguageLocDataEntry(fileName, locData):
    command = "INSERT INTO language_loc_data VALUES(\""+fileName+"\",\" "+locData+"\")"
    executeDBCommand(command);
    
def writeLayoutLocDataEntry(fileName, locData):
    command = "INSERT INTO layout_loc_data VALUES(\""+fileName+"\",\" "+locData+"\")"
    executeDBCommand(command);

def writeDrawableLocDataEntry(fileName, locData):
    command = "INSERT INTO drawable_loc_data VALUES(\""+fileName+"\",\" "+locData+"\")"
    executeDBCommand(command);
