import os
os.environ.setdefault('GRAPHENE_SETTINGS_MODULE', 'Core.settings')

import tracemalloc
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Structure.dialog_ui import AppMainDialogWindow

from Core.actions import ACTIONS
from Structure.system import AppSystem
# from Tests.devices.current_source_akip import test_akip_2, get_serial_port
# from Tests.devices.trm200 import test_trm_2, test_4, test_1, check_port
# from Tests.devices.rrg import test_rrg_3
# from Tests.devices.vakumetr import test_1, test_2

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
import faulthandler
faulthandler.enable()
PYTHONFAULTHANDLER = 1

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

tracemalloc.start()


def start():
    # sys.exit(0)
    app = QApplication([])
    system = AppSystem(
        actions_list=ACTIONS
    )
    system.setup()
    system.threads_setup()

    w = AppMainDialogWindow(system=system)
    w.system_connect()

    # w.show()
    # w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
    # w.showFullScreen()
    w.setWindowState(Qt.WindowFullScreen)
    w.setVisible(True)
    # w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
    # w.setWindowFlags(Qt.WindowType_Mask)
    app.exec()

# from Core.actions import ACTIONS
#
# def start_system():
#     system = CvdSystem(actions_list=ACTIONS)
#     system.setup()
#     system.threads_setup()
#     try:
#         while True:
#             sleep(1)
#     except BaseException:
#         system.stop()
#         system.destructor()


if __name__ == '__main__':
    start()

print("Exit")
