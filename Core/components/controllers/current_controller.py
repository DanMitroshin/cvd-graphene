import random
from time import sleep
from .base import AbstractController
from ..devices import CurrentSourceDevice

MAX_CURRENT = 132.0
MAX_SET_CURRENT = 1.0 # MAX_CURRENT
CLEAR_COMMAND = "*CLS"
REMOTE_COMMAND = f"SYST:REM"
OUTPUT_1_COMMAND = f"OUTP 1"
OUTPUT_0_COMMAND = f"OUTP 0"
GET_ERRORS_COMMAND = "SYST:ERR?"
GET_CURRENT_ACTUAL = "SOURce:CURRent?"  # 10-4-32
GET_VOLTAGE_ACTUAL = "SOURce:VOLTage?"  # 10-4-35
SET_MAX_VOLTAGE_LIMIT = "SOUR:VOLT:PROT:LEV 13.75"  # 10-4-36 Max voltage limit
SET_ZERO_VOLTAGE_LIMIT = "SOUR:VOLT:PROT:LEV 0"  # 10-4-36 Max voltage limit
# max_current_limit = "SOURce:CURRent:PROTection:LEVel 132"  # 10-4-43 Max current limit
SET_MAX_CURRENT_LIMIT = f"SOUR:CURR:PROT:LEV {int(MAX_CURRENT)}"  # 10-4-43 Max current limit
SET_ZERO_CURRENT_LIMIT = "SOUR:CURR:PROT:LEV 0"  # 10-4-43 Max current limit
# max_voltage_actual = "SOURce:VOLTage 13.12"  # 10-4-34 Voltage limit for actual value
SET_VOLTAGE_ACTUAL = "SOUR:VOLT 13.12"  # 10-4-34 Voltage limit for actual value
SET_ZERO_VOLTAGE_ACTUAL = "SOUR:VOLT 0"  # 10-4-34 Voltage limit for actual value
# max_current_actual = "SOURce:CURRent 1.0"  # 10-4-40 Current limit for actual value
SET_CURRENT_ACTUAL = "SOUR:CURR"  # 10-4-40 Current limit for actual value # + " 1.0"
SET_ZERO_CURRENT_ACTUAL = "SOUR:CURR 0"  # 10-4-40 Current limit for actual value

SLEEP_TIME = 0.05


class CurrentSourceController(AbstractController):
    device_class = CurrentSourceDevice

    def setup(self):
        super().setup()
        self.exec_command(command=CLEAR_COMMAND)
        sleep(SLEEP_TIME)
        self.exec_command(command=REMOTE_COMMAND)
        sleep(SLEEP_TIME)
        self.exec_command(command=OUTPUT_1_COMMAND)
        sleep(SLEEP_TIME)
        self.exec_command(command=SET_MAX_VOLTAGE_LIMIT)
        sleep(SLEEP_TIME)
        self.exec_command(command=SET_MAX_CURRENT_LIMIT)
        sleep(SLEEP_TIME)
        self.exec_command(command=SET_VOLTAGE_ACTUAL)

    def destructor(self):
        super().destructor()
        print("|> Current source destructor")
        # self.exec_command(command=SET_ZERO_CURRENT_ACTUAL)
        # sleep(SLEEP_TIME)
        self.exec_command(command=SET_ZERO_CURRENT_ACTUAL)
        sleep(SLEEP_TIME)
        self.exec_command(command=SET_ZERO_VOLTAGE_ACTUAL)
        sleep(SLEEP_TIME)
        self.exec_command(command=OUTPUT_0_COMMAND)

    @AbstractController.device_command()
    def exec_command(self, command=None, value=None):
        answer = self.device.exec_command(command=command, value=value)
        sleep(0.05)
        errors = self.device.exec_command(command=GET_ERRORS_COMMAND)
        # print("|> CUR S:", answer, errors)
        if errors and errors.lower() != "0 no error":
            sleep(0.05)
            self.device.exec_command(command=CLEAR_COMMAND)
            raise Exception(errors)
        return answer

    def get_current_value(self):
        return self.exec_command(command=GET_CURRENT_ACTUAL)

    def set_current_value(self, value: float = 0.0):
        value = min(value, MAX_SET_CURRENT)
        print("Set value function:", value)
        ans = self.exec_command(command=SET_CURRENT_ACTUAL, value=value)
        # raise Exception("Ошибка установки значения тока: ...")
        return value

    def get_voltage_value(self):
        return random.random()
        return self.exec_command(command=GET_VOLTAGE_ACTUAL)
