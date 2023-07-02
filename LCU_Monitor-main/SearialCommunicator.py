import serial
from serial.tools import list_ports
import threading
import random
import time
import pyvisa
import ctypes


ser = serial.Serial(port="COM3", baudrate=9600, timeout=0.5,bytesize=serial.EIGHTBITS,stopbits = serial.STOPBITS_ONE,parity=serial.PARITY_NONE)
#↑シリアル通信の設定を行っています(左から、I/Oポートの設定、ボーレートの設定、タイムアウトの設定、バイトサイズの設定、ストップビットの設定、優先度の設定を行っています)
data=open("datas.txt",'w')
#↑出力データを書き込むためのファイルを読み込んでいます
end=True

def outPut():#0.2秒おきにACUへ信号を出力しています (なぜ0.2秒ごとの理由は特にありません)
    while True:
        code="@0BAU W9600<cr><lf>"#ACUをセットアップするためのコマンドです
        ASCII=code.encode('ascii')#上記のコマンドをアスキーに変換しています pythonではByte型にこの時点でなっています
        ser.write(ASCII) #アスキーに変換したコマンドを送信しています
        time.sleep(0.2)
    
def inPut():#0.1秒おきに信号を受信しています (なぜ0.1秒ごとの理由は特にありません)
    while end: 
        time.sleep(0.1)
        line=ser.read_all()
        s=str(line)
        data.write("\n")
        data.write(s)




def main():#ここでは、上記の(OutPut,input関数)をスレッドリングを利用して、並列処理させています
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

    

if __name__ == '__main__':
    main()



