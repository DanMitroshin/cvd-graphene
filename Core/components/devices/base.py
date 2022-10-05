from Core.components.communicators import AbstractCommunicator
from Core.constants import DEVICE_STATUS
from Core.exceptions.communicators import BaseCommunicatorException
from Core.exceptions.devices import BaseDeviceException, DefectiveDeviceException


class AbstractDevice(object):
    """
    Device class with base method `exec_command`

    """
    def __init__(
            self,
            communication_interface=None,
    ):
        self.communication_interface: AbstractCommunicator = communication_interface
        self._last_command = None
        self._status = DEVICE_STATUS.INACTIVE
        self._errors = []

    def _setup_device(self):
        try:
            self.communication_interface.setup_configuration()
            self._status = DEVICE_STATUS.ACTIVE
        except Exception as e:
            self._status = DEVICE_STATUS.HAS_ERRORS
            self._errors.append(SavedError(e, description="Device setup error"))

    # def on/off/
    def exec_command(self, command, value=None):
        """
        Main function for execution user commands
        :param command:
        :param value:
        :return:
        """
        if self._status == DEVICE_STATUS.HAS_ERRORS:
            raise DefectiveDeviceException

        self._last_command = command
        try:
            preprocessing_value = self._preprocessing_value(command, value)
            answer = self.communication_interface.send(preprocessing_value)

            return self._postprocessing_value(answer)

        except BaseDeviceException as e:
            return self._handle_device_exception(e)
        except BaseCommunicatorException as e:
            return self._handle_interface_exception(e)
        except Exception as e:
            raise e

    def _handle_interface_exception(self, e: BaseCommunicatorException):
        raise e

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
