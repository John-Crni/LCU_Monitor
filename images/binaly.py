
#ascii_string = ' @0<ack><cr> <lf>'

# 各文字のASCIIコードを取得し、16進数に変換してエスケープシーケンスとして連結
#hex_escape_sequence = ''.join([r'\x' + hex(ord(char))[2:] for char in ascii_string])


#print(hex_escape_sequence)

# 16進数のエスケープシーケンスをバイト列に変換
#byte_data = bytes.fromhex(''.join(hex_escape_sequence.split(r'\x')[1:]))

# バイト列を文字列にデコード
#decoded_string = byte_data.decode('ascii')

#print(decoded_string)


hex_input = "FFFF"

# 16進数を10進数に変換
decimal_value = int(hex_input, 16)

# 2の補数を計算
complement_value = (1 << (len(hex_input) * 4)) - decimal_value

# 10進数を16進数文字列に変換
hex_output = hex(complement_value)[2:]

print(hex_output.zfill(len(hex_input)))  # 必要な桁数に0埋め




