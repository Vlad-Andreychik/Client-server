import socket
import time
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', 9009))
        logging.info(f"[SERVER STARTED {time.strftime('%H:%M:%S', time.localtime())}]!")

    def start_listen(self):
        self.server.listen()
        logging.info(
            f"[LISTENING {time.strftime('%H:%M:%S', time.localtime())}] Server is listening on {socket.gethostname()}")

    @staticmethod
    def receive_msg(conn):
        msg_length = conn.recv(64)
        if msg_length:
            msg_length = int(msg_length)
            return conn.recv(msg_length)

    @staticmethod
    def send_service_msg(conn, msg):
        msg = msg.encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        conn.send(send_length)
        time.sleep(0.1)
        conn.send(msg)

    @staticmethod
    def send_msg(conn, msg):
        msg = msg.encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        conn.send(send_length)
        time.sleep(0.1)
        conn.send(msg)

    @staticmethod
    def send_to(conn, msg, sock):
        msg = msg.encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        conn.sendto(send_length, sock)
        time.sleep(0.1)
        conn.sendto(msg, sock)

    def accept_connection(self):
        return self.server.accept()

    def close_server(self):
        self.server.close()
