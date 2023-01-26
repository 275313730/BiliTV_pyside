import time

from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QHBoxLayout, QFrame
from bilibili_api.user import User

from utils.BiliAPI import BiliAPI
from utils.Const import Const
from utils.DataManager import DataManager
from utils.Notify import Notify
from utils.Utils import Utils
from .MonitorButton import MonitorButton
from .MonitorScreen import MonitorScreen


class Monitor(QFrame):
    position: list[int] = []
    add_up_signal: Signal = Signal(int)
    del_up_signal: Signal = Signal(int)
    button: MonitorButton
    screen: MonitorScreen
    layout: QHBoxLayout
    user: User
    
    def __init__(self, position: list[int]):
        super().__init__()
        self.setMinimumSize(*Const.min_size)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.position = position
        self.create_button()
        self.add_up_signal.connect(self.emit_uid)
        self.del_up_signal.connect(self.emit_reset)
        self.check_position()
        self.setLayout(self.layout)
        self.show()
    
    def check_position(self) -> None:
        if DataManager.check_position_exist(self.position):
            up = DataManager.get_up_data_from_position(self.position)
            self.emit_uid(up['uid'])
            DataManager.add_up(up['uid'], self.position)
    
    # 循环获取up信息
    def loop(self) -> None:
        if self.screen:
            try:
                self.get_new_data(self.screen.uid)
                if BiliAPI.network_error:
                    BiliAPI.network_error = False
                    Notify.text("网络恢复正常")
            except Exception as e:
                print(e)
                if not BiliAPI.network_error:
                    BiliAPI.network_error = True
                    Notify.text("网络错误，无法获取UP信息")
            finally:
                Utils.set_timeout(Const.loop_time, self.loop)
    
    def create_button(self) -> None:
        button = MonitorButton()
        button.add_up_signal = self.add_up_signal
        self.layout.addWidget(button)
        self.button = button
    
    def create_screen(self, uid: int) -> None:
        screen = MonitorScreen(uid)
        screen.del_up_signal = self.del_up_signal
        self.layout.addWidget(screen)
        self.screen = screen
        DataManager.add_up(uid, self.position)
        self.user = User(uid)
        up_data = DataManager.get_up_data_from_uid(uid)
        self.screen.update_user_info(up_data["user"])
        self.screen.update_label("dynamic", up_data["dynamic"])
        self.screen.update_label("video", up_data["video"])
        self.screen.update_label("live", up_data['live'])
        self.loop()
    
    def emit_uid(self, uid: int) -> None:
        self.button.hide()
        self.create_screen(uid)
    
    def emit_reset(self, uid: int) -> None:
        self.screen.deleteLater()
        DataManager.del_up(uid)
        self.button.show()
    
    # 获取up信息
    def get_new_data(self, uid: int) -> None:
        up_data = DataManager.get_up_data_from_uid(uid)
        nick_name = up_data['user']['nick_name']
        
        if DataManager.need_update(uid, "user"):
            new_user_info = BiliAPI.get_user_info(self.user)
            BiliAPI.call_count += 1
            print(f"API调用次数:{BiliAPI.call_count},运行时长(分钟):{int((time.time() - BiliAPI.run_start_time) / 60)}")
            DataManager.update_up_data(uid, "user", new_user_info)
            self.screen.update_user_info(new_user_info)
        
        if DataManager.need_update(uid, "dynamic"):
            new_dynamic_data = BiliAPI.get_dynamic_data(self.user)
            BiliAPI.call_count += 1
            print(f"API调用次数:{BiliAPI.call_count},运行时长(分钟):{int((time.time() - BiliAPI.run_start_time) / 60)}")
            update_status = DataManager.update_up_data(uid, "dynamic", new_dynamic_data)
            if update_status:
                self.screen.update_label("dynamic", dict(id=new_dynamic_data['id'], read=False))
                Notify.text(f'「{nick_name}」发布了一条新动态')
        
        if DataManager.need_update(uid, "video"):
            new_video_data = BiliAPI.get_video_data(self.user)
            BiliAPI.call_count += 1
            print(f"API调用次数:{BiliAPI.call_count},运行时长(分钟):{int((time.time() - BiliAPI.run_start_time) / 60)}")
            update_status = DataManager.update_up_data(uid, "video", new_video_data)
            if update_status:
                self.screen.update_label("video", dict(bvid=new_video_data['bvid'], read=False))
                Notify.text(f'「{nick_name}」发布了一条新视频')
        
        if DataManager.need_update(uid, "live"):
            new_live_info = BiliAPI.get_live_info(self.user)
            BiliAPI.call_count += 1
            print(f"API调用次数:{BiliAPI.call_count},运行时长(分钟):{int((time.time() - BiliAPI.run_start_time) / 60)}")
            update_status = DataManager.update_up_data(uid, "live", new_live_info)
            if update_status:
                self.screen.update_label("live", new_live_info)
                if new_live_info['live_status']:
                    Notify.text(f'「{nick_name}」上播了')
                else:
                    Notify.text(f'「{nick_name}」下播了')
