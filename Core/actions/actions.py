import time

from coregraphene.auto_actions import AppAction, ValveListArgument, GasListArgument, SccmArgument, TimeEditArgument, \
    FloatArgument, IntKeyArgument, FloatKeyArgument, get_total_seconds_from_time_arg
from coregraphene.conf import settings
from coregraphene.recipe.exceptions import NotAchievingRecipeStepGoal


ACTIONS_NAMES = settings.ACTIONS_NAMES
TABLE_ACTIONS_NAMES = settings.TABLE_ACTIONS_NAMES
MAX_RECIPE_STEP_SECONDS = settings.MAX_RECIPE_STEP_SECONDS


class TurnOnPumpAction(AppAction):
    name = TABLE_ACTIONS_NAMES.TURN_ON_PUMP
    key = ACTIONS_NAMES.TURN_ON_PUMP


class OpenValveAction(AppAction):
    name = TABLE_ACTIONS_NAMES.OPEN_VALVE
    key = ACTIONS_NAMES.OPEN_VALVE
    args_info = [ValveListArgument]


class CloseValveAction(AppAction):
    name = TABLE_ACTIONS_NAMES.CLOSE_VALVE
    key = ACTIONS_NAMES.CLOSE_VALVE
    args_info = [ValveListArgument]


class CloseAllValvesAction(AppAction):
    name = TABLE_ACTIONS_NAMES.CLOSE_ALL_VALVES
    key = ACTIONS_NAMES.CLOSE_ALL_VALVES


class SetRrgValueAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_RRG_VALUE
    key = ACTIONS_NAMES.SET_RRG_VALUE
    args_info = [GasListArgument, SccmArgument]


class SetRrgValueWithPauseAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_RRG_VALUE_WITH_PAUSE
    key = ACTIONS_NAMES.SET_RRG_VALUE_WITH_PAUSE
    args_info = [GasListArgument, SccmArgument, TimeEditArgument]


class PumpOutCameraAction(AppAction):
    name = TABLE_ACTIONS_NAMES.PUMP_OUT_CAMERA
    key = ACTIONS_NAMES.PUMP_OUT_CAMERA
    args_info = [FloatArgument, TimeEditArgument]


class VentilateCameraAction(AppAction):
    name = TABLE_ACTIONS_NAMES.VENTILATE_CAMERA
    key = ACTIONS_NAMES.VENTILATE_CAMERA
    args_info = [IntKeyArgument, IntKeyArgument]


class RampAction1(AppAction):
    name = TABLE_ACTIONS_NAMES.RAMP
    key = ACTIONS_NAMES.RAMP
    args_info = [FloatKeyArgument, TimeEditArgument]


class RampAction(AppAction):
    name = TABLE_ACTIONS_NAMES.RAMP
    key = ACTIONS_NAMES.RAMP
    args_info = [FloatKeyArgument, TimeEditArgument]

    def action(self, target_current, time_limit):
        start_time = time.time()

        target_current = float(target_current)
        self.system.set_target_current_ramp_action(target_current)
        self.system.set_is_active_ramp_action(True)

        pause = 1  # secs

        seconds = get_total_seconds_from_time_arg(time_limit)
        if seconds <= pause:
            seconds = pause
        end_time = start_time + seconds
        left_time = end_time - time.time()

        current_value = self.system.current_value
        local_current_value = current_value
        # delta_value = target_current - current_value

        def get_next_target():
            if left_time <= pause:
                return target_current
            delta_value = target_current - local_current_value
            return delta_value / left_time * pause + local_current_value

        while True:
            if self._is_stop_state():
                break

            left_time = max(0, end_time - time.time())
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

        self.system.set_is_active_ramp_action(False)


class SetTemperatureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.SET_TEMPERATURE
    key = ACTIONS_NAMES.SET_TEMPERATURE
    args_info = [IntKeyArgument, TimeEditArgument]


class PauseAction(AppAction):
    name = TABLE_ACTIONS_NAMES.PAUSE
    key = ACTIONS_NAMES.PAUSE
    args_info = [TimeEditArgument]


class FullOpenPumpAction(AppAction):
    name = TABLE_ACTIONS_NAMES.FULL_OPEN_PUMP
    key = ACTIONS_NAMES.FULL_OPEN_PUMP
    args_info = []


class FullClosePumpAction(AppAction):
    name = TABLE_ACTIONS_NAMES.FULL_CLOSE_PUMP
    key = ACTIONS_NAMES.FULL_CLOSE_PUMP


class StabilizePressureAction(AppAction):
    name = TABLE_ACTIONS_NAMES.STABILIZE_PRESSURE
    key = ACTIONS_NAMES.STABILIZE_PRESSURE
    args_info = [FloatArgument, TimeEditArgument]


ACTIONS = [
    # TurnOnPumpAction(),
    # OpenValveAction(),
    # CloseValveAction(),
    # CloseAllValvesAction(),
    # SetRrgValueAction(),
    # SetRrgValueWithPauseAction(),
    # PumpOutCameraAction(),
    # VentilateCameraAction(),
    # RampAction(),
    # SetTemperatureAction(),
    # PauseAction(),
    # FullOpenPumpAction(),
    # FullClosePumpAction(),
    # StabilizePressureAction(),
]
