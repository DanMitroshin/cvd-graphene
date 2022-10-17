from Core.components.communication_methods import BaseCommunicationMethod
from Core.constants import COMMUNICATION_INTERFACE_STATUS
from Core.exceptions.communicators import InactiveCommunicatorException, BaseCommunicatorException
from Core.exceptions.communicators.base import SetupCommunicatorException


class AbstractCommunicator(object):
    communication_method_class: BaseCommunicationMethod = None

    def __init__(
            self,
            speed=None,
            port=None,
    ):
        self.communication_method = self.communication_method_class()
        self.speed = speed
        self.port = port

        self._status = COMMUNICATION_INTERFACE_STATUS.INACTIVE
        self._errors = []
        # self.setup_configuration()

    def setup(self):
        try:
            self._status = COMMUNICATION_INTERFACE_STATUS.ACTIVE
            self.communication_method.setup()
        except Exception as e:
            self._errors.append(e)
            self._status = COMMUNICATION_INTERFACE_STATUS.HAS_ERRORS
            raise SetupCommunicatorException from e

    def is_valid(self, raise_exception=True):
        e = None
        if self._status == COMMUNICATION_INTERFACE_STATUS.INACTIVE:
            e = InactiveCommunicatorException()
            self._errors.append(e)
        elif self._status == COMMUNICATION_INTERFACE_STATUS.HAS_ERRORS:
            if bool(self._errors):
                e = self._errors[-1]
            else:
                self._status = COMMUNICATION_INTERFACE_STATUS.ACTIVE

        if e is not None and raise_exception:
            raise e

        return not bool(self._errors)

    def send(self, value, raise_exception=True):
        """
        preprocess value -> send value -> get answer -> answer processing ->
        1. has mistakes -> raise error
        2. all oKey -> return value
        :return:
        """
        self.is_valid(raise_exception=raise_exception)

        try:
            preprocessing_value = self._preprocessing_value(value)
            answer = self.communication_method.send(preprocessing_value)

            return self._postprocessing_value(answer)

        except Exception as e:
            return self._handle_exception(e)

    def _preprocessing_value(self, value):
        return value

    def _postprocessing_value(self, value):
        """
        Is answer is oKey?
        1. Answer OK ? -> _extract_value
        2. Else -> _handle_exception
        :return:
        """
        return value

    def _handle_exception(self, e):
        raise BaseCommunicatorException from e
