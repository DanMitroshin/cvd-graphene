import datetime
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import (
    QFrame, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QLineEdit, QWidget, QMainWindow, QGridLayout, QFileDialog,
)

from Structure.dialog_ui.MainBlockWidget import MainBlockWidget
from Structure.dialog_ui.RightButtonsWidget import RightButtonsWidget
from Structure.dialog_ui.TableWidget import AppTableWidget
from Structure.dialog_ui.components import LogWidget
from Structure.system import CvdSystem
from coregraphene.constants import RECIPE_STATES


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CVD-Graphene")

        ##############################################################################
        ##############################################################################
        ##############################################################################
        ##############################################################################
        ##############################################################################

        self.system = CvdSystem()
        self.system.setup()
        self.system.threads_setup()

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

        # self.main_interface_layout_widget.pressure_block.o2.connect_valve_function(
        #     self.system.change_valve_state
        # )
        for gas in self.main_interface_layout_widget.pressure_block.gases:
            gas.connect_valve_function(self.system.change_valve_state)

        self.main_interface_layout_widget.temperature_block.current_settings.set_current_block.\
            set_value_function = self.system.set_current
        # self.system.change_valve_state("")

    def on_create_recipe(self):
        try:
            self.table_widget.on_create_recipe()
        except Exception as e:
            print("On create recipe function error:", e)

    def on_open_recipe(self):
        try:
            file_path = QFileDialog.getOpenFileName(self, 'Выбрать рецепт', '')[0]
            if file_path:
                data = self.system.get_recipe_file_data(file_path)
                self.table_widget.on_open_recipe_file(file_path, data)
        except Exception as e:
            print("On open recipe error:", e)

    def close(self) -> bool:
        self.system.stop()
        return super().close()

    def clear_log(self, uid):
        self.system.clear_log(uid=uid)
        self.log = None

    def __del__(self):
        # print("Window del")
        self.system.destructor()

    def click_press(self):
        self.counter += 1
        self.label.setText(f"PRESSED: {self.counter}")

    def show_time(self):
        print("TIME:", datetime.datetime.now())

    def start_recipe(self):
        try:
            recipe = self.table_widget.get_values()
            ready = self.system.run_recipe(recipe)
            if not ready:
                return
            self._recipe_history = []
            self.add_recipe_step("Инициализация рецепта")
            self.table_widget.on_close()
            self.main_interface_layout_widget.deactivate_interface()
            self.right_buttons_layout_widget.activate_manage_recipe_buttons()
        except Exception as e:
            print("Start recipe UI error:", e)

    def add_recipe_step(self, name="---", index=None):
        index = index if index else len(self._recipe_history)
        if self._current_recipe_step:
            if self._current_recipe_step.get('index', -1) == index:
                return
        self._current_recipe_step = {"name": name, "index": index}
        self._recipe_history.append(f"{datetime.datetime.utcnow().time()} [{index}] {name}")
        try:
            self.main_interface_layout_widget.set_current_step(self._recipe_history[-1])
        except:
            pass

    def get_values_and_log_state(self):
        try:

            self.system.get_values()
            recipe_step = self.system.current_recipe_step
            if recipe_step:
                self.add_recipe_step(**recipe_step)
            recipe_state = self.system.recipe_state
            if recipe_state != self._recipe_state:
                self._recipe_state = recipe_state
                if recipe_state == RECIPE_STATES.STOP:
                    self.main_interface_layout_widget.activate_interface()
                    self.right_buttons_layout_widget.deactivate_manage_recipe_buttons()


            self.main_interface_layout_widget.pressure_control_block.show_pressure_block.set_value(
                self.system.accurate_vakumetr_value
            )

            # print("VOLTAGE:", self.system.voltage_value)
            # VOLTAGE
            self.main_interface_layout_widget.temperature_block.current_settings.set_voltage_value(
                self.system.voltage_value
            )
            self.main_interface_layout_widget.temperature_block.current_settings.set_current_value(
                self.system.current_value
            )
        except Exception as e:
            self.system._add_error_log(Exception("Ошибка считывания значения: " + str(e)))
            # self.errors.append()
            # self.close()
            print("ERROR", e)
        finally:
            try:
            # print("FINALLY:", self.log, "| has logs:",  self.system.has_logs)
                if self.log is None and self.system.has_logs:
                    self.log = self.system.first_log
                    self.log_widget.set_log(self.log)
            except Exception as e:
                print("Set log error:", e)
