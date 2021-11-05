from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QBrush, QPalette, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout

HEIGHT_SIZE = 190
WIDTH_SIZE = 320


class StatusWidget(QWidget):
    def __init__(self, parent):
        super(StatusWidget, self).__init__(parent)
        self.__set_background()
        self.__init_ui()
        self.__epi_setter = None
        self.show()

    def set_title(self, title):
        self.title_label.setText(str(title))

    def set_sub_title(self, sub_title):
        self.sub_title_label.setText(str(sub_title))

    def set_end_of_epi(self, eoe):
        self.eoe_label.setText(str(eoe))

    def set_current_epi(self, curr_epi):
        self.curr_epi_txt.setText(str(curr_epi))

    def set_epi_setter(self, setter_func):
        self.__epi_setter = setter_func

    def __force_set_epi(self):
        self.__epi_setter()

    def __init_ui(self):
        self.setFixedSize(WIDTH_SIZE, HEIGHT_SIZE)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.inner_layout = QHBoxLayout()

        self.title_label = QLabel("제목", self)
        self.title_label.setAlignment(Qt.AlignHCenter)
        self.title_label.font().setBold(True)
        self.title_label.move(0, 8)
        self.title_label.resize(WIDTH_SIZE, 32)
        self.title_label.setFont(QtGui.QFont("a디딤돌", 22))
        self.title_label.setStyleSheet('background-color: rgba(0, 0, 0, 0); Color: #999999')

        self.sub_title_label = QLabel("SN-ToonViewer", self)
        self.sub_title_label.setAlignment(Qt.AlignHCenter)
        self.sub_title_label.font().setBold(True)
        self.sub_title_label.move(0, 48)
        self.sub_title_label.resize(WIDTH_SIZE, 32)
        self.sub_title_label.setFont(QtGui.QFont("a디딤돌", 22))
        self.sub_title_label.setStyleSheet('background-color: rgba(0, 0, 0, 0); Color: #999999')

        self.curr_epi_txt = QLineEdit("0", self)
        self.curr_epi_txt.move(36, 110)
        self.curr_epi_txt.resize(110, 56)
        self.curr_epi_txt.setAlignment(Qt.AlignCenter)
        self.curr_epi_txt.setFont(QtGui.QFont("a디딤돌", 48))
        self.curr_epi_txt.setStyleSheet('background-color: rgba(0, 0, 0, 0); Color: white;')

        self.eoe_label = QLabel("720", self)
        self.eoe_label.setAlignment(Qt.AlignHCenter)
        self.eoe_label.font().setBold(True)
        self.eoe_label.move(192, 108)
        self.eoe_label.resize(110, 60)
        self.eoe_label.setFont(QtGui.QFont("a디딤돌", 52))
        self.eoe_label.setStyleSheet('background-color: rgba(0, 0, 0, 0); Color: #999999')

    def __set_background(self):
        self._background = QLabel("", self)
        self._background.move(0, 0)
        self._background.resize(WIDTH_SIZE, HEIGHT_SIZE)
        self._background.setStyleSheet('background-image: url("./res/bg_stat_bar.png");')
