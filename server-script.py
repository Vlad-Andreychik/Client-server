from Server import serverclient
import threading
from Server.serverclient import time_now

server = serverclient.Server()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION {time_now()}] {addr} connected.")

    connected = True
    while connected:
        msg = server.receive_msg(conn).decode('utf-8')
        if msg == '!q':
            connected = False
            print(f"[{addr}] Disconnected")
        else:
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode('utf-8'))

    conn.close()


def start():
    server.start_listen()
    while True:
        conn, addr = server.accept_connection()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS {time_now()}] {threading.activeCount() - 1}")


start()
