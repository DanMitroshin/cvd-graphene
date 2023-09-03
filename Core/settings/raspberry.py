# from Core.utils import get_serial_port
#
#
# SERIAL_PORT = get_serial_port()
MAX_RECIPE_STEP_SECONDS = 60 * 60 * 24 * 2  # set to None for remove limit for step time

# ACCURATE_VAKUMETR_PORT = 1
ACCURATE_VAKUMETR_COMMUNICATOR_PORT = 1
# ACCURATE_VAKUMETR_USB_PORT = '/dev/ttyUSB1'  # FOR CVD-GRAPHENE USE USB1 (?)
ACCURATE_VAKUMETR_USB_PORT = '1-1.4.4'  # порт по usb (хаб или отдельно -- неважно),
# команда для определения: sudo dmesg | grep ttyUSB | grep usb
ACCURATE_VAKUMETR_BAUDRATE = 115200  # FOR CVD-GRAPHENE USE USB1 (?)

# CURRENT_SOURCE_USB_PORT = '/dev/ttyUSB0'
CURRENT_SOURCE_USB_PORT = '1-1.4.1.2'
CURRENT_SOURCE_BAUDRATE = 115200
CURRENT_SOURCE_COMMUNICATOR_PORT = 3

# PYROMETER_TEMPERATURE_USB_PORT = '/dev/ttyUSB2'
PYROMETER_TEMPERATURE_USB_PORT = '1-1.4.1.3'
PYROMETER_TEMPERATURE_BAUDRATE = 19200

# BACK_PRESSURE_VALVE_USB_PORT = '/dev/ttyUSB3'
BACK_PRESSURE_VALVE_USB_PORT = '1-1.4.3'  # Mb pyrometr
BACK_PRESSURE_VALVE_BAUDRATE = 9600

BH_RRG_CONTROLLER_USB_PORT = '1-1.4.3'

AIR_VALVE_CONFIGURATION = {
    'PORT': 17, "NAME": "Air",
}
AIR_VALVE_NAME = AIR_VALVE_CONFIGURATION['NAME']

PUMP_CONFIGURATION = {
    'MANAGE_PORT': 1,  # порт управления (вкл/выкл)
    'VALVE_PORT': 18,  # открыть/закрыть клапан перед насосом
    "NAME": 'Pump',
}

MAX_DEFAULT_SCCM_VALUE = 200

RRG_SPI_READ_CHANNEL = 0
RRG_SPI_WRITE_CHANNEL = 1
RRG_SPI_SPEED = 20000
RRG_SPI_READ_DEVICE = 1  # Potential vakumetr port
RRG_SPI_WRITE_DEVICE = 0  # ONLY 0 because we have only one instrument for write using spi

VAKUMETR_SPI_READ_CHANNEL = 0
VAKUMETR_SPI_SPEED = 20000
VAKUMETR_SPI_READ_DEVICE = 0

DIGITAL_FUSE_PORTS = [5, 22, 6, 27]

VALVES_CONFIGURATION = [
    {
        "NAME": "Ar",
        'PORT': 3,  # GPIO PORT FOR RELE
        "IS_GAS": True,
        "MAX_SCCM": 200.0,  # NOT NECESSARY, IF NOT PROVIDED, WILL BE USED `MAX_DEFAULT_SCCM_VALUE`
        'ADDRESS': 0,  # RRG ADDRESS FOR SPI (from 0 to 7: 000, 001, ..., 111)
        'DAC_ADDRESS': 0,  # RRG ADDRESS FOR SPI DAC [SET VALUE] (from 0 to 7: 000, 001, ..., 111)
        'VAKUMETR_ADDRESS': 0,  # VAKUMETR ADDRESS FOR READING PRESSURE IN BALLOON
    },
    {
        'PORT': 25, "NAME": "C_2H_2", "IS_GAS": True,
        'ADDRESS': 2, 'DAC_ADDRESS': 2, 'VAKUMETR_ADDRESS': 2,
    },
    {
        'PORT': 24, "NAME": "CH_4", "IS_GAS": True,
        'ADDRESS': 1, 'DAC_ADDRESS': 1, 'VAKUMETR_ADDRESS': 4,
    },
    {
        'PORT': 4, "NAME": "N_2", "IS_GAS": True,
        'ADDRESS': 3, 'DAC_ADDRESS': 3, 'VAKUMETR_ADDRESS': 3,
    },
    {
        'PORT': 23, "NAME": "H_2", "IS_GAS": True,
        'ADDRESS': 4, 'DAC_ADDRESS': 7, 'VAKUMETR_ADDRESS': 5,
    },
    # {'PORT': 7, "NAME": "O_2", "IS_GAS": True},
    # {'PORT': 8, "NAME": "N_2", "IS_GAS": True},
    # {'PORT': 9, "NAME": "Ar", "IS_GAS": True},
]

ALL_GPIO_VALVES_CONFIG = VALVES_CONFIGURATION + \
                         [AIR_VALVE_CONFIGURATION] + \
                         [PUMP_CONFIGURATION]

# VALVE_LIST = list(map(lambda x: x.get('NAME'), VALVES_CONFIGURATION))
VALVE_LIST = list(map(lambda x: x.get('NAME'), ALL_GPIO_VALVES_CONFIG))
# GAS_LIST = list(map(lambda x: x.get('NAME'), filter(lambda x: x.get("IS_GAS", False), VALVES_CONFIGURATION)))
GAS_LIST = list(map(lambda x: x.get('NAME'), VALVES_CONFIGURATION))

TABLE_COLUMN_NAMES = ["Процесс", "Аргумент 1", "Аргумент 2", "Аргумент 3", "Комментарий"]
