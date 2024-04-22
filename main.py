import serial.tools.list_ports
import sys
import threading
import serial
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit,
                             QPushButton, QComboBox, QLabel, QMessageBox, QHBoxLayout)

class SerialPortThread(threading.Thread):
    def __init__(self, serial_instance, rx_text_edit, tx_text_edit):
        super().__init__()
        self.serial = serial_instance
        self.rx_text_edit = rx_text_edit
        self.tx_text_edit = tx_text_edit
        self.running = True

    def run(self):
        while self.running:
            if self.serial.inWaiting() > 0:
                try:
                    data = self.serial.readline().decode('utf-8', errors='ignore')
                    self.rx_text_edit.append(data)
                except serial.SerialException as e:
                    print(f"Error reading serial port: {e}")
                    break

    def stop(self):
        self.running = False

class SerialPortAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('串口调试助手')
        self.setGeometry(100, 100, 600, 400)
        self.serial_instance = None
        self.thread = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 串口号下拉框
        self.port_label = QLabel('串口号:')
        self.port_combo = QComboBox()
        self.port_combo.addItems(["COM2", "COM3"])  # 假设COM2和COM3已连接
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_combo)

        # 波特率下拉框
        self.baudrate_label = QLabel('波特率:')
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(['9600', '19200', '38400', '57600', '115200'])
        layout.addWidget(self.baudrate_label)
        layout.addWidget(self.baudrate_combo)

        # 打开串口按钮
        self.open_button = QPushButton('打开串口')
        self.open_button.clicked.connect(self.open_serial_port)
        layout.addWidget(self.open_button)

        # 发送按钮
        self.send_button = QPushButton('发送')
        self.send_button.clicked.connect(self.send_data)
        layout.addWidget(self.send_button)

        # 接收数据文本框
        self.rx_text_edit = QTextEdit()
        self.rx_text_edit.setReadOnly(True)
        layout.addWidget(self.rx_text_edit)

        # 发送数据文本框
        self.tx_text_edit = QTextEdit()
        layout.addWidget(self.tx_text_edit)

        # 发送布局
        send_layout = QHBoxLayout()
        self.send_layout_widget = QWidget()
        self.send_layout_widget.setLayout(send_layout)
        layout.addWidget(self.send_layout_widget)

        central_widget.setLayout(layout)

    def open_serial_port(self):
        port = self.port_combo.currentText()
        baudrate = int(self.baudrate_combo.currentText())
        self.serial_instance = serial.Serial(port, baudrate, timeout=1)
        if self.serial_instance.isOpen():
            self.start_serial_thread()
            self.open_button.setEnabled(False)
            self.send_button.setEnabled(True)
            QMessageBox.information(self, "串口状态", f"串口 {port} 已打开")
        else:
            QMessageBox.critical(self, "串口错误", "无法打开串口")

    def start_serial_thread(self):
        if self.thread is not None:
            self.thread.stop()
        self.thread = SerialPortThread(self.serial_instance, self.rx_text_edit, self.tx_text_edit)
        self.thread.start()

    def send_data(self):
        if self.serial_instance and self.serial_instance.isOpen():
            data = self.tx_text_edit.toPlainText()
            self.serial_instance.write(data.encode('utf-8'))
            self.tx_text_edit.append("Sent: " + data)  # 显示发送的数据

    def closeEvent(self, event):
        if self.thread:
            self.thread.stop()
            self.thread.join()
        if self.serial_instance:
            if self.serial_instance.isOpen():
                self.serial_instance.close()
            self.open_button.setEnabled(True)
            self.send_button.setEnabled(False)
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    main_window = SerialPortAssistant()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()