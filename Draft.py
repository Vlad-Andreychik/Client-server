from Client import clientclient
from Server import serverclient
import threading

server = serverclient.Server()
while True:
    question = input("Do you want to quit?(y/n)")
    if question == 'y':
        break
    server.start_listen()
    client = clientclient.Client()
    client.connect_to_server()
    thread = threading.Thread(target=clientclient.Client)
    thread.start()
    msg = client.send_message_to_specific_user()
    conn, addr = server.accept_connection()
    server.receive_msg(conn)
    print(f"[{client.name}] {msg.decode('utf-8')}")
    server.send_msg(conn, "Msg received")

server.close_server()
