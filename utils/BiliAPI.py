from bilibili_api import user, sync


class BiliAPI:
    # 获取up资料
    @staticmethod
    def get_user_info(u: user.User) -> dict:
        user_info = sync(u.get_user_info())
        avatar_url = user_info['face']
        nickname = user_info['name']
        return dict(nick_name=nickname, avatar_url=avatar_url)
    
    # 获取up动态信息
    @staticmethod
    def get_dynamic_data(u: user.User) -> dict:
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
    def get_video_data(u: user.User) -> dict:
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
