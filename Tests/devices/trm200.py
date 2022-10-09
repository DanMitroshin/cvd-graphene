
try:
    import wiringpi
except:
    pass
import serial
from time import sleep
import codecs

from Core.utils.algorithms import crc16

PORT = "/dev/ttyUSB0"
#  '/dev/ttyAMA0'

def f(i):
    return str(hex(i))[2:]

def crc16x(data: str, poly: hex = 0xA001) -> str:
    '''
        CRC-16 MODBUS HASHING ALGORITHM
    '''
    crc = 0xFFFF
    for byte in data:
        crc ^= ord(byte)
        for _ in range(8):
            crc = ((crc >> 1) ^ poly
                   if (crc & 0x0001)
                   else crc >> 1)

    hv = hex(crc).upper()[2:]
    blueprint = '0000'
    return blueprint if len(hv) == 0 else blueprint[:-len(hv)] + hv

def test_1():
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen(PORT, 115200)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    # for i in '1':
        # sleep(1)
    # SEND_STR = f'0010MV00D\r'
    command = f"02030001"
    # command += crc16x(command)
    # command = f"02030001"
    hi, lo = crc16(codecs.decode(command, "hex"))  # CRC = b'\x58\x7A'

    # print("!!!!!!!!!! {0:02X} {1:02X}".format(hi, lo))
    # print("ALL COMM:", s + f(lo) + f(hi))
    command += f(lo) + f(hi)
    # byte_command = bytearray(command.encode("ASCII")) # + bytes([hi, lo])
    # byte_command = codecs.decode(command, "hex")  # + bytes([hi, lo])
    # serial = wiringpi.serialOpen('/dev/ttyACM0', 9600)  # Requires device/baud and returns an ID
    ans = wiringpi.serialPuts(serial, command)
    # print("Answer:", ans)
    # b = ""
    counter = 0
    # sleep(1)
    while True:
        b = wiringpi.serialGetchar(serial)
        counter += 1
        if counter > 100 or b is None or b == -1:
            print(b, end='|')
            break
    print('')
    wiringpi.serialClose(serial)


def test_2():

    RS485 = serial.Serial(
        # port='/dev/ttyAMA0',
        port=PORT,
        writeTimeout=0,
        write_timeout=0,
        # baudrate=115200,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.001,
    )

    while True:
        # n = 2
        # command = f"00{n}030001"
        command = f"02030001"
        hi, lo = crc16(codecs.decode(command, "hex"))  # CRC = b'\x58\x7A'

        # print("!!!!!!!!!! {0:02X} {1:02X}".format(hi, lo))
        # print("ALL COMM:", s + f(lo) + f(hi))
        command += f(lo) + f(hi)
        byte_command = bytearray(command.encode("ASCII")) # + bytes([hi, lo])
        # byte_command = codecs.decode(command, "hex")  # + bytes([hi, lo])
        # print("GGG", b'0010MV0' + bytes([hi, lo]))
        # command += crc
        print("BYTE COMMAND:", byte_command)
        # RS485.write(bytearray(command.encode("ASCII")))
        RS485.write(byte_command)
        sleep(0.005)
        x = RS485.readline()
        print(x)
        sleep(1)


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

    serialInst.port = PORT  # portList[-1]

    serialInst.open()


def test_4():
    s = f"002030001"
    crc = ''.join(list(map(lambda x: chr(x - 128), crc16(s))))
    print("CRC!", crc)
    s += crc
    print("ENC:", s.encode("ASCII"))


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        # test_3()
        # test_2()
        test_4()
        # test_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
