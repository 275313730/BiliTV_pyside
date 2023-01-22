from PySide6.QtCore import QObject, Signal
from bilibili_api import user, sync

from monitor.DataManager import DataManager
from monitor.Monitor import Monitor
from monitor.MonitorScreen import MonitorScreen
from utils import set_timeout
from monitor.Notify import Notify


class MonitorManager(QObject):
    monitors: list[Monitor] = []
    add_up_signal = Signal(int)
    change_up_signal = Signal(int, int)
    start_loop_signal = Signal()
    loop_time: float = 10000
    
    def __init__(self):
        super().__init__()
        self.add_up_signal.connect(self.get_new_data)
        self.change_up_signal.connect(self.change_up)
        self.start_loop_signal.connect(self.loop)
    
    # 添加监控器
    def add_monitor(self, monitor: Monitor):
        monitor.add_up_signal = self.add_up_signal
        monitor.change_up_signal = self.change_up_signal
        self.monitors.append(monitor)
        if DataManager.check_position_exist(monitor.position):
            up = DataManager.get_up_data_from_position(monitor.position)
            monitor.emit_uid(up['uid'])
            DataManager.add_up(up['uid'], monitor.position)
    
    # 循环获取up信息
    def loop(self):
        for data in DataManager.all_up_data:
            self.get_new_data(int(data['uid']))
        set_timeout(self.loop_time, self.loop)
    
    # 获取up信息
    def get_new_data(self, uid: int):
        u = user.User(uid)
        screen: MonitorScreen = self.find_screen_by_uid(uid)
        up_data = DataManager.get_up_data_from_uid(uid)
        nick_name = up_data['user']['nick_name']
        
        if DataManager.need_update(uid, "user"):
            new_user_info = self.get_user_info(u)
            DataManager.update_up_data(uid, "user", new_user_info)
            screen.update_user_info(new_user_info)
        else:
            screen.update_user_info(up_data["user"])
        
        if DataManager.need_update(uid, "dynamic"):
            new_dynamic_data = self.get_dynamic_data(u)
            update_status = DataManager.update_up_data(uid, "dynamic", new_dynamic_data)
            screen.update_label("dynamic", dict(id=new_dynamic_data['id']))
            if update_status: Notify.text(f'「{nick_name}」发布了一条新动态')
        else:
            screen.update_label("dynamic", dict(id=up_data["dynamic"]['id']))
        
        if DataManager.need_update(uid, "video"):
            new_video_data = self.get_video_data(u)
            update_status = DataManager.update_up_data(uid, "video", new_video_data)
            screen.update_label("video", dict(bvid=new_video_data['bvid']))
            if update_status: Notify.text(f'「{nick_name}」发布了一条新视频')
        else:
            screen.update_label("video", dict(bvid=up_data['video']['bvid']))
        
        if DataManager.need_update(uid, "live"):
            new_live_info = self.get_live_info(u)
            update_status = DataManager.update_up_data(uid, "live", new_live_info)
            screen.update_label("live", new_live_info)
            if update_status:
                if new_live_info['live_status']:
                    Notify.text(f'「{nick_name}」上播了')
                else:
                    Notify.text(f'「{nick_name}」下播了')
        else:
            screen.update_label("live", up_data['live'])
    
    def change_up(self, old_uid: int, new_uid: int):
        old_data = DataManager.get_up_data_from_uid(old_uid)
        position = old_data["position"]
        DataManager.del_up(old_uid)
        DataManager.add_up(new_uid, position)
        self.get_new_data(new_uid)
    
    # 根据uid获取screen
    def find_screen_by_uid(self, uid: int):
        for monitor in self.monitors:
            if monitor.screen.uid == uid:
                return monitor.screen
    
    # 获取up资料
    @staticmethod
    def get_user_info(u: user.User):
        user_info = sync(u.get_user_info())
        avatar_url = user_info['face']
        nickname = user_info['name']
        return dict(nick_name=nickname, avatar_url=avatar_url)
    
    # 获取up动态信息
    @staticmethod
    def get_dynamic_data(u: user.User):
        # 用于记录下一次起点
        offset = 0
        # 用于存储所有动态
        dynamics = []
        page = sync(u.get_dynamics(offset))
        if 'cards' in page:
            # 若存在 cards 字段（即动态数据），则将该字段列表扩展到 dynamics
            dynamics.extend(page['cards'])
        if len(dynamics) > 0:
            last_dynamic = dynamics[0]['desc']
            return dict(time=last_dynamic['timestamp'], id=last_dynamic['dynamic_id'])
        return dict(time=0, url="")
    
    # 获取up视频信息
    @staticmethod
    def get_video_data(u: user.User):
        video_data = sync(u.get_videos(ps=1))
        video_list = video_data['list']['vlist']
        if len(video_list) > 0:
            video_info = video_list[0]
            return dict(time=video_info['created'], bvid=video_info['bvid'])
        return dict(time=0, bvid="")
    
    # 获取up直播信息
    @staticmethod
    def get_live_info(u: user.User):
        live_data = sync(u.get_live_info())
        live_info = live_data['live_room']
        return dict(live_status=int(live_info['liveStatus']), url=live_info['url'])
