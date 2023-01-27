from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton, QInputDialog, QMessageBox

from utils.DataManager import DataManager


class MonitorButton(QPushButton):
    add_up_signal: Signal
    
    def __init__(self):
        super().__init__()
        self.setText("添加up主")
        self.setMinimumSize(50, 20)
        self.clicked.connect(self.on_click)
        self.enterEvent = lambda event: self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def on_click(self) -> None:
        text, ok = QInputDialog.getText(self, 'uid设置',
                                        '输入up主的uid:')
        if ok:
            if text.isnumeric():
                uid = int(text)
                if DataManager.check_up_exist(uid):
                    QMessageBox.about(self, "错误", "up主已添加")
                else:
                    self.add_up_signal.emit(uid)
            else:
                QMessageBox.about(self, "错误", "请输入数字")
