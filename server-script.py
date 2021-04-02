import threading

from DB import dbclient
from Server import serverclient
from Server.serverclient import time_now

server = serverclient.Server()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION {time_now()}] {addr} try to connect.")
    db = dbclient.DB("DB/userdata.db")
    connected = False
    server.send_msg(conn, "If you wanna sign in choose 1, if you wanna sign up choose 2")
    msg = server.receive_msg(conn).decode('utf-8')

    # Sign in
    if msg == "1":
        while connected is False:
            server.send_msg(conn, "Please, enter your login ")
            login = server.receive_msg(conn).decode('utf-8')
            server.send_msg(conn, "Please, enter your password")
            password = server.receive_msg(conn).decode('utf-8')
            if db.exist_login(login):
                if db.select_for_sign_in(login) == password:
                    connected = True
                    server.send_msg(conn, "SUCCESS")
                else:
                    server.send_msg(conn, "Wrong login or password. Try again")

    # Sign up
    elif msg == "2":
        while connected is False:
            server.send_msg(conn, "Please, enter your login ")
            login = server.receive_msg(conn).decode('utf-8')
            server.send_msg(conn, "Please, enter your password")
            password = server.receive_msg(conn).decode('utf-8')
            if not db.exist_login(login):
                db.add_user(login, password)
                connected = True
                server.send_msg(conn, "SUCCESS")
            else:
                server.send_msg(conn, "This login already exist. Try again")

    # Connected
    while connected:
        code = server.receive_msg(conn).decode('utf-8')
        if code == '!q':
            connected = False
            print(f"[{addr}] Disconnected")
        elif code == '1':
            message = server.receive_msg(conn).decode('utf-8')
            print(f"[{addr}] {message}")

    conn.close()


def start():
    server.start_listen()
    while True:
        conn, addr = server.accept_connection()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS {time_now()}] {threading.activeCount() - 1}")


start()
