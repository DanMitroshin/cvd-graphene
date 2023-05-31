from coregraphene.system_effects import ManyDeviceSystemEffect, SystemEffect


class ChangeAirValveStateEffect(SystemEffect):
    def _call_function(self, is_open):
        return self._system.air_valve_controller.set_is_open_state(is_open)


class ChangeGasValveStateEffect(ManyDeviceSystemEffect):
    def _call_function(self, is_open, device_num=None):
        return self._system._valves[device_num].set_is_open_state(is_open)


# =========== PUMP
class ChangePumpValveStateEffect(SystemEffect):
    def _call_function(self, is_open):
        return self._system.pump_valve_controller.set_is_open_state(is_open)


class ChangePumpManageStateEffect(SystemEffect):
    def _call_function(self, is_open):
        return self._system.pump_manage_controller.set_is_open_state(is_open)


# ======== RRG
class SetTargetRrgSccmEffect(ManyDeviceSystemEffect):
    def _call_function(self, sccm, device_num):
        return self._system.rrgs_controller.set_target_sccm(sccm, device_num)


class FullCloseRrgEffect(ManyDeviceSystemEffect):
    def _call_function(self, device_num):
        return self._system.rrgs_controller.full_close(device_num)


class FullOpenRrgEffect(ManyDeviceSystemEffect):
    def _call_function(self, device_num):
        return self._system.rrgs_controller.full_open(device_num)


class SetTargetCurrentEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_target_current(value)


class SetRampSecondsEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_ramp_seconds(int(value))


class SetTargetCurrentRampEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_target_current_ramp_value(value)


class SetIsRampActiveEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_is_ramp_active(value)


class SetIsRampWaitingEffect(SystemEffect):
    def _call_function(self, value):
        return self._system.set_is_ramp_waiting(value)


# TEMPERATURE


class SetTargetTemperatureSystemEffect(SystemEffect):
    def _call_function(self, value):
        print(f'|> New PID target temperature: {value}')
        return self._system.set_target_temperature_value(value)


class SetIsTemperatureRegulationActiveEffect(SystemEffect):
    def _call_function(self, value):
        return value
        # return self._system.set_is_ramp_active(value)

    def _on_get_value(self, value):
        self._system.temperature_regulation = bool(value)
