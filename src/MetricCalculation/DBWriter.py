'''
Created on Feb 12, 2014

@author: ess0006
'''
import MySQLdb as mdb
import sys

class DBWriter(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def connect(self):
        host, username, password, db = readFile(self, 'C:\\apks\\db\\metricdb.txt')
        return mdb.connect(host, username, password, db);

    def readFile(self, filePath):
        lines = tuple(open(filePath, 'r'))
        return lines[0].replace("\n", ""), lines[1].replace("\n", ""), lines[2].replace("\n", ""), lines[3].replace("\n", "")
    
    def writeError(self,message):
        f = open("DB_write_error_log.txt", 'a')
        f.write(message+"\n")
        f.close()
    
    def executeDBCommand(self, command):
        try:
            with self.con:
                cur = self.con.cursor()
                cur.execute(command)
        except mdb.Error, e:
            self.writeError(command + "Resulted in Error %d: %s" % (e.args[0],e.args[1]))
        except:
            self.writeError ("!!!!! Unexpected error:" + str(sys.exc_info()[0]) + " When Executing Command "+command)
        
        
    def writeAppTable(self, filename, appLabel, appFQName, market):
        command = "INSERT INTO Apps VALUES(\"" + filename + "\",\"" + appLabel + "\",\"" + appFQName + "\",\" " + market +"\")"
        self.executeDBCommand(command);
        
    def writeSizeMetricsTable(self, filename, numByteCodeInstructions, numMethods, 
                              numClasses, methodsPerClass, ipm, cyclomatic, wmc):
        command = "INSERT INTO SizeMetrics VALUES(\"" + filename + "\"," + str(numByteCodeInstructions)
        command = command + "," + str(numMethods) + "," + str(numClasses) + "," + str(methodsPerClass)
        command = command + "," + str(ipm) + "," + str(cyclomatic) + "," + str(wmc) +")"
        self.executeDBCommand(command);
        
    def writeOOMetricsTable(self, filename, noc, dit, lcom, cbo, ppiv, apd):
        command = "INSERT INTO OOMetrics VALUES(\"" + filename + "\"," + str(noc) 
        command = command + "," + str(dit) + "," + str(lcom) + "," + str(cbo) + "," + str(ppiv)
        command = command + "," + str(apd) + ")"
        self.executeDBCommand(command);
        
    def writeMVCMetricsTable(self, filename, mvc):
        command = "INSERT INTO MVCMetrics VALUES(\"" + filename + "\"," + str(mvc) + ")"
        self.executeDBCommand(command);
        
    def writeRatingsTable(self, filename, rating, numRatings, numDownloads):
        command = "INSERT INTO Ratings VALUES(\"" + filename + "\"," + str(rating) + "," + str(numRatings) + "," + str(numDownloads) + ")"
        self.executeDBCommand(command);