import wiringpi
from time import sleep


def test_1():
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    for i in '1':
        sleep(1)
        SEND_STR = f'00{i}0MV00D\r'
        # serial = wiringpi.serialOpen('/dev/ttyACM0', 9600)  # Requires device/baud and returns an ID
        ans = wiringpi.serialPuts(serial, SEND_STR)
        print("Answer:", ans)
        b = ""
        counter = 0
        sleep(1)
        while True:
            b = wiringpi.serialGetchar(serial)
            counter += 1
            print(b, end='|')
            if counter > 100 or b is None or b == -1:
                break
        print('')
    wiringpi.serialClose(serial)


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        test_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
