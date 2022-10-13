# from Tests.devices.ports import get_serial_port

try:
    import wiringpi
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


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        test_rough_vakumetr_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
