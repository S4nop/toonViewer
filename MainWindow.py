import atexit
from PyQt5.QtWidgets import *
from ToonGround import ToonGround
from Utils.Utils import clean_caches


def main():
    atexit.register(clean_caches)
    app = QApplication([])
    grn = ToonGround('전지적 독자 시점', '747269')
    app.exec()


if __name__ == '__main__':
    main()
