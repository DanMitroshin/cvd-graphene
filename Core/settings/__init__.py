"""
MAIN FILE WITH SETTINGS
IMPORT HERE ALL NECESSARY SETTINGS FOR YOUR DEVICE AND CONNECTIONS

"""

from .actions import *
from .raspberry import *
import platform


LOCAL_MODE = platform.system() != 'Linux'
