from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class MonitorScreen(QWidget):
    uid: int = 0
    dynamic: QLabel = None
    dynamic_check: bool = True
    video: QLabel = None
    video_check: bool = True
    live: QLabel = None

    def __init__(self, uid: int):
        super().__init__()

        self.uid = uid
        v_box = QVBoxLayout(self)
        self.init_ui(v_box)
        self.show()

    def init_ui(self, v_box: QVBoxLayout):
        self.dynamic = QLabel("")
        self.video = QLabel("")
        self.live = QLabel("")
        v_box.addWidget(self.dynamic)
        v_box.addSpacing(5)
        v_box.addWidget(self.video)
        v_box.addSpacing(5)
        v_box.addWidget(self.live)

    def update_label(self, data_type: str, data_content: dict):
        if data_type == "dynamic":
            if data_content['dynamic_update'] and not self.dynamic_check:
                self.dynamic.setText("发布新动态，点击查看")
            else:
                self.dynamic.setText("暂无新动态")
        elif data_type == "video":
            if data_content['video_update'] and not self.video_check:
                self.video.setText("发布新视频，点击查看")
            else:
                self.video.setText("暂无新视频")
        elif data_type == "live":
            if data_content["live_status"] == 1:
                self.live.setText("直播中")
            else:
                self.live.setText("咕咕咕")
