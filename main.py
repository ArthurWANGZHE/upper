import sys
from PyQt5.QtWidgets import QApplication
from Ui import Ui
from communication import Communication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui()
    comm = Communication(ui)
    ui.show()
    sys.exit(app.exec_())