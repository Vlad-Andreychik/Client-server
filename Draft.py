from Client import clientclient
from Server import serverclient

server = serverclient.Server()
while True:
    question = input('Do you want to quit?(y/n)')
    if question == 'y':
        break
    server.start_listen()
    client = clientclient.Client()
    client.connect_to_server()
    msg = 'Hello'
    client.send_message_to_specific_user(msg)
    conn, addr = server.accept_connection()
    server.receive_msg(conn)
    print(f'[{addr}] {msg}')
    server.send_msg(conn, 'Msg received')

server.close_server()
