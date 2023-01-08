from PySide6.QtCore import QObject, Signal
from bilibili_api import user, sync

from monitor.DataManager import DataManager
from monitor.Monitor import Monitor
from monitor.MonitorScreen import MonitorScreen


class MonitorManager(QObject):
    monitors: list[Monitor] = []
    add_up_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.add_up_signal.connect(self.get_new_data)

    # 添加监控器
    def add_monitor(self, monitor: Monitor):
        monitor.add_up_signal = self.add_up_signal
        self.monitors.append(monitor)
        if DataManager.check_position_exist(monitor.position):
            up = DataManager.get_up_data_from_position(monitor.position)
            monitor.emit_uid(up['uid'])
            DataManager.add_up(up['uid'], monitor.position)

    # 循环获取up信息
    def loop(self):
        for data in DataManager.up_data:
            self.get_new_data(data['uid'])
        pass

    # 获取up信息
    def get_new_data(self, uid: int):
        u = user.User(uid)
        screen: MonitorScreen = self.find_screen_by_uid(uid)

        new_dynamic_data = self.get_dynamic_data(u)
        dynamic_update = DataManager.update_up_data(uid, "dynamic", new_dynamic_data)
        screen.update_label("dynamic", dict(dynamic_update=dynamic_update, id=new_dynamic_data['id']))

        new_video_data = self.get_video_data(u)
        video_update = DataManager.update_up_data(uid, "video", new_video_data)
        screen.update_label("video", dict(video_update=video_update, bvid=new_video_data['bvid']))

        new_live_info = self.get_live_info(u)
        DataManager.update_up_data(uid, "live", new_live_info)
        screen.update_label("live", new_live_info)

    # 根据uid获取screen
    def find_screen_by_uid(self, uid: int):
        for monitor in self.monitors:
            if monitor.screen.uid == uid:
                return monitor.screen

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
        return dict(live_status=live_info['liveStatus'], url=live_info['url'])
