import socket


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[NEW CLIENT]')

    def connect_to_server(self):
        self.client.connect(('localhost', 9009))
        print('[CONNECTING]')

    def sign_in_to_server(self):
        pass

    def send_message_to_specific_user(self, msg):
        message = msg.encode('utf-8')
        self.client.send(message)

    def send_broadcast_message(self):
        pass
