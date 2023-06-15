import os

os.environ.setdefault('GRAPHENE_SETTINGS_MODULE', 'Core.settings')

import tracemalloc
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QProcessEnvironment
from PyQt5.QtQuick import QQuickView
from PyQt5 import QtGui, QtCore
from Structure.dialog_ui import AppMainDialogWindow

from Core.actions import ACTIONS
from Structure.system import AppSystem
# from Tests.devices.current_source_akip import test_akip_2, get_serial_port
# from Tests.devices.trm200 import test_trm_2, test_4, test_1, check_port
# from Tests.devices.rrg import test_rrg_3
# from Tests.devices.vakumetr import test_1, test_2

# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.environ["QML2_IMPORT_PATH"] = dir_path
os.environ["QT_VIRTUALKEYBOARD_STYLE"] = "testkeyboard10" #"testkeyboard1"
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


# for i in QProcessEnvironment.systemEnvironment().keys():
#     print(i)

import faulthandler
faulthandler.enable()
PYTHONFAULTHANDLER = 1

import resource, sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**5)

import threading
threading.stack_size(2**26)

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


def handleVisibleChanged():
    if not QtGui.QGuiApplication.inputMethod().isVisible():
        return
    for w in QtGui.QGuiApplication.allWindows():
        if w.metaObject().className() == "QtVirtualKeyboard::InputView":
            keyboard = w.findChild(QtCore.QObject, "keyboard")
            if keyboard is not None:
                r = w.geometry()
                r.moveTop(int(keyboard.property("y")))
                w.setMask(QtGui.QRegion(r))
                return


def start():
    # sys.exit(0)
    app = QApplication([])
    # engine = QQmlApplicationEngine()
    # engine.load('main.qml')
    # return
    #QtGui.QInputMethod().visibleChanged.connect(is_visible)
    # QtGui.QInputMethod().setVisible(True)

    inputMethod = app.inputMethod()
    inputMethod.visibleChanged.connect(handleVisibleChanged)

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

    # QtGui.QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)
    w.setWindowState(Qt.WindowFullScreen)
    # w.setGeometry(app.desktop().screenGeometry())
    w.setVisible(True)
    # w.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
    # w.setWindowFlags(Qt.WindowType_Mask)
    # visible = False
    screen_h = app.desktop().screenGeometry().height()
    w.setFixedHeight(screen_h)
    w.setFixedWidth(app.desktop().screenGeometry().width())

    def is_visible():
        visible = inputMethod.isVisible()
        # visible = not visible
        print("VISIBLEEEEEEEEE CHANGED", visible)
        # print('SCREEN', app.desktop().screenGeometry().height())
        # print(inputMethod.anchorRectangle())
        print(inputMethod.anchorRectangle().y())
        shift = 300
        if visible:
            shift *= -1
        w.milw.move(0, shift)
        # pg = w.milw.frameGeometry()
        # if visible:
        #     pass
        #     # w.milw.hide()
        #     # w.setMinimumHeight(200 + screen_h)
        #     # w.setContentsMargins(-200, 0, 0, 200)
        #     new_geometry = w.main_widget.geometry().adjusted(
        #         0, -200,
        #         0, pg.height() - 200,
        #     )
        #     w.milw.setGeometry(new_geometry)
        # else:
        #     pass
        #     # w.milw.show()
        #     # w.setMinimumHeight(screen_h)
        #     # w.setContentsMargins(0, 0, 0, 0)
        w.milw.setAttribute(Qt.WA_Moved, True)

        # w.milw.move(pg.x(), pg.y() + shift)
        # w.milw.layout.
        # w.show()

    inputMethod.visibleChanged.connect(is_visible)
    # w.hide()
    # w.show()
    # w.milw.move(200, 200)
    # w.milw.setAttribute(Qt.WA_Moved, True)

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

# import threading
#
# a = 0
# def x():
#     global a
#     for i in range(100000):
#         a += 1
#
# threads = []
#
# for j in range(10):
#     thread = threading.Thread(target=x)
#     threads.append(thread)
#     thread.start()
#
# for thread in threads:
#     thread.join()
#
# print(a)
# assert a == 1000000


if __name__ == '__main__':
    # pass
    start()

print("Exit")
