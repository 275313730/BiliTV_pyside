from threading import Timer
import base64

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
            return Const.windows_user_path + "/"
        else:
            return Const.mac_user_path + "/"
    
    @staticmethod
    def get_favicon_data():
        bs64_str = Const.favicon_base64
        # 将base64格式的数据装换为二进制数据
        imgdata = base64.b64decode(bs64_str)
        return imgdata
