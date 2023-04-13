# from Core.utils import get_serial_port
#
#
# SERIAL_PORT = get_serial_port()
MAX_RECIPE_STEP_SECONDS = 60 * 60 * 24 * 2  # set to None for remove limit for step time

# ACCURATE_VAKUMETR_PORT = 1
ACCURATE_VAKUMETR_COMMUNICATOR_PORT = 1
ACCURATE_VAKUMETR_USB_PORT = '/dev/ttyUSB1'  # FOR CVD-GRAPHENE USE USB1 (?)
ACCURATE_VAKUMETR_BAUDRATE = 115200  # FOR CVD-GRAPHENE USE USB1 (?)

# CURRENT_SOURCE_PORT = '/dev/ttyUSB0'  # 3
CURRENT_SOURCE_USB_PORT = '/dev/ttyUSB0'
CURRENT_SOURCE_BAUDRATE = 115200
CURRENT_SOURCE_COMMUNICATOR_PORT = 3

PYROMETER_TEMPERATURE_USB_PORT = '/dev/ttyUSB2'
PYROMETER_TEMPERATURE_BAUDRATE = 19200

AIR_VALVE_CONFIGURATION = {
    'PORT': 3, "NAME": "Air",
}
AIR_VALVE_NAME = AIR_VALVE_CONFIGURATION['NAME']

PUMP_CONFIGURATION = {
    'MANAGE_PORT': 1,  # порт управления (вкл/выкл)
    'VALVE_PORT': 18,  # открыть/закрыть клапан перед насосом
    "NAME": 'PUMP',
}

MAX_DEFAULT_SCCM_VALUE = 200

RRG_SPI_READ_CHANNEL = 0
RRG_SPI_WRITE_CHANNEL = 1
RRG_SPI_SPEED = 20000
RRG_SPI_READ_DEVICE = 0
RRG_SPI_WRITE_DEVICE = 0

DIGITAL_FUSE_PORTS = [5, 22, 6, 27]

VALVES_CONFIGURATION = [
    {
        "NAME": "O_2",
        'PORT': 25,  # GPIO PORT FOR RELE
        "IS_GAS": True,
        "MAX_SCCM": 200.0,  # NOT NECESSARY, IF NOT PROVIDED, WILL BE USED `MAX_DEFAULT_SCCM_VALUE`
        'ADDRESS': 0,  # RRG ADDRESS FOR SPI (from 0 to 7: 000, 001, ..., 111)
     },
    {'PORT': 17, "NAME": "N_2", "IS_GAS": True, 'ADDRESS': 1, },
    {'PORT': 24, "NAME": "Ar", "IS_GAS": True, 'ADDRESS': 2, },
    {'PORT': 4, "NAME": "C_2", "IS_GAS": True, 'ADDRESS': 3, },
    {'PORT': 23, "NAME": "F_2", "IS_GAS": True, 'ADDRESS': 4, },
    # {'PORT': 7, "NAME": "O_2", "IS_GAS": True},
    # {'PORT': 8, "NAME": "N_2", "IS_GAS": True},
    # {'PORT': 9, "NAME": "Ar", "IS_GAS": True},
    # {'PORT': 10, "NAME": "C_2", "IS_GAS": True},
    # {'PORT': 11, "NAME": "F_2", "IS_GAS": True},
    # {'PORT': 12, "NAME": "PUMP", "IS_GAS": False},
    # {'PORT': 13, "NAME": "AIR", "IS_GAS": False},
]

ALL_GPIO_VALVES_CONFIG = VALVES_CONFIGURATION + [AIR_VALVE_CONFIGURATION]

# VALVE_LIST = list(map(lambda x: x.get('NAME'), VALVES_CONFIGURATION))
VALVE_LIST = list(map(lambda x: x.get('NAME'), ALL_GPIO_VALVES_CONFIG))
# GAS_LIST = list(map(lambda x: x.get('NAME'), filter(lambda x: x.get("IS_GAS", False), VALVES_CONFIGURATION)))
GAS_LIST = list(map(lambda x: x.get('NAME'), VALVES_CONFIGURATION))


TABLE_COLUMN_NAMES = ["Процесс", "Аргумент 1", "Аргумент 2", "Аргумент 3", "Комментарий"]
