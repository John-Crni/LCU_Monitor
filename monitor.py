from tkinter import *
import datetime
from dateutil import tz
import pytz
import time

import dateutil
import dateutil.rrule
import astropy.coordinates
import astropy.time

from astropy.units import deg
from astropy.units import m

def calc_lst(location, datetime_):
    localtime = astropy.time.Time(datetime_, format='datetime', location=location)
    return localtime.sidereal_time('apparent')

def daily_timeseries(date, timezone, interval):
    tzdate = dateutil.parser.parse(
        '{date} 00:00:00 TZ'.format(**locals()), 
        tzinfos = {'TZ': dateutil.tz.gettz(timezone)},
    )

    series = list(dateutil.rrule.rrule(
        freq = dateutil.rrule.MINUTELY, 
        interval = interval, 
        dtstart = tzdate,
        until = tzdate + dateutil.relativedelta.relativedelta(hours=+24),
    ))

    return series[:-1]


def daily_lst(location, date, timezone, interval=10):
    timeseriese = daily_timeseries(date, timezone, interval)
    lst = calc_lst(location, timeseriese)
    return timeseriese, lst

def print_lst(location, date, timezone, interval=10):
    localtime, lst = daily_lst(location, date, timezone, interval)

    sep = '-'*18
    print('{date} ({timezone})'.format(**locals()))
    print()
    print('Time    --    LST')
    hour0 = None
    for _lt, _lst in zip(localtime, lst):
        _lt_ = _lt.strftime('%H:%M')
        _lst_h = int(_lst.hour)
        _lst_m = int((_lst.hour - _lst_h) * 60)
        _lst_ = '{_lst_h:02d}:{_lst_m:02d}'.format(**locals())

        if hour0 != _lst_h:
            print(sep)
            hour0 = _lst_h
            pass

        print('{_lt_}  --  {_lst_}'.format(**locals()))
        continue

def click_btn_2a():
    button_2a['text'] = 'クリックしました'

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

    

dt = datetime.datetime.now()
JST=datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
UTC=datetime.datetime.now(pytz.timezone('UTC'))
year_date=str(dt.year)+"."+str(dt.month)+"."+str(dt.day)
JST_S="JST:"+getTime(str(JST))
UTC_S="UTC:"+getTime(str(UTC))

    
root = Tk() # この下に画面構成を記述
    
# ----------- ①Window作成 ----------- #
root.title('tkinterの使い方')   # 画面タイトル設定
root.geometry('1250x750')       # 画面サイズ設定
root.resizable(False, False)   # リサイズ不可に設定
    
# ----------- ②Frameを定義 ----------- #
JST_YD_F = Frame(root, width=250, height=50, borderwidth=2, relief='solid')
JST_Time_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
UTC_Time_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')
LST_Time_F = Frame(root, width=325, height=50, borderwidth=2, relief='solid')

# Frameサイズを固定
JST_YD_F.propagate(False)
JST_Time_F.propagate(False)
UTC_Time_F.propagate(False)
LST_Time_F.propagate(False)


# Frameを配置（grid）
JST_YD_F.grid(row=0, column=0)
JST_Time_F.grid(row=0, column=1)
UTC_Time_F.grid(row=0, column=2)
LST_Time_F.grid(row=0, column=3)
    
# JST_YEAR_DATE label(フレーム1左上)
label_1a = Label(JST_YD_F, text=year_date, font=('System', 30,"bold"))
label_1a.pack(padx=5, pady=10)
    
# JST_TIME label(フレーム1左上)
JST_Lb = Label(JST_Time_F, text=JST_S, font=('System', 30,"bold"))
JST_Lb.pack(padx=5, pady=10)
JST_Lb.after(1000, updateJST)

# JST_TIME label(フレーム1左上)
UTC_Lb = Label(UTC_Time_F, text=UTC_S, font=('System', 30,"bold"))
UTC_Lb.pack(padx=5, pady=10)
UTC_Lb.after(1000, updateUCT)


    

root.mainloop()


