import sys, os, datetime
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QVBoxLayout,
    QLabel, QCheckBox, QComboBox, QLineEdit, QStyle,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QFrame, QPushButton
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QMetaType, QRect

from Core.exceptions.communicators import InactiveCommunicatorException
from Core.ui import StyleSheet
from Core.utils.algorithms import crc16
from Structure.dialog_ui import UiMainWindow, MainWindow
from Tests.devices.current_source_akip import test_akip_2, test_akip_1
from Tests.devices.trm200 import test_2, test_4, test_1
from Tests.devices.rrg import test_3
# from Tests.devices.vakumetr import test_1, test_2

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

# s = StyleSheet({
#     "close_button": {
#         "height": "70px",
#         "font-size": "20px",
#         "background-color": "rgb(255, 150, 150)",
#     }
# })
# print("SSSSSSSSS", s.close_button)
# print("SSSSSSSSS 2", s.close_button1)
# sys.exit()

class MainWindow1(QMainWindow):
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

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

    def click_press(self):
        self.counter += 1
        self.label.setText(f"PRESSED: {self.counter}")

    def show_time(self):
        print("TIME:", datetime.datetime.now())

class AbstractAppUIWidget(QWidget):
    pass



###################################################################


class Test:

    def handler_decorator(func):
        def magic(self):
            print("start magic")
            self.check()
            func(self)
            print("end magic")

        return magic

    def __init__(self):
        self.counter = 123
        print("COUNTER SET UP!")

    @handler_decorator
    def on_click(self):
        print("ON CLICK, Counter:", self.counter)

    def check(self):
        self.counter += 1
        print("CHECK COUNTER:", self.counter)


# t = Test()
# t.on_click()

# def bar():
#     raise InactiveCommunicatorException(communicator_id="ref_234")
#
# bar()

# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = UiMainWindow()
# ui.setup_ui(MainWindow)
# MainWindow.showFullScreen()
# sys.exit(app.exec_())

# print((int(899.99) // 100))
# sys.exit()

def crc16x(data: str, poly: hex = 0xA001) -> str:
    '''
        CRC-16 MODBUS HASHING ALGORITHM
    '''
    crc = 0xFFFF
    for byte in data:
        crc ^= ord(byte)
        for _ in range(8):
            crc = ((crc >> 1) ^ poly
                   if (crc & 0x0001)
                   else crc >> 1)

    hv = hex(crc).upper()[2:]
    blueprint = '0000'
    return blueprint if len(hv) == 0 else blueprint[:-len(hv)] + hv


if __name__ == "__main__":
    print("TEST 1 ===>")
    try:
        import libscrc
        import codecs
        # test_3()
        # hi, lo = crc16(b'\x01\x06\x03\xE9\x00\x00')  # CRC = b'\x58\x7A'
        # print("{0:02X} {1:02X}".format(hi, lo))
        # s = "02030001"
        # s = "7A"
        # s1 = 0x7A
        # # s1 = hex(35633330)
        # print(s1)
        # print("SDFSDFSD", bytes([s1]))
        # print("SSSS > ", codecs.decode(s, "hex"))
        # hi, lo = crc16(codecs.decode(s, "hex"))  # CRC = b'\x58\x7A'
        # # hi, lo = crc16(bytearray("002030001".encode("ASCII")))  # CRC = b'\x58\x7A'
        # # hi, lo = crc16(bytearray("002030001".encode("ASCII")))  # CRC = b'\x58\x7A'
        # # ans = crc16x("002030001")  # CRC = b'\x58\x7A'
        # # print("CRC16:", ans)
        # def f(i):
        #     return str(hex(i))[2:]
        # print("!!!!!!!!!! {0:02X} {1:02X}".format(hi, lo))
        # print("ALL COMM:", s + f(lo) + f(hi))
        # # print("GGG",b'0010MV0' + (hi).to_bytes(1, byteorder='big'))
        # print("GGG", bytearray("002030001".encode("ASCII")) + bytes([hi, lo]))
        #
        # crc16_ = libscrc.modbus(b'0010MV0')
        # h_crc = str(hex(crc16_))[2:]
        # print("CRC:", crc16_, str(hex(crc16_)), str(hex(crc16_))[2:])
        # binary_str = codecs.decode(h_crc, "hex")
        # print("BS ==> ", str(binary_str, 'ascii'))
        # print(bytearray.fromhex(str(hex(crc16_))[2:]).decode())
        # test_1()
        # test_3()
        test_akip_1()
        # test_akip_2()
        # test_2()
        # test_4()
        # test_1()
        print("TEST 1 ===> PASSED")
    except Exception as e:
        print("[ERROR]", e)
        print("TEST 1 ===> FAILED")

sys.exit(0)
app = QApplication([])
w = MainWindow()
# w.show()
# w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
# w.showFullScreen()
w.setWindowState(Qt.WindowFullScreen)
w.setVisible(True)
# w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
# w.setWindowFlags(Qt.WindowType_Mask)
app.exec()
