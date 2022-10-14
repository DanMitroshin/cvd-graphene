# from Tests.devices.ports import get_serial_port

try:
    import wiringpi
    import spidev
except:
    pass
# import serial
# from time import sleep
# import codecs


def test_rough_vakumetr_1():
    SPIchannel = 3
    SPIspeed = 100000
    wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)
    send_data = b'000'
    while True:
        receive_data = wiringpi.wiringPiSPIDataRW(SPIchannel, send_data)
        print("|> Receive:", receive_data)


def test_rough_vakumetr_2():
    SPIchannel = 3
    SPIspeed = 100000
    spi = spidev.SpiDev()
    spi.open(SPIchannel, 0)
    spi.max_speed_hz = 50000
    print("Connected!")
    # spi.lsbfirst = False
    # spi.cshigh = False
    # spi.mode = 0b01
    # spi.bits_per_word = 8
    send_data = b'000'

    txData = [0x00, 0x00]
    rxData = spi.xfer(txData)
    print("Receive:", end=' ')
    for i in range(len(rxData)):
        print(hex(rxData[i]), end=' ')
    print('')

    spi.close()


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        test_rough_vakumetr_2()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
