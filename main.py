import sys
from PySide6.QtWidgets import QApplication

from BiliTV import BiliTV


def main():
    app = QApplication(sys.argv)
    tv = BiliTV()
    sys.exit(app.exec())


if __name__ == '__main__':  
    main()
