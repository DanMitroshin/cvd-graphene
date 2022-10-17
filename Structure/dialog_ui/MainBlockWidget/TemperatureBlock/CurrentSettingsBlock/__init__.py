from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect

from Structure.dialog_ui.components import ParameterLatexLabel, ParameterLabel
from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .ActualTemperature import ActualTemperature
from .RiseCurrentBlock import RiseCurrentBlock
from .SetCurrentBlock import SetCurrentBlock
from .styles import styles


class CurrentSettingsBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("current_settings_block")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        self.setGraphicsEffect(shadow)

        self.actual_temperature = ActualTemperature()
        self.layout.addWidget(self.actual_temperature, QtCore.Qt.AlignTop)

        self.set_current_block = SetCurrentBlock()
        self.layout.addWidget(self.set_current_block, )

        self.voltage_label = ParameterLabel()
        self.voltage_value = 0.0
        self.set_voltage_value(self.voltage_value)

        self.current_label = ParameterLabel()
        self.current_value = 0.0
        self.set_current_value(self.current_value)

        self.labels = QHBoxLayout()
        self.labels.addWidget(self.voltage_label, alignment=QtCore.Qt.AlignLeft)
        self.labels.addWidget(self.current_label, alignment=QtCore.Qt.AlignRight)

        self.layout.addLayout(self.labels, )
        self.rise_current_block = RiseCurrentBlock()
        self.layout.addWidget(self.rise_current_block, QtCore.Qt.AlignCenter)

    def set_voltage_value(self, value):
        self.voltage_value = value
        self.voltage_label.setText(f"U = {self.voltage_value}V")

    def set_current_value(self, value):
        self.current_value = value
        self.current_label.setText(f"I = {self.current_value}A")
