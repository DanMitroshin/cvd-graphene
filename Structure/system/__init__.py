import uuid
import time
import os
from math import isnan

import pandas as pd
from time import sleep
from threading import Thread

from coregraphene.components.controllers import (
    AbstractController,
    AccurateVakumetrController,
    ValveController,
    CurrentSourceController,
)

from coregraphene.conf import settings
from coregraphene.constants import NOTIFICATIONS, RECIPE_STATES

from Structure.system.exceptions.conditions import BadNumbersConditionException, BaseConditionException
from Structure.system.recipe_runner import RecipeRunner

VALVES_CONFIGURATION = settings.VALVES_CONFIGURATION
TABLE_COLUMN_NAMES = settings.TABLE_COLUMN_NAMES


class EventLog:
    def __init__(self, log, log_type=NOTIFICATIONS.LOG):
        self.uid = uuid.uuid4()
        self.log = log
        self.log_type = log_type

    def __str__(self):
        return f"{self.uid} | {self.log_type} | {self.log}"


class CvdSystem(object):

    def __init__(self):
        self._last_action_answer = None
        self._errors = []
        self._event_logs = []
        self._is_working = True

        self._recipe = None
        self._recipe_runner = RecipeRunner(
            # ...
            on_success_end_recipe=self._on_success_end_recipe,
            set_current_recipe_step=self._set_current_recipe_step,
        )
        self._recipe_thread = None
        self._recipe_history = []
        self._recipe_current_step = ""
        self._recipe_state = RECIPE_STATES.STOP

        # CONTROLLERS
        self.accurate_vakumetr_controller = AccurateVakumetrController()
        self._valves = {}
        for valve_conf in VALVES_CONFIGURATION:
            self._valves[valve_conf["NAME"]] = ValveController(port=valve_conf["PORT"])

        self.current_source_controller = CurrentSourceController(
            on_change_current=self.on_change_current,
            on_change_voltage=self.on_change_voltage,
            on_set_current=None,  # ДОБАВИТЬ РЕАЛЬНОЕ ВЛИЯНИЕ - ПРОСТОЕ ВЫСТАВЛЕНИЕ АКТУАЛЬНОГО ЗНАЧЕНИЯ В UI
        )

        self._controllers: list[AbstractController] = [
            self.accurate_vakumetr_controller,
            self.current_source_controller,
        ]

        for valve in self._valves.values():
            self._controllers.append(valve)

        # VALUES
        self.accurate_vakumetr_value = 0.0
        self.current_value = 0.0
        self.voltage_value = 0.0

        # self._add_error_log("Тупая тупая ошибка где много букв self.accurate_vakumetr_value = self.accurate_vakume self.accurate_vakumetr_value = self.accurate_vakumetr_controller.get_value()")
        # self._add_log("Тупая тупая заметка!!!!!", log_type=NOTIFICATIONS.LOG)

    @property
    def has_logs(self):
        return bool(self._event_logs)

    @property
    def first_log(self):
        try:
            return self._event_logs[0]
        except:
            return None

    def clear_log(self, uid):
        self._event_logs = list(filter(lambda x: x.uid != uid, self._event_logs))

    def setup(self):
        for controller in self._controllers:
            if controller is not None:
                controller.setup()

    def threads_setup(self):
        # for controller in self._controllers:
        #     if controller is not None:
        #         controller.setup()
        return
        self.current_source_controller.thread_setup(
            self.is_working,
            self._add_log,
            self._add_error_log
        )
        self.current_source_controller.run()

    def stop(self):
        """
        Function for execute before closing main ui program to destroy all threads
        :return:
        """
        self._is_working = False

    def is_working(self):
        return self._is_working

    def destructor(self):
        print("System del | Controllers:", len(self._controllers))
        self._is_working = False
        for controller in self._controllers:
            if controller is not None:
                controller.destructor()
        if self._recipe_thread is not None:
            self._recipe_thread.join()

    def check_conditions(self):
        if 5 > 6:
            raise BadNumbersConditionException
        return True

    def action(func):
        """
        Decorator for actions, that check all conditions and system state
        :return: new decorated function
        """

        def wrapper(self, *args, **kwargs):
            try:
                self.check_conditions()

                answer = func(self, *args, **kwargs)
                self._last_action_answer = answer
                return answer
            except Exception as e:
                return self._handle_exception(e)

        return wrapper

    def _add_log(self, log, log_type=NOTIFICATIONS.LOG):
        try:
            self._event_logs.append(EventLog(log, log_type=log_type))
        except Exception as e:
            print(f"Add event log error: {e}")

    def _add_error_log(self, e):
        self._add_log(str(e), log_type=NOTIFICATIONS.ERROR)

    def _handle_exception(self, e):
        print("Raise exception in handler!")
        self._add_error_log(e)
        self._errors.append(e)
        if isinstance(e, BaseConditionException):
            pass

    def log_state(self):
        for controller in self._controllers:
            value = controller.get_value()

    @action
    def change_valve_state(self, gas):
        # t = Thread(target=self.long_function)
        # t.start()
        # return 1
        valve = self._valves.get(gas, None)
        if valve is None:
            return False
        return valve.change_state()

    def on_change_current(self, value):
        self.current_value = value

    def on_change_voltage(self, value):
        self.voltage_value = value

    @action
    def set_current(self, value):
        return self.current_source_controller.set_current_value(value)

    def get_values(self):
        try:
            # pass
            self.accurate_vakumetr_value = self.accurate_vakumetr_controller.get_value()
            # self.current_value = self.current_source_controller.get_current_value()
            # self.voltage_value = self.current_source_controller.get_voltage_value()
            # print("VOLT VAL:", self.voltage_value)
        except Exception as e:
            self._add_error_log(e)

    @property
    def recipe_state(self):
        return self._recipe_runner.recipe_state

    def on_pause_recipe(self):
        self._recipe_runner.set_recipe_state(RECIPE_STATES.PAUSE)

    def on_stop_recipe(self):
        self._recipe_runner.set_recipe_state(RECIPE_STATES.STOP)

    def save_recipe_file(self, path: str = None, file: str = None, file_path=None, data=None):
        if file_path is None and (file is None or len(file) < 8):
            self._handle_exception(Exception(f"Ошибка сохранения {file}: название файла не может быть меньше 8 символов"))
            return
        try:
            df = pd.DataFrame(data, columns=TABLE_COLUMN_NAMES)
            total_path = file_path if file_path else os.path.join(path, file)  # "recipes/test3.xlsx"
            df.to_excel(excel_writer=total_path)
        except Exception as e:
            self._handle_exception(Exception(f"Ошибка сохранения {file}: {str(e)}"))
        else:
            self._add_log(f"Файл {file} сохранён")

    def get_recipe_file_data(self, file_path: str):
        file_name = None
        try:
            file_name = os.path.basename(file_path)
            # print("FILE P:", file_path, file_name)
            excel_data_df = pd.read_excel(file_path, header=None)
            cols = excel_data_df.columns.ravel()
            arr = []
            for col in cols[1:]:
                a = excel_data_df[col].tolist()[1:]
                for i in range(len(a)):
                    # try:
                    if i + 1 > len(arr):
                        arr.append([])
                    if type(a[i]) != str and isnan(a[i]):
                        a[i] = ""
                    arr[i].append(str(a[i]))
            # print("RECIPE GET ARRAY DATA", arr)
            return arr
        except Exception as e:
            self._handle_exception(Exception(f"Ошибка открытия {file_name}: {str(e)}"))

    def _on_success_end_recipe(self):
        try:
            self._add_log("Рецепт успешно выполнен")
            # self._recipe_thread.join()
            self._recipe_thread = None
            self._recipe = None
        except Exception as e:
            print("On success end recipe error:", e)

    def run_recipe(self, recipe):
        if type(recipe) != list:
            self._add_error_log(Exception("Чтение рецепта завершилось с ошибками"))
            return False

        self._recipe = recipe
        self._recipe_runner.set_recipe(self._recipe)
        ready = self._recipe_runner.check_recipe()
        if ready:
            self._recipe_thread = Thread(target=self._recipe_runner.run_recipe)
            self._recipe_thread.start()
        print("|>> WHAT'S READY:", ready)
        return ready

    def _set_current_recipe_step(self, name, index=None):
        index = index if index else (len(self._recipe_history) + 1)
        self._recipe_current_step = {'name': name, 'index': index}
        self._recipe_history.append(self._recipe_current_step)

    @property
    def current_recipe_step(self):
        return self._recipe_current_step
