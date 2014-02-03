'''
Created on Jan 31, 2012

@author: Billy Symon
'''
import os
import os.path

count = 0
for root, dirs, files in os.walk("C:\\apks\\downloaded\\slideme"):
    for file in files:
        print "********************************************"
        os.system("apktool -v d -f \""+os.path.join(root, file)+"\" \"C:\\apks\\decompiled\\slideme\\"+file[0:-4]+"\"")
        count += 1
        print "********************************************"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "           "+str(count)+" files decompiled"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
