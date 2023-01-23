import os
import sys
from threading import Timer

from utils.Const import Const


class Utils:
    @staticmethod
    def set_timeout(ms: float, fn: callable, *args, **kwargs):
        t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
        t.start()
        return t
    
    @staticmethod
    def get_path():
        if Const.system == "windows":
            return ""
        else:
            return os.path.split(sys.argv[0])[0] + "/"
