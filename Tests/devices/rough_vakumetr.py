# from Tests.devices.ports import get_serial_port

try:
    import wiringpi
except:
    pass

try:
    import spidev
except Exception as e:
    print("Spidev import error:", e)
# import serial
from time import sleep
# import codecs


def test_rough_vakumetr_1():
    SPIchannel = 0
    SPIspeed = 100000
    wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)
    send_data = b'000'
    while True:
        receive_data = wiringpi.wiringPiSPIDataRW(SPIchannel, send_data)
        print("|> Receive:", receive_data)
        sleep(1)

import string
digs = string.digits + string.ascii_letters


def int2base(x, base=2):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x = x // base

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


# WORK VERSION
def test_rough_vakumetr_2():
    SPIchannel = 0
    SPIspeed = 10000
    spi = spidev.SpiDev()
    spi.open(SPIchannel, 0)  # 0 - выбор чипа
    spi.max_speed_hz = SPIspeed
    print("Connected!")
    # spi.lsbfirst = False
    # spi.cshigh = False
    # spi.mode = 0b01
    # spi.bits_per_word = 8
    send_data = b'000'

    txData = [0x80, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
    while True:
        txData = [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
        rxData = spi.xfer(txData)
        print("Receive:", rxData)
        print("Receive:", end=' ')
        if len(rxData) >= 3:
            s = ''.join(map(lambda x: int2base(x).zfill(8), rxData[:4]))
            n = int(s[8:18], 2)
            print(n) #, s, s[8:18])
        sleep(1)

    spi.close()


# TEST ЦАП
def test_rough_vakumetr_3():
    SPIchannel = 1
    SPIspeed = 10000
    spi = spidev.SpiDev()
    spi.open(SPIchannel, 0)  # 0 - выбор чипа
    spi.max_speed_hz = SPIspeed
    print("Connected!")
    # spi.lsbfirst = False
    # spi.cshigh = False
    # spi.mode = 0b01
    # spi.bits_per_word = 8

    txData = [0x80, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
    while True:
        s = '0000010000000000'
        # txData = [int(s, 2)]
        txData = [0x01, 0x00]
        txData = [0x80, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
        rxData = spi.xfer(txData)
        print("Receive:", rxData)
        print("Receive:", end=' ')
        if len(rxData) >= 3:
            s = ''.join(map(lambda x: int2base(x).zfill(8), rxData[:4]))
            n = int(s[8:18], 2)
            print(n) #, s, s[8:18])
        sleep(0.01)

    spi.close()


if __name__ == "__main__":
    print("TEST 1 ===>")
    # test_rough_vakumetr_3()
    try:
        # test_rough_vakumetr_2()  # WORK VERSION
        test_rough_vakumetr_3()
        # s = '0000010000000000'
        # h = int2base(int(s, 2), base=16)
        # h = int(hex(int(s, 2)), 16)
        # print(h, type(h), type(0x44))
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
