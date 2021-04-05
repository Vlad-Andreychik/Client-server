import threading
from DB import dbclient
from server import serverclient
import time
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

server = serverclient.Server()
clients = {}
clients_lock = threading.Lock()


class UserHandler(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def registration(self, db):
        server.send_service_msg(self.conn, '1')
        server.send_msg(self.conn, "Please, enter your login ")
        login = server.receive_msg(self.conn).decode('utf-8')
        server.send_service_msg(self.conn, '1')
        server.send_msg(self.conn, "Please, enter your password")
        password = server.receive_msg(self.conn).decode('utf-8')
        find_login = db.select_where('*', 'login', login)
        if not find_login:
            db.insert(login, password)
            server.send_service_msg(self.conn, '2')
            server.send_msg(self.conn, "SUCCESS")
            with clients_lock:
                clients[login] = self.addr
            return True
        else:
            server.send_service_msg(self.conn, '1')
            server.send_msg(self.conn, "This login already exist. Try again")
            return False

    def authentication(self, db):
        server.send_service_msg(self.conn, '1')
        server.send_msg(self.conn, "Please, enter your login ")
        login = server.receive_msg(self.conn).decode('utf-8')
        server.send_service_msg(self.conn, '1')
        server.send_msg(self.conn, "Please, enter your password")
        password = server.receive_msg(self.conn).decode('utf-8')
        find_login = db.select_where('*', 'login', login)
        if find_login:
            if db.select_where('password', 'login', login)[0][0] == password:
                server.send_service_msg(self.conn, '2')
                server.send_msg(self.conn, "SUCCESS")
                with clients_lock:
                    clients[login] = self.addr
                return True
            else:
                server.send_service_msg(self.conn, '1')
                server.send_msg(self.conn, "Wrong login or password. Try again")
                return False
        else:
            server.send_service_msg(self.conn, '1')
            server.send_msg(self.conn, "Wrong login or password. Try again")
            return False

    def run(self):
        db = dbclient.DB('DB/userdata.db')
        logging.info(f"[NEW CONNECTION {time.strftime('%H:%M:%S', time.localtime())}] {self.addr} try to connect.")
        connected = False
        while connected is False:
            server.send_service_msg(self.conn, '1')
            server.send_msg(self.conn,
                            "If you wanna sign in choose 1, if you wanna sign up choose 2, print !q for quit")
            msg = server.receive_msg(self.conn).decode('utf-8')
            # Sign in
            if msg == "1":
                connected = self.authentication(db)
            # Sign up
            elif msg == "2":
                connected = self.registration(db)
            elif msg == '!q':
                connected = False
                logging.info(f"[{self.addr}] Disconnected")
            else:
                logging.info('Try again')

        # Connected
        while connected:
            code = server.receive_msg(self.conn)
            if code.decode('utf-8') == '!q':
                connected = False
                logging.info(f"[{self.addr}] Disconnected")
            elif code.decode('utf-8') == '1':
                message = server.receive_msg(self.conn)
                logging.info(f"[{self.addr}] {message.decode('utf-8')}")
            elif code.decode('utf-8') == '2':
                server.send_msg(self.conn, 'Please, type your message')
                msg_for_all = server.receive_msg(self.conn)
                for client in clients.values():
                    server.send_to(self.conn, msg_for_all, client)
            elif code.decode('utf-8') == '4':
                server.send_msg(self.conn, 'Please, specify user you want to send mail.')
                user = server.receive_msg(self.conn).decode('utf-8')
                socket_of_user = clients[user]
                server.send_msg(self.conn, 'Please, type your message')
                msg_for_user = server.receive_msg(self.conn)
                server.send_to(self.conn, msg_for_user, socket_of_user)
        self.conn.close()
        db.disconnect()


def start():
    server.start_listen()
    while True:
        conn, addr = server.accept_connection()
        thread = UserHandler(conn, addr)
        thread.start()
        logging.info(
            f"[ACTIVE CONNECTIONS {time.strftime('%H:%M:%S', time.localtime())}] {threading.activeCount() - 1}")


start()
