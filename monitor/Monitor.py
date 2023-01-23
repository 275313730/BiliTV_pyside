from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QHBoxLayout, QFrame

from utils.Const import Const
from utils.DataManager import DataManager
from .MonitorButton import MonitorButton
from .MonitorScreen import MonitorScreen


class Monitor(QFrame):
    position: list[int] = []
    add_up_signal: Signal = None
    del_up_signal: Signal = Signal(int)
    button: MonitorButton = None
    screen: MonitorScreen = None
    layout: QHBoxLayout = None
    
    def __init__(self, position: list[int]):
        super().__init__()
        self.setMinimumSize(*Const.min_size)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.position = position
        self.create_button()
        self.del_up_signal.connect(self.emit_reset)
        self.show()
    
    def create_button(self):
        button = MonitorButton(self.emit_uid)
        self.layout.addWidget(button)
        self.button = button
    
    def create_screen(self, uid: int):
        screen = MonitorScreen(uid)
        screen.del_up_signal = self.del_up_signal
        self.layout.addWidget(screen)
        self.screen = screen
        DataManager.add_up(uid, self.position)
        self.add_up_signal.emit(uid)
    
    def emit_uid(self, uid: int):
        self.button.hide()
        self.create_screen(uid)
    
    def emit_reset(self, uid: int):
        self.screen.deleteLater()
        DataManager.del_up(uid)
        self.button.show()
