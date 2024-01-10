from skyfield.api import Topos, load, EarthSatellite,position_of_radec,wgs84,Star,Angle
from datetime import datetime, timedelta, timezone


ts = load.timescale(builtin=True)
TTT = ts.now()+ timedelta(seconds=50)      

test=wgs84.latlon(45, 5)

print(str(TTT.utc.hour)+":"+str(TTT.utc.minute)+":"+str(TTT.utc.second))                

print(None is False)  

# 時、分、秒の成分
hours = 15
minutes = 9
seconds = 54.25

# 時間を度に変換
hours_in_degrees = hours * 15  # 1時間は15度

# 分を度に変換
minutes_in_degrees = minutes * 0.25  # 1分は0.25度

# 秒を度に変換
seconds_in_degrees = seconds * (1/240)  # 1秒は1/240度

# 合計を計算
total_degrees = hours_in_degrees + minutes_in_degrees + seconds_in_degrees

# Angleオブジェクトを作成
angle = Angle(degrees=total_degrees)

print(str(angle))
