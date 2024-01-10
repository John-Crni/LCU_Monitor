def sbca_to_angle(sbca_value, bit_count=16, resolution=90.0):
    """
    Convert SBCA formatted value to angle.

    Parameters:
    - sbca_value: SBCA formatted value as an integer.
    - bit_count: Number of bits used for SBCA representation.
    - resolution: Maximum angle represented by the SBCA format.

    Returns:
    - Angle in degrees.
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
        

# Convert decimal value to angle using the sbca_to_angle function
angle_result = sbca_to_angle("1000")
print( 2 ** 16 - 1)

print(f"Angle: {normNum(str(angle_result))} degrees")

