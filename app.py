import sys, os, datetime
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QVBoxLayout,
    QLabel, QCheckBox, QComboBox, QLineEdit, QStyle,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QFrame, QPushButton
)
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMetaType, QRect

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


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

        self.input = QLineEdit()
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

    def click_press(self):
        self.counter += 1
        self.label.setText(f"PRESSED: {self.counter}")


class AbstractAppUIWidget(QWidget):
    pass


class AppEventHandler(object):
    def __int__(self, *args, **kwargs):
        pass

    def on_click(self, *args):
        pass

    # def on_

###################################################################


class SavedError(object):
    def __init__(self, e: Exception, description="ERROR"):
        self.error = e
        self.description = description
        self.created_at = datetime.datetime.utcnow()

    def __str__(self):
        return f"[{self.description}] {self.created_at} - {str(self.error)}"

class BaseInterfaceException(Exception):
    pass


class COMMUNICATION_INTERFACE_STATE:
    INACTIVE = 0
    ACTIVE = 1
    HAS_ERRORS = 2

class AbstractCommunicationInterface(object):
    def __init__(
            self,
            speed=None,
            channel=None,
    ):
        self.speed = speed
        self.channel = channel  # port
        self._status = COMMUNICATION_INTERFACE_STATE.INACTIVE
        self.setup_configuration()

    def setup_configuration(self):
        self._status = COMMUNICATION_INTERFACE_STATE.ACTIVE

    def send(self, value):
        """
        preprocess value -> send value -> get answer -> answer processing ->
        1. has mistakes -> raise error
        2. all oKey -> return value
        :return:
        """
        pass

    def _preprocessing_value(self, value):
        pass

    def _process_answer(self):
        """
        Is answer is oKey?
        1. Answer OK ? -> _extract_value
        2. Else -> _handle_exception
        :return:
        """
        pass

    def _extract_value(self):
        """

        :return: value from receiving answer
        """
        pass

    def _handle_exception(self):
        pass


class BaseDeviceException(Exception):
    pass

class DefectiveDeviceException(BaseDeviceException):
    pass


class DEVICE_STATUS:
    INACTIVE = 0
    ACTIVE = 1
    HAS_ERRORS = 2


class AbstractDevice(object):
    """
    Device class with base method `exec_command`

    """
    def __init__(
            self,
            communication_interface=None,
    ):
        self.communication_interface: AbstractCommunicationInterface = communication_interface
        self._last_command = None
        self._status = DEVICE_STATUS.INACTIVE
        self._errors = []

    def _setup_device(self):
        try:
            self.communication_interface.setup_configuration()
            self._status = DEVICE_STATUS.ACTIVE
        except Exception as e:
            self._status = DEVICE_STATUS.HAS_ERRORS
            self._errors.append(SavedError(e, description="Device setup error"))

    # def on/off/
    def exec_command(self, command, value=None):
        """
        Main function for execution user commands
        :param command:
        :param value:
        :return:
        """
        if self._status == DEVICE_STATUS.HAS_ERRORS:
            raise DefectiveDeviceException

        self._last_command = command
        try:
            preprocessing_value = self._preprocessing_value(command, value)
            answer = self.communication_interface.send(preprocessing_value)

            return self._postprocessing_value(answer)

        except BaseDeviceException as e:
            return self._handle_device_exception(e)
        except BaseInterfaceException as e:
            return self._handle_interface_exception(e)
        except Exception as e:
            raise e

    def _handle_interface_exception(self, e: BaseInterfaceException):
        raise e

    def _handle_device_exception(self, e: BaseDeviceException):
        raise e

    def _preprocessing_value(self, command, value):
        """
        Connect command with value to one meaning to send for communication interface
        :param command:
        :param value:
        :return:
        """
        return f"{command}_{value}"

    def _postprocessing_value(self, value):
        return value


class AbstractDeviceController(object):
    """

    """

    def send(self, *args, **kwargs):
        """
        Send value to sensor
        :param args:
        :param kwargs:
        :return: any value from sensor answer
        """
        pass

    def wait_seconds(self, seconds, after_wait=None, **kwargs):
        """

        :param after_wait: function for execute after waiting
        :param seconds: amount of seconds
        :param kwargs:
        :return:
        """
        pass

    def wait_until_value(self, value, on_reached=None, **kwargs):
        """
        Wait time until target value is not reached
        :param on_reached: function for execute after value is reached
        :param value: target value
        :param kwargs:
        :return:
        """


app = QApplication(sys.argv)
w = MainWindow()
w.showFullScreen()
# w.show()
app.exec_()
