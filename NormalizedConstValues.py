from enum import Enum

class ACUControlMode(Enum):
    Slave=1
    Indiv=2
    
class StowMode(Enum):
    Pos=1
    Lock=2
    Release=3
    NONE=4

class SelialValues(Enum):
    none="none"
    enable="enable"
    conected="conected"
    disconected="disconected"
    notconect="notconect"
    unkowm="unkowm"
    
class StarNames(Enum):
    sun="sun"
    mercury="mercury"
    venus="venus"
    mars="mars"
    
class ButtonMode(Enum):
    Normal=1
    Radio=2
    
class ButtonChangeStats(Enum):
    OnlyColor=1
    ChangeAll=2
    
class Coordinate(Enum):
    B1950=1
    J2000=2
    GAL=3
    StarName=4
    
class CommandMode(Enum):
    UpdateAxis=1
    ReadAxis=2

class AxisMode(Enum):
    Prog=3
    Manu=3.5
    ManuSet=4
    ManuStop=5
    Stby=6


    