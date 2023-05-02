import time

from coregraphene.auto_actions import AppAction, ValveListArgument, GasListArgument, SccmArgument, TimeEditArgument, \
    FloatArgument, IntKeyArgument, FloatKeyArgument, get_total_seconds_from_time_arg
from coregraphene.conf import settings
from coregraphene.recipe.exceptions import NotAchievingRecipeStepGoal


ACTIONS_NAMES = settings.ACTIONS_NAMES
TABLE_ACTIONS_NAMES = settings.TABLE_ACTIONS_NAMES
MAX_RECIPE_STEP_SECONDS = settings.MAX_RECIPE_STEP_SECONDS


def get_gas_index_by_name(name):
    for i, gas in enumerate(settings.VALVES_CONFIGURATION):
        if gas['NAME'] == name:
            return i


class PauseAction(AppAction):
    name = TABLE_ACTIONS_NAMES.PAUSE
    key = ACTIONS_NAMES.PAUSE
    args_info = [TimeEditArgument]

    def do_action(self, seconds):  # , *args, **kwargs):
        # print("SLEEP SECONDS:", seconds, time.time())
        start = time.time()
        while time.time() - start < seconds:
            time.sleep(1)
            if self._is_stop_state():
                break


class TurnOnPumpAction(AppAction):
    name = TABLE_ACTIONS_NAMES.TURN_ON_PUMP
    key = ACTIONS_NAMES.TURN_ON_PUMP

    def do_action(self):
        self.system.change_pump_manage_active_action(True)


class OpenValveAction(AppAction):
    name = TABLE_ACTIONS_NAMES.OPEN_VALVE
    key = ACTIONS_NAMES.OPEN_VALVE
    args_info = [ValveListArgument]

    def do_action(self, valve_name: str):
        is_gas = valve_name in list(map(lambda x: x['NAME'], settings.VALVES_CONFIGURATION))
        is_air = valve_name == settings.AIR_VALVE_CONFIGURATION['NAME']
        if is_air:
            self.system.change_air_valve_opened(True)
        elif is_gas:
            index = get_gas_index_by_name(valve_name)
            self.system.change_gas_valve_opened(True, device_num=index)
        else:
            self.system.change_pump_valve_opened_action(True)


class CloseValveAction(AppAction):
    name = TABLE_ACTIONS_NAMES.CLOSE_VALVE
    key = ACTIONS_NAMES.CLOSE_VALVE
    args_info = [ValveListArgument]

    def do_action(self, valve_name: str):
        is_gas = valve_name in list(map(lambda x: x['NAME'], settings.VALVES_CONFIGURATION))
        is_air = valve_name == settings.AIR_VALVE_CONFIGURATION['NAME']
        if is_air:
            self.system.change_air_valve_opened(False)
        elif is_gas:
            index = get_gas_index_by_name(valve_name)
            self.system.change_gas_valve_opened(False, device_num=index)
        else:
            self.system.change_pump_valve_opened_action(False)


class CloseAllValvesAction(AppAction):
    name = TABLE_ACTIONS_NAMES.CLOSE_ALL_VALVES
    key = ACTIONS_NAMES.CLOSE_ALL_VALVES

    def do_action(self):
        self.system.change_air_valve_opened(False)

        for i, _ in enumerate(settings.VALVES_CONFIGURATION):
            self.system.change_gas_valve_opened(False, device_num=i)

        self.system.change_pump_valve_opened_action(False)


class SetThrottlePercentAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_THROTTLE_PERCENT
    key = ACTIONS_NAMES.SET_THROTTLE_PERCENT
    args_info = [IntKeyArgument]

    def do_action(self, target_percent: int):
        self.system.back_pressure_valve_controller.set_target_percent(target_percent)


class FullOpenThrottleAction(AppAction):
    name = TABLE_ACTIONS_NAMES.FULL_OPEN_THROTTLE
    key = ACTIONS_NAMES.FULL_OPEN_THROTTLE
    args_info = []

    def do_action(self):
        self.system.back_pressure_valve_controller.on_full_open()


class FullCloseThrottleAction(AppAction):
    name = TABLE_ACTIONS_NAMES.FULL_CLOSE_THROTTLE
    key = ACTIONS_NAMES.FULL_CLOSE_THROTTLE
    args_info = []

    def do_action(self):
        self.system.back_pressure_valve_controller.on_full_close()


class SetThrottlePressureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_THROTTLE_PRESSURE
    key = ACTIONS_NAMES.SET_THROTTLE_PRESSURE
    args_info = [FloatKeyArgument]

    def do_action(self, target_pressure: float):
        self.system.back_pressure_valve_controller.turn_on_regulation(target_pressure)


class SetRrgSccmValueAction(AppAction):
    """
    Установить значение sccm для ррг
    """
    name = TABLE_ACTIONS_NAMES.SET_RRG_VALUE
    key = ACTIONS_NAMES.SET_RRG_VALUE
    args_info = [GasListArgument, SccmArgument]

    def do_action(self, valve_name: str, sccm: float):
        index = get_gas_index_by_name(valve_name)
        self.system.set_target_rrg_sccm_action(sccm, device_num=index)


class SetRrgSccmValueWithPauseAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_RRG_VALUE_WITH_PAUSE
    key = ACTIONS_NAMES.SET_RRG_VALUE_WITH_PAUSE
    args_info = [GasListArgument, SccmArgument, TimeEditArgument]

    def do_action(self, valve_name: str, sccm: float, seconds: int):

        action_rrg = SetRrgSccmValueAction()
        action_rrg.system = self.system
        action_rrg.action(valve_name, sccm)

        action_pause = PauseAction()
        action_pause.system = self.system
        action_pause.action(seconds)


class PumpOutCameraAction(AppAction):
    """
    1) закрываются все клапаны
    2) отправляется команда на клапан обратного давления открыться на 7%
    3) включается насос
    4) ожидаем наступления давления 10мбар
    5) открывает большой клапан на насос
    6) отправляет на клапан обратного давления команду полностью закрыться
    7) ожидаем наступления давления 10^-3 мбар
    8) закрываем все клапаны
    """
    name = TABLE_ACTIONS_NAMES.PUMP_OUT_CAMERA
    key = ACTIONS_NAMES.PUMP_OUT_CAMERA
    # args_info = [FloatArgument, TimeEditArgument]
    args_info = []

    def do_action(self):
        start_time = time.time()

        # 1 - закрываются все клапаны
        close_valves = CloseAllValvesAction()
        close_valves.system = self.system
        close_valves.action()

        # 2 - отправляется команда на клапан обратного давления открыться на 7%
        throttle_percent = SetThrottlePercentAction()
        throttle_percent.system = self.system
        throttle_percent.action(7.0)

        # 3 - включается насос
        turn_on_pump = TurnOnPumpAction()
        turn_on_pump.system = self.system
        turn_on_pump.action()

        # 4 - ожидаем наступления давления 10 мбар
        while self.system.get_accurate_vakumetr_value() >= 10.0:
            if self._is_stop_state():
                return

            delta_time = time.time() - start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Откачка не завершилась до достижения максимального времени")
                raise NotAchievingRecipeStepGoal

        # 5 - открывает большой клапан на насос
        open_pump = OpenValveAction()
        open_pump.system = self.system
        open_pump.action("Pump")

        # 6 - отправляет на клапан обратного давления команду полностью закрыться
        close_throttle = FullCloseThrottleAction()
        close_throttle.system = self.system
        close_throttle.action()

        # 7 - ожидаем наступления давления 10^-3 мбар
        while self.system.get_accurate_vakumetr_value() >= 0.001:
            if self._is_stop_state():
                return

            delta_time = time.time() - start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Откачка не завершилась до достижения максимального времени")
                raise NotAchievingRecipeStepGoal

        # 8 - закрываются все клапаны
        close_valves = CloseAllValvesAction()
        close_valves.system = self.system
        close_valves.action()


class VentilateCameraAction(AppAction):
    name = TABLE_ACTIONS_NAMES.VENTILATE_CAMERA
    key = ACTIONS_NAMES.VENTILATE_CAMERA
    args_info = [IntKeyArgument, IntKeyArgument]


class RampAction(AppAction):
    name = TABLE_ACTIONS_NAMES.RAMP
    key = ACTIONS_NAMES.RAMP
    args_info = [FloatKeyArgument, TimeEditArgument]

    def do_action(self, target_current: float, seconds: int):
        start_time = time.time()

        self.system.set_target_current_ramp_action(target_current)

        self.system.set_is_active_ramp_action(True)

        pause = 1  # secs

        if seconds <= pause:
            seconds = pause
        end_time = start_time + seconds
        left_time = end_time - time.time()

        current_value = self.system.current_value
        local_current_value = current_value
        # # delta_value = target_current - current_value

        def get_next_target():
            if left_time <= pause:
                return target_current
            delta_value = target_current - local_current_value
            return delta_value / left_time * pause + local_current_value

        while True:
            if self._is_stop_state():
                break

            left_time = max(0.0, end_time - time.time())
            next_target_current = get_next_target()
            self.system.set_target_current_action(next_target_current)
            self.system.set_ramp_seconds_action(left_time)

            if left_time <= 0:
                break

            time.sleep(1)

            current_value = self.system.current_value
            local_current_value = current_value

            delta_time = time.time() - start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                raise NotAchievingRecipeStepGoal

        # time.sleep(4)
        self.system.set_is_active_ramp_action(False)


class SetTargetTemperatureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_TARGET_TEMPERATURE
    key = ACTIONS_NAMES.SET_TARGET_TEMPERATURE
    args_info = [IntKeyArgument]

    def do_action(self, target_temperature: int):
        self.system.set_target_temperature_action(target_temperature)


class StartTemperatureRegulationAction(AppAction):
    name = TABLE_ACTIONS_NAMES.START_TEMPERATURE_REGULATION
    key = ACTIONS_NAMES.START_TEMPERATURE_REGULATION
    args_info = []

    def do_action(self, target_temperature: int):
        start_time = time.time()
        target_temperature = self.system.target_temperature

        # PID constants
        Kp = 0.5
        Ki = 0.1
        Kd = 0.2

        # Initial values
        error = 0
        integral = 0
        derivative = 0
        output = 0
        prev_error = 0
        current = 0

        # Desired setpoint temperature and heating rate
        setpoint = 50
        heating_rate = 5

        # Maximum and minimum output values
        max_output = 100
        min_output = 0

        # Maximum and minimum current values
        max_current = 10
        min_current = 0

        # Main loop
        while True:
            if self._is_stop_state():
                return

            delta_time = time.time() - start_time
            if MAX_RECIPE_STEP_SECONDS and (delta_time >= MAX_RECIPE_STEP_SECONDS):
                self.system.add_error_log(f"Регуляция температуры не завершилась до достижения максимального времени")
                raise NotAchievingRecipeStepGoal
            # Read temperature sensor
            current_temp = read_temperature_sensor()

            # Calculate error
            error = setpoint - current_temp

            # Calculate integral term
            integral += error

            # Calculate derivative term
            derivative = error - prev_error

            # Calculate output value
            output = Kp * error + Ki * integral + Kd * derivative

            # Limit output value
            if output > max_output:
                output = max_output
            elif output < min_output:
                output = min_output

            # Calculate desired current
            desired_current = output + heating_rate * error

            # Limit desired current
            if desired_current > max_current:
                desired_current = max_current
            elif desired_current < min_current:
                desired_current = min_current

            # Set current through current source
            set_current(desired_current)

            # Store previous error and current
            prev_error = error
            current = desired_current

            # Wait for some time before polling again
            time.sleep(0.1)


class StabilizePressureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.STABILIZE_PRESSURE
    key = ACTIONS_NAMES.STABILIZE_PRESSURE
    args_info = [FloatArgument, TimeEditArgument]


ACTIONS = [
    TurnOnPumpAction(),
    OpenValveAction(),
    CloseValveAction(),
    CloseAllValvesAction(),
    SetRrgSccmValueAction(),
    SetRrgSccmValueWithPauseAction(),
    PumpOutCameraAction(),

    SetThrottlePressureAction(),
    FullOpenThrottleAction(),
    FullCloseThrottleAction(),
    SetThrottlePercentAction(),

    SetTargetTemperatureAction(),
    PauseAction(),
    # FullOpenPumpAction(),
    # FullClosePumpAction(),
    # StabilizePressureAction(),
    RampAction(),
]
