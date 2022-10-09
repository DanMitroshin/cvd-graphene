import wiringpi


def test_1():
    SEND_STR = '0010MV00D\r'
    # serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)  # Requires device/baud and returns an ID
    serial = wiringpi.serialOpen('DEFAULT_COM_PORT', 9600)  # Requires device/baud and returns an ID
    print("Serial:", serial)
    ans = wiringpi.serialPuts(serial, SEND_STR)
    print("Answer:", ans)
    b = ""
    counter = 0
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
