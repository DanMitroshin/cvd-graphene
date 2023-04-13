import gc
import random
import time
from threading import Thread, get_ident, Lock

from Core.actions.actions import RampAction
from coregraphene.auto_actions import BaseThreadAction
from coregraphene.system_actions import SingleAnswerSystemAction
from .system_actions import ChangeGasValveStateAction, ChangeAirValveStateAction, SetTargetCurrentAction, \
    SetRampSecondsAction, SetTargetCurrentRampAction, SetIsRampActiveAction, SetIsRampWaitingAction, \
    SetTargetRrgSccmAction, FullCloseRrgAction, FullOpenRrgAction
from coregraphene.components.controllers import (
    AbstractController,
    AccurateVakumetrController,
    ValveController,
    CurrentSourceController, PyrometerTemperatureController, SeveralRrgAdcDacController, DigitalFuseController,
)
from coregraphene.system import BaseSystem
from coregraphene.conf import settings
from coregraphene.utils import get_available_usb_ports

VALVES_CONFIGURATION = settings.VALVES_CONFIGURATION
LOCAL_MODE = settings.LOCAL_MODE


class AppSystem(BaseSystem):
    current_value = 0.0
    voltage_value = 0.0
    target_current_value = 0.0
    target_current_ramp_value = 0.0
    ramp_seconds = 0
    ramp_active = False
    ramp_waiting = False
    ramp_lock = Lock()

    def _determine_attributes(self):
        used_ports = []
        self.vakumetr_port = settings.ACCURATE_VAKUMETR_USB_PORT
        self.current_source_port = settings.CURRENT_SOURCE_USB_PORT
        self.pyrometer_temperature_port = settings.PYROMETER_TEMPERATURE_USB_PORT
        # return
        # self.rrg_port = None
        # self.termodat_port = None
        self._ports_attr_names = {
            'vakumetr': 'vakumetr_port',
            'current_source': 'current_source_port',
            'pyrometer': 'pyrometer_temperature_port',
        }
        self._controllers_check_classes = {
            'vakumetr': AccurateVakumetrController,
            'current_source': CurrentSourceController,
            'pyrometer': PyrometerTemperatureController,
        }

        self._default_controllers_kwargs = {
            'vakumetr': {
                'port_communicator': settings.ACCURATE_VAKUMETR_COMMUNICATOR_PORT,
            },
            'current_source': {
                'port_communicator': settings.CURRENT_SOURCE_COMMUNICATOR_PORT,
            },
        }

        usb_ports = get_available_usb_ports()
        if LOCAL_MODE:
            usb_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
        print("PORTS USB:", usb_ports)
        for controller_code, controller_class in self._controllers_check_classes.items():
            for port in usb_ports:  # ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']:
                if port in used_ports:
                    continue
                controller: AbstractController = controller_class(
                    port=port,
                    **self._default_controllers_kwargs.get(controller_code, {})
                )
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
            'current_source:', self.current_source_port,
            "pyrometer", self.pyrometer_temperature_port,
        )
        assert self.vakumetr_port is not None
        assert self.current_source_port is not None
        assert self.pyrometer_temperature_port is not None

        self.ports = {
            'vakumetr': self.vakumetr_port,
            'current_source': self.current_source_port,
            'pyrometer': self.pyrometer_temperature_port,
        }

        gc.collect()

    def _init_controllers(self):
        self.accurate_vakumetr_controller = AccurateVakumetrController(
            get_potential_port=self.get_potential_controller_port,
            port_communicator=settings.ACCURATE_VAKUMETR_COMMUNICATOR_PORT,
            baudrate=settings.ACCURATE_VAKUMETR_BAUDRATE,
            port=self.vakumetr_port,
            # active=False,
        )
        self.pyrometer_temperature_controller = PyrometerTemperatureController(
            get_potential_port=self.get_potential_controller_port,
            baudrate=settings.PYROMETER_TEMPERATURE_BAUDRATE,
            port=self.pyrometer_temperature_port,
        )

        self.air_valve_controller = ValveController(
            port=settings.AIR_VALVE_CONFIGURATION['PORT'],
        )

        self._valves = {}
        # for valve_conf in VALVES_CONFIGURATION:
        #     self._valves[valve_conf["NAME"]] = ValveController(port=valve_conf["PORT"])
        for i, valve_conf in enumerate(VALVES_CONFIGURATION):
            self._valves[i] = ValveController(port=valve_conf["PORT"])

        # RRG_SPI_READ_CHANNEL = 0
        # RRG_SPI_WRITE_CHANNEL = 1
        # RRG_SPI_SPEED = 20000
        # RRG_SPI_READ_DEVICE = 0
        # RRG_SPI_WRITE_DEVICE = 0

        self.rrgs_controller = SeveralRrgAdcDacController(
            config=VALVES_CONFIGURATION,
            read_channel=settings.RRG_SPI_READ_CHANNEL,
            write_channel=settings.RRG_SPI_WRITE_CHANNEL,
            speed=settings.RRG_SPI_SPEED,
            read_device=settings.RRG_SPI_READ_DEVICE,
            write_device=settings.RRG_SPI_WRITE_DEVICE,
        )

        self._digital_fuses = {}
        for i, port in enumerate(settings.DIGITAL_FUSE_PORTS):
            self._digital_fuses[i] = DigitalFuseController(port=port)

        self.current_source_controller = CurrentSourceController(
            port=self.current_source_port,
            port_communicator=settings.CURRENT_SOURCE_COMMUNICATOR_PORT,
            baudrate=settings.CURRENT_SOURCE_BAUDRATE,
            active=True,
        )

        self._controllers: list[AbstractController] = [
            self.accurate_vakumetr_controller,
            self.air_valve_controller,
            self.pyrometer_temperature_controller,
            self.rrgs_controller,
            self.current_source_controller,
        ]

        for valve in self._valves.values():
            self._controllers.append(valve)

        for fuse in self._digital_fuses.values():
            self._controllers.append(fuse)

    def _init_actions(self):
        super()._init_actions()

        # ===== Valves ======== #
        self.change_gas_valve_opened = ChangeGasValveStateAction(system=self)
        self.change_air_valve_opened = ChangeAirValveStateAction(system=self)

        # ===== RRG =========== #
        self.set_target_rrg_sccm_action = SetTargetRrgSccmAction(system=self)
        self.full_close_rrg_action = FullCloseRrgAction(system=self)
        self.full_open_rrg_action = FullOpenRrgAction(system=self)

        self.get_current_rrg_sccm = SingleAnswerSystemAction(system=self)
        self.rrgs_controller.get_current_flow.connect(self.get_current_rrg_sccm)

        # ===== Pyrometer ===== #
        self.set_current_temperature = SingleAnswerSystemAction(system=self)
        self.set_current_temperature.connect(self._on_get_current_temperature)
        self.pyrometer_temperature_controller.get_temperature_action \
            .connect(self.set_current_temperature)

        # ===== Pyrometer ===== #
        # A lot of...

        # ===== Current AKIP == #
        self.set_target_current_action = SetTargetCurrentAction(system=self)

        self.get_current_action = SingleAnswerSystemAction(system=self)
        self.get_current_action.connect(self._on_get_actual_current)
        self.current_source_controller.get_current_action.connect(self.get_current_action)

        self.get_voltage_action = SingleAnswerSystemAction(system=self)
        self.get_voltage_action.connect(self._on_get_actual_voltage)
        self.current_source_controller.get_voltage_action.connect(self.get_voltage_action)

        self.set_ramp_seconds_action = SetRampSecondsAction(system=self)
        self.set_target_current_ramp_action = SetTargetCurrentRampAction(system=self)

        self.set_is_active_ramp_action = SetIsRampActiveAction(system=self)
        self.set_is_waiting_ramp_action = SetIsRampWaitingAction(system=self)

        #########################

    def _init_values(self):
        self.accurate_vakumetr_value = 0.0
        self.pyrometer_temperature_value = 0.0
        # self.current_value = 0.0
        # self.voltage_value = 0.0

    def pause_test(self):
        secs = random.random() * 20 + 5
        time.sleep(secs)
        print("I SLEEP", secs, "ident:", get_ident())

    def test_ramp(self):
        arr = []
        for _ in range(30):
            th = Thread(target=self.pause_test)
            th.start()
            # th.is_alive()
            # time.sleep(1)
            arr.append(th)
        # pops = []
        while arr:
            for i, thread in enumerate(arr):
                if not thread.is_alive():
                    thread.join()
                    print('TH NAME JOINED:', thread.getName())
                    arr.pop(i)
                    break
            time.sleep(0.2)
        print("ENDING!")

    def on_ramp_press_start(self, *args):
        try:
            if self.ramp_waiting:
                return
            self.set_is_waiting_ramp_action(True)
            if self.ramp_active:
                self.ramp_active = False
                return

            thread_action = BaseThreadAction(
                system=self,
                action=RampAction,
            )
            thread_action.set_action_args(
                self.target_current_ramp_value,
                f"0:{self.ramp_seconds}"
            )
            thread_action.action.is_stop_state_function = self._ramp_is_stop_function
            self._add_action_to_loop(thread_action=thread_action)

        except Exception as e:
            print("ERR RAMP START:", e)

    def _ramp_is_stop_function(self):
        return not (self.is_working() and self.ramp_active)

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

    @BaseSystem.action
    def set_target_current(self, value):
        return self.current_source_controller.set_target_current(value)

    def _on_get_current_temperature(self, value):
        self.pyrometer_temperature_value = value

    def _on_get_actual_current(self, value):
        self.current_value = value

    def _on_get_actual_voltage(self, value):
        self.voltage_value = value

    def set_ramp_seconds(self, value):
        try:
            self.ramp_seconds = int(value)
        except:
            self.ramp_seconds = 0
        return self.ramp_seconds

    def set_target_current_ramp_value(self, value):
        try:
            self.target_current_ramp_value = float(value)
        except:
            self.target_current_ramp_value = 0.0
        return self.target_current_ramp_value

    def set_is_ramp_active(self, value):
        self.ramp_active = bool(value)
        # self.ramp_waiting = False
        self.set_is_waiting_ramp_action(False)
        return self.ramp_active

    def set_is_ramp_waiting(self, value):
        self.ramp_waiting = bool(value)
        return self.ramp_waiting

    def _get_values(self):
        # pass
        # self.accurate_vakumetr_value = self.accurate_vakumetr_controller.get_value()
        self.accurate_vakumetr_value = self.accurate_vakumetr_controller.vakumetr_value
        # self.current_value = self.current_source_controller.get_current_value()
        # self.voltage_value = self.current_source_controller.get_voltage_value()
        # print("VOLT VAL:", self.voltage_value)
