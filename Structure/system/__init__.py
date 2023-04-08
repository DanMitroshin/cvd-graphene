import gc

from .system_actions import ChangeGasValveStateAction, ChangeAirValveStateAction
from coregraphene.components.controllers import (
    AbstractController,
    AccurateVakumetrController,
    ValveController,
    CurrentSourceController,
)
from coregraphene.system import BaseSystem
from coregraphene.conf import settings
from coregraphene.utils import get_available_usb_ports

VALVES_CONFIGURATION = settings.VALVES_CONFIGURATION
LOCAL_MODE = settings.LOCAL_MODE


class AppSystem(BaseSystem):

    def _determine_attributes(self):
        used_ports = []
        self.vakumetr_port = None
        return
        # self.rrg_port = None
        # self.termodat_port = None
        self._ports_attr_names = {
            'vakumetr': 'vakumetr_port',
        }
        self._controllers_check_classes = {
            'vakumetr': AccurateVakumetrController,
        }

        usb_ports = get_available_usb_ports()
        if LOCAL_MODE:
            usb_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
        print("PORTS USB:", usb_ports)
        for controller_code, controller_class in self._controllers_check_classes.items():
            for port in usb_ports:  # ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']:
                if port in used_ports:
                    continue
                controller: AbstractController = controller_class(port=port)
                controller.setup()
                is_good = controller.check_command()
                if is_good:
                    setattr(self, self._ports_attr_names[controller_code], port)
                    used_ports.append(port)
                    break

                controller.destructor()
                del controller

        print(
            "|> FOUND PORTS:",
            "vakumetr:", self.vakumetr_port,
            # "rrg:", self.rrg_port,
            # "termodat:", self.termodat_port
        )
        assert self.vakumetr_port is not None
        # assert self.rrg_port is not None
        # assert self.termodat_port is not None

        self.ports = {
            'vakumetr': self.vakumetr_port,
            # 'rrg': self.rrg_port,
            # 'termodat': self.termodat_port,
        }

        gc.collect()

    def _init_controllers(self):
        self.accurate_vakumetr_controller = AccurateVakumetrController(
            get_potential_port=self.get_potential_controller_port,
            port_communicator=settings.ACCURATE_VAKUMETR_COMMUNICATOR_PORT,
            port=self.vakumetr_port,
            active=False,
        )

        self.air_valve_controller = ValveController(
            port=settings.AIR_VALVE_CONFIGURATION['PORT'],
        )

        self._valves = {}
        # for valve_conf in VALVES_CONFIGURATION:
        #     self._valves[valve_conf["NAME"]] = ValveController(port=valve_conf["PORT"])
        for i, valve_conf in enumerate(VALVES_CONFIGURATION):
            self._valves[i] = ValveController(port=valve_conf["PORT"])

        self.current_source_controller = CurrentSourceController(
            port=settings.CURRENT_SOURCE_USB_PORT,
            port_communicator=settings.CURRENT_SOURCE_COMMUNICATOR_PORT,
            baudrate=settings.CURRENT_SOURCE_BAUDRATE,
            on_change_current=self.on_change_current,
            on_change_voltage=self.on_change_voltage,
            on_set_current=None,  # ДОБАВИТЬ РЕАЛЬНОЕ ВЛИЯНИЕ - ПРОСТОЕ ВЫСТАВЛЕНИЕ АКТУАЛЬНОГО ЗНАЧЕНИЯ В UI
        )

        self._controllers: list[AbstractController] = [
            self.accurate_vakumetr_controller,
            self.current_source_controller,
        ]

        for valve in self._valves.values():
            self._controllers.append(valve)

    def _init_actions(self):
        super()._init_actions()

        # ===== Valves ===== #
        self.change_gas_valve_opened = ChangeGasValveStateAction(system=self)
        self.change_air_valve_opened = ChangeAirValveStateAction(system=self)

    def _init_values(self):
        self.accurate_vakumetr_value = 0.0
        self.current_value = 0.0
        self.voltage_value = 0.0

    def check_conditions(self):
        return True

    def log_state(self):
        pass
        # for controller in self._controllers:
        #     value = controller.get_value()

    # @BaseSystem.action
    # def change_valve_state(self, gas):
    #     # t = Thread(target=self.long_function)
    #     # t.start()
    #     # return 1
    #     valve = self._valves.get(gas, None)
    #     if valve is None:
    #         return False
    #     return valve.change_state()

    def _change_valve_state(self, valve, name):
        new_state = valve.change_state()
        # print(f"Valve {name} new state: {new_state}")
        return new_state

    @BaseSystem.action
    def change_valve_state(self, gas_num):
        valve = self._valves.get(gas_num, None)
        if valve is None:
            return False
        return self._change_valve_state(valve, gas_num)

    @BaseSystem.action
    def change_air_valve_state(self):
        return self._change_valve_state(self.air_valve_controller, "AIR")

    def on_change_current(self, value):
        self.current_value = value

    def on_change_voltage(self, value):
        self.voltage_value = value

    @BaseSystem.action
    def set_current(self, value):
        return self.current_source_controller.set_current_value(value)

    def _get_values(self):
        # pass
        # self.accurate_vakumetr_value = self.accurate_vakumetr_controller.get_value()
        self.accurate_vakumetr_value = self.accurate_vakumetr_controller.vakumetr_value
        # self.current_value = self.current_source_controller.get_current_value()
        # self.voltage_value = self.current_source_controller.get_voltage_value()
        # print("VOLT VAL:", self.voltage_value)
