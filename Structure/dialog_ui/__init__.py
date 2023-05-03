from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from Core.actions import ACTIONS
from .MainBlockWidget import MainBlockWidget
# from Structure.dialog_ui.RightButtonsWidget import RightButtonsWidget
# from Structure.dialog_ui.TableWidget import AppTableWidget
# from Structure.dialog_ui.components import LogWidget

from coregraphene.conf import settings
from coregraphene.constants import RECIPE_STATES, RECIPE_STATES_TO_STR, NOTIFICATIONS
from grapheneqtui.structures import BaseMainDialogWindow
from ..system import AppSystem


class AppMainDialogWindow(BaseMainDialogWindow):
    main_interface_widget_class = MainBlockWidget
    system: AppSystem = None

    actions_list = ACTIONS
    recipe_states = RECIPE_STATES
    recipe_states_to_str = RECIPE_STATES_TO_STR
    recipe_table_column_names = settings.TABLE_COLUMN_NAMES
    notifications_configuration = NOTIFICATIONS

    def _init__11__old(self):
        super().__init__()
        self.setWindowTitle("CVD-Graphene")

        ##############################################################################
        ##############################################################################
        ##############################################################################
        ##############################################################################
        ##############################################################################

        # self.system = CvdSystem()
        # self.system.setup()
        # self.system.threads_setup()

        self._recipe_history = []
        self._current_recipe_step = None
        self._recipe_state = RECIPE_STATES.STOP

        self.main_window = QHBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setObjectName("main_widget")
        # self.main_widget.setStyleSheet("background-color: rgb(240, 220, 255);")
        self.main_widget.setStyleSheet(
            "QWidget#main_widget {background-color: rgb(240, 240, 240);}"
        )
        self.main_widget.setLayout(self.main_window)

        self.main_interface_layout_widget = MainBlockWidget(

        )
        self.main_window.addWidget(self.main_interface_layout_widget)

        self.right_buttons_layout_widget = RightButtonsWidget(
            on_close=self.close,
            on_create_recipe=self.on_create_recipe,
            on_open_recipe=self.on_open_recipe,
        )
        self.main_window.addWidget(self.right_buttons_layout_widget)

        # Устанавливаем центральный виджет Window.
        # self.setCentralWidget(container)
        self.setCentralWidget(self.main_widget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_values_and_log_state)
        self.timer.start(500)

        # TABLE WIDGET FOR RECIPE ###################################
        self.table_widget = AppTableWidget(
            parent=self,
            save_recipe_file=self.system.save_recipe_file,
            get_recipe_file_data=self.system.get_recipe_file_data,
            start_recipe=self.start_recipe,
        )

        # LOG NOTIFICATION WIDGET ###################################
        self.log = None
        self.log_widget = LogWidget(on_close=self.clear_log, parent=self)
        self.log_widget.move(100, 100)

        # self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        # self.close()
        ############################################
        # CONNECT FUNCTIONS ########################

        # for gas in self.main_interface_layout_widget.pressure_block.gases:
        #     gas.connect_valve_function(self.system.change_valve_state)
        #
        # self.main_interface_layout_widget.temperature_block.current_settings.set_current_block.\
        #     set_value_function = self.system.set_current

    def connect_controllers_actions(self):
        # GASES #################
        for gas in self.milw.pressure_block.gases:
            num = gas.number

            # gas.connect_valve_function(self.system.change_valve_state)
            gas.update_is_valve_open_signal.connect(
                self.system.change_valve_state)
            # self.system.change_gas_valve_opened.connect(
            #     gas.draw_is_open, device_num=num)
            self.system.change_gas_valve_opened.connect(
                gas.on_update_is_valve_open_signal.emit, device_num=num)

            # gas.connect_change_sccm_function(self.system.set_target_rrg_sccm_effect)
            gas.update_target_sccm_signal.connect(self.system.set_target_rrg_sccm_effect)
            # self.system.set_target_rrg_sccm_effect.connect(
            #     gas.draw_set_target_sccm, device_num=gas.number)
            self.system.set_target_rrg_sccm_effect.connect(
                gas.column_info.update_target_signal.emit, device_num=gas.number)
            # self.system.full_open_rrg_effect.connect(
            #     gas.draw_set_target_sccm, device_num=gas.number)
            self.system.full_open_rrg_effect.connect(
                gas.column_info.update_target_signal.emit, device_num=gas.number)
            # self.system.full_close_rrg_effect.connect(
            #     gas.draw_set_target_sccm, device_num=gas.number)
            self.system.full_close_rrg_effect.connect(
                gas.column_info.update_target_signal.emit, device_num=gas.number)

            # self.system.current_rrg_sccm_effect.connect(
            #     gas.update_current_sccm_label, device_num=gas.number)
            self.system.current_rrg_sccm_effect.connect(
                gas.column_info.update_current_signal.emit, device_num=gas.number)

            # Balloon gas pressure
            self.system.current_gas_balloon_pressure_effect.connect(
                gas.on_update_gas_name_color_by_pressure_signal.emit, device_num=gas.number)

        # AIR #################
        # self.milw.pressure_block.air. \
        #     connect_valve_function(self.system.change_air_valve_state)
        self.milw.pressure_block.air.update_is_valve_open_signal\
            .connect(self.system.change_air_valve_state)
        self.system.change_air_valve_opened.connect(
            self.milw.pressure_block.air.on_update_is_valve_open_signal.emit)
        #######################

        # PUMP ################
        self.milw.pressure_block.pump_block.update_pump_valve_state_signal\
            .connect(self.system.change_pump_valve_state)
        self.system.change_pump_valve_opened_effect.connect(
            self.milw.pressure_block.pump_block.on_update_pump_valve_is_open_signal.emit)

        self.milw.pressure_block.pump_block.update_pump_state_signal\
            .connect(self.system.change_pump_manage_state)
        self.system.change_pump_manage_active_effect.connect(
            self.milw.pressure_block.pump_block.on_update_pump_is_open_signal.emit)

        # << THROTTLE >> #
        self.milw.pressure_block.pump_block.update_throttle_state_signal\
            .connect(self.system.back_pressure_valve_controller.on_change_state)
        self.system.throttle_state_effect.connect(
            self.milw.pressure_block.pump_block.on_update_throttle_state_signal.emit)

        self.system.throttle_current_pressure_effect.connect(
            self.milw.pressure_block.pump_block.throttle_info.update_current_signal.emit)

        self.milw.pressure_block.pump_block.throttle_info.on_update_target_signal \
            .connect(self.system.back_pressure_valve_controller.turn_on_regulation)
        self.system.throttle_target_pressure_effect.connect(
            self.milw.pressure_block.pump_block.throttle_info.update_target_signal.emit)
        #######################

        # CURRENT

        self.milw.temperature_block.current_settings.set_current_block.\
            set_value_function = self.system.set_target_current
        self.system.target_current_effect.connect(
            self.milw.temperature_block.current_settings.set_current_block.set_value
        )

        self.system.actual_current_effect.connect(
            self.milw.temperature_block.current_settings.set_current_value
        )
        self.system.actual_voltage_effect.connect(
            self.milw.temperature_block.current_settings.set_voltage_value
        )
        # RAMP
        # self.milw.temperature_block.current_settings.rise_current_block\
        #     .ramp_button.clicked.connect(self.system.on_ramp_press_start)
        self.milw.temperature_block.current_settings.rise_current_block\
            .on_ramp_press = self.system.on_ramp_press_start
        self.milw.temperature_block.current_settings.rise_current_block\
            .input_current.textEdited.connect(self.system.set_target_current_ramp_value)
        self.milw.temperature_block.current_settings.rise_current_block\
            .input_time.textEdited.connect(self.system.set_ramp_seconds)

        self.system.ramp_seconds_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block.left_time_signal.emit
        )
        self.system.target_current_ramp_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block.target_current_signal.emit
        )
        self.system.is_active_ramp_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block\
                .active_ramp_signal.emit
        )
        self.system.is_waiting_ramp_effect.connect(
            self.milw.temperature_block.current_settings.rise_current_block\
                .waiting_ramp_signal.emit
        )

        # PYROMETER ############
        # self.system.current_temperature_effect.connect(
        #     self.milw.temperature_block.set_actual_temperature
        # )
        self.system.current_temperature_effect.connect(
            self.milw.pressure_control_block.show_temperature.update_temperature_signal.emit
        )
        ########################

        # VAKUMETR #############
        # self.milw.pressure_control_block.show_pressure_block.set_value(
        #     self.system.accurate_vakumetr_value
        # )
        ########################
        # self.system.test_ramp()

    # def on_create_recipe(self):
    #     try:
    #         self.table_widget.on_create_recipe()
    #     except Exception as e:
    #         print("On create recipe function error:", e)
    #
    # def on_open_recipe(self):
    #     try:
    #         file_path = QFileDialog.getOpenFileName(self, 'Выбрать рецепт', '')[0]
    #         if file_path:
    #             data = self.system.get_recipe_file_data(file_path)
    #             self.table_widget.on_open_recipe_file(file_path, data)
    #     except Exception as e:
    #         print("On open recipe error:", e)
    #
    # def close(self) -> bool:
    #     self.system.stop()
    #     return super().close()
    #
    # def clear_log(self, uid):
    #     self.system.clear_log(uid=uid)
    #     self.log = None
    #
    # def __del__(self):
    #     # print("Window del")
    #     self.system.destructor()
    #
    # def click_press(self):
    #     self.counter += 1
    #     self.label.setText(f"PRESSED: {self.counter}")
    #
    # def show_time(self):
    #     print("TIME:", datetime.datetime.now())
    #
    # def start_recipe(self):
    #     try:
    #         recipe = self.table_widget.get_values()
    #         ready = self.system.run_recipe(recipe)
    #         if not ready:
    #             return
    #         self._recipe_history = []
    #         self.add_recipe_step("Инициализация рецепта")
    #         self.table_widget.on_close()
    #         self.main_interface_layout_widget.deactivate_interface()
    #         self.right_buttons_layout_widget.activate_manage_recipe_buttons()
    #     except Exception as e:
    #         print("Start recipe UI error:", e)
    #
    # def add_recipe_step(self, name="---", index=None):
    #     index = index if index else len(self._recipe_history)
    #     if self._current_recipe_step:
    #         if self._current_recipe_step.get('index', -1) == index:
    #             return
    #     self._current_recipe_step = {"name": name, "index": index}
    #     self._recipe_history.append(f"{datetime.datetime.utcnow().time()} [{index}] {name}")
    #     try:
    #         self.main_interface_layout_widget.set_current_step(self._recipe_history[-1])
    #     except:
    #         pass

    def _update_ui_values(self):
        self.milw.pressure_control_block.show_pressure_block.set_value(
            self.system.accurate_vakumetr_value
        )

        # print("VOLTAGE:", self.system.voltage_value)
        # VOLTAGE
        self.main_interface_layout_widget.temperature_block.current_settings.set_voltage_value(
            self.system.voltage_value
        )
        # self.main_interface_layout_widget.temperature_block.current_settings.set_current_value(
        #     self.system.current_value
        # )

    # def get_values_and_log_state(self):
    #     try:
    #
    #         self.system.get_values()
    #         recipe_step = self.system.current_recipe_step
    #         if recipe_step:
    #             self.add_recipe_step(**recipe_step)
    #         recipe_state = self.system.recipe_state
    #         if recipe_state != self._recipe_state:
    #             self._recipe_state = recipe_state
    #             if recipe_state == RECIPE_STATES.STOP:
    #                 self.main_interface_layout_widget.activate_interface()
    #                 self.right_buttons_layout_widget.deactivate_manage_recipe_buttons()
    #
    #
    #         self.main_interface_layout_widget.pressure_control_block.show_pressure_block.set_value(
    #             self.system.accurate_vakumetr_value
    #         )
    #
    #         # print("VOLTAGE:", self.system.voltage_value)
    #         # VOLTAGE
    #         self.main_interface_layout_widget.temperature_block.current_settings.set_voltage_value(
    #             self.system.voltage_value
    #         )
    #         self.main_interface_layout_widget.temperature_block.current_settings.set_current_value(
    #             self.system.current_value
    #         )
    #     except Exception as e:
    #         self.system._add_error_log(Exception("Ошибка считывания значения: " + str(e)))
    #         # self.errors.append()
    #         # self.close()
    #         print("ERROR", e)
    #     finally:
    #         try:
    #         # print("FINALLY:", self.log, "| has logs:",  self.system.has_logs)
    #             if self.log is None and self.system.has_logs:
    #                 self.log = self.system.first_log
    #                 self.log_widget.set_log(self.log)
    #         except Exception as e:
    #             print("Set log error:", e)
