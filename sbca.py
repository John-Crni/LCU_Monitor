def convertDeg2Hex(angle,mode=1):
    '''
    this is used to angle to sbca hex
    '''
    isminus=angle<0
    angle=abs(angle)
    oyabun=0.005493164
    if mode==2:
        oyabun=0.001373291
    fixint=int(angle/oyabun)
    hexvalue=hex(fixint)
    first_digit=0
    if mode==2:
        binary_representation = bin(int(hexvalue, 16))[2:].zfill(16)
        first_digit = binary_representation[0]
        print(hexvalue,",",first_digit)

    if ((isminus and first_digit=="0")or(not isminus and first_digit=="1")) and mode==2:
        print("ISMINUS")
        fixint=int(hexvalue,16)
        fixint=~fixint
        fixint+=65536
        hexvalue=hex(fixint)
        print(hexvalue)
    re=""
    for i in range(2,len(hexvalue)):
        re+=str(hexvalue[i])
    return re

def convertHex2Deg(sbca_value, bit_count=16, resolution=360.0,mode=1):
    """
    Convert SBCA formatted value to angle.
    """
    hex_number = sbca_value  # 16進数として扱う文字列
    decimal_value = int(hex_number, 16)
    binary_number = bin(int(hex_number, 16))[2:].zfill(16)
    print(binary_number)
    if binary_number[0]=="1" and mode==2:
        decimal_value=(1 << (len(hex_number) * 4)) - decimal_value
        decimal_value*=-1
    normalized_value = decimal_value / 65535  # Normalize to [0, 1]
    angle = normalized_value * resolution
    return angle

sbca_value=convertDeg2Hex(0.137,mode=2)
print(convertHex2Deg(sbca_value=sbca_value,resolution=90.0,mode=2))