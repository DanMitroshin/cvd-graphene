from coregraphene.system_actions import ManyDeviceSystemAction, SystemAction


class ChangeAirValveStateAction(SystemAction):
    def _call_function(self, is_open):
        return self._system.air_valve_controller.set_is_open_state(is_open)


class ChangeGasValveStateAction(ManyDeviceSystemAction):
    def _call_function(self, is_open, device_num=None):
        return self._system._valves[device_num].set_is_open_state(is_open)
