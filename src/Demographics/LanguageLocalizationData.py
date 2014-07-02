'''
Created on May 14, 2014

@author: ess0006
'''
import MySQLdb as mdb
import sys

if __name__ == '__main__':
    pass

def connect():
    host, username, password, db = readFile('C:\\apks\\db\\dem_db.txt')
    return mdb.connect(host, username, password, db);

def readFile(filePath):
    lines = tuple(open(filePath, 'r'))
    return lines[0].replace("\n", ""), lines[1].replace("\n", ""), lines[2].replace("\n", ""), lines[3].replace("\n", "")

def executeDBCommand(command, one):
    con = connect()
    try:
        with con:
            cur = con.cursor()
            cur.execute(command)
            if one:
                value = cur.fetchone()
                return value[0]
            else:
                value = cur.fetchall()
                return value
    except:
        print "error"
    finally:
        if con:
            con.close()
            
locData = executeDBCommand("SELECT distinct locData FROM ess0006_android_dem_db.language_loc_data",False)

totalWithLoc = int(executeDBCommand("SELECT count(distinct filename) FROM ess0006_android_dem_db.language_loc_data;",True))
totalApps = int(executeDBCommand("SELECT count(distinct filename) FROM ess0006_android_dem_db.master;",True))

f = open('languagelocalizations2.csv','a')
f.write('localization,# of all apps,# of apps with localizations\n')

for loc in locData:
    print loc[0]
    curCount = int(executeDBCommand("SELECT count(distinct filename) FROM ess0006_android_dem_db.language_loc_data WHERE locData = \'" + loc[0] + "\';",True))
    percent = float(float(curCount)/float(totalApps) * 100)
    if percent >= 5:
        f.write(loc[0] + "," + str(percent) + "," + str(float(float(curCount)/float(totalWithLoc) * 100)) + "\n")
f.close()