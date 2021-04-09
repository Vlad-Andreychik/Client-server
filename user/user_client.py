"""Module of user that provides connecting to the server"""

import logging
import socket
import sys
import time

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class User:
    """
    Class of user that provided initialization of user and his communication with server
    """

    def __init__(self, host, port):
        """
        Constructor init takes 2 parameters
        :param host: its defines a server you would to connect
        :param port: its defines a port you would to use
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect_to_server(self):
        """
        Method for connecting to the server
        """
        self.client.connect((self.host, self.port))

    def send_code_message_to_server(self, code):
        """
        Method used for code service messages
        :param code: code number
        """
        message = code.encode('utf-8')
        message_length = len(message)
        send_length = str(message_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        self.client.send(send_length)
        time.sleep(0.1)
        self.client.send(message)

    def send_message_to_server(self):
        """
        Method used for sending messages to server
        """
        message = input('Message ')
        self.send_code_message_to_server(message)

    def receive_message(self):
        """
        Method that receives message
        :return: received message
        """
        msg_length = self.client.recv(64)
        if msg_length:
            msg_length = int(msg_length)
            return self.client.recv(msg_length)

    def close_connection(self):
        """
        Method that closes connection with a server
        """
        self.client.close()


if __name__ == '__main__':
    user = User('localhost', 9009)
    user.connect_to_server()
    connected = True
    while connected:
        code_from_server = user.receive_message()
        if code_from_server.decode('utf-8') == '!q':
            connected = False
            logging.info(f"Disconnected")
        elif code_from_server.decode('utf-8') == '1':
            message_from_server = user.receive_message()
            logging.info(f"{message_from_server.decode('utf-8')}")
            user.send_message_to_server()
        elif code_from_server.decode('utf-8') == '2':
            authorized = True
            message_from_server = user.receive_message()
            logging.info(message_from_server.decode('utf-8'))
            while authorized:
                choice = input("""
                        Choose an option:
                        1 - Send message to server
                        !q - Disconnect
                        """)
                if choice == '1':
                    user.send_code_message_to_server('1')
                    user.send_message_to_server()
                elif choice == '!q':
                    user.send_code_message_to_server('!q')
                    logging.info('You disconnected from the server')
                    user.close_connection()
                    sys.exit()
                else:
                    logging.info("Try again")
