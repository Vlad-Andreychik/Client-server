"""Module of handler that communicates with client"""

import logging
import sys
import time
from enum import Enum

from clients import db_client

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class MessageCodes(Enum):
    """
    Class of codes that set rules for communication
    """
    CODE_LISTEN = '1'
    CODE_SUCCESS = '2'


class UserHandler:
    """
    Class of handler that communicates with user
    """

    def __init__(self, conn, address):
        """
        Constructor init takes 2 parameters and runs method run()
        :param conn: connection parameters
        :param address: address of client
        """
        self.conn = conn
        self.address = address
        self.run()

    def receive_message(self):
        """
        Method that receives message
        :return: received message
        """
        msg_length = self.conn.recv(64)
        if msg_length:
            msg_length = int(msg_length)
            return self.conn.recv(msg_length)

    def __send_message(self, message):
        """
        Private method for sending messages
        :param message: message
        """
        message = message.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        self.conn.send(send_length)
        time.sleep(0.1)
        self.conn.send(message)

    def send_service_message(self, message):
        """
        Method used for sending service messages
        :param message: code message
        """
        self.__send_message(message)

    def send_msg(self, message):
        """
        Method used for sending messages
        :param message: message
        """
        self.__send_message(message)

    def send_to(self, message, address):
        """
        Method used for sending messages to special user
        :param message: message
        :param address: address of user-receiver
        """
        message = message.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b'' * (64 - len(send_length))
        self.conn.sendto(send_length, address)
        time.sleep(0.1)
        self.conn.sendto(message, address)

    def registration(self, database):
        """
        Method that sets scenario for registration a new user on the server
        :param database: database that keeps logins and passwords
        """
        self.send_service_message(MessageCodes.CODE_LISTEN.value)
        self.send_msg("Please, enter your login ")
        login = self.receive_message().decode('utf-8')
        self.send_service_message(MessageCodes.CODE_LISTEN.value)
        self.send_msg("Please, enter your password")
        password = self.receive_message().decode('utf-8')
        find_login = database.select_where('*', 'login', login)
        if not find_login:
            database.insert(login, password)
            self.send_service_message(MessageCodes.CODE_SUCCESS.value)
            self.send_msg("SUCCESS")
            return True
        else:
            self.send_service_message(MessageCodes.CODE_LISTEN.value)
            self.send_msg("This login already exist. Try again")
            return False

    def authentication(self, database):
        """
        Method that sets scenario for authentication a existing user on the server
        :param database: database that keeps logins and passwords
        """
        self.send_service_message(MessageCodes.CODE_LISTEN.value)
        self.send_msg("Please, enter your login ")
        login = self.receive_message().decode('utf-8')
        self.send_service_message(MessageCodes.CODE_LISTEN.value)
        self.send_msg("Please, enter your password")
        password = self.receive_message().decode('utf-8')
        find_login = database.select_where('*', 'login', login)
        if find_login:
            if database.select_where('password', 'login', login)[0][0] == password:
                self.send_service_message(MessageCodes.CODE_SUCCESS.value)
                self.send_msg("SUCCESS")
                return True
            else:
                self.send_service_message(MessageCodes.CODE_LISTEN.value)
                self.send_msg("Wrong login or password. Try again")
                return False
        else:
            self.send_service_message(MessageCodes.CODE_LISTEN.value)
            self.send_msg("Wrong login or password. Try again")
            return False

    def run(self):
        """
        Method that runs communication between server and client
        """
        db = db_client.DB('../DB/userdata.db')
        logging.info(f"[NEW CONNECTION {time.strftime('%H:%M:%S', time.localtime())}] {self.address} try to connect.")
        connected = False
        while connected is False:
            self.send_service_message(MessageCodes.CODE_LISTEN.value)
            self.send_msg(
                "If you wanna sign in choose 1, if you wanna sign up choose 2, print !q for quit")
            msg = self.receive_message().decode('utf-8')
            # Sign in
            if msg == "1":
                connected = self.authentication(db)
            # Sign up
            elif msg == "2":
                connected = self.registration(db)
            elif msg == '!q':
                connected = False
                logging.info(f"[{self.address}] Disconnected")
            else:
                logging.info('Try again')

        # Connected
        while connected:
            code = self.receive_message()
            if code.decode('utf-8') == '!q':
                connected = False
                logging.info(f"[{self.address}] Disconnected")
            elif code.decode('utf-8') == '1':
                message = self.receive_message()
                logging.info(f"[{self.address}] {message.decode('utf-8')}")
        self.conn.close()
        db.disconnect()
