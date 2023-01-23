import os

from utils.Const import Const


class Notify:
    
    @staticmethod
    def text(content: str):
        if Const.system == "windows":
            from windows_toasts import WindowsToaster, ToastText1
            wintoaster = WindowsToaster('BiliTV')
            new_toast = ToastText1()
            new_toast.SetBody(content)
            wintoaster.show_toast(new_toast)
        elif Const.system == "darwin":
            os.system('osascript -e \'display notification "' + content + '" with title "BiliTV"\'')
