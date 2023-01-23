from json import load, dumps

from utils.Utils import Utils


class Config:
    @staticmethod
    def load(property_name):
        fr = open(Utils.get_path() + '/config.json', 'r', encoding="utf-8")
        config_data = load(fr)
        fr.close()
        return config_data[property_name]
    
    @staticmethod
    def modify(property_name, property_content):
        fr = open(Utils.get_path() + 'config.json', 'r', encoding="utf-8")
        config_data = load(fr)
        config_data[property_name] = property_content
        fr.close()
        fw = open(Utils.get_path() + 'config.json', 'w', encoding="utf-8")
        fw.write(dumps(config_data))
        fw.close()
