from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel

from .PressureBlock import PressureBlock
from .PressureControlBlock import PressureControlBlock
from .TemperatureBlock import TemperatureBlock
from .styles import styles


class MainBlockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("main_block_widget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet("* {background-color: rgb(0, 0, 255);}")

        self.pressure_block = PressureBlock()
        self.layout.addWidget(self.pressure_block)

        self.pressure_control_block = PressureControlBlock()
        self.layout.addWidget(self.pressure_control_block)

        self.temperature_block = TemperatureBlock()
        self.layout.addWidget(self.temperature_block)

        self.inactive_widget = QWidget(self)
        self.inactive_widget.setObjectName("inactive_widget")
        self.inactive_widget.setStyleSheet(styles.inactive_widget)
        self.inactive_widget.hide()

        self.recipe_labels_layout = QVBoxLayout()
        self.last_recipe_step = QLabel()
        self.current_recipe_step = QLabel()
        self.recipe_labels_layout.addWidget(self.current_recipe_step)
        self.recipe_labels_layout.addWidget(self.last_recipe_step)

        self.current_recipe_step_text = ""
        self.last_recipe_step_text = ""

        self.inactive_widget.setLayout(self.recipe_labels_layout)

    def deactivate_interface(self):
        self.inactive_widget.show()

    def activate_interface(self):
        self.current_recipe_step_text = ""
        self.last_recipe_step_text = ""
        self.current_recipe_step.setText(self.current_recipe_step_text)
        self.last_recipe_step.setText(self.last_recipe_step_text)

        self.inactive_widget.hide()

    def set_current_step(self, step=""):
        self.last_recipe_step_text = self.current_recipe_step_text
        self.current_recipe_step_text = step

        self.current_recipe_step.setText(self.current_recipe_step_text)
        self.last_recipe_step.setText(self.last_recipe_step_text)
