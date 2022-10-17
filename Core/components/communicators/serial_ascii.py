from .base import AbstractCommunicator
from ..communication_methods import SerialAsciiCommunicationMethod
from ...settings import LOCAL_MODE


class SerialAsciiCommunicator(AbstractCommunicator):
    communication_method_class = SerialAsciiCommunicationMethod
    ADDRESS_PORT_LEN = 3

    def _preprocessing_value(self, value="MV00"):
        return f"{str(self.port).zfill(self.ADDRESS_PORT_LEN)}0{value}D\r"

    def _postprocessing_value(self, value: str):
        answer = value.split('\r')[0]
        if len(answer) < 8:
            return ""
        ans_length = int(answer[6:8])
        return answer[8:8 + ans_length]


class SerialAsciiAkipCommunicator(AbstractCommunicator):
    communication_method_class = SerialAsciiCommunicationMethod
    ADDRESS_PORT_LEN = 3

    def _preprocessing_value(self, value="MV00"):
        return f"A{str(self.port).zfill(self.ADDRESS_PORT_LEN)}{value};\n"

    def _postprocessing_value(self, value: str):
        if LOCAL_MODE:
            return ""
        return value.strip()
