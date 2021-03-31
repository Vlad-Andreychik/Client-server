import sys

from Client import clientclient

client = clientclient.Client()
client.connect_to_server()

connected = True
while connected:
    choice = input("""
    Choose an option:
    1 - Send message to server
    2 - Send Broadcast message
    3 - Disconnect
    4 - Take message from the server
    """)
    if choice == '1':
        client.send_message_to_server()
    if choice == '2':
        client.send_broadcast_message()
    if choice == '3':
        client.send_disconnect_message_to_server()
        print('You disconnected from the server')
        connected = False
    if choice == '4':
        msg = client.receive_message()
        print(msg.decode('utf-8'))

sys.exit()
