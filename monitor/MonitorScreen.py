import requests
from PySide6.QtCore import Qt, QPropertyAnimation, Property
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from utils import add_extra_stylesheet


class MonitorScreen(QWidget):
    uid: int = 0
    size: int = 95
    
    avatar: QLabel = None
    animation: QPropertyAnimation = None
    target: QPixmap = None
    pixmap: QPixmap = None
    avatar_url: str = None
    nick_name: QLabel = None
    
    dynamic: QLabel = None
    dynamic_check: bool = True
    video: QLabel = None
    video_check: bool = True
    live: QLabel = None
    live_status: bool = False
    
    switch: QLabel = None
    close: QLabel = None
    
    def __init__(self, uid: int):
        super().__init__()
        self.uid = uid
        self.init_ui()
        self.show()
    
    # 初始化ui
    def init_ui(self):
        v_box = QVBoxLayout(self)
        v_box.setContentsMargins(0, 5, 0, 0)
        self.nick_name = QLabel("")
        add_extra_stylesheet(self.nick_name, ".QLabel{{color:white;}}")
        self.nick_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box.addWidget(self.nick_name)
        h_widget = QWidget()
        h_box = QHBoxLayout(h_widget)
        h_box.setContentsMargins(0, 0, 0, 10)
        v_box.addWidget(h_widget)
        self.init_user(h_box)
        self.init_label(h_box)
        self.init_tool()
    
    def init_user(self, h_box: QHBoxLayout):
        self.avatar = QLabel()
        self.target = QPixmap(self.size, self.size)
        self.target.fill(Qt.transparent)
        self.init_animation()
        h_box.addWidget(self.avatar)
    
    def init_label(self, h_box: QHBoxLayout):
        label_widget = QWidget()
        v_box = QVBoxLayout(label_widget)
        h_box.addWidget(label_widget)
        self.dynamic = QLabel("")
        self.video = QLabel("")
        self.live = QLabel("")
        v_box.addWidget(self.dynamic)
        v_box.addWidget(self.video)
        v_box.addWidget(self.live)
    
    def init_tool(self):
        self.switch = QLabel("=", self)
        self.close = QLabel("X", self)
        add_extra_stylesheet(self.switch, ".QLabel{{color:white;}}")
        add_extra_stylesheet(self.close, ".QLabel{{color:white;}}")
        self.close.move(self.width() - 10, self.height() - 10)
        self.switch.move(self.width() - 20, self.height() - 10)
    
    #  更新用户信息
    def update_user_info(self, user_info: dict) -> bool:
        avatar_url = user_info['avatar_url']
        nick_name = user_info['nick_name']
        self.nick_name.setText(nick_name)
        if avatar_url == self.avatar_url: return False
        self.avatar_url = avatar_url
        res = requests.get(avatar_url)
        img = QImage.fromData(res.content)
        self.pixmap = QPixmap.fromImage(img).scaled(self.size, self.size, Qt.KeepAspectRatioByExpanding,
                                                    Qt.SmoothTransformation)
        self.rotate_avatar(0)
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
    
    def init_animation(self):
        self.animation = QPropertyAnimation(self, b'rotation')
        self.animation.setDuration(20000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
    
    rotation = Property(int, fset=rotate_avatar)
    
    def update_label(self, data_type: str, data_content: dict):
        if data_type == "dynamic":
            if not self.dynamic_check:
                add_extra_stylesheet(self.dynamic, ".QLabel{{color:QTMATERIAL_PRIMARYCOLOR;}}")
                self.dynamic.setText("发布新动态，点击查看")
            else:
                add_extra_stylesheet(self.dynamic, ".QLabel{{color:white;}}")
                self.dynamic.setText("暂无新动态")
        elif data_type == "video":
            if not self.video_check:
                add_extra_stylesheet(self.video, ".QLabel{{color:QTMATERIAL_PRIMARYCOLOR;}}")
                self.video.setText("发布新视频，点击查看")
            else:
                add_extra_stylesheet(self.video, ".QLabel{{color:white;}}")
                self.video.setText("暂无新视频")
        elif data_type == "live":
            if data_content["live_status"] == 1:
                self.live.setText("直播中")
                add_extra_stylesheet(self.live, ".QLabel{{color:{QTMATERIAL_PRIMARYCOLOR};}}")
                if not self.live_status:
                    self.live_status = True
                    self.animation.start()
            else:
                add_extra_stylesheet(self.live, ".QLabel{{color:white}}")
                self.live.setText("咕咕咕")
                if self.live_status:
                    self.live_status = False
                    self.animation.stop()
                    self.rotate_avatar(0)
