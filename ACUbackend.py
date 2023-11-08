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
 
        result = ["COM2"]
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
        
    
    def ComTest(self):
        ser = serial.Serial(port="COM1", baudrate=9600, timeout=0.5,bytesize=serial.EIGHTBITS,stopbits = serial.STOPBITS_ONE,parity=serial.PARITY_NONE)
        commands = [ 0xB6, 0x01, 0x02, 0x00 ]
        for cmd in commands:
            data = struct.pack("B", cmd)
            print("tx: ", data)
            ser.write(data)
        ser.flush()
        rx = ser.readline()
        print("rx: ", rx)
        ser.close()

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
    def __init__(self,ACU=None):
        self.ACUmonitor=ACU
        if self.ACUmonitor is not None:
            self.isACUenable=True
            print(self.__class__.__name__+"ACU OK!")
    def sleep(self,TIME=0.1):
        if TIME>0:
            time.sleep(float(TIME))
        
class Serialcommunicator(AsyncedClass):
    Serial=None
    RoopBackCom= [ 0xB6, 0x01, 0x02, 0x00 ]
    RoopBackExpected=b'\xb6\x01\x02\x00'
    InputAsync=None
    OutPutAsync=None
    def Async(self):
        print("ASYNC!")
        self.sleep()
    def __init__(self,acu=None,PORT="COM1",baud_rate=9600,time_out=0.5,byte_size=serial.EIGHTBITS,stop_bits = serial.STOPBITS_ONE,PARITY=serial.PARITY_NONE):
        super().__init__(acu)
        
        print("self")
        '''
        self.Serial=serial.Serial(port=PORT, baudrate=baud_rate, timeout=time_out,bytesize=byte_size,stopbits = stop_bits,parity=PARITY)
        for cmd in commands:
            data = struct.pack("B", cmd)
            print("tx: ", data)
            ser.write(data)
        ser.flush()
        rx = ser.readline()
        print("rx: ", rx)
        ser.close()
        '''

class comMonitor(AsyncedClass):
    def Async(self):
        print(self.ACUmonitor.FrontEnd.COM_F.combbox.get())
        self.sleep()
    def __init__(self,acu=None):
        super().__init__(acu)

        
    

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
                    print("同期するクラスに、Async()と名前付けされている関数がありません")
            if self.Func is not None and self.alive:
                self.Func()
