import uuid

from Core.components.controllers import AccurateVakumetrController, ValveController, CurrentSourceController
from Core.components.controllers.base import AbstractController
from Core.settings import VALVES_CONFIGURATION
from Structure.system.exceptions.conditions import BadNumbersConditionException, BaseConditionException
from Structure.system.constants import NOTIFICATIONS


class CvdSystem(object):
    class EventLog:
        def __init__(self, log, log_type=NOTIFICATIONS.LOG):
            self.uid = uuid.uuid4()
            self.log = log
            self.log_type = log_type

    def __init__(self):
        self._last_action_answer = None
        self._errors = []
        self._event_logs = []

        # CONTROLLERS
        self.accurate_vakumetr_controller = AccurateVakumetrController()
        self._valves = {}
        for valve_conf in VALVES_CONFIGURATION:
            self._valves[valve_conf["NAME"]] = ValveController(port=valve_conf["PORT"])
        self.current_source_controller = CurrentSourceController()

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

    def setup(self):
        for controller in self._controllers:
            if controller is not None:
                controller.setup()

    def destructor(self):
        print("System del | Controllers:", len(self._controllers))
        for controller in self._controllers:
            if controller is not None:
                controller.destructor()

    def check_conditions(self):
        if 5 > 6:
            raise BadNumbersConditionException
        return True

    def action(func):
        """
        Decorator for actions, that check all conditions and system state
        :return: new decorated function
        """

        def wrapper(self: CvdSystem, *args, **kwargs):
            try:
                self.check_conditions()

                answer = func(self, *args, **kwargs)
                self._last_action_answer = answer
                return answer
            except Exception as e:
                return self._handle_exception(e)

        return wrapper

    def _add_log(self, log, log_type):
        try:
            self._event_logs.append(self.EventLog(log, log_type=log_type))
        except Exception as e:
            print(f"Add event log error: {e}")

    def _add_error_log(self, e):
        pass

    def _handle_exception(self, e):
        self._add_error_log(e)
        self._errors.append(e)
        if isinstance(e, BaseConditionException):
            pass

    def log_state(self):
        for controller in self._controllers:
            value = controller.get_value()

    def change_valve_state(self, gas):
        valve = self._valves.get(gas, None)
        if valve is None:
            return False
        return valve.change_state()

    def set_current(self, value):
        return self.current_source_controller.set_current_value(value)

    def get_values(self):
        self.accurate_vakumetr_value = self.accurate_vakumetr_controller.get_value()
        self.current_value = self.current_source_controller.get_current_value()
        self.voltage_value = self.current_source_controller.get_voltage_value()
