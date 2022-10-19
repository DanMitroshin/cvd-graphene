import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QFrame, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QLineEdit, QWidget, QMainWindow, QGridLayout,
)

from Structure.dialog_ui.MainBlockWidget import MainBlockWidget
from Structure.dialog_ui.RightButtonsWidget import RightButtonsWidget
from Structure.dialog_ui.components import LogWidget
from Structure.system import CvdSystem


class UiMainWindow(object):

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        # self.setWindowTitle("My App")

        # line_style = QStyle()
        # line_style.sty

        line = QFrame(MainWindow)
        # line.setObjectName(QMetaType.Type.QString)
        line.setObjectName("ll")
        line.setLineWidth(100)
        line.setFixedHeight(100)
        line.setStyleSheet("background-color: rgb(255, 0, 50);")
        # line.setGeometry(QRect(0, 10, 100, 110))
        # line.setStyle()
        # line.setFrameShape(QFrame.Shape.HLine)
        # line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line = line

        self.line = QFrame()
        self.line.setMinimumWidth(100)
        self.line.setFixedHeight(20)
        # self.line.setGeometry(QRect(60, 110, 751, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                QtWidgets.QSizePolicy.Policy.Minimum)

        self.label = QLabel()
        # self.label.setStyleSheet('color:"red";font-size: 32;')
        self.label.setStyleSheet("""
                QWidget {
                    border: 2px solid black;
                    border-radius: 10px;
                    background-color: rgb(255, 255, 255);
                    font-size: 32px;
                    max-width: 300px;
                    }
                """)

        self.input = QLineEdit(MainWindow)
        self.input.textChanged.connect(self.label.setText)

        layout = QHBoxLayout()
        layout_v = QVBoxLayout()
        layout.addWidget(self.line)
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        self.button_close = QPushButton("нажать для закрытия программы")
        self.button_close.clicked.connect(self.close)
        self.button_close.setStyleSheet("""
                QPushButton {
                    height: 200px;
                    font-size: 20px;
                }
                """)
        layout_v.addLayout(layout)
        self.button = QPushButton("Press Me!")
        self.button.setStyleSheet("""
                        QPushButton {
                            height: 100px;
                            font-size: 16px;
                        }
                        """)
        self.counter = 0
        self.button.clicked.connect(self.click_press)

        layout_v.addWidget(self.button)
        layout_v.addWidget(self.button_close)

        container = QWidget()
        container.setLayout(layout_v)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        # MainWindow.resize(534, 364)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 1, 2, 3, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 2, 0, 1, 2)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 534, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Тест приложения на Python с модулем PyQt5"))
        self.label.setText(_translate("MainWindow", "Трекер события !@#"))
        self.label_2.setText(_translate("MainWindow", "Описание события:"))
        self.pushButton.setText(_translate("MainWindow", "Следить"))
        self.label_3.setText(_translate("MainWindow", "До наступления события осталось: ХХ дней )))"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        # line_style = QStyle()
        # line_style.sty

        line = QFrame()
        # line.setObjectName(QMetaType.Type.QString)
        line.setObjectName("ll")
        line.setLineWidth(100)
        line.setFixedHeight(100)
        # line.setStyleSheet("background-color: rgb(255, 0, 50);")
        # line.setGeometry(QRect(0, 10, 100, 110))
        # line.setStyle()
        # line.setFrameShape(QFrame.Shape.HLine)
        # line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line = line

        self.line = QFrame()
        self.line.setMinimumWidth(100)
        self.line.setFixedHeight(20)
        # self.line.setGeometry(QRect(60, 110, 751, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                QtWidgets.QSizePolicy.Policy.Minimum)

        self.label = QLabel()
        # self.label.setStyleSheet('color:"red";font-size: 32;')
        # self.label.setStyleSheet("""
        # QWidget {
        #     border: 2px solid black;
        #     border-radius: 10px;
        #     background-color: rgb(255, 255, 255);
        #     font-size: 32px;
        #     max-width: 300px;
        #     }
        # """)

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QHBoxLayout()
        layout_v = QVBoxLayout()
        layout.addWidget(self.line)
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        self.button_close = QPushButton("CLOSE X")
        self.button_close.clicked.connect(self.close)
        # self.button_close.setStyleSheet("""
        #     height: 100px;
        #     font-size: 20px;
        # """)
        layout_v.addLayout(layout)
        self.button = QPushButton("Press Me!")
        # self.button.setStyleSheet("""
        #         QPushButton {
        #             height: 100px;
        #             font-size: 16px;
        #         }
        #         """)
        self.counter = 0
        self.button.clicked.connect(self.click_press)

        layout_v.addWidget(self.button)
        layout_v.addWidget(self.button_close)

        container = QWidget()
        container.setLayout(layout_v)

        ##############################################################################
        ##############################################################################
        ##############################################################################
        ##############################################################################
        ##############################################################################

        self.system = CvdSystem()
        self.system.setup()

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
        )
        self.main_window.addWidget(self.right_buttons_layout_widget)

        # Устанавливаем центральный виджет Window.
        # self.setCentralWidget(container)
        self.setCentralWidget(self.main_widget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_values_and_log_state)
        self.timer.start(1000)

        self.log = None
        self.log_widget = LogWidget(on_close=self.clear_log, parent=self)
        self.log_widget.move(100, 100)

        ############################################
        # CONNECT FUNCTIONS ########################

        self.main_interface_layout_widget.pressure_block.o2.connect_valve_function(
            self.system.change_valve_state
        )
        self.main_interface_layout_widget.temperature_block.current_settings.set_current_block.\
            set_value_function = self.system.set_current
        # self.system.change_valve_state("")

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

    def get_values_and_log_state(self):
        try:
            self.system.get_values()

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


# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = UiMainWindow()
#     ui.setup_ui(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
