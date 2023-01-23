import os

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (QWidget, QGridLayout, QMainWindow)
from qt_material import QtStyleTools

from monitor.Monitor import Monitor
from utils.Config import Config
from utils.Style import Style


class BiliTV(QMainWindow, QtStyleTools):
    layout: QGridLayout = None
    
    def __init__(self):
        super().__init__()
        self.init_window()
        self.create_monitor()
        self.show()
    
    def init_window(self) -> None:
        self.apply_stylesheet(self, theme=f'{Config.load("current_theme")}.xml')
        central_widget = QWidget()
        Style.change_stylesheet(self, ".BiliTV{{background-color:{QTMATERIAL_SECONDARYCOLOR}}}")
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.move(200, 200)
        self.setWindowTitle("BiliTV")
    
    def create_monitor(self) -> None:
        for i in range(Config.load('max_row')):
            for j in range(Config.load('window_per_row')):
                position = [i, j]
                monitor = Monitor(position)
                self.layout.addWidget(monitor, *position)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        os._exit(0)
