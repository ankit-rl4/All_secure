import sys
import socket
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from ui_main import Ui_MainWindow
from cryptography.fernet import Fernet
import encrypt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag = None
        self.start_c = clientThread()
        self.start_s = serverThread()
        self.main_wind = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_wind)
        self.main_wind.setWindowTitle("Message Secure")
        self.main_wind.setWindowIcon(QIcon("logo.png"))
        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser_3.setReadOnly(True)
        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
        self.ui.button_encrypt.clicked.connect(self.gotoEn)
        self.ui.button_decryptor.clicked.connect(self.gotoDe)
        self.ui.button_en_msg.clicked.connect(self.en_msg)
        self.ui.pushButton.clicked.connect(self.de_msg)
        self.ui.home_button.clicked.connect(self.gotohome)
        self.ui.start_server_button.clicked.connect(self.gotoserver)
        self.ui.connect_ip_button.clicked.connect(self.gotoclient)
        self.ui.send_button.clicked.connect(self.send_msg)
        self.key = b'gHR_dOruS_1ntL3GsUmv_FMSRgliYJ5zmGSWo0qi5bA='
        self.fernet = Fernet(self.key)
        self.ui.pushButton_3.clicked.connect(self.closeit)
        self.ui.textBrowser.setAcceptRichText(True)
        self.ui.textBrowser_3.setAcceptRichText(True)
        self.ui.lineEdit.setValidator(QIntValidator())
        self.ui.plainTextEdit.setReadOnly(True)

    def show(self):
        self.main_wind.show()
        self.recieve_msg()

    def gotoEn(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.EncryptorWindow)

    def gotohome(self):
        if self.flag == None:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Chat_page)

    def gotoDe(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.DecryptorWindow)

    def gotoserver(self):
        self.flag = 0
        self.ui.stackedWidget.setCurrentWidget(self.ui.Chat_page)
        self.ui.con_to_label.setText("IP- 127.0.0.1.11111")
        self.start_s.start()

    def send_msg(self):
        self.msg = self.ui.msg_box.toPlainText()
        self.ui.msg_box.setPlainText("")
        if self.msg == ' ' or self.msg == '':
            pass
        else:
            self.ui.plainTextEdit.appendPlainText(f"You : {self.msg}")
            if self.flag == 0:
                self.start_s.sendMsg(self.msg)
            else:
                self.start_c.sendMsg(self.msg)

    def gotoclient(self):
        self.flag = 1
        self.ui.stackedWidget.setCurrentWidget(self.ui.Chat_page)
        self.ui.con_to_label.setText("connected to :-127.0.0.1.11111")
        self.ip = self.ui.ip_input.text()
        self.port = self.ui.port_input.text()
        self.start_c.getipPort(self.ip, self.port)
        self.start_c.start()

    def recieve_msg(self):
        try:
            self.start_s.any_s.connect(self.appendmsg)
            self.start_c.any_signal.connect(self.appendmsg)
        except:
            pass

    def appendmsg(self, string):
        self.ui.plainTextEdit.appendPlainText(f"Connection : {string}")

    def closeit(self):
        if self.flag == 0:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
            self.start_s.close_con()
            self.start_s.stop()


        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
            self.start_c.close_con()
            self.start_c.stop()
        self.flag == None

    def en_msg(self):
        self.ui.textBrowser.clear()
        self.ui.Access_code.setText("")
        self.enm = self.ui.En_Input_msg.toPlainText()
        self.ui.En_Input_msg.setText("")
        self.enmd = encrypt.encrypt_text(self.enm)
        self.ui.textBrowser.append(self.enmd[0])
        self.ui.Access_code.setText(self.enmd[1])

    def de_msg(self):
        self.dem = self.ui.textEdit.toPlainText()
        self.accode = self.ui.lineEdit.text()
        self.ui.textBrowser_3.clear()
        self.ui.textEdit.setText("")
        self.ui.lineEdit.setText("")
        self.accode = encrypt.numtolist(self.accode)
        self.msg_de = encrypt.decrypt_text(self.dem, self.accode)
        print(self.msg_de)
        self.ui.textBrowser_3.append(self.msg_de)


class serverThread(QtCore.QThread):
    any_s = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.port = 11111
        self.ip = "127.0.0.1"
        self.con = ''
        self.key = b'gHR_dOruS_1ntL3GsUmv_FMSRgliYJ5zmGSWo0qi5bA='
        self.fernet = Fernet(self.key)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, conn):
        try:
            while True:
                received = conn.recv(1024)
                if received == ' ':
                    pass
                else:
                    received = self.fernet.decrypt(received)
                    print(received.decode())
                    self.any_s.emit(received.decode())
        except:
            pass

    def sendMsg(self, msg):
        send_msg = msg.replace('b', '').encode()
        if send_msg == ' ':
            pass
        else:
            encMessage = self.fernet.encrypt(send_msg)
            self.con.sendall(encMessage)

    def close_con(self):
        self.s.close()

    def run(self):

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 11111))
        self.s.listen(1)
        (self.con, addr) = self.s.accept()
        self.connect(self.con)


class clientThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.ip, self.port = None, None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.key = b'gHR_dOruS_1ntL3GsUmv_FMSRgliYJ5zmGSWo0qi5bA='
        self.fernet = Fernet(self.key)

    def getipPort(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            while True:
                r_msg = self.s.recv(1024)
                if not r_msg:
                    break
                if r_msg == '':
                    pass
                else:
                    r_msg = self.fernet.decrypt(r_msg)
                    print(r_msg.decode())
                    self.any_signal.emit(r_msg.decode())
        except:
            pass

    def sendMsg(self, msg):
        send_msg = msg.replace('b', '').encode()
        if send_msg == ' ' or send_msg == '':
            pass
        else:
            encMessage = self.fernet.encrypt(send_msg)
            self.s.sendall(encMessage)

    def close_con(self):
        self.s.close()

    def run(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = int(self.port)
        self.s.connect((self.ip, port))
        self.connect()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
