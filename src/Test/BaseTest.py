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
import src.MetricCalculation.UncheckedBundles as UncheckedBundles
import src.MetricCalculation.BadSmellMethodCalls as BadSmellMethodCalls
import src.MetricCalculation.ANRMetrics as ANRMetrics
import src.MetricCalculation.BatteryMetrics as BatteryMetrics
import src.MetricCalculation.IntentLaunchMetrics as IntentLaunchMetrics

class Test(unittest.TestCase):


    def setUp(self):
        self.decFolderPath =  'C:\\apks\\EmployeeListApp_dec'
        self.sourceCodePaths = []
        self.layoutFilePaths = []
        
            
        #get path for each source code file that we will consider - EmployeeListApp
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
                
                
        self.decFolderPath2 =  'C:\\apks\\TestApp1_dec'
        self.sourceCodePaths2 = []
        self.layoutFilePaths2 = []
            
        #get path for each source code file that we will consider - TestApp1
        smaliPath2 = self.decFolderPath2 + '\\smali'
        packageName2 = "com.example.testapp1"
        dirPaths2 = MCD.getSourceCodeDirectoryPaths(smaliPath2, packageName2)
        #navigate using fully qualified packageName
        for codeDir in dirPaths2:
            for root, dirs, files in os.walk(codeDir):
                for file in files:
                    if file not in MCD.ignoreFiles:
                        self.sourceCodePaths2.append(os.path.join(root, file))
        
        layoutPath2 = self.decFolderPath2 + '\\res\\layout'
        for root, dirs, files in os.walk(layoutPath):
            for file in files:
                self.layoutFilePaths2.append(os.path.join(root, file))


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
        
    def test04_UncheckedBundles(self):
        ub = UncheckedBundles.UncheckedBundles(self.sourceCodePaths2, self.layoutFilePaths2)
        ub.extractData()
        
        self.assertEqual(ub.getNumUncheckedBundles(),0)
        self.assertEqual(ub.getNumCheckedBundles(),1)
    
    def test05_BadSmellMethodCalls(self):
        bsm = BadSmellMethodCalls.BadSmellMethodCalls(self.sourceCodePaths2, self.layoutFilePaths2)
        bsm.extractData()
        
        self.assertEqual(bsm.getNumShowCalls(),1)
        self.assertEqual(bsm.getNumDismissCalls(),1)
        self.assertEqual(bsm.getNumSetContentViewCalls(),1)
        self.assertEqual(bsm.getNumCreateScaledBitmapCalls(),0)
        self.assertEqual(bsm.getNumOnKeyDownCalls(),0)
        self.assertEqual(bsm.getNumIsPlayingCalls(),0)
        self.assertEqual(bsm.getNumUnregisterRecieverCalls(),0)
        self.assertEqual(bsm.getNumOnBackPressedCalls(),0)
        self.assertEqual(bsm.getNumShowDialogCalls(),0)
        self.assertEqual(bsm.getNumCreateCalls(),2)
        
    def test06_ANRMetrics(self):
        anr = ANRMetrics.ANRMetrics(self.sourceCodePaths2, self.layoutFilePaths2)
        anr.extractData()

        self.assertEqual(anr.getNumNetworkOnMainThread(),2)
        self.assertEqual(anr.getNumSQLLiteOnMainThread(),1)
        self.assertEqual(anr.getNumFileIOOnMainThread(),1)
        self.assertEqual(anr.getNumBitmapOnMainThread(),1)
        self.assertEqual(anr.getNumNetworkOnBgThread(),0)
        self.assertEqual(anr.getNumSQLLiteOnBgThread(),0)
        self.assertEqual(anr.getNumFileIOOnBgThread(),0)
        self.assertEqual(anr.getNumBitmapOnBgThread(),0)
        
    def test06_BatteryMetrics(self):
        bat = BatteryMetrics.BatteryMetrics(self.sourceCodePaths2, self.layoutFilePaths2)
        bat.extractData()
        
        self.assertEqual(bat.getNumNoTimeoutWakeLocks(),0)
        self.assertEqual(bat.getNumLocationListeners(),1)
        self.assertEqual(bat.getNumGpsUses(),1)
        self.assertEqual(bat.getNumDomParsers(),1)
        self.assertEqual(bat.getNumSaxParsers(),1)
        self.assertEqual(bat.getNumXMLPullParsers(),1)
        
    def test06_IntentLaunchMetrics(self):
        ilm = IntentLaunchMetrics.IntentLaunchMetrics(self.sourceCodePaths2, self.layoutFilePaths2, "com.example.testapp1")
        ilm.extractData()
        
        self.assertEqual(ilm.getNumStartActivities(),1)
        self.assertEqual(ilm.getNumStartActivity(),1)
        self.assertEqual(ilm.getNumStartInstrumentation(),1)
        self.assertEqual(ilm.getNumStartIntentSender(),1)
        self.assertEqual(ilm.getNumStartService(),1)
        self.assertEqual(ilm.getNumStartActionMode(),1)
        self.assertEqual(ilm.getNumStartActivityForResult(),1)
        self.assertEqual(ilm.getNumStartActivityFromChild(),1)
        self.assertEqual(ilm.getNumStartActivityFromFragment(),1)
        self.assertEqual(ilm.getNumStartActivityIfNeeded(),1)
        self.assertEqual(ilm.getNumStartIntentSenderForResult(),1)
        self.assertEqual(ilm.getNumStartIntentSenderFromChild(),1)
        self.assertEqual(ilm.getNumStartNextMatchingActivity(),1)
        self.assertEqual(ilm.getNumStartSearch(),1)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()