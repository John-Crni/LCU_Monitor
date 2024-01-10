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

'''
class GIFManager(AsyncedClass):
    _please_stop = False
    path = path
    label = label
    duration = []  # フレーム表示間隔
    frames = []  # 読み込んだGIFの画像フレーム
    last_frame_index = None
    
    def Async(self):

        self.sleep()
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        if isinstance(self.path, str):
            img = Image.open(self.path)
            frames = []
        frame_index = 0
        super().__init__(acu)
    def load_frames1(self):
        try:
            while True:
                frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(frame_index)
                frame_index += 1
        except EOFError:
            self.frames = frames
            self.last_frame_index = frame_index - 1
'''

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
        if not self.getDeviceConectStats():
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
        if self.isDeviceConected and not self.getConectStats():
            try:
                if isinstance(self.Serial,serial.Serial):
                    self.Serial.close()
                    self.Serial=None
                self.setText2CommandLine(text="TryConect")
                self.Serial=serial.Serial(self.Port, self.Baudrate)
            except (OSError, serial.SerialException):#切断されたときに呼ばれる
                self.setFaild2Conect()
            except:
                if isinstance(self.Serial,serial.Serial):
                    self.setText2CommandLine(text="ProgExept!")
                pass
            else:
                self.setSuccces2Conect()
                self.Succces2ConectFunc()
        if self.getConectStats():
            try:
                self.SerialFunc()
            except (OSError, serial.SerialException):#切断されたときに呼ばれる
                self.setDeviceDisconected()
                self.disConectFunc()
            except:
                if isinstance(self.Serial,serial.Serial):
                    self.setText2CommandLine(text="ProgExept!")
                pass
            
            
        self.sleep()

    def SerialFunc(self):
        pass
    
    def __init__(self,acu=None,sleepT=0.1,message="Serialcommunicator4GeneralUse",ma=None,deviceName="none",deviceType="none"):
        self.deviceName=deviceName
        self.deviceType=deviceType
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)
        
class decodeDatafromAcu():
    
    def POSdata(self,data):
        pass
        
    
    
class AnntenaController(Serialcommunicator4GeneralUse):
    
    ACUmodeManager=None
    
    setUped=False
    
    ElevationAngle=0
    
    AzimuthAngle=0
    
    timeScale=None
    
    planets=None
    Site=None
    Earth=None
    TimeScale=None
    
    ReceivedData=None
    
    #----
    
    TRAP=False
    
    #----
    
    
    def Succces2ConectFunc(self):
        super(AnntenaController,self).Succces2ConectFunc()
        self.ACUmonitor.FrontEnd.Setconect2Antenna()
        
    def disconectSerial(self):#Setnotconect2Antenna
        super(AnntenaController,self).disconectSerial()
        self.ACUmonitor.FrontEnd.Setnotconect2Antenna()
        self.setUped=False
        
    def TryReadAnttenaPosition(self):#@8POS R2<cr><lf> read axes position A and B
        if self.TRAP is False:
            self.SerialWrite("@8POS R2<cr><lf>")
            self.TRAP=true
        if self.TRAP:
            pass
            
    def SerialWrite(self,code="@0BAU W9600<cr><lf>"):
        if self.Serial is not None:
            ASCII=code.encode('ascii')#上記のコマンドをアスキーに変換しています pythonではByte型にこの時点でなっています
            self.Serial.write(ASCII)
            
    def calculateAngles(self):
        ra=None
        dec=None
        if self.ACUmodeManager.getRaDecMode:#Ra,Decの場合
            ra,dec=self.ACUmodeManager.getRaDecValue
            pass
        else:#星の名前
            pass
            
    
    def setUpAntenna(self):
        if not self.setUped:
            #self.timeScale=load.timescale(builtin=True)
            pass
        else:
            pass
    
    def setAzRot2Anttena(self,rot=0):
        pass
    
    def setElRot2Anttena(self,rot=0):
        pass
    
    def convertRot2Text(self,rot=0):
        pass
    
    def convertText2Rot(self,text="0"):
        pass
    
    def convertDeg2Hex(self,angle):
        '''
        this is used to angle to sbca hex
        '''
        fixint=int(angle/0.005493164)
        return hex(fixint)
    
    def normNum(num,ren=2,value="9",normround=5):
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
    
    def convertHex2Deg(sbca_value, bit_count=16, resolution=90.0):
        """
        Convert SBCA formatted value to angle.
        """
        hex_number = sbca_value  # 16進数として扱う文字列
        decimal_value = int(hex_number, 16)
        binary_number = bin(int(hex_number, 16))[2:].zfill(len(hex_number) * 4)  # 16進数を10進数に変換し、その後2進数に変換して0埋め
        if binary_number[0]=="1":
            decimal_value=(1 << (len(hex_number) * 4)) - decimal_value
            decimal_value*=-1
        normalized_value = decimal_value / 65535  # Normalize to [0, 1]
        angle = normalized_value * resolution
        return angle
    
    def updateAzEL(self):
        Altaz=None
        t=self.TimeScale.now()+timedelta(milliseconds=130) 
        if self.ACUmodeManager.getRaDecMode():#True=Ra,Dec
            ra, dec=self.ACUmodeManager.getRaDecValue()
            star = Star(ra_hours=ra,dec_degrees=dec)
            astrometric = self.Site.at(t).observe(star)
            apparent = astrometric.apparent()
            Altaz = apparent.altaz()
        else:
            planet=planets[self.ACUmodeManager.getRaDecValue()]  
            astrometric = self.Earth.at(t).observe(planet)
            apparent = astrometric.apparent()
            Altaz = apparent.altaz()



    '''
        def Succces2ConectFunc(self):#接続が初めてできた時に呼ばれる
            pass
        
        def disConectFunc(self):#接続が着れた時に呼ばれる
            pass
    '''
    

    def SerialFunc(self):
        super(AnntenaController,self).SerialFunc()
        self.setUpAntenna()
        self.ReceivedData = self.Serial.readline().decode('utf-8') #or ascii
        if self.setUped:
            if self.ACUmodeManager.getControllMode:#SLAVE_MODE
                #ここで0.1秒ごとの計算を行う
                if self.ACUmodeManager.getAzMode:#True=Prog
                    pass
                elif self.ACUmodeManager.getAzMode is False:#False=Manual
                    pass
                else: #None=Stanby
                    pass
                
                if self.ACUmodeManager.getElMode:#True=Prog
                    pass
                elif self.ACUmodeManager.getElMode is False:#False=Manual
                    pass
                else: #None=Stanby
                    pass
                
            else:
                pass
        
        
    def __init__(self,acu=None,sleepT=0.1,message="Serialcommunicator4GeneralUse",ma=None,deviceName="none",deviceType="none"):
        super().__init__(acu=acu,sleepT=sleepT,message=message,ma=ma,deviceName=deviceName,deviceType=deviceType)
        self.ACUmodeManager=ACUmonitorModeManager(acu=self.ACUmonitor)
        self.planets = load('de421.bsp')
        self.Earth=self.planets['earth']
        self.Site=self.Earth+wgs84.latlon(45, 5)
        self.TimeScale=load.timescale(builtin=True)


class ACUmonitorModeManager():

    IS_SLAVE_MODE=False
    IS_INDIVISUAL_MODE=True

    STOW_IS_POS=False
    STOW_IS_REL=False
    STOW_IS_LOCK=True

    AZ_IS_STBY=False
    AZ_IS_PROG=True
    AZ_IS_MAN=False

    EL_IS_STBY=False
    EL_IS_PROG=True
    EL_IS_MAN=False
    
    IS_USE_RADEC=True
    IS_USE_STARNAME=False
    
    ACU=None
    
    def update(self):
        self.IS_SLAVE_MODE,self.IS_INDIVISUAL_MODE,self.STOW_IS_POS,self.STOW_IS_REL,self.STOW_IS_LOCK,self.AZ_IS_STBY,self.AZ_IS_PROG,self.AZ_IS_MAN,self.EL_IS_STBY,self.EL_IS_PROG,self.EL_IS_MAN=self.ACU.FrontEnd.getStats()
    
    def getControllMode(self):#True=SLAVE,False=INDIVISUAL
        return self.IS_SLAVE_MODE
    
    def getAzMode(self):#True=Prog,False=Manu,None=Stby
        re=None
        if self.AZ_IS_PROG:
            re=true
        elif self.AZ_IS_MAN:
            re=False
        return re
    
    def getElMode(self):#True=Prog,False=Manu,None=Stby
        re=None
        if self.EL_IS_PROG:
            re=true
        elif self.EL_IS_MAN:
            re=False
        return re
    
    def getRaDecMode(self):#True=Ra,Dec,False=StarName
        return self.IS_USE_RADEC
    
    def getRaDecValue(self):#Ra,Dec is [ra],[dec],Starmode="mars"
        pass
        
    
    def __init__(self,acu=None):
        self.ACU=acu
        pass

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
            if self.Func is not None and self.alive:
                self.Func()


