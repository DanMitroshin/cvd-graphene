import time
import traceback
from Core.components.devices import AbstractDevice
from Core.exceptions.controllers import ControllerInWaiting


class AbstractController(object):
    """
    Class for device controllers
    """

    device_class = None

    def __init__(self, *args, **kwargs):
        if self.device_class is not None:
            self.device: AbstractDevice = self.device_class()

        self._active = True
        # target value and function for calling after sensor reach this value
        self._target_value = None
        self._on_reached = None

        # Params for setting sensor unreachable for time of delay
        self._start_timer = None
        self._delay = None
        self._after_waiting = None

        self._last_answer = None
        self._errors = []

    def setup(self):
        self.device.setup()

    def destructor(self):
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

    @device_command()
    def exec_command(self, command=None, value=None):
        """
        Send command with value to sensor
        :param command:
        :param value:
        :return: answered value from sensor
        """
        return self.device.exec_command(command=command, value=value)

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
