from Core.components.communicators import AbstractCommunicator
from Core.constants import DEVICE_STATUS
from Core.exceptions.devices import BaseDeviceException, DefectiveDeviceException, SetupDeviceException, \
    InactiveDeviceException


class AbstractDevice(object):
    """
    Device class with base method `exec_command`

    """
    communicator: AbstractCommunicator = None

    def __init__(
            self,
            communicator=None,
    ):
        if communicator is not None:
            self.communicator: AbstractCommunicator = communicator
        self._last_command = None
        self._status = DEVICE_STATUS.INACTIVE
        self._errors = []

    def setup(self):
        try:
            self.communicator.setup()
            self._status = DEVICE_STATUS.ACTIVE
        except Exception as e:
            self._status = DEVICE_STATUS.HAS_ERRORS
            self._errors.append(e)
            raise SetupDeviceException from e

    def is_valid(self, raise_exception=True):
        e = None
        if self._status == DEVICE_STATUS.INACTIVE:
            e = InactiveDeviceException()
            self._errors.append(e)
        elif self._status == DEVICE_STATUS.HAS_ERRORS:
            if bool(self._errors):
                e = self._errors[-1]
            else:
                self._status = DEVICE_STATUS.ACTIVE

        if e is not None and raise_exception:
            raise e

        return not bool(self._errors)

    # def on/off/
    def exec_command(self, command, value=None):
        """
        Main function for execution user commands
        :param command:
        :param value:
        :return:
        """
        self.is_valid()

        self._last_command = command
        try:
            preprocessing_value = self._preprocessing_value(command, value)
            answer = self.communicator.send(preprocessing_value)

            return self._postprocessing_value(answer)

        except Exception as e:
            return self._handle_exception(e)

    def _handle_exception(self, e: Exception):
        raise BaseDeviceException from e

    def _handle_device_exception(self, e: BaseDeviceException):
        raise e

    def _preprocessing_value(self, command, value):
        """
        Connect command with value to one meaning to send for communication interface
        :param command:
        :param value:
        :return:
        """
        return f"{command}_{value}"

    def _postprocessing_value(self, value):
        return value
