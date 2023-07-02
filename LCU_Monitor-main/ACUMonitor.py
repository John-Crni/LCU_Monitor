import ACUmonitorGUI
import ACUbackend
import threading
import time
from multiprocessing import Process
import asyncio

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
        ACU.setUpAsync2List(As=ACUbackend.comMonitor(acu=ACU))
        StartGUI.ApperGUI()
        StartGUI.LoopGui()

class ACU_Monitor():
    BackEnd=None
    FrontEnd=None
    def __init__(self):
        print("INIT!")
    def getBackEnd(self):
        return self.BackEnd
    def getFrontEnd(self):
        return self.FrontEnd
    def setUpAsync2List(self,As=None):
        self.FrontEnd.setupAsync2List(As)

app=Start()



    