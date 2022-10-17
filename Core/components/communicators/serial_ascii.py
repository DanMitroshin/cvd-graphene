from .base import AbstractCommunicator
from ..communication_methods import SerialAsciiCommunicationMethod


class SerialAsciiCommunicator(AbstractCommunicator):
    communication_method_class = SerialAsciiCommunicationMethod

    def _preprocessing_value(self, value="MV00"):
        return f"{str(self.port).zfill(3)}0{value}D\r"

    def _postprocessing_value(self, value: str):
        answer = value.split('\r')[0]
        if len(answer) < 8:
            return ""
        ans_length = int(answer[6:8])
        return answer[8:8 + ans_length]
