from skyfield.api import Angle

def hms_string_to_angle(hms_string):
    # 文字列を' '（空白）で分割
    components = hms_string.split()

    # 'h', 'm', 's'を削除して数値に変換
    hours = float(components[0].replace('h', ''))
    minutes = float(components[1].replace('m', ''))
    seconds = float(components[2].replace('s', ''))

    # 時、分、秒を度に変換
    hours_in_degrees = hours * 15  # 1時間は15度
    minutes_in_degrees = minutes * 0.25  # 1分は0.25度
    seconds_in_degrees = seconds * (1/240)  # 1秒は1/240度

    # 合計を計算
    total_degrees = hours_in_degrees + minutes_in_degrees + seconds_in_degrees

    # Angleオブジェクトを作成
    angle = Angle(degrees=total_degrees)

    return angle

# テスト
hms_string = "15h 09m 54.25s"
angle = hms_string_to_angle(hms_string)
print(angle)
