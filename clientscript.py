import logging
from user import userclient
import sys
import time

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = userclient.User('localhost', 9009)
client.connect_to_server()
connected = True
while connected:
    code = client.receive_message()
    if code.decode('utf-8') == '!q':
        connected = False
        logging.info(f"Disconnected")
    elif code.decode('utf-8') == '1':
        message = client.receive_message()
        logging.info(f"{message.decode('utf-8')}")
        client.send_message_to_server()
    elif code.decode('utf-8') == '2':
        authorized = True
        msg = client.receive_message()
        logging.info(msg.decode('utf-8'))
        while authorized:
            choice = input("""
                    Choose an option:
                    1 - Send message to server
                    2 - Send Broadcast message
                    3 - Take message from the server
                    4 - Send message to specific user
                    !q - Disconnect
                    """)
            if choice == '1':
                client.send_code_message_to_server('1')
                client.send_message_to_server()
            elif choice == '2':
                client.send_code_message_to_server('2')
                user = client.receive_message()
                logging.info(user.decode('utf-8'))
                client.send_message_to_server()
            elif choice == '3':
                msg = client.receive()
                logging.info(msg.decode('utf-8'))
            elif choice == '4':
                client.send_code_message_to_server('4')
                user = client.receive_message()
                logging.info(user.decode('utf-8'))
                client.send_message_to_server()
                serv_response = client.receive_message()
                logging.info(serv_response.decode('utf-8'))
                client.send_message_to_server()
            elif choice == '!q':
                client.send_code_message_to_server('!q')
                logging.info('You disconnected from the server')
                client.close_connection()
                sys.exit()
            else:
                logging.info("Try again")
