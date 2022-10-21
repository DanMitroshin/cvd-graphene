import time
import traceback
from threading import Thread

from Core.components.commands import BaseCommand
from Core.components.devices import AbstractDevice
from Core.exceptions.controllers import ControllerInWaiting
from Core.settings import LOCAL_MODE


class AbstractController(object):
    """
    Class for device controllers
    """

    device_class = None

    def __init__(self, *args, **kwargs):
        if self.device_class is not None:
            self.device: AbstractDevice = self.device_class()

        self._active = True

        # THREAD VARIABLES ############################
        self._runnable = False
        self._is_global_working = True
        self._thread = None
        self._commands_queue = []
        self._is_thread_reading = False
        self._last_thread_command: BaseCommand = None
        self._start_thread_read_time = None
        self._critical_read_time = -0.1 if LOCAL_MODE else 3.0

        # target value and function for calling after sensor reach this value
        self._target_value = None
        self._on_reached = None

        # Params for setting sensor unreachable for time of delay
        self._start_timer = None
        self._delay = None
        self._after_waiting = None

        self._last_answer = None
        self._errors = []

    def thread_setup(self, is_working, add_log, add_error, **kwargs):
        self._runnable = True
        self._is_global_working = is_working
        self._add_log = add_log
        self._add_error = add_error
        # print("IS WORK OBJECT", is_working)

    @property
    def _is_working(self):
        if type(self._is_global_working) == bool:
            return self._is_global_working
        return self._is_global_working()

    def _on_thread_error(self, exception: Exception):
        self._add_error(exception)

    def add_command(self, command: BaseCommand):
        if self._runnable and self._is_working:
            self._commands_queue.append(command)

    def _add_command_force(self, command: BaseCommand):
        if self._runnable:
            self._commands_queue.insert(0, command)

    def _run_thread_command(self, command: BaseCommand):
        self._last_thread_command = command
        self._exec_command(command=command)

    def _thread_read_command(self):
        if self._start_thread_read_time is None:
            self._start_thread_read_time = time.time()

        if time.time() - self._start_thread_read_time > self._critical_read_time:
            self._start_thread_read_time = None
            self._is_thread_reading = False
            read_value = ""
        else:
            read_value = self.device.read()
            print(f"|> Read value for C[{self._last_thread_command.command}]: {read_value}")
            if read_value:
                self._start_thread_read_time = None
                self._is_thread_reading = False
                # print("READ FOR:", self._last_thread_command.command)
                self._last_thread_command.on_answer(read_value)
        return read_value

    def _run(self):
        to_exit = False
        while True:
            time.sleep(0.2)
            try:
                if self._is_thread_reading:
                    self._thread_read_command()
                elif len(self._commands_queue) > 0:
                    if not self._is_working and not to_exit:
                        self._commands_queue.clear()
                        continue
                    command: BaseCommand = self._commands_queue.pop(0)
                    print("|> CURRENT COMMAND [c]:", command.command)
                    if command.repeat:
                        self._commands_queue.append(command)
                    if command.with_answer:
                        self._is_thread_reading = True
                    self._run_thread_command(command)
                else:
                    if to_exit:
                        break
                    if not self._is_working:
                        to_exit = True
                        self._commands_queue = self._get_last_commands_to_exit()

            except Exception as e:
                self._on_thread_error(e)

    def run(self):
        if self._runnable and self._thread is None:
            self._thread = Thread(target=self._run)
            self._thread.start()

    def _get_last_commands_to_exit(self):
        return []

    def setup(self):
        self.device.setup()

    def destructor(self):
        if self._thread is not None:
            self._thread.join()
        self.device.destructor()

    @property
    def is_get_value(self):
        return True

    def device_command(strong=False):
        """
        Decorator for commands
        :return: new decorated function
        """
        def command_wrapper(func):
            def wrapper(self, **kwargs):
                try:
                    if not strong and not self._active:
                        raise ControllerInWaiting
                    self._last_answer = func(self, **kwargs)
                    return self._last_answer
                except Exception as e:
                    return self._handle_exception(e)

            return wrapper
        return command_wrapper

    def thread_command(func):
        """
        Decorator for commands
        :return: new decorated function
        """
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                return self._on_thread_error(e)

        return wrapper

    @device_command()
    def exec_command(self, command=None, value=None):
        """
        Send command with value to sensor
        :param command:
        :param value:
        :return: answered value from sensor
        """
        return self.device.exec_command(command=command, value=value)

    @device_command()
    def _exec_command(self, command: BaseCommand):
        """
        Send command with value to sensor
        :param command:
        :param value:
        :return: answered value from sensor
        """
        return self.device.exec_command(command=command.command, value=command.value)

    @device_command(strong=True)
    def get_value(self):
        """
        Send command with getting value from device
        :return: answered value from device
        """
        # raise NotImplementedError
        command = None
        value = None
        return self.device.exec_command(command=command, value=value)

    def get_last_answer(self):
        return self._last_answer

    def _handle_exception(self, e):
        s = traceback.format_exc()
        print(s)
        raise e

    def wait_seconds(self, seconds=None, after_wait=None, **kwargs):
        """
        Wait for seconds before actions;
        :param after_wait: function for execute after waiting
        :param seconds: amount of seconds
        :param kwargs:
        :return:
        """
        self._start_timer = time.time()
        self._delay = seconds
        self._after_waiting = after_wait

    def wait_until_value(self, target_value, on_reached=None, **kwargs):
        """
        TODO: ADD COMMAND PARAMS FOR EXECUTION TO REACH TARGET VALUE
        Wait time until target value is not reached
        :param on_reached: function for execute after value is reached
        :param target_value: target value
        :param kwargs:
        :return:
        """
        self._target_value = target_value
        self._on_reached = on_reached
