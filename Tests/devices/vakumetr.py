import wiringpi


def test_1():
    SEND_STR = '0010MV00D\r'
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    ans = wiringpi.serialPuts(serial, SEND_STR)
    print("Answer:", ans)
    wiringpi.serialClose(serial)


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        test_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")
