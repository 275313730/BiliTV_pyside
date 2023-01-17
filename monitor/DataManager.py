import json
import time


class DataManager:
    all_up_data: list[dict] = []
    
    @staticmethod
    def load_up_data():
        fr = open('up_data.json', 'r', encoding='utf-8')
        DataManager.all_up_data = json.load(fr)
        fr.close()
    
    @staticmethod
    def write_up_data():
        fw = open('up_data.json', 'w', encoding='utf-8')
        fw.write(json.dumps(DataManager.all_up_data))
        fw.close()
    
    @staticmethod
    def check_up_exist(uid):
        for data in DataManager.all_up_data:
            if data['uid'] == uid: return True
        return False
    
    @staticmethod
    def check_position_exist(position):
        for data in DataManager.all_up_data:
            if data['position'] == position: return True
        return False
    
    @staticmethod
    def get_up_data_from_uid(uid):
        for data in DataManager.all_up_data:
            if data['uid'] != uid: continue
            return data
        return None
    
    @staticmethod
    def get_up_data_from_position(position):
        for data in DataManager.all_up_data:
            if data['position'] != position: continue
            return data
        return None
    
    @staticmethod
    def add_up(uid, position):
        if DataManager.check_up_exist(uid): return False
        if DataManager.check_position_exist(position):
            DataManager.modify_up(uid, position)
        else:
            DataManager.all_up_data.append(
                dict(uid=uid, position=position, user=dict(avatar_url="", nick_name="", last_check_time=0),
                     dynamic=dict(time=0, id=0, last_check_time=0),
                     video=dict(time=0, bvid=0, last_check_time=0),
                     live=dict(live_status=0, url='', last_check_time=0)))
        DataManager.write_up_data()
        return True
    
    @staticmethod
    def modify_up(uid, position):
        for data in DataManager.all_up_data:
            if data['position'] != position: continue
            data['uid'] = uid
            return True
        return False
    
    @staticmethod
    def del_up(uid):
        if not DataManager.check_up_exist(uid): return False
        for data in DataManager.all_up_data:
            if data['uid'] != uid: continue
            DataManager.all_up_data.remove(data)
            DataManager.write_up_data()
            return True
        return False
    
    @staticmethod
    def update_up_data(uid: int, data_type: str, data_content: dict):
        up_data = DataManager.get_up_data_from_uid(uid)
        data = up_data[data_type]
        if data_type == 'user':
            data['avatar_url'] = data_content['avatar_url']
            data['nick_name'] = data_content['nick_name']
        elif data_type == 'dynamic':
            if data['time'] < data_content['time']:
                data['time'] = data_content['time']
                data['id'] = data_content['id']
                data['read'] = False
        elif data_type == 'video':
            if data['time'] < data_content['time']:
                data['time'] = data_content['time']
                data['bvid'] = data_content['bvid']
                data['read'] = False
        elif data_type == 'live':
            if data['live_status'] != data_content['live_status']:
                data['live_status'] = data_content['live_status']
                data['url'] = data_content['url']
        data['last_check_time'] = int(time.time())
        DataManager.write_up_data()
        return True
    
    @staticmethod
    def need_update(uid: int, data_type: str):
        t = int(time.time())
        up_data = DataManager.get_up_data_from_uid(uid)
        last_check_time = up_data[data_type]['last_check_time']
        if data_type == "user":
            return t - last_check_time > 24 * 60 * 60 * 1000
        elif data_type == "dynamic":
            return t - last_check_time > 2 * 60 * 1000
        elif data_type == "video":
            return t - last_check_time > 2 * 60 * 1000
        elif data_type == "live":
            return t - last_check_time > 2 * 60 * 1000


DataManager.load_up_data()
