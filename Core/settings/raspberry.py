from Core.utils import get_serial_port


SERIAL_PORT = get_serial_port()

ACCURATE_VAKUMETR_PORT = 1
ACCURATE_VAKUMETR_USB_PORT = '/dev/ttyUSB1'
CURRENT_SOURCE_PORT = 3

VALVES_CONFIGURATION = [
    {'PORT': 7, "NAME": "O_2"}
]
