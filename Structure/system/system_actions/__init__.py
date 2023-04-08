from coregraphene.system_actions import ManyDeviceSystemAction, SystemAction


class ChangeAirValveStateAction(SystemAction):
    def _call_function(self, is_open):
        return self._system.air_valve_controller.set_is_open_state(is_open)


class ChangeGasValveStateAction(ManyDeviceSystemAction):
    def _call_function(self, is_open, device_num=None):
        # print("Valve call...", is_open, device_num)
        ans = self._system._valves[device_num].set_is_open_state(is_open)
        # print("Valve call 2...", is_open, device_num, ans)
        return ans
