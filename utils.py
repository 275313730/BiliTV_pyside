import json
import os
import sys
import logging
from threading import Timer
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


def set_timeout(ms, fn, *args, **kwargs):
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))  # 重点


sys.excepthook = handle_exception  # 重点

