import wiringpi
import serial
from time import sleep


def test_1():
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 115200)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    # for i in '1':
        # sleep(1)
    SEND_STR = f'0010MV00D\r'
    # serial = wiringpi.serialOpen('/dev/ttyACM0', 9600)  # Requires device/baud and returns an ID
    ans = wiringpi.serialPuts(serial, SEND_STR)
    # print("Answer:", ans)
    # b = ""
    counter = 0
    # sleep(1)
    while True:
        b = wiringpi.serialGetchar(serial)
        counter += 1
        print(b, end='|')
        if counter > 100 or b is None or b == -1:
            break
    print('')
    wiringpi.serialClose(serial)


def test_2():

    RS485 = serial.Serial(
        # port='COM17',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.001
    )

    while True:
        n = 1
        command = f"00{n}0MV00D\r"
        # print(command)
        RS485.write(bytearray(command.encode("ASCII")))
        sleep(0.005)
        x = RS485.readline()
        print(x)


def test_3():
    import time
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()

    command = "0020MV00D"

    serialInst = serial.Serial()
    portList = []

    for onePort in ports:
        portList.append(str(onePort))
        print(str(onePort))

    print("Ports list:", portList)

    # val = input("select Port: COM")
    #
    # for x in range(0, len(portList)):
    #     if portList[x].startswith("COM" + str(val)):
    #         portVar = "COM" + str(val)
    #         print(portVar)

    serialInst.baudrate = 115200

    serialInst.port = '/dev/ttyAMA0'  # portList[-1]

    serialInst.open()


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        test_3()
        test_2()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
