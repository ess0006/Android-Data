'''
Created on Jan 27, 2014

@author: ess0006
'''
import fileinput

if __name__ == '__main__':
    pass
numInstr = 0
path = "C:\\Users\\ess0006\\Documents\\androidviews.txt"

lines = tuple(open('C:\\apks\\db\\dem_db.txt', 'r'))
for line in lines:
    print line
#for line in fileinput.input([path]):
    #line = line.replace("\n","")
    #print line + "\"," 