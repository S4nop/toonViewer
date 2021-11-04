import threading

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QBrush, QPalette, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QSizePolicy, QScrollArea, QVBoxLayout, QLayout

_lock = threading.Lock()
class ConsecutiveImageViewer(QWidget):
    def __init__(self, parent, move_callback):
        super(ConsecutiveImageViewer, self).__init__(parent)

        self.inner_widget = QWidget()
        self.inner_widget.resize(690, 150000)

        self.move_callback = move_callback
        self.current_viewer_idx = 0

        self.__init_scroll_area()

    def set_height(self, height):
        self.scroll_area.resize(self.scroll_area.width(), height)
        self.resize(self.scroll_area.width(), height)
        for i in range(0, 3):
            self.image_viewers[i].adjustSize()

    def set_next_img(self, img):
        next_viewer = self.__get_next_viewer()
        next_viewer.setFixedSize(QSize(img.width(), img.height()))
        next_viewer.setPixmap(img)

    def set_prev_img(self, img):
        prev_viewer = self.__get_prev_viewer()
        prev_viewer.setFixedSize(QSize(img.width(), img.height()))
        prev_viewer.setPixmap(img)

    def ready(self):
        self.image_viewers = [
            QLabel(self.inner_widget),
            QLabel(self.inner_widget),
            QLabel(self.inner_widget),
        ]
        for i in range(1, 3):
            self.move_next()

        self.__get_prev_viewer().move(0, -30000)

    def scroll_with_value(self, delta):
        _lock.acquire()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().value() - delta)
        _lock.release()
        self.__wheel_event(None)

    def move_next(self):
        self.__reorder_to_next()
        self.current_viewer_idx = (self.current_viewer_idx + 1) % 3
        self.move_callback('next')

    def move_prev(self):
        self.__reorder_to_prev()
        self.current_viewer_idx = 2 if self.current_viewer_idx == 0 else (self.current_viewer_idx - 1)
        self.move_callback('prev')

    def __wheel_event(self, e):
        if self.__get_next_viewer().y() - self.scroll_area.verticalScrollBar().value() < 120:
            self.move_next()
        # 버그가 있어 일단 Disable
        # elif self.__get_curr_viewer().y() - self.scroll_area.verticalScrollBar().value() > -120:
        #     self.move_prev()

    def __reorder_to_next(self):
        prev_viewer = self.__get_prev_viewer()
        curr_viewer = self.__get_curr_viewer()
        next_viewer = self.__get_next_viewer()
        curr_viewer.move(0, 0)
        next_viewer.move(0, curr_viewer.y() + curr_viewer.height())
        prev_viewer.move(0, next_viewer.y() + next_viewer.height())
        _lock.acquire()
        self.scroll_area.verticalScrollBar().setValue(next_viewer.y())
        _lock.release()

    def __reorder_to_prev(self):
        prev_viewer = self.__get_prev_viewer()
        curr_viewer = self.__get_curr_viewer()
        next_viewer = self.__get_next_viewer()
        next_viewer.move(0, 0)
        prev_viewer.move(0, next_viewer.y() + next_viewer.height())
        curr_viewer.move(0, prev_viewer.y() + prev_viewer.height())
        _lock.acquire()
        self.scroll_area.verticalScrollBar().setValue(prev_viewer.y())
        _lock.release()

    def __get_prev_viewer(self):
        return self.image_viewers[self.current_viewer_idx - 1]

    def __get_curr_viewer(self):
        return self.image_viewers[self.current_viewer_idx]

    def __get_next_viewer(self):
        return self.image_viewers[(self.current_viewer_idx + 1) % 3]

    def __init_scroll_area(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.inner_widget)
        self.scroll_area.resize(690, self.height())
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inner_widget.wheelEvent = self.__wheel_event
