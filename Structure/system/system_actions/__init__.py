from coregraphene.system_actions import ManyDeviceSystemAction, SystemAction


class ChangeAirValveStateAction(SystemAction):
    def _call_function(self, is_open):
        return self._system.air_valve_controller.set_is_open_state(is_open)


class ChangeGasValveStateAction(ManyDeviceSystemAction):
    def _call_function(self, is_open, device_num=None):
        return self._system._valves[device_num].set_is_open_state(is_open)


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
