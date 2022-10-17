from .base import AbstractDevice
from ..communicators import SerialAsciiAkipCommunicator
from ...settings import CURRENT_SOURCE_PORT


class CurrentSourceDevice(AbstractDevice):
    def __init__(self):
        super().__init__()
        self.communicator = SerialAsciiAkipCommunicator(port=CURRENT_SOURCE_PORT)

    def _preprocessing_value(self, command, value):
        return f"{command} {value}".strip()
