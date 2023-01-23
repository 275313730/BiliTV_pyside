import os

from PySide6.QtWidgets import QWidget


class Style:
    active_label_style: str = ".QLabel{{color:white;}} .QLabel:hover{{background-color:{QTMATERIAL_SECONDARYCOLOR};border-radius:5px}}"
    normal_label_style: str = ".QLabel{{color:{QTMATERIAL_SECONDARYLIGHTCOLOR};}}"
    close_button_style: str = ".QLabel{{color:white;}} .QLabel:hover{{color:{QTMATERIAL_SECONDARYLIGHTCOLOR}}}"
    
    @staticmethod
    def change_stylesheet(o: QWidget, extra_stylesheet: str):
        o.setStyleSheet(extra_stylesheet.format(**os.environ))
