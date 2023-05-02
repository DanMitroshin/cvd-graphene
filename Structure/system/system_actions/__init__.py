from coregraphene.system_actions import ManyDeviceSystemAction, SystemAction


class ChangeAirValveStateAction(SystemAction):
    def _call_function(self, is_open):
        return self._system.air_valve_controller.set_is_open_state(is_open)


class ChangeGasValveStateAction(ManyDeviceSystemAction):
    def _call_function(self, is_open, device_num=None):
        return self._system._valves[device_num].set_is_open_state(is_open)


# =========== PUMP
class ChangePumpValveStateAction(SystemAction):
    def _call_function(self, is_open):
        return self._system.pump_valve_controller.set_is_open_state(is_open)


class ChangePumpManageStateAction(SystemAction):
    def _call_function(self, is_open):
        return self._system.pump_manage_controller.set_is_open_state(is_open)


# ======== RRG
class SetTargetRrgSccmAction(ManyDeviceSystemAction):
    def _call_function(self, sccm, device_num):
        return self._system.rrgs_controller.set_target_sccm(sccm, device_num)


class FullCloseRrgAction(ManyDeviceSystemAction):
    def _call_function(self, device_num):
        return self._system.rrgs_controller.full_close(device_num)


class FullOpenRrgAction(ManyDeviceSystemAction):
    def _call_function(self, device_num):
        return self._system.rrgs_controller.full_open(device_num)


class SetTargetCurrentAction(SystemAction):
    def _call_function(self, value):
        return self._system.set_target_current(value)


class SetRampSecondsAction(SystemAction):
    def _call_function(self, value):
        return self._system.set_ramp_seconds(int(value))


class SetTargetCurrentRampAction(SystemAction):
    def _call_function(self, value):
        return self._system.set_target_current_ramp_value(value)


class SetIsRampActiveAction(SystemAction):
    def _call_function(self, value):
        return self._system.set_is_ramp_active(value)


class SetIsRampWaitingAction(SystemAction):
    def _call_function(self, value):
        return self._system.set_is_ramp_waiting(value)


# TEMPERATURE


class SetTargetTemperatureSystemAction(SystemAction):
    def _call_function(self, value):
        return self._system.set_target_temperature_value(value)


class SetIsTemperatureRegulationActiveAction(SystemAction):
    def _call_function(self, value):
        return value
        # return self._system.set_is_ramp_active(value)

    def _on_get_value(self, value):
        self._system.temperature_regulation = bool(value)
