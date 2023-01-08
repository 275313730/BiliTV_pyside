import os

from PySide6.QtWidgets import (QWidget, QGridLayout, QMainWindow)
from qt_material import QtStyleTools

from monitor.MonitorManager import MonitorManager
from monitor.Monitor import Monitor
from utils import Config


class BiliTV(QMainWindow, QtStyleTools):
    layout: QGridLayout = None
    monitorManager = MonitorManager()

    def __init__(self):
        super().__init__()
        self.init_window()
        self.create_monitor()
        self.show()

    def init_window(self):
        self.apply_stylesheet(self, theme=f'{Config.load("current_theme")}.xml')
        central_widget = QWidget()
        extra_stylesheet = ".BiliTV{{background-color:{QTMATERIAL_SECONDARYCOLOR}}}"
        self.setStyleSheet(extra_stylesheet.format(**os.environ))
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.move(200, 200)
        self.setWindowTitle("BiliTV")

    def create_monitor(self):
        for i in range(Config.load('max_row')):
            for j in range(Config.load('window_per_row')):
                position = [i, j]
                monitor = Monitor(position)
                self.monitorManager.add_monitor(monitor)
                self.layout.addWidget(monitor, *position)
