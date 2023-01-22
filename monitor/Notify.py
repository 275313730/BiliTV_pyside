import os
import platform


class Notify:
    system: str = platform.system().lower()
    
    @staticmethod
    def text(content: str):
        if Notify.system == "windows":
            from windows_toasts import WindowsToaster, ToastText1
            wintoaster = WindowsToaster('BiliTV')
            new_toast = ToastText1()
            new_toast.SetBody(content)
            wintoaster.show_toast(new_toast)
        elif Notify.system == "darwin":
            os.system('osascript -e \'display notification "' + content + '" with title "BiliTV"\'')

