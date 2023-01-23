import json


class Config:
    @staticmethod
    def load(property_name):
        fr = open('config.json', 'r', encoding="utf-8")
        config_data = json.load(fr)
        fr.close()
        return config_data[property_name]
    
    @staticmethod
    def modify(property_name, property_content):
        fr = open('config.json', 'r', encoding="utf-8")
        config_data = json.load(fr)
        config_data[property_name] = property_content
        fr.close()
        fw = open('config.json', 'w', encoding="utf-8")
        fw.write(json.dumps(config_data))
        fw.close()
