from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel, QComboBox

class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('串口通信')
        self.setGeometry(100, 100, 800, 600)

        self.port_combo = QComboBox(self)
        self.baudrate_combo = QComboBox(self)
        self.baudrate_combo.addItems(['9600', '19200', '38400', '57600', '115200'])

        self.open_button = QPushButton('打开串口', self)
        self.send_button = QPushButton('发送数据', self)

        self.receive_area = QTextEdit(self)
        self.receive_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('串口号'))
        layout.addWidget(self.port_combo)
        layout.addWidget(QLabel('波特率'))
        layout.addWidget(self.baudrate_combo)
        layout.addWidget(self.open_button)
        layout.addWidget(self.send_button)
        layout.addWidget(self.receive_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)