import logging
import socket
import sys
import time

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class User:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect_to_server(self):
        self.client.connect((self.host, self.port))

    def send_code_message_to_server(self, code):
        msg = code.encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        self.client.send(send_length)
        time.sleep(0.1)
        self.client.send(msg)

    def send_message_to_server(self):
        msg = input('Message ').encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        self.client.send(send_length)
        time.sleep(0.1)
        self.client.send(msg)

    def send_broadcast_message(self):
        msg = input('Message ').encode('utf-8')
        self.client.sendto(msg, ('<broadcast>', 9009))

    def receive_message(self):
        msg_length = self.client.recv(64)
        if msg_length:
            msg_length = int(msg_length)
            return self.client.recv(msg_length)

    def receive(self):
        return self.client.recv(64)

    def close_connection(self):
        self.client.close()


