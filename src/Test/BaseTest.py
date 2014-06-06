'''
A baseline test used for regression testing.  Based on the
EmployeeListApp application.
Created on Feb 3, 2014

@author: ess0006
'''
import unittest
import os
import src.MetricCalculation.MetricCalculationDriver as MCD
import src.MetricCalculation.SizeMetrics as SizeMetrics
import src.MetricCalculation.CKMetrics as CKMetrics
import src.MetricCalculation.MVCMetrics as MVCMetrics

class Test(unittest.TestCase):


    def setUp(self):
        self.decFolderPath =  'C:\\apks\\EmployeeListApp_dec'
        self.sourceCodePaths = []
        self.layoutFilePaths = []
        
            
        #get path for each source code file that we will consider
        smaliPath = self.decFolderPath + '\\smali'
        packageName = "com.example.employeelistapp"
        dirPaths = MCD.getSourceCodeDirectoryPaths(smaliPath, packageName)
        #navigate using fully qualified packageName
        for codeDir in dirPaths:
            for root, dirs, files in os.walk(codeDir):
                for file in files:
                    if file not in MCD.ignoreFiles:
                        self.sourceCodePaths.append(os.path.join(root, file))
        
        layoutPath = self.decFolderPath + '\\res\\layout'
        for root, dirs, files in os.walk(layoutPath):
            for file in files:
                self.layoutFilePaths.append(os.path.join(root, file))


    def tearDown(self):
        pass


    def test01_SizeMetrics(self):
        sm = SizeMetrics.SizeMetrics(self.sourceCodePaths)
        sm.extractData()
        
        self.assertEqual(sm.getNumFiles(), 5)
        self.assertEqual(sm.getNumClasses(), 5)
        self.assertEqual(sm.getNumMethods(), 25)
        self.assertEqual(sm.getNumInstructions(), 207)
        self.assertEqual(sm.getMethodsPerClass(), 5.0)
        self.assertEqual(sm.getInstructionsPerMethod(), 8.28)
        self.assertEqual(sm.getCyclomatic(), 1.2)
        self.assertEqual(sm.getWMC(), 5.2, .001)
        
    def test02_OOMetrics(self):
        ck = CKMetrics.CKMetrics(self.sourceCodePaths, "com.example.employeelistapp")
        ck.extractData()
        
        self.assertEqual(ck.getNOC(), 2)
        self.assertEqual(ck.getDIT(), 2)
        self.assertAlmostEqual(ck.getLCOM(), 36.11, 2)#rounded to two decimal places when done by hand
        self.assertEqual(ck.getCBO(), .2)  
        self.assertEqual(ck.getPPIV(), 100.0)
        self.assertEqual(ck.getAPD(), 3.8)
        
    def test03_MVCMetrics(self):
        mvc = MVCMetrics.MVCMetrics(self.sourceCodePaths, self.layoutFilePaths)
        mvc.extractData()
        
        self.assertEqual(mvc.getNumViewsInController(), 1)
        self.assertEqual(mvc.getNumViewsNotInController(), 2)
        self.assertAlmostEqual(mvc.getSepVCScore(), 66.667, 2)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()