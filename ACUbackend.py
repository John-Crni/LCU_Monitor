import sys
import glob
import serial
import threading
import time
import struct
import asyncio
import getTime as MyTime
import pynmea2
from serial.tools import list_ports
from datetime import datetime,timedelta
import datetime as DATE_TIME
from pytz import timezone
import dateutil
import dateutil.parser
from dateutil import tz
import astropy as ASTRO
import astropy.coordinates
from astropy.units import deg
from astropy.units import m
from skyfield.api import Topos, load, EarthSatellite,position_of_radec,wgs84,Star
import pynmea2
import ephem
import unicodedata
from NormalizedConstValues import CommandMode,AxisMode,StowMode,ACUControlMode,Coordinate
import copy

class RadDiffCalc():
    Coord1=None
    Coord2=None
    Coord3=None
    Coord4=None

    def __init__(self):
        self.Coord1=radfunc(coord=1)
        self.Coord2=radfunc(coord=2)
        self.Coord3=radfunc(coord=3)
        self.Coord4=radfunc(coord=4)
        self.Coord1.AfterInit(LeftCoord=self.Coord2,rightCoord=self.Coord4)
        self.Coord2.AfterInit(LeftCoord=self.Coord3,rightCoord=self.Coord1)
        self.Coord3.AfterInit(LeftCoord=self.Coord4,rightCoord=self.Coord2)
        self.Coord4.AfterInit(LeftCoord=self.Coord1,rightCoord=self.Coord3)

    def CalcDiff(self,Start=0,Goal=0):
        coord=self.Coord1.Getrad2Coord(rad=Start)
        if coord is self.Coord1.coord:
            return self.Coord1.getRadFactor(start_rad=Start,goal_rad=Goal)
        if coord is self.Coord2.coord:
            return self.Coord2.getRadFactor(start_rad=Start,goal_rad=Goal)
        if coord is self.Coord3.coord:
            return self.Coord3.getRadFactor(start_rad=Start,goal_rad=Goal)
        if coord is self.Coord4.coord:
            return self.Coord4.getRadFactor(start_rad=Start,goal_rad=Goal)

class radfunc():
    coord=0
    left=None
    right=None
    myRad=0
    goal=0
    myMax=0
    MyMin=0

    def Getrad2Coord(self,rad=0):
        if rad>=0 and rad<90:
            return 1
        if rad>=90 and rad<180:
            return 2
        if rad>=180 and rad<270:
            return 3
        if rad>=270 and rad<=360:
            return 4

    def MyFunc(self):
        return self.goal-self.myRad
    
    def leftFunc(self):
        re=0
        if self.coord==4:
            re= (self.goal+360)-self.myRad
        else:
            re=self.goal-self.myRad
        return re
    
    def rightFunc(self):
        re=0
        if self.coord==1:
            re= self.goal+(self.myRad-360)
        else:
            re=self.goal-self.myRad
        return re

    def otherFunc(self):
        leftdiff=self.myMax-self.myRad+90+self.goal-self.left.myMax
        rightdiff=self.MyMin-self.myRad-90-self.goal-self.right.myMax
        rightdiff*=-1
        if leftdiff<rightdiff:
            return leftdiff
        else:
            return rightdiff*-1

    def getRadFactor(self,start_rad=0,goal_rad=0):
        self.myRad=start_rad
        self.goal=goal_rad
        Coord=self.Getrad2Coord(rad=goal_rad)
        if Coord is self.left.coord:
            return self.leftFunc()
        elif Coord is self.right.coord:
            return self.rightFunc()
        elif Coord is self.coord:
            return self.MyFunc()
        else:
            return self.otherFunc()
            
    def AfterInit(self,LeftCoord=None,rightCoord=None):
        self.left=LeftCoord
        self.right=rightCoord
    
    def __init__(self,coord=0):
        self.coord=coord
        if self.coord==1:
            self.myMax=90
            self.MyMin=0
        if self.coord==2:
            self.myMax=180
            self.MyMin=90
        if self.coord==3:
            self.myMax=270
            self.MyMin=180
        if self.coord==4:
            self.myMax=360
            self.MyMin=270

class ACUBackEnd():
    
    ACU_Monitor=None
    
    ASYNC_TEST=None
    
    SelectedCOM="none"

    SELECTED_COM_STATS="none"

    def getCOM_STATS(self):
        re="unkowm"
        if self.SelectedCOM=="none" and self.SELECTED_COM_STATS=="none":
            re="notconect"
        if self.SelectedCOM!="none" and self.SELECTED_COM_STATS=="conected":
            re="conected"
        if self.SelectedCOM!="none" and (self.SELECTED_COM_STATS=="none" or self.SELECTED_COM_STATS=="disconected"):
            re="disconected"
        return re

    def __init__(self):
        print("ACUBackEnd_ISBEGUN!")
        
    def selected(self):
        print("SELECTED!")
    
    def getSerialPorts(self):
        """ Lists serial port names
 
            :raises EnvironmentError:
            On unsupported or unknown platforms
            :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
 
        result = ["TEST"]
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def outPut(self):#0.2秒おきにACUへ信号を出力しています (なぜ0.2秒ごとの理由は特にありません)
        while True:
            code="@0BAU W9600<cr><lf>"#ACUをセットアップするためのコマンドです
            ASCII=code.encode('ascii')#上記のコマンドをアスキーに変換しています pythonではByte型にこの時点でなっています
            ser.write(ASCII) #アスキーに変換したコマンドを送信しています
            time.sleep(0.2)
    
    def inPut(self):#0.1秒おきに信号を受信しています (なぜ0.1秒ごとの理由は特にありません)
        while end: 
            time.sleep(0.1)
            line=ser.read_all()
            s=str(line)
            data.write("\n")
            data.write(s)
            
    async def TEST(self):
        ser=Serialcommunicator()
        
    
    def comTest(self,PORT="COM1"):
        re=False
        try:
            ser = serial.Serial(port=PORT, baudrate=9600, timeout=0.5,bytesize=serial.EIGHTBITS,stopbits = serial.STOPBITS_ONE,parity=serial.PARITY_NONE)
            commands = [ 0xB6, 0x01, 0x02, 0x00 ]
            for cmd in commands:
                data = struct.pack("B", cmd)
                print("tx: ", data)
                ser.write(data)
            ser.flush()
            rx = ser.readline()
            print("rx: ", rx)
            ser.close()
            re=True
        except(OSError, serial.SerialException):
            print("SerialError!")
            pass
        return re


    def main(self):#ここでは、上記の(OutPut,input関数)をスレッドリングを利用して、並列処理させています
        outPut_func = threading.Thread(target=outPut)
        inPut_func = threading.Thread(target=inPut)
        outPut_func.start()
        inPut_func.start()
        time.sleep(60) #一分間 ACUと通信を行うためのタイマーです
        ser.close #シリアル通信をやめています
        end=False #Input関数の無限ループを終わらせています
        time.sleep(1)
        data.close()#txtファイルへの出力を終了させています
        print("END")
        
class AsyncedClass():
    ACUmonitor=None
    isACUenable=False
    sleepTime=0.1
    message="None"
    def __init__(self,ACU=None):
        self.ACUmonitor=ACU
        if self.ACUmonitor is not None:
            self.isACUenable=True
            print(self.__class__.__name__+"AsyncedClasss OK!")
    def sleep(self):
        if self.sleepTime>0:
            time.sleep(float(self.sleepTime))

class Serialcommunicator():
    Serial=None
    RoopBackCom= [ 0xB6, 0x01, 0x02, 0x00 ]
    RoopBackExpected=b'\xb6\x01\x02\x00'
    isRoopBackOk=False
    master=None
    def __init__(self,ms=None,PORT="COM4",baud_rate=9600,time_out=0.5,byte_size=serial.EIGHTBITS,stop_bits = serial.STOPBITS_ONE,PARITY=serial.PARITY_NONE):
        self.isRoopBackOk=False
        self.master=ms
        try:
            self.Serial=serial.Serial(port=PORT, baudrate=baud_rate, timeout=time_out,bytesize=byte_size,stopbits = stop_bits,parity=PARITY)
        except:
            print("Serialcommunicator:"+"シリアルポートが開けませんでした")
            self.setError2Conbobox()
            raise EnvironmentError('Unsupported platform')
            #pass
        try:
            commands = [ 0xB6, 0x01, 0x02, 0x00 ]
            for cmd in commands:
                data = struct.pack("B", cmd)
                print("tx: ", data)
                self.Serial.write(data)
        except:
            print("Serialcommunicator:"+"シリアルポートへの書き込みが失敗しました")
            self.setError2Conbobox()
            raise EnvironmentError('Unsupported platform')
            #pass,readline
        self.Serial.flush()
        rx = self.Serial.read_all()
        self.isRoopBackOk=(rx==self.RoopBackExpected)
        if self.isRoopBackOk:
            print("試験に成功しました!")
        print(rx)
        print("シリアルポートの接続に成功しました!")
        self.setenable2Conbobox()
    def SerialWrite(self):
        if self.Serial is not None:
            code="@0BAU W9600<cr><lf>"#ACUをセットアップするためのコマンドです
            ASCII=code.encode('ascii')#上記のコマンドをアスキーに変換しています pythonではByte型にこの時点でなっています
            print(ASCII)
            self.Serial.write(ASCII)
    def SerialInput(self):
        if self.Serial is not None:
            line=self.Serial.read_all()
            s=str(line)
            print("Input:"+s)
    def closeSrialPort(self):
        if self.Serial is not None:
            self.Serial.close()
    def setError2Conbobox(self):
        self.master.ACUmonitor.FrontEnd.COM_STATS_F.label.configure(text=self.ACUmonitor.FrontEnd.COM_F.combbox.get()+"is Not Support!",fg_color="red")
        self.master.ACUmonitor.FrontEnd.COM_F.combbox.configure(fg_color="red")
    def setenable2Conbobox(self):
        self.master.ACUmonitor.FrontEnd.COM_STATS_F.label.configure(text=self.ACUmonitor.FrontEnd.COM_F.combbox.get()+"is Support!",fg_color="blue")
        self.master.ACUmonitor.FrontEnd.COM_F.combbox.configure(fg_color="#3B8ED0")

class comMonitor(AsyncedClass):
    def Async(self):
        print("HELLO")
        self.sleep()
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)

class enableAsyncOnsite(AsyncedClass):
    AsyncList=None
    def setAsyncClass(self,Asyncs=None):
        if Asyncs is not None:
            #self.AsyncList.append(acu.BackEnd.Async(Asyncs))
            print("[enableAsyncOnsite]APPEND!")
    def Async(self):
        self.sleep()
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)
        
class GIFexecuter(AsyncedClass):
    GUI=None
    def Async(self):
        if self.GUI is not None:
            self.GUI.setGifFrames()
        self.sleep()
    def __init__(self,acu=None,sleepT=0.06,message="Its'Me!",ma=None,GUI=None):
        self.GUI=GUI
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)

class setTime(AsyncedClass):
    ts=None
    t0=None
    def Async(self):
        UTC=DATE_TIME.datetime.now(DATE_TIME.timezone.utc)
                
        JST=UTC.astimezone(timezone('Asia/Tokyo'))
        LST=self.setLSTFormat(datetime_=JST)
        jst_time="JST:"+str(JST.hour)+":"+str(JST.minute)+":"+str(JST.second)
        utc_time="UTC:"+str(UTC.hour)+":"+str(UTC.minute)+":"+str(UTC.second)
        year_time=(str(JST.year)+"."+str(JST.month)+"."+str(JST.day))
        self.ACUmonitor.FrontEnd.updateTimerbybackend(Year_Time=year_time,JSTformat=jst_time,UTCformat=utc_time,LSTformat=LST,UTC=str(TTT.utc.second))
        self.sleep()
        
    def setLSTFormat(self,datetime_):
        location=ASTRO.coordinates.EarthLocation(
            lon = (138 + 28/60 + 21.2/3600) * deg,
            lat = (35 + 56/60 + 40.9/3600)  * deg,
            height = 1350 * m,
        )
        localtime = ASTRO.time.Time(datetime_, format='datetime', location=location)
        lst=localtime.sidereal_time('apparent')
        lst_h = int(lst.hour)
        lst_m = int((lst.hour - lst_h) * 60)
        lst_s = int((lst.hour - lst_h - lst_m/60) * 3600)
        lst_ = '{lst_h:02d}:{lst_m:02d}:{lst_s:02d}'.format(**locals())
        msg = '{lst_}'.format(**locals())
        return "LST:"+msg
    
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        self.ts=load.timescale(builtin=True)
        super().__init__(acu)

class Serialcommunicator4GeneralUse(AsyncedClass):
    none="none"
    enable="enable"
    conected="conected"
    disconected="disconected"
    notconect="notconect"
    unkowm="unkowm"

    #GPSからのデータは恐らく数値型
    deviceType=none
    deviceName=none
    isDeviceConected=False
    isSucccesConect=False
    Serial=None
    Port=none
    Baudrate=9600
    serialInputter=None
    ControllMode="REAL"
    
    #--ANGENT
    mode=True
    timer=0
    funcok=False
    #--TEST--
    
    def getStringEqual(self,text1="none",text2="NONE"):
        return text1.casefold()==text2.casefold()

    def setText2CommandLine(self,text="none"):
        self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert(text+":["+self.deviceType+"]")
    
    def setDeviceDisconected(self):
        self.isDeviceConected=False
        self.isSucccesConect=False
        self.setText2CommandLine(text=" Disconected!")

    def setDeviceConected(self):
        self.isDeviceConected=True
        self.isSucccesConect=False
        self.setText2CommandLine(text=" Conected!")
        
    def Succces2ConectFunc(self):#接続が初めてできた時に呼ばれる
        pass
    
    def disConectFunc(self):#接続が着れた時に呼ばれる
        pass


    def setSuccces2Conect(self):
        self.isSucccesConect=True

    def setFaild2Conect(self):
        self.isSucccesConect=False
        self.setText2CommandLine(text=" ConectFaild!")

    def getConectStats(self):
        return self.isSucccesConect
    
    def getDeviceConectStats(self):
        return self.isSucccesConect
    
    def disconectSerial(self):
        if isinstance(self.Serial,serial):
            self.Serial.close()


    def Async(self):
        #-----IF TEST MODE FUNCTION--START---
        if not self.mode and self.timer<=1:#timer<=3で時間差を作っている
            self.timer+=self.sleepTime

        if not self.mode and self.timer>=1 and not self.funcok:
            self.setDeviceConected()
            self.sleep()
            self.sleep()
            self.sleep()
            self.sleep()
            self.setText2CommandLine(text="TryConect")
            
            self.setSuccces2Conect()
            self.Succces2ConectFunc()
            self.serialInputter.isSerialSet=True
            self.funcok=True
        
        if self.funcok:
            self.SerialFunc()
        #-----IF TEST MODE FUNCTION--END-----
        if not self.getDeviceConectStats() and self.mode:
            ports=list_ports.comports()
            device=[info for info in ports if self.deviceName in info.description] #.descriptionでデバイスの名前を取得出来る
            if not len(device) == 0:
                self.Port=device[0].device
                self.setDeviceConected()
            else:
                if self.isDeviceConected:
                    self.setDeviceDisconected()
                else:
                    self.isDeviceConected=False
                    self.isSucccesConect=False
        if self.isDeviceConected and not self.getConectStats() and self.mode:
            try:
                if isinstance(self.Serial,serial.Serial):
                    self.Serial.close()
                    self.Serial=None
                self.setText2CommandLine(text="TryConect")
                self.Serial=serial.Serial(self.Port, self.Baudrate,timeout=0.1)


            except (OSError, serial.SerialException):#切断されたときに呼ばれる
                self.setFaild2Conect()
            except:
                if isinstance(self.Serial,serial.Serial):
                    self.setText2CommandLine(text="ProgExept!")
                pass
            else:
                self.setSuccces2Conect()
                self.Succces2ConectFunc()
                self.serialInputter.isSerialSet=True
                self.serialInputter.Myserial=self.Serial
        if self.getConectStats() and self.mode:
            try:
                self.SerialFunc()
            except (OSError, serial.SerialException):#切断されたときに呼ばれる
                self.setDeviceDisconected()
                self.disConectFunc()
            except:
                if isinstance(self.Serial,serial.Serial):
                    self.setText2CommandLine(text="SerialWorong!")
                else:
                    self.setText2CommandLine(text="ProgExept!")
                pass
        self.sleep()

    def SerialFunc(self):
        pass
    
    def __init__(self,testMode=False,acu=None,sleepT=0.1,message="Serialcommunicator4GeneralUse",ma=None,deviceName="none",deviceType="none",inputter=None):
        self.deviceName=deviceName
        self.deviceType=deviceType
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        self.serialInputter=inputter
        #self.ControllMode=mode
        self.mode=not testMode
        super().__init__(acu)

class AnntenaMovement(AsyncedClass):
    
    kp = 1.5  # 任意の値、調整が必要
    ki = 0.001  # 任意の値、調整が必要
    kd = 0.01  # 任意の値、調整が必要
    prev_Azerror = 0
    Azintegral = 0
    prev_Elerror = 0
    Elintegral = 0

    def Async(self):
        if isinstance(self.Agent,AnntenaAgent):
            if self.Agent.On:#getAzStats,posMode,rate
                Azstats=self.Agent.getAzStats()
                Elstats=self.Agent.getElStats()
                #print("アンテナ代理",Azstats)
                if Azstats[2]=="posMode" or Azstats[2]=="rate":
                    self.AzPID()
                if Elstats[2]=="posMode" or Elstats[2]=="rate":
                    self.ElPID()
        self.sleep()
        
    def AzPID(self):
        dt = self.sleepTime
        currentangle=self.convertHex2AzPos(self.Agent.AzRealRad)
        target_angle=self.convertHex2AzPos(self.Agent.AzRad)
        if abs(self.relative_angle(first_angle=currentangle, second_angle=target_angle))>0.01:
            angular_velocity = self.calculate(setpoint=target_angle, current_value=currentangle, dt=dt,axis=1)

            # 角速度が制限範囲内に収める 
            angular_velocity = max(-45, min(45, angular_velocity))

            #print("BEFORE ADD ANGLE=",currentangle,"velo=",(angular_velocity * dt),"Tgt=",target_angle)
            currentangle=self.add_angle(original_angle=currentangle,add_angle=(angular_velocity * dt))
            #print("AFTER ADD ANGLE=",currentangle)
            self.Agent.AzRealRad=self.convertDeg2Hex(currentangle)
            #print(f"Current Angle: {currentangle}",f"Current Velocity:{angular_velocity}")
            #Diff=self.relative_angle(first_angle=current_angle, second_angle=target_angle)
            
    def ElPID(self):
        dt = self.sleepTime
        currentangle=self.convertHex2ElPos(self.Agent.ElRealRad)
        target_angle=self.convertHex2ElPos(self.Agent.ElRad)
        if abs(self.relative_angle(first_angle=currentangle, second_angle=target_angle))>0.01:
            angular_velocity = self.calculate(setpoint=target_angle, current_value=currentangle, dt=dt,axis=2)

            # 角速度が制限範囲内に収める
            angular_velocity = max(-45, min(45, angular_velocity))

            currentangle=self.add_angle(original_angle=currentangle,add_angle=(angular_velocity * dt))
                        
            self.Agent.ElRealRad=self.convertDeg2Hex(currentangle)
            #print(f"Current Angle: {currentangle}",f"Current Velocity:{angular_velocity}")
            #Diff=self.relative_angle(first_angle=current_angle, second_angle=target_angle)
     
    def convertDeg2Hex(self,angle):
        '''
        this is used to angle to sbca hex
        '''
        fixint=int(angle/0.005493164)
        hexvalue=hex(fixint)
        re=""
        for i in range(2,len(hexvalue)):
            re+=str(hexvalue[i])
        return re

    def convertHex2Deg(self,sbca_value, bit_count=16, resolution=360.0,mode=1):
        """
        Convert SBCA formatted value to angle.
        """
        hex_number = sbca_value  # 16進数として扱う文字列
        decimal_value = int(hex_number, 16)
        binary_number = bin(int(hex_number, 16))[2:].zfill(len(hex_number) * 4)  # 16進数を10進数に変換し、その後2進数に変換して0埋め
        if binary_number[0]=="1" and mode==2:
            decimal_value=(1 << (len(hex_number) * 4)) - decimal_value
            decimal_value*=-1
        normalized_value = decimal_value / 65535  # Normalize to [0, 1]
        angle = normalized_value * resolution
        return angle

    def convertHex2AzPos(self,sbca_value):
        return self.convertHex2Deg(sbca_value=sbca_value,resolution=360.0,mode=1)

    def convertHex2ElPos(self,sbca_value):
        return self.convertHex2Deg(sbca_value=sbca_value,resolution=360.0,mode=1)

    def convertHex2Rate(self,sbca_value):
        return self.convertHex2Deg(sbca_value=sbca_value,resolution=90.0,mode=2)

    def calculate(self, setpoint, current_value, dt,axis=1):#axis 1=az,2=el
        error = self.relative_angle(current_value,setpoint)
        if axis==1:
            self.Azintegral += error * dt
            derivative = (error - self.prev_Azerror) / dt
            output = self.kp * error + self.ki * self.Azintegral + self.kd * derivative
            self.prev_Azerror = error
        else:
            self.Elintegral += error * dt
            derivative = (error - self.prev_Elerror) / dt
            output = self.kp * error + self.ki * self.Elintegral + self.kd * derivative
            self.prev_Elerror = error
        return output
    
    def relative_angle(self,first_angle, second_angle):
        # 角度が範囲外の場合、正規化する
        first_angle = first_angle % 360
        second_angle = second_angle % 360

        # 0°から見たときの相対角度を計算
        relative_angle = second_angle - first_angle

        # 結果が180°より大きい場合、-180°から180°の範囲に収める
        if relative_angle > 180:
            relative_angle -= 360
        elif relative_angle < -180:
            relative_angle += 360

        return relative_angle
    
    def add_angle(self,original_angle,add_angle):
        original_angle = original_angle % 360
        add_angle = add_angle % 360
        
        angle=original_angle+add_angle
        angle%=360
        
        if angle<0:
            angle+=360
            
        return angle
    
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        self.ts=load.timescale(builtin=True)
        super().__init__(acu)
   
    def setAgent(self,Agentclass):
        self.Agent=Agentclass

class AnntenaAgent():
    '''
    アンテナを模倣したクラス]
    text.split(split_word)
    text.replace(delstr, '')
    time.sleep(float(self.sleepTime))
    '''
    
    bit_contents={"0-1-2":{"0":"stby","1":"rate","2":"SynSlave","3":"posMode"},"3":{"0":"Ifil","1":"Ⅱfil"}}
    Error="@8"
    IsInitialServo=False
    IsInitialACU=False
    
    Result=""
    
    On=False
    Off=True
    
    AzStats="1000"
    ElStats="1000"
    
    AzRad="0000"
    ElRad="0000"
    
    AzRealRad="0000"
    ElRealRad="0000"
    
    AzRate="0000"
    ElRate="0000"
    
    AzFistPos=0
    ElFirstPos=0
    
    def __init__(self,Anntena):
        if isinstance(Anntena,AnntenaMovement):
            Anntena.setAgent(self)
    
    def getAzStats(self):
        text_len=len(self.AzStats)
        print("getAzStats",self.AzStats)
        re=[]
        for i in range(1,text_len):
            if i==1:
                re.append(self.bit_contents["0-1-2"][self.AzStats[i]])
            if i==2:
                re.append(self.bit_contents["0-1-2"][self.AzStats[i]])
            if i==3:
                re.append(self.bit_contents["0-1-2"][self.AzStats[i]])
        return re
    
    def getElStats(self):
        text_len=len(self.ElStats)
        print("getElStats",self.ElStats)
        re=[]
        for i in range(1,text_len):
            if i==1:
                re.append(self.bit_contents["0-1-2"][self.ElStats[i]])
            if i==2:
                re.append(self.bit_contents["0-1-2"][self.ElStats[i]])
            if i==3:
                re.append(self.bit_contents["0-1-2"][self.ElStats[i]])
        return re
            
    def SetInitialmode(self,text):
        if text[0] is "@" and text[1] is "8":
            self.IsInitialServo=True
            self.IsInitialACU=False
        elif text[0] is "@" and text[1] is "0":
            self.IsInitialACU=True
            self.IsInitialServo=False
        else:
            self.IsInitialServo=False
            self.IsInitialACU=False

    def deleateInitial(self,text,initial):
        return text.replace(initial,'')

    def splitSpace(self,text):
        return text.split(" ")
    
    def splitText(self,text,sp):
        re=[text]
        if text.find(sp)>=0:
            re=text.split(sp)
        return re
        
    def setMessage(self,message):
        re="@?"
        print("[",type(self),"]data:",message.decode('ascii'))
        if isinstance(message,bytes):
            normMessage=message.decode('ascii') #or ascii
            self.SetInitialmode(normMessage)
            if self.IsInitialACU:
                initialdeleate=self.deleateInitial(text=normMessage,initial="@0")
                split=self.splitSpace(initialdeleate)
                split[len(split)-1]=self.deleateInitial(text=split[len(split)-1],initial="\r\n")
                if split[0] is "LBL":
                    if split[1] is "R1":
                        re="@0AZIMUTH"
                    if split[1] is "R2":
                        re="@0AZIMUTH,ELEVATION"
                    if split[1] is "R3":
                        re="@0AZIMUTH,ELEVATION,TILT"
                if split[0] is "STA":
                    if split[1] is "R40":
                        re="@0"
            elif self.IsInitialServo:
                initialdeleate=self.deleateInitial(text=normMessage,initial="@8")
                split=self.splitSpace(initialdeleate)
                split[len(split)-1]=self.deleateInitial(text=split[len(split)-1],initial="\r\n")
                
                if split[0]=="DO":
                    if split[1]=="W0300":
                        re="@0"
                        self.On=True
                        self.Off=False
                    if split[1]=="W0200":
                        re="@0"
                        self.On=False
                        self.Off=True
                    if split[1]=="R2":
                        if self.On:
                            re="@80300,0000"
                            
                        elif self.Off:
                            re="@80200,0000"
                elif split[0] == "MOD" and self.On:
                    if split[1] == "R1":
                        re="@8"+self.AzStats
                    if split[1] == "R2":
                        re="@8"+self.AzStats+","+self.ElStats
                    elif split[1].find("W")>=0:
                        initialdeleate=self.deleateInitial(text=split[1],initial="W")
                        split2=self.splitText(text=initialdeleate,sp=",")
                        split2[len(split2)-1]=self.deleateInitial(text=split2[len(split2)-1],initial="\r\n")
                        
                        for i in range(0,len(split2)):
                            if i==0:
                                self.AzStats=split2[0]
                            if i==1:
                                self.ElStats=split2[1]
                        
                        re="@8"
                elif split[0] == "POS"and self.On:
                    print("split2=",split)
                    if split[1] == "R1":
                        re="@8"+self.AzRealRad
                    elif split[1] == "R2":
                        re="@8"+self.AzRealRad+","+self.ElRealRad
                    elif split[1].find("W")>=0:
                        initialdeleate=self.deleateInitial(text=split[1],initial="W")
                        split2=self.splitText(text=initialdeleate,sp=",")
                        split2[len(split)-1]=self.deleateInitial(text=split2[len(split2)-1],initial="\r\n")
                        for i in range(0,len(split2)):
                            if i==0:
                                self.AzRad=split2[0]
                            if i==1:
                                self.ElRad=split2[1]
                        re="@8"
                elif split[0] == "RTE"and self.On:
                    if split[1] == "R1":
                        re="@8"+self.AzRate
                    elif split[1] == "R2":
                        re="@8"+self.AzRate+","+self.ElRate
                    elif split[1].find("W")>=0:
                        initialdeleate=self.deleateInitial(text=split[1],initial="W")
                        split2=self.splitText(text=initialdeleate,sp=",")
                        split2[len(split)-1]=self.deleateInitial(text=split2[len(split2)-1],initial="\r\n")
                        for i in range(0,len(split2)):
                            if i==0:
                                self.AzRad=split2[0]
                            if i==1:
                                self.ElRad=split2[1]
                        re="@8"
        print("[",type(self),"]RE:",re)
        self.Result=re.encode('ascii')
    
class ComClassBase():
    __serialCodes={'cr':"\r",'lf':"\n",'ack':'<<0x06>>','Space':'<<x20>>','cr(acu)':'<<x0d>>','ignoreM':'@?'}
    
    __isMessageSended=False
    
    __isMustCheckMessage=False
    
    __isMessageReceived=False
    
    __mySendedMessage="none"
    
    __recivedMessageContents=None
    
    __messageIgnoreTimes=3#何回応答メッセージが届かなかったら次の処理に移るかの目安
    
    __ignoretime=0
    
    __serialclass=None
    
    __executeStop=False
    
    __StopbyError=False

    def convertDeg2Hex(self,angle):
        '''
        this is used to angle to sbca hex
        '''
        fixint=int(angle/0.005493164)
        return hex(fixint)
    
    def normNum(self,num,ren=2,value="9",normround=5):
        find=num.find(".")
        lengh=len(num)
        okFlag=0
        re=float(num)
        if find!=-1:
            for i in range(find+1,lengh-1):
                if num[i] is value:
                    okFlag+=1
                else:
                    break
        if okFlag>=ren:
            re=round(re)
        else:
            re=round(re,normround)
        return re
    
    def convertHex2Deg(self,sbca_value="0000", bit_count=16, resolution=90.0,mode=1):
        """
        Convert SBCA formatted value to angle.
        """
        hex_number = sbca_value  # 16進数として扱う文字列
        decimal_value = int(hex_number, 16)
        binary_number = bin(int(hex_number, 16))[2:].zfill(len(hex_number) * 4)  # 16進数を10進数に変換し、その後2進数に変換して0埋め
        if binary_number[0]=="1" and mode==2:
            decimal_value=(1 << (len(hex_number) * 4)) - decimal_value
            decimal_value*=-1
        normalized_value = decimal_value / 65535  # Normalize to [0, 1]
        angle = normalized_value * resolution
        return angle
    
    def convertHex2AzPos(self,sbca_value):
        return self.convertHex2Deg(sbca_value=sbca_value,resolution=360.0,mode=1)

    def convertHex2ElPos(self,sbca_value):
        return self.convertHex2Deg(sbca_value=sbca_value,resolution=360.0,mode=1)

    def convertHex2Pos(self,sbca_value):
        return self.convertHex2Deg(sbca_value=sbca_value,resolution=90.0,mode=2)

    
    def executeCommand(self,command,isMustCheckMessage,ignoreTimes,getdata):
        if self.__executeStop:
            return
        
        self.__messageIgnoreTimes=ignoreTimes
        self.__isMustCheckMessage=isMustCheckMessage
        
        if self.__ignoretime>=self.__messageIgnoreTimes or self.__isMessageReceived:
            if self.__ignoretime>=self.__messageIgnoreTimes:
                self.__StopbyError=True
            self.setStopExecute()
            
        if self.__ignoretime>0:
            command=self.__mySendedMessage

        if self.__isMessageSended:#PCから送信済み
            if self.__isMustCheckMessage:
                if self.isIgnorePattern(getdata):#データが不十分過ぎたら
                    self.__ignoretime+=1
                    self.__isMessageSended=False
                    print("データが不十分です"+getdata,type(self))
                else:
                    self.checkMessage(getdata)#応答メッセージをチェックし、異常が無ければ
                pass
            else:
                self.__isMessageSended=False
                self.setStopExecute()
        else:
            print("WRITED",type(self),command)
            self.__serialWrite(command)
            self.__isMessageSended=True
            self.__mySendedMessage=command

    def setIsMessageReceived(self):
        self.__isMessageReceived=True

    def getIgnoretime(self):
        return self.__ignoretime
    
    def setMessageContents(self,text):
        self.__recivedMessageContents=text
        self.__isMessageReceived=True
        self.setStopExecute()

    def getTextDeleateStr(self,text,delstr):
        return text.replace(delstr, '')
    
    def getSplitText(self,text,split_word=','):
        return text.split(split_word)

    def getStopstats(self):
        return {"isStop":self.__executeStop,"byError":self.__StopbyError}
    
    def getContents(self):
        return self.__recivedMessageContents

    def getReceivedMessageContents(self):
        pass
            
    def checkMessage(self,message):#以上が無ければ、__isMessageReceivedと__recivedMessageContentsを変える
        pass
    
    def setStopExecute(self):
        self.__executeStop=True
        self.__ignoretime=0
        self.__mySendedMessage="none"
        self.__isMessageSended=False
        self.__isMustCheckMessage=False
        self.__isMessageReceived=False
        print("終了します",type(self),"Error",self.__StopbyError)
   
    def setEnableExecute(self):
        self.__executeStop=False
        self.__StopbyError=False
        self.__recivedMessageContents=None
        
    def __normalizeCode(self,code):
        return code
    
    def getSendedMessage(self):
        return self.__mySendedMessage
    
    def isIgnorePattern(self,message):#子クラスでオーバーライド
        pass
    
    def getnormSerialCode(self,serialcode="none"):
        normCode=self.__normalizeCode(serialcode)
        return self.__serialCodes[normCode]
    
    def __serialWrite(self,code="@0BAU W9600"):
        if  isinstance(self.__serialclass,Serialcommunicator4GeneralUse):
            code+=(self.__serialCodes['cr']+self.__serialCodes['lf'])
            self.__serialclass.SerialWrite(code)

    def __init__(self,serialclass=None):
        self.__serialclass=serialclass
        print("初期化完了")

class powerOnOffCom(ComClassBase):
    def __init__(self,serialclass=None):
        super().__init__(serialclass=serialclass)

    def isIgnorePattern(self,message):#子クラスでオーバーライド
        super(powerOnOffCom,self).isIgnorePattern(message)
        ig=message.find(self.getnormSerialCode('ignoreM'))
        ig=(ig>=0)
        nothing=message is ""
        return (ig or nothing)
    
    def checkMessage(self,message):#異常が無ければ、__isMessageReceivedと__recivedMessageContentsを変える
        super(powerOnOffCom,self).checkMessage(message)
        In8=self.message.find("@8")
        if In8>=0:
            if self.getSendedMessage().find("0300")>=0:
                self.setMessageContents(True)
            if self.getSendedMessage().find("0200")>=0:
                self.setMessageContents(False)

    def getReceivedMessageContents(self):
        super(powerOnOffCom,self).getReceivedMessageContents()
        return self.getContents()

class checkoutputCom(ComClassBase):
    def __init__(self,serialclass=None):
        super().__init__(serialclass=serialclass)

    def isIgnorePattern(self,message):#子クラスでオーバーライド
        super(checkoutputCom,self).isIgnorePattern(message)
        ig=message.find(self.getnormSerialCode('ignoreM'))
        ig=(ig>=0)
        nothing=message is ""
        return (ig or nothing)
    
    def checkMessage(self,message):#異常が無ければ、__isMessageReceivedと__recivedMessageContentsを変える
        super(checkoutputCom,self).checkMessage(message)
        InRpos=self.getSendedMessage().find("R")
        isInR=InRpos>=0
        if isInR:
            deleateInitial=self.getTextDeleateStr(text=message,delstr='@8')
            howmany=int(self.getSendedMessage()[InRpos+1])
            AzEl=self.getSplitText(text=deleateInitial)
            if howmany==2:
                if AzEl[0]=="0300":
                    self.setMessageContents(True)
                elif AzEl[0]=="0200":
                    self.setMessageContents(False)

    def getReceivedMessageContents(self):
        super(checkoutputCom,self).getReceivedMessageContents()
        return self.getContents()
        
class AxisModeCom(ComClassBase):
    
    bit_contents={"0-1-2":{"0":"stby","1":"rate","2":"SynSlave","3":"posMode"},"3":{"0":"Ifil","1":"Ⅱfil"}}
    
    def __init__(self,serialclass=None):
        super().__init__(serialclass=serialclass)
        
    def isIgnorePattern(self,message):#子クラスでオーバーライド
        super(AxisModeCom,self).isIgnorePattern(message)
        ig=message.find(self.getnormSerialCode('ignoreM'))
        ig=(ig>=0)
        nothing=message is ""
        return (ig or nothing)
    
    def getMessageContents(self,text):
        text_len=len(text)
        re=[]
        for i in range(1,text_len):
            if i==1:
                re.append(self.bit_contents["0-1-2"][text[i]])
            if i==2:
                re.append(self.bit_contents["0-1-2"][text[i]])
            if i==3:
                re.append(self.bit_contents["0-1-2"][text[i]])
        return re
            
    def checkMessage(self,message):#異常が無ければ、__isMessageReceivedと__recivedMessageContentsを変える
        super(AxisModeCom,self).checkMessage(message)
        InRpos=self.getSendedMessage().find("R")
        isInR=InRpos is not -1
        InWpos=self.getSendedMessage().find("W")
        isInW=InWpos is not -1
        if isInR:
            deleateInitial=self.getTextDeleateStr(text=message,delstr='@8')
            howmany=int(self.getSendedMessage()[InRpos+1])
            if howmany==1:
                az=self.getMessageContents(deleateInitial)
                self.setMessageContents({"Az":az[2]})
            elif howmany==2:
                AzEl=self.getSplitText(text=deleateInitial)
                
                az=self.getMessageContents(AzEl[0])
                el=self.getMessageContents(AzEl[1])
                self.setMessageContents({"Az":az[2],"El":el[2]})
        if isInW:
            print("self.getSendedMessage=",self.getSendedMessage())
            deleateInitial=self.getTextDeleateStr(text=self.getSendedMessage(),delstr='@8MOD W')
            howmany=int(deleateInitial.count(",")+1)
            if howmany==1:
                az=self.getMessageContents(deleateInitial)
                self.setMessageContents({"Az":az[2]})
            elif howmany==2:
                AzEl=self.getSplitText(text=deleateInitial)
                az=self.getMessageContents(AzEl[0])
                el=self.getMessageContents(AzEl[1])
                self.setMessageContents({"Az":az[2],"El":el[2]})
            
        
    def getReceivedMessageContents(self):
        super(AxisModeCom,self).getReceivedMessageContents()
        return self.getContents()

class PositionCom(ComClassBase):
    
    
    def __init__(self,serialclass=None):
        super().__init__(serialclass=serialclass)

    def isIgnorePattern(self,message):#子クラスでオーバーライド
        super(PositionCom,self).isIgnorePattern(message)
        ig=message.find(self.getnormSerialCode('ignoreM'))
        ig=(ig>=0)
        nothing=message is ""
        return (ig or nothing)
    
    def checkMessage(self,message):#異常が無ければ、__isMessageReceivedと__recivedMessageContentsを変える
        super(PositionCom,self).checkMessage(message)
        InRpos=self.getSendedMessage().find("R")
        isInR=InRpos is not -1
        InWpos=self.getSendedMessage().find("W")
        isInW=InWpos is not -1

        if isInR:
            deleateInitial=self.getTextDeleateStr(text=message,delstr='@8')
            howmany=int(self.getSendedMessage()[InRpos+1])
            if howmany==1:
                self.setMessageContents({"Az":self.convertHex2Deg(sbca_value=deleateInitial,resolution=360)})
            elif howmany==2:
                AzEl=self.getSplitText(text=deleateInitial)
                print("AZ",AzEl[0])
                print(type(AzEl[0]))
                self.setMessageContents({"Az":self.convertHex2AzPos(sbca_value=AzEl[0]),"El":self.convertHex2ElPos(sbca_value=AzEl[1])})
        if isInW:
            deleateInitial=self.getTextDeleateStr(text=self.getSendedMessage(),delstr='@8POS W')
            print("now ignore=",self.getIgnoretime())
            howmany=int(deleateInitial.count(",")+1)
            if howmany==1:
                self.setMessageContents({"Az":self.convertHex2Deg(sbca_value=deleateInitial,resolution=360)})
            elif howmany==2:
                AzEl=self.getSplitText(text=deleateInitial)
                self.setMessageContents({"Az":self.convertHex2Deg(sbca_value=AzEl[0],resolution=360),"El":self.convertHex2Deg(sbca_value=AzEl[1],resolution=360)})

        
    def getReceivedMessageContents(self):
        super(PositionCom,self).getReceivedMessageContents()
        return self.getContents()
        

class ObserbDiffClass():
    
    __nowstats=None
    
    __beforestats=None
    
    __statsType=1
    
    __ischange=False
    
    
    '''
    __statsType
    1=数字
    2=CommandMode
    '''
    
    def setNowstats(self,stats):
        self.__nowstats=stats
        self.setStats()
        
    def setbeforestats(self,stats):
        self.__beforestats=stats
        
    def __init__(self,statsType):
        self.__statsType=statsType
        if statsType==1:
            self.__beforestats=0
            self.__nowstats=0
            
    def isValue(self,n):
        re=False
        if isinstance(n, int):
            re=True
        if isinstance(n, float):
            re=True
        return re
        
    def setStats(self):#どちらかがNoneでも実行する場合もある
        re=False
        if self.__statsType==1 and self.isValue(self.__nowstats) and self.isValue(self.__beforestats):
            if self.__nowstats is not self.__beforestats:
                re=True
        if self.__statsType==2:
            if self.__nowstats is not self.__beforestats:
                re=True
        self.__ischange=re
        
    def getchangeStats(self):
        return self.__ischange
    
    def getNowstats(self):
        return self.__nowstats
    
    def getBfrstats(self):
        return self.__beforestats
    
    def chancellnow(self):
        self.__nowstats=self.__beforestats
        
class RotManager(ObserbDiffClass):
    
    bfr_time=None
    
    speed=0
    
    def __init__(self):
        super().__init__(statsType=1)
        self.setNowstats(stats=None)
        self.setbeforestats(stats=None)
        
    def reset(self):
        self.bfr_time=None
        self.update_interval=None
        self.setNowstats(stats=None)
        self.setbeforestats(stats=None)
        self.speed=0

    def updateRot(self,rot):
        self.setbeforestats(self.getNowstats())
        self.setNowstats(rot)
        if self.bfr_time is None:
            self.bfr_time=time.time()
        if self.getchangeStats():
            end = time.time()  # 現在時刻（処理完了後）を取得
            interval = end - self.bfr_time  # 処理完了後の時刻から処理開始前の時刻を減算する
            self.speed=self.relative_angle(first_angle=self.getBfrstats(), second_angle=self.getNowstats())/interval
            

    def relative_angle(self,first_angle, second_angle):
        # 角度が範囲外の場合、正規化する
        first_angle = first_angle % 360
        second_angle = second_angle % 360

        # 0°から見たときの相対角度を計算
        relative_angle = second_angle - first_angle

        # 結果が180°より大きい場合、-180°から180°の範囲に収める
        if relative_angle > 180:
            relative_angle -= 360
        elif relative_angle < -180:
            relative_angle += 360

        return relative_angle

class AxisStatsManager():
    
    __nowProgRot=None
    
    __nowRealRot=0
    
    __axisStats=None
    
    __statsCommand="0001"#prog
    
    __NowAxisMode=None
    
    __BfrAxisMode=None
        
    __rotation_manager=None
    
    name="AZ"
    
    def setRealRot(self,rot):
        self.__nowRealRot=rot
        self.__rotation_manager.updateRot(rot=rot)
        
    def getRealRot(self):
        return self.__nowRealRot
    
    def getProgRot(self):
        return self.__nowProgRot

        
    def setProgRot(self,rot):
        self.__nowProgRot=rot

    
    def getRotSpeed(self):
        return self.__rotation_manager.speed
    
    def __init__(self,name=""):
        self.__rotation_manager=RotManager()
        self.name=name
        
        
    def reset(self):
        self.__nowProgRot=None
        self.__nowRealRot=0
        self.__axisStats=None
        self.__statsCommand="0001"
        self.__rotation_manager.reset()
        self.__NowAxisMode=None
        self.__BfrAxisMode=None
        
    def setStatsCom(self,com):
        self.__statsCommand=com
        
        
    def getStatsCom(self):
        return self.__statsCommand
    

    def updateStats(self,axisStats):
        if isinstance(axisStats,AxisMode):
            #print("STATS_THE=",axisStats,self.name)
            self.__BfrAxisMode=self.__NowAxisMode
            self.__NowAxisMode=axisStats
            
    def getStats(self):
        return {"nowAxismode":self.__NowAxisMode,"bfrAxismode":self.__BfrAxisMode}
    
    def isstby2notstby(self):
        return self.__BfrAxisMode is AxisMode.Stby and self.__NowAxisMode is AxisMode.Stby

    def isstats2stby(self):
        return self.__BfrAxisMode is not AxisMode.Stby and self.__NowAxisMode is AxisMode.Stby
    
    def isstats2manustop(self):
        return self.__BfrAxisMode is not AxisMode.ManuStop and self.__NowAxisMode is AxisMode.ManuStop

    def isstats2manuset(self):
        return self.__BfrAxisMode is not AxisMode.ManuSet and self.__NowAxisMode is AxisMode.ManuSet

class AnntenaController(Serialcommunicator4GeneralUse):
        
    setUped=False
        
    timeScale=None
    
    planets=None
    Site=None
    Earth=None
    TimeScale=None
        
    #----------
    ACUAgent=None
    AnntenaMovement=None
    #----------
    
    #-----
    AzMaxRot=360
    AzMinRot=-360
    ElMaxRot=89
    ElMinRot=0
    
    AzRotSum=0
    #-----
    
    #----
    PowerOnOffCom=None
    CheckOutPutCom=None
    AxisModeCom=None
    PositionCom=None
    
    IscheckPowerOn=None
    PowerOn=False
    IscheckManualMode=False
    IsexecuteManualMode=False
    IsManualMode=False
    
    #----
    
    def getData(self):
        return self.ReceivedData
    
    def Succces2ConectFunc(self):
        super(AnntenaController,self).Succces2ConectFunc()
        self.setConectStats2GUI(flag=True)
        
    def disconectSerial(self):#Setnotconect2Antenna
        super(AnntenaController,self).disconectSerial()
        self.setConectStats2GUI(flag=False)
        self.AzStatsManager.reset()
        self.ElStatsManager.reset()
        self.AxisComStats=None
        self.NowCommand=None
        self.NowCommandKind=None
        self.EXECUTED=False
        self.READED=False
        self.setUped=False
        
        self.PowerOnOffCom.setStopExecute()
        self.CheckOutPutCom.setStopExecute()
        self.AxisModeCom.setStopExecute()
        self.PositionCom.setStopExecute()
    
        self.IscheckPowerOn=None
        self.PowerOn=False
        self.IscheckManualMode=False
        self.IsManualMode=False
        
    def setConectStats2GUI(self,flag):
        if flag:
            self.ACUmonitor.FrontEnd.Setconect2Antenna()
            self.ACUmonitor.FrontEnd.setNotConect(flag=False)
            self.ACUmonitor.FrontEnd.setConect(flag=True)
            self.ACUmonitor.FrontEnd.setAnttenaMoving(flag=False)
            self.ACUmonitor.FrontEnd.setAzMoving(flag=False)
            self.ACUmonitor.FrontEnd.setElMoving(flag=False)

        else:
            self.ACUmonitor.FrontEnd.Setnotconect2Antenna()
            self.ACUmonitor.FrontEnd.setNotConect(flag=True)
            self.ACUmonitor.FrontEnd.setConect(flag=False)
            self.ACUmonitor.FrontEnd.setAnttenaMoving(flag=False)
            self.ACUmonitor.FrontEnd.setAzMoving(flag=False)
            self.ACUmonitor.FrontEnd.setElMoving(flag=False)

            
    def setUpAntenna(self):
        if not self.setUped:
            if not self.mode:
                if  self.IscheckPowerOn is not None:
                    if not self.PowerOnOffCom.getContents() and not self.IscheckPowerOn:
                        self.PowerOnOffCom.executeCommand(command="@8DO W0300",isMustCheckMessage=False,ignoreTimes=3,getdata=self.serialInputter.data)
                        self.IscheckPowerOn=True
                    else:
                        self.PowerOn=True
                        self.setText2CommandLine(text="AnntenaIsWorking")
                else:
                    self.CheckOutPutCom.executeCommand(command="@8DO R2",isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
                    #"print(self.serialInputter.data)
                    if self.CheckOutPutCom.getContents() is True:
                        self.IscheckPowerOn=True
                    elif self.CheckOutPutCom.getContents() is False:
                        self.IscheckPowerOn=False
                if self.PowerOn:
                    if self.IscheckManualMode:
                        self.AxisModeCom.executeCommand(command="@8MOD R2",isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
                        print("AZ",self.AxisModeCom.getContents()["Az"])
                        if  self.AxisModeCom.getContents()["Az"]=="stby" or self.AxisModeCom.getContents()["El"]=="stby":
                            self.AxisModeCom.setStopExecute()
                            self.AxisModeCom.setEnableExecute()
                            self.AxisModeCom.executeCommand(command="@8MOD W1003,1003",isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
                        else:
                            self.IsManualMode=True
                            self.setText2CommandLine(text="AZ:"+str(self.AxisModeCom.getContents()["Az"])+"EL:"+str(self.AxisModeCom.getContents()["El"]))
                    elif not self.IscheckManualMode:
                        self.IscheckManualMode=True
                        self.AxisModeCom.executeCommand(command="@8MOD R2",isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
                if self.IsManualMode:
                    self.setUped=True
                    self.setText2CommandLine(text="AzElStandby")
                    #self.setPowerOn2GUI()

    def getTimeNow(self):
        return self.TimeScale.now()+timedelta(milliseconds=150) 
    
    def getAzELrot(self,coords):
        Az=None
        El=None
        if isinstance(coords,dict):
            if len(coords)>0:
                #self.UpdateAzEL=True
                mode=coords["coordmode"]
                t=self.getTimeNow()
                if mode is Coordinate.J2000:
                    star = Star(ra_hours=coords["ra"],dec_degrees=coords["dec"])
                    astrometric = self.Site.at(t).observe(star)
                    apparent = astrometric.apparent()
                    alt, az, distance = apparent.altaz()
                    Az=az.degrees
                    El=alt.degrees
                if mode is Coordinate.StarName:
                    planet=planets[coords["star"]]
                    astrometric = self.Earth.at(t).observe(planet)           
                    ra, dec, distance = astrometric.radec()
                    star = Star(ra_hours=ra.hours,dec_degrees=dec.degrees)
                    astrometric = self.Site.at(t).observe(star)
                    apparent = astrometric.apparent()
                    alt, az, distance = apparent.altaz()
                    Az=az.degrees
                    El=alt.degrees
        return Az,El

    def getAngleDiff(self,first_angle,second_angle):
        # 角度が範囲外の場合、正規化する
        first_angle = first_angle % 360
        second_angle = second_angle % 360
        # 0°から見たときの相対角度を計算
        relative_angle = second_angle - first_angle
        # 結果が180°より大きい場合、-180°から180°の範囲に収める
        if relative_angle > 180:
            relative_angle -= 360
        elif relative_angle < -180:
            relative_angle += 360
        return relative_angle

    def convertDeg2Hex(self,angle):
        '''
        this is used to angle to sbca hex
        '''
        fixint=int(angle/0.005493164)
        hexvalue=hex(fixint)
        re=""
        for i in range(2,len(hexvalue)):
            re+=str(hexvalue[i])
        return re

    
    #---ADVANCED--COMEXECUTRER-------
    AZ_MODE=None
    EL_MODE=None
    BFR_AZ_MODE=None
    BFR_EL_MODE=None

    
    def monitorAzmode(self):
        self.AZ_MODE,self.BFR_AZ_MODE=self.ACUmonitor.FrontEnd.getAzMode()
    
    def monitorElmode(self):
        self.EL_MODE,self.BFR_EL_MODE=self.ACUmonitor.FrontEnd.getElMode()
        
    def ischangeAz2notStby(self):
        return self.BFR_AZ_MODE is AxisMode.Stby and self.AZ_MODE is not AxisMode.Stby
    
    def ischangeAz2Stby(self):
        return self.BFR_AZ_MODE is not AxisMode.Stby and self.AZ_MODE is AxisMode.Stby
    
    def ischangeEl2notStby(self):
        return self.BFR_EL_MODE is AxisMode.Stby and self.EL_MODE is not AxisMode.Stby
    
    def ischangeEl2Stby(self):
        return self.BFR_EL_MODE is not AxisMode.Stby and self.EL_MODE is AxisMode.Stby


    def getAzmanualRot(self):
        return self.ACUmonitor.FrontEnd.getAzRot()
    
    def getElmanualRot(self):
        return self.ACUmonitor.FrontEnd.getElRot()

    def setAzValues(self,progRot=0,realRot=0,rotdiff=0,rotSpeed=0):
        self.ACUmonitor.FrontEnd.updateAzValues(progRot=progRot,realRot=realRot,rotdiff=rotdiff,rotSpeed=rotSpeed)

    def setElValues(self,progRot=0,realRot=0,rotdiff=0,rotSpeed=0):
        self.ACUmonitor.FrontEnd.updateElValues(progRot=progRot,realRot=realRot,rotdiff=rotdiff,rotSpeed=rotSpeed)

     
    
    def setAz2StbyCom(self):
        #self.AzStatsManager.setStatsCom(com="1000")
        print("setAz2StbyCom")
        self.executeCommand(kind=CommandMode.UpdateAxisMode,comvalue="@8MOD W1000")    

    def setAz2ManuCom(self):
        #self.AzStatsManager.setStatsCom(com="1003")
        self.executeCommand(kind=CommandMode.UpdateAxisMode,comvalue="@8MOD W1003")    

    def setEl2StbyCom(self):
        #self.ElStatsManager.setStatsCom(com="1000")
        self.executeCommand(kind=CommandMode.UpdateAxisMode,comvalue="@8MOD W"+self.AzStatsManager.getStatsCom()+",1000")    

    def setEl2ManuCom(self):
        #self.AzStatsManager.setStatsCom(com="1003")
        self.executeCommand(kind=CommandMode.UpdateAxisMode,comvalue="@8MOD W"+self.AzStatsManager.getStatsCom()+",1003")    

    def executeAxisRead(self):
        self.executeCommand(kind=CommandMode.ReadAxis,comvalue="@8POS R2")    

    def executeAxisUpdate(self,azrot=0,elrot=0):
        az=self.convertDeg2Hex(angle=azrot)
        el=self.convertDeg2Hex(angle=elrot)
        self.executeCommand(kind=CommandMode.UpdateAxis,comvalue="@8POS W"+az+","+el)    

    def AzorEl2AxisModeChange(self):
        return self.ischangeAz2notStby() or self.ischangeAz2Stby() or self.ischangeEl2notStby() or self.ischangeEl2Stby()

    def convertDeg2Hex(self,angle):
        '''
        this is used to angle to sbca hex
        '''
        fixint=int(angle/0.005493164)
        hexvalue=hex(fixint)
        re=""
        for i in range(2,len(hexvalue)):
            re+=str(hexvalue[i])
        return re.upper()
    
    def getAngleDiff(self,first_angle, second_angle):
        # 角度が範囲外の場合、正規化する
        relative_angle=None
        if first_angle is not None and second_angle is not None:
            first_angle = first_angle % 360
            second_angle = second_angle % 360

            # 0°から見たときの相対角度を計算
            relative_angle = second_angle - first_angle

            # 結果が180°より大きい場合、-180°から180°の範囲に収める
            if relative_angle > 180:
                relative_angle -= 360
            elif relative_angle < -180:
                relative_angle += 360

        return relative_angle


    AzStatsManager=None
    ElStatsManager=None
    AxisComStats=None
    
    NowCommand=None
    NowCommandKind=None
    
    EXECUTED=False
    READED=True
    
    def isValue(self,n):
        re=False
        if isinstance(n, int):
            re=True
        if isinstance(n, float):
            re=True
        return re

    def getwhatdoAxisCom(self):
        if self.AxisComStats is None:
            self.AxisComStats=CommandMode.ReadAxis
        elif isinstance(self.AxisComStats,CommandMode):
            if self.AxisComStats is CommandMode.ReadAxis:
                self.AxisComStats=CommandMode.UpdateAxis
            elif self.AxisComStats is CommandMode.UpdateAxis:
                self.AxisComStats=CommandMode.ReadAxis
        return self.AxisComStats
    
    def executeCommand(self,kind=None,comvalue=""):
        if isinstance(kind,CommandMode) and comvalue!="" and not self.EXECUTED:
            self.READED=False
            self.EXECUTED=True
            if kind is CommandMode.UpdateAxisMode:
                self.NowCommandKind=CommandMode.UpdateAxisMode
                self.NowCommand=self.AxisModeCom#setEnableExecute
                self.NowCommand.executeCommand(command=comvalue,isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
            
            if kind is CommandMode.ReadAxisMode:
                self.NowCommandKind=CommandMode.ReadAxisMode
                self.NowCommand=self.AxisModeCom
                self.NowCommand.executeCommand(command=comvalue,isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
            
            if kind is CommandMode.UpdateAxis:
                self.NowCommandKind=CommandMode.UpdateAxis
                self.NowCommand=self.PositionCom
                print("execute=",comvalue)
                self.NowCommand.executeCommand(command=comvalue,isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
            
            if kind is CommandMode.ReadAxis:
                print("EXECUTE READAXIS!")
                self.NowCommandKind=CommandMode.ReadAxis
                self.NowCommand=self.PositionCom
                self.NowCommand.executeCommand(command=comvalue,isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)

    def readCommand(self):
        if isinstance(self.NowCommandKind,CommandMode) and isinstance(self.NowCommand,ComClassBase) and not self.READED and self.EXECUTED:
            stopstats=self.NowCommand.getStopstats()
            if stopstats["isStop"] and not stopstats["byError"]:
                self.READED=True
                self.EXECUTED=False
                if self.NowCommandKind is CommandMode.UpdateAxisMode or self.NowCommandKind is CommandMode.ReadAxisMode:
                    axisstats=self.NowCommand.getReceivedMessageContents()
                    if axisstats["Az"]=="stby":
                        self.AzStatsManager.setStatsCom(com="1000")
                    if axisstats["Az"]=="posMode":
                        self.AzStatsManager.setStatsCom(com="1003")
                    if "El" in axisstats:
                        if axisstats["El"]=="stby":
                            self.ElStatsManager.setStatsCom(com="1000")
                        if axisstats["El"]=="posMode":
                            self.ElStatsManager.setStatsCom(com="1003")
                
                if self.NowCommandKind is CommandMode.UpdateAxis:
                    axisstats=self.NowCommand.getReceivedMessageContents()
                    #print("axisstats1=",axisstats,"Elin",("El" in axisstats))
                    self.AzStatsManager.setProgRot(axisstats["Az"])
                    if "El" in axisstats:
                        self.ElStatsManager.setProgRot(axisstats["El"])
                        
                if self.NowCommandKind is CommandMode.ReadAxis:
                    axisstats=self.NowCommand.getReceivedMessageContents()
                    #print("axisstats2=",axisstats)
                    self.AzStatsManager.setRealRot(axisstats["Az"])
                    if "El" in axisstats:#self.ACUmonitor.FrontEnd.setAnttenaMoving(flag=False)
                        self.ElStatsManager.setRealRot(axisstats["El"])#getRotSpeed,isValue
                    self.setAzValues(progRot=self.AzStatsManager.getProgRot(),realRot=self.AzStatsManager.getRealRot(),rotdiff=self.getAngleDiff(first_angle=self.AzStatsManager.getRealRot(), second_angle=self.AzStatsManager.getProgRot()),rotSpeed=self.AzStatsManager.getRotSpeed())
                    self.setElValues(progRot=self.ElStatsManager.getProgRot(),realRot=self.ElStatsManager.getRealRot(),rotdiff=self.getAngleDiff(first_angle=self.ElStatsManager.getRealRot(), second_angle=self.ElStatsManager.getProgRot()),rotSpeed=self.ElStatsManager.getRotSpeed())
                    azmove=self.isValue(self.AzStatsManager.getRotSpeed())
                    elmove=self.isValue(self.ElStatsManager.getRotSpeed())
                    self.ACUmonitor.FrontEnd.setAnttenaMoving(flag=azmove or elmove)
                    self.ACUmonitor.FrontEnd.setAzMoving(flag=azmove)
                    self.ACUmonitor.FrontEnd.setElMoving(flag=elmove)
                self.NowCommand.setEnableExecute()
                self.NowCommandKind=None
                self.NowCommand=None
                
            elif not stopstats["isStop"] and not stopstats["byError"]:
                if self.NowCommandKind is CommandMode.UpdateAxisMode or self.NowCommandKind is CommandMode.ReadAxisMode:
                    self.NowCommand.executeCommand(command="",isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
                if self.NowCommandKind is CommandMode.UpdateAxis or self.NowCommandKind is CommandMode.ReadAxis:
                    self.NowCommand.executeCommand(command="",isMustCheckMessage=True,ignoreTimes=3,getdata=self.serialInputter.data)
            elif stopstats["byError"] and stopstats["isStop"]:
                self.NowCommand.setStopExecute()
                self.NowCommand.setEnableExecute()
                self.NowCommandKind=None
                self.NowCommand=None
                self.READED=True
                self.EXECUTED=False
                print("ERROR!")
                pass#ここにエラー時の処理を書く
    #---ADVANCED--COMEXECUTRER-END-------updateStats

    
    def SerialFunc(self):
        super(AnntenaController,self).SerialFunc()
        self.setUpAntenna()
        if self.setUped:
            self.readCommand()
            if self.READED:
                self.monitorAzmode()
                self.monitorElmode()
                if self.AzorEl2AxisModeChange():#AzかElの状態が変わったことを示す
                    if self.ischangeAz2Stby():
                        self.setAz2StbyCom()
                    if self.ischangeEl2Stby():
                        self.setEl2StbyCom()
                    if self.ischangeAz2notStby():
                        self.setAz2ManuCom()
                    if self.ischangeEl2notStby():
                        self.setEl2ManuCom()
                else:#AzとELはそのまま
                    do=self.getwhatdoAxisCom()
                    if do is CommandMode.ReadAxis:
                        self.executeAxisRead()
                    else:
                        planet_coords=self.ACUmonitor.FrontEnd.getPlanetCoords()
                        Az,El=self.getAzELrot(planet_coords)
                        azrot=self.AzStatsManager.getRealRot()
                        elrot=self.ElStatsManager.getRealRot()
                        if Az is None and self.AZ_MODE is not AxisMode.Prog:
                            if self.AZ_MODE is AxisMode.ManuSet:
                                Az=self.getAzmanualRot()
                            if self.BFR_AZ_MODE is AxisMode.ManuSet and self.AZ_MODE is AxisMode.ManuStop or (self.BFR_AZ_MODE is AxisMode.Prog and self.AZ_MODE is AxisMode.Manu):
                                Az=azrot
                        
                        if El is None and self.EL_MODE is not AxisMode.Prog:
                            if self.EL_MODE is AxisMode.ManuSet:
                                El=self.getElmanualRot()
                            if self.BFR_EL_MODE is AxisMode.ManuSet and self.EL_MODE is AxisMode.ManuStop or (self.BFR_EL_MODE is AxisMode.Prog and self.EL_MODE is AxisMode.Manu):
                                El=elrot
                        
                        if Az is None and El is None and self.AZ_MODE:
                            self.executeAxisRead()
                        else:
                            self.executeAxisUpdate(azrot=(Az if Az is not None else azrot),elrot=(El if El is not None else elrot))
            
        
    def SerialWrite(self,text):#isinstance(self.Serial,serial):
        if self.Serial is not None and self.ControllMode is "REAL":
            ASCII=text.encode('ascii')#上記のコマンドをアスキーに変換しています pythonではByte型にこの時点でなっています
            self.Serial.write(ASCII)
        else:
            self.ACUAgent.setMessage(text.encode('ascii'))
            
    def readline(self):
        return self.ACUAgent.Result
        
    def __init__(self,acu=None,sleepT=0.1,message="Serialcommunicator4GeneralUse",ma=None,deviceName="none",deviceType="none",inputter=None,movent=None,testMode=False):
        super().__init__(acu=acu,sleepT=sleepT,message=message,ma=ma,deviceName=deviceName,deviceType=deviceType,inputter=inputter,testMode=testMode)
        self.serialInputter.Myserial=self
        self.AzStatsManager=AxisStatsManager(name="AZ")
        self.ElStatsManager=AxisStatsManager(name="EL")
        self.planets = load('de421.bsp')
        self.Earth=self.planets['earth']
        self.Site=self.Earth+wgs84.latlon(45, 5)
        self.TimeScale=load.timescale(builtin=True)
        self.PowerOnOffCom=powerOnOffCom(serialclass=self)
        self.CheckOutPutCom=checkoutputCom(serialclass=self)
        self.AxisModeCom=AxisModeCom(serialclass=self)
        self.PositionCom=PositionCom(serialclass=self)
        if testMode:
            self.ACUAgent=AnntenaAgent(movent)



class InputRoopClass(AsyncedClass):

    data=None

    isSerialSet=False

    Myserial=None
    
    Mode="REAL" #or TEST

    def Async(self):
        if self.isSerialSet and isinstance(self.Myserial,serial.Serial):
            self.data = self.Myserial.readline().decode('ascii')  
            pass
        elif self.isSerialSet and isinstance(self.Myserial,AnntenaController):
            self.data = self.Myserial.readline().decode('ascii')  
        else:
            #print("成功!")
            pass
        self.sleep()

    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)

class GPSManager(Serialcommunicator4GeneralUse):
    
    GPSstats=False
    
    def SerialFunc(self):
        super(GPSManager,self).SerialFunc()
        data = self.Serial.readline().decode('utf-8')  # NMEAデータの読み込み
                                
        if data.startswith('$GNRMC'):  # GNRMCセンテンスの処理
            msg = pynmea2.parse(data)
            stats = msg.status  # ステータス (A: 有効、V: 無効)
            if self.getStringEqual(text1=stats,text2="A"):
                self.GPSstats=True
            else:
                self.GPSstats=False
            self.setText2CommandLine(stats)
                    
        elif data.startswith('$GNGGA') and self.GPSstats:
            msg = pynmea2.parse(data)
            lat_dir = msg.lat_dir
            latitude = msg.latitude  # 緯度
            longitude = msg.longitude  # 経度
            lon_dir = msg.lon_dir
            altitude = msg.altitude  # 高度
            hdop = msg.horizontal_dil  # 水平精度 (HDOP)
            time = msg.timestamp  # 時刻
            time = datetime.combine(datetime.today().date(), time)


    def __init__(self,acu=None,sleepT=0.1,message="Serialcommunicator4GeneralUse",ma=None,deviceName="none",deviceType="none"):
        super().__init__(acu=acu,sleepT=sleepT,message=message,ma=ma,deviceName=deviceName,deviceType=deviceType)
        
class GPSTimer(AsyncedClass):
    #GPSからのデータは恐らく数値型
    GPSdeviceName="Prolific"
    isGPSConected=False
    isSucccesConect=False
    Port="COM"
    Baudrate=9600
    ser=None
    def getTime(self):
        num=timezone.find(":")
    
    def setDeviceDisconected(self):
        self.isGPSConected=False
        self.isSucccesConect=False
    def setDeviceConected(self):
        self.isGPSConected=True
        self.isSucccesConect=False
    def setSuccces2Conect(self):
        self.isSucccesConect=True
        self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert("Succces2Conect"+":[GPSdevice]")
    def setFaild2Conect(self):
        self.isSucccesConect=False
    def getConectStats(self):
        return self.isSucccesConect
    def getDeviceConectStats(self):
        return self.isGPSConected
    
    def getVeryAccurateTime(self):
        print("")
        
        
    def Async(self):
        if not self.getDeviceConectStats():
            ports=list_ports.comports()
            device=[info for info in ports if self.GPSdeviceName in info.description] #.descriptionでデバイスの名前を取得出来る
            if not len(device) == 0:
                self.Port=device[0].device
                self.setDeviceConected()
                self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert("GPSConected!"+":[GPSdevice]")
        if self.isGPSConected and not self.getConectStats():
            try:
                if self.ser is not None:
                    self.ser.close()
                self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert("TrytoConect"+":[GPSdevice]")
                self.ser=serial.Serial(self.Port, self.Baudrate)
                print("Serialcommunicator:"+"シリアルポートを開きました:"+self.Port)
                self.setSuccces2Conect()
            except:
                self.setFaild2Conect()
                self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert("FaildtoConect"+":[GPSdevice]")
        if self.getConectStats():
            
            try:
                data = self.ser.readline().decode('utf-8')  # NMEAデータの読み込み
                
                print(data+"\n"+str(data.startswith('$GNRMC',0)))
                
                if data.startswith('$GNRMC'):  # GNRMCセンテンスの処理
                    msg = pynmea2.parse(data)
                    stats = msg.status  # ステータス (A: 有効、V: 無効)
                    self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert(stats+":[GPSdevice]")
                    
                elif data.startswith('$GNGGA'):
                    msg = pynmea2.parse(data)
                    lat_dir = msg.lat_dir
                    latitude = msg.latitude  # 緯度
                    longitude = msg.longitude  # 経度
                    lon_dir = msg.lon_dir
                    altitude = msg.altitude  # 高度
                    hdop = msg.horizontal_dil  # 水平精度 (HDOP)
                    time = msg.timestamp  # 時刻
                    time = datetime.combine(datetime.today().date(), time)
                    print("GPStime="+time)                
                    
            except:#切断されたときに呼ばれる
                self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert("Disconected"+":[GPSdevice]")
                self.setDeviceDisconected()
            
        #self.sleep()
    
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)

class SpeedClass():
    before=0
    now=0
    def get_diff(self):
        return self.now-self.before
    def __init__(self) -> None:
        pass

class moveTEST(AsyncedClass):
    Az_prog=0
    El_Prog=0
    Azreal=90
    Elreal=0
    speed=2
    Az_Calcltor=None

    Az_Speed_calc=SpeedClass()
    El_Speed_calc=SpeedClass()

    bfr_az_diff=0
    bfr_el_diff=0


    def Async(self):
        if self.ACUmonitor.FrontEnd.SELECTED_COM is "TEST":
            az_mode="prog"
            el_mode="prog"
            az_prog=self.Az_prog
            el_prog=self.El_Prog
            ACU_IS_INDI,ACU_IS_SLAVE=self.ACUmonitor.FrontEnd.getMode()
            Allmode="indiv" if ACU_IS_INDI else "slave"
            ELmoveMode="none"
            AZmoveMode="none"
            if ACU_IS_SLAVE:
                EL_IS_STBY,EL_IS_PROG,EL_IS_MAN=self.ACUmonitor.FrontEnd.getElmode()
                ELmoveMode="stby" if EL_IS_STBY else "prog"
                AZ_IS_STBY,AZ_IS_PROG,AZ_IS_MAN=self.ACUmonitor.FrontEnd.getAzmode()
                AZmoveMode="stby" if AZ_IS_STBY else "prog"
                if AZ_IS_PROG:
                    self.Azprog()
                    az_prog=self.Az_prog
                elif AZ_IS_MAN:
                    az_prog=self.Az_prog=self.ACUmonitor.FrontEnd.getAzManualRot()/10000
                if EL_IS_PROG:
                    self.Elprog()
                    el_prog=self.El_Prog
                elif EL_IS_MAN:
                    el_prog=self.El_Prog=self.ACUmonitor.FrontEnd.getElManualRot()/10000
                if AZ_IS_STBY or AZ_IS_MAN:
                    az_mode="manu"
                if EL_IS_STBY or EL_IS_MAN:
                    el_mode="manu"
            elif ACU_IS_INDI:
                az_prog=0
                el_prog=0
            start_monitor1 = time.perf_counter()
            self.Az_Speed_calc.before=self.Azreal
            self.El_Speed_calc.before=self.Elreal
            
            self.setAz(mode=Allmode,moveMode=AZmoveMode)
            self.setEl(mode=Allmode,moveMode=ELmoveMode)
            start_monitor2 = time.perf_counter()
            work_time=start_monitor2-start_monitor1
            self.Az_Speed_calc.now=self.Azreal
            self.El_Speed_calc.now=self.Elreal



            self.ACUmonitor.FrontEnd.LCU.updateEl_num(pnum=el_prog,nnum=self.Elreal,work_time=work_time,speed=self.El_Speed_calc.get_diff(),mode=el_mode)
            self.ACUmonitor.FrontEnd.LCU.updateAz_num(pnum=az_prog,nnum=self.Azreal,work_time=work_time,speed=self.Az_Speed_calc.get_diff(),mode=az_mode)
        self.sleep()
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        self.Az_Calcltor=RadDiffCalc()
        super().__init__(acu)
    def Azprog(self):
        self.Az_prog+=(self.speed*self.sleepTime)
        self.Az_prog%=360
    def Elprog(self):
        self.El_Prog+=(self.speed*self.sleepTime)
        self.El_Prog%=90
    def setAz(self,mode="slave",moveMode="prog"):
        if moveMode=="stby":
            self.Azreal=self.Azreal
        if mode=="slave" and moveMode!="stby":
            diff=self.Az_Calcltor.CalcDiff(Start=self.Azreal,Goal=self.Az_prog)
            if diff<0:
                self.Azreal-=(self.speed*self.sleepTime)
            elif diff>0:
                self.Azreal+=(self.speed*self.sleepTime)
            if diff<=(self.speed*self.sleepTime) and self.bfr_az_diff>=(self.speed*self.sleepTime):
                self.Azreal=self.Az_prog
            self.bfr_az_diff=self.Azreal
        elif mode=="indiv":
            self.Azreal+=(self.speed*self.sleepTime)
            self.Azreal%=360
    def setEl(self,mode="slave",moveMode="prog"):
        if moveMode=="stby":
            self.Elreal=self.Elreal
        if mode=="slave" and moveMode!="stby":
            diff=self.El_Prog-self.Elreal
            if diff<0:
                self.Elreal-=(self.speed*self.sleepTime)
            elif diff>0:
                self.Elreal+=(self.speed*self.sleepTime)
            if diff<=(self.speed*self.sleepTime) and self.bfr_el_diff>=(self.speed*self.sleepTime):
                self.Elreal=self.El_Prog
            self.bfr_az_diff=self.Azreal
        elif mode=="indiv":
            self.Elreal+=(self.speed*self.sleepTime)
            self.Elreal%=90

class serialComunicator(AsyncedClass):
    none="none"
    enable="enable"
    conected="conected"
    disconected="disconected"
    notconect="notconect"
    unkowm="unkowm"

    selected_com=none
    selected_com_stats=none
    stats=disconected

    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)
    
    def set_Stats(self,stats="unkowm",com="?"):
        if stats==self.notconect:
            print("set notconect")
            self.selected_com=self.none
            self.selected_com_stats=self.none
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM_STATS=False
            self.ACUmonitor.FrontEnd.DISCONECT_BUTTOM.setDisable()
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM.setNormal()
            self.ACUmonitor.FrontEnd.COM_F.setNormal()
            self.ACUmonitor.FrontEnd.UPDATE_COM_BUTTOM.setNormal()
        if stats==self.disconected:
            print("set disconected")
            self.setdisconnect()
            self.selected_com_stats=self.disconected
            self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert(stats+"["+self.selected_com+"]")
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM_STATS=False
            self.ACUmonitor.FrontEnd.DISCONECT_BUTTOM.setDisable()
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM.setNormal()
            self.ACUmonitor.FrontEnd.COM_F.setNormal()
            self.ACUmonitor.FrontEnd.UPDATE_COM_BUTTOM.setNormal()
        if stats==self.conected:
            print("set conected")
            self.selected_com=com
            self.selected_com_stats=self.conected
            self.ACUmonitor.FrontEnd.LCU.Commad_Line.Insert(stats+"["+self.selected_com+"]")
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM_STATS=False
            self.ACUmonitor.FrontEnd.DISCONECT_BUTTOM.setNormal()
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM.setDisable()
            self.ACUmonitor.FrontEnd.COM_F.setDisable()
            self.ACUmonitor.FrontEnd.UPDATE_COM_BUTTOM.setDisable()
        
    def get_STATS(self):
        if self.selected_com==self.none and self.selected_com_stats==self.none and self.ACUmonitor.FrontEnd.CONECT_BUTTOM_STATS:
            return self.notconect
        if self.selected_com!=self.none and self.selected_com_stats==self.conected:
            return self.conected
        if self.selected_com!=self.none and (self.selected_com_stats==self.none or self.selected_com_stats==self.disconected):
            return self.disconected
        return self.unkowm
        
    def StartSerial(self,PORT="COM4",baud_rate=9600,time_out=0.5,byte_size=serial.EIGHTBITS,stop_bits = serial.STOPBITS_ONE,PARITY=serial.PARITY_NONE):
        try:
            self.Serial=serial.Serial(port=PORT, baudrate=baud_rate, timeout=time_out,bytesize=byte_size,stopbits = stop_bits,parity=PARITY)
            print("Serialcommunicator:"+"シリアルポートを開きました:"+PORT)
            self.set_Stats(stats=self.conected,com=PORT)
        except:
            self.ACUmonitor.FrontEnd.CONECT_BUTTOM_STATS=False
            self.set_Stats(stats=self.notconect)
            print("Serialcommunicator:"+"シリアルポートが開けませんでした:"+PORT)
            #"pass


    def setdisconnect(self):
        self.Serial.close()
        self.Serial=None
        
    def test(self):
        print("Hello")

    def Async(self):
        stats=self.get_STATS()
        if stats==self.notconect:
            self.StartSerial(PORT=self.ACUmonitor.FrontEnd.COM_F.directBody.get())
        if stats==self.conected:
            try:
                self.communicater()
            except:
                self.ACUmonitor.FrontEnd.CONECT_BUTTOM_STATS=False
                self.set_Stats(stats=self.disconected)
                pass
        if self.ACUmonitor.FrontEnd.DISCONECT_BUTTOM_STATS:
            self.ACUmonitor.FrontEnd.DISCONECT_BUTTOM_STATS=False
            print("self.ACUmonitor.FrontEnd.DISCONECT_BUTTOM_STATS=False")
            self.set_Stats(stats=self.disconected)
        if stats==self.disconected:
            self.set_Stats(stats=self.notconect)
            
        
        self.sleep()
        #stats=self.get_STATS()
        """

        """
            


    def communicater(self):
        print("ASYNC_COM_TEST")
    
    

    

    



        
        

class SerialCommunicator2(AsyncedClass):
    T=0.1
    st="None"
    Serial=None
    Inited=True
    before_com=""
    now_com=""
    def Async(self):
        self.now_com=self.ACUmonitor.FrontEnd.COM_F.combbox.get()
        if self.now_com!=self.before_com:
            print("CHANGED!"+self.now_com+"B:"+self.before_com)
            self.Inited=True
        if self.ACUmonitor.FrontEnd.COM_F.combbox.get()!="Disconected" and self.Inited:
            self.Inited=False
            print(self.now_com)
            self.init_port(PORT=self.ACUmonitor.FrontEnd.COM_F.combbox.get())
            #self.comunication=Serialcommunicator(PORT=self.ACUmonitor.FrontEnd.COM_F.combbox.get())
        self.before_com=self.now_com

        self.sleep(self.T)
    def __init__(self,acu=None,tim=0.1,St="Its'Me!"):
        self.T=tim
        self.st=St
        super().__init__(acu)
    def init_port(self,acu=None,PORT="COM4",baud_rate=9600,time_out=0.5,byte_size=serial.EIGHTBITS,stop_bits = serial.STOPBITS_ONE,PARITY=serial.PARITY_NONE):
        try:
            self.Serial=serial.Serial(port=PORT, baudrate=baud_rate, timeout=time_out,bytesize=byte_size,stopbits = stop_bits,parity=PARITY)
        except:
            print("Serialcommunicator:"+"シリアルポートが開けませんでした:"+PORT)
            self.setError2Conbobox()
            #raise EnvironmentError('Unsupported platform')
            pass
        try:
            commands = [ 0xB6, 0x01, 0x02, 0x00 ]
            for cmd in commands:
                data = struct.pack("B", cmd)
                print("tx: ", data)
                self.Serial.write(data)
        except:
            print("Serialcommunicator:"+"シリアルポートへの書き込みが失敗しました")
            self.setError2Conbobox()
            #raise EnvironmentError('Unsupported platform')
            pass
        self.Serial.flush()
        rx = self.Serial.read_all()
        print(rx)
        print("シリアルポートの接続に成功しました!")
        self.setenable2Conbobox()
        self.Serial.close()
        self.Serial=None
    def SerialWrite(self):
        if self.Serial is not None:
            code="@0BAU W9600<cr><lf>"#ACUをセットアップするためのコマンドです
            ASCII=code.encode('ascii')#上記のコマンドをアスキーに変換しています pythonではByte型にこの時点でなっています
            print(ASCII)
            try:
                self.Serial.write(ASCII)
            except:
                self.setError2Conbobox()
                print("書き込みに失敗しました")
            self.setenable2Conbobox()
    def SerialInput(self):
        if self.Serial is not None:
            self.setenable2Conbobox()
            try:
                line=self.Serial.read_all()
            except:
                self.setError2Conbobox()
                print("読み込みに失敗しました")
            s=str(line)
            print("Input:"+s)
    def closeSrialPort(self):
        if self.Serial is not None:
            self.Serial.close()
    def setError2Conbobox(self):
        self.ACUmonitor.FrontEnd.COM_STATS_F.label.configure(text=self.ACUmonitor.FrontEnd.COM_F.combbox.get()+"is Not Support!",fg_color="red")
        self.ACUmonitor.FrontEnd.COM_F.combbox.configure(fg_color="red")
    def setenable2Conbobox(self):
        self.ACUmonitor.FrontEnd.COM_STATS_F.label.configure(text=self.ACUmonitor.FrontEnd.COM_F.combbox.get()+"is Support!",fg_color="blue")
        self.ACUmonitor.FrontEnd.COM_F.combbox.configure(fg_color="#3B8ED0")

class PRINT():
    def Async(self):
        time.sleep(0.1)
        print("せいこうだ!")

class Async(threading.Thread):
    FuncClass=None
    Func=None
    def __init__(self,funcClass=None,func=None):
        super().__init__()
        if funcClass is not None:
            self.FuncClass=funcClass
        if func is not None:
            self.Func=func
        self.started = threading.Event()
        self.alive = True
        self.start()

    def __del__(self):
        self.kill()

    def begin(self):
        print("begin_ASYNC")
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nend")

    def kill(self):
        self.alive = False
        print("ASYNC_KILLED")
        self.started.set()
        self.join()

    def run(self):
        while self.alive:
            if self.FuncClass is not None and self.alive:
                try:
                    self.FuncClass.Async()
                except:
                    print("同期するクラスに、Async()と名前付けされている関数がありません,もしくはそれ以外のエラーが起きています")
                    import traceback
                    traceback.print_exc()
                    self.kill()
            if self.Func is not None and self.alive:
                self.Func()


