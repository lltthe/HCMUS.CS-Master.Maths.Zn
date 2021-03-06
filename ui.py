import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class ZnCalcMainWindow(QMainWindow):
    def __init__(self):
        super(ZnCalcMainWindow, self).__init__()
        self.show()

class ZnCalc():
    def __init__(self):
        self.app = QApplication(sys.argv)

    def build(self):
        self.main = ZnCalcMainWindow()
        return self

    def go(self):
        sys.exit(self.app.exec_())