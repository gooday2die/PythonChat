from socket import *

global user_list
user_list = list()

class ClientConnectionTest:  # Class for Checking new connections from client
    def __init__(self, port):
        """
        Initializer method for ClientConnectionTest
        @param string port : Port for server listening
        @return none
        """

        self.port = int(port)  # Instance variable for port
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(('', int(port)))  # Start binding from here

    def get_new_connection(self):
        """
        A method for getting new connections
        When a new connection is set, server sends 200
        If server gets 300 in return, it saves the socket object
        into the user list for future use.

        @param none
        @return none
        """

        print("[Server] Listening on port " + str(self.port))

        self.server_sock.listen(1)
        self.connection_sock, self.addr = self.server_sock.accept()

        print("[Server] IP " + str(self.addr)+ " connected!")

        self.connection_sock.send("200".encode('utf-8'))
        #  Send 200 for new conneciton establishment
        self.connection_sock.settimeout(5)  # Max timeout second is 5 second

        temp_receive_data = self.connection_sock.recv(1024).decode("utf-8")
        #  Receives data for new connection establishment

        if temp_receive_data == '300':  # If received 300 which is OK
            print("[Server] IP " + str(self.addr) + " added to User List")
            user_list.append(self.connection_sock)  # Appends connectionSock to lst

        else:  # If 300 not received which is ERROR
            print("[Server] IP " + str(self.addr) + " was not added to User List")


if __name__ == "__main__":
    CT1 = ClientConnectionTest(60000)
    CT1.get_new_connection()
    CT1.get_new_connection()

    print(user_list)

    user_list[0].send("hello world!".encode("utf-8"))
