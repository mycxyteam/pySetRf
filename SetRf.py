import sys
import threading
from msilib import Dialog

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import logging
import serial
import serial.tools.list_ports

class CustomComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):  # 重写showPopup函数
        self.popupAboutToBeShown.emit()  # 发送信号
        super(CustomComboBox, self).showPopup()

#    def __init__(self, parent = None):
#        super(CustomComboBox,self).__init__(parent)

    """
    # 重写showPopup函数
    def showPopup(self):
        # 先清空原有的选项
        self.clear()
        index = 0
        # 获取接入的所有串口信息，插入combobox的选项中
        portlist = self.get_port_list(self)
        if portlist is not None:
            for i in portlist:
                self.insertItem(index, i)
                index += 1
        QComboBox.showPopup(self)   # 弹出选项框

    @staticmethod
    def get_port_list(self):
        try:
            port_list = serial.tools.list_ports.comports()
            print(port_list)
#            for port in port_list:
#                yield str(port)
        except Exception as e:
            logging.error("获取接入的所有串口设备出错！\n错误信息："+str(e))
    """
message_bandWidth_dict = {
    ''         : 0x80,
    'BW125KHZ' : 0x70,
    'BW250KHZ' : 0x80,
    'BW500KHZ' : 0x90


}
message_sprFactor_dict = {
    ''     : 0x70,
    'SF06' : 0x60,
    'SF07' : 0x70,
    'SF08' : 0x80,
    'SF09' : 0x90,
    'SF10' : 0xA0
}
message_codingRate_dict = {
    ''       : 0x04,
    'CR_4_5' : 0x02,
    'CR_4_6' : 0x04,
    'CR_4_7' : 0x06,
    'CR_4_8' : 0x08
}
message_TrueOrFalse_dict = {
    ''     : 0,
    'TRUE' : 1,
    'FALSE': 0
}

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
#        self.setupUi(self)
#        self.get_port_list()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RF数据设置"))

        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        com_name = []
        com_name = self.get_port_list()
        self.addLabel(self, QtCore.QRect(300, 90, 70, 25), "串口:")
        self.addComboBox_portName(self, QtCore.QRect(390, 90, 90, 25), com_name, "comboBox_portName")
        self.ComboBox_portName.popupAboutToBeShown.connect(self.update_portName)
        self.PushButton_Open = QtWidgets.QPushButton(self.centralWidget)
        self.addPushButton(self, QtCore.QRect(500, 90, 70, 25), "打开串口", self.PushButton_Open)
        self.PushButton_Open.clicked.connect(self.OpenSerial)

        self.addLabel(self, QtCore.QRect(260, 140, 140, 25), "LoRa_Freq：")
        self.addLabel(self, QtCore.QRect(260, 180, 140, 25), "BandWidth：")
        self.addLabel(self, QtCore.QRect(260, 220, 140, 25), "SprFactor：")
        self.addLabel(self, QtCore.QRect(260, 260, 140, 25), "CodingRate：")
        self.addLabel(self, QtCore.QRect(260, 300, 140, 25), "PowerCfig：")
        self.addLabel(self, QtCore.QRect(260, 340, 140, 25), "MaxPowerOn：")
        self.addLabel(self, QtCore.QRect(260, 380, 140, 25), "CRCON：")
        self.addLabel(self, QtCore.QRect(260, 420, 140, 25), "HeaderOn：")

        self.LineEdit_LoRa_Freq = QtWidgets.QLineEdit(self.centralWidget)
        self.ComboBox_BandWidth = QtWidgets.QComboBox(self.centralWidget)
        self.ComboBox_SprFactor = QtWidgets.QComboBox(self.centralWidget)
        self.ComboBox_CodingRate = QtWidgets.QComboBox(self.centralWidget)
        self.LineEdit_PowerCfig = QtWidgets.QLineEdit(self.centralWidget)
        self.ComboBox_MaxPowerOn = QtWidgets.QComboBox(self.centralWidget)
        self.ComboBox_CRCON = QtWidgets.QComboBox(self.centralWidget)
        self.ComboBox_HeaderOn = QtWidgets.QComboBox(self.centralWidget)
        self.addlineEdit(self, QtCore.QRect(450,140,120,25), self.LineEdit_LoRa_Freq)
        self.addComboBox(QtCore.QRect(450,180,120,25), "comboBox", self.ComboBox_BandWidth)
        self.ComboBox_BandWidth.addItems(["", "BW125KHZ", "BW250KHZ", "BW500KHZ"])
        self.addComboBox(QtCore.QRect(450, 220, 120, 25), "comboBox", self.ComboBox_SprFactor)
        self.ComboBox_SprFactor.addItems(["", "SF06", "SF07", "SF08", "SF09", "SF10", "SF11", "SF12"])
        self.addComboBox(QtCore.QRect(450, 260, 120, 25), "comboBox", self.ComboBox_CodingRate)
        self.ComboBox_CodingRate.addItems(["", "CR_4_5", "CR_4_6", "CR_4_7", "CR_4_8"])
        self.addlineEdit(self, QtCore.QRect(450, 300, 120, 25), self.LineEdit_PowerCfig)
        self.addComboBox(QtCore.QRect(450, 340, 120, 25), "comboBox", self.ComboBox_MaxPowerOn)
        self.ComboBox_MaxPowerOn.addItems(["", "TRUE", "FALSE"])
        self.addComboBox(QtCore.QRect(450, 380, 120, 25), "comboBox", self.ComboBox_CRCON)
        self.ComboBox_CRCON.addItems(["", "TRUE", "FALSE"])
        self.addComboBox(QtCore.QRect(450, 420, 120, 25), "comboBox", self.ComboBox_HeaderOn)
        self.ComboBox_HeaderOn.addItems(["", "TRUE", "FALSE"])

        self.PushButton_read = QtWidgets.QPushButton(self.centralWidget)
        self.PushButton_set = QtWidgets.QPushButton(self.centralWidget)
        self.addPushButton(self, QtCore.QRect(300, 500, 70, 30), "读取", self.PushButton_read)
        self.addPushButton(self, QtCore.QRect(450, 500, 70, 30), "设置", self.PushButton_set)
        self.PushButton_read.clicked.connect(self.TxReadInfo)
        self.PushButton_set.clicked.connect(self.TxWriteInfo)
        self.PushButton_set.setEnabled(False)
        self.PushButton_read.setEnabled(False)

    def update_portName(self):
        List = []
        List = self.get_port_list()
        self.ComboBox_portName.clear()
        for comName in List:
            self.ComboBox_portName.addItem(comName)


    def addLabel(self, argc, argv, argb):
        self.Label = QtWidgets.QLabel(self.centralWidget)
        self.Label.setGeometry(argv)
        self.Label.setObjectName("Label")
        self.Label.setText(argb)
        self.Label.setFont(QFont("宋体",12,QFont.Normal))
        self.Label.setAlignment(Qt.AlignRight)

    def addComboBox_portName(self, argc, argv, argb, argn):
        self.ComboBox_portName = CustomComboBox(self.centralWidget)
        self.ComboBox_portName.setGeometry(argv)
        self.ComboBox_portName.setObjectName(argn)
        self.ComboBox_portName.setAccessibleName(argn)
        for comName in argb:
            self.ComboBox_portName.addItem(comName)

    def addComboBox(self,argc,argv,argb):
        argb.setGeometry(argc)
        argb.setObjectName(argv)
        argb.setAccessibleName(argv)
#        argb.addItems(["BW125KHZ", "BW250KHZ", "BW500KHZ"])

    def addlineEdit(self, argc, argv, argb):
#        argb = QtWidgets.QLineEdit(self.centralWidget)
        argb.setGeometry(argv)
        argb.setObjectName("LineEdit")

    def addPushButton(self, argc, argv, argb,argn):
#        argn = QtWidgets.QPushButton(argc.centralWidget)
        argn.setGeometry(argv)
        argn.setText(argb)
 #       print(self.PushButton_read)


    def OpenSerial(self):
        if self.PushButton_Open.text() == "打开串口":
 #           serial.Serial.port = self.ComboBox_portName.currentText()
 #           print(serial.Serial)
            self.port_mes = QSerialPortInfo(self.ComboBox_portName.currentText())
            self.serial_port_state = self.port_mes.isBusy()
            if self.serial_port_state == False:
                self.SerialPort = serial.Serial()
                self.SerialPort.port = self.ComboBox_portName.currentText()
                self.SerialPort.baudrate = 19200#serial.Serial.baudrate = 19200
                self.SerialPort.bytesize = 8#serial.Serial.bytesize = 8
                self.SerialPort.stopbits = 1#serial.Serial.stopbits = 1
                self.SerialPort.parity = serial.PARITY_NONE#serial.Serial.parity = serial.PARITY_NONE
              #  print(serial.Serial.parity)
              #  print(serial.Serial.port)
                self.SerialPort.timeout = 0#serial.Serial.timeout = 0
                try:
                    # 打开串口
                    # self.port = serial.Serial(serial_name1, baud_rate, int(data_bseit), parity=serial.PARITY_NONE)#打开串口
                    # self.port.open()
#                    print(self.SerialPort)
                    self.SerialPort.open()
#                    print(self.SerialPort)
                    self.port_mes = QSerialPortInfo(self.SerialPort.port)  # 判断串口状态，若是则返回True,反之返回False
#                    print(self.port_mes)
                    self.serial_port_state = self.port_mes.isBusy()
#                    print(self.serial_port_state)
                    if self.serial_port_state == True:  # 再增加一个判断串口是否占用,若已占用，说明已打开成功
                        self.PushButton_Open.setText("关闭串口")  # 串口打开成功后状态显示为打开状态，即关闭
                        self.PushButton_read.setEnabled(True)
                        self.PushButton_set.setEnabled(True)

                        self.timer = QTimer(self)
                        self.timer.timeout.connect(self.receive_data)
                        self.timer.start(10)
#                        self.pushButton_ture()  # 成功打开串口后，再使能相关按钮
#                        self.receive_data(1)  # 打开成功后接收使能打开
                        QtWidgets.QApplication.processEvents()
                except:
 #                   my_pyqt_wigth.show()
 #                   my_pyqt_wigth.serial_open_error_mage()
                    print("串口打开失败")
                    pass

        elif self.PushButton_Open.text() == '关闭串口':

            # time.sleep(0.2)
            # print(type(self.port))
            self.SerialPort.close()
            self.PushButton_Open.setText("打开串口")
            self.PushButton_set.setEnabled(False)
            self.PushButton_read.setEnabled(False)

    def get_port_list(self):
        """
        获取当前系统所有COM口
        :return:
        """
        com_list = []  # 用于保存端口名的列表
        port_list = serial.tools.list_ports.comports()  # 获取本机端口，返回list
        for port in port_list:
            com_list.append(port[0])  # 保存端口到列表
#        print(com_list)
        return com_list  # 返回列表

    def TxReadInfo(self):
        ReadStr = "___read()"
#        ReadStrList = []
#        ReadStrList.append(915)
#        ReadStrList.append(15)
#        ReadStr = ReadStr+str(ReadStrList)
        print(ReadStr)
        self.SerialPort.write(ReadStr.encode('gbk'))

    def TxWriteInfo(self):
        WriteStr = "___write"
        WriteStrList = []
        if(self.LineEdit_LoRa_Freq.text() == ''):
            Freq = '915'
        else:
            Freq = self.LineEdit_LoRa_Freq.text()
        WriteStrList.append(int(Freq))
        WriteStrList.append(message_bandWidth_dict[self.ComboBox_BandWidth.currentText()])
        WriteStrList.append(message_sprFactor_dict[self.ComboBox_SprFactor.currentText()])
        WriteStrList.append(message_codingRate_dict[self.ComboBox_CodingRate.currentText()])
        if (self.LineEdit_PowerCfig.text() == ''):
            Power = '15'
        else:
            Power = self.LineEdit_PowerCfig.text()
        WriteStrList.append(int(Power))
        WriteStrList.append(message_TrueOrFalse_dict[self.ComboBox_MaxPowerOn.currentText()])
        WriteStrList.append(message_TrueOrFalse_dict[self.ComboBox_CRCON.currentText()])
        WriteStrList.append(message_TrueOrFalse_dict[self.ComboBox_HeaderOn.currentText()])
        WriteStr += '('
        for tempstr in WriteStrList:
            WriteStr += str(tempstr)
            WriteStr += ','
        WriteStr = WriteStr[0:-1]
        WriteStr += ')'
        print(WriteStrList)
        print(WriteStr)

        self.SerialPort.write(str(WriteStr).encode('gbk'))

    def receive_data(self):
        self.port_mes = QSerialPortInfo(self.SerialPort.port)  # 判断串口状态，若是则返回True,反之返回False
        self.serial_port_state = self.port_mes.isBusy()
        if self.serial_port_state == True:  # 再增加一个判断串口是否占用,若已占用，说明已打开成功
            res_data = self.SerialPort.read_all()
            info = []
            if len(res_data) != 0:
                print(str(res_data))
                print(str(res_data).__contains__('___'))
                if str(res_data).__contains__('___') == False:
                    return
                if(res_data != b'___(Ok)' ):
                    for te in str(res_data).split(','):
                        if te.__contains__('('):
        #                    print((te.split('(')[1]))
                            conum = te.split('(')[1]
                            t = 0
                            for c in conum:
                                if ord(c) < ord('A'):
                                    t = t * 16 + int(c)
                                elif ord(c) < ord('a'):
                                    t = t * 16 + int(ord(c) - ord('A') + 10)
                                else:
                                    t = t * 16 + int(ord(c) - ord('a') + 10)
     #                       print(t)
                            info.append(t)
                        elif te.__contains__(')'):
        #                    print((te.split(')')[0]))
                            conum = te.split(')')[0]
                            t = 0
                            for c in conum:
                                if ord(c) < ord('A'):
                                    t = t * 16 + int(c)
                                elif ord(c) < ord('a'):
                                    t = t * 16 + int(ord(c) - ord('A') + 10)
                                else:
                                    t = t * 16 + int(ord(c) - ord('a') + 10)
                            info.append(t)
                        else:
        #                    print((te))
                            t = 0
                            for c in te:
                                if ord(c) < ord('A'):
                                    t = t * 16 + int(c)
                                elif ord(c) < ord('a'):
                                    t = t * 16 + int(ord(c) - ord('A') + 10)
                                else:
                                    t = t * 16 + int(ord(c) - ord('a') + 10)
                            info.append(t)
                    print(info)
                    self.LineEdit_LoRa_Freq.setText(str(info[0]))
                    index = 0
                    for band in message_bandWidth_dict:
                        if(int(message_bandWidth_dict[band]) == int(str(info[1]))):
                            if band != '':
                                self.ComboBox_BandWidth.setCurrentIndex(index)
                        index = index + 1
                    index = 0
                    for band in message_sprFactor_dict:
                        if (int(message_sprFactor_dict[band]) == int(str(info[2]))):
                            if band != '':
                                self.ComboBox_SprFactor.setCurrentIndex(index)
                        index = index + 1
                    index = 0
                    for band in message_codingRate_dict:
                        if (int(message_codingRate_dict[band]) == int(str(info[3]))):
                            if band != '':
                                self.ComboBox_CodingRate.setCurrentIndex(index)
                        index = index + 1
                    self.LineEdit_PowerCfig.setText(str(info[4]))
                    index = 0
                    for band in message_TrueOrFalse_dict:
                        if (int(message_TrueOrFalse_dict[band]) == int(str(info[5]))):
                            if band != '':
                                self.ComboBox_MaxPowerOn.setCurrentIndex(index)
                        index = index + 1
                    index = 0
                    for band in message_TrueOrFalse_dict:
                        if (int(message_TrueOrFalse_dict[band]) == int(str(info[6]))):
                            if band != '':
                                self.ComboBox_CRCON.setCurrentIndex(index)
                        index = index + 1
                    index = 0
                    for band in message_TrueOrFalse_dict:
                        if (int(message_TrueOrFalse_dict[band]) == int(str(info[7]))):
                            if band != '':
                                self.ComboBox_HeaderOn.setCurrentIndex(index)
                        index = index + 1
                else:
                    # 通过setModal(bool)方法设置模态
     #               window = QWidget()
                    qd = QDialog(MainWindow)
                    qd.resize(200, 100)
                    qd.setModal(True)

                    qd.Label = QtWidgets.QLabel(qd)
                    qd.Label.setGeometry(QtCore.QRect(40, 40, 100, 60))
                    qd.Label.setObjectName("Label")
                    qd.Label.setText("设置完成")
                    qd.Label.setFont(QFont("宋体", 12, QFont.Normal))
                    qd.Label.setAlignment(Qt.AlignRight)

                    qd.setWindowTitle("DE")
                    qd.show()

     #               window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())