import socket


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = input('Enter your login ')

    def connect_to_server(self):
        self.client.connect(('localhost', 9009))

    def sign_in_to_server(self):
        pass

    def send_disconnect_message_to_server(self):
        self.client.send('!q'.encode('utf-8'))

    def send_message_to_server(self):
        message = input('Message ').encode('utf-8')
        self.client.send(message)
        return message

    def send_broadcast_message(self):
        message = input('Message ').encode('utf-8')
        self.client.sendto(message, ('<broadcast>', 9009))
        return message

    def receive_message(self):
        return self.client.recv(1024)

    def close_connection(self):
        self.client.close()
