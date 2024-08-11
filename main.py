from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import os

includePath = os.path.abspath(os.getcwd() + '\\Include')
sys.path.append(includePath)

from wallpaperdl import WallpaperDL

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WallpaperDL()
    window.show()
    app.exec_()