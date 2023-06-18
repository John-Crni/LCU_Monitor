from tkinter import *
import datetime
from dateutil import tz
import pytz
import time
import sys
import dateutil
import dateutil.parser
import astropy.coordinates
from astropy.units import deg
from astropy.units import m

def calc_lst(location, datetime_):
    localtime = astropy.time.Time(datetime_, format='datetime', location=location)
    return localtime.sidereal_time('apparent')

def now(timezone):
    _now = datetime.datetime.now()
    tzdate = dateutil.parser.parse(
        '{_now} TZ'.format(**locals()), 
        tzinfos = {'TZ': dateutil.tz.gettz(timezone)},
    )
    return tzdate

def getLST():
    location=astropy.coordinates.EarthLocation(
        lon = (138 + 28/60 + 21.2/3600) * deg,
        lat = (35 + 56/60 + 40.9/3600)  * deg,
        height = 1350 * m,
    )
    localtime = now('Asia/Tokyo')
    lst = calc_lst(location, localtime)
    lst_h = int(lst.hour)
    lst_m = int((lst.hour - lst_h) * 60)
    lst_s = int((lst.hour - lst_h - lst_m/60) * 3600)
    lst_ = '{lst_h:02d}:{lst_m:02d}:{lst_s:02d}'.format(**locals())
    msg = '{lst_}'.format(**locals())
    return msg

def getTime(timezone):
    '''
    JST,UTCの時間の正規化を行う
    '''
    num=timezone.find(":")
    return timezone[num-2:num+6]

def updateJST():
    JST=datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    JST_S="JST:"+getTime(str(JST))
    # ラベルのテキストを更新
    JST_Lb.config(text=JST_S)
    # 1000msごとに再度tick関数を呼び出す
    JST_Lb.after(1000, updateJST)
    
def updateUCT():
    UTC=datetime.datetime.now(pytz.timezone('UTC'))
    UTC_S="UTC:"+getTime(str(UTC))
    # ラベルのテキストを更新
    UTC_Lb.config(text=UTC_S)
    # 1000msごとに再度tick関数を呼び出す
    UTC_Lb.after(1000, updateUCT)
    
def updateLST():
    LST_S="LST:"+getLST()
    # ラベルのテキストを更新
    LST_Lb.config(text=LST_S)
    # 1000msごとに再度tick関数を呼び出す
    LST_Lb.after(1000, updateLST)

    

dt = datetime.datetime.now()
JST=datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
UTC=datetime.datetime.now(pytz.timezone('UTC'))
year_date=str(dt.year)+"."+str(dt.month)+"."+str(dt.day)
JST_S="JST:"+getTime(str(JST))
UTC_S="UTC:"+getTime(str(UTC))
LST_S="LST:"+getLST()


    
root = Tk() # この下に画面構成を記述
    
# ----------- ①Window作成 ----------- #
root.title('LCU_CONTROLLER')   # 画面タイトル設定
root.geometry('1250x750')       # 画面サイズ設定
root.resizable(False, False)   # リサイズ不可に設定
    
# ----------- ②Frameを定義 ----------- #
JST_YD_F = Frame(root, width=250, height=50, borderwidth=2, relief='solid')
JST_Time_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
UTC_Time_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
LST_Time_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
AZ_F = Frame(root, width=80, height=30, borderwidth=2, relief='solid')
EL_F = Frame(root, width=80, height=30, borderwidth=2, relief='solid')
REAL_F = Frame(root, width=100, height=50, borderwidth=2, relief='solid')
REAL_AZ_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
REAL_EL_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
PROG_F = Frame(root, width=100, height=50, borderwidth=2, relief='solid')
PROG_AZ_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
PROG_EL_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
RP_DIFF_F = Frame(root, width=100, height=50, borderwidth=2, relief='solid')
RP_DIFF_AZ_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
RP_DIFF_EL_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
#SPEED----------------------------------------------------------------------
SPEED_F = Frame(root, width=100, height=50, borderwidth=2, relief='solid')
SPEED_AZ_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
SPEED_EL_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
#STOW----------------------------------------------------------------------
STOW_F = Frame(root, width=100, height=50, borderwidth=2, relief='solid')
STOW_AZ_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
STOW_EL_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
#LIMIT----------------------------------------------------------------------
LIMIT_F = Frame(root, width=100, height=50, borderwidth=2, relief='solid')
LIMIT_AZ_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
LIMIT_EL_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')


# Frameサイズを固定
JST_YD_F.propagate(False)
JST_Time_F.propagate(False)
UTC_Time_F.propagate(False)
LST_Time_F.propagate(False)
AZ_F.propagate(False)
EL_F.propagate(False)
REAL_F.propagate(False)
REAL_AZ_F.propagate(False)
REAL_EL_F.propagate(False)
PROG_F.propagate(False)
PROG_AZ_F.propagate(False)
PROG_EL_F.propagate(False)
RP_DIFF_F.propagate(False)
RP_DIFF_AZ_F.propagate(False)
RP_DIFF_EL_F.propagate(False)
SPEED_F.propagate(False)
SPEED_AZ_F.propagate(False)
SPEED_EL_F.propagate(False)
STOW_F.propagate(False)
STOW_AZ_F.propagate(False)
STOW_EL_F.propagate(False)
LIMIT_F.propagate(False)
LIMIT_AZ_F.propagate(False)
LIMIT_EL_F.propagate(False)

# Frameを配置（grid）
JST_YD_F.grid(row=0, column=0)
JST_Time_F.grid(row=0, column=1)
UTC_Time_F.grid(row=0, column=2)
LST_Time_F.grid(row=0, column=3)
AZ_F.grid(row=1, column=1, columnspan=1)
EL_F.grid(row=1, column=2)
REAL_F.grid(row=2, column=0)
REAL_AZ_F.grid(row=2, column=1)
REAL_EL_F.grid(row=2, column=2)
PROG_F.grid(row=3, column=0)
PROG_AZ_F.grid(row=3, column=1)
PROG_EL_F.grid(row=3, column=2)
RP_DIFF_F.grid(row=4, column=0)
RP_DIFF_AZ_F.grid(row=4, column=1)
RP_DIFF_EL_F.grid(row=4, column=2)
SPEED_F.grid(row=5, column=0)
SPEED_AZ_F.grid(row=5, column=1)
SPEED_EL_F.grid(row=5, column=2)
STOW_F.grid(row=6, column=0)
STOW_AZ_F.grid(row=6, column=1)
STOW_EL_F.grid(row=6, column=2)
LIMIT_F.grid(row=7, column=0)
LIMIT_AZ_F.grid(row=7, column=1)
LIMIT_EL_F.grid(row=7, column=2)
    
# JST_YEAR_DATE label(フレーム1左上)
label_1a = Label(JST_YD_F, text=year_date, font=('System', 30,"bold"))
label_1a.pack(padx=5, pady=10)
    
# JST_TIME label(フレーム2左上)
JST_Lb = Label(JST_Time_F, text=JST_S, font=('System', 30,"bold"))
JST_Lb.pack(padx=5, pady=10)
JST_Lb.after(1000, updateJST)

# JST_TIME label(フレーム3左上)
UTC_Lb = Label(UTC_Time_F, text=UTC_S, font=('System', 30,"bold"))
UTC_Lb.pack(padx=5, pady=10)
UTC_Lb.after(1000, updateUCT)

# LST_TIME label(フレーム4左上)
LST_Lb = Label(LST_Time_F, text=LST_S, font=('System', 30,"bold"))
LST_Lb.pack(padx=5, pady=10)
LST_Lb.after(1000, updateLST)

# AZ label(フレーム4左上)
AZ_Lb = Label(AZ_F, text="AZ", font=('System', 23,"bold"))
AZ_Lb.pack(padx=10, pady=5)

# REAL_AZ label(フレーム4左上)
REAL_AZ_Lb = Label(REAL_AZ_F, text="169.23142", font=('System', 30,"bold"))
REAL_AZ_Lb.pack(padx=10, pady=5)

# REAL_EL label(フレーム4左上)
REAL_EL_Lb = Label(REAL_EL_F, text="90.10308", font=('System', 30,"bold"))
REAL_EL_Lb.pack(padx=10, pady=5)

# EL label(フレーム4左上)
EL_Lb = Label(EL_F, text="EL", font=('System', 23,"bold"))
EL_Lb.pack(padx=10, pady=5)

# REAL label(フレーム4左上)
REAL_Lb = Label(REAL_F, text="REAL", font=('System', 30,"bold"))
REAL_Lb.pack(padx=10, pady=5)

# PROG label(フレーム4左上)
PROG_Lb = Label(PROG_F, text="PROG", font=('System', 30,"bold"))
PROG_Lb.pack(padx=10, pady=5)

# PROG_AZ label(フレーム4左上)
PROG_AZ_Lb = Label(PROG_AZ_F, text="169.23142", font=('System', 30,"bold"))
PROG_AZ_Lb.pack(padx=10, pady=5)

# PROG_EL label(フレーム4左上)
REAL_EL_Lb = Label(PROG_EL_F, text="90.10308", font=('System', 30,"bold"))
REAL_EL_Lb.pack(padx=10, pady=5)

# DIFF label(フレーム4左上)
DIFF_Lb = Label(RP_DIFF_F, text="DIFF", font=('System', 30,"bold"))
DIFF_Lb.pack(padx=10, pady=5)


    

root.mainloop()


