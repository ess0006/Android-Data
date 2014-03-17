import MySQLdb

'''
Created on Mar 15, 2014

@author: Eric
'''

if __name__ == '__main__':
    pass

db = MySQLdb.connect()
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
    
    if(mpc < 10):
        score += 5
    elif (mpc < 15):
        score += 4
    elif (mpc < 18):
        score += 3
    elif (mpc < 20):
        score += 2
    elif (mpc < 22):
        score += 1
    
    if(ipm < 10):
        score += 5
    elif (ipm < 20):
        score += 4
    elif (ipm < 30):
        score += 3
    elif (ipm < 40):
        score += 2
    elif (ipm < 100):
        score += 1
        
    if(cyclomatic < 3):
        score += 5
    elif (cyclomatic < 5):
        score += 4
    elif (cyclomatic < 7):
        score += 3
    elif (cyclomatic < 9):
        score += 2
    elif (cyclomatic < 10):
        score += 1
        
    if(wmc < 3):
        score += 5
    elif (wmc < 5):
        score += 4
    elif (wmc < 7):
        score += 3
    elif (wmc < 9):
        score += 2
    elif (wmc < 10):
        score += 1
        
    if(noc < 2):
        score += 5
    elif (noc < 3):
        score += 4
    elif (noc < 5):
        score += 3
    elif (noc < 7):
        score += 2
    elif (noc < 10):
        score += 1
        
    if(dit == 1):
        score += 5
    elif (dit == 2):
        score += 4
    elif (dit == 3):
        score += 3
    elif (dit == 4):
        score += 2
    elif (dit == 5):
        score += 1
    
    score += float(lcom) / 20
    
    score += float(ppiv) / 20
    
    if(apd == 0):
        score += 5
    elif (apd == 1):
        score += 4
    elif (apd == 2):
        score += 3
    elif (apd == 3):
        score += 2
    elif (apd == 4):
        score += 1
        
    score += float(mvc) / 20
    
    score = score / 10
    
    query = 'INSERT into MetricScores values (\''+filename.replace('\'','\'\'')+'\', ' + str(score) +')'
    cursor.execute(query)
    
db.close()
print "finished"