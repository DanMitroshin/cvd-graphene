from Core.constants import COMMUNICATION_INTERFACE_STATUS


class AbstractCommunicator(object):
    def __init__(
            self,
            speed=None,
            channel=None,
    ):
        self.speed = speed
        self.channel = channel  # port
        self._status = COMMUNICATION_INTERFACE_STATUS.INACTIVE
        self.setup_configuration()

    def setup_configuration(self):
        self._status = COMMUNICATION_INTERFACE_STATUS.ACTIVE

    def send(self, value):
        """
        preprocess value -> send value -> get answer -> answer processing ->
        1. has mistakes -> raise error
        2. all oKey -> return value
        :return:
        """
        pass

    def _preprocessing_value(self, value):
        pass

    def _process_answer(self):
        """
        Is answer is oKey?
        1. Answer OK ? -> _extract_value
        2. Else -> _handle_exception
        :return:
        """
        pass

    def _extract_value(self):
        """

        :return: value from receiving answer
        """
        pass

    def _handle_exception(self):
        pass
