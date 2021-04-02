import sys

from Client import clientclient


def client_on_server(connection=True):
    while connection:
        choice = input("""
        Choose an option:
        1 - Send message to server
        2 - Send Broadcast message
        3 - Take message from the server
        4 - Disconnect
        """)
        if choice == '1':
            client.send_code_message_to_server()
            client.send_message_to_server()
        elif choice == '2':
            client.send_broadcast_message()
        elif choice == '3':
            msg = client.receive_message()
            print(msg.decode('utf-8'))
        elif choice == '4':
            client.send_disconnect_message_to_server()
            print('You disconnected from the server')
            connection = False
        else:
            print("Try again")
    sys.exit()


client = clientclient.Client()
client.connect_to_server()
connected = False
client.print_receive_message()
msg = client.send_message_to_server()

# Sign in
if msg.decode('utf-8') == "1":
    while connected is False:
        client.print_receive_message()
        client.send_message_to_server()
        client.print_receive_message()
        client.send_message_to_server()
        answer = client.receive_message().decode('utf-8')
        if answer == "SUCCESS":
            print(answer)
            client_on_server()

# Sign up
if msg.decode('utf-8') == "2":
    while connected is False:
        client.receive_message()
        client.send_message_to_server()
        client.receive_message()
        client.send_message_to_server()
        answer = client.receive_message()
        print(answer)
        if answer == "SUCCESS":
            connected = True
            client_on_server()
