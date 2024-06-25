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
        super().__init__()
        self.serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.bytesize = 8  # 设置数据位
        self.serial.stopbits = 1  # 设置停止位
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
    def __init__(self, port='COM7', baudrate=9600):
        self.serial_thread = SerialThread(port, baudrate)
        self.serial_thread.received_data.connect(self.receive_data)
        self.serial_thread.error_signal.connect(self.handle_error)
        self.serial_thread.start()
        # Adding a small delay to ensure the serial port has time to open
        import time
        time.sleep(0.1)  # Adjust the delay as needed


    def is_serial_connected(self):
        return self.serial_thread.serial.is_open


    def process_number1(self,num):
        # 四舍五入取整
        rounded_num = round(num)

        # 判断原来的数是正还是负
        is_negative = rounded_num < 0

        # 如果是负数，取其绝对值进行后续处理
        if is_negative:
            rounded_num = abs(rounded_num)
        hex_num = hex(int(rounded_num))[2:]

        hex_result = hex_num.zfill(4)


        """
        # 把16进制转换成2进制
        bin_num = bin(int(hex_num, 16))

        # 取二进制反码
        bin_num_inverse = ''.join('1' if bit == '0' else '0' for bit in bin_num[2:])

        # 如果是负数，采用2进制补码
        if is_negative:
            # 找到最高位的1，然后取反
            index_of_first_one = bin_num_inverse.find('1')
            bin_num_complement = bin_num_inverse[:index_of_first_one] + bin_num[2:][index_of_first_one:]
        else:
            bin_num_complement = bin_num_inverse

        # 把这个2进制转化为16进制
        hex_result = hex(int(bin_num_complement, 2))[2:].zfill(4)
        """

        return hex_result

    def process_number2(self,num):
        # 四舍五入取整
        rounded_num = round(num)

        # 判断原来的数是正还是负
        is_negative = rounded_num < 0

        # 如果是负数，取其绝对值进行后续处理
        if is_negative:
            rounded_num = abs(rounded_num)

        # 转换为16进制
        hex_num = hex(int(rounded_num))

        # 把16进制转换成2进制
        bin_num = bin(int(hex_num, 16))

        # 取二进制反码
        bin_num_inverse = ''.join('1' if bit == '0' else '0' for bit in bin_num[2:])

        # 如果是负数，采用2进制补码
        if is_negative:
            # 找到最高位的1，然后取反
            index_of_first_one = bin_num_inverse.find('1')
            bin_num_complement = bin_num_inverse[:index_of_first_one] + bin_num[2:][index_of_first_one:]
        else:
            bin_num_complement = bin_num_inverse

        # 把这个2进制转化为16进制
        hex_result = hex(int(bin_num_complement, 2))[2:].zfill(2)

        return hex_result

    def packing(self,points, velocity, acceleration, jerk):
        packges=[]

        length=len(points)-1
        for i in range(length):
            packge = []
            packge.append(points[i])
            packge.append(points[i+1])
            packge.append(velocity[i])
            packge.append(acceleration[i])
            # packge.append(jerk[i])
            packges.append(packge)
            # print(packge)
        return packges

    def write(self,package):
        data = package
        # package[[x1,y1,z1],[x2,y2,z2],v,a]
        # print(data[0][0])

        # 包头和包尾
        header = 'FF0'
        footer = 'FE'
        x1,y1,z1,x2,y2,z2 = data[0][0]*100,data[0][1]*100,data[0][2]*100,data[1][0]*100,data[1][1]*100,data[1][2]*100
        v1,a1=data[2],data[3]
        ppp=[x1,y1,z1,x2,y2,z2,v1,a1]
        #print(ppp)
        # print(x1)
        mse=1000
        if x1 >=0:
            mse=mse+100
        if y1>=0:
            mse=mse+10
        if z1>=0:
            mse=mse+1
        # print(mse)
        mse_str=str(mse)
        oo=int(mse_str,2)
        hex_num=hex(oo)
        # print(hex_num)
        int_num = int(hex_num, 16)
        rnum = hex(int_num)[2:]

        a=self.process_number1(x1)
        b=self.process_number1(y1)
        c=self.process_number1(z1)
        d=self.process_number1(x2)
        e=self.process_number1(y2)
        f=self.process_number1(z2)

        g=self.process_number2(v1)
        h=self.process_number2(a1)

        complete_package=''
        complete_package+=header
        complete_package += rnum
        complete_package+=' '
        complete_package+=a
        #complete_package+=d
        complete_package += ' '
        complete_package+=b
        #complete_package+=e
        complete_package += ' '
        complete_package+=c
        #complete_package+=f
        complete_package += ' '
        complete_package+=g
        complete_package += ' '
        complete_package+=h
        complete_package += ' '
        complete_package+=footer
        #print(complete_package)
        return complete_package


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

    def send_data(self, data):
        if self.serial_thread and self.serial_thread.serial.is_open:
            # 将十六进制字符串转换为字节
            data_bytes = bytes.fromhex(data)
            self.serial_thread.serial.write(data_bytes)
            print(f"发送数据: {data}")
            # 接收并处理返回的信息
            # response = self.serial_thread.serial.read(2).decode('utf-8')
            # print(f"接收到返回信息: {response}")

        else:
            print("串口未打开或发送线程未启动")

    def receive_data(self):
        # 接收并处理返回的信息
        response = self.serial_thread.serial.read(2).decode('utf-8')
        # print(f"接收到返回信息: {response}")
        return response

    def handle_error(self, error_message):
        print(f"发生错误: {error_message}")
        self.receive_area.insertPlainText(f"\n错误: {error_message}\n")

    def closeEvent(self, event):
        if self.serial_thread and self.serial_thread.isRunning():
            self.serial_thread.stop()
        super().closeEvent(event)