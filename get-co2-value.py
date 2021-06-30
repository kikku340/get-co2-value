"""
1病周期でCO2値を取得するプログラム
センサ:MH-Z14B
"""

import serial
import time


s = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.1)

def read_co2():
    # MH-Z14Bにコマンド送信&レスポンス受信
    s.write(bytes([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]))
    data = s.read(9)

    if len(data) != 9:
        print("受信バイト数が正しくありません。受信バイト数：{0}byte", len(data))
        s.reset_input_buffer()
        return None

    # スタートバイト(0xff)とコマンド(0x86)が正しいか
    if data[0] != 0xFF or data[1] != 0x86:
        print("受信データに誤りがあります")
        s.reset_input_buffer()
        return None

    # チェックサム確認
    checksum = 0xFF - (sum(data[1:7]) & 0xFF) + 1
    if checksum != data[8]:
        print("チェックサムエラー")
        s.reset_input_buffer()
        return None

    return data[2] * 256 + data[3]

while True:
    co2 = read_co2()
    print(co2, "ppm")
    time.sleep(1)