'''
Created on May 8, 2014

@author: ess0006
'''
import MySQLdb as mdb
import sys

markets = ["appsapk", "fdroid", "slideme"]

if __name__ == '__main__':
    pass

def getExternalLibraries():
    return executeDBCommand("SELECT DISTINCT * FROM ess0006_android_dem_db.libraries limit 0, 50000;")

def connect():
    host, username, password, db = readFile('C:\\apks\\db\\dem_db.txt')
    return mdb.connect(host, username, password, db);

def readFile(filePath):
    lines = tuple(open(filePath, 'r'))
    return lines[0].replace("\n", ""), lines[1].replace("\n", ""), lines[2].replace("\n", ""), lines[3].replace("\n", "")

def executeDBCommand(command):
    con = connect()
    try:
        with con:
            cur = con.cursor()
            cur.execute(command)
            value = cur.fetchall()
            return value
    except mdb.Error, e:
        writeError(command + "Resulted in Error %d: %s" % (e.args[0],e.args[1]))
    except:
        writeError ("!!!!! Unexpected error:" + str(sys.exc_info()[0]) + " When Executing Command "+command)
    finally:
        if con:
            con.close()

def writeError(message):
    f = open("Data_Mining_log.txt", 'a')
    f.write(message+"\n")
    f.close()
    
cursor = getExternalLibraries()
print cursor[0]
print cursor[0][0]
print cursor[0][1]

dict = {}

for entry in cursor:
    if(entry[1] in dict):
        dict[entry[1]] = dict[entry[1]] + 1
    else:
        dict[entry[1]] = 1
        
total = len(cursor) - 13 #lazy way to handle the blank lirbraries - should fix later
for key in dict:
    print key + ": " + str(dict[key]) + ", " + str((dict[key]/float(total))*100) + "%"