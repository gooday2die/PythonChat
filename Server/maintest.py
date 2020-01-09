from socket import *
from threading import Thread
import time


global user_list
user_list = list()


class ClientConnectionManagement:  # Class for Checking new connections
    def __init__(self, port):
        """
        Initializer method for ClientConnectionManagement
        @param string port : Port for server listening
        @return none
        """

        self.port = int(port)  # Instance variable for port
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(('', int(port)))  # Start binding from here
        print("[Server] Listening on port " + str(self.port))

    def check_new_connection(self):
        """
        A method for getting new connections
        When a new connection is set, server sends 200
        If server gets 300 in return, it saves the socket object
        into the user list for future use.

        @param none
        @return none
        """

        self.server_sock.listen(1)
        self.connection_sock, self.addr = self.server_sock.accept()

        print("[Server] IP " + str(self.addr) + " connected!")

        self.connection_sock.send("200".encode('utf-8'))
        #  Send 200 for new conneciton establishment
        self.connection_sock.settimeout(5)  # Max timeout second is 5 second

        temp_receive_data = self.connection_sock.recv(1024).decode("utf-8")
        #  Receives data for new connection establishment

        if temp_receive_data == '300':  # If received 300 which is OK
            print("[Server] IP " + str(self.connection_sock.getpeername()) +
                  " added to User List")
            user_list.append(self.connection_sock)

        else:  # If 300 not received which is ERROR
            print("[Server] IP " + str(self.addr) + " was not added to User")

    def check_disconnection(self, connection_socket_object):
        temp_receive_data = connection_socket_object.recv(1024)
        temp_receive_data = temp_receive_data.decode('utf-8')

        if temp_receive_data == "!!exit()":
            print("[Server] " + str(connection_socket_object.getpeername()) +
                  " disconnected")

            user_list.remove(connection_socket_object)
            connection_socket_object.close()

    def check_disconnection_thread(self):
        for connection_socket_object in user_list:
            Thread(target = self.check_disconnection,
                   args = (connection_socket_object,)).start()


def print_user_list_loop():
    print(user_list)


def thread_for_checking_connections():
    cm = ClientConnectionManagement(60000)

    while True:
        # Thread(target = check_new_connection_loop, args = (cm,)).start()
        Thread(target = cm.check_new_connection).start()
        Thread(target = cm.check_disconnection_thread).start()
        # Thread(target = print_user_list_loop).start()
        time.sleep(1)


if __name__ == "__main__":


    """
    cm = ClientConnectionManagement(60000)

    while True:
        Thread(target = check_new_connection_loop, args = (cm,)).start()
        Thread(target = print_user_list_loop).start()
        time.sleep(1)
    """
    '''
    CT1 = ClientConnectionManagement(60000)
    CT1.check_new_connection()
    CT1.check_new_connection()
    '''
    thread_for_checking_connections()

    print(user_list)

    # user_list[0].send("hello world!".encode("utf-8"))
