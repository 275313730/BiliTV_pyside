from PySide6.QtWidgets import QPushButton, QInputDialog, QMessageBox

from utils.DataManager import DataManager


class MonitorButton(QPushButton):
    def __init__(self, emit_uid: callable):
        super().__init__()
        self.setText("添加up主")
        self.setMinimumSize(50, 20)
        self.clicked.connect(lambda: self.on_click(emit_uid))
        self.show()

    def on_click(self, emit_uid: callable):
        text, ok = QInputDialog.getText(self, 'uid设置',
                                        '输入up主的uid:')
        if ok:
            if text.isnumeric():
                uid = int(text)
                if DataManager.check_up_exist(uid):
                    QMessageBox.about(self, "错误", "up主已添加")
                else:
                    emit_uid(uid)
            else:
                QMessageBox.about(self, "错误", "请输入数字")
