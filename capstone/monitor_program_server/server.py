import socket
from db import save_to_database
from _thread import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal, QThread
import sys

# 클라이언트 소켓 리스트 초기화
client_sockets = []

# 서버 호스트 및 포트 설정
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1234

# 클라이언트 쓰레드 클래스 정의
class ClientThread(QThread):
    # 수신 시그널 정의
    received = pyqtSignal(str)

    def __init__(self, client_socket, addr):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr

    def run(self):
        # 클라이언트 연결 출력
        print('>> Connected by:', self.addr[0], ':', self.addr[1])
        connected_message = '>> Connected by:'+ str(self.addr[0])+ ':'+ str(self.addr[1])
        save_to_database("Connected", " " , connected_message)

        while True:
            try:
                # 데이터 수신
                data = self.client_socket.recv(1024)

                if not data:
                    # 클라이언트 연결 종료
                    print('>> Disconnected by', self.addr[0], ':', self.addr[1])
                    break

                received_message = data.decode()
                # 수신된 메시지 출력
                print('>> Received from', self.addr[0], ':', self.addr[1], received_message)

                # 클라이언트 IP 주소를 이름으로 하는 파일에 수신된 메시지 저장
                with open(f"{self.addr[0]}.txt", "a", encoding='utf-8') as f:
                    f.write(received_message)

                # 수신된 데이터를 다른 클라이언트에게 전송
                for client in client_sockets:
                    if client != self.client_socket:
                        client.send(data)

                # 수신 시그널 발생
                self.received.emit(received_message)

            except ConnectionResetError as e:
                # 클라이언트 연결 종료
                print('>> Disconnected by', self.addr[0], ':', self.addr[1])
                break

        # 클라이언트 소켓 리스트에서 제거
        if self.client_socket in client_sockets:
            client_sockets.remove(self.client_socket)
            # 제거 후 남은 클라이언트 수 출력
            print('remove client list:', len(client_sockets))

        # 클라이언트 소켓 닫기
        self.client_socket.close()


# 로그 창 클래스 정의
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Log Server")
        self.setFixedSize(800, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_log(self, message):
        # 로그 창에 메시지 추가
        self.text_edit.append(message)


# 서버 쓰레드 클래스 정의
class Server(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        # 서버 시작 메시지 출력
        print('>> Server Start with IP:', HOST)

        # 서버 소켓 생성 및 설정
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            # 클라이언트 접속 대기
            print('>> Wait')

            # 클라이언트 연결 수락
            client_socket, addr = server_socket.accept()

            # 클라이언트 소켓 리스트에 추가
            client_sockets.append(client_socket)

            # 클라이언트 쓰레드 생성 및 실행
            client_thread = ClientThread(client_socket, addr)
            client_thread.received.connect(log_window.add_log)
            client_thread.start()

            # 접속한 클라이언트 수 출력
            print("접속 PC 수:", len(client_sockets))

        # 서버 소켓 닫기
        server_socket.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 로그 창 생성 및 표시
    log_window = LogWindow()
    log_window.show()

    # 서버 쓰레드 생성 및 실행
    server_thread = Server()
    server_thread.start()

    sys.exit(app.exec_())
