import socket


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', 9009))
        print('[SERVER STARTED]!')

    def start_listen(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {socket.gethostname()}")

    @staticmethod
    def receive_msg(conn):
        conn.recv(1024)

    @staticmethod
    def send_msg(conn, msg):
        conn.send(msg.encode('utf-8'))

    def register_new_user(self):
        pass

    def authenticate_user(self):
        pass

    def accept_connection(self):
        # self.server.accept()
        return self.server.accept()

    def close_server(self):
        print()
        self.server.close()
