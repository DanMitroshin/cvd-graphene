try:
    import wiringpi
except:
    pass
import serial
from time import sleep

PORT = "/dev/ttyUSB0"
#  '/dev/ttyAMA0'

def test_akip_1():
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen(PORT, 19200)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    # for i in '1':
        # sleep(1)
    SEND_STR = f"A007SYST:BEEP?0X0A"
    # serial = wiringpi.serialOpen('/dev/ttyACM0', 9600)  # Requires device/baud and returns an ID
    ans = wiringpi.serialPuts(serial, SEND_STR)
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


def test_akip_2():

    RS485 = serial.Serial(
        # port='/dev/ttyAMA0',
        port=PORT,
        # writeTimeout=0,
        # write_timeout=0,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.001,
    )
    ADDRESS = 3
    command_remote = f"A00{ADDRESS}SYSTem:REMote;\n"
    remote = f"SYSTem:REMote"
    command_beep_on = f"A00{ADDRESS}SYST:BEEP 1;\n"
    command_beep_off = f"A00{ADDRESS}SYST:BEEP 0;\n"

    command_measure_current = f"A00{ADDRESS}MEASure:CURRent?;\n"  # 10-4-32
    command_measure_voltage = f"A00{ADDRESS}MEASure:VOLTage?;\n"  # 10-4-31

    command_set_voltage = f"A00{ADDRESS}SOURce:VOLTage 30;\n"  # 10-4-34 // 30V
    command_get_voltage = f"A00{ADDRESS}SOURce:VOLTage?;\n"  # 10-4-35

    command_set_current = f"A00{ADDRESS}SOURce:CURRent 1;\n"  # 10-4-40
    command_get_current = f"A00{ADDRESS}SOURce:CURRent?;\n"  # 10-4-41

    command_get_errors = f"A00{ADDRESS}SYSTem:ERRor?;\n"  #

    def create_command(c):
        return f"A00{ADDRESS};\n"

    def run_command(command):
        RS485.write(bytearray(command.encode("ASCII")))
        _answer = RS485.readline()
        command_get_errors = f"A00{ADDRESS}SYSTem:ERRor?;\n"
        RS485.write(bytearray(command_get_errors.encode("ASCII")))
        _errors = RS485.readline()
        print(f"[COMMAND] {command}. Answer: {_answer} | Status: {_errors}")
        return _answer, _errors
        # print("ANSWER:", x)

    max_voltage_limit = "SOURce:VOLTage:PROTection:LEVel 13.75"  # 10-4-36 Max voltage limit
    max_current_limit = "SOURce:CURRent:PROTection:LEVel 132"  # 10-4-43 Max current limit
    max_voltage_actual = "SOURce:VOLTage 13.12"  # 10-4-34 Voltage limit for actual value
    max_current_actual = "SOURce:CURRent 1.0"  # 10-4-40 Current limit for actual value

    command_remote = create_command(remote)
    answer, errors = run_command(command_remote)
    sleep(1)
    answer, errors = run_command(create_command(max_voltage_limit))
    sleep(1)
    answer, errors = run_command(create_command(max_current_limit))
    sleep(1)
    answer, errors = run_command(create_command(max_voltage_actual))
    sleep(1)
    answer, errors = run_command(command_get_voltage)
    print("|> CURRENT VOLTAGE:", answer)
    sleep(1)

    while True:
        answer, errors = run_command(create_command(max_current_actual))
        answer, errors = run_command(command_get_current)
        print("|> CURRENT ACTUAL:", answer)
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

    # serialInst.baudrate = 115200
    serialInst.baudrate = 9600

    serialInst.port = PORT  # portList[-1]

    serialInst.open()


if __name__ == "__main__":
    print("TEST 1 ===>")
    # try:
    test_3()
    test_akip_2()
    # test_1()
    print("TEST 1 ===> PASSED")
    # except Exception as e:
    #     print("[ERROR]", e)
    #     print("TEST 1 ===> FAILED")
