import MySQLdb

'''
Created on Mar 15, 2014

@author: Eric
'''

if __name__ == '__main__':
    pass

db = MySQLdb.connect(host="acadmysql.duc.auburn.edu", port=3306, user="ess0006", passwd="esdb@dmin", db = "ess0006_thesis_db")
cursor = db.cursor()

cursor.execute("SELECT filename, mvc FROM MVCMetrics limit 0, 20000;")
filenames = cursor.fetchall()

for list in filenames:
    filename = list[0]
    mvc = list[1]#already have mvc metric score
    
    #get size metrics
    sizeQuery = 'SELECT * FROM SizeMetrics WHERE filename = \''+filename.replace('\'','\'\'')+'\' limit 0, 20000;'
    cursor.execute(sizeQuery)
    result = cursor.fetchall()
    
    mpc = result[0][4]
    ipm = result[0][5]
    cyclomatic = result[0][6]
    wmc = result[0][7]
    
    #get OO metrics
    ooQuery = 'SELECT * FROM OOMetrics WHERE filename = \''+filename.replace('\'','\'\'')+'\' limit 0, 20000;'
    cursor.execute(ooQuery)
    result = cursor.fetchall()
    
    noc = result[0][1]
    dit = result[0][2]
    lcom = result[0][3]
    cbo = result[0][4]
    ppiv = result[0][5]
    apd = result[0][6]
    
    #calcualate the new rating
    score = 0.0
    mpcScore = 0.0
    ipmScore = 0.0
    cyclomaticScore = 0.0
    wmcScore = 0.0
    nocScore = 0.0
    ditScore = 0.0
    lcomScore = 0.0
    cboScore = 0.0
    ppivScore = 0.0
    apdScore = 0.0
    mvcScore = 0.0
    
    if(mpc < 10):
        mpcScore = 5
    elif (mpc < 15):
        mpcScore = 4
    elif (mpc < 18):
        mpcScore = 3
    elif (mpc < 20):
        mpcScore = 2
    elif (mpc < 22):
        mpcScore = 1
    
    if(ipm < 10):
        ipmScore = 5
    elif (ipm < 20):
        ipmScore = 4
    elif (ipm < 30):
        ipmScore = 3
    elif (ipm < 40):
        ipmScore = 2
    elif (ipm < 100):
        ipmScore = 1
        
    if(cyclomatic < 3):
        cyclomaticScore = 5
    elif (cyclomatic < 5):
        cyclomaticScore = 4
    elif (cyclomatic < 7):
        cyclomaticScore = 3
    elif (cyclomatic < 9):
        cyclomaticScore = 2
    elif (cyclomatic < 10):
        cyclomaticScore = 1
        
    if(wmc < 3):
        wmcScore = 5
    elif (wmc < 5):
        wmcScore = 4
    elif (wmc < 7):
        wmcScore = 3
    elif (wmc < 9):
        wmcScore = 2
    elif (wmc < 10):
        wmcScore = 1
        
    if(noc < 2):
        nocScore = 5
    elif (noc < 3):
        nocScore = 4
    elif (noc < 5):
        nocScore = 3
    elif (noc < 7):
        nocScore = 2
    elif (noc < 10):
        nocScore = 1
        
    if(dit == 1):
        ditScore = 5
    elif (dit == 2):
        ditScore = 4
    elif (dit == 3):
        ditScore = 3
    elif (dit == 4):
        ditScore = 2
    elif (dit == 5):
        ditScore = 1
    
    lcomScore = float(lcom) / 20
    
    #TODO: CBO scores
    if(cbo < 3):
        cboScore = 5
    elif (cbo < 4):
        cboScore = 4
    elif (cbo < 4.5):
        cboScore = 3
    elif (cbo < 5):
        cboScore = 2
    elif (cbo < 10):
        cboScore = 1
    
    ppivScore += float(ppiv) / 20
    
    if(apd == 0):
        apdScore = 5
    elif (apd == 1):
        apdScore = 4
    elif (apd == 2):
        apdScore = 3
    elif (apd == 3):
        apdScore = 2
    elif (apd == 4):
        apdScore = 1
        
    mvcScore = float(mvc) / 20
    
    score = (mvcScore + mpcScore + ipmScore +cyclomaticScore + wmcScore + nocScore + ditScore + lcomScore + cboScore + ppivScore + apdScore) / 11.0
    
    query = 'INSERT into MetricScores values (\''+filename.replace('\'','\'\'')+'\', ' + str(score) + ', ' + str(mvcScore) + ', ' + str(mpcScore) + ', ' + str(ipmScore) + ', ' + str(cyclomaticScore)+ ', ' + str(wmcScore)+ ', ' + str(nocScore)+ ', ' + str(ditScore)+ ', ' + str(lcomScore) + ', ' + str(cboScore) + ', ' + str(ppivScore) + ', ' + str(apdScore) +')'
    cursor.execute(query)
    
db.close()
print "finished"