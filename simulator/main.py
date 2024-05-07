import sys
from PyQt5.QtWidgets import QApplication
from simulator_window import SimulatorWindow

def main():
    app = QApplication(sys.argv)
    main_window = SimulatorWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
