import platform


class Const:
    dynamic_url: str = "https://t.bilibili.com/"
    video_url: str = "https://www.bilibili.com/video/"
    min_size: list[int] = [250, 150]
    padding_size: list[int] = [10, 10]
    loop_time: float = 3000
    system: str = platform.system().lower()
