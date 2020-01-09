from socket import *
from threading import Thread
import sys
import os
import time


global user_list
user_list = list()

global cm


class ClientConnectionManagement:  # Class for Checking new connections
    def __init__(self, port):
        """
        Initializer method for ClientConnectionManagement
        @param string port : Port for server listening
        @return none
        """

        self.port = int(port)  # Instance variable for port
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # Setting sockets as SOL_SOCKET and SO_REUSEADDR would allow the port
        # 60000 to be used right after killing this process. If not used,
        # You should wait for the OS to kill that port which takes some time.

        try:
            self.server_sock.bind(('', int(port)))  # Start binding from here
            print("[Server] Listening on port " + str(self.port))

        except OSError:
            print("[ERROR] The port is already being used.")
            exit()

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
        """
        A method for checking disconnection by connection_socket_object
        If this connection socket object sends !!exit() which is for
        disconnection, the server removes the corresponding connection socket
        from user list.

        @param connection_socket_object : the connection socket object to check
        @return none
        """

        try:
            temp_receive_data = connection_socket_object.recv(1024)
            temp_receive_data = temp_receive_data.decode('utf-8')
            # Receives a data from the connected socket object.

            if temp_receive_data == "!!exit()":
                # If the received data is !!exit(), server removes that object
                print("[Server] " + str(connection_socket_object.getpeername())
                      + " disconnected")
                # connection_socket_object.getpeername() is the ip of the
                # connected device

                user_list.remove(connection_socket_object)
                # removes that connection socket object from list
                # connection_socket_object.close()
                # closes that socket connection from server

        except:
            # I do know that this is a really bad expression, however
            # there seems to be a lot of exceptions that can be made in the
            # try expression up above. So I have decided to ignore any
            # exceptions for this.
            pass

    def check_disconnection_thread(self):
        """
        A method for checking multiple disconnections at once by using
        multithreading. This method automatically scans all the connected
        sockets and checks if some object is disconnected

        @param none
        @return none
        """

        for connection_socket_object in user_list:
            # Repeats for all the instances in user_list
            Thread(target=self.check_disconnection,
                   args=(connection_socket_object,)).start()
            # When using Thread function, the args must be in args = (arg,)
            # format. Otherwise, it would not work at all.


def receive_console_commands():
    """
    A function for receiving console commands.
    Commands :
    - show_user_list : shows all connected users
    - stop : stops server

    @param none
    @return none
    """
    command_list = ['show_user_list', 'stop']
    command = ''
    command = input(command)

    if command not in command_list:
        print("[Server] Wrong command entered.")

    elif command == 'show_user_list':
        show_user_list()

    elif command == 'stop':
        stop_server()


def show_user_list():
    """
    A function for printing out all the user_list.
    Just used for development and would not be used in the future.

    @param none
    @return none
    """

    print("[Server] Total " + str(len(user_list)) + " connected users : ")

    for entry in user_list:
        print(entry.getpeername())


def stop_server():
    global cm
    """
    A function for stopping server PROPERLY.
    Closes the server socket and exits python

    @param none
    @return none
    """
    print("[Server] Stopping Server...")
    # cm.server_sock.shutdown(SHUT_RDWR)
    # cm.server_sock.close()
    print("[Server] Bye!")

    os._exit(0)
    # Using sys.exit does not work here because this function
    # would be called inside a thread. So using os._exit(0) would kill this


def thread_for_checking_connections():
    """
    A function which is a set of threads looping forever.
    This function declares a ClientConnectionManagement object and
    checks the connections. Automatically detects new connections and
    disconnections.

    @param none
    @return none
    """

    while True:
        Thread(target=cm.check_new_connection).start()  # New connections
        Thread(target=cm.check_disconnection_thread).start()  # Disconnection
        # Thread(target = show_user_list_loop).start()  # For testing
        time.sleep(1)
        # If this function does not have a delay, the socket program will
        # exceed its limits and too many requests would be handled. So this
        # script waits 1 second to avoid overflow in socket area.


if __name__ == "__main__":
    global cm
    cm = ClientConnectionManagement(60000)

    while True:
        try:
            Thread(target=thread_for_checking_connections).start()
            Thread(target=receive_console_commands).start()
            time.sleep(1)
        except OSError:
            pass
        # If this function does not have a delay, the socket program will
        # exceed its limits and too many requests would be handled. So this
        # script waits 1 second to avoid overflow in socket area.

    print(user_list)
