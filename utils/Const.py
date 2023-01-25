import platform


class Const:
    dynamic_url: str = "https://t.bilibili.com/"
    video_url: str = "https://www.bilibili.com/video/"
    min_size: list[int] = [250, 150]
    padding_size: list[int] = [10, 10]
    loop_time: float = 10000  # 单位:毫秒(ms)
    update_min_interval: float = 30  # 单位:秒(s)
    system: str = platform.system().lower()
