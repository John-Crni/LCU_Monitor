import ACUmonitorGUI
import ACUbackend
import threading
import time
#from multiprocessing import Process
#import asyncio

ACUMONITOR=None

class Start():
    def __init__(self):
        print("SATRT!")
        global ACUMONITOR
        ACU=ACU_Monitor()
        ACUMONITOR=ACU
        BackEnd=ACUbackend.ACUBackEnd()
        ACU.BackEnd=BackEnd
        StartGUI=ACUmonitorGUI.StartGUI()
        FrontEnd=StartGUI.getGUI()
        ACU.FrontEnd=FrontEnd
        ACU.BackEnd.ACU_Monitor=ACU
        ACU.FrontEnd.ACU_Monitor=ACU
        print(ACU.FrontEnd.NAME)
        #roop=ACUbackend.InputRoopClass(acu=ACU,sleepT=0.05)
        #ACU.setUpAsync2List(As=roop)
        #"ACU.setUpAsync2List(As=ACUbackend.AnntenaController(acu=ACU,sleepT=0.1,deviceName="USB Serial Port",deviceType="ACU",inputter=roop))#InputRoopClass
        #ACU.setUpAsync2List(As=ACUbackend.moveTEST(acu=ACU,sleepT=0.1))
        #ACU.setUpAsync2List(As=ACUbackend.GPSManager(acu=ACU,sleepT=0.1,deviceName="Prolific",deviceType="GPS"))
        #ACU.setUpAsync2List(As=ACUbackend.setTime(acu=ACU,sleepT=0.25))
        #ACU.setUpAsync2List(As=ACUbackend.comMonitor(acu=ACU,sleepT=0.5))
        StartGUI.ApperGUI()
        StartGUI.LoopGui()

class ACU_Monitor():
    BackEnd=None
    FrontEnd=None
    execteAsyncClass=None
    def __init__(self):
        print("INIT!")
    def getBackEnd(self):
        return self.BackEnd
    def getFrontEnd(self):
        return self.FrontEnd
    def setUpAsync2List(self,As=None):
        self.FrontEnd.setupAsync2List(As)

app=Start()
