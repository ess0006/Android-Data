'''
This class represents a java method.
Created on Jan 24, 2014

@author: Eric Shaw
'''

class Method(object):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.fieldsUsed = []
        
    def addFieldUsed(self, field):
        if field not in self.fieldsUsed:
            self.fieldsUsed.append(field)
        
    def getFieldsUsed(self):
        return self.fieldsUsed
    
    def setName(self, name):
        self.name = name
        
    def getName(self):    
        return self.name