from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QHBoxLayout, QLineEdit

from Structure.dialog_ui.components import ParameterLatexLabel, LatexWidget
from Structure.dialog_ui.constants import SHADOW_BLUR_RADIUS
from .styles import styles

RGB = [175, 175, 250]

class RiseCurrentBlock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("rise_current_block")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.input_layout = QGridLayout()

        self.label_current = LatexWidget(
            text="$I_{final}$",
            rgb=RGB,
            fon_size_mult=2.5
        )
        # self.label_current.setText("I_final")
        self.label_current.setStyleSheet(styles.label)

        self.label_current_1 = QLabel()
        self.label_current_1.setText("A")
        self.label_current_1.setStyleSheet(styles.label)
        self.label_current_1.setAlignment(QtCore.Qt.AlignLeft)

        self.label_time = LatexWidget(
            text="$t_{rise}$",
            rgb=RGB,
            fon_size_mult=2.5
        )
        # self.label_time.setText("t_rise")
        self.label_time.setStyleSheet(styles.label)

        self.label_time_1 = QLabel()
        self.label_time_1.setText("s")
        self.label_time_1.setStyleSheet(styles.label)
        self.label_time_1.setAlignment(QtCore.Qt.AlignLeft)

        self.input_current = QLineEdit()
        self.input_current.setStyleSheet(styles.input)
        self.input_time = QLineEdit()
        self.input_time.setStyleSheet(styles.input)

        self.input_layout.addWidget(self.label_current, 0, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.input_layout.addWidget(self.input_current, 0, 1, QtCore.Qt.AlignBottom)
        self.input_layout.addWidget(self.label_current_1, 0, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.input_layout.addWidget(self.label_time, 1, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.input_layout.addWidget(self.input_time, 1, 1, QtCore.Qt.AlignTop)
        self.input_layout.addWidget(self.label_time_1, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # self.input_layout.setRowStretch(0, 10)
        # self.input_layout.setRowStretch(1, 100)

        ####################
        self.ramp_button = QPushButton()
        self.ramp_button.setText("Ramp")
        self.ramp_button.setStyleSheet(styles.button)

        self.layout.addLayout(self.input_layout, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.ramp_button,)
