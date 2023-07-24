import sys
import glob
import serial
import threading
import time
import struct
import asyncio

class ACUBackEnd():
    
    ACU_Monitor=None
    
    ASYNC_TEST=None
    
    SelectedCOM=None
    
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
 
        result = ["COM3"]
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
    now_com=""
    before_com=""
    def Async(self):
        self.before_com=self.now_com
        self.now_com=self.ACUmonitor.FrontEnd.COM_F.combbox.get()
        if self.now_com is not "Disconected" and (self.now_com!=self.before_com or self.ACUmonitor.FrontEnd.SELECTED_COM_ENABLE is False):
            try:
                ser = serial.Serial(port=self.now_com, baudrate=9600, timeout=0.5,bytesize=serial.EIGHTBITS,stopbits = serial.STOPBITS_ONE,parity=serial.PARITY_NONE)
                commands = [ 0xB6, 0x01, 0x02, 0x00 ]
                for cmd in commands:
                    data = struct.pack("B", cmd)
                    print("tx: ", data)
                    ser.write(data)
                ser.flush()
                rx = ser.readline()
                print("rx: ", rx)
                ser.close()
                #self.ACUmonitor.FrontEnd.COM_STATS_F.label.configure(text=(self.now_com+" is Enable!"),bg_color="#3B8ED0")
                self.ACUmonitor.FrontEnd.SELECTED_COM=self.now_com
                #self.ACUmonitor.FrontEnd.COM_F.combbox.setDisable()
            except(OSError, serial.SerialException):
                print("SerialError!")
                #self.ACUmonitor.FrontEnd.COM_STATS_F.label.configure(text=(self.now_com+" is Disable!"),bg_color="red")
                pass
        self.sleep()
    def __init__(self,acu=None,sleepT=0.1,message="Its'Me!",ma=None):
        self.sleepTime=sleepT
        self.message=message
        self.master=ma
        super().__init__(acu)
        
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
            if self.Func is not None and self.alive:
                self.Func()
