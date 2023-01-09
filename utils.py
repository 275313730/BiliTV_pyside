import json
import os

from PySide6.QtWidgets import QWidget


class Config:
    @staticmethod
    def load(property_name):
        fr = open('data/config.json', 'r', encoding="utf-8")
        config_data = json.load(fr)
        fr.close()
        return config_data[property_name]

    @staticmethod
    def modify(property_name, property_content):
        fr = open('data/config.json', 'r', encoding="utf-8")
        config_data = json.load(fr)
        config_data[property_name] = property_content
        fr.close()
        fw = open('data/config.json', 'w', encoding="utf-8")
        fw.write(json.dumps(config_data))
        fw.close()


def add_extra_stylesheet(o: QWidget, extra_stylesheet: str):
    stylesheet = o.styleSheet()
    o.setStyleSheet(stylesheet + extra_stylesheet.format(**os.environ))
