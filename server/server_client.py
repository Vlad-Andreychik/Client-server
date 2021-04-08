"""Module of server that provides launching of server"""

import logging
import socket
import sys
import threading
import time

from clients import handler

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Server:
    """
    Class of server that is used for creating a server
    """

    def __init__(self, host, port):
        """
        Constructor init takes 2 parameters
        :param host: its defines a server hostname or host address
        :param port: its defines a port you would to use
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        logging.info(f"[SERVER STARTED {time.strftime('%H:%M:%S', time.localtime())}]!")

    def start_listen(self):
        """
        Method that starts listening on a server
        """
        self.server.listen()
        logging.info(
            f"[LISTENING {time.strftime('%H:%M:%S', time.localtime())}] Server is listening on {socket.gethostname()}")

    def accept_connection(self):
        """
        Method that accepts connections to server
        """
        return self.server.accept()

    def close_server(self):
        """
        Method that closes server
        """
        self.server.close()


if __name__ == '__main__':
    server = Server('', 9009)
    server.start_listen()
    while True:
        conn, address = server.accept_connection()
        thread = threading.Thread(target=handler.UserHandler, args=(conn, address))
        thread.start()
        logging.info(
            f"[ACTIVE CONNECTIONS {time.strftime('%H:%M:%S', time.localtime())}] {threading.activeCount() - 1}")
