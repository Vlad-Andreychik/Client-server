import socket
import time

time_string = ("%H:%M:%S")


def time_now():
    return time.strftime(time_string, time.localtime())


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', 9009))
        print(f'[SERVER STARTED {time_now()}]!')

    def start_listen(self):
        self.server.listen()
        print(f"[LISTENING {time_now()}] Server is listening on {socket.gethostname()}")

    @staticmethod
    def receive_msg(conn):
        return conn.recv(64)

    @staticmethod
    def send_msg(conn, msg):
        return conn.send(msg.encode('utf-8'))

    @staticmethod
    def send_service_msg(conn, msg):
        conn.send(msg.encode('utf-8'))

    def accept_connection(self):
        return self.server.accept()

    def close_server(self):
        self.server.close()

    def register_new_user(self):
        pass

    def authenticate_user(self):
        pass
