# 定义通信协议，实现串口通信
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel, QComboBox, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal
import serial
import serial.tools.list_ports
import struct

class SerialThread(QThread):
    received_data = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, port, baudrate):
        self.serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.running = False

    def run(self):
        try:
            self.serial.open()
            self.running = True
            while self.running:
                if self.serial.in_waiting:
                    data = self.serial.read_all().decode('utf-8')
                    self.received_data.emit(data)
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            if self.serial.is_open:
                self.serial.close()
            self.running = False

    def stop(self):
        self.running = False
        if self.serial.is_open:
            self.serial.close()



    def write_data(self, data):
        if self.serial.is_open:
            try:
                self.serial.write(data.encode('utf-8'))
            except Exception as e:
                self.error_signal.emit(str(e))

class Communication:
    def __init__(self):
        self.serial_thread = None

    def packing(self,points, velocity, acceleration, jerk):
        packges=[]

        length=len(points)-1
        for i in range(length):
            packge = []
            packge.append(points[i])
            packge.append(points[i+1])
            packge.append(velocity[i])
            packge.append(acceleration[i])
            packge.append(jerk[i])
            packges.append(packge)
        return packges

    def write(self,package):
        data = package

        # 包头和包尾
        header = b'\xFF'
        footer = b'\xFE'

        # 打包数据部分，使用'<'作为小端序的指定，'d'表示双精度浮点数
        packed_data = b''
        for point in data:
            packed_data += struct.pack('<3d', *point)  # 每个点包含3个双精度浮点数

        # 完整的数据包
        complete_packet = header + packed_data + footer
        return complete_packet

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def open_serial(self):
        if self.serial_thread and self.serial_thread.isRunning():
            self.serial_thread.stop()
            self.open_button.setText("打开串口")
            print("串口已关闭")
        else:
            port = self.port_combo.currentText()
            baudrate = int(self.baudrate_combo.currentText())
            self.serial_thread = SerialThread(port, baudrate)
            self.serial_thread.received_data.connect(self.receive_data)
            self.serial_thread.error_signal.connect(self.handle_error)
            self.serial_thread.start()
            self.open_button.setText("关闭串口")
            print("串口已打开")

    def send_data(self,data):
        if self.serial_thread and self.serial_thread.serial.is_open:
            self.serial_thread.write_data(data)
            print(f"发送数据: {data}")
        else:
            print("串口未打开或发送线程未启动")

    def receive_data(self, data):
        self.receive_area.insertPlainText(data)

    def handle_error(self, error_message):
        print(f"发生错误: {error_message}")
        self.receive_area.insertPlainText(f"\n错误: {error_message}\n")

    def closeEvent(self, event):
        if self.serial_thread and self.serial_thread.isRunning():
            self.serial_thread.stop()
        super().closeEvent(event)