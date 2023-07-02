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

Year_Time="1969/7/29"
JSTformat="???"
UTCformat="???"
LSTformat="???"

@staticmethod
def getLocalTime():
    return datetime.datetime.now()

def updateAllTime():
    allTime=getLocalTime()
    setYearFormat(allTime)
    jst=getJST(allTime)
    setJSTFormat(jst)
    setUTCFormat(allTime)
    setLSTFormat(jst)

def setYearFormat(dt):
    global Year_Time
    Year_Time=(str(dt.year)+"."+str(dt.month)+"."+str(dt.day))
    
def getJST(_now):
    JST = dateutil.parser.parse(
        '{_now} TZ'.format(**locals()), 
        tzinfos = {'TZ': dateutil.tz.gettz('Asia/Tokyo')},
    )
    return JST
    
def setJSTFormat(JST):
    global JSTformat
    JSTformat="JST:"+getTime(str(JST))
    
def setUTCFormat(_now):
    global UTCformat
    UTC = dateutil.parser.parse(
        '{_now} TZ'.format(**locals()), 
        tzinfos = {'TZ': dateutil.tz.gettz('UTC')},
    )
    UTCformat="UTC:"+getTime(str(UTC))
    
def setLSTFormat(datetime_):
    global LSTformat
    location=astropy.coordinates.EarthLocation(
        lon = (138 + 28/60 + 21.2/3600) * deg,
        lat = (35 + 56/60 + 40.9/3600)  * deg,
        height = 1350 * m,
    )
    localtime = astropy.time.Time(datetime_, format='datetime', location=location)
    lst=localtime.sidereal_time('apparent')
    lst_h = int(lst.hour)
    lst_m = int((lst.hour - lst_h) * 60)
    lst_s = int((lst.hour - lst_h - lst_m/60) * 3600)
    lst_ = '{lst_h:02d}:{lst_m:02d}:{lst_s:02d}'.format(**locals())
    msg = '{lst_}'.format(**locals())
    LSTformat="LST:"+msg
    
    
def getTime(timezone):
    '''
    JST,UTCの時間の正規化を行う
    '''
    num=timezone.find(":")
    return timezone[num-2:num+6]
    

def getYearFormat():
    dt=getLocalTime()
    return (str(dt.year)+"."+str(dt.month)+"."+str(dt.day))

