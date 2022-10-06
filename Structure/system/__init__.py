import uuid

from Core.components.controllers.base import AbstractController
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
        self._controllers: list[AbstractController] = []

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
