import os

from PySide6.QtGui import QCloseEvent, QIcon, QAction
from PySide6.QtWidgets import (QWidget, QGridLayout, QMainWindow, QMenu, QSystemTrayIcon)
from qt_material import QtStyleTools

from monitor.Monitor import Monitor
from utils.Config import Config
from utils.Style import Style


class BiliTV(QMainWindow, QtStyleTools):
    layout: QGridLayout
    icon: QIcon
    context_menu: QMenu
    tray_icon: QSystemTrayIcon
    
    def __init__(self):
        super().__init__()
        self.init_window()
        self.create_monitor()
        self.init_ui()
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
    
    def init_ui(self):
        self.icon = QIcon("favicon.ico")
        self.setWindowIcon(self.icon)
        self.create_tray_icon(self.icon)
        self.tray_icon.show()
    
    def create_context_menu(self):
        quit_action = QAction("退出", self, triggered=lambda: os._exit(0))
        
        menu = QMenu(self)
        menu.addAction(quit_action)
        return menu
    
    def create_tray_icon(self, icon):
        self.context_menu = self.create_context_menu()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(self.context_menu)
        self.tray_icon.setIcon(icon)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.showMinimized()
