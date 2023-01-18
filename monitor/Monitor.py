from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QHBoxLayout, QFrame

from utils import Config
from .DataManager import DataManager
from .MonitorButton import MonitorButton
from .MonitorScreen import MonitorScreen


class Monitor(QFrame):
    position: list[int] = []
    add_up_signal: Signal = None
    change_up_signal: Signal = None
    button: MonitorButton = None
    screen: MonitorScreen = None
    layout: QHBoxLayout = None
    
    def __init__(self, position: list[int]):
        super().__init__()
        self.setMinimumSize(*Config.load('min_size'))
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.position = position
        self.create_button()
        self.show()
    
    def create_button(self):
        button = MonitorButton(self.emit_uid)
        self.layout.addWidget(button)
        self.button = button
    
    def create_screen(self, uid: int):
        screen = MonitorScreen(uid, self.emit_reset)
        self.layout.addWidget(screen)
        self.screen = screen
        self.screen.change_up_signal = self.change_up_signal
        DataManager.add_up(uid, self.position)
        self.add_up_signal.emit(uid)
    
    def emit_uid(self, uid: int):
        self.button.hide()
        self.create_screen(uid)
    
    def emit_reset(self, uid: int):
        self.screen.deleteLater()
        DataManager.del_up(uid)
        self.button.show()
