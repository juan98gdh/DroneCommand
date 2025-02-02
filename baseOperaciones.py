import socket
import time

Host = '127.0.0.1'
SendPort = 8888
RecvPort = 9876


class baseOperaciones(object):
    """docstring for baseOperaciones."""

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def __init__(self, arg):
    #     super(baseOperaciones, self).__init__()
    #     self.arg = arg

    def socket_listen(self, host, port):
        self.recv_socket.bind((host, port))
        self.recv_socket.listen()

        conn, addr = self.recv_socket.accept()

        print(f"Connected by {addr}")

        data = conn.recv(1024)
        if data:
            print(f"recieved {data}")
        else:
            pass
        conn.sendall(b'mundo')

        return conn

    def socket_send(self, host, port):
        self.send_socket.connect((host, port))
        self.send_socket.sendall(b'hola')
        data = self.send_socket.recv(1024)

        print(f'recieved data {data}')

    def reset_connection(self, conn):
        conn.close()


bo = baseOperaciones()
conn = bo.socket_listen(Host, RecvPort)

time.sleep(5)

bo.socket_send(Host, SendPort)

time.sleep(1)
print("hola")
bo.reset_connection(conn)
time.sleep(1)
bo.socket_listen(Host, RecvPort)
