import requests
from PySide6.QtCore import Qt, QPropertyAnimation, Property
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView


class MonitorScreen(QWidget):
    uid: int = 0
    size: int = 95
    view: QGraphicsView = None
    scene: QGraphicsScene = None
    avatar: QLabel = None
    animation: QPropertyAnimation = None
    target: QPixmap = None
    pixmap: QPixmap = None
    pixmap_item: QGraphicsPixmapItem = None
    avatar_url: str = None
    dynamic: QLabel = None
    dynamic_check: bool = True
    video: QLabel = None
    video_check: bool = True
    live: QLabel = None

    def __init__(self, uid: int):
        super().__init__()
        self.uid = uid
        self.init_ui()
        self.show()

    # 初始化ui
    def init_ui(self):
        v_box = QVBoxLayout(self)
        self.init_avatar(v_box)
        self.dynamic = QLabel("")
        self.video = QLabel("")
        self.live = QLabel("")
        # v_box.addWidget(self.dynamic)
        # v_box.addSpacing(5)
        # v_box.addWidget(self.video)
        # v_box.addSpacing(5)
        # v_box.addWidget(self.live)

    def init_avatar(self, v_box: QVBoxLayout):
        self.avatar = QLabel()
        self.target = QPixmap(self.size, self.size)
        self.target.fill(Qt.transparent)
        v_box.addWidget(self.avatar)

    #  更新头像
    def update_avatar(self, avatar_url: str) -> bool:
        if avatar_url == self.avatar_url: return False
        self.avatar_url = avatar_url
        res = requests.get(avatar_url)
        img = QImage.fromData(res.content)
        self.pixmap = QPixmap.fromImage(img).scaled(self.size, self.size, Qt.KeepAspectRatioByExpanding,
                                                    Qt.SmoothTransformation)

        self.avatar.show()
        if self.animation is None: self.start_animation()
        return True

    def rotate_avatar(self, degree: int):
        painter = QPainter(self.target)
        painter.translate(self.size / 2, self.size / 2)
        painter.rotate(float(degree))
        painter.translate(-self.size / 2, -self.size / 2)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.LosslessImageRendering, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.size, self.size, self.size, self.size)
        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        self.avatar.setPixmap(self.target)

    def start_animation(self):
        self.animation = QPropertyAnimation(self, b'rotation')
        self.animation.setDuration(20000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
        self.animation.start()

    rotation = Property(int, fset=rotate_avatar)

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
