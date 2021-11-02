import threading
import time
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QWheelEvent, QPixmap
from PyQt5.QtWidgets import QMainWindow, QPushButton

from Crawler.Crawler import Crawler
from widgets.ConsecutiveImageViewer import ConsecutiveImageViewer
from widgets.StatusWidget import StatusWidget


class ToonGround(QMainWindow):
    def __init__(self, toon_title, toon_id):
        super().__init__()
        self.__toon_title = toon_title
        self.__toon_id = toon_id
        self.__toon_image_viewer = None
        self.__toon_image_list = []
        self.__auto_scroll_running = False
        self.__auto_scroll_speed = 1
        self.__auto_scroll_thread = None
        self.__crawler = Crawler()

        self.__last_saved_epi = 0
        self.__current_idx = -2
        self.__last_epi_no = \
            int(self.__crawler.get_last_epi_no(self.__toon_id))

        self.__request_toon_images(1)
        self.__caching_all_toon_images()
        self.__set_background()
        self.__init_ui()
        self.show()

    def toon_viewer_move_callback(self, direction):
        pixmap = QPixmap()
        if direction == 'next':
            self.__current_idx = self.__current_idx + 1
            pixmap.load(self.__toon_image_list[self.__current_idx + 1])
            self.__toon_image_viewer.set_next_img(pixmap)
        elif self.__current_idx > -1:
            self.__current_idx = self.__current_idx - 1
            pixmap.load(self.__toon_image_list[self.__current_idx - 1])
            self.__toon_image_viewer.set_prev_img(pixmap)
        self.__update_status_window()

    def wheelEvent(self, e: QWheelEvent):
        self.__toon_image_viewer.scroll_with_value(e.angleDelta().y())

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.next_button.move(self.width() - 90, self.height() - 280)
        self.prev_button.move(self.width() - 170, self.height() - 280)
        self.auto_scroll_button.move(self.width() - 250, self.height() - 280)
        self.stat_window.move(self.width() - 340, self.height() - 200)
        self.__toon_image_viewer.move(int(self.width() / 2 - self.__toon_image_viewer.width() / 2), 0)
        self.__toon_image_viewer.set_height(self.height())

    def __move_prev(self):
        if self.__current_idx > 0:
            self.__toon_image_viewer.move_prev()

    def __move_next(self):
        if self.__current_idx < len(self.__toon_image_list) - 1:
            self.__toon_image_viewer.move_next()

    def __toggle_auto_scroll(self):
        if self.__auto_scroll_running:
            self.__auto_scroll_running = False
        else:
            self.__auto_scroll_thread = threading.Thread(target=self.__scroll_down_in_thread, daemon=True)
            self.__auto_scroll_running = True
            self.__auto_scroll_thread.start()

    def __scroll_down_in_thread(self):
        while self.__auto_scroll_running:
            self.__toon_image_viewer.scroll_with_value(-50)
            time.sleep(0.005)

    def __caching_all_toon_images(self):
        # 학교에서 과도한 패킷을 날리는 것을 방지하기 위해 받아오는 웹툰 회차를 3으로 제한
        threading.Thread(target=self.__request_toon_images, args=(3, ), daemon=True).start()

    def __request_toon_images(self, until):
        while self.__last_saved_epi < until:
            self.__last_saved_epi += 1
            new_images = self.__crawler.get_toon_images(self.__toon_id, self.__last_saved_epi)
            self.__toon_image_list += new_images

    def __set_background(self):
        self.setStyleSheet("background-color: black;")

    def __init_ui(self):
        self.setMinimumSize(1540, 920)
        self.__init_buttons()
        self.__init_status_window()
        self.__init_image_viewer()

    def __init_status_window(self):
        self.stat_window = StatusWidget(self)
        self.stat_window.set_title(self.__toon_title)
        self.stat_window.set_end_of_epi(self.__last_epi_no)

    def __update_status_window(self):
        self.stat_window.set_current_epi(self.__current_idx // 4 + 1)

    def __init_image_viewer(self):
        self.__toon_image_viewer = ConsecutiveImageViewer(self, self.toon_viewer_move_callback)
        self.__toon_image_viewer.resize(710, self.height())
        self.__toon_image_viewer.ready()

    def __init_buttons(self):
        icon_size = QSize(74, 74)
        self.next_button = QPushButton('', self)
        self.next_button.setStyleSheet(
            'QPushButton'
            '{ background-image: url("./res/ic_next.png"); }'
            "QPushButton::hover"
            '{ background-image: url("./res/ic_next_mouse_on.png"); }'
        )
        self.next_button.resize(icon_size)
        self.next_button.clicked.connect(self.__move_next)

        self.prev_button = QPushButton('', self)
        self.prev_button.setStyleSheet(
            'QPushButton'
            '{ background-image: url("./res/ic_prev.png"); }'
            "QPushButton::hover"
            '{ background-image: url("./res/ic_prev_mouse_on.png"); }'
        )
        self.prev_button.resize(icon_size)
        self.prev_button.clicked.connect(self.__move_prev)

        self.auto_scroll_button = QPushButton('', self)
        self.auto_scroll_button.setStyleSheet(
            'QPushButton'
            '{ background-image: url("./res/ic_auto_scroll.png"); }'
            "QPushButton::hover"
            '{ background-image: url("./res/ic_auto_scroll_mouse_on.png"); }'
        )
        self.auto_scroll_button.resize(icon_size)
        self.auto_scroll_button.clicked.connect(self.__toggle_auto_scroll)
