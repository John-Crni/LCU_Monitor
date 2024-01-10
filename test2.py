from tkinter import filedialog
import unicodedata


def ra_to_degrees(hours, minutes, seconds):
    # 1時間 = 15度
    degrees_per_hour = 15

    # 時間を度に変換
    total_hours = hours + minutes / 60 + seconds / 3600
    degrees = total_hours * degrees_per_hour

    return degrees

# 赤緯を度に変換する関数
def dec_to_degrees(degrees, minutes, seconds, sign):
    # 度数を度に変換
    total_degrees = degrees + minutes / 60 + seconds / 3600

    # 符号を考慮
    if sign.lower() == 's' or sign.lower() == '-':
        total_degrees *= -1

    return total_degrees

def convertData2RaDec(text):
    rightText=(normText.split('='))[1]
    
    

filename = filedialog.askopenfilename(
    title = "座標読み取り",
    filetypes = [("テキストファイルオンリー", ".txt") ], # ファイルフィルタ
    initialdir = "./" # 自分自身のディレクトリ
    )
print(filename)

f = open(filename,'r')

datalist = f.readlines()

f.close()


RaDecData=None
hours=0
minutes=0
seconds=0

degrees=0
minutes=0
seconds=0
sign=""
for data in datalist:#1h 13m 0.0760510177733309,N 24° 1' 2.045871885199233
    normText=data.replace(' ', '')
    normText=unicodedata.normalize('NFKC', normText)
    print(normText.lower())
    if normText.lower().find('ra,dec')>=0:
        RaDecData=(normText.split('='))[1]
        RaDecData=(RaDecData.split(','))
        ra,dec=RaDecData[0],RaDecData[1]
        rahourpos=ra.find('h')
        raminutepos=ra.find('m')
        Rahour=ra[0:rahourpos]
        Raminute=ra[rahourpos+1:raminutepos]
        Raseconds=ra[raminutepos+1:(len(ra)-1)]
        RaDegrees=ra_to_degrees(int(Rahour),int(Raminute),float(Raseconds))
        
        decsign=ra[0]
        decdegreepos=dec.find('#')
        decminutepos=dec.find("'")
        dechour=dec[1:decdegreepos]
        decminute=dec[decdegreepos+1:decminutepos]
        decseconds=dec[decminutepos+1:(len(dec)-1)]
        decDegrees=dec_to_degrees(int(dechour), int(decminute), float(decseconds), decsign)
        RaDecData[0]=RaDegrees
        RaDecData[1]=decDegrees
        break
    

print(RaDecData)

# テキスト読み込みなどの処理文


